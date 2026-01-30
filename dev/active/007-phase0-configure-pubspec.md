# Task 007: Configure pubspec.yaml Dependencies

## Phase
0 - Project Setup

## Description
Add all required dependencies to pubspec.yaml for the project.

## Steps
1. Open `pubspec.yaml`
2. Update with all dependencies:

```yaml
name: letmedomywork
description: Automated follow-up email reminder app
publish_to: 'none'
version: 1.0.0+1

environment:
  sdk: '>=3.0.0 <4.0.0'

dependencies:
  flutter:
    sdk: flutter

  # State Management
  flutter_bloc: ^8.1.3
  equatable: ^2.0.5

  # Database
  sqflite: ^2.3.0
  path: ^1.8.3

  # Secure Storage
  flutter_secure_storage: ^9.0.0

  # Email Sending
  mailer: ^6.0.1

  # Background Tasks
  workmanager: ^0.5.2

  # Notifications
  flutter_local_notifications: ^16.3.0

  # Date/Time
  intl: ^0.18.1

  # File Operations
  path_provider: ^2.1.1
  file_picker: ^6.1.1

  # Dependency Injection
  get_it: ^7.6.4

  # Connectivity
  connectivity_plus: ^5.0.2

  # UI
  cupertino_icons: ^1.0.2

dev_dependencies:
  flutter_test:
    sdk: flutter
  flutter_lints: ^3.0.1
  mockito: ^5.4.4
  build_runner: ^2.4.7

flutter:
  uses-material-design: true
```

3. Run: `flutter pub get`

## Acceptance Criteria
- [ ] All dependencies listed in pubspec.yaml
- [ ] `flutter pub get` completes without errors
- [ ] No version conflicts

## Dependencies
- Task 006 (Create Flutter Project)

## Parallel Work
Can run parallel with: None

## Estimated Effort
15 minutes
