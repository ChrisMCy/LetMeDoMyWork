# Task 069: Create EditTodoScreen

## Phase
3 - UI Foundation & MVP

## Description
Implement the screen for editing an existing TODO.

## Steps
1. Create `lib/presentation/screens/todo/edit_todo_screen.dart`
2. Load existing TODO data
3. Handle interval change (triggers next_send recalculation)
4. Add delete option

## Code Structure
```dart
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import '../../../core/di/injection.dart';
import '../../../core/theme/app_dimensions.dart';
import '../../../domain/entities/todo.dart';
import '../../../domain/repositories/todo_repository.dart';
import '../../bloc/todo/todo_bloc.dart';
import '../../bloc/todo/todo_event.dart';
import '../../widgets/app_button.dart';
import '../../widgets/app_dialog.dart';
import '../../widgets/app_text_field.dart';
import '../../widgets/loading_indicator.dart';
import 'widgets/language_toggle.dart';
import 'widgets/date_time_picker.dart';

class EditTodoScreen extends StatefulWidget {
  final int todoId;

  const EditTodoScreen({super.key, required this.todoId});

  @override
  State<EditTodoScreen> createState() => _EditTodoScreenState();
}

class _EditTodoScreenState extends State<EditTodoScreen> {
  final _formKey = GlobalKey<FormState>();
  final _emailController = TextEditingController();
  final _firstNameController = TextEditingController();
  final _lastNameController = TextEditingController();
  final _subjectController = TextEditingController();
  final _textController = TextEditingController();

  String _language = 'EN';
  int _intervalDays = 3;
  int _originalIntervalDays = 3;
  TimeOfDay _sendTime = const TimeOfDay(hour: 9, minute: 0);

  bool _isLoading = true;
  bool _isSaving = false;
  Todo? _todo;

  final _todoRepository = getIt<TodoRepository>();

  @override
  void initState() {
    super.initState();
    _loadTodo();
  }

  Future<void> _loadTodo() async {
    final todo = await _todoRepository.getTodoById(widget.todoId);
    if (todo == null) {
      Navigator.pop(context);
      return;
    }

    setState(() {
      _todo = todo;
      _emailController.text = todo.recipientEmail;
      _firstNameController.text = todo.recipientFirstName ?? '';
      _lastNameController.text = todo.recipientLastName ?? '';
      _subjectController.text = todo.subject;
      _textController.text = todo.initialText ?? '';
      _language = todo.language;
      _intervalDays = todo.intervalDays;
      _originalIntervalDays = todo.intervalDays;
      _sendTime = todo.sendTime;
      _isLoading = false;
    });
  }

  @override
  void dispose() {
    _emailController.dispose();
    _firstNameController.dispose();
    _lastNameController.dispose();
    _subjectController.dispose();
    _textController.dispose();
    super.dispose();
  }

  void _swapNames() {
    final temp = _firstNameController.text;
    _firstNameController.text = _lastNameController.text;
    _lastNameController.text = temp;
  }

  Future<void> _save() async {
    if (!_formKey.currentState!.validate()) return;
    if (_todo == null) return;

    setState(() => _isSaving = true);

    final updatedTodo = _todo!.copyWith(
      recipientEmail: _emailController.text.trim(),
      recipientFirstName: _firstNameController.text.trim(),
      recipientLastName: _lastNameController.text.trim(),
      subject: _subjectController.text.trim(),
      initialText: _textController.text.trim(),
      language: _language,
      intervalDays: _intervalDays,
      sendTime: _sendTime,
    );

    final intervalChanged = _intervalDays != _originalIntervalDays;

    context.read<TodoBloc>().add(
      UpdateTodo(updatedTodo, intervalChanged: intervalChanged),
    );

    setState(() => _isSaving = false);
    Navigator.pop(context);
  }

  Future<void> _delete() async {
    final confirmed = await AppDialog.showConfirmation(
      context: context,
      title: 'Delete TODO?',
      message: 'This will permanently delete this TODO and all its sent emails. This action cannot be undone.',
      confirmText: 'Delete',
      isDangerous: true,
    );

    if (confirmed) {
      context.read<TodoBloc>().add(DeleteTodo(widget.todoId));
      Navigator.pop(context);
    }
  }

  @override
  Widget build(BuildContext context) {
    if (_isLoading) {
      return Scaffold(
        appBar: AppBar(title: const Text('Edit TODO')),
        body: const LoadingView(message: 'Loading TODO...'),
      );
    }

    return Scaffold(
      appBar: AppBar(
        title: const Text('Edit TODO'),
        actions: [
          IconButton(
            icon: const Icon(Icons.delete),
            onPressed: _delete,
            tooltip: 'Delete',
          ),
          TextButton(
            onPressed: _isSaving ? null : _save,
            child: _isSaving
                ? const SizedBox(
                    width: 20,
                    height: 20,
                    child: CircularProgressIndicator(strokeWidth: 2),
                  )
                : const Text('Save'),
          ),
        ],
      ),
      body: Form(
        key: _formKey,
        child: ListView(
          padding: const EdgeInsets.all(AppDimensions.paddingScreen),
          children: [
            // Status indicators
            if (_todo!.isPaused)
              _buildStatusBanner('Paused', Icons.pause_circle, Colors.orange),
            if (_todo!.isCompleted)
              _buildStatusBanner('Completed', Icons.check_circle, Colors.green),

            // Email (read-only for existing TODO)
            AppTextField.email(
              controller: _emailController,
              label: 'Recipient Email',
              readOnly: true, // Can't change email after creation
            ),
            const SizedBox(height: AppDimensions.spacingMd),

            // Name fields with swap
            Row(
              children: [
                Expanded(
                  child: AppTextField(
                    controller: _firstNameController,
                    label: 'First Name',
                  ),
                ),
                IconButton(
                  icon: const Icon(Icons.swap_horiz),
                  onPressed: _swapNames,
                  tooltip: 'Swap names',
                ),
                Expanded(
                  child: AppTextField(
                    controller: _lastNameController,
                    label: 'Last Name',
                  ),
                ),
              ],
            ),
            const SizedBox(height: AppDimensions.spacingLg),

            // Language Toggle
            LanguageToggle(
              selectedLanguage: _language,
              onChanged: (lang) => setState(() => _language = lang),
            ),
            const SizedBox(height: AppDimensions.spacingMd),

            // Subject
            AppTextField(
              controller: _subjectController,
              label: 'Subject',
              validator: (v) => v?.isEmpty == true ? 'Required' : null,
            ),
            const SizedBox(height: AppDimensions.spacingMd),

            // Text
            AppTextField.multiline(
              controller: _textController,
              label: 'Email Body',
              maxLines: 6,
            ),
            const SizedBox(height: AppDimensions.spacingLg),

            // Interval
            _buildIntervalSelector(),
            if (_intervalDays != _originalIntervalDays)
              Padding(
                padding: const EdgeInsets.only(top: 8),
                child: Text(
                  'Changing interval will recalculate the next send date',
                  style: TextStyle(
                    color: Colors.orange,
                    fontSize: 12,
                  ),
                ),
              ),
            const SizedBox(height: AppDimensions.spacingMd),

            // Send Time
            DateTimePicker(
              label: 'Preferred Send Time',
              time: _sendTime,
              onTimeChanged: (time) => setState(() => _sendTime = time),
            ),
            const SizedBox(height: AppDimensions.spacingXl),

            // Save Button
            AppButton.primary(
              text: 'Save Changes',
              isLoading: _isSaving,
              isFullWidth: true,
              onPressed: _save,
            ),
            const SizedBox(height: AppDimensions.spacingMd),

            // Delete Button
            AppButton.danger(
              text: 'Delete TODO',
              icon: Icons.delete,
              isFullWidth: true,
              onPressed: _delete,
            ),
          ],
        ),
      ),
    );
  }

  Widget _buildStatusBanner(String text, IconData icon, Color color) {
    return Container(
      margin: const EdgeInsets.only(bottom: AppDimensions.spacingMd),
      padding: const EdgeInsets.all(12),
      decoration: BoxDecoration(
        color: color.withOpacity(0.1),
        borderRadius: BorderRadius.circular(8),
        border: Border.all(color: color),
      ),
      child: Row(
        children: [
          Icon(icon, color: color),
          const SizedBox(width: 8),
          Text(
            text,
            style: TextStyle(color: color, fontWeight: FontWeight.w600),
          ),
        ],
      ),
    );
  }

  Widget _buildIntervalSelector() {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          'Send Interval: $_intervalDays days',
          style: Theme.of(context).textTheme.titleSmall,
        ),
        Slider(
          value: _intervalDays.toDouble(),
          min: 1,
          max: 14,
          divisions: 13,
          label: '$_intervalDays days',
          onChanged: (value) {
            setState(() => _intervalDays = value.round());
          },
        ),
      ],
    );
  }
}
```

## Acceptance Criteria
- [ ] Loads existing TODO data
- [ ] Email field is read-only (can't change after creation)
- [ ] Shows status banner if paused/completed
- [ ] Name swap works
- [ ] Warning shown when interval is changed
- [ ] Delete with confirmation dialog
- [ ] Save updates TODO and navigates back
- [ ] Loading state while fetching TODO

## Dependencies
- Task 056-057 (Widgets)
- Task 059 (AppDialog)
- Task 062 (TodoBloc)
- Task 068 (Shared widgets like LanguageToggle, DateTimePicker)

## Parallel Work
Can run parallel with: Task 068

## Estimated Effort
2-3 hours
