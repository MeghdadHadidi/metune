---
name: peachflow:plan
description: Create delivery plan. Without arguments creates overall quarterly roadmap. With quarter argument (Q1, Q2, etc.) creates detailed quarter plan with user stories and tasks. Supports incremental planning for new features added mid-project.
argument-hint: "[Q1|Q2|Q3|Q4 optional]"
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Grep, Glob, Task, AskUserQuestion, Bash
---

# /peachflow:plan - Delivery Planning Phase

Create delivery plans with support for incremental planning when new features are added.

## Output Responsibility

**CRITICAL**: This command is responsible for the unified output to the user.

- Sub-agents return minimal responses (just confirmation of what was done)
- DO NOT let agent responses bubble up to the user
- Collect results from all agents, then provide ONE final summary at the end
- Only this command suggests next steps, not the agents

## Pre-flight Check

**CRITICAL**: Check initialization and requirements status.

```bash
# Check if peachflow is initialized
if [ ! -f ".peachflow-state.json" ]; then
  echo "NOT_INITIALIZED"
fi

# Check design phase status
design_status=$(${CLAUDE_PLUGIN_ROOT}/scripts/state-manager.sh get-phase design)

# Get planning status
plan_status=$(${CLAUDE_PLUGIN_ROOT}/scripts/state-manager.sh get-phase plan)

# Get requirement counts
${CLAUDE_PLUGIN_ROOT}/scripts/doc-parser.sh count brs
${CLAUDE_PLUGIN_ROOT}/scripts/doc-parser.sh count features
${CLAUDE_PLUGIN_ROOT}/scripts/doc-parser.sh count frs
```

**If NOT initialized:**
```
Peachflow is not initialized for this project.

Run /peachflow:init first to set up the project.
```

**If design not completed (for first planning):**
```
Design phase not complete.

Run /peachflow:design first to create architecture and UX specifications.
```

## Mode Detection

| Argument | Plan Status | Mode |
|----------|-------------|------|
| None | `pending` | **Initial Overall Plan** |
| None | `completed` | **Incremental Planning** (check for new requirements) |
| `Q1`, `Q2`, etc. | Any | **Quarterly Plan** |

---

## Requirements Tracking

The state file tracks what's been planned:

```json
{
  "requirements": {
    "planned": ["BR-001", "BR-002", "F-001", "F-002"],
    "unplanned": ["BR-015", "BR-016", "F-020"]
  }
}
```

**Every planning session must:**
1. Check for unplanned requirements
2. Incorporate new requirements appropriately
3. Update planned/unplanned lists when done

---

## Mode 1: Initial Overall Plan

When plan status is `pending` and no quarter specified.

### Workflow

#### Phase 1: Initialize

```bash
mkdir -p docs/04-plan
${CLAUDE_PLUGIN_ROOT}/scripts/state-manager.sh set-phase plan in_progress
```

#### Phase 2: Gather All Requirements

```bash
# List all documented requirements
${CLAUDE_PLUGIN_ROOT}/scripts/doc-search.sh list brs
${CLAUDE_PLUGIN_ROOT}/scripts/doc-search.sh list features
${CLAUDE_PLUGIN_ROOT}/scripts/doc-search.sh list frs
```

#### Phase 3: Product Manager Analysis
**Invoke**: product-manager agent

Product manager will:
- Review BRD to understand business priorities
- Review user research to understand user journey
- Split PRD features into logical delivery phases
- Group features into epics
- Prioritize based on business value and dependencies

#### Phase 4: Tech Lead Consultation
**Invoke**: tech-lead agent

Tech lead will:
- Review proposed epic groupings
- Assess technical dependencies
- Identify what must come first (auth before features)
- Mark requirements that can be delivered in parallel
- Ensure each quarter's requirements form cohesive, testable features

#### Phase 5: Create plan.md

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
  - BRs: BR-001, BR-002
  - Features: F-001, F-002
  - FRs: FR-001, FR-002, FR-003
  - NFRs: NFR-001, NFR-010

