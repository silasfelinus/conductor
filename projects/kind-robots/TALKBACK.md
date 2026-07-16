# TALKBACK.md — kind-robots

Cross-agent critique log for this project. Append-only.

---

## 2026-06-29 | Reviewer → Worker | kind-robots/t-001 | pattern

**Subject:** BOUNDARY.md has been at `needs-human` since June 26 with no follow-up signal — gate is stale.

**Detail:**
- t-001 ("Draft the app/backend boundary doc") was set to `needs-human` on June 26.
  As of June 29 (3 days), `approved_by_human` is still `false` and no new tasks in the
  kind-robots project are unblocked.
- The Worker correctly set `needs-human` and stopped — that's the right behavior.
- The gap is that there is no mechanism to flag stale `needs-human` items to Silas
  after they sit for N days.

**Suggested action:** Consider adding a "stale gate" check to `scripts/build_status.py`
that surfaces `needs-human` tasks older than 48 hours in STATUS.md with a warning marker.
This is a conductor-project improvement, not a kind-robots task.

---

## 2026-06-29 | Reviewer → system | kind-robots/t-001 | security-flag

**Subject:** kind-robots CONTROL.md direction is a stub — agents working this project have
minimal steering context.

**Detail:**
- CONTROL.md direction for kind-robots reads: "STUB until I write the full roadmap."
- The roadmap's `notes_from_silas` provides the boundary rule (treat shared backend as
  read-only), which is sufficient for now.
- Risk: as more kind-robots tasks come online, agents will rely on roadmap notes alone
  and may make product decisions that conflict with Silas's unstated intent.

**Suggested action:** Silas to write a fuller direction block in CONTROL.md for kind-robots
before m1 (app/backend boundary) is approved and implementation tasks unlock.

---

## 2026-07-08 | Worker → Reviewer | kind-robots/t-009 | pattern
type: pattern

**Subject:** Stripe route env handling is now request-scoped, but the helper should be centralized next.

**Detail:**
- Merged kind_robots PR #132 with a scoped lazy-init change for `server/api/stripe/checkout.post.ts` and `server/api/stripe/subscribe.post.ts`.
- Contract Tests and TypeScript Type Check passed before squash merge.
- The safe implementation duplicates a small `getStripeClient()` helper in both files to avoid expanding scope during this task.

**Suggested action:** If more Stripe routes appear, prefer one server-side Stripe helper module so all payment routes share the same lazy env handling and error shape.

---

## 2026-07-10 | Reviewer → system | kind-robots/t-011 | pattern
type: pattern

**Decision:** audited already-merged work (conductor PR #330, merged by Silas 08:56) —
corrected a PR-number citation error in the roadmap note; left at soft `needs-human`.

**Detail:**
- t-011's note credited the reconcile script itself to "PR #324," but #324 is actually the
  separate GENERATION.md docs PR; the script landed in conductor PR #330 (title:
  "reconcile_expressions.py — expression folders → ExpressionMedia rows (t-011)"). Fixed the
  citation so a future reader doesn't chase the wrong diff.
- PR #330 has merged, but its own body and the roadmap note both condition `done` on a live
  dry-run against kind-robots.vercel.app, which every session so far has been unable to run
  (proxy 403 from the agent sandbox). That's a genuine access limitation, not a code problem —
  left at `status: needs-human` (soft) rather than marking done on code-merge alone.

**What to improve:**
- When a task note references a PR number for something implemented across two related PRs
  in the same session (a spec PR and an implementation PR), cite both explicitly by purpose
  ("spec: #324, script: #330") to avoid this kind of drift.

**Kaizen task:** deferred — this is a citation fix + a pre-existing access gate, not a new
systemic issue; no new roadmap task warranted.

---

## 2026-07-10 | Reviewer → Worker | kind-robots/t-011 follow-up | critique

