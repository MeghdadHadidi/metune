---
name: workflow-gates
description: |
  This skill provides workflow gate validation patterns for peachflow commands. Use when implementing clarification gates in commands, checking prerequisites before phase transitions, or validating document completeness. Applies automatically during plan and implement commands.
---

# Workflow Gates

Peachflow enforces gates between workflow phases to ensure quality and completeness before progressing.

## Gate Philosophy

**No phase can proceed if the previous phase has unresolved questions.**

This prevents:
- Building on incomplete foundations
- Wasting effort on wrong assumptions
- Late-stage rework from early ambiguity

---

## Clarification Gate

### What It Checks

The clarification gate scans for `[NEEDS CLARIFICATION]` markers in relevant documents.

### Gate Locations

| Transition | Gate Location | Documents Checked |
|------------|---------------|-------------------|
| discover → plan | Before planning | `specs/discovery/*.md` |
| plan → implement | Before implementation | `specs/discovery/*.md` + `specs/quarterly/Q{XX}/*.md` |

### Implementation Pattern

```bash
# Clarification gate check
check_clarification_gate() {
  local docs_path="$1"
  local count=$(grep -rn "NEEDS CLARIFICATION" "$docs_path" 2>/dev/null | wc -l | tr -d ' ')

  if [ "$count" -gt 0 ]; then
    echo "BLOCKED"
    return 1
  else
    echo "PASSED"
    return 0
  fi
}

# Usage in commands
if [ "$(check_clarification_gate 'specs/discovery/')" = "BLOCKED" ]; then
  # Show blocking message
  # List unresolved items
  # Suggest running /peachflow:clarify
  exit 1
fi
```

### Blocking Output Format

When a gate blocks, output this format:

```markdown
## ⛔ {Phase} Blocked: Unresolved Clarifications

{Phase} cannot proceed until all `[NEEDS CLARIFICATION]` markers are resolved.

### Unresolved Items Found ({N} total)

| # | File | Line | Question |
|---|------|------|----------|
| 1 | {path} | {line} | {question text} |
| 2 | {path} | {line} | {question text} |

### How to Resolve

**Option 1: Interactive Clarification**
```
/peachflow:clarify
```

**Option 2: Manual Resolution**
Edit the files directly to replace `[NEEDS CLARIFICATION: question]` with your decision.

### After Resolution

Run `/{command}` again once all items are resolved.
```

### Success Output Format

When gate passes:

```markdown
✅ Clarification gate passed
- Documents scanned: {N} files
- Unresolved items: 0
- Proceeding to {phase}...
```

---

## Prerequisite Gates

### Discovery Prerequisites

Before `/peachflow:discover`:
- Either a product description argument provided
- OR `specs/discovery/analyze-report.md` exists
- If neither, block and explain options

### Plan Prerequisites

Before `/peachflow:plan`:
- `specs/discovery/prd.md` exists
- `specs/discovery/architecture.md` exists
- Clarification gate passes on discovery docs

### Plan Q{XX} Prerequisites

Before `/peachflow:plan Q1`:
- `specs/quarterly/roadmap.md` exists
- `specs/quarterly/Q{XX}-overview.md` exists
- Clarification gate passes

### Implement Prerequisites

Before `/peachflow:implement`:
- On a feature branch (pattern: `NNN-QXX-*`)
- `specs/quarterly/Q{XX}/tasks.md` exists
- Clarification gate passes on discovery + planning docs

---

## Gate Checking Patterns

### Comprehensive Check Function

