# Zuzu: Shifting Lands — playtest readiness dossier (t-048), 2026-11-14 PT

Prepared for the playtest handoff Silas directed on 2026-11-13 PT ("help wrap up Shifting Lands … Last step is to
flip the project to playtest"). This is the agent-only proof that nothing authored, painted, mapped or tested is missing.
It is not Silas's acceptance: that stays with t-018 (needs-human, creative-approval).

Play: `/play/zuzu-shifting-lands` on kind_robots main. A self-hosted deploy needs Silas's Force Update.

## 1. What a player gets

| Area | State | Evidence |
|---|---|---|
| Travelers | 13 premades and custom travelers (13 species, point-buy stats). Every premade has an identity deed, 4 own cards, 3 own choices on shared cards and 3 own endings: 52 cards, 39 choices, 39 endings. | kind_robots #5125; `verifyShiftingPersonalTravelers` |
| Shared deck | 120 V6 encounter cards over 15 locations in 5 lands, 7 cast cameo cards, 5 major trials with 8 routes each, moral ledger, cross-land echoes, spent deeds, kitchen-sister follower arc. | `verifyShiftingV6`, `V7`, `V8`, `FollowerRecruitmentV9`, `SpentDeeds` |
| Endings | 19 shared endings (10 mark endings, 2 V7 retitles, 7 moral constellations) and 39 personal endings. All 58 are witnessed by a replayable seed and policy. | `verifyShiftingEndingsGraph`; `ENDINGS-GRAPH-2026-11-13.json` |
| Front end | Art-led title screen (Continue, New journey, Scrapbook, Achievements), 13-traveler creator, illustrated board, choice hand, ending reader with plates, persistent scrapbook (13 traveler pages and 19 shared plates). | kind_robots #5127 |
| Progress | Versioned replay saves V2 to V10 with migrations, a personal endings record, a shared endings record and 20 achievements. | `verifyShiftingSaveLedger`, `verifyShiftingScrapbook`, t-051 |
| Voice | Player-facing text is second person. No text or image defaults to Zuzu as the player. Zuzu-featuring plates are filtered from places and strangers' cards. | 2026-11-13 audit; kind_robots #5125 |

## 2. Art bound to UI slots

From `utils/scripts/shiftingLandsArtCoverage.ts`, which enumerates every image slot from the runtime registries:

| Slot | Total | Own painting | Fallback plate | No plate |
|---|---:|---:|---:|---:|
| Shared card faces (V6) | 120 | 120 | 0 | 0 |
| Cast cameo cards | 7 | 1 | 6 | 0 |
| Travelers' own cards | 52 | 52 | 0 | 0 |
| Choice outcomes (success/failure) | 1053 | 532 | 521 | 0 |
| Trial route outcomes | 80 | 54 | 0 | 26 |
| Shared endings | 19 | 19 | 0 | 0 |
| Personal endings | 39 | 39 | 0 | 0 |
| Traveler portraits | 13 | 13 | 0 | 0 |
| Species portraits | 13 | 13 | 0 | 0 |

Notes:
- **Cameo cards:** the 6 fallbacks show Book One plates without Zuzu in them. That is allowed, and the contract test checks it.
- **ROUND-16-RETAKES (2026-11-14 PT, playtest iteration):** shipped the last five plates. Every own card and personal ending now has its own painting.
- **Outcomes and trial routes:** "No plate" means the matrix found neither a consequence plate nor a bespoke card plate. The game still never shows a blank. `outcomePlate` falls back to the played location's art, and `trialPlate` falls back to the land's trial or boss art (`stores/shiftingLandsJourneyStore.ts`).

Every curated plate was checked by eye against its prompt. Rejected: human figures, lettering or pseudo-text, a koala or straw kasa outside Zuzu's own road, wrong species. Ledgers carry the verdicts: ROUND-3, ROUND-7, ROUND-8 to ROUND-15 (ROUND-16 queued) and ENDINGS-STANDARD-ROUND-1. An outcome without its own plate falls back to its card's painting (design, t-028).

## 3. Tests and adversarial play

All run on kind_robots main by the `shifting-lands-gameplay` workflow:

- **Personal travelers:** 2,940 personal journeys. Every own card, choice and ending is reached, replay is exact, travelers never meet themselves, and the legacy V10 digest is pinned.
- **Endings graph:** 24,192 journeys, all 58 endings witnessed, every witness replays exactly. This found and fixed four constellation endings that had been unreachable since V8.
- **Adversarial battery:** 1,176 journeys across 7 policies (kind, ruthless, greedy, cautious, mixed, chaotic, pathological) and 14 travelers.
  - No soft locks.
  - 5,783 junk actions refused without throwing.
  - 2,352 forged saves refused.
  - Balance: kind play wins 74%, cautious 77%, ruthless 32%. Every traveler wins 58–96% of kind or careful journeys.
- **Other contracts:** character creator (14 travelers × 500 seeds × 15 locations, no self-encounter), scene-art contract, board, trials, V4 to V8 contracts, scrapbook.
- **Visual QA (t-047):** title, creator, mid-road own card, personal ending and scrapbook at 390, 768, 1440 and 1920 px. No horizontal overflow, no page errors, 14 traveler options at every width.

## 4. Roadmap reconciliation

| Task | Outcome |
|---|---|
| t-053 Personalize every premade traveler | done: 13 roads, kind_robots #5125 to #5144 |
| t-029 Art round 3 (twice-missed consequence plates) | done: superseded by ROUND-7 and ROUND-12 outcome rounds (586 outcome plates ship) |
| t-033 Art round 4 (the 72 new cards) | done: 120/120 shared card faces painted |
| t-024 Verify prose, dice, flips, art and replay | done: gameplay workflow plus endings graph |
| t-044 Scene-to-image coverage | done: `shiftingLandsArtCoverage.ts` matrix (section 2) |
| t-017 Seed/property playtests and balance | done: adversarial battery and balance report (section 3) |
| t-046 Adversarial end-to-end battery | done: section 3 |
| t-047 Visual QA at four widths | done: section 3 |
| t-048 This dossier | done |
| t-018 Silas's creative approval | needs-human (creative-approval). Playtest feedback goes here. |
| t-004, t-012, t-014 | cancelled by Silas 2026-11-13 PT |
| t-002, t-043, t-045, t-050 | done (conductor #7351) |

## 5. Known limits for the playtest (not blockers)

- Settings are presentation only: motion and dice sound. There is no volume, text-size or reset-all control (main-game standard "Settings": Partial).
- Saves are per browser (localStorage). There is no account-backed save.
- Hester Kell and Augustin are provisional names. Some family names were invented for the new roads (Tamsin's Corran, Wenna and Pip; Augustin's Madam Ferrule and Nell; Mags's son Lark).
- Several dark personal endings turn on betraying a child: Hester's writ, Wren's kit, the Coyote's runaways, Gideon's three names. Harm is kept off-screen per the world guardrails. This tone is for Silas to judge at t-018.
- Outcome plates fall back to card art where no consequence plate passed curation.
