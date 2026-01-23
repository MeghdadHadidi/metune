---
name: clean-code
description: This skill should be used when writing code, implementing features, fixing bugs, refactoring, or generating any code output. Applies when the user asks to "implement", "create", "build", "write code", "add a feature", "fix a bug", "refactor", "update code", "modify", or "clean up code". Also applies when reviewing code for quality issues. Enforces type safety, clean imports, no redundancy, and code quality standards across TypeScript, Python, Go, and Rust.
---

# Clean Code Standards

Apply these standards when writing or modifying code. These rules enforce type safety, eliminate redundancy, and maintain code cleanliness across all programming languages.

## Core Principles

1. **Type Safety First** - No `any` types, explicit return types, proper null handling
2. **Clean Imports** - No unused imports, organized order, no circular dependencies
3. **No Redundancy** - No dead code, no duplicate logic, single responsibility
4. **Explicit Over Implicit** - Clear naming, obvious intent, self-documenting code

## Type Safety Rules

### No `any` Types

Never use `any`. Use proper alternatives:

| Instead of | Use |
|------------|-----|
| `any` | `unknown` (for truly unknown data) |
| `any[]` | `T[]` with generic or specific type |
| `Record<string, any>` | `Record<string, unknown>` or specific interface |
| `(...args: any[])` | Proper function signature |

```typescript
// BAD
function parse(data: any): any { ... }
const items: any[] = response.data;

// GOOD
function parse(data: unknown): ParsedResult { ... }
const items: Item[] = response.data;
```

### Explicit Return Types

Always declare return types for functions:

```typescript
// BAD
function getUser(id: string) {
  return db.users.find(id);
}

// GOOD
function getUser(id: string): Promise<User | null> {
  return db.users.find(id);
}
```

### Proper Null Handling

Use explicit null checks, not truthy/falsy:

```typescript
// BAD
if (user) { ... }
const name = user && user.name;

// GOOD
if (user !== null && user !== undefined) { ... }
const name = user?.name ?? 'Unknown';
```

### Type Narrowing

Use proper type guards and narrowing:

```typescript
// BAD
function handle(value: string | number) {
  return (value as string).toUpperCase();
}

// GOOD
function handle(value: string | number): string {
  if (typeof value === 'string') {
    return value.toUpperCase();
  }
  return value.toString();
}
```

## Import Standards

### No Unused Imports

Remove all imports that are not used in the file. Before finishing any file:

1. Check every import statement
2. Verify each imported symbol is actually used
3. Remove unused imports

### Import Organization

Organize imports in this order, with blank lines between groups:

```typescript
// 1. External packages (node_modules)
import React from 'react';
import { useQuery } from '@tanstack/react-query';

// 2. Internal absolute imports (aliases like @/)
import { Button } from '@/components/ui';
import { useAuth } from '@/hooks';

// 3. Relative imports (local files)
import { UserCard } from './UserCard';
import type { UserProps } from './types';
```

### No Circular Dependencies

Avoid files that import each other. Signs of circular dependencies:

- Runtime errors about undefined values
- Type-only imports working but value imports failing

Solutions:
- Extract shared code to a third file
- Use dependency injection
- Restructure module boundaries

## Code Cleanliness

### No Dead Code

Remove all:
- Commented-out code blocks
- Unreachable code after return/throw
- Unused variables and functions
- Empty blocks (catch, if, else)
- Console.log statements (except intentional logging)

```typescript
// BAD
function calculate(x: number): number {
  // const old = x * 2;
  const result = x * 3;
  return result;
  console.log('done'); // unreachable
}

// GOOD
function calculate(x: number): number {
  return x * 3;
}
```

### No Duplicate Logic

Extract repeated code into functions:

```typescript
// BAD
const userA = { ...data, createdAt: new Date(), updatedAt: new Date() };
const userB = { ...data, createdAt: new Date(), updatedAt: new Date() };

// GOOD
function withTimestamps<T>(data: T): T & { createdAt: Date; updatedAt: Date } {
  return { ...data, createdAt: new Date(), updatedAt: new Date() };
}
const userA = withTimestamps(dataA);
const userB = withTimestamps(dataB);
```

### Single Responsibility

Each function should do one thing:

```typescript
// BAD
function processUser(user: User): void {
  validateUser(user);
  saveToDatabase(user);
  sendEmail(user);
  logActivity(user);
}

// GOOD
function createUser(user: User): Promise<User> {
  const validated = validateUser(user);
  return saveToDatabase(validated);
}
// Call sendEmail and logActivity separately or in orchestrating function
```

## Pre-Completion Checklist

Before finishing any code task, verify:

- [ ] No `any` types anywhere
- [ ] All functions have explicit return types
- [ ] No unused imports
- [ ] Imports are organized (external → internal → relative)
- [ ] No commented-out code
- [ ] No console.log (except intentional)
- [ ] No unreachable code
- [ ] No duplicate logic
- [ ] Proper null/undefined handling
- [ ] Types match API contracts

## Language-Specific Guidelines

### TypeScript/JavaScript

See `references/typescript.md` for detailed TypeScript patterns including:
- Strict mode configuration
- Generic patterns
- Utility types
- Error handling patterns

### Python

See `references/python.md` for Python-specific guidelines including:
- Type hints (PEP 484)
- Import organization (isort style)
- No unused variables (ruff/flake8)

### Go

See `references/go.md` for Go-specific guidelines including:
- Error handling patterns
- Interface design
- No unused imports (go vet)

### Rust

See `references/rust.md` for Rust-specific guidelines including:
- Ownership patterns
- Error handling with Result
- Unused code warnings

## Quick Reference Table

| Issue | Detection | Fix |
|-------|-----------|-----|
| `any` type | Search for `: any` | Replace with specific type or `unknown` |
| Missing return type | Function without `: ReturnType` | Add explicit return type |
| Unused import | Greyed out in IDE, lint error | Delete the import |
| Dead code | After return/throw | Remove unreachable code |
| Duplicate logic | Similar code blocks | Extract to function |
| Type assertion | `as Type` | Use type guard instead |

## Applying These Standards

This skill applies automatically during any code generation or modification task, including:

- Implementing new features or tasks
- Creating UI components or API endpoints
- Fixing bugs or refactoring existing code
- Code review and quality assessment

Follow these standards alongside any other project-specific guidelines (tagging, testing, etc.).
