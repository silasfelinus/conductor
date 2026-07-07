/// In-memory implementation of [PersistenceService].
///
/// This is the local-first source of truth for the domain layer today. It is
/// deliberately dependency-free so it can back the UI and be exercised in unit
/// tests without a device or database. A durable SQLite adapter is the next
/// task (see roadmap t-004+ / the customer-sync architecture note); it will
/// implement the same interface and can reuse the validation + total-calc
/// helpers unchanged.
library;

import '../domain/ids.dart';
import '../domain/money.dart';
import '../domain/validation.dart';
import '../models/appointment.dart';
import '../models/customer.dart';
import 'persistence_service.dart';

class InMemoryPersistenceService implements PersistenceService {
  InMemoryPersistenceService({DateTime Function()? clock})
      : _now = clock ?? DateTime.now;

  final DateTime Function() _now;
  final Map<String, Customer> _customers = {};
  final Map<String, Appointment> _appointments = {};

  @override
  Future<List<Customer>> listCustomers() async {
    final all = _customers.values.toList()
      ..sort((a, b) =>
          a.name.toLowerCase().compareTo(b.name.toLowerCase()));
    return all;
  }

  @override
  Future<Customer?> getCustomer(String customerId) async =>
      _customers[customerId];

  @override
  Future<Customer> upsertCustomer(UpsertCustomerInput input) async {
    final name = validateClientName(input.name);
    final email = validateOptionalEmail(input.email);
    final now = _now();

    if (input.id != null) {
      final existing = _customers[input.id];
      if (existing == null) {
        throw const ValidationException('That customer no longer exists.');
      }
      final updated = existing.copyWith(
        name: name,
        email: email,
        clearEmail: email == null,
        updatedAt: now,
      );
      _customers[updated.id] = updated;
      return updated;
    }

    final created = Customer(
      id: newLocalId('cust'),
      name: name,
      email: email,
      createdAt: now,
      updatedAt: now,
    );
    _customers[created.id] = created;
    return created;
  }

  @override
  Future<void> deleteCustomer(String customerId) async {
    _customers.remove(customerId);
    // Detach appointments rather than deleting them: historic receipts remain
    // readable via clientNameSnapshot (SPEC.md).
    for (final entry in _appointments.entries.toList()) {
      if (entry.value.customerId == customerId) {
        _appointments[entry.key] =
            entry.value.copyWith(clearCustomerId: true, updatedAt: _now());
      }
    }
  }

  @override
  Future<List<Appointment>> listAppointments([
    AppointmentFilter? filter,
  ]) async {
    Iterable<Appointment> results = _appointments.values;

    if (filter != null) {
      if (filter.customerId != null) {
        results = results.where((a) => a.customerId == filter.customerId);
      }
      final query = filter.clientNameQuery?.trim().toLowerCase();
      if (query != null && query.isNotEmpty) {
        results = results.where(
            (a) => a.clientNameSnapshot.toLowerCase().contains(query));
      }
      if (filter.appointmentDateFrom != null) {
        final from = _dateOnly(filter.appointmentDateFrom!);
        results = results.where(
            (a) => !_dateOnly(a.appointmentDate).isBefore(from));
      }
      if (filter.appointmentDateTo != null) {
        final to = _dateOnly(filter.appointmentDateTo!);
        results = results
            .where((a) => !_dateOnly(a.appointmentDate).isAfter(to));
      }
    }

    final list = results.toList()
      // Newest appointment first.
      ..sort((a, b) => b.appointmentDate.compareTo(a.appointmentDate));
    return list;
  }

  @override
  Future<Appointment> createAppointment(CreateAppointmentInput input) async {
    final clientName = validateClientName(input.clientName);
    final hourlyRateCents = validateHourlyRateCents(input.hourlyRateCents);
    final timeSpentMinutes = validateTimeSpentMinutes(input.timeSpentMinutes);
    final productCostCents = validateProductCostCents(input.productCostCents);

    if (input.customerId != null && !_customers.containsKey(input.customerId)) {
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
    _appointments[appointment.id] = appointment;
    return appointment;
  }

  @override
  Future<void> deleteAppointment(String appointmentId) async {
    _appointments.remove(appointmentId);
  }

  static DateTime _dateOnly(DateTime d) => DateTime(d.year, d.month, d.day);
}
