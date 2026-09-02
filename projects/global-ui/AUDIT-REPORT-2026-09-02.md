# Weekly Site Audit — 2026-09-02

Read-and-report run per `projects/global-ui/SITE-AUDIT-AGENT.md`. No git/build/live-HTTP
commands were run; all cross-checks used Glob/Grep against a local read-only clone of
`/home/user/kind_robots/`. All writes were limited to this report and up to 3 new roadmap
tasks.

## Scope

Active projects per `project-overrides.yaml` (`status: active`), exactly as listed:
kapowarr, kindrobots-unraid, conductor, kind-robots, text-generation, interface-vision,
humboldt-scoop-cms, model-builder, digital-storefront, ai-art-academy, coloring-book,
brainstorm, mural-design, storybook, davinci, media-watchlist, conductor-app,
alexa-integration, mermaids-of-venice, coat-dance, taskmaster, appmaker, ruler-hooked,
lora-ingestion, kind-economy, cthulhuquarium, scene-animator, mandarin-tutor,
rainbow-butterflies (29 projects).

### Not a kind_robots-surface project (skipped after a quick check)

These roadmaps either describe a separate repo/app entirely, or only mention kind_robots
paths in passing (incident notes, a consuming REST client, etc.) rather than describing
kind_robots surfaces to build/verify:

- **kapowarr** — personal fork of an unrelated app; its one kind_robots mention is about
  the sync mechanism (`server/api/conductor/sync.post.ts`) used *by* Conductor, not a
  kapowarr feature.
- **kindrobots-unraid** — Unraid/Docker infrastructure project; its schema/Prisma mentions
  are about deployment verification, not app surfaces.
- **conductor** — the coordination system's own roadmap; its kind_robots file mentions are
  incident/kaizen notes about bugs already found and fixed elsewhere, not surfaces this
  project is building.
- **conductor-app** — a Flutter native mobile client that *consumes* the kind_robots REST
  API; its references to `stores/conductorStore.ts` / `components/conductor/*.vue` are
  cross-references for parity, not Flutter's own surfaces.
- **humboldt-scoop-cms** — a separate WordPress + Flutter field-ops repo
  (`humboldtscoopsolutions`), not kind_robots.
- **alexa-integration** — reviewed in more depth (real `stores/serendipityVoiceStore.ts`,
  `components/pages/serendipity-page.vue` references) — see Gaps below; not skipped.
- **mermaids-of-venice** — content project; its one surface reference
  (`components/pages/mermaids-page.vue`) is a completed, human-owned personal-note
  placeholder with no open verification needed.
- **coat-dance** — content project with zero kind_robots surface references in its
  roadmap.
- **mural-design** — content/fence-painting project; its one kind_robots reference
  (`/mural` page, `t-007`, done) was already verified as shipped.

All other 20 projects were audited in full against `/home/user/kind_robots/`:
kind-robots, interface-vision, model-builder, digital-storefront, ai-art-academy,
coloring-book, brainstorm, storybook, davinci, media-watchlist, taskmaster, appmaker,
ruler-hooked, lora-ingestion, kind-economy, cthulhuquarium, mandarin-tutor,
rainbow-butterflies, alexa-integration, text-generation, scene-animator.

## Method

For each of the 20 audited projects: extracted every `server/api/`, `components/`,
`stores/`, and `pages/` path mentioned in the roadmap, plus every bare `*Store.ts`
filename and every `.vue`/`.ts` basename, and checked each against the actual
`/home/user/kind_robots/` tree (Glob/find + Grep only, no live requests). Basename-only
matches were manually spot-checked against context, since many were regex artifacts from
route-suffix filenames (e.g. `[id].get.ts` fragmenting into a bare `get.ts`) rather than
real gaps.

## Gaps

Only one file-level gap survived spot-checking as genuinely new and undocumented anywhere
in an active roadmap. Everything else the cross-check flagged as "missing" turned out to
already have its own prior-audit correction task on file (see Notable non-findings below)
— a good sign for roadmap health, not a gap in this audit's coverage.

- `[kind-robots] surface "server/api/components/index.post.ts" and "server/api/components/[id].patch.ts"` — mentioned as live routes in kind-robots/t-033's last recheck (2026-07-25); not found in code as of this audit, and the `Component` Prisma model itself no longer appears anywhere in `prisma/schema.prisma` (84 models checked, none named `Component`). No roadmap task records when or why it was removed.

## Orphans noticed

