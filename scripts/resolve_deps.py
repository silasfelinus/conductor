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
try:
    import yaml
except ImportError:
    print("PyYAML not installed; run: pip install pyyaml", file=sys.stderr); sys.exit(1)

def as_list(v):
    if v is None: return []
    return v if isinstance(v, list) else [v]

def satisfied(task):
    if task.get("status") != "done":
        return False
    if task.get("gate_human"):
        return bool(task.get("approved_by_human"))
    return True

def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--dry-run", action="store_true")
    args = ap.parse_args()

    changed_total = 0
    for path in sorted(glob.glob("projects/*/roadmap.yaml")):
        if os.sep + "_template" + os.sep in path:
            continue
        rm = yaml.safe_load(open(path)) or {}
        tasks = rm.get("tasks", [])
        by_id = {t["id"]: t for t in tasks}
        changed = []
        for t in tasks:
            if t.get("status") != "waiting":
                continue
            deps = as_list(t.get("depends_on"))
            if deps and all(d in by_id and satisfied(by_id[d]) for d in deps):
                t["status"] = "ready"
                changed.append(t["id"])
        if changed:
            changed_total += len(changed)
            print(f"{rm.get('project', path)}: unblocked {', '.join(changed)}")
            if not args.dry_run:
                with open(path, "w") as f:
                    yaml.safe_dump(rm, f, sort_keys=False, default_flow_style=False, width=100)
    if changed_total == 0:
        print("No tasks to unblock.")

if __name__ == "__main__":
    main()
