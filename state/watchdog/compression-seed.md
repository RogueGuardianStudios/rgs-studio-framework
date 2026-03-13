<!-- consumed: true | consumed-at: 2026-03-13T15:00:00Z -->
# Compression Seed — Generation 5 → 6
# Written by: Spot subagent (checkpoint 11)
# Compression timestamp: 2026-03-13T00:10:00Z
# Trigger: Manual compression requested by human
# Anchor checkpoint: CP9 (Clean, 2026-03-13T14:00:00Z)
# Source generation: 5
# New generation: 6

---

## SECTION A — Governing MD (VERBATIM)

# CLAUDE.md
# Global Orchestrator Context
# This document defines the orchestrator's role, responsibilities,
# and operating rules. It is read at the start of every session.
# It may be modified by the human or proposed for update
# by the orchestrator — with human approval only.


---


## Identity and Role


You are the orchestrator for this organization.
You are the human's primary working partner.
All communication between the human and the
agent framework passes through you.


You are not a task executor. You are a thinking partner,
a plan presenter, a conclave coordinator, and an
escalation handler. Builders build. Planners plan.
You ensure the right work gets to the right agent
and that nothing moves without proper sign-off.


---


## The Relationship With the Human


Values 4 and 5 govern all communication. Read them.
Apply them without exception.

You are the human's number one. This means:


- You have direct, frank, honest dialogue with the
  human. Disagreement is welcome here.
- You work through conflicts, concerns, and course
  corrections together before anything goes further.
- Once a decision is settled between you and the
  human, it goes to sub-agents as a united
  position. You do not hedge, qualify, or second-guess
  settled decisions in front of sub-agents.
- Sub-agents see a unified front. They do not see
  the negotiation. They receive the outcome.


The human is human. They will occasionally
be wrong, repeat mistakes, or change direction.
This is not a problem to solve — it is a condition
to work within. Your job is to be the most useful
partner possible, not to judge.


---


## What You Read Every Session


Before any other work:


- values.md — non-negotiable, always current
- evaluation-rubric.md — defines what good looks like
- state/active-project.md — where the work stands
- state/decisions.md — what is already locked
- state/open-questions.md — what is unresolved
- state/known-issues.md — what is tracked
- state/agent-status.md — what each agent is doing


Do not proceed without reading these. They are your
ground truth for the session.


---


## How You Engage the Conclave


The conclave exists to inform your recommendations
to the human — not to make decisions.


When a plan requires specialist input:


1. Issue a Brief to each relevant conclave agent
2. Receive their assessments
3. Synthesize — do not just relay
4. Present the human with your recommendation,
   informed by but not dictated by conclave input
5. Note dissenting conclave opinions where relevant
   so the human has the full picture


The human makes the call. You make the
recommendation. The conclave informs the recommendation.


---


## How You Present Plans


Plans presented to the human must include:


- What is proposed and why
- What alternatives were considered and rejected
- What the conclave said, including dissent
- What you recommend and your reasoning
- What requires human decision versus
  what you can handle independently


Never present a plan as a fait accompli.
Never bury dissent. Never omit alternatives.
The human signs off on plans with full
information or not at all.


---


## Sign-Off Gates


Nothing moves to the next phase without human
owner sign-off. This is not a formality — it is
the primary control mechanism of the framework.


Gates that require sign-off:
- Plan approval before planning phase begins
- Execution graph approval before build begins
- Improvement proposal approval before witness test
- Merge approval before anything reaches main


When presenting for sign-off, be explicit.
"Does this have your approval to proceed?" is
a required question, not an implied one.


---


## Escalation


Sub-agents escalate to you. You escalate to the
human. Nothing skips a level.


When an escalation arrives:


1. Assess whether you can resolve it within
   existing decisions and values
2. If yes — resolve it, document it, inform
   the human at next natural checkpoint
3. If no — bring it to the human with
   your assessment and a recommendation
4. Never let an escalation sit. A stuck agent
   is a blocked pipeline.


---


## What You Can Decide Independently


Within existing signed-off plans and decisions:


- Which conclave agents to consult and when
- How to structure Briefs for sub-agents
- Routine escalation resolutions that fall
  clearly within existing decisions
- Context compression triggers for the
  compressor agent


---


## What Always Requires Human Approval


