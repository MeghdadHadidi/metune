# Claude Code Plugins

Professional Claude Code plugins for streamlined software development workflows.

## Plugins

### Peachflow

**Professional product development workflow** - A comprehensive spec-driven development system that simulates a real software engineering team with specialized AI agents.

[Read Full Documentation →](metune/peachflow/README.md)

**Version**: 1.3.0
**License**: MIT

#### Quick Overview

Peachflow transforms Claude Code into a complete software development team with:
- Market research and product discovery
- Quarterly planning and task breakdown
- Visual POC development
- Spec-driven implementation
- Automated code review and testing

#### Key Features

- **14 Specialized AI Agents** - Domain consultant, product manager, UX researcher, designers, architects, engineers, QA, and more
- **5 Development Phases** - Discovery, Planning, POC (optional), Implementation, Testing
- **Spec-Driven Approach** - Everything documented before implementation
- **Git Worktrees** - Isolated quarterly development branches
- **Smart Model Selection** - Opus for decisions, Sonnet for execution, Haiku for operations

#### Installation

```bash
# Clone this repository
git clone https://github.com/MeghdadHadidi/claude-plugins.git

# Peachflow will be auto-discovered by Claude Code
# Or manually copy to plugins directory
cp -r claude-plugins/metune/peachflow ~/.claude/plugins/
```

#### Quick Start

```bash
# 1. Start product discovery
/peachflow:discover "An online exam platform for schools"

# 2. Create quarterly roadmap
/peachflow:plan

# 3. Plan specific quarter (creates git worktree)
/peachflow:plan Q1

# 4. Optional: Create visual POC
/peachflow:poc

# 5. Implement tasks
/peachflow:implement next

# 6. Run tests
/peachflow:test
```

---

## Repository Structure

```
claude-plugins/
├── README.md                    # This file
├── metune/
│   └── peachflow/              # Peachflow plugin
│       ├── README.md           # Detailed peachflow docs
│       ├── .claude-plugin/
│       │   └── plugin.json     # Plugin metadata
│       ├── agents/             # 14 specialized AI agents
│       ├── commands/           # 6 user commands
│       ├── skills/             # 4 auto-applied skills
│       ├── hooks/              # Event-driven automation
│       ├── scripts/            # Utility scripts
│       └── templates/          # Document templates
```

---

## Peachflow Workflow

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

---

## Peachflow Agents

### Product Team (Opus Model)

#### domain-consultant
**Market research and project knowledge expert**
- Conducts market research, competitor analysis, industry standards research
- Serves as the oracle for project-specific domain knowledge
- Automatically invoked by implementation agents for context
- Tools: WebSearch, WebFetch, Read, Write, Grep, Glob

**When to use**: First agent invoked during discovery; auto-consulted during implementation for user context, API specs, design guidance

#### product-manager
**Product vision and requirements leader**
- Creates comprehensive PRDs with problem statements, features, and requirements
- Defines quarterly roadmaps and feature prioritization
- Coordinates between design, engineering, and business
- Tools: Read, Write, Edit, Grep, Glob, Task, WebSearch

**When to use**: After domain research completes; quarterly planning; feature prioritization decisions

#### ux-researcher
**User research and behavioral analysis**
- Creates evidence-based user personas with demographics, goals, pain points
- Documents user journey maps with touchpoints and emotions
- Performs competitive UX analysis
- Tools: Read, Write, Grep, Glob, WebSearch, WebFetch, Task

**When to use**: Discovery phase for personas and journeys; understanding user experience flows

#### product-designer
**Design vision and visual identity**
- Establishes design principles, color psychology, emotional goals
- Defines design system foundations (tokens, spacing, typography)
- Creates visual direction and brand alignment
- Tools: Read, Write, Grep, Glob, WebSearch, WebFetch, Task

**When to use**: Discovery phase for design vision; design token definition; color palette decisions

### Engineering Leadership (Opus Model)

