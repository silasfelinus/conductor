#!/usr/bin/env python3
"""Validate the eight real Hoshimori gallery pilot requests against authored faces.

This ledger is an opt-in ArtJob producer. Its jobs/art fields are durable
receipts, never proof that images have been delivered to the game.
"""
from __future__ import annotations

import argparse
from pathlib import Path
import sys

import yaml

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "projects/memory-dungeon/art"
LEDGER = ART / "HOSHIMORI-GALLERY-PILOT-ROUND-1.yaml"
SELECTED = {"e07": (6, 7, 9, 10), "e08": (3, 4, 6, 7)}
sys.path.insert(0, str(ROOT / "scripts"))
from memory_dungeon_hoshimori_prompt_contract import validate_prompt  # noqa: E402
from enqueue_art_requests import build_request  # noqa: E402


def validate(data: dict, sources: dict[str, dict], *, require_jobs: bool = False) -> dict:
    if not isinstance(data, dict) or data.get("auto_submit") is not True:
        raise ValueError("pilot must be an opted-in production ledger")
    if any(data.get(k) != v for k, v in {
        "project_slug": "memory-dungeon", "priority": 0,
        "is_public": False, "is_mature": False, "cast_loras": False,
    }.items()):
        raise ValueError("pilot project/visibility/queue settings changed")
    lanes = data.get("lanes")
    if not isinstance(lanes, list) or len(lanes) != 1 or any(
        lanes[0].get(k) != v for k, v in {
            "key": "krea2", "engine": "krea2", "prompt": "prose",
        }.items()
    ):
        raise ValueError("pilot requires exactly one Krea2 lane")
    subjects = data.get("subjects")
    if not isinstance(subjects, list) or len(subjects) != 8:
        raise ValueError("pilot must contain eight gallery faces")
    expected = [
        face for world, indices in SELECTED.items()
        for index in indices for face in [sources[world]["faces"][index - 1]]
    ]
    seen_jobs: set[int] = set()
    for subject, face in zip(subjects, expected):
        world = face["id"].split("-")[1]
        asset = face["image_path"].removeprefix("public/").removesuffix(".webp")
        if any(subject.get(key) != value for key, value in {
            "key": face["id"], "face_id": face["id"], "world": world,
            "site_key": face["site_key"], "title": face["source_title"],
            "asset": asset, "size": "768x1024", "prompt_prose": face["prompt"],
            "seed": (50700 if world == "e07" else 50800) + int(face["id"].split("-")[2]),
        }.items()):
            raise ValueError(f"pilot source drift: {face['id']}")
        validate_prompt(subject["prompt_prose"], face["id"])
        request = build_request(data, lanes[0], subject)
        if (request["engine"] != "krea2" or request["projectSlug"] != "memory-dungeon"
                or request["priority"] != 0 or request["isPublic"] or request["isMature"]):
            raise ValueError(f"unsafe enqueue request: {face['id']}")
        jobs = subject.get("jobs") or {}
        if not isinstance(jobs, dict) or set(jobs) - {"krea2"}:
            raise ValueError(f"unexpected job lane: {face['id']}")
        job_id = jobs.get("krea2")
        if job_id is None:
            if require_jobs:
                raise ValueError(f"unsubmitted gallery face: {face['id']}")
        elif type(job_id) is not int or job_id <= 0 or job_id in seen_jobs:
            raise ValueError(f"invalid/duplicate ArtJob receipt: {face['id']}")
        else:
            seen_jobs.add(job_id)
        art = subject.get("art") or {}
        if not isinstance(art, dict) or set(art) - {"krea2"}:
            raise ValueError(f"unexpected art lane: {face['id']}")
        if art and job_id is None:
            raise ValueError(f"art status without ArtJob receipt: {face['id']}")
        if art:
            row = art["krea2"]
            if not isinstance(row, dict) or row.get("status") not in {
                "PENDING", "RUNNING", "DONE", "FAILED", "CANCELLED",
            }:
                raise ValueError(f"invalid art status: {face['id']}")
            image_id = row.get("art_image_id")
            if image_id is not None and (type(image_id) is not int or image_id <= 0):
                raise ValueError(f"invalid ArtImage receipt: {face['id']}")
            if image_id is not None and row["status"] != "DONE":
                raise ValueError(f"ArtImage claimed before DONE: {face['id']}")
    return {"faces": len(subjects), "submitted": len(seen_jobs), "unsubmitted": 8 - len(seen_jobs)}


def load_and_validate(*, require_jobs: bool = False) -> dict:
    data = yaml.safe_load(LEDGER.read_text(encoding="utf-8"))
    sources = {
        world: yaml.safe_load((ART / f"HOSHIMORI-{world.upper()}-GALLERY-BRIEFS.yaml").read_text(encoding="utf-8"))
        for world in SELECTED
    }
    return validate(data, sources, require_jobs=require_jobs)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--require-jobs", action="store_true")
    args = parser.parse_args()
    try:
        result = load_and_validate(require_jobs=args.require_jobs)
    except (OSError, yaml.YAMLError, ValueError) as exc:
        print(f"::error::Hoshimori gallery pilot invalid: {exc}", file=sys.stderr)
        return 1
    print(f"Hoshimori gallery pilot: {result['faces']} source-backed faces; "
          f"{result['submitted']} durable ArtJob IDs; {result['unsubmitted']} unsubmitted. "
          "No delivery or in-game integration inferred.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
