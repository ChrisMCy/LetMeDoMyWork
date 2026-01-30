# Task 020: Create Settings Entity

## Phase
1 - Core Infrastructure

## Description
Create the Settings domain entity for app configuration.

## Steps
1. Create `lib/domain/entities/settings.dart`
2. Define all properties
3. Implement Equatable

## Code Structure
```dart
import 'package:equatable/equatable.dart';

class Settings extends Equatable {
  final int id; // Always 1
  final int maxFollowUps;
  final int randomizeMinutes;
  final String? smtpProvider; // 'gmail', 'outlook', 'custom'
  final String? smtpHost;
  final int? smtpPort;
  final String? smtpUsername;
  final bool smtpUseTls;
  final List<String> subjectsDe;
  final List<String> subjectsEn;
  final List<String> textsDe;
  final List<String> textsEn;
  final List<int> selectedSubjectsDe;
  final List<int> selectedSubjectsEn;
  final List<int> selectedTextsDe;
  final List<int> selectedTextsEn;
  final DateTime lastOpened;
  final DateTime createdAt;
  final DateTime updatedAt;

  const Settings({
    this.id = 1,
    this.maxFollowUps = 10,
    this.randomizeMinutes = 30,
    // ... all properties
  });

  Settings copyWith({ ... });

  @override
  List<Object?> get props => [ ... ];
}
```

## Acceptance Criteria
- [ ] Settings entity created
- [ ] All properties from DatabaseSchema.md included
- [ ] Default values set correctly
- [ ] Equatable implemented
- [ ] Template lists handled as List<String>

## Dependencies
- Task 007 (Configure pubspec - equatable package)

## Parallel Work
Can run parallel with: Task 019, 021

## Estimated Effort
30 minutes
