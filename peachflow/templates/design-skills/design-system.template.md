# Design System Template

This template is used by the design-lead agent to create a project-specific design system skill.

## Instructions for Design-Lead Agent

When creating the design system skill from this template:

1. Replace all `{{placeholder}}` values with project-specific values
2. Remove any sections that don't apply to the project
3. Add any project-specific tokens or patterns
4. Output the result to `.claude/skills/design-system.md`

---

## Template Content (copy below this line)

```markdown
---
name: design-system
description: Use when implementing UI components, styling elements, or making visual design decisions for {{PROJECT_NAME}}. Provides color tokens, typography scales, spacing system, and component patterns.
---

# {{PROJECT_NAME}} Design System

Apply these design tokens and patterns when implementing any UI work.

## Color Tokens

### Brand Colors
- `--color-primary`: {{PRIMARY_COLOR}} - Primary brand color, use for CTAs and key actions
- `--color-primary-hover`: {{PRIMARY_HOVER}} - Hover state for primary elements
- `--color-secondary`: {{SECONDARY_COLOR}} - Secondary accent color

### Semantic Colors
- `--color-success`: {{SUCCESS_COLOR}} - Success states, confirmations
- `--color-warning`: {{WARNING_COLOR}} - Warning states, caution
- `--color-error`: {{ERROR_COLOR}} - Error states, destructive actions
- `--color-info`: {{INFO_COLOR}} - Informational elements

### Neutral Scale
- `--color-bg`: {{BG_COLOR}} - Main background
- `--color-surface`: {{SURFACE_COLOR}} - Card/panel backgrounds
- `--color-border`: {{BORDER_COLOR}} - Borders and dividers
- `--color-text`: {{TEXT_COLOR}} - Primary text
- `--color-text-muted`: {{TEXT_MUTED}} - Secondary text

### Dark Mode (if applicable)
{{DARK_MODE_TOKENS}}

## Typography

### Font Stack
- Primary: {{PRIMARY_FONT}}
- Monospace: {{MONO_FONT}}

### Type Scale
- `--text-xs`: 0.75rem / 1rem line-height
- `--text-sm`: 0.875rem / 1.25rem line-height
- `--text-base`: 1rem / 1.5rem line-height
- `--text-lg`: 1.125rem / 1.75rem line-height
- `--text-xl`: 1.25rem / 1.75rem line-height
- `--text-2xl`: 1.5rem / 2rem line-height
- `--text-3xl`: 1.875rem / 2.25rem line-height
- `--text-4xl`: 2.25rem / 2.5rem line-height

### Font Weights
- Regular: 400
- Medium: 500
- Semibold: 600
- Bold: 700

## Spacing System

Use 4px base unit with these scale values:
- `--space-1`: 4px
- `--space-2`: 8px
- `--space-3`: 12px
- `--space-4`: 16px
- `--space-5`: 20px
- `--space-6`: 24px
- `--space-8`: 32px
- `--space-10`: 40px
- `--space-12`: 48px
- `--space-16`: 64px

## Border Radius

- `--radius-sm`: 4px - Buttons, inputs
- `--radius-md`: 8px - Cards, modals
- `--radius-lg`: 12px - Large containers
- `--radius-full`: 9999px - Pills, avatars

## Shadows

- `--shadow-sm`: 0 1px 2px rgba(0,0,0,0.05)
- `--shadow-md`: 0 4px 6px rgba(0,0,0,0.1)
- `--shadow-lg`: 0 10px 15px rgba(0,0,0,0.1)
- `--shadow-xl`: 0 20px 25px rgba(0,0,0,0.1)

## Z-Index Scale

- `--z-dropdown`: 100
- `--z-sticky`: 200
- `--z-modal`: 300
- `--z-toast`: 400
- `--z-tooltip`: 500

## Component Patterns

### Buttons
{{BUTTON_PATTERNS}}

### Forms
{{FORM_PATTERNS}}

### Cards
{{CARD_PATTERNS}}

## Code Comment Schema

When implementing, add this comment to track:
```
// peachflow: T-XXX | E-XXX | QX
```
```
