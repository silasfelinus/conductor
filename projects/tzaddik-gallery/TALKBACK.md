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

