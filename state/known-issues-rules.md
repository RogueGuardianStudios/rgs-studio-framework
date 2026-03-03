# known-issues-rules.md
# Rogue Guardian Studios — Known Issues Rules
# This document governs how known-issues.md and
# known-issues-archive.md are maintained.
# All agents that read or write known-issues.md must
# read this document first.
# This document is immutable. Only the studio owner
# may modify it.

---

## Who Reads known-issues.md

- Orchestrator — every session, before any work
- Conclave agents — before any consultation
- Planner — before producing any execution graph
- Builders — before beginning any implementation
- Reviewer — before scoring any output

No agent begins work without awareness of
current known issues. An agent that builds
against an unread known issue creates
compounding problems.

---

## Who Reads known-issues-archive.md

Nobody loads this by default.
Load it only when investigating an issue that
may have occurred before.
Check here before treating a problem as new.

---

## Who Writes These Files

The orchestrator is the primary maintainer.
Any agent may submit a new issue or update
to an existing entry via escalation.
The orchestrator decides severity and ownership.

The studio owner may write directly at any time.

Only the orchestrator may move entries to
known-issues-archive.md.

---

## When known-issues.md Must Be Updated

- When a new issue is identified — add immediately
- When severity changes — update the entry
- When an owner is assigned — update the entry
- When an issue is resolved — archive and remove
- When a workaround is put in place — note it
- At the close of every significant session

Issues are never left without an owner.
An unowned issue is an ignored issue.

---

## Severity Escalation

If an issue's severity increases:

- Update the severity field immediately
- If it becomes Critical — escalate to orchestrator
  before any other work continues
- Document why the severity changed in the notes

Severity never decreases without orchestrator
confirmation. A downgrade that hides a real
problem violates Value 1.

---

## Ownership Rules

Every open issue must have an owner at all times.
The owner is responsible for:

- Keeping the status current
- Driving resolution or escalating blockers
- Updating notes when anything changes

If an owner becomes inactive on an issue,
the orchestrator reassigns it.

---

## Resolution Process

When an issue is resolved:

1. Document the resolution path in the notes
2. If resolution produced a decision, add it
   to decisions.md with a reference pointer
3. Copy the full entry to known-issues-archive.md
4. Remove the entry from known-issues.md

An issue is never removed without being
archived first.

---

## What known-issues.md Is Not

- It is not a backlog or task list
- It is not a place for open questions
- It is not a wishlist of improvements
- It is not optional reading

Known problems only. Current. Owned. Tracked.

---

## Escalation

Critical issues escalate to the orchestrator
immediately — before any other work in the
session continues.

If an issue has had no status update in two
sessions, the orchestrator flags it at session
start. Stale issues are unmanaged risk.

---

*Rules version: 1.0*
*Created: 2026-03-02*
*Author: Studio Owner — Rogue Guardian Studios*
*Next review: At studio owner's discretion*


