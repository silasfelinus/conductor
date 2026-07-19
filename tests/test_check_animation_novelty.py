"""
Tests for check_animation_novelty.py — the advisory keyword-overlap novelty check for
animation-manager's PITCHES.yaml (conductor animation-manager t-009). No API calls.
"""

from pathlib import Path

import pytest
import yaml

import scripts.check_animation_novelty as can


def pitch(**overrides):
    base = {
        "id": "demo-pitch",
        "title": "Demo Pitch",
        "status": "pitched",
        "technique": "Canvas 2D particles",
        "surprise": "Glowing particles drift across the screen",
    }
    base.update(overrides)
    return base


# --------------------------------------------------------------------------- #
# tokenize / jaccard
# --------------------------------------------------------------------------- #

def test_tokenize_drops_stopwords_and_short_tokens():
    tokens = can.tokenize("A tiny bird flies over the wide open sea with the wind")
    assert "tiny" in tokens
    assert "flies" in tokens
    # stopwords and short words are dropped
    assert "the" not in tokens
    assert "sea" not in tokens  # len 3, below MIN_TOKEN_LEN
    assert "with" not in tokens


def test_jaccard_identical_sets_is_one():
    a = {"glow", "particle", "drift"}
    score, shared = can.jaccard(a, set(a))
    assert score == 1.0
    assert shared == a


def test_jaccard_empty_set_is_zero():
    score, shared = can.jaccard(set(), {"glow"})
    assert score == 0.0
    assert shared == set()


def test_jaccard_disjoint_sets_is_zero():
    score, _ = can.jaccard({"glow", "particle"}, {"stone", "gear"})
    assert score == 0.0


# --------------------------------------------------------------------------- #
# find_collisions
# --------------------------------------------------------------------------- #

def test_find_collisions_flags_near_duplicate_pitches():
    pitches = [
        pitch(id="firefly-glow", technique="Canvas 2D particles with additive glow",
              surprise="Glowing fireflies drift lazily across the desktop at dusk"),
        pitch(id="firefly-glow-v2", technique="Canvas 2D particles with additive glow",
              surprise="Glowing fireflies drift lazily across the desktop at night"),
        pitch(id="clockwork-garden", technique="SVG scene graph with cached shapes",
              surprise="Brass gears pollinate mechanical flowers in a quiet greenhouse"),
    ]
    collisions = can.find_collisions(pitches, threshold=0.2)
    ids = {(c.pitch_id, c.other_id) for c in collisions}
    assert ("firefly-glow", "firefly-glow-v2") in ids
    assert not any("clockwork-garden" in pair for pair in ids)


def test_find_collisions_respects_threshold():
    pitches = [
        pitch(id="a", technique="Canvas particles", surprise="Glowing dust drifts"),
        pitch(id="b", technique="WebGL shader field", surprise="Glowing dust drifts"),
    ]
    loose = can.find_collisions(pitches, threshold=0.1)
    strict = can.find_collisions(pitches, threshold=0.99)
    assert len(loose) == 1
    assert len(strict) == 0


def test_find_collisions_only_id_filters_pairs():
    pitches = [
        pitch(id="a", technique="Canvas particles glow", surprise="Dust drifts"),
        pitch(id="b", technique="Canvas particles glow", surprise="Dust drifts"),
        pitch(id="c", technique="Isometric procedural tiles", surprise="Tiny agents wander"),
    ]
    collisions = can.find_collisions(pitches, threshold=0.2, only_id="c")
    assert collisions == []
    collisions = can.find_collisions(pitches, threshold=0.2, only_id="a")
    assert len(collisions) == 1
    assert {collisions[0].pitch_id, collisions[0].other_id} == {"a", "b"}


def test_collision_missing_fields_never_collide():
    pitches = [pitch(id="a", technique="", surprise=""), pitch(id="b", technique="", surprise="")]
    assert can.find_collisions(pitches, threshold=0.01) == []


# --------------------------------------------------------------------------- #
# CLI / main
# --------------------------------------------------------------------------- #

def _write_pitches(tmp_path: Path, pitches: list[dict]) -> Path:
    path = tmp_path / "PITCHES.yaml"
    path.write_text(yaml.safe_dump({"pitches": pitches}, sort_keys=False), encoding="utf-8")
    return path


def test_main_reports_no_collisions_exit_zero(tmp_path, capsys):
    path = _write_pitches(tmp_path, [
        pitch(id="a", technique="Canvas particles", surprise="Glowing dust"),
        pitch(id="b", technique="Isometric tiles", surprise="Tiny wandering agents"),
    ])
    code = can.main(["--pitches", str(path)])
    assert code == 0
    assert "no collisions" in capsys.readouterr().out


def test_main_strict_exits_nonzero_on_collision(tmp_path):
    path = _write_pitches(tmp_path, [
        pitch(id="a", technique="Canvas particles glow", surprise="Dust drifts slowly"),
        pitch(id="b", technique="Canvas particles glow", surprise="Dust drifts slowly"),
    ])
    assert can.main(["--pitches", str(path), "--strict"]) == 1
    # same data, non-strict is advisory only
    assert can.main(["--pitches", str(path)]) == 0


def test_main_unknown_pitch_id_errors(tmp_path):
    path = _write_pitches(tmp_path, [pitch(id="a")])
    assert can.main(["--pitches", str(path), "--pitch", "does-not-exist"]) == 2


def test_main_json_output_is_parseable(tmp_path, capsys):
    import json

    path = _write_pitches(tmp_path, [
        pitch(id="a", technique="Canvas particles glow", surprise="Dust drifts slowly"),
        pitch(id="b", technique="Canvas particles glow", surprise="Dust drifts slowly"),
    ])
    can.main(["--pitches", str(path), "--json"])
    payload = json.loads(capsys.readouterr().out)
    assert len(payload) == 1
    assert payload[0]["pitch"] == "a"
    assert payload[0]["collides_with"] == "b"


def test_real_pitches_file_parses_and_has_no_high_collisions():
    """Guards against the real PITCHES.yaml regressing into unparseable YAML again
    (a colon inside an unquoted scalar broke this file once — see conductor/t-009)."""
    real = Path(__file__).resolve().parent.parent / "projects" / "animation-manager" / "PITCHES.yaml"
    pitches = can.load_pitches(real)
    assert len(pitches) >= 1
    collisions = can.find_collisions(pitches, threshold=0.5)
    assert collisions == [], f"unexpectedly high-overlap pitches: {[c.as_dict() for c in collisions]}"
