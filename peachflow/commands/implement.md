---
name: peachflow:implement
description: Execute implementation of the current sprint's tasks. Works within a sprint worktree, plans approach, implements tasks in order, and tracks progress in the graph. Uses plan mode for each task.
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Grep, Glob, Task, Bash, EnterPlanMode, ExitPlanMode, TaskCreate, TaskUpdate, TaskList
---

# /peachflow:implement - Sprint Task Implementation

Execute implementation of tasks in the current sprint. This command operates within a sprint worktree and implements tasks systematically.

## Output Responsibility

**CRITICAL**: This command is responsible for unified output to the user.

- Sub-agents return minimal responses (just confirmation of what was done)
- DO NOT let agent responses bubble up to the user
- Collect results from all agents, then provide summaries at checkpoints
- Only this command suggests next steps

## Pre-flight Check

```bash
# Check if we're in a worktree (not main working tree)
if ! git rev-parse --is-inside-work-tree > /dev/null 2>&1; then
  echo "NOT_IN_GIT_REPO"
  exit 1
fi

# Check if this is a worktree
worktree_root=$(git rev-parse --show-toplevel)
main_worktree=$(git worktree list | head -1 | awk '{print $1}')

if [ "$worktree_root" = "$main_worktree" ]; then
  echo "NOT_IN_WORKTREE"
  exit 1
fi

# Find the graph file (in main worktree)
graph_path="${main_worktree}/.peachflow-graph.json"
state_path="${main_worktree}/.peachflow-state.json"

if [ ! -f "$graph_path" ]; then
  echo "GRAPH_NOT_FOUND"
  exit 1
fi

# Get active sprint
current_sprint=$(python3 -c "import json; print(json.load(open('$state_path')).get('currentSprint', ''))")

if [ -z "$current_sprint" ]; then
  echo "NO_ACTIVE_SPRINT"
  exit 1
fi

echo "READY sprint=$current_sprint"
```

**If NOT in git repo:**
```
Not in a git repository. Navigate to a project directory first.
```

**If NOT in worktree:**
```
This command must be run from a sprint worktree.

To start a sprint:
  /peachflow:create-sprint

Then switch to the worktree it creates.
```

**If no active sprint:**
```
No active sprint found.

Run /peachflow:create-sprint first to create a sprint.
```

---

## Step 1: Load Sprint Context

```bash
# Set graph path for peachflow-graph.py
export PEACHFLOW_GRAPH_PATH="$graph_path"

# Get sprint details
sprint_info=$(${CLAUDE_PLUGIN_ROOT}/scripts/peachflow-graph.py get sprint $current_sprint --format json)

# Get tasks in this sprint
sprint_tasks=$(echo "$sprint_info" | python3 -c "
import json, sys
sprint = json.load(sys.stdin)
print(','.join(sprint['taskIds']))
")

# Get full task details
for task_id in $(echo $sprint_tasks | tr ',' ' '); do
  ${CLAUDE_PLUGIN_ROOT}/scripts/peachflow-graph.py get task $task_id --format json
done
```

Parse the sprint and show status:

```
Sprint: S-001 - auth-foundation
Quarter: Q1

Tasks: 6 total
  - 2 completed
  - 1 in progress
  - 3 pending

Ready to work on:
  [BE] T-003: Implement password hashing
  [FE] T-005: Build login form
  [DevOps] T-006: Configure session storage
```

---

## Step 2: Get Ready Tasks

Find tasks that can be worked on (pending, no blockers within sprint):

```bash
# Get ready tasks from this sprint
ready_tasks=$(python3 -c "
import json, sys, os

graph_path = os.environ['PEACHFLOW_GRAPH_PATH']
with open(graph_path) as f:
    graph = json.load(f)

sprint_id = '$current_sprint'
sprint = graph['entities']['sprints'].get(sprint_id, {})
task_ids = sprint.get('taskIds', [])

ready = []
for tid in task_ids:
    task = graph['entities']['tasks'].get(tid, {})
    if task.get('status') != 'pending':
        continue
    # Check dependencies
    deps = graph['relationships']['task_dependencies'].get(tid, [])
    blocked = False
    for dep in deps:
        dep_task = graph['entities']['tasks'].get(dep, {})
        if dep_task.get('status') not in ['completed', 'skipped']:
            blocked = True
            break
    if not blocked:
        ready.append(task)

print(json.dumps(ready))
")
```

**If no ready tasks:**
Check if sprint is complete or all tasks are blocked.

---

## Step 3: Enter Plan Mode for Implementation

For each batch of parallel tasks, enter plan mode to design the implementation approach.

**Use EnterPlanMode** to plan the implementation:

```
I will now plan the implementation approach for these tasks:

[FE] T-003: Build login form component
[BE] T-004: Create authentication API
[DevOps] T-005: Set up JWT configuration

This will involve:
1. Reading relevant design skills for guidance
2. Understanding the codebase structure
3. Identifying files to create/modify
4. Planning the implementation order
```

### In Plan Mode

1. **Load Design Skills** (if any exist):
   ```bash
   ls .claude/skills/
   # If design-system.md exists, load it
   ```

2. **Analyze Task Requirements**:
   - Read the task chain to understand context
   ```bash
   export PEACHFLOW_GRAPH_PATH="$graph_path"
   ${CLAUDE_PLUGIN_ROOT}/scripts/peachflow-graph.py chain T-003
   ```
   - Understand acceptance criteria from user story
   - Identify technical requirements

3. **Explore Codebase** (use Explore agent if needed):
   - Find relevant existing files
   - Understand patterns in use
   - Identify integration points

4. **Write Plan**:
   - List files to create/modify
   - Outline implementation steps
   - Note any risks or clarifications needed

