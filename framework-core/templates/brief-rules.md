# brief-rules.md
# Rogue Guardian Studios — Brief Rules
# This document governs how BRIEF_TEMPLATE.md is
# used and maintained.
# All agents that produce or receive a Brief must
# read this document first.
# This document is immutable. Only the studio owner
# may modify it.

---

## What a Brief Is

A Brief is the standard handoff format between
agents for task-level work. It is not a phase
transition document — that is the Handoff.
A Brief is how one agent tells another what to
do, what is locked, and when to stop and escalate.

A Brief is not optional. No agent begins a task
without a Brief. No exceptions.

---

## Who Produces a Brief

The orchestrator produces all Briefs issued to
conclave agents, the planner, and builders.
The orchestrator may delegate Brief production
to the planner for builder-level Briefs, but
remains accountable for their completeness.

---

## Who Reads a Brief

The receiving agent reads the Brief in full
before beginning any work. The receiving agent
completes the acknowledgement section before
starting. Work does not begin on an unacknowledged
Brief.

---

## Transmitting Agent Sign-Off

When the receiving agent confirms the task is
done, the transmitting agent reviews the output
and confirms it resolves the original issue.

The transmitting agent signs the Brief only when:
- The receiving agent's output meets the
  success condition
- The issue that prompted the Brief is resolved

If the issue is not fully resolved, the
transmitting agent issues an updated Brief
or escalates. They do not sign off on
incomplete work.

---

## Transmitting Agent Fallback

If the transmitting agent is unavailable when
the receiving agent completes their task —
due to session end, reassignment, or being
stood down — the following process applies:

1. The orchestrator identifies the gap
2. A new agent of the same type as the
   transmitting agent is spun up
3. The new agent reads the Brief, the original
   issue, and the receiving agent's output
4. The new agent completes the transmitting
   agent sign-off if the success condition is met
5. The orchestrator documents the fallback
   in state/decisions.md with a reference
   to the Brief

The fallback agent inherits the sign-off
responsibility only. It does not inherit
the transmitting agent's full context.

---

## Brief Versioning

When a Brief is updated mid-task:
- Increment the Brief version number
- Document what changed and why
- The receiving agent re-acknowledges the
  updated Brief before continuing

A receiving agent that continues work on a
superseded Brief version without acknowledging
the update is working from stale instructions.

---

## Skills

The transmitting agent specifies which skills
the receiving agent should load. This includes
both standard studio skills and custom skills
built for specific projects.

The receiving agent loads only the skills
listed in the Brief. Loading unlisted skills
without justification violates the context
loading rules in CLAUDE.md.

---

## Escalation

If a receiving agent encounters a situation
not covered by the Brief and not within their
defined authority to resolve, they stop and
escalate to the orchestrator.

A receiving agent that makes decisions outside
their Brief without escalating is acting without
justification. This violates Value 3.

---

*Rules version: 1.0*
*Created: 2026-03-02*
*Author: Studio Owner — Rogue Guardian Studios*
*Next review: At studio owner's discretion*

