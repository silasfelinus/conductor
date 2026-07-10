library;

import 'package:path/path.dart' as p;
import 'package:path_provider/path_provider.dart';
import 'package:sqlite3/sqlite3.dart';

import '../domain/ids.dart';
import '../domain/money.dart';
import '../domain/validation.dart';
import '../models/appointment.dart';
import '../models/customer.dart';
import 'persistence_service.dart';

/// A pending deletion tombstone awaiting sync propagation
/// (docs/sync-engine-design.md §2). `serverId` is null when the row was
/// never synced — the engine may drop those without a network round-trip.
class SyncOutboxEntry {
  const SyncOutboxEntry({
    required this.entity,
    required this.localId,
    required this.serverId,
    required this.deletedAt,
  });

  final String entity; // 'customer' | 'appointment'
  final String localId;
  final String? serverId;
  final DateTime deletedAt;
}

class SqlitePersistenceService implements PersistenceService {
  SqlitePersistenceService._(
    this._db, {
    DateTime Function()? clock,
    bool ownsDatabase = true,
  })  : _now = clock ?? DateTime.now,
        _ownsDatabase = ownsDatabase {
    _configure();
    _migrate();
  }

  static Future<SqlitePersistenceService> open({
    DateTime Function()? clock,
    String? filename,
  }) async {
    final supportDir = await getApplicationSupportDirectory();
    await supportDir.create(recursive: true);
    final dbPath = p.join(
      supportDir.path,
      filename ?? 'superkate_services_calculator.sqlite',
    );
    return SqlitePersistenceService._(
      sqlite3.open(dbPath),
      clock: clock,
    );
  }

  factory SqlitePersistenceService.inMemory({DateTime Function()? clock}) {
    return SqlitePersistenceService._(
      sqlite3.openInMemory(),
      clock: clock,
    );
  }

  /// Wraps an already-open database (e.g. a test-seeded older-schema DB) and
  /// runs migrations on it. The caller keeps ownership of [db].
  factory SqlitePersistenceService.forDatabase(
    Database db, {
    DateTime Function()? clock,
  }) {
    return SqlitePersistenceService._(
      db,
      clock: clock,
      ownsDatabase: false,
    );
  }

  final Database _db;
  final DateTime Function() _now;
  final bool _ownsDatabase;

  void close() {
    if (_ownsDatabase) {
      _db.dispose();
    }
  }

  @override
  Future<List<Customer>> listCustomers() async {
    final rows = _db.select(
      'SELECT * FROM customers ORDER BY lower(name) ASC, created_at ASC',
    );
    return rows.map(_customerFromRow).toList();
  }

  @override
  Future<Customer?> getCustomer(String customerId) async {
    final rows = _db.select(
      'SELECT * FROM customers WHERE id = ? LIMIT 1',
      [customerId],
    );
    if (rows.isEmpty) {
      return null;
    }
    return _customerFromRow(rows.single);
  }

  @override
  Future<Customer> upsertCustomer(UpsertCustomerInput input) async {
    final name = validateClientName(input.name);
    final email = validateOptionalEmail(input.email);
    final now = _now();
    final nowIso = _toIso(now);

    if (input.id != null) {
      final existing = await getCustomer(input.id!);
      if (existing == null) {
        throw const ValidationException('That customer no longer exists.');
      }
      final updated = existing.copyWith(
        name: name,
        email: email,
        clearEmail: email == null,
        updatedAt: now,
      );
      _db.execute(
        '''
        UPDATE customers
        SET name = ?, email = ?, updated_at = ?
        WHERE id = ?
        ''',
        [updated.name, updated.email, _toIso(updated.updatedAt), updated.id],
      );
      return updated;
    }

    final created = Customer(
      id: newLocalId('cust'),
      name: name,
      email: email,
      createdAt: now,
      updatedAt: now,
    );
    _db.execute(
      '''
      INSERT INTO customers (id, name, email, created_at, updated_at)
      VALUES (?, ?, ?, ?, ?)
      ''',
      [created.id, created.name, created.email, nowIso, nowIso],
    );
    return created;
  }

  @override
  Future<void> deleteCustomer(String customerId) async {
    _db.execute('BEGIN IMMEDIATE TRANSACTION');
    try {
      _writeOutboxTombstone('customer', customerId, 'customers');
      _db.execute('DELETE FROM customers WHERE id = ?', [customerId]);
      _db.execute(
        '''
        UPDATE appointments
        SET customer_id = NULL, updated_at = ?
        WHERE customer_id = ?
        ''',
        [_toIso(_now()), customerId],
      );
      _db.execute('COMMIT');
    } catch (_) {
      _db.execute('ROLLBACK');
      rethrow;
    }
  }

