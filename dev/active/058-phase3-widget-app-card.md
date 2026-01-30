# Task 058: Create AppCard Widget

## Phase
3 - UI Foundation & MVP

## Description
Create reusable card widget with optional swipe support.

## Steps
1. Create `lib/presentation/widgets/app_card.dart`
2. Implement base card styling
3. Add tap and long press support
4. Prepare for swipe integration

## Code Structure
```dart
import 'package:flutter/material.dart';
import '../../core/theme/app_colors.dart';
import '../../core/theme/app_dimensions.dart';

class AppCard extends StatelessWidget {
  final Widget child;
  final VoidCallback? onTap;
  final VoidCallback? onLongPress;
  final EdgeInsetsGeometry? padding;
  final EdgeInsetsGeometry? margin;
  final Color? backgroundColor;
  final Color? borderColor;
  final double? elevation;
  final double? borderRadius;
  final bool showBorder;

  const AppCard({
    super.key,
    required this.child,
    this.onTap,
    this.onLongPress,
    this.padding,
    this.margin,
    this.backgroundColor,
    this.borderColor,
    this.elevation,
    this.borderRadius,
    this.showBorder = false,
  });

  @override
  Widget build(BuildContext context) {
    Widget card = Card(
      elevation: elevation ?? AppDimensions.cardElevation,
      margin: margin ?? const EdgeInsets.symmetric(
        horizontal: AppDimensions.spacingMd,
        vertical: AppDimensions.spacingSm,
      ),
      shape: RoundedRectangleBorder(
        borderRadius: BorderRadius.circular(
          borderRadius ?? AppDimensions.radiusLg,
        ),
        side: showBorder
            ? BorderSide(
                color: borderColor ?? AppColors.divider,
                width: 1,
              )
            : BorderSide.none,
      ),
      color: backgroundColor ?? AppColors.surface,
      child: Padding(
        padding: padding ?? const EdgeInsets.all(AppDimensions.paddingCard),
        child: child,
      ),
    );

    if (onTap != null || onLongPress != null) {
      return InkWell(
        onTap: onTap,
        onLongPress: onLongPress,
        borderRadius: BorderRadius.circular(
          borderRadius ?? AppDimensions.radiusLg,
        ),
        child: card,
      );
    }

    return card;
  }
}

/// Card with gradient background (for TODO cards)
class GradientCard extends StatelessWidget {
  final Widget child;
  final VoidCallback? onTap;
  final VoidCallback? onLongPress;
  final Color startColor;
  final Color endColor;
  final EdgeInsetsGeometry? padding;
  final EdgeInsetsGeometry? margin;

  const GradientCard({
    super.key,
    required this.child,
    required this.startColor,
    required this.endColor,
    this.onTap,
    this.onLongPress,
    this.padding,
    this.margin,
  });

  @override
  Widget build(BuildContext context) {
    return Container(
      margin: margin ?? const EdgeInsets.symmetric(
        horizontal: AppDimensions.spacingMd,
        vertical: AppDimensions.spacingSm,
      ),
      decoration: BoxDecoration(
        gradient: LinearGradient(
          begin: Alignment.topLeft,
          end: Alignment.bottomRight,
          colors: [startColor, endColor],
        ),
        borderRadius: BorderRadius.circular(AppDimensions.radiusLg),
        boxShadow: [
          BoxShadow(
            color: startColor.withOpacity(0.3),
            blurRadius: 8,
            offset: const Offset(0, 4),
          ),
        ],
      ),
      child: Material(
        color: Colors.transparent,
        child: InkWell(
          onTap: onTap,
          onLongPress: onLongPress,
          borderRadius: BorderRadius.circular(AppDimensions.radiusLg),
          child: Padding(
            padding: padding ?? const EdgeInsets.all(AppDimensions.paddingCard),
            child: child,
          ),
        ),
      ),
    );
  }
}

/// Card showing error state
class ErrorCard extends StatelessWidget {
  final Widget child;
  final String? errorMessage;
  final VoidCallback? onRetry;

  const ErrorCard({
    super.key,
    required this.child,
    this.errorMessage,
    this.onRetry,
  });

  @override
  Widget build(BuildContext context) {
    return AppCard(
      borderColor: AppColors.error,
      showBorder: true,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          child,
          if (errorMessage != null) ...[
            const SizedBox(height: AppDimensions.spacingSm),
            Row(
              children: [
                Icon(Icons.error_outline, color: AppColors.error, size: 16),
                const SizedBox(width: 4),
                Expanded(
                  child: Text(
                    errorMessage!,
                    style: TextStyle(
                      color: AppColors.error,
                      fontSize: 12,
                    ),
                  ),
                ),
                if (onRetry != null)
                  TextButton(
                    onPressed: onRetry,
                    child: const Text('Retry'),
                  ),
              ],
            ),
          ],
        ],
      ),
    );
  }
}
```

## Usage Examples
```dart
AppCard(
  onTap: () => _openDetails(),
  child: Text('Card content'),
)

GradientCard(
  startColor: AppColors.getTodoColor(sendCount, maxSends),
  endColor: AppColors.getTodoColorLight(sendCount, maxSends),
  child: TodoCardContent(...),
)

ErrorCard(
  errorMessage: 'Failed to send email',
  onRetry: () => _retrySend(),
  child: TodoCardContent(...),
)
```

## Acceptance Criteria
- [ ] Basic card with consistent styling
- [ ] Tap and long press callbacks
- [ ] Gradient card variant for TODOs
- [ ] Error card variant with retry
- [ ] Customizable padding, margin, colors
- [ ] Proper border radius

## Dependencies
- Task 051 (AppColors)
- Task 053 (AppDimensions)

## Parallel Work
Can run parallel with: Task 056, 057, 059

## Estimated Effort
1 hour
