import 'package:flutter_test/flutter_test.dart';
import 'package:superkate_services_calculator/data/persistence_service.dart';
import 'package:superkate_services_calculator/data/sqlite_persistence_service.dart';

void main() {
  late SqlitePersistenceService service;
  var clockTick = 0;

  DateTime clock() => DateTime.utc(2026, 7, 8, 12, clockTick++);

  setUp(() {
    clockTick = 0;
    service = SqlitePersistenceService.inMemory(clock: clock);
  });

  tearDown(() {
    service.close();
  });

  test('creates and updates customers with normalized optional email', () async {
    final customer = await service.upsertCustomer(
      const UpsertCustomerInput(
        name: '  Kate  ',
        email: ' kate@example.com ',
      ),
    );

    expect(customer.name, 'Kate');
    expect(customer.email, 'kate@example.com');

    final updated = await service.upsertCustomer(
      UpsertCustomerInput(
        id: customer.id,
        name: 'Superkate',
        email: '',
      ),
    );

    expect(updated.id, customer.id);
    expect(updated.name, 'Superkate');
    expect(updated.email, isNull);
    expect((await service.listCustomers()).single, updated);
  });

  test('persists appointments and recalculates totals from source fields', () async {
    final customer = await service.upsertCustomer(
      const UpsertCustomerInput(
        name: 'Kate',
        email: 'kate@example.com',
      ),
    );

    final appointment = await service.createAppointment(
      CreateAppointmentInput(
        customerId: customer.id,
        clientName: customer.name,
        appointmentDate: DateTime(2026, 7, 8),
        hourlyRateCents: 10000,
        timeSpentMinutes: 90,
        productCostCents: 2500,
      ),
    );

    final saved = await service.listAppointments();
    expect(saved.single.id, appointment.id);
    expect(saved.single.customerId, customer.id);
    expect(saved.single.clientNameSnapshot, 'Kate');
    expect(saved.single.hourlyRateCents, 10000);
    expect(saved.single.timeSpentMinutes, 90);
    expect(saved.single.productCostCents, 2500);
    expect(saved.single.appointmentTotalCents, 17500);
  });

  test('defaults product cost to zero', () async {
    final appointment = await service.createAppointment(
      CreateAppointmentInput(
        clientName: 'Kate',
        appointmentDate: DateTime(2026, 7, 8),
        hourlyRateCents: 8000,
        timeSpentMinutes: 45,
      ),
    );

    expect(appointment.productCostCents, 0);
    expect(appointment.appointmentTotalCents, 6000);
  });

  test('search filters by customer, client name, and date range', () async {
    final kate = await service.upsertCustomer(
      const UpsertCustomerInput(name: 'Kate'),
    );
    await service.createAppointment(
      CreateAppointmentInput(
        customerId: kate.id,
        clientName: 'Kate',
        appointmentDate: DateTime(2026, 7, 8),
        hourlyRateCents: 10000,
        timeSpentMinutes: 60,
      ),
    );
    await service.createAppointment(
      CreateAppointmentInput(
        clientName: 'Ronin',
        appointmentDate: DateTime(2026, 7, 9),
        hourlyRateCents: 8000,
        timeSpentMinutes: 60,
      ),
    );

    final byCustomer = await service.listAppointments(
      AppointmentFilter(customerId: kate.id),
    );
    expect(byCustomer.single.clientNameSnapshot, 'Kate');

    final byName = await service.listAppointments(
      const AppointmentFilter(clientNameQuery: 'ron'),
    );
    expect(byName.single.clientNameSnapshot, 'Ronin');

    final byDate = await service.listAppointments(
      AppointmentFilter(
        appointmentDateFrom: DateTime(2026, 7, 9),
        appointmentDateTo: DateTime(2026, 7, 9),
      ),
    );
    expect(byDate.single.clientNameSnapshot, 'Ronin');
  });

  test('deleting a customer detaches appointments without deleting history', () async {
    final customer = await service.upsertCustomer(
      const UpsertCustomerInput(name: 'Kate'),
    );
    await service.createAppointment(
      CreateAppointmentInput(
        customerId: customer.id,
        clientName: customer.name,
        appointmentDate: DateTime(2026, 7, 8),
        hourlyRateCents: 10000,
        timeSpentMinutes: 60,
      ),
    );

    await service.deleteCustomer(customer.id);

    expect(await service.getCustomer(customer.id), isNull);
    final appointments = await service.listAppointments();
    expect(appointments.single.customerId, isNull);
    expect(appointments.single.clientNameSnapshot, 'Kate');
  });

  test('deleting an appointment removes only that appointment', () async {
    final first = await service.createAppointment(
      CreateAppointmentInput(
        clientName: 'Kate',
        appointmentDate: DateTime(2026, 7, 8),
        hourlyRateCents: 10000,
        timeSpentMinutes: 60,
      ),
    );
    await service.createAppointment(
      CreateAppointmentInput(
        clientName: 'Ronin',
        appointmentDate: DateTime(2026, 7, 9),
        hourlyRateCents: 8000,
        timeSpentMinutes: 60,
      ),
    );

    await service.deleteAppointment(first.id);

    final remaining = await service.listAppointments();
    expect(remaining.length, 1);
    expect(remaining.single.clientNameSnapshot, 'Ronin');
  });
}
