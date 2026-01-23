---
name: peachflow:analyze
description: Analyze an existing codebase to prepare for peachflow integration. Creates analyze-report.md that can be used by discover command. Use when adding peachflow to a project already in progress.
argument-hint: "[optional: context description of the project]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Task, WebSearch
---

# /peachflow:analyze - Existing Project Analysis

Analyze an existing codebase to understand its structure, technologies, and state. Creates a foundation for integrating peachflow into projects already in progress.

## When to Use

- Adding peachflow to an existing project
- Project has existing code that needs to be understood
- Want to run discovery on a partially-built product
- Need to create a roadmap for completing an existing project

## Prerequisites

- Must be in a directory with existing code
- Project should have some structure (not empty)

---

## Workflow

### Step 1: Codebase Discovery

**Auto-invoke**: Explore agent (thorough)

Analyze the codebase to understand:

#### Project Structure
```bash
# Get directory structure
find . -type f -name "*.ts" -o -name "*.tsx" -o -name "*.js" -o -name "*.jsx" \
  -o -name "*.py" -o -name "*.go" -o -name "*.rs" \
  | head -100

# Check for common config files
ls -la package.json tsconfig.json .env.example Cargo.toml go.mod pyproject.toml 2>/dev/null
```

#### Technology Detection
- **Package managers**: package.json, Cargo.toml, go.mod, pyproject.toml
- **Frameworks**: Next.js, React, Vue, Django, FastAPI, etc.
- **Databases**: Prisma schema, migrations, ORMs
- **Infrastructure**: Docker, Kubernetes, CI/CD configs

#### Code Analysis
- Entry points and main modules
- API routes and endpoints
- Database models and schemas
- UI components and pages
- Tests and coverage

### Step 2: Architecture Understanding

Identify and document:

1. **Frontend Architecture**
   - Framework and libraries
   - Component structure
   - State management
   - Routing approach
   - Styling solution

2. **Backend Architecture**
   - Runtime and framework
   - API design (REST/GraphQL/tRPC)
   - Database and ORM
   - Authentication method
   - External integrations

3. **Infrastructure**
   - Hosting approach
   - CI/CD pipeline
   - Environment configuration
   - Deployment strategy

### Step 3: Progress Assessment

Evaluate what's been built:

1. **Feature Completeness**
   - What features are working?
   - What features are partially done?
   - What features are planned but not started?
   - What's broken or needs refactoring?

2. **Code Quality**
   - Test coverage
   - Type safety
   - Code organization
   - Documentation state

3. **Technical Debt**
   - Known issues
   - TODO/FIXME comments
   - Outdated dependencies
   - Performance concerns

### Step 4: Context Integration

If user provided context argument, integrate it:
- Business context
- Team information
- Timeline constraints
- Priority areas

---

## Output

Create `specs/discovery/analyze-report.md`:

