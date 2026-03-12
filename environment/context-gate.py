#!/usr/bin/env python3
"""
PreToolUse hook — Context Gate

Pure infrastructure. No reasoning. No decisions beyond
threshold comparison and flag checks.

Reads context metrics and Spot state files.
Approves or blocks tool use based on:
  1. HALT flag presence
  2. Rotation trigger presence
  3. Context threshold breach

Runs before every tool call. Must be fast.
"""

import json
import os
import re
import sys
from pathlib import Path


WATCHDOG_DIR = Path("state/watchdog")
METRICS_FILE = WATCHDOG_DIR / "context-metrics.json"


def approve():
    json.dump({"decision": "approve"}, sys.stdout)
    sys.stdout.flush()


def block(reason):
    json.dump({"decision": "block", "reason": reason}, sys.stdout)
    sys.stdout.flush()


def read_json_safe(path):
    """Read a JSON file. Return empty dict on any failure."""
    try:
        with open(path, "r") as f:
            return json.load(f)
    except (OSError, json.JSONDecodeError, ValueError):
        return {}


def find_spot_file(session_id):
    """Find the Spot state file for this session's agent.

    Spot state files are named spot-[agent-name].md.
    The context-metrics.json maps session IDs to agent names.
    """
    if not WATCHDOG_DIR.is_dir():
        return None

    metrics = read_json_safe(METRICS_FILE)
    session_data = metrics.get(session_id, {})
    agent_name = session_data.get("agent_name")

    if not agent_name:
        return None

    spot_file = WATCHDOG_DIR / f"spot-{agent_name}.md"
    if spot_file.is_file():
        return spot_file
    return None


def has_halt_flag(spot_file):
    """Check if the Spot state file contains a HALT flag."""
    try:
        content = spot_file.read_text()
        return bool(re.search(r"^halt:\s*true", content, re.MULTILINE))
    except OSError:
        return False


def has_rotation_trigger(spot_file):
    """Check if the Spot state file contains a rotation trigger."""
    try:
        content = spot_file.read_text()
        return bool(re.search(r"^trigger:\s*rotation", content, re.MULTILINE))
    except OSError:
        return False


def read_spot_config(spot_file):
    """Read rotation config from the Spot state file.

    Extracts key-value pairs from the session configuration
    section of the state file.
    """
    config = {
        "agent_context_at_last_rotation": 0,
        "rotation_threshold_percent": 10,
    }
    try:
        content = spot_file.read_text()
        match = re.search(
            r"agent_context_at_last_rotation:\s*(\d+(?:\.\d+)?)", content
        )
        if match:
            config["agent_context_at_last_rotation"] = float(match.group(1))
        match = re.search(
            r"rotation_threshold_percent:\s*(\d+(?:\.\d+)?)", content
        )
        if match:
            config["rotation_threshold_percent"] = float(match.group(1))
    except OSError:
        pass
    return config


def write_rotation_trigger(spot_file, agent_context, reason):
    """Append a rotation trigger to the Spot state file.

    This is the only write the context gate performs.
    Spot reads it on next wake and executes the rotation.
    """
    import datetime

    trigger_block = (
        f"\n---\n"
        f"trigger: rotation\n"
        f"reason: {reason}\n"
        f"timestamp: {datetime.datetime.now(datetime.timezone.utc).isoformat()}\n"
        f"agent_context_at_trigger: {agent_context}\n"
    )
    try:
        with open(spot_file, "a") as f:
            f.write(trigger_block)
    except OSError:
        pass


def main():
    try:
        input_data = json.load(sys.stdin)
    except (json.JSONDecodeError, ValueError):
        approve()
        return

    session_id = input_data.get("session_id", "unknown")

    # Fast path: no watchdog directory means no monitoring
    if not WATCHDOG_DIR.is_dir():
        approve()
        return

    # Read context metrics for this session
    metrics = read_json_safe(METRICS_FILE)
    session_data = metrics.get(session_id, {})
    agent_context = session_data.get("used_percentage", 0)

    # Find this agent's Spot state file
    spot_file = find_spot_file(session_id)
    if not spot_file:
        approve()
        return

    # Check HALT flag — values breach under review
    if has_halt_flag(spot_file):
        block("HALT flag active — values breach under review by human")
        return

    # Check existing rotation trigger — rotation in progress
    if has_rotation_trigger(spot_file):
        block("Rotation trigger active — Spot rotation in progress")
        return

    # Check context threshold — should we trigger rotation?
    config = read_spot_config(spot_file)
    context_at_last_rotation = config["agent_context_at_last_rotation"]
    threshold = config["rotation_threshold_percent"]
    delta = agent_context - context_at_last_rotation

    if delta >= threshold:
        write_rotation_trigger(spot_file, agent_context, "context_threshold")
        block(
            f"Context threshold reached (delta: {delta:.1f}%, "
            f"threshold: {threshold:.1f}%) — triggering Spot rotation"
        )
        return

    approve()


if __name__ == "__main__":
    main()
