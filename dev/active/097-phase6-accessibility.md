# Task 097: Implement Accessibility Features

## Phase
6 - Polish & Testing

## Description
Ensure the app meets accessibility standards.

## Steps
1. Add semantic labels
2. Ensure touch targets >= 48dp
3. Check color contrast
4. Support screen readers

## Code Implementation

### Semantic Labels
```dart
// Add to TODO Card
Semantics(
  label: 'TODO: ${todo.subject}. '
      'Recipient: ${todo.recipientEmail}. '
      'Sent ${sendCount} times. '
      '${todo.isPaused ? "Paused" : "Active"}.',
  child: TodoCard(...),
)

// Add to buttons
Semantics(
  button: true,
  label: 'Send email now',
  child: IconButton(
    icon: const Icon(Icons.send),
    onPressed: _sendEmail,
  ),
)

// Add to swipe actions
Dismissible(
  key: ...,
  child: Semantics(
    label: 'Swipe right to complete, swipe left to ${todo.isPaused ? "resume" : "pause"}',
    child: ...,
  ),
)
```

### Touch Target Wrapper
```dart
class AccessibleTouchTarget extends StatelessWidget {
  final Widget child;
  final VoidCallback? onTap;
  final String? semanticLabel;
  final double minSize;

  const AccessibleTouchTarget({
    super.key,
    required this.child,
    this.onTap,
    this.semanticLabel,
    this.minSize = 48.0,
  });

  @override
  Widget build(BuildContext context) {
    return Semantics(
      label: semanticLabel,
      button: onTap != null,
      child: InkWell(
        onTap: onTap,
        child: ConstrainedBox(
          constraints: BoxConstraints(
            minWidth: minSize,
            minHeight: minSize,
          ),
          child: Center(child: child),
        ),
      ),
    );
  }
}
```

### Color Contrast Check
```dart
// Utility to check contrast ratio
class ContrastChecker {
  /// Check if two colors have sufficient contrast
  /// WCAG AA requires 4.5:1 for normal text, 3:1 for large text
  static bool hasGoodContrast(Color foreground, Color background) {
    final ratio = _contrastRatio(foreground, background);
    return ratio >= 4.5;
  }

  static double _contrastRatio(Color fg, Color bg) {
    final l1 = _relativeLuminance(fg);
    final l2 = _relativeLuminance(bg);
    final lighter = l1 > l2 ? l1 : l2;
    final darker = l1 > l2 ? l2 : l1;
    return (lighter + 0.05) / (darker + 0.05);
  }

  static double _relativeLuminance(Color color) {
    double r = color.red / 255;
    double g = color.green / 255;
    double b = color.blue / 255;

    r = r <= 0.03928 ? r / 12.92 : pow((r + 0.055) / 1.055, 2.4).toDouble();
    g = g <= 0.03928 ? g / 12.92 : pow((g + 0.055) / 1.055, 2.4).toDouble();
    b = b <= 0.03928 ? b / 12.92 : pow((b + 0.055) / 1.055, 2.4).toDouble();

    return 0.2126 * r + 0.7152 * g + 0.0722 * b;
  }
}
```

### Focus Management
```dart
// Ensure focus is visible
class FocusableWidget extends StatelessWidget {
  final Widget child;
  final VoidCallback? onTap;

  const FocusableWidget({
    super.key,
    required this.child,
    this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return Focus(
      child: Builder(
        builder: (context) {
          final hasFocus = Focus.of(context).hasFocus;
          return Container(
            decoration: hasFocus
                ? BoxDecoration(
                    border: Border.all(
                      color: AppColors.primary,
                      width: 2,
                    ),
                    borderRadius: BorderRadius.circular(8),
                  )
                : null,
            child: InkWell(
              onTap: onTap,
              child: child,
            ),
          );
        },
      ),
    );
  }
}
```

### Accessibility Testing Checklist
```dart
// Run these tests
void runAccessibilityTests(WidgetTester tester) {
  // Check semantic labels
  testWidgets('has semantic labels', (tester) async {
    await tester.pumpWidget(MyApp());

    // Verify key elements have labels
    expect(
      find.bySemanticsLabel(RegExp('TODO:')),
      findsWidgets,
    );
  });

  // Check touch targets
  testWidgets('touch targets are at least 48x48', (tester) async {
    await tester.pumpWidget(MyApp());

    final buttons = find.byType(IconButton);
    for (final button in buttons.evaluate()) {
      final size = tester.getSize(find.byWidget(button.widget));
      expect(size.width, greaterThanOrEqualTo(48));
      expect(size.height, greaterThanOrEqualTo(48));
    }
  });
}
```

## Acceptance Criteria
- [ ] All interactive elements have semantic labels
- [ ] Touch targets >= 48dp
- [ ] Color contrast meets WCAG AA (4.5:1)
- [ ] Screen reader can navigate app
- [ ] Focus indicators visible
- [ ] No information conveyed by color alone
- [ ] Text scales with system font size

## Testing
Use TalkBack (Android) to test:
1. Can navigate to all elements
2. All elements announced correctly
3. Actions can be performed
4. State changes announced

## Dependencies
- All UI tasks

## Parallel Work
Can run parallel with: Task 094-096

## Estimated Effort
2-3 hours
