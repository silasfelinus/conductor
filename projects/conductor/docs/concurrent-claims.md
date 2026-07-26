# Design doc: concurrent Worker claims via per-project leases

Design record for `conductor/t-033`, the suggested first task from
`pitches/2026-07-16-concurrent-worker-claim-leases.md` (approved by Silas
2026-07-25). Pins the contention model on paper before any harness or
`claim_task.py` change ships. No code changes in this doc — implementation is
future `ready` work once this model is accepted.

## 1. Lease semantics

The existing lease is exactly what `roadmap_claims.py` already implements:
`status: claimed` + `claimed_by` + `claimed_at`, reclaimable once
`claimed_at` is older than `CLAIM_TTL_MINUTES` (90). `claim_is_stale()`
already treats a missing/unparseable `claimed_at` as stale too, so a
hand-edited or pre-mechanism claim can never lock a task forever. None of
this needs to change for concurrency — it was already written to answer "is
this claim still alive," a question that matters *more*, not differently,
once several claims can be alive at once.

**Is 90 minutes still the right bound under N concurrent lanes?** Yes, and
the reasoning gets stronger, not weaker, with concurrency:

- The TTL exists to catch a crashed/abandoned session, not to police a slow
  one. That failure mode (a session dies mid-task) is per-session and
  independent of how many other sessions are also running — N lanes running
  in parallel doesn't make any single lane's crash more or less likely, so
  the same 90-minute bound still fits the "real burst cycle: research +
  implementation + PR" case it was set for.
- What concurrency *does* change is the cost of a false reclaim (a session
  that's still alive but slow gets its task grabbed out from under it,
  producing exactly the double-build collision `claim_task.py` exists to
  prevent). With N lanes contending for the same pool of `ready` tasks
  instead of 1, a shorter TTL raises that collision risk without a matching
  benefit — abandoned-claim recovery speed was never the bottleneck on
  throughput. Leave `CLAIM_TTL_MINUTES` at 90 for the v1 rollout in section 4;
  revisit only if real collision data says otherwise.

**What must a session do if its own lease expires mid-task?** Today nothing
enforces re-validation before the PR — a session that's still working past
90 minutes has no way to know its `claimed_at` is now stale from another
picker's point of view. Under N=1 (today) this is nearly harmless: a second
picker only exists if a new session starts a fresh cycle, and
`next_ready_task.py` surfacing the task as pickable again is rare enough in
practice that the two sessions' work has consistently been caught at push
time (`ALREADY_CLAIMED`/non-fast-forward) rather than actually colliding.
Under N>1, a second lane is *already running concurrently* and can pick the
"abandoned" task in the same window the first lane is still mid-implementation
— the race window shrinks from "next hourly cycle" to "another lane's next
`claim_task.py` call," which is minutes, not hours.

Required behavior change for parallel lanes: **before opening a PR (the
`status: review` step, hard rule/AGENTS.md step 7), a session must re-fetch
`origin/main` and check its own claim is still intact** — same
`project/task_id`, `claimed_by` still equal to its own session id, and
`status` still `claimed` (not reclaimed by someone else and possibly already
completed). Concretely: `read_file_at_ref(ROOT, "origin/main", roadmap_path)`
then re-run `find_task` + compare `claimed_by`. Two outcomes:

- **Still ours:** proceed to `status: review` as today.
- **Reclaimed by another session:** the "Same-session post-compaction
  collisions" playbook already in AGENTS.md § Rotation collisions applies
  verbatim — `git fetch origin main`, diff the task's current state, and
  defer to whichever side actually landed a merge rather than pushing a
  wrap-up over it. This doc doesn't need to invent a new resolution
  procedure, only extend the existing one's trigger from "resuming after
  compaction" to "finishing under a possibly-expired lease."

This re-validation is the one real behavior gap concurrency opens up in
lease semantics; everything else about the TTL model already generalizes.

