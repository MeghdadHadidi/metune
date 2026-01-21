---
name: peachflow:clarify
description: Manually trigger clarification questions on current documents. Scans for NEEDS CLARIFICATION markers and asks targeted questions.
argument-hint: "[optional: specific document or phase to clarify]"
allowed-tools: Read, Write, Edit, Grep, Glob, AskUserQuestion
---

# /peachflow:clarify - Manual Clarification

Manually trigger clarification questions on project documents. Useful when:
- You want to resolve pending questions before proceeding
- New information is available that affects existing documents
- You skipped clarification during a phase

## When to Use

- After receiving stakeholder feedback
- Before starting implementation
- When requirements change
- To resolve accumulated `[NEEDS CLARIFICATION]` markers

---

## Workflow

### Step 1: Scan Documents
**Auto-invoke**: clarification-agent

```bash
# Find all clarification markers
grep -rn "NEEDS CLARIFICATION\|TBD\|TODO\|UNCLEAR\|ASSUMPTION" specs/
```

### Step 2: Categorize Issues

Group by urgency:
- **Blocking**: Can't proceed without answer
- **Important**: Affects major decisions
- **Nice-to-have**: Refines details

### Step 3: Ask Questions

Use AskUserQuestion with structured options (max 5 per round):

```json
{
  "questions": [
    {
      "question": "Who is the primary target user for this product?",
      "header": "Target User",
      "options": [
        {"label": "B2B Enterprise", "description": "Large companies, procurement process"},
        {"label": "B2B SMB", "description": "Small businesses, owner-led decisions"},
        {"label": "B2C Consumer", "description": "Individual users, price-conscious"},
        {"label": "B2C Prosumer", "description": "Power users, premium features"}
      ],
      "multiSelect": false
    }
  ]
}
```

### Step 4: Update Documents

Replace markers with answers:

**Before:**
```markdown
### Target Audience
[NEEDS CLARIFICATION: Who is the primary user?]
```

**After:**
```markdown
### Target Audience
**Primary**: B2B Enterprise users (large companies with 500+ employees)
- Procurement-driven purchasing
- Multiple stakeholder approval required
- Value reliability over cost
[RESOLVED: 2026-01-20]
```

### Step 5: Generate Summary

```markdown
## Clarification Summary

**Session**: Manual clarification
**Date**: 2026-01-20

### Resolved This Session
| Item | Question | Answer | Impact |
|------|----------|--------|--------|
| PRD-001 | Target audience | B2B Enterprise | Affects pricing, features |
| PRD-002 | Monetization | SaaS subscription | Affects architecture |

### Still Pending
| Item | Question | Blocking? | Owner |
|------|----------|-----------|-------|
| ARCH-001 | Scale expectations | Yes | Product |

### Documents Updated
- specs/discovery/prd.md (2 items resolved)
- specs/discovery/architecture.md (1 item resolved)

### Next Steps
1. Resolve blocking items before /peachflow:plan
2. Re-run /peachflow:clarify after stakeholder meeting
```

---

## Input Examples

```bash
# Clarify all documents
/peachflow:clarify

# Clarify specific phase
/peachflow:clarify discovery
/peachflow:clarify "quarterly plan"

# Clarify specific document
/peachflow:clarify specs/discovery/prd.md
```

---

## Clarification Markers

### Standard Markers

| Marker | Meaning | Usage |
|--------|---------|-------|
| `[NEEDS CLARIFICATION: question]` | Unresolved question | Most common |
| `[ASSUMPTION: statement]` | Implicit assumption to validate | Risky assumptions |
| `[TBD]` | To be determined | Placeholder |
| `[TODO]` | Action needed | Tasks |
| `[UNCLEAR: description]` | Ambiguous requirement | Vague specs |

### Resolution Markers

| Marker | Meaning |
|--------|---------|
| `[RESOLVED: date]` | Question answered |
| `[DEFERRED: reason]` | Intentionally postponed |
| `[REJECTED: reason]` | Not applicable |

---

## Question Formulation Rules

1. **Be Specific**: Not "What's the target audience?" but "Is the primary user a B2B enterprise buyer or B2C consumer?"

2. **Offer Options**: Provide 2-4 concrete choices when possible

3. **Explain Impact**: Why does this answer matter for the project?

4. **Prioritize**: Ask most critical (blocking) questions first

5. **Limit Scope**: Max 5 questions per clarification round

---

## Integration Points

### Auto-invoked after:
- `/peachflow:discover` completion
- `/peachflow:plan` completion
- `/peachflow:plan Q1` completion

### Manual invocation:
- `/peachflow:clarify` - anytime

---

## Collaboration Flow

```
/peachflow:clarify
      │
      ▼
┌─────────────────────────────────┐
│     Scan Documents              │
│     Find all markers            │
└─────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────┐
│     Categorize & Prioritize     │
│     clarification-agent         │
└─────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────┐
│     Ask Questions               │
│     (max 5 per round)           │
└─────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────┐
│     Update Documents            │
│     Mark as resolved            │
└─────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────┐
│     Generate Summary            │
│     document-manager            │
└─────────────────────────────────┘
      │
      ▼
[Clarification Complete]
```

---

## Notes

- Clarification is **always safe** - it only updates existing documents
- Multiple rounds may be needed for complex projects
- Blocking items should be resolved before proceeding to next phase
- Keep clarification summaries for project history
