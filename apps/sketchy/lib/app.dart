import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import 'core/app_state.dart';
import 'core/theme/sketchy_theme.dart';
import 'features/assignment/assignment_screen.dart';
import 'features/calibration/calibration_screen.dart';
import 'features/critique/critique_screen.dart';
import 'features/submission/submission_screen.dart';

/// Caches a single [GoRouter] instance -- built lazily via [buildSketchyRouter]
/// -- so navigation state survives widget rebuilds instead of resetting on
/// every SketchyApp.build() call.
final Provider<GoRouter> sketchyRouterProvider =
    Provider<GoRouter>(buildSketchyRouter);

/// Builds the router with a redirect that keeps an uncalibrated user on the
/// calibration screen, per PRODUCT-SPEC.md's "First Session (Calibration)".
GoRouter buildSketchyRouter(Ref ref) {
  return GoRouter(
    initialLocation: '/calibration',
    redirect: (context, state) {
      final bool isCalibrated =
          ref.read(sketchyControllerProvider).isCalibrated;
      final bool goingToCalibration = state.matchedLocation == '/calibration';
      if (!isCalibrated && !goingToCalibration) {
        return '/calibration';
      }
      if (isCalibrated && goingToCalibration) {
        return '/assignment';
      }
      return null;
    },
    routes: [
      GoRoute(
        path: '/calibration',
        builder: (context, state) => const CalibrationScreen(),
      ),
      GoRoute(
        path: '/assignment',
        builder: (context, state) => const AssignmentScreen(),
      ),
      GoRoute(
        path: '/submission',
        builder: (context, state) => const SubmissionScreen(),
      ),
      GoRoute(
        path: '/critique',
        builder: (context, state) => const CritiqueScreen(),
      ),
    ],
  );
}

/// Root widget for the Sketchy app.
class SketchyApp extends ConsumerWidget {
  const SketchyApp({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final GoRouter router = ref.watch(sketchyRouterProvider);
    return MaterialApp.router(
      title: 'Sketchy',
      theme: buildSketchyTheme(),
      routerConfig: router,
    );
  }
}
