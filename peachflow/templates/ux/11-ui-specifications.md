# UI Specifications Template (Per Screen)

## Screen: [Screen Name]

### Overview
- **URL/Route**: [/path]
- **Purpose**: [Brief description]
- **User Story**: [US-XXX]
- **Persona**: [Primary user]

### Wireframe
```
┌──────────────────────────────────────────┐
│  [Header/Navigation]                     │
├──────────────────────────────────────────┤
│                                          │
│  [Main Content Area]                     │
│                                          │
│  ┌──────────┐  ┌──────────┐             │
│  │  Card 1  │  │  Card 2  │             │
│  └──────────┘  └──────────┘             │
│                                          │
│  [CTA Button]                            │
│                                          │
├──────────────────────────────────────────┤
│  [Footer]                                │
└──────────────────────────────────────────┘
```

### Components Used
| Component | Variant | Notes |
|-----------|---------|-------|
| Header | Default | Logged-in state |
| Card | Elevated | Product listing |
| Button | Primary, Large | Main CTA |

### States

#### Default State
- [Description of initial state]
- Data: [What data is shown]

#### Loading State
- Skeleton screens for [elements]
- Spinner for [elements]

#### Empty State
- Message: "[Empty state message]"
- Action: [CTA to resolve]

#### Error State
- Display: [How errors shown]
- Recovery: [How to recover]

### Interactions

| Element | Trigger | Action |
|---------|---------|--------|
| Card | Click | Navigate to detail |
| CTA Button | Click | Open modal / submit |
| Filter | Change | Filter results |

### Data Requirements
| Field | Type | Source | Format |
|-------|------|--------|--------|
| [Field 1] | String | API | As-is |
| [Field 2] | Date | API | "Jan 15, 2024" |
| [Field 3] | Number | API | "$1,234" |

### Accessibility Notes
- [ ] Page title: "[Descriptive title]"
- [ ] Main landmark for content
- [ ] Skip link to main content
- [ ] [Other specific requirements]

### Responsive Behavior
| Breakpoint | Changes |
|------------|---------|
| xs | Single column, stacked cards |
| md | Two column grid |
| lg | Three column grid |

### Analytics Events
| Event | Trigger | Data |
|-------|---------|------|
| page_view | On load | { page: "[name]" } |
| cta_click | Button click | { action: "[action]" } |

---

## Screen: [Next Screen Name]

[Repeat structure above for each screen]
