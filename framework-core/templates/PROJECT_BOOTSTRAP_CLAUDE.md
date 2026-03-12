# CLAUDE.md
# Project Bootstrap
# This file connects a project repository to the
# agent-governance-framework via git submodule.
# Place this file at the root of your project repo.
# It tells Claude Code to load the orchestrator
# from the framework submodule.
#
# Setup:
#   git submodule add [YOUR_FRAMEWORK_REPO_URL] agent-governance-framework
#   git submodule update --init
#
# Replace [PROJECT_NAME] with the project directory
# name under agent-governance-framework/projects/
# (e.g., example-project)


---


## Bootstrap


You are the orchestrator for this project.
Before doing anything else, read the following files
from the framework submodule in this repository:


1. agent-governance-framework/values.md
2. agent-governance-framework/CLAUDE.md
3. agent-governance-framework/agents/orchestrator.md
4. agent-governance-framework/state/active-project.md
5. agent-governance-framework/state/decisions.md
6. agent-governance-framework/state/open-questions.md
7. agent-governance-framework/state/agent-status.md
8. agent-governance-framework/state/known-issues.md
9. agent-governance-framework/projects/[PROJECT_NAME]/CLAUDE.md


Those documents define who you are, how you operate,
and what this project is. Follow them without exception.


After reading, give the human a brief status
summary before any other work.


---


## Project-Specific Notes


Add any project-specific context here that does not
belong in the framework. This section is for things
unique to this repo's setup — local build commands,
environment specifics, or repository conventions
that are not covered by the framework.


---


*Bootstrap template version: 1.0*
*Replace [PROJECT_NAME] with the project directory name.*
*See docs/submodule-setup.md for full setup instructions.*
