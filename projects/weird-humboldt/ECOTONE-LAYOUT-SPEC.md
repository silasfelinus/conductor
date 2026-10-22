# Ecotone: single-surface board and responsive tab layout spec

**t-014 · 2026-10-22 · text-only design.** Applies [VIEWPORT-ACHIEVEMENTS-CONTRACT.md](VIEWPORT-ACHIEVEMENTS-CONTRACT.md); that contract wins on any conflict. This is a plan for a future Kind Robots implementation, not a shipped screen. No deploy, no new art, no publication clearance (t-004 / t-007 gates stand).

## 1. Surface model

The Ecotone page owner is one `ecotone-shell` element sized to the usable viewport:

- `height: calc(100dvh - var(--kr-site-header-h))` with a `100vh` fallback; `padding` includes `env(safe-area-inset-*)`.
- `display: grid; overflow: hidden; min-width: 0; min-height: 0`. `html`, `body` and the page root never scroll (vertical or horizontal).
- Every flex/grid child sets `min-width: 0; min-height: 0`, so intrinsic image/prose size can never stretch the shell.
- Same primitives as the modern Shifting Lands journey board (`journey-shell`, `kr-pane-scroll`) and Shifting Desks (compact toolbar, `max-h-[90dvh]` dialogs). Reuse them; do not clone their Pinia stores or ID namespaces.

## 2. Screen structure (top to bottom, one view at a time)

| Region | Content | Rules |
| --- | --- | --- |
| **Top bar** (one row, fixed height) | Region/chapter chip · character control (five skill stats in a popover) · Clarity/status · **Endings 0/32** · Menu/Help | No second masthead or full redundant title. Wraps to icon-only controls under 400px width. Tap targets at least 44px. |
| **Stage** (flex, fills remainder) | Illustrated card face, concise narrative, optional cast badge, **decision area**, outcome overlay | Card art uses `object-fit: cover/contain` in a bounded box; never sets page height. |
| **Tab strip** | Journey · Character · Journal · Map · Achievements · Endings · Settings | Labelled `role="tablist"`, roving tabindex. Selecting a tab **replaces** the stage pane or opens a dialog. Never stacked below it. |

Decision area: 2 to 4 choice buttons, each showing the stat/check target and a consequence hint. The outcome overlay stays inside the stage bounds and its **Continue** button is pinned to the overlay's bottom edge, outside the scrolling prose.

## 3. Inner scroll ownership

Exactly these elements may scroll, each with `overflow-y: auto; overscroll-behavior: contain` and a bounded height:

1. **Narrative prose pane** inside the stage (only when the longest authored card overflows; choices are siblings of the pane, not inside it, so they stay visible).
2. **Journal / Journey / Map list pane** inside its tab.
3. **Endings grid** inside the dialog (32 slots, 4 groups of 8).
4. **Help / Tutorial / Settings dialog body.**

Choices, outcome Continue, modal Close, tab strip and top bar are never inside a scrolling pane. Modals use focus trap with Escape to close and focus restore to the opener; hidden panels get `inert` so they cannot take focus. Opening/closing a tab or dialog must not reset the current card, dice, seed, tab selection or progress.

## 4. Layout by viewport

Layout is chosen from **available width and height** (container queries / `matchMedia` on both axes), not width breakpoints alone.

| Viewport | Class | Arrangement |
| --- | --- | --- |
| 320×568 (fallback), 375×667, 390×844 | Phone portrait | Top bar (icon-only below 400px) / stage: card art about 35 to 40% of stage height (min 120px), prose pane, choices full width stacked / bottom tab strip. Character, Journal, Map, Endings are tabs or dialogs replacing the stage. Art may collapse to a thin banner at 320×568 so choices stay visible. |
| 768×1024, 820×1180 | Tablet portrait | Same stack as phone with larger art (about 45%); choices may go two-up when each is 2 lines or fewer. Tab strip stays at the bottom. |
| 1024×768, 1280×720 (wide-short) | Landscape | Card art left (about 45%), prose + choices right, both full stage height. Tabs along the top bar's right or a slim left rail. Below 700px height, drop the rail and use the tab strip as a bottom bar. |
| 1440×900, 1920×1080 | Desktop | Card and choices side by side; optional thin rail (up to 240px) for chapter and companion info. Content is capped at about 1400px wide and centered. |

Short-and-wide rule: when `height < 700` and `width >= 900`, use the landscape arrangement even on large screens, and cap art at `max-height: 100%` of the stage.

## 5. Robustness requirements

- Browser zoom to 200% and text scaling to 200%: the layout flips to the phone arrangement; nothing clips.
- On-screen keyboard (settings text inputs): `visualViewport` resize shrinks the shell; the focused input scrolls inside its dialog pane.
- Art loading, 404 or unapproved art: a fixed-aspect placeholder with alt text; information and buttons remain legible and the stage height does not change.
- Reduced motion: transitions and unlock toasts become instant/fades only.
- iOS safe-area insets on all four sides; landscape notch safe.

## 6. Testable viewport rules

Run in a mounted-page Cypress/Playwright suite (pattern: `cypress/public/shifting-desks-endings.cy.ts`, `utils/scripts/auditResponsiveLayout.mjs`). Viewports: 320×568, 375×667, 390×844, 768×1024, 820×1180, 1024×768, 1280×720, 1440×900, 1920×1080.

States per viewport: first run; ordinary card; **longest authored card**; open dice resolution; outcome overlay; full badges; Journal active; Endings dialog (empty and all 32 discovered); art 404.

| ID | Assertion |
| --- | --- |
| V1 | `documentElement.scrollHeight <= visualViewport.height + 1` and `scrollWidth <= innerWidth + 1` (shell is the only owner). |
| V2 | `getComputedStyle(body).overflow` is not scrollable and `window.scrollY` stays 0 after `scrollTo(0, 9999)`. |
| V3 | Every active choice button's `getBoundingClientRect()` lies fully inside the viewport, or inside a pane whose own rect is inside the viewport and which is not itself scrolled past it. |
| V4 | Outcome **Continue**, dialog **Close**, tab strip and top bar are never descendants of an `overflow: auto` element. |
| V5 | Only the elements named in section 3 have `scrollHeight > clientHeight` and non-hidden overflow. |
| V6 | No element's rect extends beyond the viewport horizontally (excluding `sr-only`). |
| V7 | Endings dialog: grid inside the dialog bounds, no horizontal spill, Escape closes and focus returns to the Endings button. |
| V8 | Tab keyboard: arrow keys move between tabs, hidden panels are `inert`, no focus trap outside open dialogs. |
| V9 | Opening and closing every tab leaves the card id, dice state, seed and progress unchanged. |
| V10 | With art 404, the choices' rects are identical (within 2px) to the art-loaded layout. |

## 7. Handoff and open points

- Conductor owns this spec; Kind Robots owns the page, the Endings dialog and the achievements wiring (contract section B).
- Open for creative review (t-004): tab ordering and labels; whether the thin desktop rail shows companion info or chapter info.
- The implementation task must add the V1 to V10 tests before any preview link is offered, and a green PR does not authorize publication.
