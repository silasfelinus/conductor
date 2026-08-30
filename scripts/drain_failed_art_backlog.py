#!/usr/bin/env python3
"""drain_failed_art_backlog.py — requeue an infra-caused FAILED ArtJob backlog,
but only after proving the render box can actually render right now.

Why this exists (2026-08-25). The art queue had accumulated 420 FAILED ArtJobs,
every one of them COMFY, every one of them at attempts=3. Nothing in the repo
could resubmit them:

  * repair_failed_kindrobots_artjobs.py is deliberately narrow -- it only selects
    failures whose *payload* is wrong (legacy imagePath, retired brand-style
    token). It correctly selected zero of the 420 and printed all of them as
    "unhandled", which is honest but leaves no path forward.
  * The bare POST /api/art/queue/reenqueue-failed endpoint has no policy at all.
    Pointing it at 420 ids while the render host is still broken burns 3 attempts
    each -- 1260 render attempts -- and drops every job straight back to FAILED,
    having also flushed the original error text that the diagnosis depends on.

So the missing piece is not "a way to requeue" but "a way to requeue that refuses
to fire into a host that is still down". That is the whole point of this script:

  1. Classify every FAILED job by *why* it failed (see classify_failure).
     Render-host faults are worth retrying verbatim; a payload that names a model
     the box does not have is not, and is reported instead of resubmitted.
  2. Requeue a small canary batch first and poll it to a terminal state.
  3. Only drain the rest if the canary actually rendered.
  4. Skip any job whose target image already exists (see target_media_state).
     "Retryable" says the payload is sound; it does not say the work is still
     wanted, and the relay writes to the job's imagePath either way -- so
     requeuing a job a later render already satisfied silently replaces a good
     image with a different one. Pass --include-rendered to re-roll on purpose.

A canary that fails is a success for this script: it means the backlog was left
intact, with its error text, for whoever fixes the host.

Usage:
    python scripts/drain_failed_art_backlog.py                  # dry run: classify only
    python scripts/drain_failed_art_backlog.py --live           # canary, then drain
    python scripts/drain_failed_art_backlog.py --live --canary 5
    python scripts/drain_failed_art_backlog.py --live --skip-canary   # see below
    python scripts/drain_failed_art_backlog.py --include-rendered     # re-roll too

--skip-canary exists for the case where the host was *just* confirmed healthy by
other means (a fresh DONE in the queue, Silas saying the drive is back). It is
not the default and should not become one.

Requires KR_API_TOKEN. KR_BASE_URL defaults to https://kindrobots.org.
"""

import argparse
import re
import sys
import time
import urllib.error
import urllib.request
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
import consume_art_queue as consumer  # noqa: E402
from media_direct_consumer import (  # noqa: E402
    _media_url,
    normalize_kindrobots_image_path,
)

PAGE_SIZE = 200
REQUEUE_BATCH_SIZE = 100
DIAGNOSTIC_ERROR_LIMIT = 400

# How long to wait for the canary batch to reach a terminal state. The relay
# claims one job at a time and a cold model load has been measured at ~11
# minutes (cthulhuquarium/t-005), so this is deliberately generous.
CANARY_POLL_SECONDS = 20
CANARY_TIMEOUT_SECONDS = 25 * 60

TERMINAL_STATUSES = ("DONE", "FAILED", "CANCELLED")

# How long to wait on the HEAD that asks whether a job's target image already
# exists. Same budget as media_direct_consumer.MEDIA_EXISTS_TIMEOUT_SECONDS --
# this is a static file host, not a render.
MEDIA_EXISTS_TIMEOUT_SECONDS = 8