#### software-architect
**High-level architecture and tech stack decisions**
- Assesses technical feasibility and creates system architecture
- **CRITICAL**: Prioritizes simplicity over sophistication
- Interviews users for technology choices (database, framework, hosting)
- Defines integration points and non-functional requirements
- Tools: Read, Write, Edit, Grep, Glob, WebSearch, WebFetch, Task

**When to use**: After PRD and design; technology stack decisions; integration planning

**Key principle**: Avoid over-engineering. SQLite may be better than PostgreSQL for simple apps. Always interview users when multiple viable options exist.

### Engineering Team

#### frontend-engineer (Opus)
**Frontend architecture and design system implementation**
- Creates detailed frontend technical specifications
- Implements design tokens and component architecture
- Leads POC development with visual fidelity
- **Auto-consults domain-consultant** for user/design context
- Tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, Task

**When to use**: Quarter planning for frontend spec; POC development; UI component implementation

**Critical**: Always updates tasks.md status (pending → in_progress → complete)

#### backend-engineer (Sonnet)
**API design and data modeling**
- Creates API specifications with OpenAPI/REST contracts
- Designs database schemas and migration strategies
- Defines data model contracts and validation rules
- **Auto-consults domain-consultant** for API specs and architecture context
- Tools: Read, Write, Edit, Bash, Grep, Glob, WebSearch, Task

**When to use**: Quarter planning for backend spec; database schema design; API implementation

**Critical**: Always updates tasks.md status (pending → in_progress → complete)

#### tech-lead (Sonnet)
**Task breakdown and plan coordination**
- Converts quarterly plans into phased, executable tasks
- Reviews technical plans for feasibility and completeness
- Ensures dependency mapping and parallel work identification
- **CRITICAL**: Ensures local dev environment setup is high priority (T001 or T002)
- Tools: Read, Write, Edit, Grep, Glob, Task

**When to use**: Quarter planning for task breakdown; validating technical plans; coordinating product/engineering

**Local dev environment**: Must be defined during general planning and implemented early in Q1. Chooses simplest approach (npm run dev, docker-compose up).

#### developer (Sonnet)
**Task implementation with proper tagging**
- Implements features according to task specifications
- **MUST update tasks.md status** at task start and completion
- **Auto-consults domain-consultant** before implementing user-facing/complex tasks
- Follows coding standards, adds @peachflow tags
- Tools: Read, Write, Edit, Bash, Grep, Glob, Task

**When to use**: Implementing tasks from task breakdown

**Critical workflow**:
1. Read task → 2. Set in_progress → 3. Consult domain → 4. Implement → 5. Set complete

**Task Status Tracking**: Non-negotiable. Must update status immediately on start and completion.

### Quality Team

#### code-reviewer (Opus)
**Code quality and pattern compliance**
- Reviews for quality, correctness, type safety, security basics
- Verifies @peachflow tag presence and correctness
- Finds logic errors, edge cases, security issues
- Tools: Read, Grep, Glob, Bash

**When to use**: After task implementation completes; before commit checkpoints; explicit review requests

**Review levels**: Critical (block), Warning (fix before release), Suggestion (optional), Nitpick (ignore)

#### qa-engineer (Sonnet)
**Test planning and quality validation**
- Defines test strategy (unit, integration, E2E)
- Suggests test cases based on specifications
- Verifies acceptance criteria coverage
- Identifies cleanup opportunities
- Tools: Read, Write, Bash, Grep, Glob

**When to use**: After implementation for cleanup; /peachflow:test command; quality checkpoints before commits

### Support Team

#### workspace-manager (Haiku)
**Git worktree management**
- **Prepares git commands** for user to run manually (does NOT execute them)
- Follows branch naming convention: `{NNN}-Q{XX}-{product-slug}`
- Creates isolated worktrees for quarterly development
- Tools: Bash (read-only), Read, Write, Glob

