---
product: {product-name}
quarter: Q{XX}
document: backend-spec
version: 1.0
status: draft | review | approved
created: {date}
updated: {date}
owner: backend-engineer
---

# Backend Specification: Q{XX} - {Theme}

## Overview

{Summary of backend work for this quarter}

**Reference Documents**:
- [Quarterly Plan](./plan.md)
- [Frontend Spec](./frontend-spec.md)
- [Data Contracts](./data-contracts.md)
- [Architecture](../../discovery/architecture.md)

---

## API Design

### Base Configuration
```
Base URL: /api/v1
Content-Type: application/json
Authentication: Bearer token (JWT)
```

### API Endpoints

#### Authentication
[TAGS: Q{XX}, E{XX}, auth, api]

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| POST | `/auth/register` | Create new user | No |
| POST | `/auth/login` | Authenticate user | No |
| POST | `/auth/logout` | Invalidate session | Yes |
| POST | `/auth/refresh` | Refresh access token | Yes |
| POST | `/auth/forgot-password` | Request password reset | No |
| POST | `/auth/reset-password` | Reset password | No |

---

##### POST /auth/register

**Request**:
```typescript
interface RegisterRequest {
  email: string;      // valid email
  password: string;   // min 8 chars, 1 upper, 1 number
  name: string;       // 2-100 chars
}
```

**Response (201)**:
```typescript
interface RegisterResponse {
  user: {
    id: string;
    email: string;
    name: string;
    createdAt: string;
  };
  tokens: {
    accessToken: string;
    refreshToken: string;
    expiresIn: number;
  };
}
```

**Errors**:
| Code | Status | Message |
|------|--------|---------|
| EMAIL_EXISTS | 409 | Email already registered |
| VALIDATION_ERROR | 400 | Invalid input data |

---

##### POST /auth/login

**Request**:
```typescript
interface LoginRequest {
  email: string;
  password: string;
}
```

**Response (200)**:
```typescript
interface LoginResponse {
  user: User;
  tokens: Tokens;
}
```

**Errors**:
| Code | Status | Message |
|------|--------|---------|
| INVALID_CREDENTIALS | 401 | Invalid email or password |
| ACCOUNT_LOCKED | 423 | Account temporarily locked |

---

#### {Resource} CRUD
[TAGS: Q{XX}, E{XX}, {resource}, api]

| Method | Endpoint | Description | Auth |
|--------|----------|-------------|------|
| GET | `/{resource}` | List resources | Yes |
| POST | `/{resource}` | Create resource | Yes |
| GET | `/{resource}/:id` | Get resource | Yes |
| PATCH | `/{resource}/:id` | Update resource | Yes |
| DELETE | `/{resource}/:id` | Delete resource | Yes |

---

##### GET /{resource}

**Query Parameters**:
| Param | Type | Default | Description |
|-------|------|---------|-------------|
| page | number | 1 | Page number |
| limit | number | 20 | Items per page (max 100) |
| search | string | - | Search term |
| sort | string | -createdAt | Sort field (prefix - for desc) |
| status | string | - | Filter by status |

**Response (200)**:
```typescript
interface ListResponse<T> {
  data: T[];
  meta: {
    total: number;
    page: number;
    limit: number;
    totalPages: number;
  };
}
```

---

##### POST /{resource}

**Request**:
```typescript
interface Create{Resource}Request {
  // Required fields
  name: string;
  // Optional fields
  description?: string;
}
```

**Response (201)**:
```typescript
interface {Resource}Response {
  id: string;
  name: string;
  description: string | null;
  createdAt: string;
  updatedAt: string;
}
```

**Errors**:
| Code | Status | Message |
|------|--------|---------|
| VALIDATION_ERROR | 400 | Invalid input |
| UNAUTHORIZED | 401 | Not authenticated |
| FORBIDDEN | 403 | Not authorized |

---

##### GET /{resource}/:id

