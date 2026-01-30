# Task 016: Create Database Migrations System

## Phase
1 - Core Infrastructure

## Description
Implement a migration system for future database schema updates.

## Steps
1. Create `lib/services/database/database_migrations.dart`
2. Implement version tracking using PRAGMA user_version
3. Create _onUpgrade handler
4. Create migration helper methods

## Code Structure
```dart
class DatabaseMigrations {
  static Future<void> migrate(Database db, int oldVersion, int newVersion) async {
    for (int version = oldVersion + 1; version <= newVersion; version++) {
      await _runMigration(db, version);
    }
  }

  static Future<void> _runMigration(Database db, int version) async {
    switch (version) {
      case 2:
        await _migrateV1ToV2(db);
        break;
      // Future migrations
    }
  }

  static Future<void> _migrateV1ToV2(Database db) async {
    // Example: Add new column
    // await db.execute('ALTER TABLE todos ADD COLUMN priority INTEGER DEFAULT 0');
  }
}
```

## Acceptance Criteria
- [ ] Migration class created
- [ ] Version tracking works
- [ ] _onUpgrade in DatabaseHelper calls migrations
- [ ] Test migration helper (mock v1→v2)
- [ ] Rollback not needed (SQLite limitation)

## Dependencies
- Task 014 (DatabaseHelper)
- Task 015 (Database Constants)

## Parallel Work
Can run parallel with: None

## Estimated Effort
1 hour
