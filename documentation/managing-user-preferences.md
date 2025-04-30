# User Preferences System Documentation

## 1. Overview

A system to persistently store and retrieve user preferences (default DICOM directory) via an SQLite database.

Key features:
 - Cross-platform (Windows/macOS/Linux).
 - Hidden storage directory (~/.onko).
 - Abstract interface for consistency.

## 2. Components

### 2.1 UserPreferencesDB.py

**Purpose:** Manages SQLite database operations

### 2.2 UserPreferences.py

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

