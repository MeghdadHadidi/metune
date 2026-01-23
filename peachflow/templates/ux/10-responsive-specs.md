# Responsive Design Specifications Template

## Breakpoints

| Name | Width | Target Devices |
|------|-------|----------------|
| xs | < 576px | Small phones |
| sm | ≥ 576px | Large phones |
| md | ≥ 768px | Tablets |
| lg | ≥ 992px | Small laptops |
| xl | ≥ 1200px | Desktops |
| 2xl | ≥ 1400px | Large screens |

### CSS Variables
```css
--breakpoint-sm: 576px;
--breakpoint-md: 768px;
--breakpoint-lg: 992px;
--breakpoint-xl: 1200px;
--breakpoint-2xl: 1400px;
```

## Layout Adaptations

### Container Widths
| Breakpoint | Max Width | Padding |
|------------|-----------|---------|
| xs | 100% | 16px |
| sm | 540px | 16px |
| md | 720px | 24px |
| lg | 960px | 24px |
| xl | 1140px | 32px |
| 2xl | 1320px | 32px |

### Grid System
- 12-column grid
- Gutter: 16px (mobile), 24px (tablet+)
- Stack to single column at xs

## Component Adaptations

### Navigation
| Breakpoint | Behavior |
|------------|----------|
| xs-md | Hamburger menu, slide-out drawer |
| lg+ | Full horizontal navigation |

### Cards
| Breakpoint | Layout |
|------------|--------|
| xs | Single column, full width |
| sm-md | Two columns |
| lg+ | Three or four columns |

### Tables
| Breakpoint | Behavior |
|------------|----------|
| xs-sm | Horizontal scroll or card view |
| md+ | Full table display |

### Forms
| Breakpoint | Layout |
|------------|--------|
| xs | Single column, stacked labels |
| md+ | Optional inline labels |

### Modals
| Breakpoint | Size |
|------------|------|
| xs | Full screen |
| sm-md | 90% width, centered |
| lg+ | Fixed width (480px-640px) |

## Typography Scaling

| Element | xs-sm | md-lg | xl+ |
|---------|-------|-------|-----|
| H1 | 28px | 32px | 40px |
| H2 | 24px | 28px | 32px |
| H3 | 20px | 22px | 24px |
| Body | 16px | 16px | 16px |
| Small | 14px | 14px | 14px |

## Touch Targets

### Minimum Sizes
- Mobile: 44px × 44px (Apple HIG)
- Desktop: 24px × 24px minimum

### Spacing
- At least 8px between touch targets
- Larger spacing on mobile (12-16px)

## Testing Requirements

### Viewport Testing
- [ ] iPhone SE (375px)
- [ ] iPhone 14 Pro (393px)
- [ ] iPad (768px)
- [ ] iPad Pro (1024px)
- [ ] Desktop (1440px)
- [ ] Large monitor (1920px)

### Orientation
- [ ] Portrait mode
- [ ] Landscape mode (mobile)

### Accessibility
- [ ] 200% zoom on desktop
- [ ] Text-only zoom
- [ ] High contrast mode
