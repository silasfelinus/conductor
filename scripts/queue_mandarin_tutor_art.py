#!/usr/bin/env python3
"""Stage deterministic Mandarin Tutor v2 illustration requests for the shared art lane.

The Kind Robots Mandarin catalog remains the vocabulary source of truth. This
script fetches its derived /api/mandarin/art-manifest, writes an auditable local
snapshot, and appends every missing v2 `illustrate` request to projects/art-prompts.yaml.

v2 is a deliberate full art-direction reset. Existing v1 assets or requests do
not satisfy a v2 card. The durable ArtJob queue can absorb the complete corpus
while the home renderer drains it at its own pace.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.request
from pathlib import Path
from typing import Any

import yaml

ROOT = Path(__file__).resolve().parent.parent
ART_PROMPTS = ROOT / "projects" / "art-prompts.yaml"
SNAPSHOT = ROOT / "projects" / "mandarin-tutor" / "art-manifest.json"
KR_BASE_URL = os.environ.get("KR_BASE_URL", "https://kindrobots.org").rstrip("/")
MANIFEST_URL = f"{KR_BASE_URL}/api/mandarin/art-manifest"
EXPECTED_RECIPE_VERSION = "v2"
EXPECTED_ART_DIRECTION_ID = "modern-chinese-picturebook-v2"
DEFAULT_BATCH_SIZE = 1000
MANDARIN_PRIORITY = 80
TOP_LEVEL_KEY = re.compile(r"^[A-Za-z0-9_-]+:\s*(?:#.*)?$")


def fetch_manifest(timeout: int = 30) -> dict[str, Any]:
    request = urllib.request.Request(
        MANIFEST_URL,
        method="GET",
        headers={"Accept": "application/json", "User-Agent": "conductor-mandarin-art/2"},
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except (urllib.error.URLError, TimeoutError, OSError, json.JSONDecodeError) as error:
        raise RuntimeError(f"Mandarin art manifest unavailable at {MANIFEST_URL}: {error}") from error

    if not isinstance(payload, dict) or payload.get("success") is not True:
        raise RuntimeError("Mandarin art manifest response was not successful.")
    data = payload.get("data")
    if not isinstance(data, dict) or not isinstance(data.get("entries"), list):
        raise RuntimeError("Mandarin art manifest response is missing data.entries.")
    return data


def load_manifest_file(path: Path) -> dict[str, Any]:
    """Read a manifest produced by a Kind Robots build that is not deployed yet.

    Production is self-hosted on Alexandria and updates on Silas's schedule, so
    a recipe fix can be correct, merged, and still unreachable by this script for
    days. `--manifest-file` lets the corpus be staged from a manifest generated
    by running the target branch locally and hitting its own
    /api/mandarin/art-manifest -- the same code path production will serve, just
    earlier.

    It is not a way around the manifest contract: the payload goes through the
    same validate_manifest as a fetched one, and the snapshot Conductor commits
    is the artifact that gets audited either way. Record which build produced it
    in the commit message.
    """
    payload = json.loads(path.read_text(encoding="utf-8"))
    # Accept both the raw manifest and a saved API envelope.
    data = payload.get("data") if isinstance(payload, dict) and "data" in payload else payload
    if not isinstance(data, dict) or not isinstance(data.get("entries"), list):
        raise RuntimeError(f"{path} does not contain a Mandarin art manifest.")
    return data


def validate_manifest(manifest: dict[str, Any]) -> list[dict[str, Any]]:
    recipe_version = str(manifest.get("recipeVersion") or "").strip()
    if recipe_version != EXPECTED_RECIPE_VERSION:
        raise RuntimeError(
            f"Expected Mandarin art recipe {EXPECTED_RECIPE_VERSION}, got {recipe_version or 'none'}."
        )
    art_direction = manifest.get("artDirection")
    art_direction_id = (
        str(art_direction.get("id") or "").strip() if isinstance(art_direction, dict) else ""
    )
    if art_direction_id != EXPECTED_ART_DIRECTION_ID:
        raise RuntimeError(
            f"Expected Mandarin art direction {EXPECTED_ART_DIRECTION_ID}, got {art_direction_id or 'none'}."
        )

    entries = manifest.get("entries")
    if not isinstance(entries, list):
        raise RuntimeError("Manifest entries must be a list.")

    expected_prefix = f"mandarin-tutor-{EXPECTED_RECIPE_VERSION}-"
    expected_path = f"public/images/mandarin-tutor/cards/{EXPECTED_RECIPE_VERSION}/"
    seen_ids: set[str] = set()
    seen_paths: set[str] = set()
    valid: list[dict[str, Any]] = []
    for index, raw in enumerate(entries):
        if not isinstance(raw, dict):
            raise RuntimeError(f"Manifest entry {index} is not an object.")
        request_id = str(raw.get("requestId") or "").strip()
        image_path = str(raw.get("imagePath") or "").strip()
        strategy = str(raw.get("strategy") or "").strip()
        prompt = raw.get("prompt")
        if not request_id.startswith(expected_prefix):
            raise RuntimeError(f"Manifest entry {index} has an invalid v2 requestId.")
        if not image_path.startswith(expected_path):
            raise RuntimeError(f"Manifest entry {request_id} has an invalid v2 imagePath.")
        if str(raw.get("artDirectionId") or "").strip() != EXPECTED_ART_DIRECTION_ID:
            raise RuntimeError(f"Manifest entry {request_id} has the wrong art direction.")
        if strategy not in {"illustrate", "glyph-only"}:
            raise RuntimeError(f"Manifest entry {request_id} has an invalid strategy.")
        if strategy == "illustrate" and not str(prompt or "").strip():
            raise RuntimeError(f"Illustrated manifest entry {request_id} has no prompt.")
        if request_id in seen_ids or image_path in seen_paths:
            raise RuntimeError(f"Manifest has a duplicate request id or image path at {request_id}.")
        seen_ids.add(request_id)
        seen_paths.add(image_path)
        valid.append(raw)
    return valid


def write_snapshot(manifest: dict[str, Any]) -> bool:
    SNAPSHOT.parent.mkdir(parents=True, exist_ok=True)
    rendered = json.dumps(manifest, ensure_ascii=False, indent=2, sort_keys=True) + "\n"
    previous = SNAPSHOT.read_text(encoding="utf-8") if SNAPSHOT.exists() else ""
    if previous == rendered:
        return False
    SNAPSHOT.write_text(rendered, encoding="utf-8")
    return True


def load_existing_requests() -> tuple[set[str], set[str]]:
    if not ART_PROMPTS.exists():
        return set(), set()
    data = yaml.safe_load(ART_PROMPTS.read_text(encoding="utf-8")) or {}
    requests = data.get("requests") if isinstance(data, dict) else []
    if not isinstance(requests, list):
        requests = []
    ids = {
        str(entry.get("id") or "").strip()
        for entry in requests
        if isinstance(entry, dict) and entry.get("id")
    }
    paths = {
        str(entry.get("image_path") or "").strip()
        for entry in requests
        if isinstance(entry, dict) and entry.get("image_path")
    }
    return ids, paths


def request_entry(raw: dict[str, Any]) -> dict[str, Any]:
    simplified = str(raw.get("simplified") or "").strip()
    pinyin = str(raw.get("pinyin") or "").strip()
    meaning = str(raw.get("meaning") or "").strip()
    image_path = str(raw["imagePath"]).strip()
    image_url = str(raw.get("imageUrl") or "").strip()
    prompt = " ".join(str(raw.get("prompt") or "").split())

    # The per-card framing/light/palette/handling/ground draw the recipe baked
    # into this prompt. Recorded so QA can tell a weak render apart from a weak
    # style draw without re-deriving anything.
    manifest_variant = raw.get("styleVariant")
    style_variant = (
        str(manifest_variant["id"])
        if isinstance(manifest_variant, dict) and manifest_variant.get("id")
        else ""
    )

    label_parts = [part for part in [simplified, pinyin, meaning] if part]
    return {
        "id": str(raw["requestId"]),
        "source": "mandarin-tutor",
        "status": "pending",
        "priority": MANDARIN_PRIORITY,
        "target_repo": "silasfelinus/kind_robots",
        "project_slug": "mandarin-tutor",
        "recipe_version": EXPECTED_RECIPE_VERSION,
        "art_direction_id": EXPECTED_ART_DIRECTION_ID,
        "style_variant": style_variant,
        "image_path": image_path,
        "source_url": f"https://media.acrocatranch.com{image_url}" if image_url.startswith("/") else image_url,
        "page_url": "https://kindrobots.org/play/mandarin",
        "variant": "image",
        "label": " · ".join(label_parts)[:240],
        "engine": str(raw.get("engine") or "krea2"),
        "size": f"{int(raw.get('width') or 768)}x{int(raw.get('height') or 768)}",
        "prompt": prompt,
    }


def render_request(entry: dict[str, Any]) -> str:
    return yaml.safe_dump(
        [entry],
        allow_unicode=True,
        default_flow_style=False,
        sort_keys=False,
        width=1000,
    ).rstrip() + "\n"


def append_request_blocks(blocks: list[str]) -> None:
    if not blocks:
        return
    text = ART_PROMPTS.read_text(encoding="utf-8") if ART_PROMPTS.exists() else "requests:\n"
    lines = text.splitlines(keepends=True)
    request_index = next(
        (index for index, line in enumerate(lines) if line.strip() == "requests:" and not line.startswith((" ", "\t"))),
        None,
    )
    if request_index is None:
        if text and not text.endswith("\n"):
            text += "\n"
        text += "requests:\n" + "".join(blocks)
        ART_PROMPTS.write_text(text, encoding="utf-8")
        return

    insert_at = len(lines)
    for index in range(request_index + 1, len(lines)):
        line = lines[index]
        if line.startswith((" ", "\t")) or not line.strip() or line.lstrip().startswith("#"):
            continue
        if TOP_LEVEL_KEY.match(line.rstrip("\n")):
            insert_at = index
            break

    lines.insert(insert_at, "".join(blocks))
    ART_PROMPTS.write_text("".join(lines), encoding="utf-8")


def queue_batch(manifest: dict[str, Any], batch_size: int) -> dict[str, int]:
    entries = validate_manifest(manifest)
    existing_ids, existing_paths = load_existing_requests()
    illustrated = [entry for entry in entries if entry.get("strategy") == "illustrate"]
    glyph_only = [entry for entry in entries if entry.get("strategy") == "glyph-only"]
    missing = [
        entry
        for entry in illustrated
        if str(entry.get("requestId") or "") not in existing_ids
        and str(entry.get("imagePath") or "") not in existing_paths
    ]
    selected = missing[: max(0, batch_size)]
    staged = [request_entry(entry) for entry in selected]
    append_request_blocks([render_request(entry) for entry in staged])
    return {
        "total": len(entries),
        "illustrated": len(illustrated),
        "glyph_only": len(glyph_only),
        "already_staged": len(illustrated) - len(missing),
        "missing": len(missing),
        "queued": len(selected),
        "unvaried": sum(1 for entry in staged if not entry["style_variant"]),
        "distinct_variants": len({entry["style_variant"] for entry in staged if entry["style_variant"]}),
    }


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--batch-size",
        type=int,
        default=DEFAULT_BATCH_SIZE,
        help=f"maximum new Mandarin v2 requests to append (default {DEFAULT_BATCH_SIZE}, enough for the full core corpus)",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="fail when the public v2 manifest cannot be fetched instead of preserving the existing queue",
    )
    parser.add_argument(
        "--manifest-file",
        type=Path,
        default=None,
        help=(
            "stage from a manifest saved from a Kind Robots build instead of fetching the live one. "
            "For a recipe fix that is merged but not yet deployed to Alexandria; the payload still "
            "goes through the same validation. Record the producing build in the commit."
        ),
    )
    args = parser.parse_args(argv)
    if args.batch_size < 0:
        parser.error("--batch-size must be >= 0")

    try:
        manifest = (
            load_manifest_file(args.manifest_file) if args.manifest_file else fetch_manifest()
        )
        validate_manifest(manifest)
    except (RuntimeError, OSError, json.JSONDecodeError) as error:
        # An explicitly named file is always fatal: the fail-open path exists so
        # a scheduled run survives production being briefly unreachable, not so
        # an operator's typo silently stages nothing.
        if args.strict or args.manifest_file:
            print(f"ERROR: {error}", file=sys.stderr)
            return 1
        print(f"WARNING: {error}; preserving the current Mandarin art queue.", file=sys.stderr)
        return 0

    snapshot_changed = write_snapshot(manifest)
    summary = queue_batch(manifest, args.batch_size)
    print(
        "Mandarin v2 art manifest: "
        f"{summary['total']} core cards, {summary['illustrated']} illustrated, "
        f"{summary['glyph_only']} glyph-only."
    )
    print(
        "v2 queue state: "
        f"{summary['already_staged']} already staged, {summary['missing']} still missing, "
        f"{summary['queued']} appended this run."
    )
    if summary["queued"]:
        print(f"v2 style draws: {summary['distinct_variants']} distinct across {summary['queued']} cards.")
        if summary["unvaried"]:
            print(
                f"WARNING: {summary['unvaried']} staged card(s) carry no styleVariant. That manifest "
                "predates the per-card style draw, so those prompts are all in one style.",
                file=sys.stderr,
            )
    print(f"Manifest snapshot {'updated' if snapshot_changed else 'unchanged'}: {SNAPSHOT.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
