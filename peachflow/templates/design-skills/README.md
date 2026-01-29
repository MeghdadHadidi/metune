# Design Skill Templates

These templates are used by the **design-lead agent** during the `/peachflow:design` phase to generate project-specific design skills.

## Purpose

Instead of creating many UX documentation files that agents must read and parse, we generate **skills** that are automatically loaded when developers implement UI tasks. This approach:

1. **Reduces context overhead** - Skills are loaded on-demand, not read every time
2. **Provides actionable guidance** - Skills contain code patterns, not just descriptions
3. **Integrates with workflow** - Developers invoke skills naturally during implementation

## Available Templates

| Template | Output Skill | Purpose |
|----------|--------------|---------|
| `design-system.template.md` | `.claude/skills/design-system.md` | Colors, typography, spacing, shadows |
| `component-patterns.template.md` | `.claude/skills/component-patterns.md` | Button, form, card, modal patterns |
| `interaction-patterns.template.md` | `.claude/skills/interaction-patterns.md` | Animations, transitions, states |
| `content-voice.template.md` | `.claude/skills/content-voice.md` | Copy, tone, error messages |
| `accessibility.template.md` | `.claude/skills/accessibility.md` | ARIA, keyboard, screen readers |
| `responsive-layout.template.md` | `.claude/skills/responsive-layout.md` | Breakpoints, grids, adaptive layouts |

## How It Works

### During Design Phase

1. Design-lead agent reads each template
2. Using PRD, BRD, and any user input, fills in placeholders
3. Generates project-specific skill files in `.claude/skills/`
4. Skills are committed to the project repository

### During Implementation Phase

1. Frontend developer picks up a [FE] task
2. Invokes relevant skills: `design-system`, `component-patterns`, etc.
3. Skills provide framework-specific code patterns
4. Code follows consistent design language

## Template Placeholders

Templates use `{{PLACEHOLDER}}` syntax for values that need to be filled in:

- `{{PROJECT_NAME}}` - The project's name
- `{{PRIMARY_COLOR}}` - Primary brand color (hex or CSS variable)
- `{{FRAMEWORK}}` - Frontend framework (react, vue, svelte, etc.)
- `{{*_CODE}}` - Code examples for the target framework

## Customization

If a project needs additional design skills:

1. Create a new template in this directory
2. Follow the existing pattern: instructions + template content
3. Update the design-lead agent to use the new template
4. Add to the README table above

## Integration with Tech Lead

When the tech-lead creates task breakdowns, they should reference which design skills apply:

```markdown
### T-042: [FE] Create user profile card
Implement the profile card component showing avatar, name, and stats.

**Design skills:** design-system, component-patterns (Card section)
**Acceptance criteria:**
- Uses design tokens for colors and spacing
- Follows card pattern from component-patterns
- Responsive at all breakpoints
```
