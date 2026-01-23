---
product: {product-name}
quarter: Q{XX}
document: frontend-spec
version: 1.0
status: draft | review | approved
created: {date}
updated: {date}
owner: frontend-engineer
---

# Frontend Specification: Q{XX} - {Theme}

## Overview

{Summary of frontend work for this quarter}

**Reference Documents**:
- [Quarterly Plan](./plan.md)
- [Backend Spec](./backend-spec.md)
- [Data Contracts](./data-contracts.md)
- [Design Vision](../../discovery/design-vision.md)

---

## Design System Implementation

### Design Tokens

#### Colors
```typescript
// src/design-system/tokens/colors.ts
export const colors = {
  primary: {
    50: '{#hex}',
    100: '{#hex}',
    // ...
    900: '{#hex}',
  },
  secondary: {
    // ...
  },
  semantic: {
    success: '{#hex}',
    warning: '{#hex}',
    error: '{#hex}',
    info: '{#hex}',
  },
  neutral: {
    // ...
  },
} as const;
```

#### Typography
```typescript
// src/design-system/tokens/typography.ts
export const typography = {
  fontFamily: {
    primary: '{font-stack}',
    secondary: '{font-stack}',
    mono: '{font-stack}',
  },
  fontSize: {
    xs: '0.75rem',    // 12px
    sm: '0.875rem',   // 14px
    base: '1rem',     // 16px
    lg: '1.125rem',   // 18px
    xl: '1.25rem',    // 20px
    '2xl': '1.5rem',  // 24px
    '3xl': '2rem',    // 32px
  },
  fontWeight: {
    regular: 400,
    medium: 500,
    semibold: 600,
    bold: 700,
  },
  lineHeight: {
    tight: 1.2,
    normal: 1.5,
    relaxed: 1.75,
  },
} as const;
```

#### Spacing
```typescript
// src/design-system/tokens/spacing.ts
export const spacing = {
  0: '0',
  1: '0.25rem',   // 4px
  2: '0.5rem',    // 8px
  3: '0.75rem',   // 12px
  4: '1rem',      // 16px
  5: '1.25rem',   // 20px
  6: '1.5rem',    // 24px
  8: '2rem',      // 32px
  10: '2.5rem',   // 40px
  12: '3rem',     // 48px
  16: '4rem',     // 64px
} as const;
```

---

## Component Architecture

### Component Hierarchy

```
Components
├── Primitives (atomic, no business logic)
│   ├── Button
│   ├── Input
│   ├── Text
│   ├── Card
│   ├── Badge
│   └── Icon
├── Patterns (composed, reusable)
│   ├── Form
│   ├── Modal
│   ├── Dropdown
│   ├── Table
│   └── Navigation
└── Features (business-specific)
    ├── {Feature}Card
    ├── {Feature}Form
    └── {Feature}List
```

### Primitive Components

#### Button
[TAGS: Q{XX}, design-system, primitives]

**File**: `src/design-system/primitives/Button.tsx`

**Variants**:
| Variant | Usage |
|---------|-------|
| primary | Main actions |
| secondary | Secondary actions |
| outline | Tertiary actions |
| ghost | Subtle actions |
| destructive | Dangerous actions |

**Sizes**: `sm`, `md`, `lg`

**States**: default, hover, active, focus, disabled, loading

**Props Interface**:
```typescript
interface ButtonProps {
  variant?: 'primary' | 'secondary' | 'outline' | 'ghost' | 'destructive';
  size?: 'sm' | 'md' | 'lg';
  loading?: boolean;
  disabled?: boolean;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
  fullWidth?: boolean;
  children: React.ReactNode;
  onClick?: () => void;
}
```

---

#### Input
[TAGS: Q{XX}, design-system, primitives]

**File**: `src/design-system/primitives/Input.tsx`

**Variants**: `default`, `filled`

**States**: default, focus, error, disabled

**Props Interface**:
```typescript
interface InputProps {
  type?: 'text' | 'email' | 'password' | 'number';
  label?: string;
  placeholder?: string;
  error?: string;
  hint?: string;
  leftIcon?: React.ReactNode;
  rightIcon?: React.ReactNode;
  disabled?: boolean;
  required?: boolean;
}
```

---

#### Card
[TAGS: Q{XX}, design-system, primitives]

**File**: `src/design-system/primitives/Card.tsx`

**Variants**: `elevated`, `outlined`, `filled`

