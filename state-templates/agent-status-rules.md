# agent-status-rules.md
# Agent Status Rules
# This document governs how agent-status.md is maintained.
# All agents that read or write agent-status.md must
# read this document first.
# This document is immutable. Only the human
# may modify it.

---

## Who Reads This File

- Orchestrator — every session, before any work
- Any agent that needs to know what others are doing
- Human — at any time for pipeline visibility

---

## Who Writes This File

The orchestrator is the primary maintainer.
Agents may request their own status be updated
via escalation — they do not write directly.
The orchestrator makes all updates.

The human may write directly at any time.

---

## When It Must Be Updated

The orchestrator updates agent-status.md:

- When any agent begins a new task
- When any agent completes a task
- When any agent becomes blocked
- When a blocker is resolved
- When an agent is spun up or stood down
- At the close of every significant session

A status that does not reflect reality is
worse than no status at all. Stale entries
create false confidence in the pipeline.

---

## How It Is Updated

This file is rewritten, not appended to.
It reflects current state only.
The previous version is preserved in the
GitHub commit log automatically.

When updating:
- Update only the entries that have changed
- Update the Last updated field on every
  changed entry
- Never leave a Blocked entry without a
  reference to known-issues.md

---

## Blocked Entries

An agent marked Blocked must always have:
- A reference to the relevant known-issues.md entry
- A current task field that describes what
  they were doing when they became blocked

A blocked agent with no known issue reference
is an untracked problem. Log the issue in
known-issues.md immediately.

---

## What This File Is Not

- It is not a task history
- It is not a performance record
- It is not a substitute for reading
  the agent's own branch files
- It is not optional reading for the orchestrator

Current state only. Always accurate. Never stale.

---

## Escalation

If the orchestrator identifies an agent that
has been blocked for more than one session
without progress on the known issue, escalate
to the human.

A persistently blocked agent is a pipeline
problem, not just an individual agent problem.

---

*Rules version: 1.0*
*Created: 2026-03-02*
*Author: [Your Name]*
*Next review: At human's discretion*

