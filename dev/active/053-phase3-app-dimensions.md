# Task 053: Create App Dimensions

## Phase
3 - UI Foundation & MVP

## Description
Define consistent spacing, sizing, and dimension constants.

## Steps
1. Create `lib/core/theme/app_dimensions.dart`
2. Define spacing scale
3. Define component sizes
4. Define animation durations

## Code Structure
```dart
class AppDimensions {
  // Prevent instantiation
  AppDimensions._();

  // Spacing Scale (based on 4dp grid)
  static const double spacingXxs = 2.0;
  static const double spacingXs = 4.0;
  static const double spacingSm = 8.0;
  static const double spacingMd = 16.0;
  static const double spacingLg = 24.0;
  static const double spacingXl = 32.0;
  static const double spacingXxl = 48.0;

  // Padding
  static const double paddingScreen = 16.0;
  static const double paddingCard = 12.0;
  static const double paddingButton = 12.0;
  static const double paddingInput = 16.0;

  // Border Radius
  static const double radiusSm = 4.0;
  static const double radiusMd = 8.0;
  static const double radiusLg = 12.0;
  static const double radiusXl = 16.0;
  static const double radiusRound = 999.0;

  // Icon Sizes
  static const double iconSm = 16.0;
  static const double iconMd = 24.0;
  static const double iconLg = 32.0;
  static const double iconXl = 48.0;

  // Button Heights
  static const double buttonHeightSm = 32.0;
  static const double buttonHeightMd = 44.0;
  static const double buttonHeightLg = 56.0;

  // Input Heights
  static const double inputHeight = 48.0;
  static const double inputHeightMultiline = 120.0;

  // Card Dimensions
  static const double cardElevation = 2.0;
  static const double cardMinHeight = 80.0;

  // FAB
  static const double fabSize = 56.0;
  static const double fabMini = 40.0;

  // AppBar
  static const double appBarHeight = 56.0;

  // Bottom Navigation
  static const double bottomNavHeight = 80.0;

  // Tab Bar
  static const double tabBarHeight = 48.0;

  // Touch Targets (Accessibility)
  static const double touchTargetMin = 48.0;

  // Swipe Thresholds
  static const double swipeThreshold = 0.3;  // 30% of width
  static const double swipeDismissThreshold = 0.5;  // 50% of width

  // Animation Durations (ms)
  static const int animationFast = 150;
  static const int animationNormal = 300;
  static const int animationSlow = 500;

  // Snackbar Duration (ms)
  static const int snackbarDuration = 4000;
  static const int snackbarDurationShort = 2000;
  static const int snackbarDurationLong = 6000;

  // Max Widths (for tablets/responsive)
  static const double maxContentWidth = 600.0;
  static const double maxDialogWidth = 400.0;

  // Badge
  static const double badgeSize = 24.0;
  static const double badgeFontSize = 12.0;
}
```

## Acceptance Criteria
- [ ] Spacing scale follows 4dp grid
- [ ] All component sizes defined
- [ ] Touch targets >= 48dp for accessibility
- [ ] Animation durations consistent
- [ ] Swipe thresholds defined

## Dependencies
- None

## Parallel Work
Can run parallel with: Task 050, 051, 052

## Estimated Effort
20 minutes
