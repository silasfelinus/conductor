#!/usr/bin/env python3
"""
scan_art_queue_sampler.py — count queued ArtJobs whose sampler settings exceed
what their engine is distilled for, i.e. the rows that will FAIL at claim with

    [engine-step-mismatch] krea2 runs at roughly 12 steps or fewer; got 20.

Why this exists: on 2026-08-09 the queue reported 8 recent failures, all that
one error, on jobs enqueued 2026-08-02..04 — before kind_robots' prompt contract
shipped (2026-08-08). `recheck_render_queue.py` shows the last N failures, which
answers "what just broke" but not "how much more of this is coming". Answering
that meant paging the whole 2815-row PENDING backlog by hand. The answer was 27,
and knowing it was 27 rather than 2000 is what made the fix a clamp instead of a
mass re-enqueue. Next time, run this.

    python scripts/scan_art_queue_sampler.py                 # PENDING (default)
    python scripts/scan_art_queue_sampler.py --status FAILED --ids

Requires KR_API_TOKEN (admin-capable). KR_BASE_URL defaults to the production
deployment, same as the other queue scripts.

SCOPE — read this before concluding "the backlog is clean". This checks the
MECHANICAL half of the contract only: steps and cfg against ENGINE_MAX_STEPS /
ENGINE_MAX_CFG in consume_art_queue_core.py. The prompt-text rules
(conditional-instruction, format-vocabulary, text-exclusion-pile,
vague-brand-style) live in kind_robots' server/utils/artPromptContract.ts and
are deliberately NOT reimplemented here: a second copy of those regexes would
drift from the enforcing one and report false confidence. A clean run means "no
row will die on its sampler settings", not "every row will render".

Since 2026-08-09 the claim endpoint clamps these settings rather than failing the
row (server/utils/artJobSamplerRepair.ts), so a non-zero count is no longer a
queue of pending failures — it is a count of pre-fix rows that will be repaired
as they drain, and a signal that some producer is still writing out-of-band
numbers. Read it that way.
"""

from __future__ import annotations

import argparse
import collections
import os
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))

import consume_art_queue as consumer  # noqa: E402
from consume_art_queue_core import ENGINE_MAX_CFG, ENGINE_MAX_STEPS  # noqa: E402

PAGE_SIZE = 200
MAX_PAGES = 200
RETRIES = 5


def _record(value):
    return value if isinstance(value, dict) else {}


def _clean(value) -> str:
    return value.strip() if isinstance(value, str) else ""


def _number(value):
    if value is None or value == "":
        return None
    try:
        parsed = float(value)
    except (TypeError, ValueError):
        return None
    return parsed if parsed == parsed and abs(parsed) != float("inf") else None


def _nodes(payload):
    return [_record(node) for node in _record(_record(payload).get("workflow")).values()]


def infer_engine(payload, fallback) -> str:
    """Mirror of inferQueuedArtEngine — the graph decides, not the relay label."""
    explicit = _clean(_record(payload).get("engine")).lower()
    if explicit and explicit != "comfy":
        return explicit

    saw_checkpoint_loader = False
    for node in _nodes(payload):
        class_type = _clean(node.get("class_type"))
        inputs = _record(node.get("inputs"))
        clip_type = _clean(inputs.get("type")).lower()
        model = f"{_clean(inputs.get('unet_name'))} {_clean(inputs.get('ckpt_name'))}".lower()

        if clip_type == "krea2" or "krea-2" in model:
            return "krea2"
        if clip_type == "flux2" or "flux-2-klein" in model:
            return "flux2"
        if class_type == "FluxGuidance" or clip_type == "flux":
            return "flux"
        if class_type == "CheckpointLoaderSimple":
            saw_checkpoint_loader = True

    return "comfy" if saw_checkpoint_loader else _clean(fallback).lower()


def sampler_settings(payload):
    """Mirror of queuedArtSamplerSettings — the KSampler node wins over metadata."""
    record = _record(payload)
    for node in _nodes(record):
        if _clean(node.get("class_type")) != "KSampler":
            continue
        inputs = _record(node.get("inputs"))
        steps = _number(inputs.get("steps"))
        cfg = _number(inputs.get("cfg"))
        return (
            steps if steps is not None else _number(record.get("steps")),
            cfg if cfg is not None else _number(record.get("cfg")),
        )
    return _number(record.get("steps")), _number(record.get("cfg"))


