"""Receipt, privacy and automation contract for Prom's ten canonical art candidates."""
from pathlib import Path

import yaml

from scripts.verify_prom_tactics_media import candidates

ROOT = Path(__file__).resolve().parents[1]
ASHA = ROOT / (
    "projects/comet-city-academy/art/CANON-ASHA-FOUR-ARM-REPAINT-2026-11-21.yaml"
)
CORRECTIONS = ROOT / (
    "projects/comet-city-academy/art/CANON-OUTCOME-CORRECTIONS-2026-11-22.yaml"
)
WORKFLOW = ROOT / ".github/workflows/prom-canon-candidate-media-proof.yml"


def test_four_asha_repaints_are_done_candidates_not_shipped_art():
    records = candidates([ASHA])
    assert yaml.safe_load(ASHA.read_text())["is_public"] is False
    assert [(item["job_id"], item["image_id"]) for item in records] == [
        (76529, 278466),
        (76530, 278467),
        (76531, 278468),
        (76532, 278469),
    ]
    assert all(not item["reviewed"] for item in records)
    assert all(
        item["asset"].startswith("comet-city-academy/identities/mutant-discipline/repaint/")
        for item in records
    )


def test_six_corrective_receipts_are_not_auto_approved():
    records = candidates([CORRECTIONS])
    assert yaml.safe_load(CORRECTIONS.read_text())["is_public"] is False
    assert [(item["job_id"], item["image_id"]) for item in records] == [
        (76593, 278587),
        (76594, 278588),
        (76595, 278589),
        (76596, 278590),
        (76597, 278591),
        (76598, 278592),
    ]
    assert all(not item["reviewed"] for item in records)
    assert len({item["asset"] for item in records}) == 6


def test_private_candidate_proof_fetches_source_and_exact_game_path():
    source = WORKFLOW.read_text()
    workflow = yaml.safe_load(source)
    events = workflow.get("on", workflow.get(True, {}))
    assert "workflow_dispatch" in events
    assert "push" in events
    for ledger in (ASHA, CORRECTIONS):
        relative = str(ledger.relative_to(ROOT))
        assert relative in events["push"]["paths"]
    assert workflow["permissions"] == {"contents": "write"}
    steps = workflow["jobs"]["verify-private-candidates"]["steps"]
    commands = "\n".join(step.get("run", "") for step in steps)
    assert (
        workflow["jobs"]["verify-private-candidates"]["env"]["KR_API_TOKEN"]
        == "${{ secrets.KR_API_TOKEN }}"
    )
    assert commands.count("verify_prom_tactics_media.py") == 2
    assert commands.count("verify_tactics_runtime_media.py") == 2
    assert "--require-count 4 --write-evidence" in commands
    assert "--require-count 6 --write-evidence" in commands
    assert commands.count("checkpoint_art_state.sh") == 2
    assert "PRIVATE_POLICY_VERIFIED=10" in commands
    assert 'private is not False' in commands
    assert "upload-artifact" not in source
    assert "art/enqueue" not in source
