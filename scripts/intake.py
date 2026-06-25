#!/usr/bin/env python3
"""
intake.py — Scaffold a new project from the _template and register it in repos.yaml.

Usage:
  python scripts/intake.py <slug> --kind software|content|proposal [--repo owner/repo] [--desc "short description"]

Creates:
  projects/<slug>/roadmap.yaml  (from _template)
  projects/<slug>/CHANGELOG.md

Optionally adds an entry to repos.yaml.
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


def slugify(s: str) -> str:
    return re.sub(r"[^a-z0-9-]", "-", s.lower()).strip("-")


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

    # Roadmap from template
    template_roadmap = TEMPLATE_DIR / "roadmap.yaml"
    if template_roadmap.exists():
        content = template_roadmap.read_text()
        content = content.replace("__SLUG__", slug).replace("__KIND__", args.kind)
    else:
        content = f"""project: {slug}
kind: {args.kind}

notes_from_silas: |
  (Add project notes here.)

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

    # CHANGELOG
    today = date.today().isoformat()
    changelog = f"# {slug} CHANGELOG\n\n## {today}\n- Project scaffolded via intake.py\n"
    (project_dir / "CHANGELOG.md").write_text(changelog)

    print(f"✓ Created projects/{slug}/roadmap.yaml")
    print(f"✓ Created projects/{slug}/CHANGELOG.md")

    # Register in repos.yaml
    if REPOS_FILE.exists():
        with open(REPOS_FILE) as f:
            repos_data = yaml.safe_load(f) or {}
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
            with open(REPOS_FILE, "w") as f:
                yaml.dump(repos_data, f, default_flow_style=False, sort_keys=False)
            print(f"✓ Added {slug} to repos.yaml")

    print(f"\nNext: edit projects/{slug}/roadmap.yaml to fill in milestones and tasks.")


if __name__ == "__main__":
    main()
