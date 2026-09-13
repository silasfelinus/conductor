#!/usr/bin/env python3
"""Validate unbuilt Daily Dream proposals against the creative-diversity contract.

Built historical files are immutable evidence and are ignored. Open steering proposals are
live input, so a creative-contract change applies to the entire buffered runway, not merely
the newest or files touched by the same pull request. ``--all-open`` is the migration gate:
a contract/version bump cannot merge while any queued proposal still carries the old rules.
"""
from __future__ import annotations

import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))

import author_dream_proposal as author  # noqa: E402
import build_dream_proposal as proposals  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]
BACKLOG = ROOT / "projects" / "dream-cycle" / "backlog"
OPEN_STATUSES = {"outline", "ready", "retry"}


def _proposal_data(text: str) -> dict | None:
    match = re.search(r"<!--\s*proposal-data\s*\n(.*?)\n-->", text, re.DOTALL)
    if not match:
        return None
    try:
        value = json.loads(match.group(1))
    except json.JSONDecodeError:
        return None
    return value if isinstance(value, dict) else None


def _frontmatter_value(text: str, key: str) -> str:
    match = re.search(rf"(?m)^{re.escape(key)}:\s*['\"]?([^'\"\n]+)['\"]?\s*$", text)
    return match.group(1).strip() if match else ""


def _is_open_steering(text: str) -> bool:
    """Whether a file is still capable of steering a future live build."""
    if _frontmatter_value(text, "proposal").casefold() not in {"true", "yes"}:
        return False
    status = (_frontmatter_value(text, "status") or "outline").casefold()
    if status not in OPEN_STATUSES:
        return False
    return re.search(r"<!--\s*built-data", text) is None


def _entropy_version_error(proposal: dict) -> str | None:
    """Require queued steering proposals to have been seeded under today's entropy rules."""
    seeds = proposal.get("seed_facets")
    raw = seeds.get("creative_entropy_version") if isinstance(seeds, dict) else None
    try:
        version = int(raw or 0)
    except (TypeError, ValueError):
        version = 0
    current = proposals.CREATIVE_ENTROPY_VERSION
    if version >= current:
        return None
    return (
        f"proposal creative entropy version {version} predates current version {current}; "
        "re-author it from the current brief so aquatic, semantic-family, Facet, title, and "
        "structural cooldowns are applied before any live records are built"
    )


def validate_path(path: Path) -> list[str]:
    if not path.exists() or path.suffix != ".md" or path.name.startswith("_"):
        return []
    text = path.read_text(encoding="utf-8")
    if not _is_open_steering(text):
        return []
    day = _frontmatter_value(text, "proposal_date") or _frontmatter_value(text, "created")
    proposal = _proposal_data(text)
    if not day or proposal is None:
        return ["missing proposal date or proposal-data block"]

    errors = proposals.validate_proposal(proposal)
    entropy_error = _entropy_version_error(proposal)
    if entropy_error:
        errors.append(entropy_error)

    premise_history = author.recent_premise_history(day)
    name_history = author.recent_name_history(day)
    errors.extend(
        author.story_diversity_complaints(
            proposal,
            premise_history,
            proposal.get("seed_facets"),
        )
    )
    characters = proposal.get("characters") or []
    if characters and isinstance(characters[0], dict):
        errors.extend(
            author.name_diversity_complaints(
                str(characters[0].get("name") or ""),
                name_history.get("characters", []),
            )
        )
    return errors


def main(argv: list[str] | None = None) -> int:
    values = list(argv if argv is not None else sys.argv[1:])
    all_open = "--all-open" in values
    paths = [Path(value) for value in values if value != "--all-open"]
    if all_open:
        paths.extend(sorted(BACKLOG.glob("*.md")))

    # Keep command-line order for useful CI output while avoiding duplicate work when a
    # changed proposal also belongs to the whole-buffer scan.
    unique: list[Path] = []
    seen: set[str] = set()
    for path in paths:
        key = path.as_posix()
        if key not in seen:
            seen.add(key)
            unique.append(path)

    failures = 0
    checked = 0
    for path in unique:
        if "projects/dream-cycle/backlog" not in path.as_posix() and not all_open:
            continue
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        if not _is_open_steering(text):
            continue
        checked += 1
        errors = validate_path(path)
        if errors:
            failures += 1
            print(f"{path}: creative contract failed", file=sys.stderr)
            for error in errors:
                print(f"  - {error}", file=sys.stderr)
        else:
            print(f"{path}: creative contract passed")
    print(f"Daily Dream creative contract: {checked} open steering proposal(s) checked, {failures} failed.")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
