import 'package:flutter_test/flutter_test.dart';
import 'package:sketchy/core/data/assignment_bank.dart';
import 'package:sketchy/core/data/critique_engine.dart';
import 'package:sketchy/core/models/assignment.dart';
import 'package:sketchy/core/models/critique.dart';
import 'package:sketchy/core/models/skill_tier.dart';

CritiqueResult _resultFor(CritiqueDimension? weakest) {
  return CritiqueResult(
    scores: const {},
    strength: 'strength',
    priorityFix: 'fix',
    weakestDimension: weakest,
    wasCorrection: weakest != null,
  );
}

void main() {
  group('applicableDimensions', () {
    test('shape category excludes value and observation', () {
      final Set<CritiqueDimension> dimensions =
          applicableDimensions(AssignmentCategory.shape);
      expect(dimensions, isNot(contains(CritiqueDimension.value)));
      expect(dimensions, isNot(contains(CritiqueDimension.observation)));
      expect(dimensions, contains(CritiqueDimension.construction));
    });

    test('finished pieces includes all five dimensions', () {
      final Set<CritiqueDimension> dimensions =
          applicableDimensions(AssignmentCategory.finishedPieces);
      expect(dimensions.length, 5);
    });
  });

  group('generateMockCritique', () {
    test('is deterministic for the same assignment id', () {
      final Assignment assignment = assignmentBank.first;
      final CritiqueResult first =
          generateMockCritique(assignment, previousWasCorrection: false);
      final CritiqueResult second =
          generateMockCritique(assignment, previousWasCorrection: false);
      expect(first.scores, second.scores);
      expect(first.weakestDimension, second.weakestDimension);
    });

    test('never scores a dimension outside the applicable set', () {
      final Assignment assignment = assignmentBank
          .firstWhere((a) => a.category == AssignmentCategory.shape);
      final CritiqueResult result =
          generateMockCritique(assignment, previousWasCorrection: false);
      expect(result.scores.keys,
          everyElement(applicableDimensions(assignment.category).contains));
    });
  });

  group('nextCategoryFor routing (CRITIQUE-RUBRIC.md §3)', () {
    test('all-strong result routes to finished pieces regardless of override',
        () {
      final AssignmentCategory next = nextCategoryFor(
        result: _resultFor(null),
        completedCategory: AssignmentCategory.fundamentals,
        previousWasCorrection: true,
      );
      expect(next, AssignmentCategory.finishedPieces);
    });

    test('friendly-progression override wins over the dimension mapping', () {
      final AssignmentCategory next = nextCategoryFor(
        result: _resultFor(CritiqueDimension.construction),
        completedCategory: AssignmentCategory.fundamentals,
        previousWasCorrection: true,
      );
      expect(next, AssignmentCategory.shape);
    });

    test('construction routes to fundamentals', () {
      final AssignmentCategory next = nextCategoryFor(
        result: _resultFor(CritiqueDimension.construction),
        completedCategory: AssignmentCategory.gesture,
        previousWasCorrection: false,
      );
      expect(next, AssignmentCategory.fundamentals);
    });

    test(
        'proportions routes to anatomy only when completed category was anatomy',
        () {
      expect(
        nextCategoryFor(
          result: _resultFor(CritiqueDimension.proportions),
          completedCategory: AssignmentCategory.anatomy,
          previousWasCorrection: false,
        ),
        AssignmentCategory.anatomy,
      );
      expect(
        nextCategoryFor(
          result: _resultFor(CritiqueDimension.proportions),
          completedCategory: AssignmentCategory.shape,
          previousWasCorrection: false,
        ),
        AssignmentCategory.fundamentals,
      );
    });

    test('line quality routes to gesture', () {
      expect(
        nextCategoryFor(
          result: _resultFor(CritiqueDimension.lineQuality),
          completedCategory: AssignmentCategory.fundamentals,
          previousWasCorrection: false,
        ),
        AssignmentCategory.gesture,
      );
    });

    test('value routes to value', () {
      expect(
        nextCategoryFor(
          result: _resultFor(CritiqueDimension.value),
          completedCategory: AssignmentCategory.fundamentals,
          previousWasCorrection: false,
        ),
        AssignmentCategory.value,
      );
    });

    test('observation routes to perspective', () {
      expect(
        nextCategoryFor(
          result: _resultFor(CritiqueDimension.observation),
          completedCategory: AssignmentCategory.fundamentals,
          previousWasCorrection: false,
        ),
        AssignmentCategory.perspective,
      );
    });
  });

  group('pickNextAssignment', () {
    test('returns an assignment matching tier and category when available', () {
      final Assignment assignment =
          pickNextAssignment(SkillTier.beginner, AssignmentCategory.gesture);
      expect(assignment.tier, SkillTier.beginner);
      expect(assignment.category, AssignmentCategory.gesture);
    });
  });
}
