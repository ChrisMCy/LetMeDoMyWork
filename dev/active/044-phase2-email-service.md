# Task 044: Create EmailService

## Phase
2 - Core Business Logic

## Description
Implement SMTP email sending service using mailer package.

## Steps
1. Create `lib/services/smtp/email_service.dart`
2. Implement SMTP connection logic
3. Implement email building and sending
4. Add timeout handling (30 seconds)
5. Add specific error messages

## Code Structure
```dart
import 'package:mailer/mailer.dart';
import 'package:mailer/smtp_server.dart';

class EmailService {
  final SmtpConfigService _configService;
  final SecureStorageService _secureStorage;

  EmailService(this._configService, this._secureStorage);

  /// Send an email
  Future<Result<void>> sendEmail({
    required String fromEmail,
    required String toEmail,
    required String subject,
    required String body,
    SmtpProvider? provider,
    SmtpConfig? customConfig,
  }) async {
    try {
      final password = await _secureStorage.getSmtpPassword();
      if (password == null || password.isEmpty) {
        return Result.failure('SMTP password not configured');
      }

      final config = customConfig ??
        _configService.getConfig(provider ?? SmtpProvider.gmail);

      final smtpServer = SmtpServer(
        config.host,
        port: config.port,
        username: fromEmail,
        password: password,
        ssl: config.useSsl,
        ignoreBadCertificate: false,
        allowInsecure: false,
      );

      final message = Message()
        ..from = Address(fromEmail)
        ..recipients.add(toEmail)
        ..subject = subject
        ..text = body;

      await send(message, smtpServer).timeout(
        const Duration(seconds: 30),
        onTimeout: () {
          throw TimeoutException('Email send timeout after 30 seconds');
        },
      );

      return Result.success(null);
    } on MailerException catch (e) {
      return Result.failure(_parseMailerError(e));
    } on TimeoutException {
      return Result.failure('Connection timeout. Check your internet connection.');
    } on SocketException {
      return Result.failure('Network error. Check your internet connection.');
    } catch (e) {
      return Result.failure('Failed to send email: $e');
    }
  }

  /// Test SMTP connection
  Future<Result<void>> testConnection({
    required String email,
    required String password,
    required SmtpProvider provider,
    SmtpConfig? customConfig,
  }) async {
    try {
      final config = customConfig ?? _configService.getConfig(provider);

      final smtpServer = SmtpServer(
        config.host,
        port: config.port,
        username: email,
        password: password,
        ssl: config.useSsl,
      );

      final message = Message()
        ..from = Address(email)
        ..recipients.add(email)
        ..subject = 'LetMeDoMyWork - Test Email'
        ..text = 'This is a test email from LetMeDoMyWork app. '
                 'Your SMTP configuration is working correctly!';

      await send(message, smtpServer).timeout(
        const Duration(seconds: 30),
      );

      return Result.success(null);
    } catch (e) {
      return Result.failure(_parseMailerError(e));
    }
  }

  String _parseMailerError(dynamic error) {
    final message = error.toString().toLowerCase();

    if (message.contains('authentication') ||
        message.contains('535') ||
        message.contains('invalid credentials')) {
      return 'Authentication failed. Check your email and app password.';
    }
    if (message.contains('connection refused') ||
        message.contains('host')) {
      return 'Could not connect to mail server. Check your settings.';
    }
    if (message.contains('certificate')) {
      return 'SSL certificate error. Try a different port or contact support.';
    }

    return 'Email error: $error';
  }
}
```

## Acceptance Criteria
- [ ] Email sends successfully via SMTP
- [ ] Timeout handled (30 seconds)
- [ ] Authentication errors parsed correctly
- [ ] Network errors handled gracefully
- [ ] Test connection feature works
- [ ] Returns Result with success or specific error

## Dependencies
- Task 007 (pubspec with mailer package)
- Task 042 (SecureStorageService)
- Task 043 (SmtpConfigService)

## Parallel Work
Must run after: Task 042, 043

## Estimated Effort
2 hours
