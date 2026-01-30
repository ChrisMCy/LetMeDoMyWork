# Task 086: Create Export/Import UI

## Phase
4 - Advanced Features

## Description
Add export/import functionality to Settings screen.

## Steps
1. Add Export/Import section to Settings screen
2. Create ExportImportDialog
3. Handle user confirmation for import

## Code Structure

### Add to settings_screen.dart
```dart
// Add in Settings screen after Templates section
const Divider(height: 32),

_buildSectionHeader('Backup & Restore'),

SettingTile(
  icon: Icons.upload,
  title: 'Export Data',
  subtitle: 'Save all data to a JSON file',
  onTap: () => _showExportDialog(),
),

SettingTile(
  icon: Icons.download,
  title: 'Import Data',
  subtitle: 'Restore from a backup file',
  onTap: () => _showImportDialog(),
),
```

### export_import_dialog.dart
```dart
import 'package:flutter/material.dart';
import 'package:share_plus/share_plus.dart';
import '../../../core/di/injection.dart';
import '../../../core/theme/app_colors.dart';
import '../../../services/backup/export_service.dart';
import '../../../services/backup/import_service.dart';
import '../../widgets/app_button.dart';
import '../../widgets/app_dialog.dart';

class ExportDialog extends StatefulWidget {
  const ExportDialog({super.key});

  @override
  State<ExportDialog> createState() => _ExportDialogState();
}

class _ExportDialogState extends State<ExportDialog> {
  final _exportService = getIt<ExportService>();
  bool _isExporting = false;
  String? _exportPath;
  String? _error;

  Future<void> _exportToFile() async {
    setState(() {
      _isExporting = true;
      _error = null;
    });

    final result = await _exportService.exportToFile();

    setState(() {
      _isExporting = false;
      if (result.isSuccess) {
        _exportPath = result.data;
      } else {
        _error = result.error;
      }
    });
  }

  Future<void> _shareExport() async {
    final result = await _exportService.exportToFile();
    if (result.isSuccess) {
      await Share.shareXFiles(
        [XFile(result.data!)],
        subject: 'LetMeDoMyWork Backup',
      );
    }
  }

  @override
  Widget build(BuildContext context) {
    return AlertDialog(
      title: const Text('Export Data'),
      content: Column(
        mainAxisSize: MainAxisSize.min,
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          const Text(
            'Export all your TODOs, sent emails, and settings to a backup file.',
          ),
          const SizedBox(height: 16),

          if (_isExporting) ...[
            const Center(child: CircularProgressIndicator()),
            const SizedBox(height: 8),
            const Text('Exporting...', textAlign: TextAlign.center),
          ] else if (_exportPath != null) ...[
            Row(
              children: [
                Icon(Icons.check_circle, color: AppColors.success),
                const SizedBox(width: 8),
                const Expanded(
                  child: Text('Export successful!'),
                ),
              ],
            ),
            const SizedBox(height: 8),
            Text(
              'Saved to: $_exportPath',
              style: TextStyle(
                fontSize: 12,
                color: AppColors.onSurfaceVariant,
              ),
            ),
          ] else if (_error != null) ...[
            Row(
              children: [
                Icon(Icons.error, color: AppColors.error),
                const SizedBox(width: 8),
                Expanded(
                  child: Text(
                    _error!,
                    style: TextStyle(color: AppColors.error),
                  ),
                ),
              ],
            ),
          ],
        ],
      ),
      actions: [
        TextButton(
          onPressed: () => Navigator.pop(context),
          child: Text(_exportPath != null ? 'Done' : 'Cancel'),
        ),
        if (_exportPath == null && !_isExporting) ...[
          TextButton.icon(
            icon: const Icon(Icons.share),
            label: const Text('Share'),
            onPressed: _shareExport,
          ),
          AppButton.primary(
            text: 'Save to Device',
            onPressed: _exportToFile,
          ),
        ],
      ],
    );
  }
}

class ImportDialog extends StatefulWidget {
  const ImportDialog({super.key});

  @override
  State<ImportDialog> createState() => _ImportDialogState();
}

class _ImportDialogState extends State<ImportDialog> {
  final _importService = getIt<ImportService>();

  bool _isLoading = false;
  ImportValidationResult? _validation;
  String? _jsonContent;
  String? _error;
  bool _isImporting = false;

  Future<void> _pickFile() async {
    setState(() {
      _isLoading = true;
      _error = null;
    });

    final result = await _importService.pickAndValidateFile();

    setState(() {
      _isLoading = false;
      if (result.isSuccess) {
        _jsonContent = result.data!.$1;
        _validation = result.data!.$2;
      } else {
        _error = result.error;
      }
    });
  }

  Future<void> _confirmImport() async {
    final confirmed = await AppDialog.showConfirmation(
      context: context,
      title: 'Replace All Data?',
      message: 'This will delete all current data and replace it with the backup. This cannot be undone.',
      isDangerous: true,
      confirmText: 'Import',
    );

    if (confirmed && _jsonContent != null) {
      setState(() => _isImporting = true);

      final result = await _importService.importData(_jsonContent!);

      setState(() => _isImporting = false);

      if (result.isSuccess) {
        Navigator.pop(context, true);
        AppDialog.showSuccess(
          context: context,
          title: 'Import Complete',
          message: 'Your data has been restored successfully.',
        );
      } else {
        setState(() => _error = result.error);
      }
    }
  }

  @override
  Widget build(BuildContext context) {
    return AlertDialog(
      title: const Text('Import Data'),
      content: Column(
        mainAxisSize: MainAxisSize.min,
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          if (_validation == null && !_isLoading) ...[
            const Text(
              'Select a backup file to restore your data. This will replace all current data.',
            ),
            const SizedBox(height: 8),
            Text(
              'Warning: This cannot be undone!',
              style: TextStyle(
                color: AppColors.error,
                fontWeight: FontWeight.bold,
              ),
            ),
          ] else if (_isLoading) ...[
            const Center(child: CircularProgressIndicator()),
            const SizedBox(height: 8),
            const Text('Reading file...', textAlign: TextAlign.center),
          ] else if (_validation != null) ...[
            Card(
              child: Padding(
                padding: const EdgeInsets.all(16),
                child: Column(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    Row(
                      children: [
                        Icon(Icons.check_circle, color: AppColors.success),
                        const SizedBox(width: 8),
                        const Text(
                          'Valid backup file',
                          style: TextStyle(fontWeight: FontWeight.bold),
                        ),
                      ],
                    ),
                    const SizedBox(height: 12),
                    _buildInfoRow('TODOs', '${_validation!.todoCount}'),
                    _buildInfoRow('Sent Emails', '${_validation!.sentEmailCount}'),
                    if (_validation!.exportedAt != null)
                      _buildInfoRow(
                        'Exported',
                        _formatDate(_validation!.exportedAt!),
                      ),
                  ],
                ),
              ),
            ),
          ],

          if (_error != null) ...[
            const SizedBox(height: 16),
            Row(
              children: [
                Icon(Icons.error, color: AppColors.error),
                const SizedBox(width: 8),
                Expanded(
                  child: Text(
                    _error!,
                    style: TextStyle(color: AppColors.error),
                  ),
                ),
              ],
            ),
          ],
        ],
      ),
      actions: [
        TextButton(
          onPressed: () => Navigator.pop(context),
          child: const Text('Cancel'),
        ),
        if (_validation == null && !_isLoading)
          AppButton.primary(
            text: 'Select File',
            onPressed: _pickFile,
          ),
        if (_validation != null && !_isImporting)
          AppButton.danger(
            text: 'Import',
            isLoading: _isImporting,
            onPressed: _confirmImport,
          ),
      ],
    );
  }

  Widget _buildInfoRow(String label, String value) {
    return Padding(
      padding: const EdgeInsets.symmetric(vertical: 2),
      child: Row(
        mainAxisAlignment: MainAxisAlignment.spaceBetween,
        children: [
          Text(label),
          Text(value, style: const TextStyle(fontWeight: FontWeight.bold)),
        ],
      ),
    );
  }

  String _formatDate(DateTime date) {
    return '${date.day}/${date.month}/${date.year} ${date.hour}:${date.minute.toString().padLeft(2, '0')}';
  }
}
```

## Usage in Settings Screen
```dart
Future<void> _showExportDialog() async {
  await showDialog(
    context: context,
    builder: (context) => const ExportDialog(),
  );
}

Future<void> _showImportDialog() async {
  final imported = await showDialog<bool>(
    context: context,
    builder: (context) => const ImportDialog(),
  );

  if (imported == true) {
    // Reload settings
    _loadSettings();
  }
}
```

## Acceptance Criteria
- [ ] Export dialog with save/share options
- [ ] Export shows progress and success
- [ ] Import dialog with file picker
- [ ] Import shows preview (counts, date)
- [ ] Dangerous confirmation before import
- [ ] Success/error feedback
- [ ] Settings reload after import

## Dependencies
- Task 084-085 (Export/Import services)
- Task 059 (AppDialog)
- Task 071 (Settings screen)

## Parallel Work
Must run after: Task 084, 085

## Estimated Effort
2 hours
