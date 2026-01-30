# Task 059: Create AppDialog Widget

## Phase
3 - UI Foundation & MVP

## Description
Create reusable dialog widgets for confirmation, error, and info.

## Steps
1. Create `lib/presentation/widgets/app_dialog.dart`
2. Implement confirmation dialog
3. Implement error dialog with retry
4. Implement info dialog
5. Add static show methods

## Code Structure
```dart
import 'package:flutter/material.dart';
import '../../core/theme/app_colors.dart';
import '../../core/theme/app_dimensions.dart';
import 'app_button.dart';

class AppDialog extends StatelessWidget {
  final String title;
  final String? message;
  final Widget? content;
  final List<Widget> actions;
  final IconData? icon;
  final Color? iconColor;

  const AppDialog({
    super.key,
    required this.title,
    this.message,
    this.content,
    required this.actions,
    this.icon,
    this.iconColor,
  });

  @override
  Widget build(BuildContext context) {
    return AlertDialog(
      title: Row(
        children: [
          if (icon != null) ...[
            Icon(icon, color: iconColor ?? AppColors.primary, size: 28),
            const SizedBox(width: AppDimensions.spacingSm),
          ],
          Expanded(child: Text(title)),
        ],
      ),
      content: content ?? (message != null ? Text(message!) : null),
      actions: actions,
      actionsAlignment: MainAxisAlignment.end,
      actionsPadding: const EdgeInsets.all(AppDimensions.spacingMd),
    );
  }

  /// Show confirmation dialog
  static Future<bool> showConfirmation({
    required BuildContext context,
    required String title,
    required String message,
    String confirmText = 'Confirm',
    String cancelText = 'Cancel',
    bool isDangerous = false,
  }) async {
    final result = await showDialog<bool>(
      context: context,
      builder: (context) => AppDialog(
        title: title,
        message: message,
        icon: isDangerous ? Icons.warning_amber_rounded : Icons.help_outline,
        iconColor: isDangerous ? AppColors.warning : null,
        actions: [
          AppButton.text(
            text: cancelText,
            onPressed: () => Navigator.of(context).pop(false),
          ),
          isDangerous
              ? AppButton.danger(
                  text: confirmText,
                  onPressed: () => Navigator.of(context).pop(true),
                )
              : AppButton.primary(
                  text: confirmText,
                  onPressed: () => Navigator.of(context).pop(true),
                ),
        ],
      ),
    );
    return result ?? false;
  }

  /// Show error dialog with optional retry
  static Future<bool> showError({
    required BuildContext context,
    required String title,
    required String message,
    VoidCallback? onRetry,
    String dismissText = 'OK',
    String retryText = 'Retry',
  }) async {
    final result = await showDialog<bool>(
      context: context,
      builder: (context) => AppDialog(
        title: title,
        message: message,
        icon: Icons.error_outline,
        iconColor: AppColors.error,
        actions: [
          AppButton.text(
            text: dismissText,
            onPressed: () => Navigator.of(context).pop(false),
          ),
          if (onRetry != null)
            AppButton.primary(
              text: retryText,
              onPressed: () {
                Navigator.of(context).pop(true);
                onRetry();
              },
            ),
        ],
      ),
    );
    return result ?? false;
  }

  /// Show info dialog
  static Future<void> showInfo({
    required BuildContext context,
    required String title,
    required String message,
    String dismissText = 'OK',
  }) async {
    await showDialog<void>(
      context: context,
      builder: (context) => AppDialog(
        title: title,
        message: message,
        icon: Icons.info_outline,
        actions: [
          AppButton.primary(
            text: dismissText,
            onPressed: () => Navigator.of(context).pop(),
          ),
        ],
      ),
    );
  }

  /// Show success dialog
  static Future<void> showSuccess({
    required BuildContext context,
    required String title,
    required String message,
    String dismissText = 'OK',
  }) async {
    await showDialog<void>(
      context: context,
      builder: (context) => AppDialog(
        title: title,
        message: message,
        icon: Icons.check_circle_outline,
        iconColor: AppColors.success,
        actions: [
          AppButton.primary(
            text: dismissText,
            onPressed: () => Navigator.of(context).pop(),
          ),
        ],
      ),
    );
  }

  /// Show custom content dialog
  static Future<T?> showCustom<T>({
    required BuildContext context,
    required String title,
    required Widget content,
    required List<Widget> actions,
    IconData? icon,
    Color? iconColor,
    bool barrierDismissible = true,
  }) {
    return showDialog<T>(
      context: context,
      barrierDismissible: barrierDismissible,
      builder: (context) => AppDialog(
        title: title,
        content: content,
        actions: actions,
        icon: icon,
        iconColor: iconColor,
      ),
    );
  }
}
```

## Usage Examples
```dart
// Confirmation
final confirmed = await AppDialog.showConfirmation(
  context: context,
  title: 'Complete TODO?',
  message: 'This will mark the TODO as completed.',
);

// Dangerous confirmation
final delete = await AppDialog.showConfirmation(
  context: context,
  title: 'Delete TODO?',
  message: 'This action cannot be undone.',
  confirmText: 'Delete',
  isDangerous: true,
);

// Error with retry
await AppDialog.showError(
  context: context,
  title: 'Send Failed',
  message: 'Could not send email. Check your connection.',
  onRetry: () => _sendEmail(),
);

// Info
await AppDialog.showInfo(
  context: context,
  title: 'Email Sent',
  message: 'Your email was sent successfully.',
);
```

## Acceptance Criteria
- [ ] Confirmation dialog with cancel/confirm
- [ ] Dangerous confirmation (red button)
- [ ] Error dialog with optional retry
- [ ] Info dialog
- [ ] Success dialog
- [ ] Custom content dialog
- [ ] Consistent styling and icons

## Dependencies
- Task 051 (AppColors)
- Task 053 (AppDimensions)
- Task 056 (AppButton)

## Parallel Work
Can run parallel with: Task 056, 057, 058

## Estimated Effort
1 hour
