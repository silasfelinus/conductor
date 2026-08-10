# coloring-book — Project TALKBACK

Append-only. Never edit or delete a prior entry.

## 2026-07-14 | Reviewer → Worker | coloring-book/t-019 | pattern

**Decision:** audited already-merged work (self-executed as Worker in a solo burst-mode session; kind_robots PR #260 merged)

**Failure category:** null (clean first pass on the scoped portion)

**What was good:**
- Read the actual kind_robots implementation before touching anything, which caught that the task description's "placeholder scaffold" framing was stale — the coloring engine (coloringStore.ts, coloring-canvas.vue, coloring-book-manager.vue) is functionally complete, not a placeholder.
- Kept the diff to exactly what was specified and verifiable: one tutorial-card entry, shaped identically to its five siblings.
- Didn't fabricate or skip the missing art assets — queued both via the established `projects/art-prompts.yaml` `requests:` mechanism instead of leaving them undocumented or inventing placeholder files.

**What to improve:**
- Could not run `eslint`/`vue-tsc` in kind_robots locally (`.nuxt/eslint.config.mjs` missing pre-`nuxt prepare`) — verification leaned on shape-parity review instead of tooling. Low risk given the change (single object-literal addition, no new imports/types), but a future session touching this file should run `nuxt prepare` first if time allows.

**Kaizen task:** t-020 — thicken coloring-book-page.vue's Generate/Proposals/Prompts tabs and add a second page set to coloring-book-manager.vue's SET_SLUGS, once t-006 lands.

**Pattern note:** Second instance this cycle (see conductor/t-012 pattern) of a roadmap task's note describing "scaffold"/"placeholder" state that had already moved past that description by the time it was picked up. Worth a standing reminder: read the target repo's current state before trusting a task's framing, especially on tasks that have sat `ready` for several days while related work merged elsewhere.

## 2026-07-17 | Reviewer → Worker | coloring-book/t-022 | pattern (autonomous conductor cycle)

**Decision:** merged conductor PR #697 (inventory reconciliation for Monster Recast book 1).
Recurring task flipped back to `status: ready` per convention; kaizen task t-029 filed.

**Failure category:** n/a (clean pass, recurring task in progress, not closed).

**What was good:**
- Reconciled all 18 represented_concept_ids without renaming or guessing files; the one
  ambiguous match (gothic-schoolgirl → mr-025) was explicitly flagged
  `needs_visual_verification: true` with a transparent "by elimination, not by text match"
  note rather than silently promoted to a confident match.
- Kept `accepted` fields untouched — respected the manifest's "confirmed approvals only from
  Silas" policy even though the task's own note allows "record accepted working files" later
  in the cycle.
- Verification was concrete and checkable: existence-checked every new inspiration path,
  reran both status scripts, confirmed the audit_roadmaps.py warning count was unchanged
  (pre-existing, unrelated).

**What to improve:**
- The elimination-only match is currently discoverable only by reading roadmap/proposals.yaml
  prose — nothing in `coloring_proposal_status.py --check` output flags it. Filed as t-029.

**Kaizen task:** t-029 — surface `needs_visual_verification`/elimination-only inspiration
matches directly in `coloring_proposal_status.py --check` output instead of leaving them to
prose notes.

## 2026-07-17 | Worker → Reviewer | coloring-book/t-022 | pattern (infra concurrency collision)

**Decision:** fixed a real infra bug found while checking on the recurring color-production
pass; no code claim beyond a one-line workflow config change. Task stayed `recurring: true`,
flipped back to `status: ready`.

**Detail:**
- `Process coloring art events` (process-color-art-events.yml, added earlier this same task's
  cycle as the connector-safe event bridge) had its first-ever run fail: 0/18 ArtJobs
  succeeded (2 immediate ComfyUI connection-refused, 16 timeouts after 300s).
- Cross-checked GitHub Actions run history: `Coloring Book Color ArtJobs`
  (monster-recast-art-jobs.yml) ran 18:37:54-21:10:53Z (success) while the event-bridge run
  went 20:34:48-22:00:43Z (failure) — a ~36-minute overlap. Both workflows call
  `consume_coloring_book_color_art.py --live` against the exact same `color-art-jobs.yaml`
  queue and the same single-worker render backend, but carried *different*
  `concurrency.group` values, so GitHub Actions ran them fully in parallel instead of
  serializing. The failed run's reported ArtJob ids (228, 229, 231, 233, 234, 236, 237,
  239-249) skip ids that the concurrently-running successful workflow was almost certainly
  consuming at the same moments — consistent with two workflows racing the same backend.
- This is exactly the "a second event would risk duplicate generation" risk this task's own
  note already flagged from an earlier cycle, just triggered by the *pre-existing*
  daily/push-triggered workflow rather than a second manually-dropped event file.
- Fix: unified `process-color-art-events.yml`'s concurrency group to
  `coloring-book-color-artjobs` (matching `monster-recast-art-jobs.yml`) so the two workflows
  now queue behind each other instead of hitting the render backend simultaneously. No other
  workflow touches either script, so no third group needed updating.
- The preserved event file (`color-art-events/20260717T203500Z-monster-recast-batch-01.yaml`)
  needs no manual edit — it self-retries on the next hourly cron and should now succeed since
  it won't race the other workflow.

**Suggested action:** when adding any new automation that shares a mutable resource (a queue
file, an external render backend, a rate-limited API) with an existing workflow, always check
whether an existing `concurrency.group` already covers that resource and reuse it — a new,
uniquely-named group only prevents self-collision, not collision with siblings touching the
same backend.

## 2026-07-25 | Reviewer (scheduled agent run) | coloring-book/t-030 | pattern

**Decision:** merged kind_robots PR #950.

**Failure category:** null — real production bug, found and fixed first-pass clean.

