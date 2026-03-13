# Context Hooks Specification
# This document defines the hook-based context monitoring
# infrastructure. The hooks are inline shell commands
# configured in Claude Code settings. No script files.
# They measure and gate. Everything that requires
# judgment belongs to Spot or the orchestrator.
---
## What the Context Hooks Are
Two inline Claude Code hooks that together implement
the **dynamic threshold pipeline**:

**StatusLine** — an inline command that runs after each
assistant message. Captures context window usage, writes
it to a plain text file, and spawns Spot when usage
exceeds the dynamic threshold.

**PreToolUse** — an inline command that runs before
every tool call. Two checks: (1) HALT flag in the Spot
state file, (2) context usage against the dynamic
threshold file. Blocks the tool call if either check
fails.

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
## The Dynamic Threshold Pipeline
The hooks implement a **threshold ratchet** that creates
natural checkpoint intervals tied to context consumption:

```
Agent acts → StatusLine writes context-pct.txt
          → StatusLine checks: pct >= context-threshold.txt?
               NO  → agent continues uninterrupted
               YES → agent pauses (PreToolUse blocks)
                   → StatusLine spawns Spot as background subprocess
                   → Spot reads work product + governing MD + checkpoints
                   → CLEAN: raise threshold +15, pass agent its MD file,
                     tell it to continue. Agent unblocks.
                   → MINOR ISSUES: raise threshold +15, pass agent its
                     MD file + list of concerns. Agent unblocks and
                     continues with awareness of issues.
                   → MAJOR ISSUES / PERSISTENT MINOR: Spot issues HALT,
                     summarizes all issues, human gets involved.
                   → COMPRESSION NEEDED (high context): Spot evaluates
                     one last time, facilitates compression via
                     checkpoint history, then agent respins.
```

### Threshold ladder
Initial: 15% → 30% → 45% → 60% → 75% → 85%
(capped at `CONTEXT_THRESHOLD_PCT - 5`)

- Fixed increment: +15 points per checkpoint
- Hard ceiling: `CONTEXT_THRESHOLD_PCT` env var (default
  90%) — absolute backstop the dynamic threshold never
  exceeds
- If context jumps past threshold + increment in a single
  message: Spot raises to `current_usage + 5` instead of
  the standard +15
- Threshold is raised on both clean checks AND minor
  issues — the agent always resumes unless HALT
- On HALT the threshold is not raised. The agent stays
  blocked until the human intervenes.

### Why the ratchet works
The threshold starts low so Spot checks the agent early.
Each clean checkpoint earns more headroom. The agent is
only paused briefly for Spot's review — seconds, not
minutes. This ties oversight to actual context consumption
rather than wall-clock time. A fast-working agent gets
checked more often. A slow agent gets checked less.
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
4. Reads the current threshold from
   `state/watchdog/context-threshold.txt` (default 15)
5. If usage >= threshold AND no active Spot instance
   (checked via `spot.lock`): spawns Spot as a background
   subprocess
6. Outputs a display string showing usage and threshold

**Output file:** `state/watchdog/context-pct.txt`

Contains a single number (e.g., `23.5`). Nothing else.
This is the only file the statusline writes directly.
The statusline also spawns Spot when threshold is
exceeded — this is the only agent-spawning action
the hooks perform.

**Lock file:** `state/watchdog/spot.lock`

Before spawning Spot the statusline checks for an
existing lock file. If one exists, it checks whether
the PID inside is still running (`kill -0`). If the
PID is stale, the lock is removed and Spot is spawned.
If the PID is active, no spawn occurs. This prevents
concurrent Spot instances.

The statusline does not make decisions. It writes data
and spawns Spot when the threshold condition is met.
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
The hook reads the dynamic threshold from
`state/watchdog/context-threshold.txt` (default 15 if
the file does not exist). It clamps this value to the
hard ceiling from `CONTEXT_THRESHOLD_PCT` (default 90%).
It then reads `state/watchdog/context-pct.txt` (written
by the StatusLine hook after each assistant message).

- If usage >= threshold → exit 2 (block tool call),
  message: "waiting for Spot review"
- If `context-pct.txt` does not exist → check passes
  (file not yet written, safe default)
- If `context-threshold.txt` does not exist → threshold
  defaults to 15 (conservative — Spot will be spawned
  early)

The context gate is a checkpoint trigger. When the
agent hits the threshold, it pauses. Spot spins up
(spawned by the StatusLine hook), runs its assessment,
raises the threshold, and the agent resumes on its
next tool call.

**Environment variables:**
- `SPOT_AGENT_NAME` — identifies which state file to
  check for HALT. Set by orchestrator at session start.
- `CONTEXT_THRESHOLD_PCT` — integer percentage for the
  hard ceiling. Default 90 if not set. The dynamic
  threshold from `context-threshold.txt` is clamped to
  this value. Set by orchestrator at session start.

The hook does not write to any files. It does not
make rotation decisions. Those are Spot's
responsibilities.
---
## What Spot Owns (moved from hooks)
Previously the hook infrastructure handled threshold
comparison and rotation triggers. Now Spot owns all
judgment directly, and the hooks own the gate:

