# Zuzu Gamebook — main-game standard audit (2026-11-12, kind_robots 7ad1136)

Fixed hero Zuzu, so item 7 is exempt.

## A) Audit
| Item | Status | Evidence | Gap |
|---|---|---|---|
| Title screen | Missing | `pages/play/zuzu-gamebook.vue:1-90` opens straight into the reader. "New journey" sits in the HUD | Needs a cover with Continue / New / Settings / Ledger / Achievements |
| Settings | Missing | none | Everything in item 2 |
| Save/load | Partial | `kr-zuzu-gamebook-v1` (Run `version: 1`, `isSavedRun`), autosaved on every choice (`stores/zuzuGamebookStore.ts:19-21,30-45`). A recovery slot keeps the previous journey. Save-code export/import works across devices (`utils/zuzuGamebook/saveCode.ts`) | Endings record is an unversioned array. One slot. No account save |
| Achievements | Partial | 3 live (`awardDeeds`, `:96-107`) | 9+ more |
| Scrapbook | Partial | Bell Ledger: endings X/15 with locks (`:250-285`) and a recent "Illustrated trail" (`:286-312`) | Unlocked endings show the **raw id** (`ending-bell`), not the title or plate. No characters, no per-run pages |
| Endings + plates | Partial | **15 endings** (4 hope, 5 dark, 6 bittersweet): `utils/zuzuGamebook/book.ts:1336-1400` (8), `acts/act8.ts` (2), `acts/act9.ts` (5). 12 have exact section plates (`sectionArt.ts:2440+`). `ending-water` uses the exact `kasa-on-water` plate | `ending-wren-lamp` and `ending-bell-keeper` share the generic `bell-tower` scene (used 12×). Queue 2 plates |
| Characters | Exempt | Fixed Zuzu, starting stats at `adventure.ts:63` | none |
| Replay hooks | Met (thin) | Branching into 15 endings, a dice seed per run, collecting endings | Nothing carries over between runs. Consider an ending-earned boon |

## B) Characters
Exempt: Silas's 2026-11-11 decision keeps the fixed protagonist Zuzu. Every other item still applies.

## C) Proposed achievements (keep the existing 3)
All are awarded in `awardDeeds(before, after)` unless noted.
- zuzu-gamebook-first-fight-won / -hopeful-ending / -ring-the-bell (existing)
- zuzu-gamebook-croc-crossing: "Through the Teeth", beat River Croc (`before.battle`, foe name, `after.sceneId === foe.win`)
- zuzu-gamebook-abbess-falls: "The Abbess Falls", beat The Abbess, same pattern
- zuzu-gamebook-reached-the-mission: "Hollow Bell", first scene with chapter `CH.V`
- zuzu-gamebook-reached-the-bell: "The Last Stair", first scene with chapter `CH.IX`
- zuzu-gamebook-quiet-draw: "One Clean Cut", fight won with a final round of `quiet-draw` (`after.lastFight.rounds`)
- zuzu-gamebook-untouched: "Not a Scratch", fight won with every round `taken === 0`
- zuzu-gamebook-double-six: "Desert Luck", `after.lastRoll.dice` is [6,6]
- zuzu-gamebook-sister-free: "Her Own Knife", flag `sister-free` newly set
- zuzu-gamebook-one-fire: "One Fire", reach `ending-four`
- zuzu-gamebook-dark-road: first `dark` ending
- zuzu-gamebook-bittersweet: first `bittersweet` ending
- zuzu-gamebook-three-tones: "All Three Roads", one of each tone, in `rememberEnding` (`:46`)
- zuzu-gamebook-five-endings: 5 of 15, in `rememberEnding`
- zuzu-gamebook-every-ending: 15 of 15, in `rememberEnding`

Skip awards on `importCode`, so a pasted save code can't unlock achievements.

## D) Three ~1-day PRs
1. **Cover + settings.** A cover view in `pages/play/zuzu-gamebook.vue` with Continue (chapter and scene title), New Journey (with confirmation, keeps the recovery slot), Settings, Bell Ledger, and the Achievements strip. Settings reuse `usePlaybookKitStore` and `playbook-kit-settings.vue` (the game already uses the playbook live-text pipeline). Include reset progress with confirmation.
2. **Achievements to 18.** Seed the records, extend `awardDeeds`/`rememberEnding`, and add a `zuzu-gamebook` entry in `utils/achievements/gameAchievements.ts`.
3. **Ledger as scrapbook.** Show ending titles plus their `SECTION_PLATES` thumbnails with silhouettes when locked, add a "Companions met" panel from flags (sister / Wren / coyote / Abbess), and keep a per-run summary on `restart()` (versioned key `kr-zuzu-gamebook-scrapbook-v1`). Queue plates for wren-lamp and bell-keeper in the conductor art ledger.

## E) Shared components across the four
- **Settings + scrapbook kit:** `stores/playbookKitStore.ts` and `utils/playbookKit/settings.ts` (textSize, font, contrast, motion, textSpeed, sound, trailer, plus resetSettings, one versioned localStorage record per game), and `components/playbook-kit/playbook-kit-{settings,scrapbook,endings,shell}.vue`. Used today by monstrique, game-of-captains and every-villain-tactics.
- **Title console:** `components/monstrexx/monstrexx-front.vue` (New / Continue / settings / scrapbook panels; the standard's reference). It could be generalized into a `game-title-console` that takes a game slug and its art.
- **Save:** Emperor's `saves.ts` for slots and rewind; Slime City's `SlimeCityAccount` + story GET/POST to generalize into a `GameSave` model for account-backed saves.
- **Achievements:** `game-achievement-strip.vue` plus `achievementsForGame()`. Each game needs an `ACHIEVEMENT_SECTIONS` entry.

## Shared notes
- Live `/api/achievements` on 2026-11-12: emperor 3, shifting-desks 3, zuzu-gamebook 3, slime-city 0.
- None of the four audited games has audio, so the "music/sound volume" setting has nothing to control until sound exists.
- None of them mounts `components/achievements/game-achievement-strip.vue`; only `pages/play/arcade/index.vue` and `components/navigation/workspace-sheet.vue` use it.
- The only account-backed save among the four is Slime City's `SlimeCityAccount`.
