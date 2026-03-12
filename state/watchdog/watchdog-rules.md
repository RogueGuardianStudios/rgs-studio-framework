# Rogue Guardian Studios — Watchdog State Rules
# Governs how the watchdog state directory is maintained.
# Covers: who reads and writes state files, what an
# orphaned file means, and the lifecycle of
# spot-[agent-name].md files.
---

## Directory Purpose

state/watchdog/ is the runtime state directory for
all active Spot instances. Files here are transient —
they exist for the duration of a monitoring session
and are destroyed at clean stand-down.

---

## Who Reads and Writes What

**spot-[agent-name].md** — One per active Spot instance.
- Created by: Spot at spin-up
- Written by: Spot (checkpoint entries, compression records)
- Read by: Spot (at respin, to reconstruct state)
- Destroyed by: Spot at clean stand-down

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
Spot writes checkpoint entries after each review cycle.
Spot writes compression records during rotation cycles.
Spot writes HALT flags when a values breach is detected.

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

The orchestrator scans for orphaned files at every session
start (step 7 of session-open protocol in orchestrator.md).

**When an orphaned file is detected:**
1. The orchestrator writes an entry to state/known-issues.md
2. The orphaned file is preserved — never deleted by automation
3. The studio owner is alerted in the opening status summary
4. No recovery is attempted autonomously

**Why orphaned files are never deleted:**
An orphaned file contains the last known checkpoint record,
compression seed, and generation count for a session that
terminated unexpectedly. Deleting it destroys the evidence
needed to understand what happened and recover if possible.

Investigation is required before work continues. The
orchestrator decides what happens next.

---

## HALT Flag Format

Written by Spot to the watched agent's branch state file
on a values breach:

```
---
halt: true
reason: values-breach
timestamp: [ISO 8601 timestamp]
spot-instance: spot-[agent-name]
```

The watched agent checks for a HALT flag before beginning
each new unit of work. On seeing the flag, it stops
immediately and outputs its current state.

Only Spot writes the HALT flag. Only Spot clears it,
after explicit studio owner approval to resume. The
HALT flag is never cleared autonomously.

---

*Document version: 2.0*
*Created: 2026-03-05*
*Updated: 2026-03-12*
*Author: Studio Owner — Rogue Guardian Studios*