**Props Interface**:
```typescript
interface CardProps {
  variant?: 'elevated' | 'outlined' | 'filled';
  padding?: 'none' | 'sm' | 'md' | 'lg';
  clickable?: boolean;
  children: React.ReactNode;
}
```

---

### Pattern Components

#### Form
[TAGS: Q{XX}, design-system, patterns]

**File**: `src/design-system/patterns/Form.tsx`

**Features**:
- Built on React Hook Form
- Zod schema validation
- Automatic error display
- Loading states
- Submit handling

**Usage**:
```typescript
<Form schema={loginSchema} onSubmit={handleLogin}>
  <Form.Field name="email" label="Email" />
  <Form.Field name="password" label="Password" type="password" />
  <Form.Submit>Log in</Form.Submit>
</Form>
```

---

#### Modal
[TAGS: Q{XX}, design-system, patterns]

**File**: `src/design-system/patterns/Modal.tsx`

**Features**:
- Focus trapping
- Escape to close
- Click outside to close (optional)
- Animation
- Accessibility (aria)

**Props Interface**:
```typescript
interface ModalProps {
  isOpen: boolean;
  onClose: () => void;
  title?: string;
  size?: 'sm' | 'md' | 'lg' | 'xl';
  closeOnOverlayClick?: boolean;
  children: React.ReactNode;
}
```

---

## Page Architecture

### Routing Structure
```
/
├── / (landing/home)
├── /auth
│   ├── /login
│   ├── /register
│   └── /forgot-password
├── /dashboard
├── /{feature}
│   ├── / (list)
│   ├── /new (create)
│   └── /:id (detail/edit)
└── /settings
```

### Page Components

#### {Feature} List Page
[TAGS: Q{XX}, E{XX}, pages]

**File**: `src/app/{feature}/page.tsx`

**Layout**:
```
┌─────────────────────────────────────────────────┐
│ Header                              [+ Create]  │
├─────────────────────────────────────────────────┤
│ Filters: [Search...] [Status ▾] [Date ▾]       │
├─────────────────────────────────────────────────┤
│ ┌─────────────────────────────────────────────┐ │
│ │ Item Card                          [Edit]   │ │
│ └─────────────────────────────────────────────┘ │
│ ┌─────────────────────────────────────────────┐ │
│ │ Item Card                          [Edit]   │ │
│ └─────────────────────────────────────────────┘ │
├─────────────────────────────────────────────────┤
│ Pagination: < 1 2 3 ... 10 >                    │
└─────────────────────────────────────────────────┘
```

**Data Requirements**:
- API: `GET /api/{feature}`
- Params: `page`, `limit`, `search`, `status`, `sort`

---

#### {Feature} Detail Page
[TAGS: Q{XX}, E{XX}, pages]

**File**: `src/app/{feature}/[id]/page.tsx`

**Layout**:
```
┌─────────────────────────────────────────────────┐
│ ← Back    {Title}                 [Edit] [Del] │
├─────────────────────────────────────────────────┤
│                                                 │
│ Section 1                                       │
│ ┌─────────────────────────────────────────────┐ │
│ │ Content                                     │ │
│ └─────────────────────────────────────────────┘ │
│                                                 │
│ Section 2                                       │
│ ┌─────────────────────────────────────────────┐ │
│ │ Content                                     │ │
│ └─────────────────────────────────────────────┘ │
│                                                 │
└─────────────────────────────────────────────────┘
```

**Data Requirements**:
- API: `GET /api/{feature}/:id`

---

## State Management

### Global State
```typescript
// src/stores/authStore.ts
interface AuthState {
  user: User | null;
  isAuthenticated: boolean;
  isLoading: boolean;
  login: (credentials: LoginCredentials) => Promise<void>;
  logout: () => void;
}
```

### Server State
Using TanStack Query for server state management.

**Query Keys Convention**:
```typescript
const queryKeys = {
  {feature}: {
    all: ['{feature}'] as const,
    lists: () => [...queryKeys.{feature}.all, 'list'] as const,
    list: (filters: Filters) => [...queryKeys.{feature}.lists(), filters] as const,
    details: () => [...queryKeys.{feature}.all, 'detail'] as const,
    detail: (id: string) => [...queryKeys.{feature}.details(), id] as const,
  },
};
```

---

## API Integration

