---
name: peachflow:init
description: Initialize peachflow for a project. Creates the state file and docs structure. Can also reconfigure an existing project.
allowed-tools: Read, Write, Bash, Glob, AskUserQuestion
aliases: [peachflow:config]
---

# /peachflow:init - Initialize or Configure Peachflow

Set up peachflow for a new project or reconfigure an existing one. This command must be run before any other peachflow commands.

## Pre-flight Check

First, check if peachflow is already initialized:

```bash
if [ -f ".peachflow-state.json" ]; then
  echo "ALREADY_INITIALIZED"
fi
```

**If already initialized (or called as /peachflow:config):**
Go to **Configuration Mode** below.

**If not initialized:**
Go to **Initialization Mode** below.

---

## Initialization Mode (New Project)

### Step 1: Get Project Information

Ask the user for project details:

```json
{
  "questions": [
    {
      "question": "What is the name of your project?",
      "header": "Project Name",
      "options": [
        {"label": "Enter name", "description": "You'll type the project name (e.g., 'TaskFlow', 'ShopEase')"}
      ],
      "multiSelect": false
    },
    {
      "question": "What type of project is this?",
      "header": "Project Type",
      "options": [
        {"label": "New project (Recommended)", "description": "Starting from scratch, no existing code"},
        {"label": "Existing codebase", "description": "Adding peachflow to a project already in development"},
        {"label": "Continuing previous work", "description": "Resuming a peachflow project from backup/export"}
      ],
      "multiSelect": false
    },
    {
      "question": "How many tasks should run in parallel during implementation?",
      "header": "Parallelism",
      "options": [
        {"label": "3 (Recommended)", "description": "Balanced - good for most projects"},
        {"label": "1", "description": "Sequential - one task at a time"},
        {"label": "2", "description": "Light parallel - two concurrent tasks"},
        {"label": "4", "description": "More parallel - four concurrent tasks"},
        {"label": "6", "description": "Maximum - six concurrent tasks"}
      ],
      "multiSelect": false
    }
  ]
}
```

### Step 2: Get Testing Configuration

```json
{
  "questions": [
    {
      "question": "What testing strategy should we use?",
      "header": "Testing",
      "options": [
        {"label": "No Tests (Recommended for MVPs)", "description": "Skip automated testing, focus on speed"},
        {"label": "TDD - Test Driven Development", "description": "Write tests first, then implementation"},
        {"label": "BDD - Behavior Driven Development", "description": "Given/When/Then style tests from user stories"},
        {"label": "ATDD - Acceptance Test Driven", "description": "Tests from acceptance criteria first"},
        {"label": "Test-last", "description": "Write tests after implementation"}
      ],
      "multiSelect": false
    },
    {
      "question": "What level of test coverage?",
      "header": "Intensity",
      "options": [
        {"label": "Essential (Recommended)", "description": "Unit tests only - fast, focused"},
        {"label": "Smart", "description": "Unit + component + mocked API testing"},
        {"label": "Intense", "description": "Everything + automated UI testing (Playwright)"}
      ],
      "multiSelect": false
    }
  ]
}
```

**Skip testing questions if user selected "No Tests"** - set intensity to "none" automatically.

### Step 3: Create State File

```bash
# Parse testing strategy: "TDD - Test Driven Development" → "tdd"
# Parse testing intensity: "Smart" → "smart"
# Parse parallelism: "3 (Recommended)" → 3

${CLAUDE_PLUGIN_ROOT}/scripts/state-manager.sh init "ProjectName" "new" "3"
${CLAUDE_PLUGIN_ROOT}/scripts/state-manager.sh set-testing "tdd" "smart"
```

This creates `.peachflow-state.json`:

```json
{
  "version": "2.0.0",
  "initialized": "2024-01-15T10:30:00Z",
  "projectName": "TaskFlow",
  "projectType": "new",
  "maxParallelTasks": 3,
  "testingStrategy": "tdd",
  "testingIntensity": "smart",
  "phases": {
    "discovery": { "status": "pending", "completedAt": null },
    "definition": { "status": "pending", "completedAt": null },
    "design": { "status": "pending", "completedAt": null },
    "plan": { "status": "pending", "completedAt": null }
  },
  "currentQuarter": null,
  "quarters": {},
  "requirements": {
    "planned": [],
    "unplanned": []
  },
  "lastUpdated": null
}
```

### Step 4: Create Directory Structure

```bash
mkdir -p docs/01-business
mkdir -p docs/02-product/ux
mkdir -p docs/02-product/architecture/adr
mkdir -p docs/03-requirements
mkdir -p docs/04-plan/quarters
mkdir -p docs/05-debt
```

### Step 5: Create Placeholder Files

**docs/clarification.md:**
```markdown
# Clarification Log

## Resolved
(None yet)

## Pending
(None yet)
```

**docs/decision-log.md:**
```markdown
# Decision Log

Decisions are tracked in `decisions.json` and exported here.

## Decisions
(None yet)
```

### Step 6: Output Summary

