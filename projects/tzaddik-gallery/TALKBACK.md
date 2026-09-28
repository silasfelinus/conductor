# Tzaddik Gallery — TALKBACK

## 2026-09-26 | Reviewer → Worker | tzaddik-gallery/t-009 (prep) | pattern

**Decision:** merged (PR #5201, `feat(tzaddik-gallery): accept initial living and memorial seed sets`)

**Failure category:** n/a — clean first-pass merge, no rejection.

**What was good:**
- Data-only, reversible change (`seed-sets.yaml` + note updates to `DESIGN-BRIEF.md`/`roadmap.yaml`), no runtime code touched.
- Verified the Dolly Parton death date against current sources rather than trusting cached/model knowledge (confirmed independently via web search during review — died 2026-08-25, correctly placed in Memorial).
- Seed-sets content matches the already-merged `discovery/2026-09-26.md` docket exactly (all 10 living + 10 deceased LLM discovery names line up), so provenance is traceable end to end.
- Explicit `suggested_by`/`accepted_by_user_id` provenance fields, and the note is careful to say seed-set acceptance is not the same as final canonical-36 curation (t-011 remains the real gate).
- Didn't jump ahead of the dependency chain: t-009 stays `status: waiting` on t-003/t-008 — this PR only staged the manifest it will consume once unlocked.

**What to improve:**
- Nothing structural. Minor nit: `seed-sets.yaml` and the roadmap.yaml hunk both end without a trailing newline — harmless, but worth a habit fix for future manifest-style files.

**Kaizen task:** deferred — the Worker's own suggestion ("require fresh life-status verification for all future accepted discovery batches") is already encoded verbatim in t-009's and t-014's task notes as of this same PR, so a new task would just restate existing scope.

**Pattern note:** This PR landed under the `silasfelinus` GitHub identity rather than a `worker/*`-bot account, consistent with the connector-only Worker pattern in `docs/github-connector-worker.md` (session-aware `task-events`/PR authorship riding the human's own GitHub App install). Treated identically to a normal Worker PR for review purposes, per AGENTS.md.

## 2026-09-26 | Worker → Reviewer | tzaddik-gallery/t-002 | pattern

**Decision:** merged (kind_robots#3050, `feat(tzaddik-gallery): add project route and nav placement`), self-reviewed and self-merged in the same scheduled-agent session that implemented it.

**Failure category:** n/a — clean landing after one CI-driven correction (see below); no Reviewer rejection.

**What was good:**
- Confirmed the Kind Robots `Project` row (id 2119) already existed via the automatic projection sync before writing any new-project code — `channelKey`/`tabKey`/`liveUrl` were the only missing presentation fields, set via `PATCH /api/projects/2119` per `SOURCE_OF_TRUTH.md`'s ownership split, without touching `project-overrides.yaml`.
- Followed the existing `music-mentor.vue` route+nav-tab pattern rather than inventing a new shape.
- Caught and root-caused a real `test:layout-contract` failure pre-merge from a first draft that wrapped the shared `project-front-page` shell inside its own page file: that shell (`components/conductor/project-front-page.vue`) already owns its own `kr-surface`/`kr-scroll` region, and per-file static analysis (`utils/scripts/verifyLayoutContract.ts`) requires every `pages/*.vue`/`*-page.vue` file to independently declare a root-surface class and scroll region in its OWN template — stacking two scroll owners that way would have shipped a real nested-scroll bug, not just a lint false positive. Rewrote the page as self-contained (mirroring `music-mentor.vue`'s proven shape) instead of forcing the shell to work.
- Also caught a Prettier ratchet failure (pure line-wrap) from the same CI run and fixed it before merge rather than leaving red CI for a human to notice.

**What to improve:**
- Didn't do a live browser click-through (no PR-preview environment exists for this repo since the Vercel migration); SSR/hydration is unverified until the next production deploy. Flagged explicitly in the PR body rather than glossed over.

**Kaizen task:** deferred — genuinely no generic improvement beyond what's already tracked; the concrete lesson (project-front-page composition risk) is written above and in the kind_robots PR body for the next session that reaches for that shell from a real routed page.

## 2026-09-26 | Reviewer → Worker | tzaddik-gallery/t-020 (prep) | pattern

**Decision:** merged (PR #5205, `feat(tzaddik-gallery): add editorial tag taxonomy and filters`), after resolving a stale-branch conflict risk.

**Failure category:** n/a — clean content, no rejection; one mechanical merge step before landing.

**What was good:**
- Docs/roadmap-only change (design brief + one new task), reversible, no runtime code or production data touched.
- The tag taxonomy is genuinely well-considered for a sensitive subject: "Politics" is explicitly scoped as descriptive ("materially relevant elected/public-policy/statecraft work"), not an ideological or endorsement axis, and the PR body reiterates that framing unprompted. Geography and living/memorial state are correctly kept out of the tag system as separate structured fields rather than folded in.
- New task t-020 has correct `depends_on: [t-003, t-004, t-005]` and doesn't jump the dependency chain.
- Explicitly anticipates taxonomy sprawl ("avoid one-person micro-tags") and bakes that constraint into the task note itself, not just the kaizen suggestion.

**What to improve:**
- The PR's base commit was already 2+ commits stale by the time it reached review (predating tzaddik-gallery/t-019, which another concurrent session had merged in the interim) — its own "How I verified" claimed "branch is 0 commits behind current main," which was true at authoring time but not at review time. `mergeable_state` came back `unknown` rather than a clean auto-merge. Verified locally: `git merge origin/main` on the PR branch resolved cleanly with git's own three-way merge (t-019 and the new t-020 landed in sequence, no id collision, `validate_roadmaps.py` clean), then pushed that merge commit back to the same PR branch before merging — per AGENTS.md's rotation-collision guidance, this is exactly the "fetch the branch's current remote tip and merge it in" pattern, not a rebase/force-push.

**Kaizen task:** deferred — the "avoid taxonomy confetti" suggestion is already written directly into t-020's own note, so a separate task would just restate it.

**Pattern note:** Second same-project PR in this session to land under the `silasfelinus` identity with a several-minute authoring/review gap wide enough for roadmap drift (t-002's `close_task.py` PRs landed in between). Worth remembering for any future tzaddik-gallery PR: check `next_free_task_id.py` fresh and diff against current `origin/main` before assuming "0 commits behind" still holds by the time a human/session actually reviews it, not just at authoring time.


## 2026-09-26 | Reviewer → Worker | tzaddik-gallery/t-003 | critique

**Decision:** rejected (pass 1)

**Failure category:** quality — kind_robots#3057 added `TzaddikCandidate`/`TzaddikCandidateTag`/`TzaddikRecheckRequest` to `schema.prisma` but never ran/committed `npx prisma generate`. CI's `verify` job (`test:generated-client-parity`) fails, diffing 8 existing generated files and flagging 3 new untracked per-model files under `prisma/generated/prisma/`. `retry_context` written on the task; `passes` incremented to 1.

**What was good:**
- All 31 other checks on the PR pass clean: migration replay against MariaDB, TypeScript, every contract-test suite. The actual schema/model design (candidate/provenance record with living/historical state, controlled tags, structured region metadata, recheck-request auditing) looks sound and matches the task's note in full.
- Single, isolated failure — no scope creep, no unrelated files touched.

**What to improve:**
- Any `schema.prisma` change needs `npx prisma generate` run and the full `prisma/generated/prisma/**` diff committed on the same branch before opening/pushing the PR — this is a mechanical, easily-scripted step (`verifyGeneratedClientParity.ts` exists specifically to catch it) and shouldn't cost a review round-trip.

**Kaizen task:** deferred — this is a first-pass gap for this task, not yet a recurring pattern across tzaddik-gallery cycles worth a dedicated follow-up task. Worth watching for recurrence.

**Pattern note:** none yet — first instance for this project.

---
_Generated by [Claude Code](https://claude.ai/code)_

## 2026-09-26 | Reviewer → Worker | tzaddik-gallery/t-003 | response

**Decision:** merged (pass 2) — audited already-rejected work after fixing it directly

**Failure category:** quality (pass 1, see above) — resolved this session, no new failure.

**What was good:**
- The pass-1 `retry_context` was accurate and specific enough to fix blind: regenerated
  the Prisma client (`npx prisma generate`) on the existing PR branch, and the resulting
  diff matched the retry note's file list exactly (8 modified generated files, 3 new
  per-model files under `prisma/generated/prisma/models/`) with no schema/model changes
  needed.
- Verified before pushing (`npm run test:generated-client-parity` locally clean) rather
  than pushing on faith; all 32 CI checks passed on the re-run, `mergeable_state: clean`
  confirmed before merge. Merged silasfelinus/kind_robots#3057 (squash, fb056ab).
- Closed conductor/tzaddik-gallery/t-003 via `close_task.py` (not a direct push to
  `main`), which surfaced a second real gap: `resolve_deps.py` had not been re-run after
  t-003 flipped to `done`, so t-004/t-005/t-006/t-010 sat `waiting` with their dependency
  already satisfied — caught by the `audit` CI check on the close-out PR itself
  (`silasfelinus/conductor#5255`) before merge, fixed in the same PR by running the
  resolver and re-pushing.

**Kaizen task:** deferred — the fix here is mechanical and already caught by an existing
CI gate (`verifyGeneratedClientParity.ts`); the actual remaining gap (a Worker session
forgetting to run `npx prisma generate` after a schema change) is in the OpenAI Worker's
own workflow, not something a conductor roadmap task can fix. Worth a dedicated kaizen
if this recurs a third time for this project — it hasn't yet.

**Pattern note:** the resolve_deps-after-close gap (t-004/t-005/t-006/t-010 above) is
the second time in this repo's history a close-out has skipped re-running the resolver
(see AGENTS.md's "Task dependencies (pipelines)" section, which already names this as
the Worker's first per-cycle step) — worth considering whether `close_task.py` should
call `resolve_deps.py` automatically for the same project when it sets a task to `done`,
rather than relying on the next session's step-1 discipline or the `audit` CI gate to
catch it after the fact.

---
_Generated by [Claude Code](https://claude.ai/code)_

## 2026-09-27 | Worker → Reviewer | tzaddik-gallery/t-004 | pattern

**Subject:** Built the Living/Memorial tab data plumbing (API + store + kr-gallery wiring)
for a project with zero curated candidates yet — both tabs render `kr-gallery`'s empty
state by design, not as a shortcut.

**Detail:**
- t-002/t-003 shipped the Prisma model and route placement only; there was no API route,
  no Pinia store, and `pages/tzaddik-gallery.vue` was a fully static 3-tab placeholder with
  hardcoded copy and no data at all.
- Added `GET /api/tzaddik?lifeState=LIVING|MEMORIAL` (public, `curationState: APPROVED` only
  — pending/archived candidates stay invisible), `stores/tzaddikStore.ts` (fetch/cache
  pattern copied from `rewardStore.ts`'s `fetchRewards`), and wired the page's Living/Memorial
  tabs onto the shared `kr-gallery` shell. Left the "About the 36" explanation tab untouched
  — it already states plainly this is not a Jewish-religious classification, satisfying the
  task note's explicit requirement.
- Deliberately scoped OUT of this task: the person detail view (t-005), submission workflow
  (t-006), and reactions (no `TZADDIK` reactionCategories value exists — filed as kaizen t-021
  rather than expanding this diff). The DESIGN-BRIEF's elaborate "large-screen single-page
  interface" composition reads as t-005's concern (a person detail view), not t-004's (list
  tabs); flagged this reading in the PR in case a reviewer disagrees.
- Verified: `npm run test` (vue-tsc, full project, exit 0), eslint clean on the 3 changed
  files, prettier clean (fixed one formatting miss before commit), `test:route-gallery-contract`
  and `test:component-reachability` both pass with no new holdouts, and both the
  prettier/lint ratchets improved rather than regressed. Did not exercise the endpoint against
  a live database — no `TzaddikCandidate` rows are curated yet, so there is nothing to query
  a real response against; verified the where-clause logic by reading the schema directly.
- silasfelinus/kind_robots#3058 merged clean (33/33 checks green). Companion
  silasfelinus/conductor#5257 (claim + review transition) also merged clean.

**Kaizen task:** t-021 — add a `TZADDIK` reactionCategories enum value ahead of t-005/t-006's
own UI work, so neither needs its own schema migration cycle just to attach reactions.

**Pattern note:** for a brand-new project where the data model exists but is still empty,
"the feature works" and "the feature has been proven against real data" are different
claims — this cycle could only verify the former (typecheck/contract/lint) and said so
explicitly rather than asserting the tabs had been seen populated.

---
_Generated by [Claude Code](https://claude.ai/code)_

## 2026-09-27 | Worker → Reviewer | tzaddik-gallery/t-021 | pattern

**Decision:** merged (self-merged, `claude/*` session-directed work) | closed to `done`

**Failure category:** null — clean first pass.

**What was good:**
- Added `TZADDIK` to `Reaction_reactionCategory`, `Reaction.tzaddikCandidateId` + its FK/index,
  and a hand-written expand-only migration (`20260927010000_add_tzaddik_reaction_target`)
  following `20260719031500_reaction_first_party_author_expand`'s exact shape.
- Caught my own overreach before it shipped: I first added `tzaddikCandidate` to
  `utils/karmaRefTypes.ts` too, and `verifyEarnedKarmaWiring.ts`/`verifyReactionTargetCoverage.ts`
  correctly failed — that file's contract requires every listed ref type to already carry a
  real, access-checked target column, which `TzaddikCandidate` doesn't have yet (no
  `userId`/`isPublic` pair for the generic content-access branch). Reverted that one file,
  left `getExpectedTargetField`'s `TZADDIK: null` entry with a comment for t-005/t-006, same
  documented pattern as `COMPONENT`.
- silasfelinus/kind_robots#3059 merged clean (37 checks, no forced re-runs). Companion
  silasfelinus/conductor#5259 (claim + review transition) and #5260 (milestone status drift
  fix, unrelated small bookkeeping caught by `check_milestone_status_drift.py` during the same
  session's sweep) also merged clean.

**Kaizen task:** deferred — the PR's own kaizen suggestion (a script flagging a
reachable-but-`null` `getExpectedTargetField` entry that's stayed that way for N days/tasks)
is a reasonable follow-on but not urgent; t-005/t-006 will naturally close it when they wire
the real access rule.

**Pattern note:** landing a new reaction target's schema/enum ahead of its UI task is exactly
two things, not three — the enum+column+migration, and (separately, later) the
karmaRefTypes.ts entry once the target is actually access-checked. Adding the karmaRefTypes.ts
entry early is the natural-feeling but wrong move; the two contract tests exist specifically to
catch that (see `verifyReactionTargetCoverage.ts`'s own history: FACET/PROJECT/CHALLENGE_SUBMISSION).

---
_Generated by [Claude Code](https://claude.ai/code)_

## 2026-09-27 | Worker → Reviewer | tzaddik-gallery/t-005 | pattern

**Decision:** merged

**What was good:**
- Wired the reaction access rule the way t-021's own note asked for it: `TzaddikCandidate` has
  no `userId`/`isPublic` pair, so `getExpectedTargetField`, `assertReactionTargetAccessible`,
  `getContentOwnerId`, and `reactionVisibility.ts`'s `canViewReactionsOn` all got a bespoke
  `tzaddikCandidate` branch instead of a naive entry in the generic maps — the same shape as
  the existing `chatId` special case, and the exact thing the prior TALKBACK entry's pattern
  note warned against skipping.
- Named the new `KarmaRefType` entry `tzaddikCandidate`, not the shorter `tzaddik` the
  reaction-category enum uses, specifically so `verifyEarnedKarmaWiring.ts`'s
  `<target>Id`-stripping regex and `verifyReactionTargetCoverage.ts`'s `${target}Id` equality
  check both pass without an exception carve-out — checked this by running the actual scripts
  rather than reading the regex and assuming it would derive the name I wanted.
- Ran all three reaction/karma contract scripts (`verifyReactionTargetCoverage.ts`,
  `verifyReactionRouteAuth.ts`, `verifyEarnedKarmaWiring.ts`) plus the full `vue-tsc` typecheck
  locally before opening the PR — these are exactly the checks that previously caught
  FACET/PROJECT/CHALLENGE_SUBMISSION being half-wired into this same map, so trusting the map
  "looked complete" without running them would have been the wrong lesson to relearn.
- silasfelinus/kind_robots#3060 merged clean (all checks green, including the ~414-step
  Contract verifiers job). Companion silasfelinus/conductor#5265 (review transition) also
  merged clean.

**Kaizen task:** t-022 — fix the pre-existing (not introduced by this PR)
`eslint-disable-next-line`/`no-explicit-any` mismatch in `getContentOwnerId`'s `modelMap`
declaration, caught while linting this PR's diff.

---
_Generated by [Claude Code](https://claude.ai/code)_

## 2026-09-27 | Reviewer → Worker | tzaddik-gallery/t-022 | pattern

**Decision:** merged (self-implemented and self-reviewed as a Conductor Agent run — no
separate Worker/Reviewer split this cycle)

**Failure category:** null (clean first-pass success)

**What was good:**
- The kaizen note from t-005 already named the exact file, function, and root cause
  (multi-line type putting the actual `any` two lines below its own disable comment),
  which made this a genuinely one-pass mechanical fix.
- Verified with all three checks the task's own scope implied: `eslint` on the changed
  file (clean), `vue-tsc --noEmit` (clean — Prisma's `findUnique` methods are
  structurally compatible with the narrower argument type), and
  `npm run test:lint-ratchet` (327 problems / 24 rules, -3 vs. baseline, ratchet holds).

**What to improve:**
- None — task scope was small and fully self-contained.

**Kaizen task:** none — no further work surfaced by this fix; t-022 was itself a kaizen
task from t-005 and needed no follow-on.

---
_Generated by [Claude Code](https://claude.ai/code)_

## 2026-09-27 | Reviewer → Worker | tzaddik-gallery/t-020 | pattern

**Decision:** merged (self-implemented and self-reviewed as a Conductor Agent run — no
separate Worker/Reviewer split this cycle)

**Failure category:** null (clean first-pass success)

**What was good:**
- `TzaddikCandidateTag`/`TzaddikEditorialTag` and both `server/api/tzaddik` GET routes
  already existed and already returned `Tags` — checked the schema and API before writing
  any UI code, rather than assuming a fresh backend build was needed. That confirmed the
  actual remaining scope was UI-only (display + filter), not a full-stack feature.
- Reused `kr-gallery`'s existing `badges` field for the card tag display instead of adding
  a new prop or bypassing the "kr-gallery stays store-free, parent owns filtering" contract
  called out in that component's own doc comment — filtering lives in the page, not the
  store or the gallery component.
- Verified with `vue-tsc --noEmit`, `eslint`, and `prettier --check` on the changed files
  (all clean) plus full CI (30/30 checks) before merging either PR.

**What to improve:**
- The task description's "filtering by one or more tags" is genuinely ambiguous between AND
  and OR semantics; picked AND (narrowing) and flagged it explicitly in "Flags for Reviewer"
  rather than guessing silently. Worth Silas's opinion if OR turns out to be the expected UX.
- Scoped out "review surfaces" (no such surface exists yet — that's tzaddik-gallery/t-006)
  rather than inventing one to fully satisfy the task's literal wording. Filed as an explicit
  gap for the kaizen task below rather than silently dropped.

**Kaizen task:** tzaddik-gallery/t-023 — extend the same tag-filter chips to the
authenticated submission/review surface once t-006 lands (and confirm AND vs. OR filter
semantics with Silas at the same time).

---
_Generated by [Claude Code](https://claude.ai/code)_

## 2026-09-27 | Reviewer → Worker | tzaddik-gallery/t-017 | critique

**Decision:** merged (silasfelinus/kind_robots#3067, squash dda94d7)

**Failure category:** null (clean first-pass success)

**What was good:**
- CI was fully green before merge (30 checks, including `layout-contract` and
  `TypeScript`) rather than relying on a plausible-looking diff alone.
- Scoped to exactly the 2 files the task called for (`tzaddik-detail-sheet.vue`,
  `pages/tzaddik-gallery.vue`); no admin/moderation controls invented ahead of t-008,
  no splash art faked ahead of t-018 — both explicitly named as deferred in "Flags for
  Reviewer" rather than silently out of scope.
- The PR description named exactly what changed (Living/Memorial/Info under one
  composed lg/xl surface, previous/next nav preserving Living/Memorial context, an
  internally-scrolling person-review rail) and matched the actual diff on inspection
  (no `v-html`/`eval`/secret-shaped patterns, no unrelated files touched).

**What to improve:**
- The `REVIEWING: 2026-09-27T215700Z-tzaddik-t017-a7f3` marker on the PR was posted
  by the same session id as the one that implemented and claimed the task, then never
  followed up with a merge — it sat past its own 20-minute TTL with no action. If a
  connector-only Worker session intends to self-review-and-merge in the same run, it
  should either follow through before the session ends or skip posting a marker it
  won't act on, so a later Reviewer sweep doesn't have to reason about whether a stale
  marker still means "someone's on this."

**Kaizen task:** tzaddik-gallery/t-024 — once t-008 lands moderation/override actions,
surface editor-only approve/archive/override controls in this same composed detail
rail instead of a separate admin page (Worker's own suggestion, taken as-is).

---
_Generated by [Claude Code](https://claude.ai/code/session_01TsV2pBaJxMvPSZBnN9TFvi)_

## 2026-09-27 | Worker → Reviewer | tzaddik-gallery/t-007 | pattern

**Subject:** Audited rather than reimplemented -- the reaction system for TzaddikCandidate
was already fully wired end-to-end before this task was claimed.

**Detail:**
- `select_role.py` flagged t-007 as `audit_candidate: "likely a zero-diff close"` because
  t-006's note mentions it; that hunch was directionally right but the actual mechanism
  was different than "already done, nothing to check" -- t-006's note explicitly says
  "No karma/reaction wiring added -- out of scope," which reads like real work remained.
- Direct code read (server/api/reactions/index.post.ts, .../tzaddikCandidate/[id].get.ts,
  utils/karmaRefTypes.ts, reactionVisibility.ts) plus an independent Explore-agent pass
  both confirmed the opposite: t-005 (kind_robots#3060) had already wired the full
  reaction stack for TZADDIK/tzaddikCandidateId -- write route, read route, access rules,
  karma ref type -- AND already embedded `<reaction-card>` + `<review-list>` in
  tzaddik-detail-sheet.vue, using the exact same components every other gallery
  (character/bot/dream/reward/scenario) uses for its own detail view. t-017's rebuild of
  that same file preserved both controls untouched.
- Closed t-007 `done` with a detailed audit note rather than writing a duplicate/parallel
  reaction UI, and filed the one genuinely open gap (no in-grid discovery affordance on
  the gallery cards) as tzaddik-gallery/t-025 -- a real UX/architecture decision with two
  different-blast-radius implementation paths, not a mechanical follow-on, so it wasn't
  built speculatively here.

**Kaizen task:** tzaddik-gallery/t-025 -- decide and build the in-grid reaction/discovery
affordance (or explicitly decide not to, given the task's own popularity-leaderboard
caution).

**Pattern note:** worth watching for elsewhere in this repo: a task's own dependency note
saying "X wiring not added -- out of scope" can describe what THAT specific PR didn't do,
not what the feature area still lacks overall -- a later PR on the same dependency chain
can close the gap without the downstream task's note ever being updated to say so. Reading
the actual current code (not just the chain of roadmap notes) caught this here.

---
_Generated by [Claude Code](https://claude.ai/code/session_01TsV2pBaJxMvPSZBnN9TFvi)_

## 2026-09-27 | Worker → Reviewer | tzaddik-gallery/t-008 | pattern

**Subject:** Built admin approve/archive + explicit content overrides entirely on
top of t-003's existing schema -- no migration needed.

**Detail:**
- Confirmed via direct code read (and an independent Explore-agent research pass)
  that every override field this task needed, including the image override, was
  already on `TzaddikCandidate` from t-003 (`displayNameOverride`,
  `biographyOverride`, `rationaleOverride`, `objectionsOverride`,
  `imageUrlOverride`, `overrideNote`, `overrideUpdatedByUserId`,
  `overrideUpdatedAt`), and `TzaddikCurationState` already had exactly the three
  states (PENDING/APPROVED/ARCHIVED) this task's state machine needed.
- Followed `server/utils/socialPostDraft.ts`'s shared-util/thin-route split
  (`approveSocialPostDraft`/`rejectSocialPostDraft`) for
  `tzaddikModeration.ts`'s approve/archive/override functions, and this
  feature's own `recheck.post.ts` convention (flat body-based route, not a
  nested `[id]/action`) for the three new routes, rather than introducing a
  third shape.
- Archiving is intentionally not terminal (unlike social-post-draft's
  DRAFT->APPROVED/REJECTED): an admin can restore an ARCHIVED candidate back to
  APPROVED, since PENDING (reject) and APPROVED (retire) both archive through
  the same state and either should be recoverable.
- silasfelinus/kind_robots#3068 merged clean (33/33 CI checks, including
  `verifyReactionTargetCoverage`/`verifyReactionRouteAuth`/
  `verifyEarnedKarmaWiring`/`auditServerApiCallers`/`verifyLayoutContract`/
  `auditIcons`, none of which this change touches but all of which stayed
  green).

**Kaizen task:** tzaddik-gallery/t-026 -- require a confirmation step before
archiving an already-APPROVED (live) candidate specifically, since that's a
higher-stakes action (removes a public roster entry) than archiving a PENDING
submission (declines something never public).

---
_Generated by [Claude Code](https://claude.ai/code/session_01TsV2pBaJxMvPSZBnN9TFvi)_


## 2026-09-28 | Reviewer -> Worker | tzaddik-gallery/t-014 | pattern

**Decision:** merged

**Failure category:** none (clean first pass)

**What was good:**
- Recognized DESIGN-BRIEF.md's "Daily discovery roster" as a two-sided system (a
  conductor-side pipeline plus a kind_robots review surface) and scoped this task to
  only the mechanical half a script can safely own, rather than attempting the full
  Daily-Dream-equivalent contract in one pass. t-015 (review surface) and t-016
  (recurring cadence) were already correctly split out as separate tasks and were
  left alone.
- Proved the pipeline end to end by actually running it to produce
  `discovery/2026-09-28.md` rather than leaving the script unexercised -- a real,
  sourced 10-living/10-deceased batch, deduplicated against both the accepted
  seed set and the prior hand-authored docket.
- Full `tests/` suite (2407 passed, 37 skipped) run locally before pushing, not just
  the new test file, catching the sandbox's `pytest` missing PyYAML in passing
  (already documented in AGENTS.md; `uv tool install pytest --with pyyaml --force`
  fixed it for this session).

**Kaizen task:** tzaddik-gallery/t-027 -- extend `excluded_names()` to also cover
pending/rejected/deferred names via kind_robots once t-015's review surface exists
(currently only sees seed-sets.yaml + prior discovery files, which is honestly
flagged in the PR rather than silently left as a gap).

---
_Generated by [Claude Code](https://claude.ai/code/session_016jW2dqQYD7nbL16s7rd5NB)_

## 2026-09-28 | Worker -> Reviewer | tzaddik-gallery/t-015 | pattern

**Decision:** self-merged (silasfelinus/conductor#5323)

**Failure category:** none (clean first pass)

**What was good:**
- Read t-014's `excluded_names()` docstring closely before designing t-015: it already
  documents the exact dedup contract DESIGN-BRIEF.md wants ("dedupe against canonical,
  historical, pending, rejected, deferred, and recently suggested people") is satisfied by
  keeping every docketed name in the pool permanently, regardless of what decision Silas
  later makes. That meant the review surface itself didn't need to feed back into dedup --
  it only needed to exist and be usable, so scope stayed to a script + a small YAML ledger
  instead of a kind_robots UI/DB build.
- Verified the script against the real dockets (`--check`, `--show`, `--decide`) before
  committing, then explicitly reset the ledger back to `decisions: []` so no fabricated
  decision landed in the PR -- the diff is honestly just the mechanism, no invented data.

**Correction made in the same close-out:** t-014's own kaizen, t-027, assumed t-015 would
require a future kind_robots database for pending/rejected/deferred state and scoped itself
around pulling that via `KR_API_TOKEN`. That premise was wrong once t-015 actually landed
conductor-side -- re-read the note before letting `resolve_deps.py` flip it to `ready` and
corrected it in place (still `ready`, for a quick verify-and-close rather than leaving a
misleading task for the next session to discover was moot).

**Kaizen task:** none new -- see the updated t-027 note above; it's already the queued
follow-on and needs only a quick close, not fresh scoping.

---
_Generated by [Claude Code](https://claude.ai/code/session_01TTvahoTzvjVE2TmqrD6nEs)_

## 2026-09-28 | Worker -> Reviewer | tzaddik-gallery/t-027 | pattern

**Decision:** closed done, no implementation PR (verification only)

**Failure category:** none (task was already satisfied)

**What happened:** t-027 was t-014's kaizen, scoped around a premise that t-015 would
require a kind_robots database for pending/rejected/deferred dedup state. t-015
(silasfelinus/conductor#5323) built a conductor-side review surface instead
(`scripts/tzaddik_review.py` + `discovery-decisions.yaml`), and `excluded_names()`
already keeps every docketed name in its dedup pool permanently regardless of
decision -- confirmed by inspection and by `tests/test_build_tzaddik_discovery.py`'s
existing dedup-violation coverage (29 tests green across both files). There was no
remaining gap to implement.

**Suggested action:** when a kaizen task depends on a not-yet-built task, re-check its
premise against what actually got built before claiming it, not just whether the
dependency reached `done` -- `resolve_deps.py` only checks status, not whether the
assumption still holds.

---
_Generated by [Claude Code](https://claude.ai/code/session_01TTvahoTzvjVE2TmqrD6nEs)_

## 2026-09-28 | Worker -> Reviewer | tzaddik-gallery/t-009, t-010 | pattern

**Decision:** t-010 closed done (implementation PR silasfelinus/conductor#5329, merged);
t-009 parked at status: claimed with a recheck note (silasfelinus/conductor#5328, merged)

**Failure category:** t-010 none (clean first pass); t-009 not a failure -- blocked on
an external deploy step, same class documented in AGENTS.md's "merge is not deploy" gap

**What happened:** Both t-009 and t-010 were sitting `status: claimed` well past
`CLAIM_TTL_MINUTES` (t-009 claimed 00:08 UTC, t-010 claimed 23:18 the prior day, both
still stale at ~04:45 UTC) with no stranded implementation branch for either -- safe to
reclaim directly per `claim_task.py`'s own re-check-against-origin/main behavior.
t-009 confirmed `POST /api/tzaddik/import` (kind_robots#3069, merged 3cf718c) still
returns the Nuxt SPA shell on production, so the actual 29-record import remains
undoable until Silas's next manual Unraid Force Update -- released the claim's *work*
without releasing the *claim itself*, matching the exact pattern the prior two sessions
on this same task already used. t-010 built
`projects/tzaddik-gallery/discovery/living36-research-pool.md` (24 sourced, internationally
diverse living candidates) and placed it inside `discovery/` rather than the project root
specifically so `excluded_names()` picks it up for dedup with zero code changes.

**Suggested action:** none new -- t-011 (FOR SILAS canonical-36 gate) still correctly
waits on both t-009 and t-010; t-009 only needs a production deploy to actually finish.

**Kaizen task:** none new this cycle -- t-010's own file already flags its own
uncertainty cases (Yo-Yo Ma's fit, three mixed-role government/activism candidates) for
Silas directly rather than needing a separate follow-on task.

---
_Generated by [Claude Code](https://claude.ai/code/session_0177zpCHHVc8NczLmpbshxUD)_

## 2026-09-28 | Agent (Claude, scheduled conductor run) | tzaddik-gallery/t-016 | pattern

type: pattern

**Subject:** `build_tzaddik_discovery.py --check` misreported "most recent: None" because its latest-docket lookup relied on alphabetical filename sort, which the deliberately-non-dated `living36-research-pool.md` breaks.

**Detail:**
- `check()` computed `latest = dockets[-1]` off `_files()`'s plain `sorted(glob("*.md"))`. `living36-research-pool.md` sorts after every `YYYY-MM-DD.md` file (letters > digits), so once that pool file existed (t-010), every `--check` run silently reported the wrong "most recent" date -- `None`, since the pool file's `date` field is `None`.
- This is exactly the kind of pipeline-health signal a recurring daily task (t-016) is supposed to trust before deciding whether a new docket is needed; a wrong answer here risks either a skipped build or a duplicate one down the line, even though it happened not to cause either yet.
- Fixed in silasfelinus/conductor worker/tzaddik-gallery-t-016: `check()` now filters to dockets with a real `date` and sorts by date before taking the latest, independent of file glob order. Added a regression test mixing a non-dated file with two dated ones.

**Suggested action:** none needed -- fix is in the same PR as this cycle's t-016 no-op re-arm. Worth remembering as a pattern: any script that walks `discovery/*.md` should treat the non-dated research-pool file as dedup-only input, never as a docket for date/ordering purposes.

---
_Generated by [Claude Code](https://claude.ai/code/session_01ForkQ7aTJTDdzrTtMUeh61)_

## 2026-09-28 | Worker -> Reviewer | tzaddik-gallery/t-011 | pattern

**Decision:** escalated to needs-human (genuine editorial gate, as designed)

**Failure category:** none -- this is the intended shape for a `gate_human: true`
task, not a stuck/failed pass

**What happened:** t-009 and t-010 both closed done, unblocking t-011. Checked
production for community reaction signal before writing anything: all 12 live
seed-set candidates read 0 reactions via `GET /api/reactions/tzaddikCandidate/:id`
-- there is genuinely no community signal yet to weigh, confirming the task's own
note ("editorial choice rather than a mechanical reaction score"). Built
`projects/tzaddik-gallery/CANONICAL-36-CANDIDATES.md`, a plain-language FOR SILAS
presentation of the full 36-slot picture: the 12 already-live candidates, the 24
sourced-but-not-yet-imported research-pool candidates (12 + 24 = 36 exactly), and
the four names (Yo-Yo Ma, Muhammad Yunus, Sonia Guajajara, Agnes Binagwaho) t-010
already flagged as needing an explicit in/out call rather than a default include.
Did not import the 24 research-pool candidates or pick a subset myself --
canonical membership is explicitly Silas's call, and pre-importing them as
`APPROVED` would have made the decision for him.

**Suggested action:** none needed from the Reviewer beyond the normal escalation
review. Once Silas responds with picks, the next Worker session imports the
accepted names via `POST /api/tzaddik/import` (`curationState: APPROVED`) using
the sourcing already gathered in `discovery/living36-research-pool.md`, then
closes t-011 with `approved_by_human: true`.

**Kaizen task:** none new -- t-016 (daily discovery) already exists to keep
filling any slots Silas leaves open.

---
_Generated by [Claude Code](https://claude.ai/code)_

## 2026-09-28 | Agent (Claude, scheduled conductor run) | tzaddik-gallery/t-024 | resolution

type: resolution

**Subject:** t-024 closed as done with no new diff -- its ask was already delivered as a side effect of t-008's implementation.

**Detail:**
- t-024 (kaizen from t-017, filed before t-008 landed) asked for editor-only
  approve/archive/override controls to live in the composed detail rail
  (`tzaddik-detail-sheet.vue`) rather than a separate admin page, once t-008
  shipped moderation/override actions.
- Reading t-008's merged implementation (silasfelinus/kind_robots#3068) shows
  it already built exactly this: an admin-gated `<section v-if="userStore.isAdmin">`
  inside the detail sheet's composed `<aside>` with Approve/Archive buttons and
  a full override form, plus an admin-only "Review queue" *tab* on the existing
  `pages/tzaddik-gallery.vue` (not a separate route/page) for discovering
  PENDING/ARCHIVED candidates that the public Living/Memorial rosters hide.
  Confirmed no `pages/admin/tzaddik*.vue` or equivalent exists.
- No code change was needed. Closed with `close_task.py ... done`, an
  `implementation_pr` pointer to #3068, and a note explaining why.

**Pattern note:** worth watching for elsewhere in this repo -- a "kaizen from
X, once Y lands" follow-up task filed against a dependency that hasn't merged
yet can end up fully subsumed by that dependency's actual implementation,
especially when the dependency's own PR description already names the same
component/file the follow-up task targets. Reading the dependency's merged
diff before claiming a downstream task -- not just checking `status: done` --
caught this here.

**Suggested action:** No action needed from Silas. Surfacing the pattern in
case a future session hits the same "already-subsumed follow-up" shape on a
different project.

---
_Generated by [Claude Code](https://claude.ai/code)_

## 2026-09-28 | Agent (Claude, scheduled conductor run) | tzaddik-gallery/t-025 | resolution

type: resolution

**Subject:** t-025 done -- in-grid reaction/discovery affordance shipped via option (b) from the task note (a bespoke tzaddik-card.vue), not option (a) (extending kr-gallery's generic GalleryItem).

**Detail:**
- Built `components/tzaddik/tzaddik-card.vue`, wrapping `reactable-card` +
  `kr-entity-card-body` the same way `bot-card.vue`/`reward-card.vue` do, and
  swapped the Living/Memorial/Review-queue grids in `pages/tzaddik-gallery.vue`
  onto it via `kr-gallery`'s existing `#item` slot -- no change to the
  generic `GalleryItem` renderer every other gallery shares.
- Earned-karma tracking used the existing generic
  `userStore.trackEarnedKarma('tzaddikCandidate', ...)`; `tzaddikCandidate`
  was already a registered `KarmaRefType` (tzaddik-gallery/t-021), so no
  backend/schema change was needed.
- Registered the new card in `verifyCardActionContract.ts`'s `ENTITY_CARDS`/
  `SHARED_BODY_CARDS` lists (its own comment says "New models get added
  here") -- contract now covers 10 entity cards, up from 9.
- Merged silasfelinus/kind_robots#3076 (squash e3daa2d). Verified: vue-tsc,
  eslint, prettier ratchet, `test:gallery-adoption`, `test:gallery-consistency`,
  `test:card-action-contract`, `test:reaction-targets`,
  `test:reaction-route-auth`, and the full 412-step Contract verifiers job,
  all green before merge.

**Suggested action:** No action needed from Silas. The card surfaces a soft
Living/Memorial + review-state badge and editorial tag chips rather than a
raw vote count, per the task note's explicit warning against an unmoderated
popularity leaderboard.

---
_Generated by [Claude Code](https://claude.ai/code)_

## 2026-09-28 | Agent (Claude, scheduled conductor run) | tzaddik-gallery/t-019 | pattern

type: pattern

**Subject:** The "Request recheck" pipeline had every piece built across three prior tasks (t-005's UI, t-009's fetch util) except the one line connecting them -- recheck.post.ts created a request row and left it PENDING forever.

**Detail:**
- `server/api/tzaddik/recheck.post.ts`'s own header comment said outright: "nothing in this repo runs the actual re-fetch yet." `server/utils/tzaddikSourceRefresh.ts` (t-009) had the Wikipedia/Wikidata/Commons fetch logic fully built and already exercised in production via the bulk import, but nothing called it from the recheck path. The schema (`TzaddikRecheckStatus`: PENDING/CHECKING/NO_CHANGE/UPDATED/NEEDS_REVIEW/FAILED) and the UI (status label, last-checked, the button itself) were also already complete from t-005/t-006 -- the store's `requestRecheck` action already re-fetched the candidate detail after posting, so wiring the backend needed zero store changes.
- This is the second time in this project a task's real remaining scope turned out to be "call the existing thing" rather than "build a new thing" (t-024/t-025 both closed as zero-diff audits of already-satisfied scope). Worth checking for already-built-but-unwired pieces before assuming a task needs new code from scratch.
- Implementation: silasfelinus/kind_robots#3080 (merged, all 32 checks green). Conductor close-outs: silasfelinus/conductor#5359 (review), this close-out (done).

**Suggested action:** No action needed from Silas. Filed tzaddik-gallery/t-028 (kaizen) for the one real gap found while building this: NEEDS_REVIEW recheck requests (a Wikipedia page-id change -- possible redirect) are only discoverable per-candidate today, with no cross-candidate admin queue.

---
_Generated by [Claude Code](https://claude.ai/code)_

## 2026-09-28 | Agent (Claude, scheduled conductor run) | tzaddik-gallery/t-028 | pattern

type: pattern

**Subject:** Extended the existing admin Review-queue tab pattern (Pending/Archived, t-008) with a third Needs-review filter rather than building a new surface.

**Detail:**
- `GET /api/tzaddik?needsReview=true` (admin-only) finds every candidate with a `NEEDS_REVIEW` recheck request and filters to only those whose *latest* request still holds that status, since a later recheck could resolve it. Reused the same gallery/card/detail-sheet plumbing t-008 built for Pending/Archived rather than a bespoke admin page, per AGENTS.md's routes-and-surfaces guidance to prefer an existing surface.
- Implementation: silasfelinus/kind_robots#3081 (merged, 33/33 checks green). Conductor close-outs: silasfelinus/conductor#5361 (review), this close-out (done).

**Suggested action:** No action needed from Silas. Filed tzaddik-gallery/t-029 (kaizen): the queue currently requires opening each candidate's detail sheet to see *why* it needs review; surfacing that reason directly on the card would save a click per item for what's meant to be a scannable queue.

---
_Generated by [Claude Code](https://claude.ai/code)_

## 2026-09-28 | Agent (Claude, scheduled conductor run) | tzaddik-gallery/t-029 | pattern

type: pattern

**Subject:** Rendered data the API already returned (RecheckRequests on the needsReview=true filter) instead of adding a new fetch, and unified the reason-parsing logic across the two surfaces that now use it.

**Detail:**
- `GET /api/tzaddik?needsReview=true` (t-028) already `include`s each candidate's latest `NEEDS_REVIEW` `RecheckRequest` -- the queue card just wasn't rendering it. Widened `TzaddikCandidateWithTags` into an optional `TzaddikModerationQueueCandidate` (only the needsReview filter's response carries `RecheckRequests`) rather than touching the server route.
- `tzaddik-detail-sheet.vue` already had a `recheckDetailLabel` computed parsing `resultJson.reason` / `error` (from t-019). Extracted it into `utils/tzaddikRecheck.ts` and had both the detail sheet and the new card computed use it, so the two surfaces can't drift on how they read the same field.
- Implementation: silasfelinus/kind_robots#3082 (merged, all checks green: vue-tsc/eslint/prettier clean locally first). Conductor close-outs: silasfelinus/conductor#5363 (review), this close-out (done).

**Suggested action:** No action needed from Silas. Filed tzaddik-gallery/t-030 (kaizen): the card now shows *why* a candidate needs review, but resolving it still needs the detail sheet -- an inline accept/dismiss action on the card itself would let an editor clear the whole queue without a click-through per candidate.

---
_Generated by [Claude Code](https://claude.ai/code)_

## 2026-09-28 | Agent (Claude, scheduled conductor run) | tzaddik-gallery/t-030 | pattern

type: pattern

**Subject:** My own kaizen note that spawned this task assumed a resolution mechanism existed that didn't -- corrected scope during implementation rather than building UI against nothing.

**Detail:**
- t-029's kaizen note said an accept/dismiss control should be "backed by the existing recheck-resolution logic." Reading `recheck.post.ts` end to end showed there wasn't any: an identity-changed recheck records `NEEDS_REVIEW` with a diagnostic `reason`/`previousPageId`/`newPageId` in `resultJson`, but nothing ever applies the new page id or clears the flag -- the only existing action was re-running "Recheck," which reproduces the identical `NEEDS_REVIEW` result every time the article identity is still different.
- Built the actual resolution path instead: `resolveTzaddikRecheckReview` (accept re-fetches live and applies the same field set the safe-update branch already writes; dismiss marks the request `NO_CHANGE` with an editor note), a new admin-only `POST /api/tzaddik/recheck-resolve`, and a `tzaddikStore` action wiring both into the queue card.
- Implementation: silasfelinus/kind_robots#3083 (merged, all checks green: vue-tsc/eslint/prettier clean locally first). Conductor close-outs: silasfelinus/conductor#5365 (review), this close-out (done).

**Suggested action:** No action needed from Silas. Filed tzaddik-gallery/t-031 (kaizen): the detail sheet's own recheck section still only offers "Recheck," not the new Update/Keep current actions -- worth the same two buttons there for an editor who opens a candidate from the queue instead of acting on the card directly.

---
_Generated by [Claude Code](https://claude.ai/code)_

## 2026-09-28 | Agent (Claude, scheduled conductor run) | tzaddik-gallery/t-031 | pattern

type: pattern

**Subject:** Gave the detail sheet the same NEEDS_REVIEW Update/Keep-current controls the queue card has, but tightened the show condition against the server's actual guard rather than copying the card's.

**Detail:**
- `tzaddik-card.vue` (t-030) shows its Update/Keep-current buttons whenever `recheckReasonLabel(...)` returns non-empty text, which is true for both `NEEDS_REVIEW` (with a `reason`) and `FAILED` (with an `error`) recheck requests. `POST /api/tzaddik/recheck-resolve` (`resolveTzaddikRecheckReview`) only accepts a resolution when the latest request is actually `status: NEEDS_REVIEW` -- it 409s otherwise. So the card's own condition has a latent path to a 409 on a `FAILED` recheck, currently unreachable per t-029's note that only the `needsReview=true` queue filter's response carries `RecheckRequests` at all.
- Rather than copy that same condition into the detail sheet, gated the new `needsRecheckReview` computed there on `latestRecheck.value?.status === 'NEEDS_REVIEW'` explicitly, matching the server's real guard.
- Implementation: silasfelinus/kind_robots#3084 (merged, all checks green: eslint/prettier/vue-tsc/layout-contract clean locally first). Conductor close-outs: silasfelinus/conductor#5368 (review), #5369 (done) -- both self-merged in the same scheduled session.

**Suggested action:** No action needed from Silas. Left a kaizen suggestion on the PR itself: tighten `tzaddik-card.vue`'s condition the same way, closing the latent (currently unreachable) 409 path there too. Worth a dedicated conductor task if a future session doesn't pick it up as an ordinary kaizen off this PR.

---
_Generated by [Claude Code](https://claude.ai/code)_

## 2026-09-28 | Agent (Claude, scheduled conductor run) | tzaddik-gallery/t-032 | pattern

type: pattern

**Subject:** Closed the same latent-409 gap t-031 left open on the card's own recheck buttons -- kaizen'd from t-031's PR, implemented as a matching but independent fix.

**Detail:**
- t-031 tightened the detail sheet's Update/Keep-current condition to `status === 'NEEDS_REVIEW'` but left `tzaddik-card.vue`'s own equivalent buttons on the broader `recheckReasonLabel(...)` non-empty check, which is also true for a `FAILED` recheck (a non-empty error string). `resolveTzaddikRecheckReview` still 409s on anything but `NEEDS_REVIEW`.
- Added a `recheckNeedsReview` computed reading `RecheckRequests?.[0]?.status === 'NEEDS_REVIEW'` directly and gated the button block on it, mirroring the detail sheet's fix rather than re-deriving anything from `recheckReasonLabel`.
- Currently unreachable in production either way, per t-029's note that only the `needsReview=true` queue filter's response carries `RecheckRequests` at all -- this closes the gap before it becomes reachable, same rationale as t-031.
- Implementation: silasfelinus/kind_robots#3085 (merged, all 29 checks green -- vue-tsc/eslint/prettier verified clean locally first). Conductor close-outs: this PR (review + done, same session).

**Suggested action:** No action needed from Silas. Both card and detail-sheet surfaces now match the server's guard exactly; worth grepping for any third consumer of `RecheckRequests[0]` before adding a fourth surface, per t-032's own kaizen note in `LEARNING.yaml`.

---
_Generated by [Claude Code](https://claude.ai/code)_
