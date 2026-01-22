---
name: peachflow:discovery-checklist
description: Validate that all strategic questions in discovery documents have been answered. Scans for incomplete checklist items and unanswered questions, reporting readiness for planning phase.
argument-hint: "[--fix to prompt for missing answers]"
allowed-tools: Read, Write, Edit, Grep, Glob, AskUserQuestion
---

# /peachflow:discovery-checklist - Discovery Validation

Validates that all strategic questions across discovery documents have been answered, ensuring the project is ready for planning.

## Overview

This command scans all discovery documents for:
1. **Strategic Question Checklists** - Tables with empty "Answer" columns
2. **Kill-the-Project Checks** - Unchecked critical validation items
3. **NEEDS CLARIFICATION markers** - Unresolved questions in document body
4. **Confidence Gaps** - Questions answered with low confidence

## Validation Process

### Step 1: Scan Discovery Documents

Read all files in `specs/discovery/`:
- `domain-research.md`
- `prd.md`
- `user-personas.md`
- `user-journeys.md`
- `design-vision.md`
- `architecture.md`

### Step 2: Extract Strategic Questions

For each document, find the "Strategic Questions Checklist" section and check:
- Tables with `| Question | Answer |` headers
- Look for empty cells in the "Answer" column
- Note confidence levels (if present)

### Step 3: Check Kill-the-Project Items

Look for sections titled "Kill-the-Project Check" and verify:
- All checkbox items `- [ ]` are evaluated
- No critical items are checked (if checked, project should stop)

### Step 4: Count NEEDS CLARIFICATION

Use grep to find all instances of `[NEEDS CLARIFICATION:` and count unresolved items.

### Step 5: Generate Report

## Report Format

Output a validation report in this format:

```markdown
# Discovery Validation Report

**Generated**: {timestamp}
**Status**: {READY | NEEDS ATTENTION | BLOCKED}

## Summary

| Document | Strategic Questions | Answered | Kill Checks | Clarifications Needed |
|----------|---------------------|----------|-------------|----------------------|
| domain-research.md | 12 | 10 | 0/4 triggered | 2 |
| prd.md | 15 | 15 | 0/4 triggered | 0 |
| ... | ... | ... | ... | ... |

## Unanswered Strategic Questions

### domain-research.md
- [ ] What is the TAM, and what % is realistically capturable?
- [ ] Why hasn't this been solved already? What's changed?

### prd.md
(none)

...

## Kill-the-Project Alerts

**CRITICAL**: The following kill conditions may be triggered:

### domain-research.md
- [x] TAM < $10M or declining — **FLAGGED: Needs review**

## Unresolved Clarifications

| Document | Clarification Needed |
|----------|---------------------|
| prd.md | [NEEDS CLARIFICATION: monetization strategy] |
| architecture.md | [NEEDS CLARIFICATION: scale expectations] |

## Low Confidence Answers

Questions answered but marked with low confidence:

| Document | Question | Confidence |
|----------|----------|------------|
| user-personas.md | What job is the user hiring this product to do? | Low |

## Recommendations

1. **Immediate Action Required**:
   - Answer remaining {N} strategic questions
   - Resolve {N} clarification markers

2. **Before Planning**:
   - Review kill-check items flagged above
   - Increase confidence on low-confidence answers

## Readiness Assessment

| Criterion | Status | Threshold |
|-----------|--------|-----------|
| Strategic Questions Answered | {X}% | >90% required |
| Kill Checks Clear | {Y}/N | All must pass |
| Clarifications Resolved | {Z}% | >80% required |
| Confidence Level | {W}% high/medium | >70% required |

**Overall Status**: {READY FOR PLANNING | NEEDS {N} MORE ITEMS | BLOCKED BY KILL CHECK}
```

## Arguments

- `--fix`: Interactive mode - prompt user to answer missing questions
- `--strict`: Require 100% completion before marking ready
- `--report`: Generate report file at `specs/discovery/validation-report.md`

## Workflow

### Default Mode (validation only)

```
/peachflow:discovery-checklist
```

Outputs validation report to console. Does not modify files.

### Fix Mode (interactive)

```
/peachflow:discovery-checklist --fix
```

1. Scans for incomplete items
2. For each missing answer, uses AskUserQuestion to prompt
3. Updates the source document with the answer
4. Re-validates and generates final report

### Strict Mode

```
/peachflow:discovery-checklist --strict
```

Returns BLOCKED unless 100% of strategic questions are answered and all clarifications resolved.

## Integration with /peachflow:plan

Before running `/peachflow:plan`, this checklist should be run to ensure:
- All strategic questions have answers
- No kill-check conditions are triggered
- Critical clarifications are resolved

The planning phase will reference these strategic answers to make informed decisions.

## Cross-Document Validation

Some questions span multiple documents. Validate consistency:

| Cross-Check | Documents | What to Verify |
|-------------|-----------|----------------|
| User definition | personas + prd | Primary user matches |
| Problem statement | prd + domain | Problem validated by market |
| Scale expectations | architecture + prd | Technical matches business |
| Design emotions | design-vision + personas | Emotions match user needs |
| Competitive position | domain + prd | Differentiation is real |

## Example Output

```
Discovery Validation Report
===========================

Status: NEEDS ATTENTION

Summary:
- 48 strategic questions across 6 documents
- 41 answered (85%)
- 0 kill-checks triggered
- 3 clarifications pending

Unanswered Questions (7):
1. [domain-research] Why hasn't this been solved already?
2. [prd] What assumption, if wrong, invalidates the product?
3. [user-personas] What moment of frustration triggers switching?
4. [user-journeys] What's the aha moment?
5. [design-vision] What visual element makes this recognizable?
6. [architecture] What's the cost of premature optimization?
7. [architecture] Who maintains this at 3am?

Recommendation: Answer remaining questions before planning.
Run /peachflow:discovery-checklist --fix for interactive completion.
```

## Notes

- Run this after `/peachflow:discover` completes
- Run before `/peachflow:plan` to validate readiness
- Strategic questions guide the planning phase decisions
- Kill-checks prevent investing in unviable products
