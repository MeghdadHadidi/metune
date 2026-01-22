# Go Clean Code Patterns

Go-specific guidelines for type safety, clean imports, and idiomatic code.

## Type Safety in Go

### Interface Design

```go
// BAD - empty interface loses type safety
func Process(data interface{}) interface{} {
    return data
}

// GOOD - specific interface
type Processor interface {
    Process() Result
}

func Process(p Processor) Result {
    return p.Process()
}

// GOOD - generics (Go 1.18+)
func Process[T any](data T) T {
    return data
}
```

### Avoid Empty Interface

```go
// BAD
func Store(key string, value interface{}) error

// GOOD - use generics or specific types
func Store[T any](key string, value T) error

// OR define what you actually need
type Storable interface {
    Marshal() ([]byte, error)
}

func Store(key string, value Storable) error
```

### Type Assertions

```go
// BAD - unchecked type assertion (panics if wrong)
user := data.(User)

// GOOD - checked type assertion
user, ok := data.(User)
if !ok {
    return fmt.Errorf("expected User, got %T", data)
}

// GOOD - type switch for multiple types
switch v := data.(type) {
case User:
    return processUser(v)
case Admin:
    return processAdmin(v)
default:
    return fmt.Errorf("unexpected type: %T", v)
}
```

## Error Handling

### Always Handle Errors

```go
// BAD - ignoring error
result, _ := riskyOperation()

// BAD - checking error but continuing
result, err := riskyOperation()
if err != nil {
    log.Println(err)
}
// continues with potentially invalid result

// GOOD - proper error handling
result, err := riskyOperation()
if err != nil {
    return nil, fmt.Errorf("risky operation failed: %w", err)
}
```

### Error Wrapping

```go
// BAD - losing context
if err != nil {
    return err
}

// GOOD - wrap with context
if err != nil {
    return fmt.Errorf("failed to fetch user %s: %w", userID, err)
}
```

### Custom Errors

```go
// BAD - string errors
if user == nil {
    return errors.New("user not found")
}

// GOOD - typed errors
type NotFoundError struct {
    Resource string
    ID       string
}

func (e *NotFoundError) Error() string {
    return fmt.Sprintf("%s with id %s not found", e.Resource, e.ID)
}

func GetUser(id string) (*User, error) {
    user := db.Find(id)
    if user == nil {
        return nil, &NotFoundError{Resource: "User", ID: id}
    }
    return user, nil
}

// Check error type
var notFound *NotFoundError
if errors.As(err, &notFound) {
    // Handle not found specifically
}
```

### Sentinel Errors

```go
var (
    ErrNotFound     = errors.New("not found")
    ErrUnauthorized = errors.New("unauthorized")
    ErrValidation   = errors.New("validation failed")
)

func GetUser(id string) (*User, error) {
    user := db.Find(id)
    if user == nil {
        return nil, ErrNotFound
    }
    return user, nil
}

// Check sentinel error
if errors.Is(err, ErrNotFound) {
    // Handle not found
}
```

## Import Organization

```go
import (
    // Standard library
    "context"
    "encoding/json"
    "fmt"
    "net/http"

    // Third-party packages
    "github.com/gin-gonic/gin"
    "github.com/jmoiron/sqlx"
    "go.uber.org/zap"

    // Internal packages
    "myapp/internal/config"
    "myapp/internal/models"
    "myapp/internal/services"
)
```

### No Unused Imports

Go compiler enforces this, but be mindful of:

```go
// BAD - import for side effects without comment
import _ "github.com/lib/pq"

// GOOD - document why
import (
    // PostgreSQL driver for database/sql
    _ "github.com/lib/pq"
)
```

## No Dead Code

### Unused Variables

```go
// Go compiler catches this, but watch for:

// BAD - assigned but never used
func process() {
    result := compute()  // compiler error
}

// If intentionally unused, use blank identifier
func handler(w http.ResponseWriter, _ *http.Request) {
    // Request not needed
}
```

### Unreachable Code

