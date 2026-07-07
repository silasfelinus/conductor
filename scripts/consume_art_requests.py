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

# Reuse the proven queue client (enqueue/poll/fetch/save + quality defaults)
# rather than reinventing it. Add scripts/ to the path so this works both when
# run as a script and when imported as scripts.consume_art_requests under pytest.
sys.path.insert(0, str(Path(__file__).parent))
import consume_art_queue as consumer  # noqa: E402

ROOT = consumer.ROOT
ART_PROMPTS_FILE = ROOT / "projects" / "art-prompts.yaml"
KIND_ROBOTS_ROOT = ROOT.parent / "kind_robots"

REPO_ROOTS = {
    "silasfelinus/conductor": ROOT,
    "silasfelinus/kind_robots": KIND_ROBOTS_ROOT,
}


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


def set_request_status(text, req_id, new_status):
    """Flip the status line of the requests: entry whose id == req_id.

    Surgical, comment-preserving line edit (pyyaml round-trip would drop the
    file's curated header + images: prompts). Returns (new_text, changed)."""
    lines = text.splitlines(keepends=True)
    id_pat = re.compile(r'^(\s*)-\s+id:\s*["\']?' + re.escape(str(req_id)) + r'["\']?\s*$')
    status_pat = re.compile(r'^(\s*)status:\s*["\']?[A-Za-z0-9_-]+["\']?\s*(#.*)?$')

    start = None
    indent = ""
    for idx, line in enumerate(lines):
        m = id_pat.match(line)
        if m:
            start = idx
            indent = m.group(1)
            break
    if start is None:
        return text, False

    j = start + 1
    while j < len(lines):
        line = lines[j]
        if line.strip():
            cur_indent = len(line) - len(line.lstrip())
            # end of this entry's block: next sibling list item or a dedent
            if re.match(r"^" + re.escape(indent) + r"-\s", line):
                break
            if cur_indent <= len(indent):
                break
        sm = status_pat.match(line)
        if sm:
            lines[j] = f"{sm.group(1)}status: {new_status}\n"
            return "".join(lines), True
        j += 1
    return text, False


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


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--live", action="store_true", help="actually queue, download, and mark done")
    parser.add_argument("--limit", type=int, default=0, help="max requests this run (0 = all)")
    parser.add_argument("--timeout", type=int, default=600, help="seconds to wait per job")
    args = parser.parse_args()

    requests = [r for r in load_requests() if is_pending(r)]

    # Already-rendered requests self-drain: mark done, never regenerate.
    satisfied = [r for r in requests if already_satisfied(r)]
    todo = [r for r in requests if not already_satisfied(r)]
    if args.limit > 0:
        todo = todo[: args.limit]

    if not requests:
        print("No pending requests in projects/art-prompts.yaml - nothing to do.")
        return 0

    print(
        f"{'LIVE' if args.live else 'DRY RUN'}: {len(todo)} to generate, "
        f"{len(satisfied)} already-present, via {consumer.KR_BASE_URL}\n"
    )

    if satisfied:
        for r in satisfied:
            print(f"  already present, will mark done: {r['image_path']}")
        if args.live:
            n = mark_done([r["id"] for r in satisfied if r.get("id")])
            print(f"  marked {n} satisfied request(s) done.\n")

    if not args.live:
        for r in todo:
            job = consumer.entry_to_job(r)
            print(
                f"  would queue {r['image_path']}"
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
    for r in todo:
        name = r["image_path"]
        try:
            job_id = consumer.enqueue(consumer.entry_to_job(r))
            print(f"  queued job {job_id} for {name} - waiting...")
            job = consumer.wait_for_job(job_id, args.timeout)
            image_b64 = consumer.fetch_image_b64(job["artImageId"])
            out, warning = consumer.save_result(r, image_b64)
            print(f"  DONE {name} -> {out.relative_to(ROOT)} (ArtImage {job['artImageId']})")
            if warning:
                print(f"    WARNING: {warning}")
            if r.get("id"):
                done_ids.append(r["id"])
        except Exception as e:  # noqa: BLE001 - keep draining the batch
            failures += 1
            print(f"  FAILED {name}: {e}", file=sys.stderr)

    marked = mark_done(done_ids)
    print(
        f"\n{len(todo) - failures}/{len(todo)} generated; {marked} marked done."
        + ("" if failures else " Next: python scripts/distribute_images.py --dry-run")
    )
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
