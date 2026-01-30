# Task 098: Write Integration Tests

## Phase
6 - Polish & Testing

## Description
Write integration tests for complete user flows.

## Steps
1. Create `integration_test/` directory
2. Write tests for main flows
3. Test on emulator/device

## Test Files
```
integration_test/
  ├── todo_flow_test.dart
  ├── settings_flow_test.dart
  ├── export_import_test.dart
  └── app_test.dart
```

## Code Structure

### app_test.dart (Test Setup)
```dart
import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:integration_test/integration_test.dart';
import 'package:letmedomywork/main.dart' as app;

void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  group('App Integration Tests', () {
    testWidgets('Full TODO lifecycle', (tester) async {
      app.main();
      await tester.pumpAndSettle();

      // Skip onboarding if shown
      final skipButton = find.text('Set up later');
      if (skipButton.evaluate().isNotEmpty) {
        await tester.tap(skipButton);
        await tester.pumpAndSettle();
        await tester.tap(find.text('Skip Anyway'));
        await tester.pumpAndSettle();
      }

      // Verify main screen
      expect(find.text('LetMeDoMyWork'), findsOneWidget);
      expect(find.text('Active'), findsOneWidget);

      // Create TODO
      await tester.tap(find.byType(FloatingActionButton));
      await tester.pumpAndSettle();

      // Fill form
      await tester.enterText(
        find.byType(TextFormField).first,
        'test@example.com',
      );
      await tester.pumpAndSettle();

      // Verify names auto-populated
      // ... more assertions

      // Save
      await tester.tap(find.text('Create TODO'));
      await tester.pumpAndSettle();

      // Verify TODO in list
      expect(find.text('test@example.com'), findsOneWidget);
    });
  });
}
```

### todo_flow_test.dart
```dart
void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  group('TODO Flow', () {
    testWidgets('Create TODO flow', (tester) async {
      app.main();
      await tester.pumpAndSettle();
      await _skipOnboarding(tester);

      // Tap FAB
      await tester.tap(find.byType(FloatingActionButton));
      await tester.pumpAndSettle();

      // Verify create screen
      expect(find.text('New TODO'), findsOneWidget);

      // Enter email
      final emailField = find.byType(TextFormField).first;
      await tester.enterText(emailField, 'john.doe@example.com');
      await tester.pumpAndSettle();

      // Verify auto-populated names
      expect(find.text('John'), findsOneWidget);
      expect(find.text('Doe'), findsOneWidget);

      // Tap save
      await tester.tap(find.text('Create TODO'));
      await tester.pumpAndSettle();

      // Verify back on main screen with TODO
      expect(find.text('LetMeDoMyWork'), findsOneWidget);
      expect(find.textContaining('john.doe@example.com'), findsOneWidget);
    });

    testWidgets('Complete TODO via swipe', (tester) async {
      app.main();
      await tester.pumpAndSettle();
      await _skipOnboarding(tester);
      await _createTestTodo(tester);

      // Find TODO card
      final todoCard = find.byType(TodoCard).first;

      // Swipe right
      await tester.drag(todoCard, const Offset(300, 0));
      await tester.pumpAndSettle();

      // Confirm dialog
      await tester.tap(find.text('Complete'));
      await tester.pumpAndSettle();

      // Verify snackbar
      expect(find.text('TODO completed'), findsOneWidget);

      // Verify undo available
      expect(find.text('Undo'), findsOneWidget);

      // Switch to Completed tab
      await tester.tap(find.text('Completed'));
      await tester.pumpAndSettle();

      // Verify TODO in completed
      expect(find.byType(TodoCard), findsOneWidget);
    });

    testWidgets('Pause and Resume TODO', (tester) async {
      app.main();
      await tester.pumpAndSettle();
      await _skipOnboarding(tester);
      await _createTestTodo(tester);

      // Find TODO card
      final todoCard = find.byType(TodoCard).first;

      // Swipe left to pause
      await tester.drag(todoCard, const Offset(-300, 0));
      await tester.pumpAndSettle();

      // Verify paused indicator
      expect(find.byIcon(Icons.pause_circle_filled), findsOneWidget);

      // Swipe left again to resume
      await tester.drag(find.byType(TodoCard).first, const Offset(-300, 0));
      await tester.pumpAndSettle();

      // Verify not paused
      expect(find.byIcon(Icons.pause_circle_filled), findsNothing);
    });
  });
}

Future<void> _skipOnboarding(WidgetTester tester) async {
  final skipButton = find.text('Set up later');
  if (skipButton.evaluate().isNotEmpty) {
    await tester.tap(skipButton);
    await tester.pumpAndSettle();
    await tester.tap(find.text('Skip Anyway'));
    await tester.pumpAndSettle();
  }
}

Future<void> _createTestTodo(WidgetTester tester) async {
  await tester.tap(find.byType(FloatingActionButton));
  await tester.pumpAndSettle();

  await tester.enterText(
    find.byType(TextFormField).first,
    'test@example.com',
  );
  await tester.pumpAndSettle();

  await tester.tap(find.text('Create TODO'));
  await tester.pumpAndSettle();
}
```

