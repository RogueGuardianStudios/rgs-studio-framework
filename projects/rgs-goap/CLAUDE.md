# rgs-goap — Project Context
# Rogue Guardian Studios
# This document defines the project-specific context
# for rgs-goap. It is read by the orchestrator alongside
# state/active-project.md when this project is active.
# It does not replace or override any studio-level
# governance. It extends it with project specifics.


---


## What This Project Is


rgs-goap is a general-purpose Goal-Oriented Action Planning
library for Unity. It provides a modular planner, actions,
goals, and world state system for NPC AI decision-making.
It is built as a reusable package — not tied to any
specific game.


---


## Technology Stack


- Unity (C#)
- Burst-compatible where performance-critical
- NUnit for testing (Unity Test Framework)
- UPM package structure


---


## Project-Specific Conventions


- All runtime code lives under Runtime/
- All editor tooling lives under Editor/
- All tests live under Tests/
- Package manifest at package.json
- Assembly definitions (.asmdef) for each folder boundary
- Public API documented with XML documentation comments
- No MonoBehaviour in core planning logic —
  pure C# for testability and Burst compatibility


---


## Conclave Specialists for This Project


The following project-level conclave agents are available
for consultation on rgs-goap work. They extend
domain-specialist.md and are defined under
projects/rgs-goap/conclave/:


- unity-architect.md — architecture decisions,
  assembly structure, dependency management
- performance-specialist.md — Burst jobs,
  NativeContainers, profiling, allocation patterns
- patterns-reviewer.md — Unity/C# patterns and
  anti-patterns, API design
- systems-designer.md — high-level GOAP system design,
  planner architecture, extensibility


---


## What Agents Load for This Project


When working on rgs-goap, agents load:


- This document — for project context
- The relevant conclave specialist MD files —
  only when consulting that specialist
- Project state files if they exist under
  projects/rgs-goap/state/


All studio-level loading rules still apply.
This document adds to what agents load.
It does not replace it.


---


*Document version: 1.0*
*Created: 2026-03-03*
*Author: Studio Owner — Rogue Guardian Studios*
*Next review: At studio owner's discretion*
