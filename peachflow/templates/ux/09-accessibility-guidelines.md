# Accessibility Guidelines Template

## Compliance Target
**WCAG 2.1 Level AA**

## Core Requirements

### Perceivable

#### Color Contrast
| Element | Minimum Ratio |
|---------|---------------|
| Normal text | 4.5:1 |
| Large text (18px+) | 3:1 |
| UI components | 3:1 |
| Focus indicators | 3:1 |

#### Text Alternatives
- All images have meaningful alt text
- Decorative images have empty alt (`alt=""`)
- Icon buttons have aria-label
- Complex images have detailed descriptions

#### Media
- Videos have captions
- Audio has transcripts
- No auto-playing media with sound

### Operable

#### Keyboard Navigation
- [ ] All interactive elements keyboard accessible
- [ ] Visible focus indicator on all elements
- [ ] Logical tab order (left-to-right, top-to-bottom)
- [ ] Skip links for main content
- [ ] No keyboard traps
- [ ] Focus trapped in modals until closed

#### Timing
- [ ] Users can extend time limits
- [ ] Pause/stop moving content
- [ ] No content flashing > 3 times/second

#### Navigation
- [ ] Multiple ways to find content (nav, search, sitemap)
- [ ] Clear page titles
- [ ] Descriptive link text (no "click here")
- [ ] Breadcrumbs for complex navigation

### Understandable

#### Language
- [ ] Page language declared (`<html lang="en">`)
- [ ] Language changes marked (`<span lang="fr">`)

#### Predictable
- [ ] Consistent navigation across pages
- [ ] Consistent identification of elements
- [ ] No unexpected context changes on focus

#### Input Assistance
- [ ] Error prevention on forms
- [ ] Clear error messages
- [ ] Labels for all form inputs
- [ ] Input format hints where needed

### Robust

#### Compatibility
- [ ] Valid HTML
- [ ] Proper use of ARIA roles
- [ ] Name, role, value exposed to assistive tech

## ARIA Guidelines

### When to Use
- Only when native HTML is insufficient
- Prefer native elements over ARIA
- Test with screen readers

### Common Patterns
```html
<!-- Button that looks like a link -->
<span role="button" tabindex="0" aria-pressed="false">

<!-- Live region for updates -->
<div aria-live="polite" aria-atomic="true">

<!-- Modal dialog -->
<div role="dialog" aria-modal="true" aria-labelledby="title">
```

## Testing Checklist

### Automated
- [ ] aXe or similar automated testing
- [ ] HTML validation
- [ ] Color contrast checking

### Manual
- [ ] Keyboard-only navigation
- [ ] Screen reader testing (VoiceOver/NVDA)
- [ ] 200% zoom testing
- [ ] High contrast mode testing

## Screen Reader Announcements

| Action | Announcement |
|--------|--------------|
| Form error | "Error: [message]" |
| Loading | "Loading..." |
| Success | "Success: [message]" |
| New content | "[Number] new items" |
