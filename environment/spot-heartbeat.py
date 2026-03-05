#!/usr/bin/env python3
"""
Rogue Guardian Studios — Spot Heartbeat Process

Persistent background script that monitors context consumption
for all active Spot instances and their watched agents.
Triggers rotation cycles when thresholds are reached.
Detects orphaned state files.

This is infrastructure — it does not reason or make decisions.
It measures, compares, and triggers. Everything requiring
judgment belongs to Spot or the orchestrator.

Launched via SessionStart hook in Claude Code.
"""

import json
import os
import re
import sys
import tempfile
import time
from datetime import datetime, timezone
from pathlib import Path

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

DEFAULT_CONFIG = {
    "heartbeat_interval_seconds": 30,
    "default_check_interval_percent": 10,
    "default_checkpoint_cap": 8,
    "watchdog_state_dir": "state/watchdog/",
    "context_metrics_file": "state/watchdog/context-metrics.json",
}


def load_config(config_path=None):
    """Load heartbeat configuration from file or use defaults."""
    config = dict(DEFAULT_CONFIG)
    if config_path and os.path.exists(config_path):
        with open(config_path, "r") as f:
            user_config = json.load(f)
            config.update(user_config)
    return config


# ---------------------------------------------------------------------------
# State file parsing
# ---------------------------------------------------------------------------

def parse_spot_state_file(filepath):
    """
    Read a spot-[agent-name].md state file and extract
    the fields the heartbeat needs for tracking.

    Returns a dict with:
      - checkpoint_count: int
      - checkpoint_cap: int
      - check_interval_percent: int
      - last_rotation_timestamp: str or None
      - generation_count: int
      - trigger_pending: bool (True if a rotation trigger is already written)
    """
    state = {
        "checkpoint_count": 0,
        "checkpoint_cap": DEFAULT_CONFIG["default_checkpoint_cap"],
        "check_interval_percent": DEFAULT_CONFIG["default_check_interval_percent"],
        "last_rotation_timestamp": None,
        "generation_count": 1,
        "trigger_pending": False,
    }

    try:
        with open(filepath, "r") as f:
            content = f.read()
    except (OSError, IOError):
        return state

    # Extract checkpoint cap from session configuration
    cap_match = re.search(r"Checkpoint cap:\s*(\d+)", content)
    if cap_match:
        state["checkpoint_cap"] = int(cap_match.group(1))

    # Extract check interval percentage
    interval_match = re.search(r"Check interval percentage:\s*(\d+)", content)
    if interval_match:
        state["check_interval_percent"] = int(interval_match.group(1))

    # Count checkpoint entries in checkpoint record
    checkpoint_matches = re.findall(r"Checkpoint (\d+)", content)
    if checkpoint_matches:
        state["checkpoint_count"] = len(checkpoint_matches)

    # Extract generation count
    gen_match = re.search(r"Current generation count:\s*(\d+)", content)
    if gen_match:
        state["generation_count"] = int(gen_match.group(1))

    # Extract last rotation timestamp
    rot_match = re.search(r"Last rotation timestamp:\s*(.+)", content)
    if rot_match:
        state["last_rotation_timestamp"] = rot_match.group(1).strip()

    # Check for pending trigger
    if "trigger: rotation" in content:
        state["trigger_pending"] = True

    return state


# ---------------------------------------------------------------------------
# Context metrics
# ---------------------------------------------------------------------------

def read_context_metrics(metrics_path):
    """
    Read context-metrics.json.
    Returns a dict keyed by agent name with context percentage values.
    """
    if not os.path.exists(metrics_path):
        return {}
    try:
        with open(metrics_path, "r") as f:
            return json.load(f)
    except (json.JSONDecodeError, OSError):
        return {}


# ---------------------------------------------------------------------------
# Tracking state
# ---------------------------------------------------------------------------

