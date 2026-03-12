# Context Hooks Specification
# This document defines the hook-based context monitoring
# infrastructure. The hooks are inline shell commands
# configured in Claude Code settings. No script files.
# They measure and gate. Everything that requires
# judgment belongs to Spot or the orchestrator.
---
## What the Context Hooks Are
Two inline Claude Code hooks that together replace the
need for a background heartbeat process:

**StatusLine** — an inline command that runs after each
assistant message. Captures context window usage and
writes it to a plain text file Spot can read.

**PreToolUse** — an inline command that runs before
every tool call. Two checks: (1) HALT flag in the Spot
state file, (2) context usage against a hard threshold.
Blocks the tool call if either check fails.

No script files. No background processes. No polling.
The hooks are configured entirely in Claude Code
settings as inline bash commands.
---
## Why Hooks Instead of a Heartbeat
The original design used a background heartbeat process
polling every 30 seconds. Hooks are better because:

1. **Simpler** — no background daemon, no script files,
   no dependencies beyond bash and jq
2. **Enforcement** — the PreToolUse hook blocks tool
   calls immediately on HALT. The agent cannot bypass it.
3. **Native** — hooks are a built-in Claude Code feature.
   No custom infrastructure to maintain.
4. **No idle-agent problem** — an idle agent is not
   consuming context. Monitoring only matters when the
   agent is active, which is when hooks fire.
---
## StatusLine Hook
The statusline receives the full Claude Code session
JSON on stdin after each assistant message. It contains:
- context_window.used_percentage
- context_window.remaining_percentage
- context_window.total_input_tokens
- context_window.context_window_size

The statusline command:
1. Reads the JSON from stdin
2. Extracts `context_window.used_percentage`
3. Writes the value to `state/watchdog/context-pct.txt`
4. Outputs a display string for the status bar

**Output file:** `state/watchdog/context-pct.txt`

Contains a single number (e.g., `23.5`). Nothing else.
This is the only file the statusline writes.
Spot reads this file at each checkpoint to track
the watched agent's context consumption.

The statusline does not make decisions. It writes data.
---
## PreToolUse Hook
The PreToolUse hook runs before every tool call.
It checks two things in sequence:

**1. HALT check**
The hook reads `state/watchdog/spot-[agent-name].md`
where `[agent-name]` comes from the `SPOT_AGENT_NAME`
environment variable set by the orchestrator at
session start.

- If `halt: true` is found → exit 2 (block tool call),
  reason written to stderr

If `SPOT_AGENT_NAME` is not set, the file path won't
match anything. The HALT check passes. Safe default for
sessions without Spot monitoring.

**2. Context gate**
The hook reads `state/watchdog/context-pct.txt`
(written by the StatusLine hook after each assistant
message). It compares the current usage against the
`CONTEXT_THRESHOLD_PCT` environment variable (set by
the orchestrator at session start, default 90%).

- If usage >= threshold → exit 2 (block tool call),
  reason written to stderr
- If `context-pct.txt` does not exist → check passes
  (file not yet written, safe default)

The context gate is a circuit breaker. It prevents
the agent from consuming more context past the hard
limit. Spot still owns the rotation decision — the
gate just freezes the agent until Spot wakes up and
triggers rotation.

**Environment variables:**
- `SPOT_AGENT_NAME` — identifies which state file to
  check for HALT. Set by orchestrator at session start.
- `CONTEXT_THRESHOLD_PCT` — integer percentage for the
  context gate. Default 90 if not set. Set by
  orchestrator at session start.

The hook does not write to any files. It does not
make rotation decisions. Those are Spot's
responsibilities.
---
## What Spot Owns (moved from hooks)
Previously the hook infrastructure handled threshold
comparison and rotation triggers. Now Spot owns all
of this directly:

**At each checkpoint, Spot:**
1. Reads `state/watchdog/context-pct.txt` for the
   watched agent's current context usage
2. Compares against `agent_context_at_last_rotation`
   plus `rotation_threshold_percent` from the state file
3. If threshold reached → triggers rotation
4. On values breach → writes HALT flag to state file
   (enforced automatically by the PreToolUse hook)

This is a cleaner separation:
- **Hooks** handle data capture (statusline) and
  hard stops (HALT enforcement + context gate)
- **Spot** handles all judgment — threshold tuning,
  drift detection, rotation decisions, escalation
---
## HALT Enforcement
When Spot writes a HALT flag to the state file:
1. The agent's next tool call hits the PreToolUse hook
2. Hook reads `halt: true` from the state file
3. Hook exits 2 — tool call blocked, reason on stderr
4. Every subsequent tool call is also blocked
5. The agent cannot perform any action until the
   human approves clearing the HALT flag
6. Spot clears the flag after human approval
7. Hook reads the cleared state file and exits 0

This is involuntary enforcement. The agent does not
need to check for HALT flags. The hook does it.
---
## Context Gate Enforcement
The context gate works the same way as HALT enforcement
but triggers on context usage instead of a values breach:
1. StatusLine writes context % to `context-pct.txt`
   after each assistant message
