---
name: implementation-context
description: |
  Use this skill when implementing tasks to get consolidated coding standards, quality checklists, and task management patterns. Reduces context usage by providing a single reference instead of multiple document reads.

  <example>
  Context: Agent starting implementation of any task
  user: "Implement the registration API"
  assistant: "Loading implementation-context for coding standards and quality requirements."
  <commentary>Agents load this skill once instead of reading 6+ separate documents.</commentary>
  </example>
---

# Implementation Context

Consolidated reference for all implementation tasks. Load this skill instead of reading multiple documents.

## Graph Tool Reference

```bash
# Task Operations
${CLAUDE_PLUGIN_ROOT}/scripts/peachflow-graph.py get task T-XXX    # Get task details
${CLAUDE_PLUGIN_ROOT}/scripts/peachflow-graph.py get story US-XXX  # Get user story
${CLAUDE_PLUGIN_ROOT}/scripts/peachflow-graph.py chain T-XXX       # Get full hierarchy

# Search Operations
${CLAUDE_PLUGIN_ROOT}/scripts/peachflow-graph.py list tasks --tag FE    # Find by tag
${CLAUDE_PLUGIN_ROOT}/scripts/peachflow-graph.py ready-tasks            # Unblocked tasks
${CLAUDE_PLUGIN_ROOT}/scripts/peachflow-graph.py depends blockers T-XXX # Check dependencies

# Status Management
${CLAUDE_PLUGIN_ROOT}/scripts/peachflow-graph.py update task T-XXX --status completed
${CLAUDE_PLUGIN_ROOT}/scripts/peachflow-graph.py stats  # Show progress
```

## Task Completion Checklist

After implementing any task:

```bash
# Mark task completed in graph
${CLAUDE_PLUGIN_ROOT}/scripts/peachflow-graph.py update task T-XXX --status completed
```

## Quality Standards by Role

### Backend [BE]
- [ ] Input validation on all endpoints
- [ ] Proper error handling with AppError class
- [ ] Authentication/authorization applied
- [ ] SQL injection prevention (parameterized queries)
- [ ] Passwords hashed (bcrypt)
- [ ] Sensitive data not logged
- [ ] Database transactions for multi-step operations

### Frontend [FE]
- [ ] All states handled (loading, error, empty, success)
- [ ] Follows existing project styling patterns
- [ ] Keyboard navigable (Tab, Enter, Escape)
- [ ] ARIA labels on interactive elements
- [ ] Works at all breakpoints
- [ ] No console errors/warnings

### DevOps [DevOps]
- [ ] Infrastructure as code (no manual steps)
- [ ] Secrets in environment variables or secret manager
- [ ] HTTPS everywhere
- [ ] Rollback strategy defined
- [ ] Monitoring in place

## Document Reference (Read Only When Needed)

| Need | Document Path |
|------|---------------|
| Product requirements | `docs/02-product/PRD.md` |
| Tech decisions | `docs/02-product/architecture/adr/` |
| Business context | `docs/01-business/BRD.md` |

## Output Format

**Return ONLY this format:**
```
Done: T-XXX completed
- [files created/modified]
- All acceptance criteria met
```

DO NOT add explanations, next steps, or summaries.
