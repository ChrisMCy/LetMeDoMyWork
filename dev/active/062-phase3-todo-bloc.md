# Task 062: Create TodoBloc

## Phase
3 - UI Foundation & MVP

## Description
Implement BLoC for TODO state management.

## Steps
1. Create `lib/presentation/bloc/todo/` directory
2. Create todo_bloc.dart, todo_event.dart, todo_state.dart
3. Implement all TODO operations

## Code Structure

### todo_event.dart
```dart
import 'package:equatable/equatable.dart';
import '../../../domain/entities/todo.dart';

abstract class TodoEvent extends Equatable {
  const TodoEvent();

  @override
  List<Object?> get props => [];
}

class LoadTodos extends TodoEvent {
  const LoadTodos();
}

class LoadCompletedTodos extends TodoEvent {
  const LoadCompletedTodos();
}

class CreateTodo extends TodoEvent {
  final Todo todo;

  const CreateTodo(this.todo);

  @override
  List<Object?> get props => [todo];
}

class UpdateTodo extends TodoEvent {
  final Todo todo;
  final bool intervalChanged;

  const UpdateTodo(this.todo, {this.intervalChanged = false});

  @override
  List<Object?> get props => [todo, intervalChanged];
}

class DeleteTodo extends TodoEvent {
  final int todoId;

  const DeleteTodo(this.todoId);

  @override
  List<Object?> get props => [todoId];
}

class CompleteTodo extends TodoEvent {
  final int todoId;

  const CompleteTodo(this.todoId);

  @override
  List<Object?> get props => [todoId];
}

class PauseTodo extends TodoEvent {
  final int todoId;

  const PauseTodo(this.todoId);

  @override
  List<Object?> get props => [todoId];
}

class ResumeTodo extends TodoEvent {
  final int todoId;

  const ResumeTodo(this.todoId);

  @override
  List<Object?> get props => [todoId];
}

class ReopenTodo extends TodoEvent {
  final int todoId;

  const ReopenTodo(this.todoId);

  @override
  List<Object?> get props => [todoId];
}

class SendEmailForTodo extends TodoEvent {
  final int todoId;

  const SendEmailForTodo(this.todoId);

  @override
  List<Object?> get props => [todoId];
}

class UndoCompleteTodo extends TodoEvent {
  final int todoId;

  const UndoCompleteTodo(this.todoId);

  @override
  List<Object?> get props => [todoId];
}
```

### todo_state.dart
```dart
import 'package:equatable/equatable.dart';
import '../../../domain/usecases/todo/get_todos_usecase.dart';

abstract class TodoState extends Equatable {
  const TodoState();

  @override
  List<Object?> get props => [];
}

class TodoInitial extends TodoState {
  const TodoInitial();
}

class TodoLoading extends TodoState {
  const TodoLoading();
}

class TodoLoaded extends TodoState {
  final List<TodoWithSendCount> activeTodos;
  final List<TodoWithSendCount> completedTodos;

  const TodoLoaded({
    required this.activeTodos,
    required this.completedTodos,
  });

  @override
  List<Object?> get props => [activeTodos, completedTodos];

  TodoLoaded copyWith({
    List<TodoWithSendCount>? activeTodos,
    List<TodoWithSendCount>? completedTodos,
  }) {
    return TodoLoaded(
      activeTodos: activeTodos ?? this.activeTodos,
      completedTodos: completedTodos ?? this.completedTodos,
    );
  }
}

class TodoError extends TodoState {
  final String message;

  const TodoError(this.message);

  @override
  List<Object?> get props => [message];
}

class TodoOperationSuccess extends TodoState {
  final String message;
  final TodoLoaded previousState;

  const TodoOperationSuccess({
    required this.message,
    required this.previousState,
  });

  @override
  List<Object?> get props => [message, previousState];
}

class TodoSending extends TodoState {
  final int todoId;
  final TodoLoaded previousState;

  const TodoSending({
    required this.todoId,
    required this.previousState,
  });

  @override
  List<Object?> get props => [todoId, previousState];
}
```

