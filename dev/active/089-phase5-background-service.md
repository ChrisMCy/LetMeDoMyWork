# Task 089: Create Background Service

## Phase
5 - Background Service & Notifications

## Description
Implement background service using WorkManager for automatic email sending.

## Steps
1. Create `lib/services/background/background_service.dart`
2. Configure WorkManager
3. Implement periodic check task
4. Implement email send task

## Code Structure
```dart
import 'package:workmanager/workmanager.dart';
import '../../../core/di/injection.dart';
import '../../../domain/repositories/todo_repository.dart';
import '../../../domain/repositories/settings_repository.dart';
import '../../../domain/usecases/email/send_email_usecase.dart';
import '../notifications/notification_service.dart';
import '../network/connectivity_service.dart';

// Task names
const String checkTodosTask = 'checkTodosTask';
const String sendEmailTask = 'sendEmailTask';

/// Top-level callback for WorkManager
@pragma('vm:entry-point')
void callbackDispatcher() {
  Workmanager().executeTask((task, inputData) async {
    // Initialize dependencies
    await setupDependencyInjection();

    switch (task) {
      case checkTodosTask:
        return await _executeCheckTodos();
      case sendEmailTask:
        final todoId = inputData?['todoId'] as int?;
        if (todoId != null) {
          return await _executeSendEmail(todoId);
        }
        return false;
      default:
        return false;
    }
  });
}

Future<bool> _executeCheckTodos() async {
  try {
    final todoRepository = getIt<TodoRepository>();
    final settingsRepository = getIt<SettingsRepository>();
    final connectivityService = getIt<ConnectivityService>();
    final notificationService = NotificationService();

    // Check connectivity
    final isOnline = await connectivityService.isConnected();

    // Get TODOs that need to be sent
    final now = DateTime.now();
    final todosToSend = await todoRepository.getTodosReadyToSend(now);

    if (todosToSend.isEmpty) {
      return true;
    }

    if (!isOnline) {
      // Mark as pending and notify
      await notificationService.showPendingSendsNotification(todosToSend.length);
      return true;
    }

    // Send emails
    final sendEmailUseCase = getIt<SendEmailUseCase>();

    for (final todo in todosToSend) {
      final result = await sendEmailUseCase.execute(todoId: todo.id!);

      if (result.isSuccess) {
        await notificationService.showEmailSentNotification(
          recipientName: todo.recipientFirstName ?? todo.recipientEmail,
          subject: todo.subject,
          todoId: todo.id,
        );
      } else {
        await notificationService.showEmailFailedNotification(
          recipientName: todo.recipientFirstName ?? todo.recipientEmail,
          error: result.error ?? 'Unknown error',
          todoId: todo.id,
        );
      }
    }

    return true;
  } catch (e) {
    print('Background task error: $e');
    return false;
  }
}

Future<bool> _executeSendEmail(int todoId) async {
  try {
    final sendEmailUseCase = getIt<SendEmailUseCase>();
    final notificationService = NotificationService();
    final todoRepository = getIt<TodoRepository>();

    final todo = await todoRepository.getTodoById(todoId);
    if (todo == null) return false;

    final result = await sendEmailUseCase.execute(todoId: todoId);

    if (result.isSuccess) {
      await notificationService.showEmailSentNotification(
        recipientName: todo.recipientFirstName ?? todo.recipientEmail,
        subject: todo.subject,
        todoId: todo.id,
      );
    } else {
      await notificationService.showEmailFailedNotification(
        recipientName: todo.recipientFirstName ?? todo.recipientEmail,
        error: result.error ?? 'Unknown error',
        todoId: todo.id,
      );
    }

    return result.isSuccess;
  } catch (e) {
    return false;
  }
}

class BackgroundService {
  static final BackgroundService _instance = BackgroundService._internal();
  factory BackgroundService() => _instance;
  BackgroundService._internal();

  Future<void> initialize() async {
    await Workmanager().initialize(
      callbackDispatcher,
      isInDebugMode: false,
    );
  }

  /// Start periodic check (every 15 minutes)
  Future<void> startPeriodicCheck() async {
    await Workmanager().registerPeriodicTask(
      'periodic_check',
      checkTodosTask,
      frequency: const Duration(minutes: 15),
      constraints: Constraints(
        networkType: NetworkType.connected,
        requiresBatteryNotLow: true,
      ),
      existingWorkPolicy: ExistingWorkPolicy.keep,
    );
  }

  /// Schedule specific email send
  Future<void> scheduleEmailSend({
    required int todoId,
    required DateTime sendAt,
  }) async {
    final delay = sendAt.difference(DateTime.now());

    if (delay.isNegative) {
      // Should have been sent already, send now
      await Workmanager().registerOneOffTask(
        'send_$todoId',
        sendEmailTask,
        inputData: {'todoId': todoId},
        constraints: Constraints(networkType: NetworkType.connected),
      );
    } else {
      await Workmanager().registerOneOffTask(
        'send_$todoId',
        sendEmailTask,
        inputData: {'todoId': todoId},
        initialDelay: delay,
        constraints: Constraints(networkType: NetworkType.connected),
      );
    }
  }

  /// Cancel scheduled email send
  Future<void> cancelScheduledSend(int todoId) async {
    await Workmanager().cancelByUniqueName('send_$todoId');
  }

  /// Cancel all background tasks
  Future<void> cancelAll() async {
    await Workmanager().cancelAll();
  }
}
```

## Repository Addition
```dart
// In TodoRepository interface
Future<List<Todo>> getTodosReadyToSend(DateTime currentTime);

// In TodoRepositoryImpl
@override
Future<List<Todo>> getTodosReadyToSend(DateTime currentTime) async {
  final db = await _databaseHelper.database;

  final result = await db.query(
    'todos',
    where: 'is_completed = 0 AND is_paused = 0 AND next_send_datetime <= ?',
    whereArgs: [currentTime.toIso8601String()],
  );

  return result.map((map) => TodoModel.fromMap(map)).toList();
}
```

## Initialize in main.dart
```dart
void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  await setupDependencyInjection();

  // Initialize background service
  await BackgroundService().initialize();
  await BackgroundService().startPeriodicCheck();

  runApp(LetMeDoMyWorkApp(...));
}
```

## Acceptance Criteria
- [ ] WorkManager initialized correctly
- [ ] Periodic task runs every ~15 minutes
- [ ] Checks for TODOs ready to send
- [ ] Sends emails when online
- [ ] Shows notifications on success/failure
- [ ] Handles offline state (marks pending)
- [ ] Scheduled sends can be cancelled
- [ ] Survives app restart

## Dependencies
- Task 007 (pubspec with workmanager)
- Task 008 (AndroidManifest permissions)
- Task 045 (SendEmailUseCase)
- Task 088 (NotificationService)

## Parallel Work
Can run parallel with: Task 088

## Estimated Effort
4-5 hours
