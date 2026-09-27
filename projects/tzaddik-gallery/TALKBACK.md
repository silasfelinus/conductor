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
