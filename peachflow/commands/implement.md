---
name: peachflow:implement
description: Execute implementation tasks from sprints. Accepts sprint id/index, quarter, or task id. Creates sprint-named worktrees for isolation.
argument-hint: "[sprint01|S-001|Q1|T-001|next]"
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, Task, AskUserQuestion
---

# /peachflow:implement - Implementation Phase

Execute implementation tasks from sprint files with smart branch and worktree management.

## Output Responsibility

**CRITICAL**: This command is responsible for the unified output to the user.

- Sub-agents return minimal responses (just confirmation of what was done)
- DO NOT let agent responses bubble up to the user
- Collect results from all agents, then provide ONE final summary at the end
- Only this command suggests next steps, not the agents

## Pre-flight Checks

**CRITICAL**: Before doing anything else, run these checks.

### Step 1: Check Git Status

```bash
current_branch=$(git branch --show-current)
has_changes=$(${CLAUDE_PLUGIN_ROOT}/scripts/git-helper.sh has-changes)
```

### Step 2: Check Initialization

```bash
if [ ! -f ".peachflow-state.json" ]; then
  echo "NOT_INITIALIZED"
fi
```

---

## Argument Detection

| Argument | Mode |
|----------|------|
| None | **Show Status** |
| `sprint01` or `S-001` | **Sprint Mode** - Execute specific sprint |
| `Q1`, `Q2`, etc. | **Quarter Mode** - Execute all sprints in quarter sequentially |
| `T-001` | **Task Mode** - Execute single task |
| `next` | **Auto Mode** - Find and execute next available task |

---

## Mode 0: Show Status (No Argument)

When called without arguments, show current implementation status.

```bash
quarter=$(${CLAUDE_PLUGIN_ROOT}/scripts/state-manager.sh get-quarter)
${CLAUDE_PLUGIN_ROOT}/scripts/sprint-manager.sh list-sprints "$quarter"
```

Output:
```
Quarter: Q1
Progress: 8/14 tasks complete

Sprints:
  S-001: Auth Foundation [completed] (5/5)
  S-002: User Dashboard [in_progress] (3/5)
  S-003: Settings & Profile [pending] (0/4)

Ready tasks in current sprint:
  - T-006: [FE] Dashboard activity feed
  - T-007: [BE] Activity API endpoint

Run: /peachflow:implement sprint02 (continue sprint)
     /peachflow:implement T-006 (specific task)
     /peachflow:implement next (auto-select)
```

---

## Mode 1: Sprint Mode

Execute a specific sprint by name or ID.

### Workflow

#### Phase 1: Parse Sprint Argument

```bash
# Normalize sprint input (sprint01, sprint1, S-001 → sprint01)
if [[ "$1" =~ ^S-([0-9]+)$ ]]; then
  sprint_num=$(printf "%02d" "${BASH_REMATCH[1]}")
  sprint="sprint${sprint_num}"
elif [[ "$1" =~ ^sprint([0-9]+)$ ]]; then
  sprint_num=$(printf "%02d" "${BASH_REMATCH[1]}")
  sprint="sprint${sprint_num}"
else
  sprint="$1"
fi

quarter=$(${CLAUDE_PLUGIN_ROOT}/scripts/state-manager.sh get-quarter)
```

#### Phase 2: Check Branch Context

```bash
current_branch=$(git branch --show-current)
```

**If on main/master:**

1. Check for uncommitted changes:
```bash
has_changes=$(${CLAUDE_PLUGIN_ROOT}/scripts/git-helper.sh has-changes)
if [ "$has_changes" = "true" ]; then
  echo "Uncommitted changes. Commit first."
  exit 1
fi
```

2. Create worktree for sprint:
```bash
# Get sprint name from file
sprint_name=$(awk -F': ' '/^name:/ {gsub(/"/, "", $2); print $2}' "docs/04-plan/quarters/${quarter}/${sprint}.md")
sprint_slug=$(echo "$sprint_name" | tr '[:upper:]' '[:lower:]' | tr ' ' '-')

branch_name="peachflow/${quarter}-${sprint}-${sprint_slug}"
worktree_path="../${PWD##*/}-${quarter}-${sprint}"

git worktree add -b "$branch_name" "$worktree_path"

${CLAUDE_PLUGIN_ROOT}/scripts/sprint-manager.sh set-status "$quarter" "$sprint" "in_progress"
```

Output:
```
Created worktree: $worktree_path
Branch: $branch_name

To continue:
  cd $worktree_path
  /peachflow:implement $sprint
```

**If on feature branch (worktree):**

Continue to task execution within sprint.

