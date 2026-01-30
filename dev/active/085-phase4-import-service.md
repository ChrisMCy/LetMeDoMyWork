# Task 085: Create Import Service

## Phase
4 - Advanced Features

## Description
Implement service for importing app data from JSON.

## Steps
1. Create `lib/services/backup/import_service.dart`
2. Parse and validate JSON
3. Replace database data
4. Handle version compatibility

## Code Structure
```dart
import 'dart:convert';
import 'dart:io';
import 'package:file_picker/file_picker.dart';
import '../../domain/entities/todo.dart';
import '../../domain/entities/settings.dart';
import '../../domain/entities/sent_email.dart';
import '../../domain/repositories/todo_repository.dart';
import '../../domain/repositories/settings_repository.dart';
import '../../services/database/database_helper.dart';

class ImportValidationResult {
  final bool isValid;
  final String? error;
  final int todoCount;
  final int sentEmailCount;
  final DateTime? exportedAt;
  final String? appVersion;

  ImportValidationResult({
    required this.isValid,
    this.error,
    this.todoCount = 0,
    this.sentEmailCount = 0,
    this.exportedAt,
    this.appVersion,
  });
}

class ImportService {
  final TodoRepository _todoRepository;
  final SettingsRepository _settingsRepository;
  final DatabaseHelper _databaseHelper;

  ImportService(
    this._todoRepository,
    this._settingsRepository,
    this._databaseHelper,
  );

  /// Pick and validate import file
  Future<Result<(String, ImportValidationResult)>> pickAndValidateFile() async {
    try {
      final result = await FilePicker.platform.pickFiles(
        type: FileType.custom,
        allowedExtensions: ['json'],
      );

      if (result == null || result.files.isEmpty) {
        return Result.failure('No file selected');
      }

      final file = File(result.files.single.path!);
      final content = await file.readAsString();

      final validation = await validateImportData(content);

      if (!validation.isValid) {
        return Result.failure(validation.error!);
      }

      return Result.success((content, validation));
    } catch (e) {
      return Result.failure('Failed to read file: $e');
    }
  }

  /// Validate JSON content
  Future<ImportValidationResult> validateImportData(String jsonString) async {
    try {
      final data = json.decode(jsonString) as Map<String, dynamic>;

      // Check required fields
      if (!data.containsKey('todos') ||
          !data.containsKey('settings') ||
          !data.containsKey('sentEmails')) {
        return ImportValidationResult(
          isValid: false,
          error: 'Invalid backup format: missing required fields',
        );
      }

      final todos = data['todos'] as List;
      final sentEmails = data['sentEmails'] as List;
      final version = data['version'] as String?;
      final exportedAtStr = data['exportedAt'] as String?;

      DateTime? exportedAt;
      if (exportedAtStr != null) {
        exportedAt = DateTime.tryParse(exportedAtStr);
      }

      // Validate version compatibility
      if (version != null && !_isVersionCompatible(version)) {
        return ImportValidationResult(
          isValid: false,
          error: 'Backup version $version is not compatible with this app version',
        );
      }

      return ImportValidationResult(
        isValid: true,
        todoCount: todos.length,
        sentEmailCount: sentEmails.length,
        exportedAt: exportedAt,
        appVersion: version,
      );
    } catch (e) {
      return ImportValidationResult(
        isValid: false,
        error: 'Invalid JSON format: $e',
      );
    }
  }

  /// Import data (replaces existing data!)
  Future<Result<void>> importData(String jsonString) async {
    try {
      final data = json.decode(jsonString) as Map<String, dynamic>;

      // Start transaction
      await _databaseHelper.clearAllData();

      // Import settings
      final settingsData = data['settings'] as Map<String, dynamic>;
      final settings = Settings.fromJson(settingsData);
      await _settingsRepository.updateSettings(settings);

      // Import TODOs
      final todosData = data['todos'] as List;
      for (final todoJson in todosData) {
        final todo = Todo.fromJson(todoJson as Map<String, dynamic>);
        await _todoRepository.createTodo(todo);
      }

      // Import sent emails
      final sentEmailsData = data['sentEmails'] as List;
      for (final emailJson in sentEmailsData) {
        final email = SentEmail.fromJson(emailJson as Map<String, dynamic>);
        await _todoRepository.saveSentEmail(email);
      }

      return Result.success(null);
    } catch (e) {
      return Result.failure('Import failed: $e');
    }
  }

  bool _isVersionCompatible(String version) {
    // For now, accept all 1.x versions
    return version.startsWith('1.');
  }
}
```

## Entity fromJson Methods (Add to entities)
```dart
// In Todo entity
factory Todo.fromJson(Map<String, dynamic> json) {
  return Todo(
    id: json['id'] as int?,
    recipientEmail: json['recipientEmail'] as String,
    recipientFirstName: json['recipientFirstName'] as String?,
    recipientLastName: json['recipientLastName'] as String?,
    subject: json['subject'] as String,
    initialText: json['initialText'] as String?,
    language: json['language'] as String,
    intervalDays: json['intervalDays'] as int,
    sendTime: TimeOfDay(
      hour: json['sendTimeHour'] as int,
      minute: json['sendTimeMinute'] as int,
    ),
    isCompleted: json['isCompleted'] as bool? ?? false,
    isPaused: json['isPaused'] as bool? ?? false,
    completedAt: json['completedAt'] != null
        ? DateTime.parse(json['completedAt'] as String)
        : null,
    nextSendDateTime: json['nextSendDateTime'] != null
        ? DateTime.parse(json['nextSendDateTime'] as String)
        : null,
    lastSendDateTime: json['lastSendDateTime'] != null
        ? DateTime.parse(json['lastSendDateTime'] as String)
        : null,
    createdAt: DateTime.parse(json['createdAt'] as String),
  );
}
```

## Database Helper Addition
```dart
// In DatabaseHelper
Future<void> clearAllData() async {
  final db = await database;
  await db.delete('sent_emails');
  await db.delete('todos');
  // Keep settings structure, just update values
}
```

## Acceptance Criteria
- [ ] File picker for JSON files
- [ ] Validates backup format
- [ ] Checks version compatibility
- [ ] Shows preview (count of todos, emails, export date)
- [ ] Replaces all existing data
- [ ] Handles malformed JSON gracefully
- [ ] Transaction-like behavior (all or nothing)

## Dependencies
- Task 026-028 (Repositories)
- Task 007 (pubspec with file_picker)
- Task 014 (DatabaseHelper)

## Parallel Work
Can run parallel with: Task 084

## Estimated Effort
2 hours
