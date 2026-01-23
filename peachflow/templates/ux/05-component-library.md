# Component Library Template

## Buttons

### Variants
| Variant | Usage | Example |
|---------|-------|---------|
| Primary | Main actions | Submit, Save |
| Secondary | Secondary actions | Cancel, Back |
| Ghost | Tertiary actions | Learn more |
| Danger | Destructive actions | Delete |

### Sizes
| Size | Height | Padding | Font Size |
|------|--------|---------|-----------|
| Small | 32px | 12px 16px | 14px |
| Medium | 40px | 16px 20px | 16px |
| Large | 48px | 20px 24px | 18px |

### States
- Default, Hover, Active, Focus, Disabled, Loading

## Form Inputs

### Text Input
- **Label**: Above input, required indicator (*)
- **Placeholder**: Example text, disappears on focus
- **Helper text**: Below input, muted color
- **Error state**: Red border, error message below
- **Sizes**: Small (32px), Medium (40px), Large (48px)

### Select
- Same sizing as text input
- Chevron indicator on right
- Options list with hover states

### Checkbox / Radio
- 20px touch target minimum
- Label to the right
- Group label above

### Toggle
- Width: 44px, Height: 24px
- Clear on/off indication
- Optional label

## Cards

### Structure
```
┌─────────────────────────┐
│ Header (optional)       │
├─────────────────────────┤
│ Body                    │
│ - Content here         │
├─────────────────────────┤
│ Footer (optional)       │
└─────────────────────────┘
```

### Variants
- Elevated (shadow)
- Outlined (border)
- Filled (background color)

## Navigation

### Top Navigation
- Logo left
- Nav items center or right
- User menu right

### Side Navigation
- Collapsible
- Icons + labels
- Active state indicator

### Breadcrumbs
- Separator: `/` or `>`
- Current page not linked
- Max 4 levels visible

## Feedback

### Toast Notifications
- Position: Top right or bottom center
- Auto-dismiss: 5 seconds
- Types: Success, Error, Warning, Info

### Modals
- Centered, backdrop overlay
- Close button top right
- Actions bottom right

### Loading States
- Skeleton screens for content
- Spinners for actions
- Progress bars for uploads
