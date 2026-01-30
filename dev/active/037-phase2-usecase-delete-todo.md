# Task 037: Create DeleteTodoUseCase

## Phase
2 - Core Business Logic

## Description
Implement the use case for deleting a TODO (with cascade).

## Steps
1. Create `lib/domain/usecases/todo/delete_todo_usecase.dart`
2. Implement deletion logic
3. Note: sent_emails cascade handled by DB foreign key

## Code Structure
```dart
import '../../repositories/todo_repository.dart';

class DeleteTodoUseCase {
  final TodoRepository _repository;

  DeleteTodoUseCase(this._repository);

  Future<Result<void>> execute(int todoId) async {
    // Verify TODO exists
    final todo = await _repository.getTodoById(todoId);
    if (todo == null) {
      return Result.failure('TODO not found');
    }

    try {
      // Delete TODO (sent_emails cascade via FK)
      await _repository.deleteTodo(todoId);
      return Result.success(null);
    } catch (e) {
      return Result.failure('Failed to delete TODO: $e');
    }
  }
}
```

## Acceptance Criteria
- [ ] Verifies TODO exists before delete
- [ ] Deletes TODO successfully
- [ ] Cascade deletes sent_emails (via DB)
- [ ] Returns Result with success or error

## Dependencies
- Task 026 (Repository Interfaces)

## Parallel Work
Can run parallel with: Task 033-036

## Estimated Effort
30 minutes
