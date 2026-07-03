import 'package:flutter_test/flutter_test.dart';
import 'package:recipe_box/main.dart';

void main() {
  testWidgets('app boots', (tester) async {
    await tester.pumpWidget(const RecipeBoxApp());
    expect(find.text('Recipe Box'), findsWidgets);
  });
}