**The hooks:**
- Capture data (StatusLine writes context-pct.txt)
- Enforce the gate (PreToolUse blocks when threshold
  exceeded or HALT flag set)
- Spawn Spot (StatusLine spawns when threshold exceeded)

**Spot (spawned on-demand by StatusLine hook):**
1. Reads the watched agent's actual work product
2. Reads the governing MD file fresh
3. Reads `state/watchdog/context-pct.txt` for current
   context usage
4. Reads `state/watchdog/context-threshold.txt` for
   the current threshold
5. Reads checkpoint history from the state file
6. Assesses the agent against its governing boundaries
7. **Clean or minor drift:** raises threshold by +15
   (capped at CEIL-5), writes agent's MD file and any
   corrective notes to `spot-notes-[agent-name].md`,
   agent resumes
8. **Major issues or persistent minor drift (3+
   consecutive):** writes HALT flag, summarizes all
   issues, escalates to human
9. **Compression zone reached:** evaluates agent one
   last time, facilitates compression, resets threshold
   to initial value (15)

This is a cleaner separation:
- **Hooks** handle data capture, gating, and Spot spawn
- **Spot** handles all judgment — assessment, threshold
  adjustment, drift detection, compression, escalation
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
The context gate works through the dynamic threshold:
1. StatusLine writes context % to `context-pct.txt`
   after each assistant message
2. StatusLine checks: is usage >= threshold in
   `context-threshold.txt`?
3. If yes: spawns Spot (if not already running)
4. Agent attempts a tool call
5. PreToolUse hook reads `context-threshold.txt`
   (clamped to hard ceiling)
6. If usage >= threshold → hook exits 2, tool call
   blocked, message: "waiting for Spot review"
7. Spot runs its assessment, raises the threshold
8. Agent's next tool call: PreToolUse reads the new
   (higher) threshold. Usage is now below threshold.
   Gate opens. Agent continues.

Unlike HALT enforcement, the context gate is temporary.
Spot always raises the threshold after clean or minor
assessments. The agent resumes with its full context
intact — no context loss.
---
## Hook Configuration
Add to `.claude/settings.json` or project settings:
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
No script files to install. No dependencies beyond
bash and jq (both standard in Claude Code environments).
The `claude` CLI must be available for Spot spawn.
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
├── context-threshold.txt      # Dynamic threshold (single integer)
│                              # Written by Spot (raises after checkpoint)
│                              # Read by StatusLine (spawn check)
│                              # Read by PreToolUse (context gate)
│                              # Initial value set by orchestrator
│                              # Default 15 if missing
├── spot.lock                  # PID of active Spot subprocess
│                              # Created by StatusLine spawn logic
│                              # Cleaned up by Spot on exit (trap EXIT)
│                              # Stale PIDs detected via kill -0
├── spot-notes-[agent-name].md # Spot's assessment + agent MD re-injection
│                              # Written by Spot after each checkpoint
│                              # Read by agent after gate lifts
│                              # Contains governing MD + corrective notes
└── spot-[agent-name].md       # One per active Spot instance
                               # Owned by Spot
                               # HALT flag read by PreToolUse hook
```
---
## Rotation Flow
1. Agent works normally. StatusLine writes context %
   to `context-pct.txt` after each assistant message.
2. When context usage reaches the current dynamic
   threshold (from `context-threshold.txt`), the
   PreToolUse hook blocks further tool calls — the
   agent is paused.
3. StatusLine spawns Spot as a background subprocess.
4. Spot reads the agent's work product, governing MD,
   checkpoint history, and current context usage.
5. **Clean or minor issues:** Spot raises threshold
   by +15 (or to `current_usage + 5` on a jump),
   writes notes to `spot-notes-[agent-name].md`,
   cleans up lock file, exits. Agent's next tool call
   passes the gate. Agent reads notes and continues.
6. **Major issues / persistent minor (3+ consecutive):**
   Spot writes HALT flag. Agent stays blocked. Human
   is notified with a full summary of issues.
7. **Compression zone (threshold would exceed CEIL-10):**
   Spot runs a final checkpoint, facilitates compression
   per normal rotation sequence, resets threshold to
   initial value (15). Agent respins with compressed
   seed. Monitoring continues from generation N+1.

Three things can stop an agent's tool calls:
- **HALT flag** — values breach or persistent drift,
  written by Spot
- **Context gate** — usage exceeds dynamic threshold,
  temporary until Spot raises it
- **Hard ceiling** — usage exceeds `CONTEXT_THRESHOLD_PCT`
  (default 90%), absolute backstop
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
- Trigger rotation (Spot facilitates compression)
- Write to Spot state files
- Interact with agents beyond approve/block/spawn
- Evaluate output quality
- Survive session end — they run within the session.
  State files persist. The hooks do not.
---
*Document version: 4.0*
*Created: 2026-03-04*
*Updated: 2026-03-12*
*Author: [Your Name]*
*Major change: Dynamic threshold pipeline. Spot spawned
on-demand by StatusLine hook. Threshold ratchet replaces
static env var gate. (v4.0)*
