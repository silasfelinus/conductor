library;

import '../domain/money.dart';
import 'sync_client.dart';
import 'sync_models.dart';

/// In-memory double of the Hair by Superkate sync backend, faithful to the
/// t-027 contract so the future sync engine can be built and tested against
/// real semantics: owner-scoped rows, server-generated IDs, monotonic
/// serverVersion, last-write-wins conflicts, loud total-mismatch rejection,
/// and tombstone propagation. Test-only — it never touches the network.
class FakeSyncClient implements SuperkateSyncClient {
  FakeSyncClient({
    this.authenticated = true,
    this.ownerUserId = 'test-owner-superkate',
    this.businessSlug = 'hair-by-superkate',
    DateTime Function()? clock,
  }) : _clock = clock ?? (() => DateTime.now().toUtc());

  /// The contract requires auth on every sync route; flip this to test the
  /// unauthenticated path.
  bool authenticated;

  final String ownerUserId;
  final String businessSlug;
  final DateTime Function() _clock;

  int _serverVersion = 0;
  int _nextId = 1;

  final Map<String, _StoredRecord<CustomerSyncRecord>> _customers = {};
  final Map<String, _StoredRecord<AppointmentSyncRecord>> _appointments = {};

  @override
  bool get isSyncAvailable => true;

  void _requireAuth() {
    if (!authenticated) {
      throw const SyncUnavailableException(
          'Sync requires an authenticated account.');
    }
  }

  @override
  Future<SyncBootstrap> bootstrap() async {
    _requireAuth();
    return SyncBootstrap(
      businessSlug: businessSlug,
      ownerUserId: ownerUserId,
      serverVersion: _serverVersion,
      features: const {
        'pushCustomers': true,
        'pushAppointments': true,
        'pullChanges': true,
        // Hard beta boundaries — the backend never flips these silently.
        'directEmailSend': false,
        'analytics': false,
      },
    );
  }

  @override
  Future<SyncPushResult> push({
    List<CustomerSyncRecord> customers = const [],
    List<AppointmentSyncRecord> appointments = const [],
  }) async {
    _requireAuth();
    final syncedAt = _clock();
    final accepted = <SyncRecordAck>[];
    final rejected = <SyncRejection>[];

    for (final record in customers) {
      final problem = _validateCustomer(record);
      if (problem != null) {
        rejected.add(problem);
        continue;
      }
      final existing = _customers[record.localId];
      final conflict =
          _conflictWith(existing?.record.updatedAt, record.updatedAt);
      if (existing != null && conflict) {
        rejected.add(SyncRejection(
          entity: 'customer',
          localId: record.localId,
          code: 'CONFLICT',
          message: 'A newer saved version already exists.',
          serverRecord: existing.record.toJson(),
        ));
        continue;
      }
      final serverId = existing?.serverId ?? 'srv_customer_${_nextId++}';
      _serverVersion++;
      _customers[record.localId] = _StoredRecord(
        serverId: serverId,
        serverVersion: _serverVersion,
        record: record,
      );
      accepted.add(SyncRecordAck(
        entity: 'customer',
        localId: record.localId,
        serverId: serverId,
        serverVersion: _serverVersion,
        syncedAt: syncedAt,
      ));
    }

    for (final record in appointments) {
      final problem = _validateAppointment(record);
      if (problem != null) {
        rejected.add(problem);
        continue;
      }
      final existing = _appointments[record.localId];
      final conflict =
          _conflictWith(existing?.record.updatedAt, record.updatedAt);
      if (existing != null && conflict) {
        rejected.add(SyncRejection(
          entity: 'appointment',
          localId: record.localId,
          code: 'CONFLICT',
          message: 'A newer saved version already exists.',
          serverRecord: existing.record.toJson(),
        ));
        continue;
      }
      final serverId = existing?.serverId ?? 'srv_appointment_${_nextId++}';
      _serverVersion++;
      _appointments[record.localId] = _StoredRecord(
        serverId: serverId,
        serverVersion: _serverVersion,
        record: record,
      );
      accepted.add(SyncRecordAck(
        entity: 'appointment',
        localId: record.localId,
        serverId: serverId,
        serverVersion: _serverVersion,
        syncedAt: syncedAt,
      ));
    }

    return SyncPushResult(
      accepted: accepted,
      rejected: rejected,
      serverVersion: _serverVersion,
      syncedAt: syncedAt,
    );
  }

