# Task 090: Create Connectivity Service

## Phase
5 - Background Service & Notifications

## Description
Implement connectivity monitoring service.

## Steps
1. Create `lib/services/network/connectivity_service.dart`
2. Monitor network status
3. Handle pending sends when coming online

## Code Structure
```dart
import 'dart:async';
import 'package:connectivity_plus/connectivity_plus.dart';

class ConnectivityService {
  final Connectivity _connectivity = Connectivity();
  StreamSubscription<List<ConnectivityResult>>? _subscription;

  final _statusController = StreamController<bool>.broadcast();
  Stream<bool> get statusStream => _statusController.stream;

  bool _isConnected = true;
  bool get isConnectedSync => _isConnected;

  /// Initialize and start monitoring
  Future<void> initialize() async {
    // Check initial status
    _isConnected = await isConnected();
    _statusController.add(_isConnected);

    // Start monitoring
    _subscription = _connectivity.onConnectivityChanged.listen(
      (results) async {
        final connected = _hasConnection(results);
        if (connected != _isConnected) {
          _isConnected = connected;
          _statusController.add(_isConnected);

          if (_isConnected) {
            await _onConnectionRestored();
          }
        }
      },
    );
  }

  /// Check current connectivity status
  Future<bool> isConnected() async {
    final results = await _connectivity.checkConnectivity();
    return _hasConnection(results);
  }

  bool _hasConnection(List<ConnectivityResult> results) {
    return results.any((result) =>
        result == ConnectivityResult.wifi ||
        result == ConnectivityResult.mobile ||
        result == ConnectivityResult.ethernet);
  }

  /// Called when connection is restored
  Future<void> _onConnectionRestored() async {
    // Trigger pending sends check
    // This will be handled by BackgroundService
    print('Connection restored - checking for pending sends');
  }

  /// Dispose resources
  void dispose() {
    _subscription?.cancel();
    _statusController.close();
  }
}

/// Widget to show offline banner
class ConnectivityBanner extends StatelessWidget {
  final Widget child;

  const ConnectivityBanner({
    super.key,
    required this.child,
  });

  @override
  Widget build(BuildContext context) {
    final connectivityService = getIt<ConnectivityService>();

    return StreamBuilder<bool>(
      stream: connectivityService.statusStream,
      initialData: connectivityService.isConnectedSync,
      builder: (context, snapshot) {
        final isConnected = snapshot.data ?? true;

        return Column(
          children: [
            AnimatedContainer(
              duration: const Duration(milliseconds: 300),
              height: isConnected ? 0 : 32,
              child: isConnected
                  ? const SizedBox.shrink()
                  : Container(
                      color: AppColors.warning,
                      child: const Center(
                        child: Row(
                          mainAxisAlignment: MainAxisAlignment.center,
                          children: [
                            Icon(
                              Icons.cloud_off,
                              size: 16,
                              color: Colors.white,
                            ),
                            SizedBox(width: 8),
                            Text(
                              'No internet connection',
                              style: TextStyle(color: Colors.white),
                            ),
                          ],
                        ),
                      ),
                    ),
            ),
            Expanded(child: child),
          ],
        );
      },
    );
  }
}
```

## Integration in main.dart
```dart
void main() async {
  // ... other initialization

  // Initialize connectivity service
  final connectivityService = getIt<ConnectivityService>();
  await connectivityService.initialize();

  runApp(LetMeDoMyWorkApp(...));
}

// In app widget
@override
Widget build(BuildContext context) {
  return MaterialApp(
    // ...
    builder: (context, child) {
      return ConnectivityBanner(
        child: child ?? const SizedBox.shrink(),
      );
    },
  );
}
```

## Acceptance Criteria
- [ ] Correctly detects WiFi/Mobile/Ethernet
- [ ] Stream updates on connectivity change
- [ ] Handles going offline
- [ ] Triggers pending check when coming online
- [ ] Offline banner widget works
- [ ] Clean disposal of resources

## Dependencies
- Task 007 (pubspec with connectivity_plus)
- Task 030 (DI setup)

## Parallel Work
Can run parallel with: Task 088, 089

## Estimated Effort
1.5 hours
