The Full Architecture
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
│   ├── conclave/
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
│   └── compressor.md                  # Summarization specialist
│                                      # maintains lean context
│                                      # across checkpoints
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
│   │   └── SKILL.md                   # How to produce a valid Brief
│   ├── compress-context/
│   │   └── SKILL.md                   # How to compress memory dumps
│   └── propose-improvement/
│       └── SKILL.md                   # How to write a valid proposal
│
├── commands/
│   ├── consult.md                     # Trigger conclave consultation
│   ├── plan.md                        # Trigger planning phase
│   ├── build.md                       # Trigger build phase
│   ├── escalate.md                    # Bubble up a conflict
│   ├── propose.md                     # Submit improvement proposal
│   └── evaluate.md                    # Trigger witness evaluation
│
├── templates/
│   ├── BRIEF_TEMPLATE.md              # Strict schema for agent briefs
│   ├── PROPOSAL_TEMPLATE.md           # Improvement proposal format
│   ├── HANDOFF_TEMPLATE.md            # Phase transition document
│   ├── EVALUATION_TEMPLATE.md         # Witness test scoring sheet
│   └── MEMORY_TEMPLATE.md             # Structure for memory dumps
│
├── state/                             # Shared war room whiteboard
│   ├── active-project.md              # Current project overview
│   ├── decisions.md                   # Decisions made, not up for debate
│   ├── open-questions.md              # Unresolved items
│   ├── known-issues.md                # Current pain points
│   └── agent-status.md               # What each agent is doing right now
│
├── improvement-proposals/
│   ├── active/
│   │   └── YYYY-MM-DD-agent-topic/
│   │       ├── proposal.md            # Problem, justification, prediction
│   │       ├── variant.md             # Modified agent/skill file
│   │       └── test-cases.md          # What tasks to run
│   ├── results/
│   │   └── YYYY-MM-DD-agent-topic/
│   │       ├── original-output/
│   │       ├── variant-output/
│   │       └── verdict.md             # Decision + reasoning
│   └── archive/
│       ├── merged/                    # Successful improvements
│       └── rejected/                  # Failed attempts + why
│
└── projects/                          # Per-project subdirectories
    └── rgs-goap/
        ├── CLAUDE.md                  # Project-specific context
        └── state/                     # Project-specific state

The Agent Branch Structure
Each active agent gets its own branch:
agent/orchestrator
agent/planner
agent/builder-core
agent/builder-editor
agent/builder-tests
agent/witness
Each branch contains:
agent-workspace/
├── memory-dump.md          # Full conversation and context
│                           # Compressed periodically by compressor agent
├── current-goals.md        # Bullet pointed, light context
├── brief.md                # Shareable summary of progress
│                           # and pain points
├── pain-points.md          # Running log of friction encountered
│                           # Source material for improvement proposals
└── scratch/                # Working files, disposable

The Information Flow
YOU
 │
 ↕ conversation
 │
ORCHESTRATOR
 │
 ├──→ reads: values.md, CLAUDE.md, state/
 ├──→ consults: conclave agents (via Brief)
 ├──→ presents: plan to you for sign-off
 │
 ↓ signed off
 │
PLANNER
 │
 ├──→ reads: signed plan, state/decisions.md
 ├──→ produces: execution graph
 │            parallel tasks
 │            sequential dependencies
 │            escalation triggers
 │
 ↓
BUILDERS (parallel where possible)
 │
 ├──→ each reads: their Brief, relevant skills
 ├──→ each writes: to their own branch
 ├──→ each updates: their current-goals.md
 ├──→ conflict? → escalate.md → orchestrator → you
 │
 ↓
REVIEWER
 │
 ├──→ reads: builder output + evaluation-rubric.md
 ├──→ checks: performance AND alignment
 ├──→ passes or sends back to builder
 │
 ↓ passed review
 │
YOU ← final sign-off before merge to main

The Improvement Cycle
BUILDER hits recurring friction
 │
 ↓ uses propose-improvement skill
 │
improvement-proposals/active/
 │
 ↓ you approve test
 │
WITNESS spins up two variants
 │
 ├── original agent
 └── variant agent
      │
      both run same test cases
      results stripped of identity
      │
 ↓ you evaluate blind
 │
 ├── Better, clean → merge to main, commit with justification
 ├── Not better → feedback to agent, try again
 ├── Better but negative consequences → reject, dissect why,
 │                                       challenge to achieve gain
 │                                       without the cost
 └── Not better but reveals something → flag to orchestrator
                                         may indicate deeper issue

The Context Flow Between Agents
FULL CONTEXT (stays in memory-dump.md, never passed directly)
     ↓ compressed by compressor agent at checkpoints
SUMMARY (stays in agent branch, readable if needed)
     ↓ agent distills to
BRIEF (shareable, strict template, lean)
     ↓ only what receiving agent needs
RECEIVING AGENT

What Is Immutable vs Evolvable

What We Build First
The logical build order:
values.md — the foundation everything else defers to
evaluation-rubric.md — defines what "better" means
templates/ — Brief, Proposal, Handoff, Evaluation, Memory
CLAUDE.md — global orchestrator context
orchestrator.md — the agent you talk to
compressor.md — essential for context health
witness.md — needed before any improvement cycle runs
conclave/ — specialist agents
planner.md + builders/ — implementation layer
skills/ — as needed per project type
commands/ — slash commands to tie it all together

