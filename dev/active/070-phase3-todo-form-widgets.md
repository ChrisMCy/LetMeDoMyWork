# Task 070: Create TODO Form Widgets

## Phase
3 - UI Foundation & MVP

## Description
Create reusable widgets for the TODO create/edit forms.

## Steps
1. Create `lib/presentation/screens/todo/widgets/` directory
2. Implement LanguageToggle
3. Implement TemplateRow
4. Implement DateTimePicker

## Code Structure

### language_toggle.dart
```dart
import 'package:flutter/material.dart';
import '../../../../core/theme/app_colors.dart';

class LanguageToggle extends StatelessWidget {
  final String selectedLanguage;
  final ValueChanged<String> onChanged;

  const LanguageToggle({
    super.key,
    required this.selectedLanguage,
    required this.onChanged,
  });

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          'Template Language',
          style: Theme.of(context).textTheme.titleSmall,
        ),
        const SizedBox(height: 8),
        SegmentedButton<String>(
          segments: const [
            ButtonSegment(
              value: 'EN',
              label: Text('English'),
              icon: Icon(Icons.language),
            ),
            ButtonSegment(
              value: 'DE',
              label: Text('Deutsch'),
              icon: Icon(Icons.language),
            ),
          ],
          selected: {selectedLanguage},
          onSelectionChanged: (selection) {
            onChanged(selection.first);
          },
        ),
      ],
    );
  }
}
```

### template_row.dart
```dart
import 'package:flutter/material.dart';
import '../../../widgets/app_text_field.dart';

class TemplateRow extends StatelessWidget {
  final String label;
  final TextEditingController controller;
  final VoidCallback onReload;

  const TemplateRow({
    super.key,
    required this.label,
    required this.controller,
    required this.onReload,
  });

  @override
  Widget build(BuildContext context) {
    return Row(
      crossAxisAlignment: CrossAxisAlignment.end,
      children: [
        Expanded(
          child: AppTextField(
            controller: controller,
            label: label,
            validator: (v) => v?.isEmpty == true ? 'Required' : null,
          ),
        ),
        const SizedBox(width: 8),
        IconButton(
          icon: const Icon(Icons.refresh),
          tooltip: 'Reload random template',
          onPressed: onReload,
        ),
      ],
    );
  }
}
```

### date_time_picker.dart
```dart
import 'package:flutter/material.dart';
import '../../../../core/theme/app_colors.dart';

class DateTimePicker extends StatelessWidget {
  final String label;
  final TimeOfDay time;
  final DateTime? date;
  final ValueChanged<TimeOfDay> onTimeChanged;
  final ValueChanged<DateTime>? onDateChanged;
  final bool showDate;

  const DateTimePicker({
    super.key,
    required this.label,
    required this.time,
    this.date,
    required this.onTimeChanged,
    this.onDateChanged,
    this.showDate = false,
  });

  @override
  Widget build(BuildContext context) {
    return Column(
      crossAxisAlignment: CrossAxisAlignment.start,
      children: [
        Text(
          label,
          style: Theme.of(context).textTheme.titleSmall,
        ),
        const SizedBox(height: 8),
        Row(
          children: [
            // Time Picker
            Expanded(
              child: InkWell(
                onTap: () => _selectTime(context),
                borderRadius: BorderRadius.circular(8),
                child: Container(
                  padding: const EdgeInsets.all(16),
                  decoration: BoxDecoration(
                    color: AppColors.surfaceVariant,
                    borderRadius: BorderRadius.circular(8),
                  ),
                  child: Row(
                    children: [
                      const Icon(Icons.access_time),
                      const SizedBox(width: 12),
                      Text(
                        _formatTime(time),
                        style: Theme.of(context).textTheme.bodyLarge,
                      ),
                    ],
                  ),
                ),
              ),
            ),

            // Date Picker (optional)
            if (showDate && date != null) ...[
              const SizedBox(width: 16),
              Expanded(
                child: InkWell(
                  onTap: () => _selectDate(context),
                  borderRadius: BorderRadius.circular(8),
                  child: Container(
                    padding: const EdgeInsets.all(16),
                    decoration: BoxDecoration(
                      color: AppColors.surfaceVariant,
                      borderRadius: BorderRadius.circular(8),
                    ),
                    child: Row(
                      children: [
                        const Icon(Icons.calendar_today),
                        const SizedBox(width: 12),
                        Text(
                          _formatDate(date!),
                          style: Theme.of(context).textTheme.bodyLarge,
                        ),
                      ],
                    ),
                  ),
                ),
              ),
            ],
          ],
        ),
      ],
    );
  }

  Future<void> _selectTime(BuildContext context) async {
    final picked = await showTimePicker(
      context: context,
      initialTime: time,
    );
    if (picked != null) {
      onTimeChanged(picked);
    }
  }

  Future<void> _selectDate(BuildContext context) async {
    if (onDateChanged == null) return;

    final picked = await showDatePicker(
      context: context,
      initialDate: date ?? DateTime.now(),
      firstDate: DateTime.now(),
      lastDate: DateTime.now().add(const Duration(days: 365)),
    );
    if (picked != null) {
      onDateChanged!(picked);
    }
  }

  String _formatTime(TimeOfDay time) {
    final hour = time.hour.toString().padLeft(2, '0');
    final minute = time.minute.toString().padLeft(2, '0');
    return '$hour:$minute';
  }

  String _formatDate(DateTime date) {
    return '${date.day.toString().padLeft(2, '0')}.${date.month.toString().padLeft(2, '0')}.${date.year}';
  }
}
```

### name_swap_field.dart
```dart
import 'package:flutter/material.dart';
import '../../../widgets/app_text_field.dart';

class NameSwapField extends StatelessWidget {
  final TextEditingController firstNameController;
  final TextEditingController lastNameController;
  final VoidCallback onSwap;

  const NameSwapField({
    super.key,
    required this.firstNameController,
    required this.lastNameController,
    required this.onSwap,
  });

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        Expanded(
          child: AppTextField(
            controller: firstNameController,
            label: 'First Name',
          ),
        ),
        IconButton(
          icon: const Icon(Icons.swap_horiz),
          onPressed: onSwap,
          tooltip: 'Swap names',
        ),
        Expanded(
          child: AppTextField(
            controller: lastNameController,
            label: 'Last Name',
          ),
        ),
      ],
    );
  }
}
```

## Acceptance Criteria
- [ ] LanguageToggle with EN/DE options
- [ ] TemplateRow with text field and reload button
- [ ] DateTimePicker for time selection
- [ ] DateTimePicker optionally shows date picker
- [ ] NameSwapField with swap button
- [ ] All widgets follow app theme

## Dependencies
- Task 051 (AppColors)
- Task 057 (AppTextField)

## Parallel Work
Can run parallel with: Task 068, 069

## Estimated Effort
1.5 hours
