---
product: {product-name}
document: design-vision
version: 1.0
status: draft | review | approved
created: {date}
updated: {date}
owner: product-designer
---

# Design Vision: {Product Name}

## Design Philosophy

### Vision Statement
{One sentence capturing the ideal user experience}

### Design Principles

1. **{Principle 1}**: {Description and rationale}
2. **{Principle 2}**: {Description and rationale}
3. **{Principle 3}**: {Description and rationale}
4. **{Principle 4}**: {Description and rationale}
5. **{Principle 5}**: {Description and rationale}

---

## Emotional Design Goals

### Target Emotions
| Emotion | Why | How |
|---------|-----|-----|
| {Trust} | {Users need to feel secure} | {Clean design, clear feedback} |
| {Confidence} | {Users should feel capable} | {Progressive disclosure} |
| {Delight} | {Memorable experience} | {Micro-interactions} |

### Brand Personality
- **Voice**: {Friendly/Professional/Playful/Authoritative}
- **Tone**: {Casual/Formal/Encouraging/Direct}
- **Character**: {If the product were a person...}

---

## Visual Direction

### Mood Board Themes

```
┌─────────────────────────────────────────────────────────────┐
│                                                             │
│   [Image 1]         [Image 2]         [Image 3]            │
│   {Description}     {Description}     {Description}        │
│                                                             │
│   [Image 4]         [Image 5]         [Image 6]            │
│   {Description}     {Description}     {Description}        │
│                                                             │
└─────────────────────────────────────────────────────────────┘
```

### Visual Keywords
- {Keyword 1}: {What it means for our design}
- {Keyword 2}: {What it means for our design}
- {Keyword 3}: {What it means for our design}
- {Keyword 4}: {What it means for our design}

### Style Direction
| Aspect | Direction | Avoid |
|--------|-----------|-------|
| Overall | {Modern minimal} | {Cluttered, busy} |
| Shapes | {Rounded, soft} | {Sharp, aggressive} |
| Imagery | {Photography, human} | {Generic stock} |
| Motion | {Subtle, purposeful} | {Flashy, distracting} |

---

## Color Strategy

### Color Psychology
[Reference: color-psychology.md]

### Primary Palette
| Color | Hex | RGB | Psychology | Usage |
|-------|-----|-----|------------|-------|
| Primary | #{hex} | rgb(r,g,b) | {Emotion} | {Where used} |
| Secondary | #{hex} | rgb(r,g,b) | {Emotion} | {Where used} |
| Accent | #{hex} | rgb(r,g,b) | {Emotion} | {Where used} |

### Semantic Colors
| Purpose | Color | Hex |
|---------|-------|-----|
| Success | {Green} | #{hex} |
| Warning | {Yellow} | #{hex} |
| Error | {Red} | #{hex} |
| Info | {Blue} | #{hex} |

### Color Accessibility
- Contrast ratios meet WCAG {AA/AAA}
- Color is not the only indicator
- Dark mode considerations: [NEEDS CLARIFICATION]

---

## Typography Strategy

### Type Scale
| Level | Size | Weight | Line Height | Usage |
|-------|------|--------|-------------|-------|
| Display | {48px} | {Bold} | {1.2} | {Hero sections} |
| H1 | {32px} | {Bold} | {1.3} | {Page titles} |
| H2 | {24px} | {Semibold} | {1.4} | {Section titles} |
| H3 | {20px} | {Semibold} | {1.4} | {Subsections} |
| Body | {16px} | {Regular} | {1.5} | {Content} |
| Small | {14px} | {Regular} | {1.5} | {Captions} |

### Font Selection
| Category | Font | Fallback | Rationale |
|----------|------|----------|-----------|
| Primary | {Font name} | {System font} | {Why chosen} |
| Secondary | {Font name} | {System font} | {Why chosen} |
| Monospace | {Font name} | {System font} | {For code} |

### Typography Principles
1. {Principle 1}
2. {Principle 2}
3. {Principle 3}

---

## Spacing & Layout

