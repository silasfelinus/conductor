import 'package:flutter_test/flutter_test.dart';
import 'package:superkate_services_calculator/domain/money.dart';
import 'package:superkate_services_calculator/sync/disabled_sync_client.dart';
import 'package:superkate_services_calculator/sync/fake_sync_client.dart';
import 'package:superkate_services_calculator/sync/sync_models.dart';

CustomerSyncRecord _customer({
  String localId = 'local-customer-1',
  String name = 'Test Client',
  String? email = 'test.client@example.test',
  DateTime? updatedAt,
  DateTime? deletedAt,
}) {
  final created = DateTime.utc(2026, 7, 10, 8);
  return CustomerSyncRecord(
    localId: localId,
    name: name,
    email: email,
    createdAt: created,
    updatedAt: updatedAt ?? created,
    deletedAt: deletedAt,
  );
}

AppointmentSyncRecord _appointment({
  String localId = 'local-appt-1',
  String? customerLocalId = 'local-customer-1',
  int hourlyRateCents = 8000,
  int timeSpentMinutes = 90,
  int productCostCents = 1500,
  int? totalCents,
  DateTime? updatedAt,
  DateTime? deletedAt,
}) {
  final created = DateTime.utc(2026, 7, 10, 9);
  return AppointmentSyncRecord(
    localId: localId,
    customerLocalId: customerLocalId,
    clientNameSnapshot: 'Test Client',
    appointmentDate: DateTime.utc(2026, 7, 8),
    hourlyRateCents: hourlyRateCents,
    timeSpentMinutes: timeSpentMinutes,
    productCostCents: productCostCents,
    appointmentTotalCents: totalCents ??
        calculateAppointmentTotalCents(
          hourlyRateCents: hourlyRateCents,
          timeSpentMinutes: timeSpentMinutes,
          productCostCents: productCostCents,
        ),
    createdAt: created,
    updatedAt: updatedAt ?? created,
    deletedAt: deletedAt,
  );
}

