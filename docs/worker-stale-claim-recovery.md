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

## Claim progress guarantee

The expected unit of Worker progress is a completed task cycle, not a claim attempt. Claiming is intermediate bookkeeping and should consume only a small part of the run.

A pending or unconsumed claim event is not a verified claim and is not, by itself, a reason to end the run.

After committing a claim event, the Worker must immediately inspect all three authoritative signals:

1. whether the `Process task events` workflow triggered;
2. whether the event was consumed; and
3. whether current `main` shows the selected task as `claimed` by `worker`.

If the event was not consumed, diagnose the workflow trigger, event shape, current task state, and recent `main` changes during the same run. Then attempt exactly one safe recovery with the capabilities currently available.

When current `main` still shows the task as `ready`, the preferred connector-safe recovery is:

1. Create `worker/<project>-<task-id>-claim-recovery` from current `main`.
2. Surgically update only the selected task's claim fields (`status`, `owner`, claim timestamp, and `updated`) and delete the exact stranded claim-event file on that branch.
3. Verify that the diff contains only the intended task fields and the stranded event removal. Preserve every unrelated roadmap byte.
4. Open and safely merge the reversible recovery PR.
5. Re-fetch current `main` and confirm the task is `claimed` by `worker` before starting implementation.
6. Delete the recovery branch after merge, then create the normal `worker/<project>-<task-id>` implementation branch from the verified claimed `main`.

Do not start implementation before the claim is verified. Do not select a second task while an unresolved claim event could still consume later and create a second active claim. Reconcile, consume, or remove the event first.

If the recovery attempt fails, classify the blocker under AGENTS.md instead of treating the claim attempt as useful task completion. Use a reviewed cleanup/release change when available so the event cannot fire later. Once the event is gone and the task is either `ready` or cleanly parked, immediately re-run dependency resolution and scan unrelated ready work.

A claim-system failure is a hard stop only when every safe claim and cleanup mechanism is unavailable or repository state is genuinely unstable. An untriggered workflow, connector timeout, pending task event, branch problem, or bookkeeping failure is never sufficient by itself to conclude the run.

Never finish a run with only "claim attempted" when a safe recovery path or unrelated eligible work remains.

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
