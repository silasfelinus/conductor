# Cthulhuquarium — main-game standard audit (2026-11-12, kind_robots 7ad1136)

This was read-only. I changed no files, made no commits and called no write APIs. Code is from kind_robots `origin/main` @ 7ad1136. I checked live state with `curl`.

## Shared findings that apply

**Live achievements: 0.** `/api/achievements` returns 145 records and none has a ruler/cthulhu/aquarium/comet/prom/captain/couch prefix.

**A test blocks 12+ achievements in every game.** `utils/scripts/verifyGameAchievements.test.ts:20-32` requires every game in `ACHIEVEMENT_GAMES` to have exactly 3 achievements, one at each tier [1,2,3]. The header comment in `utils/achievements/gameAchievements.ts` says "three per game" too.
- A prerequisite PR has to change the test: arcade games keep exactly 3; main games need 12 or more, using tiers 1–3 repeatedly.
- The same test (`:145-151`) also requires every event code to appear literally as `'<code>'` in a `.ts`/`.vue` file. That's good: it forces the award to be wired.
- Icons must exist in `assets/icons` (`:53`).

**How to register a game's achievements:**
1. Add the game to `OTHER_GAMES` in `utils/achievements/gameAchievements.ts:80`. The `key` must be the conductor slug, because `achievementCode()` builds `<slug>-<key>`.
2. Add a section to `AchievementSectionKey`/`ACHIEVEMENT_SECTIONS`.
3. Add the definitions in `utils/achievements/catalog/` (one file per game is cleaner than growing `games.ts`).
4. Create the live records with `scripts/seed_achievements.ts`, which upserts by triggerCode; queue badge art with `scripts/generate_achievement_art.ts`.
5. `GameAchievementStrip` then shows automatically in the workspace sheet (`components/navigation/workspace-sheet.vue:176`), because `achievementGameForPath` matches the route.

Guests already get pending local awards (`stores/achievementStore.ts:755`).

**What "Playbook" means here.** Cthulhuquarium does not use the shared runtime shell (Playbook Kit). It only has a **Playbook Studio/Manager** adapter (`utils/playbook/cthulhuquarium.ts`), which is authoring and review only.

**Reusable pieces:** save slots with schema migration in `utils/rulerHooked/save.ts`; save-code export/import in `utils/cometAcademy/consoleScreens.ts:107`; account-backed collection sync with a local fallback in `gameOfCaptainsStore.ts:150-270`.

**Audio:** Cthulhuquarium is the only one of the four audited games with audio, and it only has a sound on/off toggle.

## 2. Cthulhuquarium (`/play/aquarium`, conductor t-100 / t-101)

An idle game with a server-backed tank (`server/api/aquarium/**`, `stores/cthulhuquariumTankStore.ts`). It is login-only: guests get the shop window (`components/cthulhuquarium/cthulhuquarium-play.vue:8`).

**A) Audit**

| Item | Status | Evidence | Gap to close |
|---|---|---|---|
| Title screen | Missing | `cthulhuquarium-play.vue` drops straight into the tank | A light cover with Enter tank / Settings / Ichthyonomicon / Achievements (may not suit an idle game; Silas's call) |
| Settings | Partial | HUD sound toggle saved to localStorage (`cthulhuquarium-game.vue:167`, `stores/helpers/cthulhuquariumStory.ts:253`), fullscreen, guide toggle; OS reduced motion via CSS (`:3543`) | Sound and ambience volume, text size, high contrast, a reduced-motion override, and reset tank (needs a confirm-gated server endpoint; destructive, so flag it) |
| Save/load | Met | Everything is in the database (Aquarium/AquariumStock/AquariumEvent), with offline settlement through `tick.post.ts` | None |
| Achievements 12+ | Missing | 0 live | See C |
| Scrapbook | Partial | Ichthyonomicon with 151 species, silhouettes and "X of Y recorded" (`cthulhuquarium-ichthyonomicon.vue:12,76`); 20 Charlotte scenes seen once and stored on the server; 16 unlockable backgrounds | No screen to rewatch scenes or see backgrounds and finale plates, and no "characters met" page |
| Endings with plates | Partial | One finale, "The Last Aquarium" (250k coins, `server/utils/aquariumEconomy.ts:431`), with its own plate (`assets/images/cthulhuquarium/cthulhuquarium-screen-finale.webp`, `cthulhuquarium-game.vue:791`). The bestiary-complete beat shows only a trophy icon (`:745`) | Several endings. Proposal for Silas: branch the finale reframe on the tank's dominant stat (six per-stat rarities already exist: charm, empathy, grace, luck, might, wits; `aquariumEconomy.ts:107`) and queue a plate for each, plus a plate for bestiary-complete |
| Characters | Missing (may not apply) | No player avatar. Personalization is the tank: decor, sets, backgrounds, nicknames, public visibility | See B |
| Replay hooks (3+) | Met | 151-species collection, milestone-unlocked backgrounds and slot caps, rare events and rivalry, public tank browsing and leaderboard, upgrade tracks | Run-based hooks don't apply |

Dead content: the `first_hatch`, `first_breed` and `first_evolution` scenes are authored, and an `AquariumEgg` Prisma model exists, but no server or store code uses them.

**B) Character customization.** I'd recommend Silas grant an exception, or count tank customization as the character, since the tank is the avatar in an idle aquarium. A cheap optional extra: a keeper name and portrait that Charlotte uses in dialogue.

