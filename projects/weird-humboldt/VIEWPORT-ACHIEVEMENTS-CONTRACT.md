# Ecotone: achievements, completed endings and viewport-first presentation

**Direction from Silas · 2026-10-19 PT.** These are mandatory **roadmap/acceptance requirements**, not an implemented Kind Robots application or clearance to publish. Working title Ecotone; canonical Conductor slug `weird-humboldt` remains unchanged.

## The nonnegotiable rule: one visual surface per view, every device

> **Mobile, tablet and desktop each show one viewport-fitted, non-page-scrolling game surface.** Secondary information may be reached through tabs, a modal, or tightly scoped internal scroll panes. There must be **no document/body/root-page vertical or horizontal scrolling**, no clipped controls and no card off the visible surface.

Reconcile design with the currently implemented patterns rather than re-inventing layout:
- **Shifting Lands:** `silasfelinus/kind_robots/components/shifting-lands-journey-board.vue` uses a compact tabbed `journey-shell` with `min-h-0`, `overflow: hidden` and contained `kr-pane-scroll` reading sections. Compare the *modern journey board*, not the separate legacy mode with full-page `kr-scroll`.
- **Shifting Desks:** `pages/play/shifting-desks.vue` and `components/shifting-desks/shifting-desks-endings-gallery.vue` put a compact toolbar/board on one surface. The existing gallery is a `max-h-[90dvh]` accessible dialog whose grid `overflow-y-auto` belongs to the dialog content, not to the whole page.
- **Current browser verification:** `cypress/public/shifting-desks-endings.cy.ts` loads naturally reached end states at 390×844, 768×1024 and 1440×900; `utils/scripts/auditResponsiveLayout.mjs` checks actual rendered geometry for horizontal spill and clipped galleries. Use these as **patterns**; Ecotone still needs its own mounted-page end-to-end tests.

### Ecotone's proposed surface

**Main board (always one surface):**
1. **One compact top bar:** current region / chapter, the five skill stats via one small character control, Clarity/status, Menu/Help, and a persistent **Endings 0/10** progress button. Avoid a second header with a full redundant game title. Site navigation can remain separate but consumes known usable viewport height.
2. **Primary card:** illustrated location/encounter face, concise narrative and optional small character/cast badge. Card art scales with the container; do not let an intrinsic image force page height.
3. **Decision area:** 2–4 large enough choice controls with visible stat/check target and consequences; outcome overlay sits within the same bounded stage and has a Continue action that remains visible.
4. **Secondary tabs/overlays:** Journey, Character, Journal, Map, Achievements, **Endings** and optional Settings/Tutorial. Do not print every tab's contents stacked vertically under the board.

**Responsive ownership:**
- Wide desktop: card and choices side by side; optional **thin** rail for chapter/companion information. All regions have bounded flex/grid dimensions and `min-width:0; min-height:0`.
- Portrait phone: compact status bar plus active card/decisions; character, map, journal and ending gallery are tabs/dialogs **replacing or overlaying** the main panel, never below it. Condense controls but preserve comfortable tap targets. Phone portrait should not require the user to scroll the webpage to reach a choice.
- Tablet and short landscape desktop: responsive arrangement by both **available height and width**, not just breakpoints. Wide-but-short may need a different ratio; don't assume min-width guarantees available reading height.
- Very long scene prose, oversized gallery sets, or an opened journal **may scroll inside its own bounded pane**; fallback internal scroll is allowed only where genuinely needed. No clipping of the active choice, screen-reader focus, overflow menus, epilogue Continue, or modal Close.
- Account for site header, iOS safe-area insets, browser viewport bars / `dvh`, landscape, browser zoom, on-screen keyboard, accessibility text scaling, reduced motion, and focus movement. Hidden panels must not steal keyboard focus.

**Single screen means one current tab/view at a time**, not fitting a 10×10 collection with unreadably tiny cards. Achievements and Endings may be a distinct tab or bounded dialog; entering/leaving them should not reset current cards, dice, seed, tab selection, or progress.

### Minimum viewports and test assertions

At minimum render and measure:
- **Phone compact:** 375×667, 390×844 (and 320×568 fallback for tight content).
- **Tablet portrait:** 768×1024 and 820×1180.
- **Tablet/short landscape:** 1024×768 and a wide/short 1280×720.
- **Desktop:** 1440×900 and 1920×1080.
- Test ordinary and **longest** authored cards, open dice resolution, full badges, active journal and achievement/ending overlays, first run, all endings discovered, and art-loading/error fallback.

**Hard checks:** `documentElement.scrollHeight <= visualViewport.height + tolerance` **for the surface owner** (accounting for site header and browser chrome), `documentElement.scrollWidth <= viewport width + tolerance`, no unreachable buttons, no unintended document/body/root scrolling, no scroll-trap on modals, and all active controls visible or reachable in an explicit **inner** scroll region. Verify actual pixels and pointer/keyboard behavior in mounted browser tests, not only CSS class regexes or static screenshots. On narrow screens main stage should still show an active illustration/text/choice, not a blank page. Endings dialog reflows without spilling its grid.

## Two progression systems, both required

### A. In-game **Endings on File** (ten complete future families)

**Canonical source:** `ECOTONE-ENDINGS.md`, with at least the current ten named future families, 1/10/30-year epilogues and variations. **Count all ten stable canonical family IDs**, not every possible prose variant as a separate ending. Use stable lowercase IDs; no hardcoded index-based unlocks. A sample stable registry:

