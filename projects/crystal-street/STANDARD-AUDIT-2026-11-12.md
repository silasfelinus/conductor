# Terrors on Crystal Street — main-game standard audit (2026-11-12, kind_robots 7ad1136)

This was a read-only audit of kind_robots at `origin/main` 7ad1136 and the conductor repo. Live records come from `https://kindrobots.org/api/achievements`, which has 145 records. Paths below are relative to `/home/user/kind_robots` unless they start with `conductor/`.

## Shared plumbing to know first

**How game achievements are wired:**
- **Definitions** live in `utils/achievements/catalog/games.ts`. The game must also be listed in `OTHER_GAMES` in `utils/achievements/gameAchievements.ts:78-136`.
- **Sections:** `AchievementSectionKey` (`gameAchievements.ts:14-15`) only allows site, arcade, zuzu, shifting-desks and emperor-of-dust. Ecotone, Memory Dungeon and Crystal Street each need a new section or have to reuse one.
- **Test rules** (`utils/scripts/verifyGameAchievements.test.ts`) apply to every entry:
  - label of 32 characters or fewer, plus a tooltip and a subtleHint
  - an art prompt of at least 30 words
  - an icon that exists in `assets/icons`
  - non-arcade games must use `rule: event`
  - the code must appear as a literal string in components, stores, pages or utils
- **Records:** `scripts/seed_achievements.ts` upserts them by triggerCode. You can also use admin `POST /api/achievements/batch`.
- **Display:** the strip only shows for games in `ACHIEVEMENT_GAMES`, through the workspace sheet's route match (`components/navigation/workspace-sheet.vue:176`). No game renders it inside its own UI yet.
- The header comment "three per game" in `gameAchievements.ts:3` is out of date.

---

## Terrors on Crystal Street (`/play/crystal-street`)

### A) Audit

| Item | Status | Evidence | Gap to close |
|---|---|---|---|
| Title screen | Partial | `components/crystal-street/crystal-street-title.vue:48-102`: Continue the week, New week (4-step creator), Scrapbook, Settings, Theme. | An Achievements entry. |
| Settings | Partial | `stores/crystalStreetStore.ts:41-56` and `crystal-street-settings.vue`: text size S/M/L, contrast normal/high, motion full/reduced, tips, sound on/off. Reset tips, abandon week, and reset scrapbook with an armed confirmation (`:172-193`). Reachable from the title and the dial. | A volume level (sound is on/off only) and reading speed. |
| Save / load | Partial (local is Met) | Keys `crystal-street-run-v1`, `crystal-street-scrapbook-v1`, `crystal-street-settings-v1`, `crystal-street-tips-v1` (store `:35-38`). `SCHEMA_VERSION = 1` plus `repairRun` (`rules.ts:64`). Continue works after reload. | No account-backed save. |
| 12+ achievements | Missing | 0 live. | All of it. |
| Scrapbook | Met (one caveat) | Tabs for weeks, nightmares, endings and friends (`utils/crystalStreet/menu.ts`). Per-run pages with crew, clues, wins and highlights (store `ScrapbookRun`, 80 kept). The endings wall uses "???" (`crystal-street-endings.vue:45-123`). | Caveat below the table. |
| Endings | Partial | 23 villains × 4 tiers (best, good, bittersweet, bad) gives 92 endings, plus 4 specials (3 faction collapses and the Final Girl), for 96, each with its own text. Art: one `villains/<id>-ending.webp` per villain, shared by all 4 tiers (`crystal-street-ending.vue:12-15`), plus 4 special plates. `artPrompts.ts:76` already defines `endings/<villain>-<tier>`, but only counselor-jess has them, and the component doesn't use them. | Per-tier plates: 88 to queue. Wire the per-tier path with a fallback. |
| Characters | Met | Name, pronouns, 16 avatars, 6 archetypes with 6-skill spreads (`rules.ts:76-125`). | None. |
| Replay hooks | Met | 23 villains (random or chosen), seeds, 22 companions with 3-step arcs, items, Final Girl and faction endings, the scrapbook. | None. |

