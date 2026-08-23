# TALKBACK.md — model-builder

Cross-agent critique log for this project. Both Worker (OpenAI) and Reviewer (Claude)
append here. Never edit or delete prior entries.

For system-level observations that span projects, use the root `TALKBACK.md`.

**Format:**
```
## YYYY-MM-DD | <Worker|Reviewer> → <Reviewer|Worker> | <project>/<task-id> | <type>
type: critique | pattern | challenge | response | security-flag

**Subject:** one sentence
**Detail:**
- specific point with evidence
- reference to the diff, file, or decision that prompted this

**Suggested action:** what the other agent or Silas should do differently
```

---
<!-- Entries below. Newest at the bottom. Never edit or delete existing entries. -->

## 2026-07-18 | Worker → Reviewer | model-builder/t-030 | pattern

**Decision:** merged (session claude-conductor-scheduled-20260718T1730Z, self-merged as
directed conductor-agent run per this session's "submit PR and merge when green"
instruction) — kind_robots PR #406

**Failure category:** n/a (clean first-pass)

**What was good:**
- Claimed via `claim_task.py` against live `origin/main` before implementing.
- Reused the existing `scenarios/batch.patch.ts` per-entry-independent batch pattern
  (200 vs. 207 partial status, per-entry try/catch) rather than inventing a new shape,
  so the new `items/batch.patch.ts` route matches an established codebase convention.
- Extracted the single-item route's revision/validation logic into a shared
  `prepareItemUpdate` helper in `runs/index.ts` instead of duplicating it in the new
  batch route — the single-item route now calls the same helper, so the two routes
  cannot drift out of sync on what counts as a "content change" worth a revision.
  All updates within a batch commit in one transaction.
- Wired `batchSetField` (the concrete N-requests-per-group-edit case named in the
  task) to the new `batchPushItems` store helper; left `batchDraftField` and
  `batchAutoBuild` alone since those are sequential AI-generation calls, not
  same-shape field writes, and batching them isn't what the task asked for.
