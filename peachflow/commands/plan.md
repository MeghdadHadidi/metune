---
name: peachflow:plan
description: Create quarterly planning. Without arguments creates master roadmap. With quarter argument (Q1, Q01, quarter 1) creates detailed quarter plan with git worktree.
argument-hint: "[optional: Q1 | Q01 | quarter 1]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Task, AskUserQuestion
---

# /peachflow:plan - Quarterly Planning Phase

Two modes of operation:
1. **Without arguments**: Create master quarterly roadmap (no git branch)
2. **With quarter**: Create detailed quarter plan (creates git worktree)

## Prerequisites

Discovery phase complete:
- `specs/discovery/prd.md` exists
- `specs/discovery/architecture.md` exists

---

## Mode 1: Master Quarterly Roadmap

### When Called

```
/peachflow:plan
```

### Purpose

Create a comprehensive quarterly roadmap that:
- Breaks the entire product into deliverable quarters
- Ensures each quarter delivers usable functionality
- Plans for incremental rollout
- Minimizes time to market

### Workflow

#### Step 1: Review Discovery
**Auto-invoke**: product-manager, software-architect, frontend-engineer agents

Load and analyze:
- PRD features and priorities
- Architecture components
- Technical dependencies
- Design system scope

#### Step 2: Quarter Splitting Strategy
**Auto-invoke**: product-manager + tech-lead agents (collaborative)

Key questions to answer:
- What's the minimum viable first release?
- What features can ship independently?
- What has shared dependencies?
- What reduces time to market?
- What allows users to start using the product early?

Principles:
1. **Vertical slices**: Each quarter delivers working features
2. **Dependency ordering**: Build foundations first
3. **Incremental value**: Users benefit from each quarter
4. **Risk front-loading**: Tackle unknowns early

#### Step 3: Create Quarterly Plans
**Auto-invoke**: product-manager, tech-lead agents

For each quarter define:
- Theme and goals
- Features included (from PRD)
- Epics and user stories
- Technical components
- Dependencies on other quarters
- Risks and mitigations

#### Step 4: Technical Deep Dive
**Auto-invoke**: software-architect, frontend-engineer, backend-engineer agents

For each quarter:
- Detailed tech stack decisions
- API specifications
- Data model contracts
- Frontend component architecture
- Coding standards and patterns

#### Step 5: Clarification
**Auto-invoke**: clarification-agent

Ask questions about:
- Resource allocation
- Timeline constraints
- Priority trade-offs
- Technical decisions

### Output

```
specs/
└── quarterly/
    ├── roadmap.md              # Master roadmap
    ├── Q01-overview.md         # Q01 high-level
    ├── Q02-overview.md         # Q02 high-level
    └── Q03-overview.md         # Q03 high-level
```

### Roadmap Document Structure

```markdown
---
product: {product-name}
document: quarterly-roadmap
version: 1.0
created: {date}
total-quarters: {N}
---

# Quarterly Roadmap: {Product Name}

## Executive Summary
[Overview of the plan and timeline]

## Quarterly Overview

| Quarter | Theme | Features | Deliverable |
|---------|-------|----------|-------------|
| Q01 | Foundation | Auth, Core UI | User can sign up and see dashboard |
| Q02 | Core Features | Feature A, B | User can do primary tasks |
| Q03 | Enhancement | Feature C, D | Full product experience |

## Q01: {Theme}

### Goals
[What users can do after Q01]

### Features
- F001: [Feature from PRD]
- F002: [Feature from PRD]

### Epics
- E01: [Epic with user stories]
- E02: [Epic with user stories]

### Technical Focus
- [Architecture component 1]
- [Architecture component 2]

### Dependencies
None (first quarter)

### Risks
| Risk | Mitigation |
|------|------------|

---

## Q02: {Theme}
[Same structure...]

---

## Q03: {Theme}
[Same structure...]

## Technical Standards

### Coding Standards
[Project-wide standards]

### Architecture Patterns
[Patterns to follow]

### Testing Strategy
[Testing approach]
```

---

## Mode 2: Detailed Quarter Plan

