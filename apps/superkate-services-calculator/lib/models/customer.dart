/// Customer record for the Superkate Services Calculator.
///
/// Matches the SPEC.md data model: id, name, optional email, timestamps.
/// Immutable value object; the persistence service produces updated copies.
library;

class Customer {
  const Customer({
    required this.id,
    required this.name,
    required this.email,
    required this.createdAt,
    required this.updatedAt,
  });

  final String id;
  final String name;

  /// Optional receipt-prefill email. Stored as `null` when blank (never `''`).
  final String? email;

  final DateTime createdAt;
  final DateTime updatedAt;

  Customer copyWith({
    String? name,
    String? email,
    bool clearEmail = false,
    DateTime? updatedAt,
  }) {
    return Customer(
      id: id,
      name: name ?? this.name,
      email: clearEmail ? null : (email ?? this.email),
      createdAt: createdAt,
      updatedAt: updatedAt ?? this.updatedAt,
    );
  }

  /// Serialization for the local database/storage adapter. ISO-8601 strings
  /// keep timestamps portable across the storage and future sync boundaries.
  Map<String, dynamic> toMap() => {
        'id': id,
        'name': name,
        'email': email,
        'createdAt': createdAt.toUtc().toIso8601String(),
        'updatedAt': updatedAt.toUtc().toIso8601String(),
      };

  factory Customer.fromMap(Map<String, dynamic> map) => Customer(
        id: map['id'] as String,
        name: map['name'] as String,
        email: map['email'] as String?,
        createdAt: DateTime.parse(map['createdAt'] as String),
        updatedAt: DateTime.parse(map['updatedAt'] as String),
      );

  @override
  bool operator ==(Object other) =>
      other is Customer &&
      other.id == id &&
      other.name == name &&
      other.email == email &&
      other.createdAt == createdAt &&
      other.updatedAt == updatedAt;

  @override
  int get hashCode => Object.hash(id, name, email, createdAt, updatedAt);
}
