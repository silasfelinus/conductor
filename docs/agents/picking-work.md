# Picking what to work on — full procedure

> Moved verbatim from `AGENTS.md` on 2026-11-01 PT (token-essentialization pass 2). `AGENTS.md`
> keeps the condensed rule and links here; this file holds the full detail and the incident
> history behind it. If the two ever disagree, the rule in `AGENTS.md` wins — fix this file.
> Read when claiming, reviewing-state transitions, dependencies or umbrella tasks come up.

## Picking what to work on
1. **Check Todos first** — run `scripts/fetch_todos.py` and handle the top OPEN todo
   before continuing to roadmap tasks (see "Todos" section above).
2. **Read `CONTROL.md` first** — its global overview, then the block for the project you'll
   work on. CONTROL.md holds Silas's current intent and OVERRIDES anything in a roadmap it
   conflicts with. Then read this file, `projects/priority.yaml`, and the relevant
   `projects/*/roadmap.yaml` (skip `_template`).
3. **Check `project-overrides.yaml`** — lifecycle is authoritative. Work finite
   `status: active` projects first. Only when no active project has claimable ready work may
   `status: continuous` projects run, in priority order. Paused, retired, and finished projects
   are off-limits. Continuous is intentionally a fallback tier, not an equal-priority synonym
   for active.
4. Honor CONTROL.md's direction and notes, then each project's `notes_from_silas`, over
   default ordering. (STATUS.md is auto-generated and read-only — never edit it.)
5. Within the selected lifecycle tier/project, take the highest-priority task with
   `status: ready`. If a finite active project's list reaches zero open tasks, do NOT infer
   completion from N/N. Reconcile its `goal` against the actual product and add missing work
   or explicitly finish/pause it. A user-facing software project is not `finished` until its
   live/preview front end has been checked at phone/tablet/desktop widths and Silas has either
   accepted the visual state or explicitly waived that check in the current session. Proposal
   projects may keep their documented pitch cadence. Never-idle work belongs to the continuous
   lifecycle described below, not to an exhausted finite active roadmap.
6. **Claim it before doing real work**: run
   `python scripts/claim_task.py <project> <task-id> --owner <worker|reviewer> --session <id>`.
   This checks the task's live state on `origin/main` (not your local checkout, which
   may be stale) and, if claimable, pushes a small `status: claimed` commit straight to
   `origin/main` before you write any implementation. If it exits non-zero
   (`ALREADY_CLAIMED`), someone else is already on that project/task — do not implement
   it; go back to step 5 and pick the next `ready` task instead. See "Rotation
   collisions" below for why this step exists.
   Pick a collision-resistant `--session <id>`: a full ISO timestamp with seconds
   plus a short task-specific suffix (or a random token), not a coarse hour/rotation
   label — `claim_task.py` keys on project/task rather than session id, so a reused
   label never causes a false claim conflict, but it does leave the `claimed_by`/
   TALKBACK trail looking like one continuous session did unrelated work when two
   concurrent burst-mode sessions happen to reuse the same label within the same
   hour (coat-dance/t-001, 2026-07-21 — see root `TALKBACK.md` same date).
   **Connector-only Workers** (connected GitHub tools but no local shell/Python)
   claim, review, and close out through session-aware `task-events` instead:
   a `claim` event now **requires** a non-empty, collision-resistant `session`,
   the processor writes `claimed_by`/`claimed_at` and preserves the same atomic
   `ALREADY_CLAIMED` invariant as `claim_task.py` (a rival session's claim is
   consumed as a collision with no roadmap mutation, not collapsed into an
   owner-level no-op), and `review`/`done` events may carry a matching `session`
   so a session that lost the claim cannot later close the winner's task. See
   `docs/github-connector-worker.md` for the full connector runbook.
