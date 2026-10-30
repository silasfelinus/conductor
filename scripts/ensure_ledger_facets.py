#!/usr/bin/env python3
"""Create the Facets a project's Facet ledger names, once, and record their ids.

A Facet ledger is YAML under ``projects/<slug>/facets/`` with ``designer`` and a list
of ``facets`` (``slug``, ``title``, ``taxonomy``, ``description``, ``art_prompt``,
optional ``group_key``/``group_label``). Each row is created through Kind Robots'
``POST /api/facets`` -- the same route the daily dream uses for its invented Facets
(apply_daily_dream_facets.py) -- and the returned id is written back as ``facet_id``.

Idempotent by slug: a row that already has ``facet_id``, or whose slug the live catalog
already holds, is adopted rather than created again. The existence check FAILS LOUDLY:
an unreachable API is not "absent", and treating it that way mints duplicates.

Art is separate. Queue it through an ``auto_submit`` art ledger whose subjects carry
``entity_art: {type: facet, id: <facet_id>}``; the finished image then attaches to
Facet.imagePath on completion (enqueue_art_requests.build_entity_art).

Usage:
    python scripts/ensure_ledger_facets.py LEDGER            # dry run
    python scripts/ensure_ledger_facets.py LEDGER --live     # create missing Facets

Environment: KR_API_TOKEN (for --live), KR_BASE_URL.
"""

from __future__ import annotations

import argparse
import sys
import urllib.parse

try:
    from scripts import consume_art_queue_core as core
    from scripts.enqueue_art_requests import load_ledger, save_ledger
except ImportError:  # pragma: no cover - direct script execution
    import consume_art_queue_core as core
    from enqueue_art_requests import load_ledger, save_ledger

REQUIRED = ("slug", "title", "taxonomy", "description", "art_prompt")


def find_by_slug(slug, get=None):
    """The live Facet holding this slug, or None. Raises when the answer is unknown."""
    get = get or (lambda url: core.http_json("GET", url))
    # /api/facets has no exact slug filter (a `slug=` parameter is ignored and returns
    # an arbitrary first page); `search` matches title/slug/description/alias, and the
    # loop below keeps only the exact slug. Inactive and mature rows count: their slugs
    # are taken too, and the unique index is global.
    query = {"search": slug, "take": 250, "includeInactive": "true", "includeMature": "true"}
    status, resp = get(f"{core.KR_BASE_URL}/api/facets?" + urllib.parse.urlencode(query))
    rows = resp.get("data") if isinstance(resp, dict) else None
    if status != 200 or not isinstance(rows, list):
        raise RuntimeError(f"could not check whether Facet {slug} exists (HTTP {status})")
    for row in rows:
        if isinstance(row, dict) and str(row.get("slug") or "").casefold() == slug.casefold():
            return row
    return None


def payload_for(ledger, row):
    missing = [field for field in REQUIRED if not str(row.get(field) or "").strip()]
    if missing:
        raise ValueError(f"{row.get('slug') or row.get('key')}: missing {', '.join(missing)}")
    body = {
        "title": row["title"],
        "slug": row["slug"],
        "taxonomy": str(row["taxonomy"]).upper(),
        "canonicalValue": row["title"],
        "description": " ".join(str(row["description"]).split()),
        "artPrompt": " ".join(str(row["art_prompt"]).split()),
        "isPublic": True,
        "isRandomizable": bool(row.get("is_randomizable", True)),
        "randomWeight": 1,
        "creationSource": "AI",
        "designer": ledger.get("designer") or ledger.get("project_slug") or "conductor",
        "metadata": {"source": "conductor-facet-ledger", "project": ledger.get("project_slug"),
                     "ledgerKey": row.get("key") or row["slug"]},
    }
    for field, key in (("groupKey", "group_key"), ("groupLabel", "group_label")):
        if row.get(key):
            body[field] = row[key]
    return body


def ensure(path, header, ledger, *, live=False, get=None, post=None):
    """Adopt or create every row; returns (created, adopted, failures)."""
    post = post or (lambda body: core.http_json("POST", f"{core.KR_BASE_URL}/api/facets", body))
    created = adopted = failures = 0
    for row in ledger.get("facets") or []:
        if row.get("facet_id"):
            adopted += 1
            continue
        try:
            body = payload_for(ledger, row)
            existing = find_by_slug(row["slug"], get)
        except (ValueError, RuntimeError) as error:
            failures += 1
            print(f"  FAILED {row.get('slug')}: {error}", file=sys.stderr)
            continue
        if existing:
            row["facet_id"] = int(existing["id"])
            adopted += 1
            print(f"  adopted {row['slug']} -> Facet {existing['id']}")
        elif not live:
            print(f"  would create {body['taxonomy']} {body['title']} ({row['slug']})")
            continue
        else:
            status, resp = post(body)
            data = resp.get("data") if isinstance(resp, dict) else None
            facet_id = data.get("id") if isinstance(data, dict) else None
            if status not in (200, 201) or not facet_id:
                failures += 1
                message = resp.get("message") if isinstance(resp, dict) else resp
                print(f"  FAILED {row['slug']}: HTTP {status} {message}", file=sys.stderr)
                continue
            row["facet_id"] = int(facet_id)
            created += 1
            print(f"  created {body['taxonomy']} {body['title']} -> Facet {facet_id}")
        if live:
            save_ledger(path, header, ledger)
    return created, adopted, failures


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("ledger")
    parser.add_argument("--live", action="store_true", help="create missing Facets and write ids back")
    args = parser.parse_args(argv)
    if args.live and not core.KR_API_TOKEN:
        print("KR_API_TOKEN is required for --live.", file=sys.stderr)
        return 1
    header, ledger = load_ledger(args.ledger)
    created, adopted, failures = ensure(args.ledger, header, ledger, live=args.live)
    print(f"{created} created, {adopted} adopted, {failures} failed")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
