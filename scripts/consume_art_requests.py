#!/usr/bin/env python3
"""
consume_art_requests.py — generate the `requests:` section of art-prompts.yaml.

This closes the other half of the art loop. `consume_art_queue.py` drains
`projects/art-generate.yaml` (self-draining project icon/card/hero art); this
drains the `requests:` block of `projects/art-prompts.yaml` — the ad-hoc,
missing-image, and voice ("Serendipity, generate me an image of a fox")
requests written by /api/conductor/art-request and scripts/request_art.py.

Everything goes THROUGH kind_robots (art-generator-connect routing policy):

  projects/art-prompts.yaml requests:
    -> POST {KR}/api/art/queue          (one ArtJob per request)
    -> poll GET {KR}/api/art/queue/{id} (home relay renders)
    -> GET  {KR}/api/art/image/{id}?includeImageData=true
    -> projects/process/{basename}      (distribute_images.py routes from there,
                                         using each request's image_path/target_repo)
    -> mark the request status: done in art-prompts.yaml (comment-preserving)

Reuses consume_art_queue's queue machinery so generation behaves identically.

Dry-run by default. Idempotent: a request whose target image already exists in
the checked-out repo is marked done and skipped rather than regenerated.

Env: KR_API_TOKEN (required for --live), KR_BASE_URL (default matches consume_art_queue).

Usage:
  python scripts/consume_art_requests.py                 # dry run
  python scripts/consume_art_requests.py --live          # generate + download + mark done
  python scripts/consume_art_requests.py --live --limit 3
"""

import argparse
import re
import sys
from pathlib import Path

import yaml

sys.path.insert(0, str(Path(__file__).parent))
import consume_art_queue as consumer  # noqa: E402
from art_request_staging_priority import positive_job_id  # noqa: E402

ROOT = consumer.ROOT
ART_PROMPTS_FILE = ROOT / "projects" / "art-prompts.yaml"
KIND_ROBOTS_ROOT = ROOT.parent / "kind_robots"

FILLER_STEPS = 20

REPO_ROOTS = {
    "silasfelinus/conductor": ROOT,
    "silasfelinus/kind_robots": KIND_ROBOTS_ROOT,
}

LEGACY_WEAK_PROMPT_PATTERNS = [
    re.compile(
        r"^flat minimal app icon for .+?, bold clean vector shapes, square composition, no text$",
        re.IGNORECASE,
    ),
    re.compile(
        r"^polished portrait illustration for .+?, centered subject, rich Kind Robots visual style, no text, 2:3 portrait composition$",
        re.IGNORECASE,
    ),
    re.compile(
        r"^wide cinematic hero image for .+?, expressive scene with clear atmosphere and personality, no text, 16:9 landscape composition$",
        re.IGNORECASE,
    ),
    re.compile(
        r"^polished web illustration for .+?, clear subject, cohesive Kind Robots visual style, no text$",
        re.IGNORECASE,
    ),
]
GENERIC_IMAGE_ID = re.compile(r"\b(?:art\s*)?image\s*#?\s*\d+\b", re.IGNORECASE)
PROJECT_ASSET_NAME = re.compile(
    r"^(?P<slug>.+)-(?P<variant>icon|card|hero)\.[a-z0-9]+$",
    re.IGNORECASE,
)
PROJECT_FIELD_BY_VARIANT = {
    "icon": "imagePath",
    "card": "cardPath",
    "hero": "heroPath",
}


def normalized_prompt(entry):
    return " ".join(str(entry.get("prompt") or "").split())


def weak_prompt_reason(entry):
    """Return why a request is unsafe to render, or None when it is usable.

    These are the exact boilerplate prompts formerly produced by the Kind Robots
    missing-image fallback. An image model cannot resolve a database id such as
    "Image 529", and "Kind Robots visual style" is not concrete art direction.
    Keep the request pending for repair instead of spending GPU time on generic
    robot filler.
    """
    prompt = normalized_prompt(entry)
    if not prompt:
        return "empty prompt"
    if any(pattern.match(prompt) for pattern in LEGACY_WEAK_PROMPT_PATTERNS):
        return "legacy generic missing-image fallback"
    if GENERIC_IMAGE_ID.search(prompt) and (
        "clear subject" in prompt.lower() or "visual style" in prompt.lower()
    ):
        return "database image id used as the subject"
    return None


