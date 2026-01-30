# LetMeDoMyWork - Development Plan

## Overview

Dieser Plan beschreibt die optimale Strategie, um das LetMeDoMyWork-Projekt von Grund auf zu entwickeln. Die Reihenfolge ist so gewählt, dass jeder Schritt auf vorherigen aufbaut und früh testbar ist.

---

## Development Approach

### Philosophie: Bottom-Up + Iterativ

1. **Foundation First:**
   - Datenbank & Models zuerst
   - Dann Services
   - Dann UI

2. **Vertical Slices:**
   - Komplette Features von DB → UI
   - Nicht horizontal (alle Models, dann alle Services, etc.)

3. **Test Early:**
   - Unit Tests für jede Komponente
   - Integration Tests für Flows
   - Manual Testing auf echtem Gerät

4. **Iterative Refinement:**
   - MVP zuerst (minimal viable product)
   - Dann Features hinzufügen
   - Dann Polish & Optimierung

---

## Phase 0: Project Setup (1-2 Tage)

### Ziel: Development Environment & Project Grundgerüst

**Voraussetzung:** Keine - Dies ist der Startpunkt

---

### 0.1: Software Installation

**Required Software:**

| Software | Version | Download |
|----------|---------|----------|
| Flutter SDK | 3.19.0+ | https://docs.flutter.dev/get-started/install |
| Android Studio | 2023.1.1+ | https://developer.android.com/studio |
| Git | 2.x | https://git-scm.com |
| VS Code (optional) | Latest | https://code.visualstudio.com |

**Flutter Installation:**
```bash
# Windows: Extract to C:\src\flutter, add to PATH
# macOS: brew install flutter
# Linux: Download & extract, add to PATH

# Verify installation
flutter doctor
```

**Android Studio Setup:**
1. Install Android Studio
2. Open SDK Manager (Tools → SDK Manager)
3. Install SDK Platforms:
   - Android 14.0 (API 34) - Target
   - Android 5.0 (API 21) - Minimum
4. Install SDK Tools:
   - Android SDK Build-Tools
   - Android SDK Command-line Tools
   - Android Emulator
   - Android SDK Platform-Tools
5. Install Flutter & Dart Plugins (File → Settings → Plugins)
6. Accept licenses: `flutter doctor --android-licenses`

**Verify Setup:**
```bash
flutter doctor -v
# All items should show [✓]
```

---

### 0.2: Create Flutter Project

**Create Project:**
```bash
# Navigate to projects directory
cd ~/Projects  # or your preferred location

# Create Flutter project
flutter create --org com.letmedomywork letmedomywork

# Navigate into project
cd letmedomywork

# Verify it runs
flutter run
```

---

### 0.3: Configure Dependencies

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

**Install Dependencies:**
```bash
flutter pub get
```

---

### 0.4: Android Configuration

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
    <uses-permission android:name="android.permission.RECEIVE_BOOT_COMPLETED" />

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

        <!-- Boot Receiver for Background Service -->
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

---

### 0.5: Project Structure

**Create Directory Structure:**
```bash
cd lib

# Core
mkdir -p core/{constants,theme,utils,errors,di,navigation}

# Domain Layer (Business Logic)
mkdir -p domain/{entities,repositories,usecases}

# Data Layer (Implementation)
mkdir -p data/{models,repositories,datasources}

# Presentation Layer (UI)
mkdir -p presentation/{screens,widgets,bloc}
mkdir -p presentation/screens/{main,todo,settings,statistics,onboarding}

# Services
mkdir -p services/{database,smtp,storage,background,notifications,network,lifecycle,email,backup}
```

**Final Structure:**
```
lib/
├── core/
│   ├── constants/
│   ├── theme/
│   ├── utils/
│   ├── errors/
│   ├── di/
│   └── navigation/
├── data/
│   ├── models/
│   ├── repositories/
│   └── datasources/
├── domain/
│   ├── entities/
│   ├── repositories/
│   └── usecases/
├── presentation/
│   ├── bloc/
│   ├── screens/
│   │   ├── main/
│   │   ├── todo/
│   │   ├── settings/
│   │   ├── statistics/
│   │   └── onboarding/
│   └── widgets/
├── services/
│   ├── database/
│   ├── smtp/
│   ├── storage/
│   ├── background/
│   ├── notifications/
│   ├── network/
│   ├── lifecycle/
│   ├── email/
│   └── backup/
└── main.dart
```

---

### 0.6: Git Setup

**Initialize Repository:**
```bash
cd ~/Projects/letmedomywork

# Initialize git
git init

# Create .gitignore
cat > .gitignore << 'EOF'
# Flutter/Dart
.dart_tool/
.packages
build/
.flutter-plugins
.flutter-plugins-dependencies
*.iml

# Android
android/.gradle/
android/local.properties
android/*.iml
android/app/debug/
android/app/release/

# iOS (not used but good to have)
ios/.symlinks/
ios/Pods/
ios/Flutter/Flutter.framework
ios/Flutter/Flutter.podspec

# IDE
.idea/
*.swp
.vscode/

# Test
coverage/

# Misc
*.log
*.lock
!pubspec.lock
.env
*.env
EOF

# Initial commit
git add .
git commit -m "Initial project setup with Clean Architecture structure"
```

