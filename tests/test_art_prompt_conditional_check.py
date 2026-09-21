"""Tests for the shared conditional-instruction detector (dream-cycle/t-028).

Both build_ruler_hooked_art_queue.py and build_dream_records.py import
conditional_instruction_violations from here rather than keeping their own
copy of the regex — this file is the contract both builders share.
"""

import scripts.art_prompt_conditional_check as apc
import scripts.build_ruler_hooked_art_queue as bruq


def test_flags_only_when():
    violations = apc.conditional_instruction_violations(
        "a hairline vein of blue light running along the fracture "
        "only when both halves touch"
    )
    assert violations
    assert "only when" in violations[0]


def test_flags_figures_appear_conditional():
    violations = apc.conditional_instruction_violations(
        "the landscape dominates the frame, when any figures appear they are "
        "small, distant, and incidental to the setting"
    )
    assert violations


def test_ordinary_prose_with_when_is_not_flagged():
    # "when" describing a scene, not a decision the model must evaluate.
    violations = apc.conditional_instruction_violations(
        "a market at dusk when people light the lanterns"
    )
    assert violations == []


def test_clean_prompt_has_no_violations():
    assert apc.conditional_instruction_violations(
        "a single crafted lantern resting on a bare stone floor"
    ) == []


def test_build_ruler_hooked_art_queue_uses_the_shared_detector():
    # build_ruler_hooked_art_queue.py imports this module by its bare (sibling)
    # name rather than as scripts.art_prompt_conditional_check, so the two
    # references are different module objects in the test process — but they
    # come from the same file and must behave identically.
    assert bruq.conditional_instruction_violations.__module__.endswith(
        "art_prompt_conditional_check"
    )
    violations = bruq.contract_violations(
        "a fish rendered only when the tide comes in"
    )
    assert any(v.startswith("conditional-instruction") for v in violations)
