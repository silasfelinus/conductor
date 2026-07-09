import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:superkate_services_calculator/data/in_memory_onboarding_service.dart';
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
  testWidgets('app shows the splash onramp before first use', (tester) async {
    _useTallSurface(tester);
    final service = InMemoryPersistenceService();
    final onboarding = InMemoryOnboardingService();

    await tester.pumpWidget(
      SuperkateServicesCalculatorApp(
        service: Future.value(service),
        onboardingService: Future.value(onboarding),
      ),
    );
    await tester.pumpAndSettle();

    expect(find.text('Hair by Superkate'), findsOneWidget);
    expect(find.text('Private services calculator beta'), findsOneWidget);
    expect(find.text('Start local beta'), findsOneWidget);
    expect(find.text('Client name'), findsNothing);
  });

  testWidgets('onboarding start persists the choice and opens the calculator',
      (tester) async {
    _useTallSurface(tester);
    final service = InMemoryPersistenceService();
    final onboarding = InMemoryOnboardingService();

    await tester.pumpWidget(
      SuperkateServicesCalculatorApp(
        service: Future.value(service),
        onboardingService: Future.value(onboarding),
      ),
    );
    await tester.pumpAndSettle();

    await tester.tap(find.byKey(const ValueKey('start-local-beta-button')));
    await tester.pumpAndSettle();

    expect(await onboarding.hasCompletedOnboarding(), isTrue);
    expect(find.text('New appointment'), findsOneWidget);
    expect(find.text('Client name'), findsOneWidget);
    expect(find.text('Appointment total'), findsOneWidget);
  });

  testWidgets('app boots into the new-appointment form after onboarding',
      (tester) async {
    _useTallSurface(tester);
    final service = InMemoryPersistenceService();
    final onboarding = InMemoryOnboardingService(completed: true);

    await tester.pumpWidget(
      SuperkateServicesCalculatorApp(
        service: Future.value(service),
        onboardingService: Future.value(onboarding),
      ),
    );
    await tester.pumpAndSettle();

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

  testWidgets('prepare receipt opens a local mailto draft with customer email',
      (tester) async {
    _useTallSurface(tester);
    final service = InMemoryPersistenceService();
    final customer = await service.upsertCustomer(
      const UpsertCustomerInput(
        name: 'Kate',
        email: 'kate@example.com',
      ),
    );
    await service.createAppointment(
      CreateAppointmentInput(
        customerId: customer.id,
        clientName: customer.name,
        appointmentDate: DateTime(2026, 7, 8),
        hourlyRateCents: 10000,
        timeSpentMinutes: 90,
        productCostCents: 2500,
      ),
    );

    Uri? launchedUri;
    await tester.pumpWidget(
      MaterialApp(
        home: SuperkateHomePage(
          service: service,
          launchReceiptEmail: (uri) async {
            launchedUri = uri;
            return true;
          },
        ),
      ),
    );
    await tester.tap(find.text('History'));
    await tester.pumpAndSettle();

    await tester.tap(find.text('Prepare receipt'));
    await tester.pumpAndSettle();

    expect(launchedUri, isNotNull);
    expect(launchedUri!.scheme, 'mailto');
    expect(launchedUri!.path, 'kate@example.com');
    expect(launchedUri!.queryParameters['subject'],
        'Hair by Superkate receipt for Kate');
    expect(launchedUri!.queryParameters['body'], contains('Client: Kate'));
    expect(launchedUri!.queryParameters['body'], contains('Superkate loves you!'));
  });

  testWidgets('customer profiles can be added, edited, and deleted safely',
      (tester) async {
    _useTallSurface(tester);
    final service = InMemoryPersistenceService();
    final customer = await service.upsertCustomer(
      const UpsertCustomerInput(
        name: 'Kate',
        email: 'kate@example.com',
      ),
    );
    await service.createAppointment(
      CreateAppointmentInput(
        customerId: customer.id,
        clientName: customer.name,
        appointmentDate: DateTime(2026, 7, 8),
        hourlyRateCents: 10000,
        timeSpentMinutes: 60,
        productCostCents: 0,
      ),
    );

    await tester
        .pumpWidget(MaterialApp(home: SuperkateHomePage(service: service)));
    await tester.tap(find.text('Customers'));
    await tester.pumpAndSettle();

    expect(find.text('Customer profiles'), findsOneWidget);
    expect(find.text('Kate'), findsOneWidget);

    await tester.tap(find.byKey(ValueKey('edit-customer-${customer.id}')));
    await tester.pumpAndSettle();
    await tester.enterText(
        find.widgetWithText(TextField, 'Customer name'), 'Superkate');
    await tester.enterText(
        find.widgetWithText(TextField, 'Receipt email (optional)'),
        'superkate@example.com');
    await tester.tap(find.byKey(const ValueKey('save-customer-button')));
    await tester.pumpAndSettle();

    final updated = await service.getCustomer(customer.id);
    expect(updated!.name, 'Superkate');
    expect(updated.email, 'superkate@example.com');
    expect(find.text('Superkate'), findsOneWidget);

    await tester.tap(find.byKey(ValueKey('delete-customer-${customer.id}')));
    await tester.pumpAndSettle();
    await tester.tap(find.text('Delete profile'));
    await tester.pumpAndSettle();

    expect(await service.listCustomers(), isEmpty);
    final appointments = await service.listAppointments();
    expect(appointments.single.customerId, isNull);
    expect(appointments.single.clientNameSnapshot, 'Kate');
  });

  testWidgets('appointment delete removes only the selected history row',
      (tester) async {
    _useTallSurface(tester);
    final service = InMemoryPersistenceService();
    final kate = await service.createAppointment(
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

    await tester.tap(find.byKey(ValueKey('delete-appointment-${kate.id}')));
    await tester.pumpAndSettle();
    await tester.tap(
      find.byKey(const ValueKey('confirm-delete-appointment-button')),
    );
    await tester.pumpAndSettle();

    final remaining = await service.listAppointments();
    expect(remaining.length, 1);
    expect(remaining.single.clientNameSnapshot, 'Ronin');
    expect(find.text('Kate'), findsNothing);
    expect(find.text('Ronin'), findsOneWidget);
  });

  testWidgets('background pattern changes independently from theme',
      (tester) async {
    _useTallSurface(tester);
    final service = InMemoryPersistenceService();
    final onboarding = InMemoryOnboardingService(completed: true);

    await tester.pumpWidget(
      SuperkateServicesCalculatorApp(
        service: Future.value(service),
        onboardingService: Future.value(onboarding),
      ),
    );
    await tester.pumpAndSettle();

    expect(find.byKey(const ValueKey('background-circles')), findsOneWidget);

    await tester.tap(find.byTooltip('Choose background'));
    await tester.pumpAndSettle();
    await tester.tap(find.text('Hearts'));
    await tester.pumpAndSettle();

    expect(find.byKey(const ValueKey('background-hearts')), findsOneWidget);

    await tester.tap(find.byTooltip('Choose theme'));
    await tester.pumpAndSettle();
    await tester.tap(find.text('Classic'));
    await tester.pumpAndSettle();

    expect(find.byKey(const ValueKey('background-hearts')), findsOneWidget);

    await tester.tap(find.byTooltip('Choose background'));
    await tester.pumpAndSettle();
    await tester.tap(find.text('Grid'));
    await tester.pumpAndSettle();

    expect(find.byKey(const ValueKey('background-grid')), findsOneWidget);
    expect(find.text('Client name'), findsOneWidget);
  });
}
