---
name: peachflow:discover
description: Start product discovery phase. Conducts market research, creates PRD, user personas, design vision, and technical feasibility assessment. No git branch created.
argument-hint: "[product idea description]"
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Grep, Glob, WebSearch, WebFetch, Task, AskUserQuestion
---

# /peachflow:discover - Product Discovery Phase

Comprehensive product discovery creating all foundational documents before planning begins.

## Overview

Discovery is the foundation of successful product development. This phase produces:
- Market & domain research
- Product Requirements Document (PRD)
- User personas and journey maps
- Design vision and color psychology
- High-level system architecture

**No git branch is created during discovery.** The output informs quarterly planning.

---

## IMPORTANT: Existing Project Support

### If No Prompt Argument Provided

Before starting discovery, check for an analyze report:

```bash
# Check if analyze-report.md exists
if [ -f "specs/discovery/analyze-report.md" ]; then
  echo "Found analyze report - using as discovery input"
fi
```

**If `specs/discovery/analyze-report.md` exists:**
1. Read the "Information for Discovery" section
2. Use detected tech stack as **fixed constraints** (don't suggest alternatives)
3. Use "Product Summary" as starting point for PRD
4. Document "Existing Features" in PRD as already built
5. Focus discovery efforts on "Gaps to Fill"
6. Pre-resolve tech decisions that are already made

**If no analyze-report.md and no prompt:**
1. Ask user: "No product description provided and no analyze-report.md found. Please either:
   - Provide a product description: `/peachflow:discover "your product idea"`
   - Or run `/peachflow:analyze` first for existing projects"
2. Do not proceed until input is provided

### Existing Project Discovery Workflow

When building on analyze-report.md:

```
analyze-report.md exists
         │
         ▼
┌─────────────────────────────────────────┐
│  Read "Information for Discovery"       │
│  - Product Summary                      │
│  - Existing Tech Decisions              │
│  - Existing Features                    │
│  - Gaps to Fill                         │
└─────────────────────────────────────────┘
         │
         ▼
┌─────────────────────────────────────────┐
│  Lock-in Constraints                    │
│  - Tech stack is FIXED                  │
│  - Existing features are DONE           │
│  - Focus on GAPS only                   │
└─────────────────────────────────────────┘
         │
         ▼
   Continue with normal workflow,
   but with constraints applied
```

---

## Workflow

Execute these phases sequentially, automatically invoking the appropriate agents:

### Phase 1: Domain Research
**Auto-invoke**: domain-consultant agent

1. **Market Research**
   - Industry size and growth
   - Key players and market share
   - Emerging trends

2. **Competitor Analysis**
   - Feature comparison
   - Pricing strategies
   - UX patterns

3. **Industry Standards**
   - Regulatory requirements
   - Compliance needs
   - Best practices

4. **Technology Landscape**
   - Available solutions
   - Integration requirements
   - Technical constraints

**Output**: `specs/discovery/domain-research.md`

---

### Phase 2: Product Definition
**Auto-invoke**: product-manager agent

Working with domain research:
1. **Problem Definition**
   - Current state analysis
   - Pain points identification
   - Opportunity sizing

2. **Product Vision**
   - Vision statement
   - Success metrics
   - Feature prioritization

3. **Requirements**
   - Functional requirements
   - Non-functional requirements
   - Constraints and assumptions

**Output**: `specs/discovery/prd.md`

Mark items needing clarification:
- `[NEEDS CLARIFICATION: target audience details]`
- `[NEEDS CLARIFICATION: monetization strategy]`
- `[NEEDS CLARIFICATION: timeline constraints]`

---

### Phase 3: User Research
**Auto-invoke**: ux-researcher agent

1. **User Personas**
   - Primary and secondary personas
   - Demographics, goals, pain points
   - Current behavior patterns

2. **User Journeys**
   - Key journey maps
   - Touchpoints and emotions
   - Pain points and opportunities

3. **Competitive UX Analysis**
   - UX strengths/weaknesses of competitors
   - Differentiation opportunities

**Output**:
- `specs/discovery/user-personas.md`
- `specs/discovery/user-journeys.md`

---

### Phase 4: Design Vision
**Auto-invoke**: product-designer agent

1. **Design Philosophy**
   - Design principles
   - Emotional goals
   - Visual direction

2. **Color Psychology**
   - Color strategy for target emotions
   - Industry color conventions
   - Accessibility considerations

3. **Design System Foundations**
   - Token architecture
   - Typography direction
   - Spacing philosophy

**Output**:
- `specs/discovery/design-vision.md`
- `specs/discovery/color-psychology.md`
- `specs/discovery/design-system-foundations.md`

---

### Phase 5: Technical Feasibility
**Auto-invoke**: software-architect agent

1. **System Overview**
   - System boundaries
   - Major components
   - External dependencies

2. **Technology Assessment**
   - Tech stack recommendations
   - Integration requirements
   - Technical risks

3. **Architecture**
   - High-level architecture diagram
   - Component responsibilities
   - Communication patterns

**Output**: `specs/discovery/architecture.md`

Mark items needing clarification:
- `[NEEDS CLARIFICATION: scale expectations]`
- `[NEEDS CLARIFICATION: integration requirements]`
- `[NEEDS CLARIFICATION: infrastructure preferences]`

---

### Phase 6: Clarification Round
**Auto-invoke**: clarification-agent

1. Scan all documents for `[NEEDS CLARIFICATION]` markers
2. Ask targeted questions (max 5 per round)
3. Update documents with answers
4. Mark resolved items
5. Generate clarification summary

**Output**: `specs/discovery/clarifications.md`

---

## Input

```
/peachflow:discover "An online exam platform for schools that allows teachers to create exams and students to take them with anti-cheating measures"
```

## Output Structure

```
specs/
└── discovery/
    ├── domain-research.md        # Market, competitors, standards
    ├── prd.md                    # Product requirements
    ├── user-personas.md          # User personas
    ├── user-journeys.md          # Journey maps
    ├── design-vision.md          # Design philosophy
    ├── color-psychology.md       # Color strategy
    ├── design-system-foundations.md  # Token architecture
    ├── architecture.md           # High-level architecture
    └── clarifications.md         # Resolved questions
```

## Collaboration Flow

```
                    [User Input]
                         │
                         ▼
              ┌─────────────────────┐
              │  domain-consultant  │ ──→ Domain Research
              │       (opus)        │
              └─────────────────────┘
                         │
         ┌───────────────┼───────────────┐
         ▼               ▼               ▼
┌─────────────┐ ┌─────────────┐ ┌─────────────┐
│  product-   │ │    ux-      │ │  product-   │
│  manager    │ │ researcher  │ │  designer   │
│   (opus)    │ │   (opus)    │ │   (opus)    │
└─────────────┘ └─────────────┘ └─────────────┘
         │               │               │
         ▼               ▼               ▼
       PRD          Personas        Design Vision
                    Journeys        Color Psychology
                                    Design System
         │               │               │
         └───────────────┼───────────────┘
                         ▼
              ┌─────────────────────┐
              │ software-architect  │ ──→ Architecture
              │       (opus)        │
              └─────────────────────┘
                         │
                         ▼
              ┌─────────────────────┐
              │ clarification-agent │ ──→ Questions
              │      (sonnet)       │
              └─────────────────────┘
                         │
                         ▼
              [Discovery Complete]

Next: /peachflow:plan (quarterly roadmap)
```

## Notes

- **No git operations** during discovery
- All documents saved to `specs/discovery/`
- Clarification questions asked after all documents created
- Discovery should be completed before any planning begins
