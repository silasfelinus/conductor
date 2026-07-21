import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../core/app_state.dart';
import '../../core/models/assignment.dart';

/// Shows the user's current assignment: prompt, time window, success
/// criteria, and reference note (PRODUCT-SPEC.md's core loop, step 1).
class AssignmentScreen extends ConsumerWidget {
  const AssignmentScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final Assignment? assignment = ref.watch(
        sketchyControllerProvider.select((state) => state.currentAssignment));

    if (assignment == null) {
      return const Scaffold(
        body: Center(
            child: Text('No assignment yet -- complete calibration first.')),
      );
    }

    return Scaffold(
      appBar: AppBar(title: const Text('Today\'s assignment')),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          crossAxisAlignment: CrossAxisAlignment.start,
          children: [
            Chip(label: Text(assignment.category.label)),
            const SizedBox(height: 12),
            Text(
              assignment.prompt,
              style: Theme.of(context).textTheme.headlineSmall,
            ),
            const SizedBox(height: 12),
            Text('Time window: ${assignment.timeWindow}'),
            Text(
              assignment.referenceAllowed
                  ? 'Reference is allowed -- use one if it helps.'
                  : 'Draw from imagination -- no reference this time.',
            ),
            const SizedBox(height: 16),
            Text(
              'We\'ll check for:',
              style: Theme.of(context).textTheme.titleMedium,
            ),
            for (final String criterion in assignment.successCriteria)
              Padding(
                padding: const EdgeInsets.only(top: 4),
                child: Row(
                  crossAxisAlignment: CrossAxisAlignment.start,
                  children: [
                    const Text('- '),
                    Expanded(child: Text(criterion)),
                  ],
                ),
              ),
            const Spacer(),
            FilledButton(
              onPressed: () => context.go('/submission'),
              child: const Text('I\'m done -- submit for critique'),
            ),
          ],
        ),
      ),
    );
  }
}
