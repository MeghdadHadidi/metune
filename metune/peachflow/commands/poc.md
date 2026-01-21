---
name: peachflow:poc
description: Create visual POC/prototype with mocked data. Focuses on look and feel based on design documents. Optional phase for validation before full implementation.
argument-hint: "[optional: specific screens or flows to POC]"
allowed-tools: Bash, Read, Write, Edit, Grep, Glob, Task, AskUserQuestion
---

# /peachflow:poc - Visual Proof of Concept (Optional)

Create a quick visual prototype to validate look and feel before full implementation.

## Prerequisites

- Must be on a feature branch (quarter worktree)
- Quarter plan exists with design specifications
- Design vision and color psychology documents available

## Purpose

The POC phase allows stakeholders to:
- See the product before full development
- Validate design direction
- Test key user flows
- Make UI adjustments early (when changes are cheap)

## What POC Includes

- Real UI components styled with design tokens
- Mock API responses from static JSON
- Key user flows implemented
- Responsive layouts
- Loading and error states

## What POC Excludes

- Real backend API calls
- Authentication/authorization
- Data persistence
- Full test coverage
- Production optimizations

---

## Workflow

### Phase 1: POC Planning
**Auto-invoke**: product-manager + frontend-engineer agents

1. **Identify POC Scope**
   - Which screens to include
   - Which user flows to demonstrate
   - Priority order

2. **Define Mock Data**
   - What data structures needed
   - Realistic sample data
   - Edge cases to show (empty, error, loading)

### Phase 2: Setup
**Auto-invoke**: frontend-engineer agent (opus)

1. **Project Setup**
   ```bash
   # Initialize if not exists
   npm create vite@latest poc -- --template react-ts
   cd poc
   npm install
   ```

2. **Design System Setup**
   - Implement design tokens from `design-system-foundations.md`
   - Apply color palette from `color-psychology.md`
   - Set up typography and spacing

3. **Mock Setup**
   ```typescript
   // src/mocks/handlers.ts
   import { http, HttpResponse } from 'msw';
   import users from './data/users.json';
   import resources from './data/resources.json';

   export const handlers = [
     http.get('/api/users', () => {
       return HttpResponse.json(users);
     }),
     http.get('/api/resources', () => {
       return HttpResponse.json(resources);
     }),
   ];
   ```

### Phase 3: Implementation
**Auto-invoke**: frontend-engineer agent (opus)

For each screen in scope:

1. **Create Component Structure**
   ```
   src/
   ├── design-system/
   │   ├── tokens/
   │   │   ├── colors.ts
   │   │   ├── spacing.ts
   │   │   └── typography.ts
   │   └── components/
   │       ├── Button.tsx
   │       ├── Card.tsx
   │       └── Input.tsx
   ├── features/
   │   └── {feature}/
   │       ├── components/
   │       └── pages/
   ├── mocks/
   │   ├── data/
   │   │   └── *.json
   │   └── handlers.ts
   └── app/
       └── routes/
   ```

2. **Implement Screens**
   - Follow design vision
   - Use actual design tokens
   - Show all states (loading, empty, error, success)

3. **Connect Mock Data**
   - Use MSW for API mocking
   - Static JSON files for data
   - Realistic delays for loading states

### Phase 4: Review
**Auto-invoke**: product-designer + product-manager agents

1. Review POC against design vision
2. Check user flow completion
3. Identify adjustments needed
4. Document feedback

---

## Input

```
/peachflow:poc                      # POC all planned screens
/peachflow:poc dashboard            # POC specific screen
/peachflow:poc "login signup"       # POC specific flows
```

## Output Structure

```
poc/
├── src/
│   ├── design-system/
│   │   ├── tokens/
│   │   │   ├── colors.ts           # From color-psychology.md
│   │   │   ├── spacing.ts          # From design-system-foundations.md
│   │   │   └── typography.ts
│   │   └── components/
│   │       ├── Button.tsx
│   │       ├── Card.tsx
│   │       ├── Input.tsx
│   │       └── index.ts
│   ├── features/
│   │   └── {feature}/
│   │       ├── components/
│   │       └── pages/
│   ├── mocks/
│   │   ├── data/
│   │   │   ├── users.json
│   │   │   └── resources.json
│   │   ├── handlers.ts
│   │   └── browser.ts
│   └── app/
│       ├── App.tsx
│       └── routes.tsx
├── package.json
├── vite.config.ts
└── POC-NOTES.md                    # POC decisions and feedback
```

## Mock Data Structure

```json
// mocks/data/users.json
{
  "data": [
    {
      "id": "usr_001",
      "name": "Jane Smith",
      "email": "jane@example.com",
      "role": "admin",
      "avatar": "https://i.pravatar.cc/150?u=jane",
      "createdAt": "2026-01-15T10:30:00Z"
    }
  ],
  "meta": {
    "page": 1,
    "limit": 20,
    "total": 1
  }
}
```

## POC Notes Document

```markdown
# POC Notes: {Product Name}

## Scope
- Screens: [list]
- Flows: [list]

## Design Decisions Made
- [Decision 1]: [Rationale]
- [Decision 2]: [Rationale]

## Feedback Received
- [Feedback 1]: [Resolution]
- [Feedback 2]: [Resolution]

## Adjustments for Implementation
- [Adjustment 1]
- [Adjustment 2]

## Screenshots
[Include screenshots of key screens]
```

---

## Collaboration Flow

```
/peachflow:poc
      │
      ▼
┌─────────────────────────────────┐
│     POC Planning                │
│ product-manager + frontend-eng  │
│   - Scope definition            │
│   - Mock data planning          │
└─────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────┐
│     Implementation              │
│     frontend-engineer (opus)    │
│   - Design system setup         │
│   - Mock API setup              │
│   - Screen implementation       │
└─────────────────────────────────┘
      │
      ▼
┌─────────────────────────────────┐
│     Review                      │
│ product-designer + PM           │
│   - Visual validation           │
│   - Flow testing                │
│   - Feedback collection         │
└─────────────────────────────────┘
      │
      ▼
[Ready for /peachflow:implement or iterate POC]
```

## Notes

- POC is **optional** - skip if design is already validated
- POC code may or may not be used in final implementation
- Focus on **visual fidelity**, not code quality
- Use for stakeholder buy-in and early feedback
- Iterate quickly based on feedback
