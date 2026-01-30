# LetMeDoMyWork - Code Quality Framework

## Overview

Dieses Dokument definiert verbindliche Code Quality Standards für das LetMeDoMyWork-Projekt. Alle Standards basieren auf bewährten Frameworks und sind **nicht verhandelbar**.

**Prinzip:** "Kein Code ohne Tests, kein Merge ohne Quality Gates"

---

## Quality Framework: SOLID + Clean Architecture + TDD

### Gewählte Frameworks & Standards:

1. **SOLID Principles** (Object-Oriented Design)
2. **Clean Architecture** (Robert C. Martin)
3. **TDD (Test-Driven Development)** (Kent Beck)
4. **Effective Dart** (Google's Dart Style Guide)
5. **Flutter Best Practices** (Flutter Team)

---

## 1. SOLID Principles

### S - Single Responsibility Principle
**Regel:** Jede Klasse hat genau EINE Verantwortlichkeit.

**Gut:**
```dart
// ✅ Eine Verantwortlichkeit: Email senden
class EmailService {
  Future<void> sendEmail(Email email) async {
    // SMTP logic only
  }
}

// ✅ Eine Verantwortlichkeit: Platzhalter ersetzen
class PlaceholderService {
  String replace(String template, Map<String, String> data) {
    // Replacement logic only
  }
}
```

**Schlecht:**
```dart
// ❌ Zu viele Verantwortlichkeiten
class EmailManager {
  Future<void> sendEmail() async { /* ... */ }
  String replacePlaceholders() { /* ... */ }
  void saveToDatabase() { /* ... */ }
  void showNotification() { /* ... */ }
}
```

**Enforcement:**
- Max 200 Zeilen pro Klasse (Exception: Models, UI Widgets)
- Max 3 public methods pro Service-Klasse
- Code Review: "Was ist die EINE Aufgabe dieser Klasse?"

---

### O - Open/Closed Principle
**Regel:** Offen für Erweiterung, geschlossen für Modifikation.

**Gut:**
```dart
// ✅ Abstract interface
abstract class EmailProvider {
  Future<void> send(Email email);
}

// ✅ Implementierungen können hinzugefügt werden ohne EmailService zu ändern
class GmailProvider implements EmailProvider { /* ... */ }
class OutlookProvider implements EmailProvider { /* ... */ }

class EmailService {
  final EmailProvider provider;
  EmailService(this.provider);
  
  Future<void> send(Email email) => provider.send(email);
}
```

**Schlecht:**
```dart
// ❌ Muss geändert werden für jeden neuen Provider
class EmailService {
  Future<void> send(Email email, String provider) async {
    if (provider == 'gmail') { /* ... */ }
    else if (provider == 'outlook') { /* ... */ }
    // Neue Provider = Code ändern
  }
}
```

**Enforcement:**
- Use Interfaces/Abstract classes für Services
- Dependency Injection (GetIt)
- Neue Features via neue Klassen, nicht Änderung bestehender

---

### L - Liskov Substitution Principle
**Regel:** Subtypen müssen substituierbar für ihre Basistypen sein.

**Gut:**
```dart
// ✅ Alle Repositories sind austauschbar
abstract class TodoRepository {
  Future<List<Todo>> getAll();
  Future<Todo?> getById(int id);
}

class SqliteTodoRepository implements TodoRepository {
  @override
  Future<List<Todo>> getAll() async { /* SQLite */ }
  
  @override
  Future<Todo?> getById(int id) async { /* SQLite */ }
}

class InMemoryTodoRepository implements TodoRepository {
  @override
  Future<List<Todo>> getAll() async { /* In-Memory */ }
  
  @override
  Future<Todo?> getById(int id) async { /* In-Memory */ }
}

// ✅ Beide können verwendet werden ohne Code-Änderung
void test() {
  TodoRepository repo = SqliteTodoRepository(); // Funktioniert
  repo = InMemoryTodoRepository(); // Funktioniert auch
}
```

**Enforcement:**
- Alle Repository-Implementierungen erfüllen Interface-Contract
- Unit Tests für alle Implementierungen
- Mock-Implementierungen für Tests

---

### I - Interface Segregation Principle
**Regel:** Clients sollten nicht von Interfaces abhängen, die sie nicht nutzen.

**Gut:**
```dart
// ✅ Kleine, spezifische Interfaces
abstract class Readable {
  Future<Todo?> read(int id);
}

abstract class Writable {
  Future<void> write(Todo todo);
}

abstract class Deletable {
  Future<void> delete(int id);
}

// Use Cases nutzen nur was sie brauchen
class GetTodoUseCase {
  final Readable repository;
  GetTodoUseCase(this.repository);
}

class CreateTodoUseCase {
  final Writable repository;
  CreateTodoUseCase(this.repository);
}
```

**Schlecht:**
```dart
// ❌ Fat Interface
abstract class TodoRepository {
  Future<Todo?> read(int id);
  Future<void> write(Todo todo);
  Future<void> delete(int id);
  Future<List<Todo>> getAll();
  Future<void> update(Todo todo);
  Future<void> bulkDelete(List<int> ids);
  // ... 20 mehr Methoden
}

// Klasse braucht nur read(), muss aber alles implementieren
class ReadOnlyTodoRepository implements TodoRepository {
  @override
  Future<Todo?> read(int id) async { /* ... */ }
  
  @override
  Future<void> write(Todo todo) async {
    throw UnimplementedError(); // ❌
  }
  // ... 18 mehr unimplemented methods
}
```

**Enforcement:**
- Max 5 Methoden pro Interface
- Separate Interfaces für Read/Write Operations
- Composition über Fat Interfaces

---

### D - Dependency Inversion Principle
**Regel:** Abhängigkeiten auf Abstraktionen, nicht auf Konkretionen.

**Gut:**
```dart
// ✅ Use Case hängt von Interface ab
class SendEmailUseCase {
  final TodoRepository todoRepository;
  final EmailService emailService;
  
  SendEmailUseCase({
    required this.todoRepository,
    required this.emailService,
  });
}

// ✅ Konkrete Implementierung via DI
final useCase = SendEmailUseCase(
  todoRepository: getIt<TodoRepository>(), // Interface
  emailService: getIt<EmailService>(),     // Interface
);
```

**Schlecht:**
```dart
// ❌ Use Case hängt von konkreter Implementierung ab
class SendEmailUseCase {
  final SqliteTodoRepository todoRepository; // ❌ Konkret
  final GmailEmailService emailService;      // ❌ Konkret
  
  SendEmailUseCase() {
    todoRepository = SqliteTodoRepository(); // ❌ Tight coupling
    emailService = GmailEmailService();      // ❌ Tight coupling
  }
}
```

**Enforcement:**
- Constructor Dependency Injection für alle Services
- GetIt für Service Locator
- Keine `new` Aufrufe in Business Logic
- Interfaces für alle Dependencies

---

## 2. Clean Architecture Layers

### Layer Structure (Strikte Trennung)
```
┌─────────────────────────────────────────┐
│         Presentation Layer              │  ← UI, BLoC, Widgets
│  (Flutter Widgets, BLoC, State)         │
└────────────┬────────────────────────────┘
             │ depends on ↓
┌────────────▼────────────────────────────┐
│         Domain Layer                    │  ← Business Logic (CORE)
│  (Entities, Use Cases, Interfaces)      │  ← Kennt keine anderen Layers!
└─────────────────────────────────────────┘
             ↑ implements interfaces from
┌────────────┴────────────────────────────┐
│         Data Layer                      │  ← Implementation
│  (Models, Repositories, Data Sources)   │
└─────────────────────────────────────────┘
```

### Dependency Rules (KRITISCH)

**Regel 1:** Abhängigkeiten zeigen nur nach INNEN (zum Domain Layer)
- Presentation → Domain ✅ (Presentation kennt Domain)
- Data → Domain ✅ (Data implementiert Domain-Interfaces)
- Domain → Data ❌ (Domain kennt KEINE Implementierungen)
- Domain → Presentation ❌ (Domain kennt keine UI)

**Regel 2:** Domain Layer kennt KEINE äußeren Layers
- Domain kennt kein Flutter
- Domain kennt keine SQLite
- Domain kennt keine HTTP

**Regel 3:** Domain definiert Interfaces, Data implementiert
```dart
// ✅ domain/repositories/todo_repository.dart
abstract class TodoRepository {
  Future<List<Todo>> getAll();
}

// ✅ data/repositories/todo_repository_impl.dart
class TodoRepositoryImpl implements TodoRepository {
  final DatabaseHelper db;
  
  @override
  Future<List<Todo>> getAll() async {
    // SQLite implementation
  }
}
```

**Enforcement:**
- Import-Analyse: Domain darf keine data/ imports haben
- CI Check: `grep -r "import.*data/" lib/domain/` → muss leer sein
- Code Review: Dependency Direction prüfen

---

### Layer Responsibilities

**Presentation Layer:**
- UI Rendering (Widgets)
- User Input Handling
- State Management (BLoC)
- Navigation
- **KEINE Business Logic!**

**Domain Layer:**
- Business Rules (Use Cases)
- Entity Definitions
- Repository Interfaces
- Validierungslogik
- **KEINE Framework-Dependencies!**

**Data Layer:**
- API Calls (SMTP)
- Database Operations (SQLite)
- Repository Implementations
- Caching
- **KEINE Business Logic!**

---

## 3. Test-Driven Development (TDD)

### Verbindlicher TDD-Zyklus

**Für JEDES Feature:**

1. **RED:** Test schreiben (schlägt fehl)
2. **GREEN:** Code schreiben (Test grün)
3. **REFACTOR:** Code verbessern (Test bleibt grün)

**Beispiel:**
```dart
// 1. RED - Test schreiben
test('should create TODO with valid data', () async {
  // Arrange
  final useCase = CreateTodoUseCase(mockRepository);
  final todo = Todo(subject: 'Test', ...);
  
  // Act
  final result = await useCase.execute(todo);
  
  // Assert
  expect(result.isSuccess, true);
  verify(mockRepository.create(todo)).called(1);
});

// Test läuft → FAILS (Code existiert noch nicht)

// 2. GREEN - Minimaler Code um Test zu bestehen
class CreateTodoUseCase {
  final TodoRepository repository;
  
  Future<Result> execute(Todo todo) async {
    await repository.create(todo);
    return Result.success();
  }
}

// Test läuft → PASSES

// 3. REFACTOR - Code verbessern
class CreateTodoUseCase {
  final TodoRepository repository;
  
  Future<Result> execute(Todo todo) async {
    // Validation
    if (todo.subject.isEmpty) {
      return Result.failure('Subject required');
    }
    
    // Persist
    try {
      await repository.create(todo);
      return Result.success();
    } catch (e) {
      return Result.failure(e.toString());
    }
  }
}

// Test läuft → STILL PASSES
```

---

### Test Coverage Requirements

**Minimum Coverage (Nicht verhandelbar):**

| Layer | Minimum | Target |
|-------|---------|--------|
| Domain (Use Cases) | 90% | 100% |
| Data (Repositories) | 80% | 90% |
| Services | 75% | 85% |
| Presentation (BLoC) | 70% | 80% |
| UI Widgets | 50% | 60% |
| **Overall** | **70%** | **80%** |

**Check Coverage:**
```bash
flutter test --coverage
genhtml coverage/lcov.info -o coverage/html
open coverage/html/index.html
```

**CI Gate:**
```bash
# Fails wenn Coverage < 70%
flutter test --coverage
lcov --summary coverage/lcov.info | grep "lines" | awk '{print $2}' | sed 's/%//' > coverage.txt
COVERAGE=$(cat coverage.txt)
if [ $(echo "$COVERAGE < 70" | bc) -eq 1 ]; then
  echo "Coverage $COVERAGE% is below 70%"
  exit 1
fi
```

---

### Test Types & Strategy

**Unit Tests (80% aller Tests):**
- Jede Use Case
- Jeder Service
- Jede Utility Function
- Mocks für Dependencies
```dart
// Beispiel Unit Test
test('PlaceholderService replaces all placeholders', () {
  // Arrange
  final service = PlaceholderService();
  final template = 'Hi {Vorname}, re: {Subject}';
  final data = {'Vorname': 'John', 'Subject': 'Test'};
  
  // Act
  final result = service.replace(template, data);
  
  // Assert
  expect(result, 'Hi John, re: Test');
});
```

**Widget Tests (15% aller Tests):**
- Custom Widgets
- Forms
- Komplexe UI-Logik
```dart
// Beispiel Widget Test
testWidgets('TodoCard displays subject and email', (tester) async {
  // Arrange
  final todo = Todo(subject: 'Test Subject', recipientEmail: 'test@test.com');
  
  // Act
  await tester.pumpWidget(MaterialApp(home: TodoCard(todo: todo)));
  
  // Assert
  expect(find.text('Test Subject'), findsOneWidget);
  expect(find.text('test@test.com'), findsOneWidget);
});
```

**Integration Tests (5% aller Tests):**
- End-to-End User Flows
- Multi-Layer Interaktion
```dart
// Beispiel Integration Test
testWidgets('Create TODO flow', (tester) async {
  // 1. Navigate to Create screen
  await tester.tap(find.byIcon(Icons.add));
  await tester.pumpAndSettle();
  
  // 2. Fill form
  await tester.enterText(find.byKey(Key('subject')), 'Test');
  await tester.enterText(find.byKey(Key('email')), 'test@test.com');
  
  // 3. Save
  await tester.tap(find.text('Save'));
  await tester.pumpAndSettle();
  
  // 4. Verify in list
  expect(find.text('Test'), findsOneWidget);
});
```

---

### Test Quality Standards

**AAA Pattern (Arrange-Act-Assert):**
```dart
test('description', () {
  // Arrange - Setup
  final input = 'test';
  final expected = 'TEST';
  
  // Act - Execute
  final result = input.toUpperCase();
  
  // Assert - Verify
  expect(result, expected);
});
```

**Naming Convention:**
```dart
// ✅ Gut: Beschreibt WAS getestet wird
test('should return uppercase string when input is lowercase', () {});
test('should throw exception when input is null', () {});
test('should save TODO to database when valid data provided', () {});

// ❌ Schlecht: Vage, nicht aussagekräftig
test('test uppercase', () {});
test('null check', () {});
test('save works', () {});
```

**One Assertion per Test (Ideal):**
```dart
// ✅ Gut: Ein Assert pro Test
test('should set isCompleted to true', () {
  final todo = Todo().copyWith(isCompleted: true);
  expect(todo.isCompleted, true);
});

test('should set completedAt to current time', () {
  final now = DateTime.now();
  final todo = Todo().copyWith(completedAt: now);
  expect(todo.completedAt, now);
});

// ⚠️ Akzeptabel wenn zusammenhängend:
test('should complete TODO correctly', () {
  final todo = Todo().complete();
  expect(todo.isCompleted, true);
  expect(todo.completedAt, isNotNull); // Zusammenhängend
});
```

---

### Mocking Strategy

**Use Mockito for all external dependencies:**
```dart
// 1. Create Mock
@GenerateMocks([TodoRepository, EmailService])
void main() {}

// 2. Generate Mocks
// Run: flutter pub run build_runner build

// 3. Use in Tests
test('should call repository.create', () async {
  // Arrange
  final mockRepo = MockTodoRepository();
  final useCase = CreateTodoUseCase(mockRepo);
  final todo = Todo(...);
  
  when(mockRepo.create(any))
    .thenAnswer((_) async => 1);
  
  // Act
  await useCase.execute(todo);
  
  // Assert
  verify(mockRepo.create(todo)).called(1);
  verifyNoMoreInteractions(mockRepo);
});
```

**Mock Rules:**
- Mock alle externen Dependencies (DB, Network, File System)
- NICHT mocken: Value Objects, Entities, DTOs
- Verify ALL interactions (verifyNoMoreInteractions)

---

## 4. Dart/Flutter Best Practices

### Effective Dart (Google Style Guide)

**Naming Conventions:**
```dart
// ✅ Classes: UpperCamelCase
class TodoRepository {}
class EmailService {}

// ✅ Files: snake_case
// todo_repository.dart
// email_service.dart

// ✅ Variables, methods: lowerCamelCase
final userName = 'John';
void sendEmail() {}

// ✅ Constants: lowerCamelCase (nicht SCREAMING_CASE)
const maxRetries = 3;
const defaultTimeout = Duration(seconds: 30);

// ✅ Private: Leading underscore
class _PrivateClass {}
void _privateMethod() {}
final _privateField = 'value';
```

**Null Safety:**
```dart
// ✅ Use null safety correctly
String? nullableString;
String nonNullableString = 'value';

// ✅ Null-aware operators
final length = nullableString?.length ?? 0;
final upper = nullableString?.toUpperCase() ?? '';

// ✅ Late for guaranteed initialization
late final DatabaseHelper db;

void init() {
  db = DatabaseHelper(); // Must be called before use
}

// ❌ Avoid force unwrap unless 100% sure
final value = nullableString!; // Dangerous!
```

**Immutability:**
```dart
// ✅ Prefer immutable data
class Todo {
  final String subject;
  final String email;
  
  const Todo({required this.subject, required this.email});
  
  Todo copyWith({String? subject, String? email}) {
    return Todo(
      subject: subject ?? this.subject,
      email: email ?? this.email,
    );
  }
}

// ❌ Avoid mutable state
class Todo {
  String subject; // Mutable - avoid!
  String email;
}
```

**Async/Await:**
```dart
// ✅ Always await Futures
Future<void> loadData() async {
  final data = await repository.getData();
  print(data);
}

// ✅ Handle errors
Future<void> loadData() async {
  try {
    final data = await repository.getData();
    print(data);
  } catch (e) {
    print('Error: $e');
  }
}

// ❌ Don't forget await
Future<void> loadData() async {
  repository.getData(); // ❌ Forgotten await!
  print('Done'); // Prints before data loaded
}
```

---

### Flutter Best Practices

**Widget Composition:**
```dart
// ✅ Small, reusable widgets
class TodoCard extends StatelessWidget {
  final Todo todo;
  
  const TodoCard({required this.todo, Key? key}) : super(key: key);
  
  @override
  Widget build(BuildContext context) {
    return Card(
      child: ListTile(
        title: Text(todo.subject),
        subtitle: Text(todo.email),
      ),
    );
  }
}

// ❌ Giant monolithic widgets
class TodoScreen extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    return Scaffold(
      body: ListView.builder(
        itemBuilder: (context, index) {
          return Card( // ❌ Inline complex widget
            child: Column(
              children: [
                // 100+ lines of widget code
              ],
            ),
          );
        },
      ),
    );
  }
}
```

**Const Constructors:**
```dart
// ✅ Use const when possible
const SizedBox(height: 16);
const Text('Hello');
const Icon(Icons.add);

// ✅ Const constructors in custom widgets
class MyWidget extends StatelessWidget {
  const MyWidget({Key? key}) : super(key: key);
  
  @override
  Widget build(BuildContext context) {
    return const Text('Constant widget');
  }
}
```

**BuildContext Usage:**
```dart
// ✅ Use BuildContext correctly
class MyWidget extends StatelessWidget {
  @override
  Widget build(BuildContext context) {
    final theme = Theme.of(context);
    final mediaQuery = MediaQuery.of(context);
    
    return Container(
      color: theme.primaryColor,
      width: mediaQuery.size.width,
    );
  }
}

// ❌ Don't store BuildContext
class MyWidget extends StatelessWidget {
  late BuildContext _context; // ❌ Never do this!
  
  @override
  Widget build(BuildContext context) {
    _context = context; // ❌ Stored context can be invalid
    return Container();
  }
}
```

---

## 5. Code Review Checklist

### Pre-Commit Checklist (Developer)

**Before ANY commit:**
- [ ] Alle Tests grün (`flutter test`)
- [ ] Coverage ≥ 70% für neue Files
- [ ] Keine Linter Warnings (`flutter analyze`)
- [ ] Code formatiert (`dart format lib/`)
- [ ] Keine Debug prints
- [ ] Keine TODO/FIXME comments (in Tickets umwandeln)
- [ ] Commit Message folgt Convention
```bash
# Run before commit
flutter analyze
dart format lib/ test/
flutter test --coverage
# Check output - all green?
git add .
git commit -m "feat: Add TODO creation use case"
```

---

### Code Review Checklist (Reviewer)

**Für jeden Pull Request:**

**Architecture:**
- [ ] Clean Architecture Layers korrekt
- [ ] Dependency Direction korrekt (innen zeigend)
- [ ] SOLID Principles eingehalten
- [ ] Keine Business Logic in UI
- [ ] Keine UI Code in Domain

**Code Quality:**
- [ ] Naming Conventions korrekt
- [ ] Null Safety korrekt verwendet
- [ ] Keine Magic Numbers/Strings (use constants)
- [ ] Error Handling vorhanden
- [ ] Logging sinnvoll

**Tests:**
- [ ] Alle neuen Use Cases getestet
- [ ] Alle neuen Services getestet
- [ ] Edge Cases abgedeckt
- [ ] Mocks korrekt verwendet
- [ ] Coverage ≥ 70%

**Performance:**
- [ ] Keine N+1 DB Queries
- [ ] Kein blocking in UI Thread
- [ ] Keine Memory Leaks (Streams closed, Controllers disposed)

**Documentation:**
- [ ] Public APIs dokumentiert (/// comments)
- [ ] Komplexe Logik erklärt
- [ ] README updated (falls nötig)

---

## 6. Continuous Integration (CI) Gates

### Required Checks (Must Pass)

**1. Linting:**
```bash
flutter analyze
# Exit code 0 = pass, > 0 = fail
```

**2. Tests:**
```bash
flutter test
# All tests must pass
```

**3. Coverage:**
```bash
flutter test --coverage
# Coverage ≥ 70%
```

**4. Build:**
```bash
flutter build apk --release
# Build must succeed
```

### CI Pipeline (GitHub Actions Example)
```yaml
# .github/workflows/ci.yml
name: CI

on: [push, pull_request]

jobs:
  test:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - uses: subosito/flutter-action@v2
        with:
          flutter-version: '3.19.0'
      
      - name: Install dependencies
        run: flutter pub get
      
      - name: Analyze
        run: flutter analyze
      
      - name: Format check
        run: dart format --set-exit-if-changed lib/ test/
      
      - name: Run tests
        run: flutter test --coverage
      
      - name: Check coverage
        run: |
          COVERAGE=$(lcov --summary coverage/lcov.info | grep "lines" | awk '{print $2}' | sed 's/%//')
          echo "Coverage: $COVERAGE%"
          if [ $(echo "$COVERAGE < 70" | bc) -eq 1 ]; then
            echo "Coverage below 70%"
            exit 1
          fi
      
      - name: Build APK
        run: flutter build apk --release
```

---

## 7. Definition of Done (DoD)

### Ein Ticket ist DONE wenn:

**Code:**
- [ ] Code geschrieben & funktioniert
- [ ] Code reviewed & approved
- [ ] SOLID Principles eingehalten
- [ ] Clean Architecture eingehalten
- [ ] Linter clean (`flutter analyze`)
- [ ] Formatiert (`dart format`)

**Tests:**
- [ ] Unit Tests geschrieben
- [ ] Tests grün
- [ ] Coverage ≥ 70% für neue Files
- [ ] Edge Cases getestet
- [ ] Integration Test (falls relevant)

**Documentation:**
- [ ] Public APIs dokumentiert
- [ ] README updated (falls nötig)
- [ ] Breaking Changes dokumentiert

**Integration:**
- [ ] Merged to develop
- [ ] CI Pipeline grün
- [ ] Keine Merge Conflicts

**Validation:**
- [ ] Manuell getestet auf Device
- [ ] Akzeptanzkriterien erfüllt

---

## 8. Metrics & Monitoring

### Code Metrics (Track in jeder Phase)

**Complexity Metrics:**
```bash
# Cyclomatic Complexity (max 10 per function)
dart_code_metrics analyze lib/

# Lines of Code
find lib/ -name "*.dart" -exec wc -l {} + | tail -1
```

**Target Metrics:**
- Average Cyclomatic Complexity: < 5
- Max Cyclomatic Complexity: < 10
- Average File Size: < 200 lines
- Max File Size: < 400 lines (except UI screens)

**Test Metrics:**
- Test/Code Ratio: > 1.0 (mehr Test-Code als Prod-Code)
- Test Execution Time: < 30 seconds (all unit tests)
- Integration Test Time: < 2 minutes

---

### Quality Gates (Non-Negotiable)

**Gate 1: Commit**
- Linter clean
- Tests green locally

**Gate 2: Push**
- CI pipeline green
- Coverage ≥ 70%

**Gate 3: PR Merge**
- Code review approved
- All discussions resolved
- Branch up-to-date with develop

**Gate 4: Release**
- All integration tests green
- Manual testing on 3+ devices
- No critical bugs
- Performance acceptable

---

## 9. Refactoring Guidelines

### When to Refactor

**Red Flags:**
- Function > 30 lines
- Class > 200 lines
- Cyclomatic Complexity > 10
- Duplicate code (DRY violation)
- Test coverage < 70%
- 3+ levels of nesting

**Refactoring Rules:**
1. **Tests first:** Ensure tests exist before refactoring
2. **Small steps:** One refactoring at a time
3. **Green throughout:** Tests stay green during refactoring
4. **Commit often:** Each refactoring = separate commit

**Common Refactorings:**
- Extract Method
- Extract Class
- Introduce Parameter Object
- Replace Conditional with Polymorphism
- Move Method to appropriate layer

---

## 10. Performance Standards

### Performance Budgets

**App Performance:**
- Cold Start: < 3 seconds
- Hot Reload: < 1 second
- Screen Transition: < 300ms
- List Scroll: 60 FPS
- Database Query: < 100ms

**Resource Budgets:**
- APK Size: < 30 MB
- Memory Usage: < 150 MB
- Battery Drain: < 5% per hour (idle)

**Measuring:**
```bash
# Profile mode
flutter run --profile

# Performance overlay
# In app: Debug → Performance Overlay

# Memory profiling
# Flutter DevTools → Memory
```

---

## 11. Security Standards

### Sensitive Data

**NEVER commit:**
- API Keys
- Passwords
- Private Keys
- Email credentials
- Any PII (Personally Identifiable Information)

**Use:**
- flutter_secure_storage for passwords
- Environment variables for API keys
- .gitignore for sensitive files

### Code Security

**SQL Injection Prevention:**
```dart
// ✅ Use parameterized queries
db.query('todos', where: 'id = ?', whereArgs: [id]);

// ❌ Never concatenate
db.rawQuery('SELECT * FROM todos WHERE id = $id'); // SQL Injection!
```

**Input Validation:**
```dart
// ✅ Always validate user input
if (email.isEmpty || !email.contains('@')) {
  throw ValidationException('Invalid email');
}

// ✅ Sanitize before use
final sanitized = email.trim().toLowerCase();
```

---

## 12. Enforcement & Consequences

### Automated Enforcement

**Pre-Commit Hook:**
```bash
# .git/hooks/pre-commit
#!/bin/sh

echo "Running pre-commit checks..."

# Analyze
flutter analyze
if [ $? -ne 0 ]; then
  echo "❌ Linting failed"
  exit 1
fi

# Test
flutter test
if [ $? -ne 0 ]; then
  echo "❌ Tests failed"
  exit 1
fi

echo "✅ All checks passed"
exit 0
```

**CI Enforcement:**
- All PRs blocked until CI green
- No direct commits to main/develop
- Coverage check fails build if < 70%

---

### Code Review Enforcement

**Required Approvals:**
- Minimum 1 approval (selbst wenn Solo: Self-review)
- All discussions resolved
- All CI checks green

**Review SLA:**
- Start review within 24 hours
- Complete review within 48 hours

---

### Consequences of Violations

**Severity Levels:**

**Critical (Must Fix Immediately):**
- Tests failing
- Coverage < 70%
- Security vulnerability
- Data loss bug
→ Block merge, fix before anything else

**High (Fix before merge):**
- Linter errors
- Architecture violation
- Missing tests
- Performance issue
→ Cannot merge until fixed

**Medium (Fix in follow-up):**
- Minor code style issues
- Missing documentation
- Non-critical TODO
→ Create ticket, can merge

**Low (Nice to have):**
- Cosmetic improvements
- Optimization opportunities
→ Optional, may ignore

---

## 13. Learning & Improvement

### Continuous Learning

**Resources (Mandatory Reading):**
1. Clean Code (Robert C. Martin)
2. Clean Architecture (Robert C. Martin)
3. Effective Dart (https://dart.dev/guides/language/effective-dart)
4. Flutter Best Practices (https://docs.flutter.dev/development/best-practices)

**Weekly Practice:**
- Code Review eigener PRs
- Refactor mindestens 1 file
- Schreibe mindestens 1 Test für alten Code

---

### Retrospectives

**Nach jeder Phase:**
1. Was lief gut? (Code Quality)
2. Was lief schlecht? (Violations)
3. Was verbessern? (Process)
4. Action Items (Concrete tasks)

**Metrics Review:**
- Coverage Trend
- Bug Count
- Code Complexity Trend
- Test Execution Time

---

## Summary: Golden Rules

### ⚡ The 10 Commandments

1. **Tests First:** Kein Code ohne Tests
2. **SOLID Always:** Kein Merge ohne SOLID
3. **Clean Layers:** Domain kennt keine Data
4. **Coverage 70%:** Nicht verhandelbar
5. **Linter Clean:** Kein Warning, kein Error
6. **No Magic:** Constants für alle Values
7. **DRY Code:** Don't Repeat Yourself
8. **Small Functions:** Max 30 Zeilen
9. **Null Safe:** Nutze Null Safety korrekt
10. **Review Everything:** Kein Self-Merge

---

### 🎯 Quality Mantra

**"If it's not tested, it's broken."**
**"If it violates SOLID, refactor it."**
**"If coverage drops, fix it immediately."**
**"If CI is red, nothing else matters."**

---

## Appendix: Quick Reference

### Commands
```bash
# Analyze
flutter analyze

# Format
dart format lib/ test/

# Test
flutter test

# Coverage
flutter test --coverage
genhtml coverage/lcov.info -o coverage/html

# Metrics
dart_code_metrics analyze lib/

# Build
flutter build apk --release
```

### Checklists

**Before Commit:**
- [ ] Tests green
- [ ] Linter clean
- [ ] Formatted
- [ ] Coverage ≥ 70%

**Before PR:**
- [ ] Self-reviewed
- [ ] Documentation updated
- [ ] CI green
- [ ] Rebased on develop

**Before Merge:**
- [ ] Approved
- [ ] All checks green
- [ ] Discussions resolved

---

**Ende CodeQuality.md**