- [ ] **E-002: [Epic Name]** - [Brief description]
  - BRs: BR-003
  - Features: F-003
  - FRs: FR-004, FR-005
  - NFRs: NFR-002

#### Parallel Work
- E-001 and E-002 can proceed in parallel
- E-003 depends on E-001

---

### Q2: [Theme/Goal]
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

#### Phase 6: Update Requirements State

```bash
# Mark all requirements as planned
# Extract BR, F, FR, NFR IDs from plan.md
# Move them from unplanned to planned in state
```

Update state file:
```json
{
  "requirements": {
    "planned": ["BR-001", "BR-002", "F-001", "F-002", "FR-001", "FR-002"],
    "unplanned": []
  }
}
```

#### Phase 7: Finalize

```bash
${CLAUDE_PLUGIN_ROOT}/scripts/state-manager.sh set-phase plan completed
```

**Output:**
```
Initial plan complete!

Created: docs/04-plan/plan.md

Planned requirements:
  - Business: BR-001 through BR-XXX
  - Features: F-001 through F-XXX
  - Functional: FR-001 through FR-XXX
  - Non-functional: NFR-001 through NFR-XXX

Quarters defined: Q1, Q2, Q3, Q4

Next: /peachflow:plan Q1 (create detailed quarter plan)
```

---

## Mode 2: Incremental Planning

When plan status is `completed` and no quarter specified - checking for new requirements.

### Detection

```bash
# Check for unplanned requirements
unplanned=$(${CLAUDE_PLUGIN_ROOT}/scripts/state-manager.sh get-unplanned)
if [ -n "$unplanned" ]; then
  echo "NEW_REQUIREMENTS_FOUND"
fi
```

### Workflow

#### Phase 1: Present Status

```bash
# Get counts
${CLAUDE_PLUGIN_ROOT}/scripts/doc-parser.sh count brs
${CLAUDE_PLUGIN_ROOT}/scripts/doc-parser.sh count features

# Get unplanned list
${CLAUDE_PLUGIN_ROOT}/scripts/state-manager.sh get-unplanned
```

```
Existing plan detected.

Current plan status:
  - Q1: [status] (X/Y tasks)
  - Q2: [status] (X/Y tasks)
  - Q3: not started
  - Q4: not started

New requirements found (not yet planned):
  - BR-015: [title from BRD]
  - BR-016: [title from BRD]
  - F-020: [title from PRD]

These need to be incorporated into the plan.
```

#### Phase 2: Impact Analysis
**Invoke**: tech-lead agent

Tech lead will analyze:
1. **Where do new requirements fit?**
   - Which quarter by priority?
   - Which existing epic, or new epic needed?

2. **Impact on in-progress work:**
   - Does this change anything in current quarter?
   - Are there conflicts with existing tasks?

3. **Migration assessment:**
   - Do existing implementations need changes?
   - Is data migration required?
   - What's the blast radius?

Output analysis:
```markdown
## Impact Analysis: New Requirements

### BR-015: [Title]
- **Fits in**: Q2 (extends E-003)
- **Impact**: None - additive feature
- **Migration**: None

### BR-016: [Title]
- **Fits in**: Q1 (new epic E-005)
- **Impact**: HIGH - Affects E-001 (auth changes needed)
- **Migration**: User table schema change required

### F-020: [Title]
- **Fits in**: Q3 (new epic E-008)
- **Impact**: Medium - Requires E-003 modifications
- **Migration**: API versioning recommended
```

#### Phase 3: User Decision

If high-impact changes detected:

```json
{
  "questions": [{
    "question": "New requirements affect existing work. How should we proceed?",
    "header": "Planning",
    "options": [
      {"label": "Incorporate into current quarter", "description": "Add to Q1 now, may extend timeline"},
      {"label": "Schedule for next quarter", "description": "Add to Q2, less disruption"},
      {"label": "Create separate track", "description": "New parallel workstream"},
      {"label": "Review in detail first", "description": "Show full impact analysis before deciding"}
    ],
    "multiSelect": false
  }]
}
```

