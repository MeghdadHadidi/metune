---
name: peachflow:init
description: Initialize peachflow v3 for a project. Creates state file and graph structure. Can reconfigure an existing project.
allowed-tools: Read, Write, Bash, Glob, AskUserQuestion
aliases: [peachflow:config]
---

# /peachflow:init - Initialize or Configure Peachflow v3

Set up peachflow for a new project or reconfigure an existing one.

## CRITICAL: Use Settings Schema

**You MUST read and follow the settings schema for all user questions:**

```bash
cat ${CLAUDE_PLUGIN_ROOT}/templates/settings-schema.md
```

Use the EXACT question text, option labels, and descriptions from the schema. Do not improvise or vary the format.

## Pre-flight Check

```bash
if [ -f ".peachflow-state.json" ]; then
  version=$(python3 -c "import json; print(json.load(open('.peachflow-state.json')).get('version', '2.0.0'))")
  echo "ALREADY_INITIALIZED version=$version"

  # Check if v2 (version < 3.0.0)
  major_version=$(echo "$version" | cut -d. -f1)
  if [ "$major_version" -lt 3 ]; then
    echo "V2_PROJECT_DETECTED"
  fi
fi
```

**Routing based on result:**
- `V2_PROJECT_DETECTED` → Migration Mode (see Migration from v2 section)
- `ALREADY_INITIALIZED version=3.x.x` (or called as /peachflow:config) → Configuration Mode
- No state file → Initialization Mode

---

## Initialization Mode (New Project)

### Step 1: Read Settings Schema

```bash
cat ${CLAUDE_PLUGIN_ROOT}/templates/settings-schema.md
```

### Step 2: Get Project Settings

Present questions using the EXACT format from the schema. Ask in this order:

**Question 1: Project Name** (from schema Group 1)
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

**Question 2: Project Type** (from schema Group 2)
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

**Question 3: Testing Strategy** (from schema Group 3)
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

**Question 4: Testing Intensity** (from schema Group 4)
*Only ask if testing strategy is NOT "No automated tests"*
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

**Question 5: Parallel Tasks** (from schema Group 5)
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

**Question 6: Version Control** (from schema Group 6)
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

### Step 3: Map User Choices to Values

Use the value mappings from the schema:

| User Choice | State Key | Value |
|-------------|-----------|-------|
| "New project" | projectType | `"new"` |
| "Existing codebase" | projectType | `"existing"` |
| "Continuing previous" | projectType | `"continuing"` |
| "No automated tests" | testingStrategy | `"none"` |
| "TDD (Test-Driven)" | testingStrategy | `"tdd"` |
| "BDD (Behavior-Driven)" | testingStrategy | `"bdd"` |
| "Test after code" | testingStrategy | `"test-last"` |
| "Essential only" | testingIntensity | `"essential"` |
| "Standard" | testingIntensity | `"smart"` |
| "Comprehensive" | testingIntensity | `"intense"` |
| "1 (Sequential)" | maxParallelTasks | `1` |
| "2 (Light)" | maxParallelTasks | `2` |
| "3 (Balanced)" | maxParallelTasks | `3` |
| "4 (More)" | maxParallelTasks | `4` |
| "6 (Maximum)" | maxParallelTasks | `6` |
| "Yes, track in git" | versionControlDocs | `true` |
| "No, ignore in git" | versionControlDocs | `false` |

### Step 4: Create State File

```bash
python3 << 'EOF'
import json
from datetime import datetime, timezone

state = {
    "version": "3.0.0",
    "initialized": datetime.now(timezone.utc).isoformat().replace("+00:00", "Z"),
    "projectName": "PROJECT_NAME_HERE",
    "projectType": "new",
    "testingStrategy": "none",
    "testingIntensity": "none",
    "maxParallelTasks": 3,
    "versionControlDocs": True,
    "phases": {
        "discovery": {"status": "pending", "completedAt": None},
        "plan": {"status": "pending", "completedAt": None}
    },
    "currentSprint": None,
    "currentQuarter": None,
    "lastUpdated": None
}

with open(".peachflow-state.json", "w") as f:
    json.dump(state, f, indent=2)
EOF
```

