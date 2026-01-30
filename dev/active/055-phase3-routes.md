# Task 055: Create Routes Constants

## Phase
3 - UI Foundation & MVP

## Description
Define route name constants for type-safe navigation.

## Steps
1. Create `lib/core/navigation/routes.dart`
2. Define all route constants
3. Add documentation

## Code Structure
```dart
/// Route name constants for navigation
class Routes {
  // Prevent instantiation
  Routes._();

  /// Main TODO list screen with tabs
  static const String main = '/';

  /// Create new TODO screen
  static const String createTodo = '/todo/create';

  /// Edit existing TODO screen
  /// Arguments: int todoId
  static const String editTodo = '/todo/edit';

  /// View TODO details
  /// Arguments: int todoId
  static const String todoDetails = '/todo/details';

  /// Settings screen
  static const String settings = '/settings';

  /// Template management screen
  static const String templateManagement = '/settings/templates';

  /// Statistics screen
  static const String statistics = '/statistics';

  /// Welcome/onboarding screen (first launch)
  static const String welcome = '/onboarding/welcome';

  /// SMTP setup wizard
  static const String smtpSetup = '/onboarding/smtp-setup';

  /// About screen
  static const String about = '/about';
}
```

## Navigation Service (Optional Helper)
```dart
import 'package:flutter/material.dart';

class NavigationService {
  static final GlobalKey<NavigatorState> navigatorKey =
      GlobalKey<NavigatorState>();

  static NavigatorState? get navigator => navigatorKey.currentState;

  static Future<T?> navigateTo<T>(String routeName, {Object? arguments}) {
    return navigator!.pushNamed<T>(routeName, arguments: arguments);
  }

  static Future<T?> navigateToAndReplace<T>(String routeName,
      {Object? arguments}) {
    return navigator!.pushReplacementNamed<T, void>(routeName,
        arguments: arguments);
  }

  static Future<T?> navigateToAndClearStack<T>(String routeName,
      {Object? arguments}) {
    return navigator!.pushNamedAndRemoveUntil<T>(
      routeName,
      (route) => false,
      arguments: arguments,
    );
  }

  static void goBack<T>([T? result]) {
    return navigator!.pop<T>(result);
  }

  static bool canGoBack() {
    return navigator!.canPop();
  }
}
```

## Usage Examples
```dart
// Navigate to create TODO
Navigator.pushNamed(context, Routes.createTodo);

// Navigate to edit TODO with ID
Navigator.pushNamed(context, Routes.editTodo, arguments: todoId);

// Navigate and replace (e.g., after onboarding)
Navigator.pushReplacementNamed(context, Routes.main);

// Using NavigationService
NavigationService.navigateTo(Routes.settings);
NavigationService.goBack();
```

## Acceptance Criteria
- [ ] All route constants defined
- [ ] Constants documented with expected arguments
- [ ] NavigationService helper implemented
- [ ] Type-safe navigation possible

## Dependencies
- None

## Parallel Work
Can run parallel with: Task 050-054

## Estimated Effort
20 minutes
