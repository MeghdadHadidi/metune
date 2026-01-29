---
name: peachflow:design
description: Generate project-specific design skills from templates and create architecture decisions (ADRs). Design skills guide implementation agents on UI patterns, accessibility, and styling.
disable-model-invocation: true
allowed-tools: Read, Write, Edit, Grep, Glob, Task, AskUserQuestion, Bash
---

# /peachflow:design - Design Phase (v3)

Generate project-specific design skills and architecture decisions. Instead of creating UX documentation files, this command generates skills that implementation agents automatically use.

## Output Responsibility

**CRITICAL**: This command is responsible for the unified output to the user.

- Sub-agents return minimal responses
- Collect results and provide ONE final summary
- Only this command suggests next steps

## Pre-flight Check

```bash
# Check initialization
if [ ! -f ".peachflow-state.json" ] || [ ! -f ".peachflow-graph.json" ]; then
  echo "NOT_INITIALIZED"
  exit 1
fi

# Check discovery completed
discovery_status=$(python3 -c "import json; print(json.load(open('.peachflow-state.json'))['phases']['discovery']['status'])")
if [ "$discovery_status" != "completed" ]; then
  echo "DISCOVERY_NOT_COMPLETE"
fi

# Check design status
design_status=$(python3 -c "import json; print(json.load(open('.peachflow-state.json'))['phases']['design']['status'])")
```

**If discovery not complete:**
```
Discovery phase not complete. Run /peachflow:discover first.
```

---

## Design Phase Overview

The design phase creates:

1. **Design Skills** - Project-specific skills that guide UI implementation
2. **Architecture Decisions (ADRs)** - Technical decisions recorded in the graph

**NOT created (removed from v3):**
- UX documentation files (replaced by skills)
- Separate UI specification files

---

## Step 1: Initialize

```bash
# Update state
python3 -c "
import json
from datetime import datetime, timezone

with open('.peachflow-state.json', 'r') as f:
    state = json.load(f)

state['phases']['design']['status'] = 'in_progress'
state['lastUpdated'] = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')

with open('.peachflow-state.json', 'w') as f:
    json.dump(state, f, indent=2)
"

# Ensure skills directory exists
mkdir -p .claude/skills
```

---

## Step 2: Load Context

Read the documents needed for design decisions:

```bash
# Get project name
PROJECT_NAME=$(python3 -c "import json; print(json.load(open('.peachflow-state.json'))['projectName'])")

# Read BRD for brand/business context
cat docs/01-business/BRD.md

# Read PRD for features and user info
cat docs/02-product/PRD.md

# Get epics from graph
${CLAUDE_PLUGIN_ROOT}/scripts/peachflow-graph.py list epics --format json
```

---

## Step 3: Gather Design Preferences

Ask user about design direction:

```json
{
  "questions": [
    {
      "question": "What is the primary visual style for this project?",
      "header": "Visual Style",
      "options": [
        {"label": "Modern & Clean", "description": "Minimal, lots of whitespace, subtle shadows"},
        {"label": "Bold & Vibrant", "description": "Strong colors, expressive typography"},
        {"label": "Corporate & Professional", "description": "Conservative, trustworthy, structured"},
        {"label": "Playful & Friendly", "description": "Rounded corners, warm colors, casual"}
      ],
      "multiSelect": false
    },
    {
      "question": "What frontend framework will be used?",
      "header": "Framework",
      "options": [
        {"label": "React (Recommended)", "description": "Most popular, component-based"},
        {"label": "Vue.js", "description": "Progressive framework, easy learning curve"},
        {"label": "Svelte", "description": "Compiled, minimal bundle size"},
        {"label": "Plain HTML/CSS/JS", "description": "No framework, vanilla approach"}
      ],
      "multiSelect": false
    },
    {
      "question": "What styling approach?",
      "header": "Styling",
      "options": [
        {"label": "Tailwind CSS (Recommended)", "description": "Utility-first, rapid development"},
        {"label": "CSS Modules", "description": "Scoped CSS, traditional approach"},
        {"label": "Styled Components", "description": "CSS-in-JS, component-scoped"},
        {"label": "Plain CSS", "description": "Traditional stylesheets"}
      ],
      "multiSelect": false
    },
    {
      "question": "What WCAG accessibility level should we target?",
      "header": "Accessibility",
      "options": [
        {"label": "WCAG 2.1 AA (Recommended)", "description": "Standard compliance level"},
        {"label": "WCAG 2.1 AAA", "description": "Highest compliance level"},
        {"label": "Basic accessibility", "description": "Minimum viable accessibility"}
      ],
      "multiSelect": false
    }
  ]
}
```

---

## Step 4: Generate Design Skills

**Invoke**: design-lead agent

