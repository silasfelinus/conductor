from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
PRIORITY = ROOT / "projects" / "priority.yaml"


def test_kapowarr_is_highest_priority_finite_project():
    data = yaml.safe_load(PRIORITY.read_text(encoding="utf-8")) or {}
    order = data.get("order") or []

    assert order
    assert order[0] == "kapowarr"


def test_dream_cycle_ordinary_maintenance_remains_fallback():
    """Daily Dream production is schedule-driven; this list orders ordinary project work."""
    data = yaml.safe_load(PRIORITY.read_text(encoding="utf-8")) or {}
    order = data.get("order") or []

    assert order[-1] == "dream-cycle"
