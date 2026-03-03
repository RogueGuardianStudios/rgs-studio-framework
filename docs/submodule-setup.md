# Linking a Project Repo to the Framework


## Overview


The rgs-studio-framework is included in each project
repo as a git submodule. This gives every project
access to the orchestrator, agents, templates, and
studio governance — and lets improvements propagate
across projects via submodule updates.


---


## Initial Setup (New Project)


From your project repo root:


```bash
# Add the framework as a submodule
git submodule add https://github.com/RogueGuardianStudios/rgs-studio-framework.git rgs-studio-framework

# Copy the bootstrap CLAUDE.md to your repo root
cp rgs-studio-framework/templates/PROJECT_BOOTSTRAP_CLAUDE.md ./CLAUDE.md

# Edit CLAUDE.md — replace [PROJECT_NAME] with your
# project directory name (e.g., rgs-goap)

# Commit
git add .gitmodules rgs-studio-framework CLAUDE.md
git commit -m "Add rgs-studio-framework submodule"
```


---


## Cloning a Project That Uses the Framework


```bash
# Clone with submodules
git clone --recurse-submodules <project-repo-url>

# Or if already cloned without submodules
git submodule update --init
```


---


## Updating the Framework


When improvements are made to rgs-studio-framework
and you want to pull them into a project:


```bash
cd rgs-studio-framework
git pull origin main
cd ..
git add rgs-studio-framework
git commit -m "Update studio framework"
```


---


## Starting a Session


```bash
cd your-project-repo
claude
```


Claude Code reads your project's CLAUDE.md, which
bootstraps the orchestrator from the submodule.
You are now talking to the orchestrator with full
framework governance active.


---


## Adding a New Project to the Framework


1. Create a directory under
   rgs-studio-framework/projects/your-project/
2. Add a CLAUDE.md with project-specific context
3. Add conclave specialists if the project domain
   requires them
4. Commit to rgs-studio-framework
5. Update the submodule in all project repos
   that need the new project config


---


*Document version: 1.0*
*Created: 2026-03-03*
*Author: Studio Owner — Rogue Guardian Studios*
*Next review: At studio owner's discretion*
