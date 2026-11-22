"""Keep priority game art submissions ahead of unrelated long-running batches."""

from pathlib import Path

import yaml


ROOT = Path(__file__).resolve().parents[1]
WORKFLOW = ROOT / ".github/workflows/auto-art-generate.yml"
TACTICS_LEDGER = (
    ROOT
    / "projects/every-villain-tactics/art/ONE-HIT-CREW-COMBAT-STATES-2026-11-22.yaml"
)
PROM_LEDGER = (
    ROOT
    / "projects/comet-city-academy/art/AUTHORED-RECRUITS-EMOTIONS-2026-11-22.yaml"
)


def test_priority_art_submission_precedes_long_memory_and_generic_sweeps():
    document = yaml.safe_load(WORKFLOW.read_text(encoding="utf-8"))
    steps = document["jobs"]["generate"]["steps"]
    names = [step.get("name") for step in steps]

    def index(name):
        assert names.count(name) == 1
        return names.index(name)

    health = index("Check Kind Robots API health")
    recovery = index("Recover unrecorded ArtJob IDs")
    priority = index("Submit priority Prom and Tactics ArtJobs")
    checkpoint = index("Checkpoint priority Prom and Tactics ArtJob IDs")
    memory = index("Bulk-submit Memory Dungeon full art backlog")
    sweep = index("Sweep opted-in art ledgers")

    assert health < recovery < priority < checkpoint < memory < sweep
    submit = steps[priority]
    assert submit["env"]["KR_API_TOKEN"] == "${{ secrets.KR_API_TOKEN }}"
    assert "steps.krhealth.outputs.up == 'true'" in submit["if"]
    assert "scripts/enqueue_art_requests.py" in submit["run"]
    assert "--live" in submit["run"]
    assert str(TACTICS_LEDGER.relative_to(ROOT)) in submit["run"]
    assert str(PROM_LEDGER.relative_to(ROOT)) in submit["run"]
    assert 'if [ -f "$ledger" ]' in submit["run"]

    save = steps[checkpoint]
    assert "always()" in save["if"]
    assert "scripts/checkpoint_art_state.sh" in save["run"]



def test_independent_priority_workflow_can_enqueue_without_generic_backlog():
    dedicated = ROOT / ".github/workflows/prom-tactics-priority-art.yml"
    document = yaml.safe_load(dedicated.read_text(encoding="utf-8"))
    steps = document["jobs"]["submit-private-art"]["steps"]
    names = [step.get("name") for step in steps]
    submit = steps[names.index("Submit approved private Krea2 requests with stable request keys")]
    checkpoint = steps[names.index("Persist accepted ArtJob receipts before status checks")]
    status = steps[names.index("Refresh private ArtJob status and ArtImage receipts")]

    assert document["concurrency"]["cancel-in-progress"] is False
    assert document["permissions"]["contents"] == "write"
    assert "scripts/enqueue_art_requests.py" in submit["run"]
    assert str(TACTICS_LEDGER.relative_to(ROOT)) in submit["run"]
    assert str(PROM_LEDGER.relative_to(ROOT)) in submit["run"]
    assert submit["env"]["KR_API_TOKEN"] == "${{ secrets.KR_API_TOKEN }}"
    assert "always()" in checkpoint["if"]
    assert "scripts/checkpoint_art_state.sh" in checkpoint["run"]
    assert "--status" in status["run"]
    assert names.index("Persist accepted ArtJob receipts before status checks") < names.index(
        "Refresh private ArtJob status and ArtImage receipts"
    )
    keyed_script = (ROOT / "scripts/enqueue_art_requests.py").read_text(encoding="utf-8")
    assert 'body["requestKey"] = cell_request_key(' in keyed_script



def test_priority_tactics_art_requests_are_private_and_unique():
    art = yaml.safe_load(TACTICS_LEDGER.read_text(encoding="utf-8"))
    assert art["auto_submit"] is True
    assert art["is_public"] is False
    assert art["project_slug"] == "every-villain-tactics"
    assert len(art["subjects"]) == 12
    assert len({entry["key"] for entry in art["subjects"]}) == 12
    assert len({entry["asset"] for entry in art["subjects"]}) == 12
    assert all(entry["lane"] == "krea2" for entry in art["subjects"])
