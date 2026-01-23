# Design System Template

## Color Tokens

### Primary Palette
| Token | Value | Usage |
|-------|-------|-------|
| --color-primary | #XXXXXX | Primary actions, links |
| --color-primary-hover | #XXXXXX | Hover states |
| --color-primary-active | #XXXXXX | Active states |

### Neutral Palette
| Token | Value | Usage |
|-------|-------|-------|
| --color-background | #XXXXXX | Page background |
| --color-surface | #XXXXXX | Cards, panels |
| --color-border | #XXXXXX | Borders, dividers |
| --color-text | #XXXXXX | Body text |
| --color-text-muted | #XXXXXX | Secondary text |

### Semantic Colors
| Token | Value | Usage |
|-------|-------|-------|
| --color-success | #XXXXXX | Success states |
| --color-warning | #XXXXXX | Warning states |
| --color-error | #XXXXXX | Error states |
| --color-info | #XXXXXX | Informational |

## Typography

### Font Stack
```css
--font-family: [Font], system-ui, sans-serif;
--font-family-mono: [Mono Font], monospace;
```

### Type Scale
| Token | Size | Line Height | Usage |
|-------|------|-------------|-------|
| --font-size-xs | 12px | 1.5 | Captions |
| --font-size-sm | 14px | 1.5 | Small text |
| --font-size-base | 16px | 1.5 | Body |
| --font-size-lg | 18px | 1.4 | Large text |
| --font-size-xl | 20px | 1.3 | Subheadings |
| --font-size-2xl | 24px | 1.3 | Headings |
| --font-size-3xl | 32px | 1.2 | Page titles |

### Font Weights
| Token | Value |
|-------|-------|
| --font-weight-normal | 400 |
| --font-weight-medium | 500 |
| --font-weight-bold | 700 |

## Spacing Scale
| Token | Value |
|-------|-------|
| --space-xs | 4px |
| --space-sm | 8px |
| --space-md | 16px |
| --space-lg | 24px |
| --space-xl | 32px |
| --space-2xl | 48px |

## Border Radius
| Token | Value | Usage |
|-------|-------|-------|
| --radius-sm | 4px | Buttons, inputs |
| --radius-md | 8px | Cards |
| --radius-lg | 16px | Modals, large surfaces |
| --radius-full | 9999px | Pills, avatars |

## Shadows
| Token | Value | Usage |
|-------|-------|-------|
| --shadow-sm | 0 1px 2px rgba(0,0,0,0.05) | Subtle elevation |
| --shadow-md | 0 4px 6px rgba(0,0,0,0.1) | Cards |
| --shadow-lg | 0 10px 15px rgba(0,0,0,0.1) | Dropdowns, modals |

## Z-Index Scale
| Token | Value | Usage |
|-------|-------|-------|
| --z-dropdown | 100 | Dropdowns |
| --z-sticky | 200 | Sticky headers |
| --z-modal | 300 | Modals |
| --z-toast | 400 | Notifications |
