# Task 073: Create SettingTile Widget

## Phase
3 - UI Foundation & MVP

## Description
Create a reusable settings list tile widget.

## Steps
1. Create `lib/presentation/screens/settings/widgets/setting_tile.dart`
2. Implement standard settings tile layout
3. Support icon, title, subtitle, and trailing widget

## Code Structure
```dart
import 'package:flutter/material.dart';
import '../../../../core/theme/app_colors.dart';

class SettingTile extends StatelessWidget {
  final IconData icon;
  final String title;
  final String? subtitle;
  final Widget? trailing;
  final VoidCallback? onTap;
  final bool enabled;

  const SettingTile({
    super.key,
    required this.icon,
    required this.title,
    this.subtitle,
    this.trailing,
    this.onTap,
    this.enabled = true,
  });

  @override
  Widget build(BuildContext context) {
    return ListTile(
      leading: Container(
        padding: const EdgeInsets.all(8),
        decoration: BoxDecoration(
          color: AppColors.primary.withOpacity(0.1),
          borderRadius: BorderRadius.circular(8),
        ),
        child: Icon(
          icon,
          color: enabled ? AppColors.primary : AppColors.onSurfaceVariant,
        ),
      ),
      title: Text(
        title,
        style: TextStyle(
          color: enabled ? null : AppColors.onSurfaceVariant,
        ),
      ),
      subtitle: subtitle != null
          ? Text(
              subtitle!,
              style: TextStyle(
                color: enabled
                    ? AppColors.onSurfaceVariant
                    : AppColors.onSurfaceVariant.withOpacity(0.5),
              ),
            )
          : null,
      trailing: trailing,
      onTap: enabled ? onTap : null,
      enabled: enabled,
    );
  }
}

/// Setting tile with a switch
class SwitchSettingTile extends StatelessWidget {
  final IconData icon;
  final String title;
  final String? subtitle;
  final bool value;
  final ValueChanged<bool> onChanged;
  final bool enabled;

  const SwitchSettingTile({
    super.key,
    required this.icon,
    required this.title,
    this.subtitle,
    required this.value,
    required this.onChanged,
    this.enabled = true,
  });

  @override
  Widget build(BuildContext context) {
    return SettingTile(
      icon: icon,
      title: title,
      subtitle: subtitle,
      enabled: enabled,
      trailing: Switch(
        value: value,
        onChanged: enabled ? onChanged : null,
      ),
      onTap: enabled ? () => onChanged(!value) : null,
    );
  }
}

/// Setting tile showing current value
class ValueSettingTile extends StatelessWidget {
  final IconData icon;
  final String title;
  final String value;
  final VoidCallback? onTap;

  const ValueSettingTile({
    super.key,
    required this.icon,
    required this.title,
    required this.value,
    this.onTap,
  });

  @override
  Widget build(BuildContext context) {
    return SettingTile(
      icon: icon,
      title: title,
      trailing: Row(
        mainAxisSize: MainAxisSize.min,
        children: [
          Text(
            value,
            style: TextStyle(
              color: AppColors.onSurfaceVariant,
            ),
          ),
          const SizedBox(width: 4),
          const Icon(Icons.chevron_right),
        ],
      ),
      onTap: onTap,
    );
  }
}
```

## Usage Examples
```dart
// Basic tile
SettingTile(
  icon: Icons.article,
  title: 'Manage Templates',
  subtitle: 'Customize email templates',
  trailing: const Icon(Icons.chevron_right),
  onTap: () => Navigator.pushNamed(context, Routes.templates),
)

// Switch tile
SwitchSettingTile(
  icon: Icons.notifications,
  title: 'Notifications',
  subtitle: 'Show notifications when emails are sent',
  value: _notificationsEnabled,
  onChanged: (value) => setState(() => _notificationsEnabled = value),
)

// Value tile
ValueSettingTile(
  icon: Icons.repeat,
  title: 'Max Follow-ups',
  value: '10',
  onTap: () => _showMaxFollowUpsDialog(),
)
```

## Acceptance Criteria
- [ ] Basic tile with icon, title, subtitle
- [ ] Switch variant for boolean settings
- [ ] Value variant showing current value
- [ ] Trailing widget support
- [ ] Disabled state support
- [ ] Consistent styling with app theme

## Dependencies
- Task 051 (AppColors)

## Parallel Work
Can run parallel with: Task 071, 072

## Estimated Effort
30 minutes
