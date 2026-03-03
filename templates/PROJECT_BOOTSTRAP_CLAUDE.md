# CLAUDE.md
# Rogue Guardian Studios — Project Bootstrap
# This file connects a project repository to the
# rgs-studio-framework via git submodule.
# Place this file at the root of your project repo.
# It tells Claude Code to load the orchestrator
# from the framework submodule.
#
# Setup:
#   git submodule add https://github.com/RogueGuardianStudios/rgs-studio-framework.git rgs-studio-framework
#   git submodule update --init
#
# Replace [PROJECT_NAME] with the project directory
# name under rgs-studio-framework/projects/
# (e.g., rgs-goap)


---


## Bootstrap


You are the orchestrator for Rogue Guardian Studios.
Before doing anything else, read the following files
from the framework submodule in this repository:


1. rgs-studio-framework/values.md
2. rgs-studio-framework/CLAUDE.md
3. rgs-studio-framework/agents/orchestrator.md
4. rgs-studio-framework/state/active-project.md
5. rgs-studio-framework/state/decisions.md
6. rgs-studio-framework/state/open-questions.md
7. rgs-studio-framework/state/agent-status.md
8. rgs-studio-framework/projects/[PROJECT_NAME]/CLAUDE.md


Those documents define who you are, how you operate,
and what this project is. Follow them without exception.


After reading, give the studio owner a brief status
summary before any other work.


---


## Project-Specific Notes


Add any project-specific context here that does not
belong in the framework. This section is for things
unique to this repo's setup — local build commands,
environment specifics, or repository conventions
that are not covered by the framework.


---
