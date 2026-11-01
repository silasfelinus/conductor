#!/usr/bin/env python3
"""Fail-closed validation for destination-bound Hoshimori gallery ArtJobs.

The first sixteen gallery jobs used /api/art/enqueue without final media paths.
Later batches use the generic COMFY producer with conductorRequest, targetRepo
and imagePath for relay delivery. A receipt is not verified image delivery.
"""
from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

import yaml

ROOT = Path(__file__).resolve().parents[1]
ART = ROOT / "projects/memory-dungeon/art"
LEDGER = ART / "HOSHIMORI-GALLERY-BOUND-ROUND-3.yaml"
ROUND4_LEDGER = ART / "HOSHIMORI-GALLERY-BOUND-ROUND-4.yaml"
SELECTED = {"e07": (5, 8, 11, 12), "e08": (9, 10, 11, 12)}
ROUND4_SELECTED = {"e07": (13, 14, 15, 16), "e08": (13, 14, 15, 16)}
sys.path.insert(0, str(ROOT / "scripts"))
import consume_art_queue as consumer  # noqa: E402


def source_faces(round_number: int = 3) -> list[dict]:
    if round_number not in (3, 4):
        raise ValueError("unknown Hoshimori bound gallery round")
    faces = []
    selected = SELECTED if round_number == 3 else ROUND4_SELECTED
    for world, numbers in selected.items():
        source = yaml.safe_load(
            (ART / f"HOSHIMORI-{world.upper()}-GALLERY-BRIEFS.yaml").read_text(encoding="utf-8")
        )
        for number in numbers:
            faces.append(source["faces"][number - 1])
    return faces