class SpotTracker:
    """Tracks a single Spot instance and its watched agent."""

    def __init__(self, agent_name, spot_file, config):
        self.agent_name = agent_name
        self.spot_file = spot_file
        self.config = config

        # Read initial state from the spot file
        spot_state = parse_spot_state_file(spot_file)

        self.spot_status = "paused"
        self.agent_status = "active"
        self.last_rotation_timestamp = spot_state["last_rotation_timestamp"] or datetime.now(timezone.utc).isoformat()
        self.agent_context_at_last_rotation = 0
        self.agent_context_current = 0
        self.spot_checkpoint_count = spot_state["checkpoint_count"]
        self.spot_checkpoint_cap = spot_state["checkpoint_cap"]
        self.check_interval_percent = spot_state["check_interval_percent"]
        self.rotation_threshold_percent = spot_state["check_interval_percent"]

    def to_dict(self):
        return {
            "agent_name": self.agent_name,
            "spot_file": self.spot_file,
            "spot_status": self.spot_status,
            "agent_status": self.agent_status,
            "last_rotation_timestamp": self.last_rotation_timestamp,
            "agent_context_at_last_rotation": self.agent_context_at_last_rotation,
            "agent_context_current": self.agent_context_current,
            "spot_checkpoint_count": self.spot_checkpoint_count,
            "spot_checkpoint_cap": self.spot_checkpoint_cap,
            "check_interval_percent": self.check_interval_percent,
            "rotation_threshold_percent": self.rotation_threshold_percent,
        }

    def update_from_state_file(self):
        """Re-read Spot state file to pick up post-rotation updates."""
        spot_state = parse_spot_state_file(self.spot_file)
        self.spot_checkpoint_count = spot_state["checkpoint_count"]
        self.spot_checkpoint_cap = spot_state["checkpoint_cap"]
        if spot_state["last_rotation_timestamp"]:
            self.last_rotation_timestamp = spot_state["last_rotation_timestamp"]
        if spot_state["trigger_pending"]:
            # Trigger already written and not yet consumed — skip re-triggering
            return True
        return False

    def check_rotation_needed(self, agent_context_current):
        """
        Check whether rotation should be triggered.
        Returns (needed: bool, reason: str or None).
        """
        self.agent_context_current = agent_context_current

        # Trigger 1 — Agent context threshold
        agent_delta = self.agent_context_current - self.agent_context_at_last_rotation
        if agent_delta >= self.rotation_threshold_percent:
            return True, "agent_threshold"

        # Trigger 2 — Spot checkpoint cap (fires one early for headroom)
        if self.spot_checkpoint_count >= (self.spot_checkpoint_cap - 1):
            return True, "checkpoint_cap"

        return False, None

    def reset_after_rotation(self):
        """Reset tracking values after a successful rotation."""
        self.agent_context_at_last_rotation = self.agent_context_current
        self.last_rotation_timestamp = datetime.now(timezone.utc).isoformat()
        self.spot_checkpoint_count = 0


# ---------------------------------------------------------------------------
# Rotation trigger writing
# ---------------------------------------------------------------------------

def write_rotation_trigger(spot_file, reason, agent_context):
    """
    Append a rotation trigger flag to the Spot state file.
    The status line script detects this on its next invocation.
    """
    trigger_block = (
        f"\n---\n"
        f"trigger: rotation\n"
        f"reason: {reason}\n"
        f"timestamp: {datetime.now(timezone.utc).isoformat()}\n"
        f"agent_context_at_trigger: {agent_context}\n"
    )
    try:
        with open(spot_file, "a") as f:
            f.write(trigger_block)
    except (OSError, IOError) as e:
        log(f"ERROR: Failed to write rotation trigger to {spot_file}: {e}")


# ---------------------------------------------------------------------------
# Orphaned state file detection
# ---------------------------------------------------------------------------

def detect_orphaned_files(watchdog_dir, active_trackers, known_issues_path):
    """
    Check for state files with no corresponding active tracker.
    An orphaned file means either Spot or the watched agent
    terminated unexpectedly.
    """
    if not os.path.isdir(watchdog_dir):
        return

    active_agents = {t.agent_name for t in active_trackers}

    for filename in os.listdir(watchdog_dir):
        match = re.match(r"spot-(.+)\.md$", filename)
        if not match:
            continue
        agent_name = match.group(1)
        if agent_name not in active_agents:
            filepath = os.path.join(watchdog_dir, filename)
            log(f"ORPHANED STATE FILE: {filepath} — no active tracker for agent '{agent_name}'")
            write_known_issue(known_issues_path, agent_name, filepath)


def write_known_issue(known_issues_path, agent_name, orphaned_file):
    """Write an orphaned file entry to state/known-issues.md."""
    entry = (
        f"\n---\n"
        f"## Orphaned State File Detected\n"
        f"- Agent: {agent_name}\n"
        f"- File: {orphaned_file}\n"
        f"- Detected: {datetime.now(timezone.utc).isoformat()}\n"
        f"- Action required: Orchestrator investigation before work continues\n"
    )
    os.makedirs(os.path.dirname(known_issues_path), exist_ok=True)
    try:
        with open(known_issues_path, "a") as f:
            f.write(entry)
    except (OSError, IOError) as e:
        log(f"ERROR: Failed to write known issue: {e}")


