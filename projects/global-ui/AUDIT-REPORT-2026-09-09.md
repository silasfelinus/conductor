# Weekly Site Audit — 2026-09-09

Read-and-report run per `projects/global-ui/SITE-AUDIT-AGENT.md`. No git/build/live-HTTP
commands were run against `kind_robots`; all cross-checks used Glob/Grep/`git log` against a
local read-only clone of `/home/user/kind_robots/`. All writes were limited to this report and
one new roadmap task.

## Scope

Active projects per `project-overrides.yaml` (`status: active`) — same 29 projects as the
2026-09-02 audit, unchanged: ai-art-academy, alexa-integration, appmaker, brainstorm,
coat-dance, coloring-book, conductor, conductor-app, cthulhuquarium, davinci,
digital-storefront, humboldt-scoop-cms, interface-vision, kapowarr, kind-economy, kind-robots,
kindrobots-unraid, lora-ingestion, mandarin-tutor, media-watchlist, mermaids-of-venice,
model-builder, mural-design, rainbow-butterflies, ruler-hooked, scene-animator, storybook,
taskmaster, text-generation.

### Not a kind_robots-surface project (quick-checked only)

Same 8 as last time minus alexa-integration, which moved into the full-audit set this round
(it references real kind_robots surfaces — `stores/serendipityVoiceStore.ts`,
`components/pages/serendipity-page.vue` — deep enough to warrant full treatment, matching how
the 2026-09-02 report actually treated it despite listing it in this section):

- **kapowarr**, **kindrobots-unraid**, **conductor**, **conductor-app**,
  **humboldt-scoop-cms** — unchanged from 2026-09-02; no recently-updated tasks introduce a
  new kind_robots-surface claim.
- **mermaids-of-venice** — unchanged; the one surface reference remains the
  human-owned personal-note placeholder awaiting Silas's text.
- **coat-dance** — unchanged; zero kind_robots surface references.
- **mural-design** — unchanged; its one surface (`/mural` page) remains already-shipped.

The other 21 projects (20 from last time plus alexa-integration) were cross-checked against
`/home/user/kind_robots/`: kind-robots, interface-vision, model-builder, digital-storefront,
ai-art-academy, coloring-book, brainstorm, storybook, davinci, media-watchlist, taskmaster,
appmaker, ruler-hooked, lora-ingestion, kind-economy, cthulhuquarium, mandarin-tutor,
rainbow-butterflies, alexa-integration, text-generation, scene-animator.

## Method

Read the 2026-09-02 report in full first and used its "Notable non-findings" list to avoid
re-reporting already-known/already-fixed items. Then ran a full static extraction of every
`server/api/`, `components/`, `stores/*Store.ts`, and `pages/` path mentioned anywhere across
all 21 full-audit roadmaps (307 unique paths) and checked each against the current checkout —
this both catches drift introduced since 2026-09-02 and doubles as a spot-check of older
tasks (no `status: claimed` tasks exist across any of the 21 right now, so there was nothing
else to sample in that bucket). Extra attention went to tasks with `updated:` dates on or
after 2026-09-02, since those are most likely to introduce genuinely new drift the prior audit
couldn't have seen.

## Gaps

One real, previously-undocumented drift, spanning several projects because it's a single
shared subsystem:

**`components/abandonware/` — the app-wide convention for parking orphaned/unreferenced
components instead of deleting them — has disappeared from the kind_robots checkout entirely,
and no roadmap task anywhere records why.**

- `[kind-robots]` `components/abandonware/butterfly/store-butterfly.vue` — kind-robots/t-055
  (done) records this as the current location, and the 2026-09-02 audit itself confirmed it
  live at that path. Not found now.
