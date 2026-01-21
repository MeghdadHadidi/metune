---
name: peachflow:implement
description: Execute implementation tasks from quarter plan. Works only on feature branches. Implements tasks sequentially with code review and commit checkpoints.
argument-hint: "[task ID: T001 | 'next' for next task | 'phase 1' for entire phase]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Task, AskUserQuestion
---

# /peachflow:implement - Implementation Phase

Execute tasks from the quarter's task breakdown with proper tagging, testing, and commit checkpoints.

## Prerequisites

- Must be on a feature branch (quarter worktree)
- `specs/quarterly/Q{XX}/tasks.md` exists
- Plan phase complete

## Verification

```bash
# Check we're on a feature branch
git branch --show-current | grep -q "^[0-9]\{3\}-Q[0-9]"
```

---

## Workflow

### Task Selection

```
/peachflow:implement T001       # Specific task
/peachflow:implement next       # Next pending task
/peachflow:implement "phase 1"  # All tasks in phase 1
```

### Per-Task Flow

```
┌─────────────────────────────────────────┐
│ 1. Load Task Specification              │
│    - Read from tasks.md                 │
│    - Check dependencies complete        │
│    - Review related specs               │
└─────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│ 2. Implementation                       │
│    - Create/modify files                │
│    - Follow coding standards            │
│    - Add proper tags                    │
│    - Write tests                        │
└─────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│ 3. Cleanup                              │
│    - Remove console.logs                │
│    - Remove commented code              │
│    - Run linter                         │
│    - Format code                        │
└─────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│ 4. Code Review                          │
│    - code-reviewer validates            │
│    - Fix any critical issues            │
└─────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│ 5. Mark Complete                        │
│    - Update tasks.md                    │
│    - Output completion summary          │
└─────────────────────────────────────────┘
```

### Parallel Task Handling

If tasks can run in parallel (no conflicts):
- Implement both sequentially
- But don't wait for commit until both complete

---

## Tagging Requirements

### File-Level Tags

Every new/modified file gets a header:

```typescript
/**
 * @peachflow Q01/E01/US001/T003
 * @description OAuth callback handler
 * @tags auth, oauth, google, api
 * @see specs/quarterly/Q01/tasks.md#T003
 */
```

### Code Block Tags

Significant sections get inline tags:

```typescript
// @peachflow:T003 - Token validation
function validateToken(token: string): TokenValidation {
  // ...
}

// @peachflow:T003 - Session creation
async function createSession(user: User): Promise<Session> {
  // ...
}
```

---

## Cleanup After Each Task

**Auto-invoke**: qa-engineer + developer agents

Checklist:
- [ ] No console.log (except intentional)
- [ ] No commented-out code
- [ ] No unused imports
- [ ] No TODO without ticket
- [ ] Linter passes
- [ ] Prettier formatted
- [ ] Types complete (no `any`)

---

## Phase Completion

When a phase completes:

```
/peachflow:implement completes Phase 1
              │
              ▼
┌─────────────────────────────────────────┐
│ Ask User:                               │
│                                         │
│ Phase 1 (Setup) complete.               │
│ 3 tasks done, all tests passing.        │
│                                         │
│ Would you like to:                      │
│ 1. Review changes and commit            │
│ 2. Continue to Phase 2                  │
│ 3. Run full test suite first            │
└─────────────────────────────────────────┘
```

---

## Commit Checkpoint

When user chooses to commit:

```markdown
## Commit Checkpoint: Phase {N}

**Tasks Completed**: T001, T002, T003
**Files Changed**: 12 files (+450, -23)

### Changes Summary
- Initialized project structure
- Set up database schema
- Configured CI/CD pipeline

### Test Status
- Unit: 15 passing
- Integration: 5 passing
- Coverage: 82%

### Suggested Commit Message:
```
feat(Q01): complete Phase 1 - Setup

- Initialize project with Vite + React + TypeScript
- Set up PostgreSQL database with Prisma
- Configure GitHub Actions CI/CD
- Add initial design tokens

@peachflow: Q01/Phase1/T001-T003
```

Proceed with commit? [Y/n]
```

---

## Task Completion Output

```markdown
## Task T003 Complete

**Status**: Done
**Time**: [Duration]

**Files Changed**:
- CREATE: src/api/auth/oauth-callback.ts
  @peachflow: Q01/E01/US001/T003
- CREATE: src/api/auth/__tests__/oauth-callback.test.ts
- MODIFY: src/api/auth/index.ts

**Acceptance Criteria**:
- [x] Handles Google OAuth callback
- [x] Validates state parameter
- [x] Creates user session
- [x] Error handling implemented

**Tests**: 6 passing, 0 failing
**Coverage**: 94% for new code

**Cleanup**:
- [x] No console.logs
- [x] Linter passing
- [x] Formatted

**Code Review**: Passed
- No critical issues
- 1 suggestion (optional)

**Tags Applied**:
- File: @peachflow Q01/E01/US001/T003
- Blocks: 2 tagged sections

---

**Next Task**: T004 - Create login UI component
**Run**: `/peachflow:implement next` or `/peachflow:implement T004`
```

---

## Error Handling

If implementation fails:

```markdown
## Task T003 Blocked

**Issue**: Cannot find dependency module

**Details**:
Task T003 depends on T002 (Create user model)
but T002 is not marked complete.

**Options**:
1. Complete T002 first: `/peachflow:implement T002`
2. Skip and continue: `/peachflow:implement T004`
3. Mark T002 as complete if done: [Edit tasks.md]
```

---

## Input Examples

```bash
# Implement specific task
/peachflow:implement T001

# Implement next available task
/peachflow:implement next

# Implement all tasks in a phase
/peachflow:implement "phase 1"
/peachflow:implement phase1

# Implement range
/peachflow:implement T001-T005

# Resume after pause
/peachflow:implement resume
```

---

## Collaboration Flow

```
/peachflow:implement T003
         │
         ▼
┌─────────────────────────────────┐
│     Load Task Spec              │
│     document-manager (haiku)    │
└─────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│     Implementation              │
│     developer (sonnet)          │
│   + frontend-engineer (opus)    │  ← for UI tasks
│   + backend-engineer (sonnet)   │  ← for API tasks
└─────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│     Cleanup                     │
│     qa-engineer (sonnet)        │
└─────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│     Code Review                 │
│     code-reviewer (opus)        │
└─────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────┐
│     Mark Complete               │
│     Update tasks.md             │
└─────────────────────────────────┘
         │
         ▼
[Task Complete → Next Task or Phase Checkpoint]
```
