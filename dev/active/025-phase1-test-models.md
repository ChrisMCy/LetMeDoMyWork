# Task 025: Test Data Models

## Phase
1 - Core Infrastructure (Testing)

## Description
Write unit tests for all data models (TodoModel, SettingsModel, SentEmailModel).

## Steps
1. Create `test/data/models/todo_model_test.dart`
2. Create `test/data/models/settings_model_test.dart`
3. Create `test/data/models/sent_email_model_test.dart`
4. Test serialization/deserialization
5. Test edge cases

## Test Cases
```dart
// todo_model_test.dart
group('TodoModel', () {
  test('fromMap should correctly parse all fields', () {
    final map = {
      'id': 1,
      'subject': 'Test',
      'recipient_email': 'test@test.com',
      'selected_subject_indices': '[0,1,2]',
      'created_at': 1704067200000,
      // ... all fields
    };
    final model = TodoModel.fromMap(map);
    expect(model.id, 1);
    expect(model.subject, 'Test');
    expect(model.selectedSubjectIndices, [0, 1, 2]);
  });

  test('toMap should correctly serialize all fields', () {
    final model = TodoModel(...);
    final map = model.toMap();
    expect(map['subject'], 'Test');
    expect(jsonDecode(map['selected_subject_indices']), [0, 1, 2]);
  });

  test('round-trip should preserve data', () {
    final original = TodoModel(...);
    final map = original.toMap();
    final restored = TodoModel.fromMap(map);
    expect(restored, equals(original));
  });
});
```

## Acceptance Criteria
- [ ] Tests for TodoModel fromMap/toMap
- [ ] Tests for SettingsModel fromMap/toMap
- [ ] Tests for SentEmailModel fromMap/toMap
- [ ] Round-trip tests (entity → map → entity)
- [ ] Edge case tests (null values, empty strings)
- [ ] All tests pass

## Dependencies
- Task 022 (TodoModel)
- Task 023 (SettingsModel)
- Task 024 (SentEmailModel)

## Parallel Work
Can run parallel with: Task 026 (Repository Interfaces)

## Estimated Effort
1-2 hours
