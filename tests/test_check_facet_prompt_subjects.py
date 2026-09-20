"""Tests for scripts/check_facet_prompt_subjects.py. Pure prompt analysis, no network."""

import scripts.check_facet_prompt_subjects as check


def facet(**kwargs):
    row = {
        "id": 1,
        "title": "Octopus",
        "taxonomy": "ANIMAL",
        "description": None,
        "artPrompt": None,
        "imagePath": "/images/facets/octopus.webp",
    }
    row.update(kwargs)
    return row


CREATURE_CLAUSE = (
    "Show one unmistakable full creature with recognizable anatomy, personality, "
    "and habitat cues."
)
PERSON_CLAUSE = "Use a character-centered visual metaphor with a clear emotional read."


def test_generated_prompt_without_its_own_title_is_no_subject():
    """The exact live shape of facet/290. Krea painted the caption, not an octopus."""
    finding = check.inspect(
        facet(
            description="Three hearts, nine brains, infinite arms.",
            artPrompt=f"Three hearts, nine brains, infinite arms. {CREATURE_CLAUSE}",
        )
    )
    assert finding is not None
    assert finding["finding"] == "no-subject"


def test_generated_prompt_that_names_its_title_is_clean():
    assert (
        check.inspect(facet(artPrompt=f"Octopus. {CREATURE_CLAUSE}")) is None
    )


def test_hand_authored_scene_without_the_title_is_never_flagged():
    """
    The correct house style. "Batch-Made" is not a drawable noun and the prompt
    is right to not repeat it -- only a PRODUCER clause turns a missing title
    into a finding.
    """
    assert (
        check.inspect(
            facet(
                id=2411,
                title="Batch-Made",
                taxonomy="BACKSTORY",
                artPrompt=(
                    "A row of identical blank-eyed figures on a conveyor line, all "
                    "facing the same direction except one whose head has turned to "
                    "look back at the camera."
                ),
            )
        )
        is None
    )


def test_app_wrapper_outranks_a_named_subject():
    finding = check.inspect(
        facet(
            id=1771,
            title="Magic",
            taxonomy="REWARD_TYPE",
            artPrompt=(
                "Magic. A spell, charm, blessing, hex. Kind Robots premium Builder "
                "illustration for Reward Types: Magic."
            ),
        )
    )
    assert finding is not None
    assert finding["finding"] == "app-wrapper"


def test_bot_type_card_wrapper_is_flagged():
    finding = check.inspect(
        facet(
            id=1704,
            title="Assistant",
            taxonomy="BOT_TYPE",
            artPrompt=(
                "Assistant. Illustrated Bot Type card for a dependable "
                "general-purpose bot, warm rounded chassis."
            ),
        )
    )
    assert finding is not None
    assert finding["finding"] == "app-wrapper"


def test_a_real_card_in_a_scene_is_not_a_wrapper():
    assert (
        check.inspect(
            facet(
                id=2347,
                title="North Sea Rig Town",
                taxonomy="ORIGIN",
                artPrompt=(
                    "A high-visibility jacket faded to chalk, steel-toed boots, a "
                    "laminated shift card still clipped to the chest."
                ),
            )
        )
        is None
    )


def test_card_copy_is_reported_below_the_blocking_findings():
    """
    Title IS the description here, so the title test passes and the prompt is
    still the joke pasted whole. Reported, but it never decides the exit code.
    """
    finding = check.inspect(
        facet(
            id=1240,
            title="Believes they're being followed by an invisible duck.",
            taxonomy="QUIRK",
            description=(
                "Believes they're being followed by an invisible duck. Sets out a "
                "small bowl of water most evenings, just in case."
            ),
            artPrompt=(
                "Believes they're being followed by an invisible duck. Sets out a "
                f"small bowl of water most evenings, just in case. {PERSON_CLAUSE}"
            ),
        )
    )
    assert finding is not None
    assert finding["finding"] == "card-copy"


def test_curly_quotes_do_not_hide_a_matching_title():
    """
    The catalog stores curly apostrophes in titles and straight ones in some
    prompts. A naive compare reads them as different text and reports a
    no-subject finding for a prompt that does name its subject.
    """
    assert (
        check.inspect(
            facet(
                id=1240,
                title="Believes they\u2019re being followed by an invisible duck.",
                artPrompt=(
                    "Believes they're being followed by an invisible duck. "
                    f"{PERSON_CLAUSE}"
                ),
            )
        )
        is None
    )


def test_a_repair_truncated_tail_still_counts_as_generated():
    """
    Conductor's own repair strips "unmistakable silhouette, workplace cues" out
    of a registered v4 tail. The fragment left behind is what de-registered 128
    Facets in kind_robots -- this check has to keep seeing it as producer text.
    """
    finding = check.inspect(
        facet(
            id=947,
            title="Public Notary",
            taxonomy="OCCUPATION",
            artPrompt="An old brass stamp. Single distinctive figure in action, readable tools",
        )
    )
    assert finding is not None
    assert finding["finding"] == "no-subject"


def test_empty_prompt_is_not_a_finding():
    assert check.inspect(facet(artPrompt=None)) is None
    assert check.inspect(facet(artPrompt="   ")) is None
