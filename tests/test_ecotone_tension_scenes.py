"""Structural authoring checks for Ecotone's four ideological tension scenes."""

from pathlib import Path
import re

DOCUMENT = (
    Path(__file__).resolve().parents[1]
    / "projects"
    / "weird-humboldt"
    / "IDEOLOGICAL-TENSION-SCENES.md"
)
SCENES = {
    "TEN-AS": "autonomy-solidarity",
    "TEN-CR": "continuity-reinvention",
    "TEN-EE": "ecology-engineering",
    "TEN-AF": "agency-fate",
}
OPENINGS = ("sober", "tipsy", "stoned", "tripping_balls", "cocaine", "meth", "mdma")
LEADS = ("Juniper", "Kit", "Mara", "Cedar")


def _scenes():
    text = DOCUMENT.read_text(encoding="utf-8")
    matches = list(re.finditer(r"^## (TEN-[A-Z]{2}) · .*$", text, re.M))
    out = {}
    for i, m in enumerate(matches):
        end = matches[i + 1].start() if i + 1 < len(matches) else text.find("\n## Continuity")
        out[m.group(1)] = text[m.end():end]
    return text, out


def test_four_scenes_one_per_axis():
    _, scenes = _scenes()
    assert set(scenes) == set(SCENES)
    for key, axis in SCENES.items():
        assert f"tensions: [{axis}]" in scenes[key]


def test_three_real_choices_with_one_no_roll_and_distinct_failures():
    _, scenes = _scenes()
    for key, body in scenes.items():
        assert "| Choice | Check | Success / deterministic consequence | Failed check |" in body
        rows = [
            [c.strip() for c in line.split("|")[1:-1]]
            for line in body.splitlines()
            if line.startswith("| ") and not line.startswith("| ---") and not line.startswith("| Choice ")
        ]
        assert len(rows) == 3, key
        assert sum("No roll" in r[1] for r in rows) == 1, key
        assert "hybrid" in body.lower(), key
        for r in rows:
            assert len(r) == 4 and all(r), (key, r)
            if "No roll" not in r[1]:
                assert r[3] != "Not applicable." and r[2] != r[3], (key, r)


def test_every_opening_has_a_camera_note_that_hands_the_perception_back():
    _, scenes = _scenes()
    for key, body in scenes.items():
        for opening in OPENINGS:
            m = re.search(rf"^- `{opening}`: (.+)$", body, re.M)
            assert m, (key, opening)
            assert re.search(r"[.;] .*\b(can|still|is not)\b", m.group(1)), (key, opening)


def test_every_companion_argues_both_poles_in_every_scene():
    _, scenes = _scenes()
    for key, body in scenes.items():
        both = re.search(r"\*\*Both poles\.\*\*(.+)", body)
        assert both, key
        for lead in LEADS:
            assert lead in both.group(1), (key, lead)
        assert "Either can be told as a good ending" in body, key


def test_no_consumption_guidance_or_clinical_claims():
    text, _ = _scenes()
    lowered = text.lower()
    for banned in ("dose", "dosing", "snort", "inject", "where to buy", "milligram", "high feels"):
        assert banned not in lowered, banned
    assert "no art" in lowered and "120 main cards" in lowered