2. Agent attempts a tool call
3. PreToolUse hook reads `context-pct.txt`
4. If usage >= `CONTEXT_THRESHOLD_PCT` (default 90%) →
   hook exits 2, tool call blocked
5. Every subsequent tool call is also blocked
6. Spot wakes at next checkpoint, sees threshold
   exceeded, triggers rotation
7. After rotation, context resets. StatusLine writes
   the new (lower) percentage. Gate opens.

The context gate is a backup to Spot's checkpoint-based
threshold check. Spot checks every 5 minutes. The hook
checks every tool call. Between Spot's checks, the gate
prevents the agent from consuming context past the limit.
---
## Hook Configuration
Add to `.claude/settings.json` or project settings:
```json
{
  "statusLine": {
    "type": "command",
    "command": "bash -c 'D=$(cat); mkdir -p state/watchdog; echo \"$D\" | jq -r \".context_window.used_percentage // empty\" > state/watchdog/context-pct.txt; echo \"$D\" | jq -r \"\\\"Ctx: \\\\(.context_window.used_percentage // 0)%\\\"\"'"
  },
  "hooks": {
    "PreToolUse": [
      {
        "matcher": "",
        "hooks": [
          {
            "type": "command",
            "command": "bash -c 'SF=\"state/watchdog/spot-${SPOT_AGENT_NAME:-_}.md\"; [ -f \"$SF\" ] && grep -q \"^halt: true\" \"$SF\" && { echo \"HALT: values breach — blocked by Spot\" >&2; exit 2; }; CT=\"${CONTEXT_THRESHOLD_PCT:-90}\"; CF=\"state/watchdog/context-pct.txt\"; if [ -f \"$CF\" ]; then PCT=$(cut -d. -f1 < \"$CF\"); [ \"${PCT:-0}\" -ge \"$CT\" ] && { echo \"CONTEXT GATE: usage exceeds ${CT}% threshold — rotation required\" >&2; exit 2; }; fi; exit 0'"
          }
        ]
      }
    ]
  }
}
```
No script files to install. No dependencies beyond
bash and jq (both standard in Claude Code environments).
---
## Files Used by the Hook Infrastructure
```
state/watchdog/
├── watchdog-rules.md          # Governs watchdog state maintenance
├── context-pct.txt            # Written by statusline hook
│                              # Read by Spot at each checkpoint
│                              # Read by PreToolUse hook (context gate)
│                              # Contains a single number (usage %)
│                              # Not a permanent record
└── spot-[agent-name].md       # One per active Spot instance
                               # Owned by Spot
                               # HALT flag read by PreToolUse hook
```
---
## Rotation Flow
1. Agent works normally. StatusLine writes context %
   to `context-pct.txt` after each assistant message.
2. If context usage reaches the hard threshold
   (`CONTEXT_THRESHOLD_PCT`, default 90%), the
   PreToolUse hook blocks further tool calls
   immediately — the agent is frozen.
3. Spot checks at its configured interval. Reads
   `context-pct.txt` and compares against its own
   rotation threshold (`rotation_threshold_percent`).
4. When threshold reached, Spot triggers rotation
   per its normal rotation sequence.
5. After rotation, Spot resets
   `agent_context_at_last_rotation` in the state file.
6. StatusLine writes the new context % after the
   respun agent's first message. Context gate opens.
7. Monitoring continues.

Two things can stop an agent's tool calls:
- **HALT flag** — values breach, written by Spot
- **Context gate** — usage exceeds hard threshold
---
## Empirical Calibration Values
Two values must be measured during validation testing.
These inform Spot's checkpoint cap calculation and are
stored in the Spot state file at assignment:

**compression_headroom**
How much of Spot's context window is consumed by a
full rotation cycle — reading all checkpoints, reading
agent output, constructing the seed, verifying it,
and executing both respins.
Measured during Test Case 5 of the validation spec.

**average_checkpoint_size**
How much of Spot's context window is consumed by a
single checkpoint review and state file entry.
Measured during Test Case 5 of the validation spec.

Until empirical values are available use:
- compression_headroom: 40% of Spot's max context
- average_checkpoint_size: 5% of Spot's max context
- Resulting default checkpoint cap: 8

These defaults are conservative by design.
---
## What the Hooks Do Not Do
- Reason or make judgment calls
- Trigger rotation (the context gate blocks, Spot rotates)
- Write to Spot state files
- Interact with agents beyond approve/block
- Evaluate output quality
- Survive session end — they run within the session.
  State files persist. The hooks do not.
---
*Document version: 3.1*
*Created: 2026-03-04*
*Updated: 2026-03-12*
*Author: [Your Name]*
*Major change: Zero-script inline hooks. Threshold logic
moved to Spot. Scripts deleted. (v3.0)*
*Added context gate to PreToolUse hook. (v3.1)*