void main() {
  group('DisabledSyncClient (production default)', () {
    test('reports sync unavailable and refuses every call loudly', () async {
      const client = DisabledSyncClient();
      expect(client.isSyncAvailable, isFalse);
      expect(client.bootstrap, throwsA(isA<SyncUnavailableException>()));
      expect(() => client.push(customers: [_customer()]),
          throwsA(isA<SyncUnavailableException>()));
      expect(() => client.pull(), throwsA(isA<SyncUnavailableException>()));
    });
  });

  group('FakeSyncClient bootstrap', () {
    test('returns owner scope and keeps email/analytics switched off',
        () async {
      final client = FakeSyncClient();
      final boot = await client.bootstrap();
      expect(boot.businessSlug, 'hair-by-superkate');
      expect(boot.ownerUserId, 'test-owner-superkate');
      expect(boot.serverVersion, 0);
      expect(boot.features['pushCustomers'], isTrue);
      expect(boot.features['directEmailSend'], isFalse);
      expect(boot.features['analytics'], isFalse);
    });

    test('requires auth on every route', () async {
      final client = FakeSyncClient(authenticated: false);
      expect(client.bootstrap, throwsA(isA<SyncUnavailableException>()));
      expect(() => client.push(customers: [_customer()]),
          throwsA(isA<SyncUnavailableException>()));
      expect(() => client.pull(), throwsA(isA<SyncUnavailableException>()));
    });
  });

  group('FakeSyncClient push', () {
    test('accepts valid records, assigns server IDs, bumps serverVersion',
        () async {
      final client = FakeSyncClient();
      final result = await client.push(
        customers: [_customer()],
        appointments: [_appointment()],
      );

      expect(result.fullyAccepted, isTrue);
      expect(result.accepted, hasLength(2));
      expect(result.serverVersion, 2);
      final customerAck =
          result.accepted.singleWhere((a) => a.entity == 'customer');
      expect(customerAck.localId, 'local-customer-1');
      expect(customerAck.serverId, startsWith('srv_customer_'));
    });

    test('re-upserting keeps the same serverId and bumps the version',
        () async {
      final client = FakeSyncClient();
      final first = await client.push(customers: [_customer()]);
      final second = await client.push(customers: [
        _customer(
          name: 'Renamed Client',
          updatedAt: DateTime.utc(2026, 7, 10, 10),
        ),
      ]);

      expect(second.fullyAccepted, isTrue);
      expect(second.accepted.single.serverId, first.accepted.single.serverId);
      expect(second.serverVersion, greaterThan(first.serverVersion));
    });

    test('rejects a mismatched appointment total loudly', () async {
      final client = FakeSyncClient();
      final result =
          await client.push(appointments: [_appointment(totalCents: 999)]);

      expect(result.accepted, isEmpty);
      expect(result.rejected.single.code, 'VALIDATION_ERROR');
      expect(result.rejected.single.fieldErrors,
          contains('appointmentTotalCents'));
    });

    test('rejects an older edit as CONFLICT and returns the server row',
        () async {
      final client = FakeSyncClient();
      await client
          .push(customers: [_customer(updatedAt: DateTime.utc(2026, 7, 10, 12))]);
      final result = await client.push(customers: [
        _customer(
          name: 'Stale Edit',
          updatedAt: DateTime.utc(2026, 7, 10, 11),
        ),
      ]);

      expect(result.accepted, isEmpty);
      final rejection = result.rejected.single;
      expect(rejection.code, 'CONFLICT');
      expect(rejection.serverRecord, isNotNull);
      expect(rejection.serverRecord!['name'], 'Test Client');
    });

    test('partial success reports rejected rows item-by-item', () async {
      final client = FakeSyncClient();
      final result = await client.push(customers: [
        _customer(),
        _customer(localId: 'local-customer-2', name: ''),
      ]);

      expect(result.accepted, hasLength(1));
      expect(result.rejected, hasLength(1));
      expect(result.rejected.single.localId, 'local-customer-2');
    });
  });

  group('FakeSyncClient pull', () {
    test('returns only rows after the version cursor', () async {
      final client = FakeSyncClient();
      final first = await client.push(customers: [_customer()]);
      await client.push(customers: [
        _customer(localId: 'local-customer-2', name: 'Second Client'),
      ]);

      final all = await client.pull();
      expect(all.customers, hasLength(2));

      final delta = await client.pull(afterVersion: first.serverVersion);
      expect(delta.customers, hasLength(1));
      expect(delta.customers.single.localId, 'local-customer-2');
      expect(delta.customers.single.serverId, isNotNull);
      expect(delta.hasMore, isFalse);
    });

    test('propagates tombstones so deletions reach other devices', () async {
      final client = FakeSyncClient();
      await client.push(appointments: [_appointment()]);
      await client.push(appointments: [
        _appointment(
          updatedAt: DateTime.utc(2026, 7, 10, 12),
          deletedAt: DateTime.utc(2026, 7, 10, 12),
        ),
      ]);

      final pulled = await client.pull();
      expect(pulled.appointments.single.isTombstone, isTrue);
    });
  });

  group('wire records', () {
    test('round-trip through JSON preserves fields and tombstones', () {
      final record = _appointment(
        deletedAt: DateTime.utc(2026, 7, 10, 12),
      );
      final restored = AppointmentSyncRecord.fromJson(record.toJson());
      expect(restored.localId, record.localId);
      expect(restored.appointmentTotalCents, record.appointmentTotalCents);
      expect(restored.isTombstone, isTrue);
      expect(restored.appointmentDate.toUtc().year, 2026);

      final customer = _customer(deletedAt: DateTime.utc(2026, 7, 10, 12));
      final restoredCustomer = CustomerSyncRecord.fromJson(customer.toJson());
      expect(restoredCustomer.email, customer.email);
      expect(restoredCustomer.isTombstone, isTrue);
    });
  });
}