# Failure classes. The first element of each pair is the class name; jobs land in
# the first class whose pattern matches, so order is specificity order -- a
# payload fault that happens to mention the ComfyUI URL must not be swallowed by
# a broader render-host pattern.
#
# RETRYABLE means "the payload is fine, the host was not". Those are safe to
# resubmit verbatim once the host is healthy.
FAILURE_PATTERNS = (
    # --- payload faults: resubmitting these verbatim fails again, every time ---
    (
        "payload-model-missing",
        re.compile(
            r"has no matching file for|value_not_in_list|not in \(list of length",
            re.IGNORECASE,
        ),
    ),
    (
        "payload-column-range",
        re.compile(r"Out of range value for column", re.IGNORECASE),
    ),
    # --- render-host faults: the box could not read its own model files ---
    (
        "render-host-io",
        re.compile(
            r"WinError \d+|I/O device error|hostbuf_file_reader_read"
            r"|Errno \d+|Input/output error"
            # relay_agent.host_fault_in_node_errors' rewritten message, which
            # leads with the host rather than with "POST /prompt failed".
            r"|cannot read its own model files",
            re.IGNORECASE,
        ),
    ),
    (
        "render-host-unreachable",
        re.compile(
            r"connection refused|Max retries exceeded|Failed to establish"
            r"|Connection aborted|timed out",
            re.IGNORECASE,
        ),
    ),
    # --- relay/API faults: the render may even have succeeded ---
    (
        "relay-stalled",
        re.compile(
            r"Stale claim reaped|relay stopped responding"
            r"|No accepted prompt .* appeared within",
            re.IGNORECASE,
        ),
    ),
    (
        "kr-api-error",
        re.compile(r"complete\(\d+\) failed: HTTP 5\d\d", re.IGNORECASE),
    ),
)

RETRYABLE_CLASSES = frozenset(
    {
        "render-host-io",
        "render-host-model-vanished",
        "render-host-unreachable",
        "relay-stalled",
        "kr-api-error",
    }
)

# "ComfyUI has no matching file for: CLIPLoader.clip_name='qwen3vl_4b...'"
MISSING_ASSET_RE = re.compile(r"(\w+)\.(\w+)='([^']*)'")


def missing_asset_names(error):
    """The model filenames a `has no matching file for:` error names."""
    text = str(error or "")
    head = text.split(". Not in the live model list", 1)[0]
    return [value for _cls, _input, value in MISSING_ASSET_RE.findall(head) if value]


def registered_model_basenames():
    """Every model filename Kind Robots' Resource registry knows about.

    Returns None if the registry can't be read, so a caller can tell "not
    registered" from "could not check" and decline to guess either way.
    """
    status, response = consumer.http_json(
        "GET", f"{consumer.KR_BASE_URL}/api/resources?pageSize=500"
    )
    if status != 200 or not response or not response.get("success"):
        return None
    data = response.get("data")
    rows = data if isinstance(data, list) else (data or {}).get("resources") or []
    names = set()
    for row in rows:
        if not isinstance(row, dict):
            continue
        for field in ("name", "localPath"):
            value = str(row.get(field) or "").strip().replace("\\", "/")
            if value:
                names.add(value.rsplit("/", 1)[-1])
    return names or None


def refine_missing_model(job, registered):
    """Split "you named a file that never existed" from "the box lost a file".

    ComfyUI answers both with the same thing -- the name is absent from its live
    list -- and the relay can only repeat that. The Resource registry is what
    breaks the tie: a file Kind Robots has registered, and that rendered earlier
    the same day, has not been misnamed. The box stopped being able to see it,
    which is a host fault and retryable.

    Observed 2026-08-25T22:25Z: 30 jobs rejected for
    `qwen3vl_4b_fp8_scaled.safetensors` and `qwen_image_vae.safetensors`, both
    registered, both used by every job that rendered fine at 07:20Z the same
    morning, while the unet on the same graph still resolved. A partially
    readable model share, not a payload.
    """
    if not registered:
        return "payload-model-missing"
    named = missing_asset_names((job or {}).get("error"))
    if not named:
        return "payload-model-missing"
    if all(name in registered for name in named):
        return "render-host-model-vanished"
    return "payload-model-missing"


