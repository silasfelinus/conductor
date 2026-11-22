"""Art-first contract for canon-safe, queued Prom outcome repairs."""

from pathlib import Path

import yaml

from scripts.prom_canon_art_anatomy import missing_canon_traits

ROOT = Path(__file__).resolve().parents[1]
LEDGER = ROOT / "projects/comet-city-academy/art/CANON-OUTCOME-CORRECTIONS-2026-11-22.yaml"
WORKFLOW = ROOT / ".github/workflows/auto-art-generate.yml"

EXPECTED = {
    "magic-earth": {"hero", "villain"},
    "tech-genius": {"hero", "villain"},
    "mutant-discipline": {"hero", "villain"},
}


def test_corrections_are_private_new_requests_with_stable_slot_keys():
    doc = yaml.safe_load(LEDGER.read_text(encoding="utf-8"))
    assert doc["auto_submit"] is True
    assert doc["is_public"] is False
    assert doc["project_slug"] == "comet-city-academy"
    assert {lane["key"] for lane in doc["lanes"]} == {"krea2"}
    subjects = doc["subjects"]
    assert len(subjects) == 6
    assert len({item["key"] for item in subjects}) == len(subjects)
    assert len({item["seed"] for item in subjects}) == len(subjects)
    assert len({item["asset"] for item in subjects}) == len(subjects)
    actual = {}
    for item in subjects:
        assert "jobs" not in item, "Requested is not an accepted ArtJob"
        assert "art" not in item, "Unreviewed requests are not delivered art"
        assert item["lane"] == "krea2"
        assert item["size"] == "1344x768"
        assert not missing_canon_traits(item), item["key"]
        _root, _identities, signature, _outcomes, role = item["asset"].split("/")
        actual.setdefault(signature, set()).add(role)
    assert actual == EXPECTED


def test_auto_art_submits_even_when_render_box_is_unavailable():
    lines = WORKFLOW.read_text(encoding="utf-8").splitlines()
    start = next(i for i, line in enumerate(lines) if "name: Sweep opted-in art ledgers" in line)
    step = "\n".join(lines[start : start + 14])
    assert "if: ${{ steps.krhealth.outputs.up == 'true' }}" in step
    assert "steps.boxhealth.outputs.up" not in step
    assert "sweep_art_ledgers.py --live --submit-only" in step
    checkpoint = "\n".join(lines[start + 12 : start + 28])
    assert "Checkpoint opted-in art ledger ArtJob receipts" in checkpoint
    assert "checkpoint_art_state.sh" in checkpoint


def test_dedicated_prom_tactics_intake_submits_and_checkpoints_corrections():
    intake = (
        ROOT / ".github/workflows/prom-tactics-art-intake.yml"
    ).read_text(encoding="utf-8")
    name = "CANON-OUTCOME-CORRECTIONS-2026-11-22.yaml"
    assert name in intake, "new ledger must trigger the fast intake on merge"
    assert f"projects/comet-city-academy/art/{name} --live" in intake
    assert f"projects/comet-city-academy/art/{name} --status" in intake
    assert "record canonical Prom correction ArtJob receipts" in intake
    assert "Verify durable ArtJob acceptance for six corrections" in intake
    assert "steps.canon.outcome" in intake
