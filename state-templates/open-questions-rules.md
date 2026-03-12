# open-questions-rules.md
# Open Questions Rules
# This document governs how open-questions.md and
# open-questions-archive.md are maintained.
# All agents that read or write open-questions.md
# must read this document first.
# This document is immutable. Only the human
# may modify it.


---


## Who Reads open-questions.md


- Orchestrator — every session, before any work
- Conclave agents — before any consultation
- Planner — before producing any execution graph
- Builders — when their work touches an open question


This file is the conclave's primary input.
A conclave consultation without reading it first
is a consultation without context.


---


## Who Reads open-questions-archive.md


Nobody loads this by default.
Load it only when investigating a question that
may have been attempted before.
Check here before starting any new investigation.


---


## Who Writes These Files


The orchestrator is the primary maintainer.
Any agent may submit a new question or update
to an existing entry via escalation.
The orchestrator decides whether to add or update.


The human may write directly at any time.


Only the orchestrator may move entries to
open-questions-archive.md.


---


## When open-questions.md Must Be Updated


- When a new question is identified
- When an investigation begins — update status
- When an attempt is made — append to attempt log
- When a question is blocked — record the reason
- When a question is resolved — archive and remove
- At the close of every significant session


Questions are never left in a stale status.
If the status has changed, update it now.


---


## Status Definitions


- Open — identified, not yet investigated
- Investigating — actively being looked into
- Testing — a potential answer is being validated
- Blocked — cannot progress, reason documented,
  will retry when blocker is resolved
- Failed — Retry — attempt made, did not resolve
  the question, another approach is needed


A question with no status update in three sessions
is flagged by the orchestrator at session start.
Stale questions are a signal the system has lost
track of something.


---


## The Attempt Log


Every attempt to resolve a question must be
logged inline on the entry before the next
attempt begins. The log must include:


- What was tried
- What happened
- Why it did not resolve the question


An attempt that is not logged is an attempt
that will be repeated. That is waste.


---


## Resolution Process


When a question is resolved:


1. Determine resolution type — Decision or Closed
2. If Decision — add to decisions.md first,
   record the reference pointer
3. Copy the full entry including all attempt
   log entries to open-questions-archive.md
4. Add resolution notes to the archived entry
5. Remove the entry from open-questions.md


A question is never removed without being
archived first. No history is lost.


---


## What open-questions.md Is Not


- It is not a task list or backlog
- It is not a decisions log
- It is not a place for resolved items
- It is not optional reading for the conclave


Unresolved questions only. Active. Current.


---


## Escalation


If an agent identifies a question that should
be in this file but is not, escalate to the
orchestrator immediately. Untracked questions
are unmanaged risk.


If a question has been blocked or failed for
more than three sessions without progress,
the orchestrator escalates to the human
for conclave consultation.


---


*Rules version: 1.0*
*Created: 2026-03-02*
*Author: [Your Name]*
*Next review: At human's discretion*
