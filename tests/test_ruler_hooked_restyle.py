"""ruler-hooked/t-054: Chronicle + Broadside house styles, decay states, --restage."""
import sys

import pytest
import yaml

import scripts.build_ruler_hooked_art_queue as bruq


# --- house styles ----------------------------------------------------------


def test_rainbow_tiers_differ_and_name_the_decay():
    pristine = bruq.rainbow_style("pristine")
    rotten = bruq.rainbow_style("rotten")
    assert "radiant" in pristine and "toxic" not in pristine
    assert "toxic rainbow corruption" in rotten
    assert "acid lime" in bruq.rainbow_style("strained")


def test_layer_variant_is_borderless():
    for tier in bruq.TIERS:
        layer = bruq.rainbow_style(tier, "layer")
        assert "border" not in layer and "river-ribbon" not in layer
        assert "all four edges" in layer
        assert "river-ribbon" in bruq.rainbow_style(tier, "bordered")


def test_scenery_variants_carry_no_figure_clause():
    # Pilot ArtJobs 64361/64363: the figure clause paraded courtiers across layers.
    for tier in bruq.TIERS:
        assert bruq.RAINBOW_FIGURES not in bruq.rainbow_style(tier, "layer")
        assert bruq.RAINBOW_FIGURES not in bruq.rainbow_style(tier, "specimen")
        assert bruq.RAINBOW_FIGURES in bruq.rainbow_style(tier, "bordered")


def test_unknown_tier_is_an_error():
    with pytest.raises(AssertionError):
        bruq.rainbow_style("cheerful")


def test_antique_and_cartoon_tails_are_gone():
    assert not hasattr(bruq, "STYLE_TAIL")
    for clause in (bruq.SPECTRUM_PRINT, *(bruq.rainbow_style(t) for t in bruq.TIERS)):
        for word in ("cartoon", "goofy", "charming", "storybook", "medieval", "woodcut", "manuscript", "sepia"):
            assert word not in clause


def test_region_bases_drop_comic_tone_words():
    for key, base in bruq.REGION_BASE.items():
        for word in ("goofy", "cheerful", "endearing", "comical", "charming", "friendly"):
            assert word not in base.lower(), (key, word)


# --- decay states ----------------------------------------------------------


def _manifest():
    return {
        "sky": {"states": ["open"], "times": ["day"]},
        "far_shore": {"states": ["pristine"], "times": ["day", "night"]},
        "village_edge": {"states": ["hamlet"], "times": ["day"]},
        "lake": {"states": ["clear"], "times": ["day"]},
        "near_bank": {"states": ["grassy"], "times": []},
    }


def test_fallback_states_merge_without_duplicates():
    merged = bruq.merge_extra_states(_manifest())
    assert merged["lake"]["states"] == ["clear", "poisoned", "murky"]
    assert merged["near_bank"]["states"] == ["grassy", "dead", "trampled"]
    assert merged["sky"]["states"] == ["open", "choked", "overcast"]
    assert "gallows" in merged["far_shore"]["states"]
    assert "garrisoned" in merged["village_edge"]["states"]
    again = bruq.merge_extra_states(merged)
    assert again["lake"]["states"].count("poisoned") == 1


def test_every_state_has_a_base_and_a_tier():
    merged = bruq.merge_extra_states(_manifest())
    entries = bruq.layer_entries(merged)
    ids = {e["id"] for e in entries}
    assert "ruler-hooked-layer-lake-poisoned-day" in ids
    assert "ruler-hooked-layer-near_bank-dead" in ids
    assert "ruler-hooked-layer-far_shore-gallows-night" in ids
    poisoned = next(e for e in entries if e["id"] == "ruler-hooked-layer-lake-poisoned-day")
    assert "rainbow oil sheen" in poisoned["prompt"]
    assert "fluorescent toxic green pools" in poisoned["prompt"]
    assert "marginalia" not in poisoned["prompt"]
    assert set(bruq.REGION_BASE) == set(bruq.REGION_TIER)


# --- card copy -------------------------------------------------------------


def test_card_scene_drops_quoted_dialogue_whole():
    body = (
        "Vex sets a scale model on your tackle box. “Everyone deserves a lake "
        "view,” he says. “At a reasonable rate.” The water glints."
    )
    assert bruq.card_scene(body) == "Vex sets a scale model on your tackle box. The water glints."


# --- restage ---------------------------------------------------------------


HEADER = "# curated header\nimages: []\nrequests:\n"


