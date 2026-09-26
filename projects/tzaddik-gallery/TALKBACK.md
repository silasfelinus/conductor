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

