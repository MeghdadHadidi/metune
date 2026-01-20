---
product: {product-name}
document: quarterly-roadmap
version: 1.0
status: draft | review | approved
created: {date}
updated: {date}
total-quarters: {N}
target-launch: {date}
---

# Quarterly Roadmap: {Product Name}

## Executive Summary

{Overview of the development plan and key milestones}

---

## Timeline Overview

```
Q01 ─────────┬─────────── Q02 ─────────┬─────────── Q03
    {Theme}  │      {Theme}           │      {Theme}
             │                        │
    [MVP]    │    [Core Features]     │    [Full Product]
```

---

## Quarterly Summary

| Quarter | Theme | Key Deliverable | Features |
|---------|-------|-----------------|----------|
| Q01 | {Theme} | {What users can do} | F001, F002, F003 |
| Q02 | {Theme} | {What users can do} | F004, F005 |
| Q03 | {Theme} | {What users can do} | F006, F007 |

---

## Q01: {Theme}

### Goals
{What will be possible after Q01? What can users do?}

### Features Included
- **F001**: {Feature name} - {Brief description}
- **F002**: {Feature name} - {Brief description}
- **F003**: {Feature name} - {Brief description}

### Epics

#### E01: {Epic Name}
{Brief description}

**User Stories:**
- US001: As a {user}, I want {goal} so that {benefit}
- US002: As a {user}, I want {goal} so that {benefit}

#### E02: {Epic Name}
{Brief description}

**User Stories:**
- US003: ...

### Technical Focus
- {Architecture component 1}
- {Architecture component 2}
- {Integration 1}

### Dependencies
- External: {Any external dependencies}
- Internal: None (first quarter)

### Risks
| Risk | Likelihood | Impact | Mitigation |
|------|------------|--------|------------|
| {Risk} | {L/M/H} | {L/M/H} | {Strategy} |

### Success Criteria
- [ ] {Measurable outcome 1}
- [ ] {Measurable outcome 2}

---

## Q02: {Theme}

### Goals
{Building on Q01, what new capabilities?}

### Features Included
- **F004**: {Feature} - {Description}
- **F005**: {Feature} - {Description}

### Epics

#### E03: {Epic Name}
...

### Dependencies
- Requires Q01: E01, E02 complete
- External: {Dependencies}

### Success Criteria
- [ ] {Outcome 1}
- [ ] {Outcome 2}

---

## Q03: {Theme}

### Goals
{Full product experience}

### Features Included
- **F006**: {Feature} - {Description}
- **F007**: {Feature} - {Description}

### Epics
...

### Dependencies
- Requires Q02: E03 complete

### Success Criteria
- [ ] {Outcome}
- [ ] {Outcome}

---

## Technical Standards

### Coding Standards
{Project-wide coding standards that apply to all quarters}

### Architecture Patterns
{Patterns all code should follow}

### Testing Strategy
- Unit: {Coverage target}
- Integration: {Approach}
- E2E: {Approach}

### Documentation Requirements
- Code comments with @peachflow tags
- API documentation
- Component documentation

---

## Risk Register (Project-Wide)

| Risk | Quarter | Impact | Mitigation | Owner |
|------|---------|--------|------------|-------|
| {Risk} | All | High | {Strategy} | {Role} |

---

## Decision Log

| Decision | Date | Rationale | Impact |
|----------|------|-----------|--------|
| {Decision 1} | {date} | {Why} | {What changes} |

---

## Notes

- Each quarter should deliver usable functionality
- Features split to minimize dependencies
- Technical foundation front-loaded in Q01
- User feedback incorporated after each quarter