---

### 0.7: Emulator/Device Setup

**Option A: Android Emulator**
```
1. Open Android Studio
2. Tools → Device Manager
3. Create Device → Pixel 6 (or similar)
4. System Image → API 34 (Android 14.0)
5. Finish → Launch
```

**Option B: Physical Device**
```
1. Enable Developer Options:
   Settings → About Phone → Tap "Build Number" 7 times

2. Enable USB Debugging:
   Settings → Developer Options → USB Debugging

3. Connect via USB

4. Verify:
   flutter devices
```

---

### 0.8: Validation

**Run Checks:**
```bash
# Check Flutter setup
flutter doctor -v

# Check dependencies
flutter pub get

# Analyze code
flutter analyze

# Run on device/emulator
flutter run
```

**Expected Result:**
- App starts showing default Flutter counter demo
- No errors in console
- Hot reload works (press 'r')

---

**Deliverables Phase 0:**
- [ ] Flutter SDK installed and working
- [ ] Android Studio with SDK configured
- [ ] Project created with correct package ID
- [ ] All dependencies in pubspec.yaml
- [ ] Android permissions configured
- [ ] Directory structure created
- [ ] Git repository initialized
- [ ] App runs on emulator/device

---

## Phase 1: Core Infrastructure (3-5 Tage)

### Ziel: Datenbank, Models, Basic Services

**Warum zuerst?**
- Alles andere baut darauf auf
- Früh testen möglich (Unit Tests)
- Fehler in DB-Design sind teuer zu fixen

### 1.1: Database Layer (Tag 1-2)

**Tasks:**
1. **DatabaseHelper erstellen**
   - SQLite Setup
   - Table Creation
   - Indices & Triggers

2. **Database Migration System**
   - Version tracking (PRAGMA user_version)
   - _onUpgrade handler für zukünftige Migrationen
   - Migration test helper

3. **Default Templates laden**
   - 30 DE + 30 EN Subjects
   - 30 DE + 30 EN Texts
   - Als JSON in assets/ oder hardcoded

4. **Settings Singleton initialisieren**
   - Bei erstem App-Start
   - Default-Werte eintragen

**Files:**
```
lib/services/database/
  ├── database_helper.dart
  ├── database_constants.dart
  ├── database_migrations.dart
  └── default_templates.dart

test/services/database/
  ├── database_helper_test.dart
  └── database_migrations_test.dart
```

**Tests:**
- Table creation erfolgreich
- Settings-Singleton enforcement
- CRUD operations
- Triggers funktionieren
- Migration from v1 to v2 (mock future migration)

**Validation:**
```dart
// Test erstellen
test('should create database with correct schema', () async {
  final db = await DatabaseHelper().database;
  final tables = await db.rawQuery("SELECT name FROM sqlite_master WHERE type='table'");
  expect(tables.length, 3); // settings, todos, sent_emails
});
```

---

### 1.2: Models & Entities (Tag 2)

**Tasks:**
1. **Domain Entities erstellen**
   - `Todo` entity
   - `Settings` entity
   - `SentEmail` entity

2. **Data Models erstellen**
   - `TodoModel extends Todo`
   - `SettingsModel extends Settings`
   - `SentEmailModel extends SentEmail`
   - `fromMap()` / `toMap()` Methoden

**Files:**
```
lib/domain/entities/
  ├── todo.dart
  ├── settings.dart
  └── sent_email.dart

lib/data/models/
  ├── todo_model.dart
  ├── settings_model.dart
  └── sent_email_model.dart
```

**Tests:**
- Model serialization/deserialization
- JSON encoding/decoding
- Edge cases (null values, empty strings)

**Validation:**
```dart
test('TodoModel should serialize to/from Map', () {
  final todo = TodoModel(...);
  final map = todo.toMap();
  final fromMap = TodoModel.fromMap(map);
  expect(fromMap, equals(todo));
});
```

---

### 1.3: Repository Pattern (Tag 3)

**Tasks:**
1. **Repository Interfaces (Domain)**
   - `TodoRepository` (abstract)
   - `SettingsRepository` (abstract)

2. **Repository Implementations (Data)**
   - `TodoRepositoryImpl`
   - `SettingsRepositoryImpl`
   - CRUD operations via DatabaseHelper

**Files:**
```
lib/domain/repositories/
  ├── todo_repository.dart
  └── settings_repository.dart

lib/data/repositories/
  ├── todo_repository_impl.dart
  └── settings_repository_impl.dart
```

**Tests:**
- Create TODO
- Read TODOs (all, by ID, filtered)
- Update TODO
- Delete TODO (+ cascade sent_emails)
- Settings operations