**Response (200)**:
```typescript
interface {Resource}DetailResponse {
  id: string;
  name: string;
  description: string | null;
  // Related data
  {relation}: {RelatedType}[];
  createdAt: string;
  updatedAt: string;
}
```

**Errors**:
| Code | Status | Message |
|------|--------|---------|
| NOT_FOUND | 404 | Resource not found |

---

##### PATCH /{resource}/:id

**Request**:
```typescript
interface Update{Resource}Request {
  name?: string;
  description?: string;
}
```

**Response (200)**: Same as GET

---

##### DELETE /{resource}/:id

**Response (204)**: No content

**Errors**:
| Code | Status | Message |
|------|--------|---------|
| NOT_FOUND | 404 | Resource not found |
| CONFLICT | 409 | Resource has dependencies |

---

## Database Schema

### Entity Relationship Diagram
```
┌──────────────────┐       ┌──────────────────┐
│      users       │       │    {resource}    │
├──────────────────┤       ├──────────────────┤
│ id          PK   │◀──┐   │ id          PK   │
│ email       UQ   │   │   │ user_id     FK   │──┐
│ password_hash    │   └───│                  │  │
│ name             │       │ name             │  │
│ created_at       │       │ description      │  │
│ updated_at       │       │ status           │  │
│ deleted_at       │       │ created_at       │  │
└──────────────────┘       │ updated_at       │  │
                           └──────────────────┘  │
                                                 │
                           ┌──────────────────┐  │
                           │   {relation}     │  │
                           ├──────────────────┤  │
                           │ id          PK   │  │
                           │ {resource}_id FK │◀─┘
                           │ ...              │
                           └──────────────────┘
```

### Tables

#### users
[TAGS: Q{XX}, database, users]

```sql
CREATE TABLE users (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  email VARCHAR(255) NOT NULL UNIQUE,
  password_hash VARCHAR(255) NOT NULL,
  name VARCHAR(100) NOT NULL,
  email_verified_at TIMESTAMP WITH TIME ZONE,
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  deleted_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX idx_users_email ON users(email);
CREATE INDEX idx_users_deleted_at ON users(deleted_at);
```

---

#### {resource}
[TAGS: Q{XX}, database, {resource}]

```sql
CREATE TABLE {resource} (
  id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
  user_id UUID NOT NULL REFERENCES users(id),
  name VARCHAR(255) NOT NULL,
  description TEXT,
  status VARCHAR(50) DEFAULT 'active',
  created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  updated_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
  deleted_at TIMESTAMP WITH TIME ZONE
);

CREATE INDEX idx_{resource}_user_id ON {resource}(user_id);
CREATE INDEX idx_{resource}_status ON {resource}(status);
CREATE INDEX idx_{resource}_created_at ON {resource}(created_at);
```

---

### Migrations

#### Migration 001: Initial Schema
[TAGS: Q{XX}, database, migration]

**File**: `prisma/migrations/001_initial/migration.sql`

```sql
-- CreateTable users
-- CreateTable {resource}
-- CreateIndexes
```

---

### Seed Data

**File**: `prisma/seed.ts`

```typescript
const seedData = {
  users: [
    {
      email: 'test@example.com',
      password: 'hashed_password',
      name: 'Test User',
    },
  ],
  {resource}: [
    {
      name: 'Sample Item',
      description: 'A sample item for testing',
    },
  ],
};
```

---

## Service Architecture

### Service Layer Structure
```
src/
├── api/
│   ├── auth/
│   │   ├── auth.controller.ts
│   │   ├── auth.service.ts
│   │   ├── auth.validation.ts
│   │   └── auth.routes.ts
│   └── {resource}/
│       ├── {resource}.controller.ts
│       ├── {resource}.service.ts
│       ├── {resource}.validation.ts
│       └── {resource}.routes.ts
├── services/
│   ├── email.service.ts
│   └── storage.service.ts
├── repositories/
│   ├── user.repository.ts
│   └── {resource}.repository.ts
├── middleware/
│   ├── auth.middleware.ts
│   ├── validation.middleware.ts
│   └── error.middleware.ts
├── utils/
│   ├── jwt.ts
│   ├── password.ts
│   └── pagination.ts
└── types/
    └── index.ts
```