**For existing projects:**
```
Peachflow initialized for existing project.

Settings:
  Project: [name]
  Testing: [strategy] / [intensity]
  Parallel tasks: [n]

Next: /peachflow:analyze
```

**For new projects:**
```
Peachflow initialized for new project.

Settings:
  Project: [name]
  Testing: [strategy] / [intensity]
  Parallel tasks: [n]

Next: /peachflow:discover "your product idea"
```

---

## Configuration Mode (Reconfigure Existing)

When project is already initialized or called as `/peachflow:config`.

### Step 1: Show Current Settings

```bash
${CLAUDE_PLUGIN_ROOT}/scripts/state-manager.sh status
testing_strategy=$(${CLAUDE_PLUGIN_ROOT}/scripts/state-manager.sh get-testing-strategy)
testing_intensity=$(${CLAUDE_PLUGIN_ROOT}/scripts/state-manager.sh get-testing-intensity)
```

```
Current settings:
  Project: TaskFlow
  Testing: TDD / Smart
  Parallel tasks: 3

Phase status:
  [x] Discovery (completed)
  [x] Definition (completed)
  [ ] Design (pending)
  [ ] Plan (pending)
```

### Step 2: Ask What to Configure

```json
{
  "questions": [{
    "question": "What would you like to configure?",
    "header": "Configure",
    "options": [
      {"label": "Testing strategy", "description": "Change TDD/BDD/ATDD/Test-last/None"},
      {"label": "Testing intensity", "description": "Change Essential/Smart/Intense"},
      {"label": "Parallel tasks", "description": "Change how many tasks run concurrently"},
      {"label": "Project name", "description": "Rename the project"}
    ],
    "multiSelect": true
  }]
}
```

### Step 3: Apply Selected Changes

**If testing strategy selected:**
```json
{
  "questions": [{
    "question": "Select testing strategy:",
    "header": "Testing",
    "options": [
      {"label": "No Tests", "description": "Skip automated testing"},
      {"label": "TDD", "description": "Test Driven Development"},
      {"label": "BDD", "description": "Behavior Driven Development"},
      {"label": "ATDD", "description": "Acceptance Test Driven"},
      {"label": "Test-last", "description": "Tests after implementation"}
    ],
    "multiSelect": false
  }]
}
```

**If testing intensity selected:**
```json
{
  "questions": [{
    "question": "Select test intensity:",
    "header": "Intensity",
    "options": [
      {"label": "Essential", "description": "Unit tests only"},
      {"label": "Smart", "description": "Unit + component + mocked API"},
      {"label": "Intense", "description": "Everything + Playwright UI tests"}
    ],
    "multiSelect": false
  }]
}
```

**If parallel tasks selected:**
```json
{
  "questions": [{
    "question": "How many parallel tasks?",
    "header": "Parallel",
    "options": [
      {"label": "1", "description": "Sequential"},
      {"label": "2", "description": "Light parallel"},
      {"label": "3", "description": "Balanced"},
      {"label": "4", "description": "More parallel"},
      {"label": "6", "description": "Maximum"}
    ],
    "multiSelect": false
  }]
}
```

**If project name selected:**
Ask for new name via text input.

### Step 4: Update State

```bash
# Apply changes
${CLAUDE_PLUGIN_ROOT}/scripts/state-manager.sh set-testing "tdd" "smart"
${CLAUDE_PLUGIN_ROOT}/scripts/state-manager.sh set-max-parallel 4
${CLAUDE_PLUGIN_ROOT}/scripts/state-manager.sh set-project-name "NewName"
```

### Step 5: Summary

```
Configuration updated.

Changes:
  Testing: TDD → BDD
  Intensity: Smart → Intense
  Parallel: 3 → 4

Current settings:
  Project: TaskFlow
  Testing: BDD / Intense
  Parallel tasks: 4
```

---

## Testing Strategy Reference

| Strategy | Description | When to Use |
|----------|-------------|-------------|
| **No Tests** | Skip automated testing | MVPs, prototypes, time-critical |
| **TDD** | Write tests first, then code | When requirements are clear |
| **BDD** | Given/When/Then from user stories | Stakeholder collaboration |
| **ATDD** | From acceptance criteria | When criteria are explicit |
| **Test-last** | Tests after implementation | Legacy code, spikes |

## Testing Intensity Reference

| Intensity | Includes | When to Use |
|-----------|----------|-------------|
| **Essential** | Unit tests only | Fast feedback, MVPs |
| **Smart** | Unit + component + mocked API | Production apps |
| **Intense** | Smart + Playwright UI tests | Critical user flows |

---

## State File Location

The state file is created at the project root:
- `.peachflow-state.json` - Track phases, quarters, requirements, testing config

This file should be committed to version control so team members share state.

---

## Troubleshooting

**"Permission denied" errors:**
```bash
ls -la .
```

**Re-initializing:**
```bash
rm .peachflow-state.json
/peachflow:init
```
Note: This does NOT delete your docs/ - only resets state tracking.
