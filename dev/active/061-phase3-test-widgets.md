# Task 061: Test Reusable Widgets

## Phase
3 - UI Foundation & MVP (Testing)

## Description
Write widget tests for all reusable UI components.

## Steps
1. Create `test/presentation/widgets/` directory
2. Create test file for each widget
3. Test rendering and interactions

## Test Files
```
test/presentation/widgets/
  ├── app_button_test.dart
  ├── app_text_field_test.dart
  ├── app_card_test.dart
  ├── app_dialog_test.dart
  └── loading_indicator_test.dart
```

## Test Cases

### AppButton Tests
```dart
void main() {
  group('AppButton', () {
    testWidgets('should render primary button', (tester) async {
      await tester.pumpWidget(MaterialApp(
        home: Scaffold(
          body: AppButton.primary(
            text: 'Click Me',
            onPressed: () {},
          ),
        ),
      ));

      expect(find.text('Click Me'), findsOneWidget);
      expect(find.byType(ElevatedButton), findsOneWidget);
    });

    testWidgets('should show loading indicator when isLoading', (tester) async {
      await tester.pumpWidget(MaterialApp(
        home: Scaffold(
          body: AppButton.primary(
            text: 'Loading',
            isLoading: true,
          ),
        ),
      ));

      expect(find.byType(CircularProgressIndicator), findsOneWidget);
    });

    testWidgets('should be disabled when loading', (tester) async {
      bool pressed = false;
      await tester.pumpWidget(MaterialApp(
        home: Scaffold(
          body: AppButton.primary(
            text: 'Click',
            isLoading: true,
            onPressed: () => pressed = true,
          ),
        ),
      ));

      await tester.tap(find.byType(ElevatedButton));
      expect(pressed, false);
    });

    testWidgets('should render icon when provided', (tester) async {
      await tester.pumpWidget(MaterialApp(
        home: Scaffold(
          body: AppButton.primary(
            text: 'Delete',
            icon: Icons.delete,
            onPressed: () {},
          ),
        ),
      ));

      expect(find.byIcon(Icons.delete), findsOneWidget);
    });
  });
}
```

### AppTextField Tests
```dart
group('AppTextField', () {
  testWidgets('should render with label', (tester) async {
    await tester.pumpWidget(MaterialApp(
      home: Scaffold(
        body: AppTextField(label: 'Email'),
      ),
    ));

    expect(find.text('Email'), findsOneWidget);
  });

  testWidgets('should toggle password visibility', (tester) async {
    await tester.pumpWidget(MaterialApp(
      home: Scaffold(
        body: AppTextField.password(),
      ),
    ));

    // Initially obscured
    final textField = tester.widget<TextField>(find.byType(TextField));
    expect(textField.obscureText, true);

    // Tap visibility icon
    await tester.tap(find.byIcon(Icons.visibility_outlined));
    await tester.pump();

    // Now visible
    final updatedTextField = tester.widget<TextField>(find.byType(TextField));
    expect(updatedTextField.obscureText, false);
  });

  testWidgets('should validate email format', (tester) async {
    final controller = TextEditingController();
    await tester.pumpWidget(MaterialApp(
      home: Scaffold(
        body: Form(
          autovalidateMode: AutovalidateMode.always,
          child: AppTextField.email(controller: controller),
        ),
      ),
    ));

    // Enter invalid email
    await tester.enterText(find.byType(TextFormField), 'invalid');
    await tester.pump();

    expect(find.text('Enter a valid email address'), findsOneWidget);

    // Enter valid email
    await tester.enterText(find.byType(TextFormField), 'test@example.com');
    await tester.pump();

    expect(find.text('Enter a valid email address'), findsNothing);
  });
});
```

### AppDialog Tests
```dart
group('AppDialog', () {
  testWidgets('showConfirmation returns true on confirm', (tester) async {
    bool? result;

    await tester.pumpWidget(MaterialApp(
      home: Builder(
        builder: (context) => ElevatedButton(
          onPressed: () async {
            result = await AppDialog.showConfirmation(
              context: context,
              title: 'Confirm?',
              message: 'Are you sure?',
            );
          },
          child: const Text('Show'),
        ),
      ),
    ));

    await tester.tap(find.text('Show'));
    await tester.pumpAndSettle();

    expect(find.text('Confirm?'), findsOneWidget);
    expect(find.text('Are you sure?'), findsOneWidget);

    await tester.tap(find.text('Confirm'));
    await tester.pumpAndSettle();

    expect(result, true);
  });

  testWidgets('showConfirmation returns false on cancel', (tester) async {
    bool? result;

    await tester.pumpWidget(MaterialApp(
      home: Builder(
        builder: (context) => ElevatedButton(
          onPressed: () async {
            result = await AppDialog.showConfirmation(
              context: context,
              title: 'Confirm?',
              message: 'Are you sure?',
            );
          },
          child: const Text('Show'),
        ),
      ),
    ));

    await tester.tap(find.text('Show'));
    await tester.pumpAndSettle();

    await tester.tap(find.text('Cancel'));
    await tester.pumpAndSettle();

    expect(result, false);
  });
});
```

## Acceptance Criteria
- [ ] AppButton tests (all variants, loading, icons)
- [ ] AppTextField tests (types, validation, visibility toggle)
- [ ] AppCard tests (rendering, tap callbacks)
- [ ] AppDialog tests (confirmation, error, info)
- [ ] LoadingIndicator tests (rendering, skeleton animation)
- [ ] All widget tests pass

## Dependencies
- Task 056-060 (All widget implementations)

## Parallel Work
Can run parallel with: Task 062

## Estimated Effort
2-3 hours
