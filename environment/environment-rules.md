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
assistant message.

**PreToolUse hook** — inline bash command.
Two checks before every tool call:
1. HALT flag in Spot state files — blocks if active
2. Context gate — blocks if context usage exceeds
   `CONTEXT_THRESHOLD_PCT` (default 90%)

## Environment Variables

Set by the orchestrator at session start:

- `SPOT_AGENT_NAME` — identifies the Spot state file
  for this agent's session. Used by the PreToolUse
  hook to find the HALT flag.
- `CONTEXT_THRESHOLD_PCT` — integer percentage for
  the context gate hard limit. Default 90 if not set.

---

*Document version: 2.0*
*Created: 2026-03-05*
*Updated: 2026-03-12*
*Author: [Your Name]*
*Owned by: human — not subject to agent proposals*
