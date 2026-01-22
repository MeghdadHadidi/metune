# TypeScript Clean Code Patterns

Detailed TypeScript-specific patterns for clean, type-safe code.

## Strict Mode Configuration

Always enable strict mode in `tsconfig.json`:

```json
{
  "compilerOptions": {
    "strict": true,
    "noImplicitAny": true,
    "strictNullChecks": true,
    "noUnusedLocals": true,
    "noUnusedParameters": true,
    "noImplicitReturns": true,
    "noFallthroughCasesInSwitch": true,
    "exactOptionalPropertyTypes": true
  }
}
```

## Replacing `any` Types

### Unknown Data from APIs

```typescript
// BAD
async function fetchData(): Promise<any> {
  const response = await fetch('/api/data');
  return response.json();
}

// GOOD
interface ApiResponse<T> {
  data: T;
  status: number;
  message: string;
}

async function fetchData<T>(): Promise<ApiResponse<T>> {
  const response = await fetch('/api/data');
  return response.json() as ApiResponse<T>;
}

// Usage with specific type
const users = await fetchData<User[]>();
```

### Dynamic Object Keys

```typescript
// BAD
const config: Record<string, any> = {};

// GOOD - when values are truly unknown
const config: Record<string, unknown> = {};

// BETTER - when structure is known
interface Config {
  apiUrl: string;
  timeout: number;
  features: Record<string, boolean>;
}
const config: Config = { ... };
```

### Event Handlers

```typescript
// BAD
function handleEvent(event: any): void {
  console.log(event.target.value);
}

// GOOD
function handleEvent(event: React.ChangeEvent<HTMLInputElement>): void {
  console.log(event.target.value);
}
```

### Third-Party Libraries Without Types

```typescript
// BAD
import legacyLib from 'legacy-lib';
const result: any = legacyLib.process(data);

// GOOD - create minimal types
declare module 'legacy-lib' {
  interface ProcessResult {
    success: boolean;
    output: string;
  }
  export function process(data: unknown): ProcessResult;
}

import legacyLib from 'legacy-lib';
const result = legacyLib.process(data); // ProcessResult
```

## Generic Patterns

### Generic Functions

```typescript
// BAD - loses type information
function first(arr: unknown[]): unknown {
  return arr[0];
}

// GOOD - preserves type
function first<T>(arr: T[]): T | undefined {
  return arr[0];
}

const num = first([1, 2, 3]); // number | undefined
const str = first(['a', 'b']); // string | undefined
```

### Generic Constraints

```typescript
// BAD - too permissive
function getId<T>(obj: T): string {
  return (obj as any).id;
}

// GOOD - constrained
function getId<T extends { id: string }>(obj: T): string {
  return obj.id;
}
```

### Generic Factories

```typescript
// BAD
function createStore(initialState: any): any {
  let state = initialState;
  return {
    get: () => state,
    set: (newState: any) => { state = newState; }
  };
}

// GOOD
interface Store<T> {
  get: () => T;
  set: (newState: T) => void;
}

function createStore<T>(initialState: T): Store<T> {
  let state = initialState;
  return {
    get: () => state,
    set: (newState: T) => { state = newState; }
  };
}

const userStore = createStore<User>({ id: '1', name: 'John' });
```

## Utility Types

Use built-in utility types instead of manual typing:

```typescript
// Partial - all properties optional
type UpdateUser = Partial<User>;

// Required - all properties required
type CompleteUser = Required<User>;

// Pick - select specific properties
type UserCredentials = Pick<User, 'email' | 'password'>;

// Omit - exclude specific properties
type PublicUser = Omit<User, 'password' | 'ssn'>;

// Record - typed object
type UserRoles = Record<string, 'admin' | 'user' | 'guest'>;

// ReturnType - extract function return type
type FetchResult = ReturnType<typeof fetchUsers>;

// Parameters - extract function parameters
type FetchParams = Parameters<typeof fetchUsers>;
```

## Type Guards

### Custom Type Guards

