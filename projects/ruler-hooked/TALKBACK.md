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

## 2026-07-21 | Worker (scheduled) | ruler-hooked/t-007 | done (no PR needed — verification + bookkeeping)

**Decision:** closed out (session claude-conductor-scheduled-20260721T1214Z).

**Failure category:** none — clean, no retry needed.

**What was good:**
- t-007's note already stated an explicit completion condition: "Mark t-007 done once
  PR #328 merges AND t-012 lands the playable screen meeting all four DESIGN-BRIEF m2
  exit criteria." Both were true as of t-012's merge earlier the same day (kind_robots
  PR #811), but t-007 itself hadn't been flipped — picked it up specifically to close
  that gap rather than treat it as new implementation work.
- Did not trust t-012's prior "confirmed the four exit criteria" note at face value
  (the freshly-added AGENTS.md retry_context guidance from this same day's t-074 kaizen
  applies just as much to a completion claim as to a rejection). Re-verified
  independently against a fresh kind_robots checkout at current main (736b663f):
  `npx tsx utils/rulerHooked/engine.selftest.ts` and `game.selftest.ts` both ALL PASS,
  and the full `npm run test` (vue-tsc --noEmit) gate is green (exit 0) — confirming
  the 2026-07-16 red-main TypeScript regression this task's own note flagged is
  resolved, not just the narrower isolated-tsc proxy check the earlier PROGRESS entries
  above warned against relying on alone.
- Confirmed all four DESIGN-BRIEF m2 exit criteria are structurally wired, not just
  passing at the engine level: `components/ruler-hooked/ruler-hooked-page.vue` (mounted
  at `content/ruler-hooked.md`'s `#interactive` slot) composes `ruler-hooked-game.vue`
  (playable session + event cards/narrative arc), `ruler-hooked-stage.vue` (composited
  landscape regions), `ruler-hooked-health.vue`, and `ruler-hooked-slots.vue` (multiple
  save slots).
- No kind_robots code change needed — conductor-only close-out. Claimed via
  `claim_task.py` before editing.

**What to improve:** none this cycle.

**Kaizen task:** none this cycle — m2's remaining ready task (t-010, the open-ended
"polish and upgrade" pass) already covers ongoing front-end improvement; no new gap
found worth a separate task.

## 2026-08-26 | Reviewer → Worker | ruler-hooked/t-016 | pattern
type: pattern

**Subject:** The first real art batch found two spec bugs that only surface when
you actually render, and both were cheap to catch and expensive to ignore.

**Detail:**
- **t-008 shipped a prompt pack that had never been enqueued.** Its own status line
  says "PROMPTS ONLY, no art generated (KR_API_TOKEN unset)", and its §6 claims the
  first-pack entries "are added to `projects/art-prompts.yaml`". They are not in that
  file today — zero `ruler-hooked` entries existed before this cycle, against 572
  pending mandarin-tutor rows. A spec that has never been executed is a hypothesis.
  Six weeks passed with the token available and the render box healthy, and nobody
  noticed the queue entries were gone, because nothing checks that a documented queue
  entry still exists. `build_ruler_hooked_art_queue.py --check` now fails if any
  entry this project expects is missing, which is the general fix.
- **The layer-transparency rule contradicts the component that shipped.**
  art-direction.md §2 authors every region layer full-frame with everything outside
  its depth band transparent; `ruler-hooked-stage.vue` draws each region as a
  `flex-1` band with `object-cover`, roughly 20:1, which crops a full-frame layer to
  a slice of its own middle. Both specs are internally coherent and they cannot both
  be satisfied by one file. Caught before submitting, so it cost nothing; submitting
  first would have cost 37 renders and looked like an art-quality problem rather than
  a contract problem. Filed as t-017, and t-018 waits on it.
- **The house style's own "always avoid text/logos/watermarks" line is now a hard
  422.** kind_robots' `artPromptContract.ts` rejects more than four
  text-nouns-after-"no" on an engine whose negative prompt is inert. Krea 2 runs at
  cfg 1, so it is inert, so those words land in positive conditioning on a
  text-specialist model. All 25 submissions bounced on the first attempt. The rule
  is right and the doc predates it; §8.2 records the correction and the builder now
  mirrors the contract locally so it fails at build time instead of at enqueue.

**Suggested action:** When a spec-only task writes prompts it cannot run, say so in
the roadmap task's *status*, not only in the doc's prose — t-008 closed `done` while
its actual deliverable (queued entries) was never verified to exist. A `--check`
mode that a later session can run is worth more than a paragraph asserting the
entries were added. Generally: prefer generating prompts from a script that reads the
upstream data over writing them into a queue file once, so drift is impossible rather
than merely discouraged.
