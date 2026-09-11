#!/usr/bin/env python3
"""Validate changed, unbuilt Daily Dream proposals against the creative-diversity contract.

This is intentionally separate from the LLM author. Manual/backstop proposals must clear the
same history-aware story and naming checks before they can become tomorrow's steering input.
Built historical files are ignored because later art/evidence bookkeeping must not retroactively
invalidate old worlds.
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


def _entropy_version_error(proposal: dict) -> str | None:
    """Require queued steering proposals to have been seeded under today's entropy rules.

    Built history remains immutable evidence, but an unbuilt proposal is still steering input.
    Letting an old unversioned docket item build under a newer contract defeats seed cooldowns:
    the prose validator sees the already-chosen Facets and cannot retroactively undraw them.
    """
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
    if _frontmatter_value(text, "proposal").casefold() not in {"true", "yes"}:
        return []
    status = (_frontmatter_value(text, "status") or "outline").casefold()
    if status not in {"outline", "ready", "retry"}:
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
    paths = [Path(value) for value in (argv if argv is not None else sys.argv[1:])]
    failures = 0
    checked = 0
    for path in paths:
        if "projects/dream-cycle/backlog" not in path.as_posix():
            continue
        errors = validate_path(path)
        if not path.exists():
            continue
        text = path.read_text(encoding="utf-8")
        status = (_frontmatter_value(text, "status") or "outline").casefold()
        if status not in {"outline", "ready", "retry"}:
            continue
        checked += 1
        if errors:
            failures += 1
            print(f"{path}: creative contract failed", file=sys.stderr)
            for error in errors:
                print(f"  - {error}", file=sys.stderr)
        else:
            print(f"{path}: creative contract passed")
    print(f"Daily Dream creative contract: {checked} steering proposal(s) checked, {failures} failed.")
    return 1 if failures else 0


if __name__ == "__main__":
    raise SystemExit(main())
