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


def _insert_list_item(text: str, item: str, before: str | None = None) -> str:
    """Insert ``- item`` into a top-level YAML block list in `text` via text surgery,
    preserving every comment and blank line untouched (mirrors register_control_block's
    approach — a full yaml.safe_dump round-trip would strip both).

    If `before` names an existing list item, the new one is inserted immediately above
    it at matching indentation. Otherwise it's inserted right after the last top-level
    list item found in the file.
    """
    lines = text.splitlines(keepends=True)
    if before is not None:
        pattern = re.compile(rf"^(\s*)- {re.escape(before)}\s*$")
        for i, line in enumerate(lines):
            m = pattern.match(line.rstrip("\n"))
            if m:
                lines.insert(i, f"{m.group(1)}- {item}\n")
                return "".join(lines)

    list_pattern = re.compile(r"^(\s*)- \S")
    last_idx, last_indent = None, "  "
    for i, line in enumerate(lines):
        m = list_pattern.match(line)
        if m:
            last_idx, last_indent = i, m.group(1)
    if last_idx is None:
        lines.append(f"  - {item}\n")
    else:
        lines.insert(last_idx + 1, f"{last_indent}- {item}\n")
    return "".join(lines)


def register_priority(slug: str) -> None:
    if not PRIORITY_FILE.exists():
        return

    text = PRIORITY_FILE.read_text()
    if re.search(rf"^\s*- {re.escape(slug)}\s*$", text, re.MULTILINE):
        return

    new_text = _insert_list_item(text, slug, before="brainstorm")
    PRIORITY_FILE.write_text(new_text)
    print(f"✓ Added {slug} to projects/priority.yaml")


def _override_block_span(text: str, slug: str) -> tuple[int, int] | None:
    """Return the (start, end) character span of the ``- slug: <slug>`` block."""
    m = re.search(rf"^  - slug: {re.escape(slug)}\s*$", text, re.MULTILINE)
    if not m:
        return None
    start = m.start()
    next_m = re.search(r"^  - slug: ", text[m.end():], re.MULTILINE)
    end = m.end() + next_m.start() if next_m else len(text)
    return start, end


def register_override(slug: str, kind: str) -> None:
    """Set `slug`'s status/kind in project-overrides.yaml via text surgery, so header
    comments, inline comments, and blank-line block separators survive untouched — a
    yaml.safe_dump round-trip strips all of those (conductor/t-055)."""
    if not OVERRIDES_FILE.exists():
        return
    text = OVERRIDES_FILE.read_text()
    span = _override_block_span(text, slug)

    if span is not None:
        start, end = span
        block = text[start:end]
        block = re.sub(r"^(\s*status:)\s*\S+", r"\1 active", block, count=1, flags=re.MULTILINE)
        if re.search(r"^\s*kind:\s*\S+", block, re.MULTILINE):
            block = re.sub(r"^(\s*kind:)\s*\S+", rf"\1 {kind}", block, count=1, flags=re.MULTILINE)
        else:
            block = re.sub(r"^(\s*priority:.*)$", rf"\1\n    kind: {kind}", block, count=1, flags=re.MULTILINE)
        text = text[:start] + block + text[end:]
        OVERRIDES_FILE.write_text(text)
        print(f"✓ Registered {slug} in project-overrides.yaml")
        return

    entry = f"  - slug: {slug}\n    status: active\n    priority: normal\n    kind: {kind}\n"
    empty_list = re.search(r"^overrides:[ \t]*\[[ \t]*\][ \t]*\n?", text, re.MULTILINE)
    if empty_list:
        new_text = text[:empty_list.start()] + "overrides:\n" + entry + text[empty_list.end():]
    elif re.search(r"^overrides:\s*$", text, re.MULTILINE):
        new_text = text.rstrip("\n") + "\n\n" + entry
    else:
        new_text = text.rstrip("\n") + "\n\noverrides:\n" + entry
    OVERRIDES_FILE.write_text(new_text)
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