# ---------------------------------------------------------------------------
# Logging
# ---------------------------------------------------------------------------

def log(message):
    """Log a timestamped message to stderr."""
    timestamp = datetime.now(timezone.utc).isoformat()
    print(f"[heartbeat {timestamp}] {message}", file=sys.stderr)


# ---------------------------------------------------------------------------
# Discovery
# ---------------------------------------------------------------------------

def discover_spot_instances(watchdog_dir, config):
    """
    Scan the watchdog directory for spot-[agent-name].md files
    and create trackers for each.
    """
    trackers = []
    if not os.path.isdir(watchdog_dir):
        return trackers

    for filename in os.listdir(watchdog_dir):
        match = re.match(r"spot-(.+)\.md$", filename)
        if not match:
            continue
        agent_name = match.group(1)
        spot_file = os.path.join(watchdog_dir, filename)
        tracker = SpotTracker(agent_name, spot_file, config)
        trackers.append(tracker)
        log(f"Discovered Spot instance for agent: {agent_name}")

    return trackers


# ---------------------------------------------------------------------------
# Main heartbeat loop
# ---------------------------------------------------------------------------

def run_heartbeat(config):
    """Main heartbeat loop. Runs until the session ends."""

    watchdog_dir = config["watchdog_state_dir"]
    metrics_path = config["context_metrics_file"]
    interval = config["heartbeat_interval_seconds"]
    known_issues_path = os.path.join(
        os.path.dirname(watchdog_dir.rstrip("/")), "known-issues.md"
    )

    log("Heartbeat starting")
    log(f"Config: interval={interval}s, watchdog_dir={watchdog_dir}")

    trackers = []
    cycle_count = 0

    while True:
        cycle_count += 1

        # Discover new Spot instances on each cycle
        current_trackers = discover_spot_instances(watchdog_dir, config)
        known_agents = {t.agent_name for t in trackers}

        for ct in current_trackers:
            if ct.agent_name not in known_agents:
                trackers.append(ct)
                log(f"New Spot instance registered: {ct.agent_name}")

        # Remove trackers whose state files no longer exist
        trackers = [
            t for t in trackers
            if os.path.exists(t.spot_file)
        ]

        # Read context metrics
        metrics = read_context_metrics(metrics_path)

        # Process each tracker
        for tracker in trackers:
            # Update from state file
            trigger_pending = tracker.update_from_state_file()

            if trigger_pending:
                log(f"[{tracker.agent_name}] Rotation trigger already pending — skipping")
                continue

            # Get current agent context
            agent_context = metrics.get(tracker.agent_name, 0)

            # Check rotation
            needed, reason = tracker.check_rotation_needed(agent_context)

            if needed:
                log(f"[{tracker.agent_name}] Rotation triggered: {reason} "
                    f"(context={agent_context}%, checkpoints={tracker.spot_checkpoint_count}/"
                    f"{tracker.spot_checkpoint_cap})")
                write_rotation_trigger(tracker.spot_file, reason, agent_context)
            else:
                log(f"[{tracker.agent_name}] OK — context={agent_context}%, "
                    f"checkpoints={tracker.spot_checkpoint_count}/{tracker.spot_checkpoint_cap}")

        # Orphaned file detection
        detect_orphaned_files(watchdog_dir, trackers, known_issues_path)

        log(f"Cycle {cycle_count} complete — tracking {len(trackers)} instance(s)")

        time.sleep(interval)


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------

def main():
    config_path = os.environ.get("HEARTBEAT_CONFIG", None)
    config = load_config(config_path)

    # Allow environment variable overrides
    if "HEARTBEAT_INTERVAL" in os.environ:
        config["heartbeat_interval_seconds"] = int(os.environ["HEARTBEAT_INTERVAL"])
    if "WATCHDOG_STATE_DIR" in os.environ:
        config["watchdog_state_dir"] = os.environ["WATCHDOG_STATE_DIR"]
    if "CONTEXT_METRICS_FILE" in os.environ:
        config["context_metrics_file"] = os.environ["CONTEXT_METRICS_FILE"]

    try:
        run_heartbeat(config)
    except KeyboardInterrupt:
        log("Heartbeat stopped (KeyboardInterrupt)")
        sys.exit(0)


if __name__ == "__main__":
    main()
