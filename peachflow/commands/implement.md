---
name: peachflow:implement
description: Execute implementation tasks from quarterly plan. Handles branch management, worktrees, and assigns tasks to specialized developer agents.
argument-hint: "[task_id|next|all]"
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, Task, AskUserQuestion
---

# /peachflow:implement - Implementation Phase

Execute implementation tasks from the quarterly plan with smart branch and worktree management.

## Output Responsibility

**CRITICAL**: This command is responsible for the unified output to the user.

- Sub-agents return minimal responses (just confirmation of what was done)
- DO NOT let agent responses bubble up to the user
- Collect results from all agents, then provide ONE final summary at the end
- Only this command suggests next steps, not the agents

## Pre-flight Checks

**CRITICAL**: Before doing anything else, run these checks in order.

### Step 1: Check Git Status

```bash
# Get current branch
current_branch=$(git branch --show-current)

# Check for uncommitted changes
git_status=$(git status --porcelain)
```

### Step 2: Branch-Based Workflow

Based on the current branch, follow the appropriate workflow:

---

## Workflow A: On Main Branch

If `current_branch` is `main` or `master`:

### A.1: Check for Uncommitted Changes

```bash
# Use git-helper script for clean detection
has_changes=$(${CLAUDE_PLUGIN_ROOT}/scripts/git-helper.sh has-changes)
```

**If uncommitted changes exist (`has_changes` is "true"):**

Show brief status and stop:
```
Uncommitted changes detected on main. Please commit before continuing.

Run: git status
```

**STOP** - Do not continue until user commits and re-runs.

### A.2: Find Current/Next Quarter

```bash
# Get current quarter from state
current_quarter=$(${CLAUDE_PLUGIN_ROOT}/scripts/state-manager.sh get-quarter)

# Check quarter progress
progress=$(${CLAUDE_PLUGIN_ROOT}/scripts/state-manager.sh get-quarter-progress "$current_quarter")
# Returns: completed/total:in_progress:pending
```

Parse progress: `completed/total:in_progress:pending`

### A.3: Quarter Complete - Transition to Next

If `completed == total` and `in_progress == 0` and `pending == 0`:

1. Mark current quarter as completed:
```bash
${CLAUDE_PLUGIN_ROOT}/scripts/state-manager.sh set-quarter-status "$current_quarter" "completed"
```

2. Determine next quarter:
```bash
next_quarter=$(${CLAUDE_PLUGIN_ROOT}/scripts/state-manager.sh get-next-quarter "$current_quarter")
```

3. Check if next quarter plan exists:
```bash
if [ -d "docs/04-plan/quarters/${next_quarter}" ]; then
  echo "NEXT_QUARTER_EXISTS"
fi
```

4. If next quarter exists:
   - Set it as current and in_progress
   - Create worktree for it
   - Switch to worktree

5. If next quarter doesn't exist:
```
Quarter $current_quarter is complete!

No plan exists for $next_quarter yet.
Run /peachflow:plan $next_quarter to create the next quarter plan.
```

### A.4: Create Worktree and Switch

```bash
# Create feature branch for the quarter
branch_name="peachflow/${next_quarter}"
worktree_path="../${PWD##*/}-${next_quarter}"

# Create worktree
git worktree add -b "$branch_name" "$worktree_path"

# Update state with worktree location
${CLAUDE_PLUGIN_ROOT}/scripts/state-manager.sh set-worktree "$next_quarter" "$worktree_path"
${CLAUDE_PLUGIN_ROOT}/scripts/state-manager.sh set-quarter "$next_quarter"
${CLAUDE_PLUGIN_ROOT}/scripts/state-manager.sh set-quarter-status "$next_quarter" "in_progress"
```

Present to user:
```
Quarter $next_quarter worktree created at: $worktree_path

To continue implementation:
  cd $worktree_path
  /peachflow:implement

Or stay here and I'll work in the worktree context.
```

---

## Workflow B: On Feature Branch

If `current_branch` is NOT `main` or `master`:

### B.1: Identify Quarter from Branch

```bash
# Try to extract quarter from branch name (e.g., peachflow/q01)
quarter=$(echo "$current_branch" | grep -oE 'q[0-9]+' | head -1)

# If not found, use current quarter from state
if [ -z "$quarter" ]; then
  quarter=$(${CLAUDE_PLUGIN_ROOT}/scripts/state-manager.sh get-quarter)
fi
```

### B.2: Check Quarter Progress

```bash
progress=$(${CLAUDE_PLUGIN_ROOT}/scripts/state-manager.sh get-quarter-progress "$quarter")
```

Parse: `completed/total:in_progress:pending`

### B.3: All Tasks Complete

