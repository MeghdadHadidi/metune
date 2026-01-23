---
name: peachflow:discover
description: Start product discovery phase. Creates BRD and PRD through business analyst, market analyst, and user researcher agents.
argument-hint: "[product idea description]"
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Grep, Glob, WebSearch, WebFetch, Task, AskUserQuestion, Bash
---

# /peachflow:discover - Product Discovery Phase

Run comprehensive product discovery to create foundational business and product documents.

## Overview

Discovery produces:
- Business Requirements Document (BRD) in `/docs/01-business/`
- Product Requirements Document (PRD) in `/docs/02-product/`

This phase focuses on answering critical business questions efficiently without over-researching.

## Workflow

### Phase 0: Initialize

1. Create directory structure:
```bash
mkdir -p docs/01-business docs/02-product docs/03-requirements docs/04-plan
```

2. Initialize state:
```bash
${CLAUDE_PLUGIN_ROOT}/scripts/state-manager.sh init
${CLAUDE_PLUGIN_ROOT}/scripts/state-manager.sh set-phase discovery in_progress
```

### Phase 1: Business Analysis
**Invoke**: business-analyst agent

The business-analyst will:
1. Identify stakeholders and their concerns
2. Define business objectives and success criteria
3. Assess high-level risks and constraints
4. Create initial market validation
5. Document in `/docs/01-business/BRD.md`

**Output**: BRD.md with BR-XXX requirements

### Phase 2: Market Research
**Invoke**: market-analyst agent

The market-analyst will:
1. Research market size and growth
2. Identify top 3 competitors
3. Analyze competitive positioning
4. Find market gaps and opportunities
5. Update BRD with market findings

**Output**: Market analysis section in BRD.md

### Phase 3: User Research
**Invoke**: user-researcher agent

The user-researcher will:
1. Create 2-3 user personas based on target market
2. Map key user journeys
3. Identify pain points and opportunities
4. Document in `/docs/02-product/`

**Output**:
- `user-personas.md`
- `user-flows.md`

### Phase 4: Product Definition
**Invoke**: product-manager agent

The product-manager will:
1. Synthesize BRD and user research
2. Define feature set with priorities
3. Create acceptance criteria
4. Document in `/docs/02-product/PRD.md`

**Output**: PRD.md with F-XXX features

### Phase 5: Clarification
**Invoke**: clarification-agent

The clarification-agent will:
1. Scan all documents for `[NEEDS CLARIFICATION]` markers
2. Ask user targeted questions
3. Update documents with answers

**Output**: Resolved clarification items

### Phase 6: Finalize

1. Update state:
```bash
${CLAUDE_PLUGIN_ROOT}/scripts/state-manager.sh set-phase discovery completed
```

2. Show summary and next steps

## Input

```
/peachflow:discover "A project management tool for remote teams that focuses on async communication"
```

If no argument provided, prompt user for product description.

## Output Structure

```
docs/
├── 01-business/
│   └── BRD.md           # Business requirements
└── 02-product/
    ├── PRD.md           # Product requirements
    ├── user-personas.md # User personas
    └── user-flows.md    # User journey maps
```

## Agent Collaboration Flow

```
[User Input]
      │
      ▼
┌──────────────────┐
│ business-analyst │ ──→ BRD.md
│     (opus)       │
└──────────────────┘
      │
      ▼
┌──────────────────┐
│ market-analyst   │ ──→ BRD.md (market section)
│    (sonnet)      │
└──────────────────┘
      │
      ▼
┌──────────────────┐
│ user-researcher  │ ──→ user-personas.md, user-flows.md
│    (sonnet)      │
└──────────────────┘
      │
      ▼
┌──────────────────┐
│ product-manager  │ ──→ PRD.md
│     (opus)       │
└──────────────────┘
      │
      ▼
┌──────────────────┐
│ clarification    │ ──→ Resolved questions
│    (sonnet)      │
└──────────────────┘
      │
      ▼
[Discovery Complete]

Next: /peachflow:define (requirements specification)
```

## Guidelines

- **Don't over-research**: Get key insights from credible sources, then move on
- **Be practical**: Focus on answering important questions
- **Bullet points over prose**: Keep documentation scannable
- **Mark unknowns**: Use `[NEEDS CLARIFICATION: ...]` for gaps
- **Each doc max 1-2 pages**: Don't over-explain
