import 'skill_tier.dart';

/// The five scoring dimensions from CRITIQUE-RUBRIC.md §1. Not every
/// dimension applies to every assignment category (§2) -- a dimension absent
/// from [CritiqueResult.scores] means it was skipped for that category.
enum CritiqueDimension {
  construction,
  proportions,
  lineQuality,
  value,
  observation;

  String get label {
    switch (this) {
      case CritiqueDimension.construction:
        return 'Construction';
      case CritiqueDimension.proportions:
        return 'Proportions';
      case CritiqueDimension.lineQuality:
        return 'Line quality';
      case CritiqueDimension.value:
        return 'Value / light';
      case CritiqueDimension.observation:
        return 'Observation';
    }
  }
}

/// Result of a (mock) critique pass, per CRITIQUE-RUBRIC.md.
class CritiqueResult {
  const CritiqueResult({
    required this.scores,
    required this.strength,
    required this.priorityFix,
    required this.weakestDimension,
    required this.wasCorrection,
  });

  /// Only dimensions applicable to the submitted assignment's category appear
  /// here -- never a null/zero placeholder for a skipped one (CRITIQUE-RUBRIC.md §2).
  final Map<CritiqueDimension, int> scores;

  /// One encouraging sentence about what worked.
  final String strength;

  /// One specific, actionable next-focus sentence.
  final String priorityFix;

  /// The dimension that drove next-assignment routing (§3 step 2), or null
  /// when every applicable dimension scored 8+ (§3 step 5 -- no real
  /// weakness to target).
  final CritiqueDimension? weakestDimension;

  /// Whether this critique's routing was itself a correction drill -- used by
  /// the friendly-progression override (§3 step 4) to avoid two correction
  /// cycles in a row.
  final bool wasCorrection;
}

/// One step of critique history, kept so the routing algorithm can apply the
/// friendly-progression override and so the tier-advancement rule can look
/// back across recent submissions.
class CritiqueHistoryEntry {
  const CritiqueHistoryEntry({
    required this.result,
    required this.tierAtTheTime,
  });

  final CritiqueResult result;
  final SkillTier tierAtTheTime;
}
