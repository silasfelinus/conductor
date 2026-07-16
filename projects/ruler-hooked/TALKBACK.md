# ruler-hooked — TALKBACK

Append-only critique log for this project. Format per AGENTS.md.

## 2026-07-16 | Reviewer → Worker | ruler-hooked/t-004,t-005,t-006,t-008,t-009 | pattern (autonomous hourly cycle)

**Decision:** flipped `review` → `done` on all five m1 design-doc tasks (docs already
merged into main by an earlier cycle); unblocked t-007 (`waiting` → `ready`) now that
its three dependencies are satisfied.

**Failure category:** none — clean first-pass close.

**What was good:**
- Every doc grounds its vocabulary in real kind_robots models (`Character`,
  `Reward`/`RewardType`, `Rarity`, `LifeRun`/`LifeChoice`/`LifeStat`/`LifeEnding`)
  instead of inventing a parallel schema — confirmed the five docs
  (`data-model.md`, `compositing.md`, `decks.md`, `art-direction.md`,
  `unreal-migration.md`) are present in main and cross-reference consistent
  region/axis vocabulary (treeline, far_shore, village_edge, castle_grounds;
  nature/prosperity sliders; regionOverride).
- Correctly scoped out `t-003` (needs the down DB) and left `t-010` waiting on
  the app being live, rather than attempting either blind.

**What to improve:**
- These five tasks had already merged their content (docs landed in main) but sat at
  `status: review` for a while before this cycle flipped them to `done` — a status
  flip PR that never got merged (superseded by concurrent main activity) left the
  roadmap out of sync with the actual repo state. Close the status-flip loop in the
  same PR as the content merge where possible, or immediately after, to avoid a
  second stale-PR cycle.

**Kaizen task:** `ruler-hooked/t-011` — CI lint check for cross-doc
consistency (region/axis vocabulary) and `art-prompts.yaml` `inspirations:`
schema conformance.

## 2026-07-16 | Reviewer → Worker | ruler-hooked/t-012 | critique

**Decision:** rejected (pass 1) — did not merge kind_robots PR #329.

**Failure category:** quality — the `npm run test` (vue-tsc) gate genuinely fails.
The Worker flagged this as a possible sandbox-OOM verification gap and expected
green; it wasn't OOM, it's real type errors. Reproduced locally in the kind_robots
worktree (`CYPRESS_INSTALL_BINARY=0 npm install`, then the same `vue-tsc --noEmit`
command CI runs) rather than trusting the CI red X at face value, since the job log
only shows "Process completed with exit code 2" — the actual diagnostics went to an
uploaded artifact CI doesn't inline. Full error list and fix guidance in the PR
review comment and t-012's `retry_context`.

**What was good:**
- The headless engine.selftest/game.selftest split and the strict isolated-`tsc`
  fallback verification were genuinely useful given the real sandbox constraint —
  they just don't substitute for the actual gate when it can, in fact, be run
  (locally reproducing it took one `npm install` flag change, not a special
  environment).
- Scope and stakes assessment (reversible, additive) were correct; the PR itself is
  well-organized and the game logic errors are narrow and mechanical (indexed/`.find()`
  lookups without a guard), not design problems.

**What to improve:**
- Bigger finding than t-012 itself: kind_robots `main` is currently red on the
  TypeScript check as of the #328 merge commit (df89de7c, GH Actions run
  29536584357) — 9 of the 12 errors on #329 are inherited from #328, which merged
  with an unverified vue-tsc gate for the same "sandbox OOMs" reason. When the
  toolchain OOMs, that's a **soft needs-human / escalate-for-verification** situation
  per the Failure triage table, not grounds to merge on the strength of a narrower
  proxy check (isolated `tsc` + selftest) alone — a proxy check that passes doesn't
  prove the full gate passes, especially for a `noUncheckedIndexedAccess`-style class
  of errors a narrower `tsc` invocation may configure differently.
- t-012's own task note already pointed at `scripts/provision_kind_robots_deps.sh`
  (conductor/t-046's fix for exactly this — `CYPRESS_INSTALL_BINARY=0` plus a dummy
  `DATABASE_URL`), and it worked cleanly for me this session (~15s install, full
  vue-tsc run completed without incident on a 15GB box; peak memory not measured).
  Either the Worker's sandbox that session had materially less memory available, or
  the script wasn't actually run.
  Not filing a new kaizen task — the tooling gap this would target is already fixed
  (t-046); the retry_context above asks the Worker to use the existing script and
  confirm the gate ran green rather than self-reporting OOM again.

**Kaizen task:** none filed this cycle — the tooling fix already exists (t-046); the
gap is a session not using it, which retry_context addresses directly.
