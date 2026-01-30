---
name: document-standards
description: |
  Use this skill when creating or updating documentation in a Peachflow project. Applies when writing BRD, PRD, or architecture decision records (ADRs).
---

# Peachflow Document Standards

## Core Principles

1. **Brevity over verbosity**: Each document max 1-2 pages
2. **Bullet points over prose**: Scannable content
3. **Practical over theoretical**: Focus on implementation
4. **Mark unknowns**: Use `[NEEDS CLARIFICATION: ...]` for gaps

## Document Structure

All documents follow this structure:

```markdown
# Document Title

## Overview
[2-3 sentences max]

## Main Content
[Organized in sections with headers]

## Open Questions
[List of [NEEDS CLARIFICATION] items]
```

## Formatting Rules

### Headers
- Use `#` for document title
- Use `##` for main sections
- Use `###` for subsections
- Don't go deeper than `####`

### Lists
- Prefer bullet points (`-`) for unordered lists
- Use numbered lists only for sequential steps
- Keep list items to 1-2 lines max

### Tables
Use tables for structured data:
```markdown
| Column 1 | Column 2 | Column 3 |
|----------|----------|----------|
| Data | Data | Data |
```

### Checkboxes
Use for trackable items:
```markdown
- [ ] Pending item
- [x] Completed item
```

### Code/Technical
Use fenced code blocks with language:
```markdown
```typescript
const example = "code";
```
```

## Document Markers

### Clarification Needed

When information is missing or uncertain:

```markdown
[NEEDS CLARIFICATION: specific question here]
```

With options:
```markdown
[NEEDS CLARIFICATION: What authentication method?
Options:
- JWT tokens
- Session-based
- OAuth only]
```

### Inferred Content (from analyze)

When content is derived from code analysis rather than explicit requirements:

```markdown
[INFERRED: assumption based on existing user model]
```

### Technical Debt

When code quality issues are identified:

```markdown
[DEBT: missing input validation on user endpoints]
```

### Functionality Gaps

When incomplete or missing functionality is found:

```markdown
[GAP: email verification not implemented]
```

## ID Formats

| Entity | Format | Example |
|--------|--------|---------|
| Epics | E-XXX | E-001 |
| User Stories | US-XXX | US-001 |
| Tasks | T-XXX | T-001 |
| Sprints | S-XXX | S-001 |
| Clarifications | CL-XXX | CL-001 |
| ADRs | ADR-NNNN | ADR-0001 |

## File Locations

```
.peachflow-state.json       # Project settings & phase status
.peachflow-graph.json       # All work items (epics, stories, tasks, sprints)
docs/
├── 01-business/
│   └── BRD.md              # Business Requirements Document
├── 02-product/
│   ├── PRD.md              # Product Requirements Document
│   └── architecture/
│       └── adr/
│           └── ADR-NNNN-title.md
```

**Note:** Epics, user stories, tasks, and sprints are stored in the graph JSON file, not as separate markdown documents.

## Anti-patterns to Avoid

- Long paragraphs (break into bullets)
- Vague requirements ("should be fast" → "P95 < 200ms")
- Missing traceability (always link to source IDs)
- Over-documentation (1 page per concept max)
- Assumptions without marking (use [NEEDS CLARIFICATION])
