# Task 077: Implement First Launch Detection

## Phase
3 - UI Foundation & MVP

## Description
Implement logic to detect first app launch and route appropriately.

## Steps
1. Create first launch check in main.dart
2. Check if settings exist in database
3. Route to Welcome or Main screen accordingly

## Code Structure

### main.dart update
```dart
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import 'core/di/injection.dart';
import 'core/navigation/app_router.dart';
import 'core/navigation/routes.dart';
import 'core/theme/app_theme.dart';
import 'domain/repositories/settings_repository.dart';
import 'presentation/bloc/todo/todo_bloc.dart';

void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  // Initialize dependencies
  await setupDependencyInjection();

  // Check first launch
  final isFirstLaunch = await _checkFirstLaunch();

  runApp(LetMeDoMyWorkApp(isFirstLaunch: isFirstLaunch));
}

Future<bool> _checkFirstLaunch() async {
  final settingsRepo = getIt<SettingsRepository>();

  try {
    final settings = await settingsRepo.getSettings();
    // If SMTP email is not configured, consider it first launch
    return settings.smtpEmail == null || settings.smtpEmail!.isEmpty;
  } catch (e) {
    // If settings don't exist, it's first launch
    return true;
  }
}

class LetMeDoMyWorkApp extends StatelessWidget {
  final bool isFirstLaunch;

  const LetMeDoMyWorkApp({
    super.key,
    required this.isFirstLaunch,
  });

  @override
  Widget build(BuildContext context) {
    return MultiBlocProvider(
      providers: [
        BlocProvider(
          create: (context) => getIt<TodoBloc>(),
        ),
        // Add other BLoCs as needed
      ],
      child: MaterialApp(
        title: 'LetMeDoMyWork',
        theme: AppTheme.lightTheme,
        debugShowCheckedModeBanner: false,

        // Set initial route based on first launch
        initialRoute: isFirstLaunch ? Routes.welcome : Routes.main,

        onGenerateRoute: AppRouter.generateRoute,
      ),
    );
  }
}
```

### Alternative: SplashScreen approach
```dart
class SplashScreen extends StatefulWidget {
  const SplashScreen({super.key});

  @override
  State<SplashScreen> createState() => _SplashScreenState();
}

class _SplashScreenState extends State<SplashScreen> {
  @override
  void initState() {
    super.initState();
    _checkAndNavigate();
  }

  Future<void> _checkAndNavigate() async {
    // Add a small delay for splash effect
    await Future.delayed(const Duration(seconds: 1));

    final settingsRepo = getIt<SettingsRepository>();
    final settings = await settingsRepo.getSettings();

    final route = (settings.smtpEmail == null || settings.smtpEmail!.isEmpty)
        ? Routes.welcome
        : Routes.main;

    if (mounted) {
      Navigator.pushReplacementNamed(context, route);
    }
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.primary,
      body: Center(
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(
              Icons.email_outlined,
              size: 80,
              color: Colors.white,
            ),
            const SizedBox(height: 16),
            Text(
              'LetMeDoMyWork',
              style: TextStyle(
                color: Colors.white,
                fontSize: 24,
                fontWeight: FontWeight.bold,
              ),
            ),
          ],
        ),
      ),
    );
  }
}
```

### FirstLaunchService (Optional)
```dart
import 'package:shared_preferences/shared_preferences.dart';

class FirstLaunchService {
  static const String _firstLaunchKey = 'first_launch_completed';

  Future<bool> isFirstLaunch() async {
    final prefs = await SharedPreferences.getInstance();
    return prefs.getBool(_firstLaunchKey) ?? true;
  }

  Future<void> markFirstLaunchComplete() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.setBool(_firstLaunchKey, true);
  }

  Future<void> resetFirstLaunch() async {
    final prefs = await SharedPreferences.getInstance();
    await prefs.remove(_firstLaunchKey);
  }
}
```

## Acceptance Criteria
- [ ] First launch detected correctly (no SMTP configured)
- [ ] Welcome screen shown on first launch
- [ ] Main screen shown on subsequent launches
- [ ] Splash screen displays app branding briefly
- [ ] No flicker between screens
- [ ] Works after app reinstall

## Dependencies
- Task 028 (SettingsRepository)
- Task 030 (DI setup)
- Task 054-055 (Navigation)

## Parallel Work
Must run after: Task 074, 075

## Estimated Effort
1 hour
