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
Checks for HALT flag in Spot state files before
every tool call. Blocks if HALT is active.

---

*Document version: 2.0*
*Created: 2026-03-05*
*Updated: 2026-03-12*
*Author: [Your Name]*
*Owned by: human — not subject to agent proposals*
