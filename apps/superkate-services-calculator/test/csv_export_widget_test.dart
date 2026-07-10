import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:superkate_services_calculator/data/csv_export_service.dart';
import 'package:superkate_services_calculator/data/in_memory_persistence_service.dart';
import 'package:superkate_services_calculator/data/persistence_service.dart';
import 'package:superkate_services_calculator/main.dart';

void _useTallSurface(WidgetTester tester) {
  tester.view.physicalSize = const Size(1200, 2400);
  tester.view.devicePixelRatio = 1.0;
  addTearDown(tester.view.resetPhysicalSize);
  addTearDown(tester.view.resetDevicePixelRatio);
}

void main() {
  testWidgets('export flow confirms, writes CSVs, and reports the save',
      (tester) async {
    _useTallSurface(tester);
    final service = InMemoryPersistenceService();
    final customer = await service.upsertCustomer(
      const UpsertCustomerInput(name: 'Hannah', email: 'hannah@example.com'),
    );
    await service.createAppointment(
      CreateAppointmentInput(
        customerId: customer.id,
        clientName: customer.name,
        appointmentDate: DateTime(2026, 7, 9),
        hourlyRateCents: 12000,
        timeSpentMinutes: 60,
        productCostCents: 0,
      ),
    );
    final exporter = InMemoryCsvExportService();

    await tester.pumpWidget(MaterialApp(
      home: SuperkateHomePage(service: service, exportService: exporter),
    ));
    await tester.pumpAndSettle();

    await tester.tap(find.byKey(const ValueKey('export-csv-button')));
    await tester.pumpAndSettle();
    await tester.tap(find.byKey(const ValueKey('confirm-export-button')));
    await tester.pumpAndSettle();

    expect(exporter.exportCount, 1);
    expect(exporter.lastCustomersCsv, contains('Hannah'));
    expect(exporter.lastAppointmentsCsv, contains('120.00'));
    expect(find.textContaining('Exported 1 customers'), findsOneWidget);
  });

  testWidgets('cancelling the export dialog writes nothing', (tester) async {
    _useTallSurface(tester);
    final exporter = InMemoryCsvExportService();

    await tester.pumpWidget(MaterialApp(
      home: SuperkateHomePage(
        service: InMemoryPersistenceService(),
        exportService: exporter,
      ),
    ));
    await tester.pumpAndSettle();

    await tester.tap(find.byKey(const ValueKey('export-csv-button')));
    await tester.pumpAndSettle();
    await tester.tap(find.byKey(const ValueKey('cancel-export-button')));
    await tester.pumpAndSettle();

    expect(exporter.exportCount, 0);
  });
}
