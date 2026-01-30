# Task 094: Implement Animations

## Phase
6 - Polish & Testing

## Description
Add smooth animations throughout the app.

## Steps
1. Screen transitions
2. List item animations
3. Swipe animations
4. Button and feedback animations

## Code Structure

### Screen Transitions (Already in AppRouter)
```dart
// Slide from right (default)
static PageRouteBuilder _slideRoute(Widget page) {
  return PageRouteBuilder(
    pageBuilder: (context, animation, secondaryAnimation) => page,
    transitionsBuilder: (context, animation, secondaryAnimation, child) {
      const begin = Offset(1.0, 0.0);
      const end = Offset.zero;
      const curve = Curves.easeInOut;

      var tween = Tween(begin: begin, end: end).chain(
        CurveTween(curve: curve),
      );

      return SlideTransition(
        position: animation.drive(tween),
        child: child,
      );
    },
    transitionDuration: const Duration(milliseconds: 300),
  );
}
```

### List Item Animations
```dart
// lib/presentation/widgets/animated_list_item.dart
class AnimatedListItem extends StatefulWidget {
  final Widget child;
  final int index;

  const AnimatedListItem({
    super.key,
    required this.child,
    required this.index,
  });

  @override
  State<AnimatedListItem> createState() => _AnimatedListItemState();
}

class _AnimatedListItemState extends State<AnimatedListItem>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<Offset> _slideAnimation;
  late Animation<double> _fadeAnimation;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      duration: const Duration(milliseconds: 300),
      vsync: this,
    );

    // Stagger based on index
    final delay = Duration(milliseconds: widget.index * 50);

    _slideAnimation = Tween<Offset>(
      begin: const Offset(0, 0.3),
      end: Offset.zero,
    ).animate(CurvedAnimation(
      parent: _controller,
      curve: Curves.easeOut,
    ));

    _fadeAnimation = Tween<double>(
      begin: 0.0,
      end: 1.0,
    ).animate(CurvedAnimation(
      parent: _controller,
      curve: Curves.easeOut,
    ));

    Future.delayed(delay, () {
      if (mounted) _controller.forward();
    });
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return SlideTransition(
      position: _slideAnimation,
      child: FadeTransition(
        opacity: _fadeAnimation,
        child: widget.child,
      ),
    );
  }
}
```

### Swipe Animation Enhancements
```dart
// Enhanced swipe background with scale animation
Widget _buildSwipeBackground({
  required Color color,
  required IconData icon,
  required String label,
  required Alignment alignment,
  required Animation<double> animation,
}) {
  return AnimatedBuilder(
    animation: animation,
    builder: (context, child) {
      final scale = 0.8 + (animation.value * 0.4); // Scale from 0.8 to 1.2

      return Container(
        decoration: BoxDecoration(
          color: Color.lerp(color.withOpacity(0.5), color, animation.value),
          borderRadius: BorderRadius.circular(AppDimensions.radiusLg),
        ),
        alignment: alignment,
        padding: const EdgeInsets.symmetric(horizontal: 24),
        child: Transform.scale(
          scale: scale.clamp(0.8, 1.2),
          child: Row(
            mainAxisSize: MainAxisSize.min,
            children: [
              Icon(icon, color: Colors.white, size: 24),
              const SizedBox(width: 8),
              Text(
                label,
                style: const TextStyle(
                  color: Colors.white,
                  fontWeight: FontWeight.w600,
                ),
              ),
            ],
          ),
        ),
      );
    },
  );
}
```

### Button Press Animation
```dart
// lib/presentation/widgets/animated_press_button.dart
class AnimatedPressButton extends StatefulWidget {
  final Widget child;
  final VoidCallback? onTap;

  const AnimatedPressButton({
    super.key,
    required this.child,
    this.onTap,
  });

  @override
  State<AnimatedPressButton> createState() => _AnimatedPressButtonState();
}

class _AnimatedPressButtonState extends State<AnimatedPressButton>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<double> _scaleAnimation;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      duration: const Duration(milliseconds: 100),
      vsync: this,
    );

    _scaleAnimation = Tween<double>(
      begin: 1.0,
      end: 0.95,
    ).animate(CurvedAnimation(
      parent: _controller,
      curve: Curves.easeInOut,
    ));
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  void _onTapDown(TapDownDetails details) {
    _controller.forward();
  }

  void _onTapUp(TapUpDetails details) {
    _controller.reverse();
    widget.onTap?.call();
  }

  void _onTapCancel() {
    _controller.reverse();
  }

  @override
  Widget build(BuildContext context) {
    return GestureDetector(
      onTapDown: _onTapDown,
      onTapUp: _onTapUp,
      onTapCancel: _onTapCancel,
      child: ScaleTransition(
        scale: _scaleAnimation,
        child: widget.child,
      ),
    );
  }
}
```

### Success/Error Feedback Animations
```dart
// lib/presentation/widgets/animated_feedback.dart
class AnimatedFeedback extends StatefulWidget {
  final bool isSuccess;
  final VoidCallback? onComplete;

  const AnimatedFeedback({
    super.key,
    required this.isSuccess,
    this.onComplete,
  });

  @override
  State<AnimatedFeedback> createState() => _AnimatedFeedbackState();
}

class _AnimatedFeedbackState extends State<AnimatedFeedback>
    with SingleTickerProviderStateMixin {
  late AnimationController _controller;
  late Animation<double> _scaleAnimation;

  @override
  void initState() {
    super.initState();
    _controller = AnimationController(
      duration: const Duration(milliseconds: 600),
      vsync: this,
    );

    _scaleAnimation = Tween<double>(begin: 0, end: 1)
        .chain(CurveTween(curve: Curves.elasticOut))
        .animate(_controller);

    _controller.forward().then((_) {
      Future.delayed(const Duration(milliseconds: 500), () {
        widget.onComplete?.call();
      });
    });
  }

  @override
  void dispose() {
    _controller.dispose();
    super.dispose();
  }

  @override
  Widget build(BuildContext context) {
    return ScaleTransition(
      scale: _scaleAnimation,
      child: Container(
        padding: const EdgeInsets.all(24),
        decoration: BoxDecoration(
          color: widget.isSuccess
              ? AppColors.success.withOpacity(0.1)
              : AppColors.error.withOpacity(0.1),
          shape: BoxShape.circle,
        ),
        child: Icon(
          widget.isSuccess ? Icons.check : Icons.close,
          size: 48,
          color: widget.isSuccess ? AppColors.success : AppColors.error,
        ),
      ),
    );
  }
}
```

## Acceptance Criteria
- [ ] Screen transitions smooth (slide from right)
- [ ] List items animate in on load (staggered)
- [ ] Swipe backgrounds animate smoothly
- [ ] Button press has subtle scale effect
- [ ] Success/error feedback animated
- [ ] No janky animations
- [ ] Animations respect reduced motion settings

## Dependencies
- Task 050-053 (Theme)
- Task 066-067 (TODO cards)

## Parallel Work
Can run parallel with: Task 095, 096

## Estimated Effort
3-4 hours
