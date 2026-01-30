# Task 046: Create GetSentEmailsUseCase

## Phase
2 - Core Business Logic

## Description
Implement use case for retrieving sent emails for a TODO.

## Steps
1. Create `lib/domain/usecases/email/get_sent_emails_usecase.dart`
2. Implement retrieval with sorting (newest first)

## Code Structure
```dart
class GetSentEmailsUseCase {
  final TodoRepository _repository;

  GetSentEmailsUseCase(this._repository);

  /// Get all sent emails for a specific TODO
  Future<List<SentEmail>> execute({required int todoId}) async {
    final sentEmails = await _repository.getSentEmailsByTodoId(todoId);

    // Sort by sent_at descending (newest first)
    sentEmails.sort((a, b) => b.sentAt.compareTo(a.sentAt));

    return sentEmails;
  }

  /// Get the last sent email for a TODO
  Future<SentEmail?> getLastSentEmail({required int todoId}) async {
    return await _repository.getLastSentEmail(todoId);
  }

  /// Get send count for a TODO
  Future<int> getSendCount({required int todoId}) async {
    return await _repository.getSendCount(todoId);
  }
}
```

## Acceptance Criteria
- [ ] Returns sent emails sorted by date (newest first)
- [ ] getLastSentEmail returns most recent or null
- [ ] getSendCount returns correct count
- [ ] Empty list returned for TODO with no sent emails

## Dependencies
- Task 026 (Repository Interfaces)
- Task 027 (TodoRepository Implementation)

## Parallel Work
Can run parallel with: Task 045

## Estimated Effort
30 minutes
