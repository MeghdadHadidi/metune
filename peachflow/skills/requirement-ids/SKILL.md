---
name: requirement-ids
description: |
  Use this skill when creating or referencing requirements, features, epics, stories, or tasks. Ensures consistent ID formats and traceability.
---

# Requirement ID System

## ID Formats

| Type | Format | Range | Example |
|------|--------|-------|---------|
| Business Requirement | BR-XXX | 001-999 | BR-001 |
| Feature | F-XXX | 001-999 | F-001 |
| Functional Requirement | FR-XXX | 001-999 | FR-001 |
| Non-Functional Requirement | NFR-XXX | 001-999 | NFR-001 |
| Epic | E-XXX | 001-999 | E-001 |
| User Story | US-XXX | 001-999 | US-001 |
| Task | T-XXX | 001-999 | T-001 |

## ID Ranges (Recommended)

### Functional Requirements (FR)
- FR-001 to FR-099: User Management
- FR-100 to FR-199: Core Features
- FR-200 to FR-299: Integrations
- FR-300 to FR-399: Reporting
- FR-400 to FR-499: Admin Functions

### Non-Functional Requirements (NFR)
- NFR-001 to NFR-019: Performance
- NFR-020 to NFR-039: Security
- NFR-040 to NFR-059: Scalability
- NFR-060 to NFR-079: Reliability
- NFR-080 to NFR-099: Usability/Accessibility

## Traceability Chain

IDs link through the documentation chain:

```
BR-001 (Business Requirement)
  └── F-001 (Feature in PRD)
        └── FR-001, FR-002 (Functional Requirements)
              └── E-001 (Epic in Plan)
                    └── US-001, US-002 (User Stories)
                          └── T-001, T-002, T-003 (Tasks)
```

## Usage Examples

### In BRD
```markdown
### BR-001: User Self-Service Registration
Users must be able to create their own accounts without admin intervention.
```

### In PRD
```markdown
#### F-001: User Registration
- **Business Requirement**: BR-001
- **Priority**: Must Have
```

### In FRD
```markdown
#### FR-001: User Registration API
- **Feature**: F-001
- **Business Requirement**: BR-001
```

### In Plan
```markdown
## E-001: User Authentication
**FRs**: FR-001, FR-002, FR-003
**NFRs**: NFR-020, NFR-021
```

### In Stories
```markdown
## US-001: User Registration
**Epic**: E-001
**FRs**: FR-001
```

### In Tasks
```markdown
---
id: T-001
epic: E-001
story: US-001
---
## FR Reference
- FR-001: User Registration API
```

## Cross-Reference Format

When referencing other IDs in documents:

```markdown
- **Source**: BR-001, F-001
- **Related FRs**: FR-001, FR-002
- **Related NFRs**: NFR-020
- **Epic**: E-001
- **Story**: US-001
- **Dependencies**: T-001, T-002
```

## Finding by ID

```bash
# Find all references to a requirement
grep -r "FR-001" docs/ --include="*.md"

# Find all tasks for an epic
grep -r "epic: E-001" docs/04-plan/quarters/*/tasks/ --include="*.md"

# Find all features for a business requirement
grep -r "BR-001" docs/02-product/PRD.md
```

## ID Assignment Rules

1. **Sequential**: Assign IDs in order (001, 002, 003...)
2. **Never reuse**: Don't reassign deleted IDs
3. **Prefix always**: Always include type prefix
4. **Zero-pad**: Use 3 digits (001 not 1)
5. **No gaps OK**: Gaps in sequence are fine (001, 002, 005)
