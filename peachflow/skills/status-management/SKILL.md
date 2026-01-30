---
name: status-management
description: |
  Use this skill when implementing tasks or managing work items. Defines when and how to update status fields in the graph. Status updates cascade automatically (task → story → epic → quarter → sprint).

  <example>
  Context: Developer agent completing a task
  user: "Implement the login form"
  assistant: "I'll mark T-003 as in_progress, implement it, then mark it completed."
  <commentary>Agents must update task status at start and end of implementation.</commentary>
  </example>
---

# Status Management

## CRITICAL: Always Update Status

**Every implementation agent MUST:**
1. Mark task `in_progress` when starting work
2. Mark task `completed` when work is done
3. The graph automatically cascades status updates to parent entities

## Status Values by Entity Type

| Entity | Valid Statuses | Lifecycle |
|--------|---------------|-----------|
| Quarter | `planned` → `active` → `completed` | Set by commands |
| Epic | `draft` → `ready` → `in_progress` → `completed` | Auto-cascaded |
| Story | `draft` → `ready` → `in_progress` → `completed` | Auto-cascaded |
| Task | `pending` → `in_progress` → `completed` | **Agent responsibility** |
| Sprint | `planned` → `active` → `completed` | Auto-cascaded |
| Clarification | `pending` → `clarified` | Set when answered |

Special statuses:
- `blocked` - For epics/stories/tasks with unresolved blockers
- `skipped` - For tasks intentionally not implemented

## Automatic Cascading

When you update a task status, the graph automatically:

```
Task completed
    ↓
Story checks: All tasks done? → Story completed
    ↓
Epic checks: All stories done? → Epic completed
    ↓
Quarter checks: All epics done? → Quarter completed
    ↓
Sprint checks: All sprint tasks done? → Sprint completed
```

**You only need to update the task. Parents update automatically.**

## Commands

### Starting Work on a Task

```bash
# Mark task as in progress
${CLAUDE_PLUGIN_ROOT}/scripts/peachflow-graph.py update task T-XXX --status in_progress
```

### Completing a Task

```bash
# Mark task as completed (cascades to story/epic/quarter/sprint)
${CLAUDE_PLUGIN_ROOT}/scripts/peachflow-graph.py update task T-XXX --status completed
```

### Blocking a Task

```bash
# Mark task as blocked (when dependencies aren't met or issues found)
${CLAUDE_PLUGIN_ROOT}/scripts/peachflow-graph.py update task T-XXX --status blocked
```

### Skipping a Task

```bash
# Skip task (intentionally not implementing)
${CLAUDE_PLUGIN_ROOT}/scripts/peachflow-graph.py update task T-XXX --status skipped
```

## Agent Implementation Pattern

Every implementation agent should follow this pattern:

```
1. BEFORE implementing:
   ${CLAUDE_PLUGIN_ROOT}/scripts/peachflow-graph.py update task T-XXX --status in_progress

2. Implement the task...

3. AFTER successful implementation:
   ${CLAUDE_PLUGIN_ROOT}/scripts/peachflow-graph.py update task T-XXX --status completed

4. If implementation fails or is blocked:
   ${CLAUDE_PLUGIN_ROOT}/scripts/peachflow-graph.py update task T-XXX --status blocked
```

## Checking Current Status

```bash
# Get task details including status
${CLAUDE_PLUGIN_ROOT}/scripts/peachflow-graph.py get task T-XXX

# See overall progress
${CLAUDE_PLUGIN_ROOT}/scripts/peachflow-graph.py stats

# List tasks by status
${CLAUDE_PLUGIN_ROOT}/scripts/peachflow-graph.py list tasks --status pending
${CLAUDE_PLUGIN_ROOT}/scripts/peachflow-graph.py list tasks --status in_progress
${CLAUDE_PLUGIN_ROOT}/scripts/peachflow-graph.py list tasks --status completed
```

## DO NOT

- Forget to update task status (this breaks tracking)
- Manually update story/epic/quarter status (let cascade handle it)
- Mark tasks completed without actually finishing the work
- Leave tasks in `in_progress` if you stop working on them
