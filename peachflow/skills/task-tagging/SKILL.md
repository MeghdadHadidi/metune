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

To find tasks by tag, use the graph tool:

```bash
# Find all frontend tasks
${CLAUDE_PLUGIN_ROOT}/scripts/peachflow-graph.py list tasks --tag FE

# Find all backend tasks
${CLAUDE_PLUGIN_ROOT}/scripts/peachflow-graph.py list tasks --tag BE

# Find all devops tasks
${CLAUDE_PLUGIN_ROOT}/scripts/peachflow-graph.py list tasks --tag DevOps

# Find ready (unblocked) tasks
${CLAUDE_PLUGIN_ROOT}/scripts/peachflow-graph.py ready-tasks
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

## Task Structure in Graph

Tasks are stored in `.peachflow-graph.json`:

```json
{
  "entities": {
    "tasks": {
      "T-001": {
        "id": "T-001",
        "title": "Implement user registration API",
        "tag": "BE",
        "storyId": "US-001",
        "description": "POST /api/users with validation",
        "status": "pending"
      }
    }
  },
  "relationships": {
    "task_dependencies": {
      "T-003": ["T-001"]
    }
  }
}
```
