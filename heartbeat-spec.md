# Context Hooks Specification
# This document defines the hook-based context monitoring
# infrastructure. The hooks are not agents. They do not reason.
# They are infrastructure — lightweight scripts that run
# as Claude Code hooks within each agent session.
# They measure, compare, and gate. Everything that requires
# judgment belongs to Spot or the orchestrator.
---
## What the Context Hooks Are
Two Claude Code hooks that together replace the need for
a background heartbeat process:

**Context Reporter** (`environment/context-reporter.py`)
A StatusLine hook. Runs after each assistant message.
Captures context window metrics and writes them to a
shared metrics file.

**Context Gate** (`environment/context-gate.py`)
A PreToolUse hook. Runs before every tool call.
Reads context metrics, checks thresholds and flags,
and approves or blocks the tool call.

Together they form an event-driven monitoring system.
No background process. No polling. The agent's own
activity drives the monitoring cycle.
---
## Why Hooks Instead of a Heartbeat
The original design used a background heartbeat process
polling every 30 seconds. Hooks are better because:

1. **More granular** — checks happen at every tool call,
   not on a fixed timer
2. **Simpler** — no background daemon to launch, manage,
   or recover from crashes
3. **Enforcement** — the gate can block a tool call
   immediately. A heartbeat could only write flags and
   hope they were read before the next action.
4. **No idle-agent problem** — an idle agent is not
   consuming context. Monitoring only matters when the
   agent is active, which is exactly when hooks fire.
---
## Context Reporter (StatusLine Hook)
**File:** `environment/context-reporter.py`

The reporter receives Claude Code status JSON on stdin
after each assistant message. It contains:
- context_window.used_percentage
- context_window.remaining_percentage
- context_window.total_input_tokens
- context_window.context_window_size

The reporter:
1. Extracts context window metrics
2. Reads the existing metrics file
3. Updates the entry for this session
4. Writes atomically to the metrics file
   (write-to-temp then rename to prevent race conditions)

**Metrics file:** `state/watchdog/context-metrics.json`

Each session's entry:
```json
{
  "session-id-here": {
    "used_percentage": 23.5,
    "remaining_percentage": 76.5,
    "total_input_tokens": 47000,
    "context_window_size": 200000,
    "agent_name": "builder-core"
  }
}
```

The reporter does not make decisions. It writes data.
---
## Context Gate (PreToolUse Hook)
**File:** `environment/context-gate.py`

The gate receives JSON on stdin before every tool call:
```json
{
  "session_id": "...",
  "tool_name": "...",
  "tool_input": {}
}
```

The gate runs this sequence:
1. **Fast path** — if `state/watchdog/` does not exist,
   approve immediately. No monitoring configured.
2. Read `context-metrics.json` for this session's
   current context percentage
3. Find this agent's Spot state file
   (`state/watchdog/spot-[agent-name].md`).
   If no Spot file exists, approve. No Spot watching.
4. **HALT check** — if the state file contains
   `halt: true`, block with reason.
5. **Rotation trigger check** — if the state file
   contains `trigger: rotation`, block with reason.
   Rotation is already in progress.
6. **Context threshold check** — calculate delta:
   ```
   delta = current_context - context_at_last_rotation
   if delta >= rotation_threshold_percent:
       write rotation trigger to state file
       block tool use
   ```
7. If none of the above, **approve**.

The gate returns JSON on stdout:
```json
{"decision": "approve"}
```
or:
```json
{"decision": "block", "reason": "..."}
```

The gate must be fast. It runs before every tool call.
No network calls. No heavy computation. Read two small
files, compare numbers, return.
---
## How This Replaces the Heartbeat
The heartbeat had three jobs:
1. Track context consumption → **Context Reporter** does this
2. Check thresholds and trigger rotation → **Context Gate** does this
3. Detect orphaned state files → **Not needed in hook model**.
   Orphaned state files are detected by the orchestrator
   at session start when it reads `state/watchdog/`.

The heartbeat's polling cycle is replaced by the natural
cadence of tool calls. Every tool call is a monitoring
checkpoint. This is more frequent and more reliable than
a 30-second timer.
---
## Rotation Flow With Hooks
1. Agent works normally. Every tool call passes through
   the gate. Gate approves — fast path.
2. Context Reporter writes updated metrics after each
   assistant message.
3. Agent's context grows. At some tool call, the gate
   calculates that the delta exceeds the threshold.
4. Gate writes a rotation trigger to the Spot state file.
5. Gate blocks the tool call with reason:
   "Context threshold reached — triggering Spot rotation"
6. The blocked tool call surfaces in the agent's session
   as an error/notification. Spot picks up the trigger
   on its next check.
7. Spot executes the rotation cycle per spot.md.
8. After rotation, Spot clears the trigger from the
   state file and resets `agent_context_at_last_rotation`.
9. Agent resumes. Gate approves again.
---
## HALT Enforcement With Hooks
When Spot writes a HALT flag to the state file:
1. The agent's next tool call hits the gate.
2. Gate reads `halt: true` from the state file.
3. Gate blocks with reason:
   "HALT flag active — values breach under review by human"
4. Every subsequent tool call is also blocked.
5. The agent cannot perform any action until the
   human approves clearing the HALT flag.
6. Spot clears the flag after human approval.
7. Gate reads the cleared state file and approves.

This is stronger enforcement than the old model where
the agent had to check for a HALT flag voluntarily.
The gate makes it involuntary.
---
## Hook Configuration
Add to `.claude/settings.json` or project settings:
```json
{
  "hooks": {
    "StatusLine": [
      {
        "command": "python3 environment/context-reporter.py",
        "timeout": 5000
      }
    ],
    "PreToolUse": [
      {
        "command": "python3 environment/context-gate.py",
        "timeout": 5000
      }
    ]
  }
}
```
---
## Files Owned by the Hook Infrastructure
```
environment/
├── context-gate.py            # PreToolUse hook
├── context-reporter.py        # StatusLine hook
└── environment-rules.md       # Governs environment setup
state/watchdog/
├── watchdog-rules.md          # Governs watchdog state maintenance
├── context-metrics.json       # Written by context-reporter
│                              # Read by context-gate
│                              # Not a permanent record
└── spot-[agent-name].md       # One per active Spot instance
                               # Owned by Spot
                               # Read by context-gate
```
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
- Make decisions about drift or behavioral integrity
- Interact with agents beyond approve/block responses
- Evaluate output quality
- Trigger escalations — they block tool use and surface
  reasons. Spot and the orchestrator handle escalation.
- Survive session end — they run within the session.
  State files persist. The hooks do not.
---
*Document version: 2.0*
*Created: 2026-03-04*
*Updated: 2026-03-12*
*Author: [Your Name]*
*Major change: Replaced heartbeat polling model with
hook-based event-driven architecture (v2.0)*