  @override
  Future<List<Appointment>> listAppointments([
    AppointmentFilter? filter,
  ]) async {
    final rows = _db.select('SELECT * FROM appointments');
    Iterable<Appointment> results = rows.map(_appointmentFromRow);

    if (filter != null) {
      if (filter.customerId != null) {
        results = results.where((a) => a.customerId == filter.customerId);
      }
      final query = filter.clientNameQuery?.trim().toLowerCase();
      if (query != null && query.isNotEmpty) {
        results = results.where(
          (a) => a.clientNameSnapshot.toLowerCase().contains(query),
        );
      }
      if (filter.appointmentDateFrom != null) {
        final from = _dateOnly(filter.appointmentDateFrom!);
        results = results.where(
          (a) => !_dateOnly(a.appointmentDate).isBefore(from),
        );
      }
      if (filter.appointmentDateTo != null) {
        final to = _dateOnly(filter.appointmentDateTo!);
        results = results.where(
          (a) => !_dateOnly(a.appointmentDate).isAfter(to),
        );
      }
    }

    return results.toList()
      ..sort((a, b) => b.appointmentDate.compareTo(a.appointmentDate));
  }

  @override
  Future<Appointment> createAppointment(CreateAppointmentInput input) async {
    final clientName = validateClientName(input.clientName);
    final hourlyRateCents = validateHourlyRateCents(input.hourlyRateCents);
    final timeSpentMinutes = validateTimeSpentMinutes(input.timeSpentMinutes);
    final productCostCents = validateProductCostCents(input.productCostCents);

    if (input.customerId != null && await getCustomer(input.customerId!) == null) {
      throw const ValidationException('That customer no longer exists.');
    }

    final totalCents = calculateAppointmentTotalCents(
      hourlyRateCents: hourlyRateCents,
      timeSpentMinutes: timeSpentMinutes,
      productCostCents: productCostCents,
    );
    final now = _now();
    final appointment = Appointment(
      id: newLocalId('appt'),
      customerId: input.customerId,
      clientNameSnapshot: clientName,
      appointmentDate: input.appointmentDate,
      hourlyRateCents: hourlyRateCents,
      timeSpentMinutes: timeSpentMinutes,
      productCostCents: productCostCents,
      appointmentTotalCents: totalCents,
      createdAt: now,
      updatedAt: now,
      syncedAt: null,
    );

    _db.execute(
      '''
      INSERT INTO appointments (
        id,
        customer_id,
        client_name_snapshot,
        appointment_date,
        hourly_rate_cents,
        time_spent_minutes,
        product_cost_cents,
        appointment_total_cents,
        created_at,
        updated_at,
        synced_at
      ) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
      ''',
      [
        appointment.id,
        appointment.customerId,
        appointment.clientNameSnapshot,
        _toIso(appointment.appointmentDate),
        appointment.hourlyRateCents,
        appointment.timeSpentMinutes,
        appointment.productCostCents,
        appointment.appointmentTotalCents,
        _toIso(appointment.createdAt),
        _toIso(appointment.updatedAt),
        appointment.syncedAt == null ? null : _toIso(appointment.syncedAt!),
      ],
    );
    return appointment;
  }

  @override
  Future<void> deleteAppointment(String appointmentId) async {
    _db.execute('BEGIN IMMEDIATE TRANSACTION');
    try {
      _writeOutboxTombstone('appointment', appointmentId, 'appointments');
      _db.execute('DELETE FROM appointments WHERE id = ?', [appointmentId]);
      _db.execute('COMMIT');
    } catch (_) {
      _db.execute('ROLLBACK');
      rethrow;
    }
  }

  /// Records a deletion tombstone for the future SyncEngine
  /// (docs/sync-engine-design.md §2). Rows are physically deleted locally;
  /// the outbox is what lets the deletion propagate to other devices later.
  /// The engine may drop entries whose server_id is null (never synced).
  void _writeOutboxTombstone(String entity, String localId, String table) {
    final rows = _db.select(
      'SELECT server_id FROM $table WHERE id = ? LIMIT 1',
      [localId],
    );
    if (rows.isEmpty) return; // nothing deleted → nothing to propagate
    _db.execute(
      '''
      INSERT OR REPLACE INTO sync_outbox (entity, local_id, server_id, deleted_at)
      VALUES (?, ?, ?, ?)
      ''',
      [entity, localId, rows.single['server_id'] as String?, _toIso(_now())],
    );
  }

  /// Pending deletion tombstones, oldest first. Not part of
  /// [PersistenceService] — this is the SyncEngine's (and tests') window
  /// into sync bookkeeping.
  List<SyncOutboxEntry> listSyncOutbox() {
    final rows = _db.select(
      'SELECT entity, local_id, server_id, deleted_at FROM sync_outbox '
      'ORDER BY deleted_at ASC, local_id ASC',
    );
    return rows
        .map((row) => SyncOutboxEntry(
              entity: row['entity'] as String,
              localId: row['local_id'] as String,
              serverId: row['server_id'] as String?,
              deletedAt: _parseIso(row['deleted_at']),
            ))
        .toList();
  }

