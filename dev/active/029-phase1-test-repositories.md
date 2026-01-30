# Task 029: Test Repositories

## Phase
1 - Core Infrastructure (Testing)

## Description
Write unit tests for TodoRepositoryImpl and SettingsRepositoryImpl.

## Steps
1. Create `test/data/repositories/todo_repository_impl_test.dart`
2. Create `test/data/repositories/settings_repository_impl_test.dart`
3. Use in-memory SQLite for tests
4. Test all CRUD operations

## Test Cases
```dart
// todo_repository_impl_test.dart
group('TodoRepositoryImpl', () {
  late TodoRepositoryImpl repository;
  late DatabaseHelper databaseHelper;

  setUp(() async {
    databaseHelper = DatabaseHelper.test(); // In-memory DB
    repository = TodoRepositoryImpl(databaseHelper);
  });

  tearDown(() async {
    await databaseHelper.close();
  });

  test('createTodo should return inserted ID', () async {
    final todo = Todo(subject: 'Test', ...);
    final id = await repository.createTodo(todo);
    expect(id, greaterThan(0));
  });

  test('getTodoById should return todo when exists', () async {
    final id = await repository.createTodo(testTodo);
    final result = await repository.getTodoById(id);
    expect(result, isNotNull);
    expect(result!.subject, testTodo.subject);
  });

  test('completeTodo should set flags correctly', () async {
    final id = await repository.createTodo(testTodo);
    await repository.completeTodo(id);
    final result = await repository.getTodoById(id);
    expect(result!.isCompleted, true);
    expect(result.completedAt, isNotNull);
  });

  test('deleteTodo should cascade delete sent_emails', () async {
    final todoId = await repository.createTodo(testTodo);
    await repository.addSentEmail(SentEmail(todoId: todoId, ...));
    await repository.deleteTodo(todoId);
    final emails = await repository.getSentEmails(todoId);
    expect(emails, isEmpty);
  });
});
```

## Acceptance Criteria
- [ ] TodoRepository create test
- [ ] TodoRepository read tests (all, active, completed, by ID)
- [ ] TodoRepository update tests (complete, pause, resume)
- [ ] TodoRepository delete test (with cascade)
- [ ] SettingsRepository tests
- [ ] All tests pass
- [ ] Coverage > 80%

## Dependencies
- Task 027 (TodoRepository Implementation)
- Task 028 (SettingsRepository Implementation)

## Parallel Work
Can run parallel with: Task 030 (Dependency Injection)

## Estimated Effort
2-3 hours
