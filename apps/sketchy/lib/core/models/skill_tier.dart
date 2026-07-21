/// The user's current drawing skill tier, per PRODUCT-SPEC.md's calibration step.
enum SkillTier {
  beginner,
  intermediate,
  advanced;

  String get label {
    switch (this) {
      case SkillTier.beginner:
        return 'Beginner';
      case SkillTier.intermediate:
        return 'Intermediate';
      case SkillTier.advanced:
        return 'Advanced';
    }
  }

  /// Bumps to the next tier, or stays at advanced.
  SkillTier get next {
    switch (this) {
      case SkillTier.beginner:
        return SkillTier.intermediate;
      case SkillTier.intermediate:
        return SkillTier.advanced;
      case SkillTier.advanced:
        return SkillTier.advanced;
    }
  }
}

/// The focus area chosen during calibration (PRODUCT-SPEC.md question 2).
enum FocusArea {
  fundamentals,
  people,
  animals,
  environments,
  imagination;

  String get label {
    switch (this) {
      case FocusArea.fundamentals:
        return 'Fundamentals';
      case FocusArea.people:
        return 'People';
      case FocusArea.animals:
        return 'Animals';
      case FocusArea.environments:
        return 'Environments';
      case FocusArea.imagination:
        return 'Imagination';
    }
  }
}

/// Assignment categories from SKILL-LADDER.md's taxonomy (the subset the mock
/// bank currently seeds; the routing algorithm only ever names one of these).
enum AssignmentCategory {
  fundamentals,
  gesture,
  shape,
  value,
  perspective,
  anatomy,
  characterDesign,
  environments,
  styleStudies,
  finishedPieces;

  String get label {
    switch (this) {
      case AssignmentCategory.fundamentals:
        return 'Fundamentals';
      case AssignmentCategory.gesture:
        return 'Gesture';
      case AssignmentCategory.shape:
        return 'Shape';
      case AssignmentCategory.value:
        return 'Value';
      case AssignmentCategory.perspective:
        return 'Perspective';
      case AssignmentCategory.anatomy:
        return 'Anatomy';
      case AssignmentCategory.characterDesign:
        return 'Character design';
      case AssignmentCategory.environments:
        return 'Environments';
      case AssignmentCategory.styleStudies:
        return 'Style studies';
      case AssignmentCategory.finishedPieces:
        return 'Finished pieces';
    }
  }
}
