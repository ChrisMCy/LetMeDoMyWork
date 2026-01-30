# Task 037a: Create PauseTodoUseCase

## Phase
2 - Core Business Logic

## Description
Implement use case to pause a TODO, stopping automatic email sending until resumed.

## Steps
1. Create `lib/domain/usecases/todo/pause_todo_usecase.dart`
2. Implement pause logic
3. Update next_send_datetime handling

## Code Structure
```dart
import '../../repositories/todo_repository.dart';
import '../../../core/errors/result.dart';

class PauseTodoUseCase {
  final TodoRepository _todoRepository;

  PauseTodoUseCase(this._todoRepository);

  /// Pauses a TODO, stopping automatic email sending
  /// - Sets is_paused = true
  /// - Clears next_send_datetime (no scheduled sends while paused)
  Future<Result<void>> execute({required int todoId}) async {
    try {
      final todo = await _todoRepository.getTodoById(todoId);

      if (todo == null) {
        return Result.failure('TODO not found');
      }

      if (todo.isCompleted) {
        return Result.failure('Cannot pause a completed TODO');
      }

      if (todo.isPaused) {
        return Result.failure('TODO is already paused');
      }

      final updatedTodo = todo.copyWith(
        isPaused: true,
        nextSendDatetime: null, // Clear scheduled send
      );

      await _todoRepository.update(updatedTodo);

      return Result.success(null);
    } catch (e) {
      return Result.failure('Failed to pause TODO: $e');
    }
  }
}
```

## Business Rules
- Cannot pause a completed TODO
- Cannot pause an already paused TODO
- Pausing clears `next_send_datetime`
- Paused TODOs appear at the bottom of the active list

## Acceptance Criteria
- [ ] PauseTodoUseCase created
- [ ] Sets is_paused to true
- [ ] Clears next_send_datetime
- [ ] Returns error if TODO not found
- [ ] Returns error if already paused
- [ ] Returns error if completed

## Dependencies
- Task 026 (Repository Interfaces)
- Task 027 (TodoRepositoryImpl)

## Parallel Work
Can run parallel with: Task 037b, 037c

## Estimated Effort
30 minutes
