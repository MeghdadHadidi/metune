# Responsive Layout Template

This template is used by the design-lead agent to create project-specific responsive patterns.

## Instructions for Design-Lead Agent

When creating the responsive layout skill:

1. Define breakpoints based on target devices
2. Create layout patterns for key pages
3. Define container and grid systems
4. Output to `.claude/skills/responsive-layout.md`

---

## Template Content (copy below this line)

```markdown
---
name: responsive-layout
description: Use when implementing page layouts, grid systems, or responsive behavior for {{PROJECT_NAME}}. Provides breakpoints, container widths, and adaptive patterns.
---

# {{PROJECT_NAME}} Responsive Layout System

## Breakpoints

```css
/* Mobile first approach */
--breakpoint-sm: 640px;   /* Small tablets, large phones */
--breakpoint-md: 768px;   /* Tablets */
--breakpoint-lg: 1024px;  /* Small laptops */
--breakpoint-xl: 1280px;  /* Desktops */
--breakpoint-2xl: 1536px; /* Large screens */
```

### Media Query Usage
```css
/* Mobile (default) */
.component { ... }

/* Tablet and up */
@media (min-width: 768px) {
  .component { ... }
}

/* Desktop and up */
@media (min-width: 1024px) {
  .component { ... }
}
```

## Container System

```css
.container {
  width: 100%;
  margin-inline: auto;
  padding-inline: var(--space-4);
}

@media (min-width: 640px) {
  .container { max-width: 640px; }
}

@media (min-width: 768px) {
  .container { max-width: 768px; }
}

@media (min-width: 1024px) {
  .container { max-width: 1024px; }
}

@media (min-width: 1280px) {
  .container { max-width: 1280px; }
}
```

## Grid System

### CSS Grid Layout
```css
.grid {
  display: grid;
  gap: var(--space-4);
}

/* Common patterns */
.grid-cols-1 { grid-template-columns: 1fr; }
.grid-cols-2 { grid-template-columns: repeat(2, 1fr); }
.grid-cols-3 { grid-template-columns: repeat(3, 1fr); }
.grid-cols-4 { grid-template-columns: repeat(4, 1fr); }

/* Auto-fit for responsive grids */
.grid-auto {
  grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
}
```

### Responsive Grid Example
```{{FRAMEWORK}}
{{RESPONSIVE_GRID_CODE}}
```

## Page Layouts

### App Shell (Sidebar + Content)
```
+--------------------------------------------------+
|  Header                                          |
+----------+---------------------------------------+
|          |                                       |
| Sidebar  |  Main Content                         |
| (240px)  |  (flexible)                           |
|          |                                       |
+----------+---------------------------------------+
```

Mobile: Sidebar becomes hamburger menu
Tablet: Sidebar collapses to icons
Desktop: Full sidebar

```{{FRAMEWORK}}
{{APP_SHELL_CODE}}
```

### Dashboard Layout
```
+--------------------------------------------------+
|  Header                                          |
+--------------------------------------------------+
|  Stats Cards (4-col grid → 2-col → 1-col)        |
+--------------------------------------------------+
|  Chart Area       |  Activity Feed               |
|  (2/3 width)      |  (1/3 width)                 |
+--------------------------------------------------+
|  Data Table (full width, horizontal scroll)      |
+--------------------------------------------------+
```

```{{FRAMEWORK}}
{{DASHBOARD_LAYOUT_CODE}}
```

### Form Layout
```
+---------------------------+
|  Section Title            |
+---------------------------+
|  [Label]                  |
|  [Input Field           ] |
|                           |
|  [Label]    [Label]       |
|  [Input]    [Input]       |
|                           |
|  [Actions: Cancel | Save] |
+---------------------------+
```

Mobile: All fields full width
Desktop: Related fields can be side-by-side

```{{FRAMEWORK}}
{{FORM_LAYOUT_CODE}}
```

## Spacing by Viewport

| Token | Mobile | Tablet | Desktop |
|-------|--------|--------|---------|
| Page padding | 16px | 24px | 32px |
| Section gap | 24px | 32px | 48px |
| Card padding | 16px | 20px | 24px |

## Typography Scaling

| Element | Mobile | Desktop |
|---------|--------|---------|
| h1 | 1.875rem | 2.25rem |
| h2 | 1.5rem | 1.875rem |
| h3 | 1.25rem | 1.5rem |
| body | 1rem | 1rem |
| small | 0.875rem | 0.875rem |

## Navigation Patterns

### Mobile Navigation
- Hamburger menu → full-screen overlay or slide-in drawer
- Bottom navigation bar for primary actions (max 5 items)
- Keep critical actions always visible

### Tablet Navigation
- Collapsible sidebar (icons only when collapsed)
- Horizontal tabs for sections

### Desktop Navigation
- Full sidebar with labels
- Breadcrumbs for deep navigation
- Horizontal main nav + dropdown menus

## Component Adaptations

### Tables
- Mobile: Card-based layout or horizontal scroll
- Tablet+: Traditional table

### Modals
- Mobile: Full-screen sheet (slide up from bottom)
- Tablet+: Centered dialog with backdrop

### Forms
- Mobile: Single column, large touch targets
- Desktop: Multi-column where logical

## Hide/Show Utilities

```css
/* Hide on mobile, show on desktop */
.hidden-mobile {
  display: none;
}
@media (min-width: 768px) {
  .hidden-mobile { display: block; }
}

/* Show on mobile, hide on desktop */
.mobile-only {
  display: block;
}
@media (min-width: 768px) {
  .mobile-only { display: none; }
}
```

## Testing Checklist

- [ ] Test at 320px (small phones)
- [ ] Test at 375px (standard phones)
- [ ] Test at 768px (tablets)
- [ ] Test at 1024px (small laptops)
- [ ] Test at 1440px (desktops)
- [ ] Test touch interactions on mobile
- [ ] Test landscape orientation
- [ ] Verify no horizontal scroll (except tables)
```
