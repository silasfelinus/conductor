"""
Tests for list_curriculum_coverage.py — the ai-art-academy/t-056 read-only
curriculum coverage reporter. Uses a small synthetic skeleton block rather
than the real (43-entry, growing) curriculum-outline.md so these tests don't
churn every time a lane-4 cycle adds a movement.
"""

from pathlib import Path

import pytest

import scripts.list_curriculum_coverage as coverage


SAMPLE_DOC = """# Curriculum Outline

Some prose.

## Machine-readable skeleton

```yaml
movements:
  - slug: greek-vase-painting
    name: Ancient Greek Vase Painting
    era: "c. 600-400 BCE"
    artist_slugs: [exekias, euphiletos-painter]
    example_count: 4
    remix_hint: "some hint"
  - slug: renaissance
    name: Renaissance
    era: "c. 1400-1600"
    artist_slugs: [leonardo-da-vinci, raphael]
    example_count: 4
    remix_hint: "some hint"
  - slug: baroque
    name: Baroque
    era: "c. 1600-1750"
    artist_slugs: [caravaggio]
    example_count: 4
    remix_hint: "some hint"
```

Trailing prose after the fence, not part of the skeleton.
"""


def test_load_skeleton_parses_all_movements():
    movements = coverage.load_skeleton(SAMPLE_DOC)
    assert [m["slug"] for m in movements] == ["greek-vase-painting", "renaissance", "baroque"]


def test_load_skeleton_missing_heading_raises():
    with pytest.raises(ValueError, match="not found"):
        coverage.load_skeleton("# no skeleton heading here")


def test_load_skeleton_missing_fence_raises():
    with pytest.raises(ValueError, match="fence"):
        coverage.load_skeleton("## Machine-readable skeleton\n\nno fence follows")


def test_era_sort_key_orders_bce_before_ce():
    movements = coverage.load_skeleton(SAMPLE_DOC)
    ordered = sorted(movements, key=lambda m: coverage.era_sort_key(m["era"]))
    assert [m["slug"] for m in ordered] == ["greek-vase-painting", "renaissance", "baroque"]


def test_era_sort_key_unparseable_era_sorts_last():
    key_normal = coverage.era_sort_key("c. 600-400 BCE")
    key_unparseable = coverage.era_sort_key("undated")
    assert key_unparseable > key_normal


def test_era_range_handles_single_year_and_bce():
    assert coverage.era_range("c. 600-400 BCE") == (-600, -400)
    assert coverage.era_range("c. 1400-1600") == (1400, 1600)
    assert coverage.era_range("1917") == (1917, 1917)
    assert coverage.era_range("") is None
    assert coverage.era_range("undated") is None


def test_find_overlaps_detects_overlapping_ranges():
    movements = [
        {"slug": "a", "era": "c. 1800-1850"},
        {"slug": "b", "era": "c. 1840-1900"},
        {"slug": "c", "era": "c. 1950-2000"},
    ]
    overlaps = coverage.find_overlaps(movements)
    assert len(overlaps) == 1
    slugs = {overlaps[0][0]["slug"], overlaps[0][1]["slug"]}
    assert slugs == {"a", "b"}


def test_find_overlaps_no_overlap_returns_empty():
    movements = [
        {"slug": "a", "era": "c. 1400-1600"},
        {"slug": "b", "era": "c. 1600-1750"},
    ]
    # touching at a single year boundary still counts as overlap under <= / >=;
    # use a genuine gap to assert the negative case
    movements[1]["era"] = "c. 1751-1900"
    assert coverage.find_overlaps(movements) == []


def test_main_runs_against_real_curriculum_outline(monkeypatch):
    """Smoke test against the real file, catching a schema drift early."""
    assert coverage.CURRICULUM_OUTLINE.exists()
    monkeypatch.setattr("sys.argv", ["list_curriculum_coverage.py"])
    exit_code = coverage.main()
    assert exit_code == 0


def test_main_writes_json(tmp_path, monkeypatch, capsys):
    out = tmp_path / "coverage.json"
    monkeypatch.setattr(
        "sys.argv", ["list_curriculum_coverage.py", "--json", str(out)]
    )
    exit_code = coverage.main()
    assert exit_code == 0
    assert out.exists()
    data = out.read_text()
    assert "greek-vase-painting" in data or len(data) > 0