**Validation:**
```dart
test('should create and retrieve TODO', () async {
  final repo = TodoRepositoryImpl();
  final id = await repo.createTodo(testTodo);
  final retrieved = await repo.getTodoById(id);
  expect(retrieved, isNotNull);
  expect(retrieved!.subject, testTodo.subject);
});
```

---

### 1.4: Dependency Injection (Tag 3)

**Tasks:**
1. **GetIt Setup**
   - Service Locator konfigurieren
   - Alle Repositories registrieren
   - Database Helper als Singleton

**Files:**
```
lib/core/di/
  └── injection.dart
```

**Code:**
```dart
final getIt = GetIt.instance;

Future<void> setupDependencyInjection() async {
  // Database
  getIt.registerSingleton<DatabaseHelper>(DatabaseHelper());
  
  // Repositories
  getIt.registerLazySingleton<TodoRepository>(
    () => TodoRepositoryImpl(getIt<DatabaseHelper>())
  );
  
  getIt.registerLazySingleton<SettingsRepository>(
    () => SettingsRepositoryImpl(getIt<DatabaseHelper>())
  );
}
```

**Validation:**
```dart
test('should resolve dependencies', () async {
  await setupDependencyInjection();
  final repo = getIt<TodoRepository>();
  expect(repo, isNotNull);
});
```

---

## Phase 2: Core Business Logic (3-4 Tage)

### Ziel: Use Cases, Email Service, Placeholder Replacement

### 2.1: Use Cases (Tag 4)

**Tasks:**
1. **TODO Use Cases**
   - `CreateTodoUseCase`
   - `GetTodosUseCase`
   - `UpdateTodoUseCase`
   - `CompleteTodoUseCase`
   - `DeleteTodoUseCase`

2. **Email Use Cases**
   - `SendEmailUseCase`
   - `GetSentEmailsUseCase`

**Files:**
```
lib/domain/usecases/
  ├── todo/
  │   ├── create_todo.dart
  │   ├── get_todos.dart
  │   ├── update_todo.dart
  │   ├── complete_todo.dart
  │   └── delete_todo.dart
  └── email/
      ├── send_email.dart
      └── get_sent_emails.dart
```

**Tests:**
- Use Case mit Mock Repository
- Business Logic korrekt
- Edge Cases handled

**Validation:**
```dart
test('CompleteTodoUseCase should set completed flag and date', () async {
  final useCase = CompleteTodoUseCase(mockRepo);
  await useCase.execute(todoId: 1);
  verify(mockRepo.update(argThat(
    predicate((todo) => todo.isCompleted && todo.completedAt != null)
  )));
});
```

---

### 2.2: Placeholder & Email Parsing (Tag 5)

**Tasks:**
1. **PlaceholderService erstellen**
   - Replace-Logik für alle Platzhalter
   - Fallback für fehlende Daten (leerer String)
   - Unterstützte Platzhalter: {Vorname}, {Nachname}, {DateToday}, {DateLastMail}, {InitialSubject}, {DaysSinceLastMail}, {InitialText}

2. **EmailParsingService erstellen**
   - Auto-Extract First/Last Name from Email
   - Trennzeichen-Erkennung (., -, _, ,)
   - Capitalize-Funktion
   - Beispiel: "john.doe@mail.com" → ("John", "Doe")

3. **Email Template Selection**
   - Template Index Berechnung basierend auf send_count
   - Already-sent-first Logik (skip index 0)
   - Fallback auf letztes Template bei Überschreitung

**Files:**
```
lib/services/email/
  ├── placeholder_service.dart
  ├── email_parsing_service.dart
  └── template_service.dart

test/services/email/
  ├── placeholder_service_test.dart
  ├── email_parsing_service_test.dart
  └── template_service_test.dart
```

**Tests:**
- Alle Platzhalter korrekt ersetzt
- Fehlende Daten → leerer String
- Template Selection bei verschiedenen send_counts

**Validation:**
```dart
test('should replace all placeholders', () {
  final service = PlaceholderService();
  final result = service.replace(
    template: "Hi {Vorname}, bezüglich {InitialSubject}...",
    data: {
      'firstName': 'John',
      'initialSubject': 'Project X',
    }
  );
  expect(result, "Hi John, bezüglich Project X...");
});
```

---

### 2.3: Secure Storage Service (Tag 5)

**Tasks:**
1. **SecureStorageService erstellen**
   - flutter_secure_storage Wrapper
   - Save/Load/Delete SMTP Password
   - Clear all secure data (für Logout/Reset)

**Files:**
```
lib/services/storage/
  └── secure_storage_service.dart

test/services/storage/
  └── secure_storage_service_test.dart
```

**Tests:**
- Save and retrieve password
- Delete password
- Handle missing key gracefully

---

### 2.4: SMTP Email Service (Tag 5-6)

