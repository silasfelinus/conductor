from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
PRIORITY = ROOT / "projects" / "priority.yaml"


def test_lead_projects_are_the_ones_silas_named():
    """The top of this list is a human decision, and only a human moves it.

    On 2026-08-25 Silas explicitly said Mandarin Tutor and Cthulhuquarium should be the
    two top non-continuous projects, with Mandarin Tutor leading and Cthulhuquarium
    pinned immediately behind it. That superseded the prior Cthulhuquarium/Kapowarr pair
    from 2026-08-24.

    Updated 2026-09-11 on a named human decision, as the rule below requires. Silas
    accepted Mandarin Tutor in session -- "mandarin is acceptable. layout confirmed
    good." -- closing t-021 and flipping the project to `finished`. A finished project is
    a historical record and does not belong in the selectable queue, so it is removed
    here. Cthulhuquarium inherits the lead because that is where Silas already put it in
    the same 2026-08-25 call; no agent invented a new ordering. Kapowarr stays directly
    behind it, also unchanged from his decision.

    The point of this test is unchanged: an agent tidying priority.yaml must not quietly
    reorder the top, and changing it means editing this test with a named human decision
    in the docstring.
    """
    data = yaml.safe_load(PRIORITY.read_text(encoding="utf-8")) or {}
    order = data.get("order") or []

    assert len(order) >= 2
    assert order[0] == "cthulhuquarium"
    assert order[1] == "kapowarr"
    assert "mandarin-tutor" not in order


def test_dream_cycle_ordinary_maintenance_remains_fallback():
    """Daily Dream production is schedule-driven; this list orders ordinary project work."""
    data = yaml.safe_load(PRIORITY.read_text(encoding="utf-8")) or {}
    order = data.get("order") or []

    assert order[-1] == "dream-cycle"