## 2. The cap check

**Predicate**, added to `claim_task.py`'s existing critical section (the
`for attempt in range(1, MAX_ATTEMPTS + 1)` loop in `claim()`, right where it
already does `check_claimable` against a freshly-fetched `origin/main`):

```
count active non-stale claims across all projects on origin/main
if count >= N: raise ClaimError("CAP_REACHED: N active claims already in flight
  (limit N) -- rotate to review/reviewer work, or wait, instead of claiming
  another task", code=3)
```

"Active non-stale claim" reuses `task_is_claimable`'s own staleness logic
inverted: a task with `status: claimed` and `claimed_at` within
`CLAIM_TTL_MINUTES` counts toward the cap; a `status: claimed` task with a
stale `claimed_at` does not (it's already reclaimable, so it shouldn't also
occupy a cap slot — that would let a single crashed session's ghost claim
permanently shrink capacity by one). Counting requires reading every
project's `roadmap.yaml` at `origin/main`, not just the one project being
claimed into — this is the one place the check must scan the whole repo
rather than a single file, since the cap is global. `next_ready_task.py`
already iterates `projects/*/roadmap.yaml` for its own ready-task scan, so
the same directory walk is reused, not a new pattern.

**Global cap, not per-project**, for v1. Two reasons:

- The pitch's own throughput argument ("tonight there were ~20 egress-free
  ready tasks alone") is about total agent-hours in flight across the whole
  board, not about any one project being underserved — a global cap directly
  targets that.
- A per-project cap needs a second parameter (which projects get more than
  1) with no data yet to set it from. `priority.yaml` already ranks projects,
  but "high priority" and "benefits from 2 concurrent lanes" are different
  questions — coloring-book/ai-art-academy's render-backend bottleneck this
  same week (see `TALKBACK.md` 2026-07-26 entries) is a case where more
  *concurrent* claims wouldn't have helped at all, since the constraint was
  external throughput, not claim serialization. Starting global keeps the
  first rollout's only new variable to measure as "does N=2 reduce wall-clock
  without raising collisions," not two variables at once.

