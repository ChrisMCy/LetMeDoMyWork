# LetMeDoMyWork - Project Setup Guide

## System Requirements

### Development Machine

**Operating System:**
- Windows 10/11 (64-bit)
- macOS 10.14 (Mojave) or later
- Linux (Ubuntu 20.04+ or equivalent)

**Hardware:**
- CPU: 2+ cores recommended
- RAM: 8GB minimum, 16GB recommended
- Storage: 10GB free space (for Flutter SDK + Android SDK + project)
- Internet connection (for downloading dependencies)

### Target Platform

**Android:**
- Minimum SDK: API 21 (Android 5.0 Lollipop)
- Target SDK: API 34 (Android 14)
- Compile SDK: API 34

**Note:** iOS support NOT in scope for v1.0

---

## Required Software

### 1. Flutter SDK

**Version:** Flutter 3.19.0 or later (Stable channel)

**Installation:**

**Windows:**
```bash
# Download Flutter SDK
# https://docs.flutter.dev/get-started/install/windows

# Extract to C:\src\flutter

# Add to PATH
setx PATH "%PATH%;C:\src\flutter\bin"

# Verify installation
flutter doctor
```

**macOS:**
```bash
# Using Homebrew
brew install flutter

# Or download directly
# https://docs.flutter.dev/get-started/install/macos

# Add to PATH in ~/.zshrc or ~/.bash_profile
export PATH="$PATH:/path/to/flutter/bin"

# Verify installation
flutter doctor
```

**Linux:**
```bash
# Download Flutter SDK
cd ~/development
wget https://storage.googleapis.com/flutter_infra_release/releases/stable/linux/flutter_linux_3.19.0-stable.tar.xz
tar xf flutter_linux_3.19.0-stable.tar.xz

# Add to PATH in ~/.bashrc
export PATH="$PATH:$HOME/development/flutter/bin"

# Verify installation
flutter doctor
```

**Verify Installation:**
```bash
flutter --version
# Should show: Flutter 3.19.0 (or later)

flutter doctor
# Check all items - fix any issues
```

---

### 2. Android Studio

**Version:** Android Studio Hedgehog (2023.1.1) or later

**Download:** https://developer.android.com/studio

**Installation Steps:**

1. **Download and Install Android Studio**
   - Follow platform-specific installer

2. **Install Android SDK Components:**
```
   Open Android Studio
   → Tools → SDK Manager
   → SDK Platforms tab:
      ☑ Android 14.0 (API 34)
      ☑ Android 5.0 (API 21) - for minimum support
   → SDK Tools tab:
      ☑ Android SDK Build-Tools
      ☑ Android SDK Command-line Tools
      ☑ Android Emulator
      ☑ Android SDK Platform-Tools
   → Click "Apply" to download
```

3. **Install Flutter & Dart Plugins:**
```
   Open Android Studio
   → File → Settings (Windows/Linux) / Preferences (macOS)
   → Plugins
   → Search "Flutter" → Install
   → Search "Dart" → Install (usually installed with Flutter)
   → Restart Android Studio
```

4. **Accept Android Licenses:**
```bash
   flutter doctor --android-licenses
   # Accept all licenses (type 'y' for each)
```

**Verify:**
```bash
flutter doctor
# Should show:
# [✓] Android toolchain - develop for Android devices
```

---

### 3. Android Emulator (Optional but Recommended)

**Create AVD (Android Virtual Device):**
```
Open Android Studio
→ Tools → Device Manager
→ Create Device
→ Select: Pixel 6 (or any device)
→ System Image: API 34 (Android 14.0)
→ Finish

Launch emulator to verify
```

**Alternative: Physical Android Device**
```
1. Enable Developer Options on device:
   Settings → About Phone → Tap "Build Number" 7 times

2. Enable USB Debugging:
   Settings → Developer Options → USB Debugging

3. Connect device via USB

4. Verify:
   flutter devices
   # Should list your device
```

---

### 4. Git (Version Control)

**Installation:**

**Windows:**
```bash
# Download from https://git-scm.com/download/win
# Run installer with default options
```

**macOS:**
```bash
# Git comes pre-installed
# Or install via Homebrew
brew install git
```

**Linux:**
```bash
sudo apt-get update
sudo apt-get install git
```

**Verify:**
```bash
git --version
# Should show: git version 2.x.x
```

---

### 5. VS Code (Recommended Editor)

**Download:** https://code.visualstudio.com/

**Required Extensions:**
1. **Flutter** (by Dart Code)
2. **Dart** (by Dart Code)

**Optional but Helpful:**
3. Error Lens
4. GitLens
5. Bracket Pair Colorizer
6. Material Icon Theme

**Install Extensions:**
```
Open VS Code
→ Extensions (Ctrl+Shift+X / Cmd+Shift+X)
→ Search "Flutter" → Install
→ Search "Dart" → Install
```

