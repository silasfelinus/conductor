# Newsfeed — Design Brief

## Goal

Turn the Kind Robots user homepage into a useful, calm, modular newsfeed while moving the existing settings surface into its own dedicated section.

The first version should become functional quickly. It should provide good recommended feeds without demanding setup, then expose progressively deeper customization for users who want to program what they see.

## Product principles

1. **Useful by default** — a new or returning user immediately sees a thoughtful mix of relevant stories.
2. **Modular by construction** — source adapters, normalized items, feed definitions, user preferences, filtering, and presentation remain separable.
3. **Programmable without becoming dangerous** — users configure declarative filters and ordering; v1 does not execute arbitrary user code.
4. **Transparent rather than algorithmically mysterious** — every item shows its source and category, and users can see why a feed is present.
5. **Fast before fancy** — build the smallest reliable aggregation loop first and avoid database work unless existing architecture proves it necessary.
6. **Failure-tolerant** — one stale or broken source must not blank the entire homepage.

## Recommended starter feeds

- AI news
- Activism
- Malaria activism and global-health progress
- AI gaming advancements
- AI model creation, releases, and research
- Developer tips and practical engineering guidance

These are presets, not permanent silos. A feed may aggregate multiple sources, and sources may participate in multiple feeds through tags.

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

### Feed definition

A feed definition contains:

- slug and display name
- description
- icon
- default enabled state
- source references
- include/exclude tags or keywords
- default sort mode

### User preference

The user-facing store owns:

- enabled feed slugs
- feed order
- include keywords
- exclude keywords
- source toggles
- sort mode

For the MVP, use existing Pinia/local-storage persistence patterns. Do not create a database migration merely to remember feed toggles.

### Presentation

The homepage consumes normalized items from the store and renders reusable feed cards. It should not know how RSS parsing, caching, or individual source quirks work.

## MVP surface

The first genuinely useful release includes:

- settings moved away from the homepage without losing functionality
- a recommended mixed feed on the homepage
- category filtering
- source attribution and outbound links
- loading, empty, stale, and partial-error states
- user enable/disable and ordering of feed presets
- preference persistence through existing client patterns

Keyword programming, source-level controls, richer ranking, and visual polish follow after the core loop works.

## Technical bias

- Use TypeScript contracts shared between the store and rendering components.
- Keep all network interaction in the Pinia store or a small server-side aggregation layer; components do not call API routes directly.
- Prefer a registry-driven architecture over conditionals spread across components.
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
- arbitrary JavaScript expressions supplied by users
- scraping sites that prohibit it
- a new database schema
- notifications, email digests, or publishing workflows
- perfect article extraction or full-text mirroring

## Definition of done

A signed-in user lands on a homepage containing a reliable recommended newsfeed, can understand and change which feeds appear, can reorder them, and can still reach all settings in a dedicated location. The implementation is registry-driven and adding another recommended feed does not require rewriting the homepage component.
