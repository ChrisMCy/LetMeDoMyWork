# Task 037c: Create ReopenTodoUseCase

## Phase
2 - Core Business Logic

## Description
Implement use case to reopen a completed TODO, moving it back to active state.

## Steps
1. Create `lib/domain/usecases/todo/reopen_todo_usecase.dart`
2. Implement reopen logic
3. Reset completion state and recalculate next send

## Code Structure
```dart
import '../../repositories/todo_repository.dart';
import '../../repositories/settings_repository.dart';
import '../../../core/errors/result.dart';
import 'dart:math';

class ReopenTodoUseCase {
  final TodoRepository _todoRepository;
  final SettingsRepository _settingsRepository;

  ReopenTodoUseCase(this._todoRepository, this._settingsRepository);

  /// Reopens a completed TODO, moving it back to active state
  /// - Sets is_completed = false
  /// - Clears completed_at
  /// - Calculates new next_send_datetime
  /// - Optionally resets send_count (based on parameter)
  Future<Result<void>> execute({
    required int todoId,
    bool resetSendCount = false,
  }) async {
    try {
      final todo = await _todoRepository.getTodoById(todoId);

      if (todo == null) {
        return Result.failure('TODO not found');
      }

      if (!todo.isCompleted) {
        return Result.failure('TODO is not completed');
      }

      // Calculate next send datetime
      final settings = await _settingsRepository.getSettings();
      final randomMinutes = settings?.randomizeMinutes ?? 30;

      final now = DateTime.now();
      final baseDateTime = DateTime(
        now.year,
        now.month,
        now.day + todo.sendIntervalDays,
        todo.preferredSendTime.hour,
        todo.preferredSendTime.minute,
      );

      // Add randomization
      final random = Random();
      final randomOffset = random.nextInt(randomMinutes * 2) - randomMinutes;
      final nextSend = baseDateTime.add(Duration(minutes: randomOffset));

      final updatedTodo = todo.copyWith(
        isCompleted: false,
        completedAt: null,
        isPaused: false, // Ensure not paused when reopening
        nextSendDatetime: nextSend,
        // Reset send count if requested (for starting fresh)
        // Note: This would need the sent_emails to be cleared too
      );

      await _todoRepository.update(updatedTodo);

      // If resetting send count, also clear sent_emails for this TODO
      if (resetSendCount) {
        await _todoRepository.clearSentEmails(todoId);
      }

      return Result.success(null);
    } catch (e) {
      return Result.failure('Failed to reopen TODO: $e');
    }
  }
}
```

## Repository Addition
```dart
// Add to TodoRepository interface
Future<void> clearSentEmails(int todoId);

// Add to TodoRepositoryImpl
@override
Future<void> clearSentEmails(int todoId) async {
  final db = await _databaseHelper.database;
  await db.delete(
    'sent_emails',
    where: 'todo_id = ?',
    whereArgs: [todoId],
  );
}
```

## Business Rules
- Cannot reopen a TODO that is not completed
- Reopening:
  - Sets is_completed = false
  - Clears completed_at
  - Sets is_paused = false
  - Calculates new next_send_datetime
- Optional: Can reset send_count by clearing sent_emails

## Acceptance Criteria
- [ ] ReopenTodoUseCase created
- [ ] Sets is_completed to false
- [ ] Clears completed_at timestamp
- [ ] Sets is_paused to false
- [ ] Calculates new next_send_datetime
- [ ] Optional reset send count works
- [ ] Returns error if TODO not found
- [ ] Returns error if not completed

## Dependencies
- Task 026 (Repository Interfaces)
- Task 027 (TodoRepositoryImpl)
- Task 028 (SettingsRepositoryImpl)

## Parallel Work
Can run parallel with: Task 037a, 037b

## Estimated Effort
45 minutes
