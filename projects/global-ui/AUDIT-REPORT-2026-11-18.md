# Weekly Site Audit — 2026-11-18

Read-and-report run per `projects/global-ui/SITE-AUDIT-AGENT.md`. No live HTTP requests, builds or
kind_robots mutations. Static path extraction + grep against the local checkout of
`/home/user/kind_robots/` (`main`@`3acf3a3`, 2026-11-17). Writes: this report only.

## Scope

Active/continuous projects per `project-overrides.yaml`: **35** (unchanged). Same three passes as
last week, now run as a single scan:

1. Every `server/api|server/utils|components|stores|pages|utils|composables` `.ts`/`.vue` path named
   in each roadmap task — checked for existence.
2. Every `/api/...` route named in an open task (`ready`/`claimed`/`review`/`waiting`/`needs-human`)
   — matched against `server/api/**` (dynamic segments and method suffixes allowed).
3. Every existing non-script `utils/*.ts` a roadmap names — checked for a non-test importer
   (`~/`, `@/` and relative imports).

## Gaps

6 apparent misses across 5 projects; **none is real**:

- [brainstorm] `components/brainstorm/brainstorm-candidate-card.vue` (done t-007) — **new this week**:
  retired with the old workbench in kind_robots#5187 (2026-11-14) when the riff board took over
  `/brainstorm` (`pages/brainstorm.vue` → `brainstorm-play-console`). The roadmap already describes
  the riff-board direction (reopened 2026-11-03). Historical.
- [playbook-kit] `utils/playbookKit/games/thisMeansWarp.ts` (t-002, now done) — the game was renamed
  Space Couch; t-002's note maps it to `utils/playbookKit/games/spaceCouch.ts`, which exists and is
  registered in `games/index.ts`. Historical.
- [ruler-hooked] `ruler-hooked-timing-bar.vue`, [emperor-of-dust] `stores/emperorOfDustStore.ts`,
  [interface-vision] `components/storybook/storybook-mockups.vue`,
  `utils/scripts/auditWonderLabPreviews.ts` — carried over, historical (see 2026-11-11 report).

Pass 2: two hits on slime-city t-069 (`needs-human`) — `/api/auth/login.post.ts` and
`/api/auth/validate/token.ts` are file paths, and both files exist. No missing route.

Pass 3: 4 utils flagged by the regex; all have live importers on manual grep —
`ecotone/artManifest` (relative `./artManifest` from `ecotone/artStyles.ts`),
`playbook/ecotoneMysteries` (`playbook/ecotone.ts`), `playbook/kit` (store + 4 components),
`playbookKit/games/lanternFerry` (`games/index.ts`).

## Orphans

The kind_robots checkout now has 583 commits of history back to 2026-11-11, so this week a real
"added since last audit" diff of `pages/`, `server/api/` and `stores/` was possible (~40 files). Each
spot-checked surface traces to a merged PR with a roadmap or history reference
(zuzu-gamebook #5179, art slots #5048 → dream-cycle, art request keys #5031 → art-medic, deepheart
#5268, slime-city VS friends #5001, every-villain-tactics #5099, dead-air admin cinema). Four have no
conductor roadmap mention but are site infrastructure, not project scope:

- `server/api/site-feedback/*` + `admin-feedback-capture.vue` (#5086) — admin screenshot feedback
  that files kind_robots issues; the conductor issue bridge mirrors those.
- `server/api/monstrique/bible/*`, `pages/admin/monstrique-bible.vue` (#4994) — Monstrique series bible.
- `server/api/k8/fund*` — scoped-bridge proxies.
- `server/api/tutorial-notes/*`, `server/api/admin/tutorial-notes/*` — Silas Says drafts.

All reachable and admin-scoped; none needs a task.

## Proposed follow-up tasks (0 of up to 3)

None filed: no real gap. The kaizen from last week (commit the three-pass scan as a script) still
stands but `global-ui` and `conductor` are both `finished`, so it stays unfiled until Silas reopens one.

## Summary

35 active projects cross-checked. Zero real gaps, zero tasks filed. One new historical miss
(brainstorm workbench retired by the riff board) is already reflected in its roadmap.
