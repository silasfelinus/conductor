#!/usr/bin/env python3
"""Reconcile Shifting Desks art deliveries without re-enqueueing or approving images.

Rounds 13-15 overwrite earlier renders at the SAME media path. A bare HTTP 200
cannot prove a new render was delivered. Require a matching Conductor request
ID and destination, a completed ArtJob with an ArtImage, and media newer than
that ArtJob before recording delivery. Visual verdicts are always editorial.
"""
from __future__ import annotations

import argparse
import datetime as dt
import email.utils
import json
import re
import sys
import urllib.error
import urllib.parse
import urllib.request
from pathlib import Path

import yaml

ROOT = Path(__file__).resolve().parents[3]
ART_DIR = Path(__file__).resolve().parent
ROUNDS = (13, 14, 15)
MEDIA_HOST = "media.acrocatranch.com"


def timestamp(value):
    if not value:
        return None
    try:
        return dt.datetime.fromisoformat(str(value).replace("Z", "+00:00")).astimezone(dt.timezone.utc)
    except (ValueError, TypeError):
        return None


def job_request_id(job):
    payload = job.get("payload") or {}
    if not isinstance(payload, dict):
        return ""
    request = payload.get("conductorRequest") or {}
    return str(request.get("id") or job.get("idempotencyKey") or "") if isinstance(request, dict) else ""


def matching_job(row, jobs, requested_at):
    target = str(row.get("target_path") or "").replace("kind_robots ", "").strip().lstrip("/")
    candidates = []
    for job in jobs:
        payload = job.get("payload") or {}
        if not isinstance(payload, dict):
            continue
        path = str(payload.get("imagePath") or "").strip().lstrip("/")
        if (
            job_request_id(job) == str(row.get("request_id"))
            and path == target
            and str(payload.get("targetRepo") or "") == "silasfelinus/kind_robots"
            and timestamp(job.get("createdAt"))
            and timestamp(job.get("createdAt")) >= requested_at
        ):
            candidates.append(job)
    return max(candidates, key=lambda job: int(job.get("id") or 0), default=None)


def probe_media(url, *, opener=urllib.request.urlopen):
    parsed = urllib.parse.urlparse(url)
    if parsed.scheme != "https" or parsed.netloc != MEDIA_HOST or not parsed.path.startswith("/images/shifting-desks/"):
        return None, "invalid media origin or path"
    try:
        with opener(urllib.request.Request(url, method="HEAD"), timeout=8) as response:
            status = response.status
            mime = response.headers.get("Content-Type", "").split(";")[0].strip().lower()
            length = int(response.headers.get("Content-Length") or 0)
            stamp = response.headers.get("Last-Modified")
            modified = email.utils.parsedate_to_datetime(stamp).astimezone(dt.timezone.utc) if stamp else None
            if status != 200 or mime != "image/webp" or length < 1000 or not modified:
                return None, f"media unverified: HTTP {status}, {mime}, {length} bytes, modified={bool(modified)}"
            return modified, f"HEAD 200 image/webp, {length} bytes, Last-Modified {modified.isoformat()}"
    except (OSError, urllib.error.URLError, ValueError, TypeError) as exc:
        return None, f"media probe unavailable: {type(exc).__name__}"


def reconcile_row(row, jobs, requested_at, probe=probe_media):
    """Return field edits. Never modify prompt, seed, verdict, or queued requests."""
    if row.get("status") == "delivered":
        return {}
    job = matching_job(row, jobs, requested_at)
    if not job:
        return {}
    job_id = int(job["id"])
    changes = {"art_job_id": job_id}
    status = str(job.get("status") or "").upper()
    image_id = job.get("artImageId")
    if status != "DONE":
        if status in {"FAILED", "CANCELLED"}:
            changes["delivery_check"] = f"ArtJob {job_id} {status}: render not delivered"
        return {key: value for key, value in changes.items() if row.get(key) != value}

    if not isinstance(image_id, int) or image_id <= 0:
        return {key: value for key, value in changes.items() if row.get(key) != value}

    changes["art_image_id"] = image_id
    media_time, observation = probe(row.get("media_url"))
    created = timestamp(job.get("createdAt"))
    if media_time and created and media_time >= created:
        changes["status"] = "delivered"
        changes["delivery_check"] = (
            f"ArtJob {job_id} DONE, ArtImage {image_id}; {observation}; "
            f"confirmed newer than ArtJob createdAt {created.isoformat()}; visual review pending"
        )
    else:
        changes["status"] = "rendered"
        changes["delivery_check"] = (
            f"ArtJob {job_id} DONE, ArtImage {image_id}; {observation}; "
            "new render media not independently verified"
        )
    return {key: value for key, value in changes.items() if row.get(key) != value}


