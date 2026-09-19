"""The repair must remove the exclusion without damaging the picture.

Every fixture here is a real stored prompt from kindrobots.org on 2026-09-19.
"""
import importlib.util
import re
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
spec = importlib.util.spec_from_file_location(
    "repair_negation_art_prompts", ROOT / "scripts" / "repair_negation_art_prompts.py"
)
rn = importlib.util.module_from_spec(spec)
sys.modules["repair_negation_art_prompts"] = rn
spec.loader.exec_module(rn)


# Reward 393. The one Silas sent a screenshot of: a ring on a leaf, rendered
# as a crowd of Victorian faces, because the prompt ends "No figure."
RING = (
    "A simple glowing ring resting on a leaf, faint sound-ripples of animal speech "
    "emanating from it, a curious bird and beetle leaning in. No figure. Warm "
    "gold-and-green glow, crisp clean linework, gentle and wondrous, simple background."
)

# Reward 2954. Carries the 2026-08-08 repair clause, which is itself a cast list.
FOGTAP_TAIL = (
    "close enough to read material and wear, an unpeopled frame, the subject stands "
    "alone with no bystanders, no onlookers, and no crowd, rendered with the reverence "
    "given a rare artifact, unmarked surfaces, free of text"
)

# The tail artAssetSuggest.ts used to order onto every suggested prompt.
PENNY_TAIL = (
    "The overall mood is inviting and serene. no readable text, no logo, no watermark, "
    "no collage."
)


def test_ring_loses_the_negation_and_keeps_the_ring():
    fixed = rn.repair(RING)
    assert "No figure" not in fixed
    assert "glowing ring resting on a leaf" in fixed
    assert "a curious bird and beetle leaning in" in fixed
    assert "crisp clean linework" in fixed
    # The intent the negation was carrying survives, stated positively.
    assert "unpeopled" in fixed
    assert not rn.violations(fixed)


def test_the_2026_08_08_repair_clause_is_itself_repaired():
    fixed = rn.repair(FOGTAP_TAIL)
    for named in ("bystanders", "onlookers", "crowd"):
        assert named not in fixed, f"{named!r} survived the repair"
    # "unpeopled" was the half that worked; it stays, and the dangling "with"
    # the removed object left behind does not.
    assert "an unpeopled frame, the subject stands alone," in fixed
    assert "alone with," not in fixed
    assert "rendered with the reverence given a rare artifact" in fixed
    assert not rn.violations(fixed)


def test_the_suggested_exclusion_tail_goes_and_the_mood_stays():
    fixed = rn.repair(PENNY_TAIL)
    for named in ("readable text", "logo", "watermark", "collage"):
        assert named not in fixed
    assert "inviting and serene" in fixed
    assert not rn.violations(fixed)


def test_prose_that_merely_contains_a_people_word_is_untouched():
    """A crowd IN the picture is not a crowd EXCLUDED from it.

    Reward 2953's subject is literally "a single face in a crowd of matching
    ones". Only a negation makes a people noun this script's business.
    """
    prompt = (
        "Their eyes track slightly ahead of their head, already following the one true "
        "angle of reflection off a single face in a crowd of matching ones"
    )
    assert not rn.violations(prompt)
    assert rn.repair(prompt) == prompt


def test_a_clock_with_no_hands_is_a_subject_not_a_casting_note():
    """Mirrors the nouns artPromptContract.ts deliberately leaves out."""
    prompt = "a brass station clock with no hands, one object alone in frame"
    assert "people-negation" not in rn.violations(prompt)


def test_every_repair_comes_out_clean_under_its_own_detectors():
    for prompt in (RING, FOGTAP_TAIL, PENNY_TAIL):
        assert rn.violations(prompt), f"fixture is supposed to be dirty: {prompt[:60]}"
        assert not rn.violations(rn.repair(prompt))


def test_repair_never_leaves_punctuation_debris():
    for prompt in (RING, FOGTAP_TAIL, PENNY_TAIL):
        fixed = rn.repair(prompt)
        assert not re.search(r",\s*,|\.\s*,|,\s*\.|\s,|\s\.", fixed), fixed
        assert not fixed.startswith((",", ".", ";"))
        assert fixed == fixed.strip()