7. **Set `status: review` before opening the PR — every session, not just hourly
   `worker/*` runs.** This applies equally to Silas-directed `claude/*` sessions and
   burst-mode cycles doing Worker-style roadmap pickup, not only the OpenAI hourly
   Worker. Once implementation is done and you're about to `gh pr create` (or the
   GitHub MCP equivalent), run
   `python scripts/close_task.py <project> <task-id> review --session <id>` (own
   branch + its own small PR into `main` — **never** `set_task_field.py` followed by
   a direct commit/push, and never a direct push to `main` the way `claim_task.py`'s
   single atomic claim commit is sanctioned to do). `close_task.py` is not just for
   `done`: its `status` argument is generic (its own docstring's usage examples cover
   `done`, `needs-human`, and this `review` case identically), so the same
   collision-resistant, fetch-checked-against-`origin/main` git plumbing that avoids
   a stale-branch merge conflict on `done`/`needs-human` also covers `review` — no
   new script needed. (Resolved conductor/t-119, 2026-08-20: AGENTS.md previously left
   this transition's landing mechanism ambiguous — `claim_task.py` has an explicit,
   documented direct-to-`main` exception to hard rule 1 for its one atomic claim
   commit, `close_task.py`'s own docstring is explicit that hard rule 1 does **not**
   carve out a second exception for close-out-shaped bookkeeping, but nothing said
   which side of that line the `review` transition falls on. Prior git history
   (`4dac352`, `ec5086a`) was genuinely ambiguous either way. model-builder/t-029
   cycle 21 (2026-08-20) treated it as needing its own branch+PR per a strict reading
   of hard rule 1 and hit a real STATUS.md-refresh merge conflict doing so by hand
   with `set_task_field.py` + a manually-managed branch — but that conflict was a
   symptom of not using `close_task.py`'s fetch-fresh plumbing for the transition,
   not of branch+PR being the wrong shape. `close_task.py`'s own git plumbing commits
   directly against whatever `origin/main`/`origin/<branch>` looks like *at push
   time*, the same way `claim_task.py`'s does — so routing `review` through it avoids
   that conflict class without needing a new direct-to-`main` exception.) Confirm
   `claimed_by`/`owner` still identify your session and its actual branch name — it
   does not need to start with `worker/` — so a later Reviewer sweep can find the
   in-progress work by reading roadmap state, instead of having to hand-check the
   open-PR list on GitHub. Skipping this step is exactly what caused
   `superkate-hairstyle-ai/t-017` to sit at `status: claimed` after PR #317 had
   already merged (twice — see `TALKBACK.md` 2026-07-10 and 2026-07-16, and
   `superkate-hairstyle-ai/t-020`); a task left at `status: claimed` past a session's
   lifetime looks abandoned rather than in-review, and its claim can silently expire
   under `CLAIM_TTL_MINUTES` while the PR is still open. If your session merges its
   own PR in the same run (see "Reviewer (Claude) — CAN merge ... from `claude/*`
   branches" below), it's fine for `status: review` to be short-lived — set it before
   `gh pr create` and flip to `status: done` right after the merge via another
   `scripts/close_task.py` call (own branch + its own small PR, never a direct push
   to `main` — see the "software" close-out step below; several close-outs from the
   same PR/session can share one `close_task.py` branch, so the `review` and `done`
   transitions for the same task may land as one PR when both happen in the same
   run) — the point is that roadmap state never silently jumps from `claimed` to
   `done` with no externally-visible checkpoint in between.

### Rotation collisions

Picking a task does not reserve it — always claim with `claim_task.py` (step 6), which fails
fast into `ALREADY_CLAIMED` on a race; claims self-expire after 90 minutes. Full history and the
same-session post-compaction variant: `docs/agents/roles/worker.md`.

### Review-claim markers — avoiding duplicate review work

Before reviewing/merging a PR, follow the review-claim marker protocol in `docs/agents/roles/reviewer.md`.

### Task dependencies (pipelines)
A task may declare `depends_on: <task-id>` (or a list). A task is only workable when every
dependency is `status: done` AND, if the dependency is human-gated, `approved_by_human: true`.
Tasks waiting on an unmet dependency carry `status: waiting` — never claim a `waiting` task.
When Silas approves an upstream task, the next Worker run calls `scripts/resolve_deps.py`,
which flips any now-satisfied `waiting` tasks to `ready`. So the Worker's FIRST action each
cycle is to run the resolver, THEN pick a ready task.

### Umbrella sweep tasks — `remaining_scope_task`

A recurring umbrella task (e.g. a layout-contract sweep tracking several buckets toward
zero) can reach a state where every bucket is at zero except one already owned by a
dedicated follow-on task. At that point the umbrella has no independent slice left, and
claiming it directly only duplicates or collides with the follow-on. Set
`remaining_scope_task: <task-id>` on the umbrella pointing at that sibling task (same
roadmap): `run_worker.py`'s `find_ready_task`, `next_ready_task.py`'s `first_ready_task`,
and `claim_task.py` all treat the umbrella as not-yet-claimable for as long as the
referenced task exists and hasn't reached `status: done`. No field set — current behavior,
unaffected. (Filed from conductor issue #1627, interface-vision/t-017 vs. t-058.)

### Human-gated stages
A task may set `gate_human: true`, meaning its output must be approved by Silas before
dependents unblock — even for software. The Worker finishes such tasks at `status: needs-human`.
Silas approves by setting `approved_by_human: true` and `status: done` in the roadmap. The
resolver treats a gated task as still blocking until `approved_by_human: true`.