def classify_failure(job, registered=None):
    """Return the failure class for one FAILED ArtJob row.

    `registered` is the set of model filenames Kind Robots knows about, used
    only to refine a missing-model rejection (see refine_missing_model). Pass
    None to classify on the error text alone.

    Unrecognized errors classify as "unknown" and are NOT retried. Defaulting to
    deny keeps a brand-new failure mode out of a 400-job blind resubmit; it shows
    up in the report instead, which is where a human should see it first.
    """
    error = " ".join(str((job or {}).get("error") or "").split())
    if not error:
        return "unknown"
    for name, pattern in FAILURE_PATTERNS:
        if pattern.search(error):
            if name == "payload-model-missing":
                return refine_missing_model(job, registered)
            return name
    return "unknown"


def is_retryable(failure_class):
    """True when resubmitting the job verbatim could plausibly succeed."""
    return failure_class in RETRYABLE_CLASSES


def failure_diagnostic(job):
    """A prompt-free, bounded one-liner for the report.

    Mirrors repair_failed_kindrobots_artjobs.failure_diagnostic: never echo the
    prompt, and never let one pathological traceback flood the output.
    """
    job_id = (job or {}).get("id", "?")
    engine = str((job or {}).get("engine") or "unknown").strip() or "unknown"
    slug = str((job or {}).get("projectSlug") or "-").strip() or "-"
    error = " ".join(str((job or {}).get("error") or "(no error text)").split())
    if len(error) > DIAGNOSTIC_ERROR_LIMIT:
        error = error[: DIAGNOSTIC_ERROR_LIMIT - 1] + "…"
    return f"ArtJob {job_id} [{slug}] engine={engine}: {error}"


def target_media_state(job):
    """Does this FAILED job's target image already exist? -> present/absent/unknown.

    Why this exists (2026-08-29). Every one of the 22 FAILED jobs classified
    retryable, and correctly so: eleven died with `[WinError 3] ... 'Z:\\'`
    (the media share unmounted) and eleven with `WinError 10061` at
    127.0.0.1:8188 (ComfyUI not listening). Both are host faults with clean
    payloads. But half of them had *already been rendered* -- a duplicate
    enqueue on 2026-08-27T11:46 re-queued a whole ruler-hooked batch whose
    originals rendered on 08-26, so ArtJob 10124 was a second attempt at
    `characters/bard-fen.webp`, which ArtJob 9931 had already written.

    Draining those is not a harmless no-op. The relay writes the render to the
    same imagePath, so a blind requeue overwrites eleven images that already
    exist -- at a different seed, and therefore a different picture -- with
    nobody having asked for a re-roll. "Retryable" answers whether the payload
    is sound; it does not answer whether the work is still wanted.

    Deliberately tri-state. `present` needs a positive 2xx from the media
    origin; a 404 is `absent`; a timeout, DNS failure, or 5xx is `unknown` and
    is treated as still-wanted by the caller, because a media origin we cannot
    reach is not evidence that the image is there. The bias is on purpose: a
    wrongly-requeued job costs one render, a wrongly-skipped one costs a
    missing image that nothing will queue again.
    """
    payload = (job or {}).get("payload")
    payload = payload if isinstance(payload, dict) else {}
    image_path = normalize_kindrobots_image_path(payload.get("imagePath"))
    if not image_path.startswith("public/images/"):
        # Not a Kind Robots media target -- there is no URL to ask about, so
        # this check has no opinion on it.
        return "unknown", ""

    url = _media_url(image_path)
    request = urllib.request.Request(url, method="HEAD")
    try:
        with urllib.request.urlopen(
            request, timeout=MEDIA_EXISTS_TIMEOUT_SECONDS
        ) as response:
            return ("present" if 200 <= response.status < 300 else "absent"), url
    except urllib.error.HTTPError as exc:
        # 404/410 is a real answer: the file is not there. Anything else the
        # origin says (403, 500, 502) is the origin having a bad day.
        return ("absent" if exc.code in (404, 410) else "unknown"), url
    except (urllib.error.URLError, TimeoutError, OSError):
        return "unknown", url


def partition_already_rendered(jobs):
    """Split retryable jobs into (still_wanted, already_rendered, unknown_urls).

    `unknown_urls` is only for the report -- those jobs stay in `still_wanted`,
    since an unreachable media origin must not silently drop work.
    """
    still_wanted, already_rendered, unknown = [], [], []
    for job in jobs:
        state, url = target_media_state(job)
        if state == "present":
            already_rendered.append((job, url))
        else:
            still_wanted.append(job)
            if state == "unknown":
                unknown.append(job)
    return still_wanted, already_rendered, unknown


