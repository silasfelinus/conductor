#!/usr/bin/env python3
"""
consume_art_inspirations.py — generate the `inspirations:` section of
art-prompts.yaml.

Closes a gap the other two consumers don't cover: `consume_art_queue.py`
drains `projects/art-generate.yaml` (self-draining project icon/card/hero
art) and `consume_art_requests.py` drains the `requests:` block (ad-hoc /
missing-image / voice requests) — but nothing drains `inspirations:`, the
block used for multi-image ArtCollection teaching sets (e.g. ai-art-academy's
Great Wave teaching strip). Entries queued there sat at `status: pending`
indefinitely with every scheduled auto-art-generate run, because no script
ever turned them into ArtJobs (ai-art-academy/t-009).

  projects/art-prompts.yaml inspirations: -> images:
    -> POST {KR}/api/art/queue          (one ArtJob per image)
    -> poll GET {KR}/api/art/queue/{id} (home relay renders)
    -> GET  {KR}/api/art/image/{id}?includeImageData=true
    -> projects/process/{basename}      (distribute_images.py routes from there,
                                         using each image's target_repo)
    -> mark the image status: done in art-prompts.yaml (comment-preserving)

Reuses consume_art_queue's queue machinery so generation behaves identically.
Dry-run by default. Idempotent: an image whose target already exists in the
checked-out repo is marked done and skipped rather than regenerated.

Env: KR_API_TOKEN (required for --live), KR_BASE_URL (default matches consume_art_queue).

Usage:
  python scripts/consume_art_inspirations.py                 # dry run
  python scripts/consume_art_inspirations.py --live          # generate + download + mark done
  python scripts/consume_art_inspirations.py --live --limit 3
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

ENTRY_START_PAT = re.compile(r"^(\s*)-\s")
# image_path is the first key of each inspirations: list item, so it shares
# its line with the "- " marker (`  - image_path: ...`) rather than sitting
# on its own line the way consume_art_queue.py's art-generate.yaml entries
# do (project/variant/target_repo precede image_path there) — match both.
IMAGE_PATH_PAT = re.compile(r"^\s*(?:-\s*)?image_path:\s*(.+?)\s*$")
STATUS_PAT = re.compile(r'^(\s*)status:\s*["\']?[A-Za-z0-9_-]+["\']?\s*(#.*)?$')


def load_images():
    """Flatten inspirations: [{project, target_repo, images: [...]}] into
    per-image dicts carrying project/target_repo alongside their own fields."""
    if not ART_PROMPTS_FILE.exists():
        return []
    data = yaml.safe_load(ART_PROMPTS_FILE.read_text()) or {}
    out = []
    for block in data.get("inspirations") or []:
        if not isinstance(block, dict):
            continue
        project = block.get("project")
        target_repo = block.get("target_repo") or "silasfelinus/kind_robots"
        for img in block.get("images") or []:
            if not isinstance(img, dict) or not img.get("prompt") or not img.get("image_path"):
                continue
            entry = dict(img)
            entry["project"] = project
            entry["target_repo"] = target_repo
            out.append(entry)
    return out


def filter_by_id_prefix(entries, prefix):
    if not prefix:
        return entries
    return [e for e in entries if str(e.get("image_path") or "").startswith(prefix)]


def is_pending(entry):
    return str(entry.get("status") or "pending").strip().lower() == "pending"


def target_path(entry):
    root = REPO_ROOTS.get(entry.get("target_repo"), ROOT)
    return root / str(entry.get("image_path"))


def already_satisfied(entry):
    try:
        return target_path(entry).exists()
    except OSError:
        return False


def apply_default_steps(entries, steps):
    for entry in entries:
        if not entry.get("steps"):
            entry["steps"] = steps
    return entries


def set_image_status(text, image_path, new_status):
    """Flip the status line of the inspirations: image whose image_path
    matches. Surgical, comment-preserving line edit — mirrors
    consume_art_queue.set_entry_status / consume_art_requests.set_request_status
    so the file's curated header/prose never gets reformatted."""
    lines = text.splitlines(keepends=True)
    starts = [i for i, line in enumerate(lines) if ENTRY_START_PAT.match(line)]

    for idx, start in enumerate(starts):
        end = starts[idx + 1] if idx + 1 < len(starts) else len(lines)

        matched = False
        for j in range(start, end):
            m = IMAGE_PATH_PAT.match(lines[j])
            if m and m.group(1).strip().strip("'\"") == image_path:
                matched = True
                break

        if not matched:
            continue

        for j in range(start, end):
            sm = STATUS_PAT.match(lines[j])
            if sm:
                lines[j] = f"{sm.group(1)}status: {new_status}\n"
                return "".join(lines), True

        for j in range(start, end):
            pm = IMAGE_PATH_PAT.match(lines[j])
            if pm:
                indent = re.match(r"^(\s*)", lines[j]).group(1)
                lines.insert(j + 1, f"{indent}status: {new_status}\n")
                return "".join(lines), True

    return text, False


