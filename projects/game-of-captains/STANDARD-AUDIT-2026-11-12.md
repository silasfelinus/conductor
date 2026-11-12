# Space Couch — main-game standard audit (2026-11-12, kind_robots 7ad1136)

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

**What "Playbook" means here.** There are two separate things, and they aren't the same as the games' own engines:
- **Playbook Studio/Manager** (`utils/playbook/*`, `components/playbook/*`) is authoring and review only. The only runtime piece is `PlaybookRunReview`, a star rating at run end, which Space Couch uses.
- **Playbook Kit** (`utils/playbookKit/*`, `components/playbook-kit/*`, `stores/playbookKitStore.ts`) is the shared runtime shell. Of the four audited games only **Space Couch** uses it; MONSTRIQUE, Every Villain Tactics and Lantern Ferry also do. It already provides:
  - **Settings** (`playbookKit/settings.ts`): text size, font, contrast, motion, text speed, sound on/off, trailer and romance. It has Defaults, a confirm-gated "Forget progress" (`playbook-kit-settings.vue:40`) and a versioned per-game localStorage save.
  - **Scrapbook** of moments with blurred locked silhouettes and an "X of N kept" count (`playbook-kit-scrapbook.vue`).
  - **Endings gallery** with a found/total count per tone and an art slot for every ending (`playbook-kit-endings.vue`).
  - Cast, factions and secrets panes, plus a title trailer.
- **What the Kit is missing:**
  - A title screen with New / Continue / Achievements.
  - An achievements pane.
  - Separate music and sound volume levels (it only has sound on/off).
  - A page per finished run.
  - Account-backed sync.
  - A character creator.
- **Highest-leverage fix:** add an `achievements` pane to `playbook-kit-shell.vue` (panes list at `:265`) that renders `GameAchievementStrip :game="spec.conductorSlug"`, and add a music/sound volume setting to `KIT_SETTING_OPTIONS`. Doing it once helps every Kit game.

**Other reusable pieces:** save slots with schema migration in `utils/rulerHooked/save.ts`; save-code export/import in `utils/cometAcademy/consoleScreens.ts:107`; account-backed collection sync with a local fallback in `gameOfCaptainsStore.ts:150-270`.

**This game has no audio**, so the "music and sound volume" requirement can't be met until audio exists.

## 4. Space Couch (`game-of-captains`, `/play/game-of-captains`, t-041 / t-040)

**A) Audit**

| Item | Status | Evidence | Gap to close |
|---|---|---|---|
| Title screen | Partial | CONTINUE VOYAGE, START NEW GAME (with a confirmation to replace), SETTINGS, CAPTAIN'S LOG, SPECIES SCRAPBOOK 0/101 (`pages/play/game-of-captains.vue:40-110`) | Achievements button |
| Settings | Partial | Two separate settings systems. The title's "Ship settings" has large text and reduced motion (`stores/gameOfCaptainsStore.ts:473,738`). In play, the Kit pane has text size, font, contrast, motion, text speed, sound, romance, and Forget progress with confirmation | Merge them into one; there's no reset at the title. No audio |
| Save/load | Partial | Local autosave `game-of-captains-voyage-v1` (`gameOfCaptainsStore.ts:110,492`). The alien guide is saved to the account through `/api/game-of-captains/guide`. Redshirt knowledge carries across runs | `restoreVoyage` rejects any save with `version !== 1` (`utils/gameOfCaptains/rules.ts:1625`). The voyage itself isn't account-backed |
| Achievements 12+ | Missing | 0 live | See C |
| Scrapbook | Partial | Kit scrapbook of about 29 moments and an endings gallery with locks and counts (`gameOfCaptainsStore.ts:480`); 101-species alien scrapbook (`components/gameOfCaptains/alien-scrapbook.vue`) | No page per finished voyage; the Captain's Log covers only the current one |
| Endings with plates | Partial | 18 Kit endings (`utils/playbookKit/games/spaceCouch.ts:407`). Only 4 painted (`public/game-of-captains/endings/*.webp`). The in-game ending uses consequence paintings (`game-of-captains.vue:2083`) | Queue 14 plates |
| Characters | Met | 5 captains, 6 origins, 48 star signs from the Couchscope test, crew of 3–4 chosen by the player; the story adapts | Optional custom name |
| Replay hooks (3+) | Met | 18 endings, 101-species collection, carried-over redshirt knowledge, 5×6×48 starts, trio and romance branches, clone lab | None |