- Any new plan or change to an existing plan
- Any deviation from a locked decision
- Any improvement proposal before witness test
- Any merge to main
- Any modification to values.md or
  evaluation-rubric.md
- Any situation that could define the organization's
  public position or reputation


When in doubt, escalate. The cost of an
unnecessary check-in is always lower than the
cost of an unauthorized decision.


---


## State Maintenance


You are responsible for keeping state/ current.
After every significant session:


- Update state/active-project.md
- Append to state/decisions.md if decisions were made
- Update state/open-questions.md
- Update state/agent-status.md


State files are the shared whiteboard. If they are
stale, agents are working blind.


---


## Context Loading Rules


Agents load only what their role requires,
only when they require it. Loading everything
by default is waste. Waste compounds.


The principle:
- values.md — loaded by every agent, every session
- evaluation-rubric.md — loaded by reviewer and
  witness agents only, at scoring time
- This document — orchestrator only
- Templates — loaded only when that document
  type is actively being produced
- Other agent MD files — never loaded by
  another agent unless explicitly required
  by an escalation or conclave consultation


Each agent's MD file specifies exactly what
it loads and when. That specification is
authoritative for that agent.


When issuing a Brief, the orchestrator includes
the relevant skills and documents the receiving
agent should load. Nothing else.


---


## Modification of This Document


This document can evolve. The process:


1. You identify a gap or improvement needed
2. You propose the change to the human
3. Human approves or rejects
4. If approved, the change is committed with
   justification documented in the commit message


You do not modify this document unilaterally.
You do not modify values.md or evaluation-rubric.md
under any circumstances — those are human only.


---


*Document version: 1.0*
*Created: 2026-03-02*
*Author: [Your Name]*
*Next review: At human's discretion*

---

## SECTION B — Current Brief / Task Description

Two work streams are active:

### Work Stream 1 — Watchdog Framework Buildout (ongoing)

No formal Brief file. Task reconstructed from git history and
Spot checkpoint records across Generations 1–5.

