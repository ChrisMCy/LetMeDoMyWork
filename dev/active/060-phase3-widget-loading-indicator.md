# Task 060: Create Loading Indicator Widgets

## Phase
3 - UI Foundation & MVP

## Description
Create loading indicator widgets including spinner, skeleton, and overlay.

## Steps
1. Create `lib/presentation/widgets/loading_indicator.dart`
2. Implement circular spinner
3. Implement skeleton loading
4. Implement full-screen loading overlay

## Code Structure
```dart
import 'package:flutter/material.dart';
import '../../core/theme/app_colors.dart';
import '../../core/theme/app_dimensions.dart';

/// Simple circular loading indicator
class LoadingIndicator extends StatelessWidget {
  final double size;
  final double strokeWidth;
  final Color? color;

  const LoadingIndicator({
    super.key,
    this.size = 24,
    this.strokeWidth = 2,
    this.color,
  });

  @override
  Widget build(BuildContext context) {
    return SizedBox(
      width: size,
      height: size,
      child: CircularProgressIndicator(
        strokeWidth: strokeWidth,
        valueColor: AlwaysStoppedAnimation(color ?? AppColors.primary),
      ),
    );
  }
}

/// Centered loading with optional message
class LoadingView extends StatelessWidget {
  final String? message;

  const LoadingView({super.key, this.message});

  @override
  Widget build(BuildContext context) {
    return Center(
      child: Column(
        mainAxisSize: MainAxisSize.min,
        children: [
          const LoadingIndicator(size: 48, strokeWidth: 3),
          if (message != null) ...[
            const SizedBox(height: AppDimensions.spacingMd),
            Text(
              message!,
              style: TextStyle(color: AppColors.onSurfaceVariant),
            ),
          ],
        ],
      ),
    );
  }
}

/// Full-screen loading overlay
class LoadingOverlay extends StatelessWidget {
  final Widget child;
  final bool isLoading;
  final String? message;

  const LoadingOverlay({
    super.key,
    required this.child,
    required this.isLoading,
    this.message,
  });

  @override
  Widget build(BuildContext context) {
    return Stack(
      children: [
        child,
        if (isLoading)
          Container(
            color: Colors.black54,
            child: LoadingView(message: message),
          ),
      ],
    );
  }
}

/// Skeleton loading placeholder
class SkeletonLoader extends StatefulWidget {
  final double width;
  final double height;
  final double borderRadius;

  const SkeletonLoader({
    super.key,
    this.width = double.infinity,
    required this.height,
    this.borderRadius = 4,
  });

  @override
  State<SkeletonLoader> createState() => _SkeletonLoaderState();
}

class _SkeletonLoaderState extends State<SkeletonLoader>
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
    _animation = Tween<double>(begin: -1, end: 2).animate(_controller);
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
              end: Alignment(_animation.value, 0),
              colors: const [
                AppColors.shimmerBase,
                AppColors.shimmerHighlight,
                AppColors.shimmerBase,
              ],
            ),
          ),
        );
      },
    );
  }
}

/// Skeleton card for TODO list loading
class TodoCardSkeleton extends StatelessWidget {
  const TodoCardSkeleton({super.key});

  @override
  Widget build(BuildContext context) {
    return Card(
      margin: const EdgeInsets.symmetric(
        horizontal: AppDimensions.spacingMd,
        vertical: AppDimensions.spacingSm,
      ),
      child: Padding(
        padding: const EdgeInsets.all(AppDimensions.paddingCard),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Row(
              children: [
                const Expanded(
                  child: SkeletonLoader(height: 20),
                ),
                const SizedBox(width: AppDimensions.spacingMd),
                SkeletonLoader(
                  width: 40,
                  height: 24,
                  borderRadius: 12,
                ),
              ],
            ),
            const SizedBox(height: AppDimensions.spacingSm),
            const SkeletonLoader(height: 16, width: 200),
            const SizedBox(height: AppDimensions.spacingMd),
            Row(
              children: const [
                Expanded(child: SkeletonLoader(height: 14)),
                SizedBox(width: AppDimensions.spacingMd),
                Expanded(child: SkeletonLoader(height: 14)),
              ],
            ),
          ],
        ),
      ),
    );
  }
}

/// List of skeleton cards
class TodoListSkeleton extends StatelessWidget {
  final int count;

  const TodoListSkeleton({super.key, this.count = 5});

  @override
  Widget build(BuildContext context) {
    return ListView.builder(
      itemCount: count,
      physics: const NeverScrollableScrollPhysics(),
      itemBuilder: (context, index) => const TodoCardSkeleton(),
    );
  }
}
```

## Usage Examples
```dart
// Simple spinner
const LoadingIndicator()

// Centered with message
const LoadingView(message: 'Sending email...')

// Full screen overlay
LoadingOverlay(
  isLoading: _isSending,
  message: 'Sending...',
  child: YourContent(),
)

// Skeleton loading
if (state is Loading)
  const TodoListSkeleton()
else
  TodoList(todos: state.todos)
```

## Acceptance Criteria
- [ ] Circular loading indicator
- [ ] Centered loading view with message
- [ ] Full-screen loading overlay
- [ ] Skeleton loader with shimmer animation
- [ ] TODO card skeleton
- [ ] TODO list skeleton (multiple cards)

## Dependencies
- Task 051 (AppColors)
- Task 053 (AppDimensions)

## Parallel Work
Can run parallel with: Task 056, 057, 058, 059

## Estimated Effort
1.5 hours