**Subject:** t-030 was filed the same day by an ai-art-academy/t-010 roadmap-accuracy
cycle after it spot-checked `GET /api/art/queue/stats` and found 17+ permanently-failed
coloring-book ArtJobs, all failing identically on a seed-out-of-range Prisma error. This
session picked up the filed task directly rather than re-deriving the root cause.

**Detail:**
- Root cause (already correctly diagnosed by the filing cycle): `ArtImage.seed` is a
  32-bit MySQL `Int`, but 14 separate fallback seed generators across
  `server/api/comfy/**`, `server/utils/artJobRetry.ts`, `server/utils/comfyTestClient.ts`,
  and `server/api/art/queue/[id]/edit.post.ts` all produced values up to `10^15` — six
  orders of magnitude past the column's range.
- Fixed all 14 call sites (mechanical `grep -rl` + `sed`, then manually diffed each hunk)
  from `Math.floor(Math.random() * 1_000_000_000_000_000)` to
  `Math.floor(Math.random() * 2_147_483_647)`, plus added a defensive clamp
  (`clampArtImageSeed()`) at the one Prisma write site (`save-generated.post.ts`) as a
  second line of defense.
- While rechecking ai-art-academy/t-010's lane 3 (home-relay health) in the same session,
  incidentally queued job 2276 and found its seed was `25204709996469` — itself an
  out-of-range value generated by the pre-fix code still live on `main` at that moment.
  Good independent confirmation the bug was real and still active, not stale.
- Verified: prettier + eslint clean on all 15 touched files (a handful of pre-existing
  unrelated warnings/errors on 4 files confirmed present on `main` before this change too,
  not introduced by it); full-project `vue-tsc --noEmit` 0 errors. All 7 kind_robots CI
  checks green; merged squash `6de92c3`.
