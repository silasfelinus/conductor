# Task-event queue

Task events are the connector-safe way to mutate authoritative roadmap task state without replacing a large `roadmap.yaml` file.

Create one uniquely named YAML file in this directory and commit it to `main`. The `Process task events` workflow validates and consumes the event, updates the complete roadmap in its checkout, runs dependency resolution, optionally appends a learning record, deletes the event, and commits the result back to `main`.

## Event shape

```yaml
version: 1
project: challenge-center
task: t-014
operation: claim
owner: worker
note: Optional evidence or state-change context.
```

Supported operations:

- `claim` — requires the task to be `ready`; sets `owner: worker` by default.
- `review` — records that verified implementation is awaiting merge or review.
- `done` — closes the task and clears ownership.
- `ready` — releases or retries the task and clears ownership.
- `needs-human` — parks the task; add `soft_gate: true` for a non-blocking infrastructure or direction issue.
- `blocked` — closes a task that cannot proceed.
- `rearm` — returns a `recurring: true` task to `ready` and clears ownership.

Optional fields:

```yaml
updated: 2026-07-13T19:30:00+00:00
soft_gate: true
force: false
learning:
  date: 2026-07-13
  kind: software
  stakes: reversible
  passes: 0
  outcome: done
  failure_category: null
  lesson: Small event files avoid unsafe whole-roadmap connector rewrites.
```

`learning` is accepted only for `done` and `blocked`. The processor derives `project`, `task`, and `outcome` from the event and appends no duplicate record for the same project/task/outcome.

## Atomic claim protocol

When direct full-file Git access is unavailable, the event-file commit is the Worker's one atomic claim commit. The Worker must not start implementation until current `main` shows that the event was consumed and the task is `claimed` by `worker`.

Use one event per state change. Do not create a replacement event after a workflow failure unless the original event is corrected or removed as part of a reviewed repair.

## Failure behavior

Invalid events are not deleted. The workflow fails visibly and leaves the event in place for diagnosis. A failed event is a soft blocker unless its underlying action is itself hard-gated or makes all remaining work unsafe.
