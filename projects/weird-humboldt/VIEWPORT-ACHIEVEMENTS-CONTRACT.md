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

### A. In-game **Endings on File** (32 story endings; 16 hopeful, 16 dark)

**Canonical ledger:** [ECOTONE-32-ENDINGS.md](ECOTONE-32-ENDINGS.md) requires 32 unique `final_lead.opening_lens.hope|dark` strings, 8 per lead companion and 8 per opening lens, with 16 of each fate. `opening_state` comes from the voluntary festival choice and determines the first encounter, while `current_state` may change; **the final companion results from active stay/follow decisions at fixed meetings**, not an upfront independent character picker. Outcome comes from persistent stats, choices, evidence, relationships and dice checks, never substance morality. The prior ten county futures are only **scenario motifs** and do not create gallery slots.

**Persistent unlocks:** after a genuine, fully resolved end scene, record its single `endingId` and chronological follow/encounter provenance in a schema-versioned deduplicated **browser-local ledger separate from the current run**. Refresh, save/reload, New Game, later route switch and closing/reopening a modal must preserve unlocks; a pre-existing old prototype future-family ID must **not** silently grant any of the new 32. **No awards from simply reading a gallery entry.**

**One-screen gallery:** a visible compact `Endings X/32` button on the game board opens a bounded tab/modal with four companion groups, eight items per companion, each showing two fate slots for each of the four opening lenses. Optional `Hope X/16 · Dark Y/16` progress counters do not expose locked titles. Each undiscovered card shows a silhouette/neutral hint with no spoiler-bearing art, alt text or detail. Each discovered card shows the earned unique title, 1/10/30-year story, optional date/flag callbacks, and a safe replay path. **Long collections scroll only within a bounded inner pane**, never the page; Escape/Close restores focus and the exact active journey. Enforce the same 375×667, 390×844, 768×1024, 820×1180, 1024×768, 1440×900 etc viewport contracts with **32 cards**, not the old 10.

**Separate timeline metadata:** Two runs might unlock the same ID but have completely different intervening randomized cards, follow history and local consequences; display earned variant provenance / best-known callback optionally, but do not count a new unlock unless the actual `endingId` differs.

### B. **Kind Robots global Achievement system**

Reuse existing shared catalog/award flow, not a conflicting one-off achievement backend:
- `silasfelinus/kind_robots/utils/achievements/gameAchievements.ts`: game registry, section grouping, canonical achievement code, nonrepeatable awards.
- `utils/achievements/catalog/games.ts`: existing 3-tier non-arcade game definitions.
- `components/achievements/achievement-gallery.vue`: site-facing listing.

**Proposed three initial Ecotone badges** (story unlock conditions to refine, all achievable through any initial sobriety state):
1. **The First Tomorrow** (tier 1): complete one genuine Ecotone finale, receive a 1-/10-/30-year epilogue, and record its ending ID.
2. **A County of Voices** (tier 2): during real authored gameplay, fulfill **meaningful commitments with distinct groups** and reach a future reflecting those collaborations, *without* forcing a single political position.
3. **All the Possible Humboldts** (tier 3): legitimately complete **all 32** distinct `final_companion.opening_lens.outcome` endings across multiple runs, without drug-required successes or any real-world intake.

Implementation may add more *in-game* milestones in a separate expanded gallery (Bigfoot kindness, habitat rescue, companion trust, historical truth, eccentric route) **only after scoped approval**. Ensure cross-run dedupe, source rule IDs, safe replay, unlock toast with nonintrusive dismissal and reduced-motion support. Do not enqueue badge art while Silas's art gate is closed.

## Acceptance/QA table

| Contract | Required proof |
| --- | --- |
| 32 endings are distinct | 32 stable collectible IDs: 4 final leads × 4 openings × 2 earned fates, 16 hopeful/16 dark, no extra ten county-future slots |
| 32 endings are naturally reachable | Real seeded gameplay reaches every combo via the **correct fixed initial companion** and actual stay/switch meetings, with both earned hopeful and dark choices/rolls; no injected flags |
| Endings persist across runs | Real localStorage save/reload and new-game cycle preserve unlocked IDs and progress count |
| No spoilers | Locked endings hide specific title, detail, descriptive alt text and unrevealed conclusion |
| Award exactly once | Repeated finale/save restores do not duplicate ending ledger or global achievements |
| Global integration | Three canonical game achievement definitions and expected section appear in shared achievement gallery when legitimately earned |
| Opening states fair | Every lens has four hopeful/four dark outcomes and can follow any companion, including Cedar technoutopia. Ancestry and consumption aren't mechanically required to be good |
| Phone/tablet/desktop surface | For each viewport listed above, test opening, encounter, outcome, endings gallery, character/journal tabs and lengthy content with **no page-level scroll** |
| Accessible interaction | Keyboard navigation, touch size, labelled tabs, roving focus, focus restore, screen reader announcements, reduced motion, no modal keyboard trap |
| Assets fail gracefully | Empty/404/unapproved art leaves all information and buttons legible without page stretching |
| No publication shortcut | App preview and art go through existing human gates; **a green PR alone does not authorize publication** |
| Companion order and randomized stats matter | Browser gameplay demonstrates stay/follow history, seeded distinct side-card draws, stat changes and callbacks within a shared ending ID, all without page scrolling |

## Roadmap handoffs and ownership

- **Conductor** defines the design contract, encounter/ending canonical IDs, task dependencies and creative gates.
- **Kind Robots** owns the page, achievement catalog, local run persistence, browser UI and any eventually approved art.
- The eventual consumer feature work **must** derive from the reusable Shifting Lands/Desks primitives, not clone their Pinia stores/ID namespaces, and should add an Ecotone-specific browser test for both the board and endings.
- Existing `t-004` creative/art gate and `t-007` publish gate remain; these requirements do **not** authorize generating badge/icon/ending images.
- These are work acceptance criteria, not a claim that Ecotone currently has a public playable screen or working achievements.
