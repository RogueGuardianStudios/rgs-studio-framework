#!/usr/bin/env python3
"""
StatusLine hook — Context Reporter

Pure infrastructure. No reasoning.
Receives Claude Code status JSON on stdin after each
assistant message. Extracts context window metrics
and writes them atomically to context-metrics.json.

This is the data source for context-gate.py.
"""

import json
import os
import sys
import tempfile
from pathlib import Path


WATCHDOG_DIR = Path("state/watchdog")
METRICS_FILE = WATCHDOG_DIR / "context-metrics.json"


def read_json_safe(path):
    """Read a JSON file. Return empty dict on any failure."""
    try:
        with open(path, "r") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError, ValueError):
        return {}


def write_json_atomic(path, data):
    """Write JSON atomically — write to temp file then rename.

    Prevents race conditions with context-gate.py reading
    a partially written file.
    """
    path.parent.mkdir(parents=True, exist_ok=True)
    fd, tmp_path = tempfile.mkstemp(
        dir=str(path.parent), suffix=".tmp", prefix=".metrics-"
    )
    try:
        with os.fdopen(fd, "w") as f:
            json.dump(data, f, indent=2)
            f.flush()
            os.fsync(f.fileno())
        os.rename(tmp_path, str(path))
    except OSError:
        try:
            os.unlink(tmp_path)
        except OSError:
            pass


def main():
    try:
        status = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        return

    session_id = status.get("session_id", "unknown")
    context_window = status.get("context_window", {})
    used_percentage = context_window.get("used_percentage")

    if used_percentage is None:
        return

    # Read existing metrics
    metrics = read_json_safe(METRICS_FILE)

    # Preserve existing agent_name mapping if present
    existing = metrics.get(session_id, {})
    agent_name = existing.get("agent_name", status.get("agent_name"))

    # Update this session's entry
    metrics[session_id] = {
        "used_percentage": used_percentage,
        "remaining_percentage": context_window.get("remaining_percentage"),
        "total_input_tokens": context_window.get("total_input_tokens"),
        "context_window_size": context_window.get("context_window_size"),
    }

    if agent_name:
        metrics[session_id]["agent_name"] = agent_name

    # Write atomically
    write_json_atomic(METRICS_FILE, metrics)


if __name__ == "__main__":
    main()
