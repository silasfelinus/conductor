import 'package:flutter/material.dart';
import 'package:flutter_test/flutter_test.dart';
import 'package:superkate_services_calculator/data/in_memory_app_lock_service.dart';
import 'package:superkate_services_calculator/data/in_memory_onboarding_service.dart';
import 'package:superkate_services_calculator/data/in_memory_persistence_service.dart';
import 'package:superkate_services_calculator/main.dart';

void _useTallSurface(WidgetTester tester) {
  tester.view.physicalSize = const Size(1200, 2600);
  tester.view.devicePixelRatio = 1.0;
  addTearDown(tester.view.resetPhysicalSize);
  addTearDown(tester.view.resetDevicePixelRatio);
}

Future<void> _pumpApp(
  WidgetTester tester, {
  required InMemoryOnboardingService onboarding,
  required InMemoryAppLockService lock,
}) async {
  await tester.pumpWidget(
    SuperkateServicesCalculatorApp(
      service: Future.value(InMemoryPersistenceService()),
      onboardingService: Future.value(onboarding),
      appLockService: Future.value(lock),
    ),
  );
  await tester.pumpAndSettle();
}

Future<void> _tapVisible(WidgetTester tester, Finder finder) async {
  await tester.ensureVisible(finder);
  await tester.pumpAndSettle();
  await tester.tap(finder);
  await tester.pumpAndSettle();
}