None beyond what active roadmaps already track. While cross-checking, the following
top-level `kind_robots` surfaces that could have looked orphaned were confirmed covered
by an active project's roadmap: `server/api/monsters/*` and `components/cthulhuquarium/`
(cthulhuquarium), `server/api/contenders/*` (challenge-center/digital-storefront),
`server/api/botcafe/*` and `server/api/forum/*` (kind-robots/interface-vision/
rainbow-butterflies/kind-economy/alexa-integration/brainstorm). Two very small top-level
API routes, `server/api/suggest.post.ts` and `server/api/version.get.ts`, are not named
in any active roadmap, but both read as minor, self-explanatory infra endpoints not
worth a dedicated task.

## Notable non-findings (already self-corrected by prior audits)

Worth recording because they consumed most of this audit's cross-check budget: the
following file-level mismatches were found by the raw path/basename diff, but every one
already has its own already-closed roadmap task recording and correcting it, so none are
new findings:

- `components/butterfly/store-butterfly.vue` → moved to `components/abandonware/butterfly/store-butterfly.vue` (kind-robots, recorded and closed).
- `pages/video-generator.vue` → actually `pages/play/video-generator.vue`, plus its nav-reachability gap (kind-robots/t-046, t-014, done).
- `server/api/conductor/curate-request.post.ts` → deliberately removed in kind_robots PR #1244 (kind-robots/t-051, done — the direct precedent for this audit's one new proposed task).
- `server/api/stripe/charge.ts` → already documented dead code, removed.
- `components/giftshop/social-publisher.vue` → removed 2026-07-18 (digital-storefront/t-027, done).
- `server/api/store/checkout.post.ts` → corrected path is `server/api/stripe/checkout.post.ts` (digital-storefront, done).
- `components/abandonware/builder/builder-manager.vue` and `components/art/art-maker.vue` → confirmed retired/out-of-scope (ai-art-academy/t-057, t-059).
- `pages/lora.vue`, `components/lora/lora-card.vue`, `components/lora/lora-gallery.vue` → rebuilt as `content/resources.md` + `components/resources/*` (lora-ingestion/t-007, done).
- `components/ruler-hooked/ruler-hooked-page.vue`, `components/navigation/swipe-deck.vue`, `components/butterfly/single-slider.vue`, `stores/compositionStore.ts` → all found and corrected by a prior weekly audit (ruler-hooked, done).
- `stores/displayStore.ts`, `stores/linkStore.ts`, `components/pages/plan-projects-grid.vue`, `components/wonderlab/lab-gallery.vue`, `components/wonderlab/lab-manager.vue`, `components/wonderlab/component-review-feed.vue`, `pages/admin/wonderlab-review-rollout.vue`, `components/navigation/narrator-chat.vue`, `components/icons/kind-icons.vue`, `components/content/characters/character-interact.vue`, `components/storybook/storybook-mockups.vue`, `components/pages/conductor-art-gallery.vue`, `components/art/art-reactions.vue`, `components/abandonware/themes/theme-manager.vue`, `components/abandonware/pages/registration-form.vue` → all deliberately deleted/renamed/relocated and recorded across interface-vision's own extensive done-task history (t-012, t-018, t-024, t-026, t-045, t-047, t-049, t-051, t-089, t-092, t-101), with the one still-open reference (`t-104`, status `review`) itself already correctly noting `lab-gallery.vue` as "previously confirmed unreferenced."
- `components/pages/serendipity-voice-page.vue` → renamed to `components/pages/serendipity-page.vue` (alexa-integration/t-019, already corrected).

## Proposed follow-up tasks (1 of up to 3)

Given the breadth above turned up only one genuinely new, unaddressed gap, this audit
proposes one new task rather than padding to three with lower-value duplicates of
already-self-corrected findings:

1. **kind-robots/t-091** — "Investigate and document the disappearance of the Component
   model and its server/api/components/* routes" — `status: ready`, `stakes: reversible`,
   `owner: null`. Landed in `projects/kind-robots/roadmap.yaml`. Mirrors the successful
   `t-051` (curate-request.post.ts) investigation pattern.

## Summary

29 active projects were in scope; 9 were judged not to be kind_robots-surface projects
(brief note only) and 20 were fully cross-checked against `/home/user/kind_robots/`.
The roadmap ecosystem is unusually well self-auditing — nearly every raw path/basename
mismatch this audit's method surfaced was already found and corrected by an earlier
weekly audit or in-session investigation, several of which explicitly cite this same
`SITE-AUDIT-AGENT.md` process. One new, previously-undocumented gap was found and filed:
the `Component` Prisma model and its `server/api/components/*` routes, live as of
2026-07-25's last recheck, are entirely absent from the current kind_robots checkout with
no roadmap record of the removal. No orphans of note beyond items already tracked.
