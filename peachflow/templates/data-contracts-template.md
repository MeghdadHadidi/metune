---
product: {product-name}
quarter: Q{XX}
document: data-contracts
version: 1.0
status: draft | review | approved
created: {date}
updated: {date}
owner: tech-lead
---

# Data Contracts: Q{XX} - {Theme}

## Overview

This document defines the shared data structures between frontend and backend, serving as the source of truth for API communication.

**Reference Documents**:
- [Frontend Spec](./frontend-spec.md)
- [Backend Spec](./backend-spec.md)

---

## Type Definitions

### Base Types

```typescript
// Timestamps
type ISODateTime = string; // ISO 8601 format: "2024-01-15T10:30:00Z"

// Identifiers
type UUID = string;

// Pagination
interface PaginationMeta {
  total: number;
  page: number;
  limit: number;
  totalPages: number;
}

interface PaginatedResponse<T> {
  data: T[];
  meta: PaginationMeta;
}

// Errors
interface ApiError {
  code: string;
  message: string;
  details?: Record<string, string[]>;
}

interface ErrorResponse {
  error: ApiError;
}
```

---

### User Types
[TAGS: Q{XX}, types, user]

```typescript
// Core user type
interface User {
  id: UUID;
  email: string;
  name: string;
  avatarUrl: string | null;
  emailVerifiedAt: ISODateTime | null;
  createdAt: ISODateTime;
  updatedAt: ISODateTime;
}

// User for public display (limited info)
interface PublicUser {
  id: UUID;
  name: string;
  avatarUrl: string | null;
}

// User preferences (internal)
interface UserPreferences {
  theme: 'light' | 'dark' | 'system';
  notifications: {
    email: boolean;
    push: boolean;
  };
  locale: string;
}
```

---

### Authentication Types
[TAGS: Q{XX}, types, auth]

```typescript
// Tokens
interface Tokens {
  accessToken: string;
  refreshToken: string;
  expiresIn: number; // seconds until expiry
}

// Login
interface LoginRequest {
  email: string;
  password: string;
}

interface LoginResponse {
  user: User;
  tokens: Tokens;
}

// Register
interface RegisterRequest {
  email: string;
  password: string;
  name: string;
}

interface RegisterResponse {
  user: User;
  tokens: Tokens;
}

// Password Reset
interface ForgotPasswordRequest {
  email: string;
}

interface ResetPasswordRequest {
  token: string;
  password: string;
}
```

---

### {Resource} Types
[TAGS: Q{XX}, types, {resource}]

```typescript
// Base entity
interface {Resource} {
  id: UUID;
  name: string;
  description: string | null;
  status: {Resource}Status;
  createdAt: ISODateTime;
  updatedAt: ISODateTime;
}

// Status enum
type {Resource}Status = 'draft' | 'active' | 'archived';

// Extended with relations
interface {Resource}Detail extends {Resource} {
  user: PublicUser;
  {relations}: {Relation}[];
  stats: {Resource}Stats;
}

// Stats for dashboard/summary
interface {Resource}Stats {
  totalCount: number;
  activeCount: number;
  {metric}: number;
}

// Create request
interface Create{Resource}Request {
  name: string;
  description?: string;
}

// Update request (all optional)
interface Update{Resource}Request {
  name?: string;
  description?: string;
  status?: {Resource}Status;
}

// List filters
interface {Resource}ListParams {
  page?: number;
  limit?: number;
  search?: string;
  status?: {Resource}Status;
  sort?: string;
}

// List response
type {Resource}ListResponse = PaginatedResponse<{Resource}>;
```

---

### {Relation} Types
[TAGS: Q{XX}, types, {relation}]

```typescript
interface {Relation} {
  id: UUID;
  {resource}Id: UUID;
  {field}: string;
  createdAt: ISODateTime;
  updatedAt: ISODateTime;
}

interface Create{Relation}Request {
  {field}: string;
}

interface Update{Relation}Request {
  {field}?: string;
}
```

