# Task 031: Test Dependency Injection

## Phase
1 - Core Infrastructure (Testing)

## Description
Write tests for dependency injection setup.

## Steps
1. Create `test/core/di/injection_test.dart`
2. Test that all dependencies resolve correctly
3. Test singleton behavior

## Test Cases
```dart
void main() {
  group('Dependency Injection', () {
    setUp(() async {
      // Reset GetIt before each test
      await getIt.reset();
    });

    test('setupDependencyInjection should register all dependencies', () async {
      await setupDependencyInjection();

      expect(getIt.isRegistered<DatabaseHelper>(), true);
      expect(getIt.isRegistered<TodoRepository>(), true);
      expect(getIt.isRegistered<SettingsRepository>(), true);
    });

    test('DatabaseHelper should be singleton', () async {
      await setupDependencyInjection();

      final instance1 = getIt<DatabaseHelper>();
      final instance2 = getIt<DatabaseHelper>();

      expect(identical(instance1, instance2), true);
    });

    test('should resolve TodoRepository correctly', () async {
      await setupDependencyInjection();

      final repo = getIt<TodoRepository>();
      expect(repo, isA<TodoRepositoryImpl>());
    });
  });
}
```

## Acceptance Criteria
- [ ] All dependencies register correctly
- [ ] Singleton behavior verified
- [ ] Repository types correct
- [ ] No circular dependencies
- [ ] Tests pass

## Dependencies
- Task 030 (Dependency Injection Setup)

## Parallel Work
Can run parallel with: None

## Estimated Effort
30 minutes