---

### Authentication Service
[TAGS: Q{XX}, auth, service]

**File**: `src/api/auth/auth.service.ts`

```typescript
class AuthService {
  async register(data: RegisterDTO): Promise<AuthResult> {
    // 1. Check if email exists
    // 2. Hash password
    // 3. Create user
    // 4. Generate tokens
    // 5. Send verification email
    return { user, tokens };
  }

  async login(data: LoginDTO): Promise<AuthResult> {
    // 1. Find user by email
    // 2. Verify password
    // 3. Check account status
    // 4. Generate tokens
    return { user, tokens };
  }

  async refreshToken(token: string): Promise<Tokens> {
    // 1. Verify refresh token
    // 2. Generate new tokens
    return tokens;
  }
}
```

---

### {Resource} Service
[TAGS: Q{XX}, {resource}, service]

**File**: `src/api/{resource}/{resource}.service.ts`

```typescript
class {Resource}Service {
  async list(userId: string, params: ListParams): Promise<PaginatedResult<{Resource}>> {
    // 1. Build query with filters
    // 2. Execute with pagination
    // 3. Return formatted result
  }

  async create(userId: string, data: Create{Resource}DTO): Promise<{Resource}> {
    // 1. Validate data
    // 2. Create resource
    // 3. Return created resource
  }

  async getById(id: string, userId: string): Promise<{Resource}> {
    // 1. Find resource
    // 2. Check ownership/access
    // 3. Return with relations
  }

  async update(id: string, userId: string, data: Update{Resource}DTO): Promise<{Resource}> {
    // 1. Find resource
    // 2. Check ownership
    // 3. Update fields
    // 4. Return updated
  }

  async delete(id: string, userId: string): Promise<void> {
    // 1. Find resource
    // 2. Check ownership
    // 3. Soft delete
  }
}
```

---

## Validation Schemas

### Auth Validation
[TAGS: Q{XX}, auth, validation]

**File**: `src/api/auth/auth.validation.ts`

```typescript
import { z } from 'zod';

export const registerSchema = z.object({
  email: z.string().email('Invalid email format'),
  password: z.string()
    .min(8, 'Password must be at least 8 characters')
    .regex(/[A-Z]/, 'Password must contain uppercase letter')
    .regex(/[0-9]/, 'Password must contain number'),
  name: z.string().min(2).max(100),
});

export const loginSchema = z.object({
  email: z.string().email(),
  password: z.string().min(1),
});
```

---

### {Resource} Validation
[TAGS: Q{XX}, {resource}, validation]

**File**: `src/api/{resource}/{resource}.validation.ts`

```typescript
export const create{Resource}Schema = z.object({
  name: z.string().min(1).max(255),
  description: z.string().max(1000).optional(),
});

export const update{Resource}Schema = create{Resource}Schema.partial();

export const list{Resource}Schema = z.object({
  page: z.coerce.number().min(1).default(1),
  limit: z.coerce.number().min(1).max(100).default(20),
  search: z.string().optional(),
  status: z.enum(['active', 'inactive']).optional(),
  sort: z.string().default('-createdAt'),
});
```

---

## Error Handling

### Error Types
```typescript
// src/utils/errors.ts
export class AppError extends Error {
  constructor(
    public code: string,
    public message: string,
    public statusCode: number,
    public details?: unknown
  ) {
    super(message);
  }
}

export const Errors = {
  VALIDATION_ERROR: (details: unknown) =>
    new AppError('VALIDATION_ERROR', 'Invalid input', 400, details),
  UNAUTHORIZED: () =>
    new AppError('UNAUTHORIZED', 'Not authenticated', 401),
  FORBIDDEN: () =>
    new AppError('FORBIDDEN', 'Not authorized', 403),
  NOT_FOUND: (resource: string) =>
    new AppError('NOT_FOUND', `${resource} not found`, 404),
  CONFLICT: (message: string) =>
    new AppError('CONFLICT', message, 409),
};
```

