---
name: peachflow:plan
description: Create delivery plan. Without arguments creates overall quarterly roadmap. With quarter argument (Q1, Q2, etc.) creates detailed quarter plan with user stories and tasks.
argument-hint: "[Q1|Q2|Q3|Q4 optional]"
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Grep, Glob, Task, AskUserQuestion, Bash
---

# /peachflow:plan - Delivery Planning Phase

Create delivery plans with two modes: overall roadmap or detailed quarterly plan.

## Prerequisites

Design phase must be complete:
- `/docs/02-product/architecture/high-level-design.md` exists
- `/docs/02-product/ux/` has design documents

Check with:
```bash
${CLAUDE_PLUGIN_ROOT}/scripts/state-manager.sh get-phase design
```

If design not completed, prompt user to run `/peachflow:design` first.

## Mode Detection

- **No argument** (`/peachflow:plan`): Overall plan mode
- **Quarter argument** (`/peachflow:plan Q1`): Quarterly plan mode
  - Accepts: Q1, Q01, q1, q01, Q2, etc.

---

## Mode 1: Overall Plan

Creates the master roadmap splitting delivery into quarters.

### Workflow

1. **Initialize**
```bash
mkdir -p docs/04-plan
${CLAUDE_PLUGIN_ROOT}/scripts/state-manager.sh set-phase plan in_progress
```

2. **Product Manager Analysis**
**Invoke**: product-manager agent

Product manager will:
- Review BRD to understand business priorities
- Review user research to understand user journey
- Split PRD features into logical delivery phases
- Group features into epics

3. **Tech Lead Consultation**
**Invoke**: tech-lead agent

Tech lead will:
- Review proposed epic groupings
- Assess technical dependencies
- Identify what must come first (auth before features)
- Mark requirements that can be delivered in parallel
- Ensure each quarter's requirements form cohesive, testable features

4. **Create plan.md**

Output in `/docs/04-plan/plan.md`:

```markdown
# Delivery Plan

## Overview
[Brief description of delivery strategy]

## Quarterly Roadmap

### Q1: [Theme/Goal]
[Paragraph describing what users will be able to do after Q1]

#### Epics
- [ ] **E-001: [Epic Name]** - [Brief description]
  - FRs: FR-001, FR-002, FR-003
  - NFRs: NFR-001, NFR-010

- [ ] **E-002: [Epic Name]** - [Brief description]
  - FRs: FR-004, FR-005
  - NFRs: NFR-002

#### Parallel Work
- E-001 and E-002 can proceed in parallel
- E-003 depends on E-001

---

### Q2: [Theme/Goal]
[Same structure]

---

### Q3: [Theme/Goal]
[Same structure]

---

### Q4: [Theme/Goal]
[Same structure]

---

## Dependency Graph
```
E-001 ──→ E-003 ──→ E-005
   │
   └──→ E-004

E-002 (parallel)
```

## Risk Assessment
| Risk | Impact | Mitigation |
|------|--------|------------|
| [Risk] | H/M/L | [Action] |
```

5. **Finalize**
```bash
${CLAUDE_PLUGIN_ROOT}/scripts/state-manager.sh set-phase plan completed
```

---

## Mode 2: Quarterly Plan

Creates detailed user stories and tasks for a specific quarter.

### Workflow

1. **Initialize**
```bash
# Normalize quarter format (Q1, Q01 → q01)
quarter=$(echo "$1" | tr '[:upper:]' '[:lower:]' | sed 's/^q/q0/' | sed 's/q0\([0-9][0-9]\)/q\1/')
mkdir -p "docs/04-plan/quarters/${quarter}/tasks"
${CLAUDE_PLUGIN_ROOT}/scripts/state-manager.sh set-quarter "${quarter}"
```

2. **Load Quarter Context**

Read `/docs/04-plan/plan.md` to get:
- Epics assigned to this quarter
- FR/NFR IDs for each epic

3. **User Story Creation**
**Invoke**: product-manager agent

For each epic, product manager creates user stories:

