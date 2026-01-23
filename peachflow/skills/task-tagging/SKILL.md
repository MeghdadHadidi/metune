---
name: task-tagging
description: |
  Use this skill when creating or working with implementation tasks. Applies when breaking down user stories into tasks or when picking tasks for implementation.
---

# Task Tagging System

## Tag Types

Tasks are tagged by the type of work required:

| Tag | Meaning | Agent |
|-----|---------|-------|
| [FE] | Frontend work | frontend-developer |
| [BE] | Backend work | backend-developer |
| [DevOps] | Infrastructure work | devops-engineer |
| [Full] | Full-stack work | frontend + backend |

## Tag Placement

Tags appear at the start of task titles:

```markdown
# T-001: [BE] Implement user registration API
# T-002: [FE] Build registration form component
# T-003: [DevOps] Configure email service
# T-004: [Full] Implement real-time notifications
```

## Tag Guidelines

### [FE] - Frontend

Use for tasks involving:
- UI components
- Forms and validation
- Client-side state
- Styling and layout
- Client-side routing
- Frontend tests

Examples:
- [FE] Build login form with validation
- [FE] Create dashboard layout
- [FE] Implement responsive navigation

### [BE] - Backend

Use for tasks involving:
- API endpoints
- Database operations
- Authentication/authorization
- Business logic
- Server-side validation
- Backend tests

Examples:
- [BE] Create user registration endpoint
- [BE] Implement JWT authentication
- [BE] Build search API with filters

### [DevOps] - Infrastructure

Use for tasks involving:
- CI/CD pipelines
- Cloud infrastructure
- Deployment scripts
- Monitoring/alerting
- Environment setup
- Security configuration

Examples:
- [DevOps] Set up GitHub Actions workflow
- [DevOps] Configure production database
- [DevOps] Implement health check endpoints

### [Full] - Full-stack

Use only when:
- Task requires coordinated FE+BE changes
- Splitting would create artificial dependencies
- Single developer should own both sides

Examples:
- [Full] Implement WebSocket real-time updates
- [Full] Add file upload with preview

## Finding Tagged Tasks

To find all tasks of a type:

```bash
# Find all frontend tasks
grep -r "\[FE\]" docs/04-plan/quarters/*/tasks/ --include="*.md"

# Find all backend tasks
grep -r "\[BE\]" docs/04-plan/quarters/*/tasks/ --include="*.md"

# Find all devops tasks
grep -r "\[DevOps\]" docs/04-plan/quarters/*/tasks/ --include="*.md"
```

Or use the checklist manager:
```bash
${CLAUDE_PLUGIN_ROOT}/scripts/checklist-manager.sh find-tagged docs/04-plan/quarters/q01/tasks "FE"
```

## Parallel Execution

Tasks with the same tag can often run in parallel if no dependencies:

```markdown
## Parallel Group 1
- T-001: [BE] Create registration API
- T-002: [FE] Build registration form (parallel with T-001)
- T-007: [DevOps] Set up email service (parallel)

## Sequential (T-003 depends on T-001)
- T-003: [BE] Create login API (depends on T-001 for user model)
```

## Task File Format

```markdown
---
id: T-001
title: "[BE] Implement user registration API"
epic: E-001
story: US-001
status: pending
depends_on: []
parallel_with: [T-002, T-007]
---

# T-001: [BE] Implement user registration API

## Description
[What needs to be done]

## Acceptance Criteria
- [ ] [Criterion 1]
- [ ] [Criterion 2]

## Technical Notes
[Implementation guidance]
```