### Step 5: Initialize Graph

```bash
${CLAUDE_PLUGIN_ROOT}/scripts/peachflow-graph.py init
```

### Step 6: Create Directory Structure

```bash
mkdir -p docs/01-business
mkdir -p docs/02-product
mkdir -p docs/02-product/architecture/adr
```

### Step 7: Handle Version Control Setting

**If `versionControlDocs` is `false`**, add peachflow files to .gitignore:

```bash
# Check if .gitignore exists, create if not
touch .gitignore

# Check if peachflow section already exists
if ! grep -q "# Peachflow" .gitignore; then
  cat >> .gitignore << 'EOF'

# Peachflow (local-only mode)
.peachflow-state.json
.peachflow-graph.json
docs/
EOF
  echo "Added peachflow files to .gitignore"
fi
```

**If `versionControlDocs` is `true`** (default), do nothing special - files will be tracked normally.

### Step 8: Output Summary

Use the display format from the schema:

```
Current Settings
────────────────────────────────────────
Project:      [projectName]
Type:         [projectType display name]
Testing:      [testingStrategy display] / [testingIntensity display]
Parallel:     [maxParallelTasks] tasks
Git tracking: [Yes/No]

Files created:
  - .peachflow-state.json (project state)
  - .peachflow-graph.json (work items graph)
  - docs/ (document structure)

Next: /peachflow:discover "your product idea"
```

For existing codebases:
```
Next: /peachflow:analyze
```

---

## Configuration Mode (Reconfigure Existing)

### Step 1: Read Settings Schema

```bash
cat ${CLAUDE_PLUGIN_ROOT}/templates/settings-schema.md
```

### Step 2: Show Current Settings

Use the display format from the schema:

```bash
python3 << 'EOF'
import json

with open(".peachflow-state.json") as f:
    state = json.load(f)

# Display name mappings
strategy_names = {"none": "No automated tests", "tdd": "TDD (Test-Driven)", "bdd": "BDD (Behavior-Driven)", "test-last": "Test after code"}
intensity_names = {"none": "None", "essential": "Essential only", "smart": "Standard", "intense": "Comprehensive"}
type_names = {"new": "New project", "existing": "Existing codebase", "continuing": "Continuing previous"}

print("Current Settings")
print("─" * 40)
print(f"Project:      {state['projectName']}")
print(f"Type:         {type_names.get(state.get('projectType', 'new'), 'New project')}")
print(f"Testing:      {strategy_names.get(state.get('testingStrategy', 'none'), 'None')} / {intensity_names.get(state.get('testingIntensity', 'none'), 'None')}")
print(f"Parallel:     {state.get('maxParallelTasks', 3)} tasks")
print(f"Git tracking: {'Yes' if state.get('versionControlDocs', True) else 'No'}")
print()
print("Phases:")
for phase, data in state.get("phases", {}).items():
    status = data.get("status", "pending")
    icon = "[x]" if status == "completed" else "[ ]"
    print(f"  {icon} {phase.title()} ({status})")
EOF
```

### Step 3: Ask What to Configure

Use the Configuration Mode Menu from the schema:

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

### Step 4: Present Selected Setting Questions

For EACH selected setting, present the EXACT question from the schema (Groups 1-6).

**Important:** Only show questions for settings the user selected. Use the exact format from the schema.

### Step 5: Apply Changes

```bash
python3 << 'EOF'
import json
from datetime import datetime, timezone

with open(".peachflow-state.json", "r") as f:
    state = json.load(f)

# Apply changes (replace with actual values)
# state["projectName"] = "NewName"
# state["testingStrategy"] = "tdd"
# state["testingIntensity"] = "smart"
# state["maxParallelTasks"] = 4
# state["versionControlDocs"] = True

state["lastUpdated"] = datetime.now(timezone.utc).isoformat().replace("+00:00", "Z")

with open(".peachflow-state.json", "w") as f:
    json.dump(state, f, indent=2)
EOF
```

