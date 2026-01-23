# Python Clean Code Patterns

Python-specific guidelines for type safety, clean imports, and code quality.

## Type Hints (PEP 484)

### Basic Type Hints

```python
# BAD - no type hints
def get_user(id):
    return db.find(id)

# GOOD - with type hints
def get_user(user_id: str) -> User | None:
    return db.find(user_id)
```

### Common Type Patterns

```python
from typing import Optional, Union, List, Dict, Callable, Any
from collections.abc import Sequence, Mapping

# Optional (can be None)
def find_user(user_id: str) -> Optional[User]:
    return db.find(user_id)

# Modern syntax (Python 3.10+)
def find_user(user_id: str) -> User | None:
    return db.find(user_id)

# Collections
def get_users() -> list[User]:
    return db.all()

def get_config() -> dict[str, str]:
    return load_config()

# Callable
def apply_transform(
    data: list[int],
    transform: Callable[[int], int]
) -> list[int]:
    return [transform(x) for x in data]
```

### Avoiding `Any`

```python
# BAD
def process(data: Any) -> Any:
    return data.transform()

# GOOD - use Protocol for duck typing
from typing import Protocol

class Transformable(Protocol):
    def transform(self) -> 'Transformable': ...

def process(data: Transformable) -> Transformable:
    return data.transform()
```

### TypedDict for Dictionaries

```python
# BAD - untyped dict
def create_response(data) -> dict:
    return {"status": "ok", "data": data}

# GOOD - TypedDict
from typing import TypedDict

class ApiResponse(TypedDict):
    status: str
    data: dict[str, Any]
    error: str | None

def create_response(data: dict[str, Any]) -> ApiResponse:
    return {"status": "ok", "data": data, "error": None}
```

### Generics

```python
from typing import TypeVar, Generic

T = TypeVar('T')

class Repository(Generic[T]):
    def __init__(self) -> None:
        self._items: list[T] = []

    def add(self, item: T) -> None:
        self._items.append(item)

    def get_all(self) -> list[T]:
        return self._items.copy()

# Usage
user_repo: Repository[User] = Repository()
user_repo.add(User(name="John"))
```

## Import Organization

Follow isort/PEP 8 import order:

```python
# 1. Standard library imports
import os
import sys
from datetime import datetime
from typing import Optional

# 2. Third-party imports
import requests
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel

# 3. Local application imports
from app.config import settings
from app.models import User
from app.services import user_service

# 4. Relative imports (same package)
from .utils import helper
from .types import UserDTO
```

### Import Best Practices

```python
# BAD - star imports
from module import *

# BAD - unused imports
import json  # never used
from typing import List, Dict, Set  # only List used

# GOOD - explicit imports
from typing import List

# GOOD - grouping related imports
from fastapi import (
    FastAPI,
    HTTPException,
    Depends,
    Query,
)
```

## No Unused Variables

```python
# BAD - unused variable
def process_data(items: list[Item]) -> int:
    total = 0
    unused = []  # never used
    for item in items:
        total += item.value
    return total

# GOOD - remove unused
def process_data(items: list[Item]) -> int:
    total = 0
    for item in items:
        total += item.value
    return total

# If intentionally unused, prefix with underscore
def callback(event: Event, _context: Context) -> None:
    process(event)
```

## Error Handling

### Typed Exceptions

```python
# BAD - generic exception
def get_user(user_id: str) -> User:
    user = db.find(user_id)
    if not user:
        raise Exception("Not found")
    return user

# GOOD - specific exception
class NotFoundError(Exception):
    def __init__(self, resource: str, id: str) -> None:
        self.resource = resource
        self.id = id
        super().__init__(f"{resource} with id {id} not found")

class ValidationError(Exception):
    def __init__(self, field: str, message: str) -> None:
        self.field = field
        self.message = message
        super().__init__(f"Validation error on {field}: {message}")

def get_user(user_id: str) -> User:
    user = db.find(user_id)
    if not user:
        raise NotFoundError("User", user_id)
    return user
```

### Exception Handling

