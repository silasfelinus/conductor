import 'dart:math';

import '../models/assignment.dart';
import '../models/critique.dart';
import '../models/skill_tier.dart';
import 'assignment_bank.dart';

/// Which of the 5 rubric dimensions apply to a given assignment category,
/// per CRITIQUE-RUBRIC.md §2. A '-' in that table means "always skip"; this
/// mock treats every non-'-' cell (both 'yes' and '?') as applicable, since
/// judging the finer '?' condition requires the live assignment's actual
/// successCriteria wording -- a simplification called out in sketchy/t-008's
/// note for the next iteration once a real critique engine exists.
Set<CritiqueDimension> applicableDimensions(AssignmentCategory category) {
  switch (category) {
    case AssignmentCategory.fundamentals:
      return {
        CritiqueDimension.construction,
        CritiqueDimension.proportions,
        CritiqueDimension.lineQuality,
        CritiqueDimension.value,
        CritiqueDimension.observation,
      };
    case AssignmentCategory.gesture:
      return {
        CritiqueDimension.construction,
        CritiqueDimension.proportions,
        CritiqueDimension.lineQuality,
        CritiqueDimension.observation,
      };
    case AssignmentCategory.shape:
      return {
        CritiqueDimension.construction,
        CritiqueDimension.proportions,
        CritiqueDimension.lineQuality,
      };
    case AssignmentCategory.value:
      return {
        CritiqueDimension.construction,
        CritiqueDimension.proportions,
        CritiqueDimension.lineQuality,
        CritiqueDimension.value,
        CritiqueDimension.observation,
      };
    case AssignmentCategory.perspective:
      return {
        CritiqueDimension.construction,
        CritiqueDimension.proportions,
        CritiqueDimension.lineQuality,
        CritiqueDimension.value,
        CritiqueDimension.observation,
      };
    case AssignmentCategory.anatomy:
      return {
        CritiqueDimension.construction,
        CritiqueDimension.proportions,
        CritiqueDimension.lineQuality,
        CritiqueDimension.value,
        CritiqueDimension.observation,
      };
    case AssignmentCategory.characterDesign:
      return {
        CritiqueDimension.construction,
        CritiqueDimension.proportions,
        CritiqueDimension.lineQuality,
        CritiqueDimension.value,
      };
    case AssignmentCategory.environments:
      return {
        CritiqueDimension.construction,
        CritiqueDimension.proportions,
        CritiqueDimension.lineQuality,
        CritiqueDimension.value,
        CritiqueDimension.observation,
      };
    case AssignmentCategory.styleStudies:
      return {
        CritiqueDimension.construction,
        CritiqueDimension.proportions,
        CritiqueDimension.lineQuality,
        CritiqueDimension.value,
      };
    case AssignmentCategory.finishedPieces:
      return {
        CritiqueDimension.construction,
        CritiqueDimension.proportions,
        CritiqueDimension.lineQuality,
        CritiqueDimension.value,
        CritiqueDimension.observation,
      };
  }
}

/// Tie-break priority order from CRITIQUE-RUBRIC.md §3 step 2 (earlier wins).
const List<CritiqueDimension> _tieBreakPriority = [
  CritiqueDimension.construction,
  CritiqueDimension.proportions,
  CritiqueDimension.observation,
  CritiqueDimension.lineQuality,
  CritiqueDimension.value,
];

String _lowAnchor(CritiqueDimension dimension) {
  switch (dimension) {
    case CritiqueDimension.construction:
      return 'the underlying forms need to show through the linework more clearly';
    case CritiqueDimension.proportions:
      return 'a couple of proportion relationships are drifting';
    case CritiqueDimension.lineQuality:
      return 'the line could be more deliberate and less re-traced';
    case CritiqueDimension.value:
      return 'the value groups are fighting each other for attention';
    case CritiqueDimension.observation:
      return 'the shapes could match the reference more closely';
  }
}

