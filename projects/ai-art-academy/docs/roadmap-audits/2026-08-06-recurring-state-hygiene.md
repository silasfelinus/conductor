# AI Art Academy recurring-state hygiene audit

Date: 2026-08-06  
Task: `ai-art-academy/t-010`  
Lane: 2, roadmap accuracy  
Session: `2026-08-06T071232Z-ai-art-academy-t010-l2-r8p4`

## Scope

This pass compared the live `t-010` roadmap entry with its stated bookkeeping contract, the append-only continuous-improvement run log, and the connector task-event behavior documented in `docs/github-connector-worker.md`. It did not enqueue art, touch production data, or change Kind Robots application code.

## Findings

### 1. The structured rotation state is currently correct

The immediately preceding lane-1 cycle merged `silasfelinus/kind_robots#1518`. The live mapping records:

- `last_lane: 1`
- `next_lane: 2`
- `last_pr: silasfelinus/kind_robots#1518`

This cycle therefore correctly selected lane 2. No rotation repair was needed before starting.

### 2. The task note has started regrowing the history that t-039 moved out

`t-010` says historical runs belong in `docs/continuous-improvement-run-log.md` and that its roadmap note should stay short. The current note nevertheless contains several completed-cycle paragraphs, including lane 3, lane 4, and lane 1 narratives.

That is not merely cosmetic. A selector must now parse both the structured mapping and a growing pile of stale prose, recreating the ambiguity t-039 was designed to remove. Future closeout tooling should append detailed cycle evidence to the run log and keep the roadmap note to:

1. the standing lane menu;
2. one concise current operational caveat, when one exists;
3. the structured `continuous_improvement` mapping.

This audit does not rewrite the large roadmap file through the connector merely to prune prose. The safe repair belongs in the existing recurring-event tooling work so the next closeout does not immediately regrow it.

### 3. `implementation_pr` is stale and overlaps `continuous_improvement.last_pr`

The task still carries:

```yaml
implementation_pr: 'silasfelinus/kind_robots#1502'
```

while the authoritative structured field says the latest completed cycle is `silasfelinus/kind_robots#1518`. For a recurring task, a singular `implementation_pr` cannot remain truthful across cycles and now conflicts with the purpose of `last_pr`.

Recommended repair: remove `implementation_pr` from `t-010` once the roadmap can be edited through a full-file-preserving path, and use `continuous_improvement.last_pr` plus the append-only run log as the only current/history pair.

### 4. Rearm leaves stale claim identity behind

Before this session's claim, `t-010` was `status: ready` but still carried the prior cycle's `owner`, `claimed_by`, and `claimed_at`. The new claim safely replaced those fields because the processor keys eligibility on status and session, but a ready task retaining an old claim identity is misleading to audits and humans.

Recommended processor contract for `rearm`:

- set `status: ready`;
- clear `owner`;
- clear `claimed_by`;
- clear `claimed_at`;
- update the structured continuous-improvement fields when supplied by the event.

This is adjacent to the already-known nested-mapping drift tracked by the Academy roadmap. It should be fixed once in `process_task_events.py`, not patched by every recurring project.

## Current project truth

- Milestones `m2` and `m6` should remain `in-progress`.
- `m6` is intentionally perpetual because `t-010` is recurring.
- No evidence in this pass justifies changing the LoRA/render-relay gates or queuing replacement ArtJobs.
- The next rotation after this lane-2 audit is lane 3, inspiration assets.

## Completion test

This audit is complete when it is merged, the recurring task is rearmed to `ready`, and the roadmap records lane 3 as the next intended rotation without leaving this session's claim or event behind.
