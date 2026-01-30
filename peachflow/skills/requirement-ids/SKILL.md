---
name: requirement-ids
description: |
  Use this skill when creating or referencing requirements, features, epics, stories, or tasks. Ensures consistent ID formats and traceability.
---

# Requirement ID System

## ID Formats

| Type | Format | Range | Example |
|------|--------|-------|---------|
| Epic | E-XXX | 001-999 | E-001 |
| User Story | US-XXX | 001-999 | US-001 |
| Task | T-XXX | 001-999 | T-001 |
| Sprint | S-XXX | 001-999 | S-001 |
| Clarification | CL-XXX | 001-999 | CL-001 |
| ADR | ADR-NNNN | 0001-9999 | ADR-0001 |

## Hierarchy Chain

IDs link through the graph structure:

```
E-001 (Epic)
  └── US-001, US-002 (User Stories)
        └── T-001, T-002, T-003 (Tasks)

S-001 (Sprint)
  └── T-001, T-002 (Tasks assigned to sprint)
```

## Usage Examples

### Creating Epics
```bash
${CLAUDE_PLUGIN_ROOT}/scripts/peachflow-graph.py create epic \
  --title "User Authentication" \
  --quarter Q1 \
  --priority 1 \
  --description "Complete auth system"
```

### Creating Stories
```bash
${CLAUDE_PLUGIN_ROOT}/scripts/peachflow-graph.py create story \
  --epic E-001 \
  --title "User can register" \
  --description "New users can create accounts" \
  --acceptance "Given valid email,When form submitted,Then account created"
```

### Creating Tasks
```bash
${CLAUDE_PLUGIN_ROOT}/scripts/peachflow-graph.py create task \
  --story US-001 \
  --title "Create registration API" \
  --tag BE \
  --description "POST /api/users endpoint"
```

## Finding by ID

```bash
# Get entity details
${CLAUDE_PLUGIN_ROOT}/scripts/peachflow-graph.py get epic E-001
${CLAUDE_PLUGIN_ROOT}/scripts/peachflow-graph.py get story US-001
${CLAUDE_PLUGIN_ROOT}/scripts/peachflow-graph.py get task T-001

# Get hierarchy chain
${CLAUDE_PLUGIN_ROOT}/scripts/peachflow-graph.py chain T-001

# Get all descendants of an epic
${CLAUDE_PLUGIN_ROOT}/scripts/peachflow-graph.py descendants epic E-001
```

## ID Assignment Rules

1. **Sequential**: Assign IDs in order (001, 002, 003...)
2. **Never reuse**: Don't reassign deleted IDs
3. **Prefix always**: Always include type prefix
4. **Zero-pad**: Use 3 digits (001 not 1)
5. **No gaps OK**: Gaps in sequence are fine (001, 002, 005)
