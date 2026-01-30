# Task 040: Create EmailParsingService

## Phase
2 - Core Business Logic

## Description
Implement service to auto-extract first/last name from email addresses.

## Steps
1. Create `lib/services/email/email_parsing_service.dart`
2. Implement email parsing logic
3. Handle various separator patterns
4. Capitalize names correctly

## Code Structure
```dart
class EmailParsingService {
  static const List<String> _separators = ['.', '-', '_', ','];

  /// Extracts first and last name from email address
  /// Example: "john.doe@mail.com" -> ("John", "Doe")
  /// Example: "jane_smith@company.org" -> ("Jane", "Smith")
  (String firstName, String lastName) parseEmail(String email) {
    final localPart = email.split('@').first;

    // Try each separator
    for (final separator in _separators) {
      if (localPart.contains(separator)) {
        final parts = localPart.split(separator);
        if (parts.length >= 2) {
          return (
            _capitalize(parts[0]),
            _capitalize(parts[1]),
          );
        }
      }
    }

    // No separator found - return local part as first name
    return (_capitalize(localPart), '');
  }

  String _capitalize(String text) {
    if (text.isEmpty) return text;
    return text[0].toUpperCase() + text.substring(1).toLowerCase();
  }

  /// Validates email format
  bool isValidEmail(String email) {
    final regex = RegExp(r'^[\w\.-]+@[\w\.-]+\.\w{2,}$');
    return regex.hasMatch(email);
  }
}
```

## Test Cases
```dart
test('should parse email with dot separator', () {
  final service = EmailParsingService();
  final result = service.parseEmail('john.doe@mail.com');
  expect(result.$1, 'John');
  expect(result.$2, 'Doe');
});

test('should parse email with underscore', () {
  final result = service.parseEmail('jane_smith@company.org');
  expect(result.$1, 'Jane');
  expect(result.$2, 'Smith');
});

test('should handle email without separator', () {
  final result = service.parseEmail('admin@example.com');
  expect(result.$1, 'Admin');
  expect(result.$2, '');
});
```

## Acceptance Criteria
- [ ] Parses emails with dot separator
- [ ] Parses emails with dash separator
- [ ] Parses emails with underscore separator
- [ ] Handles emails without separators
- [ ] Capitalizes names correctly
- [ ] Email validation works

## Dependencies
- None

## Parallel Work
Can run parallel with: Task 039, 041, 042

## Estimated Effort
45 minutes
