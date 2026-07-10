library;

import 'sync_client.dart';
import 'sync_models.dart';

/// The production default while cloud sync is human-gated: the app stays
/// local-first and every sync call refuses loudly instead of silently
/// no-opping, so nothing can accidentally build on a half-enabled path.
class DisabledSyncClient implements SuperkateSyncClient {
  const DisabledSyncClient();

  static const String _reason =
      'Cloud sync is not enabled in this beta. Appointment and customer data '
      'stay on this device.';

  @override
  bool get isSyncAvailable => false;

  @override
  Future<SyncBootstrap> bootstrap() async =>
      throw const SyncUnavailableException(_reason);

  @override
  Future<SyncPushResult> push({
    List<CustomerSyncRecord> customers = const [],
    List<AppointmentSyncRecord> appointments = const [],
  }) async =>
      throw const SyncUnavailableException(_reason);

  @override
  Future<SyncPullResult> pull({int afterVersion = 0}) async =>
      throw const SyncUnavailableException(_reason);
}
