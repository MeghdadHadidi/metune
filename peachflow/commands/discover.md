---
name: peachflow:discover
description: Start product discovery for new projects OR add new features/initiatives to existing projects. Creates BRD/PRD and populates epics in the graph.
argument-hint: "[product idea OR feature description]"
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Grep, Glob, WebSearch, WebFetch, Task, AskUserQuestion, Bash
---

# /peachflow:discover - Discovery Phase (v3)

Run product discovery for new projects OR add new features to existing projects. Creates BRD, PRD, and initial epics in the graph.

## Output Responsibility

**CRITICAL**: This command is responsible for the unified output to the user.

- Sub-agents return minimal responses (just confirmation of what was done)
- DO NOT let agent responses bubble up to the user
- Collect results from all agents, then provide ONE final summary at the end
- Only this command suggests next steps, not the agents

## Pre-flight Check

```bash
# Check if peachflow is initialized
if [ ! -f ".peachflow-state.json" ] || [ ! -f ".peachflow-graph.json" ]; then
  echo "NOT_INITIALIZED"
  exit 1
fi

# Get version and check v3
version=$(python3 -c "import json; print(json.load(open('.peachflow-state.json')).get('version', '2.0.0'))")
if [[ ! "$version" == 3.* ]]; then
  echo "VERSION_MISMATCH: Expected v3, got $version"
fi

# Check discovery status
discovery_status=$(python3 -c "import json; print(json.load(open('.peachflow-state.json'))['phases']['discovery']['status'])")
```

**If NOT initialized:**
```
Peachflow is not initialized for this project.

Run /peachflow:init first to set up the project.
```

## Get Project Name

```bash
PROJECT_NAME=$(python3 -c "import json; print(json.load(open('.peachflow-state.json'))['projectName'])")
echo "Discovering for: $PROJECT_NAME"
```

**All agents must use `$PROJECT_NAME` when referring to the product being built.**

## Mode Detection

| Condition | Mode |
|-----------|------|
| Discovery status = "pending" | **Full Discovery** (new project) |
| Discovery status = "completed" | **Feature Discovery** (add to existing) |

---

## Mode A: Full Discovery (New Project)

When discovery has never been run.

### Workflow

#### Phase 0: Initialize

```bash
# Update state
python3 -c "
import json
from datetime import datetime, timezone

with open('.peachflow-state.json', 'r') as f:
    state = json.load(f)

state['phases']['discovery']['status'] = 'in_progress'
state['lastUpdated'] = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')

with open('.peachflow-state.json', 'w') as f:
    json.dump(state, f, indent=2)
"

# Create doc directories
mkdir -p docs/01-business docs/02-product docs/02-product/architecture/adr
```

#### Phase 1: Business Analysis
**Invoke**: business-analyst agent

Provide context:
- User's product idea (from arguments)
- Project name from state

The agent creates `/docs/01-business/BRD.md` with:
- Problem statement
- Business objectives
- Stakeholders
- Constraints
- BR-XXX requirements

#### Phase 2: Product Manager
**Invoke**: product-manager agent

Provide context:
- The BRD just created
- User's original product idea

The agent creates `/docs/02-product/PRD.md` with:
- Product vision
- Target users
- Features (F-XXX)
- Success metrics

**Additionally**, the product manager populates initial epics in the graph:

```bash
# For each major feature, create an epic
${CLAUDE_PLUGIN_ROOT}/scripts/peachflow-graph.py create epic \
  --title "User Authentication" \
  --quarter Q1 \
  --priority 1 \
  --description "Complete user authentication system including login, signup, and password recovery" \
  --deliverables "Login,Signup,Password Reset,Session Management"
```

#### Phase 3: Check for Clarifications

After discovery, scan for items needing clarification:

```bash
# Check if any clarifications were created during discovery
pending_cl=$(${CLAUDE_PLUGIN_ROOT}/scripts/peachflow-graph.py list clarifications --pending --format json | python3 -c "import json,sys; print(len(json.load(sys.stdin)))")

if [ "$pending_cl" -gt "0" ]; then
  echo "CLARIFICATIONS_NEEDED: $pending_cl"
fi
```

