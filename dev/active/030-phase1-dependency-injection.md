# Task 030: Setup Dependency Injection

## Phase
1 - Core Infrastructure

## Description
Configure GetIt service locator for dependency injection.

## Steps
1. Create `lib/core/di/injection.dart`
2. Register DatabaseHelper as singleton
3. Register repositories as lazy singletons
4. Create initialization function

## Code Structure
```dart
import 'package:get_it/get_it.dart';
import '../../data/repositories/todo_repository_impl.dart';
import '../../data/repositories/settings_repository_impl.dart';
import '../../domain/repositories/todo_repository.dart';
import '../../domain/repositories/settings_repository.dart';
import '../../services/database/database_helper.dart';

final getIt = GetIt.instance;

Future<void> setupDependencyInjection() async {
  // Database
  getIt.registerSingleton<DatabaseHelper>(DatabaseHelper());

  // Wait for database to be ready
  await getIt<DatabaseHelper>().database;

  // Repositories
  getIt.registerLazySingleton<TodoRepository>(
    () => TodoRepositoryImpl(getIt<DatabaseHelper>()),
  );

  getIt.registerLazySingleton<SettingsRepository>(
    () => SettingsRepositoryImpl(getIt<DatabaseHelper>()),
  );

  // Services (to be added later)
  // getIt.registerLazySingleton<EmailService>(...);
  // getIt.registerLazySingleton<NotificationService>(...);
}

// For testing
Future<void> setupTestDependencyInjection() async {
  // Use mock implementations
}
```

## Usage in main.dart
```dart
void main() async {
  WidgetsFlutterBinding.ensureInitialized();
  await setupDependencyInjection();
  runApp(const MyApp());
}
```

## Acceptance Criteria
- [ ] GetIt configured correctly
- [ ] DatabaseHelper registered as singleton
- [ ] Repositories registered as lazy singletons
- [ ] Initialization function async (waits for DB)
- [ ] Can resolve dependencies via getIt<Type>()
- [ ] Test helper for mock injection

## Dependencies
- Task 014 (DatabaseHelper)
- Task 027 (TodoRepository Implementation)
- Task 028 (SettingsRepository Implementation)

## Parallel Work
Can run parallel with: Task 029 (Test Repositories)

## Estimated Effort
1 hour