**Tasks:**
1. **SmtpConfigService erstellen**
   - Provider-spezifische Konfiguration (Gmail, Outlook, Custom)
   - Host/Port/TLS Defaults pro Provider

2. **EmailService erstellen**
   - SMTP Connection aufbauen
   - Email senden (plain text)
   - Error Handling mit spezifischen Fehlermeldungen
   - Timeout Handling (30 Sekunden)

**Files:**
```
lib/services/smtp/
  ├── smtp_config_service.dart
  └── email_service.dart

test/services/smtp/
  ├── smtp_config_service_test.dart
  └── email_service_test.dart
```

**Tests:**
- SMTP Connection (Mock)
- Email Build korrekt
- Error Handling

**Validation:**
```dart
test('should build email with correct headers', () async {
  final service = EmailService();
  final email = await service.buildEmail(
    from: 'sender@test.com',
    to: 'recipient@test.com',
    subject: 'Test',
    body: 'Test body',
  );
  expect(email.recipients, contains('recipient@test.com'));
});
```

---

### 2.5: Send Email Flow Integration (Tag 6)

**Tasks:**
1. **SendEmailUseCase komplett implementieren**
   - Template Selection
   - Placeholder Replacement
   - SMTP Send
   - Save to sent_emails
   - Update next_send_datetime

**Integration Test:**
```dart
test('should send email and update TODO', () async {
  // Given: TODO mit 0 gesendeten Mails
  final todo = await repo.createTodo(testTodo);

  // When: Email senden
  await sendEmailUseCase.execute(todoId: todo.id);

  // Then: sent_emails Eintrag + next_send updated
  final sentEmails = await repo.getSentEmails(todo.id);
  expect(sentEmails.length, 1);

  final updatedTodo = await repo.getTodoById(todo.id);
  expect(updatedTodo.nextSendDateTime, isNotNull);
  expect(updatedTodo.nextSendDateTime.isAfter(DateTime.now()), true);
});
```

---

### 2.6: Phase 2 Validation (Tag 6)

**Tasks:**
1. **Unit Test Coverage Check**
   - Ziel: 80%+ für Domain & Services
   - `flutter test --coverage`

2. **Integration Test: Email Flow**
   - TODO erstellen → Email senden → sent_emails prüfen
   - Template Selection korrekt
   - Placeholder Replacement korrekt

3. **Manual SMTP Test**
   - Test mit echtem Gmail Account
   - Test mit echtem Outlook Account
   - Verify: Email kommt an

**Deliverables:**
- Alle Unit Tests grün
- Email kann manuell gesendet werden (via Test-Code)
- Core Business Logic vollständig

---

## Phase 3: UI Foundation & MVP (5-6 Tage)

### Ziel: Theme, Reusable Widgets, Navigation, App Shell

**Warum UI ohne Background zuerst?**
- UI kann manuell getestet werden
- Background kommt später (komplexer)
- Früh User-Feedback möglich

### 3.1: Theme & Design System (Tag 7)

**Tasks:**
1. **App Theme erstellen**
   - Colors (Blue-Gray Palette aus Designs.md)
   - Text Styles (Roboto, verschiedene Größen)
   - Button Styles (Primary, Secondary, Text)
   - Card Styles (Elevation, Radius)
   - Input Decoration Theme

2. **Reusable Widgets**
   - AppButton (Primary/Secondary/Text variants)
   - AppTextField (mit Validation-Feedback)
   - AppCard (mit optional Swipe-Support)
   - LoadingIndicator (Spinner)
   - AppDialog (Confirmation, Error, Info)

3. **Navigation Structure**
   - App-Level Navigation (main.dart)
   - Route Definitions
   - Navigation Service (für programmatic navigation)

**Files:**
```
lib/core/theme/
  ├── app_theme.dart
  ├── app_colors.dart
  ├── app_text_styles.dart
  └── app_dimensions.dart

lib/core/navigation/
  ├── app_router.dart
  └── routes.dart

lib/presentation/widgets/
  ├── app_button.dart
  ├── app_text_field.dart
  ├── app_card.dart
  ├── app_dialog.dart
  └── loading_indicator.dart
```

**Validation:**
- App zeigt korrekte Farben
- Text Styles angewendet
- Widgets wiederverwendbar
- Navigation zwischen Screens funktioniert

---

### 3.2: Main Screen (TODO List) (Tag 7-8)

**Tasks:**
1. **State Management (BLoC)**
   - `TodoBloc` erstellen
   - Events: Load, Create, Update, Delete, Complete, Pause, Resume
   - States: Initial, Loading, Loaded, Error

2. **Main Screen UI**
   - Two Tabs (Active/Completed)
   - TODO List (sortiert nach BusinessLogik.md Regeln)
   - Empty States (unterschiedlich für Active/Completed)
   - FAB Button (nur auf Active Tab)
   - Header mit Settings & Statistics Icons