#### Phase 3: Sprint Task Execution

```bash
# Mark sprint as in progress
${CLAUDE_PLUGIN_ROOT}/scripts/sprint-manager.sh set-status "$quarter" "$sprint" "in_progress"

# Get ready tasks
ready_tasks=$(${CLAUDE_PLUGIN_ROOT}/scripts/sprint-manager.sh ready-tasks "$quarter" "$sprint")
```

Execute tasks following the parallel execution rules (see Task Execution section).

#### Phase 4: Sprint Completion Check

After each task batch:

```bash
is_complete=$(${CLAUDE_PLUGIN_ROOT}/scripts/sprint-manager.sh is-complete "$quarter" "$sprint")
if [ "$is_complete" = "true" ]; then
  ${CLAUDE_PLUGIN_ROOT}/scripts/sprint-manager.sh set-status "$quarter" "$sprint" "completed"
fi
```

---

## Mode 2: Quarter Mode

Execute all sprints in a quarter sequentially, asking user before each new sprint.

### Workflow

#### Phase 1: Setup Quarter

```bash
quarter=$(echo "$1" | tr '[:upper:]' '[:lower:]' | sed 's/^q/q0/' | sed 's/q0\([0-9][0-9]\)/q\1/')

# Check for uncommitted changes on main
if [ "$(git branch --show-current)" = "main" ]; then
  has_changes=$(${CLAUDE_PLUGIN_ROOT}/scripts/git-helper.sh has-changes)
  if [ "$has_changes" = "true" ]; then
    echo "Uncommitted changes. Commit first."
    exit 1
  fi
fi

# Create worktree for quarter
branch_name="peachflow/${quarter}"
worktree_path="../${PWD##*/}-${quarter}"
git worktree add -b "$branch_name" "$worktree_path"

${CLAUDE_PLUGIN_ROOT}/scripts/state-manager.sh set-quarter "$quarter"
${CLAUDE_PLUGIN_ROOT}/scripts/state-manager.sh set-quarter-status "$quarter" "in_progress"
```

#### Phase 2: Sprint Loop

```bash
while true; do
  # Get next incomplete sprint
  next_sprint=$(${CLAUDE_PLUGIN_ROOT}/scripts/sprint-manager.sh next-sprint "$quarter")

  if [ "$next_sprint" = "none" ]; then
    echo "All sprints complete!"
    break
  fi

  # Execute sprint tasks
  # ... (same as Sprint Mode Phase 3)

  # After sprint completes, ask user before next sprint
done
```

#### Phase 3: Between Sprints - User Checkpoint

After completing each sprint, use AskUserQuestion:

```json
{
  "questions": [{
    "question": "Sprint complete. Next action?",
    "header": "Continue?",
    "options": [
      {"label": "Continue to next sprint (Recommended)", "description": "Start the next sprint"},
      {"label": "Commit and pause", "description": "Commit current work, continue later"},
      {"label": "Review first", "description": "Review completed work before continuing"}
    ],
    "multiSelect": false
  }]
}
```

**If "Continue":** Mark sprint complete, start next sprint
**If "Commit and pause":** Show commit summary, stop
**If "Review first":** Show completed tasks summary, then ask again

---

## Mode 3: Task Mode

Execute a single specific task.

### Workflow

```bash
task_id="$1"
quarter=$(${CLAUDE_PLUGIN_ROOT}/scripts/state-manager.sh get-quarter)

# Find which sprint contains this task
for sprint_file in docs/04-plan/quarters/${quarter}/sprint*.md; do
  if grep -q "^### ${task_id}:" "$sprint_file"; then
    sprint=$(basename "$sprint_file" .md)
    break
  fi
done

# Get task details
${CLAUDE_PLUGIN_ROOT}/scripts/sprint-manager.sh get-task "$quarter" "$task_id"
```

Then execute single task (see Task Execution section).

---

## Mode 4: Auto Mode (next)

Find and execute the next available task.

```bash
quarter=$(${CLAUDE_PLUGIN_ROOT}/scripts/state-manager.sh get-quarter)
current_sprint=$(${CLAUDE_PLUGIN_ROOT}/scripts/sprint-manager.sh next-sprint "$quarter")

if [ "$current_sprint" = "none" ]; then
  echo "All sprints in $quarter complete!"
  exit 0
fi

# Get first ready task
ready_tasks=$(${CLAUDE_PLUGIN_ROOT}/scripts/sprint-manager.sh ready-tasks "$quarter" "$current_sprint")
first_task=$(echo "$ready_tasks" | grep -oE "T-[0-9]+" | head -1)

# Execute that task
```

