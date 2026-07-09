import 'package:flutter/material.dart';

import 'superkate_style.dart';

class SuperkateOnboardingScreen extends StatelessWidget {
  const SuperkateOnboardingScreen({
    super.key,
    required this.onStart,
    this.isWorking = false,
  });

  final Future<void> Function() onStart;
  final bool isWorking;

  @override
  Widget build(BuildContext context) {
    final palette = SuperkateTheme.of(context);

    return Scaffold(
      body: Container(
        decoration: BoxDecoration(gradient: palette.nightGradient),
        child: Stack(
          children: [
            Positioned(
              top: -70,
              right: -58,
              child: _OnboardingOrb(
                size: 220,
                color: palette.primary.withAlpha(43),
                glow: palette.primary.withAlpha(92),
              ),
            ),
            Positioned(
              bottom: 70,
              left: -92,
              child: _OnboardingOrb(
                size: 240,
                color: palette.secondary.withAlpha(34),
                glow: palette.secondary.withAlpha(76),
              ),
            ),
            SafeArea(
              child: Center(
                child: SingleChildScrollView(
                  padding: const EdgeInsets.all(24),
                  child: ConstrainedBox(
                    constraints: const BoxConstraints(maxWidth: 620),
                    child: Card(
                      color: palette.card,
                      shape: SuperkateStyle.cardShape(border: palette.cardBorder),
                      child: Padding(
                        padding: const EdgeInsets.all(24),
                        child: Column(
                          mainAxisSize: MainAxisSize.min,
                          crossAxisAlignment: CrossAxisAlignment.stretch,
                          children: [
                            const Align(
                              alignment: Alignment.centerLeft,
                              child: RainbowBadge(icon: Icons.content_cut),
                            ),
                            const SizedBox(height: 20),
                            Text(
                              'Hair by Superkate',
                              style: TextStyle(
                                color: palette.soft,
                                fontSize: 34,
                                fontWeight: FontWeight.w900,
                                height: 1.02,
                              ),
                            ),
                            const SizedBox(height: 8),
                            Text(
                              'Private services calculator beta',
                              style: TextStyle(
                                color: palette.secondary,
                                fontSize: 18,
                                fontWeight: FontWeight.w900,
                              ),
                            ),
                            const SizedBox(height: 18),
                            const RainbowRail(height: 6),
                            const SizedBox(height: 22),
                            Text(
                              'Set the hourly rate, time spent, and product cost, then prepare warm receipt drafts without sending anything behind your back.',
                              style: TextStyle(
                                color: palette.muted,
                                fontSize: 16,
                                height: 1.35,
                              ),
                            ),
                            const SizedBox(height: 22),
                            const _OnboardingStepCard(
                              icon: Icons.lock_outline,
                              title: 'Local-first beta',
                              body: 'Appointment and customer data stay on this device until explicit sync work is ready.',
                            ),
                            const SizedBox(height: 12),
                            const _OnboardingStepCard(
                              icon: Icons.calculate_outlined,
                              title: 'Fast salon math',
                              body: 'Rate × time plus products gives the total, with receipt details ready to review.',
                            ),
                            const SizedBox(height: 12),
                            const _OnboardingStepCard(
                              icon: Icons.favorite_border,
                              title: 'Superkate voice',
                              body: 'Rainbow styling, warm copy, and no store/publish/sending behavior in this beta.',
                            ),
                            const SizedBox(height: 24),
                            FilledButton.icon(
                              key: const ValueKey('start-local-beta-button'),
                              onPressed: isWorking
                                  ? null
                                  : () async {
                                      try {
                                        await onStart();
                                      } catch (_) {
                                        if (context.mounted) {
                                          ScaffoldMessenger.of(context)
                                            ..clearSnackBars()
                                            ..showSnackBar(
                                              const SnackBar(
                                                content: Text(
                                                  'The onramp could not be saved. Try again.',
                                                ),
                                              ),
                                            );
                                        }
                                      }
                                    },
                              icon: isWorking
                                  ? const SizedBox.square(
                                      dimension: 18,
                                      child: CircularProgressIndicator(strokeWidth: 2),
                                    )
                                  : const Icon(Icons.rocket_launch),
                              label: Text(
                                isWorking ? 'Opening your chair...' : 'Start local beta',
                              ),
                            ),
                            const SizedBox(height: 10),
                            Text(
                              'Use fake/local data until durable handoff gates are cleared.',
                              textAlign: TextAlign.center,
                              style: TextStyle(
                                color: palette.quiet,
                                fontSize: 12,
                                fontWeight: FontWeight.w700,
                              ),
                            ),
                          ],
                        ),
                      ),
                    ),
                  ),
                ),
              ),
            ),
          ],
        ),
      ),
    );
  }
}

class _OnboardingStepCard extends StatelessWidget {
  const _OnboardingStepCard({
    required this.icon,
    required this.title,
    required this.body,
  });

  final IconData icon;
  final String title;
  final String body;

  @override
  Widget build(BuildContext context) {
    final palette = SuperkateTheme.of(context);

    return Container(
      padding: const EdgeInsets.all(16),
      decoration: BoxDecoration(
        color: palette.cardStrong,
        borderRadius: BorderRadius.circular(24),
        border: Border.all(color: palette.cardBorder),
      ),
      child: Row(
        crossAxisAlignment: CrossAxisAlignment.start,
        children: [
          Container(
            width: 44,
            height: 44,
            decoration: BoxDecoration(
              shape: BoxShape.circle,
              gradient: palette.electricGradient,
              boxShadow: palette.softGlow,
            ),
            child: Icon(icon, color: palette.ink, size: 22),
          ),
          const SizedBox(width: 14),
          Expanded(
            child: Column(
              crossAxisAlignment: CrossAxisAlignment.start,
              children: [
                Text(
                  title,
                  style: TextStyle(
                    color: palette.soft,
                    fontSize: 15,
                    fontWeight: FontWeight.w900,
                  ),
                ),
                const SizedBox(height: 4),
                Text(
                  body,
                  style: TextStyle(
                    color: palette.muted,
                    fontSize: 13,
                    height: 1.3,
                  ),
                ),
              ],
            ),
          ),
        ],
      ),
    );
  }
}

class _OnboardingOrb extends StatelessWidget {
  const _OnboardingOrb({
    required this.size,
    required this.color,
    required this.glow,
  });

  final double size;
  final Color color;
  final Color glow;

  @override
  Widget build(BuildContext context) {
    return IgnorePointer(
      child: Container(
        width: size,
        height: size,
        decoration: BoxDecoration(
          shape: BoxShape.circle,
          color: color,
          boxShadow: [
            BoxShadow(
              color: glow,
              blurRadius: 90,
              spreadRadius: 18,
            ),
          ],
        ),
      ),
    );
  }
}
