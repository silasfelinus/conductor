# Weekly Site Audit — 2026-07-26

Per `projects/global-ui/SITE-AUDIT-AGENT.md`. First run under the self-assigning
`role: site-auditor` path (`scripts/select_role.py`, folded in via global-ui/t-016) —
no prior `AUDIT-REPORT-*.md` existed, so this is the baseline pass.

**Method:** cross-referenced all 31 `active` (per `project-overrides.yaml`)
conductor project roadmaps against `/home/user/kind_robots/` (API routes, Pinia
stores, Vue components, `prisma/schema.prisma`, page routes) using Glob/Grep only
— no live HTTP requests were made. Work was split across three parallel research
passes (~10 projects each); this report synthesizes their findings.

## Summary

31 active projects checked. The overwhelming majority of roadmap-claimed surfaces
exist in code exactly as described — the roadmaps are in good shape. Two real
instances of **documentation drift** were found (roadmap says a surface is
shipped/live; the surface was later intentionally removed), and both were minor,
non-functional (no broken links, no user-facing breakage). No missing-but-claimed
surfaces were found that indicate an actual regression or broken feature.

## Findings

### Drift (roadmap describes something that no longer exists)

1. **dream-cycle/t-013** — describes `/daily-dream`
   (`components/pages/daily-dream-page.vue`, `content/daily-dream.md`,
   `content/channels/play/daily-dream.md`, kind_robots PR #229) as shipped
   2026-07-14. It was intentionally removed by kind_robots PR #644 on
   2026-07-20 ("was never finished... no longer wanted"), and
   `scripts/build_digest.py` was already updated in the same window to stop
   linking to it. No live bug — just a stale "done" note. Filed
   **dream-cycle/t-020** (ready, reversible) to correct it.

2. **digital-storefront/t-008 + STORE-AUDIT.md** — describes
   `components/giftshop/social-publisher.vue` as the most-mature, best-wired
   giftshop component (2026-07-15). It was removed by kind_robots migration
   `20260718200000_remove_social_publishing` ("abandoned SocialPost/SocialTarget
   prototype") three days later, 2026-07-18. Filed **digital-storefront/t-027**
   (ready, reversible) to correct it.

### Expected / already-tracked gaps (not new findings, noted for completeness)

- **kind-robots/t-044** — `server/utils/contentAccess.ts` and the `Grant` Prisma
  model don't exist yet. Task is `status: ready`, not `done` — this is pending
  work, not a regression.
- **digital-storefront/t-017, t-020, t-021** — `Pack`/`Grant` models,
  `Resource.commercialSafe`, `ArtImage.storefrontFeatured` are all design-only,
  already filed onward as kind-robots/t-037, t-045, t-047. Forward-looking, not bugs.
- **wishmaster/t-002** — the `Composition` Prisma model gap is already
  self-documented in the task's own note. No new information.
- **davinci/t-015** — narration endpoint is explicitly spec-only per the task;
  code correctly doesn't have it yet.

### Low-confidence / likely noise

- **kind-robots/t-020** — an early note names `artjob-manager.vue`; a later
  "UPDATE" note on the same task correctly refers to `artjob-feedback-manager.vue`
  (the file that actually exists). Reads as an inexact early reference, not a
  real gap — no task filed.

### Orphans (code exists, not named in any roadmap task — informational only)

- `server/api/dream-relations/index.post.ts`/`.get.ts` — dream-cycle/t-003 once
  flagged "no DreamRelation endpoint" as a gap (filed as kind-robots/t-017); it's
  since been built. Roadmap text is stale but harmless (describes history, not
  current state).
- `server/api/comfy/kontext/kombine.post.ts` — adjacent to superkate-hairstyle-ai's
  tracked Kontext routes but not itself named in any task.
- kind-robots has more `artjob-*.vue` variants (`artjob-editor.vue`,
  `artjob-queue-browser.vue`, `artjob-failed-page-requeue.vue`) than are named in
  roadmap tasks — the admin surface has grown organically past what's tracked.

None of the orphans indicate missing functionality — they're already-built,
working code that simply isn't individually named in a roadmap task. No action
proposed.

## Projects with no checkable concrete surfaces

`brainstorm` (pitch-generation only, no API/component/store names to verify),
`superkate-services-calculator` (standalone Flutter app, separate codebase),
`sketchy`'s app-side models (Flutter app with its own DB, correctly out of
kind_robots scope), `ecosystem-map` (only generic naming patterns, which do
check out against the codebase).

## Follow-up tasks filed (2 of the allowed 3)

- `dream-cycle/t-020` — correct t-013's stale "shipped" note (Daily Dream page
  removed 2026-07-20).
- `digital-storefront/t-027` — correct STORE-AUDIT.md / t-008's stale
  description of `social-publisher.vue` (removed 2026-07-18).

A third task wasn't filed — no other finding rose to the level of a genuine,
actionable gap; the "low-confidence/noise" and "orphan" items above are noted
for the record rather than turned into tasks, per the audit's own scope (real,
impactful gaps only).

## Boundaries observed

No live HTTP requests to kind-robots.vercel.app. No `npm`/`pnpm` builds run. No
changes to `main` directly (this report + the two roadmap edits go out via PR).
No `gate_human: true` task was modified.
