#!/usr/bin/env python3
"""Read-only production readiness audit for both Hoshimori collectible galleries.

The 64 authored briefs are NOT ArtJobs. The twenty existing style-proof ArtJobs
are NOT rendered images. This checks both inventories against the last committed
delivery snapshots, and deliberately never treats a stale snapshot as a live
render heartbeat or permission to submit more work.
"""
from __future__ import annotations

import argparse
from collections import Counter
import json
from pathlib import Path
import re
from typing import Any

import yaml

from audit_memory_dungeon_hoshimori_style import validate as validate_warm_style
from audit_memory_dungeon_hoshimori_horror_style import validate as validate_horror_style
from memory_dungeon_hoshimori_prompt_contract import validate_prompt

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "projects/memory-dungeon/art"
CATEGORY_ORDER = ["character"] * 10 + ["location"] * 10 + ["event"] * 10 + ["collaboration"] * 2
WORLDS = {
    "e07": ("HOSHIMORI-E07-GALLERY-BRIEFS.yaml", "HOSHIMORI-WARM-STYLE-PROOFS.yaml",
            "HOSHIMORI-WARM-STYLE-STATUS.json", validate_warm_style),
    "e08": ("HOSHIMORI-E08-GALLERY-BRIEFS.yaml", "HOSHIMORI-HORROR-STYLE-PROOFS.yaml",
            "HOSHIMORI-HORROR-STYLE-STATUS.json", validate_horror_style),
}


def validate_gallery(data: dict[str, Any], world: str) -> list[dict[str, Any]]:
    """Reject invented production evidence, malformed destinations and bad budgets."""
    if not isinstance(data, dict) or any(data.get(k) != v for k, v in {
        "version": 1, "world": world, "project": "memory-dungeon",
        "stage": "briefs_only", "auto_submit": False,
        "expected_local": 30, "expected_collaboration": 2,
    }.items()):
        raise ValueError(f"{world}: gallery is not an authoring-only 30+2 manifest")
    faces = data.get("faces")
    if not isinstance(faces, list) or len(faces) != 32:
        raise ValueError(f"{world}: expected exactly 32 gallery faces")
    if [face.get("category") if isinstance(face, dict) else None for face in faces] != CATEGORY_ORDER:
        raise ValueError(f"{world}: wrong category order or 30+2 budget")
    ids: set[str] = set()
    paths: set[str] = set()
    for index, face in enumerate(faces, 1):
        if not isinstance(face, dict):
            raise ValueError(f"{world}: malformed gallery face")
        identifier = face.get("id")
        if not isinstance(identifier, str):
            raise ValueError(f"{world}: missing face ID")
        match = re.fullmatch(rf"hoshimori-{world}-{index:02d}-([a-z0-9-]+)", identifier)
        if match is None:
            raise ValueError(f"{world}: invalid face ID {identifier}")
        expected_path = (
            f"public/images/memory-dungeon/hoshimori/{world}/gallery/"
            f"{index:02d}-{match.group(1)}.webp"
        )
        if identifier in ids or expected_path in paths or face.get("image_path") != expected_path:
            raise ValueError(f"{world}: duplicate or invalid image destination {identifier}")
        if face.get("status") != "brief_only" or any(key in face for key in (
            "last_art_job_id", "art_image_id", "delivered", "source_url",
        )):
            raise ValueError(f"{world}: invented submission/delivery claim {identifier}")
        if not re.fullmatch(r"[1-8],[1-8]", str(face.get("site_key", ""))):
            raise ValueError(f"{world}: invalid map coordinate {identifier}")
        if len(str(face.get("source_title", ""))) < 9 or len(str(face.get("story_hook", ""))) < 50:
            raise ValueError(f"{world}: missing narrative provenance {identifier}")
        if index <= 30 and "cross_realm" in face:
            raise ValueError(f"{world}: local face has cross-realm identity {identifier}")
        if index > 30 and not re.fullmatch(r"e(?:0[1-9]|1[0-2])", str(face.get("cross_realm", ""))):
            raise ValueError(f"{world}: missing cross-realm collaboration {identifier}")
        validate_prompt(face.get("prompt"), identifier)
        ids.add(identifier)
        paths.add(expected_path)
    return faces


