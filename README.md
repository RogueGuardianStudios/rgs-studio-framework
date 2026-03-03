# rgs-studio-framework

The studio governance framework for Rogue Guardian Studios.
Contains the orchestrator, all agents, templates, skills, and
studio values that apply to every project.

---

## How to use this with a project

### Starting a new project

1. In your project repo, create a folder called `rgs-framework/`
2. Copy the entire `framework-core/` folder into `rgs-framework/`
3. Copy the entire `state-templates/` folder into `rgs-framework/state/`
4. Create `rgs-framework/state/improvement-proposals/active/`,
   `results/`, `archive/merged/`, and `archive/rejected/`
5. Edit `rgs-framework/state/active-project.md` with your
   project details

Your project repo should look like:

    your-project/
    ├── Assets/                    ← Unity project, untouched
    ├── Packages/
    ├── ProjectSettings/
    └── rgs-framework/
        ├── CLAUDE.md              ← from framework-core
        ├── values.md
        ├── evaluation-rubric.md
        ├── agents/
        ├── templates/
        ├── skills/
        ├── commands/
        └── state/                 ← from state-templates, project-specific

Open your project repo root in Claude Code.
The orchestrator will find all framework files under rgs-framework/.

---

## Drag-and-drop workflow

**Bringing the framework into a project:**
Copy `framework-core/` and `state-templates/` into your project repo
as described above. The `state/` folder is project-specific and
stays in your project repo permanently.

**Returning improvements to the framework:**
When a project session ends and the framework files have improved,
copy `rgs-framework/` from your project back into this repo —
everything EXCEPT the `state/` folder.
The `state/` folder never comes back. It belongs to the project.

Then commit and push to preserve the improvements for the next project.

---

## What lives where

| Folder | Purpose | Travels with project? |
|---|---|---|
| framework-core/ | All agent MD files, templates, skills | Yes — copy in |
| state-templates/ | Blank starting state files | Yes — copy in as state/ |
| projects/ | Project-specific conclave agents | Reference only |
| improvement-proposals/ | Archive of past proposals | No |

---

*Framework version: 1.0*
*Author: Studio Owner — Rogue Guardian Studios*
