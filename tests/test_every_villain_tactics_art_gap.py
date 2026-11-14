"""Every Villain Tactics Comfy production inventory must be complete and deduplicated.

The approved artwork lives in canonical Prom of Doom ledgers and the three EVT
request batches. Existing DONE roles and the Mags/Warren style-test receipts
are deliberately excluded from fresh requests.
"""
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "projects" / "every-villain-tactics" / "art"
FILES = {
    "fighters": "FIGHTER-REVEALS-REMAINING-2026-11-13.yaml",
    "lieutenants": "POWERED-LIEUTENANTS-REMAINING-2026-11-13.yaml",
    "crews": "HENCHMAN-CREWS-REMAINING-2026-11-13.yaml",
}
ORIGINS = ("accident", "mutant", "tech", "magic", "alien", "psychic")
AFFINITIES = ("fire", "air", "earth", "water", "discipline", "genius", "birthright", "social")
SIGNATURES = {f"{origin}-{affinity}" for origin in ORIGINS for affinity in AFFINITIES}
DONE_REVEAL_SIGNATURES = {
    "accident-fire", "accident-air", "mutant-earth",
    "tech-fire", "tech-genius", "magic-social",
}
ALREADY_PAINTED_ROLES = {
    f"{signature}-{role}"
    for signature in DONE_REVEAL_SIGNATURES
    for role in ("hero", "villain")
} | {"mutant-genius-villain"}
ALREADY_REQUESTED_SUPPORT = {"accident-earth"}


def _ledger(kind):
    return yaml.safe_load((ART / FILES[kind]).read_text())


def test_every_missing_playable_reveal_has_one_new_comfy_request():
    ledger = _ledger("fighters")
    expected = {
        f"evt-reveal-{signature}-{role}"
        for signature in SIGNATURES
        for role in ("hero", "villain")
        if f"{signature}-{role}" not in ALREADY_PAINTED_ROLES
    }
    actual = {row["key"] for row in ledger["subjects"]}
    assert len(ledger["subjects"]) == 83 == len(actual)
    assert actual == expected
    assert {
        row["asset"] for row in ledger["subjects"]
    } == {
        f"every-villain-tactics/popups/{key.removeprefix('evt-reveal-')}"
        for key in expected
    }


def test_lieutenant_and_crew_baselines_omit_existing_comfy_receipts():
    expected = SIGNATURES - ALREADY_REQUESTED_SUPPORT
    for kind, prefix in [
        ("lieutenants", "evt-lieutenant-"),
        ("crews", "evt-henchman-crew-"),
    ]:
        rows = _ledger(kind)["subjects"]
        assert len(rows) == 47
        assert {row["key"].removeprefix(prefix) for row in rows} == expected
        assert len({row["asset"] for row in rows}) == 47


def test_private_selected_checkpoint_and_distinct_render_provenance():
    all_rows = []
    for kind in FILES:
        ledger = _ledger(kind)
        assert ledger["project_slug"] == "every-villain-tactics"
        assert ledger["auto_submit"] is True
        assert ledger["is_public"] is False
        lane = ledger["lanes"][0]
        assert lane["key"] == "unstable-production"
        assert lane["engine"] == "comfy"
        assert lane["checkpoint"] == "SDXL/sdxlUnstableDiffusers_nihilmania.safetensors"
        assert lane["steps"] == 28
        assert lane["cfg"] == 7
        assert lane["sampler"] == "dpmpp_2m"
        for row in ledger["subjects"]:
            assert row["lane"] == lane["key"]
            assert row["size"] == "896x1152"
            assert len(row["prompt_prose"].split()) >= 55
            assert row["asset"].startswith("every-villain-tactics/")
            assert not row.get("jobs"), "New batch must not invent ArtJob IDs"
            all_rows.append(row)
    assert len(all_rows) == 177
    assert len({row["key"] for row in all_rows}) == 177
    assert len({row["asset"] for row in all_rows}) == 177
    assert len({row["seed"] for row in all_rows}) == 177
