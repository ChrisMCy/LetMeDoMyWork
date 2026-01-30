# Task 092: Create Inactivity Dialog

## Phase
5 - Background Service & Notifications

## Description
Implement the dialog shown when user returns after 7+ days of inactivity.

## Steps
1. Create `lib/presentation/widgets/inactivity_dialog.dart`
2. Show on app resume if TODOs were paused
3. Offer "Resume All" and "Keep Paused" options

## Code Structure
```dart
import 'package:flutter/material.dart';
import '../../core/di/injection.dart';
import '../../core/theme/app_colors.dart';
import '../../core/theme/app_dimensions.dart';
import '../../services/lifecycle/app_lifecycle_service.dart';
import 'app_button.dart';

class InactivityDialog extends StatefulWidget {
  final int pausedCount;

  const InactivityDialog({
    super.key,
    required this.pausedCount,
  });

  /// Show the dialog and return user choice
  static Future<InactivityChoice?> show(
    BuildContext context,
    int pausedCount,
  ) async {
    return showDialog<InactivityChoice>(
      context: context,
      barrierDismissible: false,
      builder: (context) => InactivityDialog(pausedCount: pausedCount),
    );
  }

  @override
  State<InactivityDialog> createState() => _InactivityDialogState();
}

enum InactivityChoice { resumeAll, keepPaused }

class _InactivityDialogState extends State<InactivityDialog> {
  final _lifecycleService = getIt<AppLifecycleService>();
  bool _isLoading = false;

  Future<void> _resumeAll() async {
    setState(() => _isLoading = true);

    await _lifecycleService.resumeAllTodos();

    if (mounted) {
      Navigator.pop(context, InactivityChoice.resumeAll);
    }
  }

  void _keepPaused() {
    Navigator.pop(context, InactivityChoice.keepPaused);
  }

  @override
  Widget build(BuildContext context) {
    return AlertDialog(
      title: Row(
        children: [
          Icon(
            Icons.access_time,
            color: AppColors.warning,
          ),
          const SizedBox(width: 8),
          const Text('Welcome Back!'),
        ],
      ),
      content: Column(
        mainAxisSize: MainAxisSize.min,
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            "It's been a while since you last used the app.",
            style: Theme.of(context).textTheme.bodyLarge,
          ),
          const SizedBox(height: 16),
          Container(
            padding: const EdgeInsets.all(12),
            decoration: BoxDecoration(
              color: AppColors.warning.withOpacity(0.1),
              borderRadius: BorderRadius.circular(8),
              border: Border.all(color: AppColors.warning.withOpacity(0.3)),
            ),
            child: Row(
              children: [
                Icon(Icons.pause_circle, color: AppColors.warning),
                const SizedBox(width: 12),
                Expanded(
                  child: Column(
                    crossAxisAlignment: CrossAxisAlignment.start,
                    children: [
                      Text(
                        '${widget.pausedCount} TODOs paused',
                        style: const TextStyle(fontWeight: FontWeight.bold),
                      ),
                      const Text(
                        'To prevent unwanted emails being sent',
                        style: TextStyle(fontSize: 12),
                      ),
                    ],
                  ),
                ),
              ],
            ),
          ),
          const SizedBox(height: 16),
          const Text(
            'What would you like to do?',
            style: TextStyle(fontWeight: FontWeight.w500),
          ),
        ],
      ),
      actions: [
        TextButton(
          onPressed: _isLoading ? null : _keepPaused,
          child: const Text('Keep Paused'),
        ),
        AppButton.primary(
          text: 'Resume All',
          isLoading: _isLoading,
          onPressed: _resumeAll,
        ),
      ],
    );
  }
}
```

## Integration in MainScreen
```dart
class _MainScreenState extends State<MainScreen> {
  @override
  void initState() {
    super.initState();
    _checkInactivity();
  }

  Future<void> _checkInactivity() async {
    final lifecycleService = getIt<AppLifecycleService>();
    final result = await lifecycleService.checkInactivityManual();

    if (result.requiresUserAction && mounted) {
      final choice = await InactivityDialog.show(
        context,
        result.pausedCount,
      );

      if (choice == InactivityChoice.resumeAll) {
        // Reload todos
        context.read<TodoBloc>().add(const LoadTodos());

        ScaffoldMessenger.of(context).showSnackBar(
          SnackBar(
            content: Text('${result.pausedCount} TODOs resumed'),
            backgroundColor: AppColors.success,
          ),
        );
      }
    }
  }

  // ... rest of MainScreen
}
```

## Acceptance Criteria
- [ ] Dialog shown when TODOs were paused
- [ ] Shows count of paused TODOs
- [ ] "Resume All" recalculates next_send and resumes
- [ ] "Keep Paused" keeps TODOs paused
- [ ] Loading state during resume
- [ ] Cannot dismiss without choosing
- [ ] TODO list reloads after choice

## Dependencies
- Task 091 (AppLifecycleService)
- Task 056 (AppButton)
- Task 064 (MainScreen integration)

## Parallel Work
Must run after: Task 091

## Estimated Effort
1.5 hours
