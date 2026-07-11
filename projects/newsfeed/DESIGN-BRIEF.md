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

## Likely Kind Robots areas to audit

The first Worker should identify the exact current paths rather than guessing, but the audit should cover:

- the current user homepage/page component
- the settings component and route ownership
- navigation registration
- user/display/page stores and persistence helpers
- existing server utilities for outbound fetches and caching
- existing card/list components that fit the feed visual language

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
