import 'package:flutter_test/flutter_test.dart';
import 'package:storybook/main.dart';

void main() {
  testWidgets('app boots', (tester) async {
    await tester.pumpWidget(const StorybookApp());
    expect(find.text('Storybook'), findsWidgets);
  });
}
