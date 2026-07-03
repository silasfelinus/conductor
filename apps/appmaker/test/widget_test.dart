import 'package:flutter_test/flutter_test.dart';
import 'package:appmaker/main.dart';

void main() {
  testWidgets('app boots', (tester) async {
    await tester.pumpWidget(const AppmakerApp());
    expect(find.text('AppMaker'), findsWidgets);
  });
}
