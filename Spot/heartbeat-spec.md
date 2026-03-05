# heartbeat-spec.md
# Rogue Guardian Studios — Spot Heartbeat
# This document defines the heartbeat process.
# The heartbeat is not an agent. It does not reason.
# It is infrastructure — a persistent background script
# that runs independently of any agent session.
# It is the only component in the framework with
# continuous runtime across session boundaries.

---

## What the Heartbeat Is

The heartbeat is a background script that runs as
part of the Claude Code session environment.
It starts at session initialization and runs
until the session ends.

It has one job: monitor context consumption for
all active Spot instances and their watched agents,
and trigger rotation cycles when thresholds are reached.

It does not reason. It does not make decisions.
It measures, compares, and triggers. Everything
that requires judgment belongs to Spot or the
orchestrator. The heartbeat executes rules.

---

## What the Heartbeat Tracks

For each active Spot instance the heartbeat maintains:

```json
{
  "agent_name": "builder-core",
  "spot_file": "state/watchdog/spot-builder-core.md",
  "spot_status": "paused",
  "agent_status": "active",
  "last_rotation_timestamp": "2026-03-04T10:00:00",
  "agent_context_at_last_rotation": 0,
  "agent_context_current": 23,
  "spot_checkpoint_count": 2,
  "spot_checkpoint_cap": 8,
  "check_interval_percent": 10,
  "rotation_threshold_percent": 10
}
```

This state is held in memory during the session.
It is not written to disk — the state file is Spot's
responsibility, not the heartbeat's. The heartbeat
reads from the state file. It does not write to it.

---

## How the Heartbeat Gets Context Data

The heartbeat reads context consumption via the
Claude Code status line mechanism.

The status line script receives JSON after each
assistant message containing:
- context_window.used_percentage
- context_window.remaining_percentage
- context_window.total_input_tokens
- context_window.context_window_size

The status line script writes the current context
percentage for each active session to a shared
metrics file the heartbeat reads:

```
state/watchdog/context-metrics.json
```

The heartbeat reads this file on each cycle.
The status line script writes to it atomically
(write-to-temp then rename) to prevent race conditions.

---

## Heartbeat Cycle

The heartbeat runs on a fixed timer interval —
default 30 seconds, configurable per session.

Each cycle:

1. Read context-metrics.json for all active sessions
2. For each active Spot instance:
   a. Calculate agent context delta since last rotation
   b. Read current Spot checkpoint count from state file
   c. Check both against their thresholds
   d. If either threshold is reached — trigger rotation
   e. Check for orphaned state files — state file exists
      but no corresponding active session
   f. Log the cycle result

---

## Rotation Trigger Logic

```
agent_delta = agent_context_current - agent_context_at_last_rotation

if agent_delta >= rotation_threshold_percent:
    trigger rotation for this Spot instance

if spot_checkpoint_count >= (spot_checkpoint_cap - 1):
    trigger rotation for this Spot instance
```

The checkpoint cap check fires one checkpoint early —
at cap minus one — to ensure Spot has headroom to
complete the rotation cycle without hitting the cap
mid-compression.

Both conditions are checked every cycle.
Whichever fires first triggers rotation.
After rotation both values reset.

---

## Triggering Rotation

When the heartbeat determines rotation is needed:

1. Write a rotation trigger to the state file:
   ```
   state/watchdog/spot-[agent-name].md
   trigger: rotation
   reason: [agent_threshold | checkpoint_cap]
   timestamp: [ISO timestamp]
   agent_context_at_trigger: [percentage]
   ```
2. The status line script detects the trigger flag
   on its next invocation and signals Spot
3. Spot executes the rotation cycle per spot.md
4. When rotation is complete Spot updates the state file
5. The heartbeat reads the updated state file and
   resets its tracking values for this instance

The heartbeat does not directly control agent or
Spot sessions. It writes trigger signals to the
state file. The status line mechanism delivers them.

