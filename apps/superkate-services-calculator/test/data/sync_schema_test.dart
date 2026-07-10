import 'package:flutter_test/flutter_test.dart';
import 'package:sqlite3/sqlite3.dart';
import 'package:superkate_services_calculator/data/persistence_service.dart';
import 'package:superkate_services_calculator/data/sqlite_persistence_service.dart';

void main() {
  late SqlitePersistenceService service;
  var clockTick = 0;

  DateTime clock() => DateTime.utc(2026, 7, 10, 12, clockTick++);

  setUp(() {
    clockTick = 0;
    service = SqlitePersistenceService.inMemory(clock: clock);
  });

  tearDown(() {
    service.close();
  });

  group('schema v2 migration', () {
    test('a v1 database migrates without losing rows', () async {
      final db = sqlite3.openInMemory();
      addTearDown(db.dispose);

      // Build a genuine v1 database by hand: v1 schema, one row per table.
      db.execute('''
        CREATE TABLE customers (
          id TEXT PRIMARY KEY,
          name TEXT NOT NULL,
          email TEXT,
          created_at TEXT NOT NULL,
          updated_at TEXT NOT NULL
        )
        ''');
      db.execute('''
        CREATE TABLE appointments (
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
      db.execute('''
        INSERT INTO customers VALUES
        ('cust-v1', 'Hannah', 'hannah@example.com',
         '2026-07-01T10:00:00.000Z', '2026-07-01T10:00:00.000Z')
        ''');
      db.execute('''
        INSERT INTO appointments VALUES
        ('appt-v1', 'cust-v1', 'Hannah', '2026-07-09T00:00:00.000Z',
         12000, 60, 0, 12000,
         '2026-07-09T12:00:00.000Z', '2026-07-09T12:00:00.000Z', NULL)
        ''');
      db.userVersion = 1;

      final migrated = SqlitePersistenceService.forDatabase(db, clock: clock);

      expect(db.userVersion, 2);
      // Existing rows survive with NULL sync state ("never synced").
      final customers = await migrated.listCustomers();
      expect(customers.single.id, 'cust-v1');
      final row = db.select('SELECT synced_at, server_id FROM customers').single;
      expect(row['synced_at'], isNull);
      expect(row['server_id'], isNull);
      // New bookkeeping tables exist; the cursor row is seeded.
      expect(db.select('SELECT * FROM sync_outbox'), isEmpty);
      expect(
        db.select('SELECT last_server_version FROM sync_state').single.values,
        [0],
      );
      // Deletes on the migrated database write outbox tombstones.
      await migrated.deleteAppointment('appt-v1');
      expect(migrated.listSyncOutbox().single.localId, 'appt-v1');
    });

    test('a fresh database opens straight at v2 and re-opens idempotently',
        () {
      final db = sqlite3.openInMemory();
      addTearDown(db.dispose);
      SqlitePersistenceService.forDatabase(db, clock: clock);
      expect(db.userVersion, 2);
      // Re-running migrations on an already-v2 database must not throw.
      SqlitePersistenceService.forDatabase(db, clock: clock);
      expect(db.userVersion, 2);
    });
  });

  group('deletion outbox', () {
    test('deleting a customer records a customer tombstone', () async {
      final customer = await service.upsertCustomer(
        const UpsertCustomerInput(name: 'Hannah', email: null),
      );
      await service.deleteCustomer(customer.id);

      final entry = service.listSyncOutbox().single;
      expect(entry.entity, 'customer');
      expect(entry.localId, customer.id);
      expect(entry.serverId, isNull); // never synced
      expect(entry.deletedAt.isUtc, isTrue);
    });

    test('deleting an appointment records a tombstone and still deletes',
        () async {
      final appointment = await service.createAppointment(
        CreateAppointmentInput(
          customerId: null,
          clientName: 'Walk-in',
          appointmentDate: DateTime.utc(2026, 7, 9),
          hourlyRateCents: 8000,
          timeSpentMinutes: 30,
          productCostCents: 0,
        ),
      );
      await service.deleteAppointment(appointment.id);

      expect(await service.listAppointments(), isEmpty);
      final entry = service.listSyncOutbox().single;
      expect(entry.entity, 'appointment');
      expect(entry.localId, appointment.id);
    });

    test('deleting a missing id writes no tombstone', () async {
      await service.deleteAppointment('appt-nope');
      await service.deleteCustomer('cust-nope');
      expect(service.listSyncOutbox(), isEmpty);
    });

    test('customer delete still detaches appointments in the same transaction',
        () async {
      final customer = await service.upsertCustomer(
        const UpsertCustomerInput(name: 'Hannah', email: null),
      );
      await service.createAppointment(
        CreateAppointmentInput(
          customerId: customer.id,
          clientName: customer.name,
          appointmentDate: DateTime.utc(2026, 7, 9),
          hourlyRateCents: 12000,
          timeSpentMinutes: 60,
          productCostCents: 0,
        ),
      );
      await service.deleteCustomer(customer.id);

      final appointments = await service.listAppointments();
      expect(appointments.single.customerId, isNull);
      expect(appointments.single.clientNameSnapshot, 'Hannah');
      expect(service.listSyncOutbox().single.entity, 'customer');
    });
  });
}
