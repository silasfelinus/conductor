# Worker stale-claim recovery

This policy prevents one recoverable bookkeeping or tooling problem from freezing the entire Worker queue across repeated runs.

## Core rule

A soft blocker may stop one task, but it must not stop unrelated ready work.

When a claimed task cannot be completed or reconciled because of connector, network, branch, file-editing, CI, or other infrastructure limitations, the Worker must classify the failure before retrying.

## First occurrence

1. Attempt one safe, scoped recovery using the capabilities currently available.
2. Do not create broad-permission helpers, repeated temporary workflows, or increasingly elaborate workarounds for a bookkeeping-only mutation.
3. If recovery fails, record the exact blocker in the task note and classify it as `transient` or `actionable` under AGENTS.md.
4. Clean up temporary branches, trigger files, workflows, and helper permissions created during the attempt.

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
2. Prefer a direct, byte-preserving roadmap edit.
3. If the current connector cannot perform that edit safely, preserve the evidence once and park the reconciliation as a soft blocker.
4. Do not hold the implementation task as `claimed` across runs merely because its roadmap closeout could not be written.
5. Continue with unrelated ready tasks. Dependents may remain waiting until reconciliation is safely applied.

## Branch hygiene

- A temporary or superseded recovery branch must be deleted in the same session its attempt is abandoned or superseded.
- Before retaining any branch, compare it with `main` and document its unique, still-needed work.
- A branch containing only a trigger, helper, or already-superseded bookkeeping artifact is disposable.

## Retry budget

The same recovery method may be attempted once. A second attempt requires a material change in capability, repository state, or instructions. Without such a change, move on.

The Worker must never report the same blocker in consecutive runs as the sole reason for doing no other work when unrelated `ready` tasks exist.
