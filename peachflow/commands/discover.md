---
name: peachflow:discover
description: Start product discovery for new projects OR add new features/initiatives to existing projects. Creates BRD/PRD or extends existing documentation.
argument-hint: "[product idea OR feature description]"
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Grep, Glob, WebSearch, WebFetch, Task, AskUserQuestion, Bash
---

# /peachflow:discover - Discovery Phase

Run product discovery for new projects OR add new features to existing projects.

## Pre-flight Check

**CRITICAL**: Check initialization and determine mode.

```bash
# Check if peachflow is initialized
if [ ! -f ".peachflow-state.json" ]; then
  echo "NOT_INITIALIZED"
fi

# Check if discovery was previously completed
discovery_status=$(${CLAUDE_PLUGIN_ROOT}/scripts/state-manager.sh get-phase discovery)
```

**If NOT initialized:**
```
Peachflow is not initialized for this project.

Run /peachflow:init first to set up the project.
```

## Get Project Name

**CRITICAL**: Always use the project name from state, not "Peachflow" or the plugin name.

```bash
# Get the project name to use in all documents
PROJECT_NAME=$(${CLAUDE_PLUGIN_ROOT}/scripts/state-manager.sh get-project-name)
echo "Discovering for: $PROJECT_NAME"
```

**All agents must use `$PROJECT_NAME` when referring to the product being built.**

## Two Modes of Operation

### Mode Detection

Based on discovery status:

| Condition | Mode |
|-----------|------|
| Discovery status = "pending" | **Full Discovery** (new project) |
| Discovery status = "completed" | **Feature Discovery** (add to existing) |

---

## Mode A: Full Discovery (New Project)

When discovery has never been run.

### Workflow

#### Phase 0: Initialize

```bash
${CLAUDE_PLUGIN_ROOT}/scripts/state-manager.sh set-phase discovery in_progress
mkdir -p docs/01-business docs/02-product docs/03-requirements docs/04-plan
```

#### Phase 1: Business Analysis
**Invoke**: business-analyst agent

Creates `/docs/01-business/BRD.md` with:
- Problem statement
- Business objectives
- Stakeholders
- Constraints
- BR-XXX requirements

#### Phase 2: Market Research
**Invoke**: market-analyst agent

Updates BRD with:
- Market validation
- Competitor analysis
- Market gaps/opportunities

#### Phase 3: User Research
**Invoke**: user-researcher agent

Creates:
- `/docs/02-product/user-personas.md`
- `/docs/02-product/user-flows.md`

#### Phase 4: Product Definition
**Invoke**: product-manager agent

