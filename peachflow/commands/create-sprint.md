---
name: peachflow:create-sprint
description: Find unlocked tasks in the current quarter, create a new sprint with up to 10 tasks, and set up a git worktree for implementation. Starts the sprint workflow.
allowed-tools: Read, Write, Bash, Glob, AskUserQuestion
---

# /peachflow:create-sprint - Create Sprint from Ready Tasks

Finds tasks that are ready to work on (no blocking dependencies), creates a sprint with up to 10 tasks, and sets up a git worktree for isolated implementation.

## Pre-flight Check

```bash
# Check initialization
if [ ! -f ".peachflow-state.json" ] || [ ! -f ".peachflow-graph.json" ]; then
  echo "NOT_INITIALIZED"
  exit 1
fi

# Check if planning is done
plan_status=$(python3 -c "import json; print(json.load(open('.peachflow-state.json'))['phases']['plan']['status'])")
if [ "$plan_status" != "completed" ]; then
  echo "PLAN_NOT_COMPLETE"
  exit 1
fi

# Check for existing active sprint
active_sprint=$(${CLAUDE_PLUGIN_ROOT}/scripts/peachflow-graph.py sprint-active --format json)
if [ "$active_sprint" != "null" ]; then
  echo "ACTIVE_SPRINT_EXISTS"
  # Show the active sprint info
  ${CLAUDE_PLUGIN_ROOT}/scripts/peachflow-graph.py sprint-active
fi
```

**If NOT initialized:**
```
Peachflow not initialized. Run /peachflow:init first.
```

**If plan not completed:**
```
Planning phase not complete. Run /peachflow:plan first.
```

**If active sprint exists:**
```
An active sprint already exists: S-00X

Sprint: [name]
Tasks: X remaining, Y completed

Options:
1. Complete current sprint first: /peachflow:implement
2. Force-complete sprint: (ask user if they want to do this)
```

---

## Step 1: Find Current Quarter

Determine which quarter to pull tasks from:

```bash
# Get current quarter from state or find the first active one
current_quarter=$(python3 -c "
import json
state = json.load(open('.peachflow-state.json'))
print(state.get('currentQuarter', 'Q1'))
")

# Verify quarter has epics
epic_count=$(${CLAUDE_PLUGIN_ROOT}/scripts/peachflow-graph.py list epics --quarter $current_quarter --format json | python3 -c "import json,sys; print(len(json.load(sys.stdin)))")

if [ "$epic_count" -eq "0" ]; then
  # Try next quarter
  for q in Q1 Q2 Q3 Q4; do
    epic_count=$(${CLAUDE_PLUGIN_ROOT}/scripts/peachflow-graph.py list epics --quarter $q --format json | python3 -c "import json,sys; print(len(json.load(sys.stdin)))")
    if [ "$epic_count" -gt "0" ]; then
      current_quarter=$q
      break
    fi
  done
fi

echo "Using quarter: $current_quarter"
```

---

## Step 2: Find Ready Tasks

Get tasks with no blocking dependencies, prioritized by epic priority:

```bash
# Get ready tasks (pending + no blockers + not assigned to a sprint)
ready_tasks=$(${CLAUDE_PLUGIN_ROOT}/scripts/peachflow-graph.py ready-tasks --quarter $current_quarter --limit 10 --format json)

task_count=$(echo "$ready_tasks" | python3 -c "import json,sys; print(len(json.load(sys.stdin)))")
```

**If no ready tasks:**
```bash
# Check if all tasks are done
all_tasks=$(${CLAUDE_PLUGIN_ROOT}/scripts/peachflow-graph.py list tasks --quarter $current_quarter --format json)
completed=$(echo "$all_tasks" | python3 -c "import json,sys; tasks=json.load(sys.stdin); print(sum(1 for t in tasks if t['status']=='completed'))")
total=$(echo "$all_tasks" | python3 -c "import json,sys; print(len(json.load(sys.stdin)))")

if [ "$completed" -eq "$total" ]; then
  echo "QUARTER_COMPLETE"
else
  echo "ALL_TASKS_BLOCKED"
fi
```

**If quarter complete:**
```
All tasks in $quarter are complete!

Progress: $completed/$total tasks done

Options:
1. Move to next quarter (if available)
2. Create new epics in this quarter
```

**If all tasks blocked:**
```
No ready tasks found. All remaining tasks have unresolved dependencies.

Blocked tasks:
[List top 5 blocked tasks with their blockers]

You may need to:
1. Complete blocking tasks first
2. Remove dependencies that are no longer needed
```

---

## Step 3: Generate Sprint Name

Analyze the ready tasks to create a descriptive sprint name:

```bash
# Get the epic IDs for the ready tasks
task_details=$(echo "$ready_tasks" | python3 -c "
import json, sys
tasks = json.load(sys.stdin)
# Get unique words from task titles for naming
words = []
for t in tasks:
    words.extend(t['title'].split()[:2])
# Generate a 2-3 word name from common themes
print(' '.join(set(words)[:3]).lower().replace(' ', '-'))
")
```

