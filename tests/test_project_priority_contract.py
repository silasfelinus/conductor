from pathlib import Path

import yaml

from scripts.audit_roadmaps import audit


ROOT = Path(__file__).resolve().parents[1]
PRIORITY = ROOT / "projects" / "priority.yaml"
OVERRIDES = ROOT / "project-overrides.yaml"


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

    Updated again 2026-09-11, same sweep, same rule. Silas confirmed Kapowarr's last gate
    from his own environment -- "Kapowarr has had successful Sab downloads, pretty sure
    torrents as well. Confirmed." -- taking it to 71/71 and `finished`; and closed
    AI Art Academy as-is ("an outdated project to test things ... I don't see it becoming
    an app"). Both leave the selectable queue. Kind Economy inherits second place, which is
    where it already sat behind Kapowarr, so again no agent invented an ordering.

    Updated 2026-09-19, same rule, opposite direction. Silas reopened Mandarin Tutor in
    session -- "i want an evolution of the mandarin project ... a tutorial page for each of
    the words that we teach, and a system where we only show flashcards after showing the
    instruction ... We should also add a point system." That names it as live work again, so
    it returns to the queue. He did NOT restate the lead position his 2026-08-25 call gave
    it, so it deliberately does NOT go back to order[0]; it sits behind the two projects he
    marked HIGH on 2026-09-18. Restoring its old lead would be an agent inventing an
    ordering from a stale decision, which is exactly what this test exists to prevent.

    The point of this test is unchanged: an agent tidying priority.yaml must not quietly
    reorder the top, and changing it means editing this test with a named human decision
    in the docstring.
    """
    data = yaml.safe_load(PRIORITY.read_text(encoding="utf-8")) or {}
    order = data.get("order") or []

    assert len(order) >= 2
    assert order[0] == "cthulhuquarium"
    assert order[1] == "kind-economy"
    for finished in ("kapowarr", "ai-art-academy"):
        assert finished not in order

    # Reopened 2026-09-19 (see docstring): present, but not the lead.
    assert "mandarin-tutor" in order
    assert order.index("mandarin-tutor") > order.index("art-archive")


def test_control_priority_band_matches_priority_queue():
    """CONTROL's human steering band must move atomically with priority.yaml."""
    report = audit()
    drifts = [
        finding
        for finding in report["findings"]
        if finding["code"] == "CONTROL_PRIORITY_DRIFT"
    ]

    assert not drifts, drifts[0]["message"] if drifts else "CONTROL priority drift"


def test_dream_cycle_ordinary_maintenance_remains_fallback():
    """Daily Dream production is schedule-driven; this list orders ordinary project work."""
    data = yaml.safe_load(PRIORITY.read_text(encoding="utf-8")) or {}
    order = data.get("order") or []

    assert order[-1] == "dream-cycle"


def test_butterfly_gallery_leads_art_archive_and_both_are_high():
    """Silas 2026-09-18: both projects are high priority, Butterfly Gallery first."""
    data = yaml.safe_load(PRIORITY.read_text(encoding="utf-8")) or {}
    order = data.get("order") or []
    assert order.index("butterfly-gallery") < order.index("art-archive")

    overrides_raw = yaml.safe_load(OVERRIDES.read_text(encoding="utf-8")) or {}
    overrides = {
        row.get("slug"): row
        for row in (overrides_raw.get("overrides") or [])
        if isinstance(row, dict) and row.get("slug")
    }
    assert overrides["butterfly-gallery"]["priority"] == "high"
    assert overrides["art-archive"]["priority"] == "high"
