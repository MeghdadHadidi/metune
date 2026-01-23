---
name: peachflow:implement
description: Execute implementation tasks from quarterly plan. Assigns tasks to frontend-developer, backend-developer, or devops-engineer based on tags. Supports parallel execution.
argument-hint: "[task_id|next|all]"
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, Task, AskUserQuestion
---

# /peachflow:implement - Implementation Phase

Execute implementation tasks from the quarterly plan with parallel agent support.

## Prerequisites

A quarterly plan must exist with tasks:
- `/docs/04-plan/quarters/qXX/tasks/` contains task files

Check current quarter:
```bash
${CLAUDE_PLUGIN_ROOT}/scripts/state-manager.sh get-quarter
```

## Arguments

- **No argument**: Show available tasks and prompt for selection
- **`T-NNN`**: Execute specific task
- **`next`**: Execute next available task (not blocked, not completed)
- **`all`**: Execute all remaining tasks (parallel where possible)

## Workflow

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
Show task status:
```
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
Pass task context to appropriate agent.

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

### 5. Parallel Execution

When `all` argument or multiple independent tasks:

1. **Identify Parallel Groups**
```
Group 1 (parallel):
  - T-001 [BE]: Registration API
  - T-002 [FE]: Registration form (parallel with T-001)
  - T-007 [DevOps]: Email service

Group 2 (after Group 1):
  - T-003 [BE]: Login API (depends on T-001)

Group 3 (after Group 2):
  - T-004 [FE]: Login form (depends on T-003)
```

2. **Launch Parallel Agents**
Use Task tool with multiple agent invocations for each parallel group.

3. **Wait for Group Completion**
Before starting next group.

## Agent Routing

| Tag | Agent | Model |
|-----|-------|-------|
| [FE] | frontend-developer | opus |
| [BE] | backend-developer | opus |
| [DevOps] | devops-engineer | sonnet |
| [Full] | frontend + backend | opus |

## Task Status Updates

Update status in task frontmatter:
- `pending` → Task not started
- `in_progress` → Agent working on it
- `completed` → All acceptance criteria met
- `deferred` → Postponed to later

## Output

After task completion, show:
```
Task T-001 completed

Acceptance Criteria:
  [x] POST /api/users endpoint created
  [x] Email validation implemented
  [x] Password hashing with bcrypt
  [x] Returns 201 on success

Updated:
  - docs/04-plan/quarters/q01/tasks/001.md (completed)
  - docs/04-plan/quarters/q01/stories.md (task checked)
  - docs/04-plan/quarters/q01/plan.md (task checked)

Next available tasks:
  [FE] T-002: Build registration form
  [BE] T-003: Implement login API
```

## Finding Tasks by Tag

To find all frontend tasks:
```bash
${CLAUDE_PLUGIN_ROOT}/scripts/checklist-manager.sh find-tagged \
  "docs/04-plan/quarters/q01/tasks" "FE"
```

## Guidelines

- **Check dependencies first**: Don't start blocked tasks
- **Update status**: Always update task status
- **Mark criteria done**: Check off acceptance criteria as completed
- **Parallel when possible**: Launch independent tasks together
- **Report blockers**: If task cannot complete, note why
