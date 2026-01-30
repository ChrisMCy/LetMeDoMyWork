# Task 035: Create UpdateTodoUseCase

## Phase
2 - Core Business Logic

## Description
Implement the use case for updating an existing TODO.

## Steps
1. Create `lib/domain/usecases/todo/update_todo_usecase.dart`
2. Handle interval change (recalculate next_send)
3. Validate changes

## Code Structure
```dart
import '../../entities/todo.dart';
import '../../repositories/todo_repository.dart';
import '../../repositories/settings_repository.dart';

class UpdateTodoUseCase {
  final TodoRepository _todoRepository;
  final SettingsRepository _settingsRepository;

  UpdateTodoUseCase(this._todoRepository, this._settingsRepository);

  Future<Result<void>> execute(Todo updatedTodo, {bool intervalChanged = false}) async {
    // Validate
    if (updatedTodo.id == null) {
      return Result.failure('TODO ID is required for update');
    }

    // Get existing TODO
    final existing = await _todoRepository.getTodoById(updatedTodo.id!);
    if (existing == null) {
      return Result.failure('TODO not found');
    }

    // If interval changed, recalculate next_send
    Todo todoToSave = updatedTodo;
    if (intervalChanged || existing.intervalDays != updatedTodo.intervalDays) {
      final settings = await _settingsRepository.getSettings();
      final newNextSend = _calculateNextSend(
        currentDate: DateTime.now(),
        sendTime: updatedTodo.sendTime,
        intervalDays: updatedTodo.intervalDays,
        randomizeMinutes: settings.randomizeMinutes,
      );
      todoToSave = updatedTodo.copyWith(nextSendDateTime: newNextSend);
    }

    try {
      await _todoRepository.updateTodo(todoToSave);
      return Result.success(null);
    } catch (e) {
      return Result.failure('Failed to update TODO: $e');
    }
  }
}
```

## Acceptance Criteria
- [ ] Validates TODO exists
- [ ] Recalculates next_send when interval changes
- [ ] Preserves other fields
- [ ] Returns Result with success or error

## Dependencies
- Task 026 (Repository Interfaces)

## Parallel Work
Can run parallel with: Task 033, 034, 036

## Estimated Effort
1 hour