String _highAnchor(CritiqueDimension dimension) {
  switch (dimension) {
    case CritiqueDimension.construction:
      return 'reads as one coherent 3D structure';
    case CritiqueDimension.proportions:
      return 'the proportions hold up under scrutiny';
    case CritiqueDimension.lineQuality:
      return 'the line is confident and deliberate';
    case CritiqueDimension.value:
      return 'the values read clearly with one obvious focal point';
    case CritiqueDimension.observation:
      return 'it matches the reference closely in structure and proportion';
  }
}

/// Generates a mock critique for a completed [assignment]. There is no live
/// AI critique call yet (out of scope for sketchy/t-008) -- scores are a
/// deterministic pseudo-random draw seeded on the assignment id, so the same
/// assignment always "critiques" the same way during manual testing.
CritiqueResult generateMockCritique(
  Assignment assignment, {
  required bool previousWasCorrection,
}) {
  final Random random = Random(assignment.id.hashCode);
  final Set<CritiqueDimension> applicable =
      applicableDimensions(assignment.category);
  final Map<CritiqueDimension, int> scores = {
    for (final CritiqueDimension dimension in applicable)
      dimension: 4 + random.nextInt(7), // 4-10, biased toward encouraging
  };

  CritiqueDimension? weakest;
  int weakestScore = 11;
  for (final CritiqueDimension dimension in _tieBreakPriority) {
    final int? score = scores[dimension];
    if (score == null) continue;
    if (score < weakestScore) {
      weakestScore = score;
      weakest = dimension;
    }
  }

  final bool allStrong = scores.values.every((score) => score >= 8);
  final CritiqueDimension? routingDimension = allStrong ? null : weakest;

  CritiqueDimension topDimension = _tieBreakPriority.firstWhere(
    (dimension) => scores.containsKey(dimension),
  );
  int topScore = scores[topDimension] ?? 0;
  for (final MapEntry<CritiqueDimension, int> entry in scores.entries) {
    if (entry.value > topScore) {
      topScore = entry.value;
      topDimension = entry.key;
    }
  }

  final String strength = 'Your ${topDimension.label.toLowerCase()} stood out: '
      '${_highAnchor(topDimension)}.';
  final String priorityFix = routingDimension == null
      ? 'Everything scored strong this round -- time for a bigger challenge.'
      : 'Focus next on ${routingDimension.label.toLowerCase()}: '
          '${_lowAnchor(routingDimension)}.';

  return CritiqueResult(
    scores: scores,
    strength: strength,
    priorityFix: priorityFix,
    weakestDimension: routingDimension,
    wasCorrection: routingDimension != null,
  );
}

/// Picks the next assignment's category per CRITIQUE-RUBRIC.md §3 steps 3-5.
AssignmentCategory nextCategoryFor({
  required CritiqueResult result,
  required AssignmentCategory completedCategory,
  required bool previousWasCorrection,
}) {
  // Step 5: nothing to correct -- combine everything.
  if (result.weakestDimension == null) {
    return AssignmentCategory.finishedPieces;
  }

  // Step 4: don't run two correction drills in a row.
  if (previousWasCorrection) {
    return AssignmentCategory.shape;
  }

  // Step 3: map the weakest dimension to its primary target category.
  switch (result.weakestDimension!) {
    case CritiqueDimension.construction:
      return AssignmentCategory.fundamentals;
    case CritiqueDimension.proportions:
      return completedCategory == AssignmentCategory.anatomy
          ? AssignmentCategory.anatomy
          : AssignmentCategory.fundamentals;
    case CritiqueDimension.lineQuality:
      return AssignmentCategory.gesture;
    case CritiqueDimension.value:
      return AssignmentCategory.value;
    case CritiqueDimension.observation:
      return AssignmentCategory.perspective;
  }
}

/// Picks a specific next [Assignment] for [tier]/[category], falling back to
/// any assignment at [tier] if the mock bank has no entry for that pairing.
Assignment pickNextAssignment(SkillTier tier, AssignmentCategory category) {
  final List<Assignment> matches = assignmentsFor(tier, category: category);
  if (matches.isNotEmpty) {
    return matches.first;
  }
  return assignmentsFor(tier).first;
}
