# Task 051: Create App Colors

## Phase
3 - UI Foundation & MVP

## Description
Define the app color palette based on Designs.md specification.

## Steps
1. Create `lib/core/theme/app_colors.dart`
2. Define primary, secondary, surface, and semantic colors
3. Define TODO card gradient colors based on send count

## Code Structure
```dart
import 'package:flutter/material.dart';

class AppColors {
  // Prevent instantiation
  AppColors._();

  // Primary Palette (Blue-Gray)
  static const Color primary = Color(0xFF5C6BC0);      // Indigo 400
  static const Color primaryLight = Color(0xFF8E99A4);
  static const Color primaryDark = Color(0xFF3949AB);

  // Secondary/Accent
  static const Color secondary = Color(0xFF26A69A);    // Teal 400
  static const Color secondaryLight = Color(0xFF64D8CB);
  static const Color secondaryDark = Color(0xFF00766C);

  // Surface Colors
  static const Color surface = Color(0xFFFAFAFA);
  static const Color surfaceVariant = Color(0xFFF5F5F5);
  static const Color background = Color(0xFFFFFFFF);

  // On Colors (Text/Icons on surfaces)
  static const Color onPrimary = Color(0xFFFFFFFF);
  static const Color onSecondary = Color(0xFFFFFFFF);
  static const Color onSurface = Color(0xFF212121);
  static const Color onSurfaceVariant = Color(0xFF757575);
  static const Color onBackground = Color(0xFF212121);

  // Semantic Colors
  static const Color error = Color(0xFFE53935);
  static const Color onError = Color(0xFFFFFFFF);
  static const Color success = Color(0xFF43A047);
  static const Color warning = Color(0xFFFFA726);

  // TODO Card Colors (based on send_count / max_sends ratio)
  static const Color todoNew = Color(0xFF81C784);       // Green - new/few sends
  static const Color todoMedium = Color(0xFFFFD54F);    // Yellow - medium
  static const Color todoHigh = Color(0xFFFF8A65);      // Orange - many sends
  static const Color todoCritical = Color(0xFFE57373);  // Red - near max

  // Paused state
  static const Color todoPaused = Color(0xFFBDBDBD);    // Gray

  // Divider
  static const Color divider = Color(0xFFE0E0E0);

  // Shimmer (loading)
  static const Color shimmerBase = Color(0xFFE0E0E0);
  static const Color shimmerHighlight = Color(0xFFF5F5F5);

  /// Get TODO card color based on send ratio
  /// [sendCount] current number of sends
  /// [maxSends] maximum allowed sends
  static Color getTodoColor(int sendCount, int maxSends) {
    if (maxSends <= 0) return todoNew;

    final ratio = sendCount / maxSends;

    if (ratio <= 0.25) return todoNew;
    if (ratio <= 0.5) return todoMedium;
    if (ratio <= 0.75) return todoHigh;
    return todoCritical;
  }

  /// Get lighter version of TODO color for gradient
  static Color getTodoColorLight(int sendCount, int maxSends) {
    final baseColor = getTodoColor(sendCount, maxSends);
    return Color.lerp(baseColor, Colors.white, 0.3)!;
  }
}
```

## Acceptance Criteria
- [ ] All colors from Designs.md defined
- [ ] TODO gradient colors based on send ratio
- [ ] Paused state color (gray)
- [ ] getTodoColor helper function works
- [ ] Colors accessible (WCAG AA contrast)

## Dependencies
- None

## Parallel Work
Can run parallel with: Task 050, 052, 053

## Estimated Effort
30 minutes
