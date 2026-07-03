import 'package:flutter_test/flutter_test.dart';
import 'package:wishmaster/main.dart';

void main() {
  testWidgets('app boots', (tester) async {
    await tester.pumpWidget(const WishmasterApp());
    expect(find.text('Wishmaster'), findsWidgets);
  });
}
