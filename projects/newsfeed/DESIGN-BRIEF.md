# Newsfeed — Design Brief

## Goal

Turn the Kind Robots user homepage into a useful, calm, modular newsfeed while moving the existing settings surface into its own dedicated section.

The first version should become functional quickly. It should provide good recommended feeds without demanding setup, then expose progressively deeper customization for users who want to program what they see.

## Product principles

1. **Useful by default** — a new or returning user immediately sees a thoughtful mix of relevant stories.
2. **Modular by construction** — source adapters, normalized items, feed definitions, user preferences, filtering, and presentation remain separable.
3. **Programmable without becoming dangerous** — users configure declarative filters and ordering; v1 does not execute arbitrary user code.
4. **Transparent rather than algorithmically mysterious** — every item shows its source and category, and users can see why a feed is present.
5. **User-controlled perspective balance** — political viewpoint metadata is visible, optional, and adjustable rather than silently baked into ranking.
6. **Fast before fancy** — build the smallest reliable aggregation loop first and avoid database work unless existing architecture proves it necessary.
7. **Failure-tolerant** — one stale or broken source must not blank the entire homepage.

## Recommended starter feeds

- AI news
- Activism
- Malaria activism and global-health progress
- AI gaming advancements
- AI model creation, releases, and research
- Developer tips and practical engineering guidance

These are presets, not permanent silos. A feed may aggregate multiple sources, and sources may participate in multiple feeds through tags.

## Adjustable political perspective

Kind Robots should take inspiration from Ground News by letting users control how much political viewpoint diversity enters their feed.

The ranking system should support simple modes such as Focused, Balanced, Broad spectrum, and Custom. Political perspective must remain an optional ranking dimension rather than infecting every feed or becoming a hidden personality profile.

Where reliable metadata exists, items may expose source-perspective labels, methodology/provenance, and a way to request contrasting coverage. Factual reliability and political perspective must remain separate dimensions. Unrated and primary sources remain valid.

Detailed contracts, guardrails, and the staged MVP path live in `BIAS-CONTROLS.md`.

## Proposed modular contract

### Feed source

A source adapter knows how to retrieve one external stream and return raw entries. RSS/Atom should be preferred for the MVP where available because it is simple, attributable, and portable.

### Normalized item

Every adapter maps into a shared item shape:

- stable ID
- title
- summary
- source name
- canonical URL
- published timestamp
- category tags
- optional image URL
- optional author
- optional political-perspective metadata
- optional metadata provenance and confidence

### Feed definition

A feed definition contains:

- slug and display name
- description
- icon
- default enabled state
- source references
- include/exclude tags or keywords
- default sort mode
- optional ranking dimensions and weights

### User preference

The user-facing store owns:

- enabled feed slugs
- feed order
- include keywords
- exclude keywords
- source toggles
- sort mode
- political perspective mode and weights
- perspective-label visibility
- contrast preference

For the MVP, use existing Pinia/local-storage persistence patterns. Do not create a database migration merely to remember feed toggles.

### Presentation

The homepage consumes normalized items from the store and renders reusable feed cards. It should not know how RSS parsing, caching, political-perspective metadata, or individual source quirks work.

## MVP surface

The first genuinely useful release includes:

- settings moved away from the homepage without losing functionality
- a recommended mixed feed on the homepage
- category filtering
- source attribution and outbound links
- loading, empty, stale, and partial-error states
- user enable/disable and ordering of feed presets
- preference persistence through existing client patterns
- architecture that supports perspective balancing without a rewrite

Keyword programming, source-level controls, richer ranking, custom political weights, contrasting-coverage grouping, and visual polish follow after the core loop works.

## Technical bias

- Use TypeScript contracts shared between the store and rendering components.
- Keep all network interaction in the Pinia store or a small server-side aggregation layer; components do not call API routes directly.
- Prefer a registry-driven architecture over conditionals spread across components.
- Treat political perspective as pluggable metadata consumed by ranking, not source-adapter or component logic.
- Use bounded caching and deduplication.
- Sanitize and truncate remote summaries; never render untrusted feed HTML directly.
- Avoid schema changes for v1.
- Treat any unavoidable shared-backend or database change as a separate proposal under Conductor boundaries.

## Audit findings — exact integration points (2026-07-14)

The homepage is **not** a `pages/index.vue` component. All routes render through
`pages/[...slug].vue`, a catch-all that resolves `route.path` against Nuxt Content
(`queryCollection('content').path(path).first()`) and renders
`<ContentRenderer :value="activePage" />`. The routed homepage document is
`content/index.md`, whose body currently embeds `:user-manager`
(`components/user/user-manager.vue`), a tabbed shell whose default `dashboard` tab
renders `components/user/user-dashboard.vue` — which directly embeds
`user-panel.vue` (profile/settings form), avatar upload, theme picker, cache-clear,
and gallery panels. **Settings genuinely live on the homepage today**, confirming
the brief's premise.

- **Homepage swap (t-003/t-006):** change `content/index.md`'s body from
  `:user-manager` to a new `:newsfeed-page` (or lighter `:home-feed`) component.
  Relocate `user-manager`'s dashboard tab so it's reachable only at the existing
  `/dashboard` route (already registered under `dashboardConfigs.user`), not the
  root — this "moves" settings without deleting any existing functionality.