```bash
# Full prerequisite and clarification check
check_workflow_gates() {
  local phase="$1"
  local quarter="$2"

  case "$phase" in
    "discover")
      # Check for input
      if [ -z "$PRODUCT_DESCRIPTION" ] && [ ! -f "specs/discovery/analyze-report.md" ]; then
        echo "BLOCKED: No input provided"
        return 1
      fi
      ;;

    "plan")
      # Check discovery complete
      if [ ! -f "specs/discovery/prd.md" ]; then
        echo "BLOCKED: Discovery not complete (missing prd.md)"
        return 1
      fi

      # Check clarification gate
      local count=$(grep -rn "NEEDS CLARIFICATION" specs/discovery/ 2>/dev/null | wc -l)
      if [ "$count" -gt 0 ]; then
        echo "BLOCKED: $count unresolved clarifications in discovery"
        return 1
      fi
      ;;

    "plan-quarter")
      # Check roadmap exists
      if [ ! -f "specs/quarterly/roadmap.md" ]; then
        echo "BLOCKED: Run /peachflow:plan first to create roadmap"
        return 1
      fi

      # Check overview exists
      if [ ! -f "specs/quarterly/${quarter}-overview.md" ]; then
        echo "BLOCKED: Quarter ${quarter} not in roadmap"
        return 1
      fi
      ;;

    "implement")
      # Check branch
      local branch=$(git branch --show-current 2>/dev/null)
      if ! echo "$branch" | grep -qE "^[0-9]{3}-Q[0-9]"; then
        echo "BLOCKED: Not on a feature branch"
        return 1
      fi

      # Extract quarter from branch
      local q=$(echo "$branch" | grep -oE "Q[0-9]{2}")

      # Check tasks exist
      if [ ! -f "specs/quarterly/${q}/tasks.md" ]; then
        echo "BLOCKED: No tasks.md for ${q}"
        return 1
      fi

      # Check clarification gate (both discovery and quarterly)
      local disc_count=$(grep -rn "NEEDS CLARIFICATION" specs/discovery/ 2>/dev/null | wc -l)
      local plan_count=$(grep -rn "NEEDS CLARIFICATION" specs/quarterly/${q}/ 2>/dev/null | wc -l)
      local total=$((disc_count + plan_count))

      if [ "$total" -gt 0 ]; then
        echo "BLOCKED: $total unresolved clarifications"
        return 1
      fi
      ;;
  esac

  echo "PASSED"
  return 0
}
```

---

## Marker Formats

### [NEEDS CLARIFICATION] Format

Used by discovery and planning agents when they can't determine an answer:

```markdown
[NEEDS CLARIFICATION: What is the expected user scale?
Options:
- <1K users (simple architecture)
- 1K-10K users (standard stack)
- 10K-100K users (scalable architecture)
- 100K+ users (distributed systems)
Context: This affects database choice, caching strategy, and hosting costs]
```

### [RESOLVED] Format

Used by clarification-agent after getting user input:

```markdown
**Expected User Scale**: 1K-10K users
- Selected: Standard PostgreSQL stack
- Rationale: Balances simplicity with room to grow
[RESOLVED: 2026-01-22 via clarification-agent]
```

### [DEFERRED] Format

Used when a decision is intentionally postponed:

```markdown
[DEFERRED: Mobile app architecture - will decide after web launch
Reason: Not enough information about mobile requirements yet
Revisit: Q3 planning phase]
```

### [KILL CHECK TRIGGERED] Format

Used when a critical issue is found:

```markdown
[KILL CHECK TRIGGERED: Market size below threshold
Finding: TAM is $5M, below $10M threshold
Recommendation: Reconsider market or pivot scope
Action Required: Stakeholder review before proceeding]
```

---

## Gate Bypass (Emergency Only)

In rare cases, gates can be bypassed with explicit acknowledgment:

```markdown
## ⚠️ Gate Bypass Requested

You've chosen to bypass the clarification gate with {N} unresolved items.

**Risks**:
- May build on incorrect assumptions
- May require rework later
- Quality may suffer

**To proceed anyway**, confirm:
```
/peachflow:implement --force T001
```

**Note**: Bypassed items will be flagged in the implementation for later review.
```

---

## Integration with Commands

Each command should:

1. **Check gates at start** - Before any work
2. **Show clear blocking message** - If gate fails
3. **Provide resolution path** - How to unblock
4. **Show success confirmation** - When gate passes

Example command integration:

```markdown
# In command instructions:

## Step 0: Gate Check (Required)

Before proceeding, verify all gates pass:

1. Run clarification gate check on relevant docs
2. If BLOCKED: Output blocking message with unresolved items
3. If PASSED: Output confirmation and proceed

DO NOT skip this step. Gates exist to prevent building on shaky foundations.
```
