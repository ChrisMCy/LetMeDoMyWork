# Task 017: Create Default Templates

## Phase
1 - Core Infrastructure

## Description
Create the default email templates (30 DE + 30 EN subjects and texts).

## Steps
1. Create `lib/services/database/default_templates.dart`
2. Add 30 German subjects
3. Add 30 English subjects
4. Add 30 German texts
5. Add 30 English texts
6. Create method to get templates as JSON strings

## Code Structure
```dart
class DefaultTemplates {
  static List<String> get subjectsDe => [
    'Follow-Up: {InitialSubject}',
    'Nochmal bzgl.: {InitialSubject}',
    'Kurze Erinnerung: {InitialSubject}',
    // ... 27 more
  ];

  static List<String> get subjectsEn => [
    'Follow-up: {InitialSubject}',
    'Re: {InitialSubject}',
    'Quick reminder: {InitialSubject}',
    // ... 27 more
  ];

  static List<String> get textsDe => [
    '''Hallo {Vorname},

ich wollte kurz nachhaken bezüglich meiner Mail vom {DateLastMail}...

Viele Grüße''',
    // ... 29 more
  ];

  static List<String> get textsEn => [ ... ];

  static String get subjectsDeJson => jsonEncode(subjectsDe);
  // ... more JSON getters
}
```

## Acceptance Criteria
- [ ] 30 German subjects defined
- [ ] 30 English subjects defined
- [ ] 30 German texts defined
- [ ] 30 English texts defined
- [ ] All use correct placeholders
- [ ] JSON encoding works correctly
- [ ] Templates match DefaultTemplates.md

## Dependencies
- Task 013 (Validate Setup - Phase 0 complete)

## Parallel Work
Can run parallel with: Task 014, 015, 016

## Estimated Effort
2 hours

## References
- DefaultTemplates.md for all template content
