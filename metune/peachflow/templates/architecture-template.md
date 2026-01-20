---
product: {product-name}
document: architecture
version: 1.0
status: draft | review | approved
created: {date}
updated: {date}
owner: software-architect
---

# Architecture: {Product Name}

## Executive Summary

{2-3 paragraph overview of the technical architecture and key decisions}

---

## System Overview

### High-Level Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                              CLIENTS                                    │
├────────────────┬────────────────┬────────────────┬─────────────────────┤
│   Web App      │   Mobile App   │   Admin Panel  │   Third-Party       │
│   (React)      │   (React Native)│   (React)      │   Integrations      │
└───────┬────────┴───────┬────────┴───────┬────────┴────────┬────────────┘
        │                │                │                 │
        └────────────────┴───────┬────────┴─────────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │      API Gateway        │
                    │    (Authentication)     │
                    └────────────┬────────────┘
                                 │
        ┌────────────────────────┼────────────────────────┐
        │                        │                        │
┌───────▼───────┐    ┌───────────▼───────────┐    ┌──────▼───────┐
│  Auth Service │    │    Core Service       │    │  {Service}   │
│               │    │                       │    │              │
└───────┬───────┘    └───────────┬───────────┘    └──────┬───────┘
        │                        │                       │
        └────────────────────────┼───────────────────────┘
                                 │
                    ┌────────────▼────────────┐
                    │       Database          │
                    │    (PostgreSQL)         │
                    └─────────────────────────┘
```

### Architecture Style
{Monolith/Microservices/Serverless/Hybrid}

**Rationale**: {Why this architecture style}

---

## Technology Stack

### Frontend
| Layer | Technology | Version | Rationale |
|-------|------------|---------|-----------|
| Framework | {React} | {19.x} | {Why} |
| State | {Zustand/Redux} | {x.x} | {Why} |
| Styling | {Tailwind/CSS Modules} | {x.x} | {Why} |
| Build | {Vite/Webpack} | {x.x} | {Why} |
| Testing | {Vitest/Jest} | {x.x} | {Why} |

### Backend
| Layer | Technology | Version | Rationale |
|-------|------------|---------|-----------|
| Runtime | {Node.js/Deno} | {x.x} | {Why} |
| Framework | {Express/Fastify/Hono} | {x.x} | {Why} |
| ORM | {Prisma/Drizzle} | {x.x} | {Why} |
| Validation | {Zod/Yup} | {x.x} | {Why} |
| Testing | {Vitest/Jest} | {x.x} | {Why} |

### Database
| Type | Technology | Rationale |
|------|------------|-----------|
| Primary | {PostgreSQL} | {Why} |
| Cache | {Redis} | {Why} |
| Search | {Elasticsearch} | {If needed} |
| Queue | {BullMQ/RabbitMQ} | {If needed} |

### Infrastructure
| Component | Technology | Rationale |
|-----------|------------|-----------|
| Hosting | {Vercel/AWS/GCP} | {Why} |
| CI/CD | {GitHub Actions} | {Why} |
| Monitoring | {DataDog/Sentry} | {Why} |
| CDN | {Cloudflare/CloudFront} | {Why} |

---

## Data Architecture

### Entity Relationship Diagram

```
┌──────────────┐       ┌──────────────┐       ┌──────────────┐
│    User      │       │   {Entity}   │       │   {Entity}   │
├──────────────┤       ├──────────────┤       ├──────────────┤
│ id           │──┐    │ id           │──┐    │ id           │
│ email        │  │    │ user_id      │◀─┘    │ {field}      │
│ name         │  │    │ {field}      │──────▶│ {field}      │
│ created_at   │  │    │ created_at   │       │ created_at   │
└──────────────┘  │    └──────────────┘       └──────────────┘
                  │
                  └──── 1:N relationship
