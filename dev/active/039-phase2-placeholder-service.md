# Task 039: Create PlaceholderService

## Phase
2 - Core Business Logic

## Description
Implement the service for replacing placeholders in email templates.

## Steps
1. Create `lib/services/email/placeholder_service.dart`
2. Implement replace logic for all placeholders
3. Handle missing data gracefully (empty string fallback)

## Supported Placeholders
- `{Vorname}` - First name
- `{Nachname}` - Last name
- `{DateToday}` - Current date
- `{DateLastMail}` - Date of last sent email
- `{InitialSubject}` - Original subject line
- `{DaysSinceLastMail}` - Days since last email
- `{InitialText}` - Original email body

## Code Structure
```dart
class PlaceholderService {
  String replace({
    required String template,
    required Map<String, dynamic> data,
  }) {
    String result = template;

    result = result.replaceAll('{Vorname}', data['firstName'] ?? '');
    result = result.replaceAll('{Nachname}', data['lastName'] ?? '');
    result = result.replaceAll('{DateToday}', _formatDate(DateTime.now()));
    result = result.replaceAll('{DateLastMail}',
      data['lastMailDate'] != null ? _formatDate(data['lastMailDate']) : '');
    result = result.replaceAll('{InitialSubject}', data['initialSubject'] ?? '');
    result = result.replaceAll('{DaysSinceLastMail}',
      _calculateDaysSince(data['lastMailDate']));
    result = result.replaceAll('{InitialText}', data['initialText'] ?? '');

    return result;
  }

  String _formatDate(DateTime date) {
    return DateFormat('dd.MM.yyyy').format(date);
  }

  String _calculateDaysSince(DateTime? lastDate) {
    if (lastDate == null) return '';
    return DateTime.now().difference(lastDate).inDays.toString();
  }
}
```

## Acceptance Criteria
- [ ] All placeholders correctly replaced
- [ ] Missing data returns empty string (no crash)
- [ ] Date formatting consistent (dd.MM.yyyy)
- [ ] Days calculation accurate

## Dependencies
- Task 007 (pubspec with intl package)

## Parallel Work
Can run parallel with: Task 040, 041, 042

## Estimated Effort
1 hour
