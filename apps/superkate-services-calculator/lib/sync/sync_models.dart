/// Wire models for the Hair by Superkate sync contract.
///
/// Mirrors projects/superkate-services-calculator/docs/backend-api-schema-contract.md
/// (t-027). These are the shapes that cross the app/backend boundary — the app
/// keeps its own local models (`Customer`, `Appointment`) as UI keys and maps
/// to these records only at the sync edge. Local-first stays the rule: nothing
/// here uploads real customer data; production sync is disabled (see
/// `DisabledSyncClient`).
library;

/// SPEC.md "Sync / Account Status": the app surfaces whether it is synced,
/// offline, has pending changes, or hit an error — without leaking customer
/// data into the message.
enum SyncStatus { disabled, idle, pendingChanges, syncing, offline, error }

/// Customer record as it crosses the sync boundary. `localId` is the app's
/// own UUID and stays the primary key on the client; `serverId` arrives from
/// the backend on first accepted upsert.
class CustomerSyncRecord {
  const CustomerSyncRecord({
    required this.localId,
    this.serverId,
    required this.name,
    required this.email,
    required this.createdAt,
    required this.updatedAt,
    this.deletedAt,
  });

  final String localId;
  final String? serverId;
  final String name;
  final String? email;
  final DateTime createdAt;
  final DateTime updatedAt;

  /// Tombstone marker — deletion propagates as an upsert, never a physical
  /// delete (contract: "no bulk physical delete").
  final DateTime? deletedAt;

  bool get isTombstone => deletedAt != null;

  Map<String, dynamic> toJson() => {
        'localId': localId,
        if (serverId != null) 'serverId': serverId,
        'name': name,
        'email': email,
        'createdAt': createdAt.toUtc().toIso8601String(),
        'updatedAt': updatedAt.toUtc().toIso8601String(),
        'deletedAt': deletedAt?.toUtc().toIso8601String(),
      };

  factory CustomerSyncRecord.fromJson(Map<String, dynamic> json) =>
      CustomerSyncRecord(
        localId: json['localId'] as String,
        serverId: json['serverId'] as String?,
        name: json['name'] as String,
        email: json['email'] as String?,
        createdAt: DateTime.parse(json['createdAt'] as String),
        updatedAt: DateTime.parse(json['updatedAt'] as String),
        deletedAt: json['deletedAt'] == null
            ? null
            : DateTime.parse(json['deletedAt'] as String),
      );
}

/// Appointment record as it crosses the sync boundary. The server recomputes
/// `appointmentTotalCents` and rejects mismatches loudly (contract choice:
/// "prefer rejection for sync contract tests so bugs are loud").
class AppointmentSyncRecord {
  const AppointmentSyncRecord({
    required this.localId,
    this.serverId,
    this.customerLocalId,
    required this.clientNameSnapshot,
    required this.appointmentDate,
    required this.hourlyRateCents,
    required this.timeSpentMinutes,
    required this.productCostCents,
    required this.appointmentTotalCents,
    required this.createdAt,
    required this.updatedAt,
    this.deletedAt,
  });

  final String localId;
  final String? serverId;
  final String? customerLocalId;
  final String clientNameSnapshot;
  final DateTime appointmentDate;
  final int hourlyRateCents;
  final int timeSpentMinutes;
  final int productCostCents;
  final int appointmentTotalCents;
  final DateTime createdAt;
  final DateTime updatedAt;
  final DateTime? deletedAt;

  bool get isTombstone => deletedAt != null;

  Map<String, dynamic> toJson() => {
        'localId': localId,
        if (serverId != null) 'serverId': serverId,
        'customerLocalId': customerLocalId,
        'clientNameSnapshot': clientNameSnapshot,
        'appointmentDate':
            appointmentDate.toUtc().toIso8601String().substring(0, 10),
        'hourlyRateCents': hourlyRateCents,
        'timeSpentMinutes': timeSpentMinutes,
        'productCostCents': productCostCents,
        'appointmentTotalCents': appointmentTotalCents,
        'createdAt': createdAt.toUtc().toIso8601String(),
        'updatedAt': updatedAt.toUtc().toIso8601String(),
        'deletedAt': deletedAt?.toUtc().toIso8601String(),
      };

