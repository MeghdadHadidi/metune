# Component Patterns Template

This template is used by the design-lead agent to create project-specific component patterns.

## Instructions for Design-Lead Agent

When creating the component patterns skill:

1. Analyze the PRD and UX requirements
2. Identify recurring UI patterns needed
3. Define patterns that match the project's needs
4. Output to `.claude/skills/component-patterns.md`

---

## Template Content (copy below this line)

```markdown
---
name: component-patterns
description: Use when building UI components for {{PROJECT_NAME}}. Provides reusable patterns for common components like buttons, forms, modals, lists, and navigation.
---

# {{PROJECT_NAME}} Component Patterns

## Button Variants

### Primary Button
```{{FRAMEWORK}}
{{PRIMARY_BUTTON_CODE}}
```
Use for: Main CTAs, form submissions, confirmations

### Secondary Button
```{{FRAMEWORK}}
{{SECONDARY_BUTTON_CODE}}
```
Use for: Secondary actions, cancel buttons

### Destructive Button
```{{FRAMEWORK}}
{{DESTRUCTIVE_BUTTON_CODE}}
```
Use for: Delete, remove, dangerous actions. Always require confirmation.

### Icon Button
```{{FRAMEWORK}}
{{ICON_BUTTON_CODE}}
```
Use for: Toolbar actions, compact UI areas

## Form Components

### Text Input
```{{FRAMEWORK}}
{{TEXT_INPUT_CODE}}
```
- Always include label
- Show validation state with border color
- Display error message below input

### Select/Dropdown
```{{FRAMEWORK}}
{{SELECT_CODE}}
```

### Checkbox Group
```{{FRAMEWORK}}
{{CHECKBOX_CODE}}
```

### Form Layout
```{{FRAMEWORK}}
{{FORM_LAYOUT_CODE}}
```
- Stack fields vertically with space-4 gap
- Right-align action buttons
- Show loading state on submit

## Card Components

### Basic Card
```{{FRAMEWORK}}
{{BASIC_CARD_CODE}}
```

### Interactive Card
```{{FRAMEWORK}}
{{INTERACTIVE_CARD_CODE}}
```
Use hover state and pointer cursor for clickable cards.

## Modal/Dialog

```{{FRAMEWORK}}
{{MODAL_CODE}}
```
- Trap focus within modal
- Close on Escape key
- Close on backdrop click (unless critical action)

## Toast/Notification

```{{FRAMEWORK}}
{{TOAST_CODE}}
```
- Auto-dismiss after 5s for success/info
- Persist for error until dismissed
- Stack from bottom-right

## Data List/Table

```{{FRAMEWORK}}
{{DATA_LIST_CODE}}
```
- Include loading skeleton
- Show empty state
- Support sorting/filtering where needed

## Navigation

### Sidebar
```{{FRAMEWORK}}
{{SIDEBAR_CODE}}
```

### Tabs
```{{FRAMEWORK}}
{{TABS_CODE}}
```

## Loading States

### Skeleton
```{{FRAMEWORK}}
{{SKELETON_CODE}}
```

### Spinner
```{{FRAMEWORK}}
{{SPINNER_CODE}}
```

## Empty States

```{{FRAMEWORK}}
{{EMPTY_STATE_CODE}}
```
Include: Icon, headline, description, CTA

## Error Boundaries

```{{FRAMEWORK}}
{{ERROR_BOUNDARY_CODE}}
```
```