def fetch_jobs(core):
    if not core.KR_API_TOKEN:
        raise RuntimeError("KR_API_TOKEN missing: cannot reconcile ArtJobs")
    jobs = []
    for page in range(1, 51):
        url = f"{core.KR_BASE_URL}/api/art/queue?projectSlug=shifting-desks&pageSize=200&page={page}"
        status, response = core.http_json("GET", url, timeout=20)
        if status != 200 or not isinstance(response, dict) or not response.get("success"):
            raise RuntimeError(f"ArtJob listing failed (HTTP {status})")
        data = response.get("data") or {}
        current = data.get("jobs") or []
        if not isinstance(current, list):
            raise RuntimeError("ArtJob listing has unexpected shape")
        jobs.extend(current)
        pagination = data.get("pagination") or {}
        if not pagination.get("hasNextPage"):
            return jobs
    raise RuntimeError("ArtJob listing exceeds 50 pages; refusing partial reconciliation")


def yaml_value(value):
    return json.dumps(value, ensure_ascii=False) if value is not None else "null"


def patch_rows(text, changes_by_request):
    """Targeted text edits preserve art briefs, YAML comments, ordering and seeds."""
    seen = set()
    pattern = re.compile(r"(?ms)^- key:.*?(?=^- key:|\\Z)")

    def update(match):
        block = match.group(0)
        identity = re.search(r"(?m)^  request_id: (\\S+)\\s*$", block)
        if not identity or identity.group(1) not in changes_by_request:
            return block
        request_id = identity.group(1)
        seen.add(request_id)
        for field, value in changes_by_request[request_id].items():
            field_pattern = re.compile(rf"(?m)^(  {re.escape(field)}: ).*$")
            if len(field_pattern.findall(block)) != 1:
                raise ValueError(f"{request_id}: expected one {field} field")
            block = field_pattern.sub(lambda m: m.group(1) + yaml_value(value), block)
        return block

    result = pattern.sub(update, text)
    if set(changes_by_request) != seen:
        raise ValueError("Requested subjects not found in ledger")
    yaml.safe_load(result)
    return result


def reconcile_files(paths, jobs, *, write=False, probe=probe_media):
    totals = {"found": 0, "delivered": 0, "rendered": 0, "waiting": 0, "changed": 0}
    for path in paths:
        original = path.read_text(encoding="utf-8")
        ledger = yaml.safe_load(original)
        requested_at = timestamp(ledger.get("requested_at"))
        if not requested_at:
            raise ValueError(f"{path}: invalid requested_at")
        edits = {}
        for row in ledger.get("subjects") or []:
            totals["found"] += 1
            update = reconcile_row(row, jobs, requested_at, probe=probe)
            if update:
                edits[str(row["request_id"])] = update
                totals["changed"] += 1
            target_status = update.get("status", row.get("status"))
            if target_status == "delivered":
                totals["delivered"] += 1
            elif target_status == "rendered":
                totals["rendered"] += 1
            else:
                totals["waiting"] += 1
        changed = patch_rows(original, edits) if edits else original
        if write and changed != original:
            path.write_text(changed, encoding="utf-8")
        print(f"{path.name}: {len(edits)} reconciled; {'written' if write else 'dry-run'}")
    print("art delivery: " + ", ".join(f"{key}={value}" for key, value in totals.items()))
    return totals


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--live", action="store_true", help="read authenticated ArtJobs and HEAD public media")
    parser.add_argument("--write", action="store_true", help="persist independently corroborated delivery facts")
    args = parser.parse_args(argv)
    if args.write and not args.live:
        parser.error("--write requires --live")
    paths = [ART_DIR / f"ROUND-{number}.yaml" for number in ROUNDS]
    if not args.live:
        for path in paths:
            ledger = yaml.safe_load(path.read_text(encoding="utf-8"))
            print(f"{path.name}: {len(ledger.get('subjects') or [])} authoring subjects")
        return 0
    sys.path.insert(0, str(ROOT))
    from scripts import consume_art_queue_core as core

    try:
        jobs = fetch_jobs(core)
        reconcile_files(paths, jobs, write=args.write)
    except (RuntimeError, OSError, ValueError) as exc:
        print(f"Art delivery reconciliation deferred: {exc}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
