"""Structural authoring checks for Ecotone's four chapter-anchored companion arcs."""

from pathlib import Path
import re


DOCUMENT = (
    Path(__file__).resolve().parents[1]
    / "projects"
    / "weird-humboldt"
    / "COMPANION-CHAPTER-ANCHORS.md"
)

ROUTES = {"JSC": "juniper", "KLS": "kit", "MLL": "mara", "CRH": "cedar"}
CHAPTERS = (1, 2, 3, 5, 6)


def _scenes():
    text = DOCUMENT.read_text(encoding="utf-8")
    matches = list(re.finditer(r"^### (JSC|KLS|MLL|CRH)-([1-5]) ·.*$", text, re.M))
    scenes = {}
    for index, match in enumerate(matches):
        key = (match.group(1), int(match.group(2)))
        assert key not in scenes, f"duplicate anchor {key}"
        end = matches[index + 1].start() if index + 1 < len(matches) else text.find(
            "\n## Continuity", match.end()
        )
        scenes[key] = text[match.end():end]
    return text, scenes


def test_four_companions_have_five_guaranteed_distinct_beats():
    text, scenes = _scenes()
    assert len(scenes) == 20
    for prefix in ROUTES:
        for beat in range(1, 6):
            assert (prefix, beat) in scenes
        assert f"**Hopeful personal epilogue:**" in scenes[(prefix, 5)]
        assert f"**Scarred personal epilogue:**" in scenes[(prefix, 5)]
    assert "guaranteed" in text.lower()
    assert "late" in text.lower()


def test_every_anchor_offers_three_real_choices_with_failure_and_no_roll():
    _, scenes = _scenes()
    for key, body in scenes.items():
        assert "| Choice | Check | Success / deterministic consequence | Failed check |" in body, key
        rows = [
            line.split("|")[1:-1]
            for line in body.splitlines()
            if line.startswith("| ")
            and not line.startswith("| ---")
            and not line.startswith("| Choice ")
        ]
        assert len(rows) == 3, (key, rows)
        for row in rows:
            assert len(row) == 4, (key, row)
            assert all(cell.strip() for cell in row), (key, row)
        assert sum("No roll" in row[1] for row in rows) == 1, key
        assert sum("No roll" not in row[1] for row in rows) == 2, key
        for row in rows:
            if "No roll" not in row[1]:
                assert row[3].strip() != "Not applicable.", key
                assert row[2].strip() != row[3].strip(), key


def test_each_route_has_recoverable_evidence_and_earned_payoff():
    text, scenes = _scenes()
    for prefix, name in ROUTES.items():
        assert f"arc_{name}_evidence" in scenes[(prefix, 1)]
        assert f"arc_{name}_promise" in scenes[(prefix, 3)]
        assert f"arc_{name}_repair" in scenes[(prefix, 4)]
        assert f"arc_{name}_payoff" in scenes[(prefix, 5)]
        assert "Recovery" in scenes[(prefix, 4)] or "recovery" in scenes[(prefix, 4)]
        assert "No roll" in scenes[(prefix, 1)]
    assert "No new art" in text
    assert "not integrated gameplay" in text
    assert "parents remain together" in text.lower() or "remain together in every outcome" in text.lower()
