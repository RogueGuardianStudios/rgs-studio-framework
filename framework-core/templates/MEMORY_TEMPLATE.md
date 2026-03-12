# MEMORY_TEMPLATE.md
# Agent Memory Dump
# This document is the persistent memory for a single agent.
# It lives in the agent's branch and is never passed directly
# to other agents. Briefs are derived from this document.
# Structure must be preserved across compression cycles.


---


## Memory Metadata


- **Agent:** [Agent name/role]
- **Branch:** [agent/name]
- **Project:** [Project name]
- **Created:** [YYYY-MM-DD]
- **Last updated:** [YYYY-MM-DD]
- **Compression count:** [0]
- **Last compressed:** [YYYY-MM-DD or Never]


---


## Current Goals


Bullet pointed. Light context only.
This section is always current — update it, do not append.


- [Goal 1]
- [Goal 2]
- [Add as needed]


---


## Decisions Log


Permanent record. Never compressed. Only appended to.
Each entry is a short summary plus a reference pointer
to the full justification. The reasoning must always
be traceable — a decision without a reference is incomplete.


Format per entry:
- [YYYY-MM-DD] [Decision summary]
  Ref: [file path or commit reference where full
  justification lives]


Entries:
- [YYYY-MM-DD] [Decision summary]
  Ref: [reference]


---


## Pain Points Log


Permanent record. Never compressed. Only appended to.
Running friction encountered during this agent's work.
Source material for improvement proposals.


Format per entry:
- [YYYY-MM-DD] [Description of friction encountered]
  Status: [Open / Proposed / Resolved]
  Ref: [improvement proposal path if one exists]


Entries:
- [YYYY-MM-DD] [Pain point description]
  Status: [Open]
  Ref: [none]


---


## Active Working Memory


Current conversation context and recent task history.
This is the section the compressor agent condenses.
Older entries are archived to GitHub before removal.
Archive path format: agent-workspace/archive/YYYY-MM-DD-compression-N.md


[Working memory content goes here — conversation context,
recent decisions under consideration, current task state,
anything the agent needs to function right now.]


---


## Compression Log


Record of every compression cycle this memory dump
has undergone. Never compressed. Only appended to.


Format per entry:
- Compression [N] — [YYYY-MM-DD]
  Performed by: [compressor agent]
  Condensed: [brief description of what was summarised]
  Archived to: [path to archived content in GitHub]
  Active memory before: [approximate line count]
  Active memory after: [approximate line count]


Entries:
- No compressions performed yet.


---


*Memory maintained under values.md v1.0*
*Active working memory is the only section subject
to compression. All other sections are permanent records.*
*Decisions log entries must always include a reference
pointer. A decision without traceable justification
violates Value 1.*