---
name: peachflow-file-organization
description: This skill provides file and directory organization patterns for peachflow projects. Use when creating new files, organizing documents, or setting up project structure. Applies automatically when working with specs, quarterly plans, or project scaffolding.
---

# Peachflow File Organization

Standard directory structure and file organization for peachflow-managed projects.

## Project Root Structure

```
project/
├── specs/                    # All specification documents
│   ├── discovery/           # Discovery phase outputs
│   └── quarterly/           # Quarterly planning outputs
├── src/                     # Source code
├── tests/                   # Test files
├── poc/                     # POC prototype (optional)
└── docs/                    # Additional documentation
```

## Specs Directory

### Discovery Phase (`specs/discovery/`)

```
specs/discovery/
├── domain-research.md           # Market, competitors, standards
├── prd.md                       # Product Requirements Document
├── user-personas.md             # User personas
├── user-journeys.md             # Journey maps
├── design-vision.md             # Design philosophy
├── color-psychology.md          # Color strategy
├── design-system-foundations.md # Token architecture
├── architecture.md              # High-level architecture
└── clarifications.md            # Resolved questions
```

### Quarterly Planning (`specs/quarterly/`)

```
specs/quarterly/
├── roadmap.md              # Master quarterly roadmap
├── Q01-overview.md         # Q01 high-level plan
├── Q02-overview.md         # Q02 high-level plan
├── Q03-overview.md         # Q03 high-level plan
└── Q01/                    # Detailed Q01 (in worktree)
    ├── plan.md             # Detailed quarter plan
    ├── frontend-spec.md    # Frontend architecture
    ├── backend-spec.md     # Backend architecture
    ├── data-contracts.md   # API/data specifications
    └── tasks.md            # Task breakdown
```

## Git Worktree Structure

When planning a specific quarter, a worktree is created:

```
parent-directory/
├── project/                           # Main repository
│   └── specs/
│       ├── discovery/
│       └── quarterly/
│           ├── roadmap.md
│           └── Q01-overview.md
│
└── project--001-Q01-product-slug/     # Worktree for Q01
    └── specs/
        └── quarterly/
            └── Q01/
                ├── plan.md
                ├── frontend-spec.md
                ├── backend-spec.md
                ├── data-contracts.md
                └── tasks.md
```

### Worktree Naming Convention

```
{repo}--{NNN}-Q{XX}-{product-slug}

Examples:
- mocket-v3--001-Q01-exam-platform
- mocket-v3--002-Q02-exam-platform
- myapp--001-Q01-inventory-system
```

## Source Code Organization

### Frontend (React/TypeScript)

```
src/
├── app/                     # App-level setup
│   ├── App.tsx
│   ├── routes.tsx
│   └── providers.tsx
├── design-system/           # Design tokens & base components
│   ├── tokens/
│   │   ├── colors.ts
│   │   ├── spacing.ts
│   │   └── typography.ts
│   └── components/
│       ├── Button/
│       ├── Card/
│       └── Input/
├── features/                # Feature-based modules
│   ├── auth/
│   │   ├── components/
│   │   ├── hooks/
│   │   ├── api/
│   │   └── types.ts
│   └── dashboard/
│       ├── components/
│       ├── hooks/
│       └── api/
├── shared/                  # Shared utilities
│   ├── hooks/
│   ├── utils/
│   └── types/
└── mocks/                   # MSW mock handlers (POC/testing)
    ├── data/
    └── handlers.ts
```

### Backend (Node.js/TypeScript)

```
src/
├── api/                     # API routes/handlers
│   ├── auth/
│   │   ├── handlers/
│   │   ├── middleware/
│   │   └── __tests__/
│   └── resources/
├── domain/                  # Business logic
│   ├── models/
│   ├── services/
│   └── repositories/
├── infrastructure/          # External integrations
│   ├── database/
│   ├── cache/
│   └── external-apis/
├── shared/                  # Shared utilities
│   ├── errors/
│   ├── validation/
│   └── types/
└── config/                  # Configuration
    ├── env.ts
    └── database.ts
```

## File Naming Conventions

| Type | Convention | Example |
|------|------------|---------|
| Components | PascalCase | `Button.tsx`, `UserCard.tsx` |
| Hooks | camelCase with `use` prefix | `useAuth.ts`, `useForm.ts` |
| Utilities | camelCase | `formatDate.ts`, `validation.ts` |
| Types | PascalCase | `User.types.ts`, `ApiResponse.ts` |
| Tests | Same as source + `.test` | `Button.test.tsx` |
| Specs | kebab-case | `user-personas.md`, `data-contracts.md` |
| Configs | kebab-case | `vite.config.ts`, `tailwind.config.js` |

## Document File Locations

| Document Type | Location |
|---------------|----------|
| Market research | `specs/discovery/domain-research.md` |
| PRD | `specs/discovery/prd.md` |
| User personas | `specs/discovery/user-personas.md` |
| User journeys | `specs/discovery/user-journeys.md` |
| Design vision | `specs/discovery/design-vision.md` |
| Color psychology | `specs/discovery/color-psychology.md` |
| Design system | `specs/discovery/design-system-foundations.md` |
| Architecture | `specs/discovery/architecture.md` |
| Quarterly roadmap | `specs/quarterly/roadmap.md` |
| Quarter overview | `specs/quarterly/Q{XX}-overview.md` |
| Quarter plan | `specs/quarterly/Q{XX}/plan.md` |
| Tasks | `specs/quarterly/Q{XX}/tasks.md` |

## When to Create vs. Where to Put

| Creating... | Put in... |
|-------------|-----------|
| New React component | `src/features/{feature}/components/` |
| Shared component | `src/design-system/components/` |
| API endpoint | `src/api/{resource}/handlers/` |
| Utility function | `src/shared/utils/` |
| Custom hook | `src/features/{feature}/hooks/` or `src/shared/hooks/` |
| Type definitions | Co-located with feature or `src/shared/types/` |
| Test file | Adjacent to source file |
| Mock data | `src/mocks/data/` |
| Spec document | `specs/discovery/` or `specs/quarterly/` |
