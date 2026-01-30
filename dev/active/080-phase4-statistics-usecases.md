# Task 080: Create Statistics Use Cases

## Phase
4 - Advanced Features

## Description
Implement use cases for calculating statistics.

## Steps
1. Create `lib/domain/usecases/statistics/` directory
2. Implement GetOverallStatsUseCase
3. Implement GetRecipientStatsUseCase
4. Implement GetTemplateStatsUseCase

## Code Structure

### get_overall_stats_usecase.dart
```dart
class OverallStats {
  final int totalTodos;
  final int activeTodos;
  final int completedTodos;
  final int pausedTodos;
  final int totalEmailsSent;
  final double avgEmailsPerTodo;
  final int todosThisWeek;
  final int emailsThisWeek;

  OverallStats({
    required this.totalTodos,
    required this.activeTodos,
    required this.completedTodos,
    required this.pausedTodos,
    required this.totalEmailsSent,
    required this.avgEmailsPerTodo,
    required this.todosThisWeek,
    required this.emailsThisWeek,
  });
}

class GetOverallStatsUseCase {
  final TodoRepository _todoRepository;

  GetOverallStatsUseCase(this._todoRepository);

  Future<OverallStats> execute() async {
    final allTodos = await _todoRepository.getAllTodos();
    final activeTodos = allTodos.where((t) => !t.isCompleted && !t.isPaused).length;
    final completedTodos = allTodos.where((t) => t.isCompleted).length;
    final pausedTodos = allTodos.where((t) => t.isPaused).length;

    int totalEmailsSent = 0;
    for (final todo in allTodos) {
      totalEmailsSent += await _todoRepository.getSendCount(todo.id!);
    }

    final avgEmails = allTodos.isNotEmpty
        ? totalEmailsSent / allTodos.length
        : 0.0;

    // This week stats
    final weekAgo = DateTime.now().subtract(const Duration(days: 7));
    final todosThisWeek = allTodos
        .where((t) => t.createdAt.isAfter(weekAgo))
        .length;

    final emailsThisWeek = await _todoRepository.getEmailsSentSince(weekAgo);

    return OverallStats(
      totalTodos: allTodos.length,
      activeTodos: activeTodos,
      completedTodos: completedTodos,
      pausedTodos: pausedTodos,
      totalEmailsSent: totalEmailsSent,
      avgEmailsPerTodo: avgEmails,
      todosThisWeek: todosThisWeek,
      emailsThisWeek: emailsThisWeek,
    );
  }
}
```

### get_recipient_stats_usecase.dart
```dart
class RecipientStats {
  final String email;
  final String? firstName;
  final String? lastName;
  final int todoCount;
  final int totalEmailsSent;
  final int completedCount;

  RecipientStats({
    required this.email,
    this.firstName,
    this.lastName,
    required this.todoCount,
    required this.totalEmailsSent,
    required this.completedCount,
  });
}

class GetRecipientStatsUseCase {
  final TodoRepository _todoRepository;

  GetRecipientStatsUseCase(this._todoRepository);

  Future<List<RecipientStats>> execute() async {
    final allTodos = await _todoRepository.getAllTodos();

    // Group by email
    final Map<String, List<Todo>> byRecipient = {};
    for (final todo in allTodos) {
      byRecipient.putIfAbsent(todo.recipientEmail, () => []).add(todo);
    }

    final stats = <RecipientStats>[];
    for (final entry in byRecipient.entries) {
      int totalSent = 0;
      int completed = 0;

      for (final todo in entry.value) {
        totalSent += await _todoRepository.getSendCount(todo.id!);
        if (todo.isCompleted) completed++;
      }

      stats.add(RecipientStats(
        email: entry.key,
        firstName: entry.value.first.recipientFirstName,
        lastName: entry.value.first.recipientLastName,
        todoCount: entry.value.length,
        totalEmailsSent: totalSent,
        completedCount: completed,
      ));
    }

    // Sort by total emails sent (descending)
    stats.sort((a, b) => b.totalEmailsSent.compareTo(a.totalEmailsSent));

    return stats;
  }
}
```

### get_template_stats_usecase.dart
```dart
class TemplateStats {
  final int templateIndex;
  final int usageCount;
  final String sampleText;

  TemplateStats({
    required this.templateIndex,
    required this.usageCount,
    required this.sampleText,
  });
}

class GetTemplateStatsUseCase {
  final TodoRepository _todoRepository;
  final SettingsRepository _settingsRepository;

  GetTemplateStatsUseCase(this._todoRepository, this._settingsRepository);

  Future<List<TemplateStats>> execute({
    required bool isSubject,
    required String language,
  }) async {
    final sentEmails = await _todoRepository.getAllSentEmails();
    final settings = await _settingsRepository.getSettings();

    // Count usage by template index
    final Map<int, int> usageCount = {};
    for (final email in sentEmails) {
      usageCount.update(
        email.templateIndexUsed,
        (count) => count + 1,
        ifAbsent: () => 1,
      );
    }

    // Get templates
    final templates = isSubject
        ? (language == 'DE'
            ? settings.subjectTemplatesDe
            : settings.subjectTemplatesEn)
        : (language == 'DE'
            ? settings.textTemplatesDe
            : settings.textTemplatesEn);

    final stats = <TemplateStats>[];
    for (int i = 0; i < templates.length; i++) {
      stats.add(TemplateStats(
        templateIndex: i,
        usageCount: usageCount[i] ?? 0,
        sampleText: templates[i].substring(0, min(50, templates[i].length)),
      ));
    }

    return stats;
  }
}
```

## Acceptance Criteria
- [ ] OverallStats calculates all metrics correctly
- [ ] RecipientStats groups by email and calculates totals
- [ ] TemplateStats shows usage count per template
- [ ] Efficient queries (avoid N+1 where possible)
- [ ] This week stats use correct date range

## Dependencies
- Task 026-028 (Repositories)

## Parallel Work
Can run parallel with: Task 081

## Estimated Effort
2-3 hours