---

## Task Execution

Core task execution logic used by all modes.

### 1. Load Task Context

```bash
task_data=$(${CLAUDE_PLUGIN_ROOT}/scripts/sprint-manager.sh get-task "$quarter" "$task_id")
```

### 2. Determine Agent by Tag

| Tag | Agent |
|-----|-------|
| [FE] | frontend-developer |
| [BE] | backend-developer |
| [DevOps] | devops-engineer |
| [Full] | frontend + backend (sequential) |

### 3. Pre-Parsed Context for Agent

**CRITICAL**: Pass all task context in the prompt. Do NOT tell agent to read files.

```markdown
## Task Context (Pre-Parsed)

**Task**: T-001
**Title**: [BE] Create user registration API
**Description**: Implement POST /api/users endpoint with validation.
**Sprint**: sprint01 (Auth Foundation)

**Story Reference**: US-001 (see stories.md for acceptance criteria)

**Paths for Status Updates**:
- SPRINT_PATH: docs/04-plan/quarters/${quarter}/${sprint}.md
- TASK_ID: T-001

Implement this task. Mark complete when done.
```

### 4. Update Task Status

After agent completes:

```bash
${CLAUDE_PLUGIN_ROOT}/scripts/sprint-manager.sh complete-task "$quarter" "$sprint" "$task_id"
```

---

## Parallel Execution

When multiple independent tasks are available:

### Get Max Parallel Setting

```bash
max_parallel=$(${CLAUDE_PLUGIN_ROOT}/scripts/state-manager.sh get-max-parallel)
```

### Group Ready Tasks

```bash
ready_tasks=$(${CLAUDE_PLUGIN_ROOT}/scripts/sprint-manager.sh ready-tasks "$quarter" "$sprint")
```

### Launch Parallel Agents

**CRITICAL**: Never launch more than `max_parallel` agents simultaneously.

```bash
# Example: max_parallel=3, 5 ready tasks
# Batch 1: Launch first 3 tasks
# Wait for completion
# Batch 2: Launch remaining 2 tasks
```

### Checkpoint After 2 Rounds

After completing 2 batches of parallel execution, use AskUserQuestion:

```json
{
  "questions": [{
    "question": "2 rounds completed. Continue?",
    "header": "Continue?",
    "options": [
      {"label": "Continue (Recommended)", "description": "Proceed to next batch"},
      {"label": "Pause and review", "description": "Stop to review work"},
      {"label": "Commit progress", "description": "Commit changes so far"}
    ],
    "multiSelect": false
  }]
}
```

Show brief summary before question:
```
Completed: T-001, T-002, T-003, T-004
Progress: 4/10 tasks in sprint
Remaining: T-005, T-006 (ready), T-007 (blocked)
```

---

## Agent Routing

| Tag | Agent | Model |
|-----|-------|-------|
| [FE] | frontend-developer | opus |
| [BE] | backend-developer | opus |
| [DevOps] | devops-engineer | sonnet |
| [Full] | frontend + backend | opus |

---

## Worktree Naming

Worktrees are named to include sprint context:

**Sprint-level worktree:**
```
../projectname-q01-sprint01/
Branch: peachflow/q01-sprint01-auth-foundation
```

**Quarter-level worktree:**
```
../projectname-q01/
Branch: peachflow/q01
```

---

## Output Examples

### Sprint Start
```
Starting sprint01: Auth Foundation

Tasks: 5 (3 parallel in first batch)
  - T-001 [BE]: Create user registration API
  - T-002 [FE]: Build registration form
  - T-003 [DevOps]: Configure email service
  - T-004 [BE]: Implement login API (after T-001)
  - T-005 [FE]: Build login form (after T-002, T-004)

Launching T-001, T-002, T-003 in parallel...
```

### Task Completion
```
Completed: T-001 [BE] Create user registration API

Sprint progress: 1/5
Next ready: T-004 [BE] (was waiting on T-001)
```

### Sprint Completion
```
Sprint sprint01 complete!

Completed tasks:
  [x] T-001: Create user registration API
  [x] T-002: Build registration form
  [x] T-003: Configure email service
  [x] T-004: Implement login API
  [x] T-005: Build login form

Ready for next sprint: sprint02 (User Dashboard)
```

---

## Guidelines

- **Always check git status first**
- **Respect branch context**: Different flows for main vs feature branches
- **Never auto-commit**: User must commit manually
- **Update sprint status**: Mark tasks and sprints as complete
- **Parallel when possible**: Launch independent tasks together
- **Ask before new sprint**: Always checkpoint between sprints
