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
- [ ] Emulator created and launches successfully
- [ ] OR physical device connected and detected
- [ ] `flutter devices` shows at least one device
- [ ] `flutter run` deploys app to device

## Dependencies
- Task 002 (Install Android Studio)
- Task 006 (Create Flutter Project)

## Parallel Work
Can run parallel with: Task 010, 011

## Estimated Effort
15-30 minutes
