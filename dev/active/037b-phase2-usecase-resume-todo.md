# Task 037b: Create ResumeTodoUseCase

## Phase
2 - Core Business Logic

## Description
Implement use case to resume a paused TODO, reactivating automatic email sending.

## Steps
1. Create `lib/domain/usecases/todo/resume_todo_usecase.dart`
2. Implement resume logic
3. Recalculate next_send_datetime

## Code Structure
```dart
import '../../repositories/todo_repository.dart';
import '../../repositories/settings_repository.dart';
import '../../../core/errors/result.dart';
import 'dart:math';

class ResumeTodoUseCase {
  final TodoRepository _todoRepository;
  final SettingsRepository _settingsRepository;

  ResumeTodoUseCase(this._todoRepository, this._settingsRepository);

  /// Resumes a paused TODO, reactivating automatic email sending
  /// - Sets is_paused = false
  /// - Calculates new next_send_datetime based on interval
  Future<Result<void>> execute({required int todoId}) async {
    try {
      final todo = await _todoRepository.getTodoById(todoId);

      if (todo == null) {
        return Result.failure('TODO not found');
      }

      if (todo.isCompleted) {
        return Result.failure('Cannot resume a completed TODO');
      }

      if (!todo.isPaused) {
        return Result.failure('TODO is not paused');
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
        isPaused: false,
        nextSendDatetime: nextSend,
      );

      await _todoRepository.update(updatedTodo);

      return Result.success(null);
    } catch (e) {
      return Result.failure('Failed to resume TODO: $e');
    }
  }
}
```

## Business Rules
- Cannot resume a completed TODO
- Cannot resume a TODO that is not paused
- Resuming calculates a new `next_send_datetime` based on:
  - Current date + send_interval_days
  - preferred_send_time
  - Randomization from settings

## Acceptance Criteria
- [ ] ResumeTodoUseCase created
- [ ] Sets is_paused to false
- [ ] Calculates new next_send_datetime
- [ ] Applies randomization from settings
- [ ] Returns error if TODO not found
- [ ] Returns error if not paused
- [ ] Returns error if completed

## Dependencies
- Task 026 (Repository Interfaces)
- Task 027 (TodoRepositoryImpl)
- Task 028 (SettingsRepositoryImpl)

## Parallel Work
Can run parallel with: Task 037a, 037c

## Estimated Effort
45 minutes
