# Rust Clean Code Patterns

Rust-specific guidelines leveraging the type system for maximum safety.

## Type Safety in Rust

Rust's type system enforces many clean code principles at compile time. Focus on using it correctly.

### No Dynamic Typing

```rust
// BAD - avoid Box<dyn Any>
use std::any::Any;

fn process(data: Box<dyn Any>) -> Box<dyn Any> {
    data
}

// GOOD - use generics
fn process<T>(data: T) -> T {
    data
}

// GOOD - use trait bounds
fn process<T: Process>(data: T) -> T::Output {
    data.process()
}
```

### Trait Bounds Over dyn Trait

```rust
// BAD - dynamic dispatch when not needed
fn summarize(item: &dyn Summary) -> String {
    item.summarize()
}

// GOOD - static dispatch with generics
fn summarize<T: Summary>(item: &T) -> String {
    item.summarize()
}

// GOOD - impl Trait for simpler syntax
fn summarize(item: &impl Summary) -> String {
    item.summarize()
}
```

### Explicit Return Types

```rust
// BAD - relies on type inference for complex returns
fn get_users() {
    vec![User::new("Alice"), User::new("Bob")]
}

// GOOD - explicit return type
fn get_users() -> Vec<User> {
    vec![User::new("Alice"), User::new("Bob")]
}
```

## Error Handling with Result

### Always Handle Results

```rust
// BAD - unwrap can panic
let file = File::open("config.toml").unwrap();

// BAD - expect still panics
let file = File::open("config.toml").expect("Failed to open config");

// GOOD - propagate with ?
fn read_config() -> Result<Config, io::Error> {
    let file = File::open("config.toml")?;
    // ... process file
    Ok(config)
}

// GOOD - handle the error
fn read_config() -> Option<Config> {
    match File::open("config.toml") {
        Ok(file) => Some(parse_config(file)),
        Err(e) => {
            eprintln!("Could not open config: {}", e);
            None
        }
    }
}
```

### Custom Error Types

```rust
use thiserror::Error;

#[derive(Error, Debug)]
pub enum AppError {
    #[error("User {0} not found")]
    NotFound(String),

    #[error("Validation error: {field} - {message}")]
    Validation { field: String, message: String },

    #[error("Database error")]
    Database(#[from] sqlx::Error),

    #[error("IO error")]
    Io(#[from] std::io::Error),
}

fn get_user(id: &str) -> Result<User, AppError> {
    db.find(id).ok_or_else(|| AppError::NotFound(id.to_string()))
}
```

### Result Combinators

```rust
// BAD - verbose match
fn get_user_name(id: &str) -> Option<String> {
    match get_user(id) {
        Some(user) => Some(user.name),
        None => None,
    }
}

// GOOD - use map
fn get_user_name(id: &str) -> Option<String> {
    get_user(id).map(|user| user.name)
}

// GOOD - chain combinators
fn get_user_email(id: &str) -> Result<String, AppError> {
    get_user(id)?
        .email
        .ok_or(AppError::Validation {
            field: "email".to_string(),
            message: "Email not set".to_string(),
        })
}
```

## Option Handling

### No Unwrap

```rust
// BAD
let name = user.name.unwrap();

// GOOD - provide default
let name = user.name.unwrap_or_default();
let name = user.name.unwrap_or_else(|| "Unknown".to_string());

// GOOD - propagate
let name = user.name?;

// GOOD - pattern match
let name = match user.name {
    Some(n) => n,
    None => return Err(AppError::Validation { ... }),
};

// GOOD - if let for simple cases
if let Some(name) = user.name {
    println!("Hello, {}", name);
}
```

### Option Combinators

```rust
// GOOD - map for transformation
let upper_name: Option<String> = user.name.map(|n| n.to_uppercase());

// GOOD - and_then for chaining
let user_role: Option<Role> = get_user(id)
    .and_then(|u| u.role);

// GOOD - filter
let active_user: Option<User> = get_user(id)
    .filter(|u| u.is_active);

// GOOD - or_else for fallback
let name = user.name
    .or_else(|| user.username)
    .unwrap_or_default();
```

## Ownership and Borrowing

### Prefer Borrowing

```rust
// BAD - takes ownership unnecessarily
fn greet(name: String) {
    println!("Hello, {}", name);
}

// GOOD - borrow when possible
fn greet(name: &str) {
    println!("Hello, {}", name);
}

// GOOD - take ownership when needed
fn consume(item: Item) -> ProcessedItem {
    // Actually needs to own the data
    ProcessedItem::from(item)
}
```

### Lifetime Clarity

```rust
// BAD - unnecessary lifetime complexity
fn first<'a, 'b>(a: &'a str, _b: &'b str) -> &'a str {
    a
}

// GOOD - let Rust infer when possible
fn first<'a>(a: &'a str, _b: &str) -> &'a str {
    a
}

// GOOD - explicit when needed for clarity
struct Parser<'a> {
    input: &'a str,
    position: usize,
}
```

