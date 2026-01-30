# Task 084: Create Export Service

## Phase
4 - Advanced Features

## Description
Implement service for exporting app data to JSON.

## Steps
1. Create `lib/services/backup/export_service.dart`
2. Serialize all data to JSON
3. Save to Downloads folder
4. Option to send via email

## Code Structure
```dart
import 'dart:convert';
import 'dart:io';
import 'package:path_provider/path_provider.dart';
import '../../domain/entities/todo.dart';
import '../../domain/entities/settings.dart';
import '../../domain/entities/sent_email.dart';
import '../../domain/repositories/todo_repository.dart';
import '../../domain/repositories/settings_repository.dart';

class ExportData {
  final Settings settings;
  final List<Todo> todos;
  final List<SentEmail> sentEmails;
  final DateTime exportedAt;
  final String appVersion;

  ExportData({
    required this.settings,
    required this.todos,
    required this.sentEmails,
    required this.exportedAt,
    required this.appVersion,
  });

  Map<String, dynamic> toJson() {
    return {
      'version': appVersion,
      'exportedAt': exportedAt.toIso8601String(),
      'settings': settings.toJson(),
      'todos': todos.map((t) => t.toJson()).toList(),
      'sentEmails': sentEmails.map((e) => e.toJson()).toList(),
    };
  }
}

class ExportService {
  final TodoRepository _todoRepository;
  final SettingsRepository _settingsRepository;

  ExportService(this._todoRepository, this._settingsRepository);

  /// Export all data to JSON file
  Future<Result<String>> exportToFile() async {
    try {
      // Gather all data
      final settings = await _settingsRepository.getSettings();
      final todos = await _todoRepository.getAllTodos();
      final sentEmails = await _todoRepository.getAllSentEmails();

      final exportData = ExportData(
        settings: settings,
        todos: todos,
        sentEmails: sentEmails,
        exportedAt: DateTime.now(),
        appVersion: '1.0.0',
      );

      // Convert to JSON
      final jsonString = const JsonEncoder.withIndent('  ')
          .convert(exportData.toJson());

      // Save to file
      final directory = await getExternalStorageDirectory();
      if (directory == null) {
        return Result.failure('Could not access storage');
      }

      final fileName = 'letmedomywork_backup_${_formatDate(DateTime.now())}.json';
      final filePath = '${directory.path}/$fileName';

      final file = File(filePath);
      await file.writeAsString(jsonString);

      return Result.success(filePath);
    } catch (e) {
      return Result.failure('Export failed: $e');
    }
  }

  /// Export to JSON string (for email attachment)
  Future<Result<String>> exportToJsonString() async {
    try {
      final settings = await _settingsRepository.getSettings();
      final todos = await _todoRepository.getAllTodos();
      final sentEmails = await _todoRepository.getAllSentEmails();

      final exportData = ExportData(
        settings: settings,
        todos: todos,
        sentEmails: sentEmails,
        exportedAt: DateTime.now(),
        appVersion: '1.0.0',
      );

      final jsonString = const JsonEncoder.withIndent('  ')
          .convert(exportData.toJson());

      return Result.success(jsonString);
    } catch (e) {
      return Result.failure('Export failed: $e');
    }
  }

  /// Get export file size estimate (in bytes)
  Future<int> estimateExportSize() async {
    final result = await exportToJsonString();
    if (result.isSuccess) {
      return utf8.encode(result.data!).length;
    }
    return 0;
  }

  String _formatDate(DateTime date) {
    return '${date.year}${date.month.toString().padLeft(2, '0')}${date.day.toString().padLeft(2, '0')}_'
           '${date.hour.toString().padLeft(2, '0')}${date.minute.toString().padLeft(2, '0')}';
  }
}
```

## Entity toJson Methods (Add to entities)
```dart
// In Todo entity
Map<String, dynamic> toJson() {
  return {
    'id': id,
    'recipientEmail': recipientEmail,
    'recipientFirstName': recipientFirstName,
    'recipientLastName': recipientLastName,
    'subject': subject,
    'initialText': initialText,
    'language': language,
    'intervalDays': intervalDays,
    'sendTimeHour': sendTime.hour,
    'sendTimeMinute': sendTime.minute,
    'isCompleted': isCompleted,
    'isPaused': isPaused,
    'completedAt': completedAt?.toIso8601String(),
    'nextSendDateTime': nextSendDateTime?.toIso8601String(),
    'lastSendDateTime': lastSendDateTime?.toIso8601String(),
    'createdAt': createdAt.toIso8601String(),
  };
}

// In SentEmail entity
Map<String, dynamic> toJson() {
  return {
    'id': id,
    'todoId': todoId,
    'subject': subject,
    'text': text,
    'templateIndexUsed': templateIndexUsed,
    'sentAt': sentAt.toIso8601String(),
  };
}
```

## Acceptance Criteria
- [ ] Exports all TODOs, settings, sent_emails
- [ ] JSON format with pretty printing
- [ ] Includes version and export timestamp
- [ ] Saves to accessible location
- [ ] Returns file path on success
- [ ] Error handling for storage issues
- [ ] Export size estimation

## Dependencies
- Task 026-028 (Repositories)
- Task 007 (pubspec with path_provider)

## Parallel Work
Can run parallel with: Task 085

## Estimated Effort
1.5 hours
