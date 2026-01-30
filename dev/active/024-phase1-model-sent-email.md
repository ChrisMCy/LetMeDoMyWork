# Task 024: Create SentEmailModel

## Phase
1 - Core Infrastructure

## Description
Create SentEmailModel data class with serialization methods.

## Steps
1. Create `lib/data/models/sent_email_model.dart`
2. Extend SentEmail entity
3. Implement fromMap() factory
4. Implement toMap() method

## Code Structure
```dart
import '../../domain/entities/sent_email.dart';

class SentEmailModel extends SentEmail {
  const SentEmailModel({
    super.id,
    required super.todoId,
    required super.subject,
    required super.body,
    required super.sentAt,
    required super.sendNumber,
    required super.templateIndex,
  });

  factory SentEmailModel.fromMap(Map<String, dynamic> map) {
    return SentEmailModel(
      id: map['id'] as int?,
      todoId: map['todo_id'] as int,
      subject: map['subject'] as String,
      body: map['body'] as String,
      sentAt: DateTime.fromMillisecondsSinceEpoch(map['sent_at'] as int),
      sendNumber: map['send_number'] as int,
      templateIndex: map['template_index'] as int,
    );
  }

  Map<String, dynamic> toMap() {
    return {
      if (id != null) 'id': id,
      'todo_id': todoId,
      'subject': subject,
      'body': body,
      'sent_at': sentAt.millisecondsSinceEpoch,
      'send_number': sendNumber,
      'template_index': templateIndex,
    };
  }

  factory SentEmailModel.fromEntity(SentEmail entity) {
    return SentEmailModel(
      id: entity.id,
      todoId: entity.todoId,
      subject: entity.subject,
      body: entity.body,
      sentAt: entity.sentAt,
      sendNumber: entity.sendNumber,
      templateIndex: entity.templateIndex,
    );
  }
}
```

## Acceptance Criteria
- [ ] SentEmailModel extends SentEmail
- [ ] fromMap correctly parses all fields
- [ ] toMap correctly serializes all fields
- [ ] DateTime handled correctly
- [ ] Optional id excluded from toMap when null

## Dependencies
- Task 021 (SentEmail Entity)

## Parallel Work
Can run parallel with: Task 022, 023

## Estimated Effort
30 minutes