---

## API Contracts

### Authentication

#### POST /api/v1/auth/register
```typescript
// Request
type RequestBody = RegisterRequest;

// Response 201
type ResponseBody = RegisterResponse;

// Errors
type Errors =
  | { code: 'EMAIL_EXISTS'; message: 'Email already registered' }
  | { code: 'VALIDATION_ERROR'; message: string; details: Record<string, string[]> };
```

#### POST /api/v1/auth/login
```typescript
// Request
type RequestBody = LoginRequest;

// Response 200
type ResponseBody = LoginResponse;

// Errors
type Errors =
  | { code: 'INVALID_CREDENTIALS'; message: 'Invalid email or password' }
  | { code: 'ACCOUNT_LOCKED'; message: 'Account temporarily locked' };
```

---

### {Resource} CRUD

#### GET /api/v1/{resource}
```typescript
// Request (query params)
type QueryParams = {Resource}ListParams;

// Response 200
type ResponseBody = {Resource}ListResponse;

// Headers
// Authorization: Bearer {accessToken}
```

#### POST /api/v1/{resource}
```typescript
// Request
type RequestBody = Create{Resource}Request;

// Response 201
type ResponseBody = {Resource};

// Errors
type Errors =
  | { code: 'VALIDATION_ERROR'; message: string }
  | { code: 'UNAUTHORIZED'; message: 'Not authenticated' };
```

#### GET /api/v1/{resource}/:id
```typescript
// Request
type PathParams = { id: UUID };

// Response 200
type ResponseBody = {Resource}Detail;

// Errors
type Errors =
  | { code: 'NOT_FOUND'; message: '{Resource} not found' }
  | { code: 'FORBIDDEN'; message: 'Not authorized' };
```

#### PATCH /api/v1/{resource}/:id
```typescript
// Request
type PathParams = { id: UUID };
type RequestBody = Update{Resource}Request;

// Response 200
type ResponseBody = {Resource};

// Errors
type Errors =
  | { code: 'NOT_FOUND'; message: '{Resource} not found' }
  | { code: 'VALIDATION_ERROR'; message: string }
  | { code: 'FORBIDDEN'; message: 'Not authorized' };
```

#### DELETE /api/v1/{resource}/:id
```typescript
// Request
type PathParams = { id: UUID };

// Response 204
// No body

// Errors
type Errors =
  | { code: 'NOT_FOUND'; message: '{Resource} not found' }
  | { code: 'CONFLICT'; message: 'Cannot delete: has dependencies' };
```

---

## Validation Rules

### User Validation
| Field | Rules |
|-------|-------|
| email | Required, valid email format, max 255 chars |
| password | Required, min 8 chars, 1 uppercase, 1 number |
| name | Required, 2-100 chars |

### {Resource} Validation
| Field | Rules |
|-------|-------|
| name | Required, 1-255 chars, trimmed |
| description | Optional, max 1000 chars |
| status | Optional, one of: draft, active, archived |

---

## Enums & Constants

### Status Values
```typescript
const {Resource}StatusValues = ['draft', 'active', 'archived'] as const;
```

### Error Codes
```typescript
const ErrorCodes = {
  // Auth
  EMAIL_EXISTS: 'EMAIL_EXISTS',
  INVALID_CREDENTIALS: 'INVALID_CREDENTIALS',
  ACCOUNT_LOCKED: 'ACCOUNT_LOCKED',
  TOKEN_EXPIRED: 'TOKEN_EXPIRED',

  // General
  VALIDATION_ERROR: 'VALIDATION_ERROR',
  UNAUTHORIZED: 'UNAUTHORIZED',
  FORBIDDEN: 'FORBIDDEN',
  NOT_FOUND: 'NOT_FOUND',
  CONFLICT: 'CONFLICT',
  INTERNAL_ERROR: 'INTERNAL_ERROR',
} as const;
```

