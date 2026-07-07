/// Persistence service contract for customers and appointments.
///
/// UI (Flutter widgets / future store) talks to this interface, never to a
/// database or API directly (SPEC.md "Storage and access"). The in-memory
/// implementation is the local-first source of truth today; a SQLite adapter
/// (and later authenticated cloud sync) slots in behind the same interface
/// without touching the UI.
library;

import '../models/appointment.dart';
import '../models/customer.dart';

class UpsertCustomerInput {
  const UpsertCustomerInput({
    this.id,
    required this.name,
    this.email,
  });

  /// When set, updates the existing customer; otherwise a new one is created.
  final String? id;
  final String name;
  final String? email;
}

class CreateAppointmentInput {
  const CreateAppointmentInput({
    this.customerId,
    required this.clientName,
    required this.appointmentDate,
    required this.hourlyRateCents,
    required this.timeSpentMinutes,
    this.productCostCents,
  });

  final String? customerId;
  final String clientName;
  final DateTime appointmentDate;
  final int hourlyRateCents;
  final int timeSpentMinutes;

  /// Optional; defaults to `0` (SPEC.md decided product choice).
  final int? productCostCents;
}

class AppointmentFilter {
  const AppointmentFilter({
    this.customerId,
    this.clientNameQuery,
    this.appointmentDateFrom,
    this.appointmentDateTo,
  });

  final String? customerId;

  /// Case-insensitive substring match against `clientNameSnapshot`.
  final String? clientNameQuery;

  /// Inclusive lower bound on `appointmentDate` (date-only comparison).
  final DateTime? appointmentDateFrom;

  /// Inclusive upper bound on `appointmentDate` (date-only comparison).
  final DateTime? appointmentDateTo;
}

abstract class PersistenceService {
  Future<List<Customer>> listCustomers();
  Future<Customer?> getCustomer(String customerId);
  Future<Customer> upsertCustomer(UpsertCustomerInput input);

  /// Deletes a customer. Existing appointments keep their `clientNameSnapshot`
  /// and have `customerId` detached to `null` (SPEC.md: no destructive cascade;
  /// historic receipts stay readable).
  Future<void> deleteCustomer(String customerId);

  Future<List<Appointment>> listAppointments([AppointmentFilter? filter]);
  Future<Appointment> createAppointment(CreateAppointmentInput input);
  Future<void> deleteAppointment(String appointmentId);
}
