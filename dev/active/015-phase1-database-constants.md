# Task 015: Create Database Constants

## Phase
1 - Core Infrastructure

## Description
Create constants file for database table names, column names, and SQL statements.

## Steps
1. Create `lib/services/database/database_constants.dart`
2. Define all table names
3. Define all column names
4. Define SQL CREATE statements
5. Define SQL index statements

## Code Structure
```dart
class DatabaseConstants {
  // Database
  static const String databaseName = 'letmedomywork.db';
  static const int databaseVersion = 1;

  // Table Names
  static const String tableSettings = 'settings';
  static const String tableTodos = 'todos';
  static const String tableSentEmails = 'sent_emails';

  // Settings Columns
  static const String colId = 'id';
  static const String colMaxFollowUps = 'max_follow_ups';
  static const String colRandomizeMinutes = 'randomize_minutes';
  // ... more columns

  // SQL Statements
  static const String createSettingsTable = '''
    CREATE TABLE $tableSettings (
      $colId INTEGER PRIMARY KEY CHECK($colId = 1),
      ...
    )
  ''';
  // ... more statements
}
```

## Acceptance Criteria
- [ ] All table names defined as constants
- [ ] All column names defined as constants
- [ ] CREATE TABLE statements for all tables
- [ ] CREATE INDEX statements
- [ ] CREATE TRIGGER statements
- [ ] No hardcoded strings in DatabaseHelper

## Dependencies
- Task 013 (Validate Setup - Phase 0 complete)

## Parallel Work
Can run parallel with: Task 014 (DatabaseHelper)

## Estimated Effort
1 hour

## References
- DatabaseSchema.md for complete schema
