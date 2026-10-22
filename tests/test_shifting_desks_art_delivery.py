"""Art deliveries require matching provenance and fresh media, never bare 200s."""
import importlib.util
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "projects/shifting-desks/art/reconcile_delivery.py"
_spec = importlib.util.spec_from_file_location("sd_reconcile_delivery", ART)
reconcile = importlib.util.module_from_spec(_spec)
_spec.loader.exec_module(reconcile)


def row():
    return {
        "request_id": "shifting-desks-r14-wellness",
        "target_path": "kind_robots public/images/shifting-desks/departments/wellness.webp",
        "media_url": "https://media.acrocatranch.com/images/shifting-desks/departments/wellness.webp",
        "status": "requested",
        "art_job_id": None,
        "art_image_id": None,
        "delivery_check": None,
        "verdict": None,
    }


def job(status="DONE", art_id=900, when="2026-10-20T20:00:00Z", request_id=None, path=None):
    base = row()
    return {
        "id": 505,
        "status": status,
        "createdAt": when,
        "updatedAt": when,
        "artImageId": art_id,
        "payload": {
            "conductorRequest": {"id": request_id or base["request_id"]},
            "targetRepo": "silasfelinus/kind_robots",
            "imagePath": path or "public/images/shifting-desks/departments/wellness.webp",
        },
    }


REQUESTED = reconcile.timestamp("2026-10-20T19:30:00Z")
AFTER = datetime(2026, 10, 20, 20, 5, tzinfo=timezone.utc)
BEFORE = datetime(2026, 10, 20, 19, 5, tzinfo=timezone.utc)


def test_matching_completed_artjob_and_new_media_are_delivered_without_approval():
    changes = reconcile.reconcile_row(row(), [job()], REQUESTED, probe=lambda _url: (AFTER, "verified image"))
    assert changes["status"] == "delivered"
    assert changes["art_job_id"] == 505
    assert changes["art_image_id"] == 900
    assert "verified image" in changes["delivery_check"]
    assert "verdict" not in changes


def test_stale_media_file_is_not_counted_as_new_render():
    changes = reconcile.reconcile_row(row(), [job()], REQUESTED, probe=lambda _url: (BEFORE, "stale image"))
    assert changes["status"] == "rendered"
    assert "not independently verified" in changes["delivery_check"]


def test_completed_artjob_with_missing_media_waits_for_delivery():
    changes = reconcile.reconcile_row(row(), [job()], REQUESTED, probe=lambda _url: (None, "unreachable"))
    assert changes["status"] == "rendered"
    assert changes["art_image_id"] == 900


def test_unmatched_request_path_or_pre_request_job_never_inferred():
    assert reconcile.reconcile_row(row(), [job(request_id="wrong")], REQUESTED) == {}
    assert reconcile.reconcile_row(row(), [job(path="public/images/shifting-desks/other.webp")], REQUESTED) == {}
    assert reconcile.reconcile_row(row(), [job(when="2026-10-19T20:00:00Z")], REQUESTED) == {}


def test_running_or_failed_artjob_does_not_claim_delivery():
    running = reconcile.reconcile_row(row(), [job(status="RUNNING", art_id=None)], REQUESTED)
    assert running == {"art_job_id": 505}
    failed = reconcile.reconcile_row(row(), [job(status="FAILED", art_id=None)], REQUESTED)
    assert "FAILED" in failed["delivery_check"]
    assert "status" not in failed


def test_done_without_artimage_is_not_delivery():
    assert reconcile.reconcile_row(row(), [job(art_id=None)], REQUESTED) == {"art_job_id": 505}


def test_existing_delivery_and_verdict_never_changed():
    old = row()
    old.update(status="delivered", verdict="redo: text garbled")
    assert reconcile.reconcile_row(old, [job()], REQUESTED) == {}


def test_later_job_id_wins_over_older_duplicate():
    old = job()
    newer = job(status="RUNNING", art_id=None)
    newer["id"] = 506
    assert reconcile.reconcile_row(row(), [old, newer], REQUESTED) == {"art_job_id": 506}


def test_targeted_yaml_update_preserves_comments_prompts_seeds_and_unrelated_row():
    text = (
        "# provenance record stays here\n"
        "round: shifting-desks-14\n"
        "subjects:\n"
        "- key: wellness\n"
        "  request_id: shifting-desks-r14-wellness\n"
        "  prompt: 'an armchair with a toothy smile'\n"
        "  seed: 64001\n"
        "  status: requested\n"
        "  delivery_check: null\n"
        "  art_job_id: null\n"
        "  art_image_id: null\n"
        "  verdict: null\n"
        "- key: other\n"
        "  request_id: shifting-desks-r14-other\n"
        "  status: requested\n"
        "  verdict: null\n"
    )
    edits = {"shifting-desks-r14-wellness": {
        "status": "delivered", "art_job_id": 505, "art_image_id": 900, "delivery_check": "verified",
    }}
    rendered = reconcile.patch_rows(text, edits)
    assert reconcile.patch_rows(rendered, edits) == rendered
    assert "# provenance record stays here" in rendered
    assert "  prompt: 'an armchair with a toothy smile'" in rendered
    assert "  seed: 64001" in rendered
    assert "  verdict: null" in rendered
    assert "- key: other\n  request_id: shifting-desks-r14-other\n  status: requested" in rendered
    assert "art_job_id: 505" in rendered


def test_public_url_probe_rejects_other_hosts_without_network():
    stamp, message = reconcile.probe_media("https://example.com/images/shifting-desks/fake.webp", opener=None)
    assert stamp is None and "invalid media" in message
