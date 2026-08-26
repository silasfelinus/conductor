from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
PRIORITY = ROOT / "projects" / "priority.yaml"


def test_lead_projects_are_the_two_silas_named():
    """The top of this list is a human decision, and only a human moves it.

    On 2026-08-25 Silas explicitly said Mandarin Tutor and Cthulhuquarium should be the
    two top non-continuous projects. Mandarin Tutor leads here, consistent with his
    earlier framing of other work as "just below Mandarin Tutor"; Cthulhuquarium is
    pinned immediately behind it. This supersedes the prior Cthulhuquarium/Kapowarr
    pair from 2026-08-24.

    The point of this test is unchanged: an agent tidying priority.yaml must not quietly
    reorder the top, and changing it means editing this test with a named human decision
    in the docstring.
    """
    data = yaml.safe_load(PRIORITY.read_text(encoding="utf-8")) or {}
    order = data.get("order") or []

    assert len(order) >= 2
    assert order[0] == "mandarin-tutor"
    assert order[1] == "cthulhuquarium"


def test_dream_cycle_ordinary_maintenance_remains_fallback():
    """Daily Dream production is schedule-driven; this list orders ordinary project work."""
    data = yaml.safe_load(PRIORITY.read_text(encoding="utf-8")) or {}
    order = data.get("order") or []

    assert order[-1] == "dream-cycle"
