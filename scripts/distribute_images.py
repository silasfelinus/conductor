#!/usr/bin/env python3
"""
distribute_images.py — Move images from projects/process/ to their target repos.

For each image in projects/process/, determines the destination by:
  1. Checking projects/art-generate.yaml for a matching image_path basename
  2. Checking projects/art-prompts.yaml (images:, inspirations:, requests: sections)
  3. Falling back to filename convention:
       {slug}-icon/card/hero.webp  → conductor:  projects/images/{file}
       {slug}-inspiration-{n}.webp → kind_robots: public/images/artcollections/{slug}/{file}

Kind Robots repo is expected at ../kind_robots relative to the conductor root.

Usage:
  python scripts/distribute_images.py           # move files
  python scripts/distribute_images.py --dry-run  # preview without moving
"""

import re
import shutil
import sys
import yaml
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
PROCESS_DIR = REPO_ROOT / "projects" / "process"
ART_GENERATE_FILE = REPO_ROOT / "projects" / "art-generate.yaml"
ART_PROMPTS_FILE = REPO_ROOT / "projects" / "art-prompts.yaml"
KIND_ROBOTS_ROOT = REPO_ROOT.parent / "kind_robots"

IMAGE_EXTS = {".webp", ".png", ".jpg", ".jpeg"}
DRY_RUN = "--dry-run" in sys.argv


def load_yaml(path):
    with open(path) as f:
        return yaml.safe_load(f) or {}


def build_lookup(gen_data, prompts_data):
    """Build filename → {target_repo, image_path} from all yaml sources.

    art-generate.yaml takes priority since it's the active batch.
    """
    lookup = {}

    # art-prompts.yaml: images: section (conductor project assets)
    for project in prompts_data.get("images") or []:
        for variant in ("icon", "card", "hero"):
            entry = project.get(variant)
            if not isinstance(entry, dict):
                continue
            path = entry.get("image_path", "")
            if path:
                lookup[Path(path).name] = {
                    "image_path": path,
                    "target_repo": "silasfelinus/conductor",
                }

    # art-prompts.yaml: inspirations: section (kind_robots artcollections)
    for project in prompts_data.get("inspirations") or []:
        target = project.get("target_repo", "silasfelinus/kind_robots")
        for img in project.get("images") or []:
            if not isinstance(img, dict):
                continue
            path = img.get("image_path", "")
            if path:
                lookup[Path(path).name] = {
                    "image_path": path,
                    "target_repo": target,
                }

    # art-prompts.yaml: requests: section (various kind_robots paths)
    for entry in prompts_data.get("requests") or []:
        if not isinstance(entry, dict):
            continue
        path = entry.get("image_path", "")
        if path:
            lookup[Path(path).name] = {
                "image_path": path,
                "target_repo": entry.get("target_repo", "silasfelinus/kind_robots"),
            }

    # art-generate.yaml: active batch — takes priority, overrides above
    for entry in (gen_data.get("batch") or {}).get("entries") or []:
        if not isinstance(entry, dict):
            continue
        path = entry.get("image_path", "")
        if path:
            lookup[Path(path).name] = {
                "image_path": path,
                "target_repo": entry.get("target_repo", "silasfelinus/conductor"),
            }

    return lookup


def infer_destination(filename):
    """Infer destination from filename convention when not in any yaml."""
    stem = Path(filename).stem
    for variant in ("icon", "card", "hero"):
        if stem.endswith(f"-{variant}"):
            return {
                "image_path": f"projects/images/{filename}",
                "target_repo": "silasfelinus/conductor",
            }
    m = re.match(r"^(.+)-inspiration-\d+$", stem)
    if m:
        slug = m.group(1)
        return {
            "image_path": f"public/images/artcollections/{slug}/{filename}",
            "target_repo": "silasfelinus/kind_robots",
        }
    return None


def resolve_abs_path(image_path, target_repo):
    if target_repo == "silasfelinus/kind_robots":
        return KIND_ROBOTS_ROOT / image_path
    return REPO_ROOT / image_path


def _yaml_file_header(path):
    """Extract leading comment lines from a YAML file."""
    lines = []
    for line in path.read_text().splitlines():
        if line.startswith("#") or line == "":
            lines.append(line)
        else:
            break
    return "\n".join(lines).rstrip() + "\n\n" if lines else ""


def prune_art_generate(gen_data, moved_filenames):
    """Remove moved entries from art-generate.yaml and rewrite it."""
    entries = (gen_data.get("batch") or {}).get("entries") or []
    remaining = [
        e for e in entries
        if Path(e.get("image_path", "")).name not in moved_filenames
    ]
    removed = len(entries) - len(remaining)
    if removed == 0:
        return

    header = _yaml_file_header(ART_GENERATE_FILE)
    body = yaml.safe_dump(
        {"batch": {"entries": remaining}},
        sort_keys=False,
        allow_unicode=True,
        width=88,
    )
    ART_GENERATE_FILE.write_text(header + body)
    print(f"  art-generate.yaml: removed {removed} entry/entries")