  void _configure() {
    _db.execute('PRAGMA foreign_keys = ON');
  }

  void _migrate() {
    final version = _db.userVersion;
    if (version < 1) {
      _db.execute('BEGIN IMMEDIATE TRANSACTION');
      try {
        _db.execute('''
          CREATE TABLE IF NOT EXISTS customers (
            id TEXT PRIMARY KEY,
            name TEXT NOT NULL,
            email TEXT,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL
          )
          ''');
        _db.execute('''
          CREATE TABLE IF NOT EXISTS appointments (
            id TEXT PRIMARY KEY,
            customer_id TEXT REFERENCES customers(id) ON DELETE SET NULL,
            client_name_snapshot TEXT NOT NULL,
            appointment_date TEXT NOT NULL,
            hourly_rate_cents INTEGER NOT NULL,
            time_spent_minutes INTEGER NOT NULL,
            product_cost_cents INTEGER NOT NULL,
            appointment_total_cents INTEGER NOT NULL,
            created_at TEXT NOT NULL,
            updated_at TEXT NOT NULL,
            synced_at TEXT
          )
          ''');
        _db.execute(
          'CREATE INDEX IF NOT EXISTS idx_customers_name ON customers(name)',
        );
        _db.execute(
          'CREATE INDEX IF NOT EXISTS idx_appointments_customer_id ON appointments(customer_id)',
        );
        _db.execute(
          'CREATE INDEX IF NOT EXISTS idx_appointments_date ON appointments(appointment_date)',
        );
        _db.userVersion = 1;
        _db.execute('COMMIT');
      } catch (_) {
        _db.execute('ROLLBACK');
        rethrow;
      }
    }
    if (_db.userVersion < 2) {
      // Schema v2 (docs/sync-engine-design.md §1-2): sync bookkeeping columns
      // and the deletion outbox. Additive only; existing rows stay untouched
      // with NULL sync state, which correctly reads as "never synced".
      _db.execute('BEGIN IMMEDIATE TRANSACTION');
      try {
        _db.execute('ALTER TABLE customers ADD COLUMN synced_at TEXT');
        _db.execute('ALTER TABLE customers ADD COLUMN server_id TEXT');
        _db.execute('ALTER TABLE appointments ADD COLUMN server_id TEXT');
        _db.execute('''
          CREATE TABLE IF NOT EXISTS sync_outbox (
            entity TEXT NOT NULL,
            local_id TEXT NOT NULL,
            server_id TEXT,
            deleted_at TEXT NOT NULL,
            PRIMARY KEY (entity, local_id)
          )
          ''');
        _db.execute('''
          CREATE TABLE IF NOT EXISTS sync_state (
            id INTEGER PRIMARY KEY CHECK (id = 1),
            last_server_version INTEGER NOT NULL DEFAULT 0
          )
          ''');
        _db.execute(
          'INSERT OR IGNORE INTO sync_state (id, last_server_version) VALUES (1, 0)',
        );
        _db.userVersion = 2;
        _db.execute('COMMIT');
      } catch (_) {
        _db.execute('ROLLBACK');
        rethrow;
      }
    }
  }

  static Customer _customerFromRow(Row row) => Customer(
        id: row['id'] as String,
        name: row['name'] as String,
        email: row['email'] as String?,
        createdAt: _parseIso(row['created_at']),
        updatedAt: _parseIso(row['updated_at']),
      );

  static Appointment _appointmentFromRow(Row row) => Appointment(
        id: row['id'] as String,
        customerId: row['customer_id'] as String?,
        clientNameSnapshot: row['client_name_snapshot'] as String,
        appointmentDate: _parseIso(row['appointment_date']),
        hourlyRateCents: _asInt(row['hourly_rate_cents']),
        timeSpentMinutes: _asInt(row['time_spent_minutes']),
        productCostCents: _asInt(row['product_cost_cents']),
        appointmentTotalCents: _asInt(row['appointment_total_cents']),
        createdAt: _parseIso(row['created_at']),
        updatedAt: _parseIso(row['updated_at']),
        syncedAt: row['synced_at'] == null ? null : _parseIso(row['synced_at']),
      );

  static int _asInt(Object? value) {
    if (value is int) {
      return value;
    }
    if (value is num) {
      return value.toInt();
    }
    return int.parse(value.toString());
  }

  static DateTime _parseIso(Object? value) => DateTime.parse(value as String);

  static String _toIso(DateTime value) => value.toUtc().toIso8601String();

  static DateTime _dateOnly(DateTime d) => DateTime(d.year, d.month, d.day);
}
