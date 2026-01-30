# Task 045: Create SendEmailUseCase

## Phase
2 - Core Business Logic

## Description
Implement the complete send email flow use case.

## Steps
1. Create `lib/domain/usecases/email/send_email_usecase.dart`
2. Integrate template selection, placeholder replacement, SMTP send
3. Save to sent_emails table
4. Update TODO's next_send_datetime

## Code Structure
```dart
class SendEmailUseCase {
  final TodoRepository _todoRepository;
  final SettingsRepository _settingsRepository;
  final EmailService _emailService;
  final TemplateService _templateService;
  final PlaceholderService _placeholderService;

  SendEmailUseCase(
    this._todoRepository,
    this._settingsRepository,
    this._emailService,
    this._templateService,
    this._placeholderService,
  );

  Future<Result<void>> execute({required int todoId}) async {
    // 1. Get TODO
    final todo = await _todoRepository.getTodoById(todoId);
    if (todo == null) {
      return Result.failure('TODO not found');
    }

    if (todo.isPaused) {
      return Result.failure('Cannot send email for paused TODO');
    }

    if (todo.isCompleted) {
      return Result.failure('Cannot send email for completed TODO');
    }

    // 2. Get settings
    final settings = await _settingsRepository.getSettings();

    // 3. Get send count
    final sendCount = await _todoRepository.getSendCount(todoId);

    // 4. Check max sends
    if (sendCount >= settings.maxFollowUps) {
      return Result.failure('Maximum follow-ups reached');
    }

    // 5. Get templates
    final subjectTemplate = await _templateService.getTemplate(
      sendCount: sendCount,
      isSubject: true,
      language: todo.language,
    );

    final textTemplate = await _templateService.getTemplate(
      sendCount: sendCount,
      isSubject: false,
      language: todo.language,
    );

    // 6. Get last sent email for placeholder data
    final lastSentEmail = await _todoRepository.getLastSentEmail(todoId);

    // 7. Replace placeholders
    final placeholderData = {
      'firstName': todo.recipientFirstName,
      'lastName': todo.recipientLastName,
      'initialSubject': todo.subject,
      'initialText': todo.initialText,
      'lastMailDate': lastSentEmail?.sentAt,
    };

    final subject = _placeholderService.replace(
      template: subjectTemplate,
      data: placeholderData,
    );

    final body = _placeholderService.replace(
      template: textTemplate,
      data: placeholderData,
    );

    // 8. Send email
    final sendResult = await _emailService.sendEmail(
      fromEmail: settings.smtpEmail,
      toEmail: todo.recipientEmail,
      subject: subject,
      body: body,
    );

    if (sendResult.isFailure) {
      return sendResult;
    }

    // 9. Save to sent_emails
    final sentEmail = SentEmail(
      todoId: todoId,
      subject: subject,
      text: body,
      templateIndexUsed: sendCount,
      sentAt: DateTime.now(),
    );
    await _todoRepository.saveSentEmail(sentEmail);

    // 10. Calculate and update next_send_datetime
    final nextSend = _calculateNextSend(
      currentDate: DateTime.now(),
      sendTime: todo.sendTime,
      intervalDays: todo.intervalDays,
      randomizeMinutes: settings.randomizeMinutes,
    );

    await _todoRepository.updateNextSend(todoId, nextSend);

    return Result.success(null);
  }

  DateTime _calculateNextSend({
    required DateTime currentDate,
    required TimeOfDay sendTime,
    required int intervalDays,
    required int randomizeMinutes,
  }) {
    final random = Random();
    final randomOffset = random.nextInt(randomizeMinutes * 2) - randomizeMinutes;

    var nextDate = currentDate.add(Duration(days: intervalDays));
    nextDate = DateTime(
      nextDate.year,
      nextDate.month,
      nextDate.day,
      sendTime.hour,
      sendTime.minute + randomOffset,
    );

    return nextDate;
  }
}
```

## Acceptance Criteria
- [ ] Validates TODO exists and is active
- [ ] Checks max follow-ups limit
- [ ] Selects correct template based on send_count
- [ ] Replaces all placeholders correctly
- [ ] Sends email via SMTP
- [ ] Saves sent_email record
- [ ] Updates next_send_datetime with randomization
- [ ] Returns appropriate errors for each failure case

## Dependencies
- Task 026-028 (Repositories)
- Task 039 (PlaceholderService)
- Task 041 (TemplateService)
- Task 044 (EmailService)

## Parallel Work
Must run after: Task 039, 041, 044

## Estimated Effort
2-3 hours
