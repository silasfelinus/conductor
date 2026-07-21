import 'skill_tier.dart';

/// A single drawing assignment, per SKILL-LADDER.md's taxonomy.
class Assignment {
  const Assignment({
    required this.id,
    required this.category,
    required this.tier,
    required this.prompt,
    required this.timeWindow,
    required this.successCriteria,
    required this.referenceAllowed,
  });

  final String id;
  final AssignmentCategory category;
  final SkillTier tier;
  final String prompt;
  final String timeWindow;
  final List<String> successCriteria;
  final bool referenceAllowed;
}
