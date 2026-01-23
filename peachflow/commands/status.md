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

# UX
echo "UX:"
ls -la docs/02-product/ux/*.md 2>/dev/null || echo "  (none)"

# Architecture
echo "Architecture:"
ls -la docs/02-product/architecture/*.md 2>/dev/null || echo "  (none)"

# ADRs
echo "ADRs:"
ls -la docs/02-product/architecture/adr/*.md 2>/dev/null || echo "  (none)"

# Requirements
echo "Requirements:"
ls -la docs/03-requirements/*.md 2>/dev/null || echo "  (none)"

# Plan
echo "Plan:"
ls -la docs/04-plan/*.md 2>/dev/null || echo "  (none)"
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
  [x] Definition: completed (2024-01-12)
  [x] Design: completed (2024-01-15)
  [>] Plan: in_progress
  [ ] Implementation: pending

Current Quarter: Q1

Documents:
  Business (1):
    - BRD.md
  Product (4):
    - PRD.md
    - user-personas.md
    - user-flows.md
  UX (11):
    - ux-strategy.md
    - design-system.md
    - [...]
  Architecture (1 + 5 ADRs):
    - high-level-design.md
    - ADR-0001: Database choice
    - ADR-0002: Authentication
    - [...]
  Requirements (2):
    - FRD.md
    - NFRs.md
  Plan:
    - plan.md

Clarifications:
  Pending: 3
  Resolved: 12

Q1 Progress:
  Epics: 2/5 complete
  User Stories: 8/15 complete
  Tasks: 24/42 complete (57%)

Next Actions:
  - Run /peachflow:plan Q1 to create quarterly plan
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
