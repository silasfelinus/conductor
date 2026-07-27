# AI Art Academy claim-metadata audit — 2026-07-27

## Finding

The recurring `ai-art-academy/t-010` task correctly returned to `status: ready` after its previous front-end polish cycle, but the live roadmap still retained the completed session's `claimed_by` and `claimed_at` fields until the next claim was processed.

This is not merely cosmetic. A ready task carrying an old session identity creates three avoidable ambiguities:

1. Humans and agents cannot tell whether the task is truly unowned or whether the status and lease disagree.
2. Connector-only workers may mistake the old session trail for an active collision when scanning a narrow roadmap excerpt.
3. Audit and recovery tooling must infer intent from status precedence instead of receiving a clean state transition.

The next claim replaced the stale identity safely because the task-event processor compared the new unique session, but the rearm transition should have cleared the old claim metadata itself.

## Current roadmap assessment

- Milestone `m2` remains correctly `in-progress`: `t-004` is structurally ready but operationally deferred until both queue depth and oldest-pending age improve substantially.
- Milestone `m5` remains correctly `in-progress`: generated Academy art is still pending, and repeated unchanged queue checks are explicitly discouraged.
- Milestone `m6` remains correctly `in-progress`: recurring task `t-010` is the continuous-improvement loop and intentionally never reaches `done`.
- The lane rotation is coherent: the previous cycle completed lane 1, so this cycle is lane 2 and the next preferred lane is lane 3.

## Recommended invariant

For every transition to `ready` or `rearm`, the task-event processor should remove all lease-specific fields unless the event explicitly supplies a replacement:

- `claimed_by`
- `claimed_at`
- branch metadata associated with the completed claim

`owner` should follow the roadmap convention for reusable recurring tasks, but it must not be treated as a session lease. The session identity belongs only to an active `claimed` or `review` state.

A regression test should start with a recurring task in `review` carrying all claim fields, process a `rearm` event, and assert:

- `status` becomes `ready`;
- claim/session/branch metadata is absent;
- unrelated bytes in the roadmap remain identical;
- a following claim by a different session succeeds without relying on stale-field overwrite behavior.

## Scope decision

This cycle records the defect and the precise expected invariant without modifying shared task-event machinery inside an Academy recurring lane. The implementation belongs in a focused Conductor task because it affects every project using connector-native rearm events and deserves processor-level regression coverage.