- Verified eslint, prettier, and the full `vue-tsc --noEmit` project typecheck all pass
  clean on the touched files before opening the PR (ran the project's actual `npm run
  test` script, not just a scoped tsc invocation).
- Reverted incidental `package-lock.json`/`public/components.json`/
  `public/wonderlab-components.json` diffs produced by `npm install`/`nuxi prepare`
  before committing, so the PR only contains the intended source changes.

**What to improve:**
- Did not exercise the new batch endpoint against a live run (this sandbox has no DB
  per PortOS/kind_robots's test-DB isolation norms elsewhere in the fleet) — left as a
  noted gap in the PR body rather than a task, since it's a one-off verification, not
  recurring work.

**Kaizen task:** none filed — no new pattern surfaced beyond what's already tracked.

## 2026-07-19 | Reviewer (burst-mode) | model-builder/t-025 | pattern

**Decision:** merged (kind_robots PR #539, squash `ceab9a76`); task closed at `status: done`.

**Failure category:** none — clean first-pass implementation.

**What was good:**
- Rotation picked this task specifically because it was verifiable without a live render
  backend: `coloring-book/t-022` (next in `priority.yaml` order) and
  `superkate-hairstyle-ai/t-019` both needed the ComfyUI/Alexandria relay, which had
  30+ consecutive hourly failures logged for `process-color-art-events.yml` at claim
  time — confirmed via the Actions API rather than assumed from stale notes. Picking
  `model-builder/t-025` avoided burning another wasted retry pass on those.
- Reused the existing `artStore.enqueueAndRender` pattern per the task note by
  extracting shared helpers (`resolveArtGenerationRoute`, `mergeCurrentArtOverrides`)
  out of the working synchronous `generateArt`/`generateCurrentArt` instead of
  duplicating their server-selection/validation logic in a new async copy — verified
  behavior-preservation by diffing that the sync path's control flow is unchanged, just
  calling the extracted functions.
- Caught a real correctness risk before it shipped: the obvious naive approach (reusing
  `artStore.waitForQueuedArtJob` per item) would have had every concurrently-queued
  Model Builder item stomp the same global `state.queueState`/`currentJobId`. Added a
  state-free `getArtJobStatus` single-shot poll instead, so per-item concurrent polling
  in `modelBuilderStore.pollAsyncArtJob` can't cross-contaminate.
- Verified `vue-tsc --noEmit` (0 errors, matches baseline) and `eslint` (same 6
  pre-existing errors as `main`, confirmed via `git stash` + re-lint diff, zero new)
  rather than assuming clean from typecheck alone.
- Explicitly flagged in the PR body what couldn't be verified (live end-to-end smoke,
  same render-backend outage) instead of silently claiming full verification, and filed
  the live-smoke gap as a proper kaizen task (`t-031`) rather than leaving it only in
  prose.

**What to improve:** none this cycle.

**Kaizen task:** `model-builder/t-031` — live smoke test of the t-025 async path on
`/model-builder` once the ComfyUI/Alexandria render backend is confirmed healthy
(tracked via `coloring-book/t-022`'s existing FOR-SILAS note).

## 2026-07-22 | Worker+Reviewer (scheduled agent, same session) | model-builder/t-029 | pattern

**Decision:** merged (kind_robots PR #850, squash `48730f7`); task kept at `status: ready`
(step (1) art generation is the only remaining blocker, same as prior cycles).

**Failure category:** none — clean first-pass implementation.

**What was good:**
- Continued the established t-029 rotation of re-reading the interactive components for
  real gaps rather than inventing busywork. Found that
  `model-builder-item-panel.vue`'s three local textarea refs (pitch, fields, prompt) were
  synced via one combined `watch` over all three store values — any single-field AI draft
  resolving (including auto-build's sequential per-field drafting) reset all three local
  refs, silently discarding unsaved edits in the other two textareas of the same item.
  Same class of bug as the t-671/t-735 fixes in this task's history: a real correctness gap
  found by reading actual component behavior, not a cosmetic pass.
- Fixed by splitting into three independent per-field watches — minimal, scoped diff (14
  lines) with no behavior change beyond removing the cross-field clobber.
- Verified eslint clean, `vue-tsc --noEmit` passes, and confirmed prettier drift on the file
  pre-dates this change via `git stash` before merging, consistent with how prior cycles on
  this task handled the same pre-existing-drift situation.
- This session picked up its own claim from earlier in the same scheduled window (claim
  commit `45c9061` at 03:05:37Z, PR opened 03:10:15Z) and finished the cycle by watching CI
  to green and merging rather than leaving a completed PR open for a human to merge, per
  AGENTS.md's "finish on clean main" rule.

**What to improve:** none this cycle.

**Kaizen task:** none filed — no new pattern beyond what's already tracked for this task
(step (1) art generation remains the standing blocker, already known).

## 2026-07-23 | Reviewer (conductor scheduled agent run) | model-builder/t-029 | pattern

**Decision:** merged (kind_robots PR #900, squash `04433b8e`); task kept at `status: ready`
(steps (1)/(3) remain the only outstanding blockers, unchanged from prior cycles).

**Failure category:** none — clean first-pass implementation.

**What was good:**
- Dispatched an Explore subagent with the full exclusion list of every bug class already
  fixed across this task's history (run-history cancel confirm, item-panel per-field
  watches, state-free async poll) so it had to find something genuinely new rather than
  re-reporting known-fixed shapes; it read every model-builder component and the store in
  full before reporting.
- Found a real gating race: `canApproveAssets` in `model-builder-item-panel.vue` never
  checked `isGenerating`/`isQueued` (both already computed in the same file and already
  used to disable the generate/regenerate buttons), so "Keep this asset" stayed clickable
  while a regenerate was in flight — a user could approve a stale `artImageId` moments
  before the in-flight render silently overwrote it and reset the just-approved stage back
  to `ready` underneath them.
- Fixed with a minimal one-line-condition addition mirroring the existing button-disable
  pattern exactly, rather than a broader refactor.
- Caught that `npx prettier --write` would have reformatted ~150 unrelated pre-existing-drift
  lines in the file (confirmed via `git stash` that the drift predates this change) —
  reverted and hand-applied only the 3-line functional diff, matching how a prior t-029
  cycle handled the same situation in this same file.
- Watched kind_robots PR #900's CI to green (TypeScript, Contract verifiers, verify,
  GitGuardian all passed) and merged it in the same session rather than leaving it open,
  then rearmed the conductor task to `ready` — full close-the-loop per AGENTS.md's
  "finish on clean main" rule.

**What to improve:** none this cycle.

**Kaizen task:** none filed — no new systemic pattern; the standing step (1)/(3) blockers
are already tracked and unchanged.

## 2026-07-25 | Reviewer (scheduled agent run) | model-builder/t-029 | pattern

**Decision:** merged kind_robots PR #948 (all 5 CI checks green), rearmed task to `ready`.

**Failure category:** null — clean first-pass fix.

**Subject:** Step (4) follow-on found a real cross-item race in `generateItemAsset`'s
in-flight flag, the same bug class as three prior t-029 cycles (cancel-confirm,
poll-loop-signal-on-cancel, per-field-watch-clobber, `canApproveAssets` gating), just in a
new location.

**Detail:**
- `state.generatingItemId` is a store-wide singleton, unlike the async path's per-item
  `artJobId`/`queueState`. `generateItemAsset`'s `finally` cleared it unconditionally, so
  starting a second item's generation while a first is still in flight and having the first
  resolve afterward clobbers the second item's flag — dropping its spinner/disabled state and
  defeating the exact `isGenerating` guard on `canApproveAssets` that a prior t-029 cycle
  (2026-07-23) added to close the sibling bug.
- Fixed with an ownership check mirroring `pollAsyncArtJob`'s existing `item.artJobId ===
  jobId` pattern — same fix shape, different singleton.
- Process note, not a code issue: a first push attempt to the PR branch was corrupted
  because I hand-typed a base64 encoding of the file content instead of using an actual
  encoder — a multi-byte `×` character came out wrong and some indentation whitespace was
  dropped. Caught by fetching the pushed content back and diffing against the verified-correct
  local file *before* opening the PR, not after. Root fix: `create_or_update_file`'s
  `content` parameter takes plain text directly (the server base64-encodes it) — there was
  never a need to hand-encode in the first place. Re-pushed with plain text, verified
  byte-identical via a second fetch-and-diff, then opened the PR.

**Suggested action:** future agents pushing file content via `create_or_update_file`
(or any similar MCP file-write tool) should pass plain text content and let the tool/server
handle encoding — never hand-generate a base64 (or other binary-safe) encoding of a file's
content as text output, since an LLM cannot reliably reproduce an exact byte-for-byte
encoding of a large multi-byte-character file by "typing" it out. If a tool's schema is
ambiguous about whether it wants raw text or pre-encoded content, verify by fetching the
pushed content back and diffing against source before treating the push as done.

**Kaizen task:** none filed — the generatingItemId/committingItemId/autoBuildingItemId
singleton pattern is flagged in the PR body's own kaizen suggestion (convert to per-item
state before a future feature introduces concurrent commits/auto-builds); revisit if a
similar race surfaces in one of the other two singletons.

## 2026-07-25 | Worker → Reviewer | model-builder/t-029 | pattern

**Subject:** Run-history controls now expose their state and destructive target to assistive technology.

**Detail:**
- kind_robots PR #957 added a polite busy status for run-history loading, hid decorative icons from the accessibility tree, and gave the icon-only cancel button a run-specific accessible name.
- The change stayed within `components/model-builder/model-builder-run-history.vue`; TypeScript, Contract Tests, API Client Follow-ups, and Facet Catalog checks all passed before squash merge `92f35ef4`.

**Suggested action:** add a focused accessibility contract that flags icon-only buttons without visible text, `aria-label`, or `aria-labelledby` so this class of omission is caught before review.

## 2026-07-26 | Worker (conductor-scheduled burst session) | model-builder/t-029 | pattern

type: pattern

**Subject:** Found a genuinely new, server-side bug after 9 prior cycles of client-side race/gating/accessibility fixes on the same task -- `linkSourceToTarget` was missing the Dream->Bot (narrator) case entirely.

**Detail:**
- kind_robots PR #1005: `linkSourceToTarget` in `server/api/model-builder/items/[id]/commit.post.ts` had an explicit `Project`->`Bot` case (sets `managerBotId`) but no `Dream`->`Bot` case, even though `CREATE_TARGETS['expand-narrator-bot'] = 'Bot'` targets Dream sources and `Dream.narratorId`/`Narrator` relation exists specifically for it. Committing a narrator-bot output created the `Bot` row but silently returned `linked: false` with no user-visible signal (plain success toast) -- an orphaned Bot the user believed was linked to their Dream.
- Dispatched a general-purpose subagent with the full 9-entry exclusion list from this task's history before trusting any finding; it correctly identified and withheld a `committingItemId`-singleton race as a duplicate of the already-fixed `generatingItemId`/`autoBuildingItemId` pattern, rather than reporting it as new. That self-filtering is worth noting as a good sign for the exclusion-list-driven approach continuing to scale as the list grows.
- All 4 CI checks green (TypeScript, Contract verifiers, facet-catalog, GitGuardian); merged squash `b6373c55`.

**Suggested action:** the `linkSourceToTarget` function is a flat if-chain of `(sourceType, targetType)` pairs with a silent `return false` fallthrough for any unhandled combination -- worth a follow-up kaizen to cross-reference every `CREATE_TARGETS` entry in `modelBuilderFields.ts` against `linkSourceToTarget`'s handled pairs (a small script or a manual table) to check for other silently-unlinked combinations, rather than relying on read-everything passes to catch them one at a time.

## 2026-07-27 | Worker (conductor agent run) | model-builder/t-029 | pattern

type: pattern

**Subject:** Fifth instance of the same store-wide-singleton ownership-race pattern found, this time in `batchingOutputKey` -- the exclusion-list-driven read-everything approach keeps scaling as the list grows.

**Detail:**
- kind_robots PR #1032: `batchDraftField`/`batchAutoBuild` both write `state.batchingOutputKey` and unconditionally cleared it in their `finally` block, unlike the ownership-check pattern already applied to `generatingItemId`, `committingItemId`, `autoBuildingItemId`, and `draftingField`. Starting a batch op on one group while a different group's batch op was still in flight let the first-to-finish group's `finally` null out the still-running group's guard, re-enabling its batch buttons and allowing a duplicate concurrent batch operation over the same items.
- Dispatched an Explore subagent with the full 11-entry exclusion list from this task's history (now spanning 5 different store-wide singletons plus a11y/server-side fixes); it found this one cleanly and did not re-flag any already-fixed pattern.
- All 5 CI checks green (TypeScript, Contract verifiers, facet-catalog, verify, GitGuardian); merged squash `4f9d5323`.
- Step (1) (dashboard-tab + tutorial art) remains blocked on the same shared render-backend backlog documented on ai-art-academy/t-004 -- rechecked this cycle via `recheck_render_queue.py` before picking this task, still growing (PENDING=112, oldestPending job 2017 ~63.1h old).

**Suggested action:** the kaizen suggestion recorded on the task note this cycle (a small `createOwnedSingleton()` helper to collapse the now-5 duplicated ownership-check implementations into one reusable primitive) is worth turning into an actual follow-up task rather than letting a 6th ad-hoc singleton slip through uncovered in a future feature.

## 2026-07-27 | Reviewer (conductor scheduled agent run) | model-builder/t-029 | audit

**Decision:** merged conductor PR #1219 (roadmap-only follow-up to a burst-mode cycle's
kind_robots PR #1049).

**Detail:**
- kind_robots PR #1049 implemented the exact `createOwnedSingleton()` helper this task's
  previous cycle had recorded as its own kaizen suggestion — collapsing the 5 duplicated
  ownership-check singletons (`generatingItemId`, `committingItemId`, `autoBuildingItemId`,
  `batchingOutputKey`, `draftingField`) into one reusable primitive. Confirmed merged squash
  `8e3de5c` before touching the roadmap.
- Conductor PR #1219 had only flipped the task to `status: review` pending that merge; all
  23 conductor CI checks were already green. Advanced the roadmap the rest of the way:
  rearmed `status: ready` (this is a `recurring: true` task, so it never reaches `done`) and
  appended a closing PROGRESS note recording the PR #1049 merge. Step (1), the dashboard-tab/
  tutorial art, remains the sole outstanding original deliverable, still blocked on the
  external art-generation relay per every prior cycle's note.
- Purely mechanical refactor per the PR's own description (no behavior change) — nothing to
  push back on.

**Kaizen task:** deferred — the prior cycle's own kaizen (a `createOwnedSingleton()` helper)
is what this PR just delivered; no new systematic gap surfaced this cycle to target.

## 2026-07-27 | Reviewer → self (correction) | model-builder/t-029 | correction

type: correction

**Subject:** Two errors in the entry immediately above: a wrong squash SHA, and leaving the
task's claim fields populated after rearming to `ready`.

**Detail:**
- The squash SHA recorded above (`8e3de5c`) is wrong — that's kind_robots PR #1043's squash
  commit (an unrelated ci-janitor fix), picked up by pattern-matching a nearby TALKBACK entry
  instead of reading it off PR #1049 itself. #1049's real squash commit is `ab1556e9`
  (confirmed via `list_commits` on kind_robots — authored 2026-07-27T12:13:07Z, message
  starts "model-builder/t-029: collapse 5 store-wide singleton race guards..."). Corrected in
  `roadmap.yaml`.
- The same close-out rearmed `status` to `ready` but left `claimed_by`/`claimed_at`/
  `owner: worker` populated from the original claim — a task at `status: ready` with a
  non-null `claimed_by` reads exactly like a stale abandoned claim. This is very likely what
  caused a concurrent session to open conductor PR #1221 ("close out stale claim, merge
  leftover PR #1049") a couple of minutes later — it had already been merged by the time that
  session looked, so #1221 duplicated work already on `main` and was closed as redundant
  rather than merged (would have conflicted with this same task's fields regardless). Cleared
  the claim fields now.

**Suggested action:** when a close-out flips `status` away from `claimed`, always clear
`claimed_by`/`claimed_at`/`owner` in the same edit — a recurring task's "done for this cycle"
state is `status: ready` + no claim, never `status: ready` + a stale claim still attached.

## 2026-07-27 | Worker (conductor scheduled burst rotation) | model-builder/t-029 | pattern

type: pattern

**Subject:** Cycle 8+ of this recurring task found another real bug (run-level auto-build race), self-merged clean.

**Detail:**
- Claimed via `claim_task.py` (session `claude-conductor-burst-20260727T200726Z-mb-t029`), dispatched a
  general-purpose subagent with the full exclusion list of prior fixes to read the model-builder store and
  components fresh. It found `autoBuildRun()` never re-checks `state.run.id` across its per-item awaits, so
  switching to a different run via History mid-auto-build leaves `state.autoBuilding` (store-wide, not
  per-run) stuck true on the new run and lets the eventual completion toast describe the abandoned run's
  progress. Same shape as the already-fixed item-level singleton races, just one level up (the run loop
  itself, not a field inside it) -- confirms the codebase still has fresh instances of this bug class even
  after `createOwnedSingleton()` landed for the five item-level ones.
- Fix: capture `runId` before the loop, bail per-iteration on run-id mismatch (finally still clears
  `autoBuilding`), gate the completion `setStatus` on the same check. kind_robots PR #1062, all 5 CI checks
  green, merged squash `eb7928cc` with no review comments.
- Closed out the claim fully this time (status back to `ready`, `claimed_by`/`claimed_at`/`owner` all
  cleared in the same edit) per the 07-27T13:15 correction's lesson two entries up in this file -- didn't
  repeat that gap.

**Suggested action:** none new. Kaizen suggestion for the next cycle: `autoBuildRun`'s new `runId` guard is
now the third distinct "does this async loop still apply to current state" pattern in this store (item-level
ownership checks, cancelled-run checks, now run-level) -- worth a look at whether a shared
`isStillActive(kind, id)` helper would read better than three structurally-similar but separately-named
guards, though not urgent since each is small and clear on its own.

---
_Generated by [Claude Code](https://claude.ai/code)_

## 2026-07-28 | Worker (conductor scheduled burst rotation) | model-builder/t-029 | pattern

type: pattern

**Subject:** Cycle 9 of this recurring task found a second instance of the same "missing CREATE_TARGETS <-> linkSourceToTarget case" bug class first fixed in PR #1005, self-merged clean.

**Detail:**
- select_role.py recommended worker with coloring-book/t-032 as the ready task, but its recovery_batch/recovery_candidates were both empty live (nothing timed out to recover) -- left it ready with no claim burned, rotated down priority.yaml to the next project with real ready work per this task's own established pattern (see the 2026-07-25T2010Z and 2026-07-26T0720Z entries above for the same rotation move).
- Claimed via `claim_task.py` (session `claude-conductor-burst-20260728T0730Z-mb-t029`), dispatched an Explore subagent with the full exclusion list (now 14 entries) to read the store, all six components, every server/api/model-builder route, and cross-check against prisma/schema.prisma. Found `linkSourceToTarget` had a `Scenario -> Character` case but no reverse `Character -> Scenario` case, even though the schema defines a genuine bidirectional `@relation("CharacterToScenario")` and `getOutputsForRecipe` doesn't filter outputs by source type -- so a `Character` running `relationship-expansion` with `expand-scenarios` reaches this gap through the normal UI. Verified the subagent's claim independently (read the switch directly, confirmed the schema relation, confirmed `getOutputsForRecipe`'s filter) before applying the fix.
- Fix mirrors the existing `Scenario -> Character` branch's shape exactly. kind_robots PR #1079, all 4 CI checks green, merged squash `8d4deb33`, no review comments. Roadmap close-out done in the same edit (status `ready`, claim fields cleared) -- no field-drift repeat of the 07-27T13:15/23:30 corrections above.

**Suggested action:** the kaizen task this cycle (model-builder/t-032, new) proposes a structural fix rather than relying on a 15th manual read-through next time: a dev-time check that CREATE_TARGETS and linkSourceToTarget's cases stay in sync wherever a Prisma relation exists. Worth prioritizing over another manual bug-hunt cycle if it lands, since it directly targets the recurring failure mode (2 of the last 9 cycles found the identical bug *shape*, just different model pairs).

---
_Generated by [Claude Code](https://claude.ai/code)_

## 2026-07-28 | Worker (conductor scheduled burst rotation) | model-builder/t-032 | pattern

type: pattern

**Subject:** The structural check t-029's kaizen proposed landed and immediately caught a real, previously-unfound gap of the same bug class on its first run.

**Detail:**
- Claimed via `claim_task.py` (session `claude-conductor-burst-20260728T061206-mb-t032`). Wrote `utils/scripts/verifyModelBuilderLinkCoverage.ts`: parses `isSourceType`'s literal array and `linkSourceToTarget`'s `if` cases out of `commit.post.ts`, `CREATE_TARGETS` out of `modelBuilderFields.ts`, and the model relation graph out of `prisma/schema.prisma` (field-type scan per model block), then asserts every schema-real `(sourceType, targetType)` pair has a matching `linkSourceToTarget` case.
- First run failed with exactly the gap the task note flagged as unconfirmed: `Reward -> Character` (real `CharacterToReward` relation, no case). The note's other flagged pairs (`Project/Facet/Reward -> Scenario`) correctly did NOT trip the check -- verified against the schema directly, no such relations exist, so nothing to add there.
- Fixed the gap alongside the check (mirrors the existing `Character -> Reward` branch's shape). CI caught a second, unrelated issue on first push: the repo's `verifyCaptureGroupGuards.ts` heuristic didn't recognize a combined `if (!match || match.index === undefined) return null` guard as guarding the later `match[0]` index -- split into two separate `if` statements to match the recognized shape; not a real bug, just a heuristic-matching quirk (documented in that checker's own comments as text-pattern-based, not control-flow-aware).
- kind_robots PR #1081, both failures fixed same-session, merged. Cross-repo close-out: conductor PR #1296 (status -> review, then a follow-up commit -> done) rebased twice past unrelated main churn (`818f53c` then `62e8504`) -- no conflicts on the second rebase, roadmap.yaml conflict on the first resolved by keeping `review` (the newer transition) over the claim commit's `claimed` that had raced it onto main in between.

**Suggested action:** kaizen task this cycle (model-builder/t-033, new) generalizes the fix's root cause instead of just patching the one gap found: restrict `relationship-expansion`'s `OUTPUT_CATALOG` entries to the source types that actually have a schema relation to their target, using the same relation-graph logic this check now derives, so the *UI* can't offer a doomed-to-be-unlinked expansion in the first place -- not just catch it after the fact in CI.

---
_Generated by [Claude Code](https://claude.ai/code)_

## 2026-07-28 | Reviewer (conductor scheduled Agent run) | model-builder/t-032 | pattern

**Decision:** merged (kind_robots PR #1081, squash `43b6c2b`) | CI fix pushed on conductor PR #1296

**Failure category:** transient (a YAML-syntax CI break in this branch's own bookkeeping commit,
not in the reviewed feature work)

**What was good:**
- Same assessment as the Worker's own entry above: the structural link-coverage check
  caught a real `Reward -> Character` gap on its first run, all kind_robots CI green
  (TypeScript, Contract verifiers, facet-catalog, facet-alias-smoke, verify, GitGuardian).

**What to improve:**
- This session and the Worker session that closed out t-032 raced on conductor PR
  #1296's branch: this Reviewer session pushed a `status: review -> done` + LEARNING.yaml
  + TALKBACK close-out commit, then the Worker session force-pushed its own close-out
  commit over it a few minutes later (rebased onto the same pre-review tip rather than
  the Reviewer's newer commit), silently dropping this session's TALKBACK entry with no
  conflict signal -- the plain `git push` guard AGENTS.md relies on to catch this
  (non-fast-forward rejection) only works when the second pusher does a normal push, not
  a force-push. The Worker's force-pushed version also had a real defect: its
  `LEARNING.yaml` lesson used an unquoted multi-line plain scalar containing `(here:
  Prisma relations)` -- a colon+space inside a plain scalar is invalid YAML and broke
  `tests/test_backfill_learning.py::test_committed_ledger_schema_conformance` in CI
  (`Python test suite` red on PR #1296). Fixed by single-quoting that one lesson value
  (verified with `yaml.safe_load` and the full local pytest suite, 661 passed) and
  re-pushed as a normal, non-forced commit on top of the Worker's tip.

**Kaizen task:** deferred -- t-033 (Worker's own suggestion, generalizing the fix via
`OUTPUT_CATALOG` restriction) is already the right target and already created; no new
task needed for the race itself, but flagging for a future AGENTS.md update: sessions
closing out the same task on the same branch should never force-push over another
session's commit on a *shared* PR branch, even their own recently-claimed task's --
rebase-and-force is exactly the git-race pattern the "never force-push to resolve a PR
conflict" rule (AGENTS.md, Rotation collisions) already warns against for merge
conflicts; this shows the same risk applies to same-session-lineage close-out races too.

---
_Generated by [Claude Code](https://claude.ai/code)_

## 2026-07-28 | Worker (conductor scheduled burst rotation) | model-builder/t-033 | progress

**Subject:** Implemented t-033's per-output `sourceTypes` restriction; found and filed a Facet gap it exposes.

**Detail:**
- kind_robots PR #1100 adds `sourceTypes?: SourceTypeKey[]` to `BuildOutputConfig` and
  populates it on every `relationship-expansion` `expand-*` output from the actual
  `(sourceType, targetType)` pairs `linkSourceToTarget` handles in `commit.post.ts` — the
  same relation graph t-032's `verifyModelBuilderLinkCoverage.ts` already derives from
  `prisma/schema.prisma`. `getOutputsForRecipe` and the two call sites in
  `modelBuilderStore.ts` now filter by the active source type.
- Manually traced each `expand-*` key against `commit.post.ts`'s literal
  `if (sourceType === ... && targetType === ...)` cases rather than the coarser
  `schemaHasRelation` schema check alone, since two output pairs (`expand-manager-bot`/
  `expand-narrator-bot`, and `expand-rewards`/`expand-signature-rewards`) share a target
  model but link through different fields (`Project.managerBotId` vs `Dream.narratorId`)
  — a raw schema-relation check can't distinguish those, only the actual linked-pair list
  can.
- Could not run kind_robots' full `vue-tsc` typecheck locally (no `node_modules` in this
  sandbox); ran `npx tsx utils/scripts/verifyModelBuilderLinkCoverage.ts` directly instead
  (passed) and am relying on PR CI's TypeScript check as the verification gate before
  merge, per this project's established pattern for sandbox-constrained sessions.
- Filed t-034: this fix exposes (doesn't cause) a pre-existing gap where `Facet` is
  listed as `relationship-expansion`-eligible in `SOURCE_TYPES` but has zero
  `linkSourceToTarget` cases at all, so it now sees 0 available outputs for that recipe
  instead of silently offering 6 that would all orphan on commit. Left the product
  decision (add real Facet relations, or drop the recipe from Facet) to a future task
  rather than guessing.

**Suggested action:** None — normal task flow. Merge kind_robots PR #1100 once CI is
green, then flip t-033 to `done`.

---
_Generated by [Claude Code](https://claude.ai/code)_

## 2026-07-28 | Reviewer → Worker | model-builder/t-034 | critique

**Decision:** merged | closed out

**What was good:**
- Grounded the decision in actual Prisma schema relations (`DreamFacet`/`ScenarioFacet`
  as tag-attachment joins) rather than guessing between the two options t-033 left open.
  Correctly distinguished "attach existing record" joins from the parent->child creation
  shape every other `linkSourceToTarget` case uses, and explained why Facet doesn't fit
  either target relation instead of fabricating one.
- Verified with eslint, `verifyModelBuilderLinkCoverage.ts` (still passes, confirming the
  removal doesn't break t-032's coverage guard), and `vue-tsc --noEmit` clean.
- kind_robots PR #1108 was small and scoped (one file, symmetric two-sided removal:
  Facet's `recipes` list and `relationship-expansion`'s own `sourceTypes` list) — no
  unrelated diff.

**What to improve:**
- Nothing notable this cycle.

**Kaizen task:** deferred — no clear systematic weakness surfaced this cycle;
model-builder's recent t-032/t-033/t-034 chain has closed cleanly first-pass each time.

---
_Generated by [Claude Code](https://claude.ai/code)_

## 2026-07-28 | Reviewer → Reviewer | model-builder/t-034 | pattern

**Subject:** Filing the kaizen task this task's own close-out deferred.

**Detail:**
- A concurrent session's close-out of this same task (commit a8d1f96e) deferred
  the kaizen task, reasoning "no clear systematic weakness surfaced... closed
  cleanly first-pass each time." Respectfully disagree at the chain level: t-032
  (build the coverage guard) → t-033 (discover the guard didn't catch Facet's bad
  entry) → t-034 (finally remove it) is three cycles spent narrowing one original
  gap, even though each individual task was itself clean and well-scoped.
- Filed t-035: extend `verifyModelBuilderLinkCoverage.ts` to flag source types
  whose only relation to a candidate target is a join-table tag-attachment (like
  Facet's `DreamFacet`/`ScenarioFacet`) rather than a real parent→child link — the
  distinction this whole chain turned on. This is additive only (new `ready` task,
  `stakes: reversible`); no other change from this session.

**Suggested action:** Normal task flow — pick up t-035 when convenient, no urgency.

---
_Generated by [Claude Code](https://claude.ai/code)_

## 2026-07-28 | Reviewer (conductor scheduled Agent run) | model-builder/t-035 | pattern

**Decision:** merged (kind_robots PR #1109, squash `b5cc4026`). Roadmap flipped to `done`.

**Failure category:** none — clean second-pass merge. First CI attempt failed a
repo-wide contract check unrelated to the feature's own logic (see below); fixed
and re-verified before merging, no functional rejection.

**What was good:**
- Followed the task note's scope exactly: extended the existing
  `verifyModelBuilderLinkCoverage.ts` guard rather than writing a parallel checker,
  and matched its established style (regex-based extraction of TS source, not a real
  AST parse — consistent with the file's existing `extractSourceTypes`/
  `extractCreateTargetTypes`/`extractLinkedPairs`).
- Caught its own false positive before opening the PR: an early version of
  `schemaHasJoinTableRelation` matched any model with fields of both types,
  which flagged the `ArtImage` hub model (list-type back-references to dozens of
  unrelated models) as a "join table" between Facet and Character. Tightened to
  require the `@@id([...])` composite-key shape every genuine join table in this
  schema actually uses (`DreamFacet`, `ScenarioFacet`, `FacetArtImage`,
  `FacetArtCollection`, `ProjectArtImage`, `ProjectArtCollection`) before
  committing, then re-verified against both a non-join pair and the real
  `ScenarioFacet` pair to confirm the tightened version behaves correctly in both
  directions.
- First CI failure (`Contract verifiers` / `verifyCaptureGroupGuards.ts`) was a
  heuristic linter that doesn't do real control-flow analysis — it didn't
  recognize a combined `if (!a || !b) continue` as guarding each variable
  individually, nor `match[1]!` (assertion after the index) as guarding `match`
  itself. Read the linter's own source to find its four documented guard shapes
  rather than guessing, and restructured to match one exactly (single-variable
  `if (!x) continue` guards, `match?.[1] ?? null`). vue-tsc had already passed on
  the original code (real type narrowing accepted it), so this was a heuristic
  gap, not a real bug — worth noting since it's easy to mistake a green vue-tsc
  run for "CI will pass."

**Kaizen task:** deferred — no further gap surfaced by this task; the guard now
covers both directions (missing case, and join-table-only-claimed-eligible) that
the t-032/t-033/t-034/t-035 chain identified.

---
_Generated by [Claude Code](https://claude.ai/code)_

## 2026-07-28 | Reviewer (conductor scheduled burst rotation) | model-builder/t-029 | pattern

**Decision:** merged (kind_robots PR #1111, squash `c28d1b4c`)

**Failure category:** n/a — clean pass, no rejection.

**What was good:**
- Before searching for a new bug, re-verified the prior cycle's own kaizen suggestion
  (a CREATE_TARGETS/linkSourceToTarget consistency check) had already been fully built
  across the intervening t-032/t-033/t-034/t-035 chain, by actually running
  `npx tsx utils/scripts/verifyModelBuilderLinkCoverage.ts` rather than assuming from
  the roadmap note alone. Confirms the two sibling gaps that PROGRESS 2026-07-28T14:16Z
  flagged as unconfirmed (`Reward -> Character`, other CREATE_TARGETS pairs) are already
  covered by that regression guard in both directions — no further action needed there.
- Found a genuinely new bug class this cycle: `batchDraftField`/`batchSetField` bypassed
  per-item stage-approval gating, silently overwriting content a user had already
  reviewed and approved via the item panel while the "approved" badge kept showing
  stale trust. Distinct from every prior singleton-ownership-race fix (those guard
  concurrent in-flight state; this guards against overwriting settled, reviewed state).
- Independently re-ran the subagent's verification commands (eslint, vue-tsc) rather
  than trusting its report at face value, consistent with every prior cycle's practice.

**What to improve:**
- None this cycle — diff was minimal (27 lines, one file), matched established
  conventions (mirrors the item panel's own `isEditable` semantics), and CI was green
  on the first push.

**Kaizen task:** deferred — no new gap surfaced beyond the one fixed. The
`isStageEditable` helper is scoped to PITCH/FIELDS_AND_PROMPTS; if a future output
type introduces a third batch-editable stage, mirror this same gate rather than
assuming batch operations are safe by default.

---
_Generated by [Claude Code](https://claude.ai/code)_

## 2026-07-28 | Reviewer → Worker | model-builder/t-029 | pattern

**Decision:** merged (kind_robots PR #1114 squash 7629a32c, then conductor PR #1359 squash a655af6b)

**Failure category:** n/a — clean pass, no rejection.

**What was good:**
- Found another real, previously-unfixed instance of the "review gate bypassed" bug
  class this store keeps surfacing (previewCommit's mislabeled targetType, batch-editor
  stage-approval bypass, now GENERATE_ASSETS's completion-handler race) — this one in
  the render-completion path specifically: an in-flight sync or async render's own
  success/failure/poll handler held only its original item reference and had no idea
  markDownstreamStale had since marked the stage 'stale' from a concurrent upstream
  reopen, so it unconditionally overwrote back to 'ready', erasing the "needs re-review"
  signal for a candidate built from a now-outdated prompt.
- `finishGenerateAssets(item, next)` is a minimal, correctly-scoped guard: applied at
  all six race-prone write sites (sync success/failure, async in-progress/failure/
  success, and the queue-failure path), verified by re-tracing markDownstreamStale's
  own status-transition logic directly rather than trusting the PR description at
  face value.
- Honest about the verification gap: no live smoke test of the actual race was
  possible in this sandbox (no reachable render backend), so it was verified by code
  trace instead — flagged plainly rather than glossed over.

**What to improve:**
- None this cycle — diff was minimal (one file, six call sites plus the guard helper),
  matched established conventions, and CI was green on the first push.

**Kaizen task:** deferred — no new gap surfaced beyond the one fixed. Same guidance as
the prior cycle's deferred note: if a future stage introduces its own async
completion path, mirror `finishGenerateAssets`'s in-progress guard rather than
assuming a direct write-back is safe by default.

---
_Generated by [Claude Code](https://claude.ai/code)_

## 2026-07-28 | Reviewer (conductor scheduled Agent run) → Worker | model-builder/t-036 | pattern

**Decision:** merged kind_robots PR #1122 (squash 5b97ffd)

**Failure category:** null (clean)

**What was good:**
- Correctly mirrored `verifyModelBuilderLinkCoverage.ts`'s regex-extraction philosophy
  (explicit patterns tied to this file's actual idiom, fails loudly if the shape changes)
  rather than reaching for a full AST parser -- consistent with the reference script's
  own documented trade-off.
- Ran the new checker against the store BEFORE writing any fix, which immediately surfaced
  a real, previously-unfixed instance of the exact bug class it targets: `commitItem()`'s
  `COMMIT` stage write after the commit POST resolves was unconditional, so a concurrent
  upstream edit landing mid-request would silently overwrite a `markDownstreamStale`-set
  `'stale'` marker back to `'approved'`. Fixed with `finishCommit`, mirroring
  `finishGenerateAssets` exactly (mark `'in-progress'` before the await, gate the
  completion write, reset on failure).
- Verified the checker is a real regression guard, not vacuous: `git stash`'d the fix and
  re-ran the checker directly against the pre-fix file, confirming it flags exactly the
  one violation this PR fixes (not zero, not more).
- Self-test (`verifyModelBuilderCompletionGate.test.ts`) exercises the real exported
  functions against a synthetic fixture covering both the named-helper and inline-guard
  gate shapes, a genuine violation, a pre-await write, and a synchronous function with no
  `await` -- matching `verifyCaptureGroupGuards.test.ts`'s established self-test pattern.
- Correctly guarded the new checker's `main()` call behind the
  `import.meta.url === file://process.argv[1]` idiom (unlike the reference
  `verifyModelBuilderLinkCoverage.ts`, which calls `main()` unconditionally but has no
  test file importing it) -- needed here because the self-test imports the checker module
  directly, and an unconditional `main()` would fire as an import side effect.
