# Environment Rules
# Governs how environment scripts are set up,
# configured, and maintained.
# These files are owned by the human.
# They are not evolvable through the normal
# agent improvement proposal process.
---

## Ownership

All files in environment/ are owned by the human.
Agents do not modify, extend, or propose changes to
these files through the normal improvement proposal
process. Changes require direct human action.

---

## Files

**environment-rules.md**
This document.

## Hooks

Context monitoring hooks are configured as inline
commands in Claude Code settings. No script files.
See `heartbeat-spec.md` for the full specification
and configuration JSON.

**StatusLine hook** — inline bash + jq command.
Writes context usage percentage to
`state/watchdog/context-pct.txt` after each
assistant message. Also checks the dynamic threshold
(from `state/watchdog/context-threshold.txt`) and
spawns Spot as a background subprocess when usage
exceeds the threshold (guarded by `spot.lock`).

**PreToolUse hook** — inline bash command.
Two checks before every tool call:
1. HALT flag in Spot state files — blocks if active
2. Context gate — blocks if context usage exceeds
   the dynamic threshold from
   `state/watchdog/context-threshold.txt` (clamped
   to the hard ceiling from `CONTEXT_THRESHOLD_PCT`)

## Environment Variables

Set by the orchestrator at session start:

- `SPOT_AGENT_NAME` — identifies the Spot state file
  for this agent's session. Used by the PreToolUse
  hook to find the HALT flag.
- `CONTEXT_THRESHOLD_PCT` — integer percentage for
  the **hard ceiling**. Default 90 if not set. The
  dynamic threshold from `context-threshold.txt` is
  clamped to this value. This is the absolute backstop
  that the dynamic threshold can never exceed. The
  actual gating threshold is managed dynamically by
  Spot via `state/watchdog/context-threshold.txt`.

## State Files (managed by hooks and Spot)

The following files in `state/watchdog/` are part of
the hook infrastructure. See `heartbeat-spec.md` and
`state/watchdog/watchdog-rules.md` for full details:

- `context-pct.txt` — written by StatusLine hook
- `context-threshold.txt` — written by Spot, read by
  both hooks. Initial value set by orchestrator
  (default 15).
- `spot.lock` — PID lock preventing concurrent Spot
  instances
- `spot-notes-[agent-name].md` — Spot's assessment
  and agent communication channel
- `spot-[agent-name].md` — Spot state file

---

*Document version: 3.0*
*Created: 2026-03-05*
*Updated: 2026-03-12*
*Author: [Your Name]*
*Owned by: human — not subject to agent proposals*
*Major change: CONTEXT_THRESHOLD_PCT is now hard ceiling.
Dynamic threshold managed by Spot via context-threshold.txt.
StatusLine hook now spawns Spot. (v3.0)*
