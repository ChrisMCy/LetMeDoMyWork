# Task 009: Configure build.gradle

## Phase
0 - Project Setup

## Description
Configure Android build.gradle with correct SDK versions and app ID.

## Steps
1. Open `android/app/build.gradle`
2. Update configuration:

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
```

## Acceptance Criteria
- [ ] compileSdkVersion set to 34
- [ ] minSdkVersion set to 21
- [ ] targetSdkVersion set to 34
- [ ] applicationId is "com.letmedomywork.app"
- [ ] App builds successfully

## Dependencies
- Task 006 (Create Flutter Project)

## Parallel Work
Can run parallel with: Task 008 (Configure Android Manifest)

## Estimated Effort
10 minutes
