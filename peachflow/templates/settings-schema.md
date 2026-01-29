# Peachflow Settings Schema

This schema defines all user-configurable settings for peachflow. The `/peachflow:init` and `/peachflow:config` commands MUST use this exact format when presenting options to users.

## How to Use This Schema

1. Read this file to get the exact question format and options
2. Present questions using AskUserQuestion with EXACTLY these options
3. Store values in `.peachflow-state.json` using the specified keys
4. Apply defaults when user skips or doesn't specify

---

## Settings Groups

### Group 1: Project Identity

**Key:** `projectName`
**Type:** Text input (via "Other" option)
**Default:** Directory name

```json
{
  "question": "What is the name of your project?",
  "header": "Project",
  "options": [
    {"label": "Use directory name", "description": "Use the current folder name as project name"},
    {"label": "Enter custom name", "description": "Type a custom project name"}
  ],
  "multiSelect": false
}
```

---

### Group 2: Project Type

**Key:** `projectType`
**Type:** Single select
**Default:** `new`

```json
{
  "question": "What type of project is this?",
  "header": "Type",
  "options": [
    {"label": "New project", "description": "Starting from scratch, no existing code"},
    {"label": "Existing codebase", "description": "Adding peachflow to a project already in development"},
    {"label": "Continuing previous", "description": "Resuming a peachflow project from backup"}
  ],
  "multiSelect": false
}
```

**Value mapping:**
- "New project" → `"new"`
- "Existing codebase" → `"existing"`
- "Continuing previous" → `"continuing"`

---

### Group 3: Testing Strategy

**Key:** `testingStrategy`
**Type:** Single select
**Default:** `none`

```json
{
  "question": "What testing approach should we use?",
  "header": "Testing",
  "options": [
    {"label": "No automated tests", "description": "Skip testing, focus on speed (good for MVPs)"},
    {"label": "TDD (Test-Driven)", "description": "Write tests first, then implementation"},
    {"label": "BDD (Behavior-Driven)", "description": "Given/When/Then tests from user stories"},
    {"label": "Test after code", "description": "Write tests after implementation"}
  ],
  "multiSelect": false
}
```

**Value mapping:**
- "No automated tests" → `"none"`
- "TDD (Test-Driven)" → `"tdd"`
- "BDD (Behavior-Driven)" → `"bdd"`
- "Test after code" → `"test-last"`

---

### Group 4: Testing Intensity

**Key:** `testingIntensity`
**Type:** Single select
**Default:** `none`
**Condition:** Only show if `testingStrategy` is NOT `none`

```json
{
  "question": "What level of test coverage?",
  "header": "Coverage",
  "options": [
    {"label": "Essential only", "description": "Unit tests for core logic"},
    {"label": "Standard", "description": "Unit + component + API mock tests"},
    {"label": "Comprehensive", "description": "Standard + end-to-end UI tests"}
  ],
  "multiSelect": false
}
```

**Value mapping:**
- "Essential only" → `"essential"`
- "Standard" → `"smart"`
- "Comprehensive" → `"intense"`

---

### Group 5: Parallel Tasks

**Key:** `maxParallelTasks`
**Type:** Single select
**Default:** `3`

```json
{
  "question": "How many tasks should run in parallel during implementation?",
  "header": "Parallel",
  "options": [
    {"label": "1 (Sequential)", "description": "One task at a time, maximum control"},
    {"label": "2 (Light)", "description": "Two concurrent tasks"},
    {"label": "3 (Balanced)", "description": "Three concurrent tasks (recommended)"},
    {"label": "4 (More)", "description": "Four concurrent tasks"},
    {"label": "6 (Maximum)", "description": "Six concurrent tasks, fastest execution"}
  ],
  "multiSelect": false
}
```

**Value mapping:**
- "1 (Sequential)" → `1`
- "2 (Light)" → `2`
- "3 (Balanced)" → `3`
- "4 (More)" → `4`
- "6 (Maximum)" → `6`

---

### Group 6: Version Control

**Key:** `versionControlDocs`
**Type:** Single select
**Default:** `true`

```json
{
  "question": "Should peachflow files be version controlled (committed to git)?",
  "header": "Git",
  "options": [
    {"label": "Yes, track in git", "description": "Commit docs, state, and graph to repository (recommended for teams)"},
    {"label": "No, ignore in git", "description": "Add peachflow files to .gitignore (local-only workflow)"}
  ],
  "multiSelect": false
}
```

**Value mapping:**
- "Yes, track in git" → `true`
- "No, ignore in git" → `false`

**When `false`, add to `.gitignore`:**
```
# Peachflow (local-only mode)
.peachflow-state.json
.peachflow-graph.json
docs/
.claude/skills/
```

---

## Configuration Mode Menu

When reconfiguring, present this menu first:

**Key:** N/A (menu only)
**Type:** Multi-select

```json
{
  "question": "Which settings do you want to change?",
  "header": "Settings",
  "options": [
    {"label": "Project name", "description": "Change the project name"},
    {"label": "Testing strategy", "description": "Change TDD/BDD/None"},
    {"label": "Testing intensity", "description": "Change Essential/Standard/Comprehensive"},
    {"label": "Parallel tasks", "description": "Change concurrent task count"},
    {"label": "Version control", "description": "Change git tracking preference"}
  ],
  "multiSelect": true
}
```

Then present ONLY the selected setting questions using the exact formats above.

---

## State File Structure

```json
{
  "version": "3.0.0",
  "initialized": "2024-01-15T10:30:00Z",
  "projectName": "TaskFlow",
  "projectType": "new",
  "testingStrategy": "tdd",
  "testingIntensity": "smart",
  "maxParallelTasks": 3,
  "versionControlDocs": true,
  "phases": {
    "discovery": { "status": "pending", "completedAt": null },
    "design": { "status": "pending", "completedAt": null },
    "plan": { "status": "pending", "completedAt": null }
  },
  "currentSprint": null,
  "currentQuarter": null,
  "lastUpdated": null
}
```

---

## Display Format for Current Settings

When showing current settings (in config mode), use this format:

```
Current Settings
────────────────────────────────────────
Project:      TaskFlow
Type:         New project
Testing:      TDD (Test-Driven) / Standard
Parallel:     3 tasks
Git tracking: Yes

Phases:
  [x] Discovery (completed)
  [x] Design (completed)
  [ ] Plan (pending)
```

---

## Consistency Rules

1. **Always use the exact question text** from this schema
2. **Always use the exact option labels** - no variations
3. **Always show options in the same order** as defined here
4. **Never add extra options** not in this schema
5. **Never change descriptions** - use them verbatim
6. **Always apply value mappings** correctly to state file
