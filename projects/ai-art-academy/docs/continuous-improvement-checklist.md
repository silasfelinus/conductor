# AI Art Academy continuous-improvement checklist

Use this checklist for recurring `t-010` cycles so each pass produces a distinct, verifiable improvement instead of re-auditing the same blockers.

## Rotation

Choose the first useful lane that has not run in the previous cycle:

1. Front-end polish
2. Roadmap accuracy
3. Inspiration and preview assets
4. Curriculum depth — if this cycle adds or edits a `stores/seeds/academyStyles.ts`
   entry, add or confirm the matching `curriculum-outline.md` section in the *same*
   cycle (or explicitly note the deferral in the task note); do not let the two
   drift, and do not treat clearing PUBLIC-DOMAIN-POLICY.md §1.3 (death date +
   creation date) as settling a curriculum "Example works" entry — §2 (an
   institution's accepted-license image) is a separate, per-work check (see
   ai-art-academy/t-050, t-051, t-052).

Record the lane, files changed, and verification in the task note before rearming `t-010`.

### Rotation state

Live rotation state lives on the roadmap task itself: `projects/ai-art-academy/roadmap.yaml`
t-010's `continuous_improvement:` field (`last_lane`/`next_lane`/`last_run`/`last_pr`) is
authoritative and should be kept current every cycle (t-039, 2026-07-26). Read that field
instead of inferring rotation from prose. Historical cycle detail lives at the task's
`run_log:` path, currently `projects/ai-art-academy/docs/continuous-improvement-run-log.md`.
Use the roadmap pointer rather than hard-coding a second history filename here.

The explicit state is the handoff between recurring cycles. Update it in the same closeout
as each `t-010` improvement whenever the available tooling supports nested-field updates;
if a connector-only `rearm` cannot update the nested mapping, make the next lane explicit
in the event note and treat the mismatch as bookkeeping debt rather than silently guessing.

## Lane 2 — roadmap accuracy

Roadmap-accuracy cycles should repair live coordination or documentation drift, not produce
another historical status essay. Prefer checks that derive their answer from current files:

- Run `python scripts/validate_roadmaps.py` and `python scripts/audit_roadmaps.py` when a
  local checkout is available. In connector-only sessions, inspect the same live roadmap,
  priority, override, task-event, PR, and Actions state directly.
- Compare curriculum coverage from `docs/curriculum-outline.md` with the current
  `stores/seeds/academyStyles.ts` seed when the Kind Robots checkout/connector is available.
  Do not copy a movement count into this checklist as long-lived truth. The most recent
  verified lane-2 pass (2026-08-07) found 47 curriculum sections and 47 seed entries; future
  cycles must recompute rather than trusting that number.
- Run the project-specific reporting/coverage helpers where relevant, especially
  `scripts/list_curriculum_coverage.py` and
  `scripts/verify_academy_style_preview_coverage.py`, instead of maintaining a manual
  table of every movement and preview here.
- Confirm t-010's `note`, `continuous_improvement`, and `run_log` agree about the last and
  next lane. The task-event rearm path has historically updated status/note without the
  nested rotation mapping, so this is an explicit check until conductor/t-103 closes the
  gap.
- Scan terminal tasks for stale *operational* lifecycle metadata (`retry_context`,
  `soft_gate`, `claimed_by`, `claimed_at`). A completed task may preserve failure history
  in its `note` or TALKBACK, but fields whose meaning is "what the next retry/blocked
  session should do" should not remain live after the task is done. Preserve history before
  removing any such field; do not erase prior critique.
- Keep active blockers short and current. Move accumulated attempt history into a task
  `run_log:` when one exists, as t-044 does, rather than stacking old incident prose in the
  roadmap note.

### Current live anchors

Use these as navigation, not as copied status:

- `t-010` — recurring continuous-improvement task and rotation state.
- `t-044` — current Kontext LoRA live-verification task; soft-gated and independently
  tracked with `docs/t-044-lora-loading-run-log.md`.
- `t-045` — LoRA A/B rerun, dependency-gated on t-044.
- `docs/curriculum-candidates/` — candidate/promotion state; inspect each file rather than
  relying on a cached count in this checklist.
- `docs/continuous-improvement-run-log.md` — append-only cycle provenance.

## Blocker discipline

Do not re-probe a blocker when the roadmap already contains fresh evidence with the same failure signature. Recheck only when capabilities, credentials, egress, relay state, database state, or instructions materially change.

A soft blocker never consumes the whole recurring cycle. Rotate to another lane and land a reversible improvement.

## Completion test

A `t-010` cycle is complete when all of the following are true:

- exactly one primary lane was selected;
- the change is scoped and reversible;
- verification is recorded;
- no live generation, publishing, deployment, spend, secrets, or production mutation occurred;
- **if the cycle opened a kind_robots PR, its CI status was polled and the PR was
  either merged or explicitly left open with a documented reason** (do not treat
  "PR opened" as the cycle's terminal state — a green, unmerged PR stranded at
  session end is not done; see the PR #814/t-036 incident below);
- the recurring task is rearmed to `ready` after merge.

Kaizen from a Reviewer pass, 2026-07-21 (t-036): a lane-1 cycle opened kind_robots
PR #814 (all 3 CI checks green) but ended the session without merging it or
rearming `t-010`, leaving the recurring task stranded at `status: claimed` with an
unmerged-but-green PR — the same failure shape as the earlier PR #942 incident
logged in this task's own roadmap note (2026-07-21 ~01:00 UTC: status field never
flipped after a merge). A later Reviewer-role session had to notice the open PR,
verify CI, and merge + rearm manually. The bullet above closes this gap for every
lane, not just lane 1 — any cycle that opens a kind_robots PR owns polling its CI
and merging (or explicitly parking it) before the cycle ends.
