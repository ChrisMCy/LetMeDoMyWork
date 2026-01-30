# Task 038: Test TODO UseCases

## Phase
2 - Core Business Logic (Testing)

## Description
Write unit tests for all TODO-related use cases.

## Steps
1. Create `test/domain/usecases/todo/` directory
2. Create test file for each use case
3. Mock repositories using Mockito
4. Test success and failure scenarios

## Test Cases
```dart
@GenerateMocks([TodoRepository, SettingsRepository])
void main() {
  group('CreateTodoUseCase', () {
    late CreateTodoUseCase useCase;
    late MockTodoRepository mockTodoRepo;
    late MockSettingsRepository mockSettingsRepo;

    setUp(() {
      mockTodoRepo = MockTodoRepository();
      mockSettingsRepo = MockSettingsRepository();
      useCase = CreateTodoUseCase(mockTodoRepo, mockSettingsRepo);
    });

    test('should return failure when subject is empty', () async {
      final todo = Todo(subject: '', ...);
      final result = await useCase.execute(todo);
      expect(result.isFailure, true);
      expect(result.error, contains('Subject'));
    });

    test('should return failure when email is invalid', () async {
      final todo = Todo(recipientEmail: 'invalid', ...);
      final result = await useCase.execute(todo);
      expect(result.isFailure, true);
    });

    test('should calculate next_send with randomization', () async {
      when(mockSettingsRepo.getSettings())
          .thenAnswer((_) async => Settings(randomizeMinutes: 30));
      when(mockTodoRepo.createTodo(any))
          .thenAnswer((_) async => 1);

      final result = await useCase.execute(validTodo);

      expect(result.isSuccess, true);
      verify(mockTodoRepo.createTodo(argThat(
        predicate((t) => t.nextSendDateTime != null)
      ))).called(1);
    });
  });

  // Similar tests for other use cases...
}
```

## Acceptance Criteria
- [ ] CreateTodoUseCase tests (validation, success, failure)
- [ ] GetTodosUseCase tests (sorting)
- [ ] UpdateTodoUseCase tests (interval change)
- [ ] CompleteTodoUseCase tests
- [ ] DeleteTodoUseCase tests
- [ ] PauseTodoUseCase tests (cannot pause completed/already paused)
- [ ] ResumeTodoUseCase tests (next_send recalculation)
- [ ] ReopenTodoUseCase tests (reset state, optional send count reset)
- [ ] All tests pass

## Dependencies
- Task 033-037 (TODO UseCases: Create, Get, Update, Complete, Delete)
- Task 037a-037c (TODO UseCases: Pause, Resume, Reopen)

## Parallel Work
Can run parallel with: Task 039 (Placeholder Service)

## Estimated Effort
2-3 hours
