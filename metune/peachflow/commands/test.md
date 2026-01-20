---
name: test
description: Run tests, analyze coverage, and suggest cleanup. Optional phase that can be run anytime during implementation.
argument-hint: "[optional: 'all' | 'unit' | 'integration' | 'e2e' | specific test file]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Task, AskUserQuestion
---

# /peachflow:test - Testing Phase (Optional)

Run tests, analyze results, and suggest cleanup improvements.

## Prerequisites

- Implementation in progress or complete
- Test framework configured
- On a feature branch (recommended)

---

## Workflow

### Test Execution

```
/peachflow:test              # Run all tests
/peachflow:test unit         # Run unit tests only
/peachflow:test integration  # Run integration tests
/peachflow:test e2e          # Run end-to-end tests
/peachflow:test src/auth     # Run tests for specific path
```

### Per-Run Flow

```
┌─────────────────────────────────────────┐
│ 1. Detect Test Framework                │
│    - Jest, Vitest, Playwright, etc.     │
│    - Read package.json scripts          │
└─────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│ 2. Run Tests                            │
│    - Execute appropriate test command   │
│    - Capture output and results         │
└─────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│ 3. Analyze Results                      │
│    - Parse test output                  │
│    - Identify failures                  │
│    - Check coverage thresholds          │
└─────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│ 4. Generate Report                      │
│    - Summary statistics                 │
│    - Failed test details                │
│    - Coverage gaps                      │
└─────────────────────────────────────────┘
              │
              ▼
┌─────────────────────────────────────────┐
│ 5. Suggest Improvements                 │
│    - Missing test coverage              │
│    - Cleanup opportunities              │
│    - Performance issues                 │
└─────────────────────────────────────────┘
```

---

## Test Report Format

```markdown
## Test Report

**Run**: 2026-01-20 15:30:00
**Branch**: 001-Q01-exam-platform
**Quarter**: Q01

### Summary

| Type | Total | Passed | Failed | Skipped |
|------|-------|--------|--------|---------|
| Unit | 45 | 43 | 2 | 0 |
| Integration | 12 | 12 | 0 | 0 |
| E2E | 8 | 7 | 1 | 0 |
| **Total** | **65** | **62** | **3** | **0** |

### Coverage

| Metric | Current | Target | Status |
|--------|---------|--------|--------|
| Statements | 78% | 80% | ⚠️ |
| Branches | 65% | 70% | ❌ |
| Functions | 82% | 80% | ✅ |
| Lines | 79% | 80% | ⚠️ |

### Failed Tests

#### 1. `auth.test.ts` - validateToken
**Error**: Expected token to be valid but got invalid
**File**: src/api/auth/__tests__/auth.test.ts:45
**Likely Cause**: Token expiry logic not handling edge case

#### 2. `login.e2e.ts` - should redirect after login
**Error**: Timeout waiting for navigation
**File**: e2e/login.e2e.ts:23
**Likely Cause**: Async state update delay

### Coverage Gaps

Files with low coverage:
- `src/api/auth/oauth-callback.ts` - 45% (needs error path tests)
- `src/components/Dashboard.tsx` - 52% (missing edge cases)

### Cleanup Suggestions

**Auto-invoke**: qa-engineer agent

1. **Remove dead code**
   - `src/utils/deprecated.ts` - unused file
   - `src/api/auth/old-handler.ts` - commented out code

2. **Fix lint warnings**
   - 3 unused imports
   - 2 any types that could be typed

3. **Performance concerns**
   - `src/components/List.tsx` - missing memo
   - `src/hooks/useData.ts` - unnecessary re-renders

---

### Recommended Actions

1. [ ] Fix 2 failing unit tests
2. [ ] Fix 1 failing E2E test
3. [ ] Add tests to reach 80% coverage
4. [ ] Run cleanup suggestions

Would you like me to:
1. Fix the failing tests
2. Add missing test coverage
3. Run cleanup
4. All of the above
```

---

## Cleanup Mode

When cleanup is requested:

**Auto-invoke**: qa-engineer agent

```markdown
## Cleanup Report

### Removed
- [ ] 3 unused imports
- [ ] 1 deprecated file
- [ ] 12 console.log statements
- [ ] 45 lines of commented code

### Fixed
- [ ] 2 `any` types replaced with proper types
- [ ] 1 missing error boundary
- [ ] 3 lint warnings

### Formatted
- [ ] 8 files reformatted with Prettier

### No Changes Needed
- ESLint rules passing
- No security vulnerabilities
- Dependencies up to date
```

---

## Integration with Implementation

After `/peachflow:implement` completes a task or phase:

```
Task T003 complete
         │
         ▼
┌─────────────────────────────────┐
│ Suggest: Run tests?             │
│                                 │
│ 1. Yes, run related tests       │
│ 2. Yes, run all tests           │
│ 3. No, continue to next task    │
└─────────────────────────────────┘
```

---

## Collaboration Flow

```
/peachflow:test
      │
      ▼
┌─────────────────────────────────┐
│     Detect & Run Tests          │
│     developer (sonnet)          │
└─────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────┐
│     Analyze Results             │
│     qa-engineer (sonnet)        │
└─────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────┐
│     Generate Report             │
│     document-manager (haiku)    │
└─────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────┐
│     Suggest Improvements        │
│     code-reviewer (opus)        │
└─────────────────────────────────┘
      │
      ▼
[Report Ready → Fix or Continue]
```

---

## Notes

- Testing is **optional** but recommended after each phase
- Cleanup is non-destructive - always shows changes before applying
- Coverage targets are configurable in project settings
- Failed tests block commit unless explicitly skipped
