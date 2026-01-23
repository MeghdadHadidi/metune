---
name: peachflow:clarify
description: Manually trigger clarification round. Scans all documents for [NEEDS CLARIFICATION] markers and interviews user.
argument-hint: ""
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Grep, Glob, AskUserQuestion, Bash
---

# /peachflow:clarify - Manual Clarification

Scan all project documents for unresolved questions and interview user to resolve them.

## Overview

This command can be run at any time to:
- Find all `[NEEDS CLARIFICATION]` markers
- Ask user targeted questions
- Update documents with answers
- Track progress in clarification.md

## Workflow

### 1. Scan Documents

Find all clarification markers:
```bash
grep -r "\[NEEDS CLARIFICATION" docs/ --include="*.md" 2>/dev/null || echo "No markers found"
```

### 2. Check Clarification Log

Read `/docs/clarification.md` if it exists:
- Check what's already resolved
- Identify pending items
- Avoid re-asking resolved questions

### 3. Invoke Clarification Agent
**Invoke**: clarification-agent

The agent will:
1. Parse all markers found
2. Categorize by priority (blocker, important, nice-to-have)
3. Formulate questions with options where possible
4. Ask user max 5 questions per round
5. Update documents with answers
6. Update clarification.md

### 4. Report Summary

Show:
- Questions resolved this round
- Questions still pending
- Recommendation for next steps

## Usage Examples

### Run after any phase
```
/peachflow:clarify
```

### Check what needs clarification without asking
First run grep directly:
```bash
grep -r "\[NEEDS CLARIFICATION" docs/ --include="*.md"
```

## Output

```
Clarification Summary
=====================

Resolved this round:
  [x] Target audience (BRD.md) - "Small business owners"
  [x] Compliance requirements (NFRs.md) - "GDPR + CCPA"

Still pending:
  [ ] Scale expectations (architecture.md) - blocking deployment planning
  [ ] Payment provider choice (FRD.md)

Recommendation:
  2 pending questions. Would you like to continue?
```

## Integration with Phases

Clarification is auto-invoked at the end of:
- `/peachflow:discover`
- `/peachflow:define`
- `/peachflow:design`
- `/peachflow:plan`

Use this command to run additional clarification rounds or check status.

## Guidelines

- Questions asked in batches of max 5
- Multi-choice when options are clear
- Free text always available
- All clarifications logged in clarification.md
- Documents updated inline when answers received
