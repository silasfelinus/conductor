"""Private media must be fetched and decoded, never published in CI artifacts."""
from pathlib import Path

import pytest
import yaml
from PIL import Image

from scripts.verify_prom_tactics_media import candidates, report, verify

ROOT = Path(__file__).resolve().parents[1]
TACTICS = (
    ROOT / "projects/every-villain-tactics/art/ONE-HIT-CREW-TELEGRAPHS-2026-11-20.yaml"
)
PROM = ROOT / "projects/comet-city-academy/art/UNSTABLE-PRODUCTION-FAMILY-ROUND-1.yaml"
FLOW = ROOT / ".github/workflows/prom-tactics-media-proof.yml"


def test_historical_receipts_are_not_new_queue_submissions():
    tactics = candidates([TACTICS])
    prom = candidates([PROM])
    assert len(tactics) == 12
    assert len(prom) == 14
    assert [x["job_id"] for x in tactics] == list(range(74393, 74405))
    assert [x["image_id"] for x in tactics] == list(range(277786, 277798))
    assert all(not x["reviewed"] for x in tactics)
    assert all(x["asset"].startswith("every-villain-tactics/") for x in tactics)


def test_done_is_not_visual_approval(tmp_path):
    source = tmp_path / "round.yaml"
    source.write_text(
        yaml.safe_dump(
            {
                "project_slug": "comet-city-academy",
                "subjects": [
                    {
                        "key": "kept",
                        "asset": "identities/a",
                        "jobs": {"krea": 10},
                        "art": {"krea": {"status": "ACCEPTED", "art_image_id": 20}},
                    },
                    {
                        "key": "rejected",
                        "asset": "identities/b",
                        "verdict": "reject: extra limbs",
                        "jobs": {"krea": 11},
                        "art": {"krea": {"status": "DONE", "art_image_id": 21}},
                    },
                    {
                        "key": "unreviewed",
                        "asset": "identities/c",
                        "jobs": {"krea": 12},
                        "art": {"krea": {"status": "DONE", "art_image_id": 22}},
                    },
                    {
                        "key": "still-queued",
                        "asset": "identities/d",
                        "jobs": {"krea": 13},
                        "art": {"krea": {"status": "RUNNING"}},
                    },
                ],
            }
        )
    )
    found = candidates([source])
    assert len(found) == 3
    assert {row["key"] for row in found if row["reviewed"]} == {
        "kept", "rejected"
    }
    assert {row["key"] for row in found if row["rejected"]} == {"rejected"}

    results, failures = verify(
        found, lambda _image_id: Image.new("RGB", (256, 256)), max_workers=2
    )
    assert not failures
    assert len(results) == 3
    assert all(len(row["pixel_sha256"]) == 64 for row in results)


def test_failed_media_does_not_leak_url_or_token(capsys):
    entries = [
        {
            "project": "private",
            "key": "broken",
            "asset": "private/asset",
            "job_id": 15,
            "image_id": 25,
            "reviewed": False,
            "rejected": False,
        }
    ]

    def inaccessible(_image_id):
        raise RuntimeError("Bearer secret-token https://private.example/blob")

    results, failures = verify(entries, inaccessible)
    assert not results
    assert failures == [
        {"key": "broken", "image_id": 25, "reason": "RuntimeError"}
    ]
    assert report(entries, results, failures) == 1
    printed = capsys.readouterr().out
    assert "secret-token" not in printed
    assert "https://private" not in printed
    assert "MEDIA_VERIFIED=0" in printed


def test_orphaned_image_receipt_rejected(tmp_path):
    source = tmp_path / "orphan.yaml"
    source.write_text(
        yaml.safe_dump(
            {
                "subjects": [
                    {
                        "key": "orphan",
                        "asset": "game/asset",
                        "art": {"krea": {"status": "DONE", "art_image_id": 25}},
                    }
                ]
            }
        )
    )
    with pytest.raises(ValueError, match="without an ArtJob receipt"):
        candidates([source])


def test_workflow_probes_private_bytes_without_publishing():
    flow = yaml.safe_load(FLOW.read_text())
    events = flow.get("on", flow.get(True, {}))
    assert "workflow_dispatch" in events
    assert "push" in events
    assert flow["permissions"] == {"contents": "read"}
    job = flow["jobs"]["verify-private-media"]
    assert job["env"]["KR_API_TOKEN"] == "${{ secrets.KR_API_TOKEN }}"
    commands = "\n".join(step.get("run", "") for step in job["steps"])
    assert "verify_prom_tactics_media.py" in commands
    assert "--require-count 12" in commands
    assert "--require-count 14" in commands
    assert "upload-artifact" not in str(flow)
    assert "art/enqueue" not in commands
