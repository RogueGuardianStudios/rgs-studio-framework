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

**context-gate.py**
PreToolUse hook. Runs before every tool call.
Checks HALT flags, rotation triggers, and context
thresholds. Approves or blocks tool use.
See `heartbeat-spec.md` for the full specification.

**context-reporter.py**
StatusLine hook. Runs after each assistant message.
Captures context window metrics and writes them
atomically to `state/watchdog/context-metrics.json`.
See `heartbeat-spec.md` for the full specification.

---

*Document version: 2.0*
*Created: 2026-03-05*
*Updated: 2026-03-12*
*Author: [Your Name]*
*Owned by: human — not subject to agent proposals*