def over_ceiling(engine, steps, cfg):
    """Return the ceilings this job exceeds, as (field, value, ceiling) tuples."""
    # kind_robots keys both "flux2" (its own normalization) and "flux2-klein"
    # (Conductor's name) for the same model; accept either spelling here too.
    ceiling_steps = ENGINE_MAX_STEPS.get(engine)
    if ceiling_steps is None and engine == "flux2":
        ceiling_steps = ENGINE_MAX_STEPS.get("flux2-klein")
    ceiling_cfg = ENGINE_MAX_CFG.get(engine)
    if ceiling_cfg is None and engine == "flux2":
        ceiling_cfg = ENGINE_MAX_CFG.get("flux2-klein")

    breaches = []
    if ceiling_steps is not None and steps is not None and steps > ceiling_steps:
        breaches.append(("steps", steps, ceiling_steps))
    if ceiling_cfg is not None and cfg is not None and cfg > ceiling_cfg:
        breaches.append(("cfg", cfg, ceiling_cfg))
    return breaches


def fetch_page(status: str, page: int):
    """GET one page, retrying the TLS/connection hiccups a long scan will hit."""
    url = (
        f"{consumer.KR_BASE_URL}/api/art/queue"
        f"?status={status}&page={page}&pageSize={PAGE_SIZE}"
    )
    last_error = None
    for attempt in range(RETRIES):
        try:
            code, response = consumer.http_json("GET", url)
        except Exception as exc:  # noqa: BLE001 - transient network, retry
            last_error = exc
            __import__("time").sleep(2 * (attempt + 1))
            continue
        if code == 200 and response and response.get("success"):
            return response.get("data") or {}
        last_error = RuntimeError(f"HTTP {code}: {response and response.get('message')}")
        __import__("time").sleep(2 * (attempt + 1))
    raise RuntimeError(f"queue page {page} unreadable: {last_error}")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--status",
        default="PENDING",
        choices=["PENDING", "RUNNING", "FAILED", "DONE", "CANCELLED"],
    )
    parser.add_argument(
        "--ids",
        action="store_true",
        help="print every offending job id, not just the counts",
    )
    args = parser.parse_args()

    if not os.environ.get("KR_API_TOKEN", "").strip():
        print("KR_API_TOKEN is required to read the queue.", file=sys.stderr)
        return 2

    scanned = 0
    engines: collections.Counter[str] = collections.Counter()
    offenders: dict[str, list[int]] = collections.defaultdict(list)
    worst: dict[str, tuple[int, float, float]] = {}

    page = 1
    while page <= MAX_PAGES:
        data = fetch_page(args.status, page)
        for job in data.get("jobs") or []:
            if not isinstance(job, dict):
                continue
            scanned += 1
            payload = job.get("payload") or {}
            engine = infer_engine(payload, job.get("engine"))
            engines[engine] += 1
            steps, cfg = sampler_settings(payload)
            for field, value, ceiling in over_ceiling(engine, steps, cfg):
                key = f"{engine}:{field}"
                offenders[key].append(job["id"])
                if key not in worst or value > worst[key][1]:
                    worst[key] = (job["id"], value, ceiling)

        pagination = data.get("pagination") or {}
        if not pagination.get("hasNextPage"):
            break
        page += 1
    else:
        print(f"stopped at the {MAX_PAGES}-page cap; results are partial", file=sys.stderr)

    total = sum(len(ids) for ids in offenders.values())
    print(f"{args.status}: scanned {scanned} job(s)")
    print(f"engines: {dict(engines)}")
    if not offenders:
        print("sampler settings: all within engine ceilings")
        return 0

    print(f"over ceiling: {total} breach(es) across {len(offenders)} engine/field pair(s)")
    for key in sorted(offenders):
        job_id, value, ceiling = worst[key]
        print(
            f"  {key}: {len(offenders[key])} job(s); "
            f"worst = job {job_id} at {value:g} (ceiling {ceiling:g})"
        )
        if args.ids:
            print(f"    ids: {sorted(offenders[key])}")
    return 1


if __name__ == "__main__":
    raise SystemExit(main())