### Step 6: Handle Version Control Change

**If versionControlDocs changed to `false`:**
```bash
# Add to .gitignore
touch .gitignore
if ! grep -q "# Peachflow" .gitignore; then
  cat >> .gitignore << 'EOF'

# Peachflow (local-only mode)
.peachflow-state.json
.peachflow-graph.json
docs/
EOF
fi
```

**If versionControlDocs changed to `true`:**
```bash
# Remove peachflow section from .gitignore
if [ -f .gitignore ]; then
  # Remove the peachflow section
  sed -i '' '/# Peachflow (local-only mode)/,/^$/d' .gitignore 2>/dev/null || \
  sed -i '/# Peachflow (local-only mode)/,/^$/d' .gitignore
fi
```

### Step 7: Show Updated Settings

Use the same display format as Step 2, but show both old and new values for changed settings:

```
Configuration updated.

Changes:
  Testing: No automated tests → TDD (Test-Driven)
  Parallel: 3 → 4

Current Settings
────────────────────────────────────────
Project:      TaskFlow
Type:         New project
Testing:      TDD (Test-Driven) / Standard
Parallel:     4 tasks
Git tracking: Yes
```

---

## File Locations

| File | Purpose | Git Tracked |
|------|---------|-------------|
| `.peachflow-state.json` | Project config, phases, sprint | Per versionControlDocs |
| `.peachflow-graph.json` | Work items: epics, stories, tasks | Per versionControlDocs |
| `docs/` | BRD, PRD, ADRs | Per versionControlDocs |

---

## Migration from v2

If a v2 project is detected (version < 3.0.0):

### Step 1: Show Migration Info

```
Peachflow v2 project detected (version X.X.X).

Migration to v3 will:
✓ Preserve your docs/ directory (BRD, PRD, ADRs)
✓ Convert sprint/task markdown files to graph structure
✓ Update state file format
```

### Step 2: Ask User About Migration

```json
{
  "question": "Would you like to migrate this project to v3?",
  "header": "Migrate",
  "options": [
    {"label": "Yes, migrate now", "description": "Run migration and update project to v3"},
    {"label": "No, keep v2", "description": "Continue using v2 format (no changes made)"}
  ],
  "multiSelect": false
}
```

### Step 3: Handle User Choice

**If "Yes, migrate now":**

```bash
# Run migration script with verbose output
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/migrate-v2-to-v3.py --verbose

# Check if migration succeeded
if [ $? -eq 0 ]; then
  echo "MIGRATION_SUCCESS"
else
  echo "MIGRATION_FAILED"
fi
```

**If migration successful:**

Show migration summary and proceed to Configuration Mode to let user review/update settings.

```
Migration complete!

Migrated:
  - X epics
  - Y user stories
  - Z tasks
  - W sprints

Backup created: .peachflow-state.json.v2.backup

Your docs/ have been preserved. Review and update settings below.
```

Then proceed to Configuration Mode (Step 2 onwards) to let user review the migrated settings.

**If migration failed:**

```
Migration failed. Your original files have not been modified.

Common issues:
- Missing docs/04-plan/plan.md file
- Malformed sprint files
- Permission issues

Run with --dry-run to see what would be migrated:
  python3 ${CLAUDE_PLUGIN_ROOT}/scripts/migrate-v2-to-v3.py --dry-run --verbose

You can also continue using v2 or manually set up v3.
```

**If "No, keep v2":**

```
Keeping v2 format. No changes made.

Note: Future versions of peachflow may require v3 format.
Run /peachflow:init again when ready to migrate.
```

### Manual Migration

Users can also run the migration script directly:

```bash
# Preview what will be migrated (no changes made)
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/migrate-v2-to-v3.py --dry-run --verbose

# Run actual migration
python3 ${CLAUDE_PLUGIN_ROOT}/scripts/migrate-v2-to-v3.py --verbose
```