  factory AppointmentSyncRecord.fromJson(Map<String, dynamic> json) =>
      AppointmentSyncRecord(
        localId: json['localId'] as String,
        serverId: json['serverId'] as String?,
        customerLocalId: json['customerLocalId'] as String?,
        clientNameSnapshot: json['clientNameSnapshot'] as String,
        appointmentDate: DateTime.parse(json['appointmentDate'] as String),
        hourlyRateCents: json['hourlyRateCents'] as int,
        timeSpentMinutes: json['timeSpentMinutes'] as int,
        productCostCents: json['productCostCents'] as int,
        appointmentTotalCents: json['appointmentTotalCents'] as int,
        createdAt: DateTime.parse(json['createdAt'] as String),
        updatedAt: DateTime.parse(json['updatedAt'] as String),
        deletedAt: json['deletedAt'] == null
            ? null
            : DateTime.parse(json['deletedAt'] as String),
      );
}

/// GET /api/superkate/sync/bootstrap response payload.
class SyncBootstrap {
  const SyncBootstrap({
    required this.businessSlug,
    required this.ownerUserId,
    required this.serverVersion,
    required this.features,
  });

  final String businessSlug;
  final String ownerUserId;
  final int serverVersion;

  /// Feature switches from the server. `directEmailSend` and `analytics`
  /// must stay false in the beta contract.
  final Map<String, bool> features;
}

/// Per-record acknowledgement inside a push response: the server hands back
/// both IDs so the app can map local → server without replacing local keys.
class SyncRecordAck {
  const SyncRecordAck({
    required this.entity,
    required this.localId,
    required this.serverId,
    required this.serverVersion,
    required this.syncedAt,
  });

  final String entity; // 'customer' | 'appointment'
  final String localId;
  final String serverId;
  final int serverVersion;
  final DateTime syncedAt;
}

/// Per-record rejection inside a push response. `serverRecord` carries the
/// current server row on CONFLICT so the client can reconcile.
class SyncRejection {
  const SyncRejection({
    required this.entity,
    required this.localId,
    required this.code,
    required this.message,
    this.fieldErrors = const {},
    this.serverRecord,
  });

  final String entity;
  final String localId;
  final String code; // 'VALIDATION_ERROR' | 'CONFLICT' | ...
  final String message;
  final Map<String, String> fieldErrors;
  final Map<String, dynamic>? serverRecord;
}

/// POST /api/superkate/sync/push response payload.
class SyncPushResult {
  const SyncPushResult({
    required this.accepted,
    required this.rejected,
    required this.serverVersion,
    required this.syncedAt,
  });

  final List<SyncRecordAck> accepted;
  final List<SyncRejection> rejected;
  final int serverVersion;
  final DateTime syncedAt;

  bool get fullyAccepted => rejected.isEmpty;
}

/// GET /api/superkate/sync/pull response payload. Includes tombstones so the
/// local client can propagate deletions.
class SyncPullResult {
  const SyncPullResult({
    required this.customers,
    required this.appointments,
    required this.serverVersion,
    required this.hasMore,
  });

  final List<CustomerSyncRecord> customers;
  final List<AppointmentSyncRecord> appointments;
  final int serverVersion;
  final bool hasMore;
}

/// Thrown by sync calls when the client cannot or must not talk to a backend:
/// production sync is disabled in this beta, and the fake client throws it
/// for unauthenticated access.
class SyncUnavailableException implements Exception {
  const SyncUnavailableException(this.message);

  final String message;

  @override
  String toString() => 'SyncUnavailableException: $message';
}
