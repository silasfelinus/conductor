#!/usr/bin/env python3
"""Attach persisted daily-dream seed Facets to newly built Kind Robots records.

``build_dream_records.py`` creates the records and art requests. This idempotent
sidecar runs immediately afterward, applies the proposal's live Facet selections
through the public model APIs, and records the result inside ``built-data`` for the
digest and future repair passes.
"""

from __future__ import annotations

import argparse
import json
import os
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from typing import Any, Iterable

ROOT = Path(__file__).resolve().parent.parent
BACKLOG = ROOT / "projects" / "dream-cycle" / "backlog"
BASE_URL = os.environ.get("KR_BASE_URL", "https://kindrobots.org").rstrip("/")
PROPOSAL_RE = re.compile(r"<!-- proposal-data\s*\n(.*?)\n-->", re.DOTALL)
BUILT_RE = re.compile(r"<!-- built-data\s*\n(.*?)\n-->", re.DOTALL)

# Historical recipe Facets were physically removed after being decomposed into
# reusable concepts. Proposals persist their original seed for reproducibility,
# so the attachment boundary expands those retired keys into today's live Facets.
FACET_KEY_EXPANSIONS: dict[str, tuple[str, ...]] = {
    "isekai-reluctant": ("isekai", "reluctant-protagonist"),
    "slice-of-life-complicated": ("slice-of-life", "complicated-relationships"),
    "shonen-aging-protagonist": ("shonen", "aging-protagonist"),
    "magical-girl-retired": ("magical-girl", "retired-hero"),
    "hard-sci-fi-soft-feelings": ("hard-science-fiction", "emotionally-intimate"),
    "body-horror-tender": ("body-horror", "tender"),
    "kaiju-from-the-kaiju-s-perspective": ("kaiju", "monster-perspective"),
    "noir-one-detail-wrong": ("noir", "reality-slightly-wrong"),
    "carnival-abandoned-still-running": ("carnival", "abandoned", "still-operating"),
    "western-strange-angle": ("western", "unusual-perspective"),
}


def _json_comment(pattern: re.Pattern[str], text: str) -> dict[str, Any] | None:
    match = pattern.search(text)
    if not match:
        return None
    try:
        value = json.loads(match.group(1))
    except json.JSONDecodeError:
        return None
    return value if isinstance(value, dict) else None


def _facet_selection(facets: Iterable[dict[str, Any]]) -> dict[str, list[Any]]:
    ids: list[int] = []
    keys: list[str] = []
    for facet in facets:
        if not isinstance(facet, dict) or facet.get("legacy") is True:
            continue
        key = str(facet.get("slug") or facet.get("canonicalValue") or "").strip()
        if key:
            keys.extend(FACET_KEY_EXPANSIONS.get(key, (key,)))
        elif isinstance(facet.get("id"), int) and facet["id"] > 0:
            # IDs are safe only as a last resort. Unlike aliases/slugs they become
            # stale when catalog rows are merged, decomposed, or physically deleted.
            ids.append(facet["id"])
    return {"facetIds": list(dict.fromkeys(ids)), "facetKeys": list(dict.fromkeys(keys))}


def _put(path: str, payload: dict[str, Any], token: str, *, dry_run: bool = False) -> dict[str, Any]:
    if dry_run:
        return {"success": True, "data": [], "dry_run": True, "path": path, "payload": payload}
    request = urllib.request.Request(
        f"{BASE_URL}{path}",
        method="PUT",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
            "User-Agent": "conductor-daily-dream-facets/1",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            result = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        body = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"PUT {path} failed ({error.code}): {body[:500]}") from error
    except (OSError, ValueError) as error:
        raise RuntimeError(f"PUT {path} failed: {error}") from error
    if not isinstance(result, dict) or result.get("success") is False:
        raise RuntimeError(f"PUT {path} returned failure: {result}")
    return result