**B) Character customization.** Exists and suits the genre. No exception needed.

**C) Proposed achievements (16)**

Most go in `stores/gameOfCaptainsStore.ts`. The single place to award ending achievements is `recordKitUnlocks` :480, on each newly unlocked `earned.endings` id; `kit.unlock` already returns whether the id is new.

| triggerCode | Label | Message | Award at |
|---|---|---|---|
| game-of-captains-launch | Unlicensed and Airborne | The couch has left the atmosphere. | `begin` :568 |
| game-of-captains-open-horizon | Captain of the Open Horizon | Vox saved your place at the bar. | `recordKitUnlocks` |
| game-of-captains-last-ship-home | The Last Ship Home | They call you by name. | same |
| game-of-captains-galactic-bargain | The Galactic Bargain | Survival, with a public debt. | same |
| game-of-captains-cost-of-command | The Cost of Command | Your warning outlived you. | same |
| game-of-captains-off-the-record | Off the Record | You found a secret ending. | same, `the-union-cancellation` or `the-witness-coalition` |
| game-of-captains-anthology | Anthology | Six different voyages, six different endings. | same, 6 Kit endings unlocked |
| game-of-captains-first-contact | First Contact, Sort Of | Your first alien species is logged. | `chooseAlienAction` :382 |
| game-of-captains-xenologist | Xenologist | 25 species in the scrapbook. | same, `alienGuide.discovered.length` reaches 25 |
| game-of-captains-field-guide | Galactic Field Guide | All 101 species. | same, reaches 101 |
| game-of-captains-couch-for-two | Couch for Two | Romance in the force bubble. | `chooseRomance` :698, any `invite-*` |
| game-of-captains-print-another | Print Another Me | The clone lab printed a captain. | `clonePrint` :633 |
| game-of-captains-trio | Three's a Crew | You finished a trio adventure. | `chooseTrio` :703 |
| game-of-captains-names-known | Learned Their Names | You remember ten redshirts. | `persist` :496, 10 or more `redshirtKnowledge` entries |
| game-of-captains-high-roller | High Roller | You beat the casino. | `visitVenue('casino', …)` :648 on a win |
| game-of-captains-every-chair | Every Captain's Chair | You finished a voyage with all five captains. | `finish` :723; needs a small cross-run record |

**D) Three PRs**
1. **Achievements and a Kit achievements pane.** Add `catalog/gameOfCaptains.ts`, wire the calls in `gameOfCaptainsStore.ts`, and add the shared `achievements` pane to `components/playbook-kit/playbook-kit-shell.vue` (this also helps MONSTRIQUE and Every Villain Tactics). Add an Achievements button on the title (`game-of-captains.vue:40`).
2. **One settings system.** Remove `preferences` (largeText/reducedMotion) from `gameOfCaptainsStore.ts` and make the title's SETTINGS render `PlaybookKitSettings`, mapping the old keys once. Add confirm-gated reset at the title. Add a version migration in `restoreVoyage` (`rules.ts:1621`).
3. **Plates and voyage pages.** Queue 14 ending plates in `conductor/projects/game-of-captains/art` (auto_submit) and set `painted` true as each lands in `spaceCouch.ts`. Append a record per finished voyage (captain, crew, losses, ending) to a `game-of-captains-voyages-v1` key and show it in the Captain's Log panel. The same record makes "Every Captain's Chair" possible.

**E)** Space Couch is the only one of the four audited games on the Playbook Kit, so the Kit fixes in the shared findings above (achievements pane, music/sound volume) land here first.