Provide context:
```
Project: $PROJECT_NAME
Visual style: [user's choice]
Framework: [user's choice]
Styling: [user's choice]
Accessibility: [user's choice]
BRD summary: [key points]
PRD features: [list]
Templates: ${CLAUDE_PLUGIN_ROOT}/templates/design-skills/

Task:
Generate project-specific design skills by filling in the templates.
Output skills to .claude/skills/

Skills to generate:
1. design-system.md - Colors, typography, spacing
2. component-patterns.md - UI component patterns
3. interaction-patterns.md - Animations, states
4. content-voice.md - Copy and tone guidelines
5. accessibility.md - ARIA and a11y patterns
6. responsive-layout.md - Breakpoints and layouts

Return: "Done: Generated X skills in .claude/skills/"
```

### Design Skill Generation Process

For each template in `${CLAUDE_PLUGIN_ROOT}/templates/design-skills/`:

1. Read the template file
2. Replace placeholders with project-specific values:
   - `{{PROJECT_NAME}}` → actual project name
   - `{{PRIMARY_COLOR}}` → derived from brand/style choice
   - `{{FRAMEWORK}}` → react/vue/svelte
   - `{{*_CODE}}` → framework-specific code examples
   - etc.
3. Write to `.claude/skills/[skill-name].md`

### Example: design-system.md Generation

Input (from user choices):
- Style: Modern & Clean
- Framework: React
- Styling: Tailwind CSS

Output `.claude/skills/design-system.md`:
```markdown
---
name: design-system
description: Use when implementing UI components, styling elements, or making visual design decisions for TaskFlow...
---

# TaskFlow Design System

## Color Tokens

### Brand Colors
- `--color-primary`: #3B82F6 - Primary brand color, use for CTAs
...
```

---

## Step 5: Create Architecture Decisions

**Invoke**: software-architect agent

Provide context:
```
Project: $PROJECT_NAME
Framework: [user's choice]
Features: [from PRD]
Epics: [from graph]
Graph tool: ${CLAUDE_PLUGIN_ROOT}/scripts/peachflow-graph.py

Task:
1. Review the features and identify key architectural decisions
2. Create ADRs for significant decisions
3. Register ADRs in the graph

Example decisions to consider:
- Authentication approach (JWT, sessions, OAuth)
- State management (Redux, Context, Zustand)
- API design (REST, GraphQL)
- Database choice (if applicable)

For each ADR:
1. Create file in docs/02-product/architecture/adr/
2. Register in graph:
   ${CLAUDE_PLUGIN_ROOT}/scripts/peachflow-graph.py create adr \
     --title "Use JWT for authentication" \
     --context "Need stateless auth for API" \
     --decision "Use JWT with refresh tokens" \
     --consequences "Need secure token storage" \
     --entity E-001

Return: "Done: Created X ADRs"
```

---

## Step 6: Finalize

```bash
# Update state
python3 -c "
import json
from datetime import datetime, timezone

with open('.peachflow-state.json', 'r') as f:
    state = json.load(f)

state['phases']['design']['status'] = 'completed'
state['phases']['design']['completedAt'] = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')
state['lastUpdated'] = datetime.now(timezone.utc).isoformat().replace('+00:00', 'Z')

with open('.peachflow-state.json', 'w') as f:
    json.dump(state, f, indent=2)
"
```

---

## Output Summary

```
Design phase complete for $PROJECT_NAME!

Design skills created in .claude/skills/:
  - design-system.md (colors, typography, spacing)
  - component-patterns.md (buttons, forms, cards, modals)
  - interaction-patterns.md (animations, transitions)
  - content-voice.md (tone, copy patterns)
  - accessibility.md (WCAG AA, ARIA patterns)
  - responsive-layout.md (breakpoints, grid system)

Architecture decisions (ADRs):
  - ADR-0001: Use JWT for authentication
  - ADR-0002: Use React Query for server state
  - ADR-0003: Use PostgreSQL for persistence

How design skills work:
  When implementing [FE] tasks, agents will automatically
  load these skills to ensure consistent design language.

Next: /peachflow:plan
```

---

## Design Skills vs Traditional Docs

| Old Approach (v2) | New Approach (v3) |
|-------------------|-------------------|
| 11 UX template files | 6 skill files |
| Agents read docs before work | Skills loaded on demand |
| Documentation-focused | Implementation-focused |
| Descriptive | Prescriptive with code |

**Benefits:**
1. Agents don't need to parse docs - skills are loaded automatically
2. Skills contain actionable code patterns, not just descriptions
3. Fewer files to maintain
4. Skills integrate with Claude Code's skill system

---

## Updating Design Skills

If design decisions change mid-project:

```
/peachflow:design --update

This will:
1. Show current skill settings
2. Ask what to change
3. Regenerate affected skills
4. Preserve any manual customizations marked with <!-- custom -->
```

---

## Tech Lead Integration

During planning, the tech-lead agent will reference design skills in task breakdowns:

```markdown
### T-042: [FE] Create user profile card

**Design skills to load:**
- design-system (for colors, spacing)
- component-patterns (Card section)
- accessibility (focus management)
```

This ensures implementation agents know which skills apply to each task.
