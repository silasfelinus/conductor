import 'package:flutter_test/flutter_test.dart';
import 'package:sketchy/main.dart';

void main() {
  testWidgets('app boots', (tester) async {
    await tester.pumpWidget(const SketchyApp());
    expect(find.text('Sketchy'), findsWidgets);
  });
}
