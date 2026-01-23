# Interaction Design Specifications Template

## Form Interactions

### Validation Timing
| Event | Validation Type |
|-------|-----------------|
| On blur | Individual field validation |
| On change | Real-time (password strength) |
| On submit | Full form validation |

### Validation Display
- Error message appears below field
- Field border turns red (--color-error)
- Error icon in field (optional)
- Scroll to first error on submit

### Validation Clearing
- On focus: Keep error visible until valid
- On valid input: Clear immediately

### Submit Behavior
1. Disable button, show loading spinner
2. Disable all form fields
3. On success: Show feedback, redirect/clear
4. On error: Re-enable form, show errors

## Navigation Interactions

### Page Transitions
- Type: Fade or slide
- Duration: 150-200ms
- Easing: ease-out

### Link Behavior
| Type | Behavior |
|------|----------|
| Internal | Client-side navigation |
| External | New tab (with indicator) |
| Download | Download with filename |

### Back Button
- Preserves scroll position
- Preserves form state (within session)

## Feedback Patterns

### Loading States

| Duration | Feedback |
|----------|----------|
| < 500ms | None (perceived as instant) |
| 500ms - 2s | Skeleton or spinner |
| > 2s | Progress indicator |
| > 10s | Cancel option |

### Success States
- Toast notification for background actions
- Inline confirmation for direct actions
- Redirect for flow completion

### Error States
- Toast for recoverable errors
- Inline for validation errors
- Full page for critical errors

## Gestures (if applicable)

### Touch
| Gesture | Action |
|---------|--------|
| Tap | Select/activate |
| Long press | Context menu |
| Swipe right | [Action] |
| Swipe left | [Action] |
| Pull down | Refresh |

### Mouse
| Action | Feedback |
|--------|----------|
| Hover | Visual state change |
| Right-click | Context menu |
| Double-click | [Action if any] |

## Keyboard Navigation

### Focus Order
- Logical left-to-right, top-to-bottom
- Skip links for main content
- Trap focus in modals

### Key Bindings
| Key | Action |
|-----|--------|
| Tab | Next focusable element |
| Shift+Tab | Previous focusable element |
| Enter | Activate button/link |
| Space | Toggle checkbox/button |
| Escape | Close modal/dropdown |
| Arrow keys | Navigate within components |
