# Animation Manager Specification

## Purpose

Animation Manager turns desktop wallpaper effects into an evolving creative product instead of an untracked component folder. It owns the loop from research and pitch through prototype, release, reactions, polish, and retirement.

The Kind Robots animation catalog remains the runtime source of truth. Conductor owns creative planning and task state. The existing Kind Robots `Component` and `Reaction` models own build history and user quality signals.

## Non-negotiable experience contract

Every animation must:

1. Be enjoyable without any pointer, keyboard, touch, or game action.
2. Keep optional interaction additive and non-blocking unless the effect is explicitly labeled interactive and excluded from startup wallpapers.
3. Work as a transparent layer over arbitrary themes and page layouts.
4. Behave correctly as both a full-screen startup wallpaper and a clipped Screen FX surface when marked eligible for both.
5. Respect `prefers-reduced-motion` with fewer elements, slower movement, lower contrast, or a quiet static state.
6. Use frame timestamps rather than assuming 60 frames per second.
7. Size itself from its rendered surface, not only `window.innerWidth` and `window.innerHeight`.
8. cancel animation frames, observers, timers, media listeners, and input listeners on unmount.
9. Avoid network requests, audio, paid services, or remote assets for the passive loop unless a later pitch explicitly approves them.
10. Preserve underlying page interaction unless `blocksInput: true` is an intentional, visible part of a Screen FX-only effect.

## Single registration contract

An animation ships with:

- `components/screenfx/<animation-id>.vue`
- one entry in `stores/animationCatalog.ts`

The catalog entry defines the stable id, label, reveal text, icon, tooltip, display color, startup eligibility, input behavior, and preferred surface. Nuxt lazy-component names are derived from the kebab-case id, so startup wallpaper and Screen FX must never maintain separate component maps.

A `generationSafe: true` animation with no blocking input is automatically eligible for:

- Screen FX selection
- explicit startup animation preferences
- the random startup animation pool
- generation/loading animation selection

## Creative pipeline

### 1. Research

Collect techniques, visual references, accessibility constraints, and novelty comparisons. Research should prefer primary browser documentation for implementation claims and should not clone a copyrighted screensaver asset-for-asset.

### 2. Pitch

Append a structured entry to `PITCHES.yaml` with:

- stable slug and title
- visual surprise
- passive loop
- optional interaction
- implementation technique
- reduced-motion behavior
- performance risk
- novelty comparison against the current catalog
- acceptance criteria
- status and build lineage

### 3. Prototype

Build the smallest complete loop. A prototype may be marked under construction but must still clean up after itself and remain safe to mount repeatedly.

### 4. Candidate

A candidate passes TypeScript, contract tests, the animation verification script, and the browser smoke matrix. It receives a `Component` attempt record before being promoted.

### 5. Shipped

A shipped effect is in the catalog and reachable through its intended surfaces. Shipping does not erase earlier attempts.

### 6. Polish or retire

Reaction comments and ratings drive the next change. A polish pass becomes a new attempt with explicit lineage. Weak or broken builds are preserved as museum records and marked broken or superseded rather than silently deleted.

## Attempt records

Use the existing `Component` model without schema changes.

Recommended fields:

- `folderName`: `screenfx`
- `componentName`: `<animation-slug>@v<build-number>`
- `title`: human title plus build number
- `isWorking`: true only after required verification
- `underConstruction`: true for prototypes or candidates
- `isBroken`: true for failed or retired attempts that should not be promoted
- `notes`: structured YAML or JSON text containing slug, build, catalog id, component path, commit, PR, technique, passive behavior, interaction behavior, reduced-motion behavior, verification, `supersedes`, and `supersededBy`

Reactions use `reactionCategory: COMPONENT` and the Component row id. The initial quality view should show rating average, rating count, reaction-type counts, and recent comments. Promotion decisions should show evidence but remain reversible and human-visible.

## Quality score

Do not hide raw signals behind one magic number. Display raw counts first. A sortable quality score may combine:

- average 1–5 rating
- number of unique raters
- positive reaction count
- negative reaction count
- unresolved comments mentioning performance, nausea, legibility, input interference, or breakage
- verification state

The score ranks attention; it does not auto-delete or auto-publish.

## Daily agent cadence

Animation Manager is autonomous but rate-limited:

- at most one new research pitch per Pacific calendar day
- at most one implementation or polish build per Pacific calendar day
- no new pitch when the buildable queue already exceeds twelve
- no cosmetic duplicate when an existing animation can be improved instead
- one claimed task at a time under normal Conductor rules

The daily build loop chooses either the highest-priority accepted pitch or a specific reaction-backed polish opportunity. Every build creates a new attempt record and updates its pitch lineage.

## Definition of done for an animation build

- passive loop is visually coherent for at least five minutes
- optional interaction is discoverable but unnecessary
- underlying page clicks still work unless deliberately blocked and labeled
- startup wallpaper and intended Screen FX regions render correctly
- no stale component map or preference registration is required
- high-DPI rendering is capped to a documented budget
- reduced-motion mode is meaningfully quieter
- mount/unmount leaves no active RAF, observer, listener, timer, or retained canvas state
- TypeScript and contract tests pass
- browser smoke results are recorded
- Component attempt record and pitch lineage are updated