```markdown
## US-001: User Registration

**Epic**: E-001
**As a** new user
**I want to** create an account with my email
**So that** I can access the platform

### Background
[Context from user personas and journeys]

### Acceptance Criteria
- [ ] User can enter email and password
- [ ] Email validation shows inline errors
- [ ] Password strength indicator displayed
- [ ] Verification email sent on success
- [ ] User redirected to onboarding

### FRs Referenced
- FR-001: User Registration
```

Consult tech-lead if story seems too large - split if needed.

4. **Task Breakdown**
**Invoke**: tech-lead agent

For each user story, tech lead creates tasks:

```markdown
## T-001: [BE] Create user registration API endpoint

**Story**: US-001
**Epic**: E-001
**Status**: pending
**Depends On**: none
**Parallel With**: T-002

### Description
Implement POST /api/users endpoint with validation.

### Acceptance Criteria
- [ ] Endpoint accepts email, password, name
- [ ] Validates email format and uniqueness
- [ ] Hashes password with bcrypt
- [ ] Returns 201 with user object (no password)
- [ ] Returns 400 with validation errors
- [ ] Rate limited to 10 requests/minute

### Technical Notes
- Follow API patterns in ADR-003
- Use Zod for validation schema
```

Each task tagged with:
- **[FE]** - Frontend
- **[BE]** - Backend
- **[DevOps]** - Infrastructure
- **[Full]** - Full-stack

5. **Create Output Files**

`/docs/04-plan/quarters/q01/plan.md`:
```markdown
# Q1 Plan

## Theme
[Quarter theme from overall plan]

## Epics

- [ ] **E-001: User Authentication**
  - [ ] US-001: User Registration
  - [ ] US-002: User Login
  - [ ] US-003: Password Reset

- [ ] **E-002: Core Dashboard**
  - [ ] US-004: Dashboard Overview
  - [ ] US-005: Activity Feed
```

`/docs/04-plan/quarters/q01/stories.md`:
```markdown
# Q1 User Stories

## E-001: User Authentication

### US-001: User Registration
[Full user story with acceptance criteria]

#### Tasks
- [ ] T-001: [BE] Create registration API
- [ ] T-002: [FE] Build registration form
- [ ] T-003: [DevOps] Configure email service

### US-002: User Login
[...]
```

`/docs/04-plan/quarters/q01/tasks/001.md`:
```markdown
---
id: T-001
title: "[BE] Create user registration API endpoint"
epic: E-001
story: US-001
status: pending
depends_on: []
parallel_with: [T-002]
---

[Full task details]
```

6. **Finalize**
```bash
echo "Quarter ${quarter} plan complete"
```

---

## Output Structure

### Overall Plan
```
docs/
└── 04-plan/
    └── plan.md          # Master roadmap
```

### Quarterly Plan
```
docs/
└── 04-plan/
    └── quarters/
        └── q01/
            ├── plan.md      # Quarter epics
            ├── stories.md   # User stories
            └── tasks/
                ├── 001.md   # Task files
                ├── 002.md
                └── ...
```

## Agent Collaboration Flow

### Overall Plan
```
┌────────────────────┐
│  product-manager   │ ──→ Epic grouping, quarterly themes
│      (opus)        │
└────────────────────┘
         │
         ▼
┌────────────────────┐
│    tech-lead       │ ──→ Dependency validation
│      (opus)        │
└────────────────────┘
         │
         ▼
      plan.md
```

### Quarterly Plan
```
┌────────────────────┐
│  product-manager   │ ──→ User stories
│      (opus)        │
└────────────────────┘
         │
         ▼
┌────────────────────┐
│    tech-lead       │ ──→ Task breakdown
│      (opus)        │
└────────────────────┘
         │
         ▼
┌────────────────────┐
│ clarification-agent│ ──→ Resolved questions
│     (sonnet)       │
└────────────────────┘
         │
         ▼
   q01/ directory
```

## Guidelines

- **Testable epics**: Each epic should result in testable functionality
- **Small tasks**: Each task completable in 1-2 days
- **Clear dependencies**: Mark what blocks what
- **Parallel identification**: Maximize concurrent work
- **ID consistency**: Use FR-XXX, NFR-XXX, E-XXX, US-XXX, T-XXX
