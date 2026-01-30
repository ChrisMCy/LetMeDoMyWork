# Task 023: Create SettingsModel

## Phase
1 - Core Infrastructure

## Description
Create SettingsModel data class with serialization methods.

## Steps
1. Create `lib/data/models/settings_model.dart`
2. Extend Settings entity
3. Implement fromMap() factory
4. Implement toMap() method
5. Handle JSON arrays for templates

## Code Structure
```dart
import 'dart:convert';
import '../../domain/entities/settings.dart';

class SettingsModel extends Settings {
  const SettingsModel({
    super.id = 1,
    super.maxFollowUps = 10,
    // ... all properties
  });

  factory SettingsModel.fromMap(Map<String, dynamic> map) {
    return SettingsModel(
      id: map['id'] as int,
      maxFollowUps: map['max_follow_ups'] as int,
      randomizeMinutes: map['randomize_minutes'] as int,
      smtpProvider: map['smtp_provider'] as String?,
      // ... parse all fields
      subjectsDe: (jsonDecode(map['subjects_de']) as List)
          .map((e) => e as String).toList(),
      selectedSubjectsDe: (jsonDecode(map['selected_subjects_de']) as List)
          .map((e) => e as int).toList(),
      // ... handle JSON fields
    );
  }

  Map<String, dynamic> toMap() {
    return {
      'id': id,
      'max_follow_ups': maxFollowUps,
      // ... all fields
      'subjects_de': jsonEncode(subjectsDe),
      'selected_subjects_de': jsonEncode(selectedSubjectsDe),
    };
  }
}
```

## Acceptance Criteria
- [ ] SettingsModel extends Settings
- [ ] fromMap handles all fields including JSON arrays
- [ ] toMap serializes all fields correctly
- [ ] Template lists (30 items each) handled
- [ ] Selected indices lists handled

## Dependencies
- Task 020 (Settings Entity)

## Parallel Work
Can run parallel with: Task 022, 024

## Estimated Effort
1 hour