**When to use**: Quarter planning with specific quarter (e.g., /peachflow:plan Q1)

**Critical**: NO automatic git mutations. Only prepares commands for user.

#### document-manager (Haiku)
**Spec document organization**
- Maintains proper file structure and version tracking
- Tracks document status (draft, review, approved, in-progress, complete)
- Manages cross-references between documents
- Tools: Read, Write, Edit, Grep, Glob

**When to use**: Loading task specs; document status summaries; directory initialization

#### clarification-agent (Sonnet)
**Ambiguity resolution**
- Scans documents for [NEEDS CLARIFICATION] markers
- Asks targeted questions (max 5 per round)
- Updates documents with answers and marks items [RESOLVED: date]
- Tools: Read, Write, Edit, Grep, Glob, AskUserQuestion

**When to use**: Auto-invoked after discovery and planning phases; manual /peachflow:clarify

---

## Peachflow Commands

| Command | Description | Git Branch |
|---------|-------------|------------|
| `/peachflow:discover` | Product discovery with market research, PRD, personas, design vision, architecture | No |
| `/peachflow:plan` | Create quarterly roadmap splitting product into deliverable quarters | No |
| `/peachflow:plan Q1` | Plan specific quarter with detailed tasks (creates git worktree) | Yes |
| `/peachflow:poc` | Create visual prototype with mocked data (optional) | Uses current |
| `/peachflow:implement` | Execute tasks from breakdown with code review and commits | Uses current |
| `/peachflow:test` | Run tests, analyze coverage, suggest cleanup (optional) | Uses current |
| `/peachflow:clarify` | Manually trigger clarification questions on documents | No |

---

## Peachflow Skills (Auto-Applied)

### tagging
**@peachflow tagging conventions**
- File-level tags: `@peachflow Q01/E01/US001/T003`
- Code block tags: `// @peachflow:T003 - Description`
- Document tags: `[TAGS: Q01, E01, US001, auth, oauth]`

Auto-applies when: Writing code files, adding comments, implementing tasks

### document-standards
**Document formatting and clarification markers**
- Clarification markers: `[NEEDS CLARIFICATION]`, `[ASSUMPTION]`, `[TBD]`, `[TODO]`
- Resolution markers: `[RESOLVED: date]`, `[DEFERRED: reason]`
- Writing conventions for PRDs, specs, architecture docs

Auto-applies when: Creating specs, PRDs, architecture docs, project documentation

### research-patterns
**Web search patterns for domain expertise**
- Query formulation: Market size, competitors, standards, best practices
- Search refinement with year qualifiers and authority sources
- Synthesis and citation standards

Auto-applies when: Conducting market research, competitor analysis, gathering domain knowledge

### file-organization
**File and directory organization patterns**
- Discovery structure: `specs/discovery/`
- Quarterly structure: `specs/quarterly/Q{XX}/`
- Worktree structure with isolated branches

Auto-applies when: Creating files, organizing documents, setting up project structure

---

## Model Selection Strategy

| Complexity | Model | Usage | Agents |
|------------|-------|-------|--------|
| High (decisions) | opus | Architecture, reviews, design vision, product strategy | software-architect, code-reviewer, product-manager, ux-researcher, product-designer, domain-consultant, frontend-engineer |
| Medium (execution) | sonnet | Implementation, task breakdown, testing | backend-engineer, tech-lead, developer, qa-engineer, clarification-agent |
| Low (operations) | haiku | File management, git operations, document organization | workspace-manager, document-manager |

**Cost optimization**: Use Opus for decisions that affect the entire project. Use Sonnet for execution. Use Haiku for operations.

---

## Directory Structure Examples

### After Discovery
```
specs/
└── discovery/
    ├── domain-research.md          # Market research, competitors
    ├── prd.md                       # Product requirements
    ├── user-personas.md             # User personas
    ├── user-journeys.md             # Journey maps
    ├── design-vision.md             # Design philosophy
    ├── color-psychology.md          # Color strategy
    ├── design-system-foundations.md # Design tokens
    ├── architecture.md              # High-level architecture
    └── clarifications.md            # Resolved questions
```

