---
name: peachflow:implement
description: Execute implementation tasks from quarter plan. Works only on feature branches. Implements tasks sequentially with code review and commit checkpoints.
argument-hint: "[task ID: T001 | 'next' for next task | 'phase 1' for entire phase]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Task, AskUserQuestion
---

# /peachflow:implement - Implementation Phase

Execute tasks from the quarter's task breakdown with proper tagging, testing, and commit checkpoints.

## Automatic Continuation

**Proceed automatically to the next task without asking.** Do not prompt the user between tasks.

Only pause and ask the user in these situations:
1. **Phase completion** - Offer commit checkpoint
2. **Context window concern** - If the conversation is getting long and starting a new task risks filling the context
3. **Blocking error** - Task has unmet dependencies or critical failure
4. **Quarter complete** - All tasks done

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
│ 5. CRITICAL: Mark Complete in tasks.md  │
│    - Update Status: pending → complete  │
│    - Check all acceptance criteria [x]  │
│    - Update frontmatter: completed: N   │
│    - Output completion summary          │
└─────────────────────────────────────────┘
```

### Task Completion Requirement (CRITICAL)

**You MUST update tasks.md before proceeding to the next task.**

This is non-negotiable. After completing a task:

1. **Update task status** in tasks.md:
   ```markdown
   - **Status**: complete  ← Change from "pending" or "in_progress"
   ```

2. **Check all acceptance criteria**:
   ```markdown
   - **Acceptance**:
     - [x] Criterion 1  ← Mark with [x]
     - [x] Criterion 2
     - [x] Criterion 3
   ```

3. **Update frontmatter counter**:
   ```yaml
   completed: 3  ← Increment this number
   ```

**DO NOT proceed to the next task until tasks.md is updated.**

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

## Phase Completion (Pause Point)

**This is one of the few times to pause and ask the user.**

When a phase completes:

```
Phase 1 complete
      │
      ▼
┌─────────────────────────────────────────┐
│ Output commit checkpoint with:          │
│  - Summary of completed tasks           │
│  - Git commands for user to run         │
│  - Offer to continue or wait            │
└─────────────────────────────────────────┘
```

Example output:
```markdown
## Phase 1 Complete ✓

**Tasks**: T001, T002, T003 done
**Files**: 12 changed (+450, -23)

### Commit Commands
```bash
git add -A
git commit -m "feat(Q01): complete Phase 1 - Setup

- Initialize project structure
- Set up database schema
- Configure CI/CD

@peachflow: Q01/Phase1/T001-T003"
```

**Continue to Phase 2?** (or commit first)
```

---

## Commit Checkpoint

When a phase completes, prepare a commit message for the user to run manually.

**DO NOT execute git commands. Prepare the message for the user.**

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

---

### Git Commands to Run

```bash
# 1. Stage all changes
git add -A

# 2. Create commit with this message
git commit -m "feat(Q01): complete Phase 1 - Setup

- Initialize project with Vite + React + TypeScript
- Set up PostgreSQL database with Prisma
- Configure GitHub Actions CI/CD
- Add initial design tokens

@peachflow: Q01/Phase1/T001-T003"
```

**Please run the commands above when ready, then confirm to continue.**
```

---

## Task Completion Output

```markdown
## Task T003 Complete ✓

**Files Changed**:
- CREATE: src/api/auth/oauth-callback.ts
- CREATE: src/api/auth/__tests__/oauth-callback.test.ts
- MODIFY: src/api/auth/index.ts

**Acceptance**: All criteria met ✓
**Tests**: 6 passing ✓
**tasks.md**: Updated ✓

---

→ Continuing to T004: Create login UI component
```

**Note**: Output is concise. Automatically continue to next task without prompting.

---

## Context Window Management

If the conversation is getting long (many tasks completed), pause before starting a new task:

```markdown
## Context Check

Completed 5 tasks in this session. Starting T006 may exceed context limits.

**Options**:
1. Continue in new session: `/peachflow:implement T006`
2. Continue anyway (may truncate earlier context)
```

Signs to watch for:
- Completed 4+ medium/large tasks in one session
- Long code review discussions
- Many file reads/writes

When in doubt, offer to pause so user can start fresh session.

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
/peachflow:implement next
         │
         ▼
┌─────────────────────────────────┐
│  Task Loop (automatic):         │
│  Load → Implement → Cleanup →   │
│  Review → Update tasks.md →     │
│  Continue to next task          │
└─────────────────────────────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
[More      [Phase
tasks in    complete]
 phase]        │
    │          ▼
    │    Commit checkpoint
    │    (PAUSE & ask user)
    │          │
    ▼          ▼
 Continue   User commits,
 auto       then continue
```

**Summary**: Auto-continue within phase. Pause only at phase end or context limit.
