---
name: peachflow:design
description: Create UX design specifications and system architecture. Produces UX documents in /docs/02-product/ux and architecture in /docs/02-product/architecture.
argument-hint: ""
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Grep, Glob, WebSearch, Task, AskUserQuestion, Bash
---

# /peachflow:design - Design Phase

Create comprehensive UX design specifications and system architecture documentation.

## Prerequisites

Definition phase must be complete:
- `/docs/03-requirements/FRD.md` exists
- `/docs/03-requirements/NFRs.md` exists

Check with:
```bash
${CLAUDE_PLUGIN_ROOT}/scripts/state-manager.sh get-phase definition
```

If definition not completed, prompt user to run `/peachflow:define` first.

## Workflow

### Phase 0: Initialize

1. Ensure prerequisites met
2. Copy UX templates to project:
```bash
mkdir -p docs/02-product/ux docs/02-product/architecture/adr
cp -r ${CLAUDE_PLUGIN_ROOT}/templates/ux/* docs/templates/ux/ 2>/dev/null || true
```

3. Update state:
```bash
${CLAUDE_PLUGIN_ROOT}/scripts/state-manager.sh set-phase design in_progress
```

### Phase 1: User Research Review
**Invoke**: user-researcher agent (briefly)

Review existing user research and ensure design is user-centered:
1. Re-read user-personas.md
2. Re-read user-flows.md
3. Identify key design implications

### Phase 2: UX Design
**Invoke**: ux-designer agent

The ux-designer will create all UX documents in `/docs/02-product/ux/`:

1. **ux-strategy.md** - UX vision and goals
2. **design-principles.md** - Guiding principles
3. **brand-guidelines.md** - Visual identity
4. **design-system.md** - Tokens, foundations
5. **component-library.md** - Component specs
6. **content-style-guide.md** - UX writing
7. **interaction-specs.md** - Interaction patterns
8. **motion-guidelines.md** - Animation principles
9. **accessibility-guidelines.md** - WCAG compliance
10. **responsive-specs.md** - Breakpoints
11. **ui-specifications.md** - Per-screen details

Each document should be max 1 page, focused on practical guidance.

### Phase 3: Architecture Design
**Invoke**: software-architect agent

The software-architect will:

1. Create high-level design in `/docs/02-product/architecture/high-level-design.md`
2. Document key technology decisions as ADRs in `/docs/02-product/architecture/adr/`:
   - `0001-database-choice.md`
   - `0002-authentication-approach.md`
   - `0003-api-architecture.md`
   - `0004-frontend-framework.md`
   - `0005-deployment-platform.md`
   - [Additional as needed]

### Phase 4: Clarification
**Invoke**: clarification-agent

Scan all design documents for `[NEEDS CLARIFICATION]` markers and resolve.

### Phase 5: Finalize

1. Update state:
```bash
${CLAUDE_PLUGIN_ROOT}/scripts/state-manager.sh set-phase design completed
```

2. Show summary and next steps

## Output Structure

```
docs/
├── 02-product/
│   ├── ux/
│   │   ├── ux-strategy.md
│   │   ├── design-principles.md
│   │   ├── brand-guidelines.md
│   │   ├── design-system.md
│   │   ├── component-library.md
│   │   ├── content-style-guide.md
│   │   ├── interaction-specs.md
│   │   ├── motion-guidelines.md
│   │   ├── accessibility-guidelines.md
│   │   ├── responsive-specs.md
│   │   └── ui-specifications.md
│   └── architecture/
│       ├── high-level-design.md
│       └── adr/
│           ├── 0001-database-choice.md
│           ├── 0002-authentication-approach.md
│           └── ...
└── templates/
    └── ux/
        └── [Template files for reference]
```

## Agent Collaboration Flow

```
[Check Prerequisites]
       │
       ▼
┌────────────────────┐
│  user-researcher   │ ──→ Review user context
│     (sonnet)       │
└────────────────────┘
       │
       ▼
┌────────────────────┐
│    ux-designer     │ ──→ 11 UX documents
│      (opus)        │
└────────────────────┘
       │
       ▼
┌────────────────────┐
│ software-architect │ ──→ HLD + ADRs
│      (opus)        │
└────────────────────┘
       │
       ▼
┌────────────────────┐
│ clarification-agent│ ──→ Resolved questions
│     (sonnet)       │
└────────────────────┘
       │
       ▼
[Design Complete]

Next: /peachflow:plan (delivery planning)
```

## Guidelines

- **Keep docs short**: Each UX doc max 1 page
- **Be practical**: Focus on implementation guidance
- **Use templates**: Reference templates in `/docs/templates/ux/`
- **Justify decisions**: ADRs explain why, not just what
- **Mark unknowns**: Use `[NEEDS CLARIFICATION: ...]`
