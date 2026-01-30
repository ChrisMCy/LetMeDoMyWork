# Task 047: Test Email Services

## Phase
2 - Core Business Logic (Testing)

## Description
Write unit tests for all email-related services.

## Steps
1. Create `test/services/email/` directory
2. Create test file for each service
3. Mock dependencies using Mockito

## Test Files
```
test/services/email/
  ├── placeholder_service_test.dart
  ├── email_parsing_service_test.dart
  └── template_service_test.dart

test/services/smtp/
  ├── smtp_config_service_test.dart
  └── email_service_test.dart

test/services/storage/
  └── secure_storage_service_test.dart
```

## Test Cases

### PlaceholderService Tests
```dart
group('PlaceholderService', () {
  late PlaceholderService service;

  setUp(() {
    service = PlaceholderService();
  });

  test('should replace {Vorname} placeholder', () {
    final result = service.replace(
      template: 'Hallo {Vorname}',
      data: {'firstName': 'John'},
    );
    expect(result, 'Hallo John');
  });

  test('should replace multiple placeholders', () {
    final result = service.replace(
      template: 'Hi {Vorname} {Nachname}, regarding {InitialSubject}',
      data: {
        'firstName': 'John',
        'lastName': 'Doe',
        'initialSubject': 'Project X',
      },
    );
    expect(result, 'Hi John Doe, regarding Project X');
  });

  test('should return empty string for missing data', () {
    final result = service.replace(
      template: 'Hi {Vorname}',
      data: {},
    );
    expect(result, 'Hi ');
  });

  test('should format date correctly', () {
    final result = service.replace(
      template: 'Today is {DateToday}',
      data: {},
    );
    expect(result, matches(r'Today is \d{2}\.\d{2}\.\d{4}'));
  });

  test('should calculate days since last mail', () {
    final result = service.replace(
      template: 'It has been {DaysSinceLastMail} days',
      data: {
        'lastMailDate': DateTime.now().subtract(Duration(days: 5)),
      },
    );
    expect(result, 'It has been 5 days');
  });
});
```

### EmailParsingService Tests
```dart
group('EmailParsingService', () {
  late EmailParsingService service;

  setUp(() {
    service = EmailParsingService();
  });

  test('should parse dot-separated email', () {
    final result = service.parseEmail('john.doe@example.com');
    expect(result.$1, 'John');
    expect(result.$2, 'Doe');
  });

  test('should parse underscore-separated email', () {
    final result = service.parseEmail('jane_smith@company.org');
    expect(result.$1, 'Jane');
    expect(result.$2, 'Smith');
  });

  test('should parse dash-separated email', () {
    final result = service.parseEmail('bob-johnson@mail.com');
    expect(result.$1, 'Bob');
    expect(result.$2, 'Johnson');
  });

  test('should handle email without separator', () {
    final result = service.parseEmail('admin@example.com');
    expect(result.$1, 'Admin');
    expect(result.$2, '');
  });

  test('should validate correct email', () {
    expect(service.isValidEmail('test@example.com'), true);
    expect(service.isValidEmail('user.name@domain.co.uk'), true);
  });

  test('should reject invalid email', () {
    expect(service.isValidEmail('invalid'), false);
    expect(service.isValidEmail('no@domain'), false);
    expect(service.isValidEmail('@example.com'), false);
  });
});
```

### SmtpConfigService Tests
```dart
group('SmtpConfigService', () {
  late SmtpConfigService service;

  setUp(() {
    service = SmtpConfigService();
  });

  test('should return Gmail config', () {
    final config = service.getConfig(SmtpProvider.gmail);
    expect(config.host, 'smtp.gmail.com');
    expect(config.port, 587);
  });

  test('should detect Gmail from email', () {
    expect(service.detectProvider('user@gmail.com'), SmtpProvider.gmail);
    expect(service.detectProvider('user@googlemail.com'), SmtpProvider.gmail);
  });

  test('should detect Outlook from email', () {
    expect(service.detectProvider('user@outlook.com'), SmtpProvider.outlook);
    expect(service.detectProvider('user@hotmail.com'), SmtpProvider.outlook);
  });

  test('should return custom for unknown domain', () {
    expect(service.detectProvider('user@company.com'), SmtpProvider.custom);
  });
});
```

## Acceptance Criteria
- [ ] PlaceholderService tests (all placeholders, missing data)
- [ ] EmailParsingService tests (all separators, validation)
- [ ] TemplateService tests (index calculation, fallback)
- [ ] SmtpConfigService tests (provider configs, detection)
- [ ] SecureStorageService tests (save, load, delete)
- [ ] All tests pass

## Dependencies
- Task 039-044 (All email services)

## Parallel Work
Can run parallel with: Task 045, 046

## Estimated Effort
2-3 hours
