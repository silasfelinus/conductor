#!/usr/bin/env python3
"""
distribute_images.py — Move images from projects/process/ to their target repos.

For each image in projects/process/, determines the destination by:
  1. Checking projects/art-generate.yaml for a matching image_path basename
  2. Checking projects/art-prompts.yaml (images:, inspirations:, requests: sections)
  3. Falling back to filename convention:
       {slug}-icon/card/hero.webp  → conductor:  projects/images/{file}
       {slug}-inspiration-{n}.webp → kind_robots: public/images/{slug}/{file}
                                   → conductor:  projects/{slug}/inspirations/{file}
  4. Falling back to slug match: a file whose name starts with a known slug
     (a conductor project or an existing kind_robots public/images/ folder) but
     has no specific resolution becomes a new inspiration:
       kind_robots: public/images/{slug}/{slug}-inspiration-{n}.webp
       conductor:  projects/{slug}/inspirations/{slug}-inspiration-{n}.webp

If a destination file already exists, the original is preserved as a new
inspiration in its slug's folder (kind_robots public/images/{slug}/) and,
when the slug is a conductor project, also copied to projects/{slug}/inspirations/.
The new image replaces it. On every run, collections.json and a gallery.json for
every indexed folder are regenerated (with full filenames) so folder<->collection
parity holds and each collection resolves on Vercel, where the CDN can't be globbed.

Kind Robots repo is expected at ../kind_robots relative to the conductor root.

Usage:
  python scripts/distribute_images.py           # move files
  python scripts/distribute_images.py --dry-run  # preview without moving
"""

import re
import shutil
import sys
from pathlib import Path

import yaml

REPO_ROOT = Path(__file__).parent.parent
PROCESS_DIR = REPO_ROOT / "projects" / "process"
UNMATCHED_DIR = PROCESS_DIR / "unmatched"
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

    for entry in prompts_data.get("requests") or []:
        if not isinstance(entry, dict):
            continue
        path = entry.get("image_path", "")
        if path:
            lookup[Path(path).name] = {
                "image_path": path,
                "target_repo": entry.get("target_repo", "silasfelinus/kind_robots"),
            }

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


def conductor_project_slugs():
    slugs = set()
    projects_dir = REPO_ROOT / "projects"
    if projects_dir.exists():
        for d in projects_dir.iterdir():
            if d.is_dir() and not d.name.startswith("_") and d.name not in ("images", "process"):
                slugs.add(d.name)
    return slugs


def known_slugs():
    """Slugs a loose file can match: conductor projects + kind_robots image folders."""
    slugs = conductor_project_slugs()
    kr_images = KIND_ROBOTS_ROOT / "public" / "images"
    if kr_images.exists():
        for d in kr_images.iterdir():
            if d.is_dir():
                slugs.add(d.name)
                for sub in d.iterdir():
                    if sub.is_dir():
                        slugs.add(sub.name)
    return slugs


def slug_for_stem(stem, slugs):
    """Longest known slug that the stem equals or starts with (separator-delimited)."""
    matches = [
        s for s in slugs
        if stem == s or stem.startswith(f"{s}-") or stem.startswith(f"{s}_")
    ]
    return max(matches, key=len) if matches else None


def slug_folder_rel(slug):
    """Folder (relative to public/images) that owns a slug's collection.

    Placement convention (Silas, 2026-07-05): nested {context}/{slug} is
    canonical, flat {slug} stays valid, artcollections/{slug} is the
    legacy/unsorted fallback. An existing nested folder wins; otherwise an
    existing flat folder; otherwise new files start a flat folder (nesting
    is adopted opportunistically, never by bulk move).
    """
    images_root = KIND_ROBOTS_ROOT / "public" / "images"
    if images_root.exists():
        for ctx in sorted(images_root.iterdir()):
            if not ctx.is_dir() or ctx.name in (slug, "artcollections"):
                continue
            if (ctx / slug).is_dir():
                return f"{ctx.name}/{slug}"
    return slug


def next_numbered_path(slug, utility, suffix):
    """Next free {folder}/{slug}-{utility}-{n}{suffix}, honoring nesting."""
    folder_rel = slug_folder_rel(slug)
    folder = KIND_ROBOTS_ROOT / "public" / "images" / folder_rel
    n = 1
    while (folder / f"{slug}-{utility}-{n}{suffix}").exists():
        n += 1
    return f"public/images/{folder_rel}/{slug}-{utility}-{n}{suffix}"


