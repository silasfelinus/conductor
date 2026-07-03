import 'package:conductor_app/app.dart';
import 'package:conductor_app/core/storage/app_storage.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:shared_preferences/shared_preferences.dart';

void main() {
  testWidgets('first launch boots to the server picker', (tester) async {
    SharedPreferences.setMockInitialValues({});
    final prefs = await SharedPreferences.getInstance();

    await tester.pumpWidget(
      ProviderScope(
        overrides: [sharedPrefsProvider.overrideWithValue(prefs)],
        child: const ConductorApp(),
      ),
    );
    await tester.pumpAndSettle();

    expect(find.text('Conductor'), findsOneWidget);
    expect(find.text('Kind Robots Cloud'), findsOneWidget);
    expect(find.text('Your own server'), findsOneWidget);
    expect(find.text('Just this device'), findsOneWidget);
  });

  testWidgets('choosing local mode lands on the projects dashboard',
      (tester) async {
    SharedPreferences.setMockInitialValues({});
    final prefs = await SharedPreferences.getInstance();

    await tester.pumpWidget(
      ProviderScope(
        overrides: [sharedPrefsProvider.overrideWithValue(prefs)],
        child: const ConductorApp(),
      ),
    );
    await tester.pumpAndSettle();

    await tester.tap(find.text('Just this device'));
    await tester.pumpAndSettle();

    expect(find.text('Projects'), findsWidgets);
    expect(find.text('New project'), findsOneWidget);
  });
}
