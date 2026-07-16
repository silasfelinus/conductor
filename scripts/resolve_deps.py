#!/usr/bin/env python3
"""
resolve_deps.py — unblock pipeline tasks whose dependencies are satisfied.

Run at the START of every Worker cycle. For each project roadmap, any task with
status: waiting becomes ready once ALL its depends_on tasks are status: done and
(if gate_human) approved_by_human: true. Writes changes back in place.

A task is "satisfied" as a dependency when:
  status == done  AND  (gate_human is falsy  OR  approved_by_human is true)

Usage: python scripts/resolve_deps.py [--dry-run]
"""
import sys, glob, os, argparse
from pathlib import Path
try:
    import yaml
except ImportError:
    print("PyYAML not installed; run: pip install pyyaml", file=sys.stderr); sys.exit(1)

sys.path.insert(0, str(Path(__file__).resolve().parent))
from roadmap_text_patch import apply_task_field_ops  # noqa: E402
from roadmap_deps import dependency_satisfied as satisfied  # noqa: E402

def as_list(v):
    if v is None: return []
    return v if isinstance(v, list) else [v]

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    changed_total = 0
    for path in sorted(glob.glob("projects/*/roadmap.yaml")):
        if os.sep + "_template" + os.sep in path:
            continue
        text = Path(path).read_text(encoding="utf-8")
        rm = yaml.safe_load(text) or {}
        tasks = rm.get("tasks", [])
        by_id = {t["id"]: t for t in tasks}
        changed = []
        for t in tasks:
            if t.get("status") != "waiting":
                continue
            deps = as_list(t.get("depends_on"))
            if deps and all(d in by_id and satisfied(by_id[d]) for d in deps):
                changed.append(t["id"])
        if changed:
            changed_total += len(changed)
            print(f"{rm.get('project', path)}: unblocked {', '.join(changed)}")
            if not args.dry_run:
                # Surgical per-task status write -- a two-task unblock must not
                # reformat the other hundreds of unrelated lines in the roadmap
                # (escaped Unicode, changed quote/block style, whole-file diff).
                for task_id in changed:
                    text = apply_task_field_ops(text, task_id, [("set", "status", "ready")])
                yaml.safe_load(text)  # confirm the edits produced valid YAML
                Path(path).write_text(text, encoding="utf-8")
    if changed_total == 0:
        print("No tasks to unblock.")

if __name__ == "__main__":
    main()