**Where the count is read from matters**: `origin/main`, inside the same
fetch-then-check-then-commit-then-push loop `claim_task.py` already runs, not
a cached count from earlier in the session. Two lanes claiming in the same
few seconds must each recompute the live count immediately before their own
push attempt (the existing non-fast-forward retry loop already handles the
resulting push race — a cap check is just one more predicate evaluated
inside `check_claimable`'s window, not a new race to solve).

**Interaction with the retry loop**: `CAP_REACHED` should exit the same way
`ALREADY_CLAIMED` does today (code 3, "rotate to the next ready
task/project") — *not* retry in the `MAX_ATTEMPTS` loop the way a genuine
push race does. Retrying a cap check in a tight loop just spins until
someone else's claim finishes or expires, which is a session-side polling
anti-pattern the codebase has otherwise avoided (see `claim_task.py`'s own
docstring: "rotate to the next ready task/project instead"). A session that
hits `CAP_REACHED` should behave exactly like one that hits
`ALREADY_CLAIMED`: fall back to Reviewer-role work (review a reviewable PR,
per `select_role.py`'s existing role split) if any is available, or end the
cycle cleanly if not. This reuses the role-assignment machinery that already
exists rather than adding new "wait and retry" behavior to `claim_task.py`.

## 3. Shared-writer safety

Enumerating every file a concurrent lane can write, and what happens when
two lanes touch the same one in the same window:

| File | Write pattern | Concurrent-write risk | Existing mitigation |
|---|---|---|---|
| `projects/<p>/roadmap.yaml` — **different task, same project** | `set_task_field.py`, line-oriented, replaces one task's field block in place | Low — two edits to different task blocks are non-overlapping line ranges; a normal git merge (or `claim_task.py`'s own rebuild-on-new-tip retry) resolves cleanly | Already handled: `claim_task.py`'s push-race retry re-reads the fresh tip and rebuilds its one-field edit against it |
| `projects/<p>/roadmap.yaml` — **same task** | same | High if it happens, but structurally prevented — the claim itself is the mutual-exclusion mechanism for a single task. Two lanes cannot both be validly `claimed` on the same task at once (section 2's cap check is a *count* limit, not a substitute for this — the per-task claim gate in `check_claimable` stays exactly as strict as it is today) | No new mitigation needed; this is precisely what claiming already prevents, independent of the cap |
| `TALKBACK.md` (root and per-project) | Manual append, whole-file edit tool | Medium — two lanes appending in the same window both read-then-write the file; a naive last-write-wins push could drop one entry | **Append-only convention (hard rule 7) already requires this**, but the *mechanism* has been session-serial so far (only one active claim at a time meant only one lane could be mid-append). Concurrency requires the same discipline `claim_task.py` uses for roadmap edits: fetch `origin/main` immediately before appending, and if it moved since the read, re-append onto the fresh tip rather than pushing a diff computed against a stale base. This is a **required harness change** for the parallel-lanes rollout, not something free from today's tooling — see "Gaps to close before rollout" below |
| `LEARNING.yaml` | Manual append (one YAML list item per closed task), read by `build_learning_summary.py` | Same shape as TALKBACK — append-only, same fetch-immediately-before-append fix needed | Same gap as TALKBACK; the "Reviewer batch-merge note" in AGENTS.md hard rule 9's companion paragraph already says *"for append-only files both sides touched (TALKBACK.md, LEARNING.yaml), keep both sides' entries rather than picking one"* — that's the correct merge policy, it just needs a live pre-push re-fetch to avoid needing a manual merge at all |
| `STATUS.md`, `workspace.html`, `ROADMAP-AUDIT.*`, `LEARNING-REPORT.md` | CI-regenerated (`refresh-status.yml`) from repo state, not hand-appended by agents | Low — these are always-regenerable outputs | Already fully covered by hard rule 9: any conflict "always resolves to the latest version (accept main's copy, or the most recent CI commit)." This rule was written for the single-lane-plus-CI-bot race and needs no change for N lanes — more concurrent producers of roadmap state just means the regenerated files go stale slightly more often between CI runs, not that the conflict rule stops applying |
| `pitches/<date>-<slug>.md`, `projects/<p>/docs/*.md` | New-file-per-task, or single-owner edits to a file only that task's own lane touches | Low — collisions would require two lanes independently choosing the identical filename, which the date+slug convention makes vanishingly unlikely | No change needed |
| A project's non-roadmap source files (e.g. `projects/humboldt-scoop-cms/src/*`) | Whatever the task touches, on the lane's own feature branch | None from concurrency itself — each lane works on its own branch/worktree per the pitch's design, and only merges to `main` via its own scoped PR, same as today's single-lane model | Worktree isolation (part of the pitch, see below) already prevents two lanes' uncommitted work from colliding on a shared checkout |

**Gaps to close before rollout** (the honest answer to "does hard rule 9
already cover this," since the pitch asked to confirm it):

Hard rule 9 fully covers the **CI-regenerated files** — no gap there. It does
**not** cover TALKBACK.md/LEARNING.yaml, because those aren't CI-regenerated;
they're hand-appended by agents, and the rule that governs them today is the
Reviewer batch-merge companion note (merge both sides), which assumes a
*human or Reviewer* resolving an occasional conflict during a sweep — not an
automated fetch-append-push loop running unattended inside a Worker lane.
Before N>1 lanes append to the same file unattended, `claim_task.py`'s
own `commit_file_on_ref` pattern (scratch-index, single-file commit, built on
a freshly-fetched parent, retried on non-fast-forward) needs to be reused —
or a thin wrapper around it added — for TALKBACK/LEARNING.yaml appends
specifically. This is the one piece of section 3 that is genuinely new
plumbing, not just "confirm the existing rule already applies."

## 4. Rollout

Start at **N=2**, not the pitch's suggested 3, and scope it to **one
project** first rather than gating by a feature flag on the harness as a
whole:

- **Why 2, not 3 for v1:** the collision surface this doc is actually
  worried about (section 3's TALKBACK/LEARNING.yaml append race) has never
  been exercised concurrently before — going straight to 3 tests both "does
  the cap check work" and "does append-race handling work" at a higher
  concurrency than either has been proven at. N=2 is the minimum value that
  exercises real contention (the cap check has to reject a 3rd claimer, two
  lanes can genuinely race an append) while keeping a failure easy to
  fully read through by hand in TALKBACK/LEARNING.yaml.
- **Why one project, not a global flag:** `ai-art-academy`'s `t-010`
  (recurring continuous-improvement) has independently demonstrated the
  concurrent-collision failure mode for real, twice, without any concurrency
  feature turned on (see `TALKBACK.md` 2026-07-26 "ai-art-academy/t-010 |
  pattern" — two same-day PRs, #1174/#1175, for the identical Hudson River
  School work; and the rearm-status bug from the same task's own note).
  That's a live signal this exact project's recurring-task shape is prone to
  the failure this rollout is meant to test *for*, which makes it a good
  canary — but it's *also* evidence the project already has enough
  contention noise from ordinary same-day reruns that a first concurrency
  test there would be hard to attribute cleanly. Pick a **different**
  high-volume, low-ambiguity project instead: **`coloring-book`**, whose
  `t-022` (recurring production pass) is well-scoped, always has a next
  action, and — per this same day's TALKBACK entries — its actual bottleneck
  right now is the external render backend, not claim contention, so running
  2 lanes there tests the claim/lease/append machinery without a confound
  from genuinely-duplicated creative work landing twice.
- **What "behind a flag" means concretely** given this repo has no runtime
  feature-flag system: an explicit allowlist, e.g. a new `CONCURRENT_PROJECTS:
  [coloring-book]` (or similar) constant read by the cap-check predicate in
  section 2 — the global N-cap only relaxes past 1 when the project being
  claimed into is on the allowlist; every other project stays at the
  existing implicit N=1 (a session already holding a claim anywhere is
  blocked from claiming again by hard rule 4, unchanged). This is a smaller
  change than a harness-level flag and keeps the blast radius of a bad
  rollout to one project's roadmap/TALKBACK file.
- **What to measure before widening:** count `CAP_REACHED` rejections
  (expected/healthy — proves the cap works) versus genuine
  `ALREADY_CLAIMED` collisions on the *same* task (would mean the per-task
  claim gate itself broke under concurrency, which should be ~impossible per
  section 2's table and any occurrence is a stop-ship bug, not a tuning
  signal) versus TALKBACK/LEARNING.yaml append conflicts requiring manual
  resolution (measures whether section 3's gap-closing plumbing actually
  works). A clean run — cap rejections present, zero same-task collisions,
  zero manual append conflicts — over a handful of cycles is the bar for
  widening the allowlist to a second project and/or raising N to 3.

## Out of scope for this doc

Per the pitch, this is the design doc only — no implementation. Not covered
here (future `ready` tasks once this model is accepted): the actual
`claim_task.py`/`git_plumbing.py` code changes for the cap predicate and the
TALKBACK/LEARNING.yaml append-commit wrapper; the harness/session-runner
side of "one git worktree per concurrent lane" (the pitch's own "Rough
effort" section already flags this as "the biggest piece, and partly a
runner concern, not a repo concern"); and any `AGENTS.md` rule-text edits
(hard rule 4's "one task in flight at a time" needs a per-*session*
carve-out, not a repo-wide change, once N>1 is real — worth its own follow-up
once the allowlist mechanism in section 4 is implemented).
