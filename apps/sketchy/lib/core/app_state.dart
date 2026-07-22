import 'package:flutter_riverpod/flutter_riverpod.dart';

import 'data/critique_engine.dart';
import 'models/assignment.dart';
import 'models/critique.dart';
import 'models/skill_tier.dart';

/// The full state of a Sketchy session: where the user is in the core loop
/// (calibration -> assignment -> submission -> critique -> next assignment).
class SketchyState {
  const SketchyState({
    this.tier,
    this.focusArea,
    this.currentAssignment,
    this.hasSubmittedDrawing = false,
    this.lastCritique,
    this.history = const [],
  });

  /// Null until calibration completes.
  final SkillTier? tier;
  final FocusArea? focusArea;
  final Assignment? currentAssignment;
  final bool hasSubmittedDrawing;
  final CritiqueResult? lastCritique;
  final List<CritiqueHistoryEntry> history;

  bool get isCalibrated => tier != null;

  SketchyState copyWith({
    SkillTier? tier,
    FocusArea? focusArea,
    Assignment? currentAssignment,
    bool? hasSubmittedDrawing,
    CritiqueResult? lastCritique,
    List<CritiqueHistoryEntry>? history,
    bool clearCritique = false,
  }) {
    return SketchyState(
      tier: tier ?? this.tier,
      focusArea: focusArea ?? this.focusArea,
      currentAssignment: currentAssignment ?? this.currentAssignment,
      hasSubmittedDrawing: hasSubmittedDrawing ?? this.hasSubmittedDrawing,
      lastCritique: clearCritique ? null : (lastCritique ?? this.lastCritique),
      history: history ?? this.history,
    );
  }
}

/// Owns the Sketchy core-loop state and the transitions between its steps.
/// All data is mock/local -- there is no backend yet (see sketchy/t-008's
/// scope note), so every transition runs synchronously and instantly.
class SketchyController extends Notifier<SketchyState> {
  @override
  SketchyState build() => const SketchyState();

  /// Completes calibration: sets the starting tier/focus and loads the first
  /// assignment, per PRODUCT-SPEC.md's "First Session (Calibration)" flow.
  void completeCalibration({
    required SkillTier tier,
    required FocusArea focusArea,
  }) {
    final Assignment first =
        pickNextAssignment(tier, _defaultCategoryFor(focusArea));
    state = state.copyWith(
      tier: tier,
      focusArea: focusArea,
      currentAssignment: first,
    );
  }

  void markDrawingSubmitted() {
    state = state.copyWith(hasSubmittedDrawing: true);
  }

  /// Runs the mock critique for the current assignment and records it.
  void runCritique() {
    final Assignment? assignment = state.currentAssignment;
    if (assignment == null) return;

    final bool previousWasCorrection =
        state.history.isNotEmpty && state.history.last.result.wasCorrection;
    final CritiqueResult result = generateMockCritique(
      assignment,
      previousWasCorrection: previousWasCorrection,
    );

    state = state.copyWith(
      lastCritique: result,
      history: [
        ...state.history,
        CritiqueHistoryEntry(result: result, tierAtTheTime: state.tier!),
      ],
    );
  }

  /// Advances to the next assignment using the critique routing algorithm,
  /// per CRITIQUE-RUBRIC.md §3, then resets the submission/critique step so
  /// the loop can run again.
  void advanceToNextAssignment() {
    final CritiqueResult? result = state.lastCritique;
    final Assignment? completed = state.currentAssignment;
    final SkillTier? tier = state.tier;
    if (result == null || completed == null || tier == null) return;

    final bool previousWasCorrection = state.history.length > 1 &&
        state.history[state.history.length - 2].result.wasCorrection;
    final AssignmentCategory nextCategory = nextCategoryFor(
      result: result,
      completedCategory: completed.category,
      previousWasCorrection: previousWasCorrection,
    );
    final Assignment next = pickNextAssignment(tier, nextCategory);

    state = state.copyWith(
      currentAssignment: next,
      hasSubmittedDrawing: false,
      clearCritique: true,
    );
  }

  AssignmentCategory _defaultCategoryFor(FocusArea focusArea) {
    switch (focusArea) {
      case FocusArea.fundamentals:
        return AssignmentCategory.fundamentals;
      case FocusArea.people:
        return AssignmentCategory.anatomy;
      case FocusArea.animals:
        return AssignmentCategory.gesture;
      case FocusArea.environments:
        return AssignmentCategory.environments;
      case FocusArea.imagination:
        return AssignmentCategory.characterDesign;
    }
  }
}

final NotifierProvider<SketchyController, SketchyState>
    sketchyControllerProvider =
    NotifierProvider<SketchyController, SketchyState>(SketchyController.new);
