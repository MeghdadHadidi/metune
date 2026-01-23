# Peachflow 2 - Agentic SDLC

A comprehensive Claude Code plugin that simulates a full software development team, managing the entire software development lifecycle from discovery to implementation.

## Overview

Peachflow 2 provides an agentic team that handles:

1. **Discovery** - Business analysis, market research, user research
2. **Definition** - Functional and non-functional requirements
3. **Design** - UX specifications, system architecture
4. **Plan** - Quarterly roadmaps, user stories, task breakdowns
5. **Implement** - Parallel task execution with specialized developers
6. **Clarification** - Resolving ambiguities throughout all phases

## Installation

Add the plugin to your Claude Code configuration:

```bash
claude --plugin-dir /path/to/peachflow
```

## Commands

| Command | Description |
|---------|-------------|
| `/peachflow:analyze` | Onboard existing project to peachflow |
| `/peachflow:discover "idea"` | Start product discovery phase |
| `/peachflow:define` | Define detailed requirements |
| `/peachflow:design` | Create UX and architecture docs |
| `/peachflow:plan` | Create quarterly roadmap |
| `/peachflow:plan Q1` | Create detailed quarter plan |
| `/peachflow:implement` | Execute implementation tasks |
| `/peachflow:implement T-001` | Execute specific task |
| `/peachflow:clarify` | Resolve pending questions |
| `/peachflow:status` | Show project status |

### Analyze Command (For Existing Projects)

Use `/peachflow:analyze` to onboard an existing codebase to peachflow:

```bash
# In a project without peachflow setup
/peachflow:analyze
```

This command:
1. **Scans the codebase** - Identifies tech stack, frameworks, structure
2. **Reverse-discovers** - Creates BRD, PRD, architecture docs from code
3. **Documents decisions** - Creates ADRs for existing technology choices
4. **Finds technical debt** - Catalogs TODO/FIXME, security gaps, test coverage
5. **Prepares for planning** - Sets up peachflow state for `/peachflow:plan`

Output includes:
- `docs/analyze-report.md` - Comprehensive analysis summary
- `docs/05-debt/` - Technical debt registry
- Standard peachflow docs with `[INFERRED]` markers

## Agents

### Analysis Phase (Existing Projects)
- **codebase-analyst** - Analyzes existing code, creates reverse-discovery docs

### Discovery Phase
- **business-analyst** - Creates BRD, stakeholder analysis
- **market-analyst** - Market research, competitor analysis
- **user-researcher** - User personas, journey maps
- **product-manager** - Creates PRD, feature prioritization

### Definition Phase
- **requirements-analyst** - Creates FRD and NFRs

### Design Phase
- **ux-designer** - Creates all UX documentation
- **software-architect** - Creates architecture and ADRs

### Plan Phase
- **product-manager** - Quarterly themes, user stories
- **tech-lead** - Task breakdown, dependency mapping

### Implementation Phase
- **frontend-developer** - [FE] tagged tasks
- **backend-developer** - [BE] tagged tasks
- **devops-engineer** - [DevOps] tagged tasks

### Throughout
- **clarification-agent** - Resolves [NEEDS CLARIFICATION] markers

## Document Structure

```
docs/
├── 01-business/
│   └── BRD.md                # Business requirements
├── 02-product/
│   ├── PRD.md                # Product requirements
│   ├── user-personas.md      # User personas
│   ├── user-flows.md         # User journeys
│   ├── ux/                   # UX documentation (11 docs)
│   └── architecture/
│       ├── high-level-design.md
│       └── adr/              # Architecture Decision Records
├── 03-requirements/
│   ├── FRD.md                # Functional requirements
│   └── NFRs.md               # Non-functional requirements
├── 04-plan/
│   ├── plan.md               # Quarterly roadmap
│   └── quarters/
│       └── q01/
│           ├── plan.md       # Quarter epics
│           ├── stories.md    # User stories
│           └── tasks/        # Individual task files
├── 05-debt/                  # Technical debt (from analyze)
│   ├── technical-debt.md     # Code quality issues
│   ├── security-gaps.md      # Security findings
│   └── test-coverage.md      # Test gaps
├── analyze-report.md         # Analysis summary (from analyze)
└── clarification.md          # Clarification log
```

## ID Formats

| Type | Format | Example |
|------|--------|---------|
| Business Requirement | BR-XXX | BR-001 |
| Feature | F-XXX | F-001 |
| Functional Requirement | FR-XXX | FR-001 |
| Non-Functional Requirement | NFR-XXX | NFR-001 |
| Epic | E-XXX | E-001 |
| User Story | US-XXX | US-001 |
| Task | T-XXX | T-001 |

## Task Tags

Tasks are tagged for agent routing:

| Tag | Agent | Work Type |
|-----|-------|-----------|
| [FE] | frontend-developer | UI, forms, client-side |
| [BE] | backend-developer | APIs, database, services |
| [DevOps] | devops-engineer | CI/CD, infrastructure |
| [Full] | frontend + backend | Full-stack work |

## State Management

Project state is tracked in `.peachflow-state.json`:
- Phase completion status
- Current quarter
- Last update timestamps

