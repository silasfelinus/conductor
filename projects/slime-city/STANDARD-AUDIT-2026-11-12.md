# Slime City: Clash — main-game standard audit (2026-11-12, kind_robots 7ad1136)

## A) Audit
| Item | Status | Evidence | Gap |
|---|---|---|---|
| Title screen | Partial | `components/slime-city-splash.vue:46-55` settings gear; `:230-255` VS / Journey / Tower / Collection tiles plus a crew picker | No Continue, Scrapbook or Achievements entry. Journey resumes silently |
| Settings | Partial | `pages/admin/slime-city.vue:90-131` has one control, "Default Clash deck" (solo/alliance). `lab.clashFormat` is not persisted (`stores/slimeCity.ts:475`) | Missing text size, reading speed, reduced motion (CSS media query only), high contrast, reset progress, persistence, and an in-play entry |
| Save/load | Partial | Server: `POST/GET /api/slime-city/story` into Prisma `SlimeCityAccount` (`prisma/schema.prisma:3842`). `SlimeCityStory` has `version: 1` and `revision` (`utils/slimeCity/storySave.ts`). Autosave via `persistStory()` (`stores/slimeCity.ts:650`) | **Guests get no persistence**: `hydrateStory` returns before loading (`:545-548`) and `persistStory` needs `storyLoaded`. Reloading mid-Clash forfeits the Tower floor (`:576-578`). VS matches are not resumable |
| Achievements 12+ | Missing | 0 live | t-060 |
| Scrapbook | Missing | none | t-059 |
| Endings + plates | Partial | `campaignEnding` (`utils/slimeCity/campaign.ts:656`): triumph or compromise × 6 crews | t-059 / t-062 |
| Characters | Partial | 6 crews (`utils/slimeCity/prototypes.ts:532+`) plus deck building | see B |
| Replay hooks | Met | 6 crew campaigns; seeded 12-floor Tower with `bestFloor`/`cinders` meta (`utils/slimeCity/allianceTower.ts:13,38`); packs/collection; PvP; storyMode/parity toggles | none |

## B) Characters
The crew choice is the "who you are" choice, and in a card battler that is a reasonable fit. A named player avatar would mostly be cosmetic. I'd treat crew + deck as meeting item 7, with an optional cosmetic crew banner or title from t-061. Silas decides.

## C) Proposed achievements (all new)
| triggerCode | Label | Message | Award at |
|---|---|---|---|
| slime-city-first-clash-win | First Blood | Your crew took the street. | `settleClash` (`stores/slimeCity.ts:1669`), victor is the player |
| slime-city-chapter-won | Turf Claimed | A campaign chapter falls your way. | `settleBout` on a campaign win |
| slime-city-campaign-{catgirls,bloodfairies,ironjaw,riot,undertow,exchange} (×6) | crew campaign title | Finished that crew's campaign. | after `settleBout` when `campaignEnding(save, team)` first becomes non-null |
| slime-city-conviction-triumph | True to the Code | Won a campaign on Conviction. | same point, ending === triumph |
| slime-city-cunning-compromise | Dirty Deal | Won by Cunning and paid for it. | same point, ending === compromise |
| slime-city-all-crews | Whole City | All six crews' stories told. | same point, all 6 non-null |
| slime-city-tower-floor-6 | Halfway Up | Cleared Tower floor 6. | `settleClash` tower branch (`:1674`), `run.floor >= 6` |
| slime-city-tower-summit | Top of the Tower | All 12 floors cleared. | same, `phase === 'complete'` |
| slime-city-first-evolution | It's Evolving | A card evolved mid-Clash. | Clash evolution event (`utils/slimeCity/clashEvolutions.ts` resolve, surfaced in `components/slime-city-clash.vue`) |
| slime-city-first-pack | Fresh Meat | Opened a Meat pack. | `purchasePack` success (`:379`) |
| slime-city-alliance-builder | Two Crews, One Deck | Saved an Alliance deck. | `commitAlliance` (`:1121`) |
| slime-city-city-finale | Slime City Decides | Made the city's final call. | `chooseFinale` (`:2108`) |
| slime-city-pvp-win | Real Rival | Beat another player. | PvP settle, `stores/slimeCityPvp.ts` |

## D) Three ~1-day PRs (title, settings, save)
1. **Guest local save.** In `hydrateStory`/`persistStory` (`stores/slimeCity.ts`), let guests save to localStorage key `kr-slime-city-story-v1`, reusing the existing validators in `utils/slimeCity/storySave.ts`. On sign-in, offer to import it into the account. Add a test in `utils/scripts/`.
2. **Settings panel.** Expand the settings view in `pages/admin/slime-city.vue:90-131`: text size, animation speed, reduced motion, high contrast, default deck format (persisted), and "Reset progress" with a typed confirmation. Add a gear in the Clash HUD (`components/slime-city-clash.vue`). Reuse the `utils/playbookKit/settings.ts` model.
3. **Title console.** In `components/slime-city-splash.vue`, add Continue (resume `journeyTeam`/`journeyScreen`), Achievements (mount `game-achievement-strip` once t-060 lands; it renders nothing until then), and a Scrapbook stub tile for t-059. Add a `slime-city` section in `utils/achievements/gameAchievements.ts`.

## E) Reusable
The `SlimeCityAccount` pattern (userId + Json + version, plus a revisioned GET/POST) is the template for a generic `GameSave` model that the other three games lack.

## Shared notes
- Live `/api/achievements` on 2026-11-12: emperor 3, shifting-desks 3, zuzu-gamebook 3, slime-city 0.
- None of the four audited games has audio, so the "music/sound volume" setting has nothing to control until sound exists.
- None of them mounts `components/achievements/game-achievement-strip.vue`; only `pages/play/arcade/index.vue` and `components/navigation/workspace-sheet.vue` use it.
- The only account-backed save among the four is Slime City's `SlimeCityAccount`.
- Shared components:
  - **Settings + scrapbook kit:** `stores/playbookKitStore.ts` and `utils/playbookKit/settings.ts` (textSize, font, contrast, motion, textSpeed, sound, trailer, plus resetSettings, one versioned localStorage record per game), and `components/playbook-kit/playbook-kit-{settings,scrapbook,endings,shell}.vue`. Used today by monstrique, game-of-captains and every-villain-tactics.
  - **Title console:** `components/monstrexx/monstrexx-front.vue` (New / Continue / settings / scrapbook panels; the standard's reference). It could be generalized into a `game-title-console` that takes a game slug and its art.
  - **Save:** Emperor's `saves.ts` for slots and rewind; Slime City's `SlimeCityAccount` + story GET/POST to generalize into a `GameSave` model for account-backed saves.
  - **Achievements:** `game-achievement-strip.vue` plus `achievementsForGame()`. Each game needs an `ACHIEVEMENT_SECTIONS` entry; slime-city has none yet.
