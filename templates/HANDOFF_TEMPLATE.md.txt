# HANDOFF_TEMPLATE.md
# Rogue Guardian Studios — Phase Handoff
# This document marks the formal close of one phase
# and the opening of the next.
# It is a checkpoint, not a task instruction.
# All fields are required unless marked optional.


---


## Handoff Metadata


- **Prepared by:** [Agent name/role]
- **Date:** [YYYY-MM-DD]
- **Project:** [Project name]
- **Phase closing:** [e.g. Planning / Build / Review]
- **Phase opening:** [e.g. Build / Review / Merge]
- **Handoff version:** [1.0, 1.1, etc. — increment on update]


---


## Phase Summary


What was accomplished in the closing phase?
Two to four sentences. Outputs only — not process.


---


## Deliverables


List every output produced during this phase.
Each item must be locatable — include file paths or
branch references.


- [Deliverable 1 — what it is, where it lives]
- [Deliverable 2 — what it is, where it lives]
- [Add as needed]


---


## Decisions Made This Phase


Decisions that are now locked. The receiving phase
does not revisit these. Escalate if a locked decision
is believed to be wrong.


- [Decision 1]
- [Decision 2]
- [Add as needed]


---


## Commit Score Log


Running record of evaluation scores from this phase.
Every commit is scored. Work was not blocked by these
scores — they are a record, not a gate.
The final PR review will reference this log.


| Commit | Date | Performance | Alignment | Overall | Flags |
|--------|------|-------------|-----------|---------|-------|
| [ref]  | [date] | [0-100]   | [0-100]   | [avg]   | [any] |
| [ref]  | [date] | [0-100]   | [0-100]   | [avg]   | [any] |


Any score below threshold is flagged here and must be
addressed before the final PR is submitted.


---


## Final PR Status


Has the final PR been submitted for group review?


- [ ] Not yet submitted
- [ ] Submitted — awaiting review
- [ ] Reviewed and approved
- [ ] Reviewed — changes required


Notes: [Any flags raised during group review]


---


## Unresolved Items


Anything that was not resolved during this phase and
must carry forward. Each item needs an owner and a
resolution path.


- [Item 1 — what it is, who owns it, what happens next]
- [Item 2 — what it is, who owns it, what happens next]


If there are no unresolved items, state that explicitly.
An empty section that was not considered is different
from a section that was checked and found empty.


---


## Known Issues Introduced


Problems created or discovered during this phase that
did not exist before it. These go to state/known-issues.md
but are flagged here for the receiving phase's awareness.


- [Issue 1]
- [Issue 2]


---


## Receiving Phase Briefing


What does the next phase need to know to start well?
This is not a full Brief — a Brief will be issued
separately for each agent in the next phase.
This is the phase-level context only.


Two to four sentences.


---


## Handoff Acknowledgement


The lead agent of the receiving phase confirms they
have read this document before work begins.


- [ ] I have read this Handoff in full
- [ ] I have reviewed the commit score log and
      understand any flagged items
- [ ] I have read values.md and evaluation-rubric.md
- [ ] I understand the locked decisions and will
      escalate rather than deviate if I disagree
- [ ] Unresolved items have been assigned and
      resolution paths are understood


Acknowledged by: [Receiving phase lead agent]
Date: [YYYY-MM-DD]


---


## Closing Phase Sign-Off


The transmitting agent confirms this phase is
genuinely complete before handing off.


- [ ] All deliverables are produced and locatable
- [ ] All commit scores are logged
- [ ] All unresolved items have owners and paths
- [ ] The final PR has been submitted or a date
      for submission is documented
- [ ] state/ has been updated to reflect
      phase completion


Confirmed by: [Transmitting agent name/role]
Date: [YYYY-MM-DD]


---


*Handoff prepared under values.md v1.0*
*Both acknowledgement sections must be complete before
this Handoff is considered closed.*
*Final PR requires full group review before merge to main.*
*See handoff-rules.md for usage and maintenance rules.*