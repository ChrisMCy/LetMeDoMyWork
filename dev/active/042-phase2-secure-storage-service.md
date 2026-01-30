# Task 042: Create SecureStorageService

## Phase
2 - Core Business Logic

## Description
Implement secure storage wrapper for sensitive data (SMTP password).

## Steps
1. Create `lib/services/storage/secure_storage_service.dart`
2. Wrap flutter_secure_storage
3. Implement save/load/delete operations

## Code Structure
```dart
import 'package:flutter_secure_storage/flutter_secure_storage.dart';

class SecureStorageService {
  static const String _smtpPasswordKey = 'smtp_password';

  final FlutterSecureStorage _storage;

  SecureStorageService() : _storage = const FlutterSecureStorage(
    aOptions: AndroidOptions(
      encryptedSharedPreferences: true,
    ),
  );

  // Constructor for testing with mock
  SecureStorageService.withStorage(this._storage);

  /// Save SMTP password securely
  Future<void> saveSmtpPassword(String password) async {
    await _storage.write(key: _smtpPasswordKey, value: password);
  }

  /// Retrieve SMTP password
  Future<String?> getSmtpPassword() async {
    return await _storage.read(key: _smtpPasswordKey);
  }

  /// Delete SMTP password
  Future<void> deleteSmtpPassword() async {
    await _storage.delete(key: _smtpPasswordKey);
  }

  /// Check if SMTP password exists
  Future<bool> hasSmtpPassword() async {
    final password = await getSmtpPassword();
    return password != null && password.isNotEmpty;
  }

  /// Clear all secure data (for reset/logout)
  Future<void> clearAll() async {
    await _storage.deleteAll();
  }
}
```

## Acceptance Criteria
- [ ] Password saved securely (encrypted)
- [ ] Password retrieved correctly
- [ ] Password deleted correctly
- [ ] Missing key returns null (no exception)
- [ ] clearAll removes all data

## Dependencies
- Task 007 (pubspec with flutter_secure_storage)

## Parallel Work
Can run parallel with: Task 039, 040, 041

## Estimated Effort
45 minutes
