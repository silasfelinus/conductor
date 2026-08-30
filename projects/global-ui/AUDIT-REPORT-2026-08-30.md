# Weekly Site Audit — 2026-08-30

Per `projects/global-ui/SITE-AUDIT-AGENT.md`, run under the self-assigning `role: site-auditor`
path (`scripts/select_role.py`), which flagged the audit as overdue (previous report
`AUDIT-REPORT-2026-08-23.md`, 7 days old). No open PRs on `silasfelinus/conductor` or
`silasfelinus/kind_robots` at session start, so nothing outranked the site-auditor role this
cycle.

**Method:** cross-referenced all 29 `active` (per `project-overrides.yaml`) conductor project
roadmaps against `/home/user/kind_robots/` (API routes, Pinia stores, Vue components,
`prisma/schema.prisma` + split `prisma/*.prisma` files, page routes) using Glob/Grep only — no
live HTTP requests were made, no npm/pnpm builds run, no dev server started. `humboldt-scoop-cms`
was checked against `/home/user/humboldtscoopsolutions/`, `kapowarr` against
`/home/user/Kapowarr/`, and `conductor`/`conductor-app` against the conductor repo itself
(`scripts/**`, `.github/workflows/**`, `apps/conductor/**`). Work was split across four parallel
read-only research passes (7-8 projects each): `ai-art-academy, alexa-integration, appmaker,
brainstorm, coat-dance, coloring-book, cthulhuquarium, davinci`; `digital-storefront,
humboldt-scoop-cms, interface-vision, kapowarr, kind-economy, kind-robots, kindrobots-unraid`;
`lora-ingestion, mandarin-tutor, media-watchlist, mermaids-of-venice, model-builder,
mural-design, rainbow-butterflies`; `ruler-hooked, scene-animator, storybook, taskmaster,
text-generation, conductor, conductor-app`. This report synthesizes their findings.

## Summary

