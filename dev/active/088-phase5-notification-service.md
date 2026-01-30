# Task 088: Create Notification Service

## Phase
5 - Background Service & Notifications

## Description
Implement notification service using flutter_local_notifications.

## Steps
1. Create `lib/services/notifications/notification_service.dart`
2. Configure notification channels
3. Implement show notification methods

## Code Structure
```dart
import 'package:flutter_local_notifications/flutter_local_notifications.dart';

class NotificationService {
  static final NotificationService _instance = NotificationService._internal();
  factory NotificationService() => _instance;
  NotificationService._internal();

  final FlutterLocalNotificationsPlugin _notifications =
      FlutterLocalNotificationsPlugin();

  static const String _channelId = 'letmedomywork_channel';
  static const String _channelName = 'LetMeDoMyWork Notifications';
  static const String _channelDescription = 'Notifications for email sends';

  Future<void> initialize() async {
    const androidSettings = AndroidInitializationSettings('@mipmap/ic_launcher');

    const initSettings = InitializationSettings(
      android: androidSettings,
    );

    await _notifications.initialize(
      initSettings,
      onDidReceiveNotificationResponse: _onNotificationTap,
    );

    // Create notification channel (Android 8.0+)
    await _createNotificationChannel();
  }

  Future<void> _createNotificationChannel() async {
    const channel = AndroidNotificationChannel(
      _channelId,
      _channelName,
      description: _channelDescription,
      importance: Importance.high,
    );

    await _notifications
        .resolvePlatformSpecificImplementation<
            AndroidFlutterLocalNotificationsPlugin>()
        ?.createNotificationChannel(channel);
  }

  void _onNotificationTap(NotificationResponse response) {
    // Handle notification tap
    // Navigate to specific TODO if payload contains todoId
    final payload = response.payload;
    if (payload != null) {
      // Parse and handle navigation
    }
  }

  /// Show notification for successful email send
  Future<void> showEmailSentNotification({
    required String recipientName,
    required String subject,
    int? todoId,
  }) async {
    const androidDetails = AndroidNotificationDetails(
      _channelId,
      _channelName,
      channelDescription: _channelDescription,
      importance: Importance.high,
      priority: Priority.high,
      icon: '@mipmap/ic_launcher',
    );

    const details = NotificationDetails(android: androidDetails);

    await _notifications.show(
      DateTime.now().millisecondsSinceEpoch ~/ 1000,
      'Email Sent',
      'Follow-up sent to $recipientName: $subject',
      details,
      payload: todoId?.toString(),
    );
  }

  /// Show notification for email send failure
  Future<void> showEmailFailedNotification({
    required String recipientName,
    required String error,
    int? todoId,
  }) async {
    const androidDetails = AndroidNotificationDetails(
      _channelId,
      _channelName,
      channelDescription: _channelDescription,
      importance: Importance.high,
      priority: Priority.high,
      icon: '@mipmap/ic_launcher',
      color: Color(0xFFE53935), // Red
    );

    const details = NotificationDetails(android: androidDetails);

    await _notifications.show(
      DateTime.now().millisecondsSinceEpoch ~/ 1000,
      'Email Send Failed',
      'Could not send to $recipientName: $error',
      details,
      payload: todoId?.toString(),
    );
  }

  /// Show notification for 7-day inactivity
  Future<void> showInactivityNotification() async {
    const androidDetails = AndroidNotificationDetails(
      _channelId,
      _channelName,
      channelDescription: _channelDescription,
      importance: Importance.high,
      priority: Priority.high,
      icon: '@mipmap/ic_launcher',
    );

    const details = NotificationDetails(android: androidDetails);

    await _notifications.show(
      1, // Fixed ID for inactivity
      'TODOs Paused',
      'Your TODOs have been paused due to inactivity. Open the app to resume.',
      details,
    );
  }

  /// Show notification for pending sends (offline)
  Future<void> showPendingSendsNotification(int count) async {
    const androidDetails = AndroidNotificationDetails(
      _channelId,
      _channelName,
      channelDescription: _channelDescription,
      importance: Importance.defaultImportance,
      priority: Priority.defaultPriority,
      icon: '@mipmap/ic_launcher',
    );

    const details = NotificationDetails(android: androidDetails);

    await _notifications.show(
      2, // Fixed ID for pending
      'Pending Emails',
      '$count emails waiting to be sent when online',
      details,
    );
  }

  /// Cancel all notifications
  Future<void> cancelAll() async {
    await _notifications.cancelAll();
  }

  /// Cancel specific notification
  Future<void> cancel(int id) async {
    await _notifications.cancel(id);
  }
}
```

## Initialize in main.dart
```dart
void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  // ... other initialization

  // Initialize notifications
  await NotificationService().initialize();

  runApp(LetMeDoMyWorkApp(...));
}
```

## Acceptance Criteria
- [ ] Notification channel created
- [ ] Email sent notification shows recipient and subject
- [ ] Email failed notification shows error
- [ ] Inactivity notification works
- [ ] Pending sends notification shows count
- [ ] Notification tap navigates to app
- [ ] Cancel notifications works

## Dependencies
- Task 007 (pubspec with flutter_local_notifications)
- Task 008 (AndroidManifest permissions)

## Parallel Work
Can run parallel with: Task 089

## Estimated Effort
2 hours
