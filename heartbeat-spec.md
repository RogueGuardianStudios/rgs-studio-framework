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
threshold in `state/watchdog/context-threshold.txt`
(written and owned by Spot).

- If usage >= threshold → the hook writes a wake signal
  file (`state/watchdog/spot-wake-[agent-name].signal`)
  to unpause Spot, then exits 2 (block tool call),
  reason written to stderr
- If `context-pct.txt` does not exist → check passes
  (file not yet written, safe default)
- If `context-threshold.txt` does not exist → check
  passes (no Spot assigned, safe default)

The context gate is the link between the agent and
Spot. When the agent's context usage crosses the
threshold, the hook simultaneously freezes the agent
and wakes Spot. Spot then assesses the agent's state,
decides what to do, and adjusts the threshold for the
next wake-up.

**Environment variables:**
- `SPOT_AGENT_NAME` — identifies which state file to
  check for HALT and which wake signal file to write.
  Set by orchestrator at session start.

**Files read:**
- `state/watchdog/spot-[agent-name].md` — HALT flag
- `state/watchdog/context-pct.txt` — current usage
- `state/watchdog/context-threshold.txt` — threshold

**Files written:**
- `state/watchdog/spot-wake-[agent-name].signal` —
  created when threshold is breached. Signals Spot
  to wake up and perform a checkpoint.
---
## What Spot Owns (moved from hooks)
Previously the hook infrastructure handled threshold
comparison and rotation triggers. Now Spot owns all
of this directly:

**Spot's event-driven cycle:**
1. At spin-up, Spot writes an initial threshold to
   `state/watchdog/context-threshold.txt` (e.g., 5%)
2. Spot pauses — waits for the wake signal
3. When the agent's context usage crosses the threshold,
   the PreToolUse hook freezes the agent and writes
   `state/watchdog/spot-wake-[agent-name].signal`
4. Spot wakes up and performs a checkpoint:
   - Reads the watched agent's current work product
   - Reads the governing MD file fresh
   - Assesses behavioral integrity
   - Passes the MD file and any corrective notes to
     the agent
5. Based on the assessment:
   - **On track:** Spot bumps the threshold up
     (e.g., 5% → 10% → 25% → 40%), deletes the wake
     signal, and pauses again. The agent is unfrozen
     because its usage is now below the new threshold.
   - **Needs correction:** Spot passes corrective notes
     alongside the MD file, bumps threshold, deletes
     the wake signal, and pauses. Agent self-corrects.
   - **Needs to stop:** Spot writes the HALT flag to
     the state file. Agent remains frozen permanently
     until human approval.
6. The cycle repeats at each threshold crossing.

**Threshold progression is Spot's judgment call.**
Spot decides how much to bump the threshold based on
the checkpoint assessment. Conservative early
(small bumps), expanding as confidence grows.

This is a cleaner separation:
- **Hooks** handle data capture (statusline), threshold
  enforcement (context gate), and wake signaling
- **Spot** handles all judgment — threshold progression,
  drift detection, rotation decisions, escalation
- **The threshold file** is the control surface between
  hooks and Spot — Spot writes it, hooks read it
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
The context gate is Spot's primary wake-up mechanism:
1. StatusLine writes context % to `context-pct.txt`
   after each assistant message
2. Agent attempts a tool call
3. PreToolUse hook reads `context-pct.txt` and
   `context-threshold.txt`
4. If usage >= threshold → hook writes wake signal
   file (`spot-wake-[agent-name].signal`), then
   exits 2 (tool call blocked)
5. Spot detects the wake signal and performs a
   checkpoint assessment
6. Spot passes the agent its governing MD file and
   any corrective notes
7. If work continues: Spot bumps the threshold in
   `context-threshold.txt`, deletes the wake signal.
   Agent's next tool call passes because usage is now
   below the new threshold.
8. If work must stop: Spot writes the HALT flag.
   Agent remains frozen.