### HTTP Status Codes
| Code | Usage |
|------|-------|
| 200 | Success (GET, PATCH) |
| 201 | Created (POST) |
| 204 | No Content (DELETE) |
| 400 | Bad Request (validation) |
| 401 | Unauthorized (not logged in) |
| 403 | Forbidden (not allowed) |
| 404 | Not Found |
| 409 | Conflict |
| 429 | Too Many Requests |
| 500 | Internal Server Error |

---

## Shared Utilities

### Type Guards
```typescript
// Check if response is an error
function isApiError(response: unknown): response is ErrorResponse {
  return (
    typeof response === 'object' &&
    response !== null &&
    'error' in response
  );
}

// Check specific error code
function isErrorCode(error: ApiError, code: string): boolean {
  return error.code === code;
}
```

### Response Helpers
```typescript
// Create success response
function success<T>(data: T): T {
  return data;
}

// Create paginated response
function paginated<T>(
  data: T[],
  total: number,
  page: number,
  limit: number
): PaginatedResponse<T> {
  return {
    data,
    meta: {
      total,
      page,
      limit,
      totalPages: Math.ceil(total / limit),
    },
  };
}

// Create error response
function error(code: string, message: string, details?: unknown): ErrorResponse {
  return {
    error: { code, message, details },
  };
}
```

---

## Schema Definitions (Zod)

### Shared Schemas
```typescript
import { z } from 'zod';

// Reusable schemas
export const uuidSchema = z.string().uuid();
export const emailSchema = z.string().email().max(255);
export const passwordSchema = z.string()
  .min(8, 'Password must be at least 8 characters')
  .regex(/[A-Z]/, 'Must contain uppercase letter')
  .regex(/[0-9]/, 'Must contain number');

// Pagination
export const paginationSchema = z.object({
  page: z.coerce.number().min(1).default(1),
  limit: z.coerce.number().min(1).max(100).default(20),
});

// Sort
export const sortSchema = z.string().regex(/^-?[a-zA-Z]+$/);
```

### Auth Schemas
```typescript
export const registerSchema = z.object({
  email: emailSchema,
  password: passwordSchema,
  name: z.string().min(2).max(100),
});

export const loginSchema = z.object({
  email: emailSchema,
  password: z.string().min(1),
});
```

### {Resource} Schemas
```typescript
export const create{Resource}Schema = z.object({
  name: z.string().min(1).max(255).trim(),
  description: z.string().max(1000).optional(),
});

export const update{Resource}Schema = create{Resource}Schema.partial().extend({
  status: z.enum(['draft', 'active', 'archived']).optional(),
});

export const {resource}ListParamsSchema = paginationSchema.extend({
  search: z.string().optional(),
  status: z.enum(['draft', 'active', 'archived']).optional(),
  sort: sortSchema.default('-createdAt'),
});
```

---

## WebSocket Events (if applicable)
[NEEDS CLARIFICATION: Real-time features needed?]

```typescript
// Client → Server
interface ClientEvents {
  'subscribe:{resource}': { id: UUID };
  'unsubscribe:{resource}': { id: UUID };
}

// Server → Client
interface ServerEvents {
  '{resource}:updated': { resource: {Resource} };
  '{resource}:deleted': { id: UUID };
}
```

---

## Versioning

### API Versioning
- Current version: v1
- Version in URL path: `/api/v1/...`
- Breaking changes require new version

### Contract Changes
| Change Type | Backward Compatible | Action |
|-------------|---------------------|--------|
| Add optional field | Yes | Minor update |
| Add required field | No | Major version |
| Remove field | No | Major version |
| Change field type | No | Major version |
| Add new endpoint | Yes | Minor update |
| Remove endpoint | No | Major version |

---

## Notes

- All dates are in ISO 8601 format with UTC timezone
- All IDs are UUIDs v4
- Strings are trimmed on server side
- Null values are explicit (not undefined)
- Arrays are never null (empty array instead)

[NEEDS CLARIFICATION: File upload contracts?]
[ASSUMPTION: REST API, no GraphQL]
