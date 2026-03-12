# active-project-rules.md
# Active Project State Rules
# This document governs how active-project.md is maintained.
# All agents that read or write active-project.md must
# read this document first.
# This document is immutable. Only the human
# may modify it.

---

## Who Reads This File

Every agent reads active-project.md at session start.
It is the first state file loaded after values.md
and CLAUDE.md. No agent begins work without reading it.

---

## Who Writes This File

The orchestrator is the primary maintainer.
No other agent may rewrite this file.
Builder and planner agents may request updates
via escalation if they identify stale information.

---

## When It Must Be Updated

The orchestrator updates active-project.md:

- At the start of every session if anything has changed
- When a phase changes
- When a blocker is identified or resolved
- When priorities shift
- When the human changes direction
- At the close of every significant session

If a session ends without an update and nothing
changed, that must be a conscious decision —
not an oversight.

---

## How It Is Updated

This file is rewritten, not appended to.
It reflects current state only.
The previous version is preserved in the
GitHub commit log automatically.

When rewriting:
- Update the Last updated field
- Update the Updated by field
- Update only what has changed
- Do not preserve outdated information
  out of caution — stale data is harmful

---

## What Must Always Be Current

These fields must never be stale:

- Current Phase and sign-off status
- Blockers — if resolved, remove them
- Agent Status Summary
- Last updated and Updated by

A file with a stale Last updated date is a signal
that the system is not being maintained. Treat it
as a blocker.

---

## What This File Is Not

- It is not a full decisions log — that is decisions.md
- It is not a full backlog — that lives in the project
- It is not a historical record — that is GitHub
- It is not a substitute for reading the full state files

It is orientation. It gets agents pointed in the
right direction quickly. Depth lives elsewhere.

---

## Escalation

If active-project.md contains information that
contradicts what an agent knows to be true,
that agent must escalate to the orchestrator
before proceeding. Do not work from stale state.

---

*Rules version: 1.0*
*Created: 2026-03-02*
*Author: [Your Name]*
*Next review: At human's discretion*

