from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
PRIORITY = ROOT / "projects" / "priority.yaml"


def test_lead_project_is_the_one_silas_named():
    """The top of this list is a human decision, and only a human moves it.

    Was `order[0] == "kapowarr"`. Silas moved Cthulhuquarium above it in session on
    2026-08-24: "yes, move this project above kapowarr, that project has been very
    successfully scaffolded, and I'm now cleaning up lose ends, this is the new creative
    project for the week." Kapowarr was not demoted in importance -- it is finishing --
    so it stays pinned directly behind the lead rather than dropping into the pack.

    The point of this test is unchanged: an agent tidying priority.yaml must not quietly
    reorder the top, and changing it means editing this test with a named human decision
    in the docstring.
    """
    data = yaml.safe_load(PRIORITY.read_text(encoding="utf-8")) or {}
    order = data.get("order") or []

    assert order
    assert order[0] == "cthulhuquarium"
    assert order[1] == "kapowarr"


def test_dream_cycle_ordinary_maintenance_remains_fallback():
    """Daily Dream production is schedule-driven; this list orders ordinary project work."""
    data = yaml.safe_load(PRIORITY.read_text(encoding="utf-8")) or {}
    order = data.get("order") or []

    assert order[-1] == "dream-cycle"