def next_inspiration_path(slug, suffix):
    """Back-compat wrapper: next free inspiration slot for a slug."""
    return next_numbered_path(slug, "inspiration", suffix)


def next_project_numbered_path(slug, utility, suffix):
    folder = REPO_ROOT / "projects" / slug / "inspirations"
    n = 1
    while (folder / f"{slug}-{utility}-{n}{suffix}").exists():
        n += 1
    return folder / f"{slug}-{utility}-{n}{suffix}"


def slug_and_utility_from_dest_filename(filename, slugs):
    """(slug, utility) for preserving an overwritten file.

    {slug}-icon.webp -> (slug, icon); {slug}-inspiration-3.webp ->
    (slug, inspiration); unrecognized names preserve as inspiration.
    """
    stem = Path(filename).stem
    utility = "inspiration"
    m = re.search(r"[-_](icon|card|hero)$", stem)
    if m:
        utility = m.group(1)
        stem = stem[: m.start()]
    else:
        m = re.search(r"[-_]([a-z]+)[-_]\d+$", stem)
        if m:
            utility = m.group(1)
            stem = stem[: m.start()]
    return (slug_for_stem(stem, slugs) or stem), utility


def slug_from_dest_filename(filename, slugs):
    """Back-compat wrapper returning just the slug."""
    return slug_and_utility_from_dest_filename(filename, slugs)[0]


def project_inspiration_dest_for_match(match, slugs, src_path):
    """Return a conductor project inspiration path for a kind_robots image.

    Only mirrors images whose slug maps to an actual conductor project. The
    kind_robots ArtCollection remains the app/UI copy; this mirror keeps each
    project folder friendly when opened directly.
    """
    if match.get("target_repo") != "silasfelinus/kind_robots":
        return None

    image_path = str(match.get("image_path") or "")
    parts = Path(image_path).parts
    if len(parts) < 4 or parts[:2] != ("public", "images"):
        return None

    filename = parts[-1]
    project_slugs = conductor_project_slugs()
    slug = slug_for_stem(Path(filename).stem, project_slugs)

    if slug is None:
        if len(parts) >= 5 and parts[-2] in project_slugs:
            slug = parts[-2]
        elif len(parts) == 4 and parts[-2] in project_slugs:
            slug = parts[-2]

    if slug is None:
        return None

    dest = REPO_ROOT / "projects" / slug / "inspirations" / filename
    if not dest.exists() or dest.read_bytes() == src_path.read_bytes():
        return dest

    _, utility = slug_and_utility_from_dest_filename(filename, slugs)
    return next_project_numbered_path(slug, utility, Path(filename).suffix.lower())


def mirror_project_inspiration(src_path, match, slugs):
    dest = project_inspiration_dest_for_match(match, slugs, src_path)
    if dest is None:
        return None

    if DRY_RUN:
        action = "already exists" if dest.exists() else "would copy"
        print(f"  {action} project inspiration  {dest.relative_to(REPO_ROOT)}")
        return dest

    dest.parent.mkdir(parents=True, exist_ok=True)
    if dest.exists() and dest.read_bytes() == src_path.read_bytes():
        print(f"  project inspiration already exists  {dest.relative_to(REPO_ROOT)}")
        return dest

    shutil.copy2(src_path, dest)
    print(f"  copied project inspiration  {dest.relative_to(REPO_ROOT)}")
    return dest


def write_gallery_manifest(folder_rel):
    """Regenerate gallery.json for a collection folder (flat "slug" or
    nested "context/slug" relative to public/images).

    Writes FULL filenames (name, not stem). The kind_robots reader
    (server/utils/folderCollections.ts -> stemsToUrls) appends .webp to any
    entry lacking an image extension, so a bare stem like "comfy-4032" would
    resolve to comfy-4032.webp and 404 a .png. Keeping the extension makes
    .png/.jpg/.gif folders resolve correctly."""
    import json

    folder = KIND_ROBOTS_ROOT / "public" / "images" / folder_rel
    if not folder.exists():
        return
    names = sorted(
        f.name for f in folder.iterdir()
        if f.is_file() and f.suffix.lower() in IMAGE_EXTS
    )
    (folder / "gallery.json").write_text(json.dumps(names) + "\n")


