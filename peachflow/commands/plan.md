---
name: peachflow:plan
description: Break down epics into user stories and tasks in the graph. Plans all quarters automatically. Creates implementable work items with dependencies.
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Grep, Glob, Task, AskUserQuestion, Bash
---

# /peachflow:plan - Planning Phase (v3)

Break down epics into user stories and tasks, storing everything in the graph. Planning is done for all quarters at once.

## Output Responsibility

**CRITICAL**: This command is responsible for unified output.

- Sub-agents return minimal responses
- Collect results and provide ONE final summary
- Only this command suggests next steps

## Pre-flight Check

```bash
# Check initialization
if [ ! -f ".peachflow-state.json" ] || [ ! -f ".peachflow-graph.json" ]; then
  echo "NOT_INITIALIZED"
  exit 1
fi

# Check discovery completed
discovery_status=$(python3 -c "import json; print(json.load(open('.peachflow-state.json'))['phases']['discovery']['status'])")
if [ "$discovery_status" != "completed" ]; then
  echo "DISCOVERY_NOT_COMPLETE"
fi

# Check if already planned
plan_status=$(python3 -c "import json; print(json.load(open('.peachflow-state.json'))['phases']['plan']['status'])")

# Get epic count
epic_count=$(${CLAUDE_PLUGIN_ROOT}/scripts/peachflow-graph.py list epics --format json | python3 -c "import json,sys; print(len(json.load(sys.stdin)))")
```

**If discovery not complete:**
```
Discovery phase not complete. Run /peachflow:discover first.
```

**If no epics:**
```
No epics found in graph. Run /peachflow:discover to create epics.
```

---

## Planning Modes

| Condition | Mode |
|-----------|------|
| Plan status = pending | **Full Planning** (all quarters) |
| Plan status = completed | **Incremental Planning** (new epics only) |

---

## Mode A: Full Planning

### Step 1: Initialize

```bash
python3 -c "
import json
from datetime import datetime, timezone

with open('.peachflow-state.json', 'r') as f:
    state = json.load(f)

state['phases']['plan']['status'] = 'in_progress'
state['lastUpdated'] = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')

with open('.peachflow-state.json', 'w') as f:
    json.dump(state, f, indent=2)
"
```

### Step 2: Load Context

```bash
# Get all epics ordered by quarter and priority
${CLAUDE_PLUGIN_ROOT}/scripts/peachflow-graph.py list epics --format json

# Read PRD for features
cat docs/02-product/PRD.md

# Get testing config
testing_strategy=$(python3 -c "import json; print(json.load(open('.peachflow-state.json')).get('testingStrategy', 'none'))")
testing_intensity=$(python3 -c "import json; print(json.load(open('.peachflow-state.json')).get('testingIntensity', 'none'))")
```

### Step 3: Product Manager - User Stories

**Invoke**: product-manager agent

For each epic, create user stories:

```
Project: $PROJECT_NAME
Graph tool: ${CLAUDE_PLUGIN_ROOT}/scripts/peachflow-graph.py
Epic: E-001 - User Authentication

Create user stories for this epic. Each story should:
- Have a clear title
- Brief description (1-2 sentences)
- 3-5 acceptance criteria

Use the graph tool:
${CLAUDE_PLUGIN_ROOT}/scripts/peachflow-graph.py create story \
  --epic E-001 \
  --title "User can register with email" \
  --description "New users can create an account using email and password" \
  --acceptance "Given valid email,When form submitted,Then account created"

Return: "Done: Created X stories for E-001"
```

### Step 4: Tech Lead - Task Breakdown

**Invoke**: tech-lead agent

For each user story, create tasks:

```
Project: $PROJECT_NAME
Graph tool: ${CLAUDE_PLUGIN_ROOT}/scripts/peachflow-graph.py
Story: US-001 - User can register with email
Acceptance criteria: [list]
Testing strategy: $testing_strategy / $testing_intensity

Create tasks to implement this story. Consider:
1. Testing strategy - include test tasks if not "none"
2. Task tags: [FE], [BE], [DevOps], [Full]
3. Dependencies between tasks

Use the graph tool:
${CLAUDE_PLUGIN_ROOT}/scripts/peachflow-graph.py create task \
  --story US-001 \
  --title "Create registration API endpoint" \
  --tag BE \
  --description "POST /api/users with email validation" \
  --depends-on ""

${CLAUDE_PLUGIN_ROOT}/scripts/peachflow-graph.py create task \
  --story US-001 \
  --title "Build registration form" \
  --tag FE \
  --description "React form with client-side validation" \
  --depends-on "T-001"

Return: "Done: Created X tasks for US-001 (Y FE, Z BE, W DevOps)"
```

### Step 5: Set Dependencies

After all tasks are created, identify cross-story dependencies:

```bash
# If T-010 (in US-003) depends on T-002 (in US-001)
${CLAUDE_PLUGIN_ROOT}/scripts/peachflow-graph.py depends add T-010 --on T-002
```

### Step 6: Update Epic/Story Status

Mark epics and stories as ready when fully planned:

```bash
# Update epic status
${CLAUDE_PLUGIN_ROOT}/scripts/peachflow-graph.py update epic E-001 --status ready

# Update story status
${CLAUDE_PLUGIN_ROOT}/scripts/peachflow-graph.py update story US-001 --status ready
```

