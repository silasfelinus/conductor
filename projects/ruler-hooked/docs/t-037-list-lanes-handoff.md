# t-037 connector handoff: `--list-lanes`

Target repository: `silasfelinus/conductor`

Intended implementation branch: `worker/ruler-hooked-t-037-openai-scheduled-2026-09-21T122311Z-ruler-hooked-t037-a11`

## Why this is a handoff

The required change is inside the existing large `scripts/build_ruler_hooked_art_queue.py`. This connector can page-read the file safely, but its file mutation action replaces the complete file and has no line-range patch operation. Reconstructing a large existing file from abbreviated/paged reads is forbidden by `AGENTS.md` and `docs/github-connector-worker.md`, so this session does not risk overwriting unseen content.

## Exact implementation

In `main()` add a boolean argument:

```python
parser.add_argument(
    "--list-lanes",
    action="store_true",
    help="print staged vs not-yet-staged counts for every produced lane and exit",
)
```

Build `entries` exactly as today, including the existing `--include-layers` behavior, and run `assert_contract(entries)` before summarizing so this mode cannot hide prompt-contract regressions.

After reading `projects/art-prompts.yaml` and computing `existing = staged_ids(text)`, but before applying `--lane`, handle `args.list_lanes`. For every lane in `sorted(LANES)`, count produced entries, staged entries whose id is in `existing`, and unstaged entries. Print one stable row per lane, for example:

```text
lane       total  staged  unstaged
card          12       3         9
concept       14      14         0
...
```

The `layer` row should be present with zeros unless `--include-layers` was supplied, because layer entries are intentionally not produced otherwise. Exit 0 after the table. `--list-lanes` must be read-only even if `--write` is also supplied. Reject combining `--list-lanes` with `--lane` via `parser.error(...)`; a summary filtered to one lane defeats the purpose.

Update the module usage block with:

```text
python scripts/build_ruler_hooked_art_queue.py --list-lanes
python scripts/build_ruler_hooked_art_queue.py --include-layers --list-lanes
```

## Regression coverage

Add focused tests alongside the existing ruler-hooked queue-builder tests. Pin these behaviors:

1. `--list-lanes` exits 0 and prints every name in `LANES` exactly once.
2. `staged + unstaged == total` for every row.
3. A known staged id increments the correct lane's staged count; an unstaged id increments unstaged.
4. `layer` is zero without `--include-layers` and reflects generated layer entries with it.
5. `--list-lanes --write` performs no write.
6. `--list-lanes --lane fish` is rejected.

Run the focused tests, then the full Python suite. No Kind Robots or production API access is required.

## Safety

This is read-only reporting over the same generated entry set and `projects/art-prompts.yaml` staged-id set the script already computes. It must not enqueue ArtJobs, modify `art-prompts.yaml`, or alter prompt generation.