If all tasks are done (`pending == 0` and `in_progress == 0`):

```
$quarter complete. Please commit and merge manually.
```

**STOP** - Wait for user to commit and merge.

### B.4: Work In Progress

If there are tasks remaining (`pending > 0` or `in_progress > 0`):

Continue to **Task Execution** workflow below.

---

## Task Execution

Once pre-flight checks pass and we're ready to work:

### 1. Load Quarter Context

```bash
quarter=$(${CLAUDE_PLUGIN_ROOT}/scripts/state-manager.sh get-quarter)
tasks_dir="docs/04-plan/quarters/${quarter}/tasks"
```

### 2. Analyze Tasks

Read all task files and categorize:
- **Pending**: status: pending, no unfinished dependencies
- **Blocked**: status: pending, has unfinished dependencies
- **In Progress**: status: in_progress
- **Completed**: status: completed

### 3. Task Selection

Based on argument:

#### No Argument
Show task status and ask which to work on:
```
Quarter: $quarter
Progress: $completed/$total complete

Available Tasks:
  [FE] T-002: Build registration form (pending)
  [BE] T-003: Implement login API (pending)
  [DevOps] T-007: Set up email service (pending, parallel)

Blocked Tasks:
  [FE] T-004: Build login form (blocked by T-003)

In Progress:
  [BE] T-001: Implement registration API (in_progress)

Which task would you like to work on?
```

#### Specific Task (T-NNN)
1. Check task exists
2. Check not already completed
3. Check dependencies met
4. Execute task

#### Next
Find first available task (not blocked, not completed) and execute.

#### All
1. Identify all executable tasks
2. Group by parallelism
3. Launch parallel agents for independent tasks

### 4. Task Execution

For each task:

1. **Read Task File**
```bash
task_file="docs/04-plan/quarters/${quarter}/tasks/NNN.md"
${CLAUDE_PLUGIN_ROOT}/scripts/doc-parser.sh task T-NNN
```

2. **Determine Agent by Tag**
- `[FE]` → frontend-developer
- `[BE]` → backend-developer
- `[DevOps]` → devops-engineer
- `[Full]` → frontend-developer + backend-developer (sequential)

3. **Update Task Status**
```bash
${CLAUDE_PLUGIN_ROOT}/scripts/checklist-manager.sh status "$task_file" "in_progress"
```

4. **Invoke Agent**
Pass task context to appropriate agent via Task tool.

5. **Agent Execution**
Agent will:
- Read task requirements
- Consult design/architecture docs
- Implement the feature
- Mark acceptance criteria as done
- Update task status to completed

6. **Update Checklists**
```bash
# Mark task done in stories.md
${CLAUDE_PLUGIN_ROOT}/scripts/checklist-manager.sh check \
  "docs/04-plan/quarters/${quarter}/stories.md" "T-NNN"

# Mark task done in plan.md
${CLAUDE_PLUGIN_ROOT}/scripts/checklist-manager.sh check \
  "docs/04-plan/quarters/${quarter}/plan.md" "T-NNN"
```

### 5. After Task Completion

Show status and next steps:
```
Task T-001 completed

Acceptance Criteria:
  [x] POST /api/users endpoint created
  [x] Email validation implemented
  [x] Password hashing with bcrypt
  [x] Returns 201 on success

Progress: $completed/$total complete

Next available tasks:
  [FE] T-002: Build registration form
  [BE] T-003: Implement login API

Continue with /peachflow:implement next
```

---

## Agent Routing

| Tag | Agent | Model |
|-----|-------|-------|
| [FE] | frontend-developer | opus |
| [BE] | backend-developer | opus |
| [DevOps] | devops-engineer | sonnet |
| [Full] | frontend + backend | opus |

## Parallel Execution

When `all` argument or multiple independent tasks:

1. **Identify Parallel Groups**
```
Group 1 (parallel):
  - T-001 [BE]: Registration API
  - T-002 [FE]: Registration form
  - T-007 [DevOps]: Email service

Group 2 (after Group 1):
  - T-003 [BE]: Login API (depends on T-001)

Group 3 (after Group 2):
  - T-004 [FE]: Login form (depends on T-003)
```

2. **Launch Parallel Agents**
Use Task tool with multiple agent invocations for each parallel group.

3. **Wait for Group Completion** before starting next group.

## Guidelines

- **Always check git status first**: Detect uncommitted changes via script, not LLM
- **Respect branch context**: Different workflows for main vs feature branches
- **Never auto-commit**: User must manually commit to maintain control
- **Update task status**: Always update status as work progresses
- **Mark criteria done**: Check off acceptance criteria as completed
- **Parallel when possible**: Launch independent tasks together
