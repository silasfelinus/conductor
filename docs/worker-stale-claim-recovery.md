# Worker stale-claim recovery

This policy prevents one recoverable bookkeeping or tooling problem from freezing the entire Worker queue across repeated runs.

## Core rule

A soft blocker may stop one task, but it must not stop unrelated ready work.

When a claimed task cannot be completed or reconciled because of connector, network, branch, file-editing, CI, or other infrastructure limitations, the Worker must classify the failure before retrying.

## Task-event bridge

For roadmap mutations, prefer the small-file bridge documented in `task-events/README.md` instead of downloading and replacing a large `roadmap.yaml` through a connector.

1. Create exactly one event file under `task-events/` for the intended mutation.
2. Commit the event as the task's atomic state-change commit.
3. Wait for the `Process task events` workflow to consume the event and commit the authoritative roadmap change.
4. Treat the mutation as successful only after the event is gone and the expected state is visible on current `main`.
5. A failed event remains in the queue and its workflow failure is the evidence to inspect. Do not create a second equivalent event.

The event bridge is the normal path for `claim`, `done`, `ready`, `review`, `needs-human`, `blocked`, and recurring-task `rearm` transitions whenever direct full-file Git access is unavailable.

## First occurrence

1. Attempt one safe, scoped recovery using the capabilities currently available.
2. Prefer one task event over temporary workflows or broad whole-file rewrites.
3. Do not create broad-permission helpers, repeated temporary workflows, or increasingly elaborate workarounds for a bookkeeping-only mutation.
4. If recovery fails, record the exact blocker in the task note and classify it as `transient` or `actionable` under AGENTS.md.
5. Clean up temporary branches, trigger files, workflows, and helper permissions created during the attempt.

## Repeated occurrence

On the next run, compare the available capabilities and repository state with the prior recorded blocker.

- If the underlying capability changed, make one new safe recovery attempt.
- If nothing material changed, do not repeat the same workaround.
- Cleanly park the task as soft `needs-human` with `soft_gate: true`, or return it to `ready` when retry is appropriate and no partial implementation would be misrepresented.
- Release the Worker claim before selecting another task.
- Re-run dependency resolution and scan the full active-project priority queue for unrelated `ready` work.

A stale claim is not a hard human gate unless the blocked action itself is security-sensitive, irreversible, outward-facing, or required for every remaining eligible task.

## Bookkeeping reconciliation

When implementation already merged elsewhere but conductor task state is stale:

1. Verify the merge and its checks from authoritative repository evidence.
2. Submit a `done` task event with the verification note and learning record.
3. If the event workflow fails, preserve the evidence once and park the reconciliation as a soft blocker.
4. Do not hold the implementation task as `claimed` across runs merely because its roadmap closeout could not be written.
5. Continue with unrelated ready tasks. Dependents may remain waiting until reconciliation is safely applied.

## Branch hygiene

- A temporary or superseded recovery branch must be deleted in the same session its attempt is abandoned or superseded.
- Before retaining any branch, compare it with `main` and document its unique, still-needed work.
- A branch containing only a trigger, helper, or already-superseded bookkeeping artifact is disposable.

## Retry budget

The same recovery method may be attempted once. A second attempt requires a material change in capability, repository state, or instructions. Without such a change, move on.

The Worker must never report the same blocker in consecutive runs as the sole reason for doing no other work when unrelated `ready` tasks exist.
