# Rogue Guardian Studios — Environment Rules
# Governs how environment scripts are set up,
# configured, and maintained.
# These files are owned by the studio owner.
# They are not evolvable through the normal
# agent improvement proposal process.
---

## Ownership

All files in environment/ are owned by the studio owner.
Agents do not modify, extend, or propose changes to
these files through the normal improvement proposal
process. Changes require direct studio owner action.

---

## Files

**spot-heartbeat.py**
The persistent background heartbeat process.
Runs outside agent sessions for the full duration
of a Claude Code session. Monitors context consumption
for all active Spot instances. Triggers rotation when
thresholds are reached. Detects orphaned state files.

**spot-status-line.py**
The status line companion script.
Runs inside each agent session. Reads Claude Code
status line JSON. Writes context percentage to
context-metrics.json atomically. Checks for rotation
trigger flags in Spot state files. Signals the session
when Spot needs to run.

**environment-rules.md**
This document.

---

## Launching the Heartbeat

The heartbeat is launched from a SessionStart hook
in the Claude Code settings:

```json
{
  "hooks": {
    "SessionStart": [
      {
        "command": "python3 environment/spot-heartbeat.py",
        "async": false
      }
    ]
  }
}
```

The heartbeat must start before any agent sessions begin.
It runs for the full session lifetime and terminates
when the session ends.

---

## Attaching the Status Line Script

The status line script is attached to each agent session
via the Claude Code status line mechanism. Each session
must set the AGENT_NAME environment variable so the
script can identify which agent's metrics to write:

```
AGENT_NAME=builder-core python3 environment/spot-status-line.py
```

The script reads JSON from stdin (piped by Claude Code)
and writes to the shared context-metrics.json file.

---

## Configuration

Configuration is passed to the heartbeat via:

1. A JSON config file (path set via HEARTBEAT_CONFIG env var)
2. Individual environment variable overrides:
   - HEARTBEAT_INTERVAL — cycle interval in seconds
   - WATCHDOG_STATE_DIR — path to watchdog state directory
   - CONTEXT_METRICS_FILE — path to shared metrics file

Defaults if no configuration is provided:
- Interval: 30 seconds
- Watchdog dir: state/watchdog/
- Metrics file: state/watchdog/context-metrics.json
- Check interval: 10%
- Checkpoint cap: 8

Per-agent overrides are set by the orchestrator at Spot
assignment and written to the Spot state file. The heartbeat
reads them from the state file when initialising tracking.

---

## Failure Handling

**If the heartbeat process crashes:**
No rotation triggers will fire. Spot instances continue
running but cannot be triggered by context thresholds.
The session must be restarted. There is no automatic
heartbeat recovery — a crashed heartbeat is a session-
level failure requiring human intervention.

**If the status line script fails:**
Context metrics for that agent session stop updating.
The heartbeat will see stale data for the affected agent.
Rotation triggers based on context threshold will not
fire for that agent. Checkpoint-cap-based triggers still
work because they are read directly from the state file.

**If context-metrics.json becomes corrupted:**
The heartbeat treats an unreadable metrics file as empty.
All context-based tracking resets to zero. This is safe
but conservative — it may delay rotation triggers until
the next status line write restores the file.

---

## Atomic Writes

The status line script writes to context-metrics.json
using atomic file operations: write to a temporary file
in the same directory, then rename. This prevents the
heartbeat from reading a partially-written file.

The heartbeat only reads this file. It never writes to it.

---

*Document version: 1.0*
*Created: 2026-03-05*
*Author: Studio Owner — Rogue Guardian Studios*
*Owned by: Studio owner — not subject to agent proposals*