#### Phase 4: Update Plan

Based on decision, update `/docs/04-plan/plan.md`:

**If adding to existing quarter:**
```markdown
---

## Plan Update: [Date]

### Added Requirements
- BR-015, BR-016, F-020

### Changes to Q1
- Added E-005: [New Epic Name]
- Modified E-001: Added tasks for new auth requirements

### Migration Tasks
- [ ] **M-001: User table migration** - Add new columns for BR-016
  - Must run before E-005 tasks
  - Rollback plan documented

---
```

**If adding to future quarter:**
```markdown
### Q2: [Updated Theme]
[Updated paragraph]

#### Epics
[Existing epics...]

- [ ] **E-008: [New Epic Name]** - From BR-015, F-020
  - BRs: BR-015
  - Features: F-020
  - FRs: [to be defined]
```

#### Phase 5: Update Quarterly Plans (if affected)

If changes affect a quarter that already has detailed plans:

```bash
# Check if quarter has detailed plan
if [ -f "docs/04-plan/quarters/q01/plan.md" ]; then
  echo "UPDATE_QUARTER_PLAN"
fi
```

**Invoke**: tech-lead agent to:
1. Add new user stories to existing `stories.md`
2. Create new task files in `tasks/`
3. Update dependencies in existing tasks if needed
4. Mark migration tasks with `[Migration]` tag

#### Phase 6: Update State

```bash
# Move newly planned requirements to planned list
```

```json
{
  "requirements": {
    "planned": ["BR-001", "...", "BR-015", "BR-016", "F-020"],
    "unplanned": []
  },
  "planUpdates": [
    {
      "date": "2024-01-20",
      "added": ["BR-015", "BR-016", "F-020"],
      "affectedQuarters": ["Q1", "Q2"],
      "migrations": ["M-001"]
    }
  ]
}
```

#### Phase 7: Summary

```
Incremental planning complete!

Added to plan:
  - BR-015: Added to Q2 (E-008)
  - BR-016: Added to Q1 (E-005) - requires migration
  - F-020: Added to Q2 (E-008)

Changes made:
  - docs/04-plan/plan.md (updated)
  - docs/04-plan/quarters/q01/stories.md (5 new stories)
  - docs/04-plan/quarters/q01/tasks/ (8 new tasks)

Migrations required:
  - M-001: User table migration (before Q1 E-005)

No unplanned requirements remaining.

Next steps:
  /peachflow:implement     - Continue implementation
  /peachflow:plan Q2       - Plan Q2 in detail
```

---

## Mode 3: Quarterly Plan

Creates detailed user stories and tasks for a specific quarter.

### Pre-check for New Requirements

Before creating detailed quarter plan, check for unplanned requirements:

```bash
unplanned=$(${CLAUDE_PLUGIN_ROOT}/scripts/state-manager.sh get-unplanned)
if [ -n "$unplanned" ]; then
  echo "WARNING: Unplanned requirements exist"
fi
```

If unplanned requirements exist:
```
Warning: There are unplanned requirements.

Consider running /peachflow:plan (without quarter) first to:
  - Incorporate new requirements into roadmap
  - Assess impact on existing plans

Continue anyway? (New requirements won't be included in this quarter's plan)
```

### Workflow

#### Phase 1: Initialize

```bash
# Normalize quarter format (Q1, Q01 → q01)
quarter=$(echo "$1" | tr '[:upper:]' '[:lower:]' | sed 's/^q/q0/' | sed 's/q0\([0-9][0-9]\)/q\1/')
mkdir -p "docs/04-plan/quarters/${quarter}/tasks"
${CLAUDE_PLUGIN_ROOT}/scripts/state-manager.sh set-quarter "${quarter}"
${CLAUDE_PLUGIN_ROOT}/scripts/state-manager.sh set-quarter-status "${quarter}" "planning"
```

