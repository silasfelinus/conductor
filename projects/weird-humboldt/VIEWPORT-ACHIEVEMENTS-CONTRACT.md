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
1. **One compact top bar:** current region / chapter, the five skill stats via one small character control, Clarity/status, Menu/Help, and a persistent **Endings 0/32** progress button. Avoid a second header with a full redundant game title. Site navigation can remain separate but consumes known usable viewport height.
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

## Companion follow history on a single visual surface

The first companion is supplied by the chosen prelude perspective; **do not place a free companion picker on the prelude or persistent toolbar**. Crossroad cards temporarily show a legible, accessible **Stay / Follow** choice, after which the active portrait and route-specific card content change without expanding beyond the viewport. The protagonist meets each other main character at an authored guaranteed stage in randomized order; game UI, Journal and companion info must retain the chronological `meeting_order` and `follow_history` and show which companion was left behind, without turning the cast into a four-character traveling party. Dice and stat changes from side cards must be reflected immediately in visible bounded widgets; no page scrolling for outcomes or gallery. Read [JOURNEY-LOOP-CONTRACT.md](JOURNEY-LOOP-CONTRACT.md). The ending gallery remains 32 slots, categorized by **final followed companion**, original opening lens and earned hope/dark fate; variations caused by order are callbacks, not extra unlocks.

## Two progression systems, both required

### A. In-game **Endings on File** (32 earned outcomes, 16 hopeful and 16 dark)

**Story registry:** [ECOTONE-32-ENDINGS.md](ECOTONE-32-ENDINGS.md). Collect exactly **4 lead companions × 4 fictional voluntary opening lenses × 2 earned fates = 32** unique IDs `lead.opening.hope|dark`. Lead is selected independently from first festival companion; `opening_state` remains immutable while `current_state` evolves. Fate is cumulative choice, verified evidence and skill/dice outcome, not a value judgment on sobriety. Old ten county futures are world-state motifs, not bonus collectibles.

**Persistent ledger:** award exactly one finale ID after actual completed play, locally versioned and deduped separately from active save; keep unlocks across new games, browser reload and current-state changes. Don't convert unshipped 10-family design motifs into fake earned 32-family slots. No points for simply visiting the gallery.

**Single-surface gallery:** toolbar `Endings X/32`, accessible tab/dialog grouped by four companions (8 slots each), four opening-state pairs (one hopeful and one dark per pair); spoiler-neutral `Hope X/16 · Dark X/16` totals optional. Undiscovered slots hide plot-specific titles, art descriptions, metadata and endings. Earned slots display individually authored title, 1/10/30-year epilogue, callbacks, first-completion and replay. All 32 in a bounded internal scroll pane when needed; **document never scrolls** on phone/tablet/desktop. Modal close/Escape restores saved game and keyboard focus.

**Parity:** Each opening has four hopeful and four dark ending IDs across companions; each companion has four good/four bad. Sobriety-first can achieve any companion's positive personal path and county progress. Completionists explore all four *fictional* optional starting perspectives over multiple runs, not real-life substances.

### B. **Kind Robots global Achievement system**

Reuse existing shared catalog/award flow, not a conflicting one-off achievement backend:
- `silasfelinus/kind_robots/utils/achievements/gameAchievements.ts`: game registry, section grouping, canonical achievement code, nonrepeatable awards.
- `utils/achievements/catalog/games.ts`: existing 3-tier non-arcade game definitions.
- `components/achievements/achievement-gallery.vue`: site-facing listing.

**Proposed three initial Ecotone badges** (story unlock conditions to refine, all achievable through any initial sobriety state):
1. **The First Tomorrow** (tier 1): complete one genuine Ecotone finale, receive a 1-/10-/30-year epilogue, and record its ending ID.
2. **A County of Voices** (tier 2): during real authored gameplay, fulfill **meaningful commitments with distinct groups** and reach a future reflecting those collaborations, *without* forcing a single political position.
3. **All the Possible Humboldts** (tier 3): legitimately discover all **32** authored companion×opening×fate endings across multiple full runs. No real-world substances or coerced in-game intake.

Implementation may add more *in-game* milestones in a separate expanded gallery (Bigfoot kindness, habitat rescue, companion trust, historical truth, eccentric route) **only after scoped approval**. Ensure cross-run dedupe, source rule IDs, safe replay, unlock toast with nonintrusive dismissal and reduced-motion support. Do not enqueue badge art while Silas's art gate is closed.

## Acceptance/QA table

| Contract | Required proof |
| --- | --- |
| 32 endings are distinct | Exactly 32 stable IDs, 16 hopeful / 16 dark, 8 per lead and 8 per opening; ten scenario motifs do not count |
| 32 naturally reachable endings | Real seeded engine choices/checks produce both results for each of 16 lead×opening combinations, including initially unpaired lead companions |
| Endings persist across runs | Real localStorage save/reload and new-game cycle preserve unlocked IDs and progress count |
| No spoilers | Locked endings hide specific title, detail, descriptive alt text and unrevealed conclusion |
| Award exactly once | Repeated finale/save restores do not duplicate ending ledger or global achievements |
| Global integration | Three canonical game achievement definitions and expected section appear in shared achievement gallery when legitimately earned |
| All states fair | Each opening can earn four positive and four dark endings without a drug-induced moral outcome bias or ancestry-based gate |
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