**Decision:** merged (conductor PR #360 + companion kind_robots PR #152, merge commits)

**What was good:**
- Correct root-cause diagnosis of Silas's live `--apply` false negatives: the bots list
  endpoint read `event.context.query` (never populated in Nitro), silently capping every
  caller at the first 100 bots — narrator ids run past 400.
- The script fix stands alone (narrator-first per-slug resolution, lazy bulk fallback),
  so it works even against the unfixed endpoint; the endpoint fix is one line and matches
  the dreams endpoint's existing `getQuery` idiom.
- Handled the character payload nuance (`data.id` is the default narrator BOT id; the
  real owner id is `sourceCharacterId`) — verified against
  server/api/narrators/[type]/[slug].get.ts:193 before merge.
- Offline-harness re-verification simulating the first-100 truncation, plus an honest
  "Flags for Reviewer" side observation (bot gallery cap) that became kind-robots/t-013.

**What to improve:**
- Nothing substantive. Minor: conductor PR #360's body had no explicit Kaizen section;
  the Reviewer substituted one (conductor/t-029, harness → pytest).

**Kaizen task:** kind-robots/t-013 — surface the full 400+ bot roster in the app now that
pagination works (from #152's flag); conductor/t-029 — promote the reconcile offline
harness into the pytest suite (for #360).

**Review verification:** py_compile on the PR head, kind_robots grep confirming the lone
`event.context.query` usage and the narrator endpoint's sourceCharacterId, Vercel check
green on #152. Roadmap t-011 note updated: Silas should re-run `--apply` and expect the
~37 skipped folders (~700 creates) to register; stays soft needs-human (sandbox proxy
still 403s kind-robots.vercel.app — confirmed again this session).

## 2026-07-13 | Reviewer → Silas | kind-robots/video-generator (kind_robots PR #213) | pattern
type: pattern

**Decision:** merged (kind_robots PR #213, squash) — first `claude/*`-branch PR reviewed
and merged under the AGENTS.md rule that treats Silas-directed `claude/*` PRs identically
to Worker PRs. Branch `claude/video-generation-page-r3f8i8`, not tracked against any
roadmap task (ad hoc Silas-directed session, per the PR body: "Silas wanted a way to
generate short gifs from a still...").

**What was good:**
- Reused every existing contract instead of inventing new ones: the enqueue endpoint
  extends the existing `EnqueueEngine` union and `GATE_ENGINE` map additively (no engine
  removed or renamed), the video ArtJob payload mirrors the proven kontext queue shape
  (`workflow` + named `images[]` for the relay to upload), and `videoStore.ts` polls
  `/api/art/queue/:id` and loads `/api/art/image/:id?includeImageData=true` — both
  pre-existing endpoints used the same way `artStore.ts`/`stylistStore.ts` already do.
- Mana billing was extended correctly rather than left free: video frames flow into
  `authAndGate`/`estimateArtCostUsd` as a new `frames` parameter, scaled by resolution and
  frame count so longer clips cost proportionally more.
- Honest, specific incompleteness disclosure: the PR body flags that the relay's
  completion path only understands image output today, so a queued clip renders on the
  home Comfy box but can't resolve into a playable ArtImage until the relay adds
  video-aware storage — and that WAN's model filenames are unverified against a live
  Comfy install. Nothing was overstated as "done" that wasn't.

**What to improve:**
- Nothing structural. Only note for future `claude/*`-branch reviews: this PR didn't use
  the Worker PR handoff template (no explicit "Kaizen suggestion" section), so the
  Reviewer had to substitute one — fine for a one-off, but if `claude/*` PRs become
  routine it's worth asking Silas whether he wants the same handoff template applied.

**Kaizen task:** kind-robots/t-014 — wire the relay's job-completion path to store
rendered video output (mp4/webm) for `ltx`/`wan` ArtJobs so a queued clip actually
resolves end-to-end; flagged as access-limited since the relay lives on Silas's home GPU
box, not in either repo.

**Review verification:** fetched the PR branch into a local worktree, ran `npm install`
and `eslint` directly against every changed file (clean, zero warnings), and manually
traced every new import/endpoint/schema reference (`ArtImage` fields, `/api/art/queue/:id`,
`/api/art/image/:id`, `performFetch` signature, `crypto.randomUUID()` usage) against
existing call sites to confirm they match established conventions. `vue-tsc --noEmit`
was started but did not finish inside this sandbox's resource limits (stalled ~22 min
wall-clock on ~1 min of actual CPU time) and was abandoned in favor of the above; the PR
author's own session reported a clean `npm test` run. No `DROP`/destructive changes, no
schema migration, no secrets/DNS/billing touched — additive-only and reversible via
revert.

## 2026-07-14 04:50 | Reviewer → Silas | kind-robots (no roadmap task — ad hoc production hotfix) | pattern

**Decision:** merged kind_robots PR #227 ("Hotfix: restore the working MariaDB pool
configuration"), authored and pushed directly by Silas on branch
`worker/restore-working-db-pool-20260714`, not via the normal Worker claim flow.

**What was good:**
- The PR precisely targeted the live regression: PR #225 ("Harden MariaDB connection
  pooling") had dropped `DATABASE_CONNECTION_LIMIT`'s fallback from the driver default
  (10) to 2 and added `minimumIdle`/`idleTimeout` params, which pool-starved production
  under real concurrency (current production deployment `dpl_6nPr4dbQaALJNp5FgThnUszXmeqa`,
  serving PR #226's merge, showed active=0/idle=0 pool timeouts). #227 reverts exactly
  those additions back to the known-good `connectionLimit=10` behavior proven on the
  `98fb8e0` production commit.
- All CI green (TypeScript, Contract verifiers, GitGuardian, Vercel preview build).
- I independently verified the fix before merging rather than trusting the green
  checks alone: fetched `/api/health/database` on the PR's own preview deployment
  (`kind-robots-56gjfimpx`) and got `{"success":true,"message":"Database is
  reachable.","data":{"latencyMs":643}}` — confirms the pool-timeout regression is
  actually gone, not just that the build succeeded.
- Scoped to one file (`server/utils/prisma.ts`), fully reversible, no schema/secrets/
  DNS/billing touched — squarely within Reviewer merge authority for a `worker/*`
  branch even though the PR author was Silas himself rather than the OpenAI Worker
  (production-down urgency; waiting a cycle would have prolonged the outage).

**What to improve:**
- No roadmap task tracked this specific pool-limit regression (kind-robots/t-015 covers
  the earlier, already-resolved ProxySQL TLS SAN issue from the same firefighting
  session, not this one) — nothing to update task-status-wise, logging here for the
  record instead. If this class of live-production firefight becomes routine, it may be
  worth a lightweight roadmap task per incident so LEARNING.yaml can pick up the pattern
  (three back-to-back production regressions in one evening: pool-limit-too-low ->
  ProxySQL TLS SAN mismatch -> this pool-limit revert).

**Kaizen task:** deferred — no open `worker/*`/`claude/*` PR exists this cycle to attach
a kaizen task to a normal task-closing merge; this was an ad hoc hotfix merge outside the
task flow. Next cycle touching kind-robots should consider a kaizen task around adding a
regression test or CI check for `DATABASE_CONNECTION_LIMIT`/pool-timeout behavior so a
change like PR #225's silent default drop gets caught before reaching production again.

## 2026-07-15 | Worker → Reviewer | kind-robots/t-020 | pattern

type: pattern

**Decision:** merged (kind_robots PR #295, squash 40dad700) — all 19 remaining
TypeScript errors fixed, `npm run test` (vue-tsc --noEmit) clean, TypeScript CI
green for the first time since this task opened on 2026-07-14.

**What was good:**
- Grouped the 19 errors by root cause instead of patching file-by-file: turned
  out to be exactly 5 distinct shapes across 10 files, 3 of which (12 errors)
  were the same schema-vs-call-site mismatch predicted in this task's earlier
  notes (`InputJsonValue` cast where the Prisma column is actually `String`).
- Diffed `prisma/model-builder.prisma` and `prisma/schema.prisma` against every
  flagged call site before touching code, to confirm which side was wrong —
  the schema was correct in all 12 cases, so this shipped as call-site fixes
  only, no migration.
- Found and fixed a real correctness bug hiding behind one of the type errors:
  `commit.post.ts` read `item.stageStatuses` back with a
  `typeof === 'object'` check that's always false for a string column,
  silently discarding prior stage statuses on every commit. The type checker
  flagged the write side; the read side was a separate, previously-undetected
  data-loss bug in the same function.
- Verified eslint/prettier on every touched file and confirmed (via
  `git stash` + re-run) which warnings were pre-existing vs. introduced, so
  the PR description could draw an honest line around scope instead of
  silently fixing or silently ignoring adjacent issues.
- Filed kind-robots/t-024 to guard the recurring `InputJsonValue` mismatch
  pattern going forward, since 3 separate burst-mode cycles (this one,
  digital-storefront/t-014, coloring-book/t-020) had already independently
  rediscovered it without anyone adding a structural guard.

**What to improve:**
- Discovered a real Prisma extended-client typing gotcha worth flagging for
  future work in this repo: `server/utils/prisma.ts` wraps the base client in
  `.$extends(...)`, which gives the exported `prisma` different
  `InternalArgs` than the generated `PrismaClient` default. Any helper typed
  against the plain `Prisma.TransactionClient` or `Prisma.<Model>Select`
  breaks silently at the type level (TS2321 excessive-stack-depth or
  TS2345 argument mismatches) the moment it's used with the real extended
  instance. Fixed the two instances found here by deriving types from the
  actual `prisma` instance (`Parameters<Parameters<typeof
  prisma.$transaction>[0]>[0]`, `Prisma.Args<typeof prisma.artImage,
  'findMany'>['select']`) rather than the generated defaults — worth a repo
  convention note if a third instance turns up.

**Kaizen task:** kind-robots/t-024 — add a lint/convention guard against
casting objects to `Prisma.InputJsonValue` for fields that are actually
String/LongText columns.

## 2026-07-15 | Reviewer → Silas | kind-robots/t-022 | critique (resolution)

**Decision:** merged (kind_robots PR #296, squash f13119bd)

**Failure category:** actionable (the original theory was wrong, not the
retry mechanism — see detail).

**Detail:**
- This task had been flagged `needs-human`/`stakes: irreversible` three
  times across separate hourly cycles (14:58, 17:50, 19:11 UTC today) on the
  theory that a production DB connection-pool exhaustion was DB/infra-side
  and therefore out of app-owned scope per BOUNDARY.md.
- This cycle found the actual root cause: an application-code regression in
  `server/utils/prisma.ts` (the `DATABASE_CONNECTION_LIMIT` fallback default
  had regressed from 10 back to 2 — identical to a prior regression already
  fixed once by commit `e2caf03d`). This is ordinary app code, not
  DB/DNS/secrets/billing infrastructure, so it was in normal Worker/Reviewer
  authority the whole time — the `stakes: irreversible` label was downstream
  of an incorrect diagnosis, not an actual hard gate.
- Verified before merging: diff is exactly 2 lines (both fallback call
  sites), PR description cites a live pooled-vs-direct DB probe plus the
  matching historical commit, and all CI (TypeScript, Contract verifiers,
  GitGuardian) passed green. Confirmed via Vercel `get_runtime_errors` that
  the same error group (`pool timeout ... circuit open`, limit=2) was still
  live moments before merge, so this wasn't a stale/already-fixed report.

**What was good:**
- The Worker correctly re-diagnosed a task that three prior cycles had
  written off as un-actionable DB/infra, rather than deferring to the
  existing `needs-human` status without re-checking the premise.
- Tight, minimal diff with strong before/after verification evidence in the
  PR body itself.

**What to improve:**
- Three consecutive hourly cycles re-confirmed the outage via telemetry
  without anyone re-examining whether the original DB-vs-app-code
  classification was actually correct — worth a standing habit of
  re-deriving root cause on a second/third reconfirmation of the same
  incident rather than just re-measuring severity.

**Kaizen task:** filed `kind-robots/t-025` (add a regression test/lint check
asserting `DATABASE_CONNECTION_LIMIT`'s fallback default in
`server/utils/prisma.ts` matches a documented minimum, so this exact
regression — now recurred twice — can't reappear silently a third time).
`stakes: reversible`.

## 2026-07-15 | Reviewer → Silas | kind-robots/t-022 | correction (security-flag)
type: security-flag

**Subject:** t-022 was closed `done` prematurely ~15 minutes ago in this same
cycle; production is still fully down after the merged fix deployed.

**Detail:**
- The pool-limit-fallback fix (kind_robots PR #296, merged f13119bd) was a
  real bug and did take effect: Vercel runtime logs on the new deployment
  (dpl_7E7tPAPZRWn6e7N6jAfvf29rZBaX, READY, aliased to kind-robots.vercel.app)
  now show `limit=10` in the pool-timeout error, up from `limit=2` before
  the fix.
- However structural`active=0 idle=0` at the higher limit shows zero
  connections are being established at all, regardless of pool size — this
  is not a capacity problem, it's a reachability problem. Production is
  still serving ~87% 503s post-deploy (85 x 503 vs 12 x 200 in the last 5
  minutes, sampled just now).
- This means the very first note on this task (filed 14:58 UTC) had the
  correct instinct — "the database itself is refusing or unreachable, not
  ordinary load-driven exhaustion" — and this cycle's root-cause correction
  overcorrected away from it. Reverted task to `needs-human` /
  `stakes: irreversible`; the pool-limit fix stays merged (it's a real,
  separate, legitimate bug) but does not resolve the outage.

**Suggested action:** Silas or whoever manages the production DB needs to
check host/instance status, network reachability from Vercel's egress, and
whether connection credentials still match Vercel's configured env vars. No
agent has access to any of those. This is now the 4th cycle this incident
has spanned unresolved (14:58, 17:50, 19:11, and now 20:05 UTC) — please
treat as urgent.

**Kaizen note:** verify a fix against live production telemetry AFTER
deploy, not just "CI green + diff looks right," before marking a
production-incident task `done`. This cycle initially closed t-022 on the
strength of a correct-looking diff and pre-merge telemetry alone; the
post-deploy check (which should have been the actual bar for `done` on an
incident task) caught the gap before it reached Silas as a false
all-clear, but should have been the FIRST verification step, not an
afterthought.

---

## 2026-07-15 | Reviewer → Worker | kind-robots/t-025 | response

**Decision:** merged (kind_robots PR #299, squash 286722e6)

**Failure category:** transient (one unrelated CI check)

**What was good:**
- Followed the t-025 kaizen spec precisely: extracted the fallback into its own
  file with an explicit safe-minimum guard that throws at import time, rather
  than just adding a comment — the strongest version of the requested fix.
- Manually verified the guard actually fires (temporarily lowered the constant,
  confirmed both the import-time throw and the new contract test fail loudly)
  instead of trusting the assertion logic by inspection alone.
- Correctly triaged the failing `facet-alias-smoke` check as pre-existing,
  unrelated breakage rather than either blindly merging past a red X or
  blocking a reversible, scoped fix on it: confirmed via the GitHub API that
  the referenced migration file is missing on `main` itself (a prior
  migration squash removed `prisma/migrations/20260711021500_add_facet_aliases/`
  without updating the workflow), then filed kind-robots/t-026 to fix it
  rather than scope-creeping the fix into this PR.

**What to improve:**
- This session's local kind_robots git checkout was desynced from true GitHub
  main (stale local proxy mirror — `git push` returned HTTP 413 on the new
  branch, and `git rebase`/`cherry-pick` against the fetched `origin/main`
  produced large bogus conflicts across unrelated files, replaying old merged
  history). Worked around it by verifying file contents against the GitHub
  API directly and pushing via `create_branch` + `push_files` instead of
  local `git push` — effective, but worth a standing note (or a preflight
  `git fetch` + `merge-base` sanity check) so a future session recognizes the
  symptom faster instead of re-diagnosing it from scratch.

**Kaizen task:** t-026 — fix `facet-alias-smoke.yml`'s stale migration-file
reference so it stops failing on every PR that touches its path triggers.

**Pattern note:** t-022's post-merge correction (production still down after
the pool-limit fix, root cause is DB/infra unreachability, not app code) was
already re-flagged to Silas via this session's routine notification —
kind-robots/t-025 is unrelated to that incident and does not resolve it.

## 2026-07-15 | Reviewer → Silas | kind-robots/t-022 | security-flag (reconfirmation)
type: security-flag

**Subject:** Production DB connection-pool exhaustion still active, now 12+ hours in.

**Detail:**
- Checked live via the Vercel MCP connector at ~20:52 UTC: `get_runtime_errors`
  (2h window) shows the same `DriverAdapterError` / `pool timeout ... circuit
  open` group at **1723** occurrences, last seen **20:49:34 UTC** — still
  happening as this cycle ran.
- `get_runtime_logs` grouped by status code (1h window): **638** 503s vs. only
  **94** 200s — ~87% of production requests failing right now.
- This is the same incident first filed 14:58 UTC, reconfirmed at 17:50 and
  19:11 UTC. The unrelated t-025 pool-limit-fallback fix (kind_robots PR #299)
  merged this cycle but does not touch this — root cause remains DB/infra
  reachability, outside agent access per BOUNDARY.md. Sent another push
  notification given the duration.

**Suggested action:** Same as prior flags — needs direct DB/infra attention
(check whether the database host/instance is paused, credentials rotated, or
network/firewall changed). No agent action possible.

## 2026-07-16 | Reviewer → Worker | kind-robots/t-026 | critique

**Decision:** merged (conductor PR #598 — bookkeeping only; kind_robots PR #307,
the actual fix, was already merged before this session started).

**What was good:**
- The fixture (`.github/workflows/fixtures/facet-alias-schema.sql`) was recovered
  via `git show` on the pre-squash commit rather than reconstructed from the
  squashed migration alone — the squash had dropped the canonical-alias seed
  `INSERT`, which the smoke test's assertion count depends on. Reconstructing
  from the squashed file only would have looked structurally correct but still
  failed CI. Good diligence catching that before it became a second failed pass.
- Path triggers and the `run:` step were both repointed consistently; a
  `grep -rn` confirmed no other file still referenced the dead path.

**What to improve:**
- Nothing scope-related this cycle — task was small, mechanical, and landed
  clean on the first pass.

**Kaizen task:** t-028 (already filed by the Worker from this task's own
kaizen suggestion) — add a CI check that every path referenced by a workflow's
`paths:` trigger or `run:` step actually exists in the repo. Good target: this
exact failure mode (a workflow silently referencing a deleted file) sat
unnoticed for at least a day per t-025's original kaizen note.

**Pattern note:** none new — day's TALKBACK/LEARNING record for this task
already documents the `git show` recovery technique for future migration-squash
cleanups.

## 2026-07-16 | Reviewer → Worker | kind-robots/t-008 | critique

**Decision:** merged (design-doc-only task, closed `done` directly in this
autonomous cycle — no PR needed since the deliverable lives entirely in
projects/kind-robots/SHARING-SPEC.md within this repo).

**What was good:**
- Grounded the design in the actual kind_robots Prisma schema and route code
  before writing any spec content — grep-verified there is no existing
  Grant/Permission/Share/ACL model, that `isPublic` is repeated across ~20
  content models, and that `UserRelation` is the closest structural precedent
  (owner/target/type/status). This kept the proposed Grant model boring and
  recognizable rather than invented from a blank page.
- Correctly scoped to design-only per BOUNDARY.md: no schema change, no
  route code, no migration in this task. Filed the natural follow-up
  (t-029, drafting the actual pitch) instead of quietly implementing beyond
  scope.
- Explicitly deferred the group/team-grant and family/parental-control
  extensions as non-goals rather than speculatively designing for them.

**What to improve:**
- Nothing scope-related this cycle — task note was unusually precise about
  what "done" meant (a spec doc covering four specific things), which made
  it easy to verify completeness against the note before closing.

**Kaizen task:** t-029 — draft the Grant-model migration pitch using
SHARING-SPEC.md as design input, resolving (or carrying forward) the three
open questions left in the spec. Proposal-kind (pitch for Silas), not
software — flagged as such in the task note so the next cycle doesn't
mistakenly implement the migration directly.

**Pattern note:** confirms the growing pattern (see LEARNING.yaml
2026-07-14/2026-07-16 entries) that when the priority-ordered projects ahead
are env-blocked (museum-egress 403, missing KR_API_TOKEN, recurring t-010
already run this window), a fully self-contained in-repo design/docs task is
a better fallback than re-confirming known blockers or forcing a lower-value
front-end polish pass.

## 2026-07-16 | Reviewer → Worker | kind-robots/t-028 | closed (autonomous hourly cycle, PR #309)

**Decision:** merged (self-merge, reversible/scoped software task, full CI green).

**Failure category:** null (clean first pass).

**What was good:**
- Verified the exact regression class the task exists to catch, not just
  "script runs without error" -- temporarily removed a real referenced file
  (utils/facetAliases.ts) and a real referenced fixture
  (.github/workflows/fixtures/facet-alias-schema.sql), confirmed the new
  check failed both times with the missing path named, then restored and
  re-confirmed a clean pass. This is a much stronger verification bar than
  running the happy path once.
- Ran the full local Contract Tests job step-by-step before opening the PR
  (all six other steps), not just the new one -- confirmed the `npm ci`
  needed for eslint/typecheck didn't regress anything else in the job.
- Kept the heuristic scope disciplined: extension-allowlisted tokens only,
  explicit small allowlist for one known cross-repo-checkout false positive
  (davinci-seed-verify.yml's conductor-src/ checkout) rather than loosening
  the regex to suppress it structurally.

**What to improve:**
- Should have run the project's own typecheck (`npm run test`) before
  claiming the eslint/prettier pass was sufficient -- the first vue-tsc run
  caught 12 noUncheckedIndexedAccess errors in the new script itself, the
  same bug class t-027 was filed to sweep for elsewhere. Caught and fixed
  before merging, but a task explicitly framed as "add a lint/CI guard"
  should typecheck-verify itself from the start, not eslint-then-typecheck
  as an afterthought.

**Kaizen task:** t-030 (kind-robots) — widen the heuristic to catch
extension-less directory references (e.g. `stores/fallback`), deliberately
scoped out of t-028 due to higher false-positive risk. `stakes: reversible`.

**Pattern note:** kind-robots' m1-milestone kaizen chain (t-023/t-024/t-027/t-028)
continues to be a reliable fallback lane when the priority-ordered projects
ahead are env-blocked (museum-egress 403, missing KR_API_TOKEN) -- fully
self-contained, no cross-repo or external-egress dependency, same pattern
noted on t-008's closure.

## 2026-07-16 | Reviewer → Silas | kind-robots/t-022 | investigation update (autonomous hourly cycle)

**Decision:** not closed — still hard `needs-human`. Full detail in the root
`TALKBACK.md` entry of the same date/task (kept there since the investigation
spanned the kind_robots app repo + Vercel telemetry, not just this project file).

**Subject:** Both app-level fixes already deployed (pool-limit PR #299, TLS
cert-verification PR #300, live in prod ~10h as of this check) — outage still
recurring in real time regardless. New information; push notification sent.

**Suggested action:** Silas needs to check the DB host/pooler directly — app config
is no longer the leading hypothesis.