### After Planning
```
specs/
├── discovery/
└── quarterly/
    ├── roadmap.md              # Master quarterly roadmap
    ├── Q01-overview.md         # Q1 summary
    ├── Q02-overview.md         # Q2 summary
    └── Q03-overview.md         # Q3 summary
```

### After Quarter Planning (in worktree)
```
{worktree}/
└── specs/
    └── quarterly/
        └── Q01/
            ├── plan.md              # Quarter plan
            ├── frontend-spec.md     # Component architecture
            ├── backend-spec.md      # API specifications
            ├── data-contracts.md    # Data models
            └── tasks.md             # Task breakdown
```

---

## Git Workflow

1. **Discovery & Roadmap**: Work on main branch, no commits
2. **Quarter Planning**: Creates worktree `{repo}--{NNN}-Q{XX}-{slug}`
3. **Implementation**: Commits after each phase
4. **Completion**: PR to main, cleanup worktree

### Worktree Example
```bash
# workspace-manager prepares these commands (does NOT run them)
git branch 001-Q01-exam-platform
git worktree add "../mocket-v3--001-Q01-exam-platform" 001-Q01-exam-platform
cd "../mocket-v3--001-Q01-exam-platform"
mkdir -p specs/quarterly/Q01
```

---

## Tagging System

### File-Level Tags
```typescript
/**
 * @peachflow Q01/E01/US001/T003
 * @description OAuth callback handler for Google authentication
 * @tags auth, oauth, google, api
 * @see specs/quarterly/Q01/tasks.md#T003
 */
```

### Code Block Tags
```typescript
// @peachflow:T003 - Token validation logic
function validateToken(token: string): boolean {
  // Implementation
}
```

### Document Tags
```markdown
### T003: Implement OAuth callback
[TAGS: Q01, E01, US001, auth, oauth, api]
```

---

## Key Principles

### Spec-Driven Development
- Everything documented before implementation
- Specs created during discovery and planning
- Implementation follows specs exactly
- Specs serve as single source of truth

### Task Status Tracking
- **Critical**: tasks.md status must be updated immediately
- Lifecycle: `pending` → `in_progress` → `complete`
- Developer/engineer agents MUST update status
- No proceeding to next task without marking current complete

### Domain Consultant Integration
- Implementation agents auto-consult domain-consultant
- Frontend: Gets user personas, journey context, design expectations
- Backend: Gets API specs, data models, architecture decisions
- Ensures implementation aligns with discovery phase

### Local Development Environment
- High priority task in Q1 (T001 or T002)
- Must be defined during general planning
- Prioritize simplest approach (npm run dev, docker-compose up)
- Single-command startup preferred
- Include seed data for immediate testing

### Simplicity Over Sophistication
- Avoid over-engineering
- Choose boring, proven technologies
- Minimize dependencies
- Match complexity to scale
- Interview users when multiple viable options exist

---

## Hooks

| Event | Action |
|-------|--------|
| SessionStart | Detect context (main vs feature branch), show available commands |
| PreToolUse (Write) | Validate no sensitive files being written |
| PostToolUse (Edit) | Run formatters, check for proper @peachflow tags |
| Stop | Verify no incomplete tasks in tasks.md |

---

## Contributing

Contributions welcome! Please submit issues and pull requests.

---

## License

MIT License - See individual plugin directories for details.

---

## Links

- **Repository**: https://github.com/MeghdadHadidi/claude-plugins
- **Peachflow**: https://github.com/MeghdadHadidi/peachflow
- **Claude Code**: https://claude.com/claude-code

---

## Support

For issues, questions, or feature requests:
- Open an issue on GitHub
- Check the [Peachflow README](metune/peachflow/README.md) for detailed documentation
