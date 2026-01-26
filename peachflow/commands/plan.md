---
name: peachflow:plan
description: Create delivery plan. Without arguments creates overall quarterly roadmap. With quarter argument (Q1, Q2, etc.) creates detailed quarter plan with sprints. Use --migrate flag to convert existing task files to sprint format.
argument-hint: "[Q1|Q2|Q3|Q4] [--migrate]"
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Grep, Glob, Task, AskUserQuestion, Bash
---

# /peachflow:plan - Delivery Planning Phase

Create delivery plans with support for incremental planning and sprint-based task organization.

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
Peachflow not initialized. Run /peachflow:init first.
```

**If design not completed (for first planning):**
```
Design phase not complete. Run /peachflow:design first.
```

## Mode Detection

| Argument | Mode |
|----------|------|
| `--migrate` | **Migration Mode** - Convert task files to sprints |
| None (plan pending) | **Initial Overall Plan** |
| None (plan completed) | **Incremental Planning** |
| `Q1`, `Q2`, etc. | **Quarterly Plan with Sprints** |

---

## Mode 0: Migration Mode (--migrate)

Converts existing task files to sprint format.

### Workflow

#### Phase 1: Detect Existing Tasks

```bash
# Find all quarters with task files
for quarter_dir in docs/04-plan/quarters/q*/; do
  if [ -d "${quarter_dir}tasks" ]; then
    task_count=$(ls "${quarter_dir}tasks"/*.md 2>/dev/null | wc -l)
    echo "$(basename $quarter_dir): $task_count tasks"
  fi
done
```

#### Phase 2: For Each Quarter with Tasks

```bash
quarter="q01"
tasks_dir="docs/04-plan/quarters/${quarter}/tasks"
```

1. **Read all task files** and extract:
   - Task ID, title, description
   - Dependencies (depends_on)
   - Status (pending/completed)

2. **Group into sprints by dependency levels:**
   - Sprint 1: Tasks with no dependencies
   - Sprint 2: Tasks depending on Sprint 1 tasks
   - Sprint 3: Tasks depending on Sprint 2 tasks
   - etc.
   - Max 10 tasks per sprint

3. **Determine sprint names** from the epic/theme of tasks in that sprint

#### Phase 3: Create Sprint Files

For each sprint, create `sprintNN.md`:

```markdown
---
id: S-001
name: "Auth Foundation"
status: pending
last_updated: 2024-01-15T10:30:00Z
---

# Sprint 01: Auth Foundation

## Tasks

### T-001: [BE] Create user registration API
Implement POST /api/users endpoint with validation.
**Depends on:** none
**Parallel with:** T-002, T-003

### T-002: [FE] Build registration form
Create registration form with email/password validation.
**Depends on:** none
**Parallel with:** T-001, T-003
```

**Task format in sprint files:**
- Title includes tag and task name
- One line description (brief, no checklists)
- Dependencies listed
- Parallel tasks listed
- Status only added when completed

#### Phase 4: Verify and Delete Old Tasks

```bash
# Count tasks in sprints
sprint_task_count=$(grep -c "^### T-" docs/04-plan/quarters/${quarter}/sprint*.md | awk -F: '{sum+=$2} END {print sum}')

# Count original task files
original_count=$(ls docs/04-plan/quarters/${quarter}/tasks/*.md 2>/dev/null | wc -l)

# Only delete if counts match
if [ "$sprint_task_count" -eq "$original_count" ]; then
  rm -rf "docs/04-plan/quarters/${quarter}/tasks"
  echo "Migrated ${original_count} tasks to sprints, deleted task files"
else
  echo "ERROR: Task count mismatch. Keeping original files."
fi
```

#### Phase 5: Summary

```
Migration complete!

Q1: 14 tasks → 3 sprints
  - sprint01: Auth Foundation (5 tasks)
  - sprint02: User Dashboard (5 tasks)
  - sprint03: Settings & Profile (4 tasks)

Q2: 12 tasks → 2 sprints
  - sprint01: Payment Integration (6 tasks)
  - sprint02: Notifications (6 tasks)

Original task files deleted after verification.
```

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
${CLAUDE_PLUGIN_ROOT}/scripts/doc-search.sh list brs
${CLAUDE_PLUGIN_ROOT}/scripts/doc-search.sh list features
${CLAUDE_PLUGIN_ROOT}/scripts/doc-search.sh list frs
```

#### Phase 3: Product Manager Analysis
**Invoke**: product-manager agent

Product manager will:
- Review BRD to understand business priorities
- Split PRD features into logical delivery phases
- Group features into epics
- Prioritize based on business value and dependencies

#### Phase 4: Tech Lead Consultation
**Invoke**: tech-lead agent

Tech lead will:
- Review proposed epic groupings
- Assess technical dependencies
- Identify what must come first
- Mark requirements that can be delivered in parallel
- **Consider testing strategy** from project settings when planning

#### Phase 5: Create plan.md

Output in `/docs/04-plan/plan.md`:

```markdown
# Delivery Plan

## Overview
[Brief description of delivery strategy]

## Testing Strategy
[From project settings: strategy + intensity]

## Quarterly Roadmap

### Q1: [Theme/Goal]
[Paragraph describing what users will be able to do after Q1]

#### Epics
- [ ] **E-001: [Epic Name]** - [Brief description]
  - BRs: BR-001, BR-002
  - Features: F-001, F-002

#### Parallel Work
- E-001 and E-002 can proceed in parallel
```

#### Phase 6: Update State and Finalize

```bash
${CLAUDE_PLUGIN_ROOT}/scripts/state-manager.sh set-phase plan completed
```

**Output:**
```
Initial plan complete!

Created: docs/04-plan/plan.md
Quarters defined: Q1, Q2, Q3, Q4

Next: /peachflow:plan Q1
```

---

## Mode 2: Incremental Planning

When plan status is `completed` and no quarter specified - checking for new requirements.

### Detection

```bash
unplanned=$(${CLAUDE_PLUGIN_ROOT}/scripts/state-manager.sh get-unplanned)
if [ -n "$unplanned" ]; then
  echo "NEW_REQUIREMENTS_FOUND"
fi
```

### Workflow

Same as before - invoke tech-lead for impact analysis, update plan.md with new requirements.

---

## Mode 3: Quarterly Plan with Sprints

Creates detailed user stories and sprint files for a specific quarter.

### Workflow

#### Phase 1: Initialize

```bash
quarter=$(echo "$1" | tr '[:upper:]' '[:lower:]' | sed 's/^q/q0/' | sed 's/q0\([0-9][0-9]\)/q\1/')
mkdir -p "docs/04-plan/quarters/${quarter}"
${CLAUDE_PLUGIN_ROOT}/scripts/state-manager.sh set-quarter "${quarter}"
${CLAUDE_PLUGIN_ROOT}/scripts/state-manager.sh set-quarter-status "${quarter}" "planning"
```

#### Phase 2: Load Quarter Context

Read `/docs/04-plan/plan.md` to get:
- Epics assigned to this quarter
- BR/F/FR/NFR IDs for each epic
- Testing strategy from project settings

#### Phase 3: User Story Creation
**Invoke**: product-manager agent

For each epic, create user stories in `stories.md`.

#### Phase 4: Task Breakdown
**Invoke**: tech-lead agent

For each user story, tech lead creates tasks with:
- Task ID, title (with tag), brief description
- Dependencies
- Consider testing strategy when estimating tasks

#### Phase 5: Group Tasks into Sprints

**Sprint grouping rules:**
1. Group tasks by dependency levels
2. First sprint: all tasks with no dependencies
3. Next sprint: tasks whose dependencies are in previous sprints
4. Max 10 tasks per sprint
5. Name each sprint based on its theme/goal

#### Phase 6: Create Sprint Files

```bash
# Create sprint files instead of individual task files
for sprint_num in 01 02 03; do
  sprint_file="docs/04-plan/quarters/${quarter}/sprint${sprint_num}.md"
done
```

**Sprint file format:**

```markdown
---
id: S-001
name: "Auth Foundation"
status: pending
last_updated: 2024-01-15T10:30:00Z
---

# Sprint 01: Auth Foundation

## Tasks

### T-001: [BE] Create user registration API
Implement POST /api/users endpoint with validation.
**Depends on:** none
**Parallel with:** T-002, T-003

### T-002: [FE] Build registration form
Create registration form with email/password validation.
**Depends on:** none
**Parallel with:** T-001, T-003

### T-003: [DevOps] Configure email service
Set up email sending infrastructure.
**Depends on:** none
**Parallel with:** T-001, T-002

### T-004: [BE] Implement login API
Create POST /api/auth/login with JWT tokens.
**Depends on:** T-001

### T-005: [FE] Build login form
Create login form integrated with API.
**Depends on:** T-002, T-004
```

#### Phase 7: Create Quarter Plan Summary

`/docs/04-plan/quarters/q01/plan.md`:
```markdown
# Q1 Plan

## Theme
[Quarter theme from overall plan]

## Sprints

### Sprint 01: Auth Foundation
- 5 tasks (3 parallel, 2 sequential)
- Goal: Basic user auth working

### Sprint 02: User Dashboard
- 5 tasks
- Goal: Dashboard with activity feed

### Sprint 03: Settings & Profile
- 4 tasks
- Goal: User can manage their account
```

#### Phase 8: Update State

```bash
${CLAUDE_PLUGIN_ROOT}/scripts/state-manager.sh set-quarter-status "${quarter}" "ready"
```

#### Phase 9: Summary

```
Quarter Q1 planned!

Created:
  - docs/04-plan/quarters/q01/plan.md
  - docs/04-plan/quarters/q01/stories.md
  - docs/04-plan/quarters/q01/sprint01.md (5 tasks)
  - docs/04-plan/quarters/q01/sprint02.md (5 tasks)
  - docs/04-plan/quarters/q01/sprint03.md (4 tasks)

Breakdown:
  - Epics: 2
  - User Stories: 5
  - Tasks: 14 (8 BE, 4 FE, 2 DevOps)
  - Sprints: 3

Next: /peachflow:implement (or /peachflow:implement sprint01)
```

---

## Sprint File Format Reference

```markdown
---
id: S-001
name: "Short Sprint Name"
status: pending|in_progress|completed
last_updated: 2024-01-15T10:30:00Z
---

# Sprint NN: Short Sprint Name

## Tasks

### T-XXX: [TAG] Task Title
Brief one-line description of what needs to be done.
**Depends on:** T-YYY, T-ZZZ (or "none")
**Parallel with:** T-AAA, T-BBB
**Status:** completed (only add when done)
```

**Key principles:**
- Minimal task descriptions (no checklists, no acceptance criteria)
- Dependencies clearly marked
- Parallel work identified
- Status only appears when completed
- Max 10 tasks per sprint

---

## Utility Scripts for Sprints

```bash
# List tasks in a sprint
${CLAUDE_PLUGIN_ROOT}/scripts/sprint-manager.sh list-tasks q01 sprint01

# Get tasks ready to execute (no blocking deps)
${CLAUDE_PLUGIN_ROOT}/scripts/sprint-manager.sh ready-tasks q01 sprint01

# Get single task details
${CLAUDE_PLUGIN_ROOT}/scripts/sprint-manager.sh get-task q01 T-001

# Mark task complete
${CLAUDE_PLUGIN_ROOT}/scripts/sprint-manager.sh complete-task q01 sprint01 T-001

# Get next incomplete sprint
${CLAUDE_PLUGIN_ROOT}/scripts/sprint-manager.sh next-sprint q01

# Check if sprint is complete
${CLAUDE_PLUGIN_ROOT}/scripts/sprint-manager.sh is-complete q01 sprint01
```

---

## Output Structure

### Overall Plan
```
docs/
└── 04-plan/
    └── plan.md          # Master roadmap
```

### Quarterly Plan with Sprints
```
docs/
└── 04-plan/
    └── quarters/
        └── q01/
            ├── plan.md       # Quarter overview
            ├── stories.md    # User stories
            ├── sprint01.md   # First sprint tasks
            ├── sprint02.md   # Second sprint tasks
            └── sprint03.md   # Third sprint tasks
```

---

## Guidelines

### Sprint Organization
- **Dependency-first**: Group tasks by dependency levels
- **Max 10 tasks**: Keep sprints manageable
- **Thematic naming**: Sprint name reflects its goal
- **Parallel identification**: Mark what can run concurrently

### Task Format in Sprints
- **Minimal**: Title + one line description only
- **No checklists**: Those are in stories.md
- **Dependencies explicit**: Always list depends_on
- **Tags required**: [FE], [BE], [DevOps], [Full]

### ID Conventions
- `S-XXX`: Sprints
- `T-XXX`: Tasks
- `E-XXX`: Epics
- `US-XXX`: User stories
