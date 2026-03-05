# Rogue Guardian Studios — Watchdog State Rules
# Governs how the watchdog state directory is maintained.
# Covers: who reads and writes state files, what an
# orphaned file means, the format of context-metrics.json,
# and the lifecycle of spot-[agent-name].md files.
---

## Directory Purpose

state/watchdog/ is the runtime state directory for
all active Spot instances and the heartbeat process.
Files here are transient — they exist for the duration
of a monitoring session and are destroyed at clean
stand-down.

---

## Who Reads and Writes What

**spot-[agent-name].md** — One per active Spot instance.
- Created by: Spot at spin-up
- Written by: Spot (checkpoint entries, compression records)
- Written by: Heartbeat (rotation trigger flags only)
- Read by: Heartbeat (checkpoint count, config, trigger status)
- Read by: Spot (at respin, to reconstruct state)
- Destroyed by: Spot at clean stand-down

**context-metrics.json** — Shared metrics file.
- Written by: Status line script (one write per agent per
  assistant message, atomic write-to-temp-then-rename)
- Read by: Heartbeat (on each cycle)
- Not a permanent record. Exists only while sessions are active.
- Not owned by any single agent.

**watchdog-rules.md** — This document.
- Read by: Any agent that needs to understand state
  directory conventions.
- Written by: Studio owner only.

---

## State File Lifecycle

**Creation:**
Spot creates state/watchdog/spot-[agent-name].md at spin-up.
The file is initialised with session configuration, checkpoint
cap, and generation 1. This happens before the watched agent
is released.

**Active use:**
Spot writes checkpoint entries after each review.
Spot writes compression records during rotation cycles.
The heartbeat reads checkpoint count and configuration
on each cycle. The heartbeat writes rotation trigger
flags when thresholds are reached.

**Rotation:**
During rotation the state file is the bridge. It persists
across both the watched agent's respin and Spot's respin.
After both respins complete, Spot reads the state file to
reconstruct its monitoring context. The generation count
is incremented. Checkpoint entries from the previous
generation are replaced by the compression record.

**Stand-down:**
When the watched agent signals task completion and Spot's
final checkpoint is clean, Spot destroys the state file.
A clean stand-down leaves no files behind.

**Abnormal termination:**
If either Spot or the watched agent terminates unexpectedly,
the state file persists as an orphan.

---

## Orphaned State Files

An orphaned state file is one that exists in state/watchdog/
without a corresponding active Spot instance and without
a corresponding active watched agent.

The heartbeat detects orphaned files on every cycle.

**When an orphaned file is detected:**
1. The heartbeat writes an entry to state/known-issues.md
2. The orphaned file is preserved — never deleted by automation
3. The orchestrator is alerted at its next session start
4. No recovery is attempted autonomously

**Why orphaned files are never deleted:**
An orphaned file contains the last known checkpoint record,
compression seed, and generation count for a session that
terminated unexpectedly. Deleting it destroys the evidence
needed to understand what happened and recover if possible.

Investigation is required before work continues. The
orchestrator decides what happens next.

---

## context-metrics.json Format

```json
{
  "builder-core": 23.5,
  "builder-tests": 45.2,
  "orchestrator": 12.8
}
```

Keys are agent names (matching AGENT_NAME env var).
Values are context window used percentage (float).

The file is written atomically by the status line script.
The heartbeat reads it on each cycle. If the file is missing
or unreadable, the heartbeat treats all context values as 0.

This file is not a permanent record. It reflects the most
recent context measurement for each active session.

---

## Rotation Trigger Flag Format

Written by the heartbeat to a Spot state file:

```
---
trigger: rotation
reason: [agent_threshold | checkpoint_cap]
timestamp: [ISO 8601 timestamp]
agent_context_at_trigger: [percentage]
```

The status line script detects "trigger: rotation" in the
state file and signals the session. Spot then executes
the rotation cycle per spot.md.

After rotation is complete, Spot removes the trigger flag
by rewriting the state file with updated post-rotation state.

---

*Document version: 1.0*
*Created: 2026-03-05*
*Author: Studio Owner — Rogue Guardian Studios*
