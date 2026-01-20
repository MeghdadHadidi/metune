# Peachflow Plugin

Professional product development workflow for Claude Code, simulating a real software engineering team.

## Overview

Peachflow provides a structured spec-driven development workflow with:
- **Discovery Phase**: Market research, PRD, user personas, design vision, architecture
- **Planning Phase**: Quarterly roadmaps, detailed task breakdowns
- **POC Phase** (optional): Visual prototypes with mocked data
- **Implementation Phase**: Task execution with code review and commits
- **Testing Phase** (optional): Test running and cleanup suggestions

## Architecture

**Commands** (explicit user invocation):
- `/peachflow:discover`, `/peachflow:plan`, `/peachflow:poc`, `/peachflow:implement`, `/peachflow:test`, `/peachflow:clarify`

**Agents** (auto-invoked by commands):
- domain-consultant, product-manager, ux-researcher, product-designer, software-architect, frontend-engineer, backend-engineer, tech-lead, developer, code-reviewer, qa-engineer, workspace-manager, document-manager, clarification-agent

**Skills** (auto-applied knowledge):
- tagging conventions, file organization, research patterns, document standards

## Quick Start

```bash
# Install plugin
cp -r peachflow-plugin ~/.claude/plugins/

# Start product discovery
/peachflow:discover "An online exam platform for schools"

# Create quarterly roadmap
/peachflow:plan

# Plan specific quarter (creates git worktree)
/peachflow:plan Q1

# Optional: Create visual POC
/peachflow:poc

# Implement tasks
/peachflow:implement next

# Run tests
/peachflow:test
```

## Workflow

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              PEACHFLOW WORKFLOW                             │
├─────────────────────────────────────────────────────────────────────────────┤
│                                                                             │
│  /peachflow:discover                                                        │
│       │                                                                     │
│       ├──→ domain-consultant (market research, competitors)                 │
│       ├──→ product-manager (PRD)                                           │
│       ├──→ ux-researcher (personas, journeys)                              │
│       ├──→ product-designer (design vision, colors)                        │
│       ├──→ software-architect (high-level architecture)                    │
│       └──→ clarification-agent (questions)                                 │
│       │                                                                     │
│       ▼                                                                     │
│  specs/discovery/  [No git branch]                                         │
│                                                                             │
│  /peachflow:plan (no args)                                                 │
│       │                                                                     │
│       ├──→ product-manager + tech-lead (quarterly split)                   │
│       └──→ clarification-agent (questions)                                 │
│       │                                                                     │
│       ▼                                                                     │
│  specs/quarterly/roadmap.md  [No git branch]                               │
│                                                                             │
│  /peachflow:plan Q1                                                        │
│       │                                                                     │
│       ├──→ workspace-manager (create git worktree)                         │
│       ├──→ frontend-engineer (detailed frontend spec)                      │
│       ├──→ backend-engineer (API specs, data contracts)                    │
│       ├──→ tech-lead (task breakdown)                                      │
│       └──→ clarification-agent (questions)                                 │
│       │                                                                     │
│       ▼                                                                     │
│  {worktree}/specs/quarterly/Q01/  [Feature branch]                         │
│                                                                             │
│  /peachflow:poc (optional)                                                 │
│       │                                                                     │
│       └──→ frontend-engineer (visual prototype)                            │
│                                                                             │
│  /peachflow:implement T001                                                 │
│       │                                                                     │
│       ├──→ developer (implementation)                                      │
│       ├──→ code-reviewer (quality check)                                   │
│       └──→ qa-engineer (cleanup suggestions)                               │
│       │                                                                     │
│       ▼                                                                     │
│  [Code with @peachflow tags]                                               │
│                                                                             │
│  /peachflow:test (optional)                                                │
│       │                                                                     │
│       └──→ qa-engineer (test report, cleanup)                              │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

## Commands

