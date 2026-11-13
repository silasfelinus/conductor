"""Round 19 must fix only 14 rejected Classic compositions without false art approval."""
from __future__ import annotations

import importlib.util
import sys
from datetime import datetime, timedelta, timezone
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "projects/shifting-desks/art"
sys.path.insert(0, str(ART))
sys.path.insert(0, str(ROOT / "scripts"))

from repair_negation_art_prompts import violations  # noqa: E402


def read(round_number):
    return yaml.safe_load((ART / f"ROUND-{round_number}.yaml").read_text(encoding="utf-8"))


def test_only_previously_rejected_classic_destinations_are_queued():
    current = read(19)
    assert current["round"] == "shifting-desks-19"
    assert current["task"] == "t-032"
    assert current["requested_at"]
    rows = current["subjects"]
    assert len(rows) == 14
    assert len({r["key"] for r in rows}) == len({r["target_path"] for r in rows}) == 14
    old = {
        r["target_path"]: r
        for n in (14, 15)
        for r in read(n)["subjects"]
        if str(r.get("verdict") or "").startswith("redo:")
    }
    assert set(old) == {r["target_path"] for r in rows}
    assert len({r["request_id"] for r in rows}) == 14
    assert len({r["seed"] for r in rows}) == 14
    for r in rows:
        prior = old[r["target_path"]]
        assert r["request_id"] == f"shifting-desks-r19-{r['key']}"
        assert r["prompt"] != prior["prompt"]
        assert r["size"] == prior["size"]
        assert r["engine"] == "krea2"
        assert r["target_path"].startswith("kind_robots public/images/shifting-desks/")
        assert r["target_path"].endswith(".webp")
        assert "ArtJob" in r["replaces"] and "ArtImage" in r["replaces"]
        assert r["failure_note"].lower().find("redo:") >= 0
        assert not violations(r["prompt"]), r["key"]


def test_every_new_round19_request_has_an_idempotent_authoring_and_queue_match():
    rows = read(19)["subjects"]
    queue = yaml.safe_load((ROOT / "projects/art-prompts.yaml").read_text(encoding="utf-8"))["requests"]
    queued_by_id = {}
    for row in queue:
        queued_by_id.setdefault(row["id"], []).append(row)
    for art in rows:
        matches = queued_by_id[art["request_id"]]
        assert len(matches) == 1, art["request_id"]
        row = matches[0]
        assert row["force"] is True
        assert row["target_repo"] == "silasfelinus/kind_robots"
        assert row["project_slug"] == "shifting-desks"
        assert row["image_path"] == art["target_path"].replace("kind_robots ", "")
        assert row["source_url"] == "/" + row["image_path"].removeprefix("public/")
        assert (row["prompt"], row["seed"], row["size"], row["engine"]) == (
            art["prompt"], art["seed"], art["size"], art["engine"]
        )
        assert row["negative_prompt"] == art["negative_prompt"]
        assert row["status"] in {"pending", "done", "rendering", "failed"}
        # Queue may complete before the round is independently reviewed: no implicit KEEP.
        if art["status"] != "delivered":
            assert art.get("verdict") is None



def test_five_original_keep_plates_have_independent_job_and_media_evidence():
    original = read(1)["subjects"]
    expected = {
        "encounter-back": (38381, 246469),
        "review-back": (38382, 246471),
        "gus-shop-steward": (38383, 246473),
        "something-ticking-in-the-toner": (38384, 246475),
        "trust-fall-over-the-shredder": (38385, 246477),
    }
    for row in original:
        if row["key"] not in expected:
            continue
        job, image = expected[row["key"]]
        assert (row["art_job_id"], row["art_image_id"]) == (job, image)
        assert row["status"] == "delivered"
        assert row["verdict"].startswith("keep:")
        assert f"ArtJob {job} DONE, ArtImage {image}" in row["delivery_check"]
        assert "confirmed newer than ArtJob" in row["delivery_check"]



def load_audit():
    file = ART / "audit_live_artjobs.py"
    spec = importlib.util.spec_from_file_location("sd_round19_audit", file)
    module = importlib.util.module_from_spec(spec)
    assert spec and spec.loader
    spec.loader.exec_module(module)
    return module


def test_legacy_provenance_requires_matching_job_and_current_media():
    audit = load_audit()
    now = datetime(2026, 10, 14, tzinfo=timezone.utc)
    row = {
        "key": "legacy-plate",
        "request_id": "shifting-desks-r1-legacy-plate",
        "target_path": "kind_robots public/images/shifting-desks/backs/review.webp",
        "media_url": "https://media.acrocatranch.com/images/shifting-desks/backs/review.webp",
        "_requested_at": "2026-10-13T05:00:00Z",
    }
    job = {
        "id": 4051, "status": "DONE", "artImageId": 7001,
        "createdAt": now.isoformat(),
        "payload": {
            "imagePath": "public/images/shifting-desks/backs/review.webp",
            "targetRepo": "silasfelinus/kind_robots",
            "conductorRequest": {"id": row["request_id"]},
        },
    }
    probe = lambda _url: (now + timedelta(minutes=4), "HEAD 200 image/webp, newer media")
    result = audit.audit_legacy_round1([row], [job], probe=probe)[0]
    assert result["job_id"] == 4051
    assert result["image_id"] == 7001
    assert result["proven_current_media"]
    for missing in (
        {**job, "payload": {**job["payload"], "conductorRequest": {"id": "unrelated"}}},
        {**job, "payload": {**job["payload"], "imagePath": "public/elsewhere.webp"}},
        {**job, "artImageId": None},
    ):
        result = audit.audit_legacy_round1([row], [missing], probe=probe)[0]
        assert result["proven_current_media"] is False
    stale = audit.audit_legacy_round1(
        [row], [job], probe=lambda _: (now - timedelta(hours=1), "old image")
    )[0]
    assert stale["proven_current_media"] is False
    assert stale["explanation"] == "do not infer delivery provenance"