**Configure VS Code:**
```json
// .vscode/settings.json (in project root)
{
  "dart.flutterSdkPath": "/path/to/flutter",
  "editor.formatOnSave": true,
  "editor.codeActionsOnSave": {
    "source.fixAll": true
  },
  "[dart]": {
    "editor.defaultFormatter": "Dart-Code.dart-code",
    "editor.formatOnSave": true,
    "editor.rulers": [80]
  }
}
```

---

## Project Creation

### 1. Create Flutter Project
```bash
# Navigate to your projects directory
cd ~/Projects

# Create new Flutter project
flutter create letmedomywork

# Navigate into project
cd letmedomywork

# Open in VS Code
code .
```

**Verify Project Structure:**
```
letmedomywork/
├── android/           # Android-specific code
├── ios/              # iOS-specific (ignore for v1.0)
├── lib/              # Main Dart code
│   └── main.dart
├── test/             # Unit tests
├── pubspec.yaml      # Dependencies
└── README.md
```

---

### 2. Configure Project

**Edit `pubspec.yaml`:**
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
  
  # Secure Storage (SMTP password)
  flutter_secure_storage: ^9.0.0
  
  # Email Sending
  mailer: ^6.0.1
  
  # Background Tasks
  workmanager: ^0.5.2
  
  # Notifications
  flutter_local_notifications: ^16.3.0
  
  # Permissions
  permission_handler: ^11.1.0
  
  # Date/Time
  intl: ^0.18.1
  
  # File Operations
  path_provider: ^2.1.1
  file_picker: ^6.1.1
  
  # Dependency Injection
  get_it: ^7.6.4
  
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
  
  # Assets (if needed)
  # assets:
  #   - assets/images/
```

**Install Dependencies:**
```bash
flutter pub get
```

---

### 3. Android Configuration

**Edit `android/app/build.gradle`:**
```gradle
android {
    compileSdkVersion 34
    
    defaultConfig {
        applicationId "com.letmedomywork.app"
        minSdkVersion 21
        targetSdkVersion 34
        versionCode 1
        versionName "1.0.0"
    }
    
    buildTypes {
        release {
            signingConfig signingConfigs.debug
            // TODO: Configure proper signing for production
        }
    }
}

dependencies {
    // Already included by Flutter
}
```

**Edit `android/app/src/main/AndroidManifest.xml`:**
```xml
<manifest xmlns:android="http://schemas.android.com/apk/res/android">
    
    <!-- Permissions -->
    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />
    <uses-permission android:name="android.permission.SCHEDULE_EXACT_ALARM" />
    <uses-permission android:name="android.permission.USE_EXACT_ALARM" />
    <uses-permission android:name="android.permission.POST_NOTIFICATIONS" />
    <uses-permission android:name="android.permission.WAKE_LOCK" />
    <uses-permission android:name="android.permission.FOREGROUND_SERVICE" />
    <uses-permission android:name="android.permission.FOREGROUND_SERVICE_DATA_SYNC" />
    
    <!-- Storage (for Android 12 and below) -->
    <uses-permission android:name="android.permission.WRITE_EXTERNAL_STORAGE"
                     android:maxSdkVersion="32" />
    <uses-permission android:name="android.permission.READ_EXTERNAL_STORAGE"
                     android:maxSdkVersion="32" />
    
    <application
        android:label="LetMeDoMyWork"
        android:name="${applicationName}"
        android:icon="@mipmap/ic_launcher">
        
        <activity
            android:name=".MainActivity"
            android:exported="true"
            android:launchMode="singleTop"
            android:theme="@style/LaunchTheme"
            android:configChanges="orientation|keyboardHidden|keyboard|screenSize|smallestScreenSize|locale|layoutDirection|fontScale|screenLayout|density|uiMode"
            android:hardwareAccelerated="true"
            android:windowSoftInputMode="adjustResize">
            
            <meta-data
              android:name="io.flutter.embedding.android.NormalTheme"
              android:resource="@style/NormalTheme"
              />
            
            <intent-filter>
                <action android:name="android.intent.action.MAIN"/>
                <category android:name="android.intent.category.LAUNCHER"/>
            </intent-filter>
        </activity>
        
        <meta-data
            android:name="flutterEmbedding"
            android:value="2" />
    </application>
</manifest>
```

---

### 4. Project Structure Setup

**Create Directory Structure:**
```bash
# From project root
cd lib