3. **TODO Card Widget**
   - Subject (gefärbt nach send_count/max_sends)
   - Email Adresse
   - Last/Next Send Dates
   - Send Count Badge (X/10)
   - Manual Send Button (📤)
   - Pause Icon (⏸️) wenn pausiert

4. **Swipe Gestures (Dismissible)**
   - Active Tab - Swipe Right: Complete TODO (mit Undo Snackbar)
   - Active Tab - Swipe Left: Pause/Resume Toggle
   - Completed Tab - Swipe Left: Reopen Dialog
   - Swipe Animations (Slide + Fade)

**Files:**
```
lib/presentation/bloc/todo/
  ├── todo_bloc.dart
  ├── todo_event.dart
  └── todo_state.dart

lib/presentation/screens/main/
  ├── main_screen.dart
  └── widgets/
      ├── todo_list_tab.dart
      ├── todo_card.dart
      ├── swipeable_todo_card.dart
      ├── empty_state.dart
      └── undo_snackbar.dart
```

**Tests:**
- BLoC emits correct states
- UI updates on state change
- Swipe gestures trigger correct actions
- Sorting korrekt (paused at bottom, by send_count)
- Color gradient based on send_count

**Validation:**
- Manuell: App öffnen, TODO Liste sehen
- Swipe Right → TODO completed, Snackbar erscheint
- Swipe Left → TODO paused/resumed
- Unit: BLoC tests
- Widget: TODO Card rendering

---

### 3.3: Create/Edit TODO Screen (Tag 8-9)

**Tasks:**
1. **Form Validation**
   - Required fields
   - Email format
   - Date/Time validation

2. **UI Implementation**
   - All input fields
   - Language Toggle
   - Template Selection mit Reload
   - Name Swap Button

**Files:**
```
lib/presentation/screens/todo/
  ├── create_todo_screen.dart
  ├── edit_todo_screen.dart
  └── widgets/
      ├── language_toggle.dart
      ├── name_swap_field.dart
      ├── template_row.dart
      └── date_time_picker.dart
```

**Tests:**
- Form validation
- Template reload randomization
- Name swap funktioniert
- Save creates TODO in DB

**Validation:**
- Manuell: TODO erstellen, in Liste sehen
- Unit: Form validation logic
- Widget: Input fields

---

### 3.4: Settings Screen (Tag 9-10)

**Tasks:**
1. **SMTP Configuration Section**
   - Provider Dropdown
   - Email/Password inputs
   - Test Email Button
   - Help Dialog

2. **Template Management**
   - Navigate to Template Selection
   - (Full implementation später)

3. **Other Settings**
   - Max Follow-Ups
   - Randomize Minutes

**Files:**
```
lib/presentation/screens/settings/
  ├── settings_screen.dart
  └── widgets/
      ├── smtp_config_section.dart
      ├── setting_tile.dart
      └── help_dialog.dart
```

**Tests:**
- Settings save/load
- SMTP validation
- Test Email sendet

**Validation:**
- Manuell: Settings ändern, speichern, neu laden
- Test Email erhalten

---

### 3.5: First Launch Flow (Tag 10)

**Tasks:**
1. **First Launch Detection**
   - Prüfen ob Settings existieren (SELECT COUNT(*) FROM settings)
   - Flag in SharedPreferences als Backup

2. **Welcome Screen**
   - App-Branding (Name, Icon, Kurzbeschreibung)
   - "Get Started" Button
   - Optional: Feature-Highlights (Carousel)

3. **SMTP Setup Wizard**
   - Schritt 1: Provider auswählen (Gmail/Outlook/Custom)
   - Schritt 2: Email & Password eingeben
   - Schritt 3: Test Email senden
   - Schritt 4: Erfolg → Navigate zu Main Screen
   - Bei Fehler: Retry-Option

4. **Skip Option**
   - "Setup Later" Link
   - Warning: "You won't be able to send emails until configured"
   - Navigate zu Main Screen (Settings incomplete)

**Files:**
```
lib/presentation/screens/onboarding/
  ├── welcome_screen.dart
  ├── smtp_setup_wizard.dart
  └── widgets/
      ├── provider_selection.dart
      ├── credentials_form.dart
      └── setup_success.dart
```

**Tests:**
- First launch detection works
- Wizard completes successfully
- Skip option works
- Second launch skips onboarding

**Validation:**
- Manuell: App deinstallieren, neu installieren
- Welcome Screen erscheint
- SMTP Setup durchlaufen
- Main Screen erreicht

---

### 3.6: Manual Send Feature (Tag 10)

**Tasks:**
1. **Send Button in TODO Card**
   - Confirmation Dialog (zeigt Subject Preview)
   - Loading State während Send
   - Trigger SendEmailUseCase
   - Success Toast + UI Update
   - Error Dialog mit Retry-Option

2. **Error Handling UI**
   - Roter Rahmen um TODO bei Fehler
   - Error Details im TODO-Detail abrufbar

