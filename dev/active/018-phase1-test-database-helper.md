# Task 018: Test DatabaseHelper

## Phase
1 - Core Infrastructure (Testing)

## Description
Write unit tests for DatabaseHelper class.

## Steps
1. Create `test/services/database/database_helper_test.dart`
2. Test database creation
3. Test table existence
4. Test settings singleton constraint
5. Test triggers

## Test Cases
```dart
void main() {
  group('DatabaseHelper', () {
    test('should create database with correct tables', () async {
      final db = await DatabaseHelper().database;
      final tables = await db.rawQuery(
        "SELECT name FROM sqlite_master WHERE type='table'"
      );
      expect(tables.map((t) => t['name']),
        containsAll(['settings', 'todos', 'sent_emails']));
    });

    test('should enforce settings singleton', () async {
      final db = await DatabaseHelper().database;
      // First insert should work
      // Second insert should fail
    });

    test('should create indices', () async { ... });

    test('should trigger completed_at on completion', () async { ... });
  });
}
```

## Acceptance Criteria
- [ ] Test file created
- [ ] All table creation tests pass
- [ ] Settings singleton test passes
- [ ] Index creation tests pass
- [ ] Trigger tests pass
- [ ] Coverage > 80% for DatabaseHelper

## Dependencies
- Task 014 (DatabaseHelper)
- Task 015 (Database Constants)
- Task 016 (Database Migrations)

## Parallel Work
Can run parallel with: Task 017 (Default Templates)

## Estimated Effort
1-2 hours
