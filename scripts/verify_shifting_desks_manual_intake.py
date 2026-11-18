#!/usr/bin/env python3
"""Read-only check that live Shifting Desks art matches manually supplied files.

Compares complete served WebP bytes to the SHA-256 manifest. A 200, image MIME
type, or an old ArtJob is not evidence that the user-installed replacement
landed. Emits JSON even on failures; never approves ROUND-19 or edits assets.
"""
from __future__ import annotations

import argparse
import hashlib
import io
import json
from pathlib import Path
from urllib.error import HTTPError, URLError
from urllib.parse import quote
from urllib.request import Request, urlopen

from PIL import Image, UnidentifiedImageError

ROOT = Path(__file__).resolve().parents[1]
MANIFEST = ROOT / "projects/shifting-desks/art/MANUAL-CLASSIC-2026-11-17.json"
DEFAULT_BASE_URL = "https://kindrobots.org"


def verify_image(row: dict, base_url: str, timeout: float = 15, opener=urlopen) -> dict:
    path = row["path"]
    if path.startswith("/") or ".." in Path(path).parts or not path.endswith(".webp"):
        raise ValueError(f"Unsafe image path: {path!r}")
    url = base_url.rstrip("/") + "/images/shifting-desks/" + quote(path, safe="/")
    result = {"path": path, "url": url, "state": "unverified",
              "expected_sha256": row["sha256"], "expected_dimensions": [row["width"], row["height"]]}
    try:
        request = Request(url, headers={"User-Agent": "Conductor-Shifting-Desks-art-acceptance/1"})
        with opener(request, timeout=timeout) as response:
            raw = response.read(15 * 1024 * 1024 + 1)
            result["status"] = getattr(response, "status", None)
            result["mime"] = response.headers.get("Content-Type", "").split(";")[0].strip().lower()
            result["last_modified"] = response.headers.get("Last-Modified")
        result["bytes"] = len(raw)
        result["sha256"] = hashlib.sha256(raw).hexdigest()
        if len(raw) > 15 * 1024 * 1024:
            result["reason"] = "Image exceeds 15 MB evidence limit"
            return result
        if result["status"] != 200 or result["mime"] != "image/webp":
            result["reason"] = "HTTP or content type mismatch"
            return result
        try:
            with Image.open(io.BytesIO(raw)) as photo:
                result["dimensions"] = list(photo.size)
                result["format"] = photo.format
                photo.verify()
        except (UnidentifiedImageError, OSError, ValueError) as exc:
            result["reason"] = f"Image decode failed: {type(exc).__name__}"
            return result
        if result["format"] != "WEBP" or result["dimensions"] != result["expected_dimensions"]:
            result["reason"] = "WebP format or image dimensions mismatch"
        elif result["sha256"] != result["expected_sha256"]:
            result["reason"] = "Served image bytes differ from the approved manual replacement"
        else:
            result["state"] = "match"
    except (HTTPError, URLError, OSError, TimeoutError) as exc:
        result["reason"] = f"{type(exc).__name__}: {str(exc)[:220]}"
    return result


def verify_manifest(document: dict, base_url: str, timeout: float = 15, opener=urlopen) -> dict:
    rows = document["images"]
    if len(rows) != 14 or len({row["path"] for row in rows}) != 14:
        raise ValueError("Expected fourteen unique Classic replacement targets")
    checked = [verify_image(row, base_url, timeout=timeout, opener=opener) for row in rows]
    matched = sum(item["state"] == "match" for item in checked)
    return {"project": "shifting-desks", "checked": len(checked), "matched": matched,
            "unverified": len(checked) - matched, "ready": matched == 14,
            "results": checked,
            "meaning": "Byte match only; not editorial art acceptance, live frame testing, or playtest clearance"}


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--manifest", type=Path, default=MANIFEST)
    parser.add_argument("--base-url", default=DEFAULT_BASE_URL)
    parser.add_argument("--timeout", type=float, default=15)
    parser.add_argument("--output", type=Path)
    parser.add_argument("--strict", action="store_true", help="Fail if any expected live image differs")
    args = parser.parse_args()
    document = json.loads(args.manifest.read_text(encoding="utf-8"))
    result = verify_manifest(document, args.base_url, args.timeout)
    report = json.dumps(result, indent=2) + "\n"
    if args.output:
        args.output.parent.mkdir(parents=True, exist_ok=True)
        args.output.write_text(report, encoding="utf-8")
    print(f"Shifting Desks installed art: {result['matched']}/{result['checked']} exact live-file matches")
    for row in result["results"]:
        if row["state"] != "match":
            print(f"  VERIFY: {row['path']}: {row.get('reason', 'unknown')}")
    return 1 if args.strict and not result["ready"] else 0


if __name__ == "__main__":
    raise SystemExit(main())
