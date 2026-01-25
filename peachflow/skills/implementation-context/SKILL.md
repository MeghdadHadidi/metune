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

## Utility Scripts Reference

```bash
# Task Operations
${CLAUDE_PLUGIN_ROOT}/scripts/doc-parser.sh task T-XXX      # Get task details
${CLAUDE_PLUGIN_ROOT}/scripts/doc-parser.sh acceptance T-XXX # Get acceptance criteria
${CLAUDE_PLUGIN_ROOT}/scripts/doc-parser.sh story US-XXX    # Get user story
${CLAUDE_PLUGIN_ROOT}/scripts/doc-parser.sh fr FR-XXX       # Get functional requirement
${CLAUDE_PLUGIN_ROOT}/scripts/doc-parser.sh nfr NFR-XXX     # Get non-functional requirement
${CLAUDE_PLUGIN_ROOT}/scripts/doc-parser.sh adr NNNN        # Get architecture decision

# Search Operations
${CLAUDE_PLUGIN_ROOT}/scripts/doc-search.sh tag [FE|BE|DevOps]  # Find tasks by tag
${CLAUDE_PLUGIN_ROOT}/scripts/doc-search.sh deps T-XXX          # Check dependencies
${CLAUDE_PLUGIN_ROOT}/scripts/doc-search.sh keyword "term" [area] # Search docs

# Status Management
${CLAUDE_PLUGIN_ROOT}/scripts/checklist-manager.sh status "path/to/task.md" "in_progress|completed"
${CLAUDE_PLUGIN_ROOT}/scripts/checklist-manager.sh check "path/to/file.md" "item text"
${CLAUDE_PLUGIN_ROOT}/scripts/checklist-manager.sh count "path/to/task.md"
```

## Task Completion Checklist

After implementing any task:

```bash
# 1. Mark task completed
${CLAUDE_PLUGIN_ROOT}/scripts/checklist-manager.sh status \
  "docs/04-plan/quarters/${quarter}/tasks/NNN.md" "completed"

# 2. Update stories.md
${CLAUDE_PLUGIN_ROOT}/scripts/checklist-manager.sh check \
  "docs/04-plan/quarters/${quarter}/stories.md" "T-NNN"

# 3. Update plan.md
${CLAUDE_PLUGIN_ROOT}/scripts/checklist-manager.sh check \
  "docs/04-plan/quarters/${quarter}/plan.md" "T-NNN"
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
- [ ] Uses only design tokens (no hardcoded values)
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
| API contracts | `docs/02-product/architecture/high-level-design.md` |
| Tech decisions | `docs/02-product/architecture/adr/` |
| UI specs | `docs/03-design/ux/ui-specifications.md` |
| Components | `docs/03-design/ux/component-library.md` |
| Design tokens | `docs/03-design/ux/design-system.md` |
| Interactions | `docs/03-design/ux/interaction-specs.md` |
| Accessibility | `docs/03-design/ux/accessibility-guidelines.md` |
| NFRs | `docs/03-requirements/NFRs.md` |

## Output Format

**Return ONLY this format:**
```
Done: T-XXX completed
- [files created/modified]
- All acceptance criteria met
```

DO NOT add explanations, next steps, or summaries.
