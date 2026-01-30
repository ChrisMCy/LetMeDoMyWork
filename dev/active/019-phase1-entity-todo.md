# Task 019: Create Todo Entity

## Phase
1 - Core Infrastructure

## Description
Create the Todo domain entity representing an email reminder campaign.

## Steps
1. Create `lib/domain/entities/todo.dart`
2. Define all properties
3. Implement Equatable for comparison
4. Add copyWith method

## Code Structure
```dart
import 'package:equatable/equatable.dart';

class Todo extends Equatable {
  final int? id;
  final String subject;
  final String recipientEmail;
  final String? recipientFirstName;
  final String? recipientLastName;
  final String initialText;
  final String language; // 'de' or 'en'
  final DateTime startDate;
  final String sendTime; // "HH:MM"
  final int intervalDays;
  final DateTime nextSendDateTime;
  final List<int> selectedSubjectIndices;
  final List<int> selectedTextIndices;
  final bool alreadySentFirst;
  final bool isPaused;
  final bool isCompleted;
  final bool pendingSend;
  final DateTime createdAt;
  final DateTime? completedAt;

  const Todo({
    this.id,
    required this.subject,
    required this.recipientEmail,
    // ... all properties
  });

  Todo copyWith({ ... });

  @override
  List<Object?> get props => [ ... ];
}
```

## Acceptance Criteria
- [ ] Todo entity created
- [ ] All properties from BusinessLogik.md included
- [ ] Equatable implemented correctly
- [ ] copyWith method works
- [ ] Nullable fields handled correctly

## Dependencies
- Task 007 (Configure pubspec - equatable package)

## Parallel Work
Can run parallel with: Task 020, 021

## Estimated Effort
30 minutes
