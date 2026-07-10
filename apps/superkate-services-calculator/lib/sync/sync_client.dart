/// Client interface for the Hair by Superkate sync backend.
///
/// Shape follows the t-027 contract (backend-api-schema-contract.md):
/// bootstrap → push (dirty local records) → pull (server changes after a
/// version cursor). Implementations:
/// - [FakeSyncClient] (fake_sync_client.dart): in-memory contract double for
///   tests and future sync-engine work.
/// - [DisabledSyncClient] (disabled_sync_client.dart): the production default
///   while cloud sync remains gated — every call refuses loudly.
///
/// No implementation in this app may contact a live endpoint, carry secrets,
/// upload real customer data, send email, or add analytics until Silas clears
/// the production sync gates (roadmap t-029/t-030 boundaries).
library;

import 'sync_models.dart';

abstract class SuperkateSyncClient {
  /// Whether this client is allowed to sync at all. UI can use this to show
  /// [SyncStatus.disabled] without triggering calls that will throw.
  bool get isSyncAvailable;

  /// GET /api/superkate/sync/bootstrap — authenticated handshake returning
  /// owner/business scope, the current server version, and feature switches.
  Future<SyncBootstrap> bootstrap();

  /// POST /api/superkate/sync/push — send locally-changed customers and
  /// appointments (including tombstones). Partial success is explicit:
  /// rejected rows come back item-by-item, never silently dropped.
  Future<SyncPushResult> push({
    List<CustomerSyncRecord> customers = const [],
    List<AppointmentSyncRecord> appointments = const [],
  });

  /// GET /api/superkate/sync/pull?afterVersion= — fetch server changes
  /// (including tombstones) after a server-version cursor.
  Future<SyncPullResult> pull({int afterVersion = 0});
}