Generate a name using the dominant epic or task themes. Examples:
- `auth-foundation` (if tasks are about authentication)
- `dashboard-core` (if tasks are dashboard-related)
- `api-endpoints` (if tasks are backend API work)

---

## Step 4: Create Sprint in Graph

```bash
# Get task IDs
task_ids=$(echo "$ready_tasks" | python3 -c "
import json, sys
tasks = json.load(sys.stdin)
print(','.join(t['id'] for t in tasks))
")

# Create sprint
sprint_result=$(${CLAUDE_PLUGIN_ROOT}/scripts/peachflow-graph.py create sprint \
  --quarter $current_quarter \
  --tasks "$task_ids" \
  --name "$sprint_name" \
  --format json)

sprint_id=$(echo "$sprint_result" | python3 -c "import json,sys; print(json.load(sys.stdin)['id'])")
```

---

## Step 5: Update Sprint Status to Active

```bash
${CLAUDE_PLUGIN_ROOT}/scripts/peachflow-graph.py update sprint $sprint_id --status active
```

---

## Step 6: Update State File

```bash
python3 -c "
import json
from datetime import datetime, timezone

with open('.peachflow-state.json', 'r') as f:
    state = json.load(f)

state['currentSprint'] = '$sprint_id'
state['currentQuarter'] = '$current_quarter'
state['lastUpdated'] = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')

with open('.peachflow-state.json', 'w') as f:
    json.dump(state, f, indent=2)
"
```

---

## Step 7: Create Git Worktree

Generate worktree name and create it:

```bash
# Get project name
project_name=$(python3 -c "import json; print(json.load(open('.peachflow-state.json'))['projectName'].lower().replace(' ', '-'))")

# Create worktree name: project-quarter-sprint-theme
# Example: taskflow-q1-s001-auth
worktree_name="${project_name}-${current_quarter,,}-${sprint_id,,}-${sprint_name}"
worktree_path="../${worktree_name}"

# Create branch name
branch_name="sprint/${sprint_id,,}-${sprint_name}"

# Create worktree
git worktree add -b "$branch_name" "$worktree_path"

# Update sprint with worktree path
${CLAUDE_PLUGIN_ROOT}/scripts/peachflow-graph.py update sprint $sprint_id --worktree "$worktree_path"
```

---

## Step 8: Create Sprint Commit

```bash
# Stage and commit the state/graph changes
git add .peachflow-state.json .peachflow-graph.json
git commit -m "$(cat <<'EOF'
peachflow: Start sprint $sprint_id - $sprint_name

Quarter: $current_quarter
Tasks: $task_count
Branch: $branch_name
Worktree: $worktree_path

Co-Authored-By: Claude Opus 4.5 <noreply@anthropic.com>
EOF
)"
```

---

## Step 9: Output Summary

```
Sprint created successfully!

Sprint: $sprint_id - $sprint_name
Quarter: $current_quarter
Tasks: $task_count

Tasks in this sprint:
  [FE] T-001: Create login form component
  [BE] T-002: Implement login API endpoint
  [BE] T-003: Add JWT token generation
  [FE] T-004: Build dashboard layout
  ...

Worktree: $worktree_path
Branch: $branch_name

---

To start implementation:

  cd $worktree_path
  /peachflow:implement

The implement command will:
1. Plan implementation approach
2. Execute tasks in dependency order
3. Mark tasks complete as they're done
4. Add peachflow tracking comments to code
```

---

## Error Handling

### Git Worktree Errors

```bash
# If worktree already exists
if [ -d "$worktree_path" ]; then
  echo "Worktree already exists at $worktree_path"
  # Ask user: reuse, remove and recreate, or choose different name
fi

# If branch already exists
if git show-ref --verify --quiet "refs/heads/$branch_name"; then
  echo "Branch $branch_name already exists"
  # Ask user: use existing, create new name, or fail
fi
```

### No Ready Tasks

If no tasks are ready due to dependencies, show the dependency chain:

```bash
${CLAUDE_PLUGIN_ROOT}/scripts/peachflow-graph.py list tasks --quarter $current_quarter --status pending --format json | python3 -c "
import json, sys
tasks = json.load(sys.stdin)
for t in tasks[:5]:
    blockers = t.get('blockedBy', [])
    if blockers:
        print(f\"{t['id']}: {t['title']}\")
        print(f\"  Blocked by: {', '.join(blockers)}\")
"
```

---

## Sprint Workflow Overview

```
/peachflow:create-sprint
    │
    ▼
Find ready tasks (no blockers, pending)
    │
    ▼
Create sprint (max 10 tasks)
    │
    ▼
Create git worktree
    │
    ▼
Commit sprint start
    │
    ▼
User: cd to worktree
    │
    ▼
/peachflow:implement
    │
    ▼
Tasks completed → Sprint done
    │
    ▼
/peachflow:create-sprint (next iteration)
```