5. **Exit Plan Mode** when plan is ready for approval.

---

## Step 4: Execute Implementation

After plan approval, implement tasks systematically.

### Create TodoWrite Tasks

For each task in the sprint batch:

```json
{
  "tasks": [
    {
      "subject": "[BE] T-003: Implement password hashing",
      "description": "Add bcrypt hashing to user registration...",
      "activeForm": "Implementing password hashing"
    },
    {
      "subject": "[FE] T-005: Build login form",
      "description": "Create React login form component...",
      "activeForm": "Building login form"
    }
  ]
}
```

### Route to Appropriate Agents

Based on task tag, invoke the correct agent:

| Tag | Agent |
|-----|-------|
| `[FE]` | frontend-developer |
| `[BE]` | backend-developer |
| `[DevOps]` | devops-engineer |
| `[Full]` | frontend-developer, then backend-developer |

**Agent Invocation Pattern:**

```
Invoke: backend-developer agent

Context:
- Task: T-003 - Implement password hashing
- Epic: E-001 - User Authentication (Q1)
- Story: US-001 - User can create account
- Acceptance: Password stored securely with bcrypt

Design skills loaded: (if applicable)
- design-system: Using color tokens for form styling
- accessibility: ARIA labels for form fields

Implementation plan:
[The plan from plan mode]

Instructions:
1. Implement according to plan
2. Add tracking comment to code
3. Return: "Done: [files changed] - [summary]"
```

### Code Tracking Comments

Agents must add a single-line tracking comment to created/modified files:

```javascript
// peachflow: T-003 | E-001 | Q1
```

```python
# peachflow: T-003 | E-001 | Q1
```

```html
<!-- peachflow: T-003 | E-001 | Q1 -->
```

This enables tracing code back to requirements.

---

## Step 5: Mark Tasks Complete

After each task is implemented:

```bash
export PEACHFLOW_GRAPH_PATH="$graph_path"
${CLAUDE_PLUGIN_ROOT}/scripts/peachflow-graph.py update task T-003 --status completed
```

---

## Step 6: Progress Checkpoint

After every 2 rounds of parallel execution (or max 4 tasks), show checkpoint:

```
Progress Checkpoint
───────────────────────────────────────

Sprint: S-001 - auth-foundation
Completed this session: 4 tasks
  ✓ [BE] T-003: Implement password hashing
  ✓ [FE] T-005: Build login form
  ✓ [DevOps] T-006: Configure session storage
  ✓ [BE] T-004: Create authentication API

Remaining: 2 tasks
  ○ [FE] T-007: Add form validation
  ○ [BE] T-008: Implement logout endpoint

Continue? (y/n)
```

---

## Step 7: Sprint Completion

When all tasks in the sprint are complete:

```bash
export PEACHFLOW_GRAPH_PATH="$graph_path"

# Mark sprint complete
${CLAUDE_PLUGIN_ROOT}/scripts/peachflow-graph.py update sprint $current_sprint --status completed

# Update state
python3 -c "
import json
from datetime import datetime, timezone

with open('$state_path', 'r') as f:
    state = json.load(f)

state['currentSprint'] = None
state['lastUpdated'] = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')

with open('$state_path', 'w') as f:
    json.dump(state, f, indent=2)
"

# Commit sprint completion
git add -A
git commit -m "$(cat <<'EOF'
peachflow: Complete sprint $current_sprint

Implemented tasks:
- T-003: Implement password hashing
- T-004: Create authentication API
- T-005: Build login form
- T-006: Configure session storage

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
EOF
)"
```

**Output:**
```
Sprint S-001 - auth-foundation complete!

Summary:
  ✓ 6 tasks implemented
  ✓ 8 files created
  ✓ 4 files modified
  ✓ All changes committed

Next steps:
  1. Return to main branch: cd .. && cd [main-worktree]
  2. Merge sprint: git merge sprint/s-001-auth-foundation
  3. Start next sprint: /peachflow:create-sprint

Or stay in worktree to review/test before merging.
```

---

## Parallel Execution Model

Get max parallel from state:

```bash
max_parallel=$(python3 -c "import json; print(json.load(open('$state_path')).get('maxParallelTasks', 3))")
```

### Parallel Task Groups

Group ready tasks by compatibility:
- Same type (all FE, or all BE) can run in parallel
- Different types (FE + BE) can run in parallel if no file conflicts
- `[Full]` tasks run sequentially

### Execution Order

1. Find all ready tasks
2. Group into parallel batches (max `maxParallelTasks`)
3. Execute batch via agents
4. Mark completed
5. Find newly unblocked tasks
6. Repeat until sprint complete

---

## Error Handling

### Task Failure

If an agent cannot complete a task:

```
Task T-003 could not be completed.

Reason: [error description]

Options:
1. Retry with different approach
2. Skip task (mark as blocked)
3. Add clarification request
4. Stop implementation
```

If skipped:
```bash
${CLAUDE_PLUGIN_ROOT}/scripts/peachflow-graph.py update task T-003 --status blocked
```

### Missing Dependencies

If a task depends on something not in the sprint:

```bash
${CLAUDE_PLUGIN_ROOT}/scripts/peachflow-graph.py depends blockers T-003
```

Show blockers and offer to pull them into current sprint or defer.

---

## Design Skills Integration

Before implementing FE tasks, check for design skills:

```bash
if [ -f ".claude/skills/design-system.md" ]; then
  echo "Loading design-system skill"
  # Pass to frontend-developer agent
fi

if [ -f ".claude/skills/component-patterns.md" ]; then
  echo "Loading component-patterns skill"
fi
```

Pass loaded skills to implementation agents so they follow design guidelines.
