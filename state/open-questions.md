# open-questions.md
# Rogue Guardian Studios — Open Questions
# This file tracks all unresolved questions affecting
# active work. It is the most dynamic state file
# in the system. Items arrive, progress, and leave.
# Resolved questions move to decisions.md or are
# archived with their full history.
# If this file is stale, the conclave is working blind.

---

## How to Read This File

Each entry is a question that has not yet been
fully resolved. Status tells you where it stands.
Attempt Log tells you what has already been tried.

Do not retry a failed approach without reading
the attempt log first.

---

## Entry Format

- **[YYYY-MM-DD]** [Question — one to two sentences]
  Owner: [Agent or role responsible for resolution]
  Status: [Open / Investigating / Testing /
           Blocked / Failed — Retry]
  Blocked reason: [Why it is stalled — if applicable]
  Next action: [What happens next and who owns it]

  Attempt Log:
  - [YYYY-MM-DD] [What was tried, what happened,
    why it did not resolve the question]
  - [Add as needed]

---

## Resolution

When a question is resolved:

Resolved → Decision:
- Add the decision to decisions.md with full
  justification and reference pointer
- Archive this entry in full to
  open-questions-archive.md including all
  attempt log entries
- Remove this entry from open-questions.md

Resolved → Closed:
- Archive this entry in full to
  open-questions-archive.md including all
  attempt log entries
- Remove this entry from open-questions.md

A question is never deleted without being
archived first. The attempt history must
be preserved.

---

## Open Questions

- **[2026-03-03]** Should orchestrator.md include explicit
  sub-agent briefing guidelines to prevent context bloat
  and compression-triggered amnesia loops?
  Owner: Orchestrator
  Status: Investigating
  Blocked reason: N/A
  Next action: Propose specific additions to orchestrator.md
  for studio owner review.

  Attempt Log:
  - [2026-03-03] Identified the problem during first real
    pipeline task (GOAP Hub color audit). Sub-agent was
    given an open-ended research prompt with no scope
    limits. It read 22 full files, hit context compression,
    and repeated its work twice. Total: 123 tool calls,
    6.5 minutes for a task that should take under 2 minutes.
    Proposed guidelines drafted below for orchestrator.md
    amendment.

  Proposed additions to orchestrator.md section
  "How You Work With Builders and Planner":

  ```
  ## How You Brief Sub-Agents

  Sub-agents operate in constrained context windows.
  A sub-agent that ingests too much material will hit
  context compression and lose track of its progress,
  causing repeated work and wasted turns.

  When briefing sub-agents:

  - Scope tightly. One agent, one focused question.
    "Find all hardcoded colors in these 3 files" not
    "audit the entire editor codebase for colors."
  - Prefer grep-and-report over read-everything.
    Tell agents to search for patterns and return
    matches with context, not to read entire files
    unless the content requires full comprehension.
  - Set explicit limits. Tell the agent how many files
    to expect and what output format you want.
  - Split large research across multiple agents.
    Three agents each covering 7 files will finish
    faster and more reliably than one agent covering 21.
  - Keep the total scope under ~1500 lines of source
    per agent. Fewer files of 300+ lines means a lower
    file count. More small files can raise the count.
    If a single file exceeds 1500 lines, that agent
    gets only that file — no additional files.
  - If a sub-agent needs full file content, have it
    read files incrementally and take notes, not load
    everything at once.

  A sub-agent that repeats its own work is a sign that
  its brief was too broad. This is the orchestrator's
  responsibility, not the sub-agent's.
  ```

- **[2026-03-03]** Should orchestrator.md include model selection
  guidelines for sub-agents to avoid wasting compute on
  mechanical tasks?
  Owner: Orchestrator
  Status: Investigating
  Blocked reason: N/A
  Next action: Propose specific additions to orchestrator.md
  for studio owner review.

  Attempt Log:
  - [2026-03-03] During the GOAP Hub color extraction task,
    4 sub-agents were launched to do mechanical find-and-replace
    of inline color references. All 4 inherited the parent
    model (Opus) despite the work being straightforward pattern
    replacement with clear instructions. This is wasteful —
    Opus is the slowest and most expensive model, and these
    tasks needed no architectural judgment. Agent 4 (12 files)
    also timed out, partly because Opus is slower per turn.
    Haiku or Sonnet would have completed faster and cheaper.

  Proposed addition to orchestrator.md section
  "How You Brief Sub-Agents" (extends existing proposal):

  ```
  ## Model Selection for Sub-Agents

  You can specify which model a sub-agent runs on.
  If you do not specify, the agent inherits your model.
  This is often wasteful.

  Choose the model based on task complexity:

  - Haiku: Mechanical tasks with clear instructions.
    Find-and-replace, reformatting, collecting data
    from files, simple code edits where the pattern
    is fully specified. Fast and cheap.
  - Sonnet: Tasks requiring moderate judgment.
    Refactoring with context awareness, writing
    tests, code review, multi-step edits where the
    agent needs to understand surrounding code.
  - Opus: Tasks requiring deep reasoning or
    architectural decisions. Design work, complex
    debugging, ambiguous requirements, anything
    where incorrect judgment could cause rework.

  Default to the cheapest model that can handle the
  task. Escalate only when the task genuinely needs
  the capability. A mechanical edit running on Opus
  is a sign of lazy briefing.
  ```

---

*This file reflects active questions only.*
*Resolved questions live in open-questions-archive.md*
*See open-questions-rules.md for maintenance rules.*