### API Client
```typescript
// src/lib/api.ts
const api = {
  {feature}: {
    list: (params: ListParams) => fetch('/api/{feature}', params),
    get: (id: string) => fetch(`/api/{feature}/${id}`),
    create: (data: CreateData) => fetch('/api/{feature}', { method: 'POST', body: data }),
    update: (id: string, data: UpdateData) => fetch(`/api/{feature}/${id}`, { method: 'PATCH', body: data }),
    delete: (id: string) => fetch(`/api/{feature}/${id}`, { method: 'DELETE' }),
  },
};
```

### Hooks
```typescript
// src/features/{feature}/hooks/use{Feature}.ts
export function use{Feature}List(filters: Filters) {
  return useQuery({
    queryKey: queryKeys.{feature}.list(filters),
    queryFn: () => api.{feature}.list(filters),
  });
}

export function use{Feature}(id: string) {
  return useQuery({
    queryKey: queryKeys.{feature}.detail(id),
    queryFn: () => api.{feature}.get(id),
  });
}

export function useCreate{Feature}() {
  return useMutation({
    mutationFn: api.{feature}.create,
    onSuccess: () => queryClient.invalidateQueries({ queryKey: queryKeys.{feature}.lists() }),
  });
}
```

---

## Testing Strategy

### Component Testing
```typescript
// src/design-system/primitives/Button.test.tsx
describe('Button', () => {
  it('renders with correct text', () => {});
  it('handles click events', () => {});
  it('shows loading state', () => {});
  it('is disabled when specified', () => {});
  it('applies correct variant styles', () => {});
});
```

### Integration Testing
```typescript
// src/features/{feature}/__tests__/{Feature}Form.test.tsx
describe('{Feature}Form', () => {
  it('submits form with valid data', () => {});
  it('shows validation errors', () => {});
  it('handles API errors', () => {});
});
```

### Coverage Targets
| Type | Target |
|------|--------|
| Primitives | 90% |
| Patterns | 80% |
| Features | 70% |
| Pages | 60% |

---

## Accessibility Requirements

### Standards
- WCAG 2.1 Level AA compliance
- Keyboard navigation for all interactive elements
- Screen reader support
- Focus management

### Checklist per Component
- [ ] Semantic HTML
- [ ] ARIA labels where needed
- [ ] Keyboard accessible
- [ ] Focus visible
- [ ] Color contrast (4.5:1 minimum)
- [ ] Touch target size (44x44 minimum)

---

## Performance Requirements

### Targets
| Metric | Target |
|--------|--------|
| LCP | < 2.5s |
| FID | < 100ms |
| CLS | < 0.1 |
| Bundle Size | < 200KB (gzipped) |

### Optimization Strategies
1. Code splitting by route
2. Lazy loading components
3. Image optimization
4. Font optimization
5. Caching strategies

---

## File Structure

```
src/
├── app/                          # Next.js app router
│   ├── (auth)/                   # Auth group
│   │   ├── login/
│   │   └── register/
│   ├── (dashboard)/              # Dashboard group
│   │   ├── {feature}/
│   │   └── settings/
│   ├── layout.tsx
│   └── page.tsx
├── components/
│   └── features/
│       └── {feature}/
│           ├── {Feature}Card.tsx
│           ├── {Feature}Form.tsx
│           └── {Feature}List.tsx
├── design-system/
│   ├── tokens/
│   │   ├── colors.ts
│   │   ├── typography.ts
│   │   └── spacing.ts
│   ├── primitives/
│   │   ├── Button.tsx
│   │   ├── Input.tsx
│   │   └── Card.tsx
│   └── patterns/
│       ├── Form.tsx
│       └── Modal.tsx
├── hooks/
│   └── use{Feature}.ts
├── lib/
│   ├── api.ts
│   └── utils.ts
├── stores/
│   └── authStore.ts
└── types/
    └── {feature}.ts
```

---

## Implementation Checklist

### Phase 1: Design System
- [ ] Design tokens implemented
- [ ] Button component with all variants
- [ ] Input component with validation states
- [ ] Card component
- [ ] Form pattern
- [ ] Modal pattern

### Phase 2: Core Pages
- [ ] Layout structure
- [ ] Authentication pages
- [ ] Dashboard shell
- [ ] Navigation

### Phase 3: Feature Pages
- [ ] {Feature} list page
- [ ] {Feature} detail page
- [ ] {Feature} create/edit forms

### Phase 4: Polish
- [ ] Loading states
- [ ] Error states
- [ ] Empty states
- [ ] Animations
- [ ] Responsive design

---

## Notes

[NEEDS CLARIFICATION: Any specific UI requirements?]
[ASSUMPTION: Using Next.js App Router]
