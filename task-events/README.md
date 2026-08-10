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
continuous_improvement_lane: 4
continuous_improvement_pr: silasfelinus/conductor#1834
verify_pr: silasfelinus/kind_robots#1718
```

`learning` is accepted only for `done` and `blocked`. The processor derives `project`, `task`, and `outcome` from the event and appends no duplicate record for the same project/task/outcome.

`continuous_improvement_lane`/`continuous_improvement_pr` are optional and only meaningful on a task that already carries a `t-010`-style nested `continuous_improvement` mapping (`last_lane`/`next_lane`/`last_run`/`last_pr`). Set both together when a task-event closes out a lane cycle (typically alongside a `rearm` event) and the processor advances the counter (`last_lane`, `next_lane = lane % 4 + 1`, `last_run`, `last_pr`) the same way `scripts/bump_continuous_improvement.py`'s manual CLI does — fixes conductor/t-103, where the counter previously froze on every close-out that went through this lighter path instead of a session hand-editing the roadmap. `continuous_improvement_lane` must be an integer 1-4; `continuous_improvement_pr` must look like `owner/repo#number`. Supplying only one of the pair is rejected as malformed.

Prefer the full mapping above. If `learning` is supplied as a bare string instead (a recurring
mistake — see conductor/t-097), the processor coerces it into `{kind, stakes, lesson}`, inferring
`kind` from the project's roadmap `kind` and `stakes` from the task's own `stakes` field when
either is a recognized value, and using the string itself as `lesson`. This keeps the processor
from hard-failing on the shape, at the cost of `kind`/`stakes` landing `null` in `LEARNING.yaml`
when they can't be inferred — write the full mapping when you know the answer.

### `verify_pr` — don't close a task on an unconfirmed merge

A `done` event's `note` claiming "merged PR #N" is not itself proof — conductor/t-112
(2026-08-10) found a scheduled run apply `done` to brainstorm/t-010 six minutes before
kind_robots#1718 actually merged, because nothing checked GitHub. Set `verify_pr:
owner/repo#number` (shape identical to `continuous_improvement_pr`) on a `done` event
whose task closure depends on a PR having merged, and the processor confirms `merged:
true` via the GitHub API *before* writing `status: done`. As a best-effort net for
events that predate this field, the processor also scans `note` for the shorthand
`kind_robots#1718` / `conductor#42` cross-reference form (not "PR #1718" prose with no
repo prefix — that's too ambiguous to guess a repo from safely). If any referenced PR
isn't merged yet, the event is redirected to `needs-human` / `soft_gate: true` with an
`AUTO-PARKED` note explaining the mismatch, instead of closing the task — re-queue a
fresh `done` event once the PR actually merges. If GitHub can't be reached at all, the
processor raises and leaves the event queued for the next run rather than guessing
either way.

## Atomic claim protocol

When direct full-file Git access is unavailable, the event-file commit is the Worker's one atomic claim commit. The Worker must not start implementation until current `main` shows that the event was consumed and the task is `claimed` by `worker`.

Use one event per state change. Do not create a replacement event after a workflow failure unless the original event is corrected or removed as part of a reviewed repair.

## Failure behavior

Invalid events are not deleted. The workflow fails visibly and leaves the event in place for diagnosis. A failed event is a soft blocker unless its underlying action is itself hard-gated or makes all remaining work unsafe.

## Surgical, byte-preserving writes

The processor (`scripts/process_task_events.py`) never reserializes a whole `roadmap.yaml` with `yaml.safe_dump`. It edits only the specific field lines an event actually changes (via `scripts/roadmap_text_patch.py`, built on `scripts/set_task_field.py`), so a status-only event produces a status-sized diff — every other task's formatting, quote style, block scalars, and literal Unicode stay byte-for-byte untouched. `scripts/resolve_deps.py`'s dependency-unblock writes (`waiting` → `ready`) use the same patcher for the same reason. `LEARNING.yaml` is append-only text: a new record is written as trailing bytes, never a full-ledger rewrite, so existing records keep whatever style they were originally saved with.

## Atomic retry behavior

`process()` validates the full event — including any `learning` payload — and computes every roadmap edit *before* writing anything, so an invalid `learning` block can never leave an already-applied status transition stranded with its event file undeleted; on any validation error, the roadmap file and the event file are both left exactly as they were.

At the Git level, the `Process task events` workflow commits and pushes straight to `main`. If `origin/main` moved between checkout and push (a concurrent claim or another commit landed first), the workflow fetches the new `main`, discards its own commit with `git reset --hard` (never a force-push), and replays the *entire* processing step — including re-running `process_task_events.py` — against the fresh base. It allows exactly one such retry; if the second push also loses the race, the job fails and every event stays queued, untouched, on `origin/main` for the next run to pick up.
