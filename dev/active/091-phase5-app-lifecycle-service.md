# Task 091: Create App Lifecycle Service

## Phase
5 - Background Service & Notifications

## Description
Implement app lifecycle tracking and 7-day inactivity handling.

## Steps
1. Create `lib/services/lifecycle/app_lifecycle_service.dart`
2. Track last_opened timestamp
3. Implement 7-day inactivity check
4. Pause all TODOs when inactive

## Code Structure
```dart
import 'package:flutter/material.dart';
import 'package:shared_preferences/shared_preferences.dart';
import '../../domain/repositories/todo_repository.dart';
import '../../domain/repositories/settings_repository.dart';
import '../notifications/notification_service.dart';

class AppLifecycleService with WidgetsBindingObserver {
  static const String _lastOpenedKey = 'last_opened_at';
  static const int _inactivityDays = 7;

  final TodoRepository _todoRepository;
  final SettingsRepository _settingsRepository;
  final NotificationService _notificationService;

  bool _hasCheckedInactivity = false;
  DateTime? _lastOpened;

  AppLifecycleService(
    this._todoRepository,
    this._settingsRepository,
    this._notificationService,
  );

  /// Initialize and register as lifecycle observer
  Future<void> initialize() async {
    WidgetsBinding.instance.addObserver(this);
    await _loadLastOpened();
  }

  /// Dispose resources
  void dispose() {
    WidgetsBinding.instance.removeObserver(this);
  }

  @override
  void didChangeAppLifecycleState(AppLifecycleState state) {
    if (state == AppLifecycleState.resumed) {
      _onAppResumed();
    } else if (state == AppLifecycleState.paused) {
      _onAppPaused();
    }
  }

  Future<void> _loadLastOpened() async {
    final prefs = await SharedPreferences.getInstance();
    final timestamp = prefs.getString(_lastOpenedKey);

    if (timestamp != null) {
      _lastOpened = DateTime.tryParse(timestamp);
    }
  }

  Future<void> _saveLastOpened() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setString(
      _lastOpenedKey,
      DateTime.now().toIso8601String(),
    );
  }

  void _onAppResumed() {
    _checkInactivity();
    _saveLastOpened();
  }

  void _onAppPaused() {
    _saveLastOpened();
  }

  /// Check for 7-day inactivity and return true if TODOs were paused
  Future<InactivityCheckResult> _checkInactivity() async {
    if (_hasCheckedInactivity) {
      return InactivityCheckResult.alreadyChecked;
    }

    _hasCheckedInactivity = true;

    if (_lastOpened == null) {
      return InactivityCheckResult.firstLaunch;
    }

    final daysSinceLastOpen = DateTime.now().difference(_lastOpened!).inDays;

    if (daysSinceLastOpen >= _inactivityDays) {
      // Pause all active TODOs
      final pausedCount = await _pauseAllActiveTodos();

      if (pausedCount > 0) {
        // Show notification
        await _notificationService.showInactivityNotification();

        return InactivityCheckResult.todosPaused(pausedCount);
      }
    }

    return InactivityCheckResult.noAction;
  }

  /// Manually check inactivity (called from UI)
  Future<InactivityCheckResult> checkInactivityManual() async {
    _hasCheckedInactivity = false;
    return _checkInactivity();
  }

  Future<int> _pauseAllActiveTodos() async {
    final activeTodos = await _todoRepository.getActiveTodos();
    int count = 0;

    for (final todo in activeTodos) {
      if (!todo.isPaused) {
        await _todoRepository.pauseTodo(todo.id!);
        count++;
      }
    }

    return count;
  }

  /// Resume all paused TODOs (after user confirms)
  Future<int> resumeAllTodos() async {
    final settings = await _settingsRepository.getSettings();
    final pausedTodos = await _todoRepository.getPausedTodos();
    int count = 0;

    for (final todo in pausedTodos) {
      // Calculate new next_send_datetime
      final nextSend = _calculateNextSend(
        currentDate: DateTime.now(),
        sendTime: todo.sendTime,
        intervalDays: todo.intervalDays,
        randomizeMinutes: settings.randomizeMinutes,
      );

      await _todoRepository.resumeTodo(todo.id!, nextSend);
      count++;
    }

    return count;
  }

  DateTime _calculateNextSend({
    required DateTime currentDate,
    required TimeOfDay sendTime,
    required int intervalDays,
    required int randomizeMinutes,
  }) {
    final random = Random();
    final randomOffset = random.nextInt(randomizeMinutes * 2) - randomizeMinutes;

    var nextDate = currentDate.add(Duration(days: intervalDays));
    nextDate = DateTime(
      nextDate.year,
      nextDate.month,
      nextDate.day,
      sendTime.hour,
      sendTime.minute + randomOffset,
    );

    return nextDate;
  }
}

/// Result of inactivity check
class InactivityCheckResult {
  final bool requiresUserAction;
  final int pausedCount;
  final String? message;

  InactivityCheckResult._({
    required this.requiresUserAction,
    this.pausedCount = 0,
    this.message,
  });

  static InactivityCheckResult get alreadyChecked =>
      InactivityCheckResult._(requiresUserAction: false);

  static InactivityCheckResult get firstLaunch =>
      InactivityCheckResult._(requiresUserAction: false);

  static InactivityCheckResult get noAction =>
      InactivityCheckResult._(requiresUserAction: false);

  static InactivityCheckResult todosPaused(int count) =>
      InactivityCheckResult._(
        requiresUserAction: true,
        pausedCount: count,
        message: '$count TODOs have been paused due to 7 days of inactivity.',
      );
}
```

## Acceptance Criteria
- [ ] Tracks last_opened timestamp
- [ ] Detects 7+ days of inactivity
- [ ] Pauses all active TODOs when inactive
- [ ] Shows notification when TODOs paused
- [ ] Resume all function works
- [ ] Recalculates next_send on resume
- [ ] Only checks once per app launch

## Dependencies
- Task 026-028 (Repositories)
- Task 088 (NotificationService)

## Parallel Work
Can run parallel with: Task 088-090

## Estimated Effort
2 hours
