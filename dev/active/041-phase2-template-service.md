# Task 041: Create TemplateService

## Phase
2 - Core Business Logic

## Description
Implement service for template selection based on send count.

## Steps
1. Create `lib/services/email/template_service.dart`
2. Implement template index calculation
3. Handle "already-sent-first" logic (skip index 0 after first send)
4. Implement fallback to last template when exceeded

## Code Structure
```dart
class TemplateService {
  final SettingsRepository _settingsRepository;

  TemplateService(this._settingsRepository);

  /// Gets the template index based on send count
  /// - First email (send_count=0): Use index 0 (initial template)
  /// - Second email (send_count=1): Use index 1 (first follow-up)
  /// - If send_count >= template count: Use last template
  Future<int> getTemplateIndex({
    required int sendCount,
    required bool isSubject,
    required String language,
  }) async {
    final settings = await _settingsRepository.getSettings();
    final templates = isSubject
      ? (language == 'DE' ? settings.subjectTemplatesDe : settings.subjectTemplatesEn)
      : (language == 'DE' ? settings.textTemplatesDe : settings.textTemplatesEn);

    if (sendCount >= templates.length) {
      return templates.length - 1; // Use last template
    }

    return sendCount;
  }

  /// Gets the actual template text for given send count
  Future<String> getTemplate({
    required int sendCount,
    required bool isSubject,
    required String language,
  }) async {
    final settings = await _settingsRepository.getSettings();
    final templates = isSubject
      ? (language == 'DE' ? settings.subjectTemplatesDe : settings.subjectTemplatesEn)
      : (language == 'DE' ? settings.textTemplatesDe : settings.textTemplatesEn);

    final index = await getTemplateIndex(
      sendCount: sendCount,
      isSubject: isSubject,
      language: language,
    );

    return templates[index];
  }

  /// Gets a random template for initial TODO creation
  Future<String> getRandomTemplate({
    required bool isSubject,
    required String language,
  }) async {
    final settings = await _settingsRepository.getSettings();
    final templates = isSubject
      ? (language == 'DE' ? settings.subjectTemplatesDe : settings.subjectTemplatesEn)
      : (language == 'DE' ? settings.textTemplatesDe : settings.textTemplatesEn);

    final random = Random();
    return templates[random.nextInt(templates.length)];
  }
}
```

## Acceptance Criteria
- [ ] Returns correct template index for send_count
- [ ] Falls back to last template when exceeded
- [ ] Supports both DE and EN languages
- [ ] Supports both subject and text templates
- [ ] Random template selection works

## Dependencies
- Task 026 (Repository Interfaces)
- Task 028 (Settings Repository Implementation)

## Parallel Work
Can run parallel with: Task 039, 040, 042

## Estimated Effort
1 hour
