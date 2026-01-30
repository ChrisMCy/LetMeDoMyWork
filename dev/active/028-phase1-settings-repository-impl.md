# Task 028: Implement SettingsRepository

## Phase
1 - Core Infrastructure

## Description
Implement the SettingsRepository interface with SQLite database operations.

## Steps
1. Create `lib/data/repositories/settings_repository_impl.dart`
2. Implement all settings operations
3. Handle singleton pattern (always id = 1)
4. Use default templates for initialization

## Code Structure
```dart
import '../../domain/entities/settings.dart';
import '../../domain/repositories/settings_repository.dart';
import '../../services/database/database_helper.dart';
import '../../services/database/default_templates.dart';
import '../models/settings_model.dart';

class SettingsRepositoryImpl implements SettingsRepository {
  final DatabaseHelper _databaseHelper;

  SettingsRepositoryImpl(this._databaseHelper);

  @override
  Future<Settings> getSettings() async {
    final db = await _databaseHelper.database;
    final result = await db.query('settings', where: 'id = 1');
    if (result.isEmpty) {
      throw Exception('Settings not initialized');
    }
    return SettingsModel.fromMap(result.first);
  }

  @override
  Future<void> updateSettings(Settings settings) async {
    final db = await _databaseHelper.database;
    final model = SettingsModel.fromEntity(settings);
    await db.update(
      'settings',
      model.toMap(),
      where: 'id = 1',
    );
  }

  @override
  Future<bool> hasSettings() async {
    final db = await _databaseHelper.database;
    final result = await db.rawQuery('SELECT COUNT(*) as count FROM settings');
    return (result.first['count'] as int) > 0;
  }

  @override
  Future<void> initializeSettings(Settings settings) async {
    final db = await _databaseHelper.database;
    final model = SettingsModel(
      subjectsDe: DefaultTemplates.subjectsDe,
      subjectsEn: DefaultTemplates.subjectsEn,
      textsDe: DefaultTemplates.textsDe,
      textsEn: DefaultTemplates.textsEn,
      // ... other defaults
    );
    await db.insert('settings', model.toMap());
  }

  @override
  Future<void> updateLastOpened(DateTime timestamp) async {
    final db = await _databaseHelper.database;
    await db.update(
      'settings',
      {'last_opened': timestamp.millisecondsSinceEpoch},
      where: 'id = 1',
    );
  }
}
```

## Acceptance Criteria
- [ ] Implements SettingsRepository interface
- [ ] getSettings returns settings (or throws if not init)
- [ ] hasSettings checks existence
- [ ] initializeSettings uses default templates
- [ ] updateLastOpened works
- [ ] Singleton pattern enforced (always id=1)

## Dependencies
- Task 014 (DatabaseHelper)
- Task 017 (Default Templates)
- Task 023 (SettingsModel)
- Task 026 (Repository Interfaces)

## Parallel Work
Can run parallel with: Task 027 (TodoRepository)

## Estimated Effort
1-2 hours
