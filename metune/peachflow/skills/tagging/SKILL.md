---
name: peachflow-tagging
description: This skill provides @peachflow tagging conventions for code and documents. Use when writing code files, adding comments, creating documentation, or implementing tasks from peachflow quarterly plans. Applies automatically when working in peachflow-managed projects.
---

# Peachflow Tagging Conventions

Apply these tagging conventions when writing or modifying code in peachflow-managed projects.

## Tag Hierarchy

```
@peachflow {Quarter}/{Epic}/{UserStory}/{Task}

Example: @peachflow Q01/E01/US001/T003
```

## File-Level Tags

Add to every new or significantly modified file:

```typescript
/**
 * @peachflow Q01/E01/US001/T003
 * @description Brief description of file purpose
 * @tags comma, separated, tags
 * @see specs/quarterly/Q01/tasks.md#T003
 */
```

### Language-Specific Formats

**TypeScript/JavaScript:**
```typescript
/**
 * @peachflow Q01/E01/US001/T003
 * @description OAuth callback handler
 * @tags auth, oauth, api
 * @see specs/quarterly/Q01/tasks.md#T003
 */
```

**Python:**
```python
"""
@peachflow Q01/E01/US001/T003
@description OAuth callback handler
@tags auth, oauth, api
@see specs/quarterly/Q01/tasks.md#T003
"""
```

**CSS/SCSS:**
```css
/**
 * @peachflow Q01/E02/US005/T012
 * @description Button component styles
 * @tags ui, components, buttons
 * @see specs/quarterly/Q01/tasks.md#T012
 */
```

**HTML:**
```html
<!--
  @peachflow Q01/E02/US005/T012
  @description Login page template
  @tags ui, pages, auth
  @see specs/quarterly/Q01/tasks.md#T012
-->
```

## Code Block Tags

Use for significant code sections within a file:

```typescript
// @peachflow:T003 - Token validation
function validateToken(token: string): TokenValidation {
  // implementation
}

// @peachflow:T003 - Session creation
async function createSession(user: User): Promise<Session> {
  // implementation
}
```

## Document Tags

In markdown/spec documents:

```markdown
### T003: Implement OAuth callback
[TAGS: Q01, E01, US001, auth, oauth, api]

**Description**: Handle OAuth provider callback...
```

## Tag Components

| Component | Format | Example | Description |
|-----------|--------|---------|-------------|
| Quarter | Q{XX} | Q01, Q02 | Two-digit quarter number |
| Epic | E{XX} | E01, E02 | Two-digit epic number |
| User Story | US{XXX} | US001 | Three-digit story number |
| Task | T{XXX} | T003 | Three-digit task number |

## Common Tags by Domain

### Authentication
`auth, oauth, google, microsoft, jwt, session, login, logout, password, 2fa`

### API
`api, rest, graphql, endpoint, middleware, validation, error-handling`

### UI/Frontend
`ui, components, pages, forms, navigation, layout, responsive, accessibility`

### Database
`db, schema, migration, query, model, orm, prisma, postgres`

### Testing
`test, unit, integration, e2e, mock, fixture`

### Infrastructure
`ci, cd, deploy, docker, kubernetes, aws, config`

## When to Apply Tags

1. **Creating new files**: Always add file-level tag
2. **Implementing tasks**: Reference task ID in all related code
3. **Modifying existing code**: Add block-level tag for significant changes
4. **Creating documents**: Include document tags section

## Tag Validation

Before committing, verify:
- [ ] All new files have file-level @peachflow tag
- [ ] Task references (T{XXX}) match tasks.md
- [ ] Epic/Story references are valid
- [ ] @see links point to existing files

## Benefits

- **Traceability**: Link code to requirements
- **Search**: Find all code for a task/story/epic
- **Review**: Understand context during code review
- **Maintenance**: Know why code exists