### settings_flow_test.dart
```dart
void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  group('Settings Flow', () {
    testWidgets('Change max follow-ups', (tester) async {
      app.main();
      await tester.pumpAndSettle();
      await _skipOnboarding(tester);

      // Navigate to settings
      await tester.tap(find.byIcon(Icons.settings));
      await tester.pumpAndSettle();

      // Tap max follow-ups
      await tester.tap(find.text('Max Follow-ups'));
      await tester.pumpAndSettle();

      // Verify dialog
      expect(find.text('Maximum emails to send per TODO'), findsOneWidget);

      // Change value (tap + multiple times)
      await tester.tap(find.byIcon(Icons.add));
      await tester.tap(find.byIcon(Icons.add));
      await tester.pumpAndSettle();

      // Save
      await tester.tap(find.text('Save'));
      await tester.pumpAndSettle();

      // Verify updated
      expect(find.text('12 emails per TODO'), findsOneWidget);
    });
  });
}
```

### export_import_test.dart
```dart
void main() {
  IntegrationTestWidgetsFlutterBinding.ensureInitialized();

  group('Export/Import Flow', () {
    testWidgets('Export and import round-trip', (tester) async {
      app.main();
      await tester.pumpAndSettle();
      await _skipOnboarding(tester);

      // Create some TODOs
      await _createTestTodo(tester, 'todo1@example.com');
      await _createTestTodo(tester, 'todo2@example.com');

      // Go to settings
      await tester.tap(find.byIcon(Icons.settings));
      await tester.pumpAndSettle();

      // Tap export
      await tester.tap(find.text('Export Data'));
      await tester.pumpAndSettle();

      // Tap save to device
      await tester.tap(find.text('Save to Device'));
      await tester.pumpAndSettle();

      // Verify success
      expect(find.text('Export successful!'), findsOneWidget);

      // Close dialog
      await tester.tap(find.text('Done'));
      await tester.pumpAndSettle();

      // Note: Full import test would require file system access
      // which is limited in integration tests
    });
  });
}
```

## Running Tests
```bash
# Run all integration tests
flutter test integration_test/

# Run specific test file
flutter test integration_test/todo_flow_test.dart

# Run on connected device
flutter test integration_test/ -d <device_id>
```

## Acceptance Criteria
- [ ] TODO creation flow tested
- [ ] TODO completion flow tested
- [ ] Pause/Resume flow tested
- [ ] Edit TODO flow tested
- [ ] Settings changes tested
- [ ] Navigation between screens tested
- [ ] All tests pass on emulator

## Dependencies
- All Phase 3 tasks
- All UI components

## Parallel Work
Must run after: Task 079 (Phase 3 complete)

## Estimated Effort
4-5 hours
