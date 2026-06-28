#!/usr/bin/env python3
"""
intake.py — Scaffold a new project, register it, and queue workspace art.

Usage:
  python scripts/intake.py <slug> --kind software|content|proposal [--repo owner/repo] [--desc "short description"]

Creates:
  projects/<slug>/roadmap.yaml
  projects/<slug>/CHANGELOG.md

Updates when present:
  repos.yaml
  projects/priority.yaml
  project-overrides.yaml
  projects/art-prompts.yaml
"""

import argparse
import re
import sys
import yaml
from datetime import date
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
TEMPLATE_DIR = REPO_ROOT / "projects" / "_template"
PROJECTS_DIR = REPO_ROOT / "projects"
REPOS_FILE = REPO_ROOT / "repos.yaml"
PRIORITY_FILE = PROJECTS_DIR / "priority.yaml"
OVERRIDES_FILE = REPO_ROOT / "project-overrides.yaml"
ART_PROMPTS_FILE = PROJECTS_DIR / "art-prompts.yaml"

ART_PROMPTS_HEADER = """# art-prompts.yaml — Image queue for Conductor project assets and Kind Robots missing-image requests
#
# Project assets use `images:` and are pruned automatically when matching files
# exist in this repo's projects/images/ folder.
#
# Site-wide missing-image reports use `requests:`. Kind Robots writes those
# requests here when an admin sees a missing image. Requests should be removed
# once the image has been generated and committed to the target repo.
#
# Project image variants:
#   icon  — square 1:1 (256×256 min). Used in nav, sidebar, card headers, favicons.
#   card  — portrait 2:3 (512×768 min). Shown on the workspace project card.
#   hero  — landscape 16:9 (1280×720 min). Shown as a banner when a project is selected.
#
# Workflow:
#   1. Copy the prompt into ChatGPT (image generation) or call the OpenAI Images API (model: gpt-image-1).
#   2. Set the correct aspect ratio in the generation UI (1:1 / 2:3 / 16:9).
#   3. Export as .webp at the minimum size listed.
#   4. Save to the image_path listed below.
#   5. Run `python scripts/build_workspace.py` to refresh the workspace.
#
# Status values: pending

"""


def slugify(s: str) -> str:
    return re.sub(r"[^a-z0-9-]", "-", s.lower()).strip("-")


def titleize(slug: str) -> str:
    return slug.replace("-", " ").title()


def load_yaml(path: Path) -> dict:
    if not path.exists():
        return {}
    with open(path) as f:
        return yaml.safe_load(f) or {}


def write_yaml(path: Path, data: dict) -> None:
    path.write_text(yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=88))


def write_art_prompts(data: dict) -> None:
    ART_PROMPTS_FILE.write_text(
        ART_PROMPTS_HEADER + yaml.safe_dump(data, sort_keys=False, allow_unicode=True, width=88)
    )


def default_art_entry(slug: str, desc: str) -> dict:
    essence = desc.strip() or f"{titleize(slug)} project"
    return {
        "project": slug,
        "icon": {
            "image_path": f"projects/images/{slug}-icon.webp",
            "size": "256x256",
            "status": "pending",
            "prompt": f"flat minimal app icon, {essence}, bold clean vector shapes, square composition, no text",
        },
        "card": {
            "image_path": f"projects/images/{slug}-card.webp",
            "size": "512x768",
            "status": "pending",
            "prompt": f"flat minimal portrait illustration, {essence}, centered subject on soft gradient backdrop, no text, 2:3 portrait composition",
        },
        "hero": {
            "image_path": f"projects/images/{slug}-hero.webp",
            "size": "1280x720",
            "status": "pending",
            "prompt": f"flat minimal wide panoramic, {essence}, cinematic scale, no text, 16:9 landscape",
        },
    }


