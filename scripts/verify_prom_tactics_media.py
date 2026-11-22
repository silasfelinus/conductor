#!/usr/bin/env python3
"""Prove private Prom/Tactics ArtImage bytes are reachable, without publishing them.

Unlike a DONE ledger receipt, this checks both the authenticated ArtImage record
and the binary media endpoint. It decodes each image to catch broken downloads.
Only identifiers, dimensions, and abbreviated pixel hashes enter public CI logs.
No source image, token, response body or private media URL is persisted.
"""

from __future__ import annotations

import argparse
import hashlib
import sys
from concurrent.futures import ThreadPoolExecutor, as_completed
from pathlib import Path

import yaml


def candidates(paths):
    entries = []
    for path in paths:
        ledger = yaml.safe_load(Path(path).read_text()) or {}
        project = ledger.get("project_slug", "unknown")
        for subject in ledger.get("subjects") or []:
            key = subject.get("key")
            asset = subject.get("asset")
            if not key or not asset:
                continue
            verdict = str(subject.get("verdict") or "").lower()
            art = subject.get("art") or {}
            jobs = subject.get("jobs") or {}
            for lane, details in art.items():
                if not isinstance(details, dict):
                    continue
                image_id = details.get("art_image_id")
                status = details.get("status")
                if status not in {"DONE", "ACCEPTED", "REJECTED"}:
                    continue
                if type(image_id) is not int or image_id <= 0:
                    continue
                job_id = jobs.get(lane)
                if type(job_id) is not int or job_id <= 0:
                    raise ValueError(
                        f"{path}: {key} has image {image_id} without an ArtJob receipt"
                    )
                entries.append(
                    {
                        "project": project,
                        "key": key,
                        "asset": asset,
                        "job_id": job_id,
                        "image_id": image_id,
                        "reviewed": verdict.startswith(("keep", "reject"))
                        or status in {"ACCEPTED", "REJECTED"},
                        "rejected": verdict.startswith("reject")
                        or status == "REJECTED",
                    }
                )
    return entries


def check_one(entry, load_image):
    """The shared loader requests metadata and authenticated media, then decodes."""
    image = load_image(entry["image_id"])
    width, height = image.size
    if width < 128 or height < 128:
        raise ValueError("decoded image has implausible dimensions")
    image.load()
    pixels = image.convert("RGB").tobytes()
    return {
        **entry,
        "width": width,
        "height": height,
        "pixel_sha256": hashlib.sha256(pixels).hexdigest(),
    }


def verify(entries, load_image, max_workers=4):
    results, failures = [], []
    with ThreadPoolExecutor(max_workers=max_workers) as pool:
        pending = {
            pool.submit(check_one, entry, load_image): entry for entry in entries
        }
        for future in as_completed(pending):
            entry = pending[future]
            try:
                results.append(future.result())
            except Exception as exc:
                # Never log a URL, header, server response, or exception body:
                # error messages can carry private media paths or parameters.
                failures.append(
                    {
                        "key": entry["key"],
                        "image_id": entry["image_id"],
                        "reason": type(exc).__name__,
                    }
                )
    return sorted(results, key=lambda row: (row["project"], row["key"])), sorted(
        failures, key=lambda row: row["key"]
    )


def report(entries, results, failures):
    print(f"RECORDED_DONE_OR_REVIEWED={len(entries)}")
    print(f"MEDIA_VERIFIED={len(results)}")
    print(f"MEDIA_FAILED={len(failures)}")
    print(f"CURATOR_REVIEWED={sum(row['reviewed'] for row in entries)}")
    print(f"CURATOR_REJECTED={sum(row['rejected'] for row in entries)}")
    groups = {}
    for item in entries:
        groups[item["project"]] = groups.get(item["project"], 0) + 1
    for project, total in sorted(groups.items()):
        print(f"PROJECT {project}: {total} receipt pairs")
    for item in results:
        print(
            "VERIFIED "
            f"key={item['key']} job={item['job_id']} image={item['image_id']} "
            f"size={item['width']}x{item['height']} "
            f"pixelhash={item['pixel_sha256'][:12]}"
        )
    for item in failures:
        print(
            f"FAILED key={item['key']} image={item['image_id']} "
            f"reason={item['reason']}"
        )
    # Duplicate pixels are warnings, not approvals or arbitrary rejections.
    fingerprints = {}
    for item in results:
        fingerprints.setdefault(item["pixel_sha256"], []).append(item["key"])
    for matching in fingerprints.values():
        if len(matching) > 1:
            print(f"POSSIBLE_DUPLICATE keys={','.join(sorted(matching))}")
    return 1 if failures or not entries else 0


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("ledgers", nargs="+")
    parser.add_argument("--require-count", type=int, default=0)
    args = parser.parse_args(argv)
    entries = candidates(args.ledgers)
    if len(entries) < args.require_count:
        print(
            f"INSUFFICIENT_RECEIPTS expected={args.require_count} "
            f"recorded={len(entries)}"
        )
        return 1
    # The importer reads the API token only in this authenticated CI step.
    from export_shifting_lands_cards import load_image

    results, failures = verify(entries, load_image)
    return report(entries, results, failures)


if __name__ == "__main__":
    sys.exit(main())
