#!/usr/bin/env python3
"""Retry the bounded Daily Dream identity repair with an approved fresh bundle slug.

A globally-unique Dream slug can be occupied by a private legacy row that the repair
credential is not authorized to enumerate. Rather than weaken Dream privacy or delete
that hidden row, this wrapper temporarily moves only the approved collision victim to
a fresh technical slug for the live rebuild. The source slug and proposal-data slug are
persisted only if the complete rebuild, art reattachment, Facets, and live verification
succeed. On any failure, the source file is restored byte-for-byte.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from pathlib import Path
from typing import Any

sys.path.insert(0, str(Path(__file__).resolve().parent))

import rebuild_dream_identity_collision as repair  # noqa: E402
import retry_dream_identity_collision_by_slug as slug_retry  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
REPAIR_DIR = ROOT / "projects" / "dream-cycle" / "record-repairs"
SLUG_RE = re.compile(r"^[a-z0-9]+(?:-[a-z0-9]+)*$")


def _replacement_slugs(request: dict[str, Any]) -> dict[str, str]:
    raw = request.get("replacement_slugs")
    if not isinstance(raw, dict) or not raw:
        raise ValueError("request must include replacement_slugs")
    replacements: dict[str, str] = {}
    bundles = set(request.get("bundles") or [])
    for relative_path, slug in raw.items():
        if relative_path not in bundles:
            raise ValueError(f"replacement slug targets unapproved bundle: {relative_path}")
        if not isinstance(slug, str) or not SLUG_RE.fullmatch(slug):
            raise ValueError(f"invalid replacement slug for {relative_path}: {slug!r}")
        replacements[str(relative_path)] = slug
    return replacements


def _replace_source_slug(text: str, new_slug: str) -> tuple[str, str]:
    fm_match = re.search(r"^slug:\s*([^\n]+)$", text, flags=re.MULTILINE)
    if not fm_match:
        raise ValueError("source has no frontmatter slug")
    old_slug = fm_match.group(1).strip().strip("'\"")
    if old_slug == new_slug:
        return text, old_slug

    text, count = re.subn(
        r"^slug:\s*[^\n]+$",
        f"slug: {new_slug}",
        text,
        count=1,
        flags=re.MULTILINE,
    )
    if count != 1:
        raise ValueError("could not replace frontmatter slug exactly once")

    proposal = repair.records._data_block(text, "proposal-data")
    if not isinstance(proposal, dict):
        raise ValueError("source has no proposal-data")
    if str(proposal.get("slug") or "") != old_slug:
        raise ValueError(
            f"proposal-data slug {proposal.get('slug')!r} does not match frontmatter {old_slug!r}"
        )
    proposal["slug"] = new_slug
    block = "<!-- proposal-data\n" + json.dumps(proposal, ensure_ascii=False) + "\n-->"
    text, count = re.subn(
        r"<!--\s*proposal-data\s*\n.*?\n-->",
        lambda _: block,
        text,
        count=1,
        flags=re.DOTALL,
    )
    if count != 1:
        raise ValueError("could not replace proposal-data exactly once")
    return text, old_slug


def _slug_tolerant_history_validator(current_proposal: dict[str, Any], historical_text: str):
    historical_proposal = repair.records._data_block(historical_text, "proposal-data")
    historical_built = repair.records._data_block(historical_text, "built-data")
    if not isinstance(historical_proposal, dict) or not isinstance(historical_built, dict):
        raise ValueError("historical source lacks proposal-data or built-data")
    current_compare = dict(current_proposal)
    historical_compare = dict(historical_proposal)
    current_compare.pop("slug", None)
    historical_compare.pop("slug", None)
    if current_compare != historical_compare:
        raise ValueError("historical source proposal differs beyond the approved technical slug replacement")
    repair.art_by_role(historical_built)
    return historical_built


def run(request_path: Path) -> dict[str, Any]:
    request = json.loads(request_path.read_text(encoding="utf-8"))
    if not isinstance(request, dict):
        raise ValueError("identity rebuild request must be a JSON object")
    repair.validate_request(request)
    replacements = _replacement_slugs(request)

    originals: dict[Path, str] = {}
    applied: list[dict[str, str]] = []
    for relative_path, new_slug in replacements.items():
        path = (ROOT / relative_path).resolve()
        if path.parent != repair.BACKLOG.resolve():
            raise ValueError(f"replacement path is outside dream-cycle backlog: {relative_path}")
        original = path.read_text(encoding="utf-8")
        originals[path] = original
        revised, old_slug = _replace_source_slug(original, new_slug)
        if old_slug == new_slug:
            raise ValueError(f"replacement slug is not a replacement for {relative_path}")
        path.write_text(revised, encoding="utf-8")
        applied.append({"path": relative_path, "old_slug": old_slug, "new_slug": new_slug})
        print(f"  staged technical slug replacement: {old_slug} -> {new_slug}")

    original_validator = repair._validate_history
    repair._validate_history = _slug_tolerant_history_validator
    try:
        receipt = slug_retry.run(request_path)
    except Exception:
        for path, original in originals.items():
            path.write_text(original, encoding="utf-8")
        raise
    finally:
        repair._validate_history = original_validator

    receipt["replacement_slugs"] = applied
    receipt_path = request_path.with_name(request_path.name.replace("-request.json", "-receipt.json"))
    receipt_path.write_text(json.dumps(receipt, indent=2, ensure_ascii=False) + "\n", encoding="utf-8")
    return receipt


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("request", type=Path)
    args = parser.parse_args()
    request_path = args.request if args.request.is_absolute() else ROOT / args.request
    if request_path.parent.resolve() != REPAIR_DIR.resolve() or not request_path.name.endswith("-request.json"):
        raise SystemExit("request must be projects/dream-cycle/record-repairs/*-request.json")
    try:
        run(request_path)
    except Exception as error:  # noqa: BLE001
        print(f"identity rebuild fresh-slug retry failed: {error}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
