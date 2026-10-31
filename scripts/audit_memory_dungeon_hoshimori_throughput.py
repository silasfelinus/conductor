#!/usr/bin/env python3
"""Read-only Hoshimori render-throughput evidence, not a delivery counter.

The queue summary endpoint intentionally leaves windowThroughput and latestDoneAt
empty. The full stats endpoint plus DONE rows (ordered by updatedAt) distinguish
an idle renderer from a slow backlog. A DONE update is NOT necessarily a render
completed in that hour, and is never proof of an attached/accepted ArtImage.
"""
from __future__ import annotations

from datetime import datetime, timedelta, timezone
import json
from typing import Any

from audit_memory_dungeon_hoshimori_relay import _get, _timestamp

PAGE_SIZE = 200
MAX_DONE_PAGES = 5
WINDOW_HOURS = 24


def fetch_recent_done(get_page, *, now: datetime, max_pages: int = MAX_DONE_PAGES) -> dict[str, Any]:
    """Fetch every DONE row updated in 24h, or explicitly mark a bounded sample."""
    if now.tzinfo is None:
        raise ValueError("now must be timezone aware")
    cutoff = now.astimezone(timezone.utc) - timedelta(hours=WINDOW_HOURS)
    rows: list[dict[str, Any]] = []
    seen: set[int] = set()
    total: int | None = None
    previous: tuple[datetime, int] | None = None
    for page in range(1, max_pages + 1):
        response = get_page(page)
        if not isinstance(response, dict):
            raise RuntimeError(f"DONE page {page} unavailable")
        pagination = response.get("pagination")
        batch = response.get("jobs")
        if not isinstance(pagination, dict) or not isinstance(batch, list):
            raise ValueError("DONE inventory missing jobs or pagination")
        count = pagination.get("totalCount")
        if not isinstance(count, int) or isinstance(count, bool) or count < 0:
            raise ValueError("invalid DONE total")
        if total is None:
            total = count
        if (count != total or pagination.get("page") != page
                or pagination.get("pageSize") != PAGE_SIZE):
            raise ValueError("DONE pagination changed during audit")
        if len(batch) > PAGE_SIZE:
            raise ValueError("oversized DONE page")
        for row in batch:
            if not isinstance(row, dict):
                raise ValueError("malformed DONE row")
            job_id = row.get("id")
            updated = _timestamp(row.get("updatedAt"))
            if (not isinstance(job_id, int) or isinstance(job_id, bool)
                    or job_id <= 0 or job_id in seen or updated is None
                    or row.get("status") != "DONE"):
                raise ValueError("invalid or duplicate DONE identity/timestamp")
            if updated > now.astimezone(timezone.utc) + timedelta(minutes=1):
                raise ValueError("future DONE timestamp")
            order = (updated, job_id)
            if previous is not None and order >= previous:
                raise ValueError("DONE updatedAt ordering changed")
            previous = order
            seen.add(job_id)
            if updated < cutoff:
                return {"jobs": rows, "complete_window": True,
                        "sampled": len(seen), "global_done_total": total}
            rows.append(row)
        if len(seen) > total:
            raise ValueError("DONE rows exceed reported total")
        if not pagination.get("hasNextPage"):
            if len(seen) != total:
                raise ValueError("DONE inventory incomplete")
            return {"jobs": rows, "complete_window": True,
                    "sampled": len(seen), "global_done_total": total}
        if len(batch) != PAGE_SIZE:
            raise ValueError("short DONE page claims another page")
    return {"jobs": rows, "complete_window": False,
            "sampled": len(seen), "global_done_total": total}


def analyze_throughput(stats: dict[str, Any], snapshot: dict[str, Any], *,
                       now: datetime) -> dict[str, Any]:
    """Report status-update evidence without inventing completion or media rates."""
    if now.tzinfo is None:
        raise ValueError("now must be timezone aware")
    if stats.get("windowHours") != WINDOW_HOURS:
        raise ValueError("expected full 24-hour queue stats")
    for key in ("staleRunningCount", "imagesCreatedInWindow"):
        value = stats.get(key)
        if not isinstance(value, int) or isinstance(value, bool) or value < 0:
            raise ValueError(f"invalid full stats {key}")
    if not isinstance(snapshot.get("jobs"), list):
        raise ValueError("DONE snapshot unavailable")
    utc_now = now.astimezone(timezone.utc)
    all_counts = {}
    comfy_counts = {}
    for hours in (1, 6, 24):
        cutoff = utc_now - timedelta(hours=hours)
        recent = [row for row in snapshot["jobs"]
                  if _timestamp(row.get("updatedAt")) >= cutoff]
        all_counts[f"{hours}h"] = len(recent)
        comfy_counts[f"{hours}h"] = sum(row.get("engine") == "COMFY" for row in recent)
    latest = _timestamp(stats.get("latestDoneAt"))
    if stats.get("latestDoneAt") is not None and latest is None:
        raise ValueError("invalid latest DONE timestamp")
    return {
        "source": "read_only_full_stats_and_done_updatedAt_inventory",
        "window_hours": WINDOW_HOURS,
        "done_rows_updated_in_window": all_counts,
        "comfy_done_rows_updated_in_window": comfy_counts,
        "exact_window_inventory": snapshot.get("complete_window") is True,
        "done_rows_examined": snapshot.get("sampled"),
        "global_done_total": snapshot.get("global_done_total"),
        "latest_done_updated_at": latest.isoformat() if latest else None,
        "latest_done_update_age_minutes": (
            round((utc_now - latest).total_seconds() / 60, 1) if latest else None
        ),
        "stale_running_count": stats["staleRunningCount"],
        "art_images_created_in_24h_all_sources": stats["imagesCreatedInWindow"],
        "images_by_server": stats.get("imagesByServer", []),
        "interpretation": (
            "DONE rows updatedAt is an activity proxy, not an exact render-completion "
            "rate: existing DONE rows can be edited later. ArtImage creation includes "
            "non-render sources. Neither number proves Hoshimori media delivery. "
            "When exact_window_inventory is false, all time-window counts are lower bounds."
        ),
    }


def main() -> int:
    from datetime import datetime, timezone
    import consume_art_queue as consumer

    if not consumer.KR_API_TOKEN:
        print("::warning::No KR_API_TOKEN; cannot inspect live render throughput")
        return 2
    now = datetime.now(timezone.utc)
    try:
        stats = _get(f"/api/art/queue/stats?window={WINDOW_HOURS}")
        if stats is None:
            raise RuntimeError("full stats endpoint unavailable")
        done = fetch_recent_done(
            lambda page: _get(
                f"/api/art/queue?status=DONE&pageSize={PAGE_SIZE}&page={page}"
            ),
            now=now,
        )
        report = analyze_throughput(stats, done, now=now)
    except (RuntimeError, ValueError, TypeError) as error:
        print(f"::error::Hoshimori throughput evidence unavailable: {type(error).__name__}")
        return 2
    print(json.dumps(report, indent=2, sort_keys=True))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