#### Phase 2: Load Quarter Context

Read `/docs/04-plan/plan.md` to get:
- Epics assigned to this quarter
- BR/F/FR/NFR IDs for each epic
- Any migration tasks required

#### Phase 3: User Story Creation
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

### Requirements Traced
- BR-002: User account management
- F-001: User registration
- FR-001: User Registration endpoint
```

Consult tech-lead if story seems too large - split if needed.

#### Phase 4: Task Breakdown
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

### Requirements Traced
- FR-001: User Registration
- NFR-010: Password Storage
```

Each task tagged with:
- **[FE]** - Frontend
- **[BE]** - Backend
- **[DevOps]** - Infrastructure
- **[Full]** - Full-stack
- **[Migration]** - Data/schema migration

#### Phase 5: Create Output Files

`/docs/04-plan/quarters/q01/plan.md`:
```markdown
# Q1 Plan

## Theme
[Quarter theme from overall plan]

## Status
- Started: [date]
- Target: [date]
- Progress: 0/X tasks complete

## Epics

- [ ] **E-001: User Authentication**
  - [ ] US-001: User Registration (3 tasks)
  - [ ] US-002: User Login (2 tasks)
  - [ ] US-003: Password Reset (3 tasks)

- [ ] **E-002: Core Dashboard**
  - [ ] US-004: Dashboard Overview (4 tasks)
  - [ ] US-005: Activity Feed (2 tasks)

## Migrations
- [ ] **M-001: Initial schema** - Run first before any E-001 work

## Dependencies
E-001 → E-002 (auth required for dashboard)
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
requirements: [FR-001, NFR-010]
---

[Full task details]
```

#### Phase 6: Update State

```bash
${CLAUDE_PLUGIN_ROOT}/scripts/state-manager.sh set-quarter-status "${quarter}" "ready"
```

Update state with quarter info:
```json
{
  "quarters": {
    "q01": {
      "status": "ready",
      "plannedAt": "2024-01-15",
      "epics": ["E-001", "E-002"],
      "taskCount": 14,
      "completedTasks": 0
    }
  }
}
```

#### Phase 7: Summary

```
Quarter Q1 planned!

Created:
  - docs/04-plan/quarters/q01/plan.md
  - docs/04-plan/quarters/q01/stories.md
  - docs/04-plan/quarters/q01/tasks/ (14 task files)

Breakdown:
  - Epics: 2
  - User Stories: 5
  - Tasks: 14 (8 BE, 4 FE, 2 DevOps)
  - Migrations: 1

Next: /peachflow:implement (start implementation)
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

---

## Agent Collaboration Flow

### Initial/Incremental Plan
```
┌────────────────────┐
│  product-manager   │ ──→ Epic grouping, quarterly themes
│      (opus)        │
└────────────────────┘
         │
         ▼
┌────────────────────┐
│    tech-lead       │ ──→ Dependencies, impact analysis
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
│ clarification-agent│ ──→ Resolve questions
│     (sonnet)       │
└────────────────────┘
         │
         ▼
   q01/ directory
```

---

## Guidelines

### Planning Principles
- **Testable epics**: Each epic should result in testable functionality
- **Small tasks**: Each task completable in 1-2 days
- **Clear dependencies**: Mark what blocks what
- **Parallel identification**: Maximize concurrent work
- **Traceability**: Every task traces to requirements

### Incremental Planning
- **Check before quarterly planning**: Always check for unplanned requirements first
- **Minimize disruption**: Prefer adding to future quarters over disrupting current work
- **Migration-first**: If migration needed, create those tasks first
- **Document changes**: Keep changelog of plan updates

### ID Conventions
- `BR-XXX`: Business requirements
- `F-XXX`: Features
- `FR-XXX`: Functional requirements
- `NFR-XXX`: Non-functional requirements
- `E-XXX`: Epics
- `US-XXX`: User stories
- `T-XXX`: Tasks
- `M-XXX`: Migrations