def validate(data: dict, faces: list[dict], *, require_jobs: bool = False,
             live_jobs: dict[int, dict] | None = None,
             round_number: int = 3,
             allow_missing_live_jobs: bool = False) -> dict:
    requests = data.get("requests") if isinstance(data, dict) else None
    if not isinstance(requests, list) or len(requests) != 8 or len(faces) != 8:
        raise ValueError("bound gallery round requires eight authored requests")
    existing = set()
    for name in ("HOSHIMORI-GALLERY-PILOT-ROUND-1.yaml", "HOSHIMORI-GALLERY-PILOT-ROUND-2.yaml"):
        prior = yaml.safe_load((ART / name).read_text(encoding="utf-8"))
        existing.update(row["face_id"] for row in prior["subjects"])
    prior_jobs: set[int] = set()
    if round_number == 4:
        previous = yaml.safe_load(LEDGER.read_text(encoding="utf-8"))
        existing.update(row["id"] for row in previous["requests"])
        prior_jobs = {row["last_art_job_id"] for row in previous["requests"]
                      if type(row.get("last_art_job_id")) is int}
    elif round_number != 3:
        raise ValueError("unknown Hoshimori bound gallery round")
    seen_ids, seen_paths, seen_jobs = set(), set(), set()
    for request, face in zip(requests, faces):
        expected = {
            "id": face["id"], "source": "memory-dungeon",
            "target_repo": "silasfelinus/kind_robots",
            "image_path": face["image_path"],
            "source_url": face["image_path"].removeprefix("public"),
            "page_url": "https://kindrobots.org/play/memory",
            "variant": "image", "engine": "krea2",
            "project_slug": "memory-dungeon", "size": "768x1024",
            "seed": (50700 if "-e07-" in face["id"] else 50800)
                    + int(face["id"].split("-")[2]),
            "label": face["source_title"], "prompt": face["prompt"],
            "is_public": False, "is_mature": False, "priority": 0,
        }
        if not isinstance(request, dict) or any(request.get(k) != v for k, v in expected.items()):
            raise ValueError(f"gallery source/visibility drift: {face['id']}")
        if request["id"] in existing or request["id"] in seen_ids:
            raise ValueError(f"duplicate gallery face: {request['id']}")
        if request["image_path"] in seen_paths:
            raise ValueError("duplicate gallery destination")
        if request.get("status", "pending") not in ("pending", "done"):
            raise ValueError("invalid gallery request state")
        job = consumer.entry_to_job(request)
        payload = job["payload"]
        binding = payload.get("conductorRequest") or {}
        if (job["engine"] != "COMFY" or job["projectSlug"] != "memory-dungeon"
                or job.get("priority") != 0 or job["resolvedSeed"] != expected["seed"]
                or payload.get("save") != {"isPublic": False, "isMature": False}
                or binding.get("id") != request["id"]
                or binding.get("imagePath") != request["image_path"]
                or binding.get("targetRepo") != "silasfelinus/kind_robots"
                or payload.get("imagePath") != request["image_path"]
                or payload.get("targetRepo") != "silasfelinus/kind_robots"):
            raise ValueError(f"unbound/unsafe ArtJob request: {request['id']}")
        receipt = request.get("last_art_job_id")
        if receipt is not None:
            if type(receipt) is not int or receipt <= 0 or receipt in seen_jobs or receipt in prior_jobs:
                raise ValueError("invalid/duplicate durable ArtJob receipt")
            seen_jobs.add(receipt)
        elif require_jobs:
            raise ValueError(f"unsubmitted gallery request: {request['id']}")
        if live_jobs is not None and receipt is not None:
            current = live_jobs.get(receipt)
            if not isinstance(current, dict):
                if allow_missing_live_jobs:
                    continue
                raise ValueError(f"ArtJob {receipt} missing from live queue")
            actual = current.get("payload") or {}
            if isinstance(actual, str):
                actual = json.loads(actual)
            actual_binding = actual.get("conductorRequest") if isinstance(actual, dict) else {}
            if (current.get("id") != receipt or current.get("projectSlug") != "memory-dungeon"
                    or current.get("engine") != "COMFY"
                    or not isinstance(actual_binding, dict)
                    or any(actual_binding.get(k) != binding.get(k)
                           for k in ("id", "imagePath", "targetRepo"))
                    or actual.get("promptString") != payload.get("promptString")
                    or actual.get("save", {}).get("isPublic") is not False
                    or actual.get("save", {}).get("isMature") is not False):
                raise ValueError(f"ArtJob {receipt} live provenance mismatch")
        seen_ids.add(request["id"])
        seen_paths.add(request["image_path"])
    return {"authored": len(requests), "submitted": len(seen_jobs),
            "unsubmitted": len(requests) - len(seen_jobs),
            "bound_live": sum(receipt in live_jobs for receipt in seen_jobs)
            if live_jobs is not None else None,
            "delivered": "not verified; separate ArtImage and media audit required"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--round", type=int, choices=(3, 4), default=3)
    parser.add_argument("--require-jobs", action="store_true")
    parser.add_argument("--live", action="store_true",
                        help="GET each durable ArtJob and verify persisted destination binding")
    args = parser.parse_args()
    try:
        ledger = LEDGER if args.round == 3 else ROUND4_LEDGER
        data = yaml.safe_load(ledger.read_text(encoding="utf-8"))
        live = None
        if args.live:
            import consume_art_requests as requests
            if not consumer.KR_API_TOKEN:
                raise RuntimeError("KR_API_TOKEN missing for authenticated live receipt verification")
            live = {row["last_art_job_id"]: requests.fetch_job(row["last_art_job_id"])
                    for row in data["requests"] if type(row.get("last_art_job_id")) is int}
        result = validate(data, source_faces(args.round), require_jobs=args.require_jobs,
                          live_jobs=live, round_number=args.round)
    except (OSError, ValueError, KeyError, TypeError, RuntimeError, yaml.YAMLError) as exc:
        print(f"::error::Hoshimori bound gallery audit failed: {exc}", file=sys.stderr)
        return 1
    print(json.dumps(result, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
