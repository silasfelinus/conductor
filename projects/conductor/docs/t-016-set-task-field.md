# conductor/t-016 — set_task_field.py fallback handoff

Target task: `conductor/t-016`

Intended file: `scripts/set_task_field.py`

Tooling status: direct creation of `scripts/set_task_field.py` through the GitHub connector was blocked by the connector safety filter during this cycle. The exact source that should be applied is preserved below so the next local/Claude pass can copy it directly instead of reconstructing it from prose.

## Intended behavior

Add a small Python utility that updates one field on one task in one project roadmap.

Example commands:

```bash
python scripts/set_task_field.py conductor t-016 status done
python scripts/set_task_field.py alexa-integration t-008 owner null
python scripts/set_task_field.py global-ui t-008 approved_by_human false
python scripts/set_task_field.py conductor t-016 updated 2026-07-03T22:12:16-07:00
```

The utility should:

- Load `projects/<project>/roadmap.yaml`.
- Find the task with the matching `id`.
- Coerce `null` / `none` / `~` to `None`.
- Coerce `true` / `false` to booleans.
- Coerce integer strings to integers.
- Keep all other values as strings.
- Print the old and new value.
- Write the YAML back with `safe_dump(sort_keys=False, default_flow_style=False, width=100)` unless `--dry-run` is passed.

## Exact script source

```python
#!/usr/bin/env python3
"""
set_task_field.py — update one field on one roadmap task without hand-editing YAML.

Use this for small, targeted status/owner/updated/note changes when a full manual
roadmap edit is risky or noisy.

Usage:
  python scripts/set_task_field.py <project> <task-id> <field> <value> [--dry-run]
  python scripts/set_task_field.py conductor t-016 status done
  python scripts/set_task_field.py alexa-integration t-008 owner null
  python scripts/set_task_field.py global-ui t-008 approved_by_human false

Supported value coercions:
  - null / none / ~ -> None
  - true / false -> booleans
  - integers -> int
  - everything else stays a string
"""
import argparse
import sys
from pathlib import Path

try:
    import yaml
except ImportError:
    print("PyYAML not installed; run: pip install pyyaml", file=sys.stderr)
    sys.exit(1)


def parse_value(raw):
    lowered = raw.strip().lower()
    if lowered in {"null", "none", "~"}:
        return None
    if lowered == "true":
        return True
    if lowered == "false":
        return False
    try:
        return int(raw)
    except ValueError:
        return raw


def load_roadmap(path):
    if not path.exists():
        raise FileNotFoundError(f"Roadmap not found: {path}")
    with path.open() as handle:
        return yaml.safe_load(handle) or {}


def find_task(roadmap, task_id):
    for task in roadmap.get("tasks", []):
        if task.get("id") == task_id:
            return task
    return None


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument("project")
    parser.add_argument("task_id")
    parser.add_argument("field")
    parser.add_argument("value")
    parser.add_argument("--dry-run", action="store_true")
    args = parser.parse_args()

    path = Path("projects") / args.project / "roadmap.yaml"
    roadmap = load_roadmap(path)
    task = find_task(roadmap, args.task_id)
    if task is None:
        print(f"Task not found: {args.project}/{args.task_id}", file=sys.stderr)
        sys.exit(1)

    old_value = task.get(args.field)
    new_value = parse_value(args.value)
    task[args.field] = new_value

    print(f"{args.project}/{args.task_id}: {args.field} {old_value!r} -> {new_value!r}")
    if args.dry_run:
        return

    with path.open("w") as handle:
        yaml.safe_dump(roadmap, handle, sort_keys=False, default_flow_style=False, width=100)


if __name__ == "__main__":
    main()
```

## Verification still needed

Once the file is applied locally or by a tool path that can write `scripts/`, run:

```bash
python scripts/set_task_field.py conductor t-016 status done --dry-run
python -m py_compile scripts/set_task_field.py
```

## Safety boundaries

No DNS, secrets, billing, deploys, production data, live endpoints, or external writes are involved. This is a local roadmap-file helper only.
