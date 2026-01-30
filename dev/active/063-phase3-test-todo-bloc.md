# Task 063: Test TodoBloc

## Phase
3 - UI Foundation & MVP (Testing)

## Description
Write comprehensive unit tests for TodoBloc.

## Steps
1. Create `test/presentation/bloc/todo/todo_bloc_test.dart`
2. Mock all use cases
3. Test all events and state transitions

## Test Cases
```dart
@GenerateMocks([
  CreateTodoUseCase,
  GetActiveTodosUseCase,
  GetCompletedTodosUseCase,
  UpdateTodoUseCase,
  DeleteTodoUseCase,
  CompleteTodoUseCase,
  PauseTodoUseCase,
  ResumeTodoUseCase,
  ReopenTodoUseCase,
  SendEmailUseCase,
])
void main() {
  late TodoBloc bloc;
  late MockCreateTodoUseCase mockCreateTodoUseCase;
  late MockGetActiveTodosUseCase mockGetActiveTodosUseCase;
  late MockGetCompletedTodosUseCase mockGetCompletedTodosUseCase;
  // ... other mocks

  setUp(() {
    mockCreateTodoUseCase = MockCreateTodoUseCase();
    mockGetActiveTodosUseCase = MockGetActiveTodosUseCase();
    mockGetCompletedTodosUseCase = MockGetCompletedTodosUseCase();
    // ... initialize other mocks

    bloc = TodoBloc(
      createTodoUseCase: mockCreateTodoUseCase,
      getActiveTodosUseCase: mockGetActiveTodosUseCase,
      getCompletedTodosUseCase: mockGetCompletedTodosUseCase,
      // ... other use cases
    );
  });

  tearDown(() {
    bloc.close();
  });

  group('LoadTodos', () {
    final activeTodos = [
      TodoWithSendCount(createTestTodo(id: 1), 2),
      TodoWithSendCount(createTestTodo(id: 2), 0),
    ];
    final completedTodos = [
      TodoWithSendCount(createTestTodo(id: 3, isCompleted: true), 5),
    ];

    blocTest<TodoBloc, TodoState>(
      'emits [TodoLoading, TodoLoaded] when LoadTodos succeeds',
      build: () {
        when(mockGetActiveTodosUseCase.execute())
            .thenAnswer((_) async => activeTodos);
        when(mockGetCompletedTodosUseCase.execute())
            .thenAnswer((_) async => completedTodos);
        return bloc;
      },
      act: (bloc) => bloc.add(const LoadTodos()),
      expect: () => [
        const TodoLoading(),
        TodoLoaded(
          activeTodos: activeTodos,
          completedTodos: completedTodos,
        ),
      ],
    );

    blocTest<TodoBloc, TodoState>(
      'emits [TodoLoading, TodoError] when LoadTodos fails',
      build: () {
        when(mockGetActiveTodosUseCase.execute())
            .thenThrow(Exception('Database error'));
        return bloc;
      },
      act: (bloc) => bloc.add(const LoadTodos()),
      expect: () => [
        const TodoLoading(),
        isA<TodoError>(),
      ],
    );
  });

  group('CreateTodo', () {
    final newTodo = createTestTodo();

    blocTest<TodoBloc, TodoState>(
      'reloads todos after successful creation',
      build: () {
        when(mockCreateTodoUseCase.execute(any))
            .thenAnswer((_) async => Result.success(1));
        when(mockGetActiveTodosUseCase.execute())
            .thenAnswer((_) async => []);
        when(mockGetCompletedTodosUseCase.execute())
            .thenAnswer((_) async => []);
        return bloc;
      },
      act: (bloc) => bloc.add(CreateTodo(newTodo)),
      verify: (_) {
        verify(mockCreateTodoUseCase.execute(any)).called(1);
        verify(mockGetActiveTodosUseCase.execute()).called(1);
      },
    );

    blocTest<TodoBloc, TodoState>(
      'emits TodoError when creation fails',
      build: () {
        when(mockCreateTodoUseCase.execute(any))
            .thenAnswer((_) async => Result.failure('Validation error'));
        return bloc;
      },
      act: (bloc) => bloc.add(CreateTodo(newTodo)),
      expect: () => [
        const TodoError('Validation error'),
      ],
    );
  });

  group('CompleteTodo', () {
    blocTest<TodoBloc, TodoState>(
      'calls completeTodoUseCase and reloads',
      build: () {
        when(mockCompleteTodoUseCase.execute(any))
            .thenAnswer((_) async => Result.success(null));
        when(mockGetActiveTodosUseCase.execute())
            .thenAnswer((_) async => []);
        when(mockGetCompletedTodosUseCase.execute())
            .thenAnswer((_) async => []);
        return bloc;
      },
      act: (bloc) => bloc.add(const CompleteTodo(1)),
      verify: (_) {
        verify(mockCompleteTodoUseCase.execute(1)).called(1);
      },
    );
  });

  group('PauseTodo', () {
    blocTest<TodoBloc, TodoState>(
      'calls pauseTodoUseCase and reloads',
      build: () {
        when(mockPauseTodoUseCase.execute(any))
            .thenAnswer((_) async => Result.success(null));
        when(mockGetActiveTodosUseCase.execute())
            .thenAnswer((_) async => []);
        when(mockGetCompletedTodosUseCase.execute())
            .thenAnswer((_) async => []);
        return bloc;
      },
      act: (bloc) => bloc.add(const PauseTodo(1)),
      verify: (_) {
        verify(mockPauseTodoUseCase.execute(1)).called(1);
      },
    );
  });

  group('SendEmailForTodo', () {
    blocTest<TodoBloc, TodoState>(
      'emits TodoSending then reloads on success',
      seed: () => TodoLoaded(activeTodos: [], completedTodos: []),
      build: () {
        when(mockSendEmailUseCase.execute(todoId: anyNamed('todoId')))
            .thenAnswer((_) async => Result.success(null));
        when(mockGetActiveTodosUseCase.execute())
            .thenAnswer((_) async => []);
        when(mockGetCompletedTodosUseCase.execute())
            .thenAnswer((_) async => []);
        return bloc;
      },
      act: (bloc) => bloc.add(const SendEmailForTodo(1)),
      expect: () => [
        isA<TodoSending>(),
        const TodoLoading(),
        isA<TodoLoaded>(),
      ],
    );

    blocTest<TodoBloc, TodoState>(
      'emits TodoError when send fails',
      seed: () => TodoLoaded(activeTodos: [], completedTodos: []),
      build: () {
        when(mockSendEmailUseCase.execute(todoId: anyNamed('todoId')))
            .thenAnswer((_) async => Result.failure('SMTP error'));
        return bloc;
      },
      act: (bloc) => bloc.add(const SendEmailForTodo(1)),
      expect: () => [
        isA<TodoSending>(),
        const TodoError('SMTP error'),
      ],
    );
  });

  group('DeleteTodo', () {
    blocTest<TodoBloc, TodoState>(
      'calls deleteTodoUseCase and reloads',
      build: () {
        when(mockDeleteTodoUseCase.execute(any))
            .thenAnswer((_) async => Result.success(null));
        when(mockGetActiveTodosUseCase.execute())
            .thenAnswer((_) async => []);
        when(mockGetCompletedTodosUseCase.execute())
            .thenAnswer((_) async => []);
        return bloc;
      },
      act: (bloc) => bloc.add(const DeleteTodo(1)),
      verify: (_) {
        verify(mockDeleteTodoUseCase.execute(1)).called(1);
      },
    );
  });
}

// Helper function
Todo createTestTodo({
  int id = 1,
  bool isCompleted = false,
  bool isPaused = false,
}) {
  return Todo(
    id: id,
    recipientEmail: 'test@example.com',
    recipientFirstName: 'John',
    recipientLastName: 'Doe',
    subject: 'Test Subject',
    isCompleted: isCompleted,
    isPaused: isPaused,
    language: 'EN',
    intervalDays: 3,
    sendTime: TimeOfDay(hour: 9, minute: 0),
    createdAt: DateTime.now(),
  );
}
```

## Acceptance Criteria
- [ ] LoadTodos success and failure tested
- [ ] CreateTodo success and validation failure tested
- [ ] CompleteTodo tested
- [ ] PauseTodo and ResumeTodo tested
- [ ] SendEmailForTodo success and failure tested
- [ ] DeleteTodo tested
- [ ] All state transitions correct
- [ ] All tests pass

## Dependencies
- Task 062 (TodoBloc)

## Parallel Work
Must run after: Task 062

## Estimated Effort
2-3 hours
