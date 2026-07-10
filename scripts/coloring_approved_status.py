#!/usr/bin/env python3
"""Report approved coloring-book masters without mutating generation queues.

The report intentionally distinguishes:
- approvals explicitly recorded in approved/manifest.yaml;
- files physically present in approved/;
- filename/path anomalies that need human cleanup.

Existing exploratory art queues remain active. This script is a preflight, not a queue editor.
"""

from __future__ import annotations

import argparse
import json
import re
import sys
from difflib import SequenceMatcher
from pathlib import Path
from typing import Any

import yaml

DEFAULT_SET_DIR = Path("projects/coloring-book/sets/monster-recast")
ASSET_PATTERN = re.compile(r"^(?P<slug>.+)-(?P<variant>color|bw)\.webp$", re.IGNORECASE)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--set-dir",
        type=Path,
        default=DEFAULT_SET_DIR,
        help=f"Coloring-book set directory (default: {DEFAULT_SET_DIR})",
    )
    parser.add_argument("--json", action="store_true", help="Print JSON instead of Markdown")
    parser.add_argument(
        "--check",
        action="store_true",
        help="Exit nonzero only for broken manifest references or malformed data",
    )
    parser.add_argument(
        "--strict",
        action="store_true",
        help="Also fail on warnings such as unmanifested files or likely filename typos",
    )
    return parser.parse_args()


def load_manifest(path: Path) -> dict[str, Any]:
    if not path.exists():
        raise FileNotFoundError(f"Missing approval manifest: {path}")
    raw = yaml.safe_load(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict):
        raise ValueError(f"Approval manifest must contain a mapping: {path}")
    approvals = raw.get("confirmed_approvals")
    if not isinstance(approvals, list):
        raise ValueError("manifest confirmed_approvals must be a list")
    return raw


def scan_approved(approved_dir: Path) -> dict[str, dict[str, str]]:
    discovered: dict[str, dict[str, str]] = {}
    if not approved_dir.exists():
        return discovered
    for path in sorted(approved_dir.glob("*.webp")):
        match = ASSET_PATTERN.match(path.name)
        if not match:
            discovered.setdefault("__unparsed__", {})[path.name] = path.as_posix()
            continue
        slug = match.group("slug")
        variant = match.group("variant").lower()
        discovered.setdefault(slug, {})[variant] = path.as_posix()
    return discovered


def relative_to_set(path: Path, set_dir: Path) -> str:
    try:
        return path.relative_to(set_dir).as_posix()
    except ValueError:
        return path.as_posix()


def fuzzy_pair_warnings(discovered: dict[str, dict[str, str]]) -> list[str]:
    color_only = [slug for slug, variants in discovered.items() if slug != "__unparsed__" and "color" in variants and "bw" not in variants]
    bw_only = [slug for slug, variants in discovered.items() if slug != "__unparsed__" and "bw" in variants and "color" not in variants]
    warnings: list[str] = []
    for color_slug in color_only:
        best_slug = None
        best_score = 0.0
        for bw_slug in bw_only:
            score = SequenceMatcher(a=color_slug, b=bw_slug).ratio()
            if score > best_score:
                best_score = score
                best_slug = bw_slug
        if best_slug and best_score >= 0.82:
            warnings.append(
                f"Likely filename typo: color slug '{color_slug}' and BW slug '{best_slug}' "
                f"look like one pair ({best_score:.0%} similarity)."
            )
    return warnings