**C) Proposed achievements (17)**

All award calls go in `stores/cthulhuquariumTankStore.ts`. The game is server-backed and login-only, so awards are always recorded.

| triggerCode | Label | Message | Award at |
|---|---|---|---|
| cthulhuquarium-first-adoption | The First One Is on the House | Your first resident moved in. | `unlock` :673, beside `queueScene('first_unlock')` :691 |
| cthulhuquarium-bestiary-10 | Collector of Small Horrors | 10 species observed. | `announceMilestones` :464, id `bestiary_10` |
| cthulhuquarium-bestiary-25 | Curator of the Uncanny | 25 species observed. | same place, `bestiary_25` |
| cthulhuquarium-bestiary-50 | Keeper of the Deep | 50 species. | `bestiary_50` |
| cthulhuquarium-bestiary-95 | Abyssal Archivist | 95 species. | `bestiary_95` |
| cthulhuquarium-bestiary-complete | Every Species, Observed | The Ichthyonomicon is full. | `announceBestiaryComplete` :469 |
| cthulhuquarium-full-tank | Standing Room Only | Your tank is full. | `announceMilestones`, `first_full_tank` |
| cthulhuquarium-spotless | Spotless | Not a speck of debris. | `first_spotless_tank`, from the clean flush :756 |
| cthulhuquarium-rivalry | Peace in the Tank | You settled your first rivalry. | `first_rivalry_resolved` :555 |
| cthulhuquarium-mythic | Something Very Old | A mythic species answered your call. | `unlock` :673 when `rarityKey(tier)==='mythic'` |
| cthulhuquarium-feeding-frenzy | Dinner Is Served | You fed five or more hungry mouths at once. | `feedHungry` :658, result length 5 or more |
| cthulhuquarium-first-set | Set Dressing | Your first set piece is installed. | `equipSet` :894 |
| cthulhuquarium-decorator | Interior Design of the Deep | Ten decorations placed. | `purchaseDecor` :953, count reaches 10 |
| cthulhuquarium-visiting-hours | Visiting Hours | Your tank is open to the public. | `setVisibility(true)` :1023 |
| cthulhuquarium-new-scenery | A Change of Scenery | You hung an unlocked background. | background change, via `/api/aquarium/background` in the story helper |
| cthulhuquarium-release | Return to the Deep | You let one go. | `sell` :717 |
| cthulhuquarium-last-aquarium | You Are Also in an Aquarium | You bought the Last Aquarium. | `purchaseFinale` :1057 |

**D) Three PRs**
1. **Achievements.** Add `catalog/cthulhuquarium.ts` and an `OTHER_GAMES` entry with route `/play/aquarium`. Wire the calls in `cthulhuquariumTankStore.ts` and add the strip.
2. **Settings panel.** A new `cthulhuquarium-settings.vue` dialog opened from the HUD. Include sound and ambience volume as gain on `utils/cthulhuquariumSound.ts` and `cthulhuquariumAmbience.ts` (replacing the boolean), text size, high contrast and a reduced-motion override, persisted in localStorage. Reset tank goes behind a confirmation; flag it for Silas because it is destructive and server-side.
3. **Memory Book tab.** Rewatch seen scenes from `CTHULHUQUARIUM_SCENES` (20), a background gallery (16), and finale plus bestiary plates shown locked until earned, with "X of N". Finale variants: queue the plates in the conductor art ledger (auto_submit) once Silas approves the branching.

**E)** No shared Playbook Kit runtime is used here. Its scrapbook and settings components (`components/playbook-kit/playbook-kit-scrapbook.vue`, `playbook-kit-settings.vue`) are the nearest reusable models for the Memory Book and settings panel.

## Decisions for Silas
- Whether Cthulhuquarium is exempt from character customization.
- Whether Cthulhuquarium's finale should branch into several endings.
- Whether a server-side "reset tank" is wanted.