def _post(path: str, payload: dict[str, Any], token: str, *, dry_run: bool = False) -> dict[str, Any]:
    if dry_run:
        return {"success": True, "data": {"slug": payload.get("slug"), "dry_run": True}}
    request = urllib.request.Request(
        f"{BASE_URL}{path}",
        method="POST",
        data=json.dumps(payload).encode("utf-8"),
        headers={
            "Accept": "application/json",
            "Content-Type": "application/json",
            "Authorization": f"Bearer {token}",
            "User-Agent": "conductor-daily-dream-facets/1",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=30) as response:
            result = json.loads(response.read().decode("utf-8"))
    except urllib.error.HTTPError as error:
        body = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(f"POST {path} failed ({error.code}): {body[:500]}") from error
    except (OSError, ValueError) as error:
        raise RuntimeError(f"POST {path} failed: {error}") from error
    if not isinstance(result, dict) or result.get("success") is False:
        raise RuntimeError(f"POST {path} returned failure: {result}")
    return result


def _facet_exists(slug: str, timeout: int = 20) -> bool:
    """Whether the catalog already holds this slug. Public read, no token."""
    url = f"{BASE_URL}/api/facets?" + urllib.parse.urlencode({"take": 1, "slug": slug})
    request = urllib.request.Request(
        url, headers={"Accept": "application/json", "User-Agent": "conductor-daily-dream-facets/1"}
    )
    try:
        with urllib.request.urlopen(request, timeout=timeout) as response:
            payload = json.loads(response.read().decode("utf-8"))
    except (OSError, ValueError, urllib.error.HTTPError):
        # Unknown is not "absent". Reporting absent here would POST a duplicate.
        raise RuntimeError(f"could not check whether Facet {slug} already exists")
    rows = payload.get("data") if isinstance(payload, dict) else None
    if not isinstance(rows, list):
        raise RuntimeError(f"unexpected /api/facets response while checking {slug}")
    return any(
        isinstance(row, dict) and str(row.get("slug") or "").casefold() == slug.casefold()
        for row in rows
    )


def ensure_invented_facets(
    proposal: dict[str, Any], token: str, *, dry_run: bool = False
) -> tuple[list[dict[str, Any]], list[str]]:
    """Create the brand-new Facets this bundle invented, if they are not there yet.

    Silas, 2026-09-02: "I would like each dream to include 1-2 new facets ...
    they should be different and fill a gap that we don't have."

    Runs before the linking pass below, because a PUT that names a slug the
    catalog does not hold resolves to nothing -- the same failure mode that ate
    every Character's Facets for six weeks, arriving from the other direction.

    Idempotent by slug, so a re-run (or --force) adopts the existing row instead
    of minting a second one. The existence check FAILS LOUDLY rather than
    assuming absence: treating an unreachable API as "not there" is how you get
    a duplicate catalog entry every night.
    """
    seeds = proposal.get("seed_facets")
    invented = seeds.get("invented") if isinstance(seeds, dict) else None
    if not isinstance(invented, list) or not invented:
        return [], []

    records: list[dict[str, Any]] = []
    errors: list[str] = []
    for facet in invented:
        if not isinstance(facet, dict):
            errors.append("seed_facets.invented contains a non-object entry")
            continue
        slug = str(facet.get("slug") or "").strip().casefold()
        if not slug:
            errors.append("an invented Facet has no slug")
            continue
        try:
            if _facet_exists(slug):
                records.append({"slug": slug, "created": False, "reason": "already in catalog"})
                continue
            payload = {
                "title": facet.get("title"),
                "slug": slug,
                "taxonomy": str(facet.get("taxonomy") or "").upper(),
                "description": facet.get("description"),
                "artPrompt": facet.get("art_prompt"),
                # Seedable from the day it lands, which is the whole point --
                # a new Facet that cannot be drawn is a dead row.
                "isRandomizable": True,
                "randomWeight": 1,
                "isPublic": True,
                "creationSource": "AI",
                "designer": "dream-cycle",
            }
            result = _post("/api/facets", payload, token, dry_run=dry_run)
            data = result.get("data") if isinstance(result.get("data"), dict) else {}
            records.append({
                "slug": slug,
                "created": True,
                "id": data.get("id"),
                "taxonomy": payload["taxonomy"],
            })
        except RuntimeError as error:
            errors.append(str(error))
    return records, errors


def _record_targets(proposal: dict[str, Any], built: dict[str, Any]) -> list[dict[str, Any]]:
    seed = proposal.get("seed_facets") if isinstance(proposal.get("seed_facets"), dict) else {}
    elements = seed.get("elements") if isinstance(seed.get("elements"), dict) else {}
    records = built.get("records") if isinstance(built.get("records"), dict) else {}
    targets: list[dict[str, Any]] = []

    def add(element: str, model: str, record: Any) -> None:
        if not isinstance(record, dict) or not isinstance(record.get("id"), int):
            return
        facets = elements.get(element)
        if not isinstance(facets, list) or not facets:
            return
        endpoint_model = {"Dream": "dreams", "Character": "characters", "Reward": "rewards", "Scenario": "scenarios"}.get(model)
        if not endpoint_model:
            return
        targets.append({
            "element": element,
            "model": model,
            "record_id": record["id"],
            "path": f"/api/{endpoint_model}/{record['id']}/facets",
            "facets": facets,
        })

    add("vibe", "Dream", records.get("world"))
    locations = records.get("locations") if isinstance(records.get("locations"), list) else []
    characters = records.get("characters") if isinstance(records.get("characters"), list) else []
    rewards = records.get("rewards") if isinstance(records.get("rewards"), list) else []
    scenarios = records.get("scenarios") if isinstance(records.get("scenarios"), list) else []
    if locations:
        add("location", "Dream", locations[0])
    if characters:
        add("character", "Character", characters[0])
    for reward in rewards:
        kind = str(reward.get("reward_type") or "").upper() if isinstance(reward, dict) else ""
        if kind == "ITEM":
            add("reward_item", "Reward", reward)
        elif kind == "SKILL":
            add("reward_skill", "Reward", reward)
    if scenarios:
        add("scenario", "Scenario", scenarios[0])
    return targets


def apply_file(path: Path, token: str, *, dry_run: bool = False, force: bool = False) -> tuple[bool, str, bool]:
    text = path.read_text(encoding="utf-8")
    proposal = _json_comment(PROPOSAL_RE, text)
    built = _json_comment(BUILT_RE, text)
    if not proposal or not built or not isinstance(proposal.get("seed_facets"), dict):
        return False, "not a built Facet-seeded proposal", False
    existing = built.get("facet_assignments")
    seed_version = proposal["seed_facets"].get("version")
    already_partial = (
        isinstance(existing, dict)
        and existing.get("seed_version") == seed_version
        and existing.get("status") == "partial"
    )
    if not force and isinstance(existing, dict) and existing.get("seed_version") == seed_version and existing.get("status") == "complete":
        return False, "already complete", False

    targets = _record_targets(proposal, built)
    if len(targets) != 6:  # world + location + character + two rewards + scenario
        return False, f"waiting for complete records ({len(targets)}/6 Facet targets)", False

    applied: list[dict[str, Any]] = []
    errors: list[str] = []

    # Create before linking: a PUT naming a slug the catalog does not hold
    # resolves to nothing.
    invented, invented_errors = ensure_invented_facets(proposal, token, dry_run=dry_run)
    errors.extend(invented_errors)
    for target in targets:
        selection = _facet_selection(target["facets"])
        if not selection["facetIds"] and not selection["facetKeys"]:
            errors.append(f"{target['element']}: no resolvable Facet ids/keys")
            continue
        try:
            result = _put(target["path"], selection, token, dry_run=dry_run)
            returned = result.get("data") if isinstance(result.get("data"), list) else []
            facet_ids = [
                row.get("id") for row in returned
                if isinstance(row, dict) and isinstance(row.get("id"), int)
            ]
            # A 200 is not proof the Facets landed. PUT /api/characters/:id/facets
            # ignored facetKeys entirely until 2026-09-02: it normalized a
            # slug-only body to zero assignments, ran its unconditional
            # deleteMany anyway, and answered success with an empty catalog. This
            # loop read that as applied, so every one of the 36 built bundles
            # recorded status "complete" with errors [] while its Character
            # carried no Facets at all -- which is what Silas eventually noticed
            # from the other end: "I just don't get the facets added as part of
            # my daily digest, so there is a discrepancy."
            #
            # `dry_run` legitimately returns nothing, so it keeps the old
            # behaviour of trusting the request it did not send.
            if not facet_ids and not dry_run:
                errors.append(
                    f"{target['element']}: requested "
                    f"{len(selection['facetKeys']) or len(selection['facetIds'])} "
                    f"Facet(s) but {target['path']} attached none"
                )
                continue
            applied.append({
                "element": target["element"],
                "model": target["model"],
                "record_id": target["record_id"],
                "facet_ids": facet_ids or selection["facetIds"],
                "facet_keys": selection["facetKeys"],
            })
        except RuntimeError as error:
            errors.append(str(error))

    built["facet_assignments"] = {
        "status": "complete" if not errors and len(applied) == len(targets) else "partial",
        "seed_version": seed_version,
        "applied_at": datetime.now(timezone.utc).isoformat(),
        "targets": applied,
        "invented": invented,
        "errors": errors,
    }
    replacement = "<!-- built-data\n" + json.dumps(built, ensure_ascii=False, sort_keys=True) + "\n-->"
    updated = BUILT_RE.sub(replacement, text, count=1)
    if not dry_run:
        path.write_text(updated, encoding="utf-8")
    return True, built["facet_assignments"]["status"], already_partial


def main(argv: list[str] | None = None) -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--dry-run", action="store_true")
    parser.add_argument("--force", action="store_true")
    parser.add_argument("--file", action="append", help="Only process this proposal file (repeatable)")
    args = parser.parse_args(argv)
    token = os.environ.get("KR_API_TOKEN", "").strip()
    if not token and not args.dry_run:
        print("KR_API_TOKEN is absent; Facet assignment skipped without blocking the hourly sweep.", file=sys.stderr)
        return 0
    files = [Path(value) for value in args.file] if args.file else sorted(BACKLOG.glob("*.md"))
    changed = 0
    partial_new = 0
    partial_persisting = 0
    for path in files:
        did_change, status, was_already_partial = apply_file(path, token, dry_run=args.dry_run, force=args.force)
        if did_change:
            changed += 1
            if status != "complete":
                if was_already_partial:
                    partial_persisting += 1
                    print(f"{path.name}: {status} (still unresolved from a prior run -- not re-failing this run's exit code)")
                else:
                    partial_new += 1
                    print(f"{path.name}: {status}")
            else:
                print(f"{path.name}: {status}")
    print(
        f"Facet assignment: {changed} proposal(s) processed, "
        f"{partial_new} newly partial, {partial_persisting} still partial from a prior run."
    )
    # Only a FRESH partial fails the hourly sweep -- that is a real, actionable
    # signal worth surfacing the day it happens. A proposal that was already
    # partial in an earlier run (same seed_version, unresolved) will keep
    # getting retried here every run since there is no short-circuit for
    # "partial" the way there is for "complete", but re-failing on it forever
    # once it has already been reported once is exactly the workflow-medic
    # "one broken thing drowns every other signal" failure mode -- see
    # conductor/t-104's 2026-08-08 hourly-conductor incident (every run failed
    # for 2+ days on a single stuck proposal, a missing FacetAlias row for
    # "culinary-fantasy", while genuinely new proposals kept succeeding
    # underneath the red status the whole time).
    return 1 if partial_new else 0


if __name__ == "__main__":
    raise SystemExit(main())
