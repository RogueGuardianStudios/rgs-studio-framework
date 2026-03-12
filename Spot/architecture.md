# The Full Architecture

rgs-studio-framework/
│
├── CLAUDE.md                          # Global orchestrator context
│                                      # Studio values, non-negotiables,
│                                      # framework rules, governance
│
├── values.md                          # Immutable. Only you can modify.
│                                      # Defines alignment criteria
│                                      # for all evaluation
│
├── evaluation-rubric.md               # How outputs are scored
│                                      # Performance axis + Alignment axis
│                                      # Defined before any test runs
│
├── agents/
│   ├── orchestrator.md                # The conversational layer
│   │                                  # Consults conclave, presents plans
│   │                                  # manages escalation
│   │
│   ├── spot.md                        # Watchdog agent
│   │                                  # Monitor + checkpoint authority
│   │                                  # + compression/rotation handler
│   │                                  # One instance per watched agent
│   │                                  # Replaces compressor.md
│   │
│   ├── condenser.md                   # Optional compression agent
│   │                                  # Spun up by Spot during rotation
│   │                                  # Condenser-assisted mode only
│   │                                  # Stronger model than Spot monitor
│   │                                  # Stands down after seed validated
│   │
│   ├── conclave/
│   │   ├── domain-specialist.md       # Base definition for all
│   │   │                              # conclave specialists
│   │   ├── unity-architect.md         # Architecture decisions
│   │   ├── performance-specialist.md  # Burst, optimization, profiling
│   │   ├── patterns-reviewer.md       # Unity/C# patterns and anti-patterns
│   │   ├── systems-designer.md        # High level system design
│   │   └── alignment-reviewer.md      # Checks proposals against values.md
│   │
│   ├── planner.md                     # Takes signed-off plan
│   │                                  # produces execution graph
│   │                                  # parallel vs sequential
│   │
│   ├── builders/
│   │   ├── builder.md                 # Base definition for all builders
│   │   ├── builder-core.md            # Core systems implementation
│   │   ├── builder-editor.md          # Unity editor tooling
│   │   ├── builder-tests.md           # Test writing and validation
│   │   └── builder-docs.md            # Documentation and README
│   │
│   ├── reviewer.md                    # Reviews builder output
│   │                                  # before it reaches you
│   │
│   ├── witness.md                     # Blind evaluation agent
│   │                                  # scores variants independently
│   │
│   └── compressor.md                  # RETIRED 2026-03-04
│                                      # Responsibilities absorbed
│                                      # into spot.md
│                                      # Preserved for traceability
│
├── environment/                       # Session-level infrastructure
│   └── environment-rules.md          # Governs environment setup
│
├── skills/
│   ├── create-unity-package/
│   │   └── SKILL.md
│   ├── create-burst-job/
│   │   └── SKILL.md
│   ├── create-scriptableobject-system/
│   │   └── SKILL.md
│   ├── write-tests/
│   │   └── SKILL.md
│   ├── write-brief/
│   │   └── SKILL.md
│   └── propose-improvement/
│       └── SKILL.md
│
├── commands/
│   ├── consult.md
│   ├── plan.md
│   ├── build.md
│   ├── escalate.md
│   ├── propose.md
│   └── evaluate.md
│
├── templates/
│   ├── BRIEF_TEMPLATE.md
│   ├── PROPOSAL_TEMPLATE.md
│   ├── HANDOFF_TEMPLATE.md
│   ├── EVALUATION_TEMPLATE.md
│   └── MEMORY_TEMPLATE.md
│
├── state/
│   ├── active-project.md
│   ├── decisions.md
│   ├── decisions-archive.md
│   ├── open-questions.md
│   ├── open-questions-archive.md
│   ├── known-issues.md
│   ├── known-issues-archive.md
│   ├── agent-status.md
│   │
│   └── watchdog/                      # Spot state
│       ├── watchdog-rules.md          # Governs watchdog state maintenance
│       └── spot-[agent-name].md       # One per active Spot instance
│                                      # Created at spin-up
│                                      # Survives respin cycles
│                                      # Destroyed at clean stand-down
│                                      # Orphaned file = known issue
│
├── improvement-proposals/
│   ├── active/
│   │   └── YYYY-MM-DD-agent-topic/
│   │       ├── proposal.md
│   │       ├── variant.md
│   │       └── test-cases.md
│   ├── results/
│   │   └── YYYY-MM-DD-agent-topic/
│   │       ├── original-output/
│   │       ├── variant-output/
│   │       └── verdict.md
│   └── archive/
│       ├── merged/
│       └── rejected/
│
└── projects/
    └── rgs-goap/
        ├── CLAUDE.md
        └── state/

