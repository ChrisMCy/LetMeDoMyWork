# Task 056: Create AppButton Widget

## Phase
3 - UI Foundation & MVP

## Description
Create reusable button widget with primary, secondary, and text variants.

## Steps
1. Create `lib/presentation/widgets/app_button.dart`
2. Implement button variants
3. Add loading state support
4. Add icon support

## Code Structure
```dart
import 'package:flutter/material.dart';
import '../../core/theme/app_colors.dart';
import '../../core/theme/app_dimensions.dart';

enum AppButtonVariant { primary, secondary, text, danger }
enum AppButtonSize { small, medium, large }

class AppButton extends StatelessWidget {
  final String text;
  final VoidCallback? onPressed;
  final AppButtonVariant variant;
  final AppButtonSize size;
  final bool isLoading;
  final bool isFullWidth;
  final IconData? icon;
  final IconData? trailingIcon;

  const AppButton({
    super.key,
    required this.text,
    this.onPressed,
    this.variant = AppButtonVariant.primary,
    this.size = AppButtonSize.medium,
    this.isLoading = false,
    this.isFullWidth = false,
    this.icon,
    this.trailingIcon,
  });

  // Named constructors for convenience
  const AppButton.primary({
    super.key,
    required this.text,
    this.onPressed,
    this.size = AppButtonSize.medium,
    this.isLoading = false,
    this.isFullWidth = false,
    this.icon,
    this.trailingIcon,
  }) : variant = AppButtonVariant.primary;

  const AppButton.secondary({
    super.key,
    required this.text,
    this.onPressed,
    this.size = AppButtonSize.medium,
    this.isLoading = false,
    this.isFullWidth = false,
    this.icon,
    this.trailingIcon,
  }) : variant = AppButtonVariant.secondary;

  const AppButton.text({
    super.key,
    required this.text,
    this.onPressed,
    this.size = AppButtonSize.medium,
    this.isLoading = false,
    this.isFullWidth = false,
    this.icon,
    this.trailingIcon,
  }) : variant = AppButtonVariant.text;

  const AppButton.danger({
    super.key,
    required this.text,
    this.onPressed,
    this.size = AppButtonSize.medium,
    this.isLoading = false,
    this.isFullWidth = false,
    this.icon,
    this.trailingIcon,
  }) : variant = AppButtonVariant.danger;

  @override
  Widget build(BuildContext context) {
    final height = _getHeight();
    final padding = _getPadding();

    Widget child = Row(
      mainAxisSize: isFullWidth ? MainAxisSize.max : MainAxisSize.min,
      mainAxisAlignment: MainAxisAlignment.center,
      children: [
        if (isLoading)
          Padding(
            padding: const EdgeInsets.only(right: 8),
            child: SizedBox(
              width: 16,
              height: 16,
              child: CircularProgressIndicator(
                strokeWidth: 2,
                valueColor: AlwaysStoppedAnimation(_getLoadingColor()),
              ),
            ),
          )
        else if (icon != null)
          Padding(
            padding: const EdgeInsets.only(right: 8),
            child: Icon(icon, size: 20),
          ),
        Text(text),
        if (trailingIcon != null && !isLoading)
          Padding(
            padding: const EdgeInsets.only(left: 8),
            child: Icon(trailingIcon, size: 20),
          ),
      ],
    );

    switch (variant) {
      case AppButtonVariant.primary:
        return SizedBox(
          width: isFullWidth ? double.infinity : null,
          height: height,
          child: ElevatedButton(
            onPressed: isLoading ? null : onPressed,
            style: ElevatedButton.styleFrom(
              padding: padding,
              backgroundColor: AppColors.primary,
              foregroundColor: AppColors.onPrimary,
            ),
            child: child,
          ),
        );

      case AppButtonVariant.secondary:
        return SizedBox(
          width: isFullWidth ? double.infinity : null,
          height: height,
          child: OutlinedButton(
            onPressed: isLoading ? null : onPressed,
            style: OutlinedButton.styleFrom(
              padding: padding,
              side: BorderSide(color: AppColors.primary),
            ),
            child: child,
          ),
        );

      case AppButtonVariant.text:
        return SizedBox(
          height: height,
          child: TextButton(
            onPressed: isLoading ? null : onPressed,
            style: TextButton.styleFrom(padding: padding),
            child: child,
          ),
        );

      case AppButtonVariant.danger:
        return SizedBox(
          width: isFullWidth ? double.infinity : null,
          height: height,
          child: ElevatedButton(
            onPressed: isLoading ? null : onPressed,
            style: ElevatedButton.styleFrom(
              padding: padding,
              backgroundColor: AppColors.error,
              foregroundColor: AppColors.onError,
            ),
            child: child,
          ),
        );
    }
  }

  double _getHeight() {
    switch (size) {
      case AppButtonSize.small:
        return AppDimensions.buttonHeightSm;
      case AppButtonSize.medium:
        return AppDimensions.buttonHeightMd;
      case AppButtonSize.large:
        return AppDimensions.buttonHeightLg;
    }
  }

  EdgeInsets _getPadding() {
    switch (size) {
      case AppButtonSize.small:
        return const EdgeInsets.symmetric(horizontal: 12, vertical: 6);
      case AppButtonSize.medium:
        return const EdgeInsets.symmetric(horizontal: 20, vertical: 10);
      case AppButtonSize.large:
        return const EdgeInsets.symmetric(horizontal: 28, vertical: 14);
    }
  }

  Color _getLoadingColor() {
    switch (variant) {
      case AppButtonVariant.primary:
      case AppButtonVariant.danger:
        return AppColors.onPrimary;
      case AppButtonVariant.secondary:
      case AppButtonVariant.text:
        return AppColors.primary;
    }
  }
}
```

## Usage Examples
```dart
AppButton.primary(
  text: 'Save',
  onPressed: () => _save(),
  isLoading: _isSaving,
)

AppButton.secondary(
  text: 'Cancel',
  onPressed: () => Navigator.pop(context),
)

AppButton.danger(
  text: 'Delete',
  icon: Icons.delete,
  onPressed: () => _confirmDelete(),
)
```

## Acceptance Criteria
- [ ] Primary, secondary, text, danger variants
- [ ] Small, medium, large sizes
- [ ] Loading state with spinner
- [ ] Icon support (leading and trailing)
- [ ] Full width option
- [ ] Disabled state when loading

## Dependencies
- Task 051 (AppColors)
- Task 053 (AppDimensions)

## Parallel Work
Can run parallel with: Task 057, 058, 059

## Estimated Effort
1 hour
