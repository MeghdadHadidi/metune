# Motion & Animation Guidelines Template

## Principles

1. **Purposeful**: Every animation should serve a purpose
2. **Fast**: Keep animations under 300ms
3. **Natural**: Use easing that mimics physical motion
4. **Subtle**: Don't distract from content

## Timing

### Duration Scale
| Token | Duration | Usage |
|-------|----------|-------|
| --duration-instant | 100ms | Hovers, toggles |
| --duration-fast | 150ms | Buttons, small elements |
| --duration-normal | 200ms | Page transitions, cards |
| --duration-slow | 300ms | Modals, complex reveals |

### When to Use
| Duration | Use Cases |
|----------|-----------|
| 100-150ms | Micro-interactions (hover, focus) |
| 150-200ms | UI feedback (button press, toggle) |
| 200-300ms | Content transitions (page, modal) |
| 300-500ms | Complex animations (charts, onboarding) |

## Easing Functions

### Standard Easings
| Token | Value | Usage |
|-------|-------|-------|
| --ease-out | cubic-bezier(0, 0, 0.2, 1) | Elements entering |
| --ease-in | cubic-bezier(0.4, 0, 1, 1) | Elements leaving |
| --ease-in-out | cubic-bezier(0.4, 0, 0.2, 1) | Moving elements |
| --ease-linear | linear | Progress bars |

## Common Animations

### Hover Effects
```css
/* Subtle lift */
transform: translateY(-2px);
transition: transform var(--duration-fast) var(--ease-out);
```

### Button Press
```css
/* Scale down slightly */
transform: scale(0.98);
transition: transform var(--duration-instant);
```

### Modal Entry
```css
/* Fade + scale from 95% */
opacity: 0 → 1;
transform: scale(0.95) → scale(1);
transition: all var(--duration-normal) var(--ease-out);
```

### Toast Notification
```css
/* Slide in from edge */
transform: translateX(100%) → translateX(0);
transition: transform var(--duration-normal) var(--ease-out);
```

### Skeleton Loading
```css
/* Shimmer effect */
background: linear-gradient(90deg, #eee, #f5f5f5, #eee);
animation: shimmer 1.5s infinite;
```

## Accessibility

### Reduced Motion
```css
@media (prefers-reduced-motion: reduce) {
  * {
    animation-duration: 0.01ms !important;
    transition-duration: 0.01ms !important;
  }
}
```

### Guidelines
- No flashing animations (seizure risk)
- Provide pause controls for auto-playing content
- Keep total animation time reasonable
- Don't animate large areas of screen
