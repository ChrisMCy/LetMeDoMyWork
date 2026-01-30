# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

LetMeDoMyWork is an Android Flutter app for automated follow-up email reminders. Users create TODO entries for email campaigns, and the app sends templated follow-up emails via SMTP at configurable intervals with human-like randomization.

**Current Status:** Phase 0 (Project Setup) - Flutter SDK installed, Android Studio installation pending.

## Session Workflow

**At session start:**
1. Read `dev/session-context.md` for current state and blockers
2. Check `dev/active/` for next task (lowest numbered file)

**At session end:**
1. Update `dev/session-context.md` with progress, decisions, blockers
2. Use `/dev-docs-update` command if approaching context limits

## Task System

**Each task has 3 files** in `dev/active/` with the same prefix:
- `NNN-phaseX-task-name.md` - Main task (description, steps, acceptance criteria)
- `NNN-phaseX-task-name-context.md` - Implementation context and decisions
- `NNN-phaseX-task-name-tasks.md` - Checklist for tracking progress

**Execute tasks with:** `/task` command (picks lowest numbered pending task)

**Workflow:**
1. Read all 3 task files and understand acceptance criteria
2. Execute the work
3. **Code Review (for code tasks, skip for Phase 0 setup):**
   - Run Architecture Review Agent (check Clean Architecture, SOLID violations)
   - Run Refactor Planning Agent (identify code quality issues)
   - Fix any violations before proceeding
4. Mark acceptance criteria as complete (`- [x]`), add Completion Notes section
5. **Move ALL 3 task files from `dev/active/` to `dev/finished/`**
6. Update `dev/session-context.md`
7. Commit with: `Complete task NNN: [description]`

**IMPORTANT:** Always move ALL 3 files (main, context, tasks) to `dev/finished/`!

## Build & Development Commands

```bash
# Install dependencies
flutter pub get

# Run app (debug)
flutter run

# Run app (release)
flutter run --release

# Run all tests
flutter test

# Run single test file
flutter test test/path/to/test_file.dart

# Run tests with coverage
flutter test --coverage

# Analyze code (linting)
flutter analyze

# Format code
dart format lib/ test/

# Build release APK
flutter build apk --release

# Check Flutter setup
flutter doctor -v
```

## Architecture (Clean Architecture)

```
lib/
├── core/           # Constants, theme, utils, errors, DI, navigation
├── domain/         # Business logic (entities, repositories interfaces, use cases)
│                   # CRITICAL: Domain knows NO other layers!
├── data/           # Implementation (models, repository impls, datasources)
├── presentation/   # UI (screens, widgets, BLoC)
└── services/       # Cross-cutting (database, smtp, background, notifications)
```

**Dependency Rules:**
- Presentation → Domain (allowed)
- Data → Domain (implements interfaces)
- Domain → Data/Presentation (FORBIDDEN - domain is pure)

## Database

SQLite via `sqflite`. Three tables:
- `settings` (singleton, id=1) - App config, SMTP settings, template libraries
- `todos` - Email campaigns with scheduling
- `sent_emails` - History of sent emails (CASCADE delete with todos)

SMTP password stored separately in `flutter_secure_storage`.

## Key Packages

- **State:** flutter_bloc, equatable, get_it (DI)
- **Database:** sqflite, flutter_secure_storage
- **Email:** mailer (SMTP)
- **Background:** workmanager, flutter_local_notifications
- **Testing:** mockito, build_runner

## Code Quality Standards

**Test Coverage Requirements:**
- Domain/Use Cases: 90%+
- Data/Repositories: 80%+
- Services: 75%+
- Overall minimum: 70%

**Before committing:**
```bash
flutter analyze          # Must be clean
dart format lib/ test/   # Must be formatted
flutter test             # All tests green
```

**SOLID principles are mandatory.** Single Responsibility, Open/Closed, Liskov Substitution, Interface Segregation, Dependency Inversion.

## Placeholder System

Email templates support placeholders:
- `{Vorname}`, `{Nachname}` - Recipient name
- `{DateToday}`, `{DateLastMail}` - Dates (DD.MM.YYYY)
- `{InitialSubject}`, `{InitialText}` - Original email content
- `{DaysSinceLastMail}` - Integer days

## Testing Strategy

**TDD Cycle:** RED (failing test) → GREEN (minimal code) → REFACTOR

```dart
// AAA Pattern
test('should do something', () {
  // Arrange
  final input = ...;

  // Act
  final result = doSomething(input);

  // Assert
  expect(result, expected);
});
```

**Factory pattern rule:** Factory values should differ from domain defaults to catch persistence bugs.

## Code Review Agents

After writing code (not for Phase 0 setup tasks), spawn these agents:

**Architecture Review Agent** (subagent_type="general-purpose"):
- Checks Clean Architecture layer violations
- Verifies SOLID principle compliance
- Ensures dependencies point inward only
- Reports any violations to fix

**Refactor Planning Agent** (subagent_type="Plan"):
- Identifies functions > 30 lines, classes > 200 lines
- Finds duplicate code and missing abstractions
- Creates refactor plan if issues found
- Confirms code is clean if no issues

**Rule:** Fix violations before committing. Create follow-up tasks for larger refactoring.

## Available Commands

- `/task` - Execute next pending task from dev/active
- `/dev-docs` - Create comprehensive strategic plan
- `/dev-docs-update` - Update documentation before context compaction

## Important Patterns

**Name Parsing:** Email local-part is split by first `.`, `-`, `_`, or `,` → capitalized first/last name.

**Send Time Calculation:**
```
actual_time = base_time + random(-max_random_minutes/2, +max_random_minutes/2)
```

**Template Selection:** Based on send_count. If `already_sent_first=true`, skip index 0.

## Windows Development Notes

- Flutter SDK: `C:\src\flutter`
- Use PowerShell for Flutter commands
- Paths use backslashes in Windows but forward slashes in Dart code