```python
# BAD - bare except
try:
    result = risky_operation()
except:
    pass

# BAD - catching Exception
try:
    result = risky_operation()
except Exception as e:
    log.error(e)

# GOOD - specific exceptions
try:
    result = risky_operation()
except ValidationError as e:
    return {"error": e.message, "field": e.field}
except NotFoundError as e:
    return {"error": f"{e.resource} not found"}
except Exception:
    # Re-raise unexpected errors
    raise
```

## Dataclasses and Pydantic

### Dataclasses for Internal Data

```python
from dataclasses import dataclass, field
from datetime import datetime

@dataclass
class User:
    id: str
    name: str
    email: str
    created_at: datetime = field(default_factory=datetime.now)
    roles: list[str] = field(default_factory=list)
```

### Pydantic for Validation

```python
from pydantic import BaseModel, EmailStr, field_validator

class CreateUserRequest(BaseModel):
    name: str
    email: EmailStr
    password: str

    @field_validator('password')
    @classmethod
    def password_strength(cls, v: str) -> str:
        if len(v) < 8:
            raise ValueError('Password must be at least 8 characters')
        return v

class UserResponse(BaseModel):
    id: str
    name: str
    email: str

    model_config = {'from_attributes': True}
```

## Function Design

### Single Responsibility

```python
# BAD - does too much
def process_order(order: Order) -> None:
    validate_order(order)
    calculate_total(order)
    save_to_db(order)
    send_confirmation_email(order)
    update_inventory(order)

# GOOD - single responsibility
def validate_order(order: Order) -> ValidatedOrder:
    # Only validation logic
    ...

def save_order(order: ValidatedOrder) -> SavedOrder:
    # Only persistence logic
    ...

def process_order(order: Order) -> SavedOrder:
    validated = validate_order(order)
    return save_order(validated)
```

### Return Type Consistency

```python
# BAD - inconsistent returns
def find_user(user_id: str):
    user = db.find(user_id)
    if user:
        return user
    # Implicit None return

# GOOD - explicit return type
def find_user(user_id: str) -> User | None:
    return db.find(user_id)
```

## Null/None Handling

```python
# BAD - truthy check for None
def get_name(user: User | None) -> str:
    if user:
        return user.name
    return "Unknown"

# GOOD - explicit None check
def get_name(user: User | None) -> str:
    if user is not None:
        return user.name
    return "Unknown"

# GOOD - early return pattern
def process_user(user: User | None) -> Result:
    if user is None:
        return Result(error="User required")

    # user is now User, not User | None
    return Result(data=user.process())
```

## Type Checking Tools

### mypy Configuration

```ini
# mypy.ini or pyproject.toml
[mypy]
python_version = "3.11"
strict = true
warn_return_any = true
warn_unused_ignores = true
disallow_untyped_defs = true
disallow_any_generics = true
```

### Common mypy Errors and Fixes

```python
# Error: Function is missing a return type annotation
def process(x): ...  # BAD
def process(x: int) -> int: ...  # GOOD

# Error: Incompatible return value type
def get_id(user: User) -> str:
    return user.id  # Ensure user.id is str

# Error: Argument has incompatible type "str | None"; expected "str"
name: str | None = get_name()
process(name)  # BAD
if name is not None:
    process(name)  # GOOD
```

## Async Patterns

```python
from typing import AsyncIterator
import asyncio

async def fetch_user(user_id: str) -> User | None:
    async with aiohttp.ClientSession() as session:
        async with session.get(f"/users/{user_id}") as response:
            if response.status == 404:
                return None
            data = await response.json()
            return User(**data)

async def fetch_users(user_ids: list[str]) -> list[User]:
    tasks = [fetch_user(uid) for uid in user_ids]
    results = await asyncio.gather(*tasks)
    return [u for u in results if u is not None]
```

## Pre-Commit Checklist for Python

- [ ] All functions have type hints
- [ ] Return types are explicit
- [ ] No `Any` types (or minimal, justified usage)
- [ ] Imports organized (standard → third-party → local)
- [ ] No unused imports (ruff/flake8 clean)
- [ ] No unused variables
- [ ] Exceptions are specific, not generic
- [ ] mypy passes with strict mode