def read_request_ledger():
    """Every request row in art-prompts.yaml, unfiltered by any staging policy.

    load_requests() is reassigned by consume_art_requests_to_media.py to apply
    Daily Dream staging order and to skip rows the relay already owns. The
    recovery pass must still see those rows: a wedged row is precisely one that
    some filter has been skipping, so reading through the patched loader would
    hide exactly the entries recovery exists to rescue.
    """
    if not ART_PROMPTS_FILE.exists():
        return []
    data = yaml.safe_load(ART_PROMPTS_FILE.read_text()) or {}
    return [
        r
        for r in (data.get("requests") or [])
        if isinstance(r, dict) and r.get("prompt") and r.get("image_path")
    ]


def load_requests():
    """Pending-or-not request dicts from art-prompts.yaml requests:."""
    return read_request_ledger()


def filter_by_id_prefix(entries, prefix):
    """Keep only entries whose id starts with prefix. No-op when prefix is falsy."""
    if not prefix:
        return entries
    return [e for e in entries if str(e.get("id") or "").startswith(prefix)]


def is_pending(entry):
    return str(entry.get("status") or "pending").strip().lower() == "pending"


def target_path(entry):
    root = REPO_ROOTS.get(entry.get("target_repo"), ROOT)
    return root / str(entry.get("image_path"))


def already_satisfied(entry):
    """True when the target image already exists in the checked-out repo."""
    try:
        return target_path(entry).exists()
    except OSError:
        return False


def job_still_reserves_submission(job_id, timeout=20):
    """True while an ArtJob still owns this request and should keep blocking
    a re-submission; False once nothing else will ever resolve the row.

    conductor/t-136: has_unresolved_submission()'s only release condition was
    "the media landed" (already_satisfied). A request whose ArtJob is later
    deleted (kind_robots' scripts/reconcile_failed_art_jobs.ts prunes
    irreparable/superseded FAILED rows) or explicitly CANCELLED never lands
    media and is never retried by anything else, so it stayed guarded
    forever -- a card that silently never gets art. Treat "the job no longer
    exists" (404) or "CANCELLED" as resolved (safe to submit again); every
    other status (PENDING, RUNNING, DONE not yet reflected in
    already_satisfied, FAILED awaiting drain_failed_art_backlog.py's
    in-place requeue) still reserves the row exactly as before -- this must
    not reopen the t-133 outage-duplicate-submission bug, so it only ever
    narrows the guard for the two terminal "nothing else will act" states.

    Requires KR_API_TOKEN; without it (offline/dry-run/tests) or on any
    network/response hiccup this stays conservative and reports the job as
    still reserving the row, matching pre-t-136 behavior exactly.
    """
    if not consumer.KR_API_TOKEN:
        return True
    try:
        status, resp = consumer.http_json(
            "GET", f"{consumer.KR_BASE_URL}/api/art/queue/{job_id}", timeout=timeout
        )
    except Exception:  # noqa: BLE001 - network hiccup, stay conservative
        return True
    if status == 404:
        return False
    if status != 200 or not isinstance(resp, dict) or not resp.get("success"):
        return True
    job = (resp.get("data") or {}).get("job") or {}
    return str(job.get("status") or "").upper() != "CANCELLED"


def fetch_job(job_id, timeout=20):
    """Return the ArtJob record for job_id, or None when it cannot be read.

    Deliberately total: every failure mode (no token, network hiccup, non-200,
    unsuccessful envelope) collapses to None so callers can treat "I could not
    look" and "nothing useful there" identically and simply do nothing.
    """
    if not consumer.KR_API_TOKEN:
        return None
    try:
        status, resp = consumer.http_json(
            "GET", f"{consumer.KR_BASE_URL}/api/art/queue/{job_id}", timeout=timeout
        )
    except Exception:  # noqa: BLE001 - network hiccup, nothing to adopt
        return None
    if status != 200 or not isinstance(resp, dict) or not resp.get("success"):
        return None
    return (resp.get("data") or {}).get("job") or None


def finished_submission_art_image(entry, timeout=20):
    """ArtImage id of a recorded ArtJob that already rendered, else None.

    conductor/t-162: a row whose ArtJob reached DONE but whose media never
    landed was wedged permanently. already_satisfied() stays False, so the row
    is never marked done; job_still_reserves_submission() keeps returning True
    (DONE is neither CANCELLED nor a 404), so it is never re-submitted either.
    Nothing else in the pipeline acts on it. Observed 2026-09-14: 16 rows in
    that state, the oldest (ArtJobs 18426-18429) stuck for over a week, each
    holding a perfectly good ArtImage nobody ever downloaded.

    The render is not lost -- only the download half of the handoff is, when
    the run that submitted the job exits before the relay finishes it. So adopt
    the existing render rather than re-queueing a second one: re-submitting
    would burn a GPU render to reproduce an image that already exists, and is
    the exact duplicate-enqueue shape t-133 closed.
    """
    job_id = positive_job_id(entry.get("last_art_job_id"))
    if job_id is None:
        return None
    job = fetch_job(job_id, timeout=timeout)
    if not job or str(job.get("status") or "").upper() != "DONE":
        return None
    return positive_job_id(job.get("artImageId"))