### Spacing Scale
```
4px  - xs (tight elements)
8px  - sm (related elements)
16px - md (standard spacing)
24px - lg (section spacing)
32px - xl (major sections)
48px - 2xl (page sections)
64px - 3xl (hero spacing)
```

### Grid System
| Breakpoint | Columns | Gutter | Margin |
|------------|---------|--------|--------|
| Mobile (<640px) | 4 | 16px | 16px |
| Tablet (640-1024px) | 8 | 24px | 32px |
| Desktop (>1024px) | 12 | 24px | 64px |

### Layout Principles
1. {Principle 1}
2. {Principle 2}

---

## Component Philosophy

### Design Tokens
[Reference: design-system-foundations.md]

### Component Categories
| Category | Examples | Priority |
|----------|----------|----------|
| Primitives | Button, Input, Card | P1 |
| Patterns | Form, Navigation, List | P2 |
| Features | Dashboard, Profile, Settings | P3 |

### States & Feedback
| State | Visual Treatment |
|-------|-----------------|
| Default | {Description} |
| Hover | {Description} |
| Active | {Description} |
| Focus | {Description} |
| Disabled | {Description} |
| Loading | {Description} |
| Error | {Description} |

---

## Motion & Animation

### Animation Principles
1. **Purpose**: Every animation should serve a purpose
2. **Performance**: Never sacrifice performance for flourish
3. **Consistency**: Use consistent timing and easing

### Timing Standards
| Type | Duration | Easing |
|------|----------|--------|
| Micro (hover) | 100-150ms | ease-out |
| Small (toggle) | 150-200ms | ease-in-out |
| Medium (modal) | 200-300ms | ease-in-out |
| Large (page) | 300-500ms | ease-out |

### Key Animations
- **Page transitions**: {Description}
- **Loading states**: {Description}
- **Micro-interactions**: {Description}
- **Celebrations**: {Description}

---

## Iconography

### Icon Style
| Attribute | Value |
|-----------|-------|
| Style | {Outlined/Filled/Duotone} |
| Stroke Width | {2px} |
| Corner Radius | {2px} |
| Grid Size | {24px base} |

### Icon Categories
1. Navigation icons
2. Action icons
3. Status icons
4. Feature icons

### Icon Library
[NEEDS CLARIFICATION: Which icon library to use?]

---

## Illustration Style

### Illustration Direction
{Description of illustration style}

### When to Use
- Empty states
- Onboarding
- Error pages
- Marketing materials

### Style Guidelines
| Attribute | Direction |
|-----------|-----------|
| Style | {Flat/3D/Hand-drawn} |
| Colors | {From palette/Extended} |
| Characters | {Human/Abstract} |
| Complexity | {Simple/Detailed} |

---

## Responsive Design

### Breakpoint Strategy
| Name | Min Width | Target Devices |
|------|-----------|----------------|
| xs | 0 | Small phones |
| sm | 640px | Large phones |
| md | 768px | Tablets |
| lg | 1024px | Laptops |
| xl | 1280px | Desktops |
| 2xl | 1536px | Large screens |

### Mobile-First Principles
1. {Principle 1}
2. {Principle 2}
3. {Principle 3}

---

## Accessibility

### WCAG Target
[NEEDS CLARIFICATION: AA or AAA compliance?]

### Key Requirements
- [ ] Color contrast ratios
- [ ] Keyboard navigation
- [ ] Screen reader support
- [ ] Focus indicators
- [ ] Reduced motion support

### Inclusive Design Considerations
{Specific considerations for this product}

---

## Design Deliverables

### Required Artifacts
- [ ] Component library
- [ ] Design tokens
- [ ] Icon set
- [ ] Illustration assets
- [ ] Prototype

### Tools
| Purpose | Tool |
|---------|------|
| Design | {Figma/Sketch} |
| Prototyping | {Figma/Principle} |
| Handoff | {Figma/Zeplin} |
| Assets | {Figma/IconJar} |

---

## References

### Inspiration
- {Reference 1}
- {Reference 2}
- {Reference 3}

### Anti-Patterns
- {What to avoid 1}
- {What to avoid 2}
