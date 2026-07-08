import 'package:flutter_test/flutter_test.dart';
import 'package:superkate_services_calculator/domain/receipt_email.dart';
import 'package:superkate_services_calculator/models/appointment.dart';
import 'package:superkate_services_calculator/models/customer.dart';

void main() {
  test('buildReceiptEmail includes customer email, appointment math, and warm copy', () {
    final appointment = Appointment(
      id: 'appt-1',
      customerId: 'cust-1',
      clientNameSnapshot: 'Kate',
      appointmentDate: DateTime(2026, 7, 8),
      hourlyRateCents: 10000,
      timeSpentMinutes: 90,
      productCostCents: 2500,
      appointmentTotalCents: 17500,
      createdAt: DateTime(2026, 7, 8, 12),
      updatedAt: DateTime(2026, 7, 8, 12),
      syncedAt: null,
    );
    final customer = Customer(
      id: 'cust-1',
      name: 'Kate',
      email: 'kate@example.com',
      createdAt: DateTime(2026, 7, 1),
      updatedAt: DateTime(2026, 7, 1),
    );

    final draft = buildReceiptEmail(
      appointment: appointment,
      customer: customer,
    );

    expect(draft.toEmail, 'kate@example.com');
    expect(draft.subject, 'Hair by Superkate receipt for Kate');
    expect(draft.body, contains('Client: Kate'));
    expect(draft.body, contains('Appointment date: 2026-07-08'));
    expect(draft.body, contains('Hourly rate: \$100.00/hour'));
    expect(draft.body, contains('Time spent: 1h 30m'));
    expect(draft.body, contains('Product cost: \$25.00'));
    expect(draft.body, contains('Total price: \$175.00'));
    expect(draft.body, contains('\$100.00 × 1h 30m + \$25.00 = \$175.00'));
    expect(draft.body, contains('Superkate loves you!'));
    expect(draft.mailtoUri.scheme, 'mailto');
    expect(draft.mailtoUri.path, 'kate@example.com');
    expect(draft.mailtoUri.queryParameters['body'], draft.body);
  });

  test('buildReceiptEmail leaves recipient blank when no email is known', () {
    final appointment = Appointment(
      id: 'appt-1',
      customerId: null,
      clientNameSnapshot: 'Walk-in',
      appointmentDate: DateTime(2026, 7, 8),
      hourlyRateCents: 8000,
      timeSpentMinutes: 45,
      productCostCents: 0,
      appointmentTotalCents: 6000,
      createdAt: DateTime(2026, 7, 8, 12),
      updatedAt: DateTime(2026, 7, 8, 12),
      syncedAt: null,
    );

    final draft = buildReceiptEmail(appointment: appointment);

    expect(draft.toEmail, isNull);
    expect(draft.mailtoUri.path, isEmpty);
    expect(draft.body, contains('Product cost: \$0.00'));
    expect(draft.body, contains('\$80.00 × 45m + \$0.00 = \$60.00'));
  });
}
