# GitHub Connector Worker Protocol

This runbook is for Worker sessions that have the connected GitHub tools but do not have a local checkout, shell, `gh`, or Python runtime.

The absence of local execution is not a reason to skip Conductor bookkeeping. The connector can safely read long files in pages, perform compare-and-swap file updates with blob SHAs, create branches and commits, inspect Actions, and merge pull requests.

## Read long files without truncation

A default `fetch_file` response may be abbreviated for display. That does not mean the file is unavailable.

1. Fetch the file repeatedly with explicit `start_line` and `end_line` ranges.
2. Continue until the final returned range is shorter than the requested page.
3. Concatenate the returned file content exactly in line order.
4. Keep the blob SHA returned by GitHub.
5. Never write a replacement assembled from an abbreviated response.

When updating an existing file, pass the exact current blob SHA to `update_file`. A SHA conflict means the file moved: re-fetch current state and reconsider the mutation. Never force or overwrite newer content.

## Claims are session-aware task events

A claim must reserve the task immediately and identify the exact session. `task-events` claim operations are session-aware: a `claim` event **requires** a non-empty, collision-resistant `session`, and the processor preserves the same atomic `ALREADY_CLAIMED` invariant as `scripts/claim_task.py`.

For a connector-native claim, create a small unique event file directly on Conductor `main`:

```yaml
version: 1
project: ai-art-academy
task: t-010
operation: claim
owner: worker
session: 2026-07-25T100000Z-ai-art-academy-t-010-a1b2
updated: '2026-07-25T10:00:00Z'
```

On a successful claim the processor sets `status: claimed`, `owner`, `claimed_by: <session>`, `claimed_at`, and `updated`. Two concurrent claims are resolved deterministically:

- A repeat claim from the **same** `owner` **and** `session` is a true no-op (idempotent replay), so retrying is safe.
- A claim from a **different** session against an already-claimed task loses the race: the processor consumes the losing event as `ALREADY_CLAIMED` with **zero** roadmap mutation, rather than leaving it as a poison event. Re-fetch the roadmap; if it does not name your session, rotate to the next `ready` task.

After creating a claim event, follow the "After creating an event" checklist below (inspect the Actions run, re-fetch, and verify the task names your session) before starting implementation.

### Direct compare-and-swap alternative

If you prefer not to wait for the task-event processor, you can still claim with a direct compare-and-swap roadmap update:

1. Page-fetch the complete current `projects/<project>/roadmap.yaml` from `main`.
2. Confirm the task is still eligible under `AGENTS.md`, including stale-claim rules.
3. Change only the selected task fields:
   - `status: claimed`
   - `owner: worker`
   - `claimed_by: <collision-resistant session id>`
   - `claimed_at: <ISO timestamp>`
   - `updated: <same ISO timestamp>`
4. Preserve unrelated bytes and YAML block formatting.
5. Update `main` with the roadmap blob SHA.
6. Treat a SHA conflict or changed task state as `ALREADY_CLAIMED`.
7. Re-fetch and verify that the task names this session before implementing.

This is the connector equivalent of `scripts/claim_task.py`: the safety property is the fresh eligibility check plus compare-and-swap write, not the presence of a local Python process.

## Later task transitions use `task-events`

For `review`, `done`, `ready`, `rearm`, `needs-human`, or `blocked`, create a small unique YAML file directly on Conductor `main`:

```yaml
version: 1
project: ai-art-academy
task: t-010
operation: rearm
updated: '2026-07-25T10:00:00Z'
note: >-
  Merged the scoped front-end accessibility pass and verified the resulting main branch.
```

Use a collision-resistant path such as:

```text
task-events/2026-07-25T100000Z-ai-art-academy-t-010-rearm-a1b2.yaml
```

Rules:

- Quote free-form scalar text or use a YAML block scalar. An unquoted `: ` can make the event invalid.
- Include `soft_gate`, `owner`, `note`, or `learning` only when applicable.
- Optionally include your `session` on `review`/`done`/etc. events. When present, the processor verifies it matches the task's live `claimed_by` and consumes the event as `ALREADY_CLAIMED` (no mutation) if a different session now owns the task — so a session that lost the claim cannot later close the winner's task. Omitting `session` keeps the legacy sessionless behavior.
- Do not use `force: true` without explicit approval for that override.
- Do not assume creation means application.

The `Process task events` workflow reads the full roadmap in its checkout, applies a targeted text patch, validates the result, resolves dependencies, commits to `main`, and removes consumed events. The workflow is serialized and retries one clean non-fast-forward race without force-pushing.

After creating an event:

1. Inspect the associated Actions run.
2. Re-fetch the roadmap and verify the expected task state.
3. If the workflow fails, inspect job logs.
4. Repair or delete only the current session's malformed or stale event using its current blob SHA.
5. Never leave a poison event blocking the shared queue.

## TALKBACK and learning closeout

Append required TALKBACK entries by page-fetching the complete current file, appending new text without modifying existing entries, and updating it with the exact current blob SHA.

Prefer the task event's `learning` payload for `done` and `blocked` outcomes so the processor appends `LEARNING.yaml` safely.

## Pull requests and merge

Implementation work still follows the normal flow:

1. Create `worker/<project>-<task-id>-<session>` from the post-claim `main` commit.
2. Implement a focused change in the correct repository.
3. Queue and verify `review` before opening the implementation PR.
4. Inspect the complete diff, reviews, threads, mergeability, commit checks, and Actions logs.
5. Fix failures on the same branch.
6. Merge only reversible, scoped, verified work allowed by `AGENTS.md`, using the expected head SHA.
7. Queue and verify `done` or `rearm` after merge.
8. Confirm no stale claim, event, PR, or branch remains.

## Invalid stopping reasons

These are not valid reasons to perform no work:

- the default file response was truncated;
- no local shell or Python runtime was available;
- the roadmap was too long for one display response;
- the task transition required changing a large roadmap;
- a tiny event file had not yet been verified.

Use paginated reads, exact-SHA writes, the task-event processor, and Actions evidence instead.