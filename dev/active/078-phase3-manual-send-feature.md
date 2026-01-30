# Task 078: Implement Manual Send Feature

## Phase
3 - UI Foundation & MVP

## Description
Complete implementation of manual email sending from TODO card.

## Steps
1. Implement send confirmation dialog with preview
2. Connect to SendEmailUseCase via BLoC
3. Show success/error feedback
4. Update UI after send

## Code Structure

### send_confirmation_dialog.dart
```dart
import 'package:flutter/material.dart';
import '../../../core/di/injection.dart';
import '../../../core/theme/app_colors.dart';
import '../../../core/theme/app_dimensions.dart';
import '../../../domain/entities/todo.dart';
import '../../../domain/repositories/settings_repository.dart';
import '../../../services/email/template_service.dart';
import '../../../services/email/placeholder_service.dart';
import '../../widgets/app_button.dart';

class SendConfirmationDialog extends StatefulWidget {
  final Todo todo;
  final int sendCount;

  const SendConfirmationDialog({
    super.key,
    required this.todo,
    required this.sendCount,
  });

  static Future<bool> show(BuildContext context, Todo todo, int sendCount) async {
    final result = await showDialog<bool>(
      context: context,
      builder: (context) => SendConfirmationDialog(
        todo: todo,
        sendCount: sendCount,
      ),
    );
    return result ?? false;
  }

  @override
  State<SendConfirmationDialog> createState() => _SendConfirmationDialogState();
}

class _SendConfirmationDialogState extends State<SendConfirmationDialog> {
  final _templateService = getIt<TemplateService>();
  final _placeholderService = getIt<PlaceholderService>();
  final _settingsRepository = getIt<SettingsRepository>();

  bool _isLoading = true;
  String _previewSubject = '';
  String _previewBody = '';

  @override
  void initState() {
    super.initState();
    _loadPreview();
  }

  Future<void> _loadPreview() async {
    // Get templates
    final subject = await _templateService.getTemplate(
      sendCount: widget.sendCount,
      isSubject: true,
      language: widget.todo.language,
    );
    final body = await _templateService.getTemplate(
      sendCount: widget.sendCount,
      isSubject: false,
      language: widget.todo.language,
    );

    // Replace placeholders
    final data = {
      'firstName': widget.todo.recipientFirstName,
      'lastName': widget.todo.recipientLastName,
      'initialSubject': widget.todo.subject,
      'initialText': widget.todo.initialText,
    };

    setState(() {
      _previewSubject = _placeholderService.replace(template: subject, data: data);
      _previewBody = _placeholderService.replace(template: body, data: data);
      _isLoading = false;
    });
  }

  @override
  Widget build(BuildContext context) {
    return AlertDialog(
      title: const Text('Send Email?'),
      content: _isLoading
          ? const SizedBox(
              height: 100,
              child: Center(child: CircularProgressIndicator()),
            )
          : SingleChildScrollView(
              child: Column(
                crossAxisAlignment: CrossAxisAlignment.start,
                mainAxisSize: MainAxisSize.min,
                children: [
                  // Recipient
                  _buildInfoRow(
                    'To:',
                    widget.todo.recipientEmail,
                    Icons.person,
                  ),
                  const Divider(height: 24),

                  // Subject Preview
                  Text(
                    'Subject:',
                    style: TextStyle(
                      fontWeight: FontWeight.bold,
                      color: AppColors.onSurfaceVariant,
                    ),
                  ),
                  const SizedBox(height: 4),
                  Container(
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      color: AppColors.surfaceVariant,
                      borderRadius: BorderRadius.circular(8),
                    ),
                    child: Text(_previewSubject),
                  ),
                  const SizedBox(height: 16),

                  // Body Preview
                  Text(
                    'Body Preview:',
                    style: TextStyle(
                      fontWeight: FontWeight.bold,
                      color: AppColors.onSurfaceVariant,
                    ),
                  ),
                  const SizedBox(height: 4),
                  Container(
                    padding: const EdgeInsets.all(12),
                    decoration: BoxDecoration(
                      color: AppColors.surfaceVariant,
                      borderRadius: BorderRadius.circular(8),
                    ),
                    constraints: const BoxConstraints(maxHeight: 150),
                    child: SingleChildScrollView(
                      child: Text(
                        _previewBody,
                        style: const TextStyle(fontSize: 13),
                      ),
                    ),
                  ),
                  const SizedBox(height: 8),

                  // Send count info
                  Text(
                    'This will be email ${widget.sendCount + 1} for this TODO.',
                    style: TextStyle(
                      fontSize: 12,
                      color: AppColors.onSurfaceVariant,
                    ),
                  ),
                ],
              ),
            ),
      actions: [
        TextButton(
          onPressed: () => Navigator.pop(context, false),
          child: const Text('Cancel'),
        ),
        AppButton.primary(
          text: 'Send',
          onPressed: _isLoading ? null : () => Navigator.pop(context, true),
        ),
      ],
    );
  }

  Widget _buildInfoRow(String label, String value, IconData icon) {
    return Row(
      children: [
        Icon(icon, size: 16, color: AppColors.onSurfaceVariant),
        const SizedBox(width: 8),
        Text(
          label,
          style: TextStyle(color: AppColors.onSurfaceVariant),
        ),
        const SizedBox(width: 4),
        Expanded(
          child: Text(
            value,
            style: const TextStyle(fontWeight: FontWeight.w500),
            overflow: TextOverflow.ellipsis,
          ),
        ),
      ],
    );
  }
}
```

### Integration in SwipeableTodoCard
```dart
void _sendEmail(BuildContext context) async {
  final confirmed = await SendConfirmationDialog.show(
    context,
    todoWithCount.todo,
    todoWithCount.sendCount,
  );

  if (confirmed) {
    context.read<TodoBloc>().add(SendEmailForTodo(todoWithCount.todo.id!));
  }
}
```

### Success/Error handling in BLoC listener
```dart
BlocListener<TodoBloc, TodoState>(
  listener: (context, state) {
    if (state is TodoOperationSuccess) {
      ScaffoldMessenger.of(context).showSnackBar(
        SnackBar(
          content: Row(
            children: [
              Icon(Icons.check_circle, color: Colors.white),
              const SizedBox(width: 8),
              Text(state.message),
            ],
          ),
          backgroundColor: AppColors.success,
        ),
      );
    }

    if (state is TodoError) {
      AppDialog.showError(
        context: context,
        title: 'Send Failed',
        message: state.message,
        onRetry: () {
          // Retry logic if needed
        },
      );
    }
  },
  child: // ...
)
```

## Acceptance Criteria
- [ ] Confirmation dialog shows email preview
- [ ] Preview includes recipient, subject, body
- [ ] Placeholders replaced in preview
- [ ] Send count displayed
- [ ] Loading state while generating preview
- [ ] Success snackbar on successful send
- [ ] Error dialog with retry on failure
- [ ] TODO card shows loading during send
- [ ] UI updates after successful send

## Dependencies
- Task 039-041 (Placeholder, Template services)
- Task 045 (SendEmailUseCase)
- Task 062 (TodoBloc)
- Task 067 (SwipeableTodoCard)

## Parallel Work
Can run parallel with: Task 077

## Estimated Effort
2 hours
