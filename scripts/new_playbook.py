#!/usr/bin/env python3
"""
new_playbook.py — Start a new Kind Robots playbook (story game) on the Playbook Kit.

Runs intake.py for every registration surface (roadmap, overrides, priority,
repos.yaml, art prompts, CONTROL.md), then replaces the generic roadmap and
design brief with the playbook ladder from projects/playbook-kit/templates/.

Usage:
  python scripts/new_playbook.py <slug> "<Title>" [--goal "one-line goal"] [--notes "Silas's words"]

The Kind Robots half is `npm run playbook:new -- <slug> "<Title>"` in kind_robots.
Recipe: kind_robots docs/playbook-kit/README.md.
"""
from __future__ import annotations

import argparse
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


def main(argv=None) -> int:
    parser = argparse.ArgumentParser(description="Start a new playbook on the Playbook Kit")
    parser.add_argument("slug", help="Project slug (kebab-case)")
    parser.add_argument("title", help="Display title")
    parser.add_argument("--goal", default="", help="One-line definition of done")
    parser.add_argument("--notes", default="", help="Silas's direction, verbatim, for notes_from_silas")
    args = parser.parse_args(argv)

    slug = intake.slugify(args.slug)
    title = args.title.strip()
    goal = args.goal.strip() or (
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
    ])

    project_dir = intake.PROJECTS_DIR / slug
    values = {
        "SLUG": slug,
        "TITLE": title,
        "CAMEL": camel_case(slug),
        "DATE": date.today().isoformat(),
        "GOAL": indent_block(goal, 2),
        "NOTES": indent_block(args.notes or "(Silas's direction, verbatim.)", 2),
    }
    (project_dir / "roadmap.yaml").write_text(
        fill((TEMPLATES / "roadmap.template.yaml").read_text(), values)
    )
    (project_dir / "DESIGN-BRIEF.md").write_text(
        fill((TEMPLATES / "DESIGN-BRIEF.template.md").read_text(), values)
    )
    print(f"✓ Wrote the playbook ladder roadmap and design brief for projects/{slug}/")
    print(
        f'\nNext, in kind_robots: npm run playbook:new -- {slug} "{title}"'
        f"\nThen claim {slug}/t-001."
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
