# Accessibility Template

This template is used by the design-lead agent to create project-specific accessibility guidelines.

## Instructions for Design-Lead Agent

When creating the accessibility skill:

1. Determine WCAG compliance level needed (AA or AAA)
2. Identify key user interactions needing accessibility
3. Provide framework-specific patterns
4. Output to `.claude/skills/accessibility.md`

---

## Template Content (copy below this line)

```markdown
---
name: accessibility
description: Use when implementing any UI component or interaction for {{PROJECT_NAME}}. Ensures WCAG {{WCAG_LEVEL}} compliance with proper ARIA, keyboard navigation, and screen reader support.
---

# {{PROJECT_NAME}} Accessibility Guide

Target: WCAG {{WCAG_LEVEL}} compliance

## Core Principles

1. **Perceivable**: Content must be presentable in ways users can perceive
2. **Operable**: UI must be operable via keyboard and assistive tech
3. **Understandable**: Content and operation must be understandable
4. **Robust**: Content must be robust enough for assistive technologies

## Keyboard Navigation

### Focus Order
- Tab moves forward through interactive elements
- Shift+Tab moves backward
- Follow visual/logical reading order
- Never set `tabindex > 0`

### Common Shortcuts
| Key | Action |
|-----|--------|
| Tab | Move to next focusable element |
| Shift+Tab | Move to previous focusable element |
| Enter/Space | Activate buttons and links |
| Escape | Close modal/dropdown/popover |
| Arrow keys | Navigate within components (menus, tabs, etc.) |

### Focus Indicators
```css
:focus-visible {
  outline: 2px solid var(--color-primary);
  outline-offset: 2px;
}

/* Remove default outline only when using focus-visible */
:focus:not(:focus-visible) {
  outline: none;
}
```

## ARIA Patterns

### Buttons
```html
<!-- Text button - no ARIA needed if text is descriptive -->
<button>Save changes</button>

<!-- Icon-only button - needs label -->
<button aria-label="Close dialog">
  <CloseIcon aria-hidden="true" />
</button>

<!-- Loading button -->
<button aria-busy="true" aria-disabled="true">
  <Spinner aria-hidden="true" />
  Saving...
</button>
```

### Form Inputs
```html
<label for="email">Email address</label>
<input
  id="email"
  type="email"
  aria-describedby="email-hint email-error"
  aria-invalid="true"
/>
<span id="email-hint">We'll never share your email</span>
<span id="email-error" role="alert">Please enter a valid email</span>
```

### Modals
```html
<div
  role="dialog"
  aria-modal="true"
  aria-labelledby="modal-title"
  aria-describedby="modal-desc"
>
  <h2 id="modal-title">Confirm deletion</h2>
  <p id="modal-desc">This action cannot be undone.</p>
  <!-- Focus trapped within modal -->
</div>
```

### Live Regions
```html
<!-- For status updates (polite, waits for pause) -->
<div aria-live="polite" aria-atomic="true">
  Changes saved
</div>

<!-- For urgent alerts (assertive, interrupts) -->
<div role="alert">
  Error: Connection lost
</div>
```

### Navigation
```html
<nav aria-label="Main navigation">
  <ul role="menubar">
    <li role="none">
      <a role="menuitem" href="/dashboard">Dashboard</a>
    </li>
  </ul>
</nav>
```

### Tabs
```html
<div role="tablist" aria-label="Settings sections">
  <button
    role="tab"
    id="tab-1"
    aria-selected="true"
    aria-controls="panel-1"
  >General</button>
  <button
    role="tab"
    id="tab-2"
    aria-selected="false"
    aria-controls="panel-2"
    tabindex="-1"
  >Security</button>
</div>

<div
  role="tabpanel"
  id="panel-1"
  aria-labelledby="tab-1"
>
  <!-- Panel content -->
</div>
```

## Color Contrast

### Minimum Ratios
- Normal text: 4.5:1 against background
- Large text (18pt+ or 14pt bold): 3:1 against background
- UI components and graphics: 3:1 against adjacent colors

### Don't Rely on Color Alone
- Add icons or patterns for status (not just red/green)
- Use underlines for links (not just color change)
- Provide text labels for charts/graphs

## Images and Icons

### Decorative Images
```html
<img src="decoration.png" alt="" role="presentation" />
<Icon aria-hidden="true" />
```

### Informative Images
```html
<img src="chart.png" alt="Sales increased 25% from Q1 to Q2" />
```

### Complex Images
```html
<figure>
  <img src="architecture.png" alt="System architecture diagram" />
  <figcaption>
    <!-- Detailed description or link to text alternative -->
  </figcaption>
</figure>
```

## Responsive Accessibility

### Touch Targets
- Minimum 44x44px for touch interfaces
- Add padding if visual element is smaller

### Zoom Support
- Content must be usable at 200% zoom
- Don't disable pinch-zoom on mobile

### Text Scaling
- Use relative units (rem, em) not px for text
- Test with browser font size at 200%

## Motion and Animation

```css
@media (prefers-reduced-motion: reduce) {
  *,
  *::before,
  *::after {
    animation-duration: 0.01ms !important;
    animation-iteration-count: 1 !important;
    transition-duration: 0.01ms !important;
  }
}
```

## Testing Checklist

Before marking any UI task complete, verify:

- [ ] All interactive elements are keyboard accessible
- [ ] Focus order follows logical reading order
- [ ] Focus indicator is visible
- [ ] Images have appropriate alt text
- [ ] Color contrast meets requirements
- [ ] ARIA attributes are correct
- [ ] Screen reader announces content correctly
- [ ] Works with browser zoom at 200%
- [ ] Respects prefers-reduced-motion
```