def recover_finished_submissions(entries, *, live, timeout=20):
    """Download renders for rows whose ArtJob finished but whose media never
    arrived, and return (recovered_ids, failure_count).

    Never enqueues anything, so this cannot reopen t-133 no matter how many
    rows it touches. Lands each render in projects/process/ exactly as the
    normal success path does, leaving distribute_images.py to route it.
    """
    recovered_ids = []
    failures = 0

    for entry in entries:
        if not is_pending(entry) or already_satisfied(entry):
            continue
        # Already staged and waiting on delivery. kind_robots media targets are
        # RETAINED in projects/process/ indefinitely (distribute_images.py never
        # moves them -- /public/images/** ships via the relay, not git), so this
        # would otherwise re-download the same bytes on every run, forever.
        staged = consumer.PROCESS_DIR / consumer.staged_filename(entry)
        if staged.exists():
            continue

        art_image_id = finished_submission_art_image(entry, timeout=timeout)
        if art_image_id is None:
            continue

        name = entry["image_path"]
        if not live:
            print(f"  would adopt ArtImage {art_image_id} for {name} (its ArtJob is already DONE)")
            continue

        try:
            image_b64 = consumer.fetch_image_b64(art_image_id)
            output, warning = consumer.save_result(entry, image_b64)
            print(f"  ADOPTED {name} -> {output.relative_to(ROOT)} (ArtImage {art_image_id})")
            if warning:
                print(f"    WARNING: {warning}")
        except Exception as error:  # noqa: BLE001 - keep draining the batch
            failures += 1
            print(f"  FAILED to adopt {name}: {error}", file=sys.stderr)
            continue

        # Landing the render is what unwedges the row; the Project cover sync is
        # a bonus that only applies to genuine project-art rows. project_art_sync_
        # payload() recovers a slug from the `{slug}-{variant}.webp` filename, which
        # misfires on card art that merely looks like it ("world-card.webp" ->
        # "Project world not found"). Letting that 404 abort the adoption would
        # leave the row pending with its render already downloaded -- re-wedging
        # the exact state this function exists to clear.
        try:
            if sync_project_art(entry, art_image_id):
                print("    synchronized Project cover path + ArtImage relation")
        except Exception as error:  # noqa: BLE001 - cosmetic next to the render
            print(f"    WARNING: Project cover sync skipped: {error}", file=sys.stderr)

        if entry.get("id"):
            recovered_ids.append(entry["id"])

    return recovered_ids, failures


def has_unresolved_submission(entry, *, check_live=False):
    """True when this entry already owns an ArtJob that hasn't finished yet.

    record_submitted_job() writes ONLY `last_art_job_id` -- it never touches
    `status`, which stays "pending" for as long as the job is in flight (and
    forever, if the job never completes). So `is_pending()` alone cannot tell
    "genuinely never submitted" from "already submitted, still rendering, or
    the render host has been down for days": every caller that filters on
    is_pending() and not also this would re-POST the same request on every
    run once nothing is left to mark it done.

    conductor/t-133 (2026-08-28): this let the Mandarin Tutor bulk lane
    (submit_mandarin_tutor_artjobs.py) and the ad-hoc drip consumer (this
    module's own main(), via consume_art_requests_to_media.py) both re-POST
    the same 709 targets, 4-5x each, during a render-host outage -- 2882
    FAILED rows, 75% of them duplicate enqueues of work already sitting
    FAILED. A prior guard (art_request_staging_priority.py's
    should_consume_after_submission) covers exactly this shape but only for
    Daily Dream requests; this is the same in-flight check, generalized to
    every source and applied at the one place ("is this row safe to submit")
    both lanes actually share.

    conductor/t-136: `check_live=True` additionally releases the guard when
    job_still_reserves_submission() confirms the recorded job is deleted or
    CANCELLED -- see that function's docstring. Callers that can't or don't
    want a network round-trip (offline checks, most tests) leave this False
    and get the original already_satisfied-only behavior unchanged.
    """
    job_id = positive_job_id(entry.get("last_art_job_id"))
    if job_id is None:
        return False
    if already_satisfied(entry):
        return False
    if check_live and not job_still_reserves_submission(job_id):
        return False
    return True


