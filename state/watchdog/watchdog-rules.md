# Watchdog State Rules
# Governs how the watchdog state directory is maintained.
# Covers: who reads and writes state files, what an
# orphaned file means, and the lifecycle of
# spot-[agent-name].md files.
---

## Directory Purpose

state/watchdog/ is the runtime state directory for
all active Spot instances and the dynamic threshold
pipeline. Files here are transient — they exist for the
duration of a monitoring session and are destroyed at
clean stand-down.

---

## Who Reads and Writes What

**spot-[agent-name].md** — One per active Spot instance.
- Created by: Spot at first invocation
- Written by: Spot (checkpoint entries, compression records,
  HALT flags)
- Read by: Spot (at each invocation, to reconstruct state),
  PreToolUse hook (checks HALT flag before every tool call)
- Destroyed by: Spot at clean stand-down

**context-pct.txt** — Current context usage percentage.
- Written by: StatusLine hook (inline command, after each
  assistant message)
- Read by: Spot (at each invocation, to check context
  usage), PreToolUse hook (context gate, before every
  tool call), StatusLine hook (spawn check)
- Contains: a single number (e.g., `23.5`)
- Not a permanent record. Overwritten on every update.

**context-threshold.txt** — Dynamic context threshold.
- Created by: Orchestrator at session start (initial value,
  default 15)
- Written by: Spot (raises after clean or minor drift
  checkpoint)
- Read by: StatusLine hook (spawn check — compares against
  context-pct.txt), PreToolUse hook (context gate — blocks
  agent when usage >= threshold), Spot (reads current
  threshold at each invocation)
- Contains: a single integer (e.g., `15`, `30`, `45`)
- Reset to initial value by Spot after compression/rotation
- Missing file default: 15 (conservative — Spot spawns early)

**spot.lock** — Spot subprocess PID lock.
- Created by: StatusLine hook spawn logic (writes PID)
- Read by: StatusLine hook (checks for existing Spot
  before spawning — stale PIDs detected via `kill -0`)
- Cleaned up by: Spot on exit (via `trap EXIT`), or
  StatusLine hook (removes stale locks)
- Contains: a single PID number
- Prevents concurrent Spot instances

**spot-notes-[agent-name].md** — Spot's assessment and
  agent communication channel.
- Created by: Spot at each invocation
- Written by: Spot (overwrites each invocation with
  latest assessment)
- Read by: Watched agent (after context gate lifts,
  agent reads its governing MD and corrective notes)
- Contains: agent's governing MD file (verbatim),
  checkpoint status, corrective notes if any,
  context usage and threshold info
- Destroyed by: Spot at clean stand-down

**watchdog-rules.md** — This document.
- Read by: Any agent that needs to understand state
  directory conventions.
- Written by: Human only.

---

## State File Lifecycle

**Creation:**
Spot creates state/watchdog/spot-[agent-name].md at its
first invocation for a watched agent. The file is
initialised with session configuration, checkpoint cap,
and generation 1. This happens during Spot's first
checkpoint cycle.

**Active use:**
Spot writes checkpoint entries after each invocation.
Spot writes compression records during rotation cycles.
Spot writes HALT flags when a values breach or persistent
drift is detected.

**Rotation:**
During rotation the state file is the bridge. It persists
across the watched agent's respin. After respin, the next
Spot invocation reads the state file to reconstruct
monitoring context. The generation count is incremented.
Checkpoint entries from the previous generation are
replaced by the compression record.

**Stand-down:**
When the watched agent signals task completion and Spot's
final checkpoint is clean, Spot destroys the state file
and the notes file. A clean stand-down leaves no files
behind (except context-pct.txt which is overwritten on
next StatusLine fire, and context-threshold.txt which the
orchestrator manages).

**Abnormal termination:**
If Spot crashes, the state file and lock file may persist.
The lock file is cleaned up by the StatusLine hook's stale
PID detection. The state file persists as an orphan.

---

## Orphaned State Files

An orphaned state file is one that exists in state/watchdog/
without a corresponding active monitoring relationship.

The orchestrator scans for orphaned files at every session
start (step 7 of session-open protocol in orchestrator.md).

**When an orphaned file is detected:**
1. The orchestrator writes an entry to state/known-issues.md
2. The orphaned file is preserved — never deleted by automation
3. The human is alerted in the opening status summary
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

Written by Spot to the watched agent's state file
on a values breach or persistent drift:

```
---
halt: true
reason: [values-breach | persistent-drift]
timestamp: [ISO 8601 timestamp]
spot-instance: spot-[agent-name]
```

The PreToolUse hook (configured inline in Claude Code
settings) enforces the HALT flag automatically. When the
hook reads `halt: true` from the state file, it blocks
every tool call the watched agent attempts. The agent
cannot bypass this — enforcement is involuntary.

Only Spot writes the HALT flag. Only Spot clears it,
after explicit human approval to resume. The
HALT flag is never cleared autonomously.

---

*Document version: 3.0*
*Created: 2026-03-05*
*Updated: 2026-03-12*
*Author: [Your Name]*
*Major change: Added context-threshold.txt, spot.lock,
and spot-notes-[agent-name].md to file listing.
Dynamic threshold pipeline. (v3.0)*
