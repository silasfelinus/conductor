#!/usr/bin/env python3
"""Submit an A/B art ledger to Kind Robots ``POST /api/art/enqueue``.

WHY THIS EXISTS. ``consume_art_queue.py`` builds its own ComfyUI graphs and only
knows krea2, flux and flux2-klein; it even aliases ``sdxl`` to krea2. Kind Robots'
enqueue route already builds correct graphs for every lane it supports (SDXL /
Illustrious / Pony checkpoints with their family sampler profiles, Z-Image, ...),
so a ledger that wants to compare checkpoints sends requests there instead of
re-implementing those graphs here.

A ledger is YAML with ``lanes`` (engine + optional checkpoint + prompt style) and
``subjects`` (one prompt pair per subject). Every subject renders once per lane;
the returned ArtJob id is written back under ``subjects[].jobs[<lane>]`` so a
re-run never submits the same cell twice. See
projects/comic-creator/issues/zuzu-koala-assassin-01/ART-ROUND-3.yaml.

Usage:
    python scripts/enqueue_art_requests.py LEDGER            # dry run, print requests
    python scripts/enqueue_art_requests.py LEDGER --live     # submit missing cells
    python scripts/enqueue_art_requests.py LEDGER --status   # record job status + ArtImage ids

Environment: KR_API_TOKEN (required for --live/--status), KR_BASE_URL.
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

import yaml

try:
    from scripts import consume_art_queue_core as core
except ImportError:  # pragma: no cover - direct script execution
    import consume_art_queue_core as core

TERMINAL_STATUSES = {"DONE", "FAILED", "CANCELLED"}


def compose_prompt(lane, subject):
    """The prompt string one lane sends for one subject."""
    style = str(lane.get("prompt") or "prose").strip().lower()
    base = subject.get("prompt_tags") if style == "tags" else subject.get("prompt_prose")
    base = base or subject.get("prompt_prose") or ""
    parts = [lane.get("prefix"), base, lane.get("suffix")]
    return ", ".join(" ".join(str(p).split()) for p in parts if p and str(p).strip())


def build_request(ledger, lane, subject):
    """The /api/art/enqueue body for one (subject, lane) cell."""
    width, height = core.parse_size(subject.get("size"))
    body = {
        "engine": lane["engine"],
        "promptString": compose_prompt(lane, subject),
        "width": width,
        "height": height,
        "isPublic": bool(ledger.get("is_public", False)),
        "isMature": bool(ledger.get("is_mature", False)),
    }
    if lane.get("checkpoint"):
        body["checkpoint"] = lane["checkpoint"]
    if lane["engine"] == "comfy":
        # Optional per-lane overrides (a checkpoint author's recommended settings).
        # Absent, Kind Robots applies the checkpoint family's sampler profile. The
        # scheduler always stays the profile's: enqueue does not forward one for comfy.
        for field in ("steps", "cfg", "sampler"):
            if lane.get(field):
                body[field] = lane[field]
    if lane["engine"] == "comfy" and subject.get("negative"):
        body["negativePrompt"] = " ".join(str(subject["negative"]).split())
    for field, key in (("projectSlug", "project_slug"), ("designer", "designer")):
        if ledger.get(key):
            body[field] = ledger[key]
    return body


def iter_cells(ledger, lane_filter=None, subject_filter=None):
    lanes = ledger.get("lanes") or []
    for subject in ledger.get("subjects") or []:
        if subject_filter and subject.get("key") not in subject_filter:
            continue
        for lane in lanes:
            if lane_filter and lane.get("key") not in lane_filter:
                continue
            yield subject, lane


def split_header(text):
    """Leading comment block, kept verbatim when the ledger is rewritten."""
    lines = text.splitlines(keepends=True)
    header = []
    for line in lines:
        if line.startswith("#") or not line.strip():
            header.append(line)
        else:
            break
    return "".join(header)


def load_ledger(path):
    text = Path(path).read_text()
    return split_header(text), yaml.safe_load(text) or {}


def save_ledger(path, header, ledger):
    Path(path).write_text(
        header + yaml.safe_dump(ledger, sort_keys=False, width=110, allow_unicode=True)
    )


def job_id_of(subject, lane_key):
    return (subject.get("jobs") or {}).get(lane_key)


def submit(path, header, ledger, cells, post=None):
    """POST every cell that has no job id yet; write the id back after each one."""
    post = post or (lambda body: core.http_json("POST", f"{core.KR_BASE_URL}/api/art/enqueue", body))
    submitted, failures = 0, 0
    for subject, lane in cells:
        if job_id_of(subject, lane["key"]):
            continue
        status, resp = post(build_request(ledger, lane, subject))
        job_id = ((resp or {}).get("data") or {}).get("jobId") if isinstance(resp, dict) else None
        if status in (200, 201) and job_id:
            subject.setdefault("jobs", {})[lane["key"]] = int(job_id)
            save_ledger(path, header, ledger)
            submitted += 1
            print(f"  queued job {job_id} for {subject['key']} [{lane['key']}]")
        else:
            failures += 1
            message = (resp or {}).get("message") if isinstance(resp, dict) else resp
            print(f"  FAILED {subject['key']} [{lane['key']}]: HTTP {status} {message}", file=sys.stderr)
    return submitted, failures


def refresh_status(path, header, ledger, get=None):
    """Record each job's status and ArtImage id under subjects[].art."""
    get = get or (lambda job_id: core.http_json("GET", f"{core.KR_BASE_URL}/api/art/queue/{job_id}"))
    counts = {}
    for subject in ledger.get("subjects") or []:
        for lane_key, job_id in (subject.get("jobs") or {}).items():
            if not job_id:
                continue
            status, resp = get(job_id)
            job = (((resp or {}).get("data") or {}).get("job") or {}) if isinstance(resp, dict) else {}
            job_status = job.get("status") or f"HTTP{status}"
            counts[job_status] = counts.get(job_status, 0) + 1
            art = subject.setdefault("art", {})
            art[lane_key] = {"status": job_status, "art_image_id": job.get("artImageId")}
    save_ledger(path, header, ledger)
    return counts


def main(argv=None):
    parser = argparse.ArgumentParser(description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("ledger")
    parser.add_argument("--live", action="store_true", help="submit cells that have no job id")
    parser.add_argument("--status", action="store_true", help="refresh job status and ArtImage ids")
    parser.add_argument("--lane", action="append", help="limit to a lane key (repeatable)")
    parser.add_argument("--subject", action="append", help="limit to a subject key (repeatable)")
    args = parser.parse_args(argv)

    header, ledger = load_ledger(args.ledger)
    cells = list(iter_cells(ledger, args.lane, args.subject))

    if (args.live or args.status) and not core.KR_API_TOKEN:
        print("KR_API_TOKEN is required for --live and --status.", file=sys.stderr)
        return 1

    if args.status:
        counts = refresh_status(args.ledger, header, ledger)
        print("status:", ", ".join(f"{k}={v}" for k, v in sorted(counts.items())) or "no jobs")
        return 0

    if not args.live:
        pending = [(s, lane) for s, lane in cells if not job_id_of(s, lane["key"])]
        print(f"DRY RUN: {len(pending)} of {len(cells)} cells would be submitted via {core.KR_BASE_URL}")
        for subject, lane in pending:
            body = build_request(ledger, lane, subject)
            print(f"  {subject['key']} [{lane['key']}] {body['width']}x{body['height']} \"{body['promptString'][:70]}\"")
        return 0

    submitted, failures = submit(args.ledger, header, ledger, cells)
    print(f"{submitted} submitted, {failures} failed")
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
