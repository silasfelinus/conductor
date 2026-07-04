# conductor/t-016 — targeted roadmap task field updater

The intended implementation is a small Python utility at `scripts/set_task_field.py`.

The direct script write was blocked by the connector safety filter during this run, even for a placeholder script. The likely issue is that the task explicitly creates a tool that edits roadmap task state, which the connector treats cautiously.

## Intended command

```bash
python scripts/set_task_field.py <project> <task-id> status=needs-human owner=worker updated=2026-07-04T03:11:06Z
```

## Intended behavior

- Read exactly one file: `projects/<project>/roadmap.yaml`.
- Find exactly one task by `id`.
- Allow only a narrow field set: `status`, `owner`, `updated`, `passes`, and `note`.
- Replace only the matching top-level field line inside that task block.
- Leave the rest of the roadmap text unchanged.
- Support `--dry-run` to print the patched result without writing.
- Exit nonzero if the project slug, task id, field name, or file path is invalid.

## Safety boundaries

- Do not allow `approved_by_human` updates.
- Do not allow arbitrary file paths.
- Do not parse and dump the full YAML document, because that defeats the purpose of minimizing unrelated text changes.
- Do not touch deploy, DNS, billing, secrets, production data, or external systems.

## Verification still needed

Once local or less-restricted repo access is available, add the script and a small unit test that proves neighboring task blocks remain byte-for-byte identical.
