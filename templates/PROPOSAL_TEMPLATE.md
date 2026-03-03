# PROPOSAL_TEMPLATE.md
# Rogue Guardian Studios — Improvement Proposal
# This document is the required format for all agent
# improvement proposals. All fields are mandatory.
# A proposal that cannot answer these questions fully
# is not ready to be submitted.

---

## Proposal Metadata

- **Submitted by:** [Agent name/role]
- **Date:** [YYYY-MM-DD]
- **Target:** [The MD or skill file proposed for modification]
- **Proposal version:** [1.0, 1.1, etc. — increment on revision]
- **Status:** [Draft / Submitted / Approved for test /
               Rejected / Merged]

---

## Problem Statement

What specific problem is this proposal solving?
Be precise. "It could be better" is not a problem statement.
Describe the exact friction, failure, or gap encountered,
and when it occurs.

Two to four sentences maximum.

---

## Evidence

What triggered this proposal? Cite specific instances.
Reference pain-points.md entries, failed outputs,
or documented mistakes where relevant.

- [Instance 1 — what happened, when]
- [Instance 2 — what happened, when]
- [Add as needed]

This section must contain at least one concrete example.
A proposal with no evidence is a guess, not a proposal.

---

## Proposed Change

What exactly is being changed and how?
Be specific. Vague proposals cannot be tested.

Attach the full modified file as variant.md alongside
this proposal. Do not paste it inline here.

Summary of the change in plain language:
[Two to four sentences describing what is different
in the variant and why that difference addresses
the problem.]

---

## Justification

Why will this change fix the problem?
Walk through the reasoning explicitly.
"It seemed right" is not a justification.

---

## Predicted Improvement

What specific improvement do you expect to see?
State this in measurable or observable terms.
The witness evaluation will be held against this prediction.

- [Predicted outcome 1]
- [Predicted outcome 2]
- [Add as needed]

---

## Potential Negative Consequences

What could go wrong with this change?
What behaviours might degrade or shift unexpectedly?
What alignment risks does this change introduce?

Do not skip this section. A proposal that claims no
possible downsides has not been thought through.

- [Risk 1]
- [Risk 2]
- [Add as needed]

---

## Test Cases

What tasks should the witness agent run to evaluate
this proposal? Tests must be sufficient to surface both
the predicted improvement and any potential negative
consequences identified above.

Attach full test cases as test-cases.md alongside
this proposal.

Summary of test coverage:
- [Test 1 — what it is testing for]
- [Test 2 — what it is testing for]
- [Add as needed]

---

## Evaluation Criteria

How will we know if this worked?
Define what a clear pass, a clear fail, and a
"better but with consequences" result looks like
for this specific proposal, before the test runs.

- Pass condition: [Specific, observable outcome]
- Fail condition: [Specific, observable outcome]
- Flag condition: [What would indicate improvement
                  alongside unintended consequences]

---

## Submitting Agent Declaration

- [ ] I have documented at least one concrete instance
      that evidences the problem
- [ ] I have attached variant.md with the full
      modified file
- [ ] I have attached test-cases.md
- [ ] I have genuinely considered potential negative
      consequences and documented them honestly
- [ ] I have defined evaluation criteria before
      submission, not after

Submitted by: [Agent name/role]
Date: [YYYY-MM-DD]

---

## Studio Owner Review

- [ ] Problem statement is valid and evidenced
- [ ] Proposed change is specific enough to test
- [ ] Test cases are sufficient to evaluate both
      performance and alignment
- [ ] Approved for witness evaluation

Decision: [Approved / Rejected / Needs revision]
Reason if rejected or revised: [Notes]

Reviewed by: Studio Owner
Date: [YYYY-MM-DD]

---

*Proposal submitted under values.md v1.0*
*No witness test runs without studio owner approval.*
*Evaluation rubric applies to all witness test outputs.*