```typescript
interface Dog {
  bark: () => void;
}

interface Cat {
  meow: () => void;
}

// Type guard function
function isDog(pet: Dog | Cat): pet is Dog {
  return 'bark' in pet;
}

function handlePet(pet: Dog | Cat): void {
  if (isDog(pet)) {
    pet.bark(); // TypeScript knows pet is Dog
  } else {
    pet.meow(); // TypeScript knows pet is Cat
  }
}
```

### Discriminated Unions

```typescript
// BAD - hard to narrow
interface Result {
  success: boolean;
  data?: unknown;
  error?: string;
}

// GOOD - discriminated union
type Result<T> =
  | { success: true; data: T }
  | { success: false; error: string };

function handleResult<T>(result: Result<T>): T | null {
  if (result.success) {
    return result.data; // TypeScript knows data exists
  }
  console.error(result.error); // TypeScript knows error exists
  return null;
}
```

## Error Handling Patterns

### Typed Errors

```typescript
// BAD
throw new Error('User not found');

// GOOD
class NotFoundError extends Error {
  constructor(
    public readonly resource: string,
    public readonly id: string
  ) {
    super(`${resource} with id ${id} not found`);
    this.name = 'NotFoundError';
  }
}

class ValidationError extends Error {
  constructor(
    public readonly field: string,
    public readonly message: string
  ) {
    super(`Validation failed for ${field}: ${message}`);
    this.name = 'ValidationError';
  }
}

// Usage
throw new NotFoundError('User', userId);
```

### Error Handling with Type Narrowing

```typescript
try {
  await createUser(data);
} catch (error) {
  // BAD
  console.error((error as any).message);

  // GOOD
  if (error instanceof ValidationError) {
    return { field: error.field, message: error.message };
  }
  if (error instanceof NotFoundError) {
    return { error: `${error.resource} not found` };
  }
  // Re-throw unknown errors
  throw error;
}
```

## Async Patterns

### Typed Promises

```typescript
// BAD
async function fetchUser(id: string) {
  const res = await fetch(`/users/${id}`);
  return res.json();
}

// GOOD
async function fetchUser(id: string): Promise<User | null> {
  const res = await fetch(`/users/${id}`);
  if (!res.ok) return null;
  return res.json() as Promise<User>;
}
```

### Promise.all with Types

```typescript
// Types preserved
const [users, posts] = await Promise.all([
  fetchUsers(),  // Promise<User[]>
  fetchPosts(),  // Promise<Post[]>
]);
// users: User[], posts: Post[]
```

## Import Best Practices

### Type-Only Imports

```typescript
// When importing only types
import type { User, Post } from './types';

// Mixed imports
import { fetchUser } from './api';
import type { User } from './types';
```

### Barrel Exports

```typescript
// components/index.ts
export { Button } from './Button';
export { Input } from './Input';
export type { ButtonProps } from './Button';
export type { InputProps } from './Input';

// Usage
import { Button, Input } from '@/components';
import type { ButtonProps } from '@/components';
```

## Common Anti-Patterns to Avoid

### Type Assertions

```typescript
// BAD - bypasses type checking
const user = response.data as User;

// GOOD - validate at runtime
function isUser(data: unknown): data is User {
  return (
    typeof data === 'object' &&
    data !== null &&
    'id' in data &&
    'name' in data
  );
}

const data = response.data;
if (!isUser(data)) {
  throw new Error('Invalid user data');
}
// data is now User
```

### Non-Null Assertion

```typescript
// BAD - can cause runtime errors
const name = user!.name;

// GOOD - handle null explicitly
const name = user?.name ?? 'Unknown';

// OR throw if null is unexpected
if (!user) {
  throw new Error('User is required');
}
const name = user.name;
```

### Index Signatures

```typescript
// BAD - allows any property
interface Config {
  [key: string]: any;
}

// GOOD - explicit properties with optional catch-all
interface Config {
  apiUrl: string;
  timeout: number;
  [key: string]: unknown; // still typed as unknown
}
```
