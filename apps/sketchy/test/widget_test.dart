import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:sketchy/app.dart';

void main() {
  testWidgets('app boots on the calibration screen', (tester) async {
    await tester.pumpWidget(const ProviderScope(child: SketchyApp()));
    expect(find.text('Let\'s find your starting point'), findsOneWidget);
  });

  testWidgets('completing calibration advances to an assignment',
      (tester) async {
    await tester.pumpWidget(const ProviderScope(child: SketchyApp()));

    await tester.tap(find.text('Start drawing'));
    await tester.pumpAndSettle();

    expect(find.text('Today\'s assignment'), findsOneWidget);
    // A success-criteria section should render for whatever assignment landed.
    expect(find.text('We\'ll check for:'), findsOneWidget);
  });

  testWidgets('full core loop reaches a critique and loads a next assignment',
      (tester) async {
    await tester.pumpWidget(const ProviderScope(child: SketchyApp()));

    await tester.tap(find.text('Start drawing'));
    await tester.pumpAndSettle();

    await tester.tap(find.text('I\'m done -- submit for critique'));
    await tester.pumpAndSettle();
    expect(find.text('Submit your drawing'), findsOneWidget);

    await tester.tap(find.text('Attach drawing'));
    await tester.pumpAndSettle();

    await tester.tap(find.text('Get critique'));
    await tester.pumpAndSettle();
    expect(find.text('Your critique'), findsOneWidget);
    expect(find.text('Scores'), findsOneWidget);

    await tester.tap(find.text('Next assignment'));
    await tester.pumpAndSettle();
    expect(find.text('Today\'s assignment'), findsOneWidget);
  });
}
