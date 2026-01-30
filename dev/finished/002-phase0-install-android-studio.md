# Task 002: Install Android Studio & SDK

## Phase
0 - Project Setup

## Description
Install Android Studio and configure the Android SDK with required components.

## Steps
1. Download Android Studio from https://developer.android.com/studio
2. Run installer with default options
3. Open SDK Manager (Tools → SDK Manager)
4. Install SDK Platforms:
   - Android 14.0 (API 34) - Target SDK
   - Android 5.0 (API 21) - Minimum SDK
5. Install SDK Tools:
   - Android SDK Build-Tools
   - Android SDK Command-line Tools
   - Android Emulator
   - Android SDK Platform-Tools

## Acceptance Criteria
- [x] Android Studio installed and opens successfully
- [x] SDK Platforms API 34 and API 21 installed (plus API 36)
- [x] All required SDK Tools installed
- [x] `flutter doctor` shows Android toolchain as OK

## Completion Notes
- Android Studio installed with SDK Platforms: API 21 (min), API 34 (target), API 36 (latest)
- SDK Tools installed: Build-Tools 36.1.0, Command-line Tools, Emulator 36.3.10.0, Platform-Tools
- Flutter & Dart plugins installed in Android Studio
- Android licenses accepted via `flutter doctor --android-licenses`
- `flutter doctor` now shows all green checkmarks
- Last Updated: 2026-01-30

## Dependencies
- Task 001 (Install Flutter SDK)

## Parallel Work
Can run parallel with: Task 003 (Install Git)

## Estimated Effort
30 minutes - 1 hour
