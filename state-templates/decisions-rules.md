# decisions-rules.md
# Decisions Log Rules
# This document governs how decisions.md and
# decisions-archive.md are maintained.
# All agents that read or write decisions.md must
# read this document first.
# This document is immutable. Only the human
# may modify it.

---

## Who Reads decisions.md

- Orchestrator — every session, before any work
- Planner — before producing any execution graph
- All conclave agents — before any consultation
- Builders — before beginning any implementation
- Reviewer — before scoring any output

If you are making decisions or working within
existing decisions, you read decisions.md.

---

## Who Reads decisions-archive.md

Nobody loads this by default.
Load it only when explicitly tracing a historical
decision that no longer appears in decisions.md.

---

## Who Writes These Files

The orchestrator writes to decisions.md after
any decision is made and confirmed.

No other agent may write to decisions.md directly.
Agents that need a decision recorded submit it
to the orchestrator for logging.

The human may write directly at any time.

Only the orchestrator may move entries to
decisions-archive.md, and only with human
approval.

---

## When decisions.md Must Be Updated

A new entry must be added:

- Immediately after any decision is made and
  confirmed by the human
- When any previously locked decision is
  overturned — the reversal is itself a new entry
- When the orchestrator resolves an escalation
  within its own authority

Decisions are never held in working memory
waiting to be logged later. If it was decided,
it is logged now.

---

## How Entries Are Written

Every entry must have:
- The date the decision was made
- A clear one to two sentence summary
- Who made it — human or orchestrator
  within authority
- A reference pointer to where the full
  justification lives
- Status — Active or Superseded

A decision entry without a reference pointer
is incomplete. An unjustified locked decision
violates Value 1 and must be corrected
before the session continues.

---

## Superseding a Decision

When a locked decision is overturned:

1. Do not edit or remove the original entry
2. Add a new entry recording the new decision
3. Mark the original entry Status as:
   Superseded by: [YYYY-MM-DD entry]
4. In the new entry, reference the original
   decision it replaces

The record of what was decided and what
replaced it must always be traceable.

---

## Archiving Process

When active entries in decisions.md reach 50
the orchestrator flags this at session start.

The archiving process:

1. Orchestrator identifies candidates —
   superseded decisions and decisions with
   no active dependencies on current work
2. Orchestrator proposes the archiving plan
   to the human — listing every entry
   proposed for archiving and why
3. Human approves or modifies the plan
4. Approved entries are moved to
   decisions-archive.md in full — complete
   context, justification, and supersession
   record preserved
5. A compression log entry is added to
   decisions.md recording the archiving action
6. The 50 entry threshold is reviewed after
   each archiving cycle and adjusted if needed

No entries are archived without human
approval. No context is stripped from
archived entries.

---

## What decisions.md Is Not

- It is not a backlog or task list
- It is not a place for open questions
- It is not a summary of discussions
- It is not editable once written

Decisions only. Locked. Permanent until archived.

---

## Escalation

If an agent encounters a decision that appears
to contradict current work or a more recent
decision that has not been logged, that agent
must escalate to the orchestrator immediately.
Do not proceed on contradictory decisions.
Surface the conflict.

---

*Rules version: 1.0*
*Created: 2026-03-02*
*Author: [Your Name]*
*Next review: At human's discretion*

