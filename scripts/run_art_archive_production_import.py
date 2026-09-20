#!/usr/bin/env python3
"""Run the private Art Archive production reconciliation through Kind Robots API.

This is the agent-safe operational lane for art-archive/t-041. It never prints
KR_API_TOKEN or per-file archive paths. The real import only runs after a
successful dry-run with at least one scanned file and zero scanner issues.
"""

from __future__ import annotations

import argparse
import json
import os
import urllib.error
import urllib.parse
import urllib.request
from typing import Any

DEFAULT_API_BASE = "https://kindrobots.org"
PAGE_SIZE = 200


def api_request(
    api_base: str,
    token: str,
    path: str,
    *,
    method: str = "GET",
) -> dict[str, Any]:
    request = urllib.request.Request(
        f"{api_base.rstrip('/')}{path}",
        method=method,
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/json",
            "User-Agent": "conductor-art-archive-import/1.0",
        },
    )
    try:
        with urllib.request.urlopen(request, timeout=300) as response:
            body = response.read().decode("utf-8")
    except urllib.error.HTTPError as error:
        body = error.read().decode("utf-8", errors="replace")
        raise RuntimeError(
            f"Kind Robots request failed: {method} {path} -> HTTP {error.code}: {body[:500]}"
        ) from error
    except urllib.error.URLError as error:
        raise RuntimeError(
            f"Kind Robots request failed: {method} {path}: {error.reason}"
        ) from error

    parsed = json.loads(body)
    if not parsed.get("success"):
        raise RuntimeError(
            f"Kind Robots rejected {method} {path}: {parsed.get('message', 'unknown error')}"
        )
    return parsed


def print_summary(label: str, data: dict[str, Any], fields: tuple[str, ...]) -> None:
    summary = {field: data.get(field) for field in fields}
    print(f"{label}: {json.dumps(summary, sort_keys=True)}")


def verify_archive_privacy(api_base: str, token: str) -> tuple[int, int]:
    checked = 0
    total = None
    page = 1
    while total is None or checked < total:
        query = urllib.parse.urlencode({"page": page, "pageSize": PAGE_SIZE})
        response = api_request(
            api_base,
            token,
            f"/api/admin/art-archive/entries?{query}",
        )
        data = response.get("data") or {}
        entries = data.get("entries") or []
        if total is None:
            total = int(data.get("total") or 0)
        if not entries:
            break

        for entry in entries:
            if entry.get("isPublic") is not False or entry.get("isMature") is not True:
                raise RuntimeError(
                    "Archive privacy verification failed: at least one imported entry "
                    "is not private+mature."
                )
        checked += len(entries)
        page += 1

    return int(total or 0), checked


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--dry-run-only",
        action="store_true",
        help="Preview production reconciliation without importing.",
    )
    parser.add_argument(
        "--api-base",
        default=os.environ.get("KR_API_BASE", DEFAULT_API_BASE),
    )
    args = parser.parse_args()

    token = os.environ.get("KR_API_TOKEN", "").strip()
    if not token:
        raise RuntimeError("KR_API_TOKEN is required for Art Archive production import.")

    dry_response = api_request(
        args.api_base,
        token,
        "/api/admin/art-archive/dry-run",
        method="POST",
    )
    dry = dry_response.get("data") or {}
    plan = dry.get("plan") or {}
    dry_summary = {
        "filesScanned": dry.get("filesScanned"),
        "cacheHitCount": dry.get("cacheHitCount"),
        "scanIssueCount": dry.get("scanIssueCount"),
        "new": plan.get("new"),
        "unchanged": plan.get("unchanged"),
        "changed": plan.get("changed"),
        "moved": plan.get("moved"),
        "copied": plan.get("copied"),
        "missing": plan.get("missing"),
        "filesWithMatchEvidence": dry.get("filesWithMatchEvidence"),
        "unmatchedModels": dry.get("unmatchedModels"),
        "confidenceCounts": dry.get("confidenceCounts"),
    }
    print(f"dry-run: {json.dumps(dry_summary, sort_keys=True)}")

    files_scanned = int(dry.get("filesScanned") or 0)
    scan_issues = int(dry.get("scanIssueCount") or 0)
    if files_scanned <= 0:
        raise RuntimeError("Dry run scanned zero files; refusing to perform production import.")
    if scan_issues:
        raise RuntimeError(
            f"Dry run reported {scan_issues} scanner issue(s); refusing to perform production import."
        )

    if args.dry_run_only:
        return 0

    import_response = api_request(
        args.api_base,
        token,
        "/api/admin/art-archive/import",
        method="POST",
    )
    imported = import_response.get("data") or {}
    print_summary(
        "import",
        imported,
        (
            "filesScanned",
            "scanIssues",
            "imagesCreated",
            "imagesReused",
            "collectionsCreated",
            "collectionsReused",
            "filesWithMatchEvidence",
            "unmatchedModels",
        ),
    )
    errors = imported.get("errors") or []
    print(f"import-errors: {len(errors)}")
    if errors:
        raise RuntimeError(
            f"Production import completed with {len(errors)} per-file error(s); "
            "private filenames are intentionally omitted from logs."
        )

    total, checked = verify_archive_privacy(args.api_base, token)
    print(
        "privacy-verification: "
        + json.dumps(
            {
                "archiveEntries": total,
                "entriesChecked": checked,
                "allCheckedEntriesPrivate": checked == total and total > 0,
                "allCheckedEntriesMature": checked == total and total > 0,
            },
            sort_keys=True,
        )
    )
    if total <= 0 or checked != total:
        raise RuntimeError(
            f"Archive verification expected a populated, fully checked result; total={total}, checked={checked}."
        )

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
