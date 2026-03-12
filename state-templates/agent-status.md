# agent-status.md
# Agent Status
# This file is a live snapshot of what every agent
# is doing right now.
# It is always current. It is never historical.
# History lives in the GitHub commit log.
# If this file is stale, the orchestrator is flying blind.

---

## How to Read This File

Each entry reflects an agent's current state.
Status tells you what they are doing right now.
Blocked entries point to known-issues.md.
Do not infer status — read it here.

---

## Status Definitions

**Active** — agent is currently working on a task.
**Idle** — agent has no current assignment.
**Blocked** — agent cannot proceed. See known-issues.md
for the relevant entry.
**Awaiting Sign-Off** — agent has completed work and
is waiting for human or orchestrator approval.
**Inactive** — agent is not spun up for this project.

---

## Entry Format

- **[Agent name/role]**
  Status: [Active / Idle / Blocked /
           Awaiting Sign-Off / Inactive]
  Current task: [One sentence describing what
  the agent is working on right now]
  Branch: [agent/branch-name]
  Blocked ref: [known-issues.md entry date and
  summary — if blocked, otherwise N/A]
  Last updated: [YYYY-MM-DD]

---

## Agent Status

- **Orchestrator**
  Status: [Status]
  Current task: [Task]
  Branch: agent/orchestrator
  Blocked ref: N/A
  Last updated: [YYYY-MM-DD]

- **Planner**
  Status: [Status]
  Current task: [Task]
  Branch: agent/planner
  Blocked ref: N/A
  Last updated: [YYYY-MM-DD]

- **Builder-core**
  Status: [Status]
  Current task: [Task]
  Branch: agent/builder-core
  Blocked ref: N/A
  Last updated: [YYYY-MM-DD]

- **Builder-editor**
  Status: [Status]
  Current task: [Task]
  Branch: agent/builder-editor
  Blocked ref: N/A
  Last updated: [YYYY-MM-DD]

- **Builder-tests**
  Status: [Status]
  Current task: [Task]
  Branch: agent/builder-tests
  Blocked ref: N/A
  Last updated: [YYYY-MM-DD]

- **Builder-docs**
  Status: [Status]
  Current task: [Task]
  Branch: agent/builder-docs
  Blocked ref: N/A
  Last updated: [YYYY-MM-DD]

- **Reviewer**
  Status: [Status]
  Current task: [Task]
  Branch: agent/reviewer
  Blocked ref: N/A
  Last updated: [YYYY-MM-DD]

- **Witness**
  Status: [Status]
  Current task: [Task]
  Branch: agent/witness
  Blocked ref: N/A
  Last updated: [YYYY-MM-DD]

- **Compressor**
  Status: [Status]
  Current task: [Task]
  Branch: agent/compressor
  Blocked ref: N/A
  Last updated: [YYYY-MM-DD]

---

*This file is current state only.*
*History lives in the GitHub commit log.*
*Blocked entries must reference known-issues.md.*
*See agent-status-rules.md for maintenance rules.*

