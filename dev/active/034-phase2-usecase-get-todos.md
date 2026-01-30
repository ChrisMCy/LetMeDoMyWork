# Task 034: Create GetTodosUseCase

## Phase
2 - Core Business Logic

## Description
Implement use cases for retrieving TODOs with proper sorting.

## Steps
1. Create `lib/domain/usecases/todo/get_todos_usecase.dart`
2. Implement GetActiveTodosUseCase
3. Implement GetCompletedTodosUseCase
4. Include send_count in response

## Code Structure
```dart
import '../../entities/todo.dart';
import '../../repositories/todo_repository.dart';

class TodoWithSendCount {
  final Todo todo;
  final int sendCount;

  TodoWithSendCount(this.todo, this.sendCount);
}

class GetActiveTodosUseCase {
  final TodoRepository _repository;

  GetActiveTodosUseCase(this._repository);

  Future<List<TodoWithSendCount>> execute() async {
    final todos = await _repository.getActiveTodos();
    final result = <TodoWithSendCount>[];

    for (final todo in todos) {
      final sendCount = await _repository.getSendCount(todo.id!);
      result.add(TodoWithSendCount(todo, sendCount));
    }

    // Sort: non-paused first, then by send_count DESC, then by created_at ASC
    result.sort((a, b) {
      if (a.todo.isPaused != b.todo.isPaused) {
        return a.todo.isPaused ? 1 : -1;
      }
      if (a.sendCount != b.sendCount) {
        return b.sendCount.compareTo(a.sendCount);
      }
      return a.todo.createdAt.compareTo(b.todo.createdAt);
    });

    return result;
  }
}

class GetCompletedTodosUseCase {
  final TodoRepository _repository;

  GetCompletedTodosUseCase(this._repository);

  Future<List<TodoWithSendCount>> execute() async {
    final todos = await _repository.getCompletedTodos();
    // ... similar implementation, sorted by completed_at DESC
  }
}
```

## Acceptance Criteria
- [ ] GetActiveTodosUseCase returns sorted list
- [ ] GetCompletedTodosUseCase returns sorted list
- [ ] Send count included with each TODO
- [ ] Sorting matches BusinessLogik.md specification

## Dependencies
- Task 026 (Repository Interfaces)

## Parallel Work
Can run parallel with: Task 033, 035, 036

## Estimated Effort
1 hour
