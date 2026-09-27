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
