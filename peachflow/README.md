# Peachflow

**Your AI development team in a CLI.** From idea to implementation, Peachflow orchestrates specialized agents through the entire software lifecycle.

```
  idea ──► discover ──► define ──► design ──► plan ──► implement ──► ship
              │            │          │         │           │
          analysts    requirements   UX &    roadmap    developers
          research    engineers    architects  tasks    build code
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
| `define` | Write detailed requirements |
| `design` | Create UX specs & architecture |
| `plan` | Build quarterly roadmap |
| `plan Q1` | Break quarter into tasks |
| `implement` | Execute tasks with dev agents |
| `clarify` | Resolve open questions |
| `status` | Show progress |

## The Team

```
┌─────────────────────────────────────────────────────────────────┐
│  DISCOVERY          DEFINITION        DESIGN         IMPLEMENT │
│  ───────────        ──────────        ──────         ───────── │
│  business-analyst   requirements-     ux-designer    frontend  │
│  market-analyst     analyst           software-      backend   │
│  user-researcher                      architect      devops    │
│  product-manager                                               │
│                                                                │
│                    + clarification-agent (always available)    │
└─────────────────────────────────────────────────────────────────┘
```

## How It Works

**New Project:**
```
init → discover → define → design → plan → plan Q1 → implement
```

**Existing Codebase:**
```
init → analyze → [plan or discover to add features] → implement
```

**Adding Features Mid-Project:**
```
discover "new feature" → plan (incremental) → implement
```

## Output Structure

```
docs/
├── 01-business/BRD.md          # Why we're building
├── 02-product/
│   ├── PRD.md                  # What we're building
│   ├── user-personas.md        # Who we're building for
│   ├── ux/                     # How it looks & feels
│   └── architecture/           # How it's structured
├── 03-requirements/            # Detailed specs (FR, NFR)
├── 04-plan/
│   ├── plan.md                 # Quarterly roadmap
│   └── quarters/q01/           # Tasks & stories
└── 05-debt/                    # Technical debt tracking
```

## Key Concepts

| Concept | Format | Example |
|---------|--------|---------|
| Business Req | BR-XXX | BR-001 |
| Feature | F-XXX | F-001 |
| Functional Req | FR-XXX | FR-001 |
| Epic | E-XXX | E-001 |
| User Story | US-XXX | US-001 |
| Task | T-XXX | T-001 |

**Task Tags:** `[FE]` frontend · `[BE]` backend · `[DevOps]` infra · `[Full]` full-stack

**Markers:** `[NEEDS CLARIFICATION: ...]` · `[INFERRED: ...]` · `[DEBT: ...]`

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
# Search & parse docs
scripts/doc-search.sh id FR-001
scripts/doc-search.sh keyword "auth" requirements
scripts/doc-parser.sh task T-001
scripts/doc-parser.sh count frs

# Generate IDs
scripts/id-generator.sh next fr    # → FR-001

# State management
scripts/state-manager.sh status
scripts/state-manager.sh get-project-name    # Get project name for docs
scripts/state-manager.sh get-unplanned
scripts/state-manager.sh get-quarter-progress q01

# Git helpers
scripts/git-helper.sh is-main
scripts/git-helper.sh create-worktree q01
```

</details>

<details>
<summary><b>State File Structure</b></summary>

`.peachflow-state.json`:
```json
{
  "projectName": "TaskFlow",
  "projectType": "new",
  "phases": { "discovery": "completed", "plan": "in_progress" },
  "currentQuarter": "q01",
  "requirements": {
    "planned": ["BR-001", "F-001"],
    "unplanned": ["F-020"]
  }
}
```

The `projectName` is used by all agents when generating documents.

</details>

---

MIT License