def apply_default_steps(entries, steps):
    """Give each entry a `steps` value unless it already set its own.

    entry_to_job() reads `steps` off the entry, so this scopes the filler-tuned
    step count to this lane (missing-image / ad-hoc / voice) and leaves the
    project-art lane on its own 30-step default. Mutates in place; not persisted
    -- mark_done does surgical line edits, never a full YAML re-dump.

    Engines with a native step count are left alone. Krea 2 Turbo is a distilled
    8-step model; stamping the filler default (20) on it pushes it out of
    distribution and over-cooks the image. Before this guard, every daily-dream
    request through this lane ran at 20 steps / cfg 7 instead of 8 / 1
    (2026-08-08, ArtJobs 7953/7954/7961/7966).
    """
    for entry in entries:
        if entry.get("steps"):
            continue
        engine = consumer.normalize_engine(entry.get("engine"))
        if engine in consumer.ENGINE_DEFAULT_STEPS:
            continue
        entry["steps"] = steps
    return entries


def find_request_block(lines, req_id):
    """Locate the requests: list item whose id == req_id.

    Returns (start_index, end_index_exclusive, indent) for the "- id: ..." line
    through the last line owned by that item, or None if req_id isn't present.
    Shared by set_request_status and set_request_field so both edit the exact
    same block boundaries.
    """
    id_pat = re.compile(r'^(\s*)-\s+id:\s*["\']?' + re.escape(str(req_id)) + r'["\']?\s*$')
    start = None
    indent = ""
    for idx, line in enumerate(lines):
        match = id_pat.match(line)
        if match:
            start = idx
            indent = match.group(1)
            break
    if start is None:
        return None

    end = start + 1
    while end < len(lines):
        line = lines[end]
        if line.strip():
            current_indent = len(line) - len(line.lstrip())
            if re.match(r"^" + re.escape(indent) + r"-\s", line):
                break
            if current_indent <= len(indent):
                break
        end += 1
    return start, end, indent


def set_request_status(text, req_id, new_status):
    """Flip the status line of the requests: entry whose id == req_id.

    Surgical, comment-preserving line edit (pyyaml round-trip would drop the
    file's curated header + images: prompts). Returns (new_text, changed).
    """
    lines = text.splitlines(keepends=True)
    status_pat = re.compile(r'^(\s*)status:\s*["\']?[A-Za-z0-9_-]+["\']?\s*(#.*)?$')

    block = find_request_block(lines, req_id)
    if block is None:
        return text, False
    start, end, _indent = block

    for index in range(start + 1, end):
        status_match = status_pat.match(lines[index])
        if status_match:
            lines[index] = f"{status_match.group(1)}status: {new_status}\n"
            return "".join(lines), True
    return text, False


def set_request_field(text, req_id, field_name, value):
    """Set (or insert) a scalar field on the requests: entry whose id == req_id.

    Same surgical, comment-preserving approach as set_request_status: replaces
    the field's line in place if present, otherwise inserts a new line right
    after the id line at the sibling fields' indent. Returns (new_text, changed).
    """
    lines = text.splitlines(keepends=True)
    field_pat = re.compile(r"^(\s*)" + re.escape(field_name) + r':\s*.*$')

    block = find_request_block(lines, req_id)
    if block is None:
        return text, False
    start, end, indent = block

    for index in range(start + 1, end):
        field_match = field_pat.match(lines[index])
        if field_match:
            lines[index] = f"{field_match.group(1)}{field_name}: {value}\n"
            return "".join(lines), True

    lines.insert(start + 1, f"{indent}  {field_name}: {value}\n")
    return "".join(lines), True


def record_submitted_job(req_id, job_id):
    """Durably record a submitted ArtJob id on its request entry before waiting.

    Called immediately after enqueue() succeeds, before wait_for_job() -- so a
    later crash, Ctrl-C, or local poll timeout still leaves a durable trail in
    art-prompts.yaml of which ArtJob was submitted for this request, instead of
    the id existing only in that run's stdout. This closes the gap behind
    conductor/t-095: a submitted ArtJob known only from a session's own prose
    notes (unrecoverable once out of context) rather than from the request file
    itself. Returns False (no-op) if req_id is missing or unknown.
    """
    if not req_id:
        return False
    text = ART_PROMPTS_FILE.read_text()
    new_text, changed = set_request_field(text, req_id, "last_art_job_id", job_id)
    if changed:
        ART_PROMPTS_FILE.write_text(new_text)
    return changed


