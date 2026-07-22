import 'dart:io';

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

  testWidgets('export flow shares exactly the two written CSV paths',
      (tester) async {
    _useTallSurface(tester);

    // FileCsvExportService performs real dart:io work (temp-directory
    // creation and file writes). testWidgets bodies run inside a FakeAsync
    // zone for animation/timer control, and that zone never resolves
    // genuine OS-level async I/O -- it just hangs until the suite's 10-minute
    // timeout. tester.runAsync() steps outside the fake zone so real async
    // calls actually complete; every real dart:io call in this test must be
    // made from inside one.
    late final Directory directory;
    await tester.runAsync(() async {
      directory = await Directory.systemTemp.createTemp('superkate-share-');
    });
    addTearDown(() async {
      await tester.runAsync(() => directory.delete(recursive: true));
    });
    final shareGateway = InMemoryCsvShareGateway();
    final exporter = FileCsvExportService(
      directory: directory,
      clock: () => DateTime(2026, 7, 10),
      shareGateway: shareGateway,
    );

    await tester.pumpWidget(MaterialApp(
      home: SuperkateHomePage(
        service: InMemoryPersistenceService(),
        exportService: exporter,
      ),
    ));
    await tester.pumpAndSettle();

    await tester.tap(find.byKey(const ValueKey('export-csv-button')));
    await tester.pumpAndSettle();
    // The confirm tap's onPressed chain runs FileCsvExportService's real
    // file writes. Driving the tap and its follow-up pumps from inside
    // runAsync keeps that real I/O's completion on the real event loop
    // instead of the fake-async zone pump() alone can never drain here.
    await tester.runAsync(() async {
      await tester.tap(find.byKey(const ValueKey('confirm-export-button')));
      var attempts = 0;
      while (shareGateway.shareCount == 0 && attempts < 500) {
        await tester.pump(const Duration(milliseconds: 10));
        await Future<void>.delayed(const Duration(milliseconds: 10));
        attempts++;
      }
    });
    await tester.pumpAndSettle();

    final customersPath =
        '${directory.path}${Platform.pathSeparator}superkate-customers-2026-07-10.csv';
    final appointmentsPath =
        '${directory.path}${Platform.pathSeparator}superkate-appointments-2026-07-10.csv';

    expect(shareGateway.shareCount, 1);
    expect(shareGateway.lastCustomersPath, customersPath);
    expect(shareGateway.lastAppointmentsPath, appointmentsPath);
    expect(File(customersPath).existsSync(), isTrue);
    expect(File(appointmentsPath).existsSync(), isTrue);
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