- Restored `prisma/generated/` to its committed state before committing — running
  `npx prisma generate` locally (via `provision_kind_robots_deps.sh`) regenerates several
  checked-in client files with sandbox-local drift unrelated to any source change (the
  same stale-generated-client artifact class documented in this project's and
  ai-art-academy's TALKBACK history); left untouched so the PR diff stayed exactly scoped
  to the seed fix.

**What was good:**
- The filing cycle (ai-art-academy/t-010) did the hard part correctly: read the actual
  source across all affected call sites rather than guessing, confirmed the schema
  constraint directly, and wrote a note precise enough that this session didn't need to
  re-investigate anything before implementing.

**What to improve:**
- None specific this cycle.

**Kaizen task:** deferred — a shared `server/utils/randomSeed.ts` helper would prevent
this exact duplicated-fallback-value bug class from recurring, but 14 near-identical call
sites is already an established pattern in this codebase (matches, e.g., the repeated
`resolveSeed`/`sleep` helper duplication across the same files) and consolidating them is
a larger refactor than this fix's scope — worth doing the next time one of these files is
touched for an unrelated reason, not as a standalone task right now.

## 2026-07-26 | Reviewer → Worker | coloring-book/t-022 | pattern

**Decision:** merged conductor PR #1102 (branch `claude/loving-wright-5a3pvo`).

**Failure category:** null — real production bug, found and fixed first-pass clean.

**What was good:**
- The Python-side fix (`scripts/consume_art_queue.py::resolve_seed()`, clamped to
  `SEED_MAX = 2_147_483_647`) is distinct from the already-merged JS-side fix
  (kind_robots PR #950, 2026-07-25, 14 call sites) for the same underlying `ArtImage.seed`
  32-bit-Int constraint — this session correctly diagnosed it as a separate shared-queue
  script rather than assuming the earlier fix already covered it, and did not duplicate
  that prior work.
- Added a dedicated regression test plus strengthened an existing one to assert the
  upper bound; full conductor suite (531 tests) green before opening the PR. All 24 CI
  checks green at review time.
- Correctly re-armed the recurring task's status; documented the still-open relay-
  throughput backlog (ArtJob 2445, queue depth 147) as a separate, already-tracked soft
  gate rather than conflating it with this fix.

**What to improve:**
- Nothing notable this cycle.

**Kaizen task:** deferred — same reasoning as the 2026-07-25 entry above (a shared
`resolveSeed` helper would prevent this bug class recurring across both the Python queue
scripts and the JS API routes, but consolidating a well-established duplicated pattern
across two languages/repos is a larger refactor than either fix's scope).

## 2026-07-27 | Reviewer → Worker | coloring-book/t-022 | critique

**Decision:** merged (PR #1250, squash 8dd7f6581b1642acc8f13cb6866443b41b4def9e).

**Failure category:** none — clean first-pass merge, no rejection.

**What was good:**
- Scoped exactly to queue-identity integrity: detects duplicate `id`/`slot` entries
  in `color-art-jobs.yaml` (a queue could otherwise look retry-safe while secretly
  carrying two entries claiming the same slot or id) and widens the semantic-gate
  job-id parser to handle both `job 2474` and `Job #2474` formats, which the prior
  parser's `parts[0] == "job"` exact-match would have silently missed (case and
  punctuation both broke it).
- Read-only diagnostic + tests only, matching this task's established convention
  (no ArtJobs submitted/retried/modified) — verified via the diff, not just the PR
  description's claim.
- Regression coverage for all 4 new cases (duplicate entry ids, duplicate slots,
  the widened job-id regex, and the existing duplicate-job-id path continuing to
  work) rather than just the happy path.

**What to improve:**
- Nothing notable this cycle — small, correctly-scoped, well-tested.

**Kaizen task:** deferred — `queue_integrity_safe` and the semantic-gate-id regex
widening are both narrow, already-complete fixes; no obvious follow-on gap this
cycle beyond the long-standing render-backlog issue already tracked elsewhere in
this file.

## 2026-07-28 | Reviewer (conductor scheduled Agent run) | coloring-book/t-022 | critique

**Decision:** merged (PR #1268, squash b873712).

**Failure category:** none — clean first-pass merge, no rejection.

**What was good:**
- Found and fixed a real, previously-unnoticed bug through actual live verification, not
  just unit tests: unlocked color-art entries re-randomize their seed on every `enqueue()`
  call, so a stale `wait_for_job()` timeout is indistinguishable from a genuinely stuck job
  on the next cycle — a plain retry would silently submit a duplicate ArtJob even when the
  original had since completed (8 of 18 Monster Recast blocked entries had this exact
  situation: `DONE` jobs sitting unused behind a stale timeout error).
- Caught its own fix's incompleteness by running `--live` against the real queue instead of
  trusting the first commit's unit tests alone: `build_entries()` dropped
  `semantic_gate_error` from the allowlisted fields it copies onto the working entry, so
  the new recovery branch could never fire in production. This produced one real duplicate
  ArtJob (2715 alongside already-`DONE` 2702) before the gap was found — the Worker caught
  it, added a regression test proving the fix, and reverted the live run's file mutations
  so the queue still names the valid job for the next cycle to recover.
- Honest, specific "not completed this cycle" note: the recovery path is unit-tested but
  unexercised end-to-end because this sandbox has `KR_API_TOKEN` but not
  `ANTHROPIC_API_KEY`, so no live candidate can clear the semantic gate here regardless of
  submission path. Left a clear pointer to what the next cycle (with a real key) should see
  happen (mr-001, mr-005–mr-011 recovered with no duplicate submission).
- All 25 CI checks green (including CodeQL, Python test suite, roadmap validation); diff
  scoped to exactly the fix (`consume_coloring_book_color_art.py`), its regression test,
  and the roadmap note.

**What to improve:**
- The task was left at `status: claimed` rather than `status: review` before the PR was
  opened (the roadmap diff shows the flip to `review` happening inside the same PR, not as
  a separate pre-PR commit) — a minor template-discipline gap per AGENTS.md step 7. Didn't
  affect this review since the PR was still findable directly, but worth the Worker
  double-checking this step goes out ahead of `gh pr create` next time, not bundled into it.

**Kaizen task:** t-031 — audit `consume_art_queue.py` and `consume_art_requests.py` for the
same unlocked-entry duplicate-submission risk on a `wait_for_job()` timeout (both share the
same timeout-message pattern t-022 just fixed for coloring-book).

## 2026-07-28 | Reviewer (conductor scheduled Agent run) | coloring-book/t-022 | pattern

**Decision:** merged (PR #1275, squash f610700).

**Failure category:** none — clean first-pass merge, no rejection.

**What was good:**
- Correctly scoped as read-only: `recovery_batch`/`recovery_actionable` are additive fields
  on the existing diagnostic (`coloring_queue_status.py`), and the PR's own note is explicit
  that no ArtJobs were submitted, retried, mutated, or deleted this cycle — an honest
  boundary for a connector-only run with no `KR_API_TOKEN`/GitHub egress to execute live.
- New regression test (`test_recovery_batch_is_bounded_by_worker_pass_size`) actually proves
  the bounding behavior (3 candidates → batch of 2 at the configured pass size), not just
  that the field exists; existing tests were extended in place rather than duplicated.
- All required checks green; only one non-required in-progress CodeQL
  (javascript-typescript) job was still running at merge time, matching the established
  "don't block on a non-required in-progress check" precedent from prior sweeps.

**What to improve:**
- Nothing specific to this diff — it's a small, well-tested, correctly-scoped diagnostic
  addition.

**Kaizen task:** t-032 — a future cycle with real execution access should actually run the
bounded `recovery_batch` this PR added against the live Monster Recast queue and confirm no
duplicate ArtJob gets submitted for an entry whose original job already completed; consider
wiring `--require-recovery-actionable` into the relevant workflow as a guard once that's
proven out.

## 2026-07-28 | Reviewer (conductor scheduled Agent run) | coloring-book/t-022 | pattern

**Decision:** merged (conductor PR #1312, squash f54d988).

**Failure category:** none — clean first-pass merge, no rejection.

**What was good:**
- Adds a compatibility path (`scripts/adopt_coloring_book_asset.py`, `accept-color`/`accept-bw`
  with an optional exact `source_path`) for legacy/manually-curated Monster Recast images that
  predate the durable ArtJob queue, without inventing fake ArtJob IDs, seeds, or engine provenance
  for them — an honest boundary matching the "adopted" fields it writes (`adopted_color_path`,
  `adopted_color_at`, etc.) staying visibly distinct from a real generated render.
- Path safety is genuinely defended, not just asserted: `safe_source()` strips a matching
  `projects/coloring-book/sets/<book>/` prefix, rejects any other `projects/`-rooted path, rejects
  absolute paths / `:` / `..` components / non-image suffixes, then re-resolves against the book's
  set directory and checks the resolved path is still a descendant before touching the filesystem.
  The event-processor side (`process_coloring_art_events.py::_source_path`) duplicates the same
  checks before a `source_path` field is even accepted from a dropped event file, so a malformed
  event can't reach the adoption script's own check as the only line of defense.
- Test coverage actually exercises the rejection paths (`test_safe_source_rejects_escape_and_external_paths`
  covers `../`, absolute, `kind_robots:`-style, cross-book, and wrong-extension cases), not just the
  happy path — and the adopt_color/adopt_bw tests confirm no `art_image_id`/fake provenance field
  gets written.
- B&W adoption still requires an already-accepted color master and runs the same semantic
  pair-fidelity gate as a generated render, recording a genuine mismatch as terminal `needs_review`
  instead of silently promoting a bad pair or retrying forever.
- All required checks green (Worker PR CI, Security Audit, Process task events).

**What to improve:**
- No roadmap task explicitly tracked this PR (t-022's recurring note covers the general Monster
  Recast production pass but wasn't updated with a pre-PR `status: review` checkpoint before
  `agent/coloring-adopt-existing-assets` opened) — same template-discipline gap noted elsewhere
  this session (media-watchlist/t-013). Didn't block review since the PR was directly findable via
  `mcp__github__list_pull_requests`, but worth a future cycle setting the task status explicitly
  before opening a PR against a recurring task.

**Kaizen task:** deferred — t-032 (execute a live `recovery_batch` pass) and t-031's follow-up
already cover the next concrete Monster Recast production steps; this adoption path is itself
groundwork those tasks can now use once real legacy assets need promoting, no new task needed yet.

**Pattern note:** Second time today (see conductor's root TALKBACK) that `select_role.py`'s direct
`api.github.com` calls 403'd in this sandbox and under-reported open PRs (`candidate_reviewable_pr_count: 0`
for both conductor and kind_robots) while the session's own `mcp__github__list_pull_requests` found two
real ones immediately. Treating MCP results as authoritative over `select_role.py`'s
`github_api_unreachable: true` output continues to be the right call every time this has come up.

---
_Generated by [Claude Code](https://claude.ai/code)_

## 2026-07-28 | Reviewer (conductor scheduled Agent run) | coloring-book/t-033 | pattern

**Decision:** merged (conductor PR #1322, squash 7a96b11). Retroactively logged as `t-033`
in the roadmap (the PR had no tracked task) and filed `t-034` as a soft `needs-human` for
Silas to pick a printer/trim/binding.

**Failure category:** none — clean first-pass merge, no rejection.

**What was good:**
- Cleanly separates source-asset readiness (36 final color/BW pairs + final cover) from
  print-layout readiness (trim/bleed/binding/paper/etc., all left explicitly `null`, not
  guessed) from export readiness (interior PDF / cover-wrap PDF / source archive existence).
  Does not assume 8.5x11 or crop the current 1024x1536 source images to a physical trim —
  states that boundary explicitly in the manifest's own `notes:`.
- `scripts/coloring_book_package_status.py` writes an ordered-by-slot interior manifest per
  book and is covered by 4 unit tests exercising every state transition (source-production →
  layout-needed → exports-needed → package-ready), including a missing-slot/missing-cover
  case. All required checks green (Worker PR CI).
- Nothing published, no spend, no POD account/listing — purely internal tooling and state,
  consistent with the project's `notes_from_silas` boundary.

**What to improve:**
- Same template-discipline gap flagged on t-022's PR: this PR opened from a branch outside
  the `worker/*`/`claude/*` claim flow (`agent/coloring-print-package-manifest`) with no
  roadmap task claimed beforehand, so it wasn't discoverable via roadmap state — only via
  `mcp__github__list_pull_requests`. This is now the second occurrence in the same project
  in one day; worth a session actually enforcing "claim before implementing" if a third
  instance shows up.

**Kaizen task:** t-034 (already filed as this task's own soft needs-human, doubling as the
kaizen follow-up) — wire the print-package.yaml layout fields once Silas picks a printer.
No separate kaizen task needed.

**Pattern note:** Second same-day, same-project instance of a merged PR with no prior
roadmap task (see t-022's entry above). Not yet worth a process-enforcement task, but a
third occurrence this week should prompt one.

---
_Generated by [Claude Code](https://claude.ai/code)_

## 2026-07-28 | Reviewer (conductor Agent run) | coloring-book/t-032 | pattern

**Decision:** merged (conductor PR #1327, squash f49ea1d). Task flipped to `done`.

**Failure category:** none — clean first-pass merge, no rejection. Worth recording anyway:
a live run against the real queue turned up a genuine bug before it reached `main`.

**What was good:**
- t-032's own note (from a prior session) had left an exact, checkable precondition for
  when this task would become actionable (`recovery_actionable: true` with a non-empty
  `recovery_batch`). This session confirmed the precondition, then executed exactly the
  two remaining steps the note specified — no scope drift.
- Before running `--live` against the queue, recognized that a plain `--limit` would sweep
  in 14 unrelated `fresh_submission_blocked` entries alongside the 4 real recovery
  candidates and risk fresh (duplicate-prone) submissions for entries this task was never
  scoped to touch. Added a minimal `--ids` filter instead of forcing the existing `--limit`
  shape to do something it wasn't built for.
- Caught its own mistake before it reached `main`: the first live run silently overwrote
  the recoverable `job N timed out` reference on all 4 entries with a "missing
  ANTHROPIC_API_KEY" message (this sandbox has no semantic-gate credential either), which
  would have quietly reintroduced the exact duplicate-ArtJob risk `recover_timed_out_job()`
  was built to prevent, on the very next credentialed cycle. Reverted the mutation
  (`git checkout -- color-art-jobs.yaml`, removed the stray webp files) *before* committing,
  root-caused it, fixed the actual bug (preserve the job reference on this specific failure
  mode), added two regression tests, and re-ran live to confirm the fix — rather than
  either committing the silent regression or giving up after the first failed attempt.
- Full local pytest suite (699 passed, 1 skipped) run both before and after the fix; PR
  CI all green before merge.

**What to improve:**
- Nothing specific this cycle — the self-caught bug is exactly the kind of thing "run it
  live and actually look at the diff before committing" is for, and it worked as intended.

**Kaizen task:** t-035 — the 14 `fresh_submission_blocked` entries have the same
underlying gap on the *other* branch of the loop (a fresh `enqueue()`'s new ArtJob id is
never recorded on a missing-credential failure, so it can never be recovered either) —
worth closing that gap too now that the recovery-side fix exists as a template.

---

## 2026-07-28 | Reviewer (conductor scheduled burst rotation) | coloring-book/t-022 | security-flag

**Decision:** did not claim/implement — diagnosed a real production infra blocker instead,
then rotated to a different project per this cycle's "note the blocker, move to next
project" instruction rather than burn cycles retrying a wall the code side can't fix.

**Subject:** the real GitHub Actions repo secret `ANTHROPIC_API_KEY` appears to be unset
(or empty) in `silasfelinus/conductor`'s Actions secrets — this is distinct from, and more
serious than, the already-documented "this Claude Code sandbox has no semantic-gate
credential" limitation noted elsewhere in this file (t-031/t-032 entries).

**Detail:**
- `projects/coloring-book/color-art-jobs.yaml`'s 18 `semantic_gate_error` entries for
  Monster Recast (slots mr-001, mr-005, mr-006, mr-007, mr-008, mr-009, mr-010, mr-011,
  mr-012, mr-013, ...) all carry the message `ANTHROPIC_API_KEY is required for the
  production semantic art gate` (source: `scripts/semantic_art_quality.py` line ~60-63).
- These are NOT stale/local-sandbox artifacts. Commits `5fbbbee` (2026-07-28T11:37:16Z) and
  `ae5b9fd` (2026-07-28T13:31:45Z), both `art: advance semantically reviewed coloring-book
  batch [skip ci]`, are authored by `conductor-bot` — the real GitHub Actions identity used
  by `.github/workflows/monster-recast-art-jobs.yml` / `process-color-art-events.yml`, both
  of which explicitly wire `ANTHROPIC_API_KEY: ${{ secrets.ANTHROPIC_API_KEY }}` into their
  env. Diffing the two commits shows only `semantic_gate_error_at` timestamps advancing by
  ~2h47m (10:15→13:02, 10:19→13:05, etc.) with the identical error message — i.e. the real,
  credentialed production workflow is re-running against the same 18 entries on schedule and
  hitting the same missing-key error every time, not a one-off blip.
- This is very likely the actual root cause behind a large share of the "0/36 final pairs
  despite dozens of burst-mode cycles" pattern this task's own note history documents: 18 of
  33 pending Monster Recast slots (>50%) cannot pass the semantic gate no matter how many
  times the workflow or a future agent retries submission, because the credential the gate
  requires isn't reaching the job.
- Blast radius: `scripts/semantic_art_quality.py` is also imported by
  `curate_art.py`/`curate_art_jobs.py` (ai-art-academy / digital-storefront art curation)
  and `challenge_runner.py`/`challenge_matchup.py` (challenge-center). A `git log --all
  --since=2026-07-27 --grep=semantic -i` this cycle showed no other project's data files
  currently carrying this exact error, so no other project appears actively blocked by it
  right now — but any of them could hit the identical wall the next time their own
  semantic-gated pipeline runs.
- Per hard rule 5 (no agent may touch secrets), no agent — Worker or Reviewer — can fix this
  directly. It needs Silas to verify/add the `ANTHROPIC_API_KEY` secret in
  `silasfelinus/conductor`'s GitHub repo settings (Settings → Secrets and variables →
  Actions).

**Suggested action:** FOR SILAS — check whether `ANTHROPIC_API_KEY` is actually present and
non-empty in the conductor repo's Actions secrets; if it was rotated/removed/expired,
re-add it. Once fixed, no roadmap change is needed — the existing hourly workflow will pick
the 18 stuck slots back up on its own next run (they're still `status: pending`, not stuck
in a terminal-failure state). Left `coloring-book/t-022` at `status: ready` (not
`needs-human`) since this is a workflow-secrets problem, not a task-spec problem, and the
other 15 pending-without-error slots may still be genuinely actionable by a future cycle;
did not want to hide those behind a project-wide gate. Future cycles: read this entry before
retrying live submission against the 18 flagged slots — it will fail identically until the
secret is fixed.

---
_Generated by [Claude Code](https://claude.ai/code)_

## 2026-07-28 | Reviewer (conductor scheduled Agent run) | coloring-book/t-022 | pattern

**Decision:** deleted stranded branch `worker/coloring-book-t-022-status-contract-a31r`
(via `branch-janitor.yml` workflow_dispatch `force_delete_branches`, session credentials
403 on direct ref deletion as documented). No PR existed for it.

**Failure category:** none — not a rejection, a duplicate-work cleanup.

**Detail:**
- The branch's actual code diff (`scripts/coloring_queue_status.py` /
  `tests/test_coloring_queue_status.py` — adding `RECOMMENDED_ACTIONS`,
  `requirement_satisfied`, `--require-recommended-action`) is byte-identical to what
  `main` already has via merged PR #1339 (confirmed in `projects/coloring-book/roadmap.yaml`
  line ~422: "Merged Conductor PR #1339 ... --require-recommended-action"). `git diff
  origin/main origin/worker/coloring-book-t-022-status-contract-a31r` on those two files
  is empty.
- Another concurrent session built the identical feature independently under a different
  branch/task label and merged first; this branch was the loser of that race with zero
  remaining unique content — a clean instance of the "Rotation collisions" pattern in
  AGENTS.md, just caught before a redundant PR was opened rather than after.
- `coloring-book/t-036` (the still-open `--require-no-semantic-gate-error` flag task) is
  unrelated and unaffected — confirmed its scope doesn't overlap this branch's content.

**Suggested action:** none needed — roadmap state (`t-022: ready`, `t-036: ready`) already
reflects reality; no task edits required. Flagging here only so a future session doesn't
wonder why a `coloring-book-t-022`-named branch vanished with no corresponding PR.

---
_Generated by [Claude Code](https://claude.ai/code)_

## 2026-07-28 | Reviewer → Worker | coloring-book/t-035 | pattern

**Decision:** merged PR #1346 (squash b23ce46)

**What was good:**
- Correctly generalized t-032's recovery-path fix to the fresh-submission branch of the
  same loop, using the same "job N" stamping convention `referenced_job_id()` already
  parses rather than inventing a new format.
- Careful edge-case handling: `enqueue()` failing outright (no ArtJob created at all)
  correctly leaves the field unstamped, distinct from a completed render that only fails
  `validate_candidate()`.
- Full regression coverage mirroring t-032's existing tests (double-stamp avoidance +
  a `main()`-level integration test), not just a unit test on the helper function alone.
- Verified with the full suite (705 passed) and correctly identified the one red check
  as the already-tracked `conductor/t-090` pre-existing issue, unrelated to this diff.

**What to improve:**
- Nothing specific this cycle.

**Kaizen task:** none new — the PR's own suggestion (coloring-book/t-036,
`--require-no-semantic-gate-error` flag) is already `ready` in this roadmap.

---
_Generated by [Claude Code](https://claude.ai/code)_

## 2026-07-28 | Reviewer (conductor scheduled Agent run) | coloring-book/t-036 | pattern

**Decision:** merged PR #1355 (squash f7a71af).

**What was good:**
- Correctly scoped to the kaizen suggestion from PR #1331 — added
  `credential_gate_errors` / `credential_gate_error_count` plus a
  `--require-no-semantic-gate-error` CLI guard to `coloring_queue_status.py`,
  matching the `ANTHROPIC_API_KEY is required` message specifically rather than
  conflating it with recoverable job-timeout or transient-enqueue
  `semantic_gate_error` entries (which already have their own detection paths).
- Verified against the live `color-art-jobs.yaml` queue, not just synthetic
  fixtures: confirmed `credential_gate_error_count` correctly reports 18 and the
  CLI exits non-zero.
- Two new regression tests distinguishing credential-wall errors from other
  `semantic_gate_error` shapes; full suite green (707 passed, 1 pre-existing
  skip, unrelated conductor/t-090).
- Correctly picked this task over the higher-priority `coloring-book/t-022` this
  cycle: t-022's only live work is blocked on the same missing
  `ANTHROPIC_API_KEY` GitHub Actions secret flagged in this file's 2026-07-28
  security-flag entry, which is still unresolved and needs Silas — retrying it
  again would have just reproduced the same documented outcome.

**What to improve:**
- Nothing specific this cycle.

**Kaizen task:** deferred — the PR's own suggestion (wiring
`--require-no-semantic-gate-error` into `process-color-art-events.yml`'s
pre-flight) is reasonable but only pays off once the underlying secret is fixed;
creating it now would just sit blocked on the same human gate. Revisit once
Silas confirms the `ANTHROPIC_API_KEY` secret is restored.

---
_Generated by [Claude Code](https://claude.ai/code)_

## 2026-07-29 | Reviewer (conductor scheduled Agent run) | coloring-book/t-022 | critique

**Decision:** merged PR #1416 (squash e5fbb4d).

**What was good:**
- Found and root-caused a real live bug while actually running the recovery pass rather
  than reasoning about it in the abstract: the except-block guard in
  `consume_coloring_book_color_art.py` only preserved a stuck job's "job N" reference
  when the failure text literally contained "ANTHROPIC_API_KEY" — any other exception
  (missing Pillow, a transient `Connection reset by peer`) silently destroyed the
  reference, and the PR shows this actually happened live (15 entries lost their
  references, 4 duplicate ArtJobs were submitted before the run was killed).
- Fix is precise: a new `RecoveryAbandoned` exception marks only the three
  backend-confirmed-dead cases (FAILED/CANCELLED, DONE-with-no-artImageId, wrong
  concept); every other exception now preserves the reference unconditionally,
  matching the actual invariant ("job's fate unknown" vs. "job confirmed dead").
  `RecoveryAbandoned` subclasses `RuntimeError` so existing `pytest.raises(RuntimeError)`
  tests keep passing.
- Three well-targeted regression tests: missing-dependency-during-save, network-error
  during status-check, and a control case confirming a genuinely FAILED job still
  clears correctly. Full suite green (773 passed) before opening the PR; CI 25/25 green.
- Honest incident accounting: documented the 4 unintended duplicate ArtJob submissions
  (2829-2832) in the roadmap note as accepted wasted capacity rather than hiding them,
  and confirmed via live `GET /api/art/queue/{id}` that the original 4 jobs (2776-2779)
  were genuinely already DONE before reverting the accidental queue-file mutations.
- Cross-referenced the closely related ai-art-academy/t-010 fauvism-request incident
  (same "reference destroyed → duplicate work" failure shape in a different pipeline)
  in the fix's own comments — good pattern recognition across projects.

**What to improve:**
- The PR left the recurring task's `status:` at `review` instead of flipping it back to
  `ready` before merge, even though its own note says "Re-armed to ready per the
  recurring-task rule" — the note and the actual roadmap field disagreed. Flipped it to
  `ready` myself as part of this review's close-out (small follow-up commit on this
  branch, not a separate PR).
- No "Kaizen suggestion" section in the PR body per the handoff template — substituted
  my own below.

**Kaizen task:** coloring-book/t-037 — migrate t-022's ~28k-character accumulated
RAN/incident note history into a dedicated run-log doc, mirroring the same fix already
filed for ai-art-academy/t-010 (t-054, 2026-07-29). The pattern is identical across both
recurring tasks: incident narrative piles up in the roadmap `note:` field cycle after
cycle with no trimming, making the roadmap file itself harder to parse and diff.

---
_Generated by [Claude Code](https://claude.ai/code)_

## 2026-07-29 | Reviewer → Worker | coloring-book/t-037 | pattern

**Decision:** merged (PR #1435)

**Failure category:** n/a — clean first-pass success

**What was good:**
- Did exactly what its own kaizen note scoped: created `t-022-run-log.md`, moved all
  ~28k characters of accumulated RAN/incident history verbatim (de-indented only),
  trimmed t-022's roadmap note to two short paragraphs plus a `run_log:` pointer,
  mirroring the identical fix already landed for ai-art-academy/t-010 (t-054).
- Verified the extraction was byte-identical before committing, and ran both
  `validate_roadmaps.py` and `audit_roadmaps.py` clean.
- Good rotation-safety judgment: noted in "Flags for Reviewer" that it deliberately
  skipped the top-ranked `ready_task` (ai-art-academy/t-010, claimed by a concurrent
  session moments earlier) and the next one (coloring-book/t-022 itself — a live
  production task with an open credential blocker and a history of concurrent-session
  collisions), picking this fully self-contained task instead rather than touching
  either blind in an unattended cycle.

**What to improve:**
- None this cycle — clean, scoped, well-verified.

**Merge conflict note:** the PR went stale (`mergeable_state: dirty`) against `main`
between opening and review, purely from the routine `STATUS.md`/`workspace.html`/
`ROADMAP-AUDIT.*` auto-refresh commits landing in between (per hard rule 9 / the
"Reviewer batch-merge note"). Resolved by merging `origin/main` into the PR branch,
taking main's copy of `ROADMAP-AUDIT.*` and regenerating via `audit_roadmaps.py`, then
verifying `git diff origin/main...HEAD --stat` showed only the four files t-037 actually
touched before pushing and merging. No worker action needed — flagging only as a
pattern note since this is now a recurring race (see conductor's own
"Reviewer batch-merge note" in AGENTS.md).

**Kaizen task:** none new this cycle — the note-bloat fix pattern (t-022/t-054-style
run-log extraction) has now been applied to both projects that had it; no further
instances currently known in this project's roadmap.

---
_Generated by [Claude Code](https://claude.ai/code)_

## 2026-08-01 | Reviewer (conductor scheduled agent run) | coloring-book/t-022 | critique

type: critique

**Decision:** merged (PR #1486) — found and fixed a real bug in the recovery-loop
bookkeeping while working the recurring production-pass task; re-armed to `ready`
(PR #1487).

**Failure category:** quality (the underlying bug, not this session's own work) —
`record_semantic_rejection()` never cleared the stale `semantic_gate_error` breadcrumb
once a recovered job's image received a genuine (non-credential) semantic verdict.

**What was good:**
- The 04:14Z hourly workflow run's own logs made the bug directly observable: mr-001/
  mr-005/mr-006 were re-judged against the exact same `art_image_id` they had already
  failed on once before, rather than getting a fresh render attempt.
- `coloring_queue_status.py --book monster-recast`'s `recommended_action` output was
  the fastest way to confirm the fix worked live (`recover-existing-jobs` →
  `submit-next-batch`, `credential_gate_error_count` 13 → 0) without needing to run
  anything against the real render backend from this sandbox.

**What to improve:**
- None this cycle from a prior Worker — this was root-caused directly from live
  workflow logs plus the code, not from a rejected PR.

**Kaizen task:** created as a note in PR #1486's description rather than a new
roadmap task this cycle (recurring-task PRs don't get a fresh kaizen task per run;
folding the suggestion — a consistency check between `semantic_gate_error` and
`semantic_rejections` history — into the next real implementation task on this
project instead of adding roadmap noise for a one-line idea).

---
_Generated by [Claude Code](https://claude.ai/code)_

## 2026-08-01 | Worker (conductor scheduled agent run) | system | coloring-book/t-022 | pattern

type: pattern

**Subject:** With no local `ANTHROPIC_API_KEY`, the highest-leverage action on a recurring
art-production task is reading the semantic gate's own rejection reasons and revising prompts
accordingly, rather than treating "no credential" as a dead end for the cycle.

**Detail:**
- Found 13 Monster Recast entries stuck at `needs_review` (3/3 attempts exhausted, scores
  22-62 vs. threshold 75). Rather than re-arming to `ready` as a no-op (the pattern several
  prior cycles on this task fell back to when blocked on credentials), read each entry's full
  `semantic_rejections` history directly from `color-art-jobs.yaml` and revised the
  corresponding prompt in `art-modeler-request.yaml` to front-load the exact attribute the
  gate said was missing.
- The gate's rejection reasons are unusually well-structured for this: they name the specific
  missing/wrong element in plain language (e.g. "no visible heavy musculature... the required
  dramatic action... is absent"). Mining that text directly into the next prompt revision is
  fast and precise compared to guessing what went wrong from the image alone.
- Reset the 13 entries' `status`/`semantic_attempts` with a targeted line-level script edit
  instead of a full `yaml.safe_dump` round-trip — the naive dump approach was tried first and
  produced a 579-line diff (pure re-wrapping, zero content change) before being reverted in
  favor of the surgical approach. Worth remembering for any future queue-metadata edit on this
  file: `safe_dump` unwraps/rewraps every folded scalar in the file, not just the touched entry.
- Unverified until the next hourly workflow run (with real ANTHROPIC_API_KEY) actually
  processes the batch — flagged explicitly in the PR body so the next cycle checks fresh
  rejection reasons rather than assuming the rewrites worked.

**Suggested action:** if this pattern (revise-from-rejection-reasons) proves effective once
verified against a live run, it's a reusable playbook for the other two books in this project
(Hollywood Recast, and book 3 once queued) — worth capturing as a short note in
`t-022-run-log.md` or a project doc once there's a confirmed before/after result to point to,
rather than re-deriving the approach from scratch each time a batch stalls at `needs_review`.

---
_Generated by [Claude Code](https://claude.ai/code)_

## 2026-08-05 | Agent run (scheduled conductor sweep) → Reviewer | coloring-book/t-022 | pattern

type: pattern

**Subject:** Reclaimed a 4-day abandoned stale claim on `t-022` (recurring task) that `check_pr_merged_drift.py` flagged this cycle; re-armed to `ready` rather than attempting a live run.

**Detail:**
- The prior claim (`claude-scheduled-20260801T092747Z-cb-t022`, claimed 2026-08-01T09:27:47Z) had no follow-up PR ever opened — confirmed via GitHub MCP search across all `coloring-book/t-022` PR history, nothing after the 07:42Z re-arm that preceded it. Sat past `CLAIM_TTL_MINUTES` (90 min) for over 4 days with no session picking it back up until this sweep.
- Confirmed the queue is currently blocked by the same production ComfyUI render-relay outage already tracked in root `RENDER-BACKLOG.md` (oldestPending ~96.2h and growing per this cycle's `recheck_render_queue.py` reading, 25/25 recent failures connection-refused) — not something a recovery pass would clear right now. Per Failure-triage this is **transient**, so no pass consumed; re-armed to `ready` with an updated note rather than left stranded at `claimed`.
- Full detail in `projects/coloring-book/t-022-run-log.md`'s 2026-08-05T22:37Z entry.

**Suggested action:** none new — the standing render-relay incident is already escalated to Silas repeatedly (hands-on relay access needed, outside agent reach). Worth noting as a pattern: a recurring task's claim can go stale silently for days with no automated re-surfacing beyond a session happening to run `check_pr_merged_drift.py` — that script earning its "run every session start" spot in CLAUDE.md is exactly why this got caught today.

---
_Generated by [Claude Code](https://claude.ai/code)_

## 2026-08-10 | Agent run (scheduled conductor sweep) | coloring-book/t-022 | pattern

type: pattern

**Subject:** Recovered all 8 remaining Monster Recast color-proposal ArtJobs after a missing-Pillow sandbox gap masked that they'd already finished rendering; Monster Recast's color stage (36/36) is now fully drained.

**Detail:**
- Checked `coloring_queue_status.py --book monster-recast` before touching anything (per the 2026-08-09T11:50Z entry's standing guidance): `recovery_actionable`, `recovery_safe: true`, no automated cron run since 2026-08-09T11:44Z. Ran a recovery pass (not a fresh submission) against the same 8 `recovery_batch` entries every recheck since 2026-08-09T16:16Z had found still queued/running.
- First attempt (`--timeout 60`) hit `RECOVERY UNVERIFIED ... Pillow is required for WebP output` on 6/8 — this sandbox had no Pillow installed (the same recurring gap several ai-art-academy cycles have hit and fixed). Confirmed the except-block fix from an earlier t-022 cycle correctly preserved all 6 job references this time (0 lost, 0 duplicates) rather than repeating the original data-loss bug.
- Installed Pillow and re-ran the identical pass: all 8 had actually already finished rendering server-side and recovered cleanly (ArtImage ids 17137-17144), 0 duplicate submissions. Visually inspected the highest-risk render (a 3-figure group scene) — clean, on-brief, no artifacts.
- `coloring_queue_status.py` after: `{done: 33, approved: 3, pending: 0}`, `recommended_action: complete`. Did not start a fresh Hollywood Recast batch — left for the daily cron (next run 2026-08-10T11:00Z) per the corrected guidance the 2026-08-09T11:40Z/11:50Z entries already established, to avoid repeating that submit/submit collision.
- Verified: `validate_roadmaps.py` clean, `git diff --stat` reviewed before committing (1 YAML file + 8 new binaries, nothing else touched).

**Suggested action:** none new — this is a straightforward instance of the already-documented missing-Pillow gap and the already-documented cron-collision-avoidance guidance, both working as intended this cycle.

---
_Generated by [Claude Code](https://claude.ai/code)_

## 2026-08-10 | Agent run (scheduled conductor sweep) | coloring-book/t-022 | pattern

type: pattern

**Subject:** Recovered 6 stuck Hollywood Recast color-proposal jobs and fixed 1 blocked prompt (format-vocabulary rule) in the same cycle; filed t-038 to stop the recurring Pillow gap from costing a wasted attempt every cycle.

**Detail:**
- `coloring_queue_status.py --book hollywood-recast` showed the daily `monster-recast-art-jobs.yml` cron had advanced Hollywood Recast to `{done: 11, pending: 25}` since the prior t-022 cycle, with 6 `recovery_batch` entries stuck on 600s ComfyUI timeouts and 1 `fresh_submission_blocked` entry (hwr-014) rejected by the live art-prompt contract's `format-vocabulary` rule.
- Recovery pass on the 6 stuck ids hit the same recurring "Pillow is required for WebP output" gap logged at least twice before (2026-07-27, 2026-08-10T02:29Z) — the existing except-block guard preserved all 6 job references correctly (0 lost, 0 duplicates) before a `pip install --user Pillow` + re-run landed all 6 cleanly.
- hwr-014's prompt opened with "Night highway action poster featuring..." — a bare "poster" trips the contract's format-vocabulary rule (physical-format request, not exempted by a following "composition/framing/layout/crop"). Reworded to "...action scene featuring..." matching this set's own house style (hwr-013's "portrait of..." uses the same noun-substitution shape), then verified the fix against the live server by resubmitting rather than trusting a local read — ArtJob 8190 queued, no 422.
- Filed `coloring-book/t-038` (kaizen, `stakes: reversible`) to bake the Pillow install into `provision_kind_robots_deps.sh` or an equivalent step, since this is now a 3rd occurrence of the identical failure-then-recover pattern and each occurrence costs a full wasted attempt before the fix is rediscovered.

**What was good:** verifying the prompt-contract fix against the live server (a real resubmission) rather than stopping at a local regex read — the error message's generic "describe the subject and aspect ratio instead" advice could have led to an over-broad rewrite; the minimal single-word substitution was enough, and only the live acceptance actually proves that.

**Suggested action:** t-038 as filed — small, reversible, no live-service impact, safe for a future worker cycle to pick up directly.

---
_Generated by [Claude Code](https://claude.ai/code/session_01G6nMgPQ2YjsGfhv3c4zNxc)_
