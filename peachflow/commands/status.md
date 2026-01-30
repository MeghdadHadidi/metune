---
name: peachflow:status
description: Show current project status including completed phases, current quarter, and task progress.
argument-hint: ""
disable-model-invocation: true
allowed-tools: Read, Grep, Glob, Bash
---

# /peachflow:status - Project Status

Display comprehensive project status including phases, documents, and task progress.

## Workflow

### 1. Check State File

```bash
${CLAUDE_PLUGIN_ROOT}/scripts/state-manager.sh status
```

This shows:
- Phase completion status
- Current quarter
- Last update time

### 2. Document Inventory

Check which documents exist:

```bash
echo "=== Documents ==="

# Business
echo "Business:"
ls -la docs/01-business/*.md 2>/dev/null || echo "  (none)"

# Product
echo "Product:"
ls -la docs/02-product/*.md 2>/dev/null || echo "  (none)"

# ADRs
echo "ADRs:"
ls -la docs/02-product/architecture/adr/*.md 2>/dev/null || echo "  (none)"
```

### 3. Clarification Status

Count pending clarifications:
```bash
pending=$(grep -r "\[NEEDS CLARIFICATION" docs/ --include="*.md" 2>/dev/null | wc -l)
echo "Pending clarifications: $pending"
```

### 4. Task Progress (if quarter selected)

If a quarter is in progress:
```bash
quarter=$(${CLAUDE_PLUGIN_ROOT}/scripts/state-manager.sh get-quarter)
if [ "$quarter" != "none" ]; then
  echo "=== ${quarter} Progress ==="
  ${CLAUDE_PLUGIN_ROOT}/scripts/checklist-manager.sh count "docs/04-plan/quarters/${quarter}/plan.md"
fi
```

### 5. Display Summary

Format output as:

```
=== Peachflow Project Status ===

Phases:
  [x] Discovery: completed (2024-01-10)
  [>] Plan: in_progress

Current Quarter: Q1
Current Sprint: S-001

Documents:
  Business (1):
    - BRD.md
  Product (2):
    - PRD.md
  ADRs (3):
    - ADR-0001: Database choice
    - ADR-0002: Authentication
    - [...]

Graph (from .peachflow-graph.json):
  Epics: 5 (2 completed)
  User Stories: 15 (8 completed)
  Tasks: 42 (24 completed, 57%)
  Sprints: 3 (1 active)

Clarifications:
  Pending: 3
  Resolved: 12

Next Actions:
  - Run /peachflow:plan to create stories and tasks
  - Run /peachflow:clarify to resolve 3 pending questions
```

## Quick Commands

Show just phases:
```bash
${CLAUDE_PLUGIN_ROOT}/scripts/state-manager.sh status
```

Show just task progress:
```bash
${CLAUDE_PLUGIN_ROOT}/scripts/checklist-manager.sh count docs/04-plan/quarters/q01/plan.md
```

Show pending clarifications:
```bash
grep -r "\[NEEDS CLARIFICATION" docs/ --include="*.md"
```