def _row(rid, prompt, **extra):
    row = {"id": rid, "source": "ruler-hooked", "status": "done", "prompt": prompt}
    row.update(extra)
    return row


def test_replace_rows_rewrites_in_place_and_keeps_neighbours():
    text = HEADER + bruq.render_block(
        [
            _row("other", "keep me"),
            _row("ruler-hooked-x", "old prompt", last_art_job_id=123),
            _row("tail", "keep me too"),
        ]
    )
    new = bruq.forced(
        {"id": "ruler-hooked-x", "source": "ruler-hooked", "status": "pending", "prompt": "new"},
        123,
    )
    out = bruq.replace_rows(text, [new])
    assert out.startswith("# curated header\n")
    rows = {r["id"]: r for r in yaml.safe_load(out)["requests"]}
    assert list(rows) == ["other", "ruler-hooked-x", "tail"]
    x = rows["ruler-hooked-x"]
    assert x["prompt"] == "new" and x["status"] == "pending" and x["force"] is True
    assert x["superseded_art_job_id"] == 123 and "last_art_job_id" not in x
    assert rows["other"]["prompt"] == "keep me" and rows["tail"]["prompt"] == "keep me too"
    assert out.count("id: ruler-hooked-x") == 1


def test_stale_rows_compares_normalized_prompt():
    entries = [{"id": "a", "prompt": "one two"}, {"id": "b", "prompt": "new"}]
    rows = {"a": {"prompt": "one\n  two"}, "b": {"prompt": "old"}}
    assert [e["id"] for e in bruq.stale_rows(entries, rows)] == ["b"]


@pytest.fixture
def staged(monkeypatch, tmp_path):
    built = [
        {"id": "ruler-hooked-card-a", "lane": "card", "size": "1x1", "status": "pending",
         "prompt": "fresh a"},
        {"id": "ruler-hooked-card-b", "lane": "card", "size": "1x1", "status": "pending",
         "prompt": "fresh b"},
    ]
    monkeypatch.setattr(bruq, "find_content_bundle", lambda: tmp_path / "content.ts")
    monkeypatch.setattr(bruq, "read_cast", lambda ts: None)
    monkeypatch.setattr(bruq, "concept_entries", lambda cast: [])
    monkeypatch.setattr(bruq, "ruler_entries", lambda: [])
    monkeypatch.setattr(bruq, "fish_entries", lambda: [])
    monkeypatch.setattr(bruq, "reward_entries", lambda ts: [])
    monkeypatch.setattr(bruq, "ending_entries", lambda ts: [])
    monkeypatch.setattr(bruq, "card_entries", lambda ts: [dict(e) for e in built])
    monkeypatch.setattr(bruq, "console_entries", lambda cast: [])
    monkeypatch.setattr(bruq, "assert_contract", lambda entries: None)
    art = tmp_path / "art-prompts.yaml"
    art.write_text(
        HEADER + bruq.render_block([_row("ruler-hooked-card-a", "old a", last_art_job_id=9)]),
        encoding="utf-8",
    )
    monkeypatch.setattr(bruq, "ART_PROMPTS", art)
    monkeypatch.setattr(bruq, "REPO", tmp_path)
    return art


def _main(monkeypatch, *argv):
    monkeypatch.setattr(sys, "argv", ["build_ruler_hooked_art_queue.py", *argv])
    return bruq.main()


def test_check_fails_on_a_stale_prompt(staged, monkeypatch):
    assert _main(monkeypatch, "--check") == 1


def test_write_without_restage_leaves_stale_rows(staged, monkeypatch):
    assert _main(monkeypatch, "--write") == 0
    rows = {r["id"]: r for r in yaml.safe_load(staged.read_text())["requests"]}
    assert rows["ruler-hooked-card-a"]["prompt"] == "old a"
    assert "force" not in rows["ruler-hooked-card-b"]


def test_write_restage_forces_every_row_then_check_passes(staged, monkeypatch):
    assert _main(monkeypatch, "--write", "--restage") == 0
    rows = {r["id"]: r for r in yaml.safe_load(staged.read_text())["requests"]}
    a, b = rows["ruler-hooked-card-a"], rows["ruler-hooked-card-b"]
    assert a["prompt"] == "fresh a" and a["force"] is True and a["status"] == "pending"
    assert a["superseded_art_job_id"] == 9 and "last_art_job_id" not in a
    assert b["prompt"] == "fresh b" and b["force"] is True
    assert staged.read_text().startswith("# curated header\n")
    assert _main(monkeypatch, "--check") == 0