**Files:**
```
lib/presentation/widgets/
  ├── send_confirmation_dialog.dart
  └── error_indicator.dart
```

**Validation:**
- Manuell: Button drücken → Email gesendet
- UI updated (Last Sent Date, Send Count)
- sent_emails Eintrag in DB
- Bei Fehler: Error Dialog erscheint

---

### 3.7: Phase 3 Validation (Tag 11)

**Tasks:**
1. **End-to-End Flow Test (Manual)**
   - App starten (First Launch)
   - SMTP konfigurieren
   - TODO erstellen
   - TODO in Liste sehen
   - Manual Send → Email erhalten
   - TODO completen (Swipe)
   - Undo Snackbar testen
   - Completed Tab prüfen

2. **Widget Test Coverage**
   - Ziel: 60%+ für presentation/widgets/
   - Alle Custom Widgets getestet

3. **Bug Fixes**
   - Gefundene Issues fixen
   - Edge Cases abdecken

**Deliverables:**
- MVP funktioniert vollständig
- User kann TODOs erstellen und manuell Emails senden
- App ist stabil (keine Crashes)

---

## Phase 4: Advanced Features (3-4 Tage)

### 4.1: Statistics Screen (Tag 11)

**Tasks:**
1. **Statistics Use Cases**
   - Calculate overall stats
   - By recipient
   - Best templates
   - Heatmap

2. **UI Implementation**
   - Cards für Stats
   - Bar Chart (Heatmap)
   - Recipient List

**Files:**
```
lib/domain/usecases/statistics/
  ├── get_overall_stats.dart
  ├── get_recipient_stats.dart
  └── get_template_stats.dart

lib/presentation/screens/statistics/
  ├── statistics_screen.dart
  └── widgets/
      ├── stat_card.dart
      └── heatmap_chart.dart
```

**Validation:**
- Manuell: Complete einige TODOs, Stats anzeigen
- Stats korrekt berechnet

---

### 4.2: Template Management (Tag 11-12)

**Tasks:**
1. **Template Selection Screen**
   - Drag & Drop Reordering
   - Add/Remove Templates
   - Edit Custom Templates

**Files:**
```
lib/presentation/screens/settings/
  ├── template_management_screen.dart
  └── widgets/
      ├── template_list_item.dart
      ├── add_template_dialog.dart
      └── draggable_list.dart
```

**Validation:**
- Manuell: Templates reordern, speichern, in TODO Creation sehen

---

### 4.3: Export/Import (Tag 12)

**Tasks:**
1. **Export Service**
   - Serialize zu JSON
   - Save to Downloads
   - Send Email (if < 10MB)

2. **Import Service**
   - Load JSON
   - Validate
   - Replace DB data

**Files:**
```
lib/services/backup/
  ├── export_service.dart
  └── import_service.dart
```

**Validation:**
- Export → File in Downloads
- Import → Daten wiederhergestellt

---

### 4.4: Phase 4 Validation (Tag 12-13)

**Tasks:**
1. **Statistics Accuracy Test**
   - Create 10+ TODOs, complete some
   - Verify stats calculations match manual calculation
   - Test edge cases (0 completions, all completions)

2. **Export/Import Round-Trip Test**
   - Export current data
   - Clear app data
   - Import backup
   - Verify all data restored correctly

3. **Template Management Test**
   - Add custom templates
   - Reorder templates
   - Delete templates
   - Verify changes persist and reflect in TODO creation

**Deliverables:**
- All advanced features functional
- No data loss during export/import

---

## Phase 5: Background Service & Notifications (3-4 Tage)

### Ziel: Automatisches Email-Senden

### 5.1: Notifications Service (Tag 13)

**Tasks:**
1. **Notification Setup**
   - flutter_local_notifications config
   - Channel erstellen
   - Show notification

**Files:**
```
lib/services/notifications/
  └── notification_service.dart
```

**Tests:**
- Notification appears
- Tap action works

---

### 5.2: Background Service (Tag 13-14)

**Tasks:**
1. **WorkManager Integration**
   - Periodic Check (15min)
   - One-time Tasks

2. **AlarmManager für Exact Sends**
   - Calculate next global send
   - Set ExactAlarm

**Files:**
```
lib/services/background/
  ├── background_service.dart
  ├── alarm_service.dart
  └── work_manager_task.dart
```

**Tests:**
- Mock: Alarm gesetzt korrekt
- Integration: Email gesendet im Hintergrund

---

### 5.3: Offline Handling (Tag 14-15)

**Tasks:**
1. **Connectivity Check**
   - Pending Send Flag
   - Retry on online

**Files:**
```
lib/services/network/
  └── connectivity_service.dart
```

**Validation:**
- Offline: TODO als pending markiert
- Online: TODO gesendet automatisch

---

### 5.4: 7-Tage Inaktivität (Tag 15)

**Tasks:**
1. **App Lifecycle**
   - last_opened tracking
   - Check on app start
   - Pause all TODOs wenn > 7 Tage
   - Dialog "Resume All" / "Keep Paused"

