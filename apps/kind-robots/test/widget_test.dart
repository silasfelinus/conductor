import 'package:flutter_test/flutter_test.dart';
import 'package:kind_robots/main.dart';

void main() {
  testWidgets('app boots', (tester) async {
    await tester.pumpWidget(const KindRobotsApp());
    expect(find.text('Kind Robots'), findsWidgets);
  });
}
