# Task 048: Test SendEmailUseCase

## Phase
2 - Core Business Logic (Testing)

## Description
Write comprehensive tests for the SendEmailUseCase.

## Steps
1. Create `test/domain/usecases/email/send_email_usecase_test.dart`
2. Mock all dependencies
3. Test complete flow and edge cases

## Test Cases
```dart
@GenerateMocks([
  TodoRepository,
  SettingsRepository,
  EmailService,
  TemplateService,
  PlaceholderService,
])
void main() {
  late SendEmailUseCase useCase;
  late MockTodoRepository mockTodoRepo;
  late MockSettingsRepository mockSettingsRepo;
  late MockEmailService mockEmailService;
  late MockTemplateService mockTemplateService;
  late MockPlaceholderService mockPlaceholderService;

  setUp(() {
    mockTodoRepo = MockTodoRepository();
    mockSettingsRepo = MockSettingsRepository();
    mockEmailService = MockEmailService();
    mockTemplateService = MockTemplateService();
    mockPlaceholderService = MockPlaceholderService();

    useCase = SendEmailUseCase(
      mockTodoRepo,
      mockSettingsRepo,
      mockEmailService,
      mockTemplateService,
      mockPlaceholderService,
    );
  });

  group('SendEmailUseCase', () {
    test('should return failure when TODO not found', () async {
      when(mockTodoRepo.getTodoById(any)).thenAnswer((_) async => null);

      final result = await useCase.execute(todoId: 1);

      expect(result.isFailure, true);
      expect(result.error, 'TODO not found');
    });

    test('should return failure when TODO is paused', () async {
      when(mockTodoRepo.getTodoById(any))
          .thenAnswer((_) async => createTestTodo(isPaused: true));

      final result = await useCase.execute(todoId: 1);

      expect(result.isFailure, true);
      expect(result.error, contains('paused'));
    });

    test('should return failure when TODO is completed', () async {
      when(mockTodoRepo.getTodoById(any))
          .thenAnswer((_) async => createTestTodo(isCompleted: true));

      final result = await useCase.execute(todoId: 1);

      expect(result.isFailure, true);
      expect(result.error, contains('completed'));
    });

    test('should return failure when max follow-ups reached', () async {
      when(mockTodoRepo.getTodoById(any))
          .thenAnswer((_) async => createTestTodo());
      when(mockSettingsRepo.getSettings())
          .thenAnswer((_) async => createTestSettings(maxFollowUps: 10));
      when(mockTodoRepo.getSendCount(any))
          .thenAnswer((_) async => 10);

      final result = await useCase.execute(todoId: 1);

      expect(result.isFailure, true);
      expect(result.error, contains('Maximum'));
    });

    test('should send email and save record on success', () async {
      // Setup mocks for successful flow
      when(mockTodoRepo.getTodoById(any))
          .thenAnswer((_) async => createTestTodo());
      when(mockSettingsRepo.getSettings())
          .thenAnswer((_) async => createTestSettings());
      when(mockTodoRepo.getSendCount(any))
          .thenAnswer((_) async => 0);
      when(mockTodoRepo.getLastSentEmail(any))
          .thenAnswer((_) async => null);
      when(mockTemplateService.getTemplate(
        sendCount: anyNamed('sendCount'),
        isSubject: anyNamed('isSubject'),
        language: anyNamed('language'),
      )).thenAnswer((_) async => 'Template text');
      when(mockPlaceholderService.replace(
        template: anyNamed('template'),
        data: anyNamed('data'),
      )).thenReturn('Replaced text');
      when(mockEmailService.sendEmail(
        fromEmail: anyNamed('fromEmail'),
        toEmail: anyNamed('toEmail'),
        subject: anyNamed('subject'),
        body: anyNamed('body'),
      )).thenAnswer((_) async => Result.success(null));
      when(mockTodoRepo.saveSentEmail(any))
          .thenAnswer((_) async => 1);
      when(mockTodoRepo.updateNextSend(any, any))
          .thenAnswer((_) async {});

      final result = await useCase.execute(todoId: 1);

      expect(result.isSuccess, true);
      verify(mockEmailService.sendEmail(
        fromEmail: anyNamed('fromEmail'),
        toEmail: anyNamed('toEmail'),
        subject: anyNamed('subject'),
        body: anyNamed('body'),
      )).called(1);
      verify(mockTodoRepo.saveSentEmail(any)).called(1);
      verify(mockTodoRepo.updateNextSend(any, any)).called(1);
    });

    test('should not save record when email fails', () async {
      when(mockTodoRepo.getTodoById(any))
          .thenAnswer((_) async => createTestTodo());
      when(mockSettingsRepo.getSettings())
          .thenAnswer((_) async => createTestSettings());
      when(mockTodoRepo.getSendCount(any))
          .thenAnswer((_) async => 0);
      when(mockTodoRepo.getLastSentEmail(any))
          .thenAnswer((_) async => null);
      when(mockTemplateService.getTemplate(
        sendCount: anyNamed('sendCount'),
        isSubject: anyNamed('isSubject'),
        language: anyNamed('language'),
      )).thenAnswer((_) async => 'Template');
      when(mockPlaceholderService.replace(
        template: anyNamed('template'),
        data: anyNamed('data'),
      )).thenReturn('Replaced');
      when(mockEmailService.sendEmail(
        fromEmail: anyNamed('fromEmail'),
        toEmail: anyNamed('toEmail'),
        subject: anyNamed('subject'),
        body: anyNamed('body'),
      )).thenAnswer((_) async => Result.failure('SMTP error'));

      final result = await useCase.execute(todoId: 1);

      expect(result.isFailure, true);
      verifyNever(mockTodoRepo.saveSentEmail(any));
      verifyNever(mockTodoRepo.updateNextSend(any, any));
    });
  });
}

// Helper functions
Todo createTestTodo({
  bool isPaused = false,
  bool isCompleted = false,
}) {
  return Todo(
    id: 1,
    recipientEmail: 'test@example.com',
    recipientFirstName: 'John',
    recipientLastName: 'Doe',
    subject: 'Test Subject',
    isPaused: isPaused,
    isCompleted: isCompleted,
    language: 'EN',
    intervalDays: 3,
    sendTime: TimeOfDay(hour: 9, minute: 0),
    createdAt: DateTime.now(),
  );
}

Settings createTestSettings({int maxFollowUps = 10}) {
  return Settings(
    smtpEmail: 'sender@example.com',
    maxFollowUps: maxFollowUps,
    randomizeMinutes: 30,
  );
}
```

## Acceptance Criteria
- [ ] Test TODO not found case
- [ ] Test paused TODO case
- [ ] Test completed TODO case
- [ ] Test max follow-ups reached
- [ ] Test successful send flow
- [ ] Test email failure doesn't save record
- [ ] All tests pass

## Dependencies
- Task 045 (SendEmailUseCase)

## Parallel Work
Must run after: Task 045

## Estimated Effort
2 hours
