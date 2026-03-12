# handoff-rules.md
# Handoff Rules
# This document governs how HANDOFF_TEMPLATE.md is
# used and maintained.
# All agents that produce or receive a Handoff must
# read this document first.
# This document is immutable. Only the human
# may modify it.

---

## What a Handoff Is

A Handoff marks the formal close of one phase and
the opening of the next. It is a checkpoint document,
not a task instruction. It confirms that a phase is
genuinely complete before work continues.

A phase is not done because agents say it is done.
A phase is done when the Handoff is signed by both
the transmitting and receiving phase leads.

---

## Who Produces a Handoff

The lead agent of the closing phase produces the
Handoff document using HANDOFF_TEMPLATE.md.
All fields are required. An incomplete Handoff
does not close the phase.

---

## Who Reads a Handoff

The lead agent of the opening phase reads the
Handoff in full before any work begins.
The orchestrator reads every Handoff regardless
of which agents are involved.

---

## When a Handoff Must Be Produced

A Handoff is produced at every phase transition:

- Planning → Build
- Build → Review
- Review → Merge

No phase transition occurs without a completed
and signed Handoff. This is not a formality —
it is the gate that prevents incomplete work
from moving forward.

---

## The Final PR Group Review

Before any Handoff can close at the Review → Merge
transition, the final PR must pass group review.

Group review membership:
- All active conclave agents
- The orchestrator

Voting rules:
- One dissenting vote — the group may proceed.
  The dissent must be documented in the Handoff.
- Two or more dissenting votes — escalate to the
  human before proceeding. Do not merge.
- Human is the final tiebreaker.
  Their decision is logged in decisions.md.

A PR that has not passed group review does not
merge to main under any circumstances.

---

## Commit Score Log

Every commit during a phase is scored against
the evaluation rubric. Scores are logged in the
Handoff as a running record.

Scoring does not block work during the phase.
It is a record, not a gate.

The final PR review references the full commit
score log. Any score below threshold flagged
during the phase must be addressed before the
final PR is submitted.

---

## Unresolved Items

Every unresolved item from the closing phase
must have an owner and a resolution path before
the Handoff is signed. An item without an owner
is an item that will be dropped.

If there are no unresolved items, that must be
stated explicitly in the Handoff. An empty section
that was not considered is different from a section
that was checked and found empty.

---

## Handoff Sign-Off

Both acknowledgement sections in the Handoff
template must be completed before the Handoff
is considered closed:

- Closing phase lead signs that the phase is
  genuinely complete
- Opening phase lead signs that they have read
  and understood the Handoff

An unsigned Handoff is an open Handoff.
Work does not begin on the next phase until
both sections are signed.

---

## Escalation

If the closing phase lead and opening phase lead
cannot agree that the phase is complete, escalate
to the orchestrator.

If the orchestrator cannot resolve the disagreement,
escalate to the human.

Do not proceed on a disputed Handoff.

---

*Rules version: 1.0*
*Created: 2026-03-02*
*Author: [Your Name]*
*Next review: At human's discretion*

