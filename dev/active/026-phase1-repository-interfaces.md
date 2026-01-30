# Task 026: Create Repository Interfaces

## Phase
1 - Core Infrastructure

## Description
Create abstract repository interfaces in the domain layer.

## Steps
1. Create `lib/domain/repositories/todo_repository.dart`
2. Create `lib/domain/repositories/settings_repository.dart`
3. Define CRUD methods for each repository

## Code Structure
```dart
// todo_repository.dart
import '../entities/todo.dart';
import '../entities/sent_email.dart';

abstract class TodoRepository {
  // Create
  Future<int> createTodo(Todo todo);

  // Read
  Future<List<Todo>> getAllTodos();
  Future<List<Todo>> getActiveTodos();
  Future<List<Todo>> getCompletedTodos();
  Future<Todo?> getTodoById(int id);
  Future<List<Todo>> getDueTodos(DateTime now);
  Future<List<Todo>> getPendingTodos();

  // Update
  Future<void> updateTodo(Todo todo);
  Future<void> completeTodo(int id);
  Future<void> reopenTodo(int id, DateTime nextSendDateTime);
  Future<void> pauseTodo(int id);
  Future<void> resumeTodo(int id, DateTime nextSendDateTime);
  Future<void> updateNextSendDateTime(int id, DateTime nextSend);
  Future<void> markPendingSend(int id, bool pending);

  // Delete
  Future<void> deleteTodo(int id);

  // Sent Emails
  Future<int> addSentEmail(SentEmail email);
  Future<List<SentEmail>> getSentEmails(int todoId);
  Future<int> getSendCount(int todoId);
  Future<SentEmail?> getLastSentEmail(int todoId);
}

// settings_repository.dart
import '../entities/settings.dart';

abstract class SettingsRepository {
  Future<Settings> getSettings();
  Future<void> updateSettings(Settings settings);
  Future<void> updateLastOpened(DateTime timestamp);
  Future<bool> hasSettings();
  Future<void> initializeSettings(Settings settings);
}
```

## Acceptance Criteria
- [ ] TodoRepository interface created
- [ ] SettingsRepository interface created
- [ ] All methods from BusinessLogik.md included
- [ ] Return types appropriate (Future, nullable where needed)
- [ ] No implementation details (pure interfaces)

## Dependencies
- Task 019, 020, 021 (Entities)

## Parallel Work
Can run parallel with: Task 025 (Test Models)

## Estimated Effort
1 hour
