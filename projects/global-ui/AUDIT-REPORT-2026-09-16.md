# Weekly Site Audit — 2026-09-16

Read-and-report run per `projects/global-ui/SITE-AUDIT-AGENT.md`. No live HTTP requests, git
mutations against `kind_robots`, or npm/pnpm builds were run; all cross-checks used
Glob/Grep/direct file reads against a local read-only checkout of `/home/user/kind_robots/`. The
only writes are this report and one new roadmap task.

## Scope

Active projects per `project-overrides.yaml` (`status: active`, cross-checked fresh this
session): **19** — appmaker, coat-dance, coloring-book, conductor, conductor-app,
cthulhuquarium, digital-storefront, humboldt-scoop-cms, kind-economy, kind-robots,
kindrobots-unraid, lora-ingestion, media-watchlist, model-builder, rainbow-butterflies,
ruler-hooked, scene-animator, storybook, text-generation.

This is a much smaller active set than the 2026-09-09 audit's 29 — in the week between, several
previously-active projects flipped to `finished`/`continuous`/`retired`/`paused`
(ai-art-academy, alexa-integration, brainstorm, davinci, mandarin-tutor, mermaids-of-venice,
mural-design, taskmaster all left the active set; per-project rationale is recorded in
`project-overrides.yaml`, not repeated here). All 19 have a `projects/<slug>/roadmap.yaml`.

## Method

For each of the 19 active roadmaps, statically extracted every `server/api/**/*.ts`,
`server/utils/**/*.ts`, `components/**/*.vue`, `stores/**/*.ts`, `pages/**/*.vue`, and
`utils/**/*.ts` path mentioned anywhere in the roadmap text (161 raw path mentions, de-duplicated
per project) and checked each against the current `/home/user/kind_robots/` checkout. Every
"missing" hit was then read in its roadmap context (not just path-existence) before being
counted as a real gap, since several projects run heavy kaizen/audit-log conventions where old
paths get mentioned in historical notes on already-`done` tasks. Also ran a directory-level
orphan pass: every top-level `components/*` and `server/api/*` directory checked against the
full text of *all* roadmaps (active and inactive), to catch backend/UI surfaces with zero
roadmap coverage anywhere.

## Gaps

**None new.** Every apparent "missing" hit from the static scan resolved to one of:

- **Already tracked and closed correctly, and verified still accurate**: `kind-robots/t-095`
  (the `components/abandonware/` disappearance, filed by the 2026-09-09 audit) is `status: done`.
  Verified independently this session that the resolution is real, not just a status flip: (a)
  `components/abandonware/` genuinely still doesn't exist in the checkout, (b)
  `utils/scripts/verifyComponentReachability.ts` now carries a header note dated 2026-08-11
  ("Silas deleted `components/abandonware/` outright... RETIRED") explaining exactly what
  happened, and (c) `nuxt.config.ts`/`tsconfig.json` no longer reference `abandonware` at all —
  the "dangling ignore rules" t-095 was filed to chase are gone. `kind-robots/t-051`
  (`curate-request.post.ts`) is the same pattern, already `done`.
- **Resolved by a task that landed after the last audit**: `kind-robots/t-103`
  (`character-flip-card.vue` orphaned-duplicate-component finding) is `status: done`; the file no
  longer exists and `<CharacterFlipCard>` has zero live call sites (one stale CSS comment only) —
  consistent with the fix having deleted it rather than kept it.
- **Expected fallout of a documented, deliberate cross-project merge**: `storybook`'s roadmap
  mentions `taskmaster-page.vue`/`taskmasterStore.ts` only inside a `done` task's historical
  description of the old architecture being replaced; `appmaker`'s roadmap mentions
  `components/taskmaster/taskmaster-sample-tasks.vue` only in an audit note dated 2026-08-18. Both
  predate the taskmaster project's 2026-09-14 retirement into storybook
  (`project-overrides.yaml`: route retired via kind_robots#2718, files deleted deliberately). Not
  a new gap — the files are supposed to be gone.
- **Already-known, already-closed non-finding from a prior audit**: `digital-storefront/t-036`
  (`status: done`) already corrected `server/api/store/checkout.post.ts` → the real path,
  `server/api/stripe/checkout.post.ts`, back on 2026-08-02.
- **Regex false positive**: `kind-robots`'s `utils/scripts/verifyXyz.ts` is a generic placeholder
  name used in a task note ("matching the existing `verifyXyz.ts` pattern") to describe a whole
  class of narrow textual-checker scripts, not a literal path.
- One informal, in-passing mention (`components/conductor/davinci-page.vue`, inside a
  multi-thousand-word `model-builder` kaizen log citing it as a "reference implementation")
  wasn't counted as a genuine roadmap surface claim — it's conversational log text, not an
  authoritative "this surface exists at this path" statement, and davinci's actual merge into
  storybook is already fully documented in `project-overrides.yaml`.

The ecosystem's self-auditing loop (each audit's findings landing as `done` tasks with real
fixes, verified by the next audit rather than just trusted) continues to hold up under a second
independent check this week.

## Orphans noticed

Directory-level pass (46 `components/*` dirs, 66 `server/api/*` dirs) found every `components/*`
top-level directory referenced somewhere in the roadmap corpus. Four `server/api/*` directories
were not: `botcafe`, `newsletter`, `agent-credentials`, `agent-profiles`. `botcafe` and
`newsletter` read as belonging to already-`finished` projects (brainstorm, newsfeed) and are out
of the active-project scope this audit covers. `agent-profiles` is covered under different
vocabulary — `rainbow-butterflies/roadmap.yaml` already discusses the `AgentProfile` model and
its MCP check-in bridge (t-051).

**`agent-credentials` is a genuine orphan**: `server/api/agent-credentials/index.get.ts`,
`index.post.ts`, and `[id].delete.ts` (list/issue/revoke an agent's API credential, guarded by
`requireHumanOrRainbowApiUser`) implement the `AgentProfileCredential` Prisma model
(`prisma/agent-profile.prisma`) but are named nowhere in `rainbow-butterflies/roadmap.yaml`,
despite the sibling `AgentProfile`/`AgentCheckIn` surfaces being explicitly tracked. Read all
three handlers — the surface itself looks complete and correctly guarded, this is a documentation
gap, not a code defect.

## Proposed follow-up tasks (1 of up to 3)

1. **rainbow-butterflies/t-053** — "Add roadmap tracking for the `server/api/agent-credentials/`
   surface (list/issue/revoke agent API credentials)" — `status: ready`, `stakes: reversible`,
   `owner: null`. Landed in `projects/rainbow-butterflies/roadmap.yaml`, milestone m2 (COMMONS),
   alongside the related AgentProfile/t-051 work.

Only one task was filed — the directory-level orphan pass turned up one genuine, previously
untracked surface, and every path-level "gap" from the static scan investigated to an
already-resolved or already-expected state rather than a new problem. Filing speculative tasks
against non-findings would work against the "small, reversible, impactful" bar this role is held
to.

## Summary

19 active projects in scope (down from 29 last week, entirely from projects graduating out of
`active` status, not audit scope-narrowing). All 19 were fully cross-checked against
`/home/user/kind_robots/`. Zero new path-level gaps — every apparent miss traced to an
already-closed audit finding, a deliberate and already-documented retirement/merge, or a regex
false positive. One new orphan found and filed: `rainbow-butterflies/t-053` for the untracked
`agent-credentials` API surface.
