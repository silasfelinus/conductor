# Weekly Site Audit — 2026-08-23

Per `projects/global-ui/SITE-AUDIT-AGENT.md`, run under the self-assigning `role: site-auditor` path (`scripts/select_role.py`), which flagged the audit as overdue (previous report `AUDIT-REPORT-2026-08-16.md`, 7 days old). No open PRs on `silasfelinus/conductor` or `silasfelinus/kind_robots`, `process-task-events.yml`/`hourly-conductor.yml` green on every recent run, and `daily-digest.yml`'s one failure this week (2026-08-22, a target-repo bug) was already fixed by a same-day dispatch — so nothing outranked the site-auditor role this cycle.

**Method:** cross-referenced all 24 `active` (per `project-overrides.yaml`) conductor project roadmaps against `/home/user/kind_robots/` (API routes, Pinia stores, Vue components, `prisma/schema.prisma`, page routes) using Glob/Grep only — no live HTTP requests were made, no npm/pnpm builds run, no dev server started. `humboldt-scoop-cms` and `kapowarr` were checked against their own local checkouts (`/home/user/humboldtscoopsolutions`, `/home/user/Kapowarr`); `conductor`/`conductor-app` were checked against their own source (`scripts/**`, `.github/workflows/**`, `apps/conductor/**`); `kindrobots-unraid` has no local catalog-repo checkout, so only its kind_robots-side claims were verifiable. Work was split across three parallel research passes (8 projects each): `ai-art-academy, alexa-integration, appmaker, brainstorm, coat-dance, coloring-book, davinci, digital-storefront`; `humboldt-scoop-cms, interface-vision, kapowarr, kind-economy, kind-robots, kindrobots-unraid, lora-ingestion, media-watchlist`; `mermaids-of-venice, model-builder, mural-design, storybook, taskmaster, text-generation, conductor, conductor-app`. This report synthesizes their findings.

## Summary

24 active projects checked, ~200+ spot-checked surface claims across "done" tasks. As in prior weeks, **no genuine code-vs-roadmap surface gaps were found** — every concrete file/route/store/model claim sampled resolved to a real matching artifact in the codebase (a handful only after correcting the auditing agents' own initial path guesses, and two cases were already self-documented drift-corrections the roadmaps themselves had already filed).

The dominant finding this cycle is a different class than prior weeks: **milestone-status staleness**. 20 of 24 projects have at least one milestone whose `status:` field (usually `not-started` or `in-progress`) doesn't match its constituent tasks' actual completion — almost always lagging behind (tasks finished, milestone field never bumped), never the reverse. This is the same pattern kind-robots/t-058 and kapowarr/t-020 previously flagged in isolated cases; this audit is the first to see it as a systemic, ecosystem-wide gap rather than a one-off. It matters because CONTROL.md documents milestones as "the UI/voice progress layer" that flows into the kind_robots front end — stale milestone status is user-facing, not just roadmap bookkeeping.

No functional regressions, no broken user-facing surfaces, and no security-relevant findings.

## Findings by project

### No surface gaps found, no milestone staleness (4 projects)
coat-dance, davinci, kind-robots, taskmaster — task claims and milestone status both matched the codebase and task-completion state exactly.

### No surface gaps found, milestone staleness only (19 projects)
ai-art-academy, alexa-integration, appmaker, brainstorm, coloring-book, digital-storefront, humboldt-scoop-cms, interface-vision, kapowarr, kind-economy, kindrobots-unraid, lora-ingestion, media-watchlist, mermaids-of-venice, model-builder, mural-design, storybook, text-generation, conductor, conductor-app — every checked surface claim matched the codebase; each project has 1 or more milestones whose `status:` field doesn't match its tasks' completion (see below). mural-design additionally has one positive-drift note: t-007's follow-up gap ("mural tab not yet promoted to the wonder.tabs registry") is stale in the other direction — the code has since caught up.

### appmaker — 1 minor path-drift finding (not filed as a task)
`t-014`'s verification note names the mounting component as `components/conductor/conductor-manager.vue`; the actual live path is `components/pages/conductor-manager.vue`. Cosmetic error in a verification-only note, no functional impact — not filed given the 3-task cap and lower impact than the milestone fixes below.

### storybook — 1 minor path-drift finding (not filed as a task)
Several tasks (e.g. t-010) describe `storybook-page.vue` without a directory; it actually lives at `components/conductor/storybook-page.vue`, not `components/pages/`. Content and line counts match exactly — not a real gap, just an implicit path assumption. Not filed for the same reason as appmaker's.

### digital-storefront — 1 minor orphan (not filed as a task)
`components/giftshop/checkout-cancel.vue` and `checkout-success.vue` exist with no roadmap mention — likely an unremarked side effect of the Stripe checkout tasks (t-022/t-023). Noted only, not filed.

## Milestone-status staleness detail (the 3 most impactful instances, filed as follow-ups)

- **conductor** — the worst instance found: all 4 of its own milestones read `status: not-started` despite m1 being 8/8 done, m2 being 102/105 done (3 needs-human), m3 being 3/3 done, and m4 being 4/4 done.
- **digital-storefront** — 4 of 6 milestones stale: m2 (4/4 done, stamped in-progress), m3 (6/6 done, stamped not-started), m4 (12/12 done, stamped not-started), m5 (2/2 done, stamped not-started).
- **kapowarr** — 3 of 9 milestones stale: m4 (3/3 done, stamped in-progress), m6 (11/11 done, stamped not-started), m9 (1/1 done, stamped not-started) — the same pattern t-020 already fixed for this project's m3.

Sixteen other projects also carry at least one stale milestone (appmaker, alexa-integration, brainstorm, coloring-book, humboldt-scoop-cms, interface-vision, kind-economy, kindrobots-unraid, lora-ingestion, media-watchlist, mermaids-of-venice, model-builder, storybook, text-generation, conductor-app) — not filed individually this cycle given the 3-task cap; the pattern and exact milestone IDs are recorded in each research pass's findings (see this report's git history / session TALKBACK for the full per-project detail) for a future audit or a dedicated sweep task to pick up.

## Orphans

Brief, not exhaustive: `components/giftshop/checkout-{cancel,success}.vue` (digital-storefront, noted above).

## Follow-up tasks filed (3, at the spec's cap)

1. `conductor/t-122` — fix all 4 of conductor's own stale milestone status fields. `stakes: reversible`.
2. `digital-storefront/t-044` — fix 4 stale milestone status fields (m2/m3/m4/m5). `stakes: reversible`.
3. `kapowarr/t-069` — fix 3 stale milestone status fields (m4/m6/m9). `stakes: reversible`.

## Boundaries respected

No live HTTP requests were made to kind-robots.vercel.app or kindrobots.org. No npm/pnpm builds were run. No task marked `gate_human: true` was touched. No existing tasks or roadmap entries were deleted. All writes were limited to the three new `ready` tasks above and this report.
