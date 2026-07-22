import '../models/assignment.dart';
import '../models/skill_tier.dart';

/// Mock assignment pool, one per (category, tier) pair. Prompts are sourced
/// verbatim from SKILL-LADDER.md's sample lists -- no invented text -- since
/// there is no backend assignment generator yet (that is a separate,
/// out-of-scope follow-up per sketchy/t-008's note).
const List<Assignment> assignmentBank = [
  // Fundamentals
  Assignment(
    id: 'fundamentals-beginner-1',
    category: AssignmentCategory.fundamentals,
    tier: SkillTier.beginner,
    prompt: 'Draw 10 straight lines, 10 curves, and 10 ellipses; circle the '
        'cleanest three of each.',
    timeWindow: '5-20 min',
    successCriteria: [
      'Lines are drawn with a single confident stroke, not re-traced.',
      'The three circled examples of each type are genuinely the cleanest.',
    ],
    referenceAllowed: true,
  ),
  Assignment(
    id: 'fundamentals-intermediate-1',
    category: AssignmentCategory.fundamentals,
    tier: SkillTier.intermediate,
    prompt: 'Draw a pair of shoes using simplified boxes and cylinders '
        'before adding contour.',
    timeWindow: '20-60 min',
    successCriteria: [
      'Underlying box/cylinder forms are visible before the contour pass.',
      'Both shoes read as the same size and perspective.',
    ],
    referenceAllowed: true,
  ),
  Assignment(
    id: 'fundamentals-advanced-1',
    category: AssignmentCategory.fundamentals,
    tier: SkillTier.advanced,
    prompt: 'Build a complex prop, such as a bicycle or coffee grinder, '
        'from major forms first.',
    timeWindow: '45-120 min',
    successCriteria: [
      'Major forms are blocked in before any surface detail.',
      'The finished prop reads as one coherent structure, not floating parts.',
    ],
    referenceAllowed: true,
  ),

  // Gesture
  Assignment(
    id: 'gesture-beginner-1',
    category: AssignmentCategory.gesture,
    tier: SkillTier.beginner,
    prompt: 'Do eight 30-second stick-figure action poses from reference.',
    timeWindow: '5-20 min',
    successCriteria: [
      'Each pose has a clear line of action.',
      'Weight looks balanced, not frozen mid-fall.',
    ],
    referenceAllowed: true,
  ),
  Assignment(
    id: 'gesture-intermediate-1',
    category: AssignmentCategory.gesture,
    tier: SkillTier.intermediate,
    prompt: 'Do six 2-minute figure gestures emphasizing weight and balance.',
    timeWindow: '20-60 min',
    successCriteria: [
      'Gesture lines are confident, not repeatedly re-traced.',
      'Weight distribution is readable at a glance.',
    ],
    referenceAllowed: true,
  ),
  Assignment(
    id: 'gesture-advanced-1',
    category: AssignmentCategory.gesture,
    tier: SkillTier.advanced,
    prompt: 'Create a dynamic action pose with clear silhouette, twist, '
        'and weight shift.',
    timeWindow: '45-120 min',
    successCriteria: [
      'Silhouette reads clearly even in flat black.',
      'Torso twist and weight shift feel physically believable.',
    ],
    referenceAllowed: true,
  ),

  // Shape
  Assignment(
    id: 'shape-beginner-1',
    category: AssignmentCategory.shape,
    tier: SkillTier.beginner,
    prompt: 'Draw three monsters using only circles, triangles, and squares.',
    timeWindow: '5-20 min',
    successCriteria: [
      'Each monster is built from the three named shapes only.',
      'The three designs are distinguishable from each other by shape alone.',
    ],
    referenceAllowed: true,
  ),
  Assignment(
    id: 'shape-intermediate-1',
    category: AssignmentCategory.shape,
    tier: SkillTier.intermediate,
    prompt: 'Design three shop signs using distinct silhouettes and no text.',
    timeWindow: '20-60 min',
    successCriteria: [
      'Each sign is identifiable from silhouette alone, without labels.',
      'The three silhouettes are meaningfully different from each other.',
    ],
    referenceAllowed: true,
  ),
  Assignment(
    id: 'shape-advanced-1',
    category: AssignmentCategory.shape,
    tier: SkillTier.advanced,
    prompt: 'Build a character lineup where each role is readable from '
        'silhouette alone.',
    timeWindow: '45-120 min',
    successCriteria: [
      'Every character in the lineup reads correctly in flat silhouette.',
      'Role (hero, sidekick, villain, etc.) is guessable without color or detail.',
    ],
    referenceAllowed: true,
  ),

  // Value
  Assignment(
    id: 'value-beginner-1',
    category: AssignmentCategory.value,
    tier: SkillTier.beginner,
    prompt: 'Shade a sphere, cube, and cylinder with one light source.',
    timeWindow: '5-20 min',
    successCriteria: [
      'Light direction is consistent across all three forms.',
      'Only light and shadow shapes are used -- no arbitrary rendering.',
    ],
    referenceAllowed: true,
  ),
  Assignment(
    id: 'value-intermediate-1',
    category: AssignmentCategory.value,
    tier: SkillTier.intermediate,
    prompt: 'Create a five-value still life from three objects.',
    timeWindow: '20-60 min',
    successCriteria: [
      'Exactly five distinct value groups are visible.',
      'Values group cleanly instead of fighting each other for attention.',
    ],
    referenceAllowed: true,
  ),
  Assignment(
    id: 'value-advanced-1',
    category: AssignmentCategory.value,
    tier: SkillTier.advanced,
    prompt: 'Design a cinematic value study for a character entering a '
        'doorway.',
    timeWindow: '45-120 min',
    successCriteria: [
      'One clear focal point is established through contrast.',
      'The value hierarchy supports the mood of the scene.',
    ],
    referenceAllowed: true,
  ),

  // Perspective
  Assignment(
    id: 'perspective-beginner-1',
    category: AssignmentCategory.perspective,
    tier: SkillTier.beginner,
    prompt: 'Draw a hallway in one-point perspective with three doors.',
    timeWindow: '5-20 min',
    successCriteria: [
      'All lines converge on a single, consistent vanishing point.',
      'The three doors sit correctly on the perspective grid.',
    ],
    referenceAllowed: true,
  ),
  Assignment(
    id: 'perspective-intermediate-1',
    category: AssignmentCategory.perspective,
    tier: SkillTier.intermediate,
    prompt: 'Draw a corner room in two-point perspective with three props.',
    timeWindow: '20-60 min',
    successCriteria: [
      'Both vanishing points are used consistently across the room and props.',
      'Props sit correctly in the room\'s depth, not pasted flat on top.',
    ],
    referenceAllowed: true,
  ),
  Assignment(
    id: 'perspective-advanced-1',
    category: AssignmentCategory.perspective,
    tier: SkillTier.advanced,
    prompt: 'Design a room from an unusual camera angle and keep objects '
        'aligned.',
    timeWindow: '45-120 min',
    successCriteria: [
      'All objects stay aligned to the chosen camera angle throughout.',
      'The unusual angle still reads as a coherent, believable space.',
    ],
    referenceAllowed: true,
  ),

  // Anatomy
  Assignment(
    id: 'anatomy-beginner-1',
    category: AssignmentCategory.anatomy,
    tier: SkillTier.beginner,
    prompt: 'Draw a simple mannequin in front, side, and three-quarter view.',
    timeWindow: '5-20 min',
    successCriteria: [
      'Proportions stay consistent across all three views.',
      'Each view is clearly recognizable as the same figure.',
    ],
    referenceAllowed: true,
  ),
  Assignment(
    id: 'anatomy-intermediate-1',
    category: AssignmentCategory.anatomy,
    tier: SkillTier.intermediate,
    prompt: 'Draw a torso and pelvis bean in six poses.',
    timeWindow: '20-60 min',
    successCriteria: [
      'The torso/pelvis relationship stays anatomically plausible in every pose.',
      'Poses are varied, not six slight repeats of the same one.',
    ],
    referenceAllowed: true,
  ),
  Assignment(
    id: 'anatomy-advanced-1',
    category: AssignmentCategory.anatomy,
    tier: SkillTier.advanced,
    prompt: 'Draw a clothed figure where folds support the gesture and '
        'anatomy.',
    timeWindow: '45-120 min',
    successCriteria: [
      'Fabric folds follow the underlying gesture rather than being decorative.',
      'The figure\'s anatomy still reads clearly through the clothing.',
    ],
    referenceAllowed: true,
  ),

  // Character design
  Assignment(
    id: 'character-design-beginner-1',
    category: AssignmentCategory.characterDesign,
    tier: SkillTier.beginner,
    prompt: 'Design a character from three words: shy, mushroom, explorer.',
    timeWindow: '5-20 min',
    successCriteria: [
      'All three words are legible in the final design.',
      'The character has one clear, simple silhouette.',
    ],
    referenceAllowed: true,
  ),
  Assignment(
    id: 'character-design-intermediate-1',
    category: AssignmentCategory.characterDesign,
    tier: SkillTier.intermediate,
    prompt: 'Design a character sheet with front pose, expression, and one '
        'important prop.',
    timeWindow: '20-60 min',
    successCriteria: [
      'Front pose, expression, and prop are all clearly presented.',
      'The prop reinforces the character\'s identity rather than being generic.',
    ],
    referenceAllowed: true,
  ),
  Assignment(
    id: 'character-design-advanced-1',
    category: AssignmentCategory.characterDesign,
    tier: SkillTier.advanced,
    prompt: 'Make a mini lineup for a story party: leader, trickster, '
        'guardian, wildcard.',
    timeWindow: '45-120 min',
    successCriteria: [
      'Each of the four roles is instantly distinguishable from the others.',
      'The lineup reads as one cohesive team, not four unrelated designs.',
    ],
    referenceAllowed: true,
  ),

  // Environments
  Assignment(
    id: 'environments-beginner-1',
    category: AssignmentCategory.environments,
    tier: SkillTier.beginner,
    prompt: 'Draw a cozy desk corner with three objects and simple '
        'perspective.',
    timeWindow: '5-20 min',
    successCriteria: [
      'The desk plane reads clearly and objects sit on top of it.',
      'One object is clearly the focal point.',
    ],
    referenceAllowed: true,
  ),
  Assignment(
    id: 'environments-intermediate-1',
    category: AssignmentCategory.environments,
    tier: SkillTier.intermediate,
    prompt: 'Design a small shop interior with a clear path and focal '
        'point.',
    timeWindow: '20-60 min',
    successCriteria: [
      'A clear path leads the eye through the space.',
      'One focal point is unambiguous.',
    ],
    referenceAllowed: true,
  ),
  Assignment(
    id: 'environments-advanced-1',
    category: AssignmentCategory.environments,
    tier: SkillTier.advanced,
    prompt: 'Paint a story environment where something just happened.',
    timeWindow: '45-120 min',
    successCriteria: [
      'Props and composition imply a specific recent event.',
      'The scene tells its story without any caption or text.',
    ],
    referenceAllowed: true,
  ),

  // Style studies
  Assignment(
    id: 'style-studies-beginner-1',
    category: AssignmentCategory.styleStudies,
    tier: SkillTier.beginner,
    prompt: 'Pick an artist or cartoon style and identify three visual '
        'rules it uses.',
    timeWindow: '5-20 min',
    successCriteria: [
      'Three specific, concrete visual rules are identified (not vague adjectives).',
      'A small drawing demonstrates at least one of the rules.',
    ],
    referenceAllowed: true,
  ),
  Assignment(
    id: 'style-studies-intermediate-1',
    category: AssignmentCategory.styleStudies,
    tier: SkillTier.intermediate,
    prompt: 'Draw an original character using three observed style rules '
        'from a chosen reference.',
    timeWindow: '20-60 min',
    successCriteria: [
      'The character is original, not a copy of the reference.',
      'All three chosen style rules are visibly applied.',
    ],
    referenceAllowed: true,
  ),
  Assignment(
    id: 'style-studies-advanced-1',
    category: AssignmentCategory.styleStudies,
    tier: SkillTier.advanced,
    prompt: 'Blend two influences into a new, named style with three '
        'rules.',
    timeWindow: '45-120 min',
    successCriteria: [
      'The blended style is genuinely distinct from either single influence.',
      'All three named rules are consistently applied throughout.',
    ],
    referenceAllowed: true,
  ),

  // Finished pieces
  Assignment(
    id: 'finished-pieces-beginner-1',
    category: AssignmentCategory.finishedPieces,
    tier: SkillTier.beginner,
    prompt: 'Finish a clean postcard-sized drawing of one object with '
        'simple shading.',
    timeWindow: '5-20 min',
    successCriteria: [
      'The drawing is fully finished, not left at rough-sketch stage.',
      'Shading is simple and consistent, not patchy.',
    ],
    referenceAllowed: true,
  ),
  Assignment(
    id: 'finished-pieces-intermediate-1',
    category: AssignmentCategory.finishedPieces,
    tier: SkillTier.intermediate,
    prompt: 'Complete a character portrait with readable expression, '
        'prop, and value grouping.',
    timeWindow: '20-60 min',
    successCriteria: [
      'Expression reads clearly at a glance.',
      'Value grouping supports the portrait rather than competing with it.',
    ],
    referenceAllowed: true,
  ),
  Assignment(
    id: 'finished-pieces-advanced-1',
    category: AssignmentCategory.finishedPieces,
    tier: SkillTier.advanced,
    prompt: 'Complete a polished illustration with thumbnail, rough, '
        'value plan, and final pass.',
    timeWindow: '45-120 min',
    successCriteria: [
      'All four stages (thumbnail, rough, value plan, final) are evident in the process.',
      'The final pass shows clear improvement over the initial rough.',
    ],
    referenceAllowed: true,
  ),
];

/// Returns every assignment matching [tier] and, if given, [category].
List<Assignment> assignmentsFor(
  SkillTier tier, {
  AssignmentCategory? category,
}) {
  return assignmentBank
      .where(
          (a) => a.tier == tier && (category == null || a.category == category))
      .toList();
}
