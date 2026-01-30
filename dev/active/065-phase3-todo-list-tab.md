# Task 065: Create TodoListTab Widget

## Phase
3 - UI Foundation & MVP

## Description
Implement the scrollable TODO list for each tab.

## Steps
1. Create `lib/presentation/screens/main/widgets/todo_list_tab.dart`
2. Implement list with sorting
3. Add pull-to-refresh
4. Handle empty state

## Code Structure
```dart
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import '../../../../domain/usecases/todo/get_todos_usecase.dart';
import '../../../bloc/todo/todo_bloc.dart';
import '../../../bloc/todo/todo_event.dart';
import 'swipeable_todo_card.dart';
import 'empty_state.dart';

class TodoListTab extends StatelessWidget {
  final List<TodoWithSendCount> todos;
  final bool isActiveTab;
  final String emptyMessage;
  final String? emptySubMessage;
  final int? sendingTodoId;

  const TodoListTab({
    super.key,
    required this.todos,
    required this.isActiveTab,
    this.emptyMessage = 'No TODOs',
    this.emptySubMessage,
    this.sendingTodoId,
  });

  @override
  Widget build(BuildContext context) {
    if (todos.isEmpty) {
      return EmptyState(
        message: emptyMessage,
        subMessage: emptySubMessage,
        icon: isActiveTab ? Icons.inbox_outlined : Icons.check_circle_outline,
      );
    }

    return RefreshIndicator(
      onRefresh: () async {
        context.read<TodoBloc>().add(const LoadTodos());
        // Wait a bit for the bloc to process
        await Future.delayed(const Duration(milliseconds: 500));
      },
      child: ListView.builder(
        padding: const EdgeInsets.only(
          top: 8,
          bottom: 88, // Space for FAB
        ),
        itemCount: todos.length,
        itemBuilder: (context, index) {
          final todoWithCount = todos[index];
          return SwipeableTodoCard(
            key: ValueKey(todoWithCount.todo.id),
            todoWithCount: todoWithCount,
            isActiveTab: isActiveTab,
            isSending: sendingTodoId == todoWithCount.todo.id,
          );
        },
      ),
    );
  }
}
```

## List Item Animation (Optional Enhancement)
```dart
class AnimatedTodoList extends StatelessWidget {
  final List<TodoWithSendCount> todos;
  final bool isActiveTab;

  const AnimatedTodoList({
    super.key,
    required this.todos,
    required this.isActiveTab,
  });

  @override
  Widget build(BuildContext context) {
    return AnimatedList(
      initialItemCount: todos.length,
      itemBuilder: (context, index, animation) {
        return SlideTransition(
          position: animation.drive(
            Tween(
              begin: const Offset(1, 0),
              end: Offset.zero,
            ).chain(CurveTween(curve: Curves.easeOut)),
          ),
          child: FadeTransition(
            opacity: animation,
            child: SwipeableTodoCard(
              todoWithCount: todos[index],
              isActiveTab: isActiveTab,
            ),
          ),
        );
      },
    );
  }
}
```

## Sorting Logic (Already in UseCase, but for reference)
```dart
// Sorting rules from BusinessLogik.md:
// Active TODOs:
// 1. Non-paused first, then paused
// 2. By send_count DESC (most sent first)
// 3. By created_at ASC (oldest first)

// Completed TODOs:
// 1. By completed_at DESC (most recently completed first)
```

## Acceptance Criteria
- [ ] Displays list of TODO cards
- [ ] Pull-to-refresh triggers reload
- [ ] Empty state when no TODOs
- [ ] Different empty states for Active vs Completed
- [ ] Proper padding for FAB overlap
- [ ] Smooth scrolling
- [ ] Sending state indicator on specific card

## Dependencies
- Task 062 (TodoBloc)
- Task 066 (SwipeableTodoCard)

## Parallel Work
Can run parallel with: Task 064

## Estimated Effort
1 hour