### Error Response Format
```typescript
interface ErrorResponse {
  error: {
    code: string;
    message: string;
    details?: unknown;
  };
}
```

---

## Security Measures

### Authentication
- JWT access tokens (15min expiry)
- Refresh tokens (7 day expiry)
- Secure HTTP-only cookies for web

### Password Security
- bcrypt hashing (10 rounds)
- Password strength requirements
- Rate limiting on auth endpoints

### API Security
- [ ] Rate limiting (100 req/min per user)
- [ ] Request validation
- [ ] SQL injection prevention (parameterized queries)
- [ ] XSS prevention (input sanitization)
- [ ] CORS configuration
- [ ] Helmet security headers

### Data Protection
- Soft deletes (data retention)
- Audit logging for sensitive operations
- PII encryption at rest [NEEDS CLARIFICATION]

---

## Testing Strategy

### Unit Tests
```typescript
// src/api/{resource}/__tests__/{resource}.service.test.ts
describe('{Resource}Service', () => {
  describe('create', () => {
    it('should create resource with valid data', async () => {});
    it('should throw on invalid data', async () => {});
  });

  describe('list', () => {
    it('should return paginated results', async () => {});
    it('should filter by status', async () => {});
    it('should search by name', async () => {});
  });
});
```

### Integration Tests
```typescript
// src/api/{resource}/__tests__/{resource}.integration.test.ts
describe('GET /api/{resource}', () => {
  it('should return 401 without auth', async () => {});
  it('should return list for authenticated user', async () => {});
  it('should paginate results', async () => {});
});
```

### Test Coverage Targets
| Layer | Target |
|-------|--------|
| Services | 90% |
| Controllers | 80% |
| Repositories | 70% |
| Utilities | 90% |

---

## Performance Requirements

### Response Time Targets
| Endpoint | p50 | p95 | p99 |
|----------|-----|-----|-----|
| Auth endpoints | 100ms | 200ms | 500ms |
| List endpoints | 100ms | 300ms | 500ms |
| Detail endpoints | 50ms | 100ms | 200ms |
| Create/Update | 100ms | 200ms | 500ms |

### Database Optimization
- Proper indexing on filtered columns
- Query optimization
- Connection pooling
- Caching strategy [NEEDS CLARIFICATION]

---

## Logging & Monitoring

### Log Levels
| Level | Usage |
|-------|-------|
| ERROR | Unhandled errors, critical failures |
| WARN | Recoverable errors, deprecations |
| INFO | Key business events, API requests |
| DEBUG | Detailed debugging (dev only) |

### Log Format
```json
{
  "timestamp": "2024-01-15T10:30:00Z",
  "level": "INFO",
  "message": "User registered",
  "userId": "uuid",
  "requestId": "uuid",
  "duration": 150
}
```

### Health Checks
- `GET /health` - Basic health
- `GET /health/ready` - DB connection check
- `GET /health/live` - Liveness probe

---

## Implementation Checklist

### Phase 1: Setup
- [ ] Project scaffolding
- [ ] Database setup
- [ ] Migration system
- [ ] Error handling
- [ ] Logging

### Phase 2: Authentication
- [ ] Register endpoint
- [ ] Login endpoint
- [ ] JWT middleware
- [ ] Refresh tokens

### Phase 3: Core API
- [ ] {Resource} CRUD
- [ ] Validation
- [ ] Pagination
- [ ] Filtering/Search

### Phase 4: Polish
- [ ] Rate limiting
- [ ] Security headers
- [ ] API documentation
- [ ] Test coverage

---

## Notes

[NEEDS CLARIFICATION: Caching strategy?]
[NEEDS CLARIFICATION: Background jobs needed?]
[ASSUMPTION: Using PostgreSQL as primary database]