void main() {
  testWidgets('onboarding offers the app lock and enabling it stores the PIN',
      (tester) async {
    _useTallSurface(tester);
    final onboarding = InMemoryOnboardingService();
    final lock = InMemoryAppLockService();
    await _pumpApp(tester, onboarding: onboarding, lock: lock);

    expect(find.text('Keep the client book private'), findsOneWidget);

    await _tapVisible(
        tester, find.byKey(const ValueKey('onboarding-app-lock-switch')));
    await tester.enterText(
        find.byKey(const ValueKey('onboarding-app-lock-pin')), '2468');
    await tester.enterText(
        find.byKey(const ValueKey('onboarding-app-lock-repeat-pin')), '2468');
    await _tapVisible(
        tester, find.byKey(const ValueKey('start-local-beta-button')));

    expect(await onboarding.hasCompletedOnboarding(), isTrue);
    expect(await lock.isEnabled(), isTrue);
    expect(await lock.verifyPin('2468'), isTrue);
    // She just set the PIN — the calculator opens without an extra lock stop.
    expect(find.text('New appointment'), findsOneWidget);
  });

  testWidgets('onboarding rejects mismatched PINs and stays on the onramp',
      (tester) async {
    _useTallSurface(tester);
    final onboarding = InMemoryOnboardingService();
    final lock = InMemoryAppLockService();
    await _pumpApp(tester, onboarding: onboarding, lock: lock);

    await _tapVisible(
        tester, find.byKey(const ValueKey('onboarding-app-lock-switch')));
    await tester.enterText(
        find.byKey(const ValueKey('onboarding-app-lock-pin')), '2468');
    await tester.enterText(
        find.byKey(const ValueKey('onboarding-app-lock-repeat-pin')), '1357');
    await _tapVisible(
        tester, find.byKey(const ValueKey('start-local-beta-button')));

    expect(find.text("Those PINs don't match each other."), findsOneWidget);
    expect(await onboarding.hasCompletedOnboarding(), isFalse);
    expect(await lock.isEnabled(), isFalse);
  });

  testWidgets('onboarding without the lock leaves it off', (tester) async {
    _useTallSurface(tester);
    final onboarding = InMemoryOnboardingService();
    final lock = InMemoryAppLockService();
    await _pumpApp(tester, onboarding: onboarding, lock: lock);

    await _tapVisible(
        tester, find.byKey(const ValueKey('start-local-beta-button')));

    expect(await onboarding.hasCompletedOnboarding(), isTrue);
    expect(await lock.isEnabled(), isFalse);
    expect(find.text('New appointment'), findsOneWidget);
  });

  testWidgets('a locked app opens with the right PIN and rejects a wrong one',
      (tester) async {
    _useTallSurface(tester);
    final onboarding = InMemoryOnboardingService(completed: true);
    final lock = InMemoryAppLockService(pin: '2468');
    await _pumpApp(tester, onboarding: onboarding, lock: lock);

    // Locked: no client data visible.
    expect(find.text('Your client book is locked. Enter your PIN to open your chair.'),
        findsOneWidget);
    expect(find.text('New appointment'), findsNothing);

    await tester.enterText(
        find.byKey(const ValueKey('app-lock-pin-field')), '1111');
    await _tapVisible(
        tester, find.byKey(const ValueKey('app-lock-unlock-button')));
    expect(find.text("That PIN doesn't match — take a breath and try again."),
        findsOneWidget);
    expect(find.text('New appointment'), findsNothing);

    await tester.enterText(
        find.byKey(const ValueKey('app-lock-pin-field')), '2468');
    await _tapVisible(
        tester, find.byKey(const ValueKey('app-lock-unlock-button')));
    expect(find.text('New appointment'), findsOneWidget);
  });

  testWidgets('settings sheet turns the lock on from the home page',
      (tester) async {
    _useTallSurface(tester);
    final onboarding = InMemoryOnboardingService(completed: true);
    final lock = InMemoryAppLockService();
    await _pumpApp(tester, onboarding: onboarding, lock: lock);

    await _tapVisible(
        tester, find.byKey(const ValueKey('app-lock-settings-button')));
    await tester.enterText(
        find.byKey(const ValueKey('app-lock-new-pin')), '7531');
    await tester.enterText(
        find.byKey(const ValueKey('app-lock-repeat-pin')), '7531');
    await _tapVisible(
        tester, find.byKey(const ValueKey('app-lock-turn-on-button')));

    expect(await lock.isEnabled(), isTrue);
    expect(await lock.verifyPin('7531'), isTrue);
    expect(
      find.text('App lock is on. Your client book opens with your PIN.'),
      findsOneWidget,
    );
  });

  testWidgets('settings sheet requires the current PIN to turn the lock off',
      (tester) async {
    _useTallSurface(tester);
    final onboarding = InMemoryOnboardingService(completed: true);
    final lock = InMemoryAppLockService(pin: '2468');
    await _pumpApp(tester, onboarding: onboarding, lock: lock);

    // Unlock first.
    await tester.enterText(
        find.byKey(const ValueKey('app-lock-pin-field')), '2468');
    await _tapVisible(
        tester, find.byKey(const ValueKey('app-lock-unlock-button')));

    await _tapVisible(
        tester, find.byKey(const ValueKey('app-lock-settings-button')));

    // Wrong current PIN keeps the lock on.
    await tester.enterText(
        find.byKey(const ValueKey('app-lock-current-pin')), '0000');
    await _tapVisible(
        tester, find.byKey(const ValueKey('app-lock-turn-off-button')));
    expect(await lock.isEnabled(), isTrue);
    expect(find.text("That PIN doesn't match — the lock stays on."),
        findsOneWidget);

    // Correct current PIN turns it off.
    await tester.enterText(
        find.byKey(const ValueKey('app-lock-current-pin')), '2468');
    await _tapVisible(
        tester, find.byKey(const ValueKey('app-lock-turn-off-button')));
    expect(await lock.isEnabled(), isFalse);
  });

  testWidgets('settings sheet changes the PIN with the current one',
      (tester) async {
    _useTallSurface(tester);
    final onboarding = InMemoryOnboardingService(completed: true);
    final lock = InMemoryAppLockService(pin: '2468');
    await _pumpApp(tester, onboarding: onboarding, lock: lock);

    await tester.enterText(
        find.byKey(const ValueKey('app-lock-pin-field')), '2468');
    await _tapVisible(
        tester, find.byKey(const ValueKey('app-lock-unlock-button')));

    await _tapVisible(
        tester, find.byKey(const ValueKey('app-lock-settings-button')));
    await tester.enterText(
        find.byKey(const ValueKey('app-lock-current-pin')), '2468');
    await tester.enterText(
        find.byKey(const ValueKey('app-lock-new-pin')), '13579');
    await tester.enterText(
        find.byKey(const ValueKey('app-lock-repeat-pin')), '13579');
    await _tapVisible(
        tester, find.byKey(const ValueKey('app-lock-change-pin-button')));

    expect(await lock.verifyPin('13579'), isTrue);
    expect(await lock.verifyPin('2468'), isFalse);
  });
}