```

### Key Entities
| Entity | Description | Key Fields |
|--------|-------------|------------|
| User | {Description} | id, email, name |
| {Entity 2} | {Description} | {fields} |
| {Entity 3} | {Description} | {fields} |

### Data Flow
{Description of how data flows through the system}

---

## API Design

### API Style
{REST/GraphQL/tRPC/gRPC}

**Rationale**: {Why this style}

### API Structure
```
/api
├── /v1
│   ├── /auth
│   │   ├── POST /register
│   │   ├── POST /login
│   │   └── POST /logout
│   ├── /users
│   │   ├── GET /me
│   │   ├── PATCH /me
│   │   └── DELETE /me
│   └── /{resource}
│       ├── GET /
│       ├── POST /
│       ├── GET /:id
│       ├── PATCH /:id
│       └── DELETE /:id
```

### API Conventions
| Aspect | Convention |
|--------|------------|
| Naming | {kebab-case/camelCase} |
| Versioning | {URL path /v1} |
| Pagination | {Cursor/Offset} |
| Filtering | {Query params} |
| Errors | {Standard format} |

### Error Response Format
```json
{
  "error": {
    "code": "VALIDATION_ERROR",
    "message": "Human readable message",
    "details": [
      { "field": "email", "message": "Invalid email format" }
    ]
  }
}
```

---

## Authentication & Authorization

### Authentication Strategy
| Method | Usage |
|--------|-------|
| JWT | {API authentication} |
| Session | {Web app} |
| OAuth | {Third-party login} |
| API Keys | {External integrations} |

### Authorization Model
{RBAC/ABAC/Custom}

### Roles & Permissions
| Role | Permissions |
|------|-------------|
| Admin | Full access |
| User | Own data CRUD |
| Guest | Read-only public |

### Security Considerations
- [ ] Password hashing (bcrypt/argon2)
- [ ] Rate limiting
- [ ] CORS configuration
- [ ] CSRF protection
- [ ] Input validation
- [ ] SQL injection prevention
- [ ] XSS prevention

---

## Component Architecture

### Frontend Components

```
src/
├── app/                    # App routes/pages
├── components/
│   ├── ui/                 # Primitives (Button, Input)
│   ├── patterns/           # Composed (Form, Modal)
│   └── features/           # Feature-specific
├── hooks/                  # Custom hooks
├── lib/                    # Utilities
├── stores/                 # State management
└── types/                  # TypeScript types
```

### Backend Services

```
src/
├── api/                    # Route handlers
│   ├── auth/
│   └── {resource}/
├── services/               # Business logic
├── repositories/           # Data access
├── models/                 # Data models
├── middleware/             # Express middleware
├── utils/                  # Helpers
└── types/                  # TypeScript types
```

---

## Integration Architecture

### External Integrations
| Service | Purpose | Priority |
|---------|---------|----------|
| {Service 1} | {Purpose} | {P1/P2/P3} |
| {Service 2} | {Purpose} | {P1/P2/P3} |

### Integration Patterns
{How integrations are handled - adapters, facades, etc.}

---

## Scalability Considerations

### Current Scale Targets
| Metric | Target |
|--------|--------|
| Concurrent Users | {X} |
| Requests/Second | {X} |
| Data Volume | {X GB} |
| Response Time (p95) | {X ms} |

### Scaling Strategy
{Horizontal/Vertical scaling approach}

### Performance Optimizations
1. {Optimization 1}
2. {Optimization 2}
3. {Optimization 3}

---

## Deployment Architecture

### Environments
| Environment | Purpose | URL |
|-------------|---------|-----|
| Development | Local development | localhost:3000 |
| Staging | Pre-production testing | staging.{domain} |
| Production | Live application | {domain} |

### CI/CD Pipeline
```
[Push] → [Lint] → [Test] → [Build] → [Deploy Staging] → [Manual Approval] → [Deploy Prod]
```

### Deployment Strategy
{Blue-green/Canary/Rolling}

---

## Monitoring & Observability

### Logging Strategy
| Level | Usage |
|-------|-------|
| ERROR | Application errors |
| WARN | Potential issues |
| INFO | Key events |
| DEBUG | Debugging (dev only) |

### Metrics
| Metric | Tool | Alert Threshold |
|--------|------|-----------------|
| Error Rate | {Sentry} | {>1%} |
| Response Time | {DataDog} | {>500ms} |
| Uptime | {Pingdom} | {<99.9%} |

### Health Checks
- `/health` - Basic health
- `/health/ready` - Readiness
- `/health/live` - Liveness

---

## Technical Decisions

### Decision Log
| Decision | Options Considered | Chosen | Rationale |
|----------|-------------------|--------|-----------|
| {Decision 1} | {A, B, C} | {B} | {Why} |
| {Decision 2} | {A, B} | {A} | {Why} |

### Open Questions
[NEEDS CLARIFICATION: {Technical question 1}]
[NEEDS CLARIFICATION: {Technical question 2}]

---

## Technical Debt & Risks

### Known Technical Debt
| Item | Impact | Priority | Plan |
|------|--------|----------|------|
| {Debt item 1} | {Impact} | {P1/P2/P3} | {When to address} |

### Technical Risks
| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| {Risk 1} | {H/M/L} | {H/M/L} | {Strategy} |

---

## References

### Documentation
- {Link to relevant docs}

### Standards
- {Coding standards doc}
- {API standards doc}

### Diagrams
- {Link to detailed diagrams}