| Command | Description | Git Branch |
|---------|-------------|------------|
| `/peachflow:discover` | Product discovery with all research | No |
| `/peachflow:plan` | Create quarterly roadmap | No |
| `/peachflow:plan Q1` | Plan specific quarter | Yes (worktree) |
| `/peachflow:poc` | Create visual prototype | Uses current |
| `/peachflow:implement` | Execute tasks | Uses current |
| `/peachflow:test` | Run tests and cleanup | Uses current |
| `/peachflow:clarify` | Ask clarification questions | No |

## Agents

### Product Team
| Agent | Model | Role |
|-------|-------|------|
| product-manager | opus | PRD, requirements, quarterly planning |
| ux-researcher | opus | User personas, journey maps |
| product-designer | opus | Design vision, color psychology |

### Engineering Team
| Agent | Model | Role |
|-------|-------|------|
| software-architect | opus | High-level architecture, tech decisions |
| frontend-engineer | opus | Design systems, component architecture |
| backend-engineer | sonnet | API specs, data contracts |
| tech-lead | sonnet | Task breakdown, plan review |
| developer | sonnet | Implementation |

### Quality Team
| Agent | Model | Role |
|-------|-------|------|
| code-reviewer | opus | Code quality, patterns |
| qa-engineer | sonnet | Test suggestions, cleanup |

### Support
| Agent | Model | Role |
|-------|-------|------|
| domain-consultant | opus | Market research, industry standards |
| clarification-agent | sonnet | Questions after each phase |
| workspace-manager | haiku | Git worktree management |
| document-manager | haiku | File organization |

## Model Selection Strategy

| Complexity | Model | Usage |
|------------|-------|-------|
| High (decisions) | opus | Architecture, reviews, design vision |
| Medium (execution) | sonnet | Implementation, task breakdown |
| Low (operations) | haiku | File management, git operations |

## Directory Structure

### After Discovery
```
specs/
└── discovery/
    ├── domain-research.md
    ├── prd.md
    ├── user-personas.md
    ├── user-journeys.md
    ├── design-vision.md
    ├── color-psychology.md
    ├── design-system-foundations.md
    ├── architecture.md
    └── clarifications.md
```

### After Planning
```
specs/
├── discovery/
└── quarterly/
    ├── roadmap.md
    ├── Q01-overview.md
    ├── Q02-overview.md
    └── Q03-overview.md
```

### After Quarter Planning (in worktree)
```
{worktree}/
└── specs/
    └── quarterly/
        └── Q01/
            ├── plan.md
            ├── frontend-spec.md
            ├── backend-spec.md
            ├── data-contracts.md
            └── tasks.md
```

## Tagging System

### File-Level Tags
```typescript
/**
 * @peachflow Q01/E01/US001/T003
 * @description OAuth callback handler
 * @tags auth, oauth, api
 * @see specs/quarterly/Q01/tasks.md#T003
 */
```

### Code Block Tags
```typescript
// @peachflow:T003 - Token validation
function validateToken(token: string) { ... }
```

### Document Tags
```markdown
### T003: Implement OAuth callback
[TAGS: Q01, E01, US001, auth, oauth, api]
```

## Clarification Markers

Documents use markers for items needing clarification:
- `[NEEDS CLARIFICATION: question]`
- `[ASSUMPTION: statement]`
- `[TBD]`
- `[TODO]`

After clarification:
- `[RESOLVED: date]`

## Git Workflow

1. **Discovery & Roadmap**: Work on main, no commits
2. **Quarter Planning**: Creates worktree `{repo}--{NNN}-Q{XX}-{slug}`
3. **Implementation**: Commits after each phase
4. **Completion**: PR to main, cleanup worktree

## Hooks

| Event | Action |
|-------|--------|
| SessionStart | Detect context, show available commands |
| PreToolUse (Write) | Validate no sensitive files |
| PostToolUse (Edit) | Run formatters, check for tags |
| Stop | Verify no incomplete tasks |

## Installation

```bash
cp -r peachflow-plugin ~/.claude/plugins/
```

## License

MIT