def register_priority(slug: str) -> None:
    if not PRIORITY_FILE.exists():
        return

    data = load_yaml(PRIORITY_FILE)
    order = data.get("order") or []
    if slug not in order:
        if "brainstorm" in order:
            order.insert(order.index("brainstorm"), slug)
        else:
            order.append(slug)
        data["order"] = order
        write_yaml(PRIORITY_FILE, data)
        print(f"✓ Added {slug} to projects/priority.yaml")


def register_override(slug: str, kind: str) -> None:
    data = load_yaml(OVERRIDES_FILE)
    overrides = data.setdefault("overrides", [])

    for entry in overrides:
        if entry.get("slug") == slug:
            entry["status"] = "active"
            entry["priority"] = entry.get("priority") or "normal"
            entry["kind"] = kind
            break
    else:
        overrides.append({"slug": slug, "status": "active", "priority": "normal", "kind": kind})

    write_yaml(OVERRIDES_FILE, data)
    print(f"✓ Registered {slug} in project-overrides.yaml")


def register_art_prompts(slug: str, desc: str) -> None:
    data = load_yaml(ART_PROMPTS_FILE)
    images = data.setdefault("images", [])
    data.setdefault("requests", [])

    if not any(entry.get("project") == slug for entry in images if isinstance(entry, dict)):
        images.append(default_art_entry(slug, desc))
        write_art_prompts(data)
        print(f"✓ Queued {slug} icon/card/hero prompts in projects/art-prompts.yaml")


def main():
    parser = argparse.ArgumentParser(description="Scaffold a new Conductor project")
    parser.add_argument("slug", help="Project slug (kebab-case)")
    parser.add_argument("--kind", choices=["software", "content", "proposal"], default="software")
    parser.add_argument("--repo", default=None, help="GitHub repo (owner/name), or omit for no external repo")
    parser.add_argument("--desc", default="", help="Short description")
    args = parser.parse_args()

    slug = slugify(args.slug)
    project_dir = PROJECTS_DIR / slug

    if project_dir.exists():
        print(f"ERROR: projects/{slug}/ already exists")
        sys.exit(1)

    project_dir.mkdir(parents=True)

    template_roadmap = TEMPLATE_DIR / "roadmap.yaml"
    if template_roadmap.exists():
        content = template_roadmap.read_text()
        content = (
            content.replace("__SLUG__", slug)
            .replace("__KIND__", args.kind)
            .replace("REPLACE-ME", slug)
            .replace("kind: software        # software | content | proposal", f"kind: {args.kind}")
        )
    else:
        content = f"""project: {slug}
kind: {args.kind}

notes_from_silas: |
  {args.desc or "(Add project notes here.)"}

milestones:
  - id: m1
    title: "First milestone"
    weight: 10
    status: not-started

tasks:
  - id: t-001
    milestone: m1
    title: "First task"
    status: ready
    owner: null
    passes: 0
    stakes: reversible
"""

    (project_dir / "roadmap.yaml").write_text(content)

    today = date.today().isoformat()
    changelog = f"# {slug} CHANGELOG\n\n## {today}\n- Project scaffolded via intake.py\n"
    (project_dir / "CHANGELOG.md").write_text(changelog)

    print(f"✓ Created projects/{slug}/roadmap.yaml")
    print(f"✓ Created projects/{slug}/CHANGELOG.md")

    if REPOS_FILE.exists():
        repos_data = load_yaml(REPOS_FILE)
        repos = repos_data.get("repos", [])
        if any(r.get("slug") == slug for r in repos):
            print(f"  (repos.yaml already has an entry for {slug})")
        else:
            repos.append({
                "slug": slug,
                "repo": args.repo,
                "kind": args.kind,
                "description": args.desc or f"{slug} project",
            })
            repos_data["repos"] = repos
            write_yaml(REPOS_FILE, repos_data)
            print(f"✓ Added {slug} to repos.yaml")

    register_priority(slug)
    register_override(slug, args.kind)
    register_art_prompts(slug, args.desc or f"{titleize(slug)} project")

    print(f"\nNext: edit projects/{slug}/roadmap.yaml to fill in milestones and tasks.")


if __name__ == "__main__":
    main()