---

## Orphaned State File Detection

On every cycle the heartbeat checks:

For every file in state/watchdog/ matching
spot-[agent-name].md:
- Is there an active agent session for [agent-name]?
- Is there an active Spot session for [agent-name]?

If a state file exists with no corresponding active
sessions — orphaned file detected.

Action:
1. Write an entry to state/known-issues.md immediately
2. Preserve the orphaned state file — do not delete it
3. Alert the orchestrator at its next session start
4. Do not attempt recovery autonomously —
   the orchestrator decides what happens next

---

## Multiple Spot Instances

The heartbeat manages all active Spot instances
simultaneously. Each instance is tracked independently.
There is no interaction between tracking states —
a rotation trigger for builder-core does not affect
the tracking state for builder-tests.

The orchestrator Spot instance is always present.
It is initialized at session start and is the first
entry in the heartbeat's tracking state.

---

## What the Heartbeat Does Not Do

- Make decisions about drift or behavioral integrity
- Write to Spot state files (except trigger flags)
- Interact with agents directly
- Evaluate output quality
- Trigger escalations — it flags orphaned files to
  known-issues.md and defers to the orchestrator
- Survive session end — it is a session-scoped process.
  State files persist. The heartbeat does not.

---

## Setup and Configuration

The heartbeat is launched from a SessionStart hook
in Claude Code:

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

Configuration is passed via environment variables
or a config file at session start:

```json
{
  "heartbeat_interval_seconds": 30,
  "default_check_interval_percent": 10,
  "default_checkpoint_cap": 8,
  "watchdog_state_dir": "state/watchdog/",
  "context_metrics_file": "state/watchdog/context-metrics.json"
}
```

Per-agent overrides are set by the orchestrator at
Spot assignment and written to the state file.
The heartbeat reads them from the state file when
initialising tracking for a new Spot instance.

---

## Status Line Script

The status line script is a companion to the heartbeat.
It runs inside each agent session and feeds context
data to the shared metrics file.

Location: environment/spot-status-line.py

It receives the Claude Code status line JSON and:
1. Extracts context_window.used_percentage
2. Writes it atomically to context-metrics.json
   keyed by agent session identifier
3. Checks for rotation trigger flags in the state file
4. If a trigger flag is present — signals the current
   session that Spot needs to run

The status line script is the bridge between the
heartbeat (which runs outside sessions) and the
agents (which run inside sessions).

---

## Empirical Calibration Values

Two values must be measured during validation testing
and stored in the heartbeat configuration:

**compression_headroom**
How much of Spot's context window is consumed by a
full rotation cycle — reading all checkpoints, reading
agent output, constructing the seed, verifying it,
and executing both respins.

Measured during Test Case 5 of the validation spec.
Used to calculate the checkpoint cap.

**average_checkpoint_size**
How much of Spot's context window is consumed by a
single checkpoint review and state file entry.

Measured during Test Case 5 of the validation spec.
Used to calculate the checkpoint cap.

Until empirical values are available use:
- compression_headroom: 40% of Spot's max context
- average_checkpoint_size: 5% of Spot's max context
- Resulting default checkpoint cap: 8

These defaults are conservative by design.

---

## Files Owned by the Heartbeat Environment

```
environment/
├── spot-heartbeat.py          # Main heartbeat process
├── spot-status-line.py        # Status line companion script
└── environment-rules.md       # Governs environment setup

state/watchdog/
├── watchdog-rules.md          # Governs watchdog state maintenance
├── context-metrics.json       # Written by status line scripts
│                              # Read by heartbeat
│                              # Not a permanent record
└── spot-[agent-name].md       # One per active Spot instance
                               # Owned by Spot
                               # Read by heartbeat
```

---

*Document version: 1.0*
*Created: 2026-03-04*
*Author: Studio Owner — Rogue Guardian Studios*
*Next review: After validation testing and first
calibration improvement cycle*