def prune_art_prompts(prompts_data, moved_filenames):
    """Remove moved entries from art-prompts.yaml images: and inspirations: sections."""
    import importlib.util, sys as _sys
    _spec = importlib.util.spec_from_file_location(
        "build_workspace", Path(__file__).parent / "build_workspace.py"
    )
    _bw = importlib.util.module_from_spec(_spec)
    _spec.loader.exec_module(_bw)

    ART_PROMPTS_HEADER = _bw.ART_PROMPTS_HEADER
    pending_art_prompt_entries = _bw.pending_art_prompt_entries
    pending_inspiration_entries = _bw.pending_inspiration_entries
    normalize_art_requests = _bw.normalize_art_requests
    image_entries = pending_art_prompt_entries(prompts_data)
    inspiration_entries = pending_inspiration_entries(prompts_data)
    request_entries = normalize_art_requests(prompts_data)

    orig_img = len(prompts_data.get("images") or [])
    orig_ins = sum(len(p.get("images") or []) for p in (prompts_data.get("inspirations") or []))
    new_ins = sum(len(p.get("images") or []) for p in inspiration_entries)

    sections = {"images": image_entries, "requests": request_entries}
    if inspiration_entries:
        sections["inspirations"] = inspiration_entries

    body = yaml.safe_dump(sections, sort_keys=False, allow_unicode=True, width=88)
    ART_PROMPTS_FILE.write_text(ART_PROMPTS_HEADER + body)

    removed_img = orig_img - len(image_entries)
    removed_ins = orig_ins - new_ins
    if removed_img or removed_ins:
        print(f"  art-prompts.yaml: removed {removed_img} project asset entry/entries, {removed_ins} inspiration entry/entries")


def distribute():
    if not PROCESS_DIR.exists():
        print(f"projects/process/ not found at {PROCESS_DIR}")
        return

    if not KIND_ROBOTS_ROOT.exists() and not DRY_RUN:
        print(f"Warning: kind_robots repo not found at {KIND_ROBOTS_ROOT}")
        print("  kind_robots files will be skipped unless the repo is present.")

    gen_data = load_yaml(ART_GENERATE_FILE) if ART_GENERATE_FILE.exists() else {}
    prompts_data = load_yaml(ART_PROMPTS_FILE) if ART_PROMPTS_FILE.exists() else {}

    lookup = build_lookup(gen_data, prompts_data)

    files = sorted(
        f for f in PROCESS_DIR.iterdir()
        if f.is_file() and f.suffix.lower() in IMAGE_EXTS
    )

    if not files:
        print("No image files in projects/process/")
        return

    print(f"Found {len(files)} file(s) in projects/process/\n")

    moved = []
    skipped_missing_repo = []
    unmatched = []

    for src in files:
        fname = src.name
        match = lookup.get(fname) or infer_destination(fname)

        if not match:
            print(f"  UNMATCHED  {fname}")
            unmatched.append(fname)
            continue

        dest = resolve_abs_path(match["image_path"], match["target_repo"])

        if match["target_repo"] == "silasfelinus/kind_robots" and not KIND_ROBOTS_ROOT.exists():
            print(f"  SKIP (no kind_robots repo)  {fname}  →  {match['target_repo']}:{match['image_path']}")
            skipped_missing_repo.append(fname)
            continue

        if DRY_RUN:
            print(f"  would move  {fname}  →  {match['target_repo']}:{match['image_path']}")
            moved.append((fname, match))
        else:
            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dest)
            src.unlink()
            print(f"  moved  {fname}  →  {match['target_repo']}:{match['image_path']}")
            moved.append((fname, match))

    if not DRY_RUN and moved:
        moved_names = {fname for fname, _ in moved}
        prune_art_generate(gen_data, moved_names)
        prune_art_prompts(prompts_data, moved_names)

    conductor_moved = [m for _, m in moved if m["target_repo"] == "silasfelinus/conductor"]
    kr_moved = [m for _, m in moved if m["target_repo"] == "silasfelinus/kind_robots"]

    print(f"\n{'[dry run] ' if DRY_RUN else ''}{len(moved)} moved, {len(unmatched)} unmatched, {len(skipped_missing_repo)} skipped")

    if not DRY_RUN and moved:
        print("\nNext steps:")
        if conductor_moved:
            print("  conductor:   git add projects/images/ && git commit -m 'chore: add generated images'")
            print("  conductor:   python scripts/build_workspace.py  # prunes art-prompts.yaml")
        if kr_moved:
            print("  kind_robots: git add public/images/artcollections/ && git commit -m 'chore: add generated images'")

    if unmatched:
        print(f"\nUnmatched files (no yaml entry or known naming convention):")
        for f in unmatched:
            print(f"  {f}")


if __name__ == "__main__":
    distribute()