- **Settings store (t-003):** there is no dedicated settings store or `/settings`
  route today. Settings are flat columns on the Prisma `User` model
  (`prisma/schema.prisma:1440`, e.g. `showMature`, `customIcons`,
  `preferredArtServerId`, `hiddenServerIds`, `vibes`, `blockList`, `smartBar`) read
  and written through `stores/userStore.ts` via `server/api/users`. Do not invent a
  generic key/value settings table — follow this same convention for any settings
  that must move, and keep new feed preferences (below) on their own store rather
  than folding them into `userStore`.

- **Feed preferences persistence (t-004/t-007):** the repo has no Pinia-persistence
  plugin. The standing convention (≥18 stores, e.g. `stores/navStore.ts:108`,
  `stores/socialStore.ts`) is a hand-rolled SSR-safe pair —
  `safeGetLocalStorage(key)` / `safeSetLocalStorage(key, value)` — for client-only
  UI state. Use that for feed enable/order/keyword-filter preferences in v1 rather
  than a database migration. Only reach for Prisma `User` columns + a new
  `server/api/users` sub-route if preferences genuinely need to survive across
  devices, and treat that as a separate, smaller proposal.

- **Dashboard-tab registry — already reserved (t-012):** `stores/helpers/dashboardHelper.ts:1264-1277`
  already has a `wonder.newsfeed` tab entry (`route: '/newsfeed'`, image
  `public/images/dashboard-tabs/wonder/newsfeed.webp`). The image file does not
  exist on disk yet — t-012 needs to generate it, not create a new registry entry.
  `stores/helpers/tutorialCards.ts`'s `tutorialChannels` has no top-level `wonder`
  key yet (only games/scenario/dream/character/reward/bot/art/sanctuary/builder/
  home/mural/conductor) — t-012 must add a new `wonder` entry with a `newsfeed`
  section, mirroring the shape of an existing `TutorialChannel`.

- **Content stubs already exist:** `content/newsfeed.md` (routed `/newsfeed` page:
  `channelKey: lab`, `dashboardKey: wonder`, `dashboardTab: newsfeed`, body
  `:newsfeed-page`) and `content/channels/lab/newsfeed.md` (lab-channel tab
  metadata). Build into these rather than creating parallel routes/content docs.

- **Conductor pitch page is separate from the real feature:**
  `components/conductor/newsfeed-page.vue` wraps
  `components/conductor/project-front-page.vue` with a static
  `ProjectFrontConfig` (`slug: 'newsfeed'`, `channelKey: 'wonder'`,
  `tabKey: 'newsfeed'`) and optionally overlays a live `Project` DB row via
  `useProjectStore().projectForSlug(slug)`. This is a status/roadmap pitch page —
  its own `deliverables.next` list says `['Feed builder + item renderers',
  'Homepage placement']`. Keep it as the pitch page (update `deliverables.done` as
  milestones land) and build the real interactive feed as a distinct component
  slotted into `project-front-page.vue`'s `#interactive` slot, or swap
  `content/newsfeed.md`'s body to render the real feed component directly once
  it's no longer just a pitch. Register any `Project` DB row through the existing
  `channelKey`/`tabKey`/`liveUrl` columns (`prisma/schema.prisma:507-509`) rather
  than inventing a new config surface.

- **Server-side aggregation (t-005):** no caching layer exists anywhere in
  `server/` today (zero use of `defineCachedEventHandler`/`defineCachedFunction`).
  Model a new `server/api/newsfeed/index.get.ts` on the shape of
  `server/api/conductor/prs.get.ts` (thin `defineEventHandler` + a shared fetch
  helper in a new `server/utils/newsfeed.ts`, following
  `server/utils/conductor-github.ts`'s pattern of a small typed fetch wrapper).
  Introduce `defineCachedEventHandler` for TTL caching of aggregated results —
  this repo has no precedent for it yet, so document the TTL choice in the PR.

- **Feed card visual language (t-006):** fork `components/dreams/dream-card.vue`
  (image-first card, title, badge row, gradient-overlay footer, hover elevation,
  `showImage`/`compact`/`showMeta` props, and a multi-source image-fallback
  chain) for a new `FeedCard.vue` — it already has the closest title/badge/
  image/timestamp visual grammar a feed item needs, plus the fallback-image
  handling that inconsistent RSS thumbnails will require. `chat-card.vue`
  (timestamp/author pattern) and `image-card.vue` are secondary references.

## Non-goals for v1

- social posting or comments
- opaque personalized ranking
- inferring a user's politics from unrelated activity
- treating political ratings as objective facts without methodology
- arbitrary JavaScript expressions supplied by users
- scraping sites that prohibit it
- a new database schema
- notifications, email digests, or publishing workflows
- perfect article extraction or full-text mirroring

## Definition of done

A signed-in user lands on a homepage containing a reliable recommended newsfeed, can understand and change which feeds appear, can reorder them, and can still reach all settings in a dedicated location. The implementation is registry-driven, political perspective is an optional transparent ranking dimension, and adding another recommended feed or ranking control does not require rewriting the homepage component.
