# Task 096: Implement Error States

## Phase
6 - Polish & Testing

## Description
Add proper error handling and display throughout the app.

## Steps
1. Network error handling
2. SMTP error display
3. Database error handling
4. Validation error display

## Code Implementation

### Global Error Handler
```dart
// lib/core/errors/error_handler.dart
class ErrorHandler {
  static String getReadableMessage(dynamic error) {
    if (error is SocketException) {
      return 'No internet connection. Please check your network.';
    }
    if (error is TimeoutException) {
      return 'Connection timed out. Please try again.';
    }
    if (error is FormatException) {
      return 'Invalid data format received.';
    }
    if (error is DatabaseException) {
      return 'Database error. Please restart the app.';
    }

    // SMTP specific errors
    final errorStr = error.toString().toLowerCase();
    if (errorStr.contains('authentication') ||
        errorStr.contains('535') ||
        errorStr.contains('invalid credentials')) {
      return 'Email authentication failed. Please check your credentials in Settings.';
    }
    if (errorStr.contains('connection refused')) {
      return 'Could not connect to email server. Check your internet connection.';
    }
    if (errorStr.contains('certificate')) {
      return 'SSL certificate error. Please contact support.';
    }

    return 'An unexpected error occurred. Please try again.';
  }

  static void showError(BuildContext context, dynamic error) {
    final message = getReadableMessage(error);

    ScaffoldMessenger.of(context).showSnackBar(
      SnackBar(
        content: Row(
          children: [
            const Icon(Icons.error_outline, color: Colors.white),
            const SizedBox(width: 8),
            Expanded(child: Text(message)),
          ],
        ),
        backgroundColor: AppColors.error,
        behavior: SnackBarBehavior.floating,
        action: SnackBarAction(
          label: 'Details',
          textColor: Colors.white,
          onPressed: () => _showErrorDetails(context, error),
        ),
      ),
    );
  }

  static void _showErrorDetails(BuildContext context, dynamic error) {
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Error Details'),
        content: SingleChildScrollView(
          child: Text(
            error.toString(),
            style: const TextStyle(fontFamily: 'monospace', fontSize: 12),
          ),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('Close'),
          ),
        ],
      ),
    );
  }
}
```

### Error Boundary Widget
```dart
// lib/presentation/widgets/error_boundary.dart
class ErrorBoundary extends StatefulWidget {
  final Widget child;
  final Widget Function(Object error)? errorBuilder;

  const ErrorBoundary({
    super.key,
    required this.child,
    this.errorBuilder,
  });

  @override
  State<ErrorBoundary> createState() => _ErrorBoundaryState();
}

class _ErrorBoundaryState extends State<ErrorBoundary> {
  Object? _error;

  @override
  void initState() {
    super.initState();
    FlutterError.onError = (details) {
      setState(() => _error = details.exception);
    };
  }

  @override
  Widget build(BuildContext context) {
    if (_error != null) {
      return widget.errorBuilder?.call(_error!) ??
          _DefaultErrorWidget(
            error: _error!,
            onRetry: () => setState(() => _error = null),
          );
    }
    return widget.child;
  }
}

class _DefaultErrorWidget extends StatelessWidget {
  final Object error;
  final VoidCallback onRetry;

  const _DefaultErrorWidget({
    required this.error,
    required this.onRetry,
  });

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(32),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              Icon(
                Icons.bug_report,
                size: 80,
                color: AppColors.error,
              ),
              const SizedBox(height: 24),
              Text(
                'Something went wrong',
                style: Theme.of(context).textTheme.headlineSmall,
              ),
              const SizedBox(height: 8),
              Text(
                ErrorHandler.getReadableMessage(error),
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: 32),
              AppButton.primary(
                text: 'Try Again',
                onPressed: onRetry,
              ),
            ],
          ),
        ),
      ),
    );
  }
}
```

### Form Validation Errors
```dart
// Enhanced form field with error display
class FormFieldWithError extends StatelessWidget {
  final Widget child;
  final String? errorText;
  final bool showError;

  const FormFieldWithError({
    super.key,
    required this.child,
    this.errorText,
    this.showError = true,
  });

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        child,
        AnimatedContainer(
          duration: const Duration(milliseconds: 200),
          height: showError && errorText != null ? 24 : 0,
          child: showError && errorText != null
              ? Padding(
                  padding: const EdgeInsets.only(top: 4, left: 12),
                  child: Row(
                    children: [
                      Icon(
                        Icons.error_outline,
                        size: 14,
                        color: AppColors.error,
                      ),
                      const SizedBox(width: 4),
                      Text(
                        errorText!,
                        style: TextStyle(
                          color: AppColors.error,
                          fontSize: 12,
                        ),
                      ),
                    ],
                  ),
                )
              : const SizedBox.shrink(),
        ),
      ],
    );
  }
}
```

### SMTP Error Dialog
```dart
class SmtpErrorDialog extends StatelessWidget {
  final String error;
  final VoidCallback? onRetry;
  final VoidCallback? onOpenSettings;

  const SmtpErrorDialog({
    super.key,
    required this.error,
    this.onRetry,
    this.onOpenSettings,
  });

  static Future<void> show(
    BuildContext context, {
    required String error,
    VoidCallback? onRetry,
  }) {
    return showDialog(
      context: context,
      builder: (context) => SmtpErrorDialog(
        error: error,
        onRetry: onRetry,
        onOpenSettings: () {
          Navigator.pop(context);
          Navigator.pushNamed(context, Routes.settings);
        },
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    final isAuthError = error.toLowerCase().contains('authentication') ||
        error.toLowerCase().contains('credentials');

    return AlertDialog(
      title: Row(
        children: [
          Icon(Icons.email_outlined, color: AppColors.error),
          const SizedBox(width: 8),
          const Text('Email Send Failed'),
        ],
      ),
      content: Column(
        mainAxisSize: MainAxisSize.min,
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(error),
          if (isAuthError) ...[
            const SizedBox(height: 16),
            Container(
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: AppColors.warning.withOpacity(0.1),
                borderRadius: BorderRadius.circular(8),
              ),
              child: Row(
                children: [
                  Icon(Icons.info_outline, color: AppColors.warning),
                  const SizedBox(width: 8),
                  const Expanded(
                    child: Text(
                      'You may need to update your app password in Settings.',
                      style: TextStyle(fontSize: 13),
                    ),
                  ),
                ],
              ),
            ),
          ],
        ],
      ),
      actions: [
        TextButton(
          onPressed: () => Navigator.pop(context),
          child: const Text('Close'),
        ),
        if (isAuthError)
          TextButton(
            onPressed: onOpenSettings,
            child: const Text('Open Settings'),
          ),
        if (onRetry != null)
          AppButton.primary(
            text: 'Retry',
            onPressed: () {
              Navigator.pop(context);
              onRetry!();
            },
          ),
      ],
    );
  }
}
```

## Acceptance Criteria
- [ ] Network errors show friendly messages
- [ ] SMTP errors suggest solutions
- [ ] Database errors handled gracefully
- [ ] Validation errors displayed inline
- [ ] Error details available (for debugging)
- [ ] Retry options where appropriate
- [ ] No crash on any error

## Dependencies
- Task 051 (AppColors)
- Task 059 (AppDialog)
- Task 056 (AppButton)

## Parallel Work
Can run parallel with: Task 094, 095

## Estimated Effort
2 hours
