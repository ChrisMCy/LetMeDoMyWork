# Task 014: Create DatabaseHelper

## Phase
1 - Core Infrastructure

## Description
Create the main DatabaseHelper class for SQLite database management.

## Steps
1. Create `lib/services/database/database_helper.dart`
2. Implement:
   - Singleton pattern
   - Database initialization
   - Table creation (settings, todos, sent_emails)
   - Index creation
   - Trigger creation

## Code Structure
```dart
class DatabaseHelper {
  static const String _databaseName = 'letmedomywork.db';
  static const int _databaseVersion = 1;

  static Database? _database;

  Future<Database> get database async {
    if (_database != null) return _database!;
    _database = await _initDatabase();
    return _database!;
  }

  Future<Database> _initDatabase() async { ... }
  Future<void> _onCreate(Database db, int version) async { ... }
  Future<void> _onUpgrade(Database db, int oldVersion, int newVersion) async { ... }
}
```

## Tables to Create
- `settings` (singleton, id always 1)
- `todos` (email campaigns)
- `sent_emails` (email history)

## Acceptance Criteria
- [ ] DatabaseHelper class created
- [ ] All three tables created on first run
- [ ] Indices created for performance
- [ ] Triggers created for auto-updates
- [ ] Singleton pattern enforced for settings table

## Dependencies
- Task 013 (Validate Setup - Phase 0 complete)

## Parallel Work
Can run parallel with: Task 015 (Database Constants)

## Estimated Effort
2-3 hours

## References
- DatabaseSchema.md for complete schema
