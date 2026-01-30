# Task 072: Create SMTP Config Section Widget

## Phase
3 - UI Foundation & MVP

## Description
Implement the SMTP configuration section for Settings screen.

## Steps
1. Create `lib/presentation/screens/settings/widgets/smtp_config_section.dart`
2. Implement provider dropdown
3. Implement email/password inputs
4. Add test email functionality
5. Add help button with provider-specific instructions

## Code Structure
```dart
import 'package:flutter/material.dart';
import '../../../../core/di/injection.dart';
import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_dimensions.dart';
import '../../../../domain/entities/settings.dart';
import '../../../../domain/repositories/settings_repository.dart';
import '../../../../services/smtp/smtp_config_service.dart';
import '../../../../services/smtp/email_service.dart';
import '../../../../services/storage/secure_storage_service.dart';
import '../../../widgets/app_button.dart';
import '../../../widgets/app_dialog.dart';
import '../../../widgets/app_text_field.dart';
import 'package:url_launcher/url_launcher.dart';

class SmtpConfigSection extends StatefulWidget {
  final Settings settings;
  final ValueChanged<Settings> onSettingsChanged;

  const SmtpConfigSection({
    super.key,
    required this.settings,
    required this.onSettingsChanged,
  });

  @override
  State<SmtpConfigSection> createState() => _SmtpConfigSectionState();
}

class _SmtpConfigSectionState extends State<SmtpConfigSection> {
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();

  final _settingsRepository = getIt<SettingsRepository>();
  final _secureStorage = getIt<SecureStorageService>();
  final _smtpConfigService = getIt<SmtpConfigService>();
  final _emailService = getIt<EmailService>();

  SmtpProvider _selectedProvider = SmtpProvider.gmail;
  bool _isTesting = false;
  bool _hasPassword = false;

  @override
  void initState() {
    super.initState();
    _emailController.text = widget.settings.smtpEmail ?? '';
    _selectedProvider = _smtpConfigService.detectProvider(
      widget.settings.smtpEmail ?? '',
    );
    _checkPassword();
  }

  Future<void> _checkPassword() async {
    final has = await _secureStorage.hasSmtpPassword();
    setState(() => _hasPassword = has);
  }

  @override
  void dispose() {
    _emailController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

  Future<void> _saveEmail() async {
    final email = _emailController.text.trim();
    final updated = widget.settings.copyWith(smtpEmail: email);
    await _settingsRepository.updateSettings(updated);
    widget.onSettingsChanged(updated);

    // Auto-detect provider
    setState(() {
      _selectedProvider = _smtpConfigService.detectProvider(email);
    });
  }

  Future<void> _savePassword() async {
    final password = _passwordController.text;
    if (password.isNotEmpty) {
      await _secureStorage.saveSmtpPassword(password);
      setState(() => _hasPassword = true);
      _passwordController.clear();

      ScaffoldMessenger.of(context).showSnackBar(
        const SnackBar(content: Text('Password saved securely')),
      );
    }
  }

  Future<void> _testConnection() async {
    final email = _emailController.text.trim();
    if (email.isEmpty) {
      AppDialog.showError(
        context: context,
        title: 'Error',
        message: 'Please enter your email address first.',
      );
      return;
    }

    final password = await _secureStorage.getSmtpPassword();
    if (password == null || password.isEmpty) {
      AppDialog.showError(
        context: context,
        title: 'Error',
        message: 'Please save your app password first.',
      );
      return;
    }

    setState(() => _isTesting = true);

    final result = await _emailService.testConnection(
      email: email,
      password: password,
      provider: _selectedProvider,
    );

    setState(() => _isTesting = false);

    if (result.isSuccess) {
      AppDialog.showSuccess(
        context: context,
        title: 'Success!',
        message: 'Test email sent successfully. Check your inbox.',
      );
    } else {
      AppDialog.showError(
        context: context,
        title: 'Connection Failed',
        message: result.error!,
        onRetry: _testConnection,
      );
    }
  }

  void _showHelp() {
    final helpUrl = _smtpConfigService.getHelpUrl(_selectedProvider);

    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: Text('${_getProviderName(_selectedProvider)} Setup'),
        content: Column(
          mainAxisSize: MainAxisSize.min,
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            const Text(
              'To use this app, you need to create an App Password:',
              style: TextStyle(fontWeight: FontWeight.bold),
            ),
            const SizedBox(height: 12),
            const Text('1. Enable 2-Factor Authentication on your account'),
            const Text('2. Generate an App Password'),
            const Text('3. Use that password in this app (not your regular password)'),
            if (helpUrl.isNotEmpty) ...[
              const SizedBox(height: 16),
              TextButton.icon(
                icon: const Icon(Icons.open_in_new),
                label: const Text('Open Setup Guide'),
                onPressed: () => launchUrl(Uri.parse(helpUrl)),
              ),
            ],
          ],
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('Got it'),
          ),
        ],
      ),
    );
  }

  String _getProviderName(SmtpProvider provider) {
    switch (provider) {
      case SmtpProvider.gmail:
        return 'Gmail';
      case SmtpProvider.outlook:
        return 'Outlook';
      case SmtpProvider.yahoo:
        return 'Yahoo';
      case SmtpProvider.custom:
        return 'Custom';
    }
  }

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(AppDimensions.paddingScreen),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          // Provider Selection
          DropdownButtonFormField<SmtpProvider>(
            value: _selectedProvider,
            decoration: const InputDecoration(
              labelText: 'Email Provider',
              prefixIcon: Icon(Icons.email),
            ),
            items: SmtpProvider.values.map((provider) {
              return DropdownMenuItem(
                value: provider,
                child: Text(_getProviderName(provider)),
              );
            }).toList(),
            onChanged: (value) {
              if (value != null) {
                setState(() => _selectedProvider = value);
              }
            },
          ),
          const SizedBox(height: AppDimensions.spacingMd),

          // Email
          AppTextField.email(
            controller: _emailController,
            label: 'Your Email',
            onSubmitted: (_) => _saveEmail(),
          ),
          const SizedBox(height: AppDimensions.spacingSm),
          Align(
            alignment: Alignment.centerRight,
            child: TextButton(
              onPressed: _saveEmail,
              child: const Text('Save Email'),
            ),
          ),
          const SizedBox(height: AppDimensions.spacingMd),

          // Password
          Row(
            children: [
              Expanded(
                child: AppTextField.password(
                  controller: _passwordController,
                  label: _hasPassword ? 'App Password (saved)' : 'App Password',
                  hint: _hasPassword ? '••••••••••••••••' : 'Enter app password',
                ),
              ),
              const SizedBox(width: 8),
              IconButton(
                icon: const Icon(Icons.help_outline),
                tooltip: 'What is an App Password?',
                onPressed: _showHelp,
              ),
            ],
          ),
          const SizedBox(height: AppDimensions.spacingSm),
          Align(
            alignment: Alignment.centerRight,
            child: TextButton(
              onPressed: _savePassword,
              child: const Text('Save Password'),
            ),
          ),
          const SizedBox(height: AppDimensions.spacingLg),

          // Test Button
          AppButton.secondary(
            text: 'Send Test Email',
            icon: Icons.send,
            isLoading: _isTesting,
            isFullWidth: true,
            onPressed: _testConnection,
          ),

          // Status indicator
          if (_hasPassword && _emailController.text.isNotEmpty)
            Padding(
              padding: const EdgeInsets.only(top: 12),
              child: Row(
                children: [
                  Icon(Icons.check_circle, color: AppColors.success, size: 16),
                  const SizedBox(width: 8),
                  Text(
                    'SMTP configured',
                    style: TextStyle(color: AppColors.success),
                  ),
                ],
              ),
            ),
        ],
      ),
    );
  }
}
```

## Acceptance Criteria
- [ ] Provider dropdown (Gmail, Outlook, Yahoo, Custom)
- [ ] Email input with save button
- [ ] Password input with save button (stored securely)
- [ ] Help button shows app password instructions
- [ ] Test email button sends test to self
- [ ] Success/error dialogs for test
- [ ] Status indicator when configured
- [ ] Auto-detect provider from email domain

## Dependencies
- Task 042 (SecureStorageService)
- Task 043-044 (SMTP services)
- Task 056-057 (Widgets)

## Parallel Work
Can run parallel with: Task 071

## Estimated Effort
2-3 hours
