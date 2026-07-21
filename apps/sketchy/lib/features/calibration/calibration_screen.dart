import 'package:flutter/material.dart';
import 'package:flutter_riverpod/flutter_riverpod.dart';
import 'package:go_router/go_router.dart';

import '../../core/app_state.dart';
import '../../core/models/skill_tier.dart';

/// Drawing experience options for calibration question 1 (PRODUCT-SPEC.md).
enum _Experience {
  newToDrawing,
  fewMonths,
  oneToThreeYears,
  threePlusYears;

  String get label {
    switch (this) {
      case _Experience.newToDrawing:
        return 'New';
      case _Experience.fewMonths:
        return 'A few months';
      case _Experience.oneToThreeYears:
        return '1-3 years';
      case _Experience.threePlusYears:
        return '3+ years';
    }
  }

  SkillTier get baselineTier {
    switch (this) {
      case _Experience.newToDrawing:
      case _Experience.fewMonths:
        return SkillTier.beginner;
      case _Experience.oneToThreeYears:
        return SkillTier.intermediate;
      case _Experience.threePlusYears:
        return SkillTier.advanced;
    }
  }
}

/// The first-session calibration flow: 3 quick questions that set the
/// starting skill tier and focus area (PRODUCT-SPEC.md "First Session").
class CalibrationScreen extends ConsumerStatefulWidget {
  const CalibrationScreen({super.key});

  @override
  ConsumerState<CalibrationScreen> createState() => _CalibrationScreenState();
}

class _CalibrationScreenState extends ConsumerState<CalibrationScreen> {
  _Experience _experience = _Experience.fewMonths;
  FocusArea _focusArea = FocusArea.fundamentals;
  final Map<String, double> _comfort = {
    'Basic shapes': 3,
    'Proportions': 3,
    'Shading': 3,
    'Perspective': 3,
  };

  SkillTier _computeTier() {
    final double average =
        _comfort.values.reduce((a, b) => a + b) / _comfort.length;
    final SkillTier baseline = _experience.baselineTier;
    if (average >= 4 && baseline != SkillTier.advanced) {
      return baseline.next;
    }
    if (average <= 2 && baseline != SkillTier.beginner) {
      return SkillTier.values[baseline.index - 1];
    }
    return baseline;
  }

  @override
  Widget build(BuildContext context) {
    return Scaffold(
      appBar: AppBar(title: const Text('Let\'s find your starting point')),
      body: ListView(
        padding: const EdgeInsets.all(16),
        children: [
          Text(
            'How long have you been drawing?',
            style: Theme.of(context).textTheme.titleMedium,
          ),
          const SizedBox(height: 8),
          Wrap(
            spacing: 8,
            children: _Experience.values.map((experience) {
              return ChoiceChip(
                label: Text(experience.label),
                selected: _experience == experience,
                onSelected: (_) => setState(() => _experience = experience),
              );
            }).toList(),
          ),
          const SizedBox(height: 24),
          Text(
            'Which area do you want to focus on?',
            style: Theme.of(context).textTheme.titleMedium,
          ),
          const SizedBox(height: 8),
          Wrap(
            spacing: 8,
            children: FocusArea.values.map((area) {
              return ChoiceChip(
                label: Text(area.label),
                selected: _focusArea == area,
                onSelected: (_) => setState(() => _focusArea = area),
              );
            }).toList(),
          ),
          const SizedBox(height: 24),
          Text(
            'Rate your comfort with each:',
            style: Theme.of(context).textTheme.titleMedium,
          ),
          for (final String skill in _comfort.keys)
            _ComfortSlider(
              label: skill,
              value: _comfort[skill]!,
              onChanged: (value) => setState(() => _comfort[skill] = value),
            ),
          const SizedBox(height: 24),
          FilledButton(
            onPressed: () {
              ref.read(sketchyControllerProvider.notifier).completeCalibration(
                    tier: _computeTier(),
                    focusArea: _focusArea,
                  );
              context.go('/assignment');
            },
            child: const Text('Start drawing'),
          ),
        ],
      ),
    );
  }
}

class _ComfortSlider extends StatelessWidget {
  const _ComfortSlider({
    required this.label,
    required this.value,
    required this.onChanged,
  });

  final String label;
  final double value;
  final ValueChanged<double> onChanged;

  @override
  Widget build(BuildContext context) {
    return Row(
      children: [
        SizedBox(width: 110, child: Text(label)),
        Expanded(
          child: Slider(
            value: value,
            min: 1,
            max: 5,
            divisions: 4,
            label: value.round().toString(),
            onChanged: onChanged,
          ),
        ),
      ],
    );
  }
}