Check status with `/peachflow:status`.

## Utility Scripts

Agents use utility scripts to reduce LLM calls and enable local document operations.

### doc-search.sh

Search and list documents:

```bash
# Search by ID (BR, FR, NFR, E, US, T, etc.)
scripts/doc-search.sh id FR-001

# Search by keyword
scripts/doc-search.sh keyword "authentication" requirements
scripts/doc-search.sh keyword "NEEDS CLARIFICATION" docs

# List items by type and status
scripts/doc-search.sh list tasks pending
scripts/doc-search.sh list frs
scripts/doc-search.sh list nfrs
scripts/doc-search.sh list adrs

# Find items by tag
scripts/doc-search.sh tag FE
scripts/doc-search.sh tag BE

# Show task dependencies
scripts/doc-search.sh deps T-001

# Find related items
scripts/doc-search.sh related FR-001
```

### doc-parser.sh

Extract structured data from documents:

```bash
# Get specific items
scripts/doc-parser.sh fr FR-001
scripts/doc-parser.sh nfr NFR-001
scripts/doc-parser.sh task T-001
scripts/doc-parser.sh story US-001
scripts/doc-parser.sh adr 0001

# Get acceptance criteria
scripts/doc-parser.sh acceptance T-001

# Count items
scripts/doc-parser.sh count frs
scripts/doc-parser.sh count tasks

# List all IDs of type
scripts/doc-parser.sh ids frs
```

### id-generator.sh

Generate sequential IDs:

```bash
# Get next ID by type
scripts/id-generator.sh next br   # BR-001, BR-002...
scripts/id-generator.sh next fr   # FR-001, FR-002...
scripts/id-generator.sh next nfr  # NFR-001, NFR-002...
scripts/id-generator.sh next e    # E-001, E-002...
scripts/id-generator.sh next us   # US-001, US-002...
scripts/id-generator.sh next t    # T-001, T-002...
scripts/id-generator.sh next dec  # DEC-001, DEC-002...

# Get next ADR number
scripts/id-generator.sh adr       # 0001, 0002...

# Get next task filename
scripts/id-generator.sh task-file q01  # 001.md, 002.md...
```

### decision-manager.sh

Manage draft-review-finalize decision workflow:

```bash
# Add draft decision
scripts/decision-manager.sh add \
  "DEC-001" \
  "Technology" \
  "Which database?" \
  "PostgreSQL" \
  '["MongoDB", "MySQL"]' \
  "ACID compliance required" \
  "architecture.md"

# Finalize decision
scripts/decision-manager.sh finalize "DEC-001" "PostgreSQL"

# List decisions
scripts/decision-manager.sh list pending
scripts/decision-manager.sh list finalized

# Generate interview format
scripts/decision-manager.sh interview

# Export to decision log
scripts/decision-manager.sh export
```

### checklist-manager.sh

Manage task checkboxes and status:

```bash
# Update task status
scripts/checklist-manager.sh status "docs/.../001.md" "in_progress"
scripts/checklist-manager.sh status "docs/.../001.md" "completed"

# Check an acceptance criteria item
scripts/checklist-manager.sh check "docs/.../001.md" "endpoint created"

# Count checked/total items
scripts/checklist-manager.sh count "docs/.../001.md"
```

## Decision Workflow

Architecture and planning decisions follow a draft-review-finalize workflow:

1. **Draft** - Agent creates decision with recommendation
2. **Interview** - User presented with options, recommendation pre-selected
3. **Finalize** - Decision updated based on user choice
4. **Document** - ADR or plan updated with final decision

Decisions stored in `docs/decisions.json` and exported to `docs/decision-log.md`.

## Workflows

### New Project Workflow

```
/peachflow:discover "your product idea"
         │
         ▼
  BRD.md, PRD.md, user-personas.md, user-flows.md
         │
         ▼
/peachflow:define
         │
         ▼
  FRD.md, NFRs.md
         │
         ▼
/peachflow:design
         │
         ▼
  UX docs (11), architecture, ADRs
         │
         ▼
/peachflow:plan
         │
         ▼
  plan.md (quarterly roadmap)
         │
         ▼
/peachflow:plan Q1
         │
         ▼
  q01/plan.md, stories.md, tasks/
         │
         ▼
/peachflow:implement
         │
         ▼
  Code implementation with parallel agents
```

### Existing Project Workflow

```
/peachflow:analyze
         │
         ▼
  Scan codebase, detect tech stack
         │
         ▼
  Generate: analyze-report.md, BRD.md, PRD.md,
            architecture docs, ADRs, technical-debt.md
         │
         ▼
  User validates findings
         │
         ▼
/peachflow:plan (or /peachflow:discover to enhance)
         │
         ▼
  Continue with standard workflow...
```

## Guidelines

- **Don't over-document**: Each doc max 1-2 pages
- **Bullet points over prose**: Keep content scannable
- **Mark unknowns**: Use `[NEEDS CLARIFICATION: ...]`
- **Trace everything**: Requirements link through chain
- **Small tasks**: Each task completable in 1-2 days

## License

MIT