def chunks(values, size):
    for index in range(0, len(values), size):
        yield values[index : index + size]


def failed_jobs():
    """Yield every FAILED ArtJob, following the queue API's pagination."""
    page = 1
    while True:
        status, response = consumer.http_json(
            "GET",
            f"{consumer.KR_BASE_URL}/api/art/queue"
            f"?status=FAILED&page={page}&pageSize={PAGE_SIZE}",
        )
        if status != 200 or not response or not response.get("success"):
            raise RuntimeError(
                f"failed ArtJob listing returned HTTP {status}: "
                f"{response and response.get('message')}"
            )
        data = response.get("data") or {}
        for job in data.get("jobs") or []:
            if isinstance(job, dict):
                yield job
        if not (data.get("pagination") or {}).get("hasNextPage"):
            break
        page += 1


def job_status(job_id):
    """Current status string for one ArtJob, or None if it can't be read."""
    status, response = consumer.http_json(
        "GET", f"{consumer.KR_BASE_URL}/api/art/queue/{job_id}"
    )
    if status != 200 or not response:
        return None
    data = response.get("data") or {}
    job = data.get("job") if isinstance(data.get("job"), dict) else data
    return (job or {}).get("status")


def requeue(job_ids):
    """Requeue exact ids through the scoped endpoint. Returns (queued, failed)."""
    queued, failed = [], []
    for batch in chunks(list(job_ids), REQUEUE_BATCH_SIZE):
        status, response = consumer.http_json(
            "POST",
            f"{consumer.KR_BASE_URL}/api/art/queue/reenqueue-failed",
            {"jobIds": batch},
            timeout=180,
        )
        if status != 200 or not response or not response.get("success"):
            failed.extend(batch)
            print(
                f"  requeue batch {batch[0]}..{batch[-1]} failed: HTTP {status} "
                f"{response and response.get('message')}",
                file=sys.stderr,
            )
            continue
        data = response.get("data") or {}
        queued.extend(data.get("requeuedJobIds") or [])
        failed.extend(data.get("failedSourceJobIds") or [])
    return queued, failed


def run_canary(job_ids, timeout_seconds=CANARY_TIMEOUT_SECONDS, sleep=time.sleep):
    """Requeue a few jobs and wait for them to finish. True only if one rendered.

    One DONE is enough: it proves the host can read its models and write an
    image, which is the exact thing the backlog is blocked on. A canary that
    goes terminal without a single DONE is a hard stop.
    """
    queued, failed = requeue(job_ids)
    if not queued:
        print(f"  canary requeue failed for {sorted(failed)}", file=sys.stderr)
        return False
    print(f"  canary requeued {queued}; waiting for a terminal state…", flush=True)

    deadline = time.monotonic() + timeout_seconds
    seen = {}
    while time.monotonic() < deadline:
        seen = {job_id: job_status(job_id) for job_id in queued}
        # flush: this loop can run for 25 minutes, and a caller redirecting the
        # output to a file or a CI log should see the canary tick, not a silent
        # process followed by one burst at the end.
        print("    " + "  ".join(f"{k}={v}" for k, v in seen.items()), flush=True)
        if all(status in TERMINAL_STATUSES for status in seen.values()):
            break
        sleep(CANARY_POLL_SECONDS)
    else:
        print("  canary timed out without a terminal state.", file=sys.stderr)
        return False

    if "DONE" in seen.values():
        print("  canary rendered — the render host is healthy.")
        return True
    print(
        "  canary did not produce a single DONE — the render host is still "
        "broken. Leaving the backlog untouched.",
        file=sys.stderr,
    )
    return False


