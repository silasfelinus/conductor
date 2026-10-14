# Weekly Site Audit — 2026-10-14

Read-and-report run per `projects/global-ui/SITE-AUDIT-AGENT.md`. No live HTTP requests, npm/pnpm
builds, or kind_robots mutations. Cross-checks used static path extraction and grep against the
local read-only checkout of `/home/user/kind_robots/` (`main`@`5905d41`, 2026-10-13).
The only writes are this report.

## Scope

Active/continuous projects per `project-overrides.yaml`: **26** (the 2026-10-07 report counted 33;
the difference is projects since flipped to finished/paused). All 26 have a roadmap.

## Method

For each active roadmap, extracted every `server/api|server/utils|components|stores|pages|utils`
`.ts`/`.vue` path mentioned and checked it exists in kind_robots. Each miss was read in roadmap context.

## Gaps

**None.** 3 apparent misses across 2 projects, none a real gap:

- [interface-vision] `components/storybook/storybook-mockups.vue` — the DONE note describes the
  mockups served at `/storybook-mockups`; the component was later replaced by
  `storybook-collection/-ending/-life-run.vue` (still present). Historical reference.
- [interface-vision] `utils/scripts/auditWonderLabPreviews.ts` — named in a done-task note
  (PR #1434); script lives outside the scanned path set today. Historical reference.
- [zuzu-gamebook] `utils/zuzuGamebook/acts/act1-4.ts` — shorthand for `act1.ts`..`act4.ts`, all present
  (plus `act5`-`act9` and `index.ts`).

Last week's retired-surface set (mission-accrual, artArchiveMediaPaths, etc.) belongs to projects no
longer active and no longer appears.

## Orphans noticed

Same caveat as prior weeks: roadmaps name domain features rather than directory paths, so a
literal-name orphan pass is noisy. No new genuine orphan identified.

## Proposed follow-up tasks (0 of up to 3)

None filed — no path-level gap survived reading in context.

## Summary

26 active projects cross-checked. Zero gaps, zero new tasks.
