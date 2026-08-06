# AI Art Academy live-task triage

Date: 2026-08-06
Task: `ai-art-academy/t-010`
Lane: 2, roadmap accuracy

## Result

The roadmap's remaining open work is internally consistent, but its two immediately visible `ready` tasks are not equally executable.

### `t-044`: keep ready, gated, and unclaimed

`t-044` is the live Kontext LoRA verification task. Its latest evidence is still ArtJobs `7622` and `7623`, queued on 2026-08-05 while the relay had 3,140 pending jobs and ComfyUI was effectively unavailable. Those jobs never reached the backend during the observation window, so neither success nor the prior `value_not_in_list` failure was established.

Roadmap treatment remains correct:

- `status: ready` preserves the next verification attempt once the relay is healthy.
- `gate_human: true` remains necessary because private `/object_info` and resource-path evidence may be required if the queued jobs reproduce the failure.
- `soft_gate: true` accurately records that infrastructure, rather than curriculum work, blocked the latest attempt.
- Do not enqueue replacement jobs until `7622` and `7623` have been checked. Re-submission would spend mana and duplicate durable evidence already in the queue.

### `t-057`: executable follow-up, but separate from this lane

`t-057` is a valid, reversible follow-up created from the most recent Academy front-end pass. It should remain a standalone task rather than being folded into recurring `t-010`: its app-wide `.kr-note*` migration crosses many component families and needs normal Kind Robots code review and TypeScript/contracts.

Keeping it separate prevents the recurring task from becoming an umbrella claim that collides with a dedicated ready task.

## Milestone accuracy

- `m2` should remain `in-progress` while `t-044` and its dependent live LoRA work remain unresolved.
- `m6` should remain `in-progress` because `t-010` is intentionally recurring.
- The completed curriculum and front-end milestones should not be reopened merely because the continuous-improvement loop continues.

## Next rotation

The next `t-010` pass should use lane 3, inspiration assets. It should not recheck the render queue unless both queue depth and oldest-pending age have materially improved from the recorded incident. A docs-only inspiration set remains the safe fallback while the relay is unhealthy.

No roadmap fields were changed in this pass because the live states already encode the correct decisions. This audit records why, so a later session does not mistake `ready` for immediately executable or duplicate the queued LoRA tests.
