# Task 104: Build Release APK

## Phase
7 - Release Preparation

## Description
Build and test the release APK.

## Steps
1. Clean project
2. Build release APK
3. Test on device
4. Verify all features

## Build Commands
```bash
# Clean project
flutter clean
flutter pub get

# Analyze code
flutter analyze

# Run tests
flutter test

# Build release APK
flutter build apk --release

# Output location:
# build/app/outputs/flutter-apk/app-release.apk

# For app bundle (Play Store):
flutter build appbundle --release

# Output location:
# build/app/outputs/bundle/release/app-release.aab
```

## APK Info
```bash
# Check APK size
ls -la build/app/outputs/flutter-apk/app-release.apk

# Analyze APK
flutter build apk --analyze-size

# Expected: < 30 MB
```

## Installation Testing
```bash
# Install on device
adb install build/app/outputs/flutter-apk/app-release.apk

# Or use flutter
flutter install --release
```

## Release Testing Checklist

### Basic Functionality
- [ ] App launches successfully
- [ ] Splash screen shows
- [ ] First launch flow works
- [ ] Create TODO works
- [ ] Edit TODO works
- [ ] Delete TODO works
- [ ] Complete TODO works
- [ ] Pause/Resume works
- [ ] Swipe gestures work

### Email Functionality
- [ ] SMTP setup works
- [ ] Test email sends
- [ ] Manual send works
- [ ] Templates load correctly
- [ ] Placeholders replaced

### Background Service
- [ ] Background service starts
- [ ] Notifications work
- [ ] Survives app close
- [ ] Survives device restart

### Other Features
- [ ] Statistics display
- [ ] Export works
- [ ] Import works
- [ ] Settings persist
- [ ] Theme correct

### Performance
- [ ] Startup time acceptable
- [ ] No lag in UI
- [ ] Memory usage reasonable
- [ ] Battery usage reasonable

### Edge Cases
- [ ] Offline mode works
- [ ] Large data sets work
- [ ] Long text handled

## Common Issues

### ProGuard Issues
If release crashes but debug works:
```bash
# Build without obfuscation first
flutter build apk --release --no-shrink

# Then add ProGuard rules for problematic classes
```

### Signing Issues
```bash
# Verify APK is signed
jarsigner -verify -verbose -certs build/app/outputs/flutter-apk/app-release.apk
```

### Size Issues
```bash
# Analyze what's taking space
flutter build apk --release --analyze-size --target-platform android-arm64

# Split by ABI to reduce size
flutter build apk --release --split-per-abi
# Creates separate APKs for arm64-v8a, armeabi-v7a, x86_64
```

## Acceptance Criteria
- [ ] Release APK builds without errors
- [ ] APK size < 30 MB
- [ ] App works on release build
- [ ] All features functional
- [ ] No crashes
- [ ] Performance acceptable
- [ ] Tested on physical device

## Dependencies
- Task 103 (Keystore)
- All previous phases complete

## Parallel Work
Must run after: Task 103

## Estimated Effort
2-3 hours (including testing)