```go
// BAD
func process() error {
    return nil
    cleanup()  // never executed
}

// GOOD - use defer for cleanup
func process() error {
    defer cleanup()
    return nil
}
```

## Null/Nil Handling

### Check Nil Before Use

```go
// BAD - potential nil dereference
func GetName(user *User) string {
    return user.Name
}

// GOOD - nil check
func GetName(user *User) string {
    if user == nil {
        return ""
    }
    return user.Name
}
```

### Return Early on Nil

```go
func ProcessUser(user *User) (*Result, error) {
    if user == nil {
        return nil, errors.New("user is required")
    }

    // user is guaranteed non-nil here
    return &Result{
        Name: user.Name,
    }, nil
}
```

### Pointer vs Value Receivers

```go
// Use pointer receiver when:
// - Method modifies the receiver
// - Receiver is large struct
// - Consistency with other methods

// GOOD - pointer receiver for mutation
func (u *User) SetName(name string) {
    u.Name = name
}

// GOOD - value receiver for read-only, small struct
func (p Point) Distance() float64 {
    return math.Sqrt(p.X*p.X + p.Y*p.Y)
}
```

## Struct Design

### Field Ordering

```go
// GOOD - exported fields first, then unexported
type User struct {
    ID        string
    Name      string
    Email     string
    CreatedAt time.Time

    db       *sql.DB
    cache    cache.Cache
    mu       sync.Mutex
}
```

### Constructor Functions

```go
// GOOD - constructor with validation
func NewUser(name, email string) (*User, error) {
    if name == "" {
        return nil, errors.New("name is required")
    }
    if !isValidEmail(email) {
        return nil, errors.New("invalid email")
    }

    return &User{
        ID:        uuid.New().String(),
        Name:      name,
        Email:     email,
        CreatedAt: time.Now(),
    }, nil
}
```

### Functional Options

```go
type Option func(*Config)

func WithTimeout(d time.Duration) Option {
    return func(c *Config) {
        c.Timeout = d
    }
}

func WithRetries(n int) Option {
    return func(c *Config) {
        c.Retries = n
    }
}

func NewClient(opts ...Option) *Client {
    cfg := &Config{
        Timeout: 30 * time.Second,  // defaults
        Retries: 3,
    }
    for _, opt := range opts {
        opt(cfg)
    }
    return &Client{config: cfg}
}

// Usage
client := NewClient(
    WithTimeout(10 * time.Second),
    WithRetries(5),
)
```

## Concurrency Patterns

### Channel Typing

```go
// GOOD - directional channels in signatures
func Producer(out chan<- int) {
    for i := 0; i < 10; i++ {
        out <- i
    }
    close(out)
}

func Consumer(in <-chan int) {
    for v := range in {
        process(v)
    }
}
```

### Context Handling

```go
// GOOD - always pass context
func FetchUser(ctx context.Context, id string) (*User, error) {
    select {
    case <-ctx.Done():
        return nil, ctx.Err()
    default:
    }

    // Proceed with operation
    return db.GetUser(ctx, id)
}
```

## Testing

### Table-Driven Tests

```go
func TestAdd(t *testing.T) {
    tests := []struct {
        name     string
        a, b     int
        expected int
    }{
        {"positive", 1, 2, 3},
        {"negative", -1, -2, -3},
        {"zero", 0, 0, 0},
    }

    for _, tt := range tests {
        t.Run(tt.name, func(t *testing.T) {
            result := Add(tt.a, tt.b)
            if result != tt.expected {
                t.Errorf("Add(%d, %d) = %d; want %d",
                    tt.a, tt.b, result, tt.expected)
            }
        })
    }
}
```

## Pre-Commit Checklist for Go

- [ ] No `interface{}` without strong justification
- [ ] All errors handled (not ignored with `_`)
- [ ] Errors wrapped with context
- [ ] Nil checks before pointer dereference
- [ ] Imports organized (stdlib → third-party → internal)
- [ ] No unused imports (go vet passes)
- [ ] No dead code
- [ ] Context passed to cancellable operations
- [ ] `go vet` and `staticcheck` pass
- [ ] `golangci-lint` clean
