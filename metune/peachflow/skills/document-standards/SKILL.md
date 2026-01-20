---
name: peachflow-document-standards
description: This skill provides document formatting standards, clarification markers, and writing conventions for peachflow projects. Use when creating specs, PRDs, architecture docs, or any project documentation. Applies automatically when writing markdown documents in peachflow projects.
---

# Peachflow Document Standards

Standard formatting, markers, and conventions for all peachflow project documents.

## Document Header (Frontmatter)

All spec documents should include YAML frontmatter:

```yaml
---
product: {product-name}
document: {document-type}
version: 1.0
status: draft | review | approved
created: {YYYY-MM-DD}
updated: {YYYY-MM-DD}
owner: {agent-name}
---
```

### Document Types
- `prd` - Product Requirements Document
- `domain-research` - Market/competitor research
- `user-personas` - User persona definitions
- `user-journeys` - User journey maps
- `design-vision` - Design philosophy
- `architecture` - Technical architecture
- `quarterly-roadmap` - Master roadmap
- `quarter-plan` - Detailed quarter plan
- `tasks` - Task breakdown
- `clarifications` - Resolved questions

## Clarification Markers

### Unresolved Markers

| Marker | Usage | Example |
|--------|-------|---------|
| `[NEEDS CLARIFICATION: question]` | Primary marker for questions | `[NEEDS CLARIFICATION: What is the expected user volume?]` |
| `[TBD]` | To be determined | `Timeline: [TBD]` |
| `[TODO]` | Action needed | `[TODO: Add competitor pricing]` |
| `[UNCLEAR: description]` | Ambiguous requirement | `[UNCLEAR: Does "admin" include super-admins?]` |
| `[ASSUMPTION: statement]` | Implicit assumption | `[ASSUMPTION: Users have stable internet]` |

### Resolution Markers

| Marker | Usage | Example |
|--------|-------|---------|
| `[RESOLVED: date]` | Question answered | `[RESOLVED: 2026-01-20]` |
| `[DEFERRED: reason]` | Intentionally postponed | `[DEFERRED: Will decide in Q2]` |
| `[REJECTED: reason]` | Not applicable | `[REJECTED: Out of scope for MVP]` |

### Marker Placement

**Inline** (for short items):
```markdown
Budget: $50,000 [NEEDS CLARIFICATION: Is this per quarter or total?]
```

**Block** (for complex items):
```markdown
### Performance Requirements
[NEEDS CLARIFICATION: What are the expected performance targets?]
- Page load time: ?
- API response time: ?
- Concurrent users: ?
```

## Section Headers

### Standard Document Sections

#### PRD
1. Executive Summary
2. Problem Statement
3. Target Users
4. Product Vision
5. Feature Requirements
6. Non-Functional Requirements
7. Constraints
8. Monetization Strategy
9. Competitive Positioning
10. Risks & Mitigations
11. Success Criteria
12. Appendices

#### Architecture Document
1. Executive Summary
2. System Context
3. System Components
4. Technology Stack
5. Communication Patterns
6. Data Architecture
7. Non-Functional Requirements
8. Integration Points
9. Technical Risks
10. Architecture Decision Records

#### Task Document
1. Summary (table)
2. Phase 1: {Name}
3. Phase 2: {Name}
4. ...
5. Commit Checkpoints
6. Implementation Order

## Tables

### Feature Table
```markdown
| ID | Feature | Description | Priority | Effort |
|----|---------|-------------|----------|--------|
| F001 | User auth | Login/signup flow | Must Have | M |
| F002 | Dashboard | Main user interface | Must Have | L |
```

### Task Table
```markdown
| Phase | Tasks | Parallel |
|-------|-------|----------|
| Setup | 3 | No |
| Core | 10 | Partial |
```

### Comparison Table
```markdown
| Aspect | Option A | Option B | Recommendation |
|--------|----------|----------|----------------|
| Cost | Low | High | A |
| Complexity | High | Low | B |
```

## Lists

### Feature/Requirement Lists
```markdown
### Core Features (MVP)
- **F001: User Authentication**
  - Login with email/password
  - OAuth (Google, Microsoft)
  - Password reset flow

- **F002: Dashboard**
  - Overview statistics
  - Recent activity
  - Quick actions
```

### Acceptance Criteria
```markdown
### T003: Implement OAuth
- [ ] Handles Google OAuth callback
- [ ] Validates state parameter
- [ ] Creates user session
- [ ] Error handling implemented
- [ ] Unit tests written
```

## Code Blocks

### Diagrams (Mermaid)
```markdown
```mermaid
graph TD
    A[User] --> B[Web App]
    B --> C[API Server]
    C --> D[Database]
```​
```

### Architecture Diagrams
```markdown
```mermaid
C4Context
    Person(user, "User")
    System(system, "Our Product")
    System_Ext(ext, "External API")
    Rel(user, system, "Uses")
    Rel(system, ext, "Integrates")
```​
```

### Data Models
```markdown
```mermaid
erDiagram
    User ||--o{ Post : creates
    User {
        uuid id PK
        string email
        timestamp created
    }
```​
```

## Cross-References

### Internal References
```markdown
[Reference: domain-research.md]
[From user-personas.md]
[See architecture.md#technology-stack]
@see specs/quarterly/Q01/tasks.md#T003
```

### Task References
```markdown
[TAGS: Q01, E01, US001, auth, oauth]
Depends on: T002, T003
Blocks: T005, T006
```

## Status Indicators

### Document Status
- `draft` - Initial creation, incomplete
- `review` - Ready for review
- `approved` - Finalized, can be implemented

### Task Status
```markdown
### T001: Initialize project
**Status**: Done | In Progress | Pending | Blocked
```

### Visual Indicators
```markdown
✅ Complete
⚠️ Warning/Partial
❌ Failed/Missing
🚧 In Progress
📋 Pending
```

## Writing Style

### Do
- Use active voice
- Be specific and measurable
- Include examples
- Reference sources
- Use consistent terminology

### Don't
- Use vague language ("fast", "easy", "simple")
- Leave ambiguous requirements
- Skip acceptance criteria
- Forget to mark uncertainties
- Use inconsistent naming

## Template Usage

When creating documents, reference templates in `peachflow-plugin/templates/`:
- `prd-template.md`
- `architecture-template.md`
- `quarterly-roadmap-template.md`
- `quarter-tasks-template.md`
- `user-personas-template.md`
- `user-journeys-template.md`
- `design-vision-template.md`
- `data-contracts-template.md`
