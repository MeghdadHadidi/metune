# Interaction Patterns Template

This template is used by the design-lead agent to create project-specific interaction patterns.

## Instructions for Design-Lead Agent

When creating the interaction patterns skill:

1. Define animation timings and easing
2. Specify state transitions
3. Document feedback patterns
4. Output to `.claude/skills/interaction-patterns.md`

---

## Template Content (copy below this line)

```markdown
---
name: interaction-patterns
description: Use when implementing animations, transitions, hover states, and interactive behaviors for {{PROJECT_NAME}}. Provides timing, easing, and state change patterns.
---

# {{PROJECT_NAME}} Interaction Patterns

## Animation Timing

### Durations
- `--duration-fast`: 150ms - Micro-interactions (hover, focus)
- `--duration-normal`: 250ms - Standard transitions (modals, dropdowns)
- `--duration-slow`: 350ms - Complex animations (page transitions)

### Easing
- `--ease-in-out`: cubic-bezier(0.4, 0, 0.2, 1) - Most transitions
- `--ease-out`: cubic-bezier(0, 0, 0.2, 1) - Elements entering
- `--ease-in`: cubic-bezier(0.4, 0, 1, 1) - Elements exiting
- `--ease-bounce`: cubic-bezier(0.68, -0.55, 0.265, 1.55) - Playful feedback

## State Transitions

### Hover States
```css
.interactive-element {
  transition: all var(--duration-fast) var(--ease-in-out);
}
.interactive-element:hover {
  {{HOVER_TRANSFORM}}
}
```

### Focus States
```css
.focusable:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}
```
Always use `focus-visible` to avoid focus rings on click.

### Active/Pressed States
```css
.button:active {
  transform: scale(0.98);
}
```

### Disabled States
- Reduce opacity to 0.5
- Change cursor to `not-allowed`
- Remove hover/focus effects

## Enter/Exit Animations

### Fade In
```css
@keyframes fadeIn {
  from { opacity: 0; }
  to { opacity: 1; }
}
```

### Slide Up
```css
@keyframes slideUp {
  from {
    opacity: 0;
    transform: translateY(10px);
  }
  to {
    opacity: 1;
    transform: translateY(0);
  }
}
```

### Scale In
```css
@keyframes scaleIn {
  from {
    opacity: 0;
    transform: scale(0.95);
  }
  to {
    opacity: 1;
    transform: scale(1);
  }
}
```

## Modal Behavior

1. **Open**: Fade in backdrop (duration-normal), scale in content from 95%
2. **Close**: Reverse animation
3. **Focus management**: Focus first focusable element, trap focus, return focus on close
4. **Scroll lock**: Prevent body scroll while open

## Dropdown Behavior

1. **Open**: Slide down with fade, position aware (flip if near edge)
2. **Close**: Reverse or instant on outside click
3. **Keyboard**: Arrow keys navigate, Enter selects, Escape closes

## Form Feedback

### Validation
- **Real-time**: Validate on blur, not on every keystroke
- **Error appearance**: Fade in error message, change border color
- **Success**: Brief checkmark animation on valid input

### Submit
1. Disable button, show loading spinner
2. On success: Show success state, redirect or close
3. On error: Shake animation, show error message

## Loading Feedback

### Skeleton Loading
- Use for content that takes >300ms to load
- Pulse animation: `opacity: 0.5 → 1 → 0.5` over 1.5s

### Progress Indication
- For operations 2-10s: Indeterminate progress bar
- For operations >10s: Determinate progress with percentage

## Gesture Support (if applicable)

{{GESTURE_PATTERNS}}

## Reduced Motion

```css
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```
Always respect user's motion preferences.
```
