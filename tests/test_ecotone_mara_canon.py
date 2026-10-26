"""Guard current Ecotone companion copy against withdrawn Mara origin claims.

Historic art-job prompts remain untouched for provenance; active copy must not
present those prompts as the character's identity or an approved keeper.
"""
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent / "projects" / "weird-humboldt"
CURRENT = (
    "DESIGN-BRIEF.md",
    "PRELUDE-STATE-CONTRACT.md",
    "PITCHES.md",
)
WITHDRAWN_ASSERTIONS = (
    "a deeply rooted Indigenous Humboldt tattoo artist",
    "Mara was raised on a local reservation",
    "Indigenous tattoo artist raised on a Humboldt reservation",
    "an Indigenous tattoo artist raised on her reservation",
    "The studio grant is **character fiction**",
    "Their tribes, histories and independent paths",
)


def test_current_companion_documents_do_not_assert_withdrawn_mara_origin():
    for filename in CURRENT:
        text = (ROOT / filename).read_text(encoding="utf-8")
        for assertion in WITHDRAWN_ASSERTIONS:
            assert assertion not in text, f"{filename}: obsolete Mara biography: {assertion}"
        assert "EXCLUDED-CONTENT-2026-10-22.md" in text


def test_legacy_mara_art_jobs_remain_auditable_but_are_not_canon():
    round1 = (ROOT / "art" / "ROUND-1.yaml").read_text(encoding="utf-8")
    bakeoff = (ROOT / "art" / "CHECKPOINT-BAKEOFF.yaml").read_text(encoding="utf-8")
    for job in ("40846", "40847", "40884", "40890", "40891"):
        assert job in round1 + bakeoff
    assert "DO NOT EXPORT/PROMOTE" in round1
    assert "LEGACY NONCANON" in round1
    assert "NOT current approval" in round1
    assert "not reuse" in bakeoff
    assert "NONCANON" in bakeoff
