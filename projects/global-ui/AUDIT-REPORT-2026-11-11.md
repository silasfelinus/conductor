# Weekly Site Audit — 2026-11-11

Read-and-report run per `projects/global-ui/SITE-AUDIT-AGENT.md`. No live HTTP requests, builds or
kind_robots mutations. Static path extraction + grep against the local checkout of
`/home/user/kind_robots/` (`main`@`7bc5dce`, 2026-11-10). Writes: this report only.

## Scope

Active/continuous projects per `project-overrides.yaml`: **35** (34 last week). Three passes:

1. Every `server/api|server/utils|components|stores|pages|utils|composables` `.ts`/`.vue` path named
   in each roadmap task — checked for existence.
2. Every `/api/...` route named in an open task (`ready`/`claimed`/`review`/`waiting`/`needs-human`)
   — matched against `server/api/**` (dynamic segments allowed).
3. New this week, per the ruler-hooked/t-053 lesson ("path-existence should also check imports"):
   every existing `utils/*.ts` a roadmap names — checked for a non-test importer.

## Gaps

7 apparent misses across 5 projects; **none is real**:

- [slime-city] `components/slime-city-alleys.vue` (done t-027) — removed when FIVE ALLEYS was folded
  into the unified 20-card CLASH (#4924 and later). `utils/slimeCity/alleys.ts` is still live
  (`clash.ts` imports `alleyDeck`), and `/admin/slime-city-pvp` renders the five-alley field.
  Historical.
- [ruler-hooked] `components/ruler-hooked/ruler-hooked-timing-bar.vue` (t-033, t-053) — last week's
  "real" finding; t-053 closed it as a false positive (control is inline in
  `ruler-hooked-fishing-encounter.vue`, util has live consumers). Historical.
- [playbook-kit] `utils/playbookKit/games/thisMeansWarp.ts` — planned output of ready t-002, not yet built.
- [emperor-of-dust] `stores/emperorOfDustStore.ts` — historical; now `emperorFortressStore.ts`. Carried over.
- [interface-vision] `components/storybook/storybook-mockups.vue`, `utils/scripts/auditWonderLabPreviews.ts`
  — historical / outside scanned set. Carried over.

Pass 2: no open task names an `/api/` route missing from `server/api/`.

Pass 3: 9 utils flagged by the first regex; the 5 non-script ones (`talkEchoes`, `playbook/artLanes`,
`rulerHooked/artLibrary`, `rulerHooked/rulerPresets`, `useOneShotSignal`) all have `~/utils/...`
importers on manual grep (regex missed the `~/` alias). The 4 `utils/scripts/*` entries are CLI
tools/verifiers by design.

## Orphans

The kind_robots checkout's history is grafted at `59e41da` (2026-11-09), so a "files added since the
last audit" diff returns the whole tree and a literal orphan pass stays noisy. Spot-checked four
pages no roadmap names: `/admin/slime-city-pvp` (linked from `slime-city-vs.vue`),
`/admin/zuzu-pinball-workshop` (channel tab `content/channels/admin/zuzu-pinball-workshop.md`),
`/admin/playbook-reviews` (linked from `playbook-forge-console.vue`), `/play/daily-pitches`
(`utils/projectPlacements.ts`). All reachable; none is an orphan.

## Proposed follow-up tasks (0 of up to 3)

None filed: no real gap. Kaizen (not filed — `global-ui` and `conductor` are both `finished`, so
neither can take new tasks without Silas reopening one): commit the three-pass scan as a script so
each weekly run is one command and the alias-aware import check is the default.

## Summary

35 active projects cross-checked. Zero real gaps, zero tasks filed; last week's one finding resolved
as a false positive.