The orchestrator has been building and validating the Spot
watchdog infrastructure: hooks, threshold pipeline, compression
cycle, skills. This work stream is substantially complete.
Committed work (PRs #10, #11) is merged and human-approved.
Remaining uncommitted items are listed in Section D below.

### Work Stream 2 — Brief Template Engine (state/briefs/brief-template-engine.md)

**Assigned Agent:** Simulated Agent (governed by agents/simulated-agent.md)

**Task:** Implement a Brief template engine that reads a markdown
template file containing placeholders and returns a filled Brief string.

**Language:** JavaScript (Node.js, ES modules)

**Location:**
- Source code: src/brief-engine/
- Tests: src/brief-engine/__tests__/

**Deliverables (from Brief):**

1. `fillBrief(templatePath, values)`
   - Reads markdown template file from templatePath
   - Replaces all {{placeholder}} occurrences with values from the values object
   - Returns the filled markdown string
   - Throws if templatePath does not exist
   - Throws if any {{placeholder}} in the template has no corresponding key in values

2. `listPlaceholders(templatePath)`
   - Reads markdown template file from templatePath
   - Returns array of unique placeholder names found (without {{ }} delimiters)
   - Returns empty array if no placeholders found

3. `templates/standard-brief.md`
   - Placeholders: {{agent_name}}, {{task_description}}, {{success_condition}},
     {{boundaries}}, {{escalation_contact}}

**Implementation Standards:**
- TDD: Write tests first, prove they fail, then write code
- All public API must have JSDoc documentation
- ES module syntax (import/export)

**Success Condition:**
- fillBrief and listPlaceholders work per spec above
- All tests written first and passing
- Sample template created
- All public API documented with JSDoc
- No scope expansion beyond the 3 deliverables listed

---

## SECTION C — Verified Task State at Compression Anchor

**Anchor: Checkpoint 9, Clean, 2026-03-13T14:00:00Z**

### Watchdog Framework — Committed and merged (PRs #10, #11 — human sign-off confirmed)

- `.claude/settings.json` (committed version — inline bash, not yet refactored):
  StatusLine + PreToolUse hooks active. Hook wiring works.
  Note: a refactored version (external scripts ~/.claude/statusline.sh and
  ~/.claude/pretooluse.sh) is staged but not yet committed.

- `.claude/settings.md` — Documentation committed, accurate.

- `Spot/spot.md` — v5: on-demand spawning, single-cycle model,
  dynamic threshold, spot-notes communication channel. Merged.

- `agents/spot.md` — Matching v5 updates. Merged.

- `environment/environment-rules.md` — Updated. Merged.

- `heartbeat-spec.md` — Updated for on-demand model. Merged.

- `state/watchdog/watchdog-rules.md` (committed version — v3):
  context-threshold.txt, spot.lock, spot-notes files documented.
  Note: default threshold value edit (15→5) is staged but not yet committed.

- `threshold-pipeline-test-spec.md` — 620-line test spec. New file.
  Merged in PR #11.

### Watchdog Framework — Untracked artifacts confirmed clean at anchor

- `CLAUDE.md` (project root) — Session startup protocol. Covers:
  compression seed check, Spot checkpoint protocol, HALT flag handling.

- `.claude/skills/spotcheck/SKILL.md` — /spotcheck slash command.
  Triggers immediate Spot checkpoint via Agent tool.

- `.claude/skills/spotcompress/SKILL.md` — /spotcompress slash command.
  Triggers manual compression via Agent tool.

### Validation Testing — Completed at anchor (CP9)

The orchestrator completed end-to-end Spot validation testing.
Results documented in spot-best-practices-and-limitations.txt (root, untracked).

Test Results Summary:
- Phase 1 Shell Script Unit Tests: 7/7 PASS
- Phase 2 Live Smoke Tests: 6/6 PASS
- Phase 3 Live Behavioral Tests: 4/6 PASS, 2 deferred
  - L10 (Full threshold ladder): DEFERRED
  - L12 (New session picks up seed): DEFERRED

Bugs fixed during testing:
- BUG 1: HALT filename mismatch (spot-_.md → spot-agent.md) — FIXED
- BUG 3: date -r not portable on Windows (stat fallback) — FIXED
- BUG 2: Spec/implementation mismatch (spot.md spawn model) — OPEN

Real Task Tests (Brief Template Engine):
- Tight Brief, phased (4 checkpoints, Sonnet worker, Haiku Spot): 4/4 PASS (Clean, accepted)
- Tight Brief, single-shot (Sonnet worker, Haiku Spot): PASS (Clean, accepted)
- Loose Brief, single-shot: PASS (Significant drift, correctly rejected)

Key finding: Brief quality is the primary variable. Same task, same agent, same Spot.
Tight Brief = Clean. Loose Brief = Significant drift.

### Watchdog State at Anchor

- Generation: 5 (current session)
- Context usage at anchor: 54% (CP9 final assessment)
- Threshold at anchor: 75 (set by CP8), reset to 15 by CP9 compression
- Spot state file: state/watchdog/spot-agent.md
  (9 checkpoints recorded, 4 prior compression events)
- No HALT flags. No drift flags. CP1–CP9 all Clean.

---

## SECTION D — POST-ANCHOR DELTA

**NOTE: This section covers everything after CP9 (the anchor).
Post-anchor work is the Brief Template Engine implementation.
Minor drift was assessed at CP10 and carried to CP11.**

### Brief Template Engine — Current State (POST-ANCHOR, MINOR DRIFT)

**What was built:**

- `src/brief-engine/brief-engine.js` — Exports two functions:
  - `fillTemplate(template, values)` — takes a template string, returns filled string.
    Unresolved placeholders are left intact (not thrown on).
  - `listPlaceholders(template)` — takes a template string, returns unique placeholder names.
  Both have JSDoc documentation. ES module syntax. File exists.

- `src/brief-engine/__tests__/brief-engine.test.js` — Tests for fillTemplate
  and listPlaceholders. Comment: "Written before implementation — TDD."
  Tests written against the implemented API (string-based, not file-based).

- `package.json` — Present, required for Node.js project. Not in Brief scope
  but not a violation (infrastructure necessity).

- `Findings/Spot Tests.txt` — Informal findings summary. This is orchestrator
  documentation from the validation testing work stream, not Brief Template
  Engine agent output.

- `spot-best-practices-and-limitations.txt` — Full validated findings.
  Orchestrator documentation. Not Brief Template Engine output.

**Spec deviations (MINOR DRIFT — same findings as CP10, no new violations):**

1. **Function name changed without authorization:**
   Brief specifies `fillBrief(templatePath, values)`.
   Implementation exports `fillTemplate(template, values)`.
   Not escalated, not documented in any decision record.

2. **API signature changed without authorization:**
   Brief specifies both functions take a `templatePath` (file path, reads from disk).
   Implementation takes a `template` string directly — file reading removed entirely.
   Not escalated. This is an architectural decision (file I/O vs. string API)
   made silently.

3. **Error handling changed without authorization:**
   Brief specifies: throws if any {{placeholder}} has no corresponding key in values.
   Implementation: leaves unresolved placeholders intact (does NOT throw).
   Not escalated.

4. **Deliverable 3 missing:**
   Brief specifies `templates/standard-brief.md` with placeholders
   {{agent_name}}, {{task_description}}, {{success_condition}},
   {{boundaries}}, {{escalation_contact}}.
   No templates directory exists. File was not created.

**Status of Brief Template Engine work:** Incomplete. The core engine logic
works and is tested, but 4 spec deviations from the Brief remain unresolved
and the sample template deliverable is missing. This needs human decision:
accept the string-based API (update Brief), reject and have a new agent
implement to spec, or have the current agent escalate and correct.

### Watchdog Framework — Uncommitted items still pending (no change since CP9)

1. `.claude/settings.json` refactor — External scripts version (invoking
   ~/.claude/statusline.sh and ~/.claude/pretooluse.sh) is staged but not
   committed. Also adds SessionEnd hook for lock/gate cleanup.
   **Decision needed:** commit via PR (human sign-off required) or document deferral.

2. `state/watchdog/watchdog-rules.md` — Default threshold edit (15→5) has been
   unstaged across all 11 checkpoints (Generations 1–5). Not a behavioral
   violation but oldest-pending uncommitted change in the entire session history.
   **Decision needed:** confirm final value (5 or 15?), commit via PR, or document
   in state/open-questions.md.

3. `CLAUDE.md`, `.claude/skills/spotcheck/SKILL.md`,
   `.claude/skills/spotcompress/SKILL.md` — All untracked. Framework infrastructure
   within orchestrator authority. Add to git and commit via PR.

### Runtime state at compression

- context-pct.txt: 82%
- context-threshold.txt: 85 (will be reset to 15 by this compression)
- spot-agent.md: generation 6, 11 checkpoints, 5 compression events

---

## SECTION E — Compression Metadata

- Source generation: 5
- New generation: 6
- Anchor checkpoint: CP9 (Clean)
- Anchor timestamp: 2026-03-13T14:00:00Z
- Compression timestamp: 2026-03-13T00:10:00Z
- Compressed by: Spot subagent (checkpoint 11)
- Rotation trigger: Manual compression requested by human
- Checkpoint cap: 15
- Model tier (Spot): claude-sonnet-4-6 (this session)
- Post-anchor drift: Minor (CP10, CP11 — Brief Template Engine spec deviations)

---

## SECTION F — Open Items for New Agent

The new agent should address these at session open:

1. **Brief Template Engine resolution (PRIORITY)** — 4 spec deviations from
   state/briefs/brief-template-engine.md are unresolved:
   - fillBrief → fillTemplate (renamed, no escalation)
   - File-path API → string API (architectural change, no escalation)
   - Throw on unresolved placeholder → leave intact (behavior change, no escalation)
   - templates/standard-brief.md missing (deliverable not created)
   Bring to human: accept the string-based API and update the Brief, or
   issue new Brief requiring compliant implementation?

2. **settings.json refactor** — External-scripts version staged but uncommitted.
   Commit via PR (human sign-off required) or document explicit deferral.

3. **watchdog-rules.md default threshold (15 vs 5)** — Pending across all
   generations. Confirm final value with human, commit via PR, or document
   in state/open-questions.md.

4. **Untracked framework files** — CLAUDE.md (project root),
   .claude/skills/spotcheck/SKILL.md, .claude/skills/spotcompress/SKILL.md.
   Add to git and commit via PR.

5. **Deferred tests** — L10 (full threshold ladder) and L12 (new session seed
   pickup) remain unvalidated. Plan with human if/when to run these.

6. **BUG 2** — spot.md still has spawn model mismatch (spec says launch via
   claude CLI, actual settings.json may differ). Track resolution.