def write_collections_index():
    """Regenerate public/images/collections.json: slug -> folder path
    (relative to public/images). Lets the kind_robots folder-collection
    endpoint resolve nested folders on the CDN, where it cannot glob.
    Precedence per the placement convention: nested > flat > artcollections.
    """
    import json

    images_root = KIND_ROBOTS_ROOT / "public" / "images"
    if not images_root.exists():
        return {}

    def has_images(d):
        return any(
            f.is_file() and f.suffix.lower() in IMAGE_EXTS for f in d.iterdir()
        )

    index = {}
    legacy = images_root / "artcollections"
    if legacy.is_dir():
        for d in sorted(legacy.iterdir()):
            if d.is_dir() and has_images(d):
                index[d.name] = f"artcollections/{d.name}"
    for d in sorted(images_root.iterdir()):
        if d.is_dir() and d.name != "artcollections" and has_images(d):
            index[d.name] = d.name
    for ctx in sorted(images_root.iterdir()):
        if not ctx.is_dir() or ctx.name == "artcollections":
            continue
        for d in sorted(ctx.iterdir()):
            if d.is_dir() and has_images(d):
                index[d.name] = f"{ctx.name}/{d.name}"

    (images_root / "collections.json").write_text(
        json.dumps(index, indent=2, sort_keys=True) + "\n"
    )
    return index