def validate_style_snapshot(
    ledger: dict[str, Any], snapshot: dict[str, Any], world: str, validator,
) -> dict[str, int]:
    """Reconcile each snapshot row to its durable receipt; never infer live health."""
    receipts = validator(ledger, require_jobs=True)
    rows = snapshot.get("results") if isinstance(snapshot, dict) else None
    if not isinstance(rows, list) or len(rows) != 10:
        raise ValueError(f"{world}: missing ten-row style delivery snapshot")
    expected = {
        f"memory-dungeon-hoshimori-{world}-style-{slug}": (job, slug)
        for slug, job in receipts.items()
    }
    seen: set[str] = set()
    counts: Counter[str] = Counter()
    for row in rows:
        if not isinstance(row, dict):
            raise ValueError(f"{world}: malformed style snapshot row")
        identifier = row.get("id")
        if identifier not in expected or identifier in seen:
            raise ValueError(f"{world}: unexpected/duplicate style snapshot identity {identifier}")
        job, slug = expected[identifier]
        destination = f"public/images/memory-dungeon/hoshimori/{world}/style-proofs/{slug}.webp"
        if row.get("jobId") != job or row.get("imagePath") != destination:
            raise ValueError(f"{world}: snapshot receipt mismatch for {identifier}")
        state = row.get("status")
        if not isinstance(state, str) or not state:
            raise ValueError(f"{world}: missing delivery state for {identifier}")
        if state == "delivered" and (
            not isinstance(row.get("artImageId"), int) or row["artImageId"] <= 0
        ):
            raise ValueError(f"{world}: delivery without ArtImage identity {identifier}")
        seen.add(identifier)
        counts[state] += 1
    if (set(expected) != seen or snapshot.get("total") != 10
            or snapshot.get("counts") != dict(sorted(counts.items()))
            or snapshot.get("delivered") != counts["delivered"]
            or snapshot.get("pendingReview") != 10 - counts["delivered"]):
        raise ValueError(f"{world}: inconsistent delivery snapshot totals")
    return {"submitted": len(receipts), "snapshot_delivered": counts["delivered"],
            "snapshot_pending": counts["pending"], "snapshot_running": counts["running"]}


def audit(manifests: dict[str, dict], ledgers: dict[str, dict], snapshots: dict[str, dict]) -> dict:
    ids: set[str] = set()
    paths: set[str] = set()
    styles: dict[str, dict[str, int]] = {}
    for world, (_, _, _, validator) in WORLDS.items():
        faces = validate_gallery(manifests[world], world)
        for face in faces:
            if face["id"] in ids or face["image_path"] in paths:
                raise ValueError("Cross-reality duplicate face ID or media destination")
            ids.add(face["id"])
            paths.add(face["image_path"])
        styles[world] = validate_style_snapshot(ledgers[world], snapshots[world], world, validator)

    delivered = sum(row["snapshot_delivered"] for row in styles.values())
    pending = sum(row["snapshot_pending"] for row in styles.values())
    return {
        "project": "memory-dungeon",
        "worlds": ["e07", "e08"],
        "source": "committed_snapshot_not_live",
        "gallery_briefs": len(ids),
        "gallery_artjobs": 0,
        "gallery_delivered_images": 0,
        "style_artjobs": sum(row["submitted"] for row in styles.values()),
        "style_snapshot_delivered": delivered,
        "style_snapshot_pending": pending,
        "style_by_world": styles,
        "ready_for_gallery_submission": False,
        "blockers": [
            "64 gallery entries are briefs_only with auto_submit=false; no gallery ArtJob receipts",
            f"{20 - delivered}/20 style proofs lack verified delivery in the last committed snapshot",
            "a committed delivery snapshot is not a live render heartbeat or fresh media check",
        ],
    }