### When Called

```
/peachflow:plan Q1
/peachflow:plan Q01
/peachflow:plan quarter 1
```

### Purpose

Create detailed implementation plan for a specific quarter and set up isolated workspace.

### Workflow

#### Step 1: Create Workspace
**Auto-invoke**: workspace-manager agent (haiku)

1. Verify on main branch, clean state
2. Create branch: `{NNN}-Q{XX}-{product-slug}`
3. Create worktree: `../{repo}--{branch}/`
4. Initialize quarter directory structure

#### Step 2: Load Quarter Overview
Read from `specs/quarterly/Q{XX}-overview.md`

#### Step 3: Detailed Product Plan
**Auto-invoke**: product-manager agent (opus)

Create detailed:
- Epic breakdowns with full user stories
- Detailed acceptance criteria
- Story prioritization
- Sprint suggestions (if applicable)

#### Step 4: Frontend Specification
**Auto-invoke**: frontend-engineer agent (opus)

Create detailed:
- Component architecture
- Design token implementation
- State management approach
- Page/route structure
- UI component inventory

#### Step 5: Backend Specification
**Auto-invoke**: backend-engineer agent (sonnet)

Create detailed:
- API endpoint specifications
- Data model contracts
- Database schema
- Authentication/authorization
- Third-party integrations

#### Step 6: Task Breakdown
**Auto-invoke**: tech-lead agent (sonnet)

Create task list:
- Grouped by phase
- Prioritized
- Dependencies mapped
- Sized (S/M/L)
- Acceptance criteria

#### Step 7: Clarification
**Auto-invoke**: clarification-agent (sonnet)

Final clarification round for this quarter.

### Output

```
{worktree}/
└── specs/
    └── quarterly/
        └── Q{XX}/
            ├── plan.md           # Detailed quarter plan
            ├── frontend-spec.md  # Frontend architecture
            ├── backend-spec.md   # Backend architecture
            ├── data-contracts.md # API/data specifications
            └── tasks.md          # Task breakdown
```

### Task Document Structure

```markdown
---
product: {product-name}
quarter: Q{XX}
document: tasks
total-tasks: {N}
status: pending
---

# Tasks: Q{XX} - {Theme}

## Summary
| Phase | Tasks | Parallel | Duration |
|-------|-------|----------|----------|
| Setup | 3 | No | Week 1 |
| Core | 10 | Partial | Week 2-3 |
| Integration | 5 | Yes | Week 4 |
| Polish | 4 | Yes | Week 5 |

## Phase 1: Setup

### T001: Initialize project
[TAGS: Q{XX}, E01, setup]
- Priority: Critical
- Size: S
- Depends: None
- Acceptance:
  - [ ] Project scaffolded
  - [ ] CI/CD configured
  - [ ] Dev environment documented

[Continue with all tasks...]

## Commit Checkpoints

After each phase, offer to:
1. Run cleanup
2. Run tests
3. Create commit

## Implementation Order
[Gantt chart or dependency graph]
```

---

## Collaboration Flow

```
/peachflow:plan (no args)
         │
         ▼
┌─────────────────────────────────────────┐
│     Review Discovery Documents          │
│  product-manager + software-architect   │
└─────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│     Quarter Splitting Strategy          │
│     product-manager + tech-lead         │
└─────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│     Create Quarter Overviews            │
│  (roadmap.md, Q01-overview.md, etc.)    │
└─────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│     Clarification Round                 │
│     clarification-agent                 │
└─────────────────────────────────────────┘
         │
         ▼
[Ready for /peachflow:plan Q1]


/peachflow:plan Q1
         │
         ▼
┌─────────────────────────────────────────┐
│     Create Git Worktree                 │
│     workspace-manager                   │
└─────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│     Detailed Specifications             │
│  frontend-engineer + backend-engineer   │
└─────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│     Task Breakdown                      │
│     tech-lead                           │
└─────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│     Clarification Round                 │
│     clarification-agent                 │
└─────────────────────────────────────────┘
         │
         ▼
[Ready for /peachflow:implement or /peachflow:poc]
```
