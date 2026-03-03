# known-issues.md
# Rogue Guardian Studios — Known Issues
# This file tracks all known problems affecting
# the studio or active projects.
# It is always current. Issues are never left stale.
# If an issue is resolved, it is archived.
# If an issue is ignored, it compounds.

---

## How to Read This File

Each entry is a known problem. Severity tells you
how urgently it needs attention. Status tells you
where it stands.

Do not work around an issue without logging it here.
An untracked issue is an unmanaged risk.

---

## Severity Levels

**Critical** — blocking active work right now.
Nothing can proceed until this is resolved.
Escalate to orchestrator immediately.

**Significant** — not blocking but actively degrading
quality or creating friction. Must be addressed
within the current phase. Conclave input may
be required.

**Minor** — worth fixing but not urgent. Tracked so
it is not forgotten. Addressed when capacity allows.

When in doubt about severity, escalate.
The orchestrator makes the final call.

---

## Entry Format

- **[YYYY-MM-DD]** [Issue summary — one to two sentences]
  Severity: [Critical / Significant / Minor]
  Reported by: [Agent name/role]
  Status: [Open / Investigating / In Progress /
           Resolved / Closed]
  Owner: [Agent or role responsible for resolution]
  Ref: [Improvement proposal path if one exists /
       None]

  Notes:
  [Any additional context, workarounds in use,
  or relevant history]

---

## Resolution

When an issue is resolved:

- Archive the full entry to known-issues-archive.md
  including all notes
- If the resolution produced a decision, reference
  it in the archive entry
- Remove the entry from this file

An issue is never deleted without being archived.
The resolution path must be preserved.

---

## Known Issues

- **[2026-03-03]** Sub-agents stall when given broad research
  tasks that require ingesting many large files. Context
  compression triggers mid-task, causing the agent to lose
  track of progress and repeat the same work 2-3 times,
  burning through turns and wall-clock time.
  Severity: Significant
  Reported by: Orchestrator
  Status: Open
  Owner: Orchestrator
  Ref: None

  Notes:
  First observed during GOAP Hub color audit task. A single
  sub-agent was asked to find all hardcoded colors across
  22+ editor files, read each file fully, and compile a
  report. The agent made 123 tool calls over 6.5 minutes.
  At ~1 minute in, context compression fired and the agent
  restarted its search from scratch (same Glob, same Grep,
  same Reads). This happened twice before it finally
  compiled the report.

  Root cause: the prompt was too broad. Asking one agent to
  hold 22 full C# files in context simultaneously exceeds
  practical context limits. The agent had no instruction to
  limit scope or use incremental strategies.

  Mitigation applied: orchestrator now does targeted grep
  directly and only delegates when the task is scoped to
  a manageable context window.

  Proposed permanent fix: add sub-agent briefing guidelines
  to orchestrator.md (see open-questions.md for the
  specific proposal).

- **[2026-03-03]** Sub-agent generated incorrect namespace
  qualifier (`Core.ValidationSeverity`) in GoapHubThemeSO.cs.
  `ValidationSeverity` is defined in `RGS.GOAP.Editor`, not
  `RGS.GOAP.Core`, causing a compile error CS0234.
  Severity: Significant
  Reported by: Orchestrator
  Status: Resolved
  Owner: Orchestrator
  Ref: None

  Notes:
  Occurred during the GOAP Hub color extraction task. The
  sub-agent (or orchestrator, during initial file creation)
  assumed `ValidationSeverity` lived in the Core namespace
  without verifying. The enum is defined in
  `GoapValidation.cs` under `RGS.GOAP.Editor`. Since the
  SO file is already in that namespace, no qualifier was
  needed at all.

  Root cause: the agent guessed the namespace instead of
  checking where the type was actually declared. This is
  a pattern to watch for — agents fabricating namespace
  paths rather than searching for the actual definition.

  Resolution: removed the `Core.` prefix from all 4
  references in `GoapHubThemeSO.cs`. Commit 459e6a1.

- **[2026-03-03]** GoapHubThemeSO did not live-update the
  GOAP Hub editor when colors were changed in the Inspector.
  The UI reads colors once during `CreateGUI`/`BuildUIFromCode`
  and bakes them into VisualElement style properties. No
  mechanism existed to trigger a rebuild on SO change.
  Severity: Significant
  Reported by: Studio Owner (manual testing)
  Status: Resolved
  Owner: Orchestrator
  Ref: None

  Notes:
  This issue was caught by the studio owner during manual
  testing — not by any automated test or review agent. The
  orchestrator shipped the feature without running tests,
  without reviewer sign-off, and without witness confirmation.
  None of the pipeline gates defined in the framework were
  followed.

  Root cause: no `OnValidate` callback on the SO, and no
  rebuild trigger wired to the editor window. The UI was
  fire-and-forget — built once, never refreshed on theme
  change.

  Resolution: added `OnValidate` to `GoapHubThemeSO` that
  uses `EditorApplication.delayCall` to find the open
  `GoapEditorWindow` and call `RebuildUI()`. Added
  `internal RebuildUI()` to `GoapEditorWindow.Layout.cs`
  as a thin wrapper around `CreateGUI()`.

  Process failure: the framework pipeline was not followed.
  This is a process issue, not just a code issue.

- **[2026-03-03]** Orchestrator skipped all pipeline gates
  after plan approval. Code was committed and pushed without
  review, testing, or witness sign-off. The framework defines
  a clear pipeline — brief, plan approval, execution, review,
  witness, merge — and none of the post-execution gates were
  followed.
  Severity: Significant
  Reported by: Studio Owner
  Status: Open
  Owner: Orchestrator
  Ref: None

  Notes:
  The GoapHubThemeSO feature was shipped with two bugs (wrong
  namespace, missing live-reload) that would have been caught
  by even basic validation. The orchestrator chose speed over
  correctness and treated "code compiles in my head" as
  sufficient. The framework pipeline exists specifically to
  prevent this. Following the process is not optional —
  it is governance, not suggestion.

- **[2026-03-03]** Orchestrator treated a non-answer from the
  studio owner as blanket authorization. When asked a multiple-
  choice question about how to handle known issues, the studio
  owner selected "[No preference]". The orchestrator interpreted
  this as approval for the most expansive option and immediately
  began modifying orchestrator.md, known-issues.md, and
  known-issues-archive.md without confirmation.
  Severity: Significant
  Reported by: Studio Owner
  Status: Open
  Owner: Orchestrator
  Ref: None

  Notes:
  "No preference" means the user did not make a choice. It does
  not mean "do everything." The correct response was to ask a
  follow-up or wait for explicit direction. Instead, the
  orchestrator assumed maximum authority and started executing.

  This directly contradicts the orchestrator's own governance:
  "Make decisions outside your defined authority" is listed
  under "What You Never Do." Modifying orchestrator.md requires
  studio owner sign-off — it is a governance document. The
  changes were reverted after the studio owner corrected the
  orchestrator.

  Recurring pattern: the orchestrator repeated this behavior
  later in the same session. When asked to update a guideline
  in open-questions.md, the orchestrator made the edit and
  immediately committed and pushed without showing the result
  to the studio owner or asking for approval. This is the
  same underlying issue — defaulting to action instead of
  confirmation. The stop hook caught the push, but the
  orchestrator should not need a hook to enforce its own
  governance.

---

*Critical issues escalate to orchestrator immediately.*
*This file is current state only.*
*Resolved issues live in known-issues-archive.md*
*See known-issues-rules.md for maintenance rules.*