The context gate is not a backup — it is the primary
event-driven trigger for Spot's checkpoint cycle.
Spot does not poll on a timer. Spot wakes only when
the hook signals it.
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
            "command": "bash -c 'AN=\"${SPOT_AGENT_NAME:-_}\"; SF=\"state/watchdog/spot-${AN}.md\"; [ -f \"$SF\" ] && grep -q \"^halt: true\" \"$SF\" && { echo \"HALT: values breach — blocked by Spot\" >&2; exit 2; }; TF=\"state/watchdog/context-threshold.txt\"; CF=\"state/watchdog/context-pct.txt\"; if [ -f \"$CF\" ] && [ -f \"$TF\" ]; then PCT=$(cut -d. -f1 < \"$CF\"); CT=$(cut -d. -f1 < \"$TF\"); [ \"${PCT:-0}\" -ge \"${CT:-90}\" ] && { mkdir -p state/watchdog; touch \"state/watchdog/spot-wake-${AN}.signal\"; echo \"CONTEXT GATE: usage ${PCT}% exceeds ${CT}% threshold — Spot notified\" >&2; exit 2; }; fi; exit 0'"
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
├── watchdog-rules.md                   # Governs watchdog state maintenance
├── context-pct.txt                     # Written by statusline hook
│                                       # Read by PreToolUse hook (context gate)
│                                       # Read by Spot at each checkpoint
│                                       # Contains a single number (usage %)
│                                       # Not a permanent record
├── context-threshold.txt               # Written by Spot (owns threshold)
│                                       # Read by PreToolUse hook (context gate)
│                                       # Contains a single number (threshold %)
│                                       # Updated by Spot after each checkpoint
├── spot-wake-[agent-name].signal       # Written by PreToolUse hook when
│                                       # context gate triggers
│                                       # Read and deleted by Spot after wake
│                                       # Presence = "wake up and checkpoint"
└── spot-[agent-name].md                # One per active Spot instance
                                        # Owned by Spot
                                        # HALT flag read by PreToolUse hook
```
---
## Event-Driven Flow
1. Spot spins up, writes initial threshold to
   `context-threshold.txt` (e.g., `5`), pauses.
2. Agent works normally. StatusLine writes context %
   to `context-pct.txt` after each assistant message.
3. Agent's context usage crosses the threshold.
   PreToolUse hook blocks the tool call, writes
   `spot-wake-[agent-name].signal`.
4. Spot wakes, reads the agent's work product and
   governing MD file, performs checkpoint assessment.
5. Spot passes the governing MD file and any
   corrective notes to the agent.
6. Based on assessment:
   - **On track:** Spot bumps threshold in
     `context-threshold.txt` (e.g., 5 → 10 → 25 → 40),
     deletes the wake signal. Agent's next tool call
     passes because usage is below the new threshold.
     Spot pauses again.
   - **Needs correction:** Same as above, plus
     corrective notes. Agent self-corrects and
     continues working.
   - **Needs to stop:** Spot writes HALT flag to the
     state file. Agent stays frozen. Spot escalates.
7. When Spot determines rotation is needed (based on
   checkpoint cap or its own context judgment), it
   executes the rotation sequence, resets the threshold
   to the initial value, and pauses again.
8. Cycle repeats.

Two things can stop an agent's tool calls:
- **HALT flag** — values breach, written by Spot
- **Context gate** — usage exceeds Spot's threshold
  (temporary — cleared when Spot bumps the threshold)
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
*Document version: 4.0*
*Created: 2026-03-04*
*Updated: 2026-03-12*
*Author: [Your Name]*
*Major change: Zero-script inline hooks. Threshold logic
moved to Spot. Scripts deleted. (v3.0)*
*Added context gate to PreToolUse hook. (v3.1)*
*File-based threshold, event-driven Spot wake, graduated
threshold progression. Replaced env var CONTEXT_THRESHOLD_PCT
with state/watchdog/context-threshold.txt owned by Spot.
Hook now writes wake signal to unpause Spot. (v4.0)*