### Step 7: Finalize

```bash
python3 -c "
import json
from datetime import datetime, timezone

with open('.peachflow-state.json', 'r') as f:
    state = json.load(f)

state['phases']['plan']['status'] = 'completed'
state['phases']['plan']['completedAt'] = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
state['currentQuarter'] = 'Q1'  # Set first quarter as current
state['lastUpdated'] = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')

with open('.peachflow-state.json', 'w') as f:
    json.dump(state, f, indent=2)
"
```

### Output Summary

```
Planning complete for $PROJECT_NAME!

Summary by Quarter:

Q1 (3 epics, 8 stories, 24 tasks):
  E-001: User Authentication [ready]
    - US-001: User can register (4 tasks)
    - US-002: User can login (3 tasks)
    - US-003: Password recovery (3 tasks)
  E-002: Dashboard [ready]
    - US-004: View activity feed (4 tasks)
    - US-005: Quick actions panel (3 tasks)
  E-003: User Profile [ready]
    - US-006: Edit profile info (4 tasks)
    - US-007: Change password (3 tasks)

Q2 (2 epics, 6 stories, 18 tasks):
  E-004: Notifications [ready]
    ...
  E-005: Settings [ready]
    ...

Total:
  - Epics: 5
  - User Stories: 14
  - Tasks: 42 (18 FE, 16 BE, 8 DevOps)

Dependency chains: 12 cross-task dependencies set

Next: /peachflow:create-sprint
```

---

## Mode B: Incremental Planning

When new epics have been added after initial planning.

### Detect New Epics

```bash
# Find epics with status "draft" (not yet planned)
${CLAUDE_PLUGIN_ROOT}/scripts/peachflow-graph.py list epics --status draft --format json
```

### Plan New Epics

Same process as full planning, but only for draft epics:
1. Product manager creates stories
2. Tech lead creates tasks
3. Dependencies set
4. Status updated to ready

---

## Graph Structure After Planning

```json
{
  "entities": {
    "quarters": {
      "Q1": { "id": "Q1", "status": "planned" }
    },
    "epics": {
      "E-001": {
        "id": "E-001",
        "title": "User Authentication",
        "quarter": "Q1",
        "priority": 1,
        "status": "ready"
      }
    },
    "stories": {
      "US-001": {
        "id": "US-001",
        "title": "User can register",
        "epicId": "E-001",
        "status": "ready",
        "acceptanceCriteria": ["..."]
      }
    },
    "tasks": {
      "T-001": {
        "id": "T-001",
        "title": "Create registration API",
        "storyId": "US-001",
        "tag": "BE",
        "status": "pending"
      },
      "T-002": {
        "id": "T-002",
        "title": "Build registration form",
        "storyId": "US-001",
        "tag": "FE",
        "status": "pending"
      }
    }
  },
  "relationships": {
    "quarter_epics": { "Q1": ["E-001"] },
    "epic_stories": { "E-001": ["US-001"] },
    "story_tasks": { "US-001": ["T-001", "T-002"] },
    "task_dependencies": { "T-002": ["T-001"] }
  }
}
```

---

## Testing Strategy Integration

Based on testing settings, tech-lead creates appropriate test tasks:

| Strategy | Tasks Created |
|----------|---------------|
| none | No test tasks |
| tdd | Test task BEFORE implementation task |
| bdd | Cucumber/Gherkin test task BEFORE |
| atdd | Acceptance test task BEFORE |
| test-last | Test task AFTER implementation task |

| Intensity | Test Scope |
|-----------|------------|
| essential | Unit tests only |
| smart | Unit + component + API mocks |
| intense | Smart + Playwright UI tests |

Example with TDD + Smart:
```
T-001: [BE] Write registration API tests (depends on: none)
T-002: [BE] Implement registration API (depends on: T-001)
T-003: [FE] Write registration form tests (depends on: none)
T-004: [FE] Build registration form (depends on: T-002, T-003)
T-005: [FE] Write integration tests (depends on: T-004)
```

---

## Visualize the Plan

After planning, users can see the full graph:

```bash
/peachflow:graph
```

Or export to markdown:

```bash
${CLAUDE_PLUGIN_ROOT}/scripts/peachflow-graph.py export --format markdown > plan-overview.md
```

---

## Clarifications During Planning

If tech-lead encounters ambiguity:

```bash
${CLAUDE_PLUGIN_ROOT}/scripts/peachflow-graph.py create clarification \
  --entity US-003 \
  --question "Should password recovery use email link or verification code?"
```

List pending clarifications:

```bash
${CLAUDE_PLUGIN_ROOT}/scripts/peachflow-graph.py list clarifications --pending
```

Run `/peachflow:clarify` to resolve them before implementation.

---

## Statistics Command

Show planning statistics:

```bash
${CLAUDE_PLUGIN_ROOT}/scripts/peachflow-graph.py stats
```

Output:
```
Project Statistics
────────────────────────────────────────
Progress: ░░░░░░░░░░░░░░░░░░░░ 0.0%

Epics:      5 total
            5 ready

Stories:   14 total
           14 ready

Tasks:     42 total
            0 completed
           42 pending
            8 blocked (by dependencies)

  By tag:
           18 [FE]
           16 [BE]
            8 [DevOps]

Clarifications: 0 pending / 0 total
```
