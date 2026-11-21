#!/usr/bin/env python3
"""Read-only, deduplicated Emperor ArtJob -> ArtImage -> export -> reference audit.

The local Kind Robots checkout is optional. No network calls, credentials, or mutations.
A DONE ArtImage in a ledger is *not* proof of a delivered file.
"""
from __future__ import annotations

import argparse
import json
import re
from collections import defaultdict
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parent.parent
LEDGERS = ROOT / "projects/emperor-of-dust/art"
MEDIA = Path("public/emperor-of-dust")
REFERENCE_DIRS = ("utils/emperorOfDust", "pages", "components", "server", "content")


def subjects_from_ledgers(ledger_dir: Path):
    for path in sorted(ledger_dir.glob("*.yaml")):
        data = yaml.safe_load(path.read_text(encoding="utf-8")) or {}
        for subject in data.get("subjects") or []:
            if isinstance(subject, dict) and subject.get("asset"):
                yield path.name, subject


def scan_references(app_root: Path):
    """Reference hits are static evidence, never proof of runtime reachability."""
    hits = defaultdict(list)
    for dirname in REFERENCE_DIRS:
        root = app_root / dirname
        if not root.exists():
            continue
        for path in root.rglob("*"):
            if not path.is_file() or path.suffix not in (".ts", ".vue", ".json", ".md", ".yaml"):
                continue
            if path.stat().st_size > 2_000_000:
                continue
            try:
                content = path.read_text(encoding="utf-8")
            except UnicodeError:
                continue
            # Only Emperor-owned files can be evidence; scanning every server
            # file against ~900 assets made a real checkout run take minutes.
            if dirname != "utils/emperorOfDust" and "emperor" not in content.lower():
                continue
            hits[path.relative_to(app_root).as_posix()] = content
    return hits


# Runtime asset constructors verified against Kind Robots' fortress modules.
# These are *potential* references, not evidence that a player reached the image.
# Each pattern is enabled only when its corresponding builder is present in source.
RUNTIME_BUILDERS = (
    ("utils/emperorOfDust/fortress/questArt.ts", "questArtUrl", re.compile(r"^quests/[a-z0-9-]+$")),
    ("utils/emperorOfDust/fortress/chanceArt.ts", "chanceArtCandidates", re.compile(r"^chance-events/[a-z0-9-]+/[a-z0-9-]+$")),
    ("utils/emperorOfDust/fortress/audienceChoiceArt.ts", "audienceChoiceImages", re.compile(r"^audiences/[a-z0-9-]+/[a-z0-9-]+$")),
    ("utils/emperorOfDust/fortress/audienceChoiceArt.ts", "audienceChoiceImages", re.compile(r"^audiences/[a-z0-9-]+-(?:enter|[a-z0-9-]+)$")),
    ("utils/emperorOfDust/fortress/talkArt.ts", "talkArt", re.compile(r"^talks/[a-z0-9-]+/[a-z0-9-]+$")),
    ("utils/emperorOfDust/fortress/talkChoiceArt.ts", "talkChoice", re.compile(r"^talks/[a-z0-9-]+/[a-z0-9-]+$")),
)


def _exact_reference(asset: str, content: str) -> bool:
    """Avoid rooms/a matching rooms/ab or rooms/a-success."""
    token = re.escape(asset)
    return re.search(r"(?<![a-zA-Z0-9_-])" + token +
                     r"(?![a-zA-Z0-9_/-])", content) is not None


def runtime_reference_candidates(asset: str, references: dict[str, str]):
    """Potential runtime URL paths, kept separate from exact static references."""
    candidates = []
    for source, symbol, pattern in RUNTIME_BUILDERS:
        content = references.get(source, "")
        if pattern.fullmatch(asset) and re.search(r"\b" + re.escape(symbol) + r"\b", content):
            candidates.append(source)
    return sorted(set(candidates))


def _is_webp(path: Path) -> bool:
    """A nonempty file is not an export: require the RIFF....WEBP container signature."""
    if not path.is_file():
        return False
    with path.open("rb") as handle:
        header = handle.read(12)
    return len(header) == 12 and header[:4] == b"RIFF" and header[8:12] == b"WEBP"


def inventory(ledger_dir: Path, app_root: Path | None = None):
    grouped = defaultdict(list)
    for ledger, subject in subjects_from_ledgers(ledger_dir):
        asset = str(subject["asset"]).strip().removesuffix(".webp")
        if not asset or asset.startswith("/") or ".." in Path(asset).parts:
            raise ValueError(f"Unsafe asset path in {ledger}: {asset!r}")
        jobs = subject.get("jobs") or {}
        art = subject.get("art") or {}
        for lane in sorted(set(jobs) | set(art)):
            image = art.get(lane) or {}
            grouped[asset].append({
                "ledger": ledger, "subject": subject.get("key"), "lane": lane,
                "job_id": jobs.get(lane), "art_image_id": image.get("art_image_id"),
                "status": image.get("status"),
            })
        if not jobs and not art:
            grouped[asset].append({
                "ledger": ledger, "subject": subject.get("key"), "lane": None,
                "job_id": None, "art_image_id": None, "status": "NOT_SUBMITTED",
            })
    references = scan_references(app_root) if app_root else {}
    results = []
    for asset, entries in sorted(grouped.items()):
        path = f"public/emperor-of-dust/{asset}.webp"
        file_path = app_root / path if app_root else None
        exported = _is_webp(file_path) if file_path else None
        # A dynamic path assembled at runtime will not be detected by static text search.
        matches = [name for name, content in references.items()
                   if _exact_reference(asset, content)]
        runtime_candidates = runtime_reference_candidates(asset, references) if app_root else []
        image_ids = sorted({str(e["art_image_id"]) for e in entries if e["art_image_id"] is not None})
        job_ids = sorted({str(e["job_id"]) for e in entries if e["job_id"] is not None})
        results.append({
            "asset": asset, "media_path": path, "exported": exported,
            "reference_files": matches, "runtime_reference_candidates": runtime_candidates,
            "reference_class": ("static" if matches else
                                "runtime_candidate" if runtime_candidates else "unreferenced"),
            "job_ids": job_ids, "art_image_ids": image_ids,
            "render_records": entries, "has_done_image": any(
                e["status"] == "DONE" and e["art_image_id"] is not None for e in entries),
            "conflicting_image_ids": len(image_ids) > 1,
        })
    summary = {
        "unique_assets": len(results),
        "without_done_image": sum(not x["has_done_image"] for x in results),
        "with_done_image_no_export": sum(x["has_done_image"] and x["exported"] is False for x in results),
        "exported_without_static_reference": sum(x["exported"] is True and not x["reference_files"] for x in results),
        "exported_runtime_candidates": sum(x["exported"] is True and x["reference_class"] == "runtime_candidate" for x in results),
        "exported_without_known_reference": sum(x["exported"] is True and x["reference_class"] == "unreferenced" for x in results),
        "conflicting_image_ids": sum(x["conflicting_image_ids"] for x in results),
        "export_verification_available": app_root is not None,
    }
    return {"summary": summary, "assets": results}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--ledgers", type=Path, default=LEDGERS)
    parser.add_argument("--kind-robots", type=Path, help="local checkout root for real file and reference checks")
    parser.add_argument("--output", type=Path, help="write JSON audit here; stdout otherwise")
    args = parser.parse_args()
    report = inventory(args.ledgers, args.kind_robots)
    encoded = json.dumps(report, indent=2)
    if args.output:
        args.output.write_text(encoded + "\n", encoding="utf-8")
    else:
        print(encoded)


if __name__ == "__main__":
    main()