def mark_done(req_ids):
    """Set status: done for each id (single read/write). Returns count changed."""
    if not req_ids:
        return 0
    text = ART_PROMPTS_FILE.read_text()
    changed = 0
    for req_id in req_ids:
        text, did = set_request_status(text, req_id, "done")
        if did:
            changed += 1
    if changed:
        ART_PROMPTS_FILE.write_text(text)
    return changed


def project_art_sync_payload(entry, art_image_id):
    """Build the Kind Robots Project cover synchronization payload when applicable.

    New missing-image reports carry explicit project metadata. Older Conductor
    project-art requests are recoverable from `{slug}-{variant}.webp`, allowing
    the existing backlog to self-heal without rewriting every historical entry.
    """
    image_path = str(entry.get("image_path") or "").strip().replace("\\", "/")
    source_url = str(entry.get("source_url") or "").strip()
    target_repo = str(entry.get("target_repo") or "").strip()
    explicit_slug = str(entry.get("project_slug") or "").strip()
    explicit_field = str(entry.get("project_field") or "").strip()
    basename = Path(image_path).name
    match = PROJECT_ASSET_NAME.match(basename)
    variant = str(
        entry.get("variant") or (match.group("variant") if match else "")
    ).lower()
    project_field = (
        explicit_field
        if explicit_field in PROJECT_FIELD_BY_VARIANT.values()
        else PROJECT_FIELD_BY_VARIANT.get(variant)
    )
    project_slug = explicit_slug or (match.group("slug") if match else "")

    if not project_slug or not project_field:
        return None

    project_id = entry.get("project_id")
    try:
        project_id = int(project_id) if project_id is not None else None
    except (TypeError, ValueError):
        project_id = None

    return {
        "projectId": project_id,
        "projectSlug": project_slug,
        "projectField": project_field,
        "variant": variant,
        "targetRepo": target_repo,
        "imagePath": image_path,
        "sourceUrl": source_url,
        "artImageId": int(art_image_id),
    }


