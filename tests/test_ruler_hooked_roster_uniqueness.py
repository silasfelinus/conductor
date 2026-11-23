"""Duplicate roster IDs must fail before art queue generation silently drops rows."""

import pytest

from scripts import build_ruler_hooked_art_queue as queue


def test_duplicate_cast_ids_name_the_offender():
    entries = [{"slug": "quill"}, {"slug": "quill"}]
    block = "    slug: 'quill'\n    slug: 'quill'\n"
    with pytest.raises(SystemExit, match="characters: duplicate ids: quill"):
        queue.expect_all(entries, block, "characters", "fixture")


def test_duplicate_fish_and_quest_ids_are_named():
    with pytest.raises(SystemExit, match="fish: duplicate ids: koi"):
        queue.assert_unique_ids(["koi", "trout", "koi"], "fish")
    with pytest.raises(SystemExit, match="quests: duplicate ids: moat"):
        queue.assert_unique_ids(["moat", "moat"], "quests")


def test_duplicate_region_keys_are_not_overwritten(tmp_path):
    content = tmp_path / "content.ts"
    content.write_text(
        "\n  regions: {\n    regions: {\n"
        "      lake: { states: ['clear'], times: ['day'] },\n"
        "      lake: { states: ['murky'], times: ['night'] },\n"
        "    },\n",
        encoding="utf-8",
    )
    with pytest.raises(SystemExit, match="regions: duplicate ids: lake"):
        queue.read_regions(content)


def test_duplicate_cards_within_deck_are_not_silently_deduplicated(tmp_path):
    content = tmp_path / "content.ts"
    card = (
        "    { id: 'royal-weir',\n"
        "      title: 'The Weir',\n"
        "      body: 'A petition arrives.', },\n"
    )
    content.write_text(
        "\n  decks: [\n" + card + card + "  ],\n"
        "  arcs: [\n" + card + "  ],\n",
        encoding="utf-8",
    )
    with pytest.raises(SystemExit, match="decks: duplicate ids: royal-weir"):
        queue.read_cards(content)


def test_cross_deck_card_reference_remains_legal(tmp_path):
    content = tmp_path / "content.ts"
    card = (
        "    { id: 'royal-weir',\n"
        "      title: 'The Weir',\n"
        "      body: 'A petition arrives.', },\n"
    )
    content.write_text(
        "\n  decks: [\n" + card + "  ],\n"
        "  arcs: [\n" + card + "  ],\n",
        encoding="utf-8",
    )
    assert [entry["id"] for entry in queue.read_cards(content)] == ["royal-weir"]
