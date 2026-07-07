/// Dependency-free client-side id generation.
///
/// The persistence layer needs stable, unique string ids that survive future
/// cloud sync (SPEC.md "Beta sync expectation"). We avoid pulling in a uuid
/// package so the domain layer stays dependency-free and testable; a
/// timestamp + monotonic counter is sufficient for single-device local-first
/// use and collision-safe within a process.
library;

int _counter = 0;

/// Returns a new locally-unique id string, e.g. `cust_l8x1a2b3_004`.
///
/// [prefix] namespaces the id by entity (`cust`, `appt`) so ids are readable
/// in debugging without leaking customer data.
String newLocalId(String prefix) {
  final micros = DateTime.now().microsecondsSinceEpoch;
  final seq = (_counter = (_counter + 1) & 0xffff);
  final stamp = micros.toRadixString(36);
  final tail = seq.toRadixString(36).padLeft(3, '0');
  return '${prefix}_${stamp}_$tail';
}
