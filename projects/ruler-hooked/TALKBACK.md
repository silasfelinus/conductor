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

## 2026-08-27 | Reviewer → Worker | ruler-hooked/t-021 + t-017 | critique

**Decision:** merged (PR #2961, squash-free merge commit `9fb4d0e`), after resolving a real merge conflict against `main` first.

**Failure category:** n/a — clean close-out, conflict was environmental (branch fell behind while a scheduled art run and PR #2962 both landed against `main`), not a Worker mistake.

**What was good:**
- The Worker's own PR body already flagged the risk correctly ("a resolution favouring the branch side would have reverted 36 completions") and got the previous round's conflict right by comparing both resolutions before adopting one — good discipline, carried forward here.
- The `t-021` spec itself is a model of "write the interpretation down, don't silently assume": it named the offline-no-runtime-AI pillar as the reason "custom" can't mean live generation, named the storage caveat (localStorage quota vs. base64 portraits) before it became a bug, and flagged the whole section as interpretation open to correction.

**What to improve:**
- This session's own conflict (base had moved 1 commit further by the time of push, from PR #2962 merging in between) was resolved the same way, one more data point that this branch attracts collisions — see the "Suggested action" below, still open.

**Conflict resolution detail** (for whoever next touches this branch or `art-prompts.yaml`'s pruning behavior):
- `LEARNING.yaml`: both sides had independently appended a `ruler-hooked/t-017` close-out record with different dates/lessons (a duplicate-close-out race, same shape as conductor/t-085). Kept both records rather than picking one, per the append-only rule.
- `projects/art-prompts.yaml`: a large interleaved conflict (40+ hunks) because both this branch and PR #2962 (cthulhuquarium) had rewritten large parts of the file. Did a semantic 3-way merge keyed by each entry's `id` (not a textual merge): computed base/head/main via `git merge-base`, diffed by id, and confirmed every id this branch had modified fell into one of two buckets — 58 ids `main` hadn't touched (reapplied this branch's edits) and 48 ids `main` had already pruned entirely (accepted the deletion). Verified the 48 pruned ids were genuine completed deliveries, not an accidental drop, by curling 3 of their `source_url`s directly (`media.acrocatranch.com`) — all resolved 200 (one needed the entry's actual `image_path`, not a guessed one, to confirm). `build_ruler_hooked_art_queue.py --include-layers --check` then reports those same 48 as "missing" — expected and not a regression: the script only checks whether an id is staged, with no "already delivered and pruned" awareness (the same class of gap the cthulhuquarium kaizen this session filed, `t-046`, is about). Full `pytest tests/` — 1284 passed, 1 skipped — and `validate_roadmaps.py` clean after the merge.

**Kaizen task:** none filed new this cycle — `t-046` (filed against cthulhuquarium this same session) already covers the general "build_*_art_queue.py has no already-shipped awareness" gap this conflict is a second instance of; extending it to `build_ruler_hooked_art_queue.py --check` too is in scope for whoever picks up t-046.

---
_Generated by [Claude Code](https://claude.ai/code)_

## 2026-08-27 | Agent (scheduled conductor session) | ruler-hooked/t-018 + t-022 | state reconciliation

type: response

**Subject:** Reconciled two tasks stuck at `status: review` from a prior session (`2026-08-26T23-claude-ruler-hooked-art`) that ended without a final status update.

**Detail:**
- `check_pr_merged_drift.py` flagged both as unverifiable candidates (its PR-shaped heuristic 403s on direct GitHub API calls in this sandbox and neither task ever had a PR to find anyway — these are ArtJob-delivered assets, not code changes).
- **t-022** ("Reward and ending illustrations"): the task's own note named its exact completion criterion — "Flip to done once the media paths are live." Spot-checked all 13 target paths directly against `kindrobots.org` (9 reward object studies + 4 ending illustrations); all returned HTTP 200. Flipped to `done`.
- **t-018** ("Render the 37-piece region/state/time environment matrix"): the note says the batch was "Deliberately not staged" pending `t-016`/`t-017`, and no PR or ArtJob batch reference exists anywhere — nothing was ever actually submitted. Both dependencies are now `done` (`t-017` finished `2026-08-27T01:34Z`, after this task's own claim at `23:30Z` the day before), so the block that justified deferring it is gone, but the status still read `review` as if something were pending review. Corrected to `ready` so the next session picks it up as real, unblocked work instead of skipping it as "already submitted."

**What was good:** read each task's own note for its stated completion/blocking criterion instead of assuming "review" uniformly means "PR awaiting merge" — the two tasks needed opposite corrections (one really was done, one was never started) and the note text was sufficient to tell them apart without guessing.

**Kaizen suggestion:** none filed — this is a one-off reconciliation of a specific stale-state gap, not a systemic tooling change. If ArtJob-delivered (non-PR) tasks reaching `review` without ever completing becomes a recurring pattern, `check_pr_merged_drift.py` could grow a second heuristic for "note says review but no ArtJob/PR reference exists at all," but two occurrences isn't yet a pattern worth building for.

---
_Generated by [Claude Code](https://claude.ai/code)_

## 2026-08-27 | Agent (scheduled conductor run) | ruler-hooked/t-021 | security-flag + pattern

type: pattern

**Subject:** Genuine rotation collision — two independent scheduled sessions fully implemented and opened PRs for the same task (t-021) within minutes of each other; the earlier PR merged first, this session's was closed unmerged once discovered.

**Detail:**
- This session claimed `ruler-hooked/t-021` via `claim_task.py` at `07:33:19Z` and worked the kind_robots implementation independently (no visibility into any other session's activity, since the other session's kind_robots work needed no conductor roadmap edit until its own close-out). By the time this session went to close out (~08:50Z), `origin/main` already showed `t-021` at `status: done`, referencing a *different* session (`claude-scheduled-20260827T0830Z-rh-t021`'s own claim timestamp collided with an even earlier, undeclared parallel session that had been on the kind_robots side since ~07:22Z) that had merged `silasfelinus/kind_robots#2142` at `07:48:07Z`.
- Their implementation is a strict superset of this session's independently-arrived-at design (same core approach: preset picker, free-text honorific+name, compositor cosmetic axis with a graceful fallback ladder) plus the custom-portrait-upload/IndexedDB piece this session had deliberately split off as a follow-on task (`t-023` in this session's draft, never landed) — theirs shipped it directly instead of deferring.
- Recovery, following the "Rotation collisions" precedent in AGENTS.md: discarded this session's local roadmap edits (would have overwritten the other session's completion note and reverted `status: done` → own draft), closed this session's now-duplicate kind_robots PR (#2143) unmerged with an explanatory comment, and force-deleted (via `branch-janitor.yml` `workflow_dispatch`, session credentials 403 on ref deletion as documented) both this session's kind_robots branch and a stray `close_task.py`-generated conductor branch that would have wrongly flipped `status: done` back to `review` had anyone merged it.
- **What made this collision different from the documented `claim_task.py` cases:** `claim_task.py` correctly prevented a *second* roadmap claim (this session's claim at `07:33:19Z` presumably raced/won against whatever the other session's own claim mechanism was, or the other session skipped the conductor-side claim step entirely and only touched kind_robots) — the actual duplication happened entirely on the *implementation* side, in a repo `claim_task.py`'s atomic-commit-to-main mechanism doesn't cover. Neither session's local state had any way to observe the other's kind_robots branch/PR mid-flight, since cross-repo work (per AGENTS.md's own "Cross-repo tasks" section) only touches the conductor roadmap at claim and close-out, not continuously.

**Suggested action:** this project's `TALKBACK.md` already has one prior entry flagging "this branch attracts collisions" (2026-08-27, ruler-hooked/t-021+t-017 conflict) — this is now a second, structurally different collision on the same project in the same day. Worth a kaizen task (not filed by this session, to avoid claiming a fourth task mid-cleanup): before implementing a cross-repo task, check the target repo's own recent branches/open PRs for the same task id in the title (a cheap `list_pull_requests`/`list_branches` grep), not just the conductor roadmap's claim state — this would have caught the collision at ~07:35Z instead of ~08:50Z.

---
_Generated by [Claude Code](https://claude.ai/code)_
