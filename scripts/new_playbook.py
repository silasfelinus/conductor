#!/usr/bin/env python3
"""
new_playbook.py — Start a new Kind Robots playbook (story game) on the Playbook Kit.

Runs intake.py for every registration surface (roadmap, overrides, priority,
repos.yaml, art prompts, CONTROL.md), then replaces the generic roadmap and
design brief with the playbook ladder from projects/playbook-kit/templates/.

Usage:
  python scripts/new_playbook.py <slug> "<Title>" [--goal "one-line goal"] [--notes "Silas's words"]
  python scripts/new_playbook.py <slug> "<Title>" --blueprint <file>

--blueprint reads a Playbook Forge blueprint (kind_robots /admin/playbook-forge):
the Project pitch or agent Todo text that carries it between
<!-- playbook-blueprint --> markers, or the bare JSON. The blueprint is saved as
projects/<slug>/BLUEPRINT.json, seeds the goal and notes, and is summarized in
the design brief.

The Kind Robots half is `npm run playbook:new -- <slug> "<Title>"` in kind_robots.
Recipe: kind_robots docs/playbook-kit/README.md.
"""
from __future__ import annotations

import argparse
import json
import re
import sys
from datetime import date
from pathlib import Path

try:
    from scripts import intake
except ImportError:  # run as `python scripts/new_playbook.py`
    sys.path.insert(0, str(Path(__file__).resolve().parent))
    import intake  # type: ignore[no-redef]

TEMPLATES = Path(__file__).resolve().parent.parent / "projects" / "playbook-kit" / "templates"


def camel_case(slug: str) -> str:
    head, *rest = slug.split("-")
    return head + "".join(part.capitalize() for part in rest)


def fill(template: str, values: dict[str, str]) -> str:
    for key, value in values.items():
        template = template.replace(f"__{key}__", value)
    return template


def indent_block(text: str, spaces: int) -> str:
    pad = " " * spaces
    return ("\n" + pad).join(line.rstrip() for line in text.strip().splitlines())


BLUEPRINT_PATTERN = re.compile(
    r"<!-- playbook-blueprint -->\s*(?:```json)?(.*?)(?:```)?\s*<!-- /playbook-blueprint -->",
    re.S,
)


def read_blueprint(text: str) -> dict:
    """The blueprint JSON from forge handoff text, or from bare JSON."""
    match = BLUEPRINT_PATTERN.search(text)
    data = json.loads(match.group(1) if match else text)
    if not isinstance(data, dict) or "endings" not in data:
        raise ValueError("not a Playbook Forge blueprint")
    return data


def blueprint_goal(title: str, b: dict) -> str:
    tier = b.get("tier") or "smallest fitting"
    return (
        f"{title}: a {tier}-tier playbook on the Playbook Kit, forged in /admin/playbook-forge: "
        f"{b.get('acts')} acts, {b.get('encounters')} encounters, {b.get('followers')} followers, "
        f"{b.get('villains')} villain(s), {b.get('endings')} unique endings, "
        f"{'fail-forward' if b.get('failForward') else 'pass/fail'} {b.get('checks')} checks, "
        f"rendered art on {b.get('checkpoint')}, every ending reachable from a fresh seed."
    )


BLUEPRINT_ROWS = [
    ("Lives in", "placement"), ("Scope", "tier"), ("Checkpoint", "checkpoint"), ("Art styles", "artStyles"),
    ("Opening", "creator"), ("Portraits", "portraits"), ("Followers", "followers"), ("Party size", "partySize"),
    ("Villains", "villains"), ("New villain each run", "villainPerRun"), ("Factions", "factions"),
    ("Romances", "romances"), ("Acts", "acts"), ("Encounters", "encounters"), ("Quests", "quests"),
    ("Reveals", "reveals"), ("Scrapbook moments", "moments"), ("Stats", "stats"), ("Checks", "checks"),
    ("Outcome tiers", "outcomes"), ("Always interesting", "failForward"), ("Endings", "endings"),
    ("Finale beats", "finaleBeats"), ("Save style", "saveStyle"), ("Unreadable save", "unreadable"),
    ("Save slots", "saveSlots"), ("Undo", "undo"),
]


def blueprint_section(b: dict) -> str:
    rows = "\n".join(f"| {label} | {b.get(key)} |" for label, key in BLUEPRINT_ROWS)
    return (
        "\n## Blueprint from the Playbook Forge\n\n"
        "Silas configured these factors in /admin/playbook-forge; the full blueprint is "
        "BLUEPRINT.json beside this brief. Build to it; re-forecast in the Forge before changing it.\n\n"
        "| Factor | Value |\n| --- | --- |\n" + rows + "\n"
    )


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Start a new playbook on the Playbook Kit")
    parser.add_argument("slug", help="Project slug (kebab-case)")
    parser.add_argument("title", help="Display title")
    parser.add_argument("--goal", default="", help="One-line definition of done")
    parser.add_argument("--notes", default="", help="Silas's direction, verbatim, for notes_from_silas")
    parser.add_argument("--blueprint", default="", help="File holding a Playbook Forge blueprint (pitch text or JSON)")
    parser.add_argument("--art-subject", default="", help="What the project art shows, as a picture (see intake.py)")
    args = parser.parse_args(argv)

    blueprint = read_blueprint(Path(args.blueprint).read_text()) if args.blueprint else None

    slug = intake.slugify(args.slug)
    title = args.title.strip()
    goal = args.goal.strip() or (blueprint_goal(title, blueprint) if blueprint else None) or (
        f"{title}: a playbook on the Playbook Kit that is fun as a one-sitting Vignette, "
        "with every ending reachable, rendered art and a one-screen console at every width."
    )
    intake.main([
        slug,
        "--kind", "software",
        "--title", title,
        "--goal", goal,
        "--repo", "silasfelinus/kind_robots",
        "--desc", f"{title}: a playbook game on the Playbook Kit.",
        "--art-subject", args.art_subject,
    ])

    project_dir = intake.PROJECTS_DIR / slug
    notes = args.notes or (
        f"Forged in /admin/playbook-forge. Idea: {blueprint.get('idea')}" if blueprint and blueprint.get("idea") else ""
    )
    values = {
        "SLUG": slug,
        "TITLE": title,
        "CAMEL": camel_case(slug),
        "DATE": date.today().isoformat(),
        "GOAL": indent_block(goal, 2),
        "NOTES": indent_block(notes or "(Silas's direction, verbatim.)", 2),
    }
    (project_dir / "roadmap.yaml").write_text(
        fill((TEMPLATES / "roadmap.template.yaml").read_text(), values)
    )
    brief = fill((TEMPLATES / "DESIGN-BRIEF.template.md").read_text(), values)
    if blueprint:
        brief += blueprint_section(blueprint)
        (project_dir / "BLUEPRINT.json").write_text(json.dumps(blueprint, indent=2) + "\n")
    (project_dir / "DESIGN-BRIEF.md").write_text(brief)
    print(f"✓ Wrote the playbook ladder roadmap and design brief for projects/{slug}/")
    print(
        f'\nNext, in kind_robots: npm run playbook:new -- {slug} "{title}"'
        f"\nThen claim {slug}/t-001."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