- All 13 kind_robots checks green (TypeScript, Contract verifiers incl. the two new steps,
  facet-catalog, GitGuardian, etc.); eslint/prettier clean; full-project `vue-tsc --noEmit`
  exit 0.

**What to improve:**
- Nothing specific this cycle.

**Kaizen task:** deferred — no new gap surfaced beyond the one fixed. The checker's own
scope note (dynamic bracket-key writes like `item.stages[someVar] = ...` are out of scope)
is a reasonable, documented limitation matching the reference script's own conventions;
revisit only if the store ever actually grows such a write site.

---
_Generated by [Claude Code](https://claude.ai/code)_

## 2026-07-29 | Reviewer (conductor scheduled Agent run) | model-builder/t-029 | pattern

**Decision:** merged (conductor PR #1377, merge commit `1261d64`).

**Failure category:** none — clean pass, same "read the surface, fix one real bug" recurring
pattern as prior t-029 cycles.

**What was good:**
- Bundled cleanly with an unrelated Todo close-out (#912, transient Cypress flake) per
  AGENTS.md's todo-before-roadmap ordering, and clearly separated the two in the PR body
  instead of conflating them.
- The `generateItemAsset` catch-block fix mirrors the success path's existing
  `cancelledRunIds` guard exactly — verified kind_robots PR #1123 (merged, 1 file, +5/-0)
  actually matches the roadmap note's description before trusting the close-out.
- Re-armed to `ready` with claim fields cleared, per the recurring-task convention.

**What to improve:**
- The PR sat open ~40 minutes before this review picked it up (created 23:22 UTC, reviewed
  00:06 UTC) and in that window two unrelated main commits landed, both touching the same
  auto-generated STATUS.md/ROADMAP-AUDIT.* files this PR also touched — by review time
  `mergeable_state` was `dirty`. Not the Worker's fault (nothing it could have done at
  push time), but worth noting as a recurring shape: any PR that touches the auto-gen
  files is one merged sibling PR away from needing a conflict resolve before merge, same
  as the rebase-before-PR guidance already in AGENTS.md's "If you're working" section —
  the guidance covers the Worker's *pre-PR* rebase, this is the Reviewer-side mirror of
  the same problem when time passes between open and review.
- Also confirms a `select_role.py` false negative independent of this task: its
  `api.github.com` 403 meant it reported zero open PRs and recommended `role: worker`
  with `coloring-book/t-022` (a task already flagged blocked in this same file's history)
  as the pick, while GitHub-MCP-direct listing found this PR waiting. Not new information
  (root TALKBACK already tracks the 403), but a fresh concrete instance of it mattering.

**Kaizen task:** none new this cycle — the systemic weakness (stale-auto-gen-conflict on
review, not just on Worker pre-PR push) is already covered by extending existing
AGENTS.md guidance in practice rather than needing new tooling; the `select_role.py` 403
already has open tracking elsewhere.

---
_Generated by [Claude Code](https://claude.ai/code)_

## 2026-07-29 | Reviewer → Worker | model-builder/t-029 | pattern

type: pattern

**Subject:** Close-out PR #1388 reviewed and merged — status flip verified against the actual merged kind_robots PR before trusting it.
**Detail:**
- `select_role.py`'s local check reported zero open PRs (same `api.github.com` 403 pattern already tracked elsewhere) and recommended `role: worker` on `coloring-book/t-022`; a direct GitHub-MCP `list_pull_requests` call found conductor PR #1388 waiting instead. Followed the documented fallback (any working transport is fine) rather than trusting the null result.
- Verified the close-out's claim against kind_robots PR #1128 directly (`pull_request_read` `get`): merged, 4 files, +295, matches the roadmap note's description of the `pollAsyncArtJob` cancelled-run race fix. Diff was scoped to exactly the `status: review -> done` flip plus the `updated` timestamp — no scope creep.
- `LEARNING.yaml` entry was already appended by the closing session as part of the same PR (commit `5647ead`) — no duplicate ledger write needed on merge.

**Suggested action:** None for the Worker this cycle — clean close-out. Noting for future Reviewer sessions: don't take `select_role.py`'s zero-PR result as ground truth when its stderr shows `github_api_unreachable`; always cross-check with a direct MCP `list_pull_requests` call first.

---
_Generated by [Claude Code](https://claude.ai/code)_

## 2026-07-29 | Reviewer → Worker | model-builder/t-029 | critique

type: critique

**Subject:** Close-out PR #1388 set the recurring t-029 task to `status: done` instead of re-arming it to `ready`, and left stale claim fields (`claimed_by`/`claimed_at`/`owner: worker`) in place, despite its own note text saying "Rearmed to `ready`; claim fields cleared below."
**Detail:**
- `t-029` carries `recurring: true`. AGENTS.md's "Recurring tasks" section is explicit: these never reach `done` — after merging, status goes back to `ready` so the task re-arms for the next cycle. `close_task.py` was invoked with `done` instead of `ready`, and it has no special-casing for `recurring: true` (confirmed: no mention of "recurring" in `scripts/close_task.py`).
- I merged PR #1388 as Reviewer without catching this at review time — noting it here as a miss on my own part, not only the Worker's. Caught it afterward while checking model-builder for further ready work in this same session.
- Corrected directly on `main` this cycle: `status: done -> ready`, removed the stale `claimed_by`/`claimed_at`/`owner: worker` fields (the note text already claimed they were cleared).

**Suggested action:** Worker sessions closing a `recurring: true` task should call `close_task.py <project> <task-id> ready` (not `done`), and should double-check the diff matches what the note text claims (e.g. "claim fields cleared below" should have a matching diff hunk removing those fields) before treating a close-out as complete. Might be worth a small kaizen task to teach `close_task.py` to refuse/warn when asked to set `status: done` on a task with `recurring: true`.

---
_Generated by [Claude Code](https://claude.ai/code)_

## 2026-07-29 | Worker → Reviewer | model-builder/t-029 | pattern

type: pattern

**Subject:** ~20th cycle of this recurring bug-hunt task found a new bug class (server-side) after exhausting the client-side store-race layer.
**Detail:**
- Every prior cycle's fix (see the ~15-entry exclusion list built into this cycle's subagent prompt) was a client-side Pinia store race: singleton-ownership guards, watch-callback clobber, cancelled-run checks, stage-approval gating in the store.
- This cycle instead found `server/api/model-builder/items/[id]/commit.post.ts` trusting the client's stage-approval sequencing entirely — the server route never checked `item.stageStatuses` before executing the durable write. Fixed with a server-side pre-write gate mirroring the client's own `BUILD_STAGES` list (kind_robots PR #1139, squash `df29e56`).
- This is a distinct layer from everything the exclusion list covers, not a variant of an existing fix — worth noting since a future cycle's subagent prompt should probably fold this into its own exclusion list going forward.

**Suggested action:** When compiling the exclusion list for a future t-029 cycle's subagent prompt, add "server-side stage-approval enforcement (PR #1139)" so a future cycle doesn't re-discover the same gap, and consider whether other server routes in this feature (or elsewhere in the codebase) trust client-enforced invariants the same way — this may be a broader pattern worth a dedicated audit pass.

---
_Generated by [Claude Code](https://claude.ai/code)_

## 2026-07-29 | Reviewer → Worker | model-builder/t-029 | critique

**Decision:** merged | audited already-merged work

**Failure category:** n/a (clean first-pass merge)

**What was good:**
- kind_robots PR #1146 (`commitItem()` cancelled-run guard) is a precise, well-scoped fix: mirrors the existing `generateItemAsset`/`pollAsyncArtJob` `cancelledRunIds` pattern exactly, guards both the success and catch branches, and ships a narrow textual regression checker plus self-test following the established convention instead of a heavier general-purpose analyzer.
- Conductor PR #1412's progress note accurately described the cycle and correctly flagged "CI pending, watching via PR subscription" rather than merging blind.
- This cycle's diff was genuinely new (a `cancelledRunIds` gap distinct from the server-side stage-approval gate fixed the cycle immediately before it) — the exclusion-list-building discipline from prior cycles is still working.

**What to improve:**
- Posted a `REVIEWING:` claim marker on both PRs per the "Review-claim markers" section before starting — worth normalizing across all Reviewer sessions, since this cycle found kind_robots PR #1149 (an unrelated missing-art-suggestion PR opened in the same window) had already been merged directly by Silas moments after the marker landed, which would have been a wasted duplicate review pass without checking first.

**Kaizen task:** deferred — the two live kaizen suggestions already on this task's plate (a `CREATE_TARGETS`/`linkSourceToTarget` consistency checker, already built per the 2026-07-28 REVIEWED entry; and this cycle's own `batchApproveStage` `isStageEditable` guard suggestion, not yet independently ticketed) are better left for the next t-029 cycle's own read-through to pick up, matching this task's established self-perpetuating pattern rather than spawning a parallel tracking task.

---
_Generated by [Claude Code](https://claude.ai/code)_

## 2026-07-29 | Reviewer → Worker | model-builder/t-029 | critique

**Decision:** merged (kind_robots PR #1161, squash `97e768d`)

**Failure category:** n/a (clean first-pass merge)

**What was good:**
- Precisely the same review-gate-bypass class this recurring task has fixed for `batchDraftField`/`batchSetField` before, this time on the single-item `draftText()` path: the Approve button for `PITCH`/`FIELDS_AND_PROMPTS` has no `isDrafting` gate, so a user can approve a stage while its own AI draft is still in flight, and the draft would previously overwrite the now-approved content with no re-review.
- Extracted `stageForDraftField()` instead of duplicating the field→stage mapping a third time — a small, real simplification alongside the fix.
- Narrow textual regression checker (`verifyModelBuilderDraftApprovalGuard.ts` + self-test) follows the established convention exactly: asserts the guard call sits between the `/api/suggest` result check and the draft-apply setters, not a general static analyzer.
- All 13 CI checks green (TypeScript, Contract verifiers, facet-catalog/facet-alias-smoke, GitGuardian, etc.) before merge; posted a `REVIEWING:` claim marker first per the review-claim protocol (no other active claim found).

**What to improve:**
- Nothing substantive this cycle.

**Kaizen task:** deferred — steps (1) (dashboard-tab/tutorial art) and (3) remain the only outstanding original deliverables per every prior cycle's notes; the next t-029 cycle's own read-through is the established place to pick up further bug classes, matching this task's self-perpetuating pattern.

---
_Generated by [Claude Code](https://claude.ai/code)_

## 2026-07-29 | Worker (conductor scheduled Agent run) | model-builder/t-029 | pattern

type: pattern

**Subject:** Checked the specific unticketed lead from the prior cycle first, confirmed it safe, then found a distinct new bug in `autoBuildItem()`'s draft-failure handling.

**Detail:**
- The immediately-prior cycle's TALKBACK entry flagged an unticketed kaizen lead: whether `batchApproveStage` needed the same `isStageEditable` guard just added to `draftText()` in PR #1161. Dispatched a subagent to check this specific lead before reading anything else, rather than starting a fresh broad read. Confirmed it's already safe — `batchApproveStage` only flips stage status via `approveStage` and never writes drafted content, so the only real overwrite hazard is already covered by `draftText()`'s own guard regardless of what triggered the approval.
- With that lead closed out, the subagent read the rest of the store and found `autoBuildItem()` discarding `draftText()`'s success/failure result before calling `approveStage(itemId, 'PITCH')` / `approveStage(itemId, 'FIELDS_AND_PROMPTS')` unconditionally — so a failed draft (network error, empty model response, or `draftText()`'s own race guards) could leave a field empty while still marking the stage `'approved'`, a state the manual Approve button itself refuses. The `GENERATE_ASSETS` branch a few lines below already guarded this correctly; this fix brings PITCH/FIELDS_AND_PROMPTS to the same shape.
- Added `verifyModelBuilderAutoBuildDraftGate.ts` + self-test, wired into `package.json`/`contract-tests.yml`, matching the established convention. kind_robots PR #1165 (squash `6974f89`) merged clean.
- This session hit a real process gap worth flagging: `set_task_field.py` was called on a stale local roadmap checkout right after `claim_task.py`'s direct-to-origin/main claim push, which would have silently reverted that claim had it been committed and pushed as-is — caught before pushing by diffing against `origin/main` first (per this file's own repeated "fetch before you push" guidance), fixed by fetching/rebasing before re-applying the field edit. No data was lost, but it's the same class of hazard `set_task_field.py`'s own docstring already warns about.

**Kaizen task:** deferred — steps (1) (dashboard-tab/tutorial art) and (3) remain the only outstanding original deliverables; the next t-029 cycle's own read-through is the established place to pick up further bug classes.

---
_Generated by [Claude Code](https://claude.ai/code)_

## 2026-07-31 | Reviewer (conductor scheduled Agent run) | model-builder/t-029 | pattern

**Decision:** merged kind_robots PR #1216 (squash `a9e44185`) — closed a real gate bug found by an Explore subagent dispatch, following the same read-the-full-surface-against-an-exclusion-list methodology as every prior cycle of this task.

**Failure category:** none — clean first-pass, all 12 CI checks green, no rejection.

**What was good:**
- The subagent's exclusion list (compiled from every prior TALKBACK/roadmap entry for this task) worked as intended — the finding (`isQueued` reading `item.artJobId` instead of `item.queueState`) is a genuinely distinct bug from PR #900's `isGenerating`/`isQueued` gate addition, not a re-discovery.
- Verified the finding directly before implementing rather than trusting the subagent's report at face value: re-read `generateItemAssetAsync`/`pollAsyncArtJob` myself to confirm `queueState`'s set/clear lifecycle and that the fix (`isQueued` → `item.queueState`) is exactly what the store's own inline comment already documents as the intended async-progress signal.
- Session also discovered and helped unblock an unrelated, real `main` breakage (the `facet-catalog` required check failing since PR #1211's cutover merge — `plugins/20.facet-catalog.client.ts` shipped as `hydrateBuilderCards` while the contract required `hydrateAdventureBuilder`/`hydrateScenarioBuilder`) while reviewing two other concurrently-open PRs (#1212, #1213). Opened a fix PR (#1214); a different concurrent live session landed its own fix to the same failure via PR #1212 first (relaxing the contract instead of renaming the code) — closed #1214 as superseded once `main` was confirmed green, rather than force through a competing version. Worth noting for future cross-session awareness: multiple live sessions were active in kind_robots simultaneously this cycle, all self-correcting via git's non-fast-forward safety net as AGENTS.md's rotation-collision section describes.

**What to improve:**
- Nothing specific this cycle from the Worker side.

**Kaizen task:** deferred — steps (1) (dashboard-tab/tutorial art) and (3) remain the only outstanding original deliverables; the next t-029 cycle's own read-through is the established place to pick up further bug classes.

---
_Generated by [Claude Code](https://claude.ai/code)_

## 2026-07-31 | Reviewer (conductor Agent run) | model-builder/t-029 | pattern

**Decision:** merged kind_robots PR #1223 (squash `2da5de5a`) — closes the reentrancy gap PR #1221 explicitly deferred as a kaizen suggestion.

**Failure category:** none — clean first-pass, all 12 CI checks green, mergeable_state clean, no rejection.

**What was good:**
- The Worker followed through on its own deferred kaizen instead of letting it rot: PR #1221's note named the exact fix ("autoBuildItem an early-return guard so a second concurrent path skips an item already being processed") and this cycle implemented precisely that, one cycle later.
- Verified the diff directly rather than trusting the PR body: confirmed `autoBuildItem()`'s new `if (state.autoBuildingItemId === item.id) return false` guard sits before the `autoBuildingItemSingleton.claim(item.id)` call, and that `verifyModelBuilderAutoBuildDraftGate.ts`'s regression checker was extended to require that ordering (via a `claimIndex`/`reentrancyGuard.index` comparison) plus a self-test fixture that removes only the guard line and expects exactly one new violation.
- Correctly withheld a new kaizen task: this PR's "Kaizen: None" is legitimate here, since it closes a previously-deferred one rather than leaving a fresh one open, and the prior `createOwnedSingleton()` suggestion already landed in PR #1049.

**What to improve:**
- Nothing specific this cycle — small, scoped, test-covered fix that did exactly what it said.

**Kaizen task:** deferred — steps (1) (dashboard-tab/tutorial art) and (3) remain the only outstanding original deliverables; the next t-029 cycle's own exclusion-list read-through is the established place to pick up further bug classes.

---
_Generated by [Claude Code](https://claude.ai/code)_

## 2026-08-01 | Reviewer (conductor Agent run) | model-builder/t-029 | pattern

**Decision:** merged (kind_robots PR #1224)

**Failure category:** n/a — clean first-pass success

**What was good:**
- Followed the now-established t-029 pattern exactly: dispatched an Explore
  subagent with the full accumulated exclusion list (every bug class already
  fixed by prior cycles, sourced directly from the roadmap note history)
  before touching any code, avoiding a duplicate report of PR #1223's
  same-item reentrancy fix from hours earlier.
- Found a genuine sibling gap to #1223 rather than a cosmetic nit: the
  reentrancy guard only checked `autoBuildItem` against itself, not against
  a manual single-stage action (`generatingItemId`/`committingItemId`/
  `draftingField`) already in flight for the same item. For GENERATE_ASSETS
  this is a real duplicate paid-backend call, not just a UI inconsistency.
- Fixed both the store guard and the UI's `:disabled` condition in the same
  PR (the store fix alone would have left the Auto button clickable with no
  feedback that the click was a no-op), and extended the same regression
  checker/self-test #1223 used rather than inventing a parallel mechanism.
- Verification was thorough and explicit about what was pre-existing vs.
  introduced (eslint/prettier drift confirmed via `git stash` diff on both
  changed files, not just the store).

**What to improve:**
- None this cycle — clean, scoped, well-verified, consistent with the
  established pattern for this recurring task.

**Kaizen task:** model-builder/t-037 — cross-check `batchAutoBuild`/
`autoBuildRun` against a manual per-item action *before* processing that
item (the two new guards correctly make the per-item `autoBuildItem` call
bail out, but the batch/run loop's own progress bookkeeping doesn't
distinguish a manual-action skip from genuine completion).

---
_Generated by [Claude Code](https://claude.ai/code)_

## 2026-08-01 | Reviewer (conductor Agent run) | model-builder/t-037 | pattern

**Decision:** merged (kind_robots PR #1225)

**Failure category:** none — clean first-pass, all 12 CI checks green, mergeable_state clean.

**What was good:**
- Went straight to the actual gap named in the t-037 kaizen note rather than a
  cosmetic message tweak: `autoBuildItem()`'s two entry guards (same-item
  reentrancy from #1223, manual-action-in-flight from #1224) both returned a
  bare `false`, identical to a genuine stage failure, so `batchAutoBuild`/
  `autoBuildRun`'s counts had no way to tell "busy, try again" apart from
  "broken." Converting the return type to a three-way outcome
  (`'committed' | 'skipped' | 'failed'`) fixes this at the source instead of
  layering a second flag on top of the boolean.
- Extended `verifyModelBuilderAutoBuildDraftGate.ts`'s textual checks (and its
  self-test fixtures) to require the new `'skipped'`/`'failed'` literals at
  the exact anchor points the old `return false` checks used — the same
  discipline every prior t-029/t-037-lineage cycle has followed for this
  checker, so the regression guard stays in sync with the code it's guarding
  instead of silently going stale.
- Explicitly scoped out auto-requeuing skipped items (the task note flagged
  it as optional) and gave a concrete reason: requeuing from inside the same
  loop risks re-racing the same still-in-flight manual action if the loop
  reaches the item again too soon. Right call — that would have been a much
  larger, riskier change for a task titled around *reporting*, not fixing.

**What to improve:**
- Nothing specific this cycle — small, scoped, test-covered, and the fix
  matches the task note's actual ask rather than a related-but-different
  improvement.

**Kaizen task:** model-builder/t-038 — pre-run "N items busy" advisory for
`batchAutoBuild`/`autoBuildRun`'s own trigger buttons, matching the
`isManualActionInFlight` disable the single-item Auto button already has.

---
_Generated by [Claude Code](https://claude.ai/code)_

## 2026-08-01 | Reviewer (conductor scheduled agent run) | model-builder/t-038 | critique

type: critique

**Decision:** merged (kind_robots PR #1226).

**Failure category:** null — clean first pass, matches the kaizen note's ask exactly.

**What was good:**
- Read the actual `isManualActionInFlight` computed in
  `model-builder-item-panel.vue` before writing anything, then promoted the
  exact same logic (not a reimplementation) into the store so the two new
  call sites can never drift from the original — mirroring 3 boolean flags
  plus a `draftingField` itemId match precisely, including confirming
  `DraftField` only has 3 possible values so the itemId-only check in the
  store helper is provably equivalent to the component's 3 separate
  `isDrafting(field)` ORs.
- Kept it advisory-only per the task note (badge + tooltip, no `:disabled`
  change on the trigger buttons) — a manual action can resolve mid-run, so a
  hard block would have been the wrong call.
- Verified narrowly and rigorously: `vue-tsc --noEmit` clean, `eslint` clean
  on all 3 touched files (confirmed the 2 `no-empty` errors in
  `modelBuilderStore.ts` are pre-existing via `git stash` before/after), and
  diffed `prettier`'s suggested rewrite against the pre-change file
  line-by-line to confirm every remaining prettier complaint was a
  pre-existing line this change never touched — rather than either ignoring
  prettier entirely or blindly running `--write` and inflating the diff with
  unrelated reformatting.

**What to improve:**
- None this cycle.

**Kaizen task:** deferred — no new gap surfaced by this task; the store
helper this cycle added is now the natural reuse point for any future
model-builder UI surface that needs the same per-item busy signal.

---
_Generated by [Claude Code](https://claude.ai/code)_

## 2026-08-01 | Reviewer → Worker | model-builder/t-029 | pattern

**Decision:** merged (kind_robots PR #1227, squash `36e40c2d`)

**What was good:**
- Subagent correctly resisted re-reporting the already-known, still-open
  t-037 kaizen (batchAutoBuild/autoBuildRun vs. manual-action) even though it
  surfaced during the read-through, and instead kept looking for a genuinely
  new gap rather than padding the cycle with known work.
- Found a real server-side gap in a route none of the ~25 prior cycles had
  touched (`prepareItemUpdate()` in `server/api/model-builder/runs/index.ts`):
  the client's `isStageEditable` gate on pitch/fieldsDraft/promptDraft edits
  was never mirrored server-side, so a direct PATCH could silently overwrite
  an already-`approved` stage's content — same bug *class* as PR #1139's
  commit-route gate, different route.
- Followed the established narrow-textual-regression-guard convention
  exactly (new `verifyModelBuilderItemPatchStageGuard.ts` + self-test,
  wired into `package.json`) and re-ran all 6 pre-existing model-builder
  verify scripts to confirm no regression before opening the PR.

**What to improve:**
- None this cycle.

**Kaizen task:** deferred — t-037 (batchAutoBuild/autoBuildRun manual-action
guard) remains the standing open kaizen from a prior cycle; no new one raised
here since this cycle's own finding was already fully fixed inline.

---
_Generated by [Claude Code](https://claude.ai/code)_

## 2026-08-01 | Reviewer → Worker | model-builder/t-029 | pattern

**Decision:** merged (kind_robots PR #1230, squash `443789a5`)

**What was good:**
- The subagent's read pass correctly identified `prepareItemUpdate()`'s
  `artImageId` handling as the one field PR #1227's `assertContentStageEditable()`
  gate didn't cover, rather than re-reporting the already-fixed pitch/fields/prompt
  gate or padding the cycle with a restated version of it.
- Fix mirrors the established gate pattern exactly (extended the `stageKey`
  union to `GENERATE_ASSETS`, single call site) instead of inventing a
  parallel check — keeps the four content fields' server-side gating on one
  code path.
- Verified the regression guard actually discriminates: confirmed via
  `git stash` that it fails against the pre-fix route and passes post-fix,
  not just that it passes once written. Ran all 9 pre-existing
  `verifyModelBuilder*` guards to confirm no regression before opening the PR.

**What to improve:**
- None this cycle.

**Kaizen task:** none new — this closes the last field-level gap in
`prepareItemUpdate()`'s stage-approval mirror (pitch/fieldsDraft/promptDraft/
artImageId are now all covered by the same gate). Worth noting for whoever
next extends `prepareItemUpdate()` with a new writable field: add it to
`assertContentStageEditable`'s coverage in the same PR, not as a follow-up —
this is the second time (PR #1227, now this) a new field shipped without the
gate and needed its own later cycle to catch it.

---
_Generated by [Claude Code](https://claude.ai/code)_

## 2026-08-01 | Reviewer (conductor Agent run) | model-builder/t-029 | pattern

type: pattern

**Subject:** Closed a real gap that a prior fix's own regression-guard comment had already flagged but not fixed: server-side writes were never blocked by `ModelBuildRun.status`, only by ownership.

**Detail:**
- `utils/scripts/verifyModelBuilderCommitCancelledRunGuard.ts`'s own header comment (written for an earlier cycle's fix) already said "The commit POST durably creates/links/promotes the target server-side regardless -- that can't be undone from here" -- correctly describing the exact gap this cycle closed, without that cycle actually closing it. That guard (and its sibling `verifyModelBuilderCancelledRunGuard.ts`) only ever checked the client-side `cancelledRunIds` Set, which is a single-tab, in-memory mechanism -- a second tab, or a tab reloaded later against a stale `modelBuilder:runId`, had no way to learn a run was cancelled and could keep writing to it indefinitely, including durably committing records via `commitItem()`.
- Added `assertRunWritable(run)` next to the existing `assertRunAccess` in `server/api/model-builder/runs/index.ts`, called from all four write-capable item routes. kind_robots PR #1239, all 11 CI checks green, merged squash `a3de06a0`.
- Did not add a new textual regression-guard script this cycle (the diff was 5 files, all route/helper code) -- filed as t-039 instead of adding unverified CI wiring in the same pass. This mirrors the same discipline the *previous* gap-closing pattern should have followed: when a fix comment says "this can't be undone from here," that's a signal the server-side check is the actual fix, not the client-side toast/reattachment behavior around it.

**Suggested action:** when a future cycle's own regression-guard comment describes a consequence ("X can't be undone," "Y persists regardless") rather than a client-side symptom, treat that as a hint to check whether the *route itself* has the corresponding guard, not just the store call site that triggered the investigation. t-039 (kaizen, this cycle) adds the missing guard script for this specific fix.

---
_Generated by [Claude Code](https://claude.ai/code)_

## 2026-08-01 | Reviewer → Worker | model-builder/t-029 | critique

type: critique

**Decision:** merged (kind_robots PR #1243, squash `4f7a6ee7`)

**Failure category:** n/a — clean first-pass merge, no rejection.

**What was good:**
- Correctly scoped a genuine bug (bare `setStatus()` calls popping toasts in the wrong run's banner after `resetRun`/`resetAll`/`openRun`) to a single, minimal fix: one new `setStatusForRun(runId, tone, message)` helper mirroring `autoBuildRun`'s existing same-run gate, applied at all 9 call sites that needed it.
- Verification was thorough and honestly scoped: eslint/prettier drift explicitly confirmed pre-existing via `git stash`, `vue-tsc` clean, and all 9 pre-existing regression guards re-run rather than assumed unaffected.
- Correctly declined to add a new narrow-textual regression guard for this fix, explaining why the bug doesn't have a clean single-anchor shape — better than forcing a guard that wouldn't actually catch a regression.

**What to improve:**
- None this cycle.

**Kaizen task:** none new — the PR's own suggestion (`verifyModelBuilderRunWritableGuard.ts`) duplicates t-029's already-tracked 2026-08-01T08:29Z kaizen from PR #1239; deferred as already-tracked rather than re-filed.

---
_Generated by [Claude Code](https://claude.ai/code)_

## 2026-08-01 | Reviewer (conductor Agent run) | model-builder/t-039 | pattern

type: pattern

**Decision:** merged (kind_robots PR #1251, squash `cfae1e07`)

**Failure category:** n/a — clean first-pass merge, no rejection.

**What was good:**
- Picked up a well-scoped, already-tracked kaizen (t-039, deferred twice — first noted in PR #1239's own body, then re-noted as "already-tracked" when PR #1243's PR body re-listed it) instead of running t-029's open-ended "read everything, find one more race condition" pattern for a 9th time today. t-029 had already landed 8 merges on 2026-08-01 alone by the time this cycle started; a bounded, concrete task closing a known testing gap was the better use of this cycle than chasing an increasingly rare 9th micro-bug.
- Added `verifyModelBuilderRunWritableGuard.ts` + self-test following the established narrow-textual-checker convention exactly (same shape as `verifyModelBuilderItemPatchStageGuard.ts`): checks all four write-capable routes for `assertRunWritable(<run>)` immediately after `assertRunAccess(<run>, auth.user)`, with a self-test covering pre-fix, fixed, reordered, and access-absent shapes for both `existing.Run` and `item.Run` variable names.
- Verification was thorough: provisioned real deps via `provision_kind_robots_deps.sh` and ran the full 17-script `test:model-builder-*` suite (all pre-existing + the 2 new), `eslint`, `prettier --check` (confirmed the one `contract-tests.yml` drift warning pre-existing via `git stash`), and full-project `vue-tsc --noEmit` — all clean, `git status --porcelain` showed exactly the 4 intended files.

**What to improve:**
- None this cycle.

**Kaizen task:** none new — flagged in the PR body instead (not re-filed as a roadmap task): `verifyModelBuilderApprovedAssetGuard.ts` and `verifyModelBuilderItemPatchStageGuard.ts` both have `package.json` scripts but neither is wired into `contract-tests.yml` yet, unlike every other Model Builder guard. Worth a small follow-up task to close that gap the same way this cycle closed t-039's.

---
_Generated by [Claude Code](https://claude.ai/code)_

## 2026-08-12 | Reviewer (conductor scheduled sweep) | model-builder/t-029 | pattern

type: pattern

**Decision:** merged (kind_robots PR #1801, source-picker `alt=""` accessibility fix) — merged by Silas directly while this session's `REVIEWING:` marker check and CI poll were in flight; reconciled the recurring task's close-out afterward.

**Failure category:** n/a — clean first-pass merge, no rejection.

**What was good:**
- Small, well-scoped, verifiable diff: one Vue component, three `alt="value"` -> `alt=""` substitutions, plausible accessibility rationale (visible text label already serves as the button's accessible name, so the redundant `alt` was making screen readers announce each source twice).
- Posted the `REVIEWING:` marker before starting per the review-claim protocol and confirmed no collision.

**What to improve:**
- None on the Worker side this cycle. Process note for future Reviewer sessions: the same Worker session had already pushed a `task-events/` rearm event straight to `main` before this session's close-out branch was opened. `close_task.py`'s base-branch check caught the eventual staleness (`mergeable_state: dirty`) once `process-task-events` applied that event on its own — the fix was to rebase onto the newly-processed `main` rather than fight it, which then correctly reduced the close-out diff to just the one gap the automated processor doesn't cover (see below).

**Kaizen task:** none new this cycle — filed directly in conductor PR #2110's body instead (a process/tooling gap, not a model-builder task): `process_task_events.py`'s `compute_transition_ops` never reads or writes an event's `implementation_pr` field, so a `rearm`/`done` task-event carrying one (as this cycle's did, `silasfelinus/kind_robots#1801`) silently leaves the roadmap's `implementation_pr` at whatever the previous cycle recorded (`#1797`) unless a session manually corrects it afterward. Worth a small conductor-repo follow-up to add `implementation_pr` handling to the processor.

---
_Generated by [Claude Code](https://claude.ai/code/session_013U4A6TNwp27RJL8QchKsXJ)_

## 2026-08-12 | Reviewer (conductor scheduled sweep) | model-builder/t-029 | pattern

type: pattern

**Decision:** merged (kind_robots PR #1805, auto-build approval-race fix)

**Failure category:** n/a — clean first-pass merge, no rejection.

**What was good:**
- Dispatched an Explore subagent with an explicit exclusion list covering every model-builder bug class fixed earlier today (stale-asset approval, async-finalization approval, batch-editor state leak, ASSET_ONLY approval, source-picker accessibility, server-side stage gating, run-writable/cancelled-run guards, cross-run status toast, GENERATE_ASSETS completion race, isCommitting Edit-button guards, link-coverage gaps, aria-pressed) and a directive to read the actual store/component code rather than trust a summary. Found a genuinely new bug: `autoBuildItem()`'s `FIELDS_AND_PROMPTS`/`GENERATE_ASSETS` blocks called `approveStage()` unconditionally after an await, with no check that a concurrent Edit click (clickable throughout auto-build — gated only by `isCommitting`, not `isAutoBuilding`) hadn't already `markDownstreamStale()`d the very stage about to be approved.
- Confirmed the bug by reading `stores/modelBuilderStore.ts` and `model-builder-item-panel.vue`'s Edit-button bindings directly before editing, rather than trusting the subagent's report alone.
- Verified the new regression guard actually discriminates: fails against the pre-fix code via `git stash`, passes against the fix. Re-ran all 19 pre-existing `test:model-builder-*` guard + self-test scripts, `eslint`, `prettier --check` (pre-existing drift on `modelBuilderStore.ts`/`package.json` confirmed via `git stash` to predate the change), `vue-tsc --noEmit` repo-wide, and `test:workflow-paths` — all clean. `git status --porcelain` confirmed exactly 5 files.

**What to improve:**
- None this cycle.

**Kaizen task:** none new this cycle — filed directly in kind_robots PR #1805's body instead (a tooling gap, not a new model-builder task): `verifyModelBuilderCompletionGate.ts`'s scanner only catches direct `item.stages.KEY = ...` assignments after an await in an async function; it can't see a write that happens indirectly through a synchronous helper call (`approveStage`, bracket notation), which is exactly how this bug slipped past that existing guard. Worth considering a generic extension (flag any `approveStage`/`rejectStage` call after an await with no adjacent status guard) instead of a new narrow per-call-site guard file each time this shape recurs.

---
_Generated by [Claude Code](https://claude.ai/code/session_01BhyUNjTLndBBqS58ChwNJX)_

## 2026-08-13 | Reviewer → Worker | model-builder/t-041 | pattern

**Decision:** merged (kind_robots#1829, conductor#2161) — closed to `done` via `close_task.py` (conductor#2162)

**Failure category:** n/a — clean first-pass merge, no rejection

**What was good:**
- Correctly identified the sibling gap: t-029's fix (kind_robots#1825) run-scoped the `{success:false}`
  response branch of `pushItem`/`batchPushItems`, but left the raw network-exception (`.catch`) branch
  calling the unscoped global `handleError()`. t-041's kaizen note named this precisely and the Worker
  fixed exactly that branch, mirroring the existing gate rather than inventing a new pattern.
- Added a static regression guard (`verifyModelBuilderPushItemErrorScopeGuard.ts` + self-test) following
  the file's established convention from t-029's own guard, proven against both pre-fix and post-fix
  source rather than just asserted.
- All 19 kind_robots checks green, all 22 conductor checks green on both PRs before merge; `vue-tsc`
  and lint-ratchet held with no rule regression.

**Kaizen task:** deferred — the Worker's own kaizen suggestion (whether `generateItemAsset`'s
unconditional `handleError()` call should also route through `setStatusForRun` once past its
`cancelledRunIds` check) is a real, well-scoped follow-up, but that catch fires on a *user-initiated*
synchronous generate action rather than a background auto-save, so the stronger global-banner treatment
may be intentional rather than a gap. Recorded here rather than filed as a new task pending a
judgment call on whether user-initiated actions should keep the stronger treatment.

**Pattern note:** this is the second kaizen-chain task in a row (after t-029 itself, chained from an
earlier cancellation-race fix) that found a second branch of the same conditional needing an identical
fix. Worth generalizing: when a kaizen task targets "the same class of issue" in a sibling code path,
check both branches of the originating conditional (success vs. exception, sync vs. async) rather than
just the one path the kaizen note names — recorded as the `LEARNING.yaml` lesson for this task.

---
_Generated by [Claude Code](https://claude.ai/code/session_01M1RrPHkwUzY1Sq2LtPvQVL)_

## 2026-08-13 | Reviewer (conductor scheduled sweep) | model-builder/t-029 | pattern

type: pattern

**Decision:** merged (kind_robots PR #1838, `draftText` run-scoping fix)

**Failure category:** n/a — clean first-pass merge, no rejection.

**What was good:**
- Dispatched a background subagent with the full accumulated exclusion list (24 existing
  `verifyModelBuilder*.ts` guard files, plus two known-fixed-but-unguarded classes) and
  found a genuinely new gap: `draftText()` is the one async Model Builder entry point that
  never adopted the `setStatusForRun(runId, ...)` pattern every sibling long-running action
  (`generateItemAsset`/`pollAsyncArtJob`/`commitItem`/`pushItem`/`batchPushItems`) already
  uses to stop a slow response from popping a misleading toast in a run the user has since
  navigated away from.
- Added `verifyModelBuilderDraftStatusScopeGuard.ts` + `.test.ts` following the established
  narrow-textual-checker convention exactly, including a "partially regressed" fixture (runId
  captured but one call site reverted) to prove the guard actually discriminates, not just a
  binary buggy/fixed pair.
- Verification was thorough and pre-existing drift was distinguished from the change's own
  diff via `git stash` before blaming it: new guard self-test + contract, all 24 pre-existing
  guards, eslint, prettier, repo-wide `vue-tsc --noEmit`, and `git status --porcelain` showing
  exactly the 5 intended files.

**What to improve:**
- None this cycle.

**Kaizen task:** none new — this is itself the standing model-builder/t-029 kaizen loop;
rearmed to `ready` per the recurring-task convention.

**Reconciliation note:** the Worker session that produced this cycle (session
`20260813T042836-modelbuilder-t029-`) opened its own close-out PR (`silasfelinus/conductor#2175`)
concurrently with a scheduled Reviewer sweep session's independent `close_task.py` reconciliation
of the same task's stale claim. The Reviewer's close-out landed first (`silasfelinus/conductor#2176`);
this entry and the fuller roadmap note below were merged in manually afterward to preserve #2175's
richer technical detail rather than letting it go stale unmerged — see root `TALKBACK.md`
2026-08-13 entries for the full sequence.

---
_Generated by [Claude Code](https://claude.ai/code)_

## 2026-08-13 | Agent (scheduled conductor sweep) → self-review | model-builder/t-029 | pattern

type: pattern

**Subject:** Recurring t-029 bug-hunt cycle, session `20260813T183600Z-sched-conductor-mb-t029`.
Claimed via `claim_task.py`, implementation delegated to a background Worker-role agent working
directly in `/home/user/kind_robots`, reviewed and merged by this same session.

**Decision:** merged (kind_robots PR #1859, squash `a2085f6b`)

**What was good:**
- Found a real, concrete bug: `batchSetField()` toasted success before `batchPushItems()`'s
  request had resolved — the one batch entry point that hadn't been brought in line with
  `batchDraftField`/`batchAutoBuild`'s await-then-report pattern. Fix is narrowly scoped (2
  functions in `modelBuilderStore.ts`), and the new guard was confirmed to fail against the
  pre-fix `origin/main` copy of the store, not just self-consistent fixtures.
- All 26 pre-existing `verifyModelBuilder*` guards + self-tests, eslint (pre-existing drift
  confirmed via `git stash`), prettier on new files, and repo-wide `vue-tsc --noEmit` all
  verified clean before merge. 20/21 checks green at merge time (only the optional docker
  "Build production image" job still running, same as the established non-blocking pattern).

**What to improve:**
- The delegated background agent's own self-reported final status was unreliable — after
  actually opening and pushing the PR, it twice ended its turn with a placeholder
  ("waiting for a background timer/sleep task") instead of a real status report, even after
  being explicitly resumed and asked for one. The parent session verified and merged directly
  via GitHub MCP rather than trusting the agent's self-report — this is the correct fallback
  (never trust a sub-agent's completion claim over a direct check of the actual PR/CI state),
  but the agent's polling-loop pattern for "wait for CI, then merge" is worth tightening in a
  future delegation so it doesn't spin on a phantom wait mechanism.

**Kaizen task:** `t-042` — build one meta-guard auditing every store action that toasts
success/failure for confirmed-outcome-before-toast, instead of continuing to find and patch
this same bug shape one function at a time (this is the third t-029 cycle to hit it — see
PR #1838 `draftText()`, PR #1829 `pushItem`/`batchPushItems` exception path, and this cycle's
`batchSetField()`).

---
_Generated by [Claude Code](https://claude.ai/code)_

## 2026-08-14 | Worker (conductor scheduled Agent run) | model-builder/t-029 | pattern

type: pattern

**Subject:** Fifth cycle since t-042's confirmedOutcomeGuard meta-guard landed found a bug the
meta-guard structurally cannot see — an *awaited* call whose own internals swallow failure,
not another un-awaited fire-and-forget toast.

**Detail:**
- `recordArtifact()` awaited `performFetch()` inside a `try/catch` but never checked the
  resolved response's `.success` field. `performFetch` never rejects for an HTTP-level failure
  (a validation error, `assertArtImageAttachable`'s 403, or a 409 from `assertRunWritable` if
  the run was cancelled mid-request) — it always resolves with `{ success: false }` — so that
  catch block was dead code in practice. Any failure of the artifact-recording POST was
  silently discarded with no error surfaced and no retry; both callers (`generateItemAsset`,
  `pollAsyncArtJob`) still marked `GENERATE_ASSETS` ready and popped a success toast
  regardless. Concrete durable effect: an approved candidate silently loses its preview image
  on the next resume/reload (`adaptItem`'s `imagePath` reconstructs purely from the
  `ModelBuildArtifact` row that was never written), with `item.artImageId`/commit still working
  since that field is set independently.
- `verifyModelBuilderConfirmedOutcomeGuard.ts` (t-042's meta-guard) only flags a *bare*,
  un-awaited call to one of the store's own Promise-returning helpers before a success toast —
  it has no way to see that a properly-awaited callee's own body discards its result. This is a
  structurally distinct bug shape from the four instances the meta-guard was built to catch
  (`draftText`, `pushItem`/`batchPushItems`, `batchSetField`), not a fifth instance of the same
  one — confirmed by checking the meta-guard's own source before writing the fix, rather than
  assuming it would have caught this.
- Also audited two other candidates this cycle before settling on `recordArtifact`:
  `batchApproveStage` (no `isStageEditable`/in-flight gate before approving) and
  `batchSetField`'s all-or-nothing partial-failure reporting on a 207 batch response. Neither
  held up to a concrete repro once traced through — `batchApproveStage`'s only wired call site
  (`FIELDS_AND_PROMPTS`) is never `'in-progress'`, and `draftText`'s own `isStageEditable`
  guard already discards a stale draft racing an approval regardless of which UI surface
  triggered the approval; the batch partial-failure gap reads as a UX nitpick, not a
  correctness bug. Reported both in the PR body as considered-and-rejected rather than silently
  discarding the dead ends.
- Kept the diff minimally scoped: `origin/main`'s copy of `modelBuilderStore.ts` already fails
  `prettier --check` (pre-existing drift unrelated to this change, confirmed via a direct
  `prettier --check` against the pre-change file). A first pass ran `prettier --write` on the
  touched file and it reformatted ~70 unrelated lines throughout the file; caught before
  committing by diffing against `origin/main`, reverted, and hand-matched the surrounding
  style for only the actually-changed lines instead.
- kind_robots PR #1877: 21/22 CI checks green at merge time (only the optional "Build
  production image" docker job still running, matching this project's established
  non-blocking pattern), squash-merged `e148178`. Added
  `verifyModelBuilderRecordArtifactSuccessGuard.ts` + `.test.ts`, all 29 `verifyModelBuilder*`
  guards + selftests verified passing (no regression).

**Suggested action:** Widen `verifyModelBuilderConfirmedOutcomeGuard.ts` (or add a sibling
guard) to also flag any store function whose body awaits `performFetch` inside a `try/catch`
with no `.success` check anywhere in scope — logged as this cycle's kaizen suggestion and as a
`LEARNING.yaml` lesson rather than a new task, since the right generalization is speculative
until a second instance of this specific shape turns up.

**Kaizen task:** deferred to a future cycle's own read-through, per this task's established
self-perpetuating pattern — the widened-guard idea above needs a second confirmed instance
before it's worth ticketing as a structural fix rather than a one-off.

---
_Generated by [Claude Code](https://claude.ai/code)_

## 2026-08-15 | Worker (conductor scheduled Agent run) | model-builder/t-029 | pattern

type: pattern

**Subject:** Sixth t-029 cycle following up on the fifth's explicit "widen scope" suggestion found a genuinely new bug class — a server-side check-then-act race, not another instance of the client-side async/store patterns the prior five cycles all found.

**Detail:**
- Read the three files the 2026-08-15T0826Z cycle flagged as unexplored ground
  (`server/utils/characterFacetSync.ts`, `server/utils/botFacetSync.ts`,
  `server/utils/facetProfileInput.ts`) plus their only call site
  (`commit.post.ts`). `characterFacetSync`/`botFacetSync` are pure
  `deleteMany`+`createMany` writes inside the commit transaction, keyed on
  composite unique constraints (`characterId+facetId+fieldKey`,
  `botId+facetId+fieldKey`) — no crash-prone race there, and no client-side
  async-fetch-ordering exposure since these run entirely server-side inside a
  single Prisma transaction.
- `syncFacetProfileUpdate()` (in `commit.post.ts`, called for Facet UPDATE-action
  commits) was different: a `findUnique`-then-`create`/`update` check-then-act
  against `FacetProfile`, whose primary key is the single column `facetId`.
  Nothing serializes `ModelBuildRun`s by `sourceId` (`runs/index.post.ts`) — an
  item's `idempotencyKey` claim only stops the *same* item committing twice, not
  two *different* runs/items both targeting the same existing Facet for an
  UPDATE. If both commits read `existingProfile` as `null` before either writes,
  the race loser's `facetProfile.create()` throws a `facetId`
  unique-constraint violation, which aborts that *entire* commit transaction —
  rolling back the sibling `tx.facet.update()` in the same transaction and
  surfacing as an opaque 500 to whoever lost the race. Self-healing on retry
  (since `existingProfile` is found the second time), but a confusing one-time
  failure a concurrent-editing user shouldn't hit at all.
- Fixed by replacing the branch with `tx.facetProfile.upsert()`, which resolves
  the create-vs-update decision atomically at the database (a single `INSERT
  ... ON DUPLICATE KEY UPDATE` on MySQL) instead of racing on a client-side
  read taken before either transaction has written.
- Extended the existing `verifyModelBuilderFacetSync.ts` (already wired into
  `.github/workflows/facet-catalog-contract.yml`, a separate CI workflow from
  the `package.json` `test:model-builder-*` group most other t-029 guards live
  in) with a `requireText`/`forbidText` pair asserting the upsert shape stays
  in place and the retired create-if-missing shape doesn't return.
- Verified: guard passes; all 67 `test:model-builder-*` npm scripts pass (no
  regression); `vue-tsc --noEmit` exits 0 repo-wide; eslint clean on both
  touched files; `prettier --check` clean except
  `verifyModelBuilderFacetSync.ts`'s pre-existing formatting drift (confirmed
  present on `origin/main` before this change via `git stash`, untouched by
  this diff's added lines); `git status --porcelain` showed exactly the 2
  intended files. kind_robots PR #1898: all CI checks green, squash-merged.

**What was good:** taking the prior cycle's explicit scope-widening suggestion
literally rather than re-treading the same store/component files a sixth time —
and recognizing early that the two facet-sync helpers were structurally immune
to the async-ordering bug class the last five cycles all found (pure
transactional writes, no client-side fetch race possible), so the search
correctly narrowed to the one function with a genuine check-then-act shape
instead of forcing a fit into a familiar pattern.

**What to improve:** none this cycle — clean first pass, no rejection.

**Kaizen task:** deferred — this cycle's PR body itself proposes the natural
next step (surface a non-blocking warning when a new run targets a source with
an existing ACTIVE run), left as a suggestion rather than a task since it's
speculative UX polish, not a confirmed gap.

---
_Generated by [Claude Code](https://claude.ai/code)_

## 2026-08-15 | Agent (scheduled conductor sweep) → self | model-builder/t-029 | worker

**Decision:** no new bug found this cycle; re-armed to `ready` per recurring-task convention.

**What happened:**
- Full CLAUDE.md sweep: no open PRs (verified via GitHub MCP on both repos), no open Todos, no
  stranded branches, no failing scheduled workflows (last several `process-task-events.yml` runs
  all `success`), site audit not overdue (6 days since last report). `check_pr_merged_drift.py`
  clean, `audit_human_gates.py` returned the standing 36-gate catalogue (1 already-known stale
  signal, appmaker/t-010, unchanged). `select_role.py`'s direct API calls 403'd as documented;
  underlying recommendation was `worker`, `ready_task: kapowarr/t-012`.
- kapowarr/t-012 and t-013 are both blocked by the same GitHub-scope wall already escalated as
  `kapowarr/t-014` (hard `needs-human`, filed by a prior cycle this same day) — skipped rather
  than writing a sixth near-identical handoff doc. mermaids-of-venice/t-013 (recurring,
  progress-gated) had already been verified no-op for 2026-08-15 Pacific by an earlier cycle
  today (manuscript blob unchanged since 2026-08-04) — skipped to respect its "at most once per
  Pacific day" contract. Next actionable `ready` task per `priority.yaml` order was
  model-builder/t-029.
- Dispatched a worktree-isolated background agent to do the deep-review cycle in kind_robots
  (per this session's own hard safety rule 12, since this session's foreground checkout at
  `/home/user/kind_robots` was available for other work). The agent's sandbox blocked git/cd
  directly against that shared checkout (the same worktree-isolation protection working as
  intended) and fell back to an independent scratch clone — same workaround a 2026-08-15T0426Z
  cycle already used, no functional impact since no push was needed.
- Agent did a genuine fresh read of `server/utils/facetProfileInput.ts` (first deep review — pure
  synchronous validation, not race-capable), re-verified `characterFacetSync.ts`/
  `botFacetSync.ts`, and re-checked the `runs/[id].patch.ts` `assertRunWritable` gap a second
  time (same conclusion: no client-reachable repro). No new bug found. Full note appended to the
  task; concrete fresh ground flagged for next cycle: either land the `runs/[id].patch.ts`
  hardening outright as a deliberate kaizen instead of deferring a third time, or widen scope to
  `stores/helpers/modelBuilderFields.ts`/`modelBuilderRecipes.ts` or the
  `relations.ts` artifact-promotion concurrency path.

**What was good:** the worktree-isolation safety rule (hard rule 12) did its job this cycle —
the background agent was correctly blocked from touching the foreground's shared kind_robots
checkout and self-recovered via the documented scratch-clone workaround with zero disruption.

**What to improve:** none this cycle — clean no-op, no rejection, safety rule verified working
as designed.

**Kaizen task:** deferred — the "land the `runs/[id].patch.ts` hardening outright" suggestion is
recorded on the task note itself for the next bug-hunt cycle to act on directly; no separate
roadmap task warranted for a one-line defense-in-depth change already fully scoped in-note.

---
_Generated by [Claude Code](https://claude.ai/code)_

## 2026-08-21 | Agent (scheduled conductor sweep) → self | model-builder/t-029 | resolution

**Decision:** merged. Cycle 32 confirmed cycle 31's suggested lead was a non-issue, then found
and fixed a real bug on the pivot.

**What happened:**
- Dispatched a background agent (no worktree isolation needed — the foreground session's
  designated branch stayed in `conductor` the whole time, never touching `kind_robots`, so hard
  rule 12 didn't apply) to work cycle 31's suggested lead against the `kind_robots` checkout:
  `runs/index.post.ts`, `runs/index.get.ts`, `runs/[id].get.ts` against their callers in
  `modelBuilderStore.ts`, plus a check for other components reading source-record raw fields as
  fragilely as `source-picker.vue` did before cycle 31's fix.
- Both checks came back clean: the three server routes had no bug, and `sourceLabel()` (the only
  other `titleField` consumer) is safe because `titleField` is always a Prisma string column
  across every `SOURCE_TYPES` entry — not exposed to the same type-mismatch class cycle 31 fixed.
- Correctly declined to force a change onto a non-issue and pivoted to a fresh bug-hunt per the
  recurring task's own fallback convention, per AGENTS.md's guidance not to fabricate a marginal
  change just to look productive.
- Found a real one: `openRun()` had no equivalent of `resumeRun()`'s "don't resume a dead run"
  check — `resumeRun()` explicitly guards `status !== 'CANCELLED'`, but `openRun()`'s cached-lookup
  and network-fetch paths both had no status check at all, and `BuildRun` didn't even carry a
  `status` field. A run cancelled elsewhere (another tab/device, or a `fetchRuns()`/`cancelRun()`
  race) could be silently reopened as fully interactive, with every subsequent write 409'ing in
  the background against `assertRunWritable`'s cancelled check and no visible explanation to the
  user.
- Fixed by adding `status` to `BuildRun`/`adaptRun`; both `openRun()` paths now refuse/discard a
  `CANCELLED` run and surface an error instead of silently opening a dead one. Added
  `verifyModelBuilderOpenRunCancelledGuard.ts` + `.test.ts`, mirroring
  `verifyModelBuilderResumeCancelledRunGuard.ts`'s established pattern, wired into
  `package.json`/`contract-tests.yml`.
- Verified per the established rigor: `vue-tsc --noEmit` repo-wide clean, eslint clean on touched
  files (2 pre-existing unrelated empty-catch-block findings confirmed via `git stash` to predate
  this change), `prettier --check` clean on new/touched files, all 121 `test:model-builder-*`
  scripts green (including the 2 new ones), scoped `git status --porcelain` (5 intended files).
- kind_robots PR #1999: all 34 CI checks green, squash-merged `21c33901e15265bb9180c7503d0d440209ab8692`.
- Conductor close-out: re-armed `model-builder/t-029` to `ready` with the cycle-32 note appended
  and `implementation_pr: silasfelinus/kind_robots#1999` recorded.

**What was good:** the agent traced cycle 31's lead to a genuine, evidence-based conclusion
("not a bug, here's why") instead of straining to manufacture a fix from it, then found a real
bug on the pivot on the first try — a cancelled-run reopen is exactly the class of silent,
narrow, user-visible bug this recurring task exists to catch. Verification was thorough and
matched the project's established bar (guard selftest + real-file pass + full test suite +
tsc/eslint/prettier + scoped diff).

**What to improve:** none this cycle.

**Kaizen task:** deferred — cycle 32's own note already names a concrete next lead
(`modelBuilderFields.ts`/`modelBuilderRecipes.ts`'s `resolveTargetModel`/`CREATE_TARGETS`/
`defaultFieldsTemplate` mapping against the Prisma schema, the same stale-mapping class cycle 22
fixed) for cycle 33 to act on directly; no separate roadmap task warranted.

---
_Generated by [Claude Code](https://claude.ai/code)_

## 2026-08-21 | Agent (scheduled conductor sweep) → self | model-builder/t-029 | resolution

**Decision:** merged. Cycle 33 confirmed cycle 32's suggested lead was a non-issue, then found
and fixed a real bug on the pivot — the second cycle in a row this session, both delegated to a
background agent working directly in `kind_robots` while the foreground session's designated
branch stayed in `conductor` (hard rule 12 not applicable, same as cycle 32).

**What happened:**
- Traced all 6 `CREATE_TARGETS` entries, `resolveTargetModel`'s dispatch, and every
  `MODEL_FIELDS` entry (names, enum choice sets, required/default fields) in
  `modelBuilderFields.ts`/`modelBuilderRecipes.ts` against `prisma/schema.prisma` — all
  correct, no stale mapping found (cycle 32's suggested lead was a clean non-issue).
- Pivoted per the recurring task's own fallback convention and found a real bug in the
  neighboring commit path, `server/api/model-builder/items/[id]/commit.post.ts`: its
  `pickText()` helper checked the prose/long-text classification *before* any explicit
  `SHORT_TEXT_MAX` override, so a field marked `prose: true` always got the 20000-char
  long-text cap regardless of a narrower override. This made the existing `SHORT_TEXT_MAX`
  entries for `Reward.flavorText`/`Dream.flavorText` (real `VarChar(512)` columns) dead code,
  and left `Bot.description`/`botIntro`/`userIntro`/`prompt` (`VarChar(764)`/`VarChar(3000)`,
  three `NOT NULL`) with no cap at all on a live path (`Bot` is a real CREATE target via
  `expand-narrator-bot`/`expand-manager-bot`).
- Fixed by reordering the truncation-length check to look at `SHORT_TEXT_MAX` first, and
  added the missing `Bot` entries. Added
  `utils/scripts/verifyModelBuilderCommitTextTruncationGuard.ts` + `.test.ts`, wired into
  `package.json`/`contract-tests.yml`. A follow-up commit was needed after the first CI run:
  the new guard's own `.match()` sites tripped the repo's capture-group-guard contract
  (wrong shape) — rewritten to the required early-exit form.
- Verified per the established rigor: guard selftest + real-file pass, all 123
  `test:model-builder-*` scripts pass, `vue-tsc --noEmit` clean, eslint/prettier clean on
  touched files, scoped `git status --porcelain` (5 intended files).
- kind_robots PR #2000: all required checks green (the non-required "Build production
  image" job was still running at merge time, correctly not waited on per that workflow's
  own documented contract). Squash-merged `7af86d2d921760e98ed5d4b318e3a93da56a6150`.
- Conductor close-out: re-armed `model-builder/t-029` to `ready` with the cycle-33 note
  appended and `implementation_pr: silasfelinus/kind_robots#2000` recorded.

**What was good:** the agent correctly distinguished a required check from a documented
non-required one instead of over-waiting, caught and fixed its own guard's contract
violation on the first CI feedback loop rather than needing a nudge, and again found a
real, narrowly-scoped, user/data-visible bug on the pivot rather than padding the cycle.

**What to improve:** none this cycle.

**Kaizen task:** deferred — cycle 33's own note already names a concrete next lead
(`DREAM_TYPES` in `modelBuilderFields.ts` missing `PROMPTBOT`/`NARRATOR` relative to
`dreamHelper.ts`'s `CREATABLE_DREAM_TYPES`, currently zero live impact since `Dream` isn't
a reachable CREATE/UPDATE target yet) for cycle 34 to act on or explicitly document as
intentional; no separate roadmap task warranted.

---
_Generated by [Claude Code](https://claude.ai/code)_

## 2026-08-21 | Agent (scheduled conductor sweep) → self | model-builder/t-029 | resolution

**Decision:** merged. Cycle 30 found and fixed a real, single-tab-reachable bug.

**What happened:**
- Continued cycle 29's suggested lead: `commitItem()`'s interaction with a concurrent
  `batchPushItems`-family call on the same item. Dispatched a worktree-isolated background
  agent (hard rule 12) to do the deep-review cycle against the `kind_robots` checkout, since
  this session's own designated branch/checkout is in `conductor`.
- Found: `batchDraftField()`, `batchSetField()`, and `batchApproveStage()` each push an item's
  full `item.stages` blob to the server without checking `isItemManualActionInFlight()` first —
  unlike `autoBuildItem()`, which already has that guard. `commitItem()`/`generateItemAsset()`
  set a transient client-local `'in-progress'` marker on `item.stages.COMMIT`/`GENERATE_ASSETS`
  before their own await and never persist it themselves; if a batch function's stage-status
  write lands after the single-item route's own dedicated final write, it can silently revert a
  just-committed item's status back to a permanently-stuck `'in-progress'` — reachable in a
  single browser tab (no clock race) because `model-builder-progress-matrix.vue` renders the
  batch editor and the item panel side by side for the same group.
- Fixed by adding the same `isItemManualActionInFlight` skip to the three batch functions,
  mirroring `autoBuildItem()`'s existing guard. Added
  `verifyModelBuilderBatchBusyItemExclusionGuard.ts` + `.test.ts`, wired into `package.json` and
  `contract-tests.yml`. Verified per the established rigor (guard selftest + real-file pass, all
  119 `test:model-builder-*` scripts green, `vue-tsc --noEmit` clean, eslint/prettier clean on
  touched files with pre-existing drift confirmed via `git stash`, scoped `git status
  --porcelain`).
- kind_robots PR #1992: 32/33 CI checks green (only the non-required Docker build job still in
  flight, matching cycles 26/28's precedent), squash-merged `cbd28d5`. Diff verified post-merge
  (431 additions, 5 files, 1 commit — matches the authored change, no squash duplication).
- Conductor close-out: re-armed `model-builder/t-029` to `ready` with the cycle-30 note appended
  and `implementation_pr: silasfelinus/kind_robots#1992` recorded.

**What was good:** the agent correctly picked up the exact lead cycle 29 left, found a genuine
single-tab-reachable bug (not a forced/speculative one) rather than padding the cycle, and
recognized `batchAutoBuild` was already safe (delegates to the already-guarded
`autoBuildItem()`) instead of touching it needlessly. The resume-and-verify-CI loop needed two
nudges (its self-scheduled "background wait" pattern kept ending the turn instead of actually
blocking) — worth noting for future dispatches: instruct agents up front to poll CI directly
without a sleep-then-stop pattern.

**What to improve:** none on the investigation itself.

**Kaizen task:** deferred — this cycle's own note names a concrete structural fix (move the
in-flight marker out of `item.stages` into a separate ephemeral field, the same way
`artJobId`/`queueState` already are) as the natural next step, and cycle 31's suggested lead
already covers auditing the single-item setters for the same gap. Recorded as a `LEARNING.yaml`
lesson rather than a new task since a second confirmed instance of the "sleep-then-stop"
sub-agent pattern would be needed before generalizing the resume-loop observation into tooling
guidance.

---
_Generated by [Claude Code](https://claude.ai/code)_

## 2026-08-22 | Agent (scheduled conductor sweep) → self | model-builder/t-029 | resolution

**Decision:** merged. Cycle 41 found and fixed a real bug plus a genuine bonus fix.

**What happened:**
- Followed cycle 40's kaizen lead exactly: the poll-treats-failure-as-pending defect class was
  fully closed app-wide (client cycles 36-39, server confirmed-clean cycle 40), so cycle 41
  returned to a fresh bug-hunt read of the Model Builder front-end surface rather than
  continuing that exhausted lead. Dispatched a worktree-isolated background agent (hard rule 12)
  against the `kind_robots` checkout.
- Found: `BuildItem.lastAutoBuildOutcome` is written only by `autoBuildRun()`/`batchAutoBuild()`,
  and `model-builder-progress-matrix.vue`/`model-builder-batch-editor.vue` render a red "failed"
  badge whenever `lastAutoBuildOutcome === 'failed' || item.error`. Nothing ever cleared
  `lastAutoBuildOutcome` once set to `'failed'` — including the manual/AI-redraft repair paths
  that already clear the sibling `item.error` for exactly this "avoid a confusing asymmetry"
  reason per that code's own existing comment. Concrete single-tab-reachable repro: auto-build
  all, one item's AI draft fails (badge correctly red), user fixes it by hand or a fresh AI
  redraft succeeds (`item.error` clears, banner disappears) — but the badge keeps lying "failed"
  for an item just fixed, with no way to clear it short of a full commit or another whole
  auto-build pass.
- Fixed by clearing `lastAutoBuildOutcome = null` everywhere `item.error` is already cleared on a
  fresh attempt/fix: `updatePitch`, `updateFields`, `updatePrompt` (plus their `onFailure`
  revert), and the start of `generateItemAsset`, `generateItemAssetAsync`, `commitItem`. Added
  `verifyModelBuilderAutoBuildOutcomeClearGuard.ts` + `.test.ts`, wired into `package.json` and
  `contract-tests.yml`.
- Genuine bonus find while verifying: `verifyModelBuilderAsyncPollFailureGuard.ts`'s own
  brace-matching helper never skipped `//`/`/* */` comments before checking quote characters, so
  ordinary contractions in comments ("doesn't") were misread as string openers — it silently
  over-captured `pollAsyncArtJob`'s body on the pre-fix file (coincidentally still balancing at
  depth 0 deep inside an unrelated function), which this cycle's own unrelated edits shifted into
  a hard, misleading "function not found" failure. Fixed the scanner to skip comments first.
- Verified per the established rigor: guard fails against the pre-fix store (9 violations),
  passes post-fix; all 132 `test:model-builder-*` scripts green; `vue-tsc --noEmit` shows the
  identical single pre-existing unrelated error before/after; eslint/prettier clean on touched
  files (pre-existing unrelated prettier drift confirmed left untouched).
- kind_robots PR #2021: 35/36 CI checks green (only the documented non-required Build production
  image job still in flight at merge time), squash-merged `a991e501437e1110e7ce56f7a576e52785e9ae02`.
  Conductor close-out: re-armed `model-builder/t-029` to `ready` with the cycle-41 note and
  `implementation_pr: silasfelinus/kind_robots#2021` recorded.

**What was good:** the agent read the existing guard convention before searching (avoided
duplicating the ~64 already-covered guard territories), found a genuinely concrete,
single-tab-reachable bug rather than a speculative one, and — notably — caught and fixed a
real *pre-existing* latent bug in another guard's own tooling that its own edit happened to
expose, rather than treating that guard's confusing failure as its own change being wrong.

**What to improve:** the same "background agent self-schedules a wait/monitor for CI and stops
instead of actually blocking" pattern flagged in this file's 2026-08-21 cycle-30 entry (and
independently in root `TALKBACK.md`'s 2026-08-22 ai-art-academy/t-076 entry) recurred here too —
even with an explicit "poll directly, don't sleep-then-stop" instruction in the dispatch prompt,
the agent still self-scheduled a monitor and ended its turn once before resuming. This is now
three independent confirmed instances across two different projects/sessions. The coordinator
side of the fix (this session: verify CI directly via its own GitHub MCP access rather than
relying on the sub-agent's self-report, merge if green, then tell the sub-agent explicitly to
stop) continues to work as a backstop, but the pattern itself is now common enough to be worth
converting from a per-cycle TALKBACK observation into standing dispatch guidance (e.g. a note in
AGENTS.md's background-agent section: CI-wait loops in a delegated agent's own prompt reliably
don't block turn-to-turn; the delegating session should poll CI itself rather than trust a
sub-agent's "waiting for X" self-report as if it were still running).

**Kaizen task:** deferred to cycle 42's own note (audit other ephemeral/session-only UI flags in
`modelBuilderStore.ts` for the same one-way-clear gap `lastAutoBuildOutcome` had). The dispatch-
pattern observation above is cross-cutting rather than model-builder-specific, so it's recorded
here as a pattern note for whichever session next touches `AGENTS.md`'s agent-dispatch guidance,
not as a new model-builder roadmap task.

---
_Generated by [Claude Code](https://claude.ai/code)_

## 2026-08-22 | Agent (scheduled conductor sweep) | model-builder/t-029 cycle 42 | resolution

**Decision:** claimed cycle 42 per cycle 41's own kaizen suggestion (audit other ephemeral/
session-only UI flags in `stores/modelBuilderStore.ts` for the same one-way-clear-gap bug
class `lastAutoBuildOutcome` had). Dispatched a worktree-isolated background agent against
the `kind_robots` checkout (hard rule 12).

- Audited: `artJobId`/`queueState` (always cleared together on terminal job status or
  cancellation, no uncaught-rejection path could strand them), the four `createOwnedSingleton`
  in-flight flags (`generatingItemId`/`committingItemId`/`autoBuildingItemId`/
  `batchingOutputKey`, always released in `finally`), `sourcesError` (single producer/consumer),
  and `StageState.note` (never read as an authoritative signal by any Vue component). All
  confirmed already correct.
- Found and fixed: `state.statusMessage`/`statusTone` (the global status banner rendered in
  `model-builder-manager.vue`) is only ever cleared by `clearStatus()`. Seven sibling functions
  already called it before a fresh attempt; `approveStage`, `rejectStage`, `reopenStage`,
  `updatePitch`, `updateFields`, `updatePrompt`, `batchSetField`, and `batchApproveStage` never
  did. Concrete repro: an "Approve pitch" PATCH fails (banner correctly shows the error), the
  user retries and it succeeds — nothing clears the stale error banner until an unrelated later
  action happens to call `clearStatus()`/`setStatus()` on its own. Fixed by adding `clearStatus()`
  to all eight, mirroring exactly where every already-fixed sibling places it.
- Added `verifyModelBuilderStaleStatusClearGuard.ts` + `.test.ts` following the cycle-41 guard's
  exact convention (walks the eight target functions, requires each body to call `clearStatus()`).
  Confirmed it fails pre-fix, passes post-fix. Wired into `package.json` and
  `.github/workflows/contract-tests.yml`.
- Verified: all 133 `test:model-builder-*` scripts pass (131 prior + 2 new), `vue-tsc --noEmit`
  shows the identical single pre-existing unrelated error before/after (confirmed via `git
  stash`), eslint clean on touched files (2 pre-existing unrelated errors elsewhere in the file
  confirmed pre-existing), prettier clean on the new files (the store file itself has pre-
  existing repo-wide `printWidth: 80` drift predating this change, out of scope — see kaizen).
- kind_robots PR #2022: 35/36 CI checks green (only the documented non-required "Build
  production image" job still in flight), squash-merged `9304024232353838eabbe7ce1a01119b1dd99195`.
  Conductor close-out: re-armed `model-builder/t-029` to `ready` with the cycle-42 note and
  `implementation_pr: silasfelinus/kind_robots#2022` recorded.

**What was good:** the agent generalized the exact fix pattern from cycle 41 (call an existing
clear helper at the start of every mutating path) rather than treating the previous fix as fully
closing the bug class, and it correctly distinguished which ephemeral fields were already safe
(with concrete reasoning per field) from the one that wasn't, rather than either over-fixing
fields that didn't need it or stopping after the first clean-looking field.

**What to improve:** a 4th confirmed instance of the "delegated background agent self-reports
'waiting on a CI timer' but doesn't actually block" pattern (cycle 30, cycle 41, this cycle, and
root TALKBACK's 2026-08-22 ai-art-academy/t-076 entry). This session polled CI directly via the
GitHub MCP connector, merged once 35/36 checks were green, and explicitly told the sub-agent via
`SendMessage` to stop rather than keep polling — avoiding a merge race — but the underlying
pattern is now common enough that it was promoted from a recurring TALKBACK observation into
`AGENTS.md` hard safety rule 13 this cycle, so future sessions don't have to rediscover it.

**Kaizen task:** none filed as a new roadmap task — cycle 43's lead is already recorded in the
task note (either a dedicated `prettier --write` formatting-only PR for `modelBuilderStore.ts`,
or confirming/documenting that CI's prettier check is expected to skip this file).

---
_Generated by [Claude Code](https://claude.ai/code)_

## 2026-08-22 | Agent (scheduled conductor sweep) | model-builder/t-029 cycle 44 | resolution

**Decision:** clean no-op — re-armed to `ready`, nothing merged, no PR opened for the implementation itself.

Per cycle 43's own kaizen note, dispatched a worktree-isolated background agent (hard rule 12) to do
a fresh bug-hunt read of the Model Builder front-end surface, since the `lastAutoBuildOutcome`/stale-
status-clear defect class (cycles 40-42) and the formatting cleanup (cycle 43) were both already
exhausted leads. The agent read `stores/modelBuilderStore.ts` in full (all 3190 lines), all 7
model-builder components, both store helpers (`modelBuilderRecipes.ts`/`modelBuilderFields.ts`), and
every `server/api/model-builder/**` route — not a sample. It specifically checked for race conditions
across concurrent async ops, stale closures, incomplete state resets, off-by-one/index bugs,
error-handling gaps, validation edge cases, mutation correctness, and logic-vs-comment mismatches.

Three plausible-looking leads were traced to ground and each turned out already handled: (1) the four
batch functions guard only on `state.autoBuilding`, not the full `isRunOperationInFlight()` check that
`autoBuildRun` uses — but `model-builder-batch-editor.vue`'s `anyBatching` computed already disables
every batch button globally the instant any group's batch op starts, closing the gap at the UI layer
(same reasoning cycle 25 already documented); (2) `model-builder-progress-matrix.vue`'s
`selectedItemId` ref looked unwatched across `store.run` changing, but the component fully
unmounts/remounts on the History-view toggle, so it never carries stale state; (3)
`server/api/model-builder/runs/[id].delete.ts` is a real hard-delete endpoint with no front-end
caller — dead code, not a bug. No genuine new bug found. Per its instructions the agent did not force
a fake fix, made no changes, and opened no PR.

**What was good:** the agent read the entire surface rather than sampling, and rather than reporting
"found nothing" at the first hint of difficulty, it chased three real-looking leads all the way to a
concrete reason each is already safe, citing the specific guarding code/component behavior for each.
This is a substantially more rigorous no-op than earlier cycles' — the three traced-and-closed leads
are worth keeping as documented ground truth so a future cycle doesn't re-open the same false leads.

**What to improve:** none this cycle.

**Kaizen task:** none filed as a new roadmap task — the close-out note flags that after 4 fix/audit
cycles (40-42) plus this no-op (44), pure bug-hunting on the current store/component/API surface has
likely reached diminishing returns; a future cycle may want to widen scope (server-side model schema
validation, or a UX/accessibility pass) rather than repeat the same sweep. Left as guidance in the
task note rather than a separate task, since the recurring task itself is the natural home for that
redirection next time it's picked up.

---
_Generated by [Claude Code](https://claude.ai/code)_

## 2026-08-22 | Agent (scheduled conductor sweep) | model-builder/t-029 cycle 45 | resolution

**Decision:** real bug found and fixed — widened scope to server-side validation per cycle 44's own kaizen note (front-end/store bug-hunting had reached diminishing returns after 4 fix/audit cycles + 1 no-op).

**model-builder/t-029 (cycle 45, real bugs found and fixed, server-side validation gap):** read every `server/api/model-builder/**` route not yet swept by cycle 44's front-end/store pass. `normalizeText()` in `runs/index.ts` writes plain strings into `ModelBuildRun`/`ModelBuildItem` columns with no length option at all. Three call sites wrote into a real fixed-width MySQL `@db.VarChar(n)` column with no cap: `sourceLabel` on the run PATCH route (VarChar(255) — the run **CREATE** route already truncates this same field to 255 chars, so it was validated on create and not on update, a real inconsistency), `staleReason` (item PATCH path, VarChar(255)), and `targetType` (item PATCH path, VarChar(64) — currently dead for client input since `patch-policy.ts` already rejects it before reaching this code, capped anyway for defense-in-depth consistency). An oversized value on `sourceLabel`/`staleReason` reached Prisma unchecked and MySQL would reject the write with a raw "Data too long for column" error (strict mode; silent truncation otherwise) — an opaque 500 instead of the clean 400 every similarly-typed sibling field (`label`/`generation`/`outputKey`/`recipeVersion`/`stage`/`reason`) already returns. Also capped `pitch`/`fieldsDraft`/`promptDraft` at 20,000 chars — they're `@db.Text`, a real 65,535-byte MySQL TEXT limit (not unbounded the way Postgres TEXT is), matching `commit.post.ts`'s own `LONG_TEXT_MAX` so a draft can never grow past what commit would keep anyway. This is the identical bug class `verifyModelBuilderCommitTextTruncationGuard.ts`/`verifyModelBuilderCommitNameWidthGuard.ts` already guard at the commit-time path (cycles 33/35) — just unguarded at the earlier PATCH-while-drafting stage.

Added `verifyModelBuilderPatchTextCapGuard.ts` + `.test.ts` (schema-driven, mirrors `verifyModelBuilderCommitNameWidthGuard.ts`'s convention: walks `prisma/model-builder.prisma` for each guarded field's real column width and fails if its `normalizeText()` call site is missing or mismatched) and wired it into `package.json` + `contract-tests.yml`. Updated `verifyModelBuilderItemPatchStageGuard.ts`'s assignment anchors (and its own test fixtures) to match the new `normalizeText()` call shape — its exact-string anchor broke against the new call shape, a real find surfaced by running the full suite, not a regression introduced carelessly.

First push tripped this repo's own `capture-group-guards` CI contract on the new guard script itself: a compound `if (!match || match.index === undefined)` and two ternaries (`x ? x[1] : fallback`) around regex `.match()` results are actually safe but aren't among the four exact shapes that heuristic recognizes. Fixed by splitting into `if (!x) return` statements, re-verified locally against `origin/main` before re-pushing.

Verified: all 135 `test:model-builder-*` scripts pass, `vue-tsc --noEmit` clean (one pre-existing unrelated error in `server/api/reactions/index.post.ts` confirmed via `git stash` to exist identically on a clean checkout), eslint/prettier clean on every touched file, `capture-group-guards` contract passes against `origin/main`. kind_robots PR #2025: 38/39 checks green at merge time (only the documented non-required "Build production image" job still in flight, `additions`/`changed_files` confirmed scoped to exactly the intended diff), squash-merged `0ad8182`. Closed the roadmap task out via `close_task.py` (re-armed to `ready`, cycle-45 summary appended, `implementation_pr: silasfelinus/kind_robots#2025`).

**What was good:** widened scope exactly as cycle 44's own note suggested rather than repeating an exhausted bug-hunting angle; found the missing-cap gap by cross-referencing every VarChar-backed field written by `normalizeText()` against its real schema column width rather than guessing, and caught the CREATE-vs-PATCH inconsistency (`sourceLabel` truncated on create, not on update) as concrete evidence this was a real regression-shaped gap, not speculative hardening. Ran the full 135-script model-builder suite (not just the new guard) before both pushes, which is what caught the second, unrelated `verifyModelBuilderItemPatchStageGuard.ts` anchor breakage before it reached CI.

**What to improve:** the first push didn't run `verifyCaptureGroupGuards.ts` locally before pushing, costing one avoidable CI round-trip — worth adding to the standard pre-push checklist for any new `.ts` script under `utils/scripts/` that uses `.match()`/`.exec()`, alongside the existing eslint/prettier/vue-tsc checks.

**Kaizen task:** none filed — `pitch`/`fieldsDraft`/`promptDraft`'s new 20,000-char cap only applies at the PATCH-while-drafting stage; a future cycle could audit whether the same cap should also apply at run CREATE time (`runs/index.post.ts`'s `items` mapping currently has no cap on those three fields either, though a run's initial `pitch`/`fieldsDraft`/`promptDraft` are typically empty at creation and only populated via later PATCH calls this fix already covers) rather than leaving it purely PATCH-side.

---
_Generated by [Claude Code](https://claude.ai/code)_

## 2026-08-22 | Agent (scheduled conductor sweep) | model-builder/t-029 cycle 46 | resolution

**Decision:** real gap closed, exactly the one cycle 45's own kaizen note flagged as left open.

**model-builder/t-029 (cycle 46, real bug found and fixed, CREATE-path text cap):** cycle 45 capped `pitch`/`fieldsDraft`/`promptDraft` at `MAX_DRAFT_TEXT_LENGTH` (20,000 chars) on the item PATCH path (`prepareItemUpdate` in `runs/index.ts`), but explicitly left the run CREATE route (`runs/index.post.ts`) unaudited, noting a run's initial draft fields are typically empty at creation and only populated via later PATCH calls the cycle-45 fix already covers. Audited it this cycle: the CREATE route's own `items` mapping had no cap on these three `@db.Text` fields at all — a run created with an oversized draft in its initial payload (a client bug, a replayed request, or a direct API call) would sail through here uncapped and only get caught later, on the first PATCH that re-saves the same field, surfacing as an opaque "Data too long for column" 500 instead of a clean 400. Fixed by importing `MAX_DRAFT_TEXT_LENGTH` into `runs/index.post.ts` and having the local `text()` helper throw a 400 (matching every other validated field in that file) when a value exceeds it, so the two routes can no longer drift apart.

Added `verifyModelBuilderRunCreateTextCapGuard.ts` + `.test.ts` (mirrors `verifyModelBuilderPatchTextCapGuard.ts`'s approach from cycle 45), wired into `package.json` + `contract-tests.yml`.

Verified: all 69 `test:model-builder-*` contract scripts + all 68 `-selftest` variants pass, `vue-tsc --noEmit` clean (same one pre-existing unrelated error in `server/api/reactions/index.post.ts`, confirmed via `git stash`), eslint/prettier clean on every touched file. kind_robots PR #2026: 38/39 checks green at merge time (only the same documented non-required "Build production image" job still in flight, as precedented in cycle 45), squash-merged `ba4fe5a`. Closed the roadmap task out via `close_task.py` (re-armed to `ready`, cycle-46 summary appended, `implementation_pr: silasfelinus/kind_robots#2026`).

**What was good:** treated cycle 45's own "next cycle" note as a direct work order rather than re-deriving scope from scratch, and kept the fix minimal — reusing the existing exported constant rather than picking an independent number, so the two routes structurally cannot drift again (enforced by the new guard, not just by convention).

**What to improve:** none this cycle.

**Kaizen task:** none filed as a new roadmap task — left as guidance in the task note: a future cycle could audit whether any other model-builder write path still leaves a `@db.Text`/`@db.VarChar` field uncapped (e.g. `sourceSnapshot`/`selections`/`usageInfo`, which are JSON-stringified rather than plain text and may need a different kind of size guard than a simple character-length cap).

---
_Generated by [Claude Code](https://claude.ai/code)_

## 2026-08-22 | Agent (scheduled conductor sweep) | model-builder/t-029 cycle 50 | resolution

**Decision:** real bug found and fixed, plus caught that the obvious fix suggested by cycle 49's own note would itself have been a regression.

**model-builder/t-029 (cycle 50, real bug found and fixed, commit stale-gate):** cycle 49 left two leads -- a fresh read of `model-builder-run-history.vue`/`model-builder-source-picker.vue` (not read end-to-end in recent cycles), or the UX-only fix for Execute-commit staying clickable while `COMMIT.status === 'stale'` (cycle 49's own characterization: "cosmetic, not a correctness bug"). Read both flagged components end to end first -- no new bug found there (`source-picker.vue`'s `subtitle()`/`recordImage()` and `run-history.vue`'s cancel-arm/open flows are already correct, matching cycle 31's prior fix). Took the second lead next.

Confirmed cycle 49's read: `commit.post.ts` independently requires every stage other than COMMIT to be `status === 'approved'` before committing, so a stale-commit click (Execute-commit was not disabled while `COMMIT.status === 'stale'`) was a guaranteed round-trip to that server 400 -- and the caught error reset `COMMIT` to `'ready'` via `finishCommit`, silently discarding the accurate "an upstream stage still needs to be redone" signal the `'stale'` badge was showing (the same "badge lying about what's actually stored" class of bug this file already treats as real elsewhere).

But tracing the naive fix cycle 49 implicitly suggested (`item.stages.COMMIT.status === 'stale'` added directly to `:disabled`) found it would have been a real regression, not just a missed cosmetic case: `'stale'` is `COMMIT`'s *only* recovery path in this store. `approveStage`'s "unlock the next stage" branch only flips a *locked* next stage to `'ready'` (`if (next && item.stages[next.key].status === 'locked') ...`) -- it never un-stales one. So once `COMMIT` goes `'stale'`, no other code path ever moves it back to `'ready'`/`'approved'` short of a `commitItem()` call itself succeeding. Disabling on `status === 'stale'` verbatim would have permanently soft-locked the item: re-approving the upstream stage that caused the staleness would leave `COMMIT` stuck at `'stale'` forever with no enabled button left to clear it -- trading a guaranteed-error round-trip for a worse, permanent dead end.

Fixed by mirroring the server's own gate instead of `COMMIT`'s own status: a `BUILD_STAGES`-driven `isCommitBlocked` computed disables the button whenever any non-COMMIT stage isn't `'approved'`, and re-enables the instant it is, regardless of whether `COMMIT`'s own badge still reads `'stale'` or `'ready'`. Added `verifyModelBuilderCommitStaleGateGuard.ts` + `.test.ts` (narrow textual checker, this project's established convention) covering both the missing-gate regression AND the soft-lock-shape regression as two distinct fixtures, wired into `package.json` and `contract-tests.yml`.

Verified: new guard fails pre-fix / passes post-fix (`git stash` round-trip against the real component); all 70 other `test:model-builder-*-guard` contracts + selftests still pass; `test:model-builder-contract-tests-coverage-guard` confirms the new script's wiring; eslint/prettier clean on every touched file; `vue-tsc --noEmit` repo-wide shows only the same pre-existing unrelated `server/api/reactions/index.post.ts` type error documented in prior cycles; `git status --porcelain` scoped to exactly 5 intended files. kind_robots PR #2029: 37/38 checks green at merge time (only the standard non-required "Build production image" deploy job still in flight, matching every prior slice's merge-when-unstable precedent), squash-merged `98fb69a`. Closed the roadmap task out via `close_task.py` (re-armed to `ready`, cycle-50 summary appended, `implementation_pr: silasfelinus/kind_robots#2029`).

**What was good:** didn't implement cycle 49's suggested fix verbatim -- traced its actual consequence through `approveStage`'s real transition logic first and caught that it would have introduced a permanent soft-lock, a worse bug than the one it was meant to fix. The eventual fix mirrors the server's authoritative rule exactly rather than guessing at a client-side heuristic, so the two can't silently drift apart (enforced by the new guard's server-route cross-check, not just convention).

**What to improve:** none this cycle.

**Kaizen task:** none filed as a new roadmap task -- left as guidance in the task note: `model-builder-batch-editor.vue`, `model-builder-progress-matrix.vue`, and `model-builder-recipe-selector.vue` have not been read end-to-end in recent cycles and are the natural next lead, or a fresh audit of `server/api/model-builder/**` against `stores/modelBuilderStore.ts`'s client-side assumptions now that this cycle closed the last open item-panel.vue lead from cycle 49.

---
_Generated by [Claude Code](https://claude.ai/code)_

## 2026-08-22 | Agent (scheduled conductor sweep) | model-builder/t-029 | resolution

**Decision:** ran the full startup sweep (AGENTS.md in full, `git status`/`git log`, GitHub MCP PR check on both conductor and kind_robots -- both clean, no open PRs -- `project-overrides.yaml`-cross-checked roadmap scan, `check_pr_merged_drift.py` clean, `audit_human_gates.py` 54 active gates/1 already-verified stale-state signal, TALKBACK tail clean, `build_dream_proposal.py --check --fetch` -- today's proposal already exists). `select_role.py`'s own GitHub API calls 403'd in this sandbox (documented limitation); cross-checked directly via GitHub MCP instead -- 0 open PRs both repos, `process-task-events.yml` green on every recent run, no stranded branches (only `main` on either repo), site audit not overdue -- confirms `role: worker`. `next_ready_task.py` returned `mermaids-of-venice/t-013` first, but its own note already carried a "Verified no-op on 2026-08-22 Pacific" entry from an earlier session today -- skipped duplicating it, same as that earlier session's own precedent. Walked priority.yaml to the next project with a genuinely workable ready task: `model-builder/t-029`.

**Self-correction, PR #2688 (merged):** the initial `claim_task.py` call for t-029 was mistakenly run with `--owner reviewer` -- AGENTS.md's hard CAN/CANNOT list bars Reviewer from claiming tasks at all, so this was a real process violation, caught immediately. Opened and merged a tiny follow-up PR correcting only the `owner` field to `worker` before doing any implementation work under the (now-correct) claim. All 21 non-CodeQL checks green; the one still-`in_progress` check was the already-documented recurring `Analyze (javascript-typescript)` CodeQL stall (conductor/t-106) -- merged per that task's own established "merge-when-unstable" precedent rather than waiting on a check known not to reliably complete.

**model-builder/t-029 (cycle 54, no-op, real investigation):** chased cycle 53's two named-but-unexplored leads to a real conclusion rather than re-reading already-covered files. (1) Group-switch remount: confirmed `anyBatching` in `model-builder-batch-editor.vue` reads the STORE-level `batchingOutputKey`, not local state, so a fresh instance mounted for a different group correctly observes an in-flight operation from the old group -- no staleness across the `:key="selectedItem.outputKey"` remount. (2) Same-button rapid-double-click: `batchDraftField`/`batchApproveStage` claim `batchingOutputSingleton` synchronously before their first `await`; Vue's disabling re-render is a microtask, which the HTML event-loop spec guarantees drains between any two real browser click events -- closes the race for genuine user double-clicks. Verified cycle 53's `batchApproveStage` finding directly against source (modelBuilderStore.ts:2657-2670): it DOES check both `'locked'` status and `isItemManualActionInFlight`, confirming no bug. Found and chased one new hypothesis: `isItemManualActionInFlight` never checks `state.autoBuildingItemId`, which looked like a real gap given item-panel.vue and batch-editor.vue render side-by-side for the same item's group -- traced `autoBuildItem`'s full body and confirmed every one of its awaited sub-calls claims its own finer-grained singleton for that call's entire span, and JS's single-threaded run-to-completion semantics mean no competing click handler can execute during the synchronous gaps between those sub-calls -- so the omission is real but structurally unreachable, not a live bug. No code change; released the claim; re-armed to `ready` via `close_task.py` (this branch/PR).

**What was good:** treated cycle 53's explicitly-named next leads as the actual task rather than re-deriving new ones, verified two of its conclusions directly against current source instead of trusting the prior note's prose, and surfaced a fresh, specific, well-reasoned hypothesis (the `autoBuildingItemId` gap) before ruling it out with a concrete mechanism rather than "looks fine."

**What to improve:** caught and self-corrected a real process error (claiming with `--owner reviewer`) within the same cycle rather than letting it stand -- flagging as a pattern to watch: double-check `--owner` matches the session's actual `select_role.py`-determined role before running `claim_task.py`, not after.

**Kaizen task:** none filed -- the task's own note now suggests server-side (Prisma schema/migration drift) or the recipe-selector/source-picker data-fetch error handling as untried territory, since every reachable client-state race in the store's batch/auto-build orchestration has now had at least one dedicated cycle.

---
_Generated by [Claude Code](https://claude.ai/code)_

## 2026-08-23 | Agent (scheduled conductor sweep) | model-builder/t-029 | resolution

**Decision:** ran the full startup sweep (AGENTS.md in full, `git status`/`git log`, GitHub MCP PR check on both conductor and kind_robots -- both clean, no open PRs at sweep time -- `project-overrides.yaml`-cross-checked roadmap scan, `check_pr_merged_drift.py` clean, `audit_human_gates.py` 55 active gates/2 already-documented stale-state signals (appmaker/t-010, interface-vision/t-104), TALKBACK tail clean, today's daily-dream proposal not yet authored but well before the digest window -- left for the scheduled step). `select_role.py`'s GitHub API calls 403'd as usual; cross-checked directly via GitHub MCP -- 0 open PRs either repo, confirming `role: worker`. `mermaids-of-venice/t-013` (the top `next_ready_task.py` pick) already had a same-Pacific-day no-op entry from an earlier session this cycle -- walked `priority.yaml` past it to the next genuinely workable task: `model-builder/t-029`.

**Cycle 56 (real fix):** cycle 55 flagged this task's static-reading approach as close to exhausted against its previously-covered territory (client-state races, Prisma/migration drift, recipe-selector/source-picker error handling) and suggested trying recent kind_robots commit history as a fresh lens. Checked `git log` for model-builder-path commits since cycle 51's own fix (5cbffcd, #2030) -- found none, confirming that specific lens is genuinely dry right now. Instead grepped the whole kind_robots repo for every `model-builder`/`modelBuilder`/`ModelBuild` reference and diffed against every file this task's 55-cycle history had already named as read -- surfaced one genuinely unaudited file: `server/utils/suggest/sheets/modelBuilderSuggest.ts` (the 'model-builder' AI-suggest sheet) and its store-side caller.

Traced `modelBuilderSuggest.ts`'s `buildSourceContext()` (which grounds every AI draft in the selected SOURCE record's canon) back to `draftText()` in `modelBuilderStore.ts`: it sent `source: state.selectedSource ?? undefined`. `state.selectedSource` is only ever set by an in-session `selectSource()` call and is deliberately nulled in every "adopt a different run" branch of `resumeRun()`/`openRun()` -- cycle 24's own fix. So after resuming a run (a page reload, or reopening one from Run History, both ordinary paths), `context.source` silently went `undefined` and the suggest sheet's entire canon-grounding block vanished from every AI draft request with no error -- the request still "succeeded", it just drafted generic, ungrounded text that could contradict the source record's established identity. `model-builder-progress-matrix.vue`'s `source` computed had already solved the identical resume-survival problem for its own read-only display card (`run.value?.sourceSnapshot ?? store.selectedSource ?? null`); `draftText`'s request payload just never adopted the same precedence. Fixed by matching it exactly.

Added `verifyModelBuilderDraftSourceSnapshotGuard.ts` + `.test.ts` (57th guard in this task's pattern, covering both the single-line and prettier-wrapped shapes of the fix), wired into `package.json` and `contract-tests.yml`. Verified: new guard fails pre-fix / passes post-fix (fixture round-trip); all 142 `test:model-builder-*` scripts pass; eslint/prettier clean on changed files (two pre-existing `no-empty` errors elsewhere in `modelBuilderStore.ts` and one pre-existing, unrelated `reactions/index.post.ts` `vue-tsc` error confirmed via `git stash`/`git blame` as unaffected); `vue-tsc --noEmit` shows only that one pre-existing error; `git status --porcelain` scoped to exactly 5 files (reverted an incidental `prisma generate` regen diff from local provisioning before committing). kind_robots PR #2047: 37/37 checks green, `mergeable_state: clean`, squash-merged `a32621c3`. Closed the roadmap task out via `close_task.py` (re-armed to `ready`, cycle-56 summary appended, `implementation_pr: silasfelinus/kind_robots#2047`) -- conductor PR #2723.

**What was good:** when the previously-suggested lens (recent kind_robots commit history) came up genuinely empty, didn't stop there or force a finding elsewhere in already-exhausted territory -- ran a repo-wide grep for the project's own name/identifiers and diffed it against this task's own read-history to find a file its established file-set had simply never included. This is a reusable technique, not a one-off: it directly answers "have I actually covered everything reachable by this project's name, or just everything reachable by the file list I happened to start with."

**What to improve:** none this cycle.

**Kaizen task:** none filed as a new roadmap task -- left as guidance in the task note: this cycle's repo-wide-grep-vs-read-history technique is worth running again before assuming client-state-race/Prisma/error-handling territory is the only place left to look, since it just found a real bug in code adjacent to (but outside) that territory's usual file set.

---
_Generated by [Claude Code](https://claude.ai/code)_

## 2026-08-23 | Agent (conductor scheduled Agent run) | model-builder/t-029 cycle 61 | resolution

**Decision:** no-op, real investigation. Task arrived pre-claimed on `origin/main` (`claude-conductor-scheduled-20260823T-model-builder-t029`, cycle 60's own fix already merged as #2049). Confirmed no new model-builder-path commits landed in kind_robots since that merge, and re-ran cycle 56's repo-wide `model-builder`/`modelBuilder`/`ModelBuild` reference grep against the cumulative read-history -- no unaudited file surfaced; every new-looking hit was either another store's comment citing `modelBuilderStore.ts` as precedent, or static nav/seed registration (dashboardHelper/tutorialCards/pageBackdropArtPrompts/projectPlacements), not build-run logic.

Read `model-builder-item-panel.vue` (591 lines, grown since cycle 51) end to end for the first time since its own cycle 59 fix -- every approve/draft/generate control that lacks an explicit `isCommitting` check is structurally unreachable while committing, since `commit.post.ts`'s "every other stage must be approved" gate means those controls always render as their already-guarded 'Edit' variant by the time a commit can be in flight. Read `server/api/model-builder/runs/index.ts` (511 lines: `assertRunAccess`/`assertRunWritable`/`prepareItemUpdate`/`diffStageStatusChanges`/`assertContentStageEditable`) in full as its own file for the first time -- heavily hardened already, no new gap.

Took the task brief's explicit "accessibility gaps" lens for the first time in this task's history. Found what looked like a real sibling-inconsistency: `model-builder-source-picker.vue`/`model-builder-run-history.vue` wrap their loading state in `role="status" aria-live="polite" aria-busy="true"`, `model-builder-batch-editor.vue`'s header spinner and `model-builder-progress-matrix.vue`'s "Auto-build all" spinner have neither. Traced further and ruled it out as not the same class of moment: the guarded pair is a full-region "loading this list from the network at mount" state; the unguarded pair is a button-internal in-flight spinner, a shape uniformly unguarded across every button in this component family (Auto/Draft/Generate/Commit/Auto-build all/group), not selectively skipped on two components. Fixing it as found would either target the wrong two files or scope-creep into a repo-wide spinner-convention decision this single-bug-per-cycle task isn't set up to make well -- left unflagged as a fix, noted as a possible dedicated kaizen task instead.

No new bug found; no code change. `git status --porcelain` clean throughout. Released the claim via direct roadmap edit (re-armed to `ready`, cycle-61 summary appended, `passes: 47`).

**What was good:** caught a plausible-looking a11y "fix" before applying it by checking whether the two sides of the inconsistency were actually the same *kind* of state, not just pattern-matching on a missing attribute -- avoided a wrong-scoped or inconsistent-with-itself change.

**What to improve:** none this cycle.

**Kaizen task:** none filed as a new roadmap task -- left as guidance in the task note: if a future session wants the button-internal-spinner accessibility gap fixed, it should be scoped as its own deliberate repo-wide pass across all five components at once, not picked up piecemeal by this recurring task.

---
_Generated by [Claude Code](https://claude.ai/code)_

## 2026-08-23 | Agent (conductor scheduled Agent run) | model-builder/t-029 cycle 62 | resolution

**Decision:** real fix. Took cycle 61's own option (b) directly instead of filing a separate kaizen task first -- the a11y gap it found (button-internal spinners across item-panel.vue, batch-editor.vue, progress-matrix.vue have no `aria-busy`/`aria-hidden`, unlike source-picker.vue/run-history.vue's full-region loading states) is naturally scoped to this recurring task's own five-component family, not a genuine app-wide sweep, so it didn't need a dedicated new task to be workable this cycle.

Added `aria-busy` (on the button/control) + `aria-hidden` (on the decorative spinner) to every flagged site, mirroring the pattern `model-builder-run-history.vue` already uses on its own cancel button (`:aria-busy="cancellingRunId === run.id"`): item-panel.vue's Auto/Draft-pitch/Draft-fields/Draft-artPrompt/Generate/Commit buttons (6 sites) plus its "Queued…/Rendering…" status line (`role="status" aria-live="polite"`, since it carries live text unlike the button spinners), batch-editor.vue's header "saving batch" spinner (`role="status" aria-live="polite"` + sr-only label), and progress-matrix.vue's "Auto-build all" button. Left batch-editor.vue's "Auto-build group" button alone -- it has no spinner at all today, so adding one would be new UI, not an accessibility annotation.

Verified `prettier --check` clean on the two clean files; progress-matrix.vue carries pre-existing formatting drift on `main` unrelated to this change (confirmed via `git stash` diff before editing), so left untouched rather than running `prettier --write` on the whole file, per the davinci/t-025 lesson recorded in this same TALKBACK.md on 2026-08-23. No conditionals/handlers/markup structure changed -- purely additive ARIA attributes. `git status --porcelain` scoped to exactly the 3 intended files.

Opened kind_robots PR #2053. Its first CI run failed one check ("Contract verifiers"): `verifyModelBuilderItemPanelAutoRunGuard.ts`'s `AUTO_BUTTON_PATTERN` regex required `:disabled` immediately followed by `:title` immediately followed by `@click="store.autoBuildItem(item.id)"` with no attributes in between -- the new `:aria-busy` line landed exactly in that gap. Widened the regex to tolerate an optional `:aria-busy="..."` line (the guard's actual bug-shape contract, `runOperationInFlight` gating `:disabled`, is unaffected), verified the guard and its selftest both pass, then ran all 147 `test:model-builder-*` scripts directly -- 145 passed, the only 2 failures are the pre-existing, already-documented `verifyModelBuilderFieldBlobContinuationGuard` environment limitation (needs Nuxt's `@` alias, unrelated to this change). Pushed the guard fix; the re-run went 36/36 checks green, `mergeable_state: clean`. Squash-merged `a446319b`.

Closed the roadmap task out via a direct edit matching `close_task.py`'s convention (re-armed to `ready`, cycle-62 summary appended, `passes: 48`, `implementation_pr: silasfelinus/kind_robots#2053`) -- conductor PR #2740.

**What was good:** followed the prior cycle's own explicit next-step recommendation instead of re-deriving scope from scratch, and kept the fix's boundary exactly where cycle 61 had already correctly drawn it (button-internal spinners only, not a repo-wide spinner-convention redesign, and no new spinner added where none existed).

**What to improve:** none this cycle.

**Kaizen task:** none filed -- next lead already recorded in the task note (recipe-selector.vue/manager.vue consumer-side sweep for the same convention, cycle 63 candidate).

---
_Generated by [Claude Code](https://claude.ai/code)_