---

# The Agent Branch Structure

Each active agent gets its own branch:

agent/orchestrator
agent/planner
agent/builder-core
agent/builder-editor
agent/builder-tests
agent/witness
agent/spot-[watched-agent-name]        # One per Spot instance
                                       # Survives respin cycles

Each branch contains:

agent-workspace/
├── memory-dump.md          # Replaced by Spot compression seed
│                           # on rotation
├── current-goals.md
├── brief.md
├── pain-points.md
└── scratch/

---

# The Information Flow

YOU
 │
 ↕ conversation
 │
ORCHESTRATOR ←————————— SPOT (orchestrator instance)
 │                        Always active. Assigned at initialization.
 ├──→ reads: values.md, CLAUDE.md, state/
 ├──→ consults: conclave agents (via Brief)
 ├──→ presents: plan to you for sign-off
 │
 ↓ signed off
 │
PLANNER ←———————————————— SPOT (if assigned)
 │
 ├──→ reads: signed plan, state/decisions.md
 ├──→ produces: execution graph
 │
 ↓
BUILDERS ←———————————————— SPOT (complexity dependent)
 │
 ├──→ each reads: Brief, relevant skills
 ├──→ each writes: to their own branch
 ├──→ conflict? → escalate → orchestrator → you
 │
 ↓
REVIEWER
 │
 ├──→ reads: builder output + evaluation-rubric.md
 ├──→ passes or sends back to builder
 │
 ↓ passed review
 │
YOU ← final sign-off before merge to main

---

# How Spot Monitors

Spot runs on a configured time interval (default: 5 minutes).
It does not pause. The watched agent does not initiate checks.

At each interval, Spot:

  Reads watched agent's current work product
       ↓
  Values breach?
       ↓ yes → Write HALT flag to agent's state file
               Escalate directly to studio owner
               Do not rotate
       ↓ no
  Assign status (Clean / Minor drift / Significant drift)
       ↓
  Act on status per status ladder
       ↓
  Write checkpoint entry to state file
       ↓
  checkpoint_count >= checkpoint_cap - 1?
       ↓ yes → Execute rotation cycle
       ↓ no  → Continue monitoring on interval

SPOT rotation cycle:

  Final checkpoint
       ↓
  Values breach on final check?
       → Write HALT flag, escalate to studio owner. Do not rotate.
       ↓
  Identify compression anchor
  (last verified clean checkpoint)
       ↓
  Branch on compression mode:
       │
       ├── Inline mode
       │    Spot constructs seed directly
       │    Spot verifies own output
       │
       └── Condenser-assisted mode
            Spot packages checkpoint record + delta
            Spot spins up Condenser (stronger model)
            Condenser produces seed
            Spot validates Condenser output
            Condenser stands down
       │
       ↓
  Respin watched agent with validated seed
       ↓
  Confirm watched agent running
       ↓
  Respin Spot from state file
       ↓
  Monitoring resumes on configured time interval

---

# Agent Protocol With Spot

1. Spot spins up, confirms ready to orchestrator
2. Agent receives Brief
3. Agent checks for HALT flag before each new unit of work —
   if flag is present, stop immediately and output current state
4. Agent works continuously — no pause/unpause required
5. Spot monitors on its own time interval independently
6. At completion: agent signals to orchestrator,
   Spot runs final checkpoint and stands down

---

# The Improvement Cycle

BUILDER hits recurring friction
 │
 ↓ logs to pain-points.md
 │
 ↓ orchestrator submits improvement proposal
 │
improvement-proposals/active/
 │
 ↓ you approve test
 │
WITNESS spins up two variants
 │
 ├── original agent
 └── variant agent — both run same test cases
      │
 ↓ you evaluate blind
 │
 ├── Better, clean → merge
 ├── Not better → retry
 ├── Better but consequences → reject, dissect
 └── Reveals something → flag to orchestrator

