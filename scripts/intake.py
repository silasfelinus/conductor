#!/usr/bin/env python3
"""
intake.py — Scaffold a new project, register it, and queue workspace art.

One pass touches every surface a new project needs so no surface gets dropped
(conductor/t-025 — filed after a Dream scaffold PR skipped the CONTROL.md block
and the art-prompt entries).

Usage:
  python scripts/intake.py <slug> --kind software|content|proposal \
      [--title "Nice Name"] [--goal "one-line goal"] [--repo owner/repo] [--desc "short description"]

Creates:
  projects/<slug>/roadmap.yaml
  projects/<slug>/DESIGN-BRIEF.md
  projects/<slug>/CHANGELOG.md

Updates when present:
  repos.yaml
  projects/priority.yaml
  project-overrides.yaml
  projects/art-prompts.yaml
  CONTROL.md            (appends a Per-project direction block)
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
CONTROL_FILE = REPO_ROOT / "CONTROL.md"
CONTROL_SECTION = "## Per-project direction"

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


def design_brief_text(title: str, goal: str, today: str) -> str:
    what = goal.strip() or "(Describe what this project is and the core payoff loop.)"
    return f"""# {title} — Design Brief

date: {today}
status: draft (scaffolded via intake.py — fill in before building)
author: (assign)

## What it is

{what}

## Who it serves

(Describe the target user and the primary use case.)

## MVP scope

(The smallest useful version — the first shippable slice.)

## Out of scope / guardrails

(Explicit non-goals and any gates: publishing, money, secrets, production, etc.)

## Open questions

(Decisions that need Silas before or during the build.)
"""


def register_design_brief(project_dir: Path, title: str, goal: str, today: str) -> None:
    brief = project_dir / "DESIGN-BRIEF.md"
    if brief.exists():
        print(f"  (DESIGN-BRIEF.md already exists for {project_dir.name})")
        return
    brief.write_text(design_brief_text(title, goal, today))
    print(f"✓ Created projects/{project_dir.name}/DESIGN-BRIEF.md")


def control_block_text(slug: str, kind: str, goal: str) -> str:
    direction = goal.strip() or "(Add steering direction for this project.)"
    return f"### {slug}  ({kind})\n**Direction:** {direction}\n**Notes:**\n- (your notes)\n"


def register_control_block(slug: str, kind: str, goal: str) -> None:
    """Append a Per-project direction block to CONTROL.md (idempotent).

    Inserts at the end of the CONTROL_SECTION block — before the next top-level
    ``## `` heading if one exists, otherwise at end of file — so it stays inside
    the per-project section even if later sections are added below it.
    """
    if not CONTROL_FILE.exists():
        return
    text = CONTROL_FILE.read_text()
    if f"### {slug}  (" in text:
        print(f"  (CONTROL.md already has a block for {slug})")
        return

    block = control_block_text(slug, kind, goal)
    marker = text.find(CONTROL_SECTION)
    if marker == -1:
        # No per-project section — append the section itself.
        new_text = text.rstrip("\n") + f"\n\n{CONTROL_SECTION}\n\n{block}"
    else:
        nxt = text.find("\n## ", marker + len(CONTROL_SECTION))
        if nxt == -1:
            new_text = text.rstrip("\n") + f"\n\n{block}"
        else:
            head, tail = text[:nxt], text[nxt:]
            new_text = head.rstrip("\n") + f"\n\n{block}\n{tail.lstrip(chr(10))}"
    CONTROL_FILE.write_text(new_text)
    print(f"✓ Added {slug} block to CONTROL.md")


def main(argv=None):
    parser = argparse.ArgumentParser(description="Scaffold a new Conductor project")
    parser.add_argument("slug", help="Project slug (kebab-case)")
    parser.add_argument("--kind", choices=["software", "content", "proposal"], default="software")
    parser.add_argument("--title", default="", help="Display title (default: titleized slug)")
    parser.add_argument("--goal", default="", help="One-line goal — seeds DESIGN-BRIEF.md and the CONTROL.md block")
    parser.add_argument("--repo", default=None, help="GitHub repo (owner/name), or omit for no external repo")
    parser.add_argument("--desc", default="", help="Short description (falls back to --goal)")
    args = parser.parse_args(argv)

    slug = slugify(args.slug)
    title = args.title.strip() or titleize(slug)
    goal = args.goal.strip() or args.desc.strip()
    desc = args.desc.strip() or goal
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
  {desc or "(Add project notes here.)"}

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
    register_design_brief(project_dir, title, goal, today)

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
                "description": desc or f"{slug} project",
            })
            repos_data["repos"] = repos
            write_yaml(REPOS_FILE, repos_data)
            print(f"✓ Added {slug} to repos.yaml")

    register_priority(slug)
    register_override(slug, args.kind)
    register_art_prompts(slug, desc or f"{titleize(slug)} project")
    register_control_block(slug, args.kind, goal)

    print(f"\nNext: edit projects/{slug}/roadmap.yaml + DESIGN-BRIEF.md to fill in milestones, tasks, and the brief.")


if __name__ == "__main__":
    main()
