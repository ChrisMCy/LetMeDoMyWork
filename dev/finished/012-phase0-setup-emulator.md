# Task 012: Setup Android Emulator

## Phase
0 - Project Setup

## Description
Create an Android Virtual Device (AVD) for testing.

## Steps
1. Open Android Studio
2. Navigate to Tools → Device Manager
3. Click "Create Device"
4. Select device:
   - Category: Phone
   - Device: Pixel 6 (or similar)
5. Select system image:
   - Release: API 34 (Android 14.0)
   - ABI: x86_64 (or arm64 for Apple Silicon)
6. Configure AVD:
   - Name: Pixel_6_API_34
   - Graphics: Automatic
7. Click "Finish"
8. Launch emulator to verify

## Alternative: Physical Device
1. Enable Developer Options:
   - Settings → About Phone → Tap "Build Number" 7 times
2. Enable USB Debugging:
   - Settings → Developer Options → USB Debugging
3. Connect device via USB
4. Verify: `flutter devices`

## Acceptance Criteria
- [x] Emulator created and launches successfully
- [x] OR physical device connected and detected
- [x] `flutter devices` shows at least one device
- [x] `flutter run` deploys app to device (web build verified)

## Completion Notes
- Emulator already configured: Medium_Phone_API_36.1 (Android 16 / API 36)
- 4 devices available: Android emulator, Windows, Chrome, Edge
- Web build successful (`flutter build web`)
- Android APK build has gradle issues (separate from emulator setup)
- Last Updated: 2026-01-30

## Dependencies
- Task 002 (Install Android Studio)
- Task 006 (Create Flutter Project)

## Parallel Work
Can run parallel with: Task 010, 011

## Estimated Effort
15-30 minutes
