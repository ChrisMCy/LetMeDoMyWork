# Task 102: Create Splash Screen

## Phase
7 - Release Preparation

## Description
Implement native splash screen for app launch.

## Steps
1. Configure native splash
2. Add branding
3. Handle transition to app

## Implementation

### Native Splash (Android 12+)
```xml
<!-- android/app/src/main/res/values/styles.xml -->
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <style name="LaunchTheme" parent="@android:style/Theme.Light.NoTitleBar">
        <item name="android:windowSplashScreenBackground">@color/splash_background</item>
        <item name="android:windowSplashScreenAnimatedIcon">@drawable/ic_launcher_foreground</item>
        <item name="android:windowSplashScreenAnimationDuration">500</item>
    </style>

    <style name="NormalTheme" parent="@android:style/Theme.Light.NoTitleBar">
        <item name="android:windowBackground">?android:colorBackground</item>
    </style>
</resources>

<!-- values/colors.xml -->
<resources>
    <color name="splash_background">#5C6BC0</color>
</resources>
```

### Legacy Splash (Pre-Android 12)
```xml
<!-- android/app/src/main/res/drawable/launch_background.xml -->
<?xml version="1.0" encoding="utf-8"?>
<layer-list xmlns:android="http://schemas.android.com/apk/res/android">
    <item android:drawable="@color/splash_background"/>
    <item>
        <bitmap
            android:gravity="center"
            android:src="@mipmap/ic_launcher" />
    </item>
</layer-list>

<!-- styles.xml for legacy -->
<style name="LaunchTheme" parent="@android:style/Theme.Light.NoTitleBar">
    <item name="android:windowBackground">@drawable/launch_background</item>
</style>
```

### Flutter Side
```dart
// In main.dart - preserve splash while initializing
void main() async {
  WidgetsFlutterBinding.ensureInitialized();

  // Keep splash screen while loading
  // (Native splash handles this automatically)

  // Initialize services
  await setupDependencyInjection();
  await NotificationService().initialize();
  await BackgroundService().initialize();

  // Check first launch
  final isFirstLaunch = await _checkFirstLaunch();

  runApp(LetMeDoMyWorkApp(isFirstLaunch: isFirstLaunch));
}
```

### Optional: Custom Flutter Splash (for more control)
```dart
class SplashScreen extends StatefulWidget {
  const SplashScreen({super.key});

  @override
  State<SplashScreen> createState() => _SplashScreenState();
}

class _SplashScreenState extends State<SplashScreen>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<double> _scaleAnimation;
  late Animation<double> _fadeAnimation;

  @override
  void initState() {
    super.initState();

    _controller = AnimationController(
      duration: const Duration(milliseconds: 800),
      vsync: this,
    );

    _scaleAnimation = Tween<double>(begin: 0.8, end: 1.0).animate(
      CurvedAnimation(parent: _controller, curve: Curves.easeOut),
    );

    _fadeAnimation = Tween<double>(begin: 0.0, end: 1.0).animate(
      CurvedAnimation(parent: _controller, curve: Curves.easeIn),
    );

    _controller.forward();
    _initializeAndNavigate();
  }

  Future<void> _initializeAndNavigate() async {
    await Future.delayed(const Duration(milliseconds: 1500));

    final isFirstLaunch = await _checkFirstLaunch();

    if (mounted) {
      Navigator.pushReplacementNamed(
        context,
        isFirstLaunch ? Routes.welcome : Routes.main,
      );
    }
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      backgroundColor: AppColors.primary,
      body: Center(
        child: FadeTransition(
          opacity: _fadeAnimation,
          child: ScaleTransition(
            scale: _scaleAnimation,
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                Container(
                  width: 100,
                  height: 100,
                  decoration: BoxDecoration(
                    color: Colors.white,
                    borderRadius: BorderRadius.circular(20),
                  ),
                  child: Icon(
                    Icons.email_outlined,
                    size: 50,
                    color: AppColors.primary,
                  ),
                ),
                const SizedBox(height: 24),
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
        ),
      ),
    );
  }
}
```

## Acceptance Criteria
- [ ] Native splash shows immediately on launch
- [ ] App icon/logo displayed
- [ ] Brand color background
- [ ] Smooth transition to app content
- [ ] No white flash between splash and app
- [ ] Works on Android 8.0 to 14

## Dependencies
- Task 101 (App Icon)

## Parallel Work
Can run parallel with: Task 101, 103

## Estimated Effort
1-2 hours
