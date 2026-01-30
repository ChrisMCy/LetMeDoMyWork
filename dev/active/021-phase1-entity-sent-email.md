# Task 021: Create SentEmail Entity

## Phase
1 - Core Infrastructure

## Description
Create the SentEmail domain entity for tracking sent emails.

## Steps
1. Create `lib/domain/entities/sent_email.dart`
2. Define all properties
3. Implement Equatable

## Code Structure
```dart
import 'package:equatable/equatable.dart';

class SentEmail extends Equatable {
  final int? id;
  final int todoId;
  final String subject;
  final String body;
  final DateTime sentAt;
  final int sendNumber;
  final int templateIndex;

  const SentEmail({
    this.id,
    required this.todoId,
    required this.subject,
    required this.body,
    required this.sentAt,
    required this.sendNumber,
    required this.templateIndex,
  });

  SentEmail copyWith({ ... });

  @override
  List<Object?> get props => [
    id, todoId, subject, body, sentAt, sendNumber, templateIndex
  ];
}
```

## Acceptance Criteria
- [ ] SentEmail entity created
- [ ] All properties from DatabaseSchema.md included
- [ ] Equatable implemented
- [ ] copyWith method works

## Dependencies
- Task 007 (Configure pubspec - equatable package)

## Parallel Work
Can run parallel with: Task 019, 020

## Estimated Effort
20 minutes