# Create directories
mkdir -p core/{constants,theme,utils,errors}
mkdir -p data/{models,repositories,datasources}
mkdir -p domain/{entities,repositories,usecases}
mkdir -p presentation/{screens,widgets,bloc}
mkdir -p services/{database,smtp,background,notifications}
```

**Final Structure:**
```
lib/
├── core/
│   ├── constants/
│   │   └── app_constants.dart
│   ├── theme/
│   │   ├── app_theme.dart
│   │   ├── app_colors.dart
│   │   └── app_text_styles.dart
│   ├── utils/
│   │   └── date_utils.dart
│   └── errors/
│       └── exceptions.dart
├── data/
│   ├── models/
│   │   ├── todo_model.dart
│   │   ├── settings_model.dart
│   │   └── sent_email_model.dart
│   ├── repositories/
│   │   └── todo_repository_impl.dart
│   └── datasources/
│       └── local_datasource.dart
├── domain/
│   ├── entities/
│   │   ├── todo.dart
│   │   └── settings.dart
│   ├── repositories/
│   │   └── todo_repository.dart
│   └── usecases/
│       ├── create_todo.dart
│       ├── send_email.dart
│       └── get_todos.dart
├── presentation/
│   ├── screens/
│   │   ├── main/
│   │   ├── create_todo/
│   │   ├── settings/
│   │   └── statistics/
│   ├── widgets/
│   │   └── todo_card.dart
│   └── bloc/
│       └── todo_bloc.dart
├── services/
│   ├── database/
│   │   └── database_helper.dart
│   ├── smtp/
│   │   └── email_service.dart
│   ├── background/
│   │   └── background_service.dart
│   └── notifications/
│       └── notification_service.dart
└── main.dart
```

---

## Dependency Configuration

### 1. WorkManager (Background Tasks)

**Android Setup:**

Edit `android/app/src/main/AndroidManifest.xml` - add inside `<application>`:
```xml
<provider
    android:name="androidx.startup.InitializationProvider"
    android:authorities="${applicationId}.androidx-startup"
    android:exported="false"
    tools:node="merge">
    <meta-data
        android:name="androidx.work.WorkManagerInitializer"
        android:value="androidx.startup"
        tools:node="remove" />
</provider>
```

**Kotlin Setup:**

Create `android/app/src/main/kotlin/com/letmedomywork/app/Application.kt`:
```kotlin
package com.letmedomywork.app

import io.flutter.app.FlutterApplication
import androidx.work.Configuration

class Application : FlutterApplication(), Configuration.Provider {
    override fun getWorkManagerConfiguration(): Configuration {
        return Configuration.Builder()
            .setMinimumLoggingLevel(android.util.Log.INFO)
            .build()
    }
}
```

Update `AndroidManifest.xml`:
```xml
<application
    android:name=".Application"
    ...
```

---

### 2. Flutter Local Notifications

**Android Setup:**

Create `android/app/src/main/res/drawable/app_icon.png` (notification icon)

Edit `android/app/src/main/AndroidManifest.xml` - add inside `<application>`:
```xml
<meta-data
    android:name="com.google.firebase.messaging.default_notification_icon"
    android:resource="@drawable/app_icon" />
<meta-data
    android:name="com.google.firebase.messaging.default_notification_color"
    android:resource="@color/notification_color" />
```

Create `android/app/src/main/res/values/colors.xml`:
```xml
<?xml version="1.0" encoding="utf-8"?>
<resources>
    <color name="notification_color">#3498DB</color>
</resources>
```

---

### 3. Flutter Secure Storage

**Android Minimum SDK Requirement:**

Already set to API 21+ in build.gradle - no additional setup needed.

**Note:** Auto-handles encryption via Android Keystore.

---

## Build & Run

### 1. Verify Setup
```bash
# Check everything is configured correctly
flutter doctor -v

# Should show all green checkmarks for:
# [✓] Flutter
# [✓] Android toolchain
# [✓] VS Code (or Android Studio)
```

---

### 2. Run on Emulator
```bash
# Start emulator (if not running)
# Via Android Studio: Tools → Device Manager → Launch

# Or via command line:
emulator -avd Pixel_6_API_34

# Run app
flutter run

# Or in debug mode with hot reload
flutter run --debug
```

**Expected Output:**
```
Launching lib/main.dart on Pixel 6 API 34 in debug mode...
Running Gradle task 'assembleDebug'...
✓ Built build/app/outputs/flutter-apk/app-debug.apk.
Installing build/app/outputs/flutter-apk/app-debug.apk...
Waiting for Pixel 6 API 34 to report its views...
Syncing files to device Pixel 6 API 34...
Flutter run key commands.
r Hot reload.
R Hot restart.
h List all available interactive commands.
d Detach (terminate "flutter run" but leave application running).
c Clear the screen
q Quit (terminate the application on the device).

Running with sound null safety

An Observatory debugger and profiler on Pixel 6 API 34 is available at: http://127.0.0.1:xxxxx/
The Flutter DevTools debugger and profiler on Pixel 6 API 34 is available at: http://127.0.0.1:xxxxx/
```

---

### 3. Run on Physical Device
```bash
# Connect device via USB
# Enable USB Debugging on device

