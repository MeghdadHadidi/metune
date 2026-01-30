# Peachflow

**Your AI development team in a CLI.** From idea to implementation, Peachflow orchestrates specialized agents through the entire software lifecycle.

```
  idea ──► discover ──► plan ──► implement ──► ship
              │           │           │
          analysts     roadmap    developers
          research     tasks      build code
```

## Quick Start

```bash
# New project
/peachflow:init
/peachflow:discover "your product idea"

# Existing project
/peachflow:init
/peachflow:analyze
```

## Commands

| Command | What it does |
|---------|--------------|
| `init` | Set up Peachflow - asks for project name (required first) |
| `analyze` | Reverse-engineer existing codebase |
| `discover "idea"` | Research & create BRD/PRD |
| `plan` | Build quarterly roadmap & break into tasks |
| `implement` | Execute tasks with dev agents |
| `clarify` | Resolve open questions |
| `status` | Show progress |

## The Team

```
┌─────────────────────────────────────────────────────────────────┐
│  DISCOVERY          PLANNING          IMPLEMENT                 │
│  ───────────        ────────          ─────────                 │
│  business-analyst   tech-lead         frontend-developer        │
│  product-manager    product-manager   backend-developer         │
│                                       devops-engineer           │
│                     software-architect (architecture decisions) │
│                                                                 │
│                    + codebase-analyst (for existing projects)   │
└─────────────────────────────────────────────────────────────────┘
```

## How It Works

**New Project:**
```
init → discover → plan → implement
```

**Existing Codebase:**
```
init → analyze → plan → implement
```

**Adding Features Mid-Project:**
```
discover "new feature" → plan (incremental) → implement
```

## Output Structure

```
.peachflow-state.json           # Project settings & phase status
.peachflow-graph.json           # Work items: epics, stories, tasks
docs/
├── 01-business/BRD.md          # Why we're building
├── 02-product/
│   ├── PRD.md                  # What we're building
│   └── architecture/adr/       # Architecture Decision Records
```

## Key Concepts

| Concept | Format | Example |
|---------|--------|---------|
| Epic | E-XXX | E-001 |
| User Story | US-XXX | US-001 |
| Task | T-XXX | T-001 |
| Sprint | S-XXX | S-001 |
| Clarification | CL-XXX | CL-001 |

**Task Tags:** `[FE]` frontend · `[BE]` backend · `[DevOps]` infra · `[Full]` full-stack

## Incremental Planning

Peachflow tracks requirements as **planned** or **unplanned**. When you add features mid-project:

1. `discover "new feature"` → adds to unplanned
2. `plan` → shows impact, asks where to place
3. Creates migration tasks if needed

## Git Workflow

Peachflow **never auto-commits**. On implementation:
- **Main branch:** Prompts to commit, then creates worktree for quarter
- **Feature branch:** Continues work, summarizes when complete

---

<details>
<summary><b>Utility Scripts Reference</b></summary>

```bash
# Graph management
scripts/peachflow-graph.py list epics
scripts/peachflow-graph.py list tasks --status pending
scripts/peachflow-graph.py ready-tasks
scripts/peachflow-graph.py stats

# State management
scripts/state-manager.sh status
scripts/state-manager.sh get-project-name

# Git helpers
scripts/git-helper.sh is-main
scripts/git-helper.sh create-worktree S-001
```

</details>

<details>
<summary><b>State File Structure</b></summary>

`.peachflow-state.json`:
```json
{
  "version": "3.0.0",
  "projectName": "TaskFlow",
  "projectType": "new",
  "phases": { "discovery": "completed", "plan": "in_progress" },
  "currentQuarter": "Q1",
  "currentSprint": "S-001"
}
```

`.peachflow-graph.json` contains all work items (epics, stories, tasks, sprints).

</details>

---

MIT License