def build_report(set_dir: Path) -> tuple[dict[str, Any], list[str], list[str]]:
    manifest_path = set_dir / "approved" / "manifest.yaml"
    manifest = load_manifest(manifest_path)
    approvals = manifest["confirmed_approvals"]
    discovered_raw = scan_approved(set_dir / "approved")

    errors: list[str] = []
    warnings: list[str] = []
    confirmed: list[dict[str, Any]] = []
    manifest_paths: set[str] = set()

    for entry in approvals:
        if not isinstance(entry, dict):
            errors.append("Every confirmed_approvals entry must be a mapping")
            continue
        missing_fields = [field for field in ("concept_id", "slug", "label", "status", "color") if not entry.get(field)]
        if missing_fields:
            errors.append(f"Approval entry is missing required fields {missing_fields}: {entry!r}")
            continue

        resolved: dict[str, Any] = {
            "concept_id": str(entry["concept_id"]),
            "slug": str(entry["slug"]),
            "label": str(entry["label"]),
            "status": str(entry["status"]),
            "notes": entry.get("notes", []),
        }
        for variant in ("color", "bw"):
            configured = entry.get(variant)
            if configured is None:
                resolved[variant] = None
                resolved[f"{variant}_exists"] = False
                continue
            configured_str = str(configured)
            manifest_paths.add(configured_str)
            asset_path = set_dir / configured_str
            exists = asset_path.is_file()
            resolved[variant] = configured_str
            resolved[f"{variant}_exists"] = exists
            if not exists:
                errors.append(f"{entry['label']}: missing configured {variant} asset {configured_str}")
        confirmed.append(resolved)

    discovered: list[dict[str, Any]] = []
    for slug, variants in sorted(discovered_raw.items()):
        if slug == "__unparsed__":
            for filename, path in sorted(variants.items()):
                warnings.append(f"Unrecognized approved filename: {filename}")
                discovered.append({"slug": filename, "status": "unparsed", "files": [relative_to_set(Path(path), set_dir)]})
            continue
        files = {variant: relative_to_set(Path(path), set_dir) for variant, path in variants.items()}
        status = "complete-pair" if {"color", "bw"}.issubset(variants) else "incomplete-pair"
        discovered.append({"slug": slug, "status": status, **files})
        for path in files.values():
            if path not in manifest_paths:
                warnings.append(f"Approved-folder asset is not referenced by the confirmation manifest: {path}")

    warnings.extend(fuzzy_pair_warnings(discovered_raw))

    queue_policy = manifest.get("queue_policy", {})
    report = {
        "set": manifest.get("set", set_dir.name),
        "manifest": relative_to_set(manifest_path, set_dir),
        "queue_policy": queue_policy,
        "confirmed_approvals": confirmed,
        "discovered_approved_assets": discovered,
        "errors": errors,
        "warnings": warnings,
    }
    return report, errors, warnings


def render_markdown(report: dict[str, Any]) -> str:
    lines = [f"# Approved design preflight — {report['set']}", ""]
    queue_policy = report.get("queue_policy", {})
    queue_active = bool(queue_policy.get("exploratory_queue_remains_active"))
    lines.append(f"Exploratory queue remains active: **{'yes' if queue_active else 'no'}**")
    if queue_policy.get("note"):
        lines.extend(["", str(queue_policy["note"]).strip()])

    lines.extend(["", "## Confirmed approvals", ""])
    for item in report["confirmed_approvals"]:
        color = item["color"] or "—"
        bw = item["bw"] or "—"
        color_mark = "✓" if item["color_exists"] else "✗"
        bw_mark = "✓" if item["bw_exists"] else "○"
        lines.append(
            f"- **{item['label']}** (`{item['concept_id']}` / `{item['slug']}`) — {item['status']}  "
            f"\n  color {color_mark} `{color}`  \n  BW {bw_mark} `{bw}`"
        )

    lines.extend(["", "## Files discovered in approved/", ""])
    if report["discovered_approved_assets"]:
        for item in report["discovered_approved_assets"]:
            paths = [f"{key}: `{value}`" for key, value in item.items() if key not in {"slug", "status", "files"}]
            if item.get("files"):
                paths.extend(f"`{value}`" for value in item["files"])
            lines.append(f"- **{item['slug']}** — {item['status']}" + (f" — {', '.join(paths)}" if paths else ""))
    else:
        lines.append("- No WebP assets found in approved/.")

    if report["warnings"]:
        lines.extend(["", "## Warnings", ""])
        lines.extend(f"- {warning}" for warning in report["warnings"])
    if report["errors"]:
        lines.extend(["", "## Errors", ""])
        lines.extend(f"- {error}" for error in report["errors"])

    lines.extend(
        [
            "",
            "## Production rule",
            "",
            "Use approved masters for production and conversion. Continue the existing exploratory queue in its current order; queued renders do not replace an approval unless Silas explicitly promotes them.",
        ]
    )
    return "\n".join(lines) + "\n"


def main() -> int:
    args = parse_args()
    try:
        report, errors, warnings = build_report(args.set_dir)
    except (FileNotFoundError, ValueError, yaml.YAMLError) as exc:
        print(f"ERROR: {exc}", file=sys.stderr)
        return 2

    if args.json:
        print(json.dumps(report, indent=2, sort_keys=True))
    else:
        print(render_markdown(report), end="")

    if args.strict and (errors or warnings):
        return 1
    if args.check and errors:
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