**Caveat: an earlier Silas decision conflicts with the new standard.** On 2026-10-24 PT Silas decided the nightmares and friends lists show only what the player has met (`crystal-street-villain-list.vue:57`, `crystal-street-crew.vue:197`). The new standard asks for locked silhouettes with "X of N". At minimum, add the counts. Whether to add silhouettes is Silas's call.

### B) Character customization

Already there (name, pronouns, 16 avatars, 6 archetypes with stat spreads) and well suited to the genre. No change proposed.

### C) Proposed achievements (15, prefix `crystal-street-`)

Hook point: `commit(next)` in `stores/crystalStreetStore.ts:264`, diffing the previous run against `next`. Scrapbook-based achievements check after `record()`.

1. `first-week` "Made It to Sunday": `next.ending` set for the first time.
2. `best-ending` "Happily Ever After": ending tier `best`.
3. `final-girl` "Final Girl": `ending.special === 'final-girl'`.
4. `burned-bridges` "Nobody's Side": a faction-collapse special.
5. `full-crew` "Full Crew": `recruitedIn(next).length >= 3`.
6. `arc-complete` "Friend for Life": a new `arc:<id>:3` flag (`rules.ts:980`).
7. `twelve-wins` "Twelve Wins": `next.wins >= BEST_WINS` (12).
8. `second-chance` "Second Chance": the pending roll has `rerolled` and succeeds.
9. `case-cracked` "Case Cracked": the week holds every clue for its villain.
10. `five-nightmares` "Five Nightmares": `metVillains.size >= 5`.
11. `all-nightmares` "Street of Terrors": all 23 villains met.
12. `best-five` "Five Best Weeks": `bestFound >= 5`.
13. `every-clique` "Every Clique": scrapbook runs cover all 6 archetypes.
14. `ten-friends` "Ten Friends": `scrapbook.friends.length >= 10`.
15. `shopper` "Mall Rat": `buy()` 3 items in one week (`rules.ts:1234`).

### D) Three smallest high-value PRs

1. **Achievements.** Edit `catalog/games.ts` and `gameAchievements.ts` (add a game and section), add the award diff in `crystalStreetStore.commit`, and add an Achievements entry to the title (`crystal-street-title.vue`, `menu.ts`).
2. **Per-tier ending plates.**
   - In `crystal-street-ending.vue:12-15` and the endings wall, use `/crystal-street/endings/<villain>-<tier>.webp`, falling back to the villain plate.
   - Queue the 88 missing plates through the conductor ledger (auto_submit), using the existing `artPrompts.ts` keys.
3. **Settings completion.** Add a volume slider (`utils/crystalStreet/sound.ts` plus a `volume` setting), a reading-speed setting, and "X of N" counts on the nightmares and friends tabs.

---

## E) Shared and reusable components

- **Playbook Kit** (`components/playbook-kit/*`, `stores/playbookKitStore.ts`, `utils/playbookKit/settings.ts`):
  - settings for text size, font, contrast, motion, text speed, sound, trailer and romance
  - scrapbook, endings, secrets, cast and trailer panes
  - one versioned localStorage record per game
  - Used by Monstrique, Game of Captains and Every Villain Tactics. It's the closest thing to a standard settings panel, scrapbook and title console. Its settings pane could be lifted for Shifting Lands and Memory Dungeon.
- **Crystal Street's** title / settings / scrapbook / endings set (`components/crystal-street/*`) is the most complete per-game example: armed-confirm reset and the "???" endings wall.
- **3-slot saves with export/import:** Ecotone (`stores/ecotoneStore.ts:261-330`) and Memory Dungeon (`utils/memoryDungeon/saveSlots.ts`). They follow the same pattern and could share a helper.
- **`components/achievements/game-achievement-strip.vue`** is reusable, but nobody mounts it inside a game today.
- **`PlaybookRunReview`** (`stores/playbookRunReviewStore.ts`) is a per-run feedback form, not a scrapbook. Don't count it toward item 5.
