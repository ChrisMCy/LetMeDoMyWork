# Task 074: Create Welcome Screen

## Phase
3 - UI Foundation & MVP

## Description
Implement the first launch welcome screen.

## Steps
1. Create `lib/presentation/screens/onboarding/welcome_screen.dart`
2. Add app branding and description
3. Add "Get Started" button
4. Add "Skip for now" option

## Code Structure
```dart
import 'package:flutter/material.dart';
import '../../../core/navigation/routes.dart';
import '../../../core/theme/app_colors.dart';
import '../../../core/theme/app_dimensions.dart';
import '../../../core/theme/app_text_styles.dart';
import '../../widgets/app_button.dart';

class WelcomeScreen extends StatelessWidget {
  const WelcomeScreen({super.key});

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: SafeArea(
        child: Padding(
          padding: const EdgeInsets.all(AppDimensions.paddingScreen * 2),
          child: Column(
            mainAxisAlignment: MainAxisAlignment.center,
            children: [
              const Spacer(),

              // App Icon
              Container(
                width: 120,
                height: 120,
                decoration: BoxDecoration(
                  color: AppColors.primary,
                  borderRadius: BorderRadius.circular(24),
                  boxShadow: [
                    BoxShadow(
                      color: AppColors.primary.withOpacity(0.3),
                      blurRadius: 20,
                      offset: const Offset(0, 10),
                    ),
                  ],
                ),
                child: const Icon(
                  Icons.email_outlined,
                  size: 64,
                  color: Colors.white,
                ),
              ),
              const SizedBox(height: 32),

              // App Name
              Text(
                'LetMeDoMyWork',
                style: AppTextStyles.headlineLarge.copyWith(
                  fontWeight: FontWeight.bold,
                ),
              ),
              const SizedBox(height: 16),

              // Tagline
              Text(
                'Automated Follow-up Reminders',
                style: AppTextStyles.titleMedium.copyWith(
                  color: AppColors.onSurfaceVariant,
                ),
                textAlign: TextAlign.center,
              ),
              const SizedBox(height: 48),

              // Features
              _buildFeature(
                Icons.schedule,
                'Automatic Scheduling',
                'Set it and forget it - emails send automatically',
              ),
              const SizedBox(height: 16),
              _buildFeature(
                Icons.text_fields,
                'Smart Templates',
                'Personalized follow-ups with placeholders',
              ),
              const SizedBox(height: 16),
              _buildFeature(
                Icons.analytics_outlined,
                'Track Progress',
                'See statistics on your follow-up success',
              ),

              const Spacer(),

              // Get Started Button
              AppButton.primary(
                text: 'Get Started',
                isFullWidth: true,
                onPressed: () {
                  Navigator.pushReplacementNamed(context, Routes.smtpSetup);
                },
              ),
              const SizedBox(height: 12),

              // Skip Option
              TextButton(
                onPressed: () => _showSkipWarning(context),
                child: Text(
                  'Set up later',
                  style: TextStyle(color: AppColors.onSurfaceVariant),
                ),
              ),
            ],
          ),
        ),
      ),
    );
  }

  Widget _buildFeature(IconData icon, String title, String description) {
    return Row(
      children: [
        Container(
          padding: const EdgeInsets.all(12),
          decoration: BoxDecoration(
            color: AppColors.primary.withOpacity(0.1),
            borderRadius: BorderRadius.circular(12),
          ),
          child: Icon(icon, color: AppColors.primary),
        ),
        const SizedBox(width: 16),
        Expanded(
          child: Column(
            crossAxisAlignment: CrossAxisAlignment.start,
            children: [
              Text(
                title,
                style: AppTextStyles.titleSmall,
              ),
              Text(
                description,
                style: AppTextStyles.bodySmall,
              ),
            ],
          ),
        ),
      ],
    );
  }

  Future<void> _showSkipWarning(BuildContext context) async {
    final skip = await showDialog<bool>(
      context: context,
      builder: (context) => AlertDialog(
        title: const Text('Skip Setup?'),
        content: const Text(
          'You won\'t be able to send emails until you configure your SMTP settings in Settings.',
        ),
        actions: [
          TextButton(
            onPressed: () => Navigator.pop(context, false),
            child: const Text('Go Back'),
          ),
          TextButton(
            onPressed: () => Navigator.pop(context, true),
            child: const Text('Skip Anyway'),
          ),
        ],
      ),
    );

    if (skip == true) {
      Navigator.pushReplacementNamed(context, Routes.main);
    }
  }
}
```

## Acceptance Criteria
- [ ] App icon and name displayed
- [ ] Tagline displayed
- [ ] Three feature highlights with icons
- [ ] "Get Started" button navigates to SMTP setup
- [ ] "Set up later" shows warning and navigates to main
- [ ] Clean, professional design

## Dependencies
- Task 051-053 (Theme)
- Task 055 (Routes)
- Task 056 (AppButton)

## Parallel Work
Can run parallel with: Task 075

## Estimated Effort
1.5 hours
