# Task 049: Phase 2 Validation

## Phase
2 - Core Business Logic (Validation)

## Description
Validate all Phase 2 deliverables before moving to UI phase.

## Steps
1. Run all unit tests
2. Check test coverage
3. Perform integration test of email flow
4. Manual SMTP test with real accounts

## Validation Checklist

### 1. Unit Test Coverage
```bash
flutter test --coverage
# Target: 80%+ for domain/ and services/
```

### 2. All Tests Pass
```bash
flutter test
# Expected: All tests green
```

### 3. Integration Test: Email Flow
```dart
// Run manually or as integration test
void main() async {
  // Setup
  await setupDependencyInjection();

  // Create TODO
  final todoRepo = getIt<TodoRepository>();
  final todoId = await todoRepo.createTodo(Todo(
    recipientEmail: 'test@example.com',
    recipientFirstName: 'John',
    recipientLastName: 'Doe',
    subject: 'Test Subject',
    language: 'EN',
    intervalDays: 3,
    sendTime: TimeOfDay(hour: 9, minute: 0),
  ));

  // Send email (will fail without SMTP, but flow should work)
  final sendUseCase = getIt<SendEmailUseCase>();
  final result = await sendUseCase.execute(todoId: todoId);

  // Verify sent_emails (if SMTP configured)
  if (result.isSuccess) {
    final sentEmails = await todoRepo.getSentEmailsByTodoId(todoId);
    assert(sentEmails.length == 1);

    final updatedTodo = await todoRepo.getTodoById(todoId);
    assert(updatedTodo!.nextSendDateTime != null);
  }

  print('Integration test completed!');
}
```

### 4. Manual SMTP Tests
- [ ] Test with Gmail account (requires App Password)
- [ ] Test with Outlook account (requires App Password)
- [ ] Verify email arrives in recipient inbox
- [ ] Verify subject and body are correct
- [ ] Verify sender address is correct

### 5. Code Quality Check
```bash
flutter analyze
# Expected: No errors, minimal warnings
```

## Acceptance Criteria
- [ ] All unit tests pass
- [ ] Test coverage >= 80% for business logic
- [ ] Integration test passes
- [ ] Manual SMTP test successful with at least one provider
- [ ] No lint errors
- [ ] All use cases return proper Result types

## Deliverables
- Core business logic fully implemented
- Email can be sent via SMTP
- Placeholder replacement works
- Template selection works
- All services have unit tests

## Dependencies
- Task 033-048 (All Phase 2 tasks)

## Next Phase
Phase 3: UI Foundation & MVP

## Estimated Effort
2-3 hours