- `[interface-vision]` `components/abandonware/conductor/plan-projects-grid.vue` — confirmed
  relocation destination per interface-vision/t-101 (done, citing kind_robots PR #1475 "Park
  orphaned components in abandonware," 80+ files moved 2026-08-05). Not found now.
- `[interface-vision]` `components/abandonware/pages/registration-form.vue`,
  `components/abandonware/themes/theme-manager.vue`,
  `components/abandonware/wonderlab/lab-gallery.vue` — referenced in interface-vision/t-104's
  note history (most recently updated 2026-09-09). Not found now.
- `[digital-storefront]` `print-swag.vue` under `components/abandonware/` —
  digital-storefront/t-037/t-003 describe it as parked there. Directory and file both gone.
- `[ruler-hooked]` `components/abandonware/butterfly/single-slider.vue` — ruler-hooked/t-012/
  t-013 record it as parked (not deleted). Not found now.
- `[ai-art-academy]` `components/abandonware/builder/builder-manager.vue` — ai-art-academy/
  t-057 (done) confirms it "retired/unused via the abandonware/ convention." Not found now.

This reads as new, not another instance of an already-known non-finding: the 2026-09-02 report
explicitly verified some of these files as currently existing under `components/abandonware/`
at the time. As of this audit, `find`/`git ls-files`/`git log --all -- components/abandonware`
all show zero trace of the directory in the local checkout's available history (~55 commits).
Yet `nuxt.config.ts:288` (`ignore: ['abandonware/**/*.vue']`), `tsconfig.json:15` (`exclude:
[..., "components/abandonware/**/*"]`), and `utils/scripts/verifyComponentReachability.ts`
(current-tense logic, `PARKED_SEGMENT`, broken-import checks, PR-facing guidance text) still
actively treat it as live policy. Unlike kind-robots/t-091's resolved Component-model case,
nothing here shows the coordinated cleanup pattern (updated CI guards, a closing
investigation) — the config/tooling references were simply left dangling. Filed as
**kind-robots/t-095**, modeled directly on t-091/t-051's precedent.

Everything else the 307-path static scan flagged as "missing" reproduces the 2026-09-02
report's own "Notable non-findings" list path-for-path (the `Component` model/routes already
closed by t-091; `art-maker.vue`, `social-publisher.vue`, `store/checkout.post.ts`,
`stripe/charge.ts`, `lora.vue`/`lora-card.vue`/`lora-gallery.vue`, `swipe-deck.vue`,
`compositionStore.ts`, `displayStore.ts`, `linkStore.ts`, `lab-manager.vue`/
`component-review-feed.vue`, `wonderlab-review-rollout.vue`, `narrator-chat.vue`,
`kind-icons.vue`, `character-interact.vue`, `storybook-mockups.vue`,
`conductor-art-gallery.vue`, `art-reactions.vue`, `serendipity-voice-page.vue`,
`pages/video-generator.vue` → `pages/play/video-generator.vue`, `curate-request.post.ts`) — no
new instances beyond the abandonware cluster above. A few additional pre-2026-09-02,
`status: done` mentions were run down as extra due diligence (`artjob-manager.vue`,
`home-feed-placeholder.vue`, `projects/[id]/art/prepare-generation.post.ts`,
`socials/[id].patch.ts`) — all self-documented as already retired/deleted elsewhere, not gaps.

All paths from tasks updated since 2026-09-02 across kind-robots, interface-vision,
model-builder, storybook, appmaker, cthulhuquarium, and rainbow-butterflies (~150 concrete
surfaces) resolved cleanly, including rainbow-butterflies' kind_robots-side backend surfaces
(`server/utils/rainbowDashboard.ts`, `server/utils/agentMessaging.ts`, `agent-profiles/*`, the
`AgentProfile`/`AgentCredential` Prisma models — which live in split schema files, not the
monolithic `prisma/schema.prisma`, worth remembering for future audits) — while its front-end
paths correctly live in the separate `silasfelinus/rainbowbutterflies` repo and aren't
kind_robots surfaces to check.

## Orphans noticed

None new. Every current top-level `server/api/` directory (66 total) and every top-level
`components/` directory (46 total) is referenced by at least one active project's roadmap. The
two previously-noted minor infra routes not named in any active roadmap
(`server/api/suggest.post.ts`, `server/api/version.get.ts`) are still un-referenced and still
read as too trivial for a dedicated task, matching the 2026-09-02 assessment. The
`components/abandonware/` finding above is the inverse of an orphan — a vanished surface,
rather than a new unclaimed one.

## Proposed follow-up tasks (1 of up to 3)

1. **kind-robots/t-095** — "Investigate and document the disappearance of
   `components/abandonware/` and the now-dangling ignore rules that still reference it" —
   `status: ready`, `stakes: reversible`, `owner: null`. Landed in
   `projects/kind-robots/roadmap.yaml`. Mirrors the successful t-091 (Component model)
   investigation pattern.

## Summary

29 active projects were in scope; 8 were judged not to be kind_robots-surface projects (brief
note only, one fewer than last time since alexa-integration moved into full-audit) and 21 were
fully cross-checked against `/home/user/kind_robots/`. The roadmap ecosystem remains unusually
well self-auditing — a from-scratch full-path extraction across all 21 full-audit roadmaps
turned up nothing the 2026-09-02 report hadn't already found and closed, apart from one new,
genuine, and moderately significant finding: the entire `components/abandonware/` archive
convention — used across at least six active projects to park rather than delete orphaned
components — has vanished from the checkout with no roadmap record of when, why, or what
replaced it, while the tooling that assumes it exists (`nuxt.config.ts`, `tsconfig.json`,
`verifyComponentReachability.ts`) was left unchanged. Filed as kind-robots/t-095.