### todo_bloc.dart
```dart
import 'package:flutter_bloc/flutter_bloc.dart';
import '../../../domain/usecases/todo/create_todo_usecase.dart';
import '../../../domain/usecases/todo/get_todos_usecase.dart';
import '../../../domain/usecases/todo/update_todo_usecase.dart';
import '../../../domain/usecases/todo/delete_todo_usecase.dart';
import '../../../domain/usecases/todo/complete_todo_usecase.dart';
import '../../../domain/usecases/todo/pause_todo_usecase.dart';
import '../../../domain/usecases/todo/resume_todo_usecase.dart';
import '../../../domain/usecases/todo/reopen_todo_usecase.dart';
import '../../../domain/usecases/email/send_email_usecase.dart';
import 'todo_event.dart';
import 'todo_state.dart';

class TodoBloc extends Bloc<TodoEvent, TodoState> {
  final CreateTodoUseCase _createTodoUseCase;
  final GetActiveTodosUseCase _getActiveTodosUseCase;
  final GetCompletedTodosUseCase _getCompletedTodosUseCase;
  final UpdateTodoUseCase _updateTodoUseCase;
  final DeleteTodoUseCase _deleteTodoUseCase;
  final CompleteTodoUseCase _completeTodoUseCase;
  final PauseTodoUseCase _pauseTodoUseCase;
  final ResumeTodoUseCase _resumeTodoUseCase;
  final ReopenTodoUseCase _reopenTodoUseCase;
  final SendEmailUseCase _sendEmailUseCase;

  TodoBloc({
    required CreateTodoUseCase createTodoUseCase,
    required GetActiveTodosUseCase getActiveTodosUseCase,
    required GetCompletedTodosUseCase getCompletedTodosUseCase,
    required UpdateTodoUseCase updateTodoUseCase,
    required DeleteTodoUseCase deleteTodoUseCase,
    required CompleteTodoUseCase completeTodoUseCase,
    required PauseTodoUseCase pauseTodoUseCase,
    required ResumeTodoUseCase resumeTodoUseCase,
    required ReopenTodoUseCase reopenTodoUseCase,
    required SendEmailUseCase sendEmailUseCase,
  })  : _createTodoUseCase = createTodoUseCase,
        _getActiveTodosUseCase = getActiveTodosUseCase,
        _getCompletedTodosUseCase = getCompletedTodosUseCase,
        _updateTodoUseCase = updateTodoUseCase,
        _deleteTodoUseCase = deleteTodoUseCase,
        _completeTodoUseCase = completeTodoUseCase,
        _pauseTodoUseCase = pauseTodoUseCase,
        _resumeTodoUseCase = resumeTodoUseCase,
        _reopenTodoUseCase = reopenTodoUseCase,
        _sendEmailUseCase = sendEmailUseCase,
        super(const TodoInitial()) {
    on<LoadTodos>(_onLoadTodos);
    on<CreateTodo>(_onCreateTodo);
    on<UpdateTodo>(_onUpdateTodo);
    on<DeleteTodo>(_onDeleteTodo);
    on<CompleteTodo>(_onCompleteTodo);
    on<PauseTodo>(_onPauseTodo);
    on<ResumeTodo>(_onResumeTodo);
    on<ReopenTodo>(_onReopenTodo);
    on<SendEmailForTodo>(_onSendEmail);
    on<UndoCompleteTodo>(_onUndoComplete);
  }

  Future<void> _onLoadTodos(LoadTodos event, Emitter<TodoState> emit) async {
    emit(const TodoLoading());
    try {
      final active = await _getActiveTodosUseCase.execute();
      final completed = await _getCompletedTodosUseCase.execute();
      emit(TodoLoaded(activeTodos: active, completedTodos: completed));
    } catch (e) {
      emit(TodoError('Failed to load TODOs: $e'));
    }
  }

  Future<void> _onCreateTodo(CreateTodo event, Emitter<TodoState> emit) async {
    final currentState = state;
    try {
      final result = await _createTodoUseCase.execute(event.todo);
      if (result.isFailure) {
        emit(TodoError(result.error!));
        return;
      }
      add(const LoadTodos()); // Reload list
    } catch (e) {
      emit(TodoError('Failed to create TODO: $e'));
    }
  }

  // ... similar implementations for other events
}
```

## Acceptance Criteria
- [ ] TodoBloc handles all events
- [ ] States properly emitted (Loading, Loaded, Error, Success)
- [ ] Undo support for complete action
- [ ] Sending state for email sending
- [ ] Proper error handling
- [ ] State contains both active and completed todos

## Dependencies
- Task 033-037 (TODO Use Cases: Create, Get, Update, Complete, Delete)
- Task 037a-037c (TODO Use Cases: Pause, Resume, Reopen)
- Task 045 (SendEmailUseCase)

## Parallel Work
Can run parallel with: Task 061

## Estimated Effort
3-4 hours
