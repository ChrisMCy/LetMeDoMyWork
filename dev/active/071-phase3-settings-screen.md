# Task 071: Create Settings Screen

## Phase
3 - UI Foundation & MVP

## Description
Implement the settings screen with SMTP configuration and app settings.

## Steps
1. Create `lib/presentation/screens/settings/settings_screen.dart`
2. Implement SMTP configuration section
3. Implement app settings (max follow-ups, randomize minutes)
4. Add template management navigation

## Code Structure
```dart
import 'package:flutter/material.dart';
import 'package:flutter_bloc/flutter_bloc.dart';
import '../../../core/di/injection.dart';
import '../../../core/navigation/routes.dart';
import '../../../core/theme/app_dimensions.dart';
import '../../../domain/entities/settings.dart';
import '../../../domain/repositories/settings_repository.dart';
import '../../widgets/app_button.dart';
import '../../widgets/app_dialog.dart';
import '../../widgets/loading_indicator.dart';
import 'widgets/smtp_config_section.dart';
import 'widgets/setting_tile.dart';

class SettingsScreen extends StatefulWidget {
  const SettingsScreen({super.key});

  @override
  State<SettingsScreen> createState() => _SettingsScreenState();
}

class _SettingsScreenState extends State<SettingsScreen> {
  final _settingsRepository = getIt<SettingsRepository>();

  bool _isLoading = true;
  Settings? _settings;

  @override
  void initState() {
    super.initState();
    _loadSettings();
  }

  Future<void> _loadSettings() async {
    final settings = await _settingsRepository.getSettings();
    setState(() {
      _settings = settings;
      _isLoading = false;
    });
  }

  Future<void> _updateSetting(Settings Function(Settings) updater) async {
    if (_settings == null) return;

    final updated = updater(_settings!);
    await _settingsRepository.updateSettings(updated);
    setState(() => _settings = updated);
  }

  @override
  Widget build(BuildContext context) {
    if (_isLoading) {
      return Scaffold(
        appBar: AppBar(title: const Text('Settings')),
        body: const LoadingView(),
      );
    }

    return Scaffold(
      appBar: AppBar(title: const Text('Settings')),
      body: ListView(
        children: [
          // SMTP Configuration Section
          _buildSectionHeader('Email Configuration'),
          SmtpConfigSection(
            settings: _settings!,
            onSettingsChanged: (updated) {
              setState(() => _settings = updated);
            },
          ),

          const Divider(height: 32),

          // App Settings
          _buildSectionHeader('App Settings'),

          // Max Follow-ups
          SettingTile(
            icon: Icons.repeat,
            title: 'Max Follow-ups',
            subtitle: '${_settings!.maxFollowUps} emails per TODO',
            onTap: () => _showMaxFollowUpsDialog(),
          ),

          // Randomize Minutes
          SettingTile(
            icon: Icons.shuffle,
            title: 'Send Time Randomization',
            subtitle: '± ${_settings!.randomizeMinutes} minutes',
            onTap: () => _showRandomizeDialog(),
          ),

          const Divider(height: 32),

          // Template Management
          _buildSectionHeader('Templates'),

          SettingTile(
            icon: Icons.article,
            title: 'Manage Templates',
            subtitle: 'Customize email subjects and bodies',
            trailing: const Icon(Icons.chevron_right),
            onTap: () => Navigator.pushNamed(context, Routes.templateManagement),
          ),

          const Divider(height: 32),

          // About
          _buildSectionHeader('About'),

          SettingTile(
            icon: Icons.info_outline,
            title: 'About LetMeDoMyWork',
            subtitle: 'Version 1.0.0',
            onTap: () => _showAboutDialog(),
          ),

          const SizedBox(height: 32),
        ],
      ),
    );
  }

  Widget _buildSectionHeader(String title) {
    return Padding(
      padding: const EdgeInsets.fromLTRB(16, 16, 16, 8),
      child: Text(
        title,
        style: Theme.of(context).textTheme.titleMedium?.copyWith(
          color: Theme.of(context).colorScheme.primary,
        ),
      ),
    );
  }

  Future<void> _showMaxFollowUpsDialog() async {
    int value = _settings!.maxFollowUps;

    final result = await showDialog<int>(
      context: context,
      builder: (context) => StatefulBuilder(
        builder: (context, setDialogState) => AlertDialog(
          title: const Text('Max Follow-ups'),
          content: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              Text('Maximum emails to send per TODO'),
              const SizedBox(height: 16),
              Row(
                mainAxisAlignment: MainAxisAlignment.center,
                children: [
                  IconButton(
                    icon: const Icon(Icons.remove),
                    onPressed: value > 1
                        ? () => setDialogState(() => value--)
                        : null,
                  ),
                  Text(
                    '$value',
                    style: Theme.of(context).textTheme.headlineMedium,
                  ),
                  IconButton(
                    icon: const Icon(Icons.add),
                    onPressed: value < 30
                        ? () => setDialogState(() => value++)
                        : null,
                  ),
                ],
              ),
            ],
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.pop(context),
              child: const Text('Cancel'),
            ),
            TextButton(
              onPressed: () => Navigator.pop(context, value),
              child: const Text('Save'),
            ),
          ],
        ),
      ),
    );

    if (result != null) {
      await _updateSetting((s) => s.copyWith(maxFollowUps: result));
    }
  }

  Future<void> _showRandomizeDialog() async {
    int value = _settings!.randomizeMinutes;

    final result = await showDialog<int>(
      context: context,
      builder: (context) => StatefulBuilder(
        builder: (context, setDialogState) => AlertDialog(
          title: const Text('Send Time Randomization'),
          content: Column(
            mainAxisSize: MainAxisSize.min,
            children: [
              const Text('Randomize send time by ± this many minutes'),
              const SizedBox(height: 16),
              Slider(
                value: value.toDouble(),
                min: 0,
                max: 120,
                divisions: 24,
                label: '$value min',
                onChanged: (v) => setDialogState(() => value = v.round()),
              ),
              Text('± $value minutes'),
            ],
          ),
          actions: [
            TextButton(
              onPressed: () => Navigator.pop(context),
              child: const Text('Cancel'),
            ),
            TextButton(
              onPressed: () => Navigator.pop(context, value),
              child: const Text('Save'),
            ),
          ],
        ),
      ),
    );

    if (result != null) {
      await _updateSetting((s) => s.copyWith(randomizeMinutes: result));
    }
  }

  void _showAboutDialog() {
    showAboutDialog(
      context: context,
      applicationName: 'LetMeDoMyWork',
      applicationVersion: '1.0.0',
      applicationLegalese: '© 2024 LetMeDoMyWork',
      children: [
        const SizedBox(height: 16),
        const Text('Automated follow-up email reminder app.'),
      ],
    );
  }
}
```

## Acceptance Criteria
- [ ] SMTP configuration section with provider selection
- [ ] Test email button
- [ ] Max follow-ups setting (1-30)
- [ ] Randomize minutes setting (0-120)
- [ ] Template management navigation
- [ ] About dialog
- [ ] Settings persist on change

## Dependencies
- Task 028 (SettingsRepository)
- Task 043-044 (SMTP services)
- Task 072 (SmtpConfigSection widget)

## Parallel Work
Can run parallel with: Task 072

## Estimated Effort
2-3 hours
