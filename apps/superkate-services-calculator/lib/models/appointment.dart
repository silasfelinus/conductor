/// Appointment record for the Superkate Services Calculator.
///
/// Matches the SPEC.md data model. Money is cents, time is minutes, and the
/// total is always calculated (see domain/money.dart), never trusted from UI.
/// `clientNameSnapshot` preserves the name used at appointment time so historic
/// receipts stay readable even if the customer profile is later renamed.
library;

class Appointment {
  const Appointment({
    required this.id,
    required this.customerId,
    required this.clientNameSnapshot,
    required this.appointmentDate,
    required this.hourlyRateCents,
    required this.timeSpentMinutes,
    required this.productCostCents,
    required this.appointmentTotalCents,
    required this.createdAt,
    required this.updatedAt,
    required this.syncedAt,
  });

  final String id;

  /// `null` for a one-off client not saved to the customer database.
  final String? customerId;

  /// Name captured at appointment time; independent of the Customer record.
  final String clientNameSnapshot;

  final DateTime appointmentDate;
  final int hourlyRateCents;
  final int timeSpentMinutes;
  final int productCostCents;

  /// Always derived from the fields above; stored for query/sort convenience.
  final int appointmentTotalCents;

  final DateTime createdAt;
  final DateTime updatedAt;

  /// `null` until a future sync pass marks the record synced. Present now so
  /// local records don't fight the beta sync design (SPEC.md).
  final DateTime? syncedAt;

  Appointment copyWith({
    String? customerId,
    bool clearCustomerId = false,
    String? clientNameSnapshot,
    DateTime? appointmentDate,
    int? hourlyRateCents,
    int? timeSpentMinutes,
    int? productCostCents,
    int? appointmentTotalCents,
    DateTime? updatedAt,
    DateTime? syncedAt,
    bool clearSyncedAt = false,
  }) {
    return Appointment(
      id: id,
      customerId: clearCustomerId ? null : (customerId ?? this.customerId),
      clientNameSnapshot: clientNameSnapshot ?? this.clientNameSnapshot,
      appointmentDate: appointmentDate ?? this.appointmentDate,
      hourlyRateCents: hourlyRateCents ?? this.hourlyRateCents,
      timeSpentMinutes: timeSpentMinutes ?? this.timeSpentMinutes,
      productCostCents: productCostCents ?? this.productCostCents,
      appointmentTotalCents:
          appointmentTotalCents ?? this.appointmentTotalCents,
      createdAt: createdAt,
      updatedAt: updatedAt ?? this.updatedAt,
      syncedAt: clearSyncedAt ? null : (syncedAt ?? this.syncedAt),
    );
  }

  Map<String, dynamic> toMap() => {
        'id': id,
        'customerId': customerId,
        'clientNameSnapshot': clientNameSnapshot,
        'appointmentDate': appointmentDate.toUtc().toIso8601String(),
        'hourlyRateCents': hourlyRateCents,
        'timeSpentMinutes': timeSpentMinutes,
        'productCostCents': productCostCents,
        'appointmentTotalCents': appointmentTotalCents,
        'createdAt': createdAt.toUtc().toIso8601String(),
        'updatedAt': updatedAt.toUtc().toIso8601String(),
        'syncedAt': syncedAt?.toUtc().toIso8601String(),
      };

  factory Appointment.fromMap(Map<String, dynamic> map) => Appointment(
        id: map['id'] as String,
        customerId: map['customerId'] as String?,
        clientNameSnapshot: map['clientNameSnapshot'] as String,
        appointmentDate: DateTime.parse(map['appointmentDate'] as String),
        hourlyRateCents: map['hourlyRateCents'] as int,
        timeSpentMinutes: map['timeSpentMinutes'] as int,
        productCostCents: map['productCostCents'] as int,
        appointmentTotalCents: map['appointmentTotalCents'] as int,
        createdAt: DateTime.parse(map['createdAt'] as String),
        updatedAt: DateTime.parse(map['updatedAt'] as String),
        syncedAt: map['syncedAt'] == null
            ? null
            : DateTime.parse(map['syncedAt'] as String),
      );

  @override
  bool operator ==(Object other) =>
      other is Appointment &&
      other.id == id &&
      other.customerId == customerId &&
      other.clientNameSnapshot == clientNameSnapshot &&
      other.appointmentDate == appointmentDate &&
      other.hourlyRateCents == hourlyRateCents &&
      other.timeSpentMinutes == timeSpentMinutes &&
      other.productCostCents == productCostCents &&
      other.appointmentTotalCents == appointmentTotalCents &&
      other.createdAt == createdAt &&
      other.updatedAt == updatedAt &&
      other.syncedAt == syncedAt;

  @override
  int get hashCode => Object.hashAll([
        id,
        customerId,
        clientNameSnapshot,
        appointmentDate,
        hourlyRateCents,
        timeSpentMinutes,
        productCostCents,
        appointmentTotalCents,
        createdAt,
        updatedAt,
        syncedAt,
      ]);
}