def infer_destination(filename, slugs):
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
            "image_path": f"public/images/{slug_folder_rel(slug)}/{filename}",
            "target_repo": "silasfelinus/kind_robots",
        }
    slug = slug_for_stem(stem, slugs)
    if slug:
        return {
            "image_path": next_inspiration_path(slug, Path(filename).suffix.lower()),
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
    import importlib.util

    spec = importlib.util.spec_from_file_location(
        "build_workspace", Path(__file__).parent / "build_workspace.py"
    )
    bw = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(bw)

    art_prompts_header = bw.ART_PROMPTS_HEADER
    pending_art_prompt_entries = bw.pending_art_prompt_entries
    pending_inspiration_entries = bw.pending_inspiration_entries
    normalize_art_requests = bw.normalize_art_requests
    image_entries = pending_art_prompt_entries(prompts_data)
    inspiration_entries = pending_inspiration_entries(prompts_data)
    request_entries = normalize_art_requests(prompts_data)

    orig_req = len(request_entries)
    request_entries = [
        e for e in request_entries
        if Path(str(e.get("image_path") or "")).name not in moved_filenames
    ]

    orig_img = len(prompts_data.get("images") or [])
    orig_ins = sum(len(p.get("images") or []) for p in (prompts_data.get("inspirations") or []))
    new_ins = sum(len(p.get("images") or []) for p in inspiration_entries)

    sections = {"images": image_entries, "requests": request_entries}
    if inspiration_entries:
        sections["inspirations"] = inspiration_entries

    body = yaml.safe_dump(sections, sort_keys=False, allow_unicode=True, width=88)
    ART_PROMPTS_FILE.write_text(art_prompts_header + body)

    removed_img = orig_img - len(image_entries)
    removed_ins = orig_ins - new_ins
    removed_req = orig_req - len(request_entries)
    if removed_img or removed_ins or removed_req:
        print(
            "  art-prompts.yaml: removed "
            f"{removed_img} project asset entry/entries, "
            f"{removed_ins} inspiration entry/entries, "
            f"{removed_req} request entry/entries"
        )


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
    slugs = known_slugs()
    touched_slugs = set()

    files = sorted(
        f for f in PROCESS_DIR.iterdir()
        if f.is_file() and f.suffix.lower() in IMAGE_EXTS
    )

    if not files:
        print("No image files in projects/process/")
        return

    print(f"Found {len(files)} file(s) in projects/process/\n")

    moved = []
    mirrored = []
    skipped_missing_repo = []
    unmatched = []

    for src in files:
        fname = src.name
        match = lookup.get(fname) or infer_destination(fname, slugs)

        if not match:
            UNMATCHED_DIR.mkdir(parents=True, exist_ok=True)
            dest = UNMATCHED_DIR / fname
            if DRY_RUN:
                print(f"  would move (unmatched)  {fname}  →  projects/process/unmatched/")
            else:
                shutil.move(str(src), dest)
                print(f"  unmatched  {fname}  →  projects/process/unmatched/")
            unmatched.append(fname)
            continue

        dest = resolve_abs_path(match["image_path"], match["target_repo"])

        if match["target_repo"] == "silasfelinus/kind_robots" and not KIND_ROBOTS_ROOT.exists():
            print(f"  SKIP (no kind_robots repo)  {fname}  →  {match['target_repo']}:{match['image_path']}")
            skipped_missing_repo.append(fname)
            continue

        preserve_path = None
        if dest.exists() and dest.read_bytes() != src.read_bytes():
            if not KIND_ROBOTS_ROOT.exists():
                print(f"  SKIP (would replace {match['image_path']} but no kind_robots repo to preserve original)  {fname}")
                skipped_missing_repo.append(fname)
                continue
            slug, utility = slug_and_utility_from_dest_filename(fname, slugs)
            preserve_path = next_numbered_path(slug, utility, dest.suffix.lower())

        if DRY_RUN:
            if preserve_path:
                preserve_match = {
                    "image_path": preserve_path,
                    "target_repo": "silasfelinus/kind_robots",
                }
                mirror_project_inspiration(dest, preserve_match, slugs)
                print(f"  would preserve original  {match['image_path']}  →  silasfelinus/kind_robots:{preserve_path}")
            mirrored_dest = mirror_project_inspiration(src, match, slugs)
            if mirrored_dest:
                mirrored.append(str(mirrored_dest.relative_to(REPO_ROOT)))
            print(f"  would move  {fname}  →  {match['target_repo']}:{match['image_path']}")
            moved.append((fname, match))
        else:
            if preserve_path:
                preserve_match = {
                    "image_path": preserve_path,
                    "target_repo": "silasfelinus/kind_robots",
                }
                mirrored_dest = mirror_project_inspiration(dest, preserve_match, slugs)
                if mirrored_dest:
                    mirrored.append(str(mirrored_dest.relative_to(REPO_ROOT)))
                preserve_dest = KIND_ROBOTS_ROOT / preserve_path
                preserve_dest.parent.mkdir(parents=True, exist_ok=True)
                shutil.move(str(dest), preserve_dest)
                touched_slugs.add(
                    str(Path(preserve_path).parent.relative_to("public/images"))
                )
                print(f"  preserved original  {match['image_path']}  →  silasfelinus/kind_robots:{preserve_path}")

            mirrored_dest = mirror_project_inspiration(src, match, slugs)
            if mirrored_dest:
                mirrored.append(str(mirrored_dest.relative_to(REPO_ROOT)))

            dest.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(src, dest)
            src.unlink()
            print(f"  moved  {fname}  →  {match['target_repo']}:{match['image_path']}")
            moved.append((fname, match))

        if match["target_repo"] == "silasfelinus/kind_robots":
            parts = Path(match["image_path"]).parts
            if parts[:2] == ("public", "images") and len(parts) in (4, 5):
                touched_slugs.add("/".join(parts[2:-1]))

    if not DRY_RUN and KIND_ROBOTS_ROOT.exists():
        index = write_collections_index()
        print("  collections.json index regenerated")
        folders = sorted(set(index.values()))
        for folder_rel in folders:
            write_gallery_manifest(folder_rel)
        print(f"  gallery.json refreshed for {len(folders)} folder(s)")

    if not DRY_RUN and moved:
        moved_names = {fname for fname, _ in moved}
        prune_art_generate(gen_data, moved_names)
        prune_art_prompts(prompts_data, moved_names)

    conductor_moved = [m for _, m in moved if m["target_repo"] == "silasfelinus/conductor"]
    kr_moved = [m for _, m in moved if m["target_repo"] == "silasfelinus/kind_robots"]

    print(
        f"\n{'[dry run] ' if DRY_RUN else ''}"
        f"{len(moved)} moved, {len(mirrored)} mirrored to project inspirations, "
        f"{len(unmatched)} unmatched, {len(skipped_missing_repo)} skipped"
    )

    if not DRY_RUN and moved:
        print("\nNext steps:")
        if conductor_moved or mirrored:
            print("  conductor:   git add projects/images/ projects/*/inspirations/ && git commit -m 'chore: add generated images'")
            print("  conductor:   python scripts/build_workspace.py  # prunes art-prompts.yaml")
        if kr_moved:
            print("  kind_robots: git add public/ && git commit -m 'chore: add generated images'")

    if unmatched:
        print("\nUnmatched files (no yaml entry or known naming convention):")
        for f in unmatched:
            print(f"  {f}")


if __name__ == "__main__":
    distribute()
