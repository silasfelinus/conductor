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


# Reward 2742 and 17 others. "2:3 portrait card composition" is framing language
# to a person and a trading CARD to a caption-conditioned model.
CARD_FRAMED = (
    "Tide Telemetry, a hull's stress lines rendered as luminous starchart "
    "constellations, 2:3 portrait card composition, museum-like object study"
)

# Reward 249. A wanted poster is what is IN the picture, not the artefact the
# picture is printed on.
WANTED_POSTER = (
    "A wanted-poster-style emblem glowing with notoriety, gritty noir tones with "
    "one hot accent, crisp bold linework, dangerous prestige, simple background."
)

# Resource 3461. LoRA trigger text, where the format IS the concept.
LORA_TRIGGER = "Movie Poster page"


def test_card_composition_keeps_the_geometry_and_drops_the_card():
    assert "format-vocabulary" in rn.violations(CARD_FRAMED)
    fixed = rn.repair(CARD_FRAMED)
    assert "card composition" not in fixed.lower()
    assert "vertical 2:3 portrait composition" in fixed
    assert "luminous starchart constellations" in fixed
    assert not rn.violations(fixed)


def test_a_format_noun_that_is_the_subject_is_left_alone():
    """A poster IN the frame is not a request to render a poster.

    No regex separates "the artefact this image is printed on" from "the thing
    this image is of", so the rule is pinned to the one phrasing with rendered
    evidence behind it. Rewriting these would delete the subject.
    """
    for prompt in (WANTED_POSTER, LORA_TRIGGER):
        assert not rn.violations(prompt)
        assert rn.repair(prompt) == prompt


# ── The families the 2026-09-19 pass left behind ────────────────────────────
#
# All five fixtures below are the real stored text on 2026-09-20, taken from
# the records the live contract refused when the outstanding 408 re-renders
# were queued. Each one is a family the repair script had no rule for, so the
# audit read "Violating: 0" while the enqueue endpoint answered 422.

# Reward 2835 and six others. CARD_COMPOSITION rewrote the framing at the front
# and left the card as an OBJECT further down, so all seven stayed rejected.
TIER_CARD = (
    "Thorn-Tide Boarding, a field of thorned singing coral parting around an "
    "invisible passage, 2:3 portrait card composition, tight centered composition "
    "on the effect, uncommon-tier ability card illustration, glowing volumetric "
    "light emanating from the effect itself"
)

# Dream 5262, 5481, 5636. Rule 4's shape exactly: a logline-only prompt where
# the boilerplate clause IS most of the prompt.
BRAND_STYLE = (
    "establishing key art for The Lucky Ladle: Every bowl tastes like a fate "
    "someone else was supposed to have. cohesive Kind Robots visual style, "
    "cinematic light with intent, every surface bare and unmarked"
)

# Reward 424. A negation opening a parenthetical: "(" is not ^, a separator, or
# whitespace, so no clause anchor could reach it.
PARENTHETICAL_PEOPLE = (
    "A glossy vintage comic book displayed reverently, bold retro cover-art "
    "energy (no specific copyrighted character — just classic comic styling), "
    "protective sleeve gleaming."
)

# Reward 249, the text half of the same blind spot.
PARENTHETICAL_TEXT = (
    "A wanted-poster-style emblem glowing with notoriety, a name implied in "
    "dramatic lettering-shapes (no readable text), surrounded by both reaching "
    "helpful hands and lurking threats."
)

# Resource 3590 "detailed_notrigger". Catalog bookkeeping, not a picture.
LORA_NO_TRIGGER = "extremely detailed (no trigger) - sliders.ntcai.xyz"


def test_the_card_as_an_object_goes_even_though_the_framing_was_substituted():
    assert "format-vocabulary" in rn.violations(TIER_CARD)
    fixed = rn.repair(TIER_CARD)
    assert "ability card" not in fixed.lower()
    assert "uncommon-tier" not in fixed.lower()
    # The geometry the framing rule preserves is still preserved.
    assert "vertical 2:3 portrait composition" in fixed
    # And the picture survives both removals.
    assert "thorned singing coral" in fixed
    assert "glowing volumetric light" in fixed
    assert not rn.violations(fixed)


def test_brand_style_becomes_medium_linework_colour_and_surface():
    assert "vague-brand-style" in rn.violations(BRAND_STYLE)
    fixed = rn.repair(BRAND_STYLE)
    assert "kind robots" not in fixed.lower()
    for word in ("illustration", "linework", "color", "texture"):
        assert word in fixed.lower()
    assert "The Lucky Ladle" in fixed
    assert not rn.violations(fixed)


def test_a_negation_in_brackets_is_still_a_negation():
    assert "negated-parenthetical" in rn.violations(PARENTHETICAL_PEOPLE)
    fixed = rn.repair(PARENTHETICAL_PEOPLE)
    assert "copyrighted character" not in fixed
    # The half after the dash is real direction and is kept.
    assert "classic comic styling" in fixed
    assert "vintage comic book" in fixed
    assert "(" not in fixed and ")" not in fixed
    assert not rn.violations(fixed)


