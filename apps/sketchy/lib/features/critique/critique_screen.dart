import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../core/app_state.dart';
import '../../core/models/critique.dart';

/// Shows the (mock) critique result: per-dimension scores, one strength, one
/// priority fix, and a way to move to the next assignment
/// (PRODUCT-SPEC.md core loop, "Feedback shown" + "Next assignment generated").
class CritiqueScreen extends ConsumerWidget {
  const CritiqueScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final CritiqueResult? result = ref
        .watch(sketchyControllerProvider.select((state) => state.lastCritique));

    if (result == null) {
      return const Scaffold(
        body: Center(child: Text('No critique yet -- submit a drawing first.')),
      );
    }

    return Scaffold(
      appBar: AppBar(title: const Text('Your critique')),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Text(
              result.strength,
              style: Theme.of(context).textTheme.titleMedium,
            ),
            const SizedBox(height: 8),
            Text(result.priorityFix),
            const SizedBox(height: 16),
            Text(
              'Scores',
              style: Theme.of(context).textTheme.titleMedium,
            ),
            for (final MapEntry<CritiqueDimension, int> entry
                in result.scores.entries)
              Padding(
                padding: const EdgeInsets.symmetric(vertical: 4),
                child: Row(
                  children: [
                    SizedBox(width: 140, child: Text(entry.key.label)),
                    Expanded(
                      child: LinearProgressIndicator(value: entry.value / 10),
                    ),
                    const SizedBox(width: 8),
                    Text('${entry.value}/10'),
                  ],
                ),
              ),
            const Spacer(),
            FilledButton(
              onPressed: () {
                ref
                    .read(sketchyControllerProvider.notifier)
                    .advanceToNextAssignment();
                context.go('/assignment');
              },
              child: const Text('Next assignment'),
            ),
          ],
        ),
      ),
    );
  }
}
