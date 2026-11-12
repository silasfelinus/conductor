# Memory Dungeon main-game standard: initial evidence audit (2026-11-11 PT)

Scope: `/play/memory`, source inspection only. This is a **gap audit**, not a claim of browser QA, delivered production art, account-backed persistence, or final acceptance. Source-of-truth: `docs/agents/main-game-standard.md`. All status judgments below are conservative.

| Requirement | Status | Evidence and acceptance gap |
| --- | --- | --- |
| Title console with New Game, Continue, Settings, Scrapbook, Achievements | **Partial** | `components/pages/memory-dungeon.vue` launches through `memory-dungeon-launcher` and supports Classic/RPG entry. A single title console with all five standard actions is not verified. |
| Persistent settings (audio, text speed/size, motion, contrast, confirmed reset) | **Partial** | `components/pages/memory-dungeon.vue` contains settings/reset references, but full accessible title/in-run controls, all preference categories, and reload persistence are unverified. |
| Versioned autosave, exact Continue, permanent unlocks, account-backed save | **Partial** | `stores/memoryWorldStore.ts` has save and Chronicle logic; `stores/memoryHoshimoriStore.ts` and `stores/memoryHoshimoriNightStore.ts` use versioned local keys. Signed-in account restoration and exact mid-encounter resume remain unverified. |
| 12+ live site achievements, awarded and surfaced | **Missing** | `utils/memoryDungeon/achievements.ts`, `utils/memoryDungeon/earthAchievements.ts` and `components/memory-dungeon/quest-log.vue` provide **local story medals**; these are not evidence of 12 live `Achievement` records with prefixed trigger codes and `game-achievement-strip.vue`. Dedicated t-069 owns implementation. |
| Persistent scrapbook: endings, characters, art, finished-run pages, locked silhouettes | **Partial** | `stores/memoryWorldStore.ts` tracks gallery/Chronicle; `components/memory-dungeon/quest-log.vue` has locked medals. No unified scrapbook covering endings, cast and per-run history was verified. |
| Several earned endings, each with a delivered painted plate | **Partial** | `stores/memoryWorldStore.ts` contains ending logic, but exhaustive ending traversal and distinct rendered ending plates have not been established. Production ArtJob IDs and integration verification required. |
| Customizable protagonist and reactive story | **Missing / unverified** | The launcher and root component inspection did not establish a character creator. This genre supports customization; do **not** assume an exception. Audit the existing character flow before implementation. |
| At least three replay hooks | **Partial** | Seeded encounters, branching choices and gallery/Chronicle collectibles are represented by `stores/memoryWorldStore.ts` and world-specific stores. Verify these survive new games and meaningfully alter replay before marking Met. |

## Prioritized implementation slices

1. **Title and navigation contract:** inventory the launcher and in-run menu; make all five title actions reachable without duplicating console chrome. Add route/component contract tests and 390/768/1440 visual QA.
2. **Persistent settings and safe reset:** centralize preference persistence, confirm destructive reset, and add reload tests.
3. **Scrapbook acceptance:** integrate earned endings, encountered characters, unlocked art and per-run summaries with locked counts, preserving existing Chronicle and gallery IDs.
4. **Character creation:** provide name/appearance/stat choices and authored acknowledgment without breaking versioned saves.
5. **Ending-art inventory:** map each reachable ending to distinct production ArtJob and verified ArtImage; queue missing work in an `auto_submit` ledger and test rendered fallback.
6. **Achievement records:** coordinate with t-069, which owns live API creation and award verification; do not count in-game medals as live site achievements.

## Verification ledger

- Read: Conductor `docs/agents/main-game-standard.md`, Memory Dungeon roadmap t-068/t-069, Kind Robots `components/pages/memory-dungeon.vue`, `components/memory-dungeon/quest-log.vue`, `stores/memoryWorldStore.ts`, and indexed achievement/store files.
- No automated test, live API award, browser rendering, ArtJob submission, or deployment was executed as part of this audit.
- Canon: twelve **playable** overworlds e01–e12, with e13–e16 retained only for compatibility per current CONTROL/roadmap supersession; preserve legacy identifiers.
- **Do not mark For Human Gate** until every item is independently verified and all world-specific production expectations are satisfied.