def summarize(classified):
    """Print the by-class report. `classified` is a list of (class, job)."""
    counts = {}
    for failure_class, _ in classified:
        counts[failure_class] = counts.get(failure_class, 0) + 1
    print("FAILED ArtJobs by failure class:")
    for failure_class in sorted(counts, key=lambda k: -counts[k]):
        mark = "retryable" if is_retryable(failure_class) else "NOT retryable"
        print(f"  {counts[failure_class]:5d}  {failure_class}  ({mark})")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--live",
        action="store_true",
        help="actually requeue (canary first, then the rest)",
    )
    parser.add_argument(
        "--canary",
        type=int,
        default=3,
        help="how many jobs to prove the host with before draining (default 3)",
    )
    parser.add_argument(
        "--skip-canary",
        action="store_true",
        help="drain without a canary; only for an independently confirmed host",
    )
    parser.add_argument(
        "--limit",
        type=int,
        default=0,
        help="requeue at most this many jobs (0 = no limit)",
    )
    parser.add_argument(
        "--include-rendered",
        action="store_true",
        help=(
            "also requeue jobs whose target image already exists on the media "
            "origin (they are skipped by default; this re-rolls the art)"
        ),
    )
    args = parser.parse_args()

    if args.live and not consumer.KR_API_TOKEN:
        print("KR_API_TOKEN is required for --live.", file=sys.stderr)
        return 1

    registered = registered_model_basenames()
    if registered is None:
        print(
            "WARNING: could not read the Resource registry — a model the box "
            "has lost cannot be told apart from one that was misnamed, so both "
            "will be held back.",
            file=sys.stderr,
        )
    classified = [(classify_failure(job, registered), job) for job in failed_jobs()]
    if not classified:
        print("No FAILED ArtJobs.")
        return 0

    summarize(classified)

    retryable = [job for cls, job in classified if is_retryable(cls)]
    blocked = [(cls, job) for cls, job in classified if not is_retryable(cls)]

    if blocked:
        print(f"\nNot resubmitting ({len(blocked)}) — these need a fix, not a retry:")
        for failure_class, job in blocked:
            print(f"  [{failure_class}] {failure_diagnostic(job)}")

    if not retryable:
        print("\nNothing is safe to resubmit.")
        return 0

    if args.include_rendered:
        print(
            "\n--include-rendered: not checking the media origin. Any job whose "
            "image already exists will be re-rendered over the top of it."
        )
    else:
        retryable, already_rendered, unknown = partition_already_rendered(retryable)
        if already_rendered:
            print(
                f"\nSkipping ({len(already_rendered)}) — the target image already "
                f"exists, so a requeue would overwrite it with a new render:"
            )
            for job, url in already_rendered:
                print(f"  ArtJob {job.get('id')} [{job.get('projectSlug') or '-'}] {url}")
            print("  Pass --include-rendered to re-roll them anyway.")
        if unknown:
            print(
                f"\nWARNING: could not reach the media origin for "
                f"{len(unknown)} job(s) — requeuing them rather than assuming "
                f"their image is already there: "
                f"{sorted(job.get('id') for job in unknown)}",
                file=sys.stderr,
            )
        if not retryable:
            print("\nEvery retryable job has already been rendered. Nothing to do.")
            return 0

    ids = sorted(job["id"] for job in retryable)
    if args.limit > 0:
        ids = ids[: args.limit]
        print(f"\n--limit {args.limit}: resubmitting only the {len(ids)} lowest ids.")

    print(f"\n{'LIVE' if args.live else 'DRY RUN'}: {len(ids)} job(s) resubmittable.")
    if not args.live:
        print("Pass --live to canary the render host and drain them.")
        return 0

    if args.skip_canary:
        print("Skipping the canary at the caller's request.")
    else:
        canary_ids = ids[-max(1, args.canary) :]
        print(f"Canary: {canary_ids}")
        if not run_canary(canary_ids):
            return 1
        ids = [job_id for job_id in ids if job_id not in canary_ids]
        if not ids:
            print("Canary covered the whole backlog. Done.")
            return 0

    queued, failed = requeue(ids)
    print(f"Resubmitted {len(queued)}/{len(ids)} ArtJobs.")
    if failed:
        print(f"Could not resubmit: {sorted(set(failed))}", file=sys.stderr)
        return 1
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
