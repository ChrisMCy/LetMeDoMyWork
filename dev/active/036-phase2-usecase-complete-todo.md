# Task 036: Create Complete/Pause/Reopen UseCases

## Phase
2 - Core Business Logic

## Description
Implement use cases for changing TODO state (complete, pause, resume, reopen).

## Steps
1. Create `lib/domain/usecases/todo/complete_todo_usecase.dart`
2. Create `lib/domain/usecases/todo/pause_todo_usecase.dart`
3. Create `lib/domain/usecases/todo/resume_todo_usecase.dart`
4. Create `lib/domain/usecases/todo/reopen_todo_usecase.dart`

## Code Structure
```dart
// complete_todo_usecase.dart
class CompleteTodoUseCase {
  final TodoRepository _repository;

  CompleteTodoUseCase(this._repository);

  Future<Result<void>> execute(int todoId) async {
    try {
      await _repository.completeTodo(todoId);
      return Result.success(null);
    } catch (e) {
      return Result.failure('Failed to complete TODO: $e');
    }
  }
}

// pause_todo_usecase.dart
class PauseTodoUseCase {
  final TodoRepository _repository;

  PauseTodoUseCase(this._repository);

  Future<Result<void>> execute(int todoId) async {
    try {
      await _repository.pauseTodo(todoId);
      return Result.success(null);
    } catch (e) {
      return Result.failure('Failed to pause TODO: $e');
    }
  }
}

// resume_todo_usecase.dart
class ResumeTodoUseCase {
  final TodoRepository _repository;
  final SettingsRepository _settingsRepository;

  ResumeTodoUseCase(this._repository, this._settingsRepository);

  Future<Result<void>> execute(int todoId) async {
    final todo = await _repository.getTodoById(todoId);
    if (todo == null) return Result.failure('TODO not found');

    final settings = await _settingsRepository.getSettings();
    final nextSend = _calculateNextSend(
      currentDate: DateTime.now(),
      sendTime: todo.sendTime,
      intervalDays: todo.intervalDays,
      randomizeMinutes: settings.randomizeMinutes,
    );

    try {
      await _repository.resumeTodo(todoId, nextSend);
      return Result.success(null);
    } catch (e) {
      return Result.failure('Failed to resume TODO: $e');
    }
  }
}

// reopen_todo_usecase.dart (similar to resume)
```

## Acceptance Criteria
- [ ] CompleteTodoUseCase sets is_completed and completed_at
- [ ] PauseTodoUseCase sets is_paused
- [ ] ResumeTodoUseCase clears is_paused, recalculates next_send
- [ ] ReopenTodoUseCase clears is_completed, recalculates next_send
- [ ] All return Result type

## Dependencies
- Task 026 (Repository Interfaces)

## Parallel Work
Can run parallel with: Task 033, 034, 035

## Estimated Effort
1-2 hours