```text
redwood-commons
silicon-estuary
global-terminal
beautiful-museum
free-county
barricaded-county
worktown
tidelands-accord
redwood-sanctuary
split-county
```

The final ID mapping must be frozen before Kind Robots import, validated against `ECOTONE-ENDINGS.md`, and migration-aware if names change. **All ten** should have eligible rules, a dated unlocked epilogue, a compact summary, and secret/hidden spoiler policy.

**Persistent account-independent ledger:** after a *real completed ending*, the authored outcome resolver emits exactly one canonical ending ID and variant provenance. Add to a **versioned, deduplicated browser-local unlock ledger** separate from the in-progress run/save. Starting over, losing a character, replaying another route, changing initial intoxication, reopening the page, or migrating save formats must **not** erase previously earned endings. Resolved ending IDs cannot be forged from a simple tab click, automatically granted from sample scenes, or recorded before the finale. Local-only v1 matches the proven Shifting Desks approach; account synchronization is a future *optional* enhancement, not a prerequisite for unlocked content.

**Player-facing Endings gallery:** a visible progress affordance on the main board, e.g. `Endings: 3 / 10`, opens a single-surface gallery or modal with all ten **slots**:
- **Discovered:** recognizable title and thumbnail (when art exists), spoiler-safe epilogue summary, timestamp/first completion if available, accessible **Read ending** and **Replay journey** actions. Show variants/callbacks through details without counting them as separate families.
- **Undiscovered:** tasteful mystery silhouette / blurred illustrative treatment (once art approved); `Undiscovered` label and subtle thematic hint, **no hidden title, ending description or art-alt-text leak**, unless the title is intentionally public. A fully secret ending can be more deeply concealed, but the count stays honest.
- **Modal UX:** close/back returns to exact current game state, focus restores, Escape works, touch gestures never accidentally start a new run, and list rows scroll internally when the 10 cards exceed dialog space. Meaningful empty state before any completion and satisfying 10/10 state afterward.

**No achievements are earned simply by scrolling the ending gallery or selecting a locked item.**

### B. **Kind Robots global Achievement system**

Reuse existing shared catalog/award flow, not a conflicting one-off achievement backend:
- `silasfelinus/kind_robots/utils/achievements/gameAchievements.ts`: game registry, section grouping, canonical achievement code, nonrepeatable awards.
- `utils/achievements/catalog/games.ts`: existing 3-tier non-arcade game definitions.
- `components/achievements/achievement-gallery.vue`: site-facing listing.

**Proposed three initial Ecotone badges** (story unlock conditions to refine, all achievable through any initial sobriety state):
1. **The First Tomorrow** (tier 1): complete one genuine Ecotone finale, receive a 1-/10-/30-year epilogue, and record its ending ID.
2. **A County of Voices** (tier 2): during real authored gameplay, fulfill **meaningful commitments with distinct groups** and reach a future reflecting those collaborations, *without* forcing a single political position.
3. **All the Possible Humboldts** (tier 3): legitimately discover all **ten** distinct future families, across any number of full runs. No grind through four forced substance states.

Implementation may add more *in-game* milestones in a separate expanded gallery (Bigfoot kindness, habitat rescue, companion trust, historical truth, eccentric route) **only after scoped approval**. Ensure cross-run dedupe, source rule IDs, safe replay, unlock toast with nonintrusive dismissal and reduced-motion support. Do not enqueue badge art while Silas's art gate is closed.

## Acceptance/QA table

| Contract | Required proof |
| --- | --- |
| Ten futures are distinct | Static enum/registry check: exactly 10 unique stable IDs and no uncategorized finale |
| Ten naturally reachable endings | Engine-generated seeded test runs exercise **every** ending family with real, valid choices; don't manufacture a save that assumes already-earned IDs |
| Endings persist across runs | Real localStorage save/reload and new-game cycle preserve unlocked IDs and progress count |
| No spoilers | Locked endings hide specific title, detail, descriptive alt text and unrevealed conclusion |
| Award exactly once | Repeated finale/save restores do not duplicate ending ledger or global achievements |
| Global integration | Three canonical game achievement definitions and expected section appear in shared achievement gallery when legitimately earned |
| All states fair | Sober/tipsy/stoned/tripping initial branches have meaningful endings and access to the gallery; ancestry isn't a mechanical gate |
| Phone/tablet/desktop surface | For each viewport listed above, test opening, encounter, outcome, endings gallery, character/journal tabs and lengthy content with **no page-level scroll** |
| Accessible interaction | Keyboard navigation, touch size, labelled tabs, roving focus, focus restore, screen reader announcements, reduced motion, no modal keyboard trap |
| Assets fail gracefully | Empty/404/unapproved art leaves all information and buttons legible without page stretching |
| No publication shortcut | App preview and art go through existing human gates; **a green PR alone does not authorize publication** |

## Roadmap handoffs and ownership

- **Conductor** defines the design contract, encounter/ending canonical IDs, task dependencies and creative gates.
- **Kind Robots** owns the page, achievement catalog, local run persistence, browser UI and any eventually approved art.
- The eventual consumer feature work **must** derive from the reusable Shifting Lands/Desks primitives, not clone their Pinia stores/ID namespaces, and should add an Ecotone-specific browser test for both the board and endings.
- Existing `t-004` creative/art gate and `t-007` publish gate remain; these requirements do **not** authorize generating badge/icon/ending images.
- These are work acceptance criteria, not a claim that Ecotone currently has a public playable screen or working achievements.
