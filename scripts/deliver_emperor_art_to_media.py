#!/usr/bin/env python3
"""Audit and deliver ALREADY-rendered Emperor ArtImages to the durable media share.

An ArtJob marked DONE is not the same as an image served by the game.
This bridge reads the private Conductor round ledgers and sends only explicit
keeper verdicts to Kind Robots' authenticated, no-clobber batch endpoint.

Offline planning (no secret or network required):
    python scripts/deliver_emperor_art_to_media.py --plan --only '^endings/'
Dry-run against the self-hosted server:
    python scripts/deliver_emperor_art_to_media.py --live --only '^quests/'
After visual curation and an explicit publication gate, deliver keepers:
    python scripts/deliver_emperor_art_to_media.py --live --write --only '^quests/'

Env: KR_API_TOKEN, KR_BASE_URL. Never logs the credential or image bytes.
This script DOES NOT submit, rerender, delete or change any ArtImage or ArtJob.
"""

from __future__ import annotations

import argparse
import hashlib
import json
import re
import sys
import urllib.request
from collections import Counter
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).resolve().parent))
import consume_art_queue_core as core

ROOT = Path(__file__).resolve().parent.parent
LEDGER_DIR = ROOT / "projects" / "emperor-of-dust" / "art"
MAX_BATCH = 24
DELIVERY_ROUTE = "/api/admin/emperor-of-dust/art-deliver"


def done_image_id(subject):
    for art in (subject.get("art") or {}).values():
        if not isinstance(art, dict):
            continue
        if art.get("status") == "DONE" and art.get("art_image_id"):
            try:
                image_id = int(art["art_image_id"])
            except (ValueError, TypeError):
                continue
            if image_id > 0:
                return image_id
    return None


def load_ledger_entries(directory=LEDGER_DIR):
    """Preserve each ledger's provenance without dumping hundreds of prompts."""
    entries = []
    for file in sorted(Path(directory).glob("*.yaml")):
        payload = yaml.safe_load(file.read_text(encoding="utf-8")) or {}
        if not isinstance(payload, dict):
            continue
        for subject in payload.get("subjects") or []:
            if not isinstance(subject, dict) or not subject.get("asset"):
                continue
            entries.append({
                "asset": str(subject["asset"]),
                "key": str(subject.get("key") or ""),
                "artImageId": done_image_id(subject),
                "verdict": str(subject.get("verdict") or "").strip().lower(),
                "ledger": file.name,
            })
    return entries


def build_plan(entries, only=None):
    """Never silently choose between different DONE render IDs for an asset."""
    pattern = re.compile(only) if only else None
    selected = [
        row for row in entries
        if row["artImageId"] and (
            pattern is None or pattern.search(row["asset"])
        )
    ]
    groups = {}
    for row in selected:
        groups.setdefault(row["asset"], []).append(row)

    keepers, unreviewed, rejected, collisions = [], [], [], []
    for asset, rows in sorted(groups.items()):
        approved = [r for r in rows if r["verdict"].startswith("keep")]
        source = approved or [
            r for r in rows if not r["verdict"].startswith("reject")
        ]
        if not source:
            rejected.append({"asset": asset, "renderIds": sorted(
                {r["artImageId"] for r in rows}
            )})
            continue
        ids = {r["artImageId"] for r in source}
        if len(ids) > 1:
            collisions.append({
                "asset": asset,
                "renderIds": sorted(ids),
                "ledgers": sorted({r["ledger"] for r in source}),
            })
            continue
        winner = source[-1]
        target = {
            "asset": asset,
            "artImageId": winner["artImageId"],
            "ledger": winner["ledger"],
        }
        if approved:
            keepers.append(target)
        else:
            unreviewed.append(target)

    return {
        "keepers": keepers,
        "unreviewed": unreviewed,
        "rejected": rejected,
        "collisions": collisions,
        "summary": {
            "rendered": len(selected),
            "uniqueAssets": len(groups),
            "keepers": len(keepers),
            "unreviewed": len(unreviewed),
            "rejected": len(rejected),
            "collisions": len(collisions),
        },
    }


def chunks(items, count=MAX_BATCH):
    for index in range(0, len(items), count):
        yield items[index:index + count]


