# Task 027: Implement TodoRepository

## Phase
1 - Core Infrastructure

## Description
Implement the TodoRepository interface with SQLite database operations.

## Steps
1. Create `lib/data/repositories/todo_repository_impl.dart`
2. Implement all CRUD operations
3. Use DatabaseHelper for database access
4. Handle data model conversions

## Code Structure
```dart
import '../../domain/entities/todo.dart';
import '../../domain/entities/sent_email.dart';
import '../../domain/repositories/todo_repository.dart';
import '../../services/database/database_helper.dart';
import '../models/todo_model.dart';
import '../models/sent_email_model.dart';

class TodoRepositoryImpl implements TodoRepository {
  final DatabaseHelper _databaseHelper;

  TodoRepositoryImpl(this._databaseHelper);

  @override
  Future<int> createTodo(Todo todo) async {
    final db = await _databaseHelper.database;
    final model = TodoModel.fromEntity(todo);
    return await db.insert('todos', model.toMap());
  }

  @override
  Future<List<Todo>> getActiveTodos() async {
    final db = await _databaseHelper.database;
    final result = await db.query(
      'todos',
      where: 'is_completed = ?',
      whereArgs: [0],
      orderBy: 'is_paused ASC, created_at ASC',
    );
    return result.map((map) => TodoModel.fromMap(map)).toList();
  }

  @override
  Future<void> completeTodo(int id) async {
    final db = await _databaseHelper.database;
    await db.update(
      'todos',
      {
        'is_completed': 1,
        'completed_at': DateTime.now().millisecondsSinceEpoch,
      },
      where: 'id = ?',
      whereArgs: [id],
    );
  }

  // ... implement all other methods
}
```

## Acceptance Criteria
- [ ] Implements TodoRepository interface
- [ ] All CRUD operations work
- [ ] Sorting correct for active/completed
- [ ] Send count query optimized
- [ ] Cascade delete works (via FK in schema)
- [ ] No SQL injection vulnerabilities

## Dependencies
- Task 014 (DatabaseHelper)
- Task 022 (TodoModel)
- Task 024 (SentEmailModel)
- Task 026 (Repository Interfaces)

## Parallel Work
Can run parallel with: Task 028 (SettingsRepository)

## Estimated Effort
2-3 hours
