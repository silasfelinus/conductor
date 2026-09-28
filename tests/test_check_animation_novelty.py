"""
Tests for check_animation_novelty.py — the advisory keyword-overlap novelty check for
animation-manager's PITCHES.yaml (conductor animation-manager t-009). No API calls.
"""

import json
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


# --------------------------------------------------------------------------- #
# --check-catalog (animation-manager t-024)
# --------------------------------------------------------------------------- #

SAMPLE_CATALOG_SOURCE = """
export const ANIMATION_EFFECTS = [
  {
    id: 'kaleidoscope-effect',
    label: 'Kaleidoscope',
    reveal: 'Symmetry',
    icon: 'kind-icon:sparkle',
    tooltip: 'Sacred geometry in motion 🔮',
    color: '#000000',
    generationSafe: true,
  },
  {
    id: 'starfield-effect',
    label: 'Warp Drive',
    reveal: 'Hyperspace!',
    icon: 'kind-icon:star',
    tooltip: "Punch it, it's warp speed ✨",
    color: '#111111',
    generationSafe: true,
  },
] as const satisfies AnimationEffectDefinition[]
"""


def test_overlap_coefficient_uses_smaller_side_as_denominator():
    # Both sides have 4 tokens here (unlike Jaccard, size alone isn't the point --
    # the point is dividing by the *smaller* side, which this keeps simple to assert).
    long_pitch_tokens = {"kaleidoscope", "bloom", "dihedral", "radial"}
    short_catalog_tokens = {"kaleidoscope", "sacred", "geometry", "motion"}
    score, shared = can.overlap_coefficient(long_pitch_tokens, short_catalog_tokens)
    assert score == pytest.approx(0.25)
    assert shared == {"kaleidoscope"}


def test_overlap_coefficient_empty_side_is_zero():
    assert can.overlap_coefficient(set(), {"a"}) == (0.0, set())


def test_parse_catalog_entries_reads_both_quote_styles():
    entries = can.parse_catalog_entries(SAMPLE_CATALOG_SOURCE)
    by_id = {e["id"]: e for e in entries}
    assert set(by_id) == {"kaleidoscope-effect", "starfield-effect"}
    assert by_id["kaleidoscope-effect"]["label"] == "Kaleidoscope"
    assert by_id["kaleidoscope-effect"]["tooltip"] == "Sacred geometry in motion 🔮"
    # double-quoted tooltip (containing an apostrophe) parses too
    assert by_id["starfield-effect"]["tooltip"] == "Punch it, it's warp speed ✨"


def test_parse_catalog_entries_missing_array_raises():
    with pytest.raises(ValueError):
        can.parse_catalog_entries("export const SOMETHING_ELSE = []")


def test_find_catalog_collisions_catches_title_match_technique_prose_misses():
    """Regression for the actual incident this check exists for: kaleidoscope-bloom's
    technique/surprise text never says "kaleidoscope", so `pitch_signature` +
    `jaccard` (the PITCHES-internal check) cannot catch the collision -- only a
    title/novelty vs. label/tooltip comparison can."""
    bloom = pitch(
        id="kaleidoscope-bloom",
        title="Kaleidoscope Bloom",
        technique="Canvas 2D offscreen wedge buffer composited via rotate/mirror transforms",
        surprise="Jewel-toned shard clusters bloom outward in perfect radial symmetry",
        novelty="No existing pitch renders through geometric symmetry compositing.",
    )
    entries = can.parse_catalog_entries(SAMPLE_CATALOG_SOURCE)

    # The PITCHES-internal signature (technique+surprise) genuinely misses it.
    assert "kaleidoscope" not in can.pitch_signature(bloom)

    collisions = can.find_catalog_collisions([bloom], entries, threshold=0.2)
    assert len(collisions) == 1
    assert collisions[0].pitch_id == "kaleidoscope-bloom"
    assert collisions[0].other_id == "catalog:kaleidoscope-effect"
    assert "kaleidoscope" in collisions[0].shared


def test_find_catalog_collisions_only_id_filters():
    a = pitch(id="a", title="Kaleidoscope Thing", novelty="")
    b = pitch(id="b", title="Unrelated Thing", novelty="")
    entries = can.parse_catalog_entries(SAMPLE_CATALOG_SOURCE)
    collisions = can.find_catalog_collisions([a, b], entries, threshold=0.2, only_id="b")
    assert collisions == []


def test_main_check_catalog_without_token_exits_2(tmp_path, monkeypatch):
    monkeypatch.delenv("GITHUB_TOKEN", raising=False)
    monkeypatch.delenv("GH_TOKEN", raising=False)
    path = _write_pitches(tmp_path, [pitch(id="a")])
    assert can.main(["--pitches", str(path), "--check-catalog"]) == 2


def test_main_check_catalog_reports_collisions_in_json(tmp_path, monkeypatch, capsys):
    monkeypatch.setenv("GITHUB_TOKEN", "fake-token-for-test")
    monkeypatch.setattr(
        can, "fetch_kind_robots_catalog_source", lambda ref, token: (SAMPLE_CATALOG_SOURCE, None)
    )
    path = _write_pitches(tmp_path, [
        pitch(id="kaleidoscope-bloom", title="Kaleidoscope Bloom", novelty="A dihedral bloom effect."),
    ])
    code = can.main(["--pitches", str(path), "--check-catalog", "--json"])
    assert code == 0
    payload = json.loads(capsys.readouterr().out)
    assert isinstance(payload, dict)
    assert payload["catalog_error"] is None
    assert any(c["collides_with"] == "catalog:kaleidoscope-effect" for c in payload["catalog_collisions"])


def test_main_check_catalog_fetch_failure_exits_2(tmp_path, monkeypatch):
    monkeypatch.setenv("GITHUB_TOKEN", "fake-token-for-test")
    monkeypatch.setattr(
        can, "fetch_kind_robots_catalog_source", lambda ref, token: (None, "HTTP 404 fetching stores/animationCatalog.ts")
    )
    path = _write_pitches(tmp_path, [pitch(id="a")])
    assert can.main(["--pitches", str(path), "--check-catalog"]) == 2


def test_main_without_check_catalog_json_is_still_a_plain_list(tmp_path, capsys):
    """--json's default shape must not change for callers that don't pass
    --check-catalog (regression guard alongside test_main_json_output_is_parseable)."""
    path = _write_pitches(tmp_path, [
        pitch(id="a", technique="Canvas particles glow", surprise="Dust drifts slowly"),
        pitch(id="b", technique="Canvas particles glow", surprise="Dust drifts slowly"),
    ])
    can.main(["--pitches", str(path), "--json"])
    payload = json.loads(capsys.readouterr().out)
    assert isinstance(payload, list)
