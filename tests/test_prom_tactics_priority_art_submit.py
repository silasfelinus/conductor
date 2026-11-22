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


def test_priority_tactics_art_requests_are_private_and_unique():
    art = yaml.safe_load(TACTICS_LEDGER.read_text(encoding="utf-8"))
    assert art["auto_submit"] is True
    assert art["is_public"] is False
    assert art["project_slug"] == "every-villain-tactics"
    assert len(art["subjects"]) == 12
    assert len({entry["key"] for entry in art["subjects"]}) == 12
    assert len({entry["asset"] for entry in art["subjects"]}) == 12
    assert all(entry["lane"] == "krea2" for entry in art["subjects"])