Creates `/docs/02-product/PRD.md` with:
- Feature set (F-XXX)
- Priorities (Must/Should/Could/Won't)
- Acceptance criteria

#### Phase 5: Clarification
**Invoke**: clarification-agent

Resolves `[NEEDS CLARIFICATION]` markers.

#### Phase 6: Finalize

```bash
${CLAUDE_PLUGIN_ROOT}/scripts/state-manager.sh set-phase discovery completed

# Track all requirements as unplanned (not yet in quarterly plan)
# This will be read by /peachflow:plan
```

Update state with discovered requirements:
```bash
# Extract BR IDs and F IDs from docs
# Add them to state.requirements.unplanned[]
```

**Output:**
```
Discovery complete!

Created:
  - docs/01-business/BRD.md (X business requirements)
  - docs/02-product/PRD.md (X features)
  - docs/02-product/user-personas.md
  - docs/02-product/user-flows.md

Requirements ready for planning:
  - BR-001 through BR-XXX
  - F-001 through F-XXX

Next: /peachflow:define (detailed requirements)
```

---

## Mode B: Feature Discovery (Add to Existing Project)

When discovery was already completed and user wants to add new features/initiatives.

### Detection

```bash
discovery_status=$(${CLAUDE_PLUGIN_ROOT}/scripts/state-manager.sh get-phase discovery)
if [ "$discovery_status" = "completed" ]; then
  echo "FEATURE_MODE"
fi
```

### Present Context

First, show the user what exists:

```bash
# Count existing items
${CLAUDE_PLUGIN_ROOT}/scripts/doc-parser.sh count brs
${CLAUDE_PLUGIN_ROOT}/scripts/doc-parser.sh count features
${CLAUDE_PLUGIN_ROOT}/scripts/doc-parser.sh count frs
```

```
Existing project detected.

Current scope:
  - X business requirements (BR-001 to BR-XXX)
  - X features (F-001 to F-XXX)
  - X functional requirements (FR-001 to FR-XXX)

Adding new feature/initiative: "[user input]"

This will run a lighter discovery process to:
  1. Research how this fits the existing product
  2. Check for conflicts with current architecture
  3. Create new BRs and Features
  4. Update relevant documents
```

### Lightweight Discovery Workflow

#### Step 1: Context Analysis

Read existing documentation to understand current state:

```bash
# Read existing BRD
cat docs/01-business/BRD.md

# Read existing PRD
cat docs/02-product/PRD.md

# Read architecture if exists
cat docs/02-product/architecture/high-level-design.md 2>/dev/null

# Check existing personas
cat docs/02-product/user-personas.md
```

#### Step 2: Feature Research
**Invoke**: business-analyst agent with context

Prompt includes:
- The new feature/initiative description
- Summary of existing BRD (objectives, constraints)
- Instruction to ADD to existing docs, not replace

Agent will:
1. Research the new feature's business case
2. Check alignment with existing objectives
3. Identify new business requirements (BR-XXX)
4. **Append** to BRD.md (new section: "## Addition: [Feature Name]")

#### Step 3: Market Validation (Optional)
**Invoke**: market-analyst agent if needed

Only if the feature represents a new market direction:
- Quick competitive check
- Validation that feature aligns with market position

#### Step 4: User Impact Analysis
**Invoke**: user-researcher agent with context

Agent will:
1. Check which personas are affected
2. Update user journeys if needed
3. Identify new pain points addressed

#### Step 5: Product Integration
**Invoke**: product-manager agent with context

Agent will:
1. Create new features (F-XXX)
2. Determine priority relative to existing features
3. Check for conflicts/dependencies with existing features
4. **Append** to PRD.md

#### Step 6: Architecture Impact Check

```bash
# Check if architecture exists
if [ -f "docs/02-product/architecture/high-level-design.md" ]; then
  echo "CHECK_ARCHITECTURE"
fi
```

If architecture exists:
- Review high-level design
- Note any architectural changes needed
- Flag for design phase update

#### Step 7: Track New Requirements

```bash
# Get new BR and F IDs that were added
# Add them to state.requirements.unplanned[]
```

Update state file to track what's new and unplanned.

#### Step 8: Summary

```
Feature discovery complete!

Added to existing project:
  - X new business requirements (BR-XXX to BR-XXX)
  - X new features (F-XXX to F-XXX)

Updated documents:
  - docs/01-business/BRD.md (appended)
  - docs/02-product/PRD.md (appended)
  - [Other updated docs]

Impact assessment:
  - Personas affected: [list]
  - Architecture changes needed: [Yes/No]
  - Potential conflicts: [list or "None identified"]

New requirements pending planning:
  - [List of unplanned BR/F IDs]

Next steps:
  /peachflow:define    - Add detailed requirements for new features
  /peachflow:plan      - Incorporate into quarterly plan
```

---

## Document Update Patterns

### Appending to BRD.md

```markdown
---

## Feature Addition: [Feature Name]
*Added: [Date]*

### Business Case
[Why this feature]

### New Business Requirements
- **BR-015**: [New requirement]
- **BR-016**: [New requirement]

### Impact on Existing Requirements
- BR-003: [How it's affected, or "No change"]

### Constraints
[New constraints, or "Inherits existing constraints"]
```

### Appending to PRD.md

```markdown
---

## Feature Addition: [Feature Name]
*Added: [Date]*

### F-020: [Feature Name]
- **Description**: [What it does]
- **User Story**: As a [persona], I want to [action] so that [benefit]
- **Priority**: [Must/Should/Could]
- **Dependencies**: [Existing features it depends on]
- **Acceptance Criteria**:
  - [ ] [Criterion]

### Impact on Existing Features
- F-005: [Requires modification because...]
- F-008: [No change needed]
```

---

## State Management

### Tracking Planned vs Unplanned

The state file tracks requirements status:

```json
{
  "requirements": {
    "planned": ["BR-001", "BR-002", "F-001", "F-002"],
    "unplanned": ["BR-015", "BR-016", "F-020"]
  },
  "features": [
    {
      "id": "F-020",
      "name": "Feature Name",
      "addedAt": "2024-01-20",
      "discoveryType": "feature",
      "status": "unplanned"
    }
  ]
}
```

This allows `/peachflow:plan` to:
- Know what's new since last planning
- Incorporate new features into existing plans
- Identify potential migrations needed

---

## Guidelines

### For Full Discovery
- Don't over-research: Get key insights, then move on
- Bullet points over prose
- Each doc max 1-2 pages
- Mark unknowns with `[NEEDS CLARIFICATION: ...]`

### For Feature Discovery
- Review existing docs before adding
- Explicitly note conflicts/dependencies
- Keep additions clearly marked (dated sections)
- Consider impact on existing architecture
- Flag if new feature needs technical design review
