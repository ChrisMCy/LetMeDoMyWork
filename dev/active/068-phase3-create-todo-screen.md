# Task 068: Create CreateTodoScreen

## Phase
3 - UI Foundation & MVP

## Description
Implement the screen for creating a new TODO.

## Steps
1. Create `lib/presentation/screens/todo/create_todo_screen.dart`
2. Implement all form fields
3. Add form validation
4. Connect to BLoC for saving

## Code Structure
```dart
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import '../../../core/di/injection.dart';
import '../../../core/theme/app_colors.dart';
import '../../../core/theme/app_dimensions.dart';
import '../../../domain/entities/todo.dart';
import '../../../services/email/email_parsing_service.dart';
import '../../../services/email/template_service.dart';
import '../../bloc/todo/todo_bloc.dart';
import '../../bloc/todo/todo_event.dart';
import '../../widgets/app_button.dart';
import '../../widgets/app_text_field.dart';
import 'widgets/language_toggle.dart';
import 'widgets/template_row.dart';
import 'widgets/date_time_picker.dart';

class CreateTodoScreen extends StatefulWidget {
  const CreateTodoScreen({super.key});

  @override
  State<CreateTodoScreen> createState() => _CreateTodoScreenState();
}

class _CreateTodoScreenState extends State<CreateTodoScreen> {
  final _formKey = GlobalKey<FormState>();
  final _emailController = TextEditingController();
  final _firstNameController = TextEditingController();
  final _lastNameController = TextEditingController();
  final _subjectController = TextEditingController();
  final _textController = TextEditingController();

  String _language = 'EN';
  int _intervalDays = 3;
  TimeOfDay _sendTime = const TimeOfDay(hour: 9, minute: 0);
  bool _isLoading = false;

  final _emailParsingService = getIt<EmailParsingService>();
  final _templateService = getIt<TemplateService>();

  @override
  void initState() {
    super.initState();
    _loadRandomTemplates();
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

  Future<void> _loadRandomTemplates() async {
    final subject = await _templateService.getRandomTemplate(
      isSubject: true,
      language: _language,
    );
    final text = await _templateService.getRandomTemplate(
      isSubject: false,
      language: _language,
    );

    setState(() {
      _subjectController.text = subject;
      _textController.text = text;
    });
  }

  void _onEmailChanged(String email) {
    if (_firstNameController.text.isEmpty && _lastNameController.text.isEmpty) {
      final (firstName, lastName) = _emailParsingService.parseEmail(email);
      _firstNameController.text = firstName;
      _lastNameController.text = lastName;
    }
  }

  void _swapNames() {
    final temp = _firstNameController.text;
    _firstNameController.text = _lastNameController.text;
    _lastNameController.text = temp;
  }

  void _onLanguageChanged(String language) {
    setState(() {
      _language = language;
    });
    _loadRandomTemplates();
  }

  Future<void> _save() async {
    if (!_formKey.currentState!.validate()) return;

    setState(() => _isLoading = true);

    final todo = Todo(
      recipientEmail: _emailController.text.trim(),
      recipientFirstName: _firstNameController.text.trim(),
      recipientLastName: _lastNameController.text.trim(),
      subject: _subjectController.text.trim(),
      initialText: _textController.text.trim(),
      language: _language,
      intervalDays: _intervalDays,
      sendTime: _sendTime,
      createdAt: DateTime.now(),
    );

    context.read<TodoBloc>().add(CreateTodo(todo));

    setState(() => _isLoading = false);
    Navigator.pop(context);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('New TODO'),
        actions: [
          TextButton(
            onPressed: _isLoading ? null : _save,
            child: _isLoading
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
            // Email
            AppTextField.email(
              controller: _emailController,
              label: 'Recipient Email',
              onChanged: _onEmailChanged,
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
              onChanged: _onLanguageChanged,
            ),
            const SizedBox(height: AppDimensions.spacingMd),

            // Subject Template
            TemplateRow(
              label: 'Subject',
              controller: _subjectController,
              onReload: () => _loadRandomTemplates(),
            ),
            const SizedBox(height: AppDimensions.spacingMd),

            // Text Template
            AppTextField.multiline(
              controller: _textController,
              label: 'Email Body',
              maxLines: 6,
            ),
            TextButton.icon(
              icon: const Icon(Icons.refresh),
              label: const Text('Reload Template'),
              onPressed: _loadRandomTemplates,
            ),
            const SizedBox(height: AppDimensions.spacingLg),

            // Interval
            _buildIntervalSelector(),
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
              text: 'Create TODO',
              isLoading: _isLoading,
              isFullWidth: true,
              onPressed: _save,
            ),
          ],
        ),
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
- [ ] Email field with validation
- [ ] Auto-populate names from email
- [ ] Name swap button works
- [ ] Language toggle (EN/DE)
- [ ] Subject field with reload button
- [ ] Email body (multiline) with reload button
- [ ] Interval slider (1-14 days)
- [ ] Send time picker
- [ ] Form validation
- [ ] Save creates TODO and navigates back
- [ ] Loading state during save

## Dependencies
- Task 040 (EmailParsingService)
- Task 041 (TemplateService)
- Task 056-057 (Widgets)
- Task 062 (TodoBloc)

## Parallel Work
Can run parallel with: Task 069

## Estimated Effort
3-4 hours
