# Task 083: Create Template Management Screen

## Phase
4 - Advanced Features

## Description
Implement the template management screen with reordering and editing.

## Steps
1. Create `lib/presentation/screens/settings/template_management_screen.dart`
2. Implement template list with drag-drop reordering
3. Add/edit/delete template functionality

## Code Structure
```dart
import 'package:flutter/material.dart';
import '../../../core/di/injection.dart';
import '../../../core/theme/app_colors.dart';
import '../../../core/theme/app_dimensions.dart';
import '../../../domain/entities/settings.dart';
import '../../../domain/repositories/settings_repository.dart';
import '../../widgets/app_button.dart';
import '../../widgets/app_dialog.dart';

class TemplateManagementScreen extends StatefulWidget {
  const TemplateManagementScreen({super.key});

  @override
  State<TemplateManagementScreen> createState() => _TemplateManagementScreenState();
}

class _TemplateManagementScreenState extends State<TemplateManagementScreen>
    with SingleTickerProviderStateMixin {
  late TabController _tabController;
  final _settingsRepository = getIt<SettingsRepository>();

  Settings? _settings;
  bool _isLoading = true;
  String _selectedLanguage = 'EN';
  bool _isSubject = true;

  List<String> _currentTemplates = [];

  @override
  void initState() {
    super.initState();
    _tabController = TabController(length: 2, vsync: this);
    _tabController.addListener(_onTabChanged);
    _loadSettings();
  }

  @override
  void dispose() {
    _tabController.dispose();
    super.dispose();
  }

  void _onTabChanged() {
    setState(() {
      _isSubject = _tabController.index == 0;
      _updateCurrentTemplates();
    });
  }

  Future<void> _loadSettings() async {
    final settings = await _settingsRepository.getSettings();
    setState(() {
      _settings = settings;
      _isLoading = false;
      _updateCurrentTemplates();
    });
  }

  void _updateCurrentTemplates() {
    if (_settings == null) return;

    if (_isSubject) {
      _currentTemplates = _selectedLanguage == 'EN'
          ? List.from(_settings!.subjectTemplatesEn)
          : List.from(_settings!.subjectTemplatesDe);
    } else {
      _currentTemplates = _selectedLanguage == 'EN'
          ? List.from(_settings!.textTemplatesEn)
          : List.from(_settings!.textTemplatesDe);
    }
  }

  Future<void> _saveTemplates() async {
    if (_settings == null) return;

    Settings updated;
    if (_isSubject) {
      updated = _selectedLanguage == 'EN'
          ? _settings!.copyWith(subjectTemplatesEn: _currentTemplates)
          : _settings!.copyWith(subjectTemplatesDe: _currentTemplates);
    } else {
      updated = _selectedLanguage == 'EN'
          ? _settings!.copyWith(textTemplatesEn: _currentTemplates)
          : _settings!.copyWith(textTemplatesDe: _currentTemplates);
    }

    await _settingsRepository.updateSettings(updated);
    setState(() => _settings = updated);

    ScaffoldMessenger.of(context).showSnackBar(
      const SnackBar(content: Text('Templates saved')),
    );
  }

  void _onReorder(int oldIndex, int newIndex) {
    setState(() {
      if (newIndex > oldIndex) newIndex--;
      final item = _currentTemplates.removeAt(oldIndex);
      _currentTemplates.insert(newIndex, item);
    });
  }

  Future<void> _addTemplate() async {
    final result = await _showEditDialog(null);
    if (result != null && result.isNotEmpty) {
      setState(() {
        _currentTemplates.add(result);
      });
    }
  }

  Future<void> _editTemplate(int index) async {
    final result = await _showEditDialog(_currentTemplates[index]);
    if (result != null) {
      setState(() {
        _currentTemplates[index] = result;
      });
    }
  }

  Future<void> _deleteTemplate(int index) async {
    if (_currentTemplates.length <= 1) {
      AppDialog.showInfo(
        context: context,
        title: 'Cannot Delete',
        message: 'You must have at least one template.',
      );
      return;
    }

    final confirmed = await AppDialog.showConfirmation(
      context: context,
      title: 'Delete Template?',
      message: 'This will permanently delete this template.',
      isDangerous: true,
    );

    if (confirmed) {
      setState(() {
        _currentTemplates.removeAt(index);
      });
    }
  }

  Future<String?> _showEditDialog(String? initialValue) async {
    final controller = TextEditingController(text: initialValue);

    return showDialog<String>(
      context: context,
      builder: (context) => AlertDialog(
        title: Text(initialValue == null ? 'Add Template' : 'Edit Template'),
        content: TextField(
          controller: controller,
          maxLines: _isSubject ? 2 : 6,
          decoration: InputDecoration(
            hintText: _isSubject
                ? 'Enter subject template...'
                : 'Enter email body template...',
            helperText: 'Use placeholders: {Vorname}, {InitialSubject}, etc.',
          ),
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('Cancel'),
          ),
          TextButton(
            onPressed: () => Navigator.pop(context, controller.text),
            child: const Text('Save'),
          ),
        ],
      ),
    );
  }

  @override
  Widget build(BuildContext context) {
    if (_isLoading) {
      return Scaffold(
        appBar: AppBar(title: const Text('Templates')),
        body: const Center(child: CircularProgressIndicator()),
      );
    }

    return Scaffold(
      appBar: AppBar(
        title: const Text('Templates'),
        actions: [
          TextButton(
            onPressed: _saveTemplates,
            child: const Text('Save'),
          ),
        ],
        bottom: TabBar(
          controller: _tabController,
          tabs: const [
            Tab(text: 'Subjects'),
            Tab(text: 'Bodies'),
          ],
        ),
      ),
      body: Column(
        children: [
          // Language Toggle
          Padding(
            padding: const EdgeInsets.all(16),
            child: SegmentedButton<String>(
              segments: const [
                ButtonSegment(value: 'EN', label: Text('English')),
                ButtonSegment(value: 'DE', label: Text('Deutsch')),
              ],
              selected: {_selectedLanguage},
              onSelectionChanged: (selection) {
                setState(() {
                  _selectedLanguage = selection.first;
                  _updateCurrentTemplates();
                });
              },
            ),
          ),

          // Template List
          Expanded(
            child: ReorderableListView.builder(
              padding: const EdgeInsets.symmetric(horizontal: 16),
              itemCount: _currentTemplates.length,
              onReorder: _onReorder,
              itemBuilder: (context, index) {
                return _buildTemplateItem(index);
              },
            ),
          ),
        ],
      ),
      floatingActionButton: FloatingActionButton(
        onPressed: _addTemplate,
        child: const Icon(Icons.add),
      ),
    );
  }

  Widget _buildTemplateItem(int index) {
    return Card(
      key: ValueKey('template_$index'),
      margin: const EdgeInsets.only(bottom: 8),
      child: ListTile(
        leading: ReorderableDragStartListener(
          index: index,
          child: const Icon(Icons.drag_handle),
        ),
        title: Text(
          _currentTemplates[index],
          maxLines: 2,
          overflow: TextOverflow.ellipsis,
        ),
        subtitle: Text('Template ${index + 1}'),
        trailing: Row(
          mainAxisSize: MainAxisSize.min,
          children: [
            IconButton(
              icon: const Icon(Icons.edit),
              onPressed: () => _editTemplate(index),
            ),
            IconButton(
              icon: const Icon(Icons.delete),
              onPressed: () => _deleteTemplate(index),
            ),
          ],
        ),
      ),
    );
  }
}
```

## Acceptance Criteria
- [ ] Tab bar for Subjects/Bodies
- [ ] Language toggle (EN/DE)
- [ ] Reorderable list with drag handles
- [ ] Edit template dialog
- [ ] Add new template via FAB
- [ ] Delete with confirmation
- [ ] Prevent deleting last template
- [ ] Save button persists changes
- [ ] Placeholder help text in edit dialog

## Dependencies
- Task 028 (SettingsRepository)
- Task 059 (AppDialog)

## Parallel Work
Can run parallel with: Task 080-082

## Estimated Effort
3-4 hours
