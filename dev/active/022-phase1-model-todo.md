# Task 022: Create TodoModel

## Phase
1 - Core Infrastructure

## Description
Create TodoModel data class with serialization methods for database operations.

## Steps
1. Create `lib/data/models/todo_model.dart`
2. Extend Todo entity
3. Implement fromMap() factory
4. Implement toMap() method
5. Handle JSON arrays for indices

## Code Structure
```dart
import '../../domain/entities/todo.dart';

class TodoModel extends Todo {
  const TodoModel({
    super.id,
    required super.subject,
    required super.recipientEmail,
    // ... all properties
  });

  factory TodoModel.fromMap(Map<String, dynamic> map) {
    return TodoModel(
      id: map['id'] as int?,
      subject: map['subject'] as String,
      recipientEmail: map['recipient_email'] as String,
      recipientFirstName: map['recipient_first_name'] as String?,
      // ... parse all fields
      selectedSubjectIndices: (jsonDecode(map['selected_subject_indices']) as List)
          .map((e) => e as int).toList(),
      // ... handle JSON fields
      createdAt: DateTime.fromMillisecondsSinceEpoch(map['created_at'] as int),
    );
  }

  Map<String, dynamic> toMap() {
    return {
      'id': id,
      'subject': subject,
      'recipient_email': recipientEmail,
      // ... all fields
      'selected_subject_indices': jsonEncode(selectedSubjectIndices),
      'created_at': createdAt.millisecondsSinceEpoch,
    };
  }

  factory TodoModel.fromEntity(Todo entity) { ... }
}
```

## Acceptance Criteria
- [ ] TodoModel extends Todo
- [ ] fromMap correctly parses all fields
- [ ] toMap correctly serializes all fields
- [ ] JSON arrays handled correctly
- [ ] DateTime converted to/from milliseconds
- [ ] Boolean converted to/from int (0/1)

## Dependencies
- Task 019 (Todo Entity)

## Parallel Work
Can run parallel with: Task 023, 024

## Estimated Effort
1 hour
