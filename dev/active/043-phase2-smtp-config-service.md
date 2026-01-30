# Task 043: Create SmtpConfigService

## Phase
2 - Core Business Logic

## Description
Implement SMTP configuration service with provider-specific defaults.

## Steps
1. Create `lib/services/smtp/smtp_config_service.dart`
2. Define provider enum and configs
3. Implement provider-specific host/port/TLS settings

## Code Structure
```dart
enum SmtpProvider {
  gmail,
  outlook,
  yahoo,
  custom,
}

class SmtpConfig {
  final String host;
  final int port;
  final bool useSsl;
  final bool useTls;

  const SmtpConfig({
    required this.host,
    required this.port,
    this.useSsl = false,
    this.useTls = true,
  });
}

class SmtpConfigService {
  static const Map<SmtpProvider, SmtpConfig> _providerConfigs = {
    SmtpProvider.gmail: SmtpConfig(
      host: 'smtp.gmail.com',
      port: 587,
      useTls: true,
    ),
    SmtpProvider.outlook: SmtpConfig(
      host: 'smtp.office365.com',
      port: 587,
      useTls: true,
    ),
    SmtpProvider.yahoo: SmtpConfig(
      host: 'smtp.mail.yahoo.com',
      port: 587,
      useTls: true,
    ),
  };

  /// Get SMTP config for provider
  SmtpConfig getConfig(SmtpProvider provider) {
    return _providerConfigs[provider] ??
      const SmtpConfig(host: '', port: 587);
  }

  /// Get config with custom values
  SmtpConfig getCustomConfig({
    required String host,
    required int port,
    bool useSsl = false,
    bool useTls = true,
  }) {
    return SmtpConfig(
      host: host,
      port: port,
      useSsl: useSsl,
      useTls: useTls,
    );
  }

  /// Detect provider from email address
  SmtpProvider detectProvider(String email) {
    final domain = email.split('@').last.toLowerCase();

    if (domain.contains('gmail') || domain.contains('googlemail')) {
      return SmtpProvider.gmail;
    } else if (domain.contains('outlook') ||
               domain.contains('hotmail') ||
               domain.contains('live')) {
      return SmtpProvider.outlook;
    } else if (domain.contains('yahoo')) {
      return SmtpProvider.yahoo;
    }

    return SmtpProvider.custom;
  }

  /// Get help URL for app password setup
  String getHelpUrl(SmtpProvider provider) {
    switch (provider) {
      case SmtpProvider.gmail:
        return 'https://support.google.com/accounts/answer/185833';
      case SmtpProvider.outlook:
        return 'https://support.microsoft.com/account-billing/manage-app-passwords';
      case SmtpProvider.yahoo:
        return 'https://help.yahoo.com/kb/generate-app-password';
      case SmtpProvider.custom:
        return '';
    }
  }
}
```

## Acceptance Criteria
- [ ] Gmail config correct (smtp.gmail.com:587)
- [ ] Outlook config correct (smtp.office365.com:587)
- [ ] Yahoo config correct (smtp.mail.yahoo.com:587)
- [ ] Provider detection from email works
- [ ] Custom config support works
- [ ] Help URLs provided for each provider

## Dependencies
- None

## Parallel Work
Can run parallel with: Task 039, 040, 041, 042

## Estimated Effort
1 hour
