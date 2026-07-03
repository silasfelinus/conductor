import 'package:flutter_test/flutter_test.dart';
import 'package:humboldt_scoop_cms/main.dart';

void main() {
  testWidgets('app boots', (tester) async {
    await tester.pumpWidget(const HumboldtScoopCmsApp());
    expect(find.text('Humboldt Scoop Solutions'), findsWidgets);
  });
}
