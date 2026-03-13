# Claude Code Settings

This document describes the Claude Code `settings.json` configuration used by the RGS Studio Framework. The actual settings live in `.claude/settings.json`.

## Overview

The settings configure two integrated systems:

1. **Status Line** — A live context-window usage monitor displayed in the Claude Code status bar.
2. **PreToolUse Hook** — A gate that runs before every tool call to enforce safety thresholds.

---

## Status Line

**Type:** `command`

The status line runs a bash command that receives Claude's internal state as JSON on stdin. It performs the following:

1. **Extracts** the current context-window usage percentage from the JSON payload.
2. **Writes** the percentage to `state/watchdog/context-pct.txt` so other components can read it.
3. **Reads the threshold** from `state/watchdog/context-threshold.txt` (defaults to `15%` if the file doesn't exist).
4. **Launches Spot** (the watchdog agent via `claude --agent agents/spot.md`) in the background if the context usage meets or exceeds the threshold — but only if Spot isn't already running (tracked via `state/watchdog/spot.lock`).
5. **Displays** a formatted status string like `Ctx: 42% / 15%` showing current usage vs. threshold.

---

## PreToolUse Hook

**Matcher:** `""` (matches all tools)

A gate that runs before every tool invocation. It enforces two checks:

### 1. Spot Halt Check
- Looks for a Spot agent state file at `state/watchdog/spot-${SPOT_AGENT_NAME}.md`.
- If that file contains `halt: true`, the tool call is **blocked** with the message: `HALT: values breach — blocked by Spot`.

### 2. Context Threshold Gate
- Reads the current threshold from `state/watchdog/context-threshold.txt` (defaults to `15%`).
- Caps the threshold at the `CONTEXT_THRESHOLD_PCT` environment variable (defaults to `90%`).
- Reads the latest context usage from `state/watchdog/context-pct.txt`.
- If usage **meets or exceeds** the threshold, the tool call is **blocked** with: `CONTEXT GATE: X% >= Y% threshold — waiting for Spot review`.

This prevents the agent from continuing work when the context window is filling up, giving Spot a chance to review and intervene.

---

## settings.json

The raw JSON configuration:

```json
{
  "statusLine": {
    "type": "command",
    "command": "bash -c 'D=$(cat); mkdir -p state/watchdog; PCT=$(echo \"$D\" | jq -r \".context_window.used_percentage // empty\"); echo \"$PCT\" > state/watchdog/context-pct.txt; CT=15; TF=\"state/watchdog/context-threshold.txt\"; [ -f \"$TF\" ] && CT=$(cat \"$TF\"); LF=\"state/watchdog/spot.lock\"; IP=$(cut -d. -f1 <<< \"${PCT:-0}\"); if [ \"${IP:-0}\" -ge \"$CT\" ]; then if [ -f \"$LF\" ]; then kill -0 \"$(cat \"$LF\")\" 2>/dev/null || rm -f \"$LF\"; fi; if [ ! -f \"$LF\" ]; then ( claude --agent agents/spot.md & echo $! > \"$LF\"; wait; rm -f \"$LF\" ) &  fi; fi; echo \"$D\" | jq -r \"\\\"Ctx: \\\\(.context_window.used_percentage // 0)% / ${CT}%\\\"\"'"
  },
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "bash -c 'SF=\"state/watchdog/spot-${SPOT_AGENT_NAME:-_}.md\"; [ -f \"$SF\" ] && grep -q \"^halt: true\" \"$SF\" && { echo \"HALT: values breach — blocked by Spot\" >&2; exit 2; }; CT=15; TF=\"state/watchdog/context-threshold.txt\"; [ -f \"$TF\" ] && CT=$(cat \"$TF\"); CEIL=\"${CONTEXT_THRESHOLD_PCT:-90}\"; [ \"$CT\" -gt \"$CEIL\" ] && CT=\"$CEIL\"; CF=\"state/watchdog/context-pct.txt\"; if [ -f \"$CF\" ]; then PCT=$(cut -d. -f1 < \"$CF\"); [ \"${PCT:-0}\" -ge \"$CT\" ] && { echo \"CONTEXT GATE: ${PCT}% >= ${CT}% threshold — waiting for Spot review\" >&2; exit 2; }; fi; exit 0'"
          }
        ]
      }
    ]
  }
}
```
