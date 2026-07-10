import 'dart:io';

import 'package:flutter_test/flutter_test.dart';
import 'package:superkate_services_calculator/data/csv_export_service.dart';
import 'package:superkate_services_calculator/domain/csv_export.dart';
import 'package:superkate_services_calculator/models/appointment.dart';
import 'package:superkate_services_calculator/models/customer.dart';

Customer _customer({
  String id = 'cust-1',
  String name = 'Hannah',
  String? email = 'hannah@example.com',
}) =>
    Customer(
      id: id,
      name: name,
      email: email,
      createdAt: DateTime.utc(2026, 7, 1, 10),
      updatedAt: DateTime.utc(2026, 7, 2, 11),
    );

Appointment _appointment({
  String id = 'appt-1',
  String clientName = 'Hannah',
  String? customerId = 'cust-1',
}) =>
    Appointment(
      id: id,
      customerId: customerId,
      clientNameSnapshot: clientName,
      appointmentDate: DateTime.utc(2026, 7, 9),
      hourlyRateCents: 12000,
      timeSpentMinutes: 90,
      productCostCents: 3050,
      appointmentTotalCents: 21050,
      createdAt: DateTime.utc(2026, 7, 9, 12),
      updatedAt: DateTime.utc(2026, 7, 9, 12),
      syncedAt: null,
    );

void main() {
  group('csvField escaping', () {
    test('passes plain values through untouched', () {
      expect(csvField('Hannah'), 'Hannah');
    });

    test('quotes commas, quotes, and newlines per RFC 4180', () {
      expect(csvField('Knight, Hannah'), '"Knight, Hannah"');
      expect(csvField('the "best" client'), '"the ""best"" client"');
      expect(csvField('line\nbreak'), '"line\nbreak"');
    });
  });

  group('centsToDecimal', () {
    test('formats cents as plain decimal dollars', () {
      expect(centsToDecimal(12000), '120.00');
      expect(centsToDecimal(5), '0.05');
      expect(centsToDecimal(0), '0.00');
      expect(centsToDecimal(-1250), '-12.50');
    });
  });

  group('customersToCsv', () {
    test('emits a header and one row per customer with CRLF endings', () {
      final csv = customersToCsv([_customer()]);
      final lines = csv.split('\r\n');
      expect(lines[0], 'name,email,created,updated,id');
      expect(lines[1], 'Hannah,hannah@example.com,2026-07-01,2026-07-02,cust-1');
      expect(csv.endsWith('\r\n'), isTrue);
    });

    test('blank email stays an empty field and tricky names are quoted', () {
      final csv = customersToCsv([
        _customer(name: 'Knight, Hannah', email: null),
      ]);
      expect(csv.split('\r\n')[1],
          '"Knight, Hannah",,2026-07-01,2026-07-02,cust-1');
    });
  });

  group('appointmentsToCsv', () {
    test('emits money as decimal dollars and the detached customer as blank',
        () {
      final csv = appointmentsToCsv([
        _appointment(),
        _appointment(id: 'appt-2', customerId: null),
      ]);
      final lines = csv.split('\r\n');
      expect(lines[0],
          'client,date,hourly_rate,time_minutes,product_cost,total,customer_id,id');
      expect(lines[1],
          'Hannah,2026-07-09,120.00,90,30.50,210.50,cust-1,appt-1');
      expect(lines[2], 'Hannah,2026-07-09,120.00,90,30.50,210.50,,appt-2');
    });
  });

  group('FileCsvExportService', () {
    test('writes both files into the export directory and returns paths',
        () async {
      final tempDir =
          await Directory.systemTemp.createTemp('superkate_export_test');
      addTearDown(() => tempDir.delete(recursive: true));

      final service = FileCsvExportService(
        directory: tempDir,
        clock: () => DateTime.utc(2026, 7, 10),
      );
      final result = await service.exportAll(
        customers: [_customer()],
        appointments: [_appointment()],
      );

      expect(result.customersPath, endsWith('superkate-customers-2026-07-10.csv'));
      expect(result.appointmentsPath,
          endsWith('superkate-appointments-2026-07-10.csv'));
      expect(await File(result.customersPath).readAsString(),
          customersToCsv([_customer()]));
      expect(await File(result.appointmentsPath).readAsString(),
          appointmentsToCsv([_appointment()]));
    });
  });
}
