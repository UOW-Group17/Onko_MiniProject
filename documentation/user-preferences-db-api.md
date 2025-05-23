# User Preferences Database API Documentaion

## 1. Overview

A system to persistently store and retrieve user preferences (default DICOM directory) via an SQLite database.

Key features:

- Cross-platform (Windows/macOS/Linux).
- Hidden storage directory (~/.onko).
- Abstract interface for consistency.

## 2. Components

### 2.1 user_pref_model.py

**Purpose:** Manages SQLite database operations

### 2.2 user_pref_controler.py

**Purpose:** Handles directory creation and database interactions.

**Key Methods**

```python
save_default_path(path: pathlib.Path) -> bool
```

- Saves path to DB.

```python
default_path() -> pathlib.Path | None
```

- Retrieves path from DB.

**OS-Specific Behaviour**

- Unix/macOS: Hidden via .onko (. prefix).
- Windows: Hidden via attrib +h command.

### 2.3 user_pref_interface.py

**Purpose:** Abstract Base Class (ABC) enforcing method consistency.

**Abstract Methods**

```python
@abstractmethod
def save_default_path(self, path: pathlib.Path) -> bool: …

@abstractmethod
def default_path(self) -> pathlib.Path | None: …
```

## 3. Usage Guide

**Basic Operations**

```python
from src.user_pref_controller import UserPrefController

# Set default path
prefs = UserPrefController()
prefs.save_default_path(Path("/home/user/dicom"))

# Get default path
print(prefs.default_path())
```
