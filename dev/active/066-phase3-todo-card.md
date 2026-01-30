# Task 066: Create TodoCard Widget

## Phase
3 - UI Foundation & MVP

## Description
Implement the TODO card displaying all relevant information.

## Steps
1. Create `lib/presentation/screens/main/widgets/todo_card.dart`
2. Display subject, email, dates, send count
3. Implement color gradient based on send count
4. Add pause indicator and manual send button

## Code Structure
```dart
import 'package:flutter/material.dart';
import 'package:intl/intl.dart';
import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_dimensions.dart';
import '../../../../core/theme/app_text_styles.dart';
import '../../../../domain/entities/todo.dart';
import '../../../../domain/usecases/todo/get_todos_usecase.dart';
import '../../../widgets/app_card.dart';

class TodoCard extends StatelessWidget {
  final TodoWithSendCount todoWithCount;
  final VoidCallback? onTap;
  final VoidCallback? onSendPressed;
  final bool isSending;
  final int maxSends;

  const TodoCard({
    super.key,
    required this.todoWithCount,
    this.onTap,
    this.onSendPressed,
    this.isSending = false,
    this.maxSends = 10,
  });

  Todo get todo => todoWithCount.todo;
  int get sendCount => todoWithCount.sendCount;

  @override
  Widget build(BuildContext context) {
    final cardColor = todo.isPaused
        ? AppColors.todoPaused
        : AppColors.getTodoColor(sendCount, maxSends);
    final cardColorLight = todo.isPaused
        ? AppColors.todoPaused.withOpacity(0.7)
        : AppColors.getTodoColorLight(sendCount, maxSends);

    return GradientCard(
      startColor: cardColor,
      endColor: cardColorLight,
      onTap: onTap,
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Top Row: Subject + Badge
          Row(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              // Pause icon if paused
              if (todo.isPaused) ...[
                Icon(
                  Icons.pause_circle_filled,
                  size: 20,
                  color: Colors.white70,
                ),
                const SizedBox(width: 8),
              ],
              // Subject
              Expanded(
                child: Text(
                  todo.subject,
                  style: AppTextStyles.todoSubject.copyWith(
                    color: Colors.white,
                  ),
                  maxLines: 2,
                  overflow: TextOverflow.ellipsis,
                ),
              ),
              const SizedBox(width: 8),
              // Send Count Badge
              _buildSendCountBadge(),
            ],
          ),
          const SizedBox(height: 8),

          // Email
          Row(
            children: [
              Icon(Icons.email_outlined, size: 16, color: Colors.white70),
              const SizedBox(width: 4),
              Expanded(
                child: Text(
                  todo.recipientEmail,
                  style: AppTextStyles.todoEmail.copyWith(
                    color: Colors.white70,
                  ),
                  overflow: TextOverflow.ellipsis,
                ),
              ),
            ],
          ),
          const SizedBox(height: 12),

          // Bottom Row: Dates + Send Button
          Row(
            children: [
              // Dates
              Expanded(
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    if (todo.lastSendDateTime != null)
                      _buildDateRow(
                        'Last:',
                        _formatDate(todo.lastSendDateTime!),
                      ),
                    if (todo.nextSendDateTime != null && !todo.isCompleted)
                      _buildDateRow(
                        'Next:',
                        _formatDate(todo.nextSendDateTime!),
                      ),
                  ],
                ),
              ),

              // Manual Send Button
              if (!todo.isCompleted && !todo.isPaused)
                _buildSendButton(),
            ],
          ),
        ],
      ),
    );
  }

  Widget _buildSendCountBadge() {
    return Container(
      padding: const EdgeInsets.symmetric(horizontal: 8, vertical: 4),
      decoration: BoxDecoration(
        color: Colors.black26,
        borderRadius: BorderRadius.circular(12),
      ),
      child: Text(
        '$sendCount/$maxSends',
        style: AppTextStyles.todoBadge,
      ),
    );
  }

  Widget _buildDateRow(String label, String date) {
    return Padding(
      padding: const EdgeInsets.only(bottom: 2),
      child: Row(
        children: [
          Text(
            label,
            style: TextStyle(
              fontSize: 12,
              color: Colors.white60,
            ),
          ),
          const SizedBox(width: 4),
          Text(
            date,
            style: TextStyle(
              fontSize: 12,
              fontWeight: FontWeight.w500,
              color: Colors.white,
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildSendButton() {
    return Material(
      color: Colors.white24,
      borderRadius: BorderRadius.circular(8),
      child: InkWell(
        onTap: isSending ? null : onSendPressed,
        borderRadius: BorderRadius.circular(8),
        child: Padding(
          padding: const EdgeInsets.all(8),
          child: isSending
              ? SizedBox(
                  width: 24,
                  height: 24,
                  child: CircularProgressIndicator(
                    strokeWidth: 2,
                    valueColor: AlwaysStoppedAnimation(Colors.white),
                  ),
                )
              : Icon(
                  Icons.send,
                  color: Colors.white,
                  size: 24,
                ),
        ),
      ),
    );
  }

  String _formatDate(DateTime date) {
    final now = DateTime.now();
    final diff = date.difference(now);

    if (diff.inDays == 0) {
      return 'Today ${DateFormat.Hm().format(date)}';
    } else if (diff.inDays == 1) {
      return 'Tomorrow ${DateFormat.Hm().format(date)}';
    } else if (diff.inDays == -1) {
      return 'Yesterday ${DateFormat.Hm().format(date)}';
    } else {
      return DateFormat('dd.MM.yyyy').format(date);
    }
  }
}
```

## Acceptance Criteria
- [ ] Displays subject (max 2 lines with ellipsis)
- [ ] Displays recipient email
- [ ] Displays send count badge (X/10)
- [ ] Gradient color based on send_count/max_sends ratio
- [ ] Gray color when paused with pause icon
- [ ] Shows last send date (if exists)
- [ ] Shows next send date (if not completed)
- [ ] Manual send button (not shown when paused/completed)
- [ ] Loading state on send button while sending
- [ ] Tap to edit/view details

## Dependencies
- Task 051 (AppColors)
- Task 052 (AppTextStyles)
- Task 058 (GradientCard)

## Parallel Work
Can run parallel with: Task 065

## Estimated Effort
2 hours