If clarifications needed, output them to user and ask for answers.

#### Phase 4: Finalize

```bash
# Update state
python3 -c "
import json
from datetime import datetime, timezone

with open('.peachflow-state.json', 'r') as f:
    state = json.load(f)

state['phases']['discovery']['status'] = 'completed'
state['phases']['discovery']['completedAt'] = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
state['lastUpdated'] = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')

with open('.peachflow-state.json', 'w') as f:
    json.dump(state, f, indent=2)
"
```

#### Output Summary

```
Discovery complete for $PROJECT_NAME!

Documents created:
  - docs/01-business/BRD.md (X business requirements)
  - docs/02-product/PRD.md (Y features)

Epics created in graph:
  - E-001: User Authentication (Q1, Priority 1)
  - E-002: Dashboard & Analytics (Q1, Priority 2)
  - E-003: Notification System (Q2, Priority 3)

[If clarifications pending:]
Clarifications needed: Z items
Run /peachflow:clarify to resolve them.

Next: /peachflow:design
```

---

## Mode B: Feature Discovery (Add to Existing)

When discovery is already complete - adding new features.

### Workflow

#### Phase 1: Understand New Feature

Parse the user's input to understand:
- What feature/initiative they want to add
- Rough scope and priority

#### Phase 2: Update Documents
**Invoke**: product-manager agent

The agent:
- Adds new features to PRD (new F-XXX entries)
- Updates BRD if there are new business requirements
- Creates new epic(s) in the graph

```bash
# Create new epic for the feature
${CLAUDE_PLUGIN_ROOT}/scripts/peachflow-graph.py create epic \
  --title "New Feature Name" \
  --quarter Q2 \
  --priority 4 \
  --description "Description of the new feature..." \
  --deliverables "Deliverable1,Deliverable2"
```

#### Phase 3: Link to Existing

If the new feature relates to existing epics:

```bash
# Create clarification if relationship unclear
${CLAUDE_PLUGIN_ROOT}/scripts/peachflow-graph.py create clarification \
  --entity E-004 \
  --question "Does this new authentication feature replace E-001 or extend it?"
```

#### Output Summary

```
Feature added to $PROJECT_NAME!

Updated:
  - docs/02-product/PRD.md (+2 features)

New epics:
  - E-004: Social Login Integration (Q2, Priority 4)

Related to:
  - E-001: User Authentication (may need coordination)

Next: /peachflow:design (to update design for new features)
```

---

## Agent Instructions

### For business-analyst

Context to provide:
```
Project: $PROJECT_NAME
Product idea: [user's input]
Existing documents: [none for new, or paths for feature add]

Create BRD with business requirements (BR-XXX).
Return only: "Done: docs/01-business/BRD.md - X business requirements"
```

### For product-manager

Context to provide:
```
Project: $PROJECT_NAME
BRD: [path or content]
Product idea: [user's input]
Graph tool: ${CLAUDE_PLUGIN_ROOT}/scripts/peachflow-graph.py

Tasks:
1. Create PRD with features (F-XXX)
2. Create epics in graph for major features
3. Assign epics to quarters based on priority

Return only: "Done: docs/02-product/PRD.md - Y features, Z epics created"
```

---

## Clarification Handling

During discovery, if agents encounter ambiguity:

```bash
# Create clarification in graph
${CLAUDE_PLUGIN_ROOT}/scripts/peachflow-graph.py create clarification \
  --entity "general" \
  --question "Should the authentication system support SSO providers?"
```

At the end of discovery, list pending clarifications:

```bash
${CLAUDE_PLUGIN_ROOT}/scripts/peachflow-graph.py list clarifications --pending
```

If any exist, prompt user to answer them or run `/peachflow:clarify`.

---

## Graph Integration

Discovery is the first phase to populate the graph with epics.

**What gets created:**
- Epics (E-XXX) for major features
- Clarifications (CL-XXX) for open questions

**What does NOT get created yet:**
- User stories (created during planning)
- Tasks (created during planning)
- ADRs (created during design)

**Epic assignment:**
- Critical/foundational → Q1
- Important but not blocking → Q2
- Nice to have → Q3/Q4
- Lower priority determined by product-manager