# Verify device is detected
flutter devices

# Run on device
flutter run -d <device-id>
```

---

### 4. Build APK (Release)
```bash
# Build release APK
flutter build apk --release

# Output location:
# build/app/outputs/flutter-apk/app-release.apk

# File size: ~15-25 MB (expected for this app)
```

**Install APK on Device:**
```bash
# Via ADB
adb install build/app/outputs/flutter-apk/app-release.apk

# Or manually:
# 1. Copy APK to device
# 2. Open file on device
# 3. Allow "Install from Unknown Sources"
# 4. Install
```

---

## Testing Setup

### 1. Unit Tests

**Run all tests:**
```bash
flutter test
```

**Run specific test:**
```bash
flutter test test/services/database/database_helper_test.dart
```

**With coverage:**
```bash
flutter test --coverage
```

---

### 2. Integration Tests

Create `integration_test/` directory:
```bash
mkdir integration_test
```

**Run integration tests:**
```bash
flutter test integration_test/
```

---

## Troubleshooting

### Common Issues

**1. "Flutter doctor" shows issues:**
```bash
# Android licenses not accepted
flutter doctor --android-licenses

# Android Studio not found
# → Reinstall Android Studio or set ANDROID_HOME manually

# VS Code not detected
# → Install Flutter & Dart extensions
```

**2. Build fails with "SDK version" error:**
```
Error: The plugin `package_name` requires a higher Android SDK version.

Solution:
Edit android/app/build.gradle
→ Increase minSdkVersion to 21
→ Set compileSdkVersion to 34
```

**3. Emulator doesn't start:**
```bash
# Check available AVDs
emulator -list-avds

# If empty, create one via Android Studio Device Manager

# Check for conflicting processes
# → Close Android Studio
# → Restart computer
```

**4. Hot reload doesn't work:**
```bash
# Full restart
r (in terminal where flutter run is running)

# Or stop and restart
q (quit)
flutter run
```

**5. Dependencies not installing:**
```bash
# Clear pub cache
flutter pub cache clean
flutter pub cache repair

# Remove pubspec.lock and try again
rm pubspec.lock
flutter pub get
```

**6. Build fails on Windows (long path error):**
```
Solution:
Move project to shorter path (e.g., C:\Projects\lmdmw)
```

---

## Development Workflow

### Recommended Workflow:

1. **Make code changes**
2. **Hot reload** (`r` in terminal)
   - For UI changes
   - Fast (< 1 second)

3. **Hot restart** (`R` in terminal)
   - For logic changes
   - Medium (few seconds)

4. **Full rebuild** (`flutter run`)
   - For dependency changes
   - For AndroidManifest changes
   - Slow (30-60 seconds)

5. **Test on real device regularly**
   - Emulator ≠ Real device
   - Especially for:
     - Background tasks
     - Notifications
     - Storage
     - Network

---

## IDE Shortcuts (VS Code)

**Flutter-specific:**
- `Ctrl+Shift+P` → "Flutter: Hot Reload"
- `Ctrl+Shift+P` → "Flutter: Hot Restart"
- `Ctrl+.` → Quick Fix / Refactor
- `F12` → Go to Definition
- `Shift+F12` → Find All References

**Code Navigation:**
- `Ctrl+P` → Quick Open File
- `Ctrl+Shift+O` → Go to Symbol in File
- `Ctrl+T` → Go to Symbol in Workspace

**Debugging:**
- `F5` → Start Debugging
- `F10` → Step Over
- `F11` → Step Into
- `Shift+F11` → Step Out

---

## Next Steps

After setup is complete:

1. ✅ Verify `flutter doctor` is all green
2. ✅ Run default Flutter app on emulator/device
3. ✅ Create project structure (directories)
4. ✅ Install all dependencies (`flutter pub get`)
5. ✅ Read through **DevelopmentPlan.md** for implementation strategy
6. ✅ Start with **Phase 1** from **DevelopmentPlan.md**

---

## Useful Commands Reference
```bash
# Project
flutter create <project_name>
flutter pub get
flutter pub upgrade

# Running
flutter run
flutter run --release
flutter run -d <device-id>

# Building
flutter build apk
flutter build apk --release
flutter build appbundle  # For Play Store

# Testing
flutter test
flutter test --coverage
flutter drive  # Integration tests

# Analyzing
flutter analyze
flutter doctor
flutter doctor -v

# Cleaning
flutter clean
flutter pub cache clean

# Devices
flutter devices
flutter emulators
flutter emulators --launch <emulator-id>

# Logs
flutter logs
adb logcat | grep flutter
```

---

**Ende ProjectSetup.md**