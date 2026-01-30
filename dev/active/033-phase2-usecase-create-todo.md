# Task 033: Create CreateTodoUseCase

## Phase
2 - Core Business Logic

## Description
Implement the use case for creating a new TODO.

## Steps
1. Create `lib/domain/usecases/todo/create_todo_usecase.dart`
2. Implement validation logic
3. Calculate next_send_datetime
4. Handle already_sent_first flag

## Code Structure
```dart
import '../../entities/todo.dart';
import '../../repositories/todo_repository.dart';
import '../../repositories/settings_repository.dart';

class CreateTodoUseCase {
  final TodoRepository _todoRepository;
  final SettingsRepository _settingsRepository;

  CreateTodoUseCase(this._todoRepository, this._settingsRepository);

  Future<Result<int>> execute(Todo todo) async {
    // Validate
    if (todo.subject.isEmpty) {
      return Result.failure('Subject is required');
    }
    if (!_isValidEmail(todo.recipientEmail)) {
      return Result.failure('Invalid email address');
    }
    if (todo.intervalDays < 1) {
      return Result.failure('Interval must be at least 1 day');
    }

    // Get settings for randomization
    final settings = await _settingsRepository.getSettings();

    // Calculate next send datetime
    final nextSend = _calculateNextSend(
      startDate: todo.startDate,
      sendTime: todo.sendTime,
      intervalDays: todo.alreadySentFirst ? todo.intervalDays : 0,
      randomizeMinutes: settings.randomizeMinutes,
    );

    // Create TODO with calculated next_send
    final todoWithNextSend = todo.copyWith(nextSendDateTime: nextSend);

    // Persist
    try {
      final id = await _todoRepository.createTodo(todoWithNextSend);
      return Result.success(id);
    } catch (e) {
      return Result.failure('Failed to create TODO: $e');
    }
  }

  bool _isValidEmail(String email) {
    return RegExp(r'^[^@]+@[^@]+\.[^@]+$').hasMatch(email);
  }

  DateTime _calculateNextSend(...) {
    // Implementation based on BusinessLogik.md
  }
}
```

## Acceptance Criteria
- [ ] Validates all required fields
- [ ] Calculates next_send_datetime correctly
- [ ] Handles already_sent_first flag
- [ ] Applies randomization from settings
- [ ] Returns Result with ID or error

## Dependencies
- Task 026 (Repository Interfaces)
- Task 030 (Dependency Injection)

## Parallel Work
Can run parallel with: Task 034, 035, 036

## Estimated Effort
1-2 hours
