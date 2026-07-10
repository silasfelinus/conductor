/// CSV serialization for the local export feature (SPEC.md: "CSV export for
/// customers and appointments"). Pure functions — no file I/O here, so the
/// exact bytes are unit-testable.
///
/// Money columns are decimal dollars (e.g. `80.00`, no `$`) so spreadsheets
/// parse them as numbers; raw cents stay out of the export to keep it
/// salon-readable. Dates are ISO so sorting works everywhere.
library;

import '../models/appointment.dart';
import '../models/customer.dart';

/// Escapes one CSV field per RFC 4180: quote when the value contains a comma,
/// quote, or newline; double any embedded quotes.
String csvField(String value) {
  if (value.contains(',') ||
      value.contains('"') ||
      value.contains('\n') ||
      value.contains('\r')) {
    return '"${value.replaceAll('"', '""')}"';
  }
  return value;
}

String _row(List<String> fields) => fields.map(csvField).join(',');

/// `12345 -> "123.45"` — plain decimal dollars for spreadsheet math.
String centsToDecimal(int cents) {
  final negative = cents < 0;
  final abs = cents.abs();
  return '${negative ? '-' : ''}${abs ~/ 100}.${(abs % 100).toString().padLeft(2, '0')}';
}

String _isoDate(DateTime value) =>
    value.toUtc().toIso8601String().substring(0, 10);

String customersToCsv(List<Customer> customers) {
  final lines = <String>[
    _row(['name', 'email', 'created', 'updated', 'id']),
    for (final c in customers)
      _row([
        c.name,
        c.email ?? '',
        _isoDate(c.createdAt),
        _isoDate(c.updatedAt),
        c.id,
      ]),
  ];
  return '${lines.join('\r\n')}\r\n';
}

String appointmentsToCsv(List<Appointment> appointments) {
  final lines = <String>[
    _row([
      'client',
      'date',
      'hourly_rate',
      'time_minutes',
      'product_cost',
      'total',
      'customer_id',
      'id',
    ]),
    for (final a in appointments)
      _row([
        a.clientNameSnapshot,
        _isoDate(a.appointmentDate),
        centsToDecimal(a.hourlyRateCents),
        a.timeSpentMinutes.toString(),
        centsToDecimal(a.productCostCents),
        centsToDecimal(a.appointmentTotalCents),
        a.customerId ?? '',
        a.id,
      ]),
  ];
  return '${lines.join('\r\n')}\r\n';
}
