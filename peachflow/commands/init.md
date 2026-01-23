---
name: peachflow:init
description: Initialize peachflow for a project. Creates the state file and docs structure. Required before using other peachflow commands.
allowed-tools: Read, Write, Bash, Glob, AskUserQuestion
---

# /peachflow:init - Initialize Peachflow

Set up peachflow for a new or existing project. This command MUST be run before any other peachflow commands.

## Pre-flight Check

First, check if peachflow is already initialized:

```bash
if [ -f ".peachflow-state.json" ]; then
  echo "ALREADY_INITIALIZED"
fi
```

**If already initialized:**
```
Peachflow is already initialized for this project.

Current status:
  [Show output of state-manager.sh status]

Commands you can use:
  /peachflow:discover "idea"  - Add new feature/initiative
  /peachflow:status          - View detailed status
  /peachflow:plan            - Continue planning
```

## Initialization Workflow

### Step 1: Get Project Information

Ask the user for project details:

```json
{
  "questions": [
    {
      "question": "What is the name of your project?",
      "header": "Project Name",
      "options": [
        {"label": "Enter name", "description": "You'll type the project name (e.g., 'TaskFlow', 'ShopEase', 'DevHub')"}
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
    }
  ]
}
```

**IMPORTANT**: The project name will be used throughout all generated documents (BRD, PRD, architecture, etc.). Make sure to capture the exact name the user wants for their product/project.

### Step 2: Create State File

```bash
# Use the project name provided by the user
${CLAUDE_PLUGIN_ROOT}/scripts/state-manager.sh init "ProjectName" "new|existing|continued"
```

This creates `.peachflow-state.json`:

```json
{
  "version": "2.0.0",
  "initialized": "2024-01-15T10:30:00Z",
  "projectName": "TaskFlow",
  "projectType": "new|existing|continued",
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
  "features": [],
  "lastUpdated": null
}
```

**Note**: The `projectName` is used by all agents when generating documents. Always use this name (not "Peachflow" or the plugin name) when referring to the product being built.

### Step 3: Create Directory Structure

```bash
mkdir -p docs/01-business
mkdir -p docs/02-product/ux
mkdir -p docs/02-product/architecture/adr
mkdir -p docs/03-requirements
mkdir -p docs/04-plan/quarters
mkdir -p docs/05-debt
```

### Step 4: Create Placeholder Files

Create minimal placeholder files:

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

### Step 5: For Existing Projects

If user selected "Existing codebase":

```
Peachflow initialized for existing project.

Next step: Run /peachflow:analyze to:
- Scan your codebase
- Create discovery documents from existing code
- Identify technical debt
- Prepare for planning

Run: /peachflow:analyze
```

### Step 6: For New Projects

If user selected "New project":

```
Peachflow initialized for new project.

Next step: Run /peachflow:discover with your product idea:

  /peachflow:discover "brief description of your product"

Example:
  /peachflow:discover "task management app for remote teams"
```

## Output Summary

```
Peachflow initialized successfully!

Created:
  ✓ .peachflow-state.json (project state)
  ✓ docs/ directory structure
  ✓ Placeholder files

Project type: [New/Existing/Continued]

Next steps:
  [Appropriate next command based on project type]
```

## State File Location

The state file is created at the project root:
- `.peachflow-state.json` - Track phases, quarters, requirements

This file should be committed to version control so team members share state.

## Troubleshooting

**"Permission denied" errors:**
```bash
# Ensure you have write access to project directory
ls -la .
```

**"Directory already exists" warnings:**
These are safe to ignore - existing directories are preserved.

**Re-initializing:**
If you need to start fresh:
```bash
rm .peachflow-state.json
/peachflow:init
```
Note: This does NOT delete your docs/ - only resets state tracking.
