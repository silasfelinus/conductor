#!/usr/bin/env python3
"""
topology.py — Print the dependency graph for all tasks across all projects.

Run from repo root: python scripts/topology.py [--project <slug>] [--dot]

Options:
  --project   Only show one project's graph
  --dot       Output Graphviz DOT format instead of plain text
"""

import argparse
import yaml
from pathlib import Path

REPO_ROOT = Path(__file__).parent.parent
PROJECTS_DIR = REPO_ROOT / "projects"


def load_all_roadmaps(project_filter=None):
    roadmaps = {}
    for project_dir in sorted(PROJECTS_DIR.iterdir()):
        if not project_dir.is_dir() or project_dir.name.startswith("_"):
            continue
        if project_filter and project_dir.name != project_filter:
            continue
        roadmap_path = project_dir / "roadmap.yaml"
        if not roadmap_path.exists():
            continue
        with open(roadmap_path) as f:
            data = yaml.safe_load(f)
        if data:
            roadmaps[project_dir.name] = data
    return roadmaps


STATUS_SYMBOLS = {
    "done": "✓",
    "ready": "→",
    "waiting": "⏳",
    "claimed": "⚙",
    "review": "👁",
    "blocked": "✗",
    "needs-human": "👤",
}


def print_text(roadmaps):
    for slug, roadmap in roadmaps.items():
        tasks = {t["id"]: t for t in (roadmap.get("tasks") or [])}
        print(f"\n{'═' * 50}")
        print(f"  {slug}  ({roadmap.get('kind', '?')})")
        print(f"{'═' * 50}")

        for task_id, task in tasks.items():
            status = task.get("status", "ready")
            symbol = STATUS_SYMBOLS.get(status, "?")
            title = task.get("title", task_id)[:50]
            deps = task.get("depends_on")
            if isinstance(deps, str):
                deps = [deps]
            dep_str = f"  deps: {', '.join(deps)}" if deps else ""
            gate = " [gate_human]" if task.get("gate_human") else ""
            print(f"  {symbol} {task_id:<12} {status:<14} {title}{gate}")
            if dep_str:
                print(f"              {dep_str}")


def print_dot(roadmaps):
    print("digraph conductor {")
    print('  rankdir=LR;')
    print('  node [shape=box, style=rounded, fontname="sans-serif"];')

    for slug, roadmap in roadmaps.items():
        tasks = roadmap.get("tasks") or []
        print(f'\n  subgraph "cluster_{slug}" {{')
        print(f'    label="{slug}";')

        for task in tasks:
            task_id = task.get("id", "?")
            status = task.get("status", "ready")
            node_id = f"{slug}__{task_id}".replace("-", "_")
            color = {
                "done": "green", "blocked": "red", "needs-human": "purple",
                "claimed": "orange", "review": "blue", "waiting": "gray",
            }.get(status, "black")
            print(f'    {node_id} [label="{task_id}\\n{status}", color="{color}"];')

        print("  }")

        for task in tasks:
            task_id = task.get("id", "?")
            node_id = f"{slug}__{task_id}".replace("-", "_")
            deps = task.get("depends_on")
            if isinstance(deps, str):
                deps = [deps]
            for dep in (deps or []):
                dep_node = f"{slug}__{dep}".replace("-", "_")
                print(f"  {dep_node} -> {node_id};")

    print("}")


def main():
    parser = argparse.ArgumentParser(description="Print Conductor task dependency topology")
    parser.add_argument("--project", default=None, help="Filter to a single project slug")
    parser.add_argument("--dot", action="store_true", help="Output Graphviz DOT format")
    args = parser.parse_args()

    roadmaps = load_all_roadmaps(args.project)

    if not roadmaps:
        print("No projects found.")
        return

    if args.dot:
        print_dot(roadmaps)
    else:
        print_text(roadmaps)


if __name__ == "__main__":
    main()