**Files:**
```
lib/services/lifecycle/
  └── app_lifecycle_service.dart

lib/presentation/widgets/
  └── inactivity_dialog.dart
```

**Validation:**
- Simuliere 7+ Tage (via DB manipulation)
- TODOs pausiert
- Notification gezeigt
- Dialog erscheint bei App-Start

---

### 5.5: Phase 5 Validation (Tag 15-16)

**Tasks:**
1. **Background Send Test (Real Device)**
   - TODO erstellen mit next_send in 5 Minuten
   - App schließen (nicht nur minimieren)
   - Warten bis Alarm triggert
   - Email sollte gesendet werden
   - Notification sollte erscheinen

2. **Offline Scenario Test**
   - Airplane Mode aktivieren
   - Alarm triggert → TODO als pending markiert
   - Airplane Mode deaktivieren
   - Email wird automatisch nachgesendet

3. **Battery Optimization Test**
   - Prüfen ob App von Battery Saver ausgenommen
   - Test nach Device Reboot
   - Test nach App Update (Simulation)

4. **Multi-Device Testing**
   - Test auf Android 10, 12, 13, 14
   - Verschiedene Hersteller (Samsung, Pixel, etc.)

**Deliverables:**
- Background Service funktioniert zuverlässig
- Emails werden pünktlich (±15 min) gesendet
- App überlebt Reboots

**Known Issues to Document:**
- Manche Hersteller (Xiaomi, Huawei) haben aggressive Battery Optimization
- User muss ggf. manuell App whitelisten

---

## Phase 6: Polish & Testing (2-3 Tage)

### 6.1: UI Polish (Tag 16)

**Tasks:**
1. **Animations**
   - Screen transitions (Slide from right)
   - List item animations (Fade in + Slide up on load)
   - Swipe animations (Slide + Color change)
   - Button ripple effects
   - Loading spinner animations
   - Success/Error feedback animations

2. **Loading States**
   - Main Screen: Skeleton loading für TODO Liste
   - Create/Edit: Button loading während Save
   - Settings: Loading während SMTP Test
   - Statistics: Skeleton loading für Daten

3. **Error States**
   - Network error screens
   - SMTP error handling mit Retry
   - Database error handling
   - Empty search results

4. **Accessibility**
   - Touch targets ≥ 48dp
   - Color contrast WCAG AA
   - Screen reader labels (semanticsLabel)
   - Focus indicators

---

### 6.2: Integration Testing (Tag 16-17)

**Tasks:**
- Complete User Flows testen:
  1. Create TODO → Send Email → Complete
  2. Pause/Resume Flow
  3. Delete mit Confirmation
  4. Export/Import Flow

**Files:**
```
integration_test/
  ├── todo_flow_test.dart
  ├── settings_flow_test.dart
  └── export_import_test.dart
```

---

### 6.3: Bug Fixes & Edge Cases (Tag 17-18)

**Tasks:**
- Fix alle gefundenen Bugs
- Edge Cases handlen:
  - Leere Listen
  - Sehr lange Texte
  - Viele TODOs (> 100)
  - Netzwerk-Fehler
  - DB-Fehler

---

## Phase 7: Release Preparation (1-2 Tage)

### 7.1: App Icon & Splash Screen (Tag 18)

**Tasks:**
- App Icon erstellen (512x512)
- Splash Screen (optional)
- App Name final

---

### 7.2: Build Release APK (Tag 18-19)

**Tasks:**
1. **Signing Configuration**
   - Keystore erstellen
   - build.gradle config

2. **Build Release**
```bash
   flutter build apk --release
```

3. **Test Release APK**
   - Auf echtem Gerät installieren
   - Alle Features testen
   - Performance check

---

### 7.3: Documentation (Tag 19)

**Tasks:**
- README.md für User
- CHANGELOG.md
- LICENSE
- Privacy Policy (falls nötig)

---

## Timeline Summary

| Phase | Dauer | Deliverable |
|-------|-------|-------------|
| 0. Project Setup | 1-2 Tage | Flutter, Android Studio, Project Structure, Git |
| 1. Infrastructure | 3-5 Tage | DB, Models, Repos, DI |
| 2. Business Logic | 4-5 Tage | Use Cases, Email Service, Placeholder, SMTP |
| 3. UI Foundation | 5-6 Tage | Theme, Main Screen, Create/Edit, Settings, First Launch, Manual Send |
| 4. Advanced Features | 3-4 Tage | Stats, Templates, Export/Import |
| 5. Background | 3-4 Tage | Auto-Send, Notifications, Offline, 7-Day Check |
| 6. Polish & Test | 2-3 Tage | Integration Tests, Animations, Fixes |
| 7. Release Prep | 1-2 Tage | APK Signing, Docs |
| **Total** | **22-31 Tage** | **v1.0 Release** |

**Realistic Estimate:** 5-7 Wochen (working solo, part-time)

