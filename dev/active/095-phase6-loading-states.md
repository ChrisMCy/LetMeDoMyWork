# Task 095: Implement Loading States

## Phase
6 - Polish & Testing

## Description
Add proper loading states throughout the app.

## Steps
1. Skeleton loading for lists
2. Button loading states
3. Screen loading states
4. Inline loading indicators

## Code Implementation

### Skeleton Improvements
```dart
// Enhanced skeleton with shimmer
class ShimmerSkeleton extends StatefulWidget {
  final double width;
  final double height;
  final double borderRadius;

  const ShimmerSkeleton({
    super.key,
    this.width = double.infinity,
    required this.height,
    this.borderRadius = 4,
  });

  @override
  State<ShimmerSkeleton> createState() => _ShimmerSkeletonState();
}

class _ShimmerSkeletonState extends State<ShimmerSkeleton>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<double> _animation;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      duration: const Duration(milliseconds: 1500),
      vsync: this,
    )..repeat();

    _animation = Tween<double>(begin: -1.5, end: 1.5).animate(
      CurvedAnimation(parent: _controller, curve: Curves.easeInOut),
    );
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return AnimatedBuilder(
      animation: _animation,
      builder: (context, child) {
        return Container(
          width: widget.width,
          height: widget.height,
          decoration: BoxDecoration(
            borderRadius: BorderRadius.circular(widget.borderRadius),
            gradient: LinearGradient(
              begin: Alignment(_animation.value - 1, 0),
              end: Alignment(_animation.value + 1, 0),
              colors: const [
                Color(0xFFE0E0E0),
                Color(0xFFF5F5F5),
                Color(0xFFE0E0E0),
              ],
              stops: const [0.0, 0.5, 1.0],
            ),
          ),
        );
      },
    );
  }
}
```

### Full Screen Loading Overlay
```dart
class LoadingOverlay {
  static OverlayEntry? _overlayEntry;

  static void show(BuildContext context, {String? message}) {
    if (_overlayEntry != null) return;

    _overlayEntry = OverlayEntry(
      builder: (context) => Material(
        color: Colors.black54,
        child: Center(
          child: Container(
            padding: const EdgeInsets.all(32),
            decoration: BoxDecoration(
              color: Colors.white,
              borderRadius: BorderRadius.circular(16),
            ),
            child: Column(
              mainAxisSize: MainAxisSize.min,
              children: [
                const CircularProgressIndicator(),
                if (message != null) ...[
                  const SizedBox(height: 16),
                  Text(message),
                ],
              ],
            ),
          ),
        ),
      ),
    );

    Overlay.of(context).insert(_overlayEntry!);
  }

  static void hide() {
    _overlayEntry?.remove();
    _overlayEntry = null;
  }
}
```

### Screen Loading State Widget
```dart
class LoadingStateWidget extends StatelessWidget {
  final bool isLoading;
  final bool hasError;
  final String? errorMessage;
  final VoidCallback? onRetry;
  final Widget child;
  final Widget? loadingWidget;

  const LoadingStateWidget({
    super.key,
    required this.isLoading,
    this.hasError = false,
    this.errorMessage,
    this.onRetry,
    required this.child,
    this.loadingWidget,
  });

  @override
  Widget build(BuildContext context) {
    if (isLoading) {
      return loadingWidget ?? const LoadingView();
    }

    if (hasError) {
      return ErrorView(
        message: errorMessage ?? 'Something went wrong',
        onRetry: onRetry,
      );
    }

    return child;
  }
}

class ErrorView extends StatelessWidget {
  final String message;
  final VoidCallback? onRetry;

  const ErrorView({
    super.key,
    required this.message,
    this.onRetry,
  });

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Padding(
        padding: const EdgeInsets.all(32),
        child: Column(
          mainAxisSize: MainAxisSize.min,
          children: [
            Icon(
              Icons.error_outline,
              size: 64,
              color: AppColors.error,
            ),
            const SizedBox(height: 16),
            Text(
              message,
              textAlign: TextAlign.center,
              style: Theme.of(context).textTheme.bodyLarge,
            ),
            if (onRetry != null) ...[
              const SizedBox(height: 24),
              AppButton.primary(
                text: 'Try Again',
                icon: Icons.refresh,
                onPressed: onRetry,
              ),
            ],
          ],
        ),
      ),
    );
  }
}
```

### Inline Loading for Specific Actions
```dart
class InlineLoadingButton extends StatelessWidget {
  final String text;
  final bool isLoading;
  final VoidCallback? onPressed;
  final IconData? icon;

  const InlineLoadingButton({
    super.key,
    required this.text,
    this.isLoading = false,
    this.onPressed,
    this.icon,
  });

  @override
  Widget build(BuildContext context) {
    return TextButton(
      onPressed: isLoading ? null : onPressed,
      child: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          if (isLoading)
            const Padding(
              padding: EdgeInsets.only(right: 8),
              child: SizedBox(
                width: 16,
                height: 16,
                child: CircularProgressIndicator(strokeWidth: 2),
              ),
            )
          else if (icon != null)
            Padding(
              padding: const EdgeInsets.only(right: 8),
              child: Icon(icon, size: 18),
            ),
          Text(text),
        ],
      ),
    );
  }
}
```

## Usage Examples
```dart
// In a screen
LoadingStateWidget(
  isLoading: state is Loading,
  hasError: state is Error,
  errorMessage: (state is Error) ? state.message : null,
  onRetry: () => bloc.add(LoadData()),
  loadingWidget: const TodoListSkeleton(),
  child: TodoList(todos: state.todos),
)

// Full screen overlay during save
AppButton.primary(
  text: 'Save',
  onPressed: () async {
    LoadingOverlay.show(context, message: 'Saving...');
    await save();
    LoadingOverlay.hide();
  },
)
```

## Acceptance Criteria
- [ ] Skeleton loading for TODO list
- [ ] Skeleton loading for statistics
- [ ] Button loading states
- [ ] Full-screen loading overlay
- [ ] Error states with retry
- [ ] Shimmer animation smooth
- [ ] Loading states consistent across app

## Dependencies
- Task 060 (LoadingIndicator base)
- Task 051 (AppColors)

## Parallel Work
Can run parallel with: Task 094, 096

## Estimated Effort
2 hours
