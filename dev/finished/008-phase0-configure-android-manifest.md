# Task 008: Configure Android Manifest

## Phase
0 - Project Setup

## Description
Configure AndroidManifest.xml with required permissions and settings.

## Steps
1. Open `android/app/src/main/AndroidManifest.xml`
2. Add permissions and configuration:

```xml
<manifest xmlns:android="http://schemas.android.com/apk/res/android">

    <!-- Network -->
    <uses-permission android:name="android.permission.INTERNET" />
    <uses-permission android:name="android.permission.ACCESS_NETWORK_STATE" />

    <!-- Alarms & Background -->
    <uses-permission android:name="android.permission.SCHEDULE_EXACT_ALARM" />
    <uses-permission android:name="android.permission.USE_EXACT_ALARM" />
    <uses-permission android:name="android.permission.WAKE_LOCK" />
    <uses-permission android:name="android.permission.FOREGROUND_SERVICE" />
    <uses-permission android:name="android.permission.FOREGROUND_SERVICE_DATA_SYNC" />
    <uses-permission android:name="android.permission.RECEIVE_BOOT_COMPLETED" />

    <!-- Notifications -->
    <uses-permission android:name="android.permission.POST_NOTIFICATIONS" />

    <!-- Storage (Android 12 and below) -->
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

            <intent-filter>
                <action android:name="android.intent.action.MAIN"/>
                <category android:name="android.intent.category.LAUNCHER"/>
            </intent-filter>
        </activity>

        <receiver android:name=".BootReceiver"
                  android:exported="true">
            <intent-filter>
                <action android:name="android.intent.action.BOOT_COMPLETED"/>
            </intent-filter>
        </receiver>

        <meta-data
            android:name="flutterEmbedding"
            android:value="2" />
    </application>
</manifest>
```

## Acceptance Criteria
- [x] All permissions added to AndroidManifest.xml
- [x] App label set to "LetMeDoMyWork"
- [x] Boot receiver configured
- [x] App still builds and runs

## Completion Notes
- Added all required permissions (INTERNET, SCHEDULE_EXACT_ALARM, WAKE_LOCK, POST_NOTIFICATIONS, etc.)
- Set app label to "LetMeDoMyWork"
- Added flutter_local_notifications boot receiver for scheduled notifications after reboot
- Added action broadcast receiver for notification actions
- Preserved existing Flutter meta-data and queries sections
- `flutter analyze` passes with no issues
- Last Updated: 2026-01-30

## Dependencies
- Task 006 (Create Flutter Project)

## Parallel Work
Can run parallel with: Task 009 (Configure build.gradle)

## Estimated Effort
15 minutes