def audit_live(
    manifests: dict[str, dict], ledgers: dict[str, dict], snapshots: dict[str, dict],
    *, jobs: list[dict] | None = None, heartbeat_state: str | None = None,
    media_probe=None,
) -> dict:
    """Recheck existing receipts and media; never enqueue or mutate ArtJobs."""
    from datetime import datetime, timezone

    from audit_memory_dungeon_hoshimori_style import audit_delivery as warm_delivery
    from audit_memory_dungeon_hoshimori_horror_style import audit_delivery as horror_delivery

    if jobs is None:
        import consume_art_queue as consumer
        from reconcile_memory_dungeon_art_jobs import server_jobs

        if not consumer.KR_API_TOKEN:
            raise RuntimeError("KR_API_TOKEN unavailable; no live ArtJob verification")
        jobs = server_jobs()

    if heartbeat_state is None:
        import check_engine_heartbeat as engine

        try:
            heartbeat_state, _ = engine.assess(
                engine.fetch_uptime(), datetime.now(timezone.utc)
            )
        except RuntimeError:
            heartbeat_state = engine.UNRESOLVED

    base = audit(manifests, ledgers, snapshots)
    delivery_auditors = {"e07": warm_delivery, "e08": horror_delivery}
    live = {}
    for world, (_, _, _, validator) in WORLDS.items():
        audit_delivery = delivery_auditors[world]
        result = (
            audit_delivery(ledgers[world], jobs)
            if media_probe is None
            else audit_delivery(ledgers[world], jobs, media_probe)
        )
        live[world] = validate_style_snapshot(ledgers[world], result, world, validator)
    live_delivered = sum(row["snapshot_delivered"] for row in live.values())
    base["live"] = {
        "source": "authenticated_artjobs_and_fresh_media_head",
        "engine_heartbeat_state": heartbeat_state,
        "style_proofs": live,
        "style_delivered": live_delivered,
        "style_not_delivered": 20 - live_delivered,
    }
    base["source"] = "live_reconciled_with_committed_snapshot"
    base["blockers"] = [
        "64 gallery entries remain briefs_only without gallery ArtJob receipts",
        f"{20 - live_delivered}/20 style proofs lack fresh verified media delivery",
        "visual inspection of the 8x8 maps, 6x6 atlases and style samples is required",
    ]
    if heartbeat_state != "ok":
        base["blockers"].append(
            f"render engine heartbeat is {heartbeat_state}; HTTP reachability is insufficient"
        )
    base["ready_for_visual_review"] = (
        heartbeat_state == "ok" and live_delivered == 20
    )
    # Even twenty verified files still need agent visual QA before gallery enqueue.
    # The authored 64 briefs carry no gallery receipts and auto_submit stays false.
    base["ready_for_gallery_submission"] = False
    return base


def load_report(directory: Path = ART) -> dict:
    manifests, ledgers, snapshots = {}, {}, {}
    for world, (gallery, ledger, snapshot, _) in WORLDS.items():
        manifests[world] = yaml.safe_load((directory / gallery).read_text(encoding="utf-8"))
        ledgers[world] = yaml.safe_load((directory / ledger).read_text(encoding="utf-8"))
        snapshots[world] = json.loads((directory / snapshot).read_text(encoding="utf-8"))
    return audit(manifests, ledgers, snapshots)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--live", action="store_true",
                        help="read current ArtJobs, media HEADs and authenticated engine heartbeat")
    parser.add_argument("--require-ready", action="store_true",
                        help="exit 2 while any real production/delivery work remains")
    args = parser.parse_args()
    try:
        report = load_report()
        if args.live:
            manifests, ledgers, snapshots = {}, {}, {}
            for world, (gallery, ledger, snapshot, _) in WORLDS.items():
                manifests[world] = yaml.safe_load((ART / gallery).read_text(encoding="utf-8"))
                ledgers[world] = yaml.safe_load((ART / ledger).read_text(encoding="utf-8"))
                snapshots[world] = json.loads((ART / snapshot).read_text(encoding="utf-8"))
            report = audit_live(manifests, ledgers, snapshots)
    except (OSError, ValueError, KeyError, TypeError, RuntimeError, yaml.YAMLError) as exc:
        print(f"::error::Hoshimori gallery readiness audit failed: {exc}")
        return 1
    print(json.dumps(report, indent=2, sort_keys=True))
    return 2 if args.require_ready and not report["ready_for_gallery_submission"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