```markdown
---
product: {detected-or-provided-name}
document: analyze-report
version: 1.0
status: analyzed
created: {date}
source: existing-codebase
---

# Codebase Analysis Report: {Project Name}

## Executive Summary

{2-3 paragraph overview of what this project is, its current state, and key findings}

---

## Project Overview

### Detected Purpose
{What this application appears to do based on code analysis}

### User-Provided Context
{Context from the optional argument, or "[Not provided - see NEEDS CLARIFICATION below]"}

---

## Technology Stack (Detected)

### Frontend
| Layer | Technology | Version | Confidence |
|-------|------------|---------|------------|
| Framework | {e.g., React} | {version} | High/Medium/Low |
| State | {e.g., Zustand} | {version} | High/Medium/Low |
| Styling | {e.g., Tailwind} | {version} | High/Medium/Low |
| Build | {e.g., Vite} | {version} | High/Medium/Low |

### Backend
| Layer | Technology | Version | Confidence |
|-------|------------|---------|------------|
| Runtime | {e.g., Node.js} | {version} | High/Medium/Low |
| Framework | {e.g., Express} | {version} | High/Medium/Low |
| ORM | {e.g., Prisma} | {version} | High/Medium/Low |
| Database | {e.g., PostgreSQL} | {version} | High/Medium/Low |

### Infrastructure
| Component | Technology | Detected From |
|-----------|------------|---------------|
| CI/CD | {e.g., GitHub Actions} | {file path} |
| Hosting | {e.g., Vercel} | {file path} |
| Containers | {e.g., Docker} | {file path} |

---

## Code Structure

### Directory Layout
```
{project-name}/
├── src/
│   ├── app/           # {description}
│   ├── components/    # {description}
│   ├── api/           # {description}
│   └── lib/           # {description}
├── prisma/            # {description}
└── tests/             # {description}
```

### Key Files
| File | Purpose | Notes |
|------|---------|-------|
| {path} | {purpose} | {notes} |

---

## Features Assessment

### Implemented Features
| Feature | Status | Quality | Location |
|---------|--------|---------|----------|
| User Authentication | Complete | Good | src/api/auth/ |
| Dashboard | Partial | Needs work | src/app/dashboard/ |
| {Feature} | {Status} | {Quality} | {Path} |

### Partially Implemented
| Feature | What's Done | What's Missing | Effort to Complete |
|---------|-------------|----------------|-------------------|
| {Feature} | {done} | {missing} | S/M/L |

### Not Started (Detected from code comments/TODO)
| Feature | Evidence | Priority Guess |
|---------|----------|----------------|
| {Feature} | {where found} | High/Medium/Low |

---

## Code Quality Assessment

### Test Coverage
- **Unit Tests**: {count} files, {coverage}% coverage
- **Integration Tests**: {count} files
- **E2E Tests**: {count} files
- **Overall Status**: {Good/Fair/Poor}

### Type Safety
- **TypeScript**: {Yes/No/Partial}
- **Strict Mode**: {Yes/No}
- **Any Count**: {count} instances of `any`

### Code Organization
- **Follows conventions**: {Yes/Mostly/No}
- **Component structure**: {Consistent/Inconsistent}
- **API organization**: {Consistent/Inconsistent}

### Documentation
- **README**: {Exists/Missing/Outdated}
- **API docs**: {Exists/Missing/Outdated}
- **Code comments**: {Good/Sparse/None}

---

## Technical Debt

### Critical Issues
| Issue | Location | Impact | Effort to Fix |
|-------|----------|--------|---------------|
| {issue} | {path} | High/Medium/Low | S/M/L |

### TODO/FIXME Items
| Comment | Location | Type |
|---------|----------|------|
| {comment} | {path}:{line} | TODO/FIXME/HACK |

### Outdated Dependencies
| Package | Current | Latest | Risk |
|---------|---------|--------|------|
| {package} | {current} | {latest} | High/Medium/Low |

---

## Migration Considerations

### Breaking Changes Needed
[NEEDS CLARIFICATION: Confirm these potential breaking changes are acceptable]

| Change | Why Needed | Impact | Alternatives |
|--------|------------|--------|--------------|
| {change} | {reason} | {impact} | {alternatives} |

### Data Migration
[NEEDS CLARIFICATION: What data exists that needs migration?]

| Data | Current State | Proposed Change |
|------|---------------|-----------------|
| {data type} | {current} | {proposed} |

---

## Recommendations

### Immediate Actions
1. {Action 1}
2. {Action 2}
3. {Action 3}

### Before Discovery Phase
[NEEDS CLARIFICATION: Confirm these items before proceeding to discovery]

1. **Project purpose and goals** - {detected purpose, confirm or correct}
2. **Target users** - {if detectable from code, otherwise "Unknown"}
3. **Completion status** - {X}% complete, {Y} features remaining
4. **Priority** - What should be built next?

### Technical Recommendations
1. {Recommendation 1}
2. {Recommendation 2}

---

## Information for Discovery

The following should be used by the discover command:

### Product Summary
{Brief description suitable for PRD introduction}

### Existing Tech Decisions
These technology choices are already made:
- Frontend: {stack}
- Backend: {stack}
- Database: {database}
- Hosting: {hosting}

### Existing Features (Don't Re-plan)
These features exist and should be documented, not re-planned:
{list of features}

### Gaps to Fill (Focus Discovery Here)
These areas need discovery attention:
{list of gaps}

### Questions for User
[NEEDS CLARIFICATION: These questions must be answered before discovery can proceed]

1. {Question about project purpose if unclear}
2. {Question about target users}
3. {Question about priorities}
4. {Question about breaking changes}

---

## Appendix

### Files Analyzed
- Total files scanned: {count}
- Code files: {count}
- Config files: {count}
- Test files: {count}

### Analysis Timestamp
- Analyzed: {timestamp}
- Git commit: {commit hash if available}
```

---

## Integration with Other Commands

### /peachflow:discover Integration

When `/peachflow:discover` is called without arguments:
1. Check if `specs/discovery/analyze-report.md` exists
2. If yes, read the "Information for Discovery" section
3. Use detected tech stack as constraints (don't change what exists)
4. Focus discovery on gaps identified
5. Pre-populate PRD with existing features

### /peachflow:plan Integration

When planning for existing projects:
1. Consider existing code as "done" work
2. Plan only for gaps and new features
3. Mark migration tasks as `[NEEDS CLARIFICATION]` for user approval
4. Don't re-architect what's working

---

## Usage Examples

```bash
# Analyze without context
/peachflow:analyze

# Analyze with context
/peachflow:analyze "This is an online exam platform for schools. We've built auth and basic UI, need to add exam creation and anti-cheating."

# Analyze with detailed context
/peachflow:analyze "E-commerce platform, React + Node stack, about 60% complete. Team of 3 developers. Need to prioritize checkout flow and inventory management."
```

---

## Collaboration Flow

```
/peachflow:analyze [context]
         │
         ▼
┌─────────────────────────────────────────┐
│  Step 1: Scan Codebase                  │
│  - Directory structure                  │
│  - Technology detection                 │
│  - Config file analysis                 │
└─────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│  Step 2: Analyze Architecture           │
│  - Frontend stack                       │
│  - Backend stack                        │
│  - Infrastructure                       │
└─────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│  Step 3: Assess Progress                │
│  - What's complete                      │
│  - What's partial                       │
│  - What's missing                       │
└─────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│  Step 4: Generate Report                │
│  - Create analyze-report.md             │
│  - Mark clarification needs             │
└─────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│  Step 5: Clarification                  │
│  - Ask user to confirm findings         │
│  - Resolve [NEEDS CLARIFICATION]        │
└─────────────────────────────────────────┘
         │
         ▼
[Ready for /peachflow:discover]
```

---

## Notes

- This command creates foundation for discovery, not a full PRD
- Existing tech choices are treated as constraints, not suggestions
- Focus is on understanding what exists, not judging it
- Migration recommendations are marked for user approval
- analyze-report.md becomes input to discover command
