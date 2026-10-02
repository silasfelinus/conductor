# kr-solitaire survey: card back art and component patterns

date: 2026-10-02 · task: kr-solitaire/t-003 · read-only survey of silasfelinus/kind_robots (no code changes)

## What exists

| Asset / component | Where | Useful for Solitaire? |
|---|---|---|
| Five workspace card backs | `/images/adventure/card/card-back{1..5}.webp`, listed as `CARD_BACKS = [1,2,3,4,5]` in `components/navigation/card-picker.vue`, duplicated in `workspace-hand.vue` and `workspace-narrator.vue` | **Yes, these are the card-back set.** Shown at `aspect-2/3` with `object-cover`. |
| Back-picker UI | `components/navigation/card-picker.vue` (header comment says `components/user/card-back-picker.vue`, stale) | Pattern to copy. Persists choice in `localStorage` key `kr.workspaceCardBack` and fires `window` event `kr:card-back-change`. Reusing the same key means a player's workspace choice carries into the game for free. |
| Flip component | `components/navigation/flip-card.vue` | Front/back slots with a CSS 3D flip (`durationMs` 650, `radius` 1.75rem, `scale` 1.06). Stock-to-waste turn can use it, but 650ms is too slow for draw-3; pass a smaller `durationMs` (about 220). |
| Entity card back (info panel) | `components/gallery/kr-card-back.vue` | Not relevant: it is the "back of a baseball card" stats panel, not a physical card back. Do not confuse it with card backs for this game. |
| Character and reward art | `components/characters/character-gallery.vue`, `components/rewards/reward-gallery.vue`, `components/bots`, `components/scenarios` | Source for J/Q/K court art (t-006/t-007), not for backs. Gallery cards also use `aspect-2/3`. |

## Aspect ratio

Everything card-shaped in kind_robots is **2:3** (`aspect-2/3`). Standard playing cards are about 5:7 (0.714) versus 2:3 (0.667), a 7% difference. Recommendation: render game cards at 2:3 to stay consistent with the five backs and the gallery, so backs need no cropping. Faces (t-006/t-007) should be generated at 2:3 too.

## Where /play pages live

`pages/play/` holds one file or one folder per game or tool: `video-generator.vue`, `aquarium/`, `challenges/`, `mandarin/` (`index.vue`, `browse.vue`, `learn/[key].vue`). `pages/play/solitaire.vue` (or `solitaire/index.vue` if stats and daily deal become sub-routes) fits the convention; no router config is needed (file-based). Pages open with an HTML comment naming their path and the task that introduced them.

## Lazy static assets

- No card images are committed in the repo: `public/` only holds icons, `cthulhuquarium-plates/` and similar, and `nuxt.config.ts` sets `transformAssetUrls.includeAbsolute: false` with the comment "`/images/...` is served by the external media origin at runtime". Card backs therefore load from the media origin by absolute path, exactly as `card-picker.vue` does, and **must not** be imported through the bundler.
- The existing lazy pattern is a plain `<img loading="lazy">`. For Solitaire only the selected back is needed up front; the picker can lazy-load the other four. Face art for 52 cards should load per-suit on demand, and the fallback deck (t-005) must be pure CSS/SVG so the game is playable before any art loads or if the media origin is down.
- `@nuxt/image` is installed but the card components use raw `<img>`; follow them.

## Recommendation: card-back set

Offer **all five existing backs** (1 to 5) as the launch set. They are already curated, already selectable in the workspace, and cost no new generation. Default to the player's stored `kr.workspaceCardBack` value (fallback 1). A sixth, game-specific "Kind Robots Solitaire" back is an optional later generation task (t-008 can decide after seeing how the five look at the small tableau size of roughly 60px wide).

Open item for t-008: the five webp files are not in this repo, so their pixel dimensions and visual style at small sizes could not be inspected from here; check on the media origin before finalizing.

## Implications for other tasks

- t-004 (engine): no UI coupling; keep `utils/solitaire/` pure TS.
- t-005 (page): `pages/play/solitaire.vue`, 2:3 cards, CSS fallback deck, reuse `flip-card.vue` with a short duration or skip flips for speed.
- t-008 (backs): reuse `kr.workspaceCardBack` and the `kr:card-back-change` event; extract the duplicated `CARD_BACKS`/`cardBackSrc` into one shared util rather than copying a fourth time.
