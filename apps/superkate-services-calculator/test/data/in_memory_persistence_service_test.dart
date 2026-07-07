import 'package:flutter_test/flutter_test.dart';
import 'package:superkate_services_calculator/data/in_memory_persistence_service.dart';
import 'package:superkate_services_calculator/data/persistence_service.dart';
import 'package:superkate_services_calculator/domain/validation.dart';

void main() {
  late InMemoryPersistenceService service;

  setUp(() {
    service = InMemoryPersistenceService();
  });

  group('customers', () {
    test('creates, lists, and updates', () async {
      final kate = await service.upsertCustomer(
          const UpsertCustomerInput(name: 'Kate', email: 'kate@example.com'));
      expect(kate.id, isNotEmpty);
      expect(kate.email, 'kate@example.com');

      final again = await service.upsertCustomer(
          UpsertCustomerInput(id: kate.id, name: 'Kate B.'));
      expect(again.id, kate.id);
      expect(again.name, 'Kate B.');
      // Email cleared when omitted on update.
      expect(again.email, isNull);

      final all = await service.listCustomers();
      expect(all.length, 1);
    });

    test('rejects a blank name', () async {
      expect(
        () => service.upsertCustomer(const UpsertCustomerInput(name: '  ')),
        throwsA(isA<ValidationException>()),
      );
    });

    test('deleting a customer detaches, not deletes, their appointments',
        () async {
      final kate = await service
          .upsertCustomer(const UpsertCustomerInput(name: 'Kate'));
      final appt = await service.createAppointment(CreateAppointmentInput(
        customerId: kate.id,
        clientName: 'Kate',
        appointmentDate: DateTime(2026, 7, 7),
        hourlyRateCents: 8000,
        timeSpentMinutes: 45,
      ));

      await service.deleteCustomer(kate.id);

      final appts = await service.listAppointments();
      expect(appts.length, 1);
      expect(appts.single.id, appt.id);
      expect(appts.single.customerId, isNull);
      // Snapshot name survives the customer deletion.
      expect(appts.single.clientNameSnapshot, 'Kate');
    });
  });

  group('appointments', () {
    test('creates with a calculated total and product defaulting to zero',
        () async {
      final appt = await service.createAppointment(CreateAppointmentInput(
        clientName: 'Walk-in',
        appointmentDate: DateTime(2026, 7, 7),
        hourlyRateCents: 8000,
        timeSpentMinutes: 45,
      ));
      expect(appt.productCostCents, 0);
      expect(appt.appointmentTotalCents, 6000);
      expect(appt.customerId, isNull);
      expect(appt.syncedAt, isNull);
    });

    test('ignores a UI-supplied total and recomputes from fields', () async {
      final appt = await service.createAppointment(CreateAppointmentInput(
        clientName: 'Kate',
        appointmentDate: DateTime(2026, 7, 7),
        hourlyRateCents: 10000,
        timeSpentMinutes: 90,
        productCostCents: 2500,
      ));
      expect(appt.appointmentTotalCents, 17500);
    });

    test('rejects zero time spent', () async {
      expect(
        () => service.createAppointment(CreateAppointmentInput(
          clientName: 'Kate',
          appointmentDate: DateTime(2026, 7, 7),
          hourlyRateCents: 8000,
          timeSpentMinutes: 0,
        )),
        throwsA(isA<ValidationException>()),
      );
    });

    test('rejects an appointment for an unknown customer', () async {
      expect(
        () => service.createAppointment(CreateAppointmentInput(
          customerId: 'cust_does_not_exist',
          clientName: 'Kate',
          appointmentDate: DateTime(2026, 7, 7),
          hourlyRateCents: 8000,
          timeSpentMinutes: 45,
        )),
        throwsA(isA<ValidationException>()),
      );
    });

    test('deletes an appointment', () async {
      final appt = await service.createAppointment(CreateAppointmentInput(
        clientName: 'Kate',
        appointmentDate: DateTime(2026, 7, 7),
        hourlyRateCents: 8000,
        timeSpentMinutes: 45,
      ));
      await service.deleteAppointment(appt.id);
      expect(await service.listAppointments(), isEmpty);
    });
  });

  group('search filters', () {
    setUp(() async {
      await service.createAppointment(CreateAppointmentInput(
        clientName: 'Alice',
        appointmentDate: DateTime(2026, 7, 1),
        hourlyRateCents: 8000,
        timeSpentMinutes: 60,
      ));
      await service.createAppointment(CreateAppointmentInput(
        clientName: 'Bob',
        appointmentDate: DateTime(2026, 7, 5),
        hourlyRateCents: 9000,
        timeSpentMinutes: 30,
      ));
      await service.createAppointment(CreateAppointmentInput(
        clientName: 'Alicia',
        appointmentDate: DateTime(2026, 7, 9),
        hourlyRateCents: 7000,
        timeSpentMinutes: 90,
      ));
    });

    test('returns newest first with no filter', () async {
      final all = await service.listAppointments();
      expect(all.map((a) => a.clientNameSnapshot).toList(),
          ['Alicia', 'Bob', 'Alice']);
    });

    test('client-name query is a case-insensitive substring match', () async {
      final results = await service.listAppointments(
          const AppointmentFilter(clientNameQuery: 'ali'));
      expect(results.map((a) => a.clientNameSnapshot).toSet(),
          {'Alice', 'Alicia'});
    });

    test('date range filter is inclusive', () async {
      final results = await service.listAppointments(AppointmentFilter(
        appointmentDateFrom: DateTime(2026, 7, 5),
        appointmentDateTo: DateTime(2026, 7, 9),
      ));
      expect(results.map((a) => a.clientNameSnapshot).toSet(),
          {'Bob', 'Alicia'});
    });
  });
}