### Dependency Graph (Critical Path)

```
Phase 0 (Setup)
    ↓
Phase 1 (DB, Models) ──────────────────────┐
    ↓                                       │
Phase 2 (Business Logic) ──────────────────┤
    ↓                                       │
Phase 3.1-3.2 (Theme, Main Screen)         │
    ↓                                       │
Phase 3.3 (Create/Edit) ← depends on 2.2   │
    ↓                                       │
Phase 3.4 (Settings) ← depends on 2.3, 2.4 │
    ↓                                       │
Phase 3.5 (First Launch) ← depends on 3.4  │
    ↓                                       │
Phase 3.6 (Manual Send) ← depends on 2.5   │
    ↓                                       │
Phase 4 (Advanced) ← can start parallel    │
    ↓                                       │
Phase 5 (Background) ← depends on Phase 3  │
    ↓                                       │
Phase 6-7 (Polish, Release)                │
```

---

## Development Best Practices

### 1. Git Workflow

**Branch Strategy:**
```
main (protected, always releasable)
  ← develop (integration branch)
      ← feature/database-layer
      ← feature/main-screen-ui
      ← feature/background-service
      etc.
```

**Commit Messages:**
```
feat: Add TODO list screen
fix: Resolve swipe gesture issue
refactor: Improve database query performance
test: Add unit tests for TodoBloc
docs: Update README with setup instructions
```

**Pull Requests:**
- Jedes Feature = eigener Branch
- PR zu develop
- Self-review vor merge
- Tests müssen grün sein

---

### 2. Testing Strategy

**Unit Tests:**
- Für jede Use Case
- Für jeden Service
- Für kritische Utils

**Widget Tests:**
- Für komplexe Widgets
- Für Custom Inputs

**Integration Tests:**
- Für User Flows
- End-to-End

**Manual Testing:**
- Auf echtem Gerät
- Verschiedene Android-Versionen
- Edge Cases

**Coverage Goal:** 70%+ für core business logic

---

### 3. Code Quality

**Linting:**
```yaml
# analysis_options.yaml
include: package:flutter_lints/flutter.yaml

linter:
  rules:
    - always_declare_return_types
    - always_require_non_null_named_parameters
    - avoid_print
    - prefer_const_constructors
    - prefer_final_fields
```

**Code Review Checklist:**
- [ ] Linter errors resolved
- [ ] Tests passing
- [ ] No hardcoded strings (use constants)
- [ ] Error handling implemented
- [ ] Null safety correct
- [ ] Performance OK (no N+1 queries)

---

### 4. Performance Monitoring

**Track:**
- App startup time (< 3 seconds)
- Screen transition time (< 300ms)
- Database query time (< 100ms)
- APK size (< 30 MB)

**Tools:**
- Flutter DevTools
- Android Profiler
- `flutter analyze`
- `flutter run --profile`

---

## Risk Mitigation

### Hohe Risiken:

**1. Background Service funktioniert nicht zuverlässig**
- **Mitigation:** Früh testen auf echtem Gerät
- **Fallback:** User muss App öffnen für Sends
- **Alternative:** Firebase Cloud Messaging

**2. SMTP blockiert/Spam**
- **Mitigation:** Gute Templates, Zeitrandomisierung
- **Fallback:** User muss App-Passwort neu konfigurieren
- **Dokumentation:** Help-Links für Provider

**3. Zu komplexe UI (zu viel Zeit)**
- **Mitigation:** MVP zuerst (Phase 3)
- **Nice-to-have:** Template Management kann später
- **Priorisierung:** Core Features > Polish

**4. Performance-Probleme bei vielen TODOs**
- **Mitigation:** Pagination implementieren
- **Monitoring:** Test mit 500+ TODOs
- **Optimierung:** Lazy Loading, Indices

---

## Success Criteria

### MVP (Phase 3 Ende):
- [ ] TODO erstellen, bearbeiten, löschen
- [ ] Email manuell senden
- [ ] Settings konfigurieren
- [ ] App stabil, keine Crashes

### v1.0 (Phase 7 Ende):
- [ ] Automatisches Email-Senden
- [ ] Background Service funktioniert
- [ ] Alle Features aus Spec implementiert
- [ ] < 5 kritische Bugs
- [ ] APK < 30 MB
- [ ] 70%+ Test Coverage

### Release Ready:
- [ ] On 3+ echten Geräten getestet
- [ ] Dokumentation vollständig
- [ ] Privacy Policy (falls required)
- [ ] Release APK signed

---

## Post-v1.0 Roadmap (Optional)

**v1.1:**
- Dark Mode
- Multi-Language UI (DE + EN)
- Email Response Detection (IMAP)

**v1.2:**
- Widget für Home Screen
- Batch Operations
- Advanced Statistics

**v2.0:**
- Cloud Backup (Google Drive)
- Template Sharing
- Email Attachments

---

**Ende DevelopmentPlan.md**