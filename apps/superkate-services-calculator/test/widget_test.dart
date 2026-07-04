import 'package:flutter_test/flutter_test.dart';
import 'package:superkate_services_calculator/main.dart';

void main() {
  testWidgets('app boots', (tester) async {
    await tester.pumpWidget(const SuperkateServicesCalculatorApp());

    expect(find.text('Superkate Services Calculator'), findsWidgets);
    expect(find.text('Appointment calculator'), findsOneWidget);
  });
}
