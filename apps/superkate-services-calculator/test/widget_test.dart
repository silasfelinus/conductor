import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:superkate_services_calculator/data/in_memory_persistence_service.dart';
import 'package:superkate_services_calculator/main.dart';

void main() {
  testWidgets('app boots into the new-appointment form', (tester) async {
    await tester.pumpWidget(const SuperkateServicesCalculatorApp());

    expect(find.text('Superkate Services Calculator'), findsWidgets);
    expect(find.text('New appointment'), findsOneWidget);
    expect(find.text('Client name'), findsOneWidget);
    expect(find.text('Appointment total'), findsOneWidget);
  });

  testWidgets('live total updates from hourly rate and a preset chip',
      (tester) async {
    await tester.pumpWidget(const MaterialApp(home: SuperkateHomePage()));

    // Default time is 1h (60m); enter $80/hr -> $80.00 total, product $0.
    await tester.enterText(
        find.widgetWithText(TextField, 'Hourly rate'), '80');
    await tester.pump();
    expect(find.text(r'$80.00'), findsOneWidget);

    // Switch to the 45m preset -> 8000 * 45 / 60 = 6000c = $60.00.
    await tester.tap(find.text('45m'));
    await tester.pump();
    expect(find.text(r'$60.00'), findsOneWidget);

    // Add $25 product cost -> $85.00.
    await tester.enterText(
        find.widgetWithText(TextField, 'Product cost (optional)'), '25');
    await tester.pump();
    expect(find.text(r'$85.00'), findsOneWidget);
  });

  testWidgets('saving persists an appointment with the calculated total',
      (tester) async {
    final service = InMemoryPersistenceService();
    await tester.pumpWidget(MaterialApp(home: SuperkateHomePage(service: service)));

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
    // $100/hr * 90m = $150.00.
    expect(appointments.single.appointmentTotalCents, 15000);
  });
}