## Import Organization

```rust
// 1. Standard library
use std::collections::HashMap;
use std::fs::File;
use std::io::{self, Read, Write};

// 2. External crates
use serde::{Deserialize, Serialize};
use tokio::sync::mpsc;

// 3. Crate-level imports
use crate::config::Config;
use crate::error::AppError;

// 4. Module-level imports
use super::utils;
```

### Re-exports for Clean APIs

```rust
// lib.rs - clean public API
pub use error::AppError;
pub use config::Config;
pub use client::Client;

// Users can do:
// use mylib::{Client, Config, AppError};
```

## No Dead Code

### Compiler Warnings

```rust
// Rust compiler warns about:
// - Unused variables (prefix with _ to silence)
// - Unused imports
// - Unreachable code
// - Dead code

// BAD - unused variable
let result = compute();  // warning: unused variable

// GOOD - if intentionally unused
let _result = compute();

// GOOD - use it
let result = compute();
process(result);
```

### Deny Warnings in CI

```rust
// In lib.rs or main.rs
#![deny(warnings)]
#![deny(unused_imports)]
#![deny(dead_code)]
```

Or in Cargo.toml:
```toml
[lints.rust]
unused = "deny"
dead_code = "deny"
```

## Struct Design

### Builder Pattern

```rust
#[derive(Default)]
pub struct RequestBuilder {
    url: String,
    method: Method,
    headers: HashMap<String, String>,
    timeout: Option<Duration>,
}

impl RequestBuilder {
    pub fn new(url: impl Into<String>) -> Self {
        Self {
            url: url.into(),
            method: Method::Get,
            ..Default::default()
        }
    }

    pub fn method(mut self, method: Method) -> Self {
        self.method = method;
        self
    }

    pub fn header(mut self, key: impl Into<String>, value: impl Into<String>) -> Self {
        self.headers.insert(key.into(), value.into());
        self
    }

    pub fn timeout(mut self, duration: Duration) -> Self {
        self.timeout = Some(duration);
        self
    }

    pub fn build(self) -> Result<Request, BuildError> {
        // Validate and build
        Ok(Request { /* ... */ })
    }
}

// Usage
let request = RequestBuilder::new("https://api.example.com")
    .method(Method::Post)
    .header("Content-Type", "application/json")
    .timeout(Duration::from_secs(30))
    .build()?;
```

### Newtype Pattern

```rust
// BAD - primitive obsession
fn create_user(name: String, email: String, age: u32) -> User;

// GOOD - newtype for validation
pub struct Email(String);

impl Email {
    pub fn new(value: impl Into<String>) -> Result<Self, ValidationError> {
        let value = value.into();
        if !value.contains('@') {
            return Err(ValidationError::InvalidEmail);
        }
        Ok(Self(value))
    }

    pub fn as_str(&self) -> &str {
        &self.0
    }
}

fn create_user(name: String, email: Email, age: u32) -> User;
```

## Async Patterns

```rust
// GOOD - async functions with proper types
async fn fetch_user(id: &str) -> Result<User, AppError> {
    let response = client.get(&format!("/users/{}", id)).send().await?;

    if response.status() == StatusCode::NOT_FOUND {
        return Err(AppError::NotFound(id.to_string()));
    }

    let user = response.json::<User>().await?;
    Ok(user)
}

// GOOD - concurrent operations
async fn fetch_all(ids: Vec<String>) -> Vec<Result<User, AppError>> {
    let futures: Vec<_> = ids.iter().map(|id| fetch_user(id)).collect();
    futures::future::join_all(futures).await
}
```

## Testing

```rust
#[cfg(test)]
mod tests {
    use super::*;

    #[test]
    fn test_email_validation() {
        assert!(Email::new("valid@example.com").is_ok());
        assert!(Email::new("invalid").is_err());
    }

    #[test]
    fn test_user_creation() -> Result<(), AppError> {
        let user = create_user(
            "Alice".to_string(),
            Email::new("alice@example.com")?,
            30,
        );
        assert_eq!(user.name, "Alice");
        Ok(())
    }
}
```

## Pre-Commit Checklist for Rust

- [ ] No `unwrap()` or `expect()` in production code
- [ ] All `Result` and `Option` properly handled
- [ ] No `Box<dyn Any>` without strong justification
- [ ] Prefer `&str` over `String` for function parameters
- [ ] Explicit return types on public functions
- [ ] `cargo clippy` passes with no warnings
- [ ] `cargo fmt` applied
- [ ] No unused imports or dead code
- [ ] Custom error types with thiserror
- [ ] Proper lifetime annotations where needed
