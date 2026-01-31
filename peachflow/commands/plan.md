---
name: peachflow:plan
description: Break down epics into user stories and tasks using Claude's native plan mode. Explores context, writes plan for approval, then creates work items.
allowed-tools: Read, Write, Edit, Grep, Glob, Bash, EnterPlanMode, ExitPlanMode, AskUserQuestion
argument-hint: [--incremental]
---

# /peachflow:plan - Planning Phase (v3)

Break down epics into user stories and tasks, storing everything in the graph. Uses Claude's native plan mode for efficient planning.

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

# Get plan status
plan_status=$(python3 -c "import json; print(json.load(open('.peachflow-state.json'))['phases']['plan']['status'])")

# Get project info
PROJECT_NAME=$(python3 -c "import json; print(json.load(open('.peachflow-state.json'))['projectName'])")

# Get epic count
epic_count=$(${CLAUDE_PLUGIN_ROOT}/scripts/peachflow-graph.py list epics --format json 2>/dev/null | python3 -c "import json,sys; print(len(json.load(sys.stdin)))" 2>/dev/null || echo "0")

# Get testing config
testing_strategy=$(python3 -c "import json; print(json.load(open('.peachflow-state.json')).get('testingStrategy', 'none'))")
testing_intensity=$(python3 -c "import json; print(json.load(open('.peachflow-state.json')).get('testingIntensity', 'none'))")
```

**If NOT_INITIALIZED:**
```
Project not initialized. Run /peachflow:init first.
```

**If DISCOVERY_NOT_COMPLETE:**
```
Discovery phase not complete. Run /peachflow:discover first.
```

**If no epics (epic_count = 0):**
```
No epics found in graph. Run /peachflow:discover to create epics.
```

---

## Workflow

### Step 1: Enter Plan Mode

Use **EnterPlanMode** tool immediately. Planning happens in plan mode where you:

1. Explore the project context
2. Design user stories and tasks
3. Write the plan for user approval
4. Exit plan mode when ready

### Step 2: In Plan Mode - Gather Context

Read the essential context:

```bash
# Get all epics
${CLAUDE_PLUGIN_ROOT}/scripts/peachflow-graph.py list epics --format json

# Read PRD for features
cat docs/02-product/PRD.md
```

### Step 3: In Plan Mode - Write Plan

Write your plan to: `.peachflow-plan.md`

**Plan Structure:**

```markdown
# Planning: $PROJECT_NAME

## Epics to Plan

### E-001: [Epic Title]
Quarter: Q1 | Priority: 1

#### User Stories

1. **US-001: [User can...]**
   - Description: [1-2 sentences]
   - Acceptance: Given X, When Y, Then Z

   Tasks:
   - T-001 [BE]: [Task title] - [brief description]
   - T-002 [FE]: [Task title] - [brief description] (depends: T-001)
   - T-003 [BE]: [Test task if TDD] (depends: none)

2. **US-002: [User can...]**
   [...]

### E-002: [Epic Title]
[...]

## Summary

- Epics: X
- User Stories: Y
- Tasks: Z (A FE, B BE, C DevOps)
- Test tasks: N (based on $testing_strategy)

## Dependencies

Cross-story dependencies:
- T-010 depends on T-002 (auth needed before protected routes)
```

**Guidelines:**
- Keep task descriptions brief (1 line)
- Use task tags: [FE], [BE], [DevOps], [Full]
- Include test tasks based on testing strategy ($testing_strategy, $testing_intensity)
- Set dependencies where one task requires another

### Step 4: Exit Plan Mode

Use **ExitPlanMode** tool when plan is complete. User will review and approve.

---

## After Plan Approval

Once the user approves, execute the plan:

### Step 5: Mark Planning Started

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

### Step 6: Create All Work Items

Read your plan from `.peachflow-plan.md` and create all work items using the graph tool:

**For each user story:**
```bash
${CLAUDE_PLUGIN_ROOT}/scripts/peachflow-graph.py create story \
  --epic E-001 \
  --title "User can register with email" \
  --description "New users register using email and password" \
  --acceptance "Given valid email,When form submitted,Then account created"
```

**For each task:**
```bash
${CLAUDE_PLUGIN_ROOT}/scripts/peachflow-graph.py create task \
  --story US-001 \
  --title "Create registration API endpoint" \
  --tag BE \
  --description "POST /api/users with email validation" \
  --depends-on ""
```

**For dependencies:**
```bash
${CLAUDE_PLUGIN_ROOT}/scripts/peachflow-graph.py depends add T-002 --on T-001
```

### Step 7: Update Status

Mark epics and stories as ready:

```bash
${CLAUDE_PLUGIN_ROOT}/scripts/peachflow-graph.py update epic E-001 --status ready
${CLAUDE_PLUGIN_ROOT}/scripts/peachflow-graph.py update story US-001 --status ready
```

### Step 8: Finalize

```bash
python3 -c "
import json
from datetime import datetime, timezone

with open('.peachflow-state.json', 'r') as f:
    state = json.load(f)

state['phases']['plan']['status'] = 'completed'
state['phases']['plan']['completedAt'] = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
state['currentQuarter'] = 'Q1'
state['lastUpdated'] = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')

with open('.peachflow-state.json', 'w') as f:
    json.dump(state, f, indent=2)
"

# Clean up plan file
rm -f .peachflow-plan.md
```

### Output

```
Planning complete for $PROJECT_NAME!

Created:
  - X user stories
  - Y tasks (A FE, B BE, C DevOps)
  - Z dependencies

Next: /peachflow:create-sprint
```

---

## Incremental Mode

If `--incremental` argument or plan status is already "completed":

1. Find draft epics only:
   ```bash
   ${CLAUDE_PLUGIN_ROOT}/scripts/peachflow-graph.py list epics --status draft --format json
   ```

2. Plan only for those epics
3. Same workflow: enter plan mode, write plan, get approval, create items

---

## Testing Strategy Reference

Include test tasks based on project settings:

| Strategy | Test Task Position |
|----------|-------------------|
| none | No test tasks |
| tdd | Test task BEFORE implementation |
| bdd | BDD test task BEFORE |
| atdd | Acceptance test task BEFORE |
| test-last | Test task AFTER implementation |

| Intensity | Scope |
|-----------|-------|
| essential | Unit tests only |
| smart | Unit + component + API mocks |
| intense | Smart + Playwright UI |

---

## Task Tags Reference

| Tag | Use For | Implemented By |
|-----|---------|----------------|
| `FE` | Frontend/UI | frontend-developer |
| `BE` | Backend/API | backend-developer |
| `DevOps` | Infrastructure | devops-engineer |
| `Full` | Both FE+BE | Both agents |

---

## Clarifications

If you encounter ambiguity while planning, add clarification:

```bash
${CLAUDE_PLUGIN_ROOT}/scripts/peachflow-graph.py create clarification \
  --entity US-003 \
  --question "Should password recovery use email link or verification code?"
```

After planning, run `/peachflow:clarify` to resolve them.
