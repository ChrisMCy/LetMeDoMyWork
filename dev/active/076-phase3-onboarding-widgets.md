# Task 076: Create Onboarding Widgets

## Phase
3 - UI Foundation & MVP

## Description
Create supporting widgets for the onboarding flow.

## Steps
1. Create `lib/presentation/screens/onboarding/widgets/` directory
2. Implement ProviderSelection widget
3. Implement SetupSuccess widget

## Code Structure

### provider_selection.dart
```dart
import 'package:flutter/material.dart';
import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_dimensions.dart';
import '../../../../services/smtp/smtp_config_service.dart';

class ProviderSelection extends StatelessWidget {
  final SmtpProvider selectedProvider;
  final ValueChanged<SmtpProvider> onProviderSelected;

  const ProviderSelection({
    super.key,
    required this.selectedProvider,
    required this.onProviderSelected,
  });

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        _buildProviderCard(
          context,
          provider: SmtpProvider.gmail,
          name: 'Gmail',
          icon: Icons.mail,
          color: Colors.red,
        ),
        const SizedBox(height: 12),
        _buildProviderCard(
          context,
          provider: SmtpProvider.outlook,
          name: 'Outlook / Hotmail',
          icon: Icons.mail,
          color: Colors.blue,
        ),
        const SizedBox(height: 12),
        _buildProviderCard(
          context,
          provider: SmtpProvider.yahoo,
          name: 'Yahoo Mail',
          icon: Icons.mail,
          color: Colors.purple,
        ),
        const SizedBox(height: 12),
        _buildProviderCard(
          context,
          provider: SmtpProvider.custom,
          name: 'Other (Custom SMTP)',
          icon: Icons.settings,
          color: Colors.grey,
        ),
      ],
    );
  }

  Widget _buildProviderCard(
    BuildContext context, {
    required SmtpProvider provider,
    required String name,
    required IconData icon,
    required Color color,
  }) {
    final isSelected = selectedProvider == provider;

    return InkWell(
      onTap: () => onProviderSelected(provider),
      borderRadius: BorderRadius.circular(AppDimensions.radiusLg),
      child: AnimatedContainer(
        duration: const Duration(milliseconds: 200),
        padding: const EdgeInsets.all(16),
        decoration: BoxDecoration(
          color: isSelected ? color.withOpacity(0.1) : AppColors.surfaceVariant,
          borderRadius: BorderRadius.circular(AppDimensions.radiusLg),
          border: Border.all(
            color: isSelected ? color : Colors.transparent,
            width: 2,
          ),
        ),
        child: Row(
          children: [
            Container(
              padding: const EdgeInsets.all(12),
              decoration: BoxDecoration(
                color: color.withOpacity(0.2),
                borderRadius: BorderRadius.circular(12),
              ),
              child: Icon(icon, color: color),
            ),
            const SizedBox(width: 16),
            Expanded(
              child: Text(
                name,
                style: Theme.of(context).textTheme.titleMedium?.copyWith(
                  fontWeight: isSelected ? FontWeight.bold : FontWeight.normal,
                ),
              ),
            ),
            if (isSelected)
              Icon(Icons.check_circle, color: color),
          ],
        ),
      ),
    );
  }
}
```

### setup_success.dart
```dart
import 'package:flutter/material.dart';
import '../../../../core/theme/app_colors.dart';
import '../../../../core/theme/app_dimensions.dart';
import '../../../widgets/app_button.dart';

class SetupSuccess extends StatelessWidget {
  final VoidCallback onContinue;

  const SetupSuccess({
    super.key,
    required this.onContinue,
  });

  @override
  Widget build(BuildContext context) {
    return Padding(
      padding: const EdgeInsets.all(AppDimensions.paddingScreen),
      child: Column(
        mainAxisAlignment: MainAxisAlignment.center,
        children: [
          const Spacer(),

          // Success Icon with animation
          TweenAnimationBuilder<double>(
            tween: Tween(begin: 0, end: 1),
            duration: const Duration(milliseconds: 600),
            curve: Curves.elasticOut,
            builder: (context, value, child) {
              return Transform.scale(
                scale: value,
                child: child,
              );
            },
            child: Container(
              padding: const EdgeInsets.all(24),
              decoration: BoxDecoration(
                color: AppColors.success.withOpacity(0.1),
                shape: BoxShape.circle,
              ),
              child: Icon(
                Icons.check_circle,
                size: 80,
                color: AppColors.success,
              ),
            ),
          ),
          const SizedBox(height: 32),

          Text(
            'You\'re all set!',
            style: Theme.of(context).textTheme.headlineMedium?.copyWith(
              fontWeight: FontWeight.bold,
            ),
          ),
          const SizedBox(height: 16),

          Text(
            'Your email is configured and ready to send follow-ups automatically.',
            style: Theme.of(context).textTheme.bodyLarge?.copyWith(
              color: AppColors.onSurfaceVariant,
            ),
            textAlign: TextAlign.center,
          ),
          const SizedBox(height: 8),

          Text(
            'Check your inbox for a test email.',
            style: Theme.of(context).textTheme.bodyMedium?.copyWith(
              color: AppColors.onSurfaceVariant,
            ),
            textAlign: TextAlign.center,
          ),

          const Spacer(),

          // Tips
          Container(
            padding: const EdgeInsets.all(16),
            decoration: BoxDecoration(
              color: AppColors.primary.withOpacity(0.1),
              borderRadius: BorderRadius.circular(12),
            ),
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Row(
                  children: [
                    Icon(Icons.lightbulb_outline, color: AppColors.primary),
                    const SizedBox(width: 8),
                    Text(
                      'Quick Tip',
                      style: TextStyle(
                        fontWeight: FontWeight.bold,
                        color: AppColors.primary,
                      ),
                    ),
                  ],
                ),
                const SizedBox(height: 8),
                const Text(
                  'Create your first TODO by tapping the + button on the main screen.',
                ),
              ],
            ),
          ),
          const SizedBox(height: 32),

          AppButton.primary(
            text: 'Start Using App',
            isFullWidth: true,
            onPressed: onContinue,
          ),
        ],
      ),
    );
  }
}
```

### credentials_form.dart (Optional)
```dart
import 'package:flutter/material.dart';
import '../../../widgets/app_text_field.dart';

class CredentialsForm extends StatelessWidget {
  final TextEditingController emailController;
  final TextEditingController passwordController;
  final VoidCallback? onHelpPressed;

  const CredentialsForm({
    super.key,
    required this.emailController,
    required this.passwordController,
    this.onHelpPressed,
  });

  @override
  Widget build(BuildContext context) {
    return Column(
      children: [
        AppTextField.email(
          controller: emailController,
          label: 'Email Address',
        ),
        const SizedBox(height: 16),
        AppTextField.password(
          controller: passwordController,
          label: 'App Password',
        ),
        if (onHelpPressed != null)
          TextButton.icon(
            icon: const Icon(Icons.help_outline, size: 18),
            label: const Text('How to get an App Password?'),
            onPressed: onHelpPressed,
          ),
      ],
    );
  }
}
```

## Acceptance Criteria
- [ ] ProviderSelection shows all providers with visual cards
- [ ] Selected provider has border highlight
- [ ] SetupSuccess shows animated checkmark
- [ ] SetupSuccess has tip for next steps
- [ ] Consistent styling with app theme

## Dependencies
- Task 051 (AppColors)
- Task 053 (AppDimensions)
- Task 056-057 (Widgets)

## Parallel Work
Can run parallel with: Task 074, 075

## Estimated Effort
1.5 hours