def sync_project_art(entry, art_image_id):
    payload = project_art_sync_payload(entry, art_image_id)
    if not payload:
        return False

    status, response = consumer.http_json(
        "POST",
        f"{consumer.KR_BASE_URL}/api/conductor/project-art-complete",
        payload,
    )
    if status != 200 or not response or not response.get("success"):
        detail = response.get("message") if isinstance(response, dict) else response
        raise RuntimeError(f"project art sync failed: HTTP {status} {detail}")
    return True


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--live", action="store_true", help="actually queue, download, and mark done")
    parser.add_argument("--limit", type=int, default=0, help="max requests this run (0 = all)")
    parser.add_argument("--timeout", type=int, default=600, help="seconds to wait per job")
    parser.add_argument(
        "--steps",
        type=int,
        default=FILLER_STEPS,
        help=f"sampler steps for requests that don't set their own (default {FILLER_STEPS}, tuned for filler art)",
    )
    parser.add_argument(
        "--id-prefix",
        default=None,
        help="only process requests whose id starts with this prefix (scope a run to one source/batch)",
    )
    parser.add_argument(
        "--force",
        action="store_true",
        help=(
            "re-submit even when the target image already exists. The default "
            "skip-if-present behaviour is right for resumed batches, but it makes "
            "a bad render permanent: once the file is on media the entry is marked "
            "done and no prompt fix can ever reach it. Use after correcting a "
            "prompt, scoped with --id-prefix."
        ),
    )
    parser.add_argument(
        "--submit-only",
        action="store_true",
        help=(
            "enqueue each request and record its ArtJob id, then stop -- do not "
            "wait for the render or download the result. Use when a batch is far "
            "larger than one session/job can sit on: the relay renders in its own "
            "time and a later run marks the rows done once the media path is live "
            "(same handoff shape as scripts/submit_daily_dream_art.py). "
            "Requests keep status: pending so that later pass can find them."
        ),
    )
    args = parser.parse_args()

    # Rescue pass first: a row whose ArtJob already finished can never reach the
    # pending filter below (has_unresolved_submission holds it) nor the satisfied
    # pass (its media never landed), so it has to be resolved before either runs.
    recovered_ids, recovery_failures = recover_finished_submissions(
        filter_by_id_prefix(read_request_ledger(), args.id_prefix),
        live=args.live,
    )
    if recovered_ids:
        # Deliberately NOT mark_done: staging a file in projects/process/ is not
        # delivery. distribute_images.py prunes a request only once the file
        # actually reached its destination, and RETAINS every kind_robots media
        # target there instead of moving it. Marking these done here would
        # re-create ai-art-academy/t-010 (2026-07-27), where a request pruned on
        # apparent delivery silently lost the record that real delivery never
        # happened -- the same class of bug this whole change exists to remove.
        print(
            f"Adopted {len(recovered_ids)} already-finished render(s) into "
            "projects/process/; distribute_images.py resolves their requests "
            "once each one actually lands.\n"
        )

    pending = filter_by_id_prefix(
        [
            request
            for request in load_requests()
            if is_pending(request)
            and not has_unresolved_submission(request, check_live=True)
        ],
        args.id_prefix,
    )
    blocked = [
        (request, weak_prompt_reason(request))
        for request in pending
        if weak_prompt_reason(request)
    ]
    requests = [request for request in pending if not weak_prompt_reason(request)]

    if blocked:
        print(f"BLOCKED: {len(blocked)} weak prompt request(s) need repair; none will be queued.")
        for request, reason in blocked:
            print(
                f"  blocked {request.get('id') or request.get('image_path')}: {reason} — "
                f'"{normalized_prompt(request)[:100]}"'
            )
        print()

    satisfied = []
    todo = []
    for request in requests:
        present = already_satisfied(request) and not args.force
        (satisfied if present else todo).append(request)
    if args.limit > 0:
        todo = todo[: args.limit]

    apply_default_steps(todo, args.steps)

    if not requests:
        if blocked:
            print("No safe pending requests remain; blocked entries stay pending for prompt repair.")
        else:
            print("No pending requests in projects/art-prompts.yaml - nothing to do.")
        return 1 if recovery_failures else 0

    print(
        f"{'LIVE' if args.live else 'DRY RUN'}: {len(todo)} to generate, "
        f"{len(satisfied)} already-present, via {consumer.KR_BASE_URL}\n"
    )

    if satisfied:
        for request in satisfied:
            print(f"  already present, will mark done: {request['image_path']}")
        if args.live:
            count = mark_done([request["id"] for request in satisfied if request.get("id")])
            print(f"  marked {count} satisfied request(s) done.\n")

    if not args.live:
        for request in todo:
            job = consumer.entry_to_job(request)
            print(
                f"  would queue {request['image_path']}"
                f"  [{job['payload']['width']}x{job['payload']['height']}]"
                f"  \"{job['payload']['promptString'][:60]}\""
            )
        print("\nRe-run with --live to generate for real (requires KR_API_TOKEN).")
        return 0

    if not consumer.KR_API_TOKEN:
        print("KR_API_TOKEN is required for --live.", file=sys.stderr)
        return 1

    done_ids = []
    failures = 0
    for request in todo:
        name = request["image_path"]
        try:
            job_id = consumer.enqueue(consumer.entry_to_job(request))
            record_submitted_job(request.get("id"), job_id)
            if args.submit_only:
                print(f"  queued job {job_id} for {name} - handed off to the relay")
                continue
            print(f"  queued job {job_id} for {name} - waiting...")
            job = consumer.wait_for_job(job_id, args.timeout)
            image_b64 = consumer.fetch_image_b64(job["artImageId"])
            output, warning = consumer.save_result(request, image_b64)
            print(f"  DONE {name} -> {output.relative_to(ROOT)} (ArtImage {job['artImageId']})")
            if warning:
                print(f"    WARNING: {warning}")
            if sync_project_art(request, job["artImageId"]):
                print("    synchronized Project cover path + ArtImage relation")
            if request.get("id"):
                done_ids.append(request["id"])
        except Exception as error:  # noqa: BLE001 - keep draining the batch
            failures += 1
            print(f"  FAILED {name}: {error}", file=sys.stderr)

    if args.submit_only:
        print(
            f"\n{len(todo) - failures}/{len(todo)} submitted; ArtJob ids recorded on "
            "each request. They stay pending until a later run finds the media path live."
        )
        return 1 if failures or recovery_failures else 0

    marked = mark_done(done_ids)
    print(
        f"\n{len(todo) - failures}/{len(todo)} generated; {marked} marked done."
        + ("" if failures else " Next: python scripts/distribute_images.py --dry-run")
    )
    return 1 if failures or recovery_failures else 0


if __name__ == "__main__":
    sys.exit(main())
