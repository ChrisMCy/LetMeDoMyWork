# Task 054: Create App Router

## Phase
3 - UI Foundation & MVP

## Description
Implement navigation structure with named routes.

## Steps
1. Create `lib/core/navigation/app_router.dart`
2. Define all route names
3. Implement route generation
4. Add navigation helper methods

## Code Structure
```dart
import 'package:flutter/material.dart';
import '../../presentation/screens/main/main_screen.dart';
import '../../presentation/screens/todo/create_todo_screen.dart';
import '../../presentation/screens/todo/edit_todo_screen.dart';
import '../../presentation/screens/settings/settings_screen.dart';
import '../../presentation/screens/statistics/statistics_screen.dart';
import '../../presentation/screens/onboarding/welcome_screen.dart';
import '../../presentation/screens/onboarding/smtp_setup_wizard.dart';
import 'routes.dart';

class AppRouter {
  static Route<dynamic> generateRoute(RouteSettings settings) {
    switch (settings.name) {
      case Routes.main:
        return _slideRoute(const MainScreen());

      case Routes.createTodo:
        return _slideRoute(const CreateTodoScreen());

      case Routes.editTodo:
        final todoId = settings.arguments as int;
        return _slideRoute(EditTodoScreen(todoId: todoId));

      case Routes.settings:
        return _slideRoute(const SettingsScreen());

      case Routes.statistics:
        return _slideRoute(const StatisticsScreen());

      case Routes.welcome:
        return _fadeRoute(const WelcomeScreen());

      case Routes.smtpSetup:
        return _slideRoute(const SmtpSetupWizard());

      case Routes.templateManagement:
        return _slideRoute(const TemplateManagementScreen());

      default:
        return _slideRoute(
          Scaffold(
            body: Center(
              child: Text('Route not found: ${settings.name}'),
            ),
          ),
        );
    }
  }

  /// Slide transition from right
  static PageRouteBuilder _slideRoute(Widget page) {
    return PageRouteBuilder(
      pageBuilder: (context, animation, secondaryAnimation) => page,
      transitionsBuilder: (context, animation, secondaryAnimation, child) {
        const begin = Offset(1.0, 0.0);
        const end = Offset.zero;
        const curve = Curves.easeInOut;

        var tween = Tween(begin: begin, end: end).chain(
          CurveTween(curve: curve),
        );

        return SlideTransition(
          position: animation.drive(tween),
          child: child,
        );
      },
      transitionDuration: const Duration(milliseconds: 300),
    );
  }

  /// Fade transition
  static PageRouteBuilder _fadeRoute(Widget page) {
    return PageRouteBuilder(
      pageBuilder: (context, animation, secondaryAnimation) => page,
      transitionsBuilder: (context, animation, secondaryAnimation, child) {
        return FadeTransition(
          opacity: animation,
          child: child,
        );
      },
      transitionDuration: const Duration(milliseconds: 300),
    );
  }
}
```

## Acceptance Criteria
- [ ] All routes defined
- [ ] Route generation works
- [ ] Slide transition for most screens
- [ ] Fade transition for welcome screen
- [ ] Arguments passed correctly (e.g., todoId for edit)
- [ ] Unknown route handled gracefully

## Dependencies
- Task 055 (Routes constants)

## Parallel Work
Can run parallel with: Task 050-053

## Estimated Effort
1 hour
