# Task 075: Create SMTP Setup Wizard

## Phase
3 - UI Foundation & MVP

## Description
Implement the step-by-step SMTP setup wizard for first launch.

## Steps
1. Create `lib/presentation/screens/onboarding/smtp_setup_wizard.dart`
2. Implement multi-step wizard
3. Step 1: Provider selection
4. Step 2: Credentials input
5. Step 3: Test connection
6. Step 4: Success confirmation

## Code Structure
```dart
import 'package:flutter/material.dart';
import '../../../core/di/injection.dart';
import '../../../core/navigation/routes.dart';
import '../../../core/theme/app_colors.dart';
import '../../../core/theme/app_dimensions.dart';
import '../../../domain/repositories/settings_repository.dart';
import '../../../services/smtp/smtp_config_service.dart';
import '../../../services/smtp/email_service.dart';
import '../../../services/storage/secure_storage_service.dart';
import '../../widgets/app_button.dart';
import '../../widgets/app_text_field.dart';
import 'widgets/provider_selection.dart';
import 'widgets/setup_success.dart';

class SmtpSetupWizard extends StatefulWidget {
  const SmtpSetupWizard({super.key});

  @override
  State<SmtpSetupWizard> createState() => _SmtpSetupWizardState();
}

class _SmtpSetupWizardState extends State<SmtpSetupWizard> {
  final _pageController = PageController();
  final _emailController = TextEditingController();
  final _passwordController = TextEditingController();

  final _settingsRepository = getIt<SettingsRepository>();
  final _secureStorage = getIt<SecureStorageService>();
  final _smtpConfigService = getIt<SmtpConfigService>();
  final _emailService = getIt<EmailService>();

  int _currentStep = 0;
  SmtpProvider _selectedProvider = SmtpProvider.gmail;
  bool _isTesting = false;
  String? _testError;

  @override
  void dispose() {
    _pageController.dispose();
    _emailController.dispose();
    _passwordController.dispose();
    super.dispose();
  }

  void _nextStep() {
    if (_currentStep < 3) {
      _pageController.nextPage(
        duration: const Duration(milliseconds: 300),
        curve: Curves.easeInOut,
      );
      setState(() => _currentStep++);
    }
  }

  void _previousStep() {
    if (_currentStep > 0) {
      _pageController.previousPage(
        duration: const Duration(milliseconds: 300),
        curve: Curves.easeInOut,
      );
      setState(() => _currentStep--);
    }
  }

  Future<void> _testAndSave() async {
    setState(() {
      _isTesting = true;
      _testError = null;
    });

    final email = _emailController.text.trim();
    final password = _passwordController.text;

    // Test connection
    final result = await _emailService.testConnection(
      email: email,
      password: password,
      provider: _selectedProvider,
    );

    if (result.isFailure) {
      setState(() {
        _isTesting = false;
        _testError = result.error;
      });
      return;
    }

    // Save credentials
    final settings = await _settingsRepository.getSettings();
    await _settingsRepository.updateSettings(
      settings.copyWith(smtpEmail: email),
    );
    await _secureStorage.saveSmtpPassword(password);

    setState(() => _isTesting = false);
    _nextStep();
  }

  void _finishSetup() {
    Navigator.pushReplacementNamed(context, Routes.main);
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(
        title: const Text('Email Setup'),
        leading: _currentStep > 0 && _currentStep < 3
            ? IconButton(
                icon: const Icon(Icons.arrow_back),
                onPressed: _previousStep,
              )
            : null,
        automaticallyImplyLeading: false,
      ),
      body: Column(
        children: [
          // Progress Indicator
          LinearProgressIndicator(
            value: (_currentStep + 1) / 4,
            backgroundColor: AppColors.surfaceVariant,
          ),

          // Step Content
          Expanded(
            child: PageView(
              controller: _pageController,
              physics: const NeverScrollableScrollPhysics(),
              children: [
                _buildProviderStep(),
                _buildCredentialsStep(),
                _buildTestStep(),
                _buildSuccessStep(),
              ],
            ),
          ),
        ],
      ),
    );
  }

  Widget _buildProviderStep() {
    return Padding(
      padding: const EdgeInsets.all(AppDimensions.paddingScreen),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            'Select your email provider',
            style: Theme.of(context).textTheme.headlineSmall,
          ),
          const SizedBox(height: 8),
          Text(
            'We\'ll configure the settings automatically',
            style: Theme.of(context).textTheme.bodyMedium?.copyWith(
              color: AppColors.onSurfaceVariant,
            ),
          ),
          const SizedBox(height: 32),

          ProviderSelection(
            selectedProvider: _selectedProvider,
            onProviderSelected: (provider) {
              setState(() => _selectedProvider = provider);
            },
          ),

          const Spacer(),

          AppButton.primary(
            text: 'Continue',
            isFullWidth: true,
            onPressed: _nextStep,
          ),
        ],
      ),
    );
  }

  Widget _buildCredentialsStep() {
    return Padding(
      padding: const EdgeInsets.all(AppDimensions.paddingScreen),
      child: Column(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Text(
            'Enter your credentials',
            style: Theme.of(context).textTheme.headlineSmall,
          ),
          const SizedBox(height: 8),
          Text(
            'Use an App Password, not your regular password',
            style: Theme.of(context).textTheme.bodyMedium?.copyWith(
              color: AppColors.onSurfaceVariant,
            ),
          ),
          const SizedBox(height: 32),

          AppTextField.email(
            controller: _emailController,
            label: 'Email Address',
          ),
          const SizedBox(height: 16),

          AppTextField.password(
            controller: _passwordController,
            label: 'App Password',
          ),

          TextButton.icon(
            icon: const Icon(Icons.help_outline, size: 18),
            label: const Text('How to get an App Password?'),
            onPressed: () => _showHelpDialog(),
          ),

          const Spacer(),

          AppButton.primary(
            text: 'Test Connection',
            isFullWidth: true,
            onPressed: _emailController.text.isNotEmpty &&
                    _passwordController.text.isNotEmpty
                ? _testAndSave
                : null,
          ),
        ],
      ),
    );
  }

  Widget _buildTestStep() {
    return Padding(
      padding: const EdgeInsets.all(AppDimensions.paddingScreen),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          if (_isTesting) ...[
            const CircularProgressIndicator(),
            const SizedBox(height: 24),
            const Text('Testing connection...'),
            const SizedBox(height: 8),
            Text(
              'Sending test email to ${_emailController.text}',
              style: TextStyle(color: AppColors.onSurfaceVariant),
            ),
          ] else if (_testError != null) ...[
            Icon(Icons.error_outline, size: 64, color: AppColors.error),
            const SizedBox(height: 24),
            Text(
              'Connection Failed',
              style: Theme.of(context).textTheme.headlineSmall,
            ),
            const SizedBox(height: 8),
            Text(
              _testError!,
              style: TextStyle(color: AppColors.error),
              textAlign: TextAlign.center,
            ),
            const SizedBox(height: 32),
            AppButton.primary(
              text: 'Try Again',
              onPressed: () {
                setState(() => _testError = null);
                _previousStep();
              },
            ),
          ],
        ],
      ),
    );
  }

  Widget _buildSuccessStep() {
    return SetupSuccess(
      onContinue: _finishSetup,
    );
  }

  void _showHelpDialog() {
    final helpUrl = _smtpConfigService.getHelpUrl(_selectedProvider);
    showDialog(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('App Password Setup'),
        content: const Text(
          '1. Go to your email provider\'s security settings\n'
          '2. Enable 2-Factor Authentication\n'
          '3. Generate an App Password\n'
          '4. Use that password here',
        ),
        actions: [
          if (helpUrl.isNotEmpty)
            TextButton(
              onPressed: () {
                // Launch URL
              },
              child: const Text('Open Guide'),
            ),
          TextButton(
            onPressed: () => Navigator.pop(context),
            child: const Text('Got it'),
          ),
        ],
      ),
    );
  }
}
```

## Acceptance Criteria
- [ ] Step 1: Provider selection with visual cards
- [ ] Step 2: Email and password input
- [ ] Step 3: Testing with loading indicator
- [ ] Step 4: Success confirmation
- [ ] Back navigation between steps
- [ ] Progress indicator
- [ ] Help dialog for app password
- [ ] Error handling with retry option
- [ ] Credentials saved on success

## Dependencies
- Task 042-044 (Storage and SMTP services)
- Task 056-057 (Widgets)
- Task 076-077 (Sub-widgets)

## Parallel Work
Can run parallel with: Task 074

## Estimated Effort
3-4 hours