def verify_delivered_media(url, sha256, base_url=None, opener=None):
    """Verify the ACTUAL served WebP bytes; an API receipt is not delivery."""
    if not isinstance(url, str) or not url.startswith("/images/emperor-of-dust/"):
        return False
    if not re.fullmatch(r"[0-9a-f]{64}", str(sha256 or "")):
        return False
    origin = (base_url or core.KR_BASE_URL).rstrip("/")
    request = urllib.request.Request(origin + url, method="GET")
    request.add_header("Accept", "image/webp")
    try:
        with (opener or urllib.request.urlopen)(request, timeout=45) as response:
            if response.status != 200:
                return False
            mime = response.headers.get("Content-Type", "").split(";")[0].strip()
            if mime != "image/webp":
                return False
            payload = response.read()
    except (OSError, ValueError):
        return False
    if not (
        len(payload) >= 20
        and payload[:4] == b"RIFF"
        and payload[8:12] == b"WEBP"
    ):
        return False
    return hashlib.sha256(payload).hexdigest() == sha256


def reconcile(
    plan, write=False, http_json=None, base_url=None, verify_media=None
):
    """Remote requests contain IDs/paths only, never art bytes or bearer tokens."""
    # Isolate conflicting render candidates so they cannot block unrelated
    # reviewed art. No candidate from a collision ever reaches the endpoint.
    if not core.KR_API_TOKEN:
        raise RuntimeError("KR_API_TOKEN absent; use --plan offline.")

    client = http_json or core.http_json
    endpoint = (base_url or core.KR_BASE_URL).rstrip("/") + DELIVERY_ROUTE
    # Dry run includes unreviewed sources to expose the actual delivery gap;
    # writes contain only explicit 'keep' verdicts from durable ledgers.
    candidates = plan["keepers"] if write else (
        plan["keepers"] + plan["unreviewed"]
    )
    if write and not candidates:
        raise RuntimeError(
            "No curator-approved keeper ArtImages in this scope; no media written."
        )
    results = []
    for batch in chunks(candidates):
        payload = {
            "targets": [
                {"asset": item["asset"], "artImageId": item["artImageId"]}
                for item in batch
            ],
            "write": bool(write),
            "curated": bool(write),
        }
        status, response = client("POST", endpoint, payload, timeout=180)
        if (
            status != 200 or not isinstance(response, dict)
            or response.get("success") is not True
            or not isinstance((response.get("data") or {}).get("results"), list)
        ):
            raise RuntimeError(
                "Emperor delivery endpoint rejected the batch "
                f"(HTTP {status}; inspect server logs; no secret shown)."
            )
        rows = response["data"]["results"]
        if len(rows) != len(batch):
            raise RuntimeError("Delivery receipt count differed from request.")
        for result, candidate in zip(rows, batch):
            if (
                result.get("asset") != candidate["asset"]
                or result.get("artImageId") != candidate["artImageId"]
                or result.get("url") != (
                    f"/images/emperor-of-dust/{candidate['asset']}.webp"
                )
            ):
                raise RuntimeError("Delivery receipt provenance mismatch.")
            if write and result.get("status") == "would-write":
                raise RuntimeError("Server ignored an authenticated write request.")
            state = result.get("status")
            reason = result.get("reason")
            if state in ("written", "already-delivered"):
                verifier = verify_media or verify_delivered_media
                if not verifier(
                    result.get("url"), result.get("sha256"),
                    base_url=base_url or core.KR_BASE_URL,
                ):
                    state = "http-verification-failed"
                    reason = "Final HTTP image bytes did not match the API receipt."
            results.append({
                "asset": candidate["asset"],
                "artImageId": candidate["artImageId"],
                "ledger": candidate["ledger"],
                "status": state,
                "artJobId": result.get("artJobId"),
                "sha256": result.get("sha256"),
                "url": result.get("url"),
                "reason": reason,
            })
    return {
        "write": bool(write),
        "summary": dict(Counter(row["status"] for row in results)),
        "results": results,
    }


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ledger-dir", type=Path, default=LEDGER_DIR)
    parser.add_argument("--only", help="regex of eligible asset paths")
    parser.add_argument("--plan", action="store_true", help="offline ledger audit")
    parser.add_argument("--live", action="store_true", help="call Kind Robots")
    parser.add_argument("--write", action="store_true",
                        help="copy only reviewed keepers to the mounted media share")
    parser.add_argument("--report", type=Path, help="write JSON receipt")
    args = parser.parse_args(argv)
    if args.write and not args.live:
        parser.error("--write requires --live")
    if args.plan and args.live:
        parser.error("--plan and --live are mutually exclusive")
    if not args.plan and not args.live:
        parser.error("choose --plan or --live")

    plan = build_plan(load_ledger_entries(args.ledger_dir), args.only)
    report = (
        {"plan": plan}
        if args.plan else
        {"plan": plan, "delivery": reconcile(plan, write=args.write)}
    )
    formatted = json.dumps(report, indent=2, sort_keys=True)
    if args.report:
        args.report.parent.mkdir(parents=True, exist_ok=True)
        args.report.write_text(formatted + "\n", encoding="utf-8")
    else:
        print(formatted)
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
