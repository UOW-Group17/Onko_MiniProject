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