  @override
  Future<SyncPullResult> pull({int afterVersion = 0}) async {
    _requireAuth();
    final customers = _customers.values
        .where((s) => s.serverVersion > afterVersion)
        .map((s) => s.withServerId())
        .cast<CustomerSyncRecord>()
        .toList();
    final appointments = _appointments.values
        .where((s) => s.serverVersion > afterVersion)
        .map((s) => s.withServerId())
        .cast<AppointmentSyncRecord>()
        .toList();
    return SyncPullResult(
      customers: customers,
      appointments: appointments,
      serverVersion: _serverVersion,
      hasMore: false,
    );
  }

  /// Contract conflict policy: reject when the incoming edit is not newer
  /// than the stored one (equal timestamps prefer the server row).
  bool _conflictWith(DateTime? stored, DateTime incoming) =>
      stored != null && !incoming.isAfter(stored);

  SyncRejection? _validateCustomer(CustomerSyncRecord record) {
    final name = record.name.trim();
    if (name.isEmpty || name.length > 120) {
      return SyncRejection(
        entity: 'customer',
        localId: record.localId,
        code: 'VALIDATION_ERROR',
        message: 'Customer name must be 1-120 characters.',
        fieldErrors: const {'name': 'Must be 1-120 characters.'},
      );
    }
    final email = record.email;
    if (email != null && (email.length > 254 || !email.contains('@'))) {
      return SyncRejection(
        entity: 'customer',
        localId: record.localId,
        code: 'VALIDATION_ERROR',
        message: 'Customer email is not valid.',
        fieldErrors: const {'email': 'Must look like an email address.'},
      );
    }
    return null;
  }

  SyncRejection? _validateAppointment(AppointmentSyncRecord record) {
    if (record.hourlyRateCents < 0 ||
        record.productCostCents < 0 ||
        record.timeSpentMinutes < 0 ||
        record.timeSpentMinutes > 24 * 60) {
      return SyncRejection(
        entity: 'appointment',
        localId: record.localId,
        code: 'VALIDATION_ERROR',
        message: 'Money must be non-negative cents; time 0-1440 minutes.',
      );
    }
    // The server recomputes the total and rejects mismatches loudly
    // (contract: bugs should be loud in sync tests).
    final expected = calculateAppointmentTotalCents(
      hourlyRateCents: record.hourlyRateCents,
      timeSpentMinutes: record.timeSpentMinutes,
      productCostCents: record.productCostCents,
    );
    if (record.appointmentTotalCents != expected) {
      return SyncRejection(
        entity: 'appointment',
        localId: record.localId,
        code: 'VALIDATION_ERROR',
        message: 'Appointment total does not match the calculated total.',
        fieldErrors: {
          'appointmentTotalCents': 'Expected $expected.',
        },
      );
    }
    return null;
  }
}

class _StoredRecord<T> {
  const _StoredRecord({
    required this.serverId,
    required this.serverVersion,
    required this.record,
  });

  final String serverId;
  final int serverVersion;
  final T record;

  /// Returns the record with the server-assigned ID attached, as the pull
  /// endpoint would.
  Object withServerId() {
    final r = record;
    if (r is CustomerSyncRecord) {
      return CustomerSyncRecord(
        localId: r.localId,
        serverId: serverId,
        name: r.name,
        email: r.email,
        createdAt: r.createdAt,
        updatedAt: r.updatedAt,
        deletedAt: r.deletedAt,
      );
    }
    if (r is AppointmentSyncRecord) {
      return AppointmentSyncRecord(
        localId: r.localId,
        serverId: serverId,
        customerLocalId: r.customerLocalId,
        clientNameSnapshot: r.clientNameSnapshot,
        appointmentDate: r.appointmentDate,
        hourlyRateCents: r.hourlyRateCents,
        timeSpentMinutes: r.timeSpentMinutes,
        productCostCents: r.productCostCents,
        appointmentTotalCents: r.appointmentTotalCents,
        createdAt: r.createdAt,
        updatedAt: r.updatedAt,
        deletedAt: r.deletedAt,
      );
    }
    throw StateError('Unknown record type: $r');
  }
}
