#!/usr/bin/env python3
"""Report whether delivered Ruler Hooked WebPs could be genuine alpha layers.

The existing art is a collection of opaque complete-scene vistas. This checker
never calls those pieces layered/composited merely because they are marked done.
It probes only the fixed Ruler Hooked media host, reads just the WebP header,
and reports missing/invalid/opaque files without modifying or enqueueing art.

Usage:
    python scripts/audit_ruler_hooked_alpha.py
    python scripts/audit_ruler_hooked_alpha.py --manifest projects/art-prompts.yaml
"""
from __future__ import annotations

import argparse
from concurrent.futures import ThreadPoolExecutor
import json
from pathlib import Path
from urllib.parse import urlparse
from urllib.request import Request, urlopen

import yaml

MEDIA_HOST = "media.acrocatranch.com"
MEDIA_PREFIX = "/images/ruler-hooked/"
MAX_BYTES = 64


def webp_alpha(header: bytes) -> str:
    """alpha, opaque, or invalid from RIFF/VP8X/VP8L/VP8 header bits."""
    if len(header) < 21 or header[:4] != b"RIFF" or header[8:12] != b"WEBP":
        return "invalid"
    chunk = header[12:16]
    if chunk == b"VP8X":
        return "alpha" if header[20] & 0x10 else "opaque"
    if chunk == b"VP8 ":
        return "opaque"
    if chunk == b"VP8L":
        if len(header) < 25 or header[20] != 0x2F:
            return "invalid"
        bits = int.from_bytes(header[21:25], "little")
        return "alpha" if bits & (1 << 28) else "opaque"
    return "invalid"


def delivered_region_requests(path: Path) -> list[dict]:
    rows = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
    return sorted(
        (
            row
            for row in rows.get("requests", [])
            if row.get("project_slug") == "ruler-hooked"
            and row.get("lane") == "layer"
            and row.get("status") == "done"
        ),
        key=lambda row: str(row.get("id", "")),
    )


def inspect(row: dict, *, remote: bool) -> dict:
    url = str(row.get("source_url") or "")
    parsed = urlparse(url)
    result = {
        "id": str(row.get("id", "")),
        "image_path": str(row.get("image_path", "")),
        "art_job_id": row.get("last_art_job_id"),
        "result": "unavailable",
    }
    if (
        parsed.scheme != "https"
        or parsed.hostname != MEDIA_HOST
        or not parsed.path.startswith(MEDIA_PREFIX)
    ):
        result["result"] = "invalid-url"
        return result
    if not remote:
        return result
    request = Request(
        url,
        headers={
            "Range": "bytes=0-63",
            "User-Agent": "Conductor-RulerHooked-AlphaAudit/1.0",
        },
    )
    try:
        with urlopen(request, timeout=4) as response:
            data = response.read(MAX_BYTES)
        result["result"] = webp_alpha(data)
    except (OSError, ValueError, TimeoutError) as exc:
        result["error"] = type(exc).__name__
    return result


def audit(manifest: Path, *, remote: bool = True) -> dict:
    rows = delivered_region_requests(manifest)
    with ThreadPoolExecutor(max_workers=8) as pool:
        entries = list(pool.map(lambda row: inspect(row, remote=remote), rows))
    counts = {
        name: sum(row["result"] == name for row in entries)
        for name in ("alpha", "opaque", "invalid", "invalid-url", "unavailable")
    }
    return {"total": len(entries), "counts": counts, "entries": entries}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--manifest", type=Path, default=Path("projects/art-prompts.yaml")
    )
    parser.add_argument(
        "--offline",
        action="store_true",
        help="validate manifest/URL selection without requesting media",
    )
    parser.add_argument("--json", type=Path, help="write the complete audit JSON")
    args = parser.parse_args()
    report = audit(args.manifest, remote=not args.offline)
    print(
        f"Ruler Hooked delivered region assets: {report['total']}, "
        + ", ".join(f"{key}={value}" for key, value in report["counts"].items())
    )
    for row in report["entries"]:
        if row["result"] != "alpha":
            print(
                f"  {row['id']}: {row['result']} "
                f"(ArtJob {row['art_job_id']}, {row['image_path']})"
            )
    if args.json:
        args.json.parent.mkdir(parents=True, exist_ok=True)
        args.json.write_text(
            json.dumps(report, indent=2, sort_keys=True) + "\n", encoding="utf-8"
        )
    # Existing opaque vistas are known and legitimate. This is a report-only
    # quality guard; no alpha is asserted and network outages are not failures.
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