def mark_done(image_paths):
    if not image_paths:
        return 0
    text = ART_PROMPTS_FILE.read_text()
    changed = 0
    for image_path in image_paths:
        text, did = set_image_status(text, image_path, "done")
        if did:
            changed += 1
    if changed:
        ART_PROMPTS_FILE.write_text(text)
    return changed


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--live", action="store_true", help="actually queue, download, and mark done")
    parser.add_argument("--limit", type=int, default=0, help="max images this run (0 = all)")
    parser.add_argument("--timeout", type=int, default=600, help="seconds to wait per job")
    parser.add_argument(
        "--steps",
        type=int,
        default=FILLER_STEPS,
        help=f"sampler steps for images that don't set their own (default {FILLER_STEPS})",
    )
    parser.add_argument(
        "--id-prefix",
        default=None,
        help="only process images whose image_path starts with this prefix",
    )
    args = parser.parse_args()

    pending = filter_by_id_prefix(
        [image for image in load_images() if is_pending(image)],
        args.id_prefix,
    )

    satisfied = []
    todo = []
    for image in pending:
        (satisfied if already_satisfied(image) else todo).append(image)
    if args.limit > 0:
        todo = todo[: args.limit]

    apply_default_steps(todo, args.steps)

    if not pending:
        print("No pending images in projects/art-prompts.yaml inspirations: - nothing to do.")
        return 0

    print(
        f"{'LIVE' if args.live else 'DRY RUN'}: {len(todo)} to generate, "
        f"{len(satisfied)} already-present, via {consumer.KR_BASE_URL}\n"
    )

    if satisfied:
        for image in satisfied:
            print(f"  already present, will mark done: {image['image_path']}")
        if args.live:
            count = mark_done([image["image_path"] for image in satisfied])
            print(f"  marked {count} satisfied image(s) done.\n")

    if not args.live:
        for image in todo:
            job = consumer.entry_to_job(image)
            print(
                f"  would queue {image['image_path']}"
                f"  [{job['payload']['width']}x{job['payload']['height']}]"
                f"  \"{job['payload']['promptString'][:60]}\""
            )
        print("\nRe-run with --live to generate for real (requires KR_API_TOKEN).")
        return 0

    if not consumer.KR_API_TOKEN:
        print("KR_API_TOKEN is required for --live.", file=sys.stderr)
        return 1

    done_paths = []
    failures = 0
    for image in todo:
        name = image["image_path"]
        try:
            job_id = consumer.enqueue(consumer.entry_to_job(image))
            print(f"  queued job {job_id} for {name} - waiting...")
            job = consumer.wait_for_job(job_id, args.timeout)
            image_b64 = consumer.fetch_image_b64(job["artImageId"])
            output, warning = consumer.save_result(image, image_b64)
            print(f"  DONE {name} -> {output.relative_to(ROOT)} (ArtImage {job['artImageId']})")
            if warning:
                print(f"    WARNING: {warning}")
            done_paths.append(name)
        except Exception as error:  # noqa: BLE001 - keep draining the batch
            failures += 1
            print(f"  FAILED {name}: {error}", file=sys.stderr)

    marked = mark_done(done_paths)
    print(
        f"\n{len(todo) - failures}/{len(todo)} generated; {marked} marked done."
        + ("" if failures else " Next: python scripts/distribute_images.py --dry-run")
    )
    return 1 if failures else 0


if __name__ == "__main__":
    sys.exit(main())
