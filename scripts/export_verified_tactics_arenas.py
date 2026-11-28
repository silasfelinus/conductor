#!/usr/bin/env python3
"""Export real, privately verified tactical arena receipts into Kind Robots.

Only an ArtImage whose recorded ArtJob, art receipt and authenticated byte proof
all agree may replace a fallback painting. Artwork review is a separate gate.
The stage-to-asset map expresses canonical routes, never hardcodes image IDs.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path

import yaml

PROJECT = Path(__file__).resolve().parents[1] / "projects/every-villain-tactics/art"
STAGES_BY_ASSET = {
    "every-villain-tactics/maps/last-order-diner": "last-order",
    "every-villain-tactics/maps/sunken-street": "sunken-street",
    "every-villain-tactics/maps/unlicensed-rescue": "unlicensed-rescue",
    "every-villain-tactics/maps/ferris-wheel": "ferris-wheel",
    "every-villain-tactics/maps/song-that-stopped": "song-that-stopped",
    "every-villain-tactics/maps/hydrant-blue": "hydrant-blue",
    "every-villain-tactics/maps/clocktower-collapse": "clocktower-collapse",
    "every-villain-tactics/maps/equation-that-escaped": "equation-that-escaped",
    "every-villain-tactics/maps/candle-that-wouldnt-die": "candle-that-wouldnt-die",
    "every-villain-tactics/maps/orchard-under-asphalt": "orchard-under-asphalt",
    "every-villain-tactics/maps/future-in-the-glass": "future-in-the-glass",
    "every-villain-tactics/maps/overdue-thunder": "overdue-thunder",
    "every-villain-tactics/maps/bell-and-the-door": "bell-and-the-door",
    "every-villain-tactics/maps/when-two-plus-two-screamed": "when-two-plus-two-screamed",
    "every-villain-tactics/maps/heir-who-said-no": "heir-who-said-no",
    "every-villain-tactics/maps/empty-applause": "empty-applause",
    "every-villain-tactics/maps/ashes-of-the-ledger": "ashes-of-the-ledger",
    "every-villain-tactics/maps/balcony-witness": "balcony-witness",
    "every-villain-tactics/maps/bridge-of-last-chances": "bridge-of-last-chances",
    "every-villain-tactics/maps/ship-with-no-port": "ship-with-no-port",
    "every-villain-tactics/maps/four-hands-and-a-promise": "four-hands-and-a-promise",
    "every-villain-tactics/maps/probability-of-panic": "probability-of-panic",
    "every-villain-tactics/maps/keys-to-the-shelter": "keys-to-the-shelter",
    "every-villain-tactics/maps/friend-nobody-remembers": "friend-nobody-remembers",
    "every-villain-tactics/maps/furnace-lift": "furnace-lift",
    "every-villain-tactics/maps/last-skyway": "last-skyway",
    "every-villain-tactics/maps/foundation-day": "foundation-day",
    "every-villain-tactics/maps/flooded-platform": "flooded-platform",
    "every-villain-tactics/maps/parade-that-couldnt-stop": "parade-that-couldnt-stop",
    "every-villain-tactics/maps/grandmas-password": "grandmas-password",
    "every-villain-tactics/maps/museum-of-tomorrow": "museum-of-tomorrow",
    "every-villain-tactics/maps/edited-rescue": "edited-rescue",
    "every-villain-tactics/maps/refuge-in-orbit": "refuge-in-orbit",
    "every-villain-tactics/maps/treaty-in-the-clouds": "treaty-in-the-clouds",
    "every-villain-tactics/maps/museum-that-moved": "museum-that-moved",
    "every-villain-tactics/maps/song-for-the-drowned": "song-for-the-drowned",
    "every-villain-tactics/maps/orders-from-home": "orders-from-home",
    "every-villain-tactics/maps/small-future": "small-future",
    "every-villain-tactics/maps/missing-coronation": "missing-coronation",
    "every-villain-tactics/maps/everyone-inside": "everyone-inside",
    "every-villain-tactics/maps/match-under-the-bed": "match-under-the-bed",
    "every-villain-tactics/maps/elevator-that-floated": "elevator-that-floated",
    "every-villain-tactics/maps/stone-that-testified": "stone-that-testified",
    "every-villain-tactics/maps/letter-no-one-sent": "letter-no-one-sent",
    "every-villain-tactics/maps/book-that-walked-away": "book-that-walked-away",
    "every-villain-tactics/maps/thought-that-wasnt-yours": "thought-that-wasnt-yours",
    "every-villain-tactics/maps/prophecy-auction": "prophecy-auction",
    "every-villain-tactics/maps/rumor-after-midnight": "rumor-after-midnight",
}
HASH = re.compile(r"^[a-f0-9]{64}$")


def receipts_from_ledgers(ledger_dir: Path) -> dict[str, dict[str, str | int]]:
    results: dict[str, dict[str, str | int]] = {}
    for ledger_path in sorted(ledger_dir.glob("*.yaml")):
        ledger = yaml.safe_load(ledger_path.read_text(encoding="utf-8")) or {}
        if not isinstance(ledger, dict) or ledger.get("is_public") is not False:
            continue
        for subject in ledger.get("subjects", []):
            if not isinstance(subject, dict):
                continue
            asset = subject.get("asset")
            stage = STAGES_BY_ASSET.get(asset)
            if stage is None:
                continue
            for lane, proof in (subject.get("media_proof") or {}).items():
                if not isinstance(proof, dict) or proof.get("status") != "VERIFIED":
                    continue
                job_id = proof.get("art_job_id")
                image_id = proof.get("art_image_id")
                art = (subject.get("art") or {}).get(lane) or {}
                job = (subject.get("jobs") or {}).get(lane)
                size = subject.get("size")
                if not (
                    isinstance(job_id, int) and job_id > 0
                    and isinstance(image_id, int) and image_id > 0
                    and job == job_id
                    and art.get("status") == "DONE"
                    and art.get("art_image_id") == image_id
                    and isinstance(size, str) and "x" in size
                    and proof.get("aspect_match") is True
                    and proof.get("blank_check") == "PASS"
                    and isinstance(proof.get("downloaded_bytes"), int)
                    and proof["downloaded_bytes"] > 0
                    and HASH.fullmatch(str(proof.get("pixel_sha256", "")))
                ):
                    raise ValueError(
                        f"{ledger_path.name}:{asset} has an inconsistent VERIFIED receipt"
                    )
                expected_w, expected_h = (int(v) for v in size.split("x", 1))
                if (proof.get("width"), proof.get("height")) != (
                    expected_w, expected_h
                ):
                    raise ValueError(f"{ledger_path.name}:{asset} has wrong dimensions")
                receipt: dict[str, str | int] = {
                    "artKey": str(asset),
                    "jobId": job_id,
                    "imageId": image_id,
                    "sourceLedger": ledger_path.name,
                }
                if stage in results and results[stage] != receipt:
                    raise ValueError(f"conflicting VERIFIED art for stage {stage}")
                results[stage] = receipt
    return dict(sorted(results.items()))


def render_typescript(receipts: dict[str, dict[str, str | int]]) -> str:
    lines = [
        "// GENERATED by conductor/scripts/export_verified_tactics_arenas.py",
        "// Only authenticated private media proofs qualify; art approval is separate.",
        "export const VERIFIED_EVT_ARENA_RECEIPTS = {",
    ]
    for stage, receipt in sorted(receipts.items()):
        lines.extend(
            [
                f"  '{stage}': {{",
                f"    artKey: '{receipt['artKey']}',",
                f"    jobId: {receipt['jobId']},",
                f"    imageId: {receipt['imageId']},",
                f"    sourceLedger: '{receipt['sourceLedger']}',",
                "  },",
            ]
        )
    lines.extend(["} as const", ""])
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ledger-dir", type=Path, default=PROJECT)
    parser.add_argument("--out", type=Path)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    generated = render_typescript(receipts_from_ledgers(args.ledger_dir))
    if args.check:
        if not args.out or not args.out.is_file():
            parser.error("--check requires --out pointing to an existing file")
        if args.out.read_text(encoding="utf-8") != generated:
            raise SystemExit("verified arena receipts are stale: regenerate before shipping")
        print("verified arena receipts match ledgers")
        return 0
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(generated, encoding="utf-8")
        print(f"wrote {args.out}")
    else:
        print(generated, end="")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
