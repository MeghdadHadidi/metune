---
name: peachflow:analyze
description: Analyze an existing codebase to onboard it to peachflow. Creates discovery documents based on implemented code and identifies technical debt.
allowed_tools: Read, Write, Edit, Grep, Glob, Bash, Task, AskUserQuestion
---

# Peachflow Analyze Command

Onboard an existing project to peachflow by analyzing the codebase and creating discovery documents based on what's already implemented.

## Output Responsibility

**CRITICAL**: This command is responsible for the unified output to the user.

- Sub-agents return minimal responses (just confirmation of what was done)
- DO NOT let agent responses bubble up to the user
- Collect results from all agents, then provide ONE final summary at the end
- Only this command suggests next steps, not the agents

## Pre-flight Check

**CRITICAL**: This command should only run on projects WITHOUT existing peachflow setup.

Check for existing setup:
```bash
# Check for peachflow state file
if [ -f ".peachflow-state.json" ]; then
  echo "ERROR: Project already has peachflow setup"
  exit 1
fi

# Check for peachflow docs structure
if [ -d "docs/01-business" ] || [ -d "docs/02-product" ]; then
  echo "WARNING: Existing docs structure found"
fi
```

If peachflow is already set up, inform the user:
> This project already has peachflow configured. Use `/peachflow:status` to see current state, or `/peachflow:plan` to continue planning.

## Workflow

### Phase 1: Codebase Analysis

Invoke the `codebase-analyst` agent to:

1. **Scan Project Structure**
   - Identify project type (web app, API, library, etc.)
   - Detect tech stack (languages, frameworks, databases)
   - Find configuration files
   - Map directory structure

2. **Analyze Dependencies**
   - Parse package.json, requirements.txt, go.mod, Cargo.toml, etc.
   - Identify key libraries and their purposes
   - Note version constraints

3. **Find Existing Documentation**
   - README files
   - Existing docs/ folders
   - Code comments and JSDoc/docstrings
   - API documentation

### Phase 2: Reverse Discovery

Based on codebase analysis, create peachflow documents:

1. **Business Context** (docs/01-business/)
   - `BRD.md` - Infer business requirements from implemented features
   - Mark assumptions with `[INFERRED: reason]`

2. **Product Definition** (docs/02-product/)
   - `PRD.md` - Document features based on code analysis
   - `user-personas.md` - Infer from user-facing code
   - `user-flows.md` - Extract from route/navigation patterns

3. **Architecture** (docs/02-product/architecture/)
   - `high-level-design.md` - Document actual architecture
   - `adr/` - Create ADRs for technology choices already made

4. **Requirements** (docs/03-requirements/)
   - `FRD.md` - Functional requirements from implementations
   - `NFRs.md` - Non-functional from configs (security, performance)

### Phase 3: Gap Analysis

Create technical debt and gap documentation:

1. **Technical Debt** (docs/05-debt/)
   - `technical-debt.md` - Code quality issues, outdated patterns
   - `security-gaps.md` - Security vulnerabilities found
   - `test-coverage.md` - Missing or incomplete tests

2. **Incomplete Features**
   - Partially implemented features
   - TODO/FIXME comments in code
   - Stubbed or mocked functionality

### Phase 4: Planning Setup

Prepare for peachflow planning:

1. Create `docs/04-plan/plan.md` with:
   - Completed work summary
   - Remaining work as potential epics
   - Technical debt items

2. Initialize `.peachflow-state.json` with:
   - Phase: "analyzed"
   - Analysis timestamp
   - Detected tech stack

### Phase 5: User Interview

Present findings to user for validation:

1. **Confirm Understanding**
   - Is the business context correct?
   - Are there missing features?
   - Priority of technical debt

2. **Define Next Steps**
   - What's the immediate priority?
   - Should debt be addressed first?
   - Ready to start planning?

## Output Structure

```
docs/
├── 01-business/
│   └── BRD.md              # Inferred business requirements
├── 02-product/
│   ├── PRD.md              # Documented features
│   ├── user-personas.md    # Inferred personas
│   ├── user-flows.md       # Extracted flows
│   └── architecture/
│       ├── high-level-design.md
│       └── adr/
│           ├── 0001-[tech-choice].md
│           └── ...
├── 03-requirements/
│   ├── FRD.md              # Functional requirements
│   └── NFRs.md             # Non-functional requirements
├── 04-plan/
│   └── plan.md             # Initial roadmap
├── 05-debt/
│   ├── technical-debt.md   # Code quality issues
│   ├── security-gaps.md    # Security findings
│   └── test-coverage.md    # Test gaps
├── analyze-report.md       # Analysis summary
└── clarification.md        # Open questions
```

## Markers

Use these markers in generated documents:

- `[INFERRED: reason]` - Assumption made during analysis
- `[NEEDS CLARIFICATION: question]` - Requires user input
- `[DEBT: description]` - Technical debt item
- `[GAP: description]` - Missing functionality

## Success Criteria

Analysis is complete when:
- [ ] Project structure documented
- [ ] Tech stack identified and documented in ADRs
- [ ] Business context inferred (BRD)
- [ ] Features documented (PRD, FRD)
- [ ] Architecture documented
- [ ] Technical debt catalogued
- [ ] User validated findings
- [ ] Ready for `/peachflow:plan`
