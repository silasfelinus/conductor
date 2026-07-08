import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:superkate_services_calculator/data/in_memory_persistence_service.dart';
import 'package:superkate_services_calculator/data/persistence_service.dart';
import 'package:superkate_services_calculator/main.dart';

/// Give tests a tall surface so the whole scrolling form (including the total
/// card and save button) is laid out and hit-testable, not pushed offstage.
void _useTallSurface(WidgetTester tester) {
  tester.view.physicalSize = const Size(1200, 2400);
  tester.view.devicePixelRatio = 1.0;
  addTearDown(tester.view.resetPhysicalSize);
  addTearDown(tester.view.resetDevicePixelRatio);
}

void main() {
  testWidgets('app boots into the new-appointment form', (tester) async {
    _useTallSurface(tester);
    await tester.pumpWidget(const SuperkateServicesCalculatorApp());

    expect(find.text('Superkate Services Calculator'), findsWidgets);
    expect(find.text('New appointment'), findsOneWidget);
    expect(find.text('Client name'), findsOneWidget);
    expect(find.text('Appointment total'), findsOneWidget);
  });

  testWidgets('live total updates from hourly rate and a preset chip',
      (tester) async {
    _useTallSurface(tester);
    await tester.pumpWidget(const MaterialApp(home: SuperkateHomePage()));

    await tester.enterText(
        find.widgetWithText(TextField, 'Hourly rate'), '80');
    await tester.pump();
    expect(find.text(r'$80.00'), findsOneWidget);

    await tester.tap(find.text('45m'));
    await tester.pump();
    expect(find.text(r'$60.00'), findsOneWidget);

    await tester.enterText(
        find.widgetWithText(TextField, 'Product cost (optional)'), '25');
    await tester.pump();
    expect(find.text(r'$85.00'), findsOneWidget);
  });

  testWidgets('saving persists an appointment with the calculated total',
      (tester) async {
    _useTallSurface(tester);
    final service = InMemoryPersistenceService();
    await tester
        .pumpWidget(MaterialApp(home: SuperkateHomePage(service: service)));

    await tester.enterText(
        find.widgetWithText(TextField, 'Client name'), 'Kate');
    await tester.enterText(
        find.widgetWithText(TextField, 'Hourly rate'), '100');
    await tester.tap(find.text('1h 30m'));
    await tester.pump();

    await tester.tap(find.text('Save appointment'));
    await tester.pumpAndSettle();

    final appointments = await service.listAppointments();
    expect(appointments.length, 1);
    expect(appointments.single.clientNameSnapshot, 'Kate');
    expect(appointments.single.appointmentTotalCents, 15000);
  });

  testWidgets('saved appointments appear in history after save', (tester) async {
    _useTallSurface(tester);
    final service = InMemoryPersistenceService();
    await tester
        .pumpWidget(MaterialApp(home: SuperkateHomePage(service: service)));

    await tester.enterText(
        find.widgetWithText(TextField, 'Client name'), 'Kate');
    await tester.enterText(
        find.widgetWithText(TextField, 'Hourly rate'), '100');
    await tester.tap(find.text('1h 30m'));
    await tester.pump();
    await tester.tap(find.text('Save appointment'));
    await tester.pumpAndSettle();

    await tester.tap(find.text('History'));
    await tester.pumpAndSettle();

    expect(find.text('Appointment history'), findsOneWidget);
    expect(find.text('Kate'), findsOneWidget);
    expect(find.text(r'$150.00'), findsWidgets);
  });

  testWidgets('history filters by client name', (tester) async {
    _useTallSurface(tester);
    final service = InMemoryPersistenceService();
    await service.createAppointment(
      CreateAppointmentInput(
        clientName: 'Kate',
        appointmentDate: DateTime(2026, 7, 8),
        hourlyRateCents: 10000,
        timeSpentMinutes: 90,
        productCostCents: 0,
      ),
    );
    await service.createAppointment(
      CreateAppointmentInput(
        clientName: 'Ronin',
        appointmentDate: DateTime(2026, 7, 9),
        hourlyRateCents: 8000,
        timeSpentMinutes: 60,
        productCostCents: 2500,
      ),
    );

    await tester
        .pumpWidget(MaterialApp(home: SuperkateHomePage(service: service)));
    await tester.tap(find.text('History'));
    await tester.pumpAndSettle();

    expect(find.text('Kate'), findsOneWidget);
    expect(find.text('Ronin'), findsOneWidget);

    await tester.enterText(
        find.widgetWithText(TextField, 'Search by client name'), 'kat');
    await tester.pumpAndSettle();

    expect(find.text('Kate'), findsOneWidget);
    expect(find.text('Ronin'), findsNothing);
  });
}
