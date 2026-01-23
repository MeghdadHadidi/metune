---
name: peachflow:define
description: Define detailed functional and non-functional requirements from BRD and PRD. Creates FRD.md and NFRs.md.
argument-hint: ""
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Grep, Glob, Task, AskUserQuestion, Bash
---

# /peachflow:define - Requirements Definition Phase

Transform business and product requirements into detailed, implementable specifications.

## Prerequisites

Discovery phase must be complete:
- `/docs/01-business/BRD.md` exists
- `/docs/02-product/PRD.md` exists

Check with:
```bash
${CLAUDE_PLUGIN_ROOT}/scripts/state-manager.sh get-phase discovery
```

If discovery not completed, prompt user to run `/peachflow:discover` first.

## Workflow

### Phase 0: Validate Prerequisites

1. Check discovery is complete
2. Read existing documents:
   - BRD.md for business requirements
   - PRD.md for features
   - user-personas.md for context
   - user-flows.md for journeys

3. Update state:
```bash
${CLAUDE_PLUGIN_ROOT}/scripts/state-manager.sh set-phase definition in_progress
```

### Phase 1: Functional Requirements
**Invoke**: requirements-analyst agent

The requirements-analyst will:
1. Map each PRD feature to detailed functional requirements
2. Specify inputs, processing, outputs
3. Define acceptance criteria for each requirement
4. Identify dependencies between requirements
5. Create `/docs/03-requirements/FRD.md`

**Output**: FRD.md with FR-XXX requirements

### Phase 2: Non-Functional Requirements
**Continue with**: requirements-analyst agent

The requirements-analyst will:
1. Extract non-functional needs from BRD
2. Define performance targets
3. Specify security requirements
4. Document scalability needs
5. Create `/docs/03-requirements/NFRs.md`

**Output**: NFRs.md with NFR-XXX requirements

### Phase 3: Clarification
**Invoke**: clarification-agent

The clarification-agent will:
1. Scan FRD and NFRs for `[NEEDS CLARIFICATION]` markers
2. Ask user targeted questions
3. Update documents with answers

### Phase 4: Finalize

1. Update state:
```bash
${CLAUDE_PLUGIN_ROOT}/scripts/state-manager.sh set-phase definition completed
```

2. Show summary and next steps

## Output Structure

```
docs/
└── 03-requirements/
    ├── FRD.md    # Functional requirements (FR-001, FR-002, ...)
    └── NFRs.md   # Non-functional requirements (NFR-001, NFR-002, ...)
```

## Agent Collaboration Flow

```
[Check Prerequisites]
       │
       ▼
┌────────────────────┐
│ requirements-analyst│ ──→ FRD.md
│      (opus)        │
└────────────────────┘
       │
       ▼
┌────────────────────┐
│ requirements-analyst│ ──→ NFRs.md
│      (opus)        │
└────────────────────┘
       │
       ▼
┌────────────────────┐
│ clarification-agent │ ──→ Resolved questions
│     (sonnet)       │
└────────────────────┘
       │
       ▼
[Definition Complete]

Next: /peachflow:design (UX and architecture)
```

## Requirement ID Format

- **FR-XXX**: Functional Requirements
  - FR-001 to FR-099: User Management
  - FR-100 to FR-199: Core Features
  - FR-200 to FR-299: Integrations

- **NFR-XXX**: Non-Functional Requirements
  - NFR-001 to NFR-019: Performance
  - NFR-020 to NFR-039: Security
  - NFR-040 to NFR-059: Scalability
  - NFR-060 to NFR-079: Reliability
  - NFR-080 to NFR-099: Usability

## Guidelines

- **Trace everything**: Every FR links to PRD feature, every NFR to BRD requirement
- **Be specific**: Avoid vague requirements
- **Make testable**: Clear acceptance criteria
- **Mark unknowns**: Use `[NEEDS CLARIFICATION: ...]`
- **Dependencies**: Document requirement dependencies
