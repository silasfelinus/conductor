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


def load_requests():
    """Pending-or-not request dicts from art-prompts.yaml requests:."""
    if not ART_PROMPTS_FILE.exists():
        return []
    data = yaml.safe_load(ART_PROMPTS_FILE.read_text()) or {}
    return [
        r
        for r in (data.get("requests") or [])
        if isinstance(r, dict) and r.get("prompt") and r.get("image_path")
    ]


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
    args = parser.parse_args()

    pending = filter_by_id_prefix(
        [request for request in load_requests() if is_pending(request)],
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
        (satisfied if already_satisfied(request) else todo).append(request)
    if args.limit > 0:
        todo = todo[: args.limit]

    apply_default_steps(todo, args.steps)

    if not requests:
        if blocked:
            print("No safe pending requests remain; blocked entries stay pending for prompt repair.")
        else:
            print("No pending requests in projects/art-prompts.yaml - nothing to do.")
        return 0

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

    marked = mark_done(done_ids)
    print(
        f"\n{len(todo) - failures}/{len(todo)} generated; {marked} marked done."
        + ("" if failures else " Next: python scripts/distribute_images.py --dry-run")
    )
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