29 active projects checked, several hundred spot-checked surface claims across `status: done`
tasks. **No genuine code-vs-roadmap surface gaps were found, and no orphans of note** — every
concrete file/route/store/model claim sampled resolved to a real matching artifact in the
codebase. This is the second consecutive clean cycle on that front (see 2026-08-23's report),
and this week's passes note several projects' own prior self-correcting tasks (e.g.
kind-robots/t-051, digital-storefront/t-027, kind-robots/t-055, ruler-hooked/t-013) as the
likely reason drift keeps getting caught before it reaches a weekly audit.

The dominant finding this cycle is a **detection gap in `check_milestone_status_drift.py`
itself**, not a one-off roadmap mistake. That script (t-135, added after last week's systemic
milestone-staleness finding) deliberately checks only two mismatch shapes — a not-started
milestone with done work under it, and a done milestone with open work under it — reasoning in
its own docstring that "there is no task-count shape that makes 'in-progress' clearly wrong."
This audit found that reasoning has a real gap: a milestone reading `in-progress`/`planned`
while *every* task under it is already `done` is exactly as wrong as the DONE-WITH-OPEN-WORK
case, just inverted, and the script currently exits clean while missing it — confirmed by this
session's own `check_milestone_status_drift.py` run at startup, which reported zero drift right
before this audit's passes turned up five real instances of exactly this shape.

No functional regressions, no broken user-facing surfaces, and no security-relevant findings.

## Findings by project

### No surface gaps found, no milestone staleness (21 projects)
alexa-integration, coat-dance, coloring-book, davinci, digital-storefront, humboldt-scoop-cms,
interface-vision, kapowarr, kind-economy, kind-robots, kindrobots-unraid, lora-ingestion,
mandarin-tutor, media-watchlist, mural-design, ruler-hooked, scene-animator, storybook,
taskmaster, text-generation, conductor-app — every checked surface claim matched the codebase,
and milestone status agreed with task completion throughout.

### No surface gaps found, minor milestone-staleness instances found (4 projects, filed below or noted)
appmaker (m1 in-progress, 2/2 tasks done), cthulhuquarium (m1 in-progress, 10/10 tasks done —
**filed as cthulhuquarium/t-064**), model-builder (m5 in-progress, 5/5 tasks done),
rainbow-butterflies (m1 in-progress, 4/4 tasks done). All four are the identical shape: a
non-done milestone status with 100% task completion underneath. Only cthulhuquarium's instance
is filed as its own task this cycle (see "Follow-up tasks filed" below); appmaker/m1,
model-builder/m5, and rainbow-butterflies/m1 are documented here and in conductor/t-138's note
for a future session or the same PR that widens the detection script to also fix directly,
given this audit's 3-task cap.

### brainstorm — systemic milestone staleness across nearly the whole roadmap (filed as brainstorm/t-032)
Every milestone (m0 through m5) reads `in-progress` or `planned` despite 100% task completion
under each (m0 3/3, m1 5/5, m2 3/3, m3 3/3, m4 6/6, m5 9/9); only m6 (1/2, t-023 still
`needs-human`) is genuinely still open. This is the same detection-gap shape as the four
single-milestone instances above, just concentrated across one entire project's roadmap rather
than one milestone — the most impactful single fix available this cycle, so it was prioritized
over the isolated single-milestone instances given the 3-task cap.

### mermaids-of-venice — one very minor, not-filed nit
m4 reads `not-started` even though its only task (t-009) already has a written site-plan doc
and sits at `needs-human` — arguably `in-progress` reads better. Intentionally parked at Silas's
direction; not worth a task on its own.

### conductor — two low-severity, not-filed observations
- t-010 (`scripts/generate_changelog.py`, done): the script exists and works as written, but no
  `CHANGELOG.md` exists at the repo root and nothing invokes the script from any workflow or doc
  — it appears to have never actually been run since being marked done. Low severity; the
  task's own scope was just "write the script."
- t-078 (informational, not a build task): its note cites a WonderLab review pipeline
  (`server/utils/wonderLabReviewDraftGenerator.ts` and two config files) as "already landed" on
  kind_robots main as of 2026-07-21; none of the three exist in kind_robots today. Plausibly
  superseded by later work and never re-verified. Worth a fresh look only if anyone revisits
  WonderLab review tooling.

### kind-economy — one unconfirmed, not-filed item
t-027's note describes an allowlist-style CI contract test enumerating every LLM/comfy-reaching
API route as "also in scope"; no such test currently exists in kind_robots. The two actual
metering-gap fixes the task's title is about are confirmed present and correctly gated. Given
the shallow local git history, this can't be fully ruled out as later-removed vs. never-built,
and the note doesn't unambiguously claim it shipped — not flagged as a hard gap.

## Orphans

None of note. coat-dance's `components/conductor/coat-dance-page.vue` has no dedicated roadmap
task, but this is the shared generic conductor project-front-page pattern every project gets,
not a coat-dance-specific gap.

## Follow-up tasks filed (3, at the spec's cap)

1. `conductor/t-138` — widen `check_milestone_status_drift.py` to also flag a non-done
   milestone status with 100% task completion underneath (the systemic fix — prevents this
   whole class of finding from needing manual rediscovery every week). `stakes: reversible`.
2. `brainstorm/t-032` — reconcile milestone status fields m0 through m5 to `done` (m6 stays
   `in-progress`); the most impactful single instance found this cycle. `stakes: reversible`.
3. `cthulhuquarium/t-064` — flip m1's status from `in-progress` to `done` (10/10 tasks done).
   `stakes: reversible`.

appmaker/m1, model-builder/m5, and rainbow-butterflies/m1 are the same shape and equally safe to
fix, but are left undocumented as their own tasks given the cap — see conductor/t-138's note,
which names all three explicitly for whoever picks that task up next.

## Boundaries respected

No live HTTP requests were made to kindrobots.org or any Vercel host. No npm/pnpm builds were
run. No task marked `gate_human: true` was touched. No existing tasks or roadmap entries were
deleted. All writes were limited to the three new `ready` tasks above and this report.