def test_a_bracketed_text_exclusion_goes_without_taking_its_sentence():
    assert "negated-parenthetical" in rn.violations(PARENTHETICAL_TEXT)
    fixed = rn.repair(PARENTHETICAL_TEXT)
    assert "no readable text" not in fixed.lower()
    assert "dramatic lettering-shapes" in fixed
    assert "reaching helpful hands" in fixed
    assert ", ," not in fixed and " ," not in fixed


def test_lora_metadata_is_not_prose_and_is_left_alone():
    """"(no trigger)" names the row, it does not describe a frame.

    Deleting it would assert the opposite of what the LoRA's own name
    ("detailed_notrigger") says. Same carve-out the "Movie Poster page" rows
    get from the format rules.
    """
    assert not rn.violations(LORA_NO_TRIGGER, "resource")
    assert rn.repair(LORA_NO_TRIGGER, "resource") == LORA_NO_TRIGGER


def test_every_new_family_comes_out_as_readable_prose():
    """Rule 5's lesson: a rule that passes its own gate can still leave debris.

    The point of the repair is a prompt a person would read as sentences, so
    assert the shape rather than only the absence of the banned words.
    """
    for prompt in (TIER_CARD, BRAND_STYLE, PARENTHETICAL_PEOPLE, PARENTHETICAL_TEXT):
        fixed = rn.repair(prompt)
        assert fixed
        assert fixed == fixed.strip()
        assert not re.search(r"[,;]\s*[,;.]", fixed)
        assert not re.search(r"\b(?:with|and|or)\s*[,.;]", fixed)
        assert "  " not in fixed


# ── The conditional family (2026-09-20) ─────────────────────────────────────
#
# Rule 1's other half, and the one the gate could never see. 103 dream prompts
# said "any figures present are small and incidental, included only for scale".
# That is a conditional -- Krea can no more evaluate "present" than it can
# evaluate "no" -- but artPromptContract's CONDITIONAL_PATTERNS anchors on a
# LEADING when/if/unless, and this phrasing has no conditional word in front of
# it. So 101 of the 103 passed every check while handing the model a decision.

SCALE_FIGURES = (
    "architectural establishing shot, the environment is the subject and any figures "
    "present are small and incidental, included only for scale, cinematic photorealism"
)

SETTING_IS_SUBJECT = (
    "wide key art, the setting is the subject; any figures present are incidental to "
    "the place, and deep atmospheric background"
)

# Lore the daily-dream producer concatenated into the caption, carrying its own
# conditional. Dream 5755 and Reward 2934 -- sentences written for a reader.
LORE_ORCHARD = (
    "A long green basin where a migrating orchard settles only when the cassowary "
    "flock chooses to scratch, nest, and scatter seed among the exposed root-mounds"
)
LORE_STONE = (
    "A palm-sized grey stone split cleanly in half, a hairline vein of blue light "
    "running along the fracture only when both halves touch"
)


def test_figures_for_scale_becomes_a_fact_about_the_frame():
    assert "conditional-instruction" in rn.violations(SCALE_FIGURES)
    fixed = rn.repair(SCALE_FIGURES)
    assert "any figures present" not in fixed.lower()
    assert "only for scale" not in fixed.lower()
    # The intent survives: a wide landscape usually DOES want distant figures.
    assert "distant figures" in fixed
    assert "cinematic photorealism" in fixed
    assert not rn.violations(fixed)


def test_the_longer_setting_phrasing_is_caught_too():
    assert "conditional-instruction" in rn.violations(SETTING_IS_SUBJECT)
    fixed = rn.repair(SETTING_IS_SUBJECT)
    assert "any figures present" not in fixed.lower()
    assert "deep atmospheric background" in fixed
    assert not rn.violations(fixed)


def test_lore_conditionals_keep_both_halves_of_the_picture():
    """"X only when Y" becomes "X as Y".

    Only the joint is rewritten. Both sides are real visual information --
    an orchard uprooting, a flock walking beside it; a split stone, a vein of
    light -- and deleting either would lose half the image.
    """
    orchard = rn.repair(LORE_ORCHARD)
    assert "only when" not in orchard.lower()
    assert "migrating orchard settles as the cassowary flock chooses" in orchard
    assert "root-mounds" in orchard

    stone = rn.repair(LORE_STONE)
    assert "only when" not in stone.lower()
    assert "vein of blue light" in stone and "both halves touch" in stone
    for fixed in (orchard, stone):
        assert not rn.violations(fixed)


def test_an_ordinary_when_is_not_a_conditional():
    """The rule is pinned to the "only when/only if" joint, not to "when".

    "a market at dusk when the lanterns are lit" describes a scene. Rewriting
    every "when" in the catalog would flatten ordinary prose.
    """
    scene = "a market at dusk when the lanterns are lit, warm crowded stalls"
    assert "conditional-instruction" not in rn.violations(scene)
    assert rn.repair(scene) == scene


def test_new_repair_directions_do_not_introduce_frame_objects():
    for prompt in (RING, PENNY_TAIL, SCALE_FIGURES, SETTING_IS_SUBJECT):
        fixed = rn.repair(prompt)
        assert not re.search(r"\b(?:frame|picture)\b", fixed, re.I), fixed
