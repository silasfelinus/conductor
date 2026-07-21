import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../core/app_state.dart';

/// Mock "attach your drawing" step. There is no real image upload or network
/// call yet -- no backend exists to receive one (out of scope for
/// sketchy/t-008; see that task's note for the follow-up plan).
class SubmissionScreen extends ConsumerWidget {
  const SubmissionScreen({super.key});

  @override
  Widget build(BuildContext context, WidgetRef ref) {
    final bool hasSubmitted = ref.watch(
      sketchyControllerProvider.select((state) => state.hasSubmittedDrawing),
    );

    return Scaffold(
      appBar: AppBar(title: const Text('Submit your drawing')),
      body: Padding(
        padding: const EdgeInsets.all(16),
        child: Column(
          mainAxisAlignment: MainAxisAlignment.center,
          children: [
            Icon(
              hasSubmitted ? Icons.check_circle : Icons.image_outlined,
              size: 96,
              color: hasSubmitted
                  ? Theme.of(context).colorScheme.primary
                  : Theme.of(context).colorScheme.outline,
            ),
            const SizedBox(height: 16),
            Text(
              hasSubmitted
                  ? 'Drawing attached! Ready for critique.'
                  : 'Attach a photo of your finished drawing.',
              textAlign: TextAlign.center,
              style: Theme.of(context).textTheme.titleMedium,
            ),
            const SizedBox(height: 24),
            if (!hasSubmitted)
              FilledButton.icon(
                icon: const Icon(Icons.add_a_photo_outlined),
                label: const Text('Attach drawing'),
                onPressed: () {
                  ref
                      .read(sketchyControllerProvider.notifier)
                      .markDrawingSubmitted();
                },
              )
            else
              FilledButton(
                onPressed: () {
                  ref.read(sketchyControllerProvider.notifier).runCritique();
                  context.go('/critique');
                },
                child: const Text('Get critique'),
              ),
          ],
        ),
      ),
    );
  }
}
