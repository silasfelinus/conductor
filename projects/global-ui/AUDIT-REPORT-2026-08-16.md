# Weekly Site Audit — 2026-08-16

Per `projects/global-ui/SITE-AUDIT-AGENT.md`, run under the self-assigning `role: site-auditor` path (`scripts/select_role.py`), which flagged the audit as overdue (previous report `AUDIT-REPORT-2026-08-09.md`, 7 days old). No open PRs, no stranded branches, no failing scheduled workflows, and no red/stale PRs on `silasfelinus/conductor` or `silasfelinus/kind_robots` at the time this session started, so nothing outranked the site-auditor role this cycle.

**Method:** cross-referenced all 24 `active` (per `project-overrides.yaml`) conductor project roadmaps against `/home/user/kind_robots/` (API routes, Pinia stores, Vue components, `prisma/schema.prisma`, page routes) using Glob/Grep only — no live HTTP requests were made, no npm/pnpm builds run, no dev server started. For conductor-internal or non-kind_robots projects (conductor, conductor-app, kindrobots-unraid, humboldt-scoop-cms, kapowarr) checked named scripts/docs against their own source instead, per prior weeks' precedent. Work was split across three parallel research passes (8 projects each): `alexa-integration, mermaids-of-venice, coat-dance, taskmaster, appmaker, ruler-hooked, music-mentor, lora-ingestion`; `ai-art-academy, coloring-book, brainstorm, mural-design, storybook, davinci, media-watchlist, conductor-app`; `kapowarr, kindrobots-unraid, conductor, kind-robots, interface-vision, humboldt-scoop-cms, model-builder, digital-storefront`. This report synthesizes their findings.

## Summary

24 active projects checked, ~150+ spot-checked surface claims across "done" tasks. The ecosystem remains well-synchronized: two-thirds of projects (16 of 24) returned **zero findings** at all. The remaining findings split into two classes:

1. **Undocumented file-path drift** (2 projects) — a surface shipped and is genuinely live, but was later renamed/relocated without a correction note the way several other projects (ruler-hooked/t-013, alexa-integration/t-019, kind-robots/t-055, digital-storefront/t-027/t-036) already do for the same class of drift.
2. **Stale milestone-status metadata** (2 projects) — a milestone's own `status:` field wasn't bumped when its tasks progressed, even though the individual task statuses are accurate. Same pattern kind-robots/t-058 already flagged for a different project.

No functional regressions, no broken user-facing surfaces, and no security-relevant findings.

## Findings by project

### No gaps found (16 projects)
ai-art-academy, alexa-integration, appmaker, coat-dance, coloring-book, conductor, conductor-app, digital-storefront, humboldt-scoop-cms, interface-vision, mermaids-of-venice, model-builder, music-mentor, mural-design, ruler-hooked, taskmaster — all spot-checked "done"-status surface claims (API routes, stores, components, Prisma models, scripts, docs) matched the current codebase, or were already covered by a dated correction note in the same roadmap from a prior audit/session.

Two apparent misses on first pass turned out to be false alarms, not gaps: ai-art-academy's starter/example manifests are intentionally served from an external media origin rather than committed to git (documented in `verifyAcademyStarterManifest.ts`); brainstorm's `BrainstormSession`/`BrainstormCandidate` Prisma models live in a separate `prisma/brainstorm.prisma` file rather than the main schema.

### kind-robots — 1 documentation-drift finding
`t-046` (done, 2026-08-08) documents wiring `pages/video-generator.vue` into the `lab` channel. The surface has since moved: the live file is `pages/play/video-generator.vue`, under the `play` channel (`content/channels/play/video-generator.md`, `utils/dataSurfaceManifest.ts`). A later task (t-014) independently confirms the `/play/video-generator` route, but t-046 itself was never corrected — unlike the analogous butterfly-component relocation, which t-055 did correct. Not a functional gap: the feature is live and reachable. **Follow-up filed: `kind-robots/t-065`.**

### lora-ingestion — 1 documentation-drift finding
`t-005`/`t-006` (both done) describe the front end as `pages/lora.vue` plus `components/lora/{lora-card,lora-gallery}.vue`. None of those three exact files exist on current `main`. The actual shipped surface is content-driven: `content/resources.md` mounting `components/resources/resource-manager.vue` (Library/Discover tabs), backed by `resource-gallery.vue`/`resource-card.vue`. Functionally equivalent and live, just under different names than the roadmap records, with no correction note anywhere. **Follow-up filed: `lora-ingestion/t-007`.**

### kapowarr — 1 stale-metadata finding
Milestone `m3` ("POLISH & SHIP") is stamped `status: not-started`, but one of its three tasks (`t-010`) is already `status: done`. **Follow-up filed: `kapowarr/t-020`.**

### kindrobots-unraid — 1 stale-metadata finding (not filed as a task, noted here)
Milestone `m3` ("Core Kind Robots application templates") is stamped `status: not-started`, but 3 of its 4 tasks (`t-005`, `t-006`, `t-013`) are already `status: done`; only `t-007` remains `waiting`. Same pattern as kapowarr's finding above. Not filed as a fourth follow-up task this cycle (spec caps follow-ups at 3, and the kapowarr instance is higher-priority per `project-overrides.yaml`) — worth a session picking this up directly next time it touches kindrobots-unraid, or folding into a future audit's task budget.

### storybook, media-watchlist, davinci — no gaps found
Extensive "done"-task claims (verify-guard scripts, workflow contracts, Prisma models, API routes) all confirmed present and correctly wired.

## Orphans

Brief, not exhaustive: `components/video-lora-picker.vue` (kind_robots) is a LoRA-selection UI for video generation not referenced by any of the 24 roadmaps checked — likely belongs to a video-generation feature area outside conductor's current tracked scope, noted only in passing, not filed as a task.

## Follow-up tasks filed (3, at the spec's cap)

1. `kind-robots/t-065` — correct t-046's stale video-generator path/channel note. `stakes: reversible`.
2. `lora-ingestion/t-007` — correct t-005/t-006's stale file-path claims. `stakes: reversible`.
3. `kapowarr/t-020` — fix stale m3 milestone status field. `stakes: reversible`.

## Boundaries respected

No live HTTP requests were made to kind-robots.vercel.app or kindrobots.org. No npm/pnpm builds were run. No task marked `gate_human: true` was touched. No existing tasks or roadmap entries were deleted. All writes were limited to the three new `ready` tasks above and this report.
