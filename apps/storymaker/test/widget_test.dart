import 'package:flutter_test/flutter_test.dart';
import 'package:storymaker/main.dart';

void main() {
  testWidgets('app boots', (tester) async {
    await tester.pumpWidget(const StorymakerApp());
    expect(find.text('Storymaker'), findsWidgets);
  });
}
