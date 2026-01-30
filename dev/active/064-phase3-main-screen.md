# Task 064: Create Main Screen

## Phase
3 - UI Foundation & MVP

## Description
Implement the main screen with two tabs (Active/Completed).

## Steps
1. Create `lib/presentation/screens/main/main_screen.dart`
2. Implement TabBar with Active and Completed tabs
3. Add FAB for creating new TODO
4. Add header with Settings and Statistics icons

## Code Structure
```dart
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import '../../../core/navigation/routes.dart';
import '../../../core/theme/app_colors.dart';
import '../../bloc/todo/todo_bloc.dart';
import '../../bloc/todo/todo_event.dart';
import '../../bloc/todo/todo_state.dart';
import 'widgets/todo_list_tab.dart';
import '../../widgets/loading_indicator.dart';

class MainScreen extends StatefulWidget {
  const MainScreen({super.key});

  @override
  State<MainScreen> createState() => _MainScreenState();
}

class _MainScreenState extends State<MainScreen>
    with SingleTickerProviderStateMixin {
  late TabController _tabController;

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 2, vsync: this);
    context.read<TodoBloc>().add(const LoadTodos());
  }

  @override
  void dispose() {
    _tabController.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('LetMeDoMyWork'),
        actions: [
          IconButton(
            icon: const Icon(Icons.bar_chart),
            tooltip: 'Statistics',
            onPressed: () => Navigator.pushNamed(context, Routes.statistics),
          ),
          IconButton(
            icon: const Icon(Icons.settings),
            tooltip: 'Settings',
            onPressed: () => Navigator.pushNamed(context, Routes.settings),
          ),
        ],
        bottom: TabBar(
          controller: _tabController,
          tabs: const [
            Tab(text: 'Active'),
            Tab(text: 'Completed'),
          ],
        ),
      ),
      body: BlocConsumer<TodoBloc, TodoState>(
        listener: (context, state) {
          if (state is TodoError) {
            ScaffoldMessenger.of(context).showSnackBar(
              SnackBar(
                content: Text(state.message),
                backgroundColor: AppColors.error,
              ),
            );
          }
          if (state is TodoOperationSuccess) {
            ScaffoldMessenger.of(context).showSnackBar(
              SnackBar(content: Text(state.message)),
            );
          }
        },
        builder: (context, state) {
          if (state is TodoLoading) {
            return const TodoListSkeleton();
          }

          if (state is TodoLoaded) {
            return TabBarView(
              controller: _tabController,
              children: [
                TodoListTab(
                  todos: state.activeTodos,
                  isActiveTab: true,
                  emptyMessage: 'No active TODOs',
                  emptySubMessage: 'Tap + to create your first follow-up',
                ),
                TodoListTab(
                  todos: state.completedTodos,
                  isActiveTab: false,
                  emptyMessage: 'No completed TODOs',
                  emptySubMessage: 'Complete a TODO by swiping right',
                ),
              ],
            );
          }

          if (state is TodoSending) {
            return TabBarView(
              controller: _tabController,
              children: [
                TodoListTab(
                  todos: state.previousState.activeTodos,
                  isActiveTab: true,
                  sendingTodoId: state.todoId,
                ),
                TodoListTab(
                  todos: state.previousState.completedTodos,
                  isActiveTab: false,
                ),
              ],
            );
          }

          // Initial or error state - show empty
          return const Center(
            child: Text('Pull down to refresh'),
          );
        },
      ),
      floatingActionButton: AnimatedBuilder(
        animation: _tabController,
        builder: (context, child) {
          // Only show FAB on Active tab
          return AnimatedOpacity(
            opacity: _tabController.index == 0 ? 1.0 : 0.0,
            duration: const Duration(milliseconds: 200),
            child: FloatingActionButton(
              onPressed: _tabController.index == 0
                  ? () => Navigator.pushNamed(context, Routes.createTodo)
                  : null,
              child: const Icon(Icons.add),
            ),
          );
        },
      ),
    );
  }
}
```

## Empty State Widget
```dart
class EmptyState extends StatelessWidget {
  final String message;
  final String? subMessage;
  final IconData icon;

  const EmptyState({
    super.key,
    required this.message,
    this.subMessage,
    this.icon = Icons.inbox_outlined,
  });

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(32),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(
              icon,
              size: 64,
              color: AppColors.onSurfaceVariant,
            ),
            const SizedBox(height: 16),
            Text(
              message,
              style: AppTextStyles.titleMedium,
              textAlign: TextAlign.center,
            ),
            if (subMessage != null) ...[
              const SizedBox(height: 8),
              Text(
                subMessage!,
                style: AppTextStyles.bodyMedium.copyWith(
                  color: AppColors.onSurfaceVariant,
                ),
                textAlign: TextAlign.center,
              ),
            ],
          ],
        ),
      ),
    );
  }
}
```

## Acceptance Criteria
- [ ] Two tabs (Active/Completed)
- [ ] AppBar with title, Statistics icon, Settings icon
- [ ] FAB only visible on Active tab
- [ ] Loading state shows skeleton
- [ ] Error state shows snackbar
- [ ] Empty states for each tab
- [ ] Pull-to-refresh support

## Dependencies
- Task 054-055 (Navigation)
- Task 060 (Loading Indicator)
- Task 062 (TodoBloc)

## Parallel Work
Can run parallel with: Task 065

## Estimated Effort
2-3 hours
