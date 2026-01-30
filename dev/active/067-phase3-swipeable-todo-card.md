# Task 067: Create SwipeableTodoCard Widget

## Phase
3 - UI Foundation & MVP

## Description
Wrap TodoCard with swipe gestures for quick actions.

## Steps
1. Create `lib/presentation/screens/main/widgets/swipeable_todo_card.dart`
2. Implement swipe right (complete) on Active tab
3. Implement swipe left (pause/resume) on Active tab
4. Implement swipe left (reopen) on Completed tab
5. Add visual feedback during swipe

## Code Structure
```dart
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_dimensions.dart';
import '../../../../core/navigation/routes.dart';
import '../../../../domain/usecases/todo/get_todos_usecase.dart';
import '../../../bloc/todo/todo_bloc.dart';
import '../../../bloc/todo/todo_event.dart';
import '../../../widgets/app_dialog.dart';
import 'todo_card.dart';

class SwipeableTodoCard extends StatelessWidget {
  final TodoWithSendCount todoWithCount;
  final bool isActiveTab;
  final bool isSending;

  const SwipeableTodoCard({
    super.key,
    required this.todoWithCount,
    required this.isActiveTab,
    this.isSending = false,
  });

  @override
  Widget build(BuildContext context) {
    if (isActiveTab) {
      return _buildActiveTabSwipeable(context);
    } else {
      return _buildCompletedTabSwipeable(context);
    }
  }

  Widget _buildActiveTabSwipeable(BuildContext context) {
    final todo = todoWithCount.todo;

    return Dismissible(
      key: ValueKey('swipe_${todo.id}'),
      confirmDismiss: (direction) async {
        if (direction == DismissDirection.startToEnd) {
          // Swipe Right: Complete
          return await _confirmComplete(context);
        } else if (direction == DismissDirection.endToStart) {
          // Swipe Left: Pause/Resume (no confirmation needed)
          _togglePause(context);
          return false; // Don't dismiss, just toggle
        }
        return false;
      },
      onDismissed: (direction) {
        if (direction == DismissDirection.startToEnd) {
          _completeTodo(context);
        }
      },
      background: _buildSwipeBackground(
        color: AppColors.success,
        icon: Icons.check_circle,
        label: 'Complete',
        alignment: Alignment.centerLeft,
      ),
      secondaryBackground: _buildSwipeBackground(
        color: todo.isPaused ? AppColors.primary : AppColors.warning,
        icon: todo.isPaused ? Icons.play_arrow : Icons.pause,
        label: todo.isPaused ? 'Resume' : 'Pause',
        alignment: Alignment.centerRight,
      ),
      child: TodoCard(
        todoWithCount: todoWithCount,
        isSending: isSending,
        onTap: () => _openEditScreen(context),
        onSendPressed: () => _sendEmail(context),
      ),
    );
  }

  Widget _buildCompletedTabSwipeable(BuildContext context) {
    final todo = todoWithCount.todo;

    return Dismissible(
      key: ValueKey('swipe_${todo.id}'),
      direction: DismissDirection.endToStart,
      confirmDismiss: (direction) async {
        return await _confirmReopen(context);
      },
      onDismissed: (direction) {
        _reopenTodo(context);
      },
      background: _buildSwipeBackground(
        color: AppColors.primary,
        icon: Icons.replay,
        label: 'Reopen',
        alignment: Alignment.centerRight,
      ),
      child: TodoCard(
        todoWithCount: todoWithCount,
        onTap: () => _openEditScreen(context),
      ),
    );
  }

  Widget _buildSwipeBackground({
    required Color color,
    required IconData icon,
    required String label,
    required Alignment alignment,
  }) {
    return Container(
      margin: const EdgeInsets.symmetric(
        horizontal: AppDimensions.spacingMd,
        vertical: AppDimensions.spacingSm,
      ),
      decoration: BoxDecoration(
        color: color,
        borderRadius: BorderRadius.circular(AppDimensions.radiusLg),
      ),
      alignment: alignment,
      padding: const EdgeInsets.symmetric(horizontal: 24),
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: alignment == Alignment.centerLeft
            ? [
                Icon(icon, color: Colors.white),
                const SizedBox(width: 8),
                Text(
                  label,
                  style: TextStyle(
                    color: Colors.white,
                    fontWeight: FontWeight.w600,
                  ),
                ),
              ]
            : [
                Text(
                  label,
                  style: TextStyle(
                    color: Colors.white,
                    fontWeight: FontWeight.w600,
                  ),
                ),
                const SizedBox(width: 8),
                Icon(icon, color: Colors.white),
              ],
      ),
    );
  }

  Future<bool> _confirmComplete(BuildContext context) async {
    return await AppDialog.showConfirmation(
      context: context,
      title: 'Complete TODO?',
      message: 'Mark "${todoWithCount.todo.subject}" as completed?',
      confirmText: 'Complete',
    );
  }

  Future<bool> _confirmReopen(BuildContext context) async {
    return await AppDialog.showConfirmation(
      context: context,
      title: 'Reopen TODO?',
      message: 'Reopen "${todoWithCount.todo.subject}"? This will recalculate the next send date.',
      confirmText: 'Reopen',
    );
  }

  void _completeTodo(BuildContext context) {
    context.read<TodoBloc>().add(CompleteTodo(todoWithCount.todo.id!));

    // Show undo snackbar
    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Text('TODO completed'),
        action: SnackBarAction(
          label: 'Undo',
          onPressed: () {
            context.read<TodoBloc>().add(
              UndoCompleteTodo(todoWithCount.todo.id!),
            );
          },
        ),
        duration: const Duration(seconds: 4),
      ),
    );
  }

  void _togglePause(BuildContext context) {
    final bloc = context.read<TodoBloc>();
    if (todoWithCount.todo.isPaused) {
      bloc.add(ResumeTodo(todoWithCount.todo.id!));
    } else {
      bloc.add(PauseTodo(todoWithCount.todo.id!));
    }
  }

  void _reopenTodo(BuildContext context) {
    context.read<TodoBloc>().add(ReopenTodo(todoWithCount.todo.id!));
  }

  void _openEditScreen(BuildContext context) {
    Navigator.pushNamed(
      context,
      Routes.editTodo,
      arguments: todoWithCount.todo.id,
    );
  }

  void _sendEmail(BuildContext context) async {
    final confirmed = await AppDialog.showConfirmation(
      context: context,
      title: 'Send Email?',
      message: 'Send follow-up email to ${todoWithCount.todo.recipientEmail}?',
      confirmText: 'Send',
    );

    if (confirmed) {
      context.read<TodoBloc>().add(SendEmailForTodo(todoWithCount.todo.id!));
    }
  }
}
```

## Acceptance Criteria
- [ ] Active Tab - Swipe Right: Confirmation → Complete → Undo Snackbar
- [ ] Active Tab - Swipe Left: Pause/Resume toggle (no dismiss)
- [ ] Completed Tab - Swipe Left: Confirmation → Reopen
- [ ] Visual swipe backgrounds with icons and labels
- [ ] Smooth swipe animations
- [ ] Confirmation dialogs before destructive actions
- [ ] Undo functionality for complete action

## Dependencies
- Task 059 (AppDialog)
- Task 062 (TodoBloc)
- Task 066 (TodoCard)

## Parallel Work
Can run parallel with: Task 065, 066

## Estimated Effort
2 hours
