#!/usr/bin/env python3
"""
Rogue Guardian Studios — Spot Status Line Script

Companion script to the heartbeat process.
Runs inside each agent session via the Claude Code status line mechanism.

Receives JSON after each assistant message containing context window data.
Writes context percentage atomically to context-metrics.json.
Checks for rotation trigger flags in the Spot state file.
Signals the current session when Spot needs to run.

This script is the bridge between the heartbeat (which runs outside
sessions) and the agents (which run inside sessions).
"""

import json
import os
import sys
import tempfile
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

DEFAULT_WATCHDOG_DIR = "state/watchdog/"
DEFAULT_METRICS_FILE = "state/watchdog/context-metrics.json"


def get_config():
    """Get configuration from environment or defaults."""
    return {
        "watchdog_state_dir": os.environ.get("WATCHDOG_STATE_DIR", DEFAULT_WATCHDOG_DIR),
        "context_metrics_file": os.environ.get("CONTEXT_METRICS_FILE", DEFAULT_METRICS_FILE),
        "agent_name": os.environ.get("AGENT_NAME", "unknown"),
    }


# ---------------------------------------------------------------------------
# Context metrics writing (atomic)
# ---------------------------------------------------------------------------

def write_context_metric(metrics_path, agent_name, used_percentage):
    """
    Write the current context percentage for this agent to
    context-metrics.json. Uses atomic write (write-to-temp
    then rename) to prevent race conditions with the heartbeat.
    """
    # Read existing metrics
    metrics = {}
    if os.path.exists(metrics_path):
        try:
            with open(metrics_path, "r") as f:
                metrics = json.load(f)
        except (json.JSONDecodeError, OSError):
            metrics = {}

    # Update this agent's entry
    metrics[agent_name] = used_percentage

    # Atomic write: write to temp file in same directory, then rename
    metrics_dir = os.path.dirname(metrics_path) or "."
    os.makedirs(metrics_dir, exist_ok=True)

    fd, tmp_path = tempfile.mkstemp(dir=metrics_dir, suffix=".tmp")
    try:
        with os.fdopen(fd, "w") as tmp_file:
            json.dump(metrics, tmp_file, indent=2)
        os.rename(tmp_path, metrics_path)
    except (OSError, IOError):
        # Clean up temp file on failure
        if os.path.exists(tmp_path):
            os.unlink(tmp_path)
        raise


# ---------------------------------------------------------------------------
# Rotation trigger detection
# ---------------------------------------------------------------------------

def check_rotation_trigger(watchdog_dir, agent_name):
    """
    Check the Spot state file for this agent for a rotation trigger flag.

    Returns:
        dict with trigger details if a trigger is pending, None otherwise.
    """
    spot_file = os.path.join(watchdog_dir, f"spot-{agent_name}.md")

    if not os.path.exists(spot_file):
        return None

    try:
        with open(spot_file, "r") as f:
            content = f.read()
    except (OSError, IOError):
        return None

    if "trigger: rotation" not in content:
        return None

    # Parse trigger details
    trigger = {"type": "rotation"}

    for line in content.split("\n"):
        line = line.strip()
        if line.startswith("reason:"):
            trigger["reason"] = line.split(":", 1)[1].strip()
        elif line.startswith("timestamp:") and "trigger" not in line:
            trigger["timestamp"] = line.split(":", 1)[1].strip()
        elif line.startswith("agent_context_at_trigger:"):
            trigger["agent_context"] = line.split(":", 1)[1].strip()

    return trigger


# ---------------------------------------------------------------------------
# Signal output
# ---------------------------------------------------------------------------

def signal_rotation_needed(trigger):
    """
    Signal the current session that Spot needs to run a rotation.
    Outputs a structured signal to stdout that the session can detect.
    """
    signal = {
        "spot_signal": "rotation_required",
        "trigger": trigger,
    }
    print(json.dumps(signal))


# ---------------------------------------------------------------------------
# Main — processes a single status line invocation
# ---------------------------------------------------------------------------

def process_status_line(status_json):
    """
    Process a single status line JSON payload from Claude Code.

    Expected input format:
    {
        "context_window": {
            "used_percentage": 23.5,
            "remaining_percentage": 76.5,
            "total_input_tokens": 47000,
            "context_window_size": 200000
        }
    }
    """
    config = get_config()

    # Extract context data
    try:
        context_window = status_json.get("context_window", {})
        used_percentage = context_window.get("used_percentage", 0)
    except (AttributeError, TypeError):
        return

    # Write context metric atomically
    write_context_metric(
        config["context_metrics_file"],
        config["agent_name"],
        used_percentage,
    )

    # Check for rotation trigger
    trigger = check_rotation_trigger(
        config["watchdog_state_dir"],
        config["agent_name"],
    )

    if trigger:
        signal_rotation_needed(trigger)


def main():
    """
    Entry point. Reads JSON from stdin (piped by Claude Code
    status line mechanism) and processes it.
    """
    try:
        raw = sys.stdin.read()
        if not raw.strip():
            return

        status_json = json.loads(raw)
        process_status_line(status_json)
    except json.JSONDecodeError:
        # Silently ignore malformed input — the status line
        # mechanism may send partial data
        pass
    except KeyboardInterrupt:
        pass


if __name__ == "__main__":
    main()
