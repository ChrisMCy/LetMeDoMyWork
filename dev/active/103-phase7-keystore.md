# Task 103: Create Keystore for Signing

## Phase
7 - Release Preparation

## Description
Create signing keystore for release builds.

## Steps
1. Generate keystore
2. Configure build.gradle
3. Secure keystore file

## Keystore Generation
```bash
# Navigate to android folder
cd android

# Generate keystore
keytool -genkey -v \
  -keystore letmedomywork-release.jks \
  -keyalg RSA \
  -keysize 2048 \
  -validity 10000 \
  -alias letmedomywork

# You will be prompted for:
# - Keystore password (SAVE THIS!)
# - Key password (can be same as keystore)
# - Name, Organization, etc.
```

## Key.properties File
```properties
# android/key.properties
# DO NOT COMMIT THIS FILE

storePassword=<your-keystore-password>
keyPassword=<your-key-password>
keyAlias=letmedomywork
storeFile=../letmedomywork-release.jks
```

## Build.gradle Configuration
```gradle
// android/app/build.gradle

// Add at the top
def keystoreProperties = new Properties()
def keystorePropertiesFile = rootProject.file('key.properties')
if (keystorePropertiesFile.exists()) {
    keystoreProperties.load(new FileInputStream(keystorePropertiesFile))
}

android {
    // ... existing config

    signingConfigs {
        release {
            keyAlias keystoreProperties['keyAlias']
            keyPassword keystoreProperties['keyPassword']
            storeFile keystoreProperties['storeFile'] ? file(keystoreProperties['storeFile']) : null
            storePassword keystoreProperties['storePassword']
        }
    }

    buildTypes {
        release {
            signingConfig signingConfigs.release
            minifyEnabled true
            shrinkResources true
            proguardFiles getDefaultProguardFile('proguard-android-optimize.txt'), 'proguard-rules.pro'
        }
    }
}
```

## ProGuard Rules (if needed)
```proguard
# android/app/proguard-rules.pro

# Flutter wrapper
-keep class io.flutter.app.** { *; }
-keep class io.flutter.plugin.**  { *; }
-keep class io.flutter.util.**  { *; }
-keep class io.flutter.view.**  { *; }
-keep class io.flutter.**  { *; }
-keep class io.flutter.plugins.**  { *; }

# Keep Mailer classes
-keep class org.apache.** { *; }
-dontwarn org.apache.**

# Keep secure storage
-keep class com.it_nomads.fluttersecurestorage.** { *; }
```

## .gitignore Updates
```gitignore
# Add to .gitignore
android/key.properties
android/*.jks
android/*.keystore
```

## Keystore Backup
**IMPORTANT: Back up your keystore!**

1. Copy keystore file to secure location
2. Document passwords securely (password manager)
3. Store in multiple secure locations

Without the keystore, you cannot update the app!

## Verification
```bash
# Verify keystore
keytool -list -v -keystore android/letmedomywork-release.jks

# Verify build
flutter build apk --release
```

## Acceptance Criteria
- [ ] Keystore generated
- [ ] key.properties created
- [ ] build.gradle configured
- [ ] ProGuard rules added
- [ ] Files added to .gitignore
- [ ] Keystore backed up securely
- [ ] Passwords documented securely
- [ ] Release build succeeds

## Dependencies
- None

## Parallel Work
Can run parallel with: Task 101, 102

## Estimated Effort
1 hour