---

# Context Flow

FULL CONTEXT
     ↓ Spot compresses at rotation trigger
COMPRESSION SEED (from verified checkpoints)
     ↓
RESPUN AGENT (clean context, verified state,
             delta flagged explicitly)

---

# What Is Immutable vs Evolvable

| Document               | Who Can Modify        | How                          |
| ---------------------- | --------------------- | ---------------------------- |
| values.md              | You only              | Deliberate, manual           |
| evaluation-rubric.md   | You only              | Deliberate, manual           |
| Global CLAUDE.md       | You + orchestrator    | With your approval           |
| Agent .md files        | Agents can propose    | Witness test + your approval |
| Skill files            | Agents can propose    | Witness test + your approval |
| State files            | Agents freely         | Within their role            |
| watchdog/ state files  | Spot only             | Within Spot lifecycle        |
| environment/ scripts   | You only              | Deliberate, manual           |
| Memory/Brief/Goals     | Agents freely         | Their own branch only        |

---

# Model Assignment Per Agent Role

Model assignment is a configurable parameter, not
an assumption baked into the framework. Each agent
role has different cognitive demands. Matching model
capability to role requirements controls cost without
sacrificing quality.

**Recommended tiers — to be validated empirically:**

| Agent Role               | Cognitive Demand                      | Recommended Tier          |
| ------------------------ | ------------------------------------- | ------------------------- |
| Orchestrator             | High — synthesis, judgment, planning  | Frontier                  |
| Conclave agents          | High — domain expertise, assessment   | Frontier                  |
| Planner                  | Medium — structured graph production  | Mid                       |
| Builders                 | Medium-High — implementation, TDD     | Mid-High                  |
| Reviewer                 | Medium — rubric-based scoring         | Mid                       |
| Witness                  | Medium — blind scoring, no advocacy   | Mid                       |
| Spot (monitoring)        | Low — classification, comparison      | Small                     |
| Spot (inline compression)| Medium — compression seed construction| Mid                       |
| Condenser                | Varies — set by orchestrator          | Orchestrator's discretion |

The orchestrator is always Frontier. It has the full
picture on task complexity and sets all other model
tiers accordingly — including the Condenser.

The Condenser does not have a fixed recommended tier.
The orchestrator assigns its model at Spot assignment
time based on task complexity and what the compression
is being asked to preserve. A simple task may need
only a Mid-tier Condenser. A complex multi-phase task
with dense technical context may warrant a stronger one.

The improvement cycle will produce evidence over time
on whether Condenser-assisted mode improves outcomes
for specific task types, and what model tier produces
sufficient fidelity at lowest cost. Model assignments
should be reviewed and updated through the normal
improvement proposal process as that data accumulates.

Do not prescribe model tiers before evidence exists.
Start conservative, measure, adjust.

**Why this matters:**

Spot's monitoring role is a classification task with
clear criteria — read output, compare against MD file,
assign one of four statuses. A smaller, faster, cheaper
model is likely sufficient. Running Spot on a small
model while builders run on a mid-tier model changes
the cost profile significantly.

The rotation cycle is more demanding than monitoring.
Constructing a compression seed requires more judgment.
Spot may benefit from temporarily upgrading its model
tier for the rotation cycle, then returning to the
smaller model for resumed monitoring.

**Validation requirement:**

During Test Case 5 (empirical calibration), run Spot
on at least two model tiers and compare detection
accuracy. If a smaller model produces equivalent
detection results, use the smaller model. Cost
optimisation should be evidence-based, not assumed.

**Configuration:**

Model assignment per agent role is set in CLAUDE.md
and each agent's MD file. It is configurable per
project. Model assignments are evolvable — as the
model landscape changes, assignments should be reviewed
through the normal improvement proposal process.

---

# What We Build First

1.  values.md
2.  evaluation-rubric.md
3.  templates/
4.  CLAUDE.md
5.  orchestrator.md
6.  spot.md
7.  condenser.md
8.  witness.md
10. conclave/
11. planner.md + builders/
12. skills/
13. commands/

Note: compressor.md is retired. Preserved for
traceability only. Not part of the active build order.
