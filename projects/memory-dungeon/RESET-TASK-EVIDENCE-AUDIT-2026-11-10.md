# Memory Dungeon reset-task evidence audit (2026-11-10 PT)

Scope: the **24 unfinished tasks** released by the twelve-world reset, excluding the new audit task t-065. This is a source-evidence review, **not** an end-to-end playtest or a completion certificate. Source of truth: CONTROL.md's twelve-world cap and TWELVE-WORLD-DELIVERY-ROADMAP.md. Old e13–e16 remain save archives only.

## Method and interpretation

Queried merged pull requests in `silasfelinus/kind_robots` and `silasfelinus/conductor` for Memory Dungeon, Briar, Hoshimori and Last Train. Inspected changed-file patches for kind_robots PRs #4959, #4957, #4869, #4839, #4807, #4894, #4531, #4540, #4860, #4911, #4821 and #4722. A merged PR proves that a **slice** exists in main, not that the task's complete acceptance criteria or production art have been verified. The reset has **24** unfinished tasks, despite t-065's older note saying 21. None of these 24 should be automatically marked done from title matches alone.

| Task | Confirmed merged evidence (selected PRs) | Remaining acceptance / next action |
| --- | --- | --- |
| t-001 expedition reducer | [#4894](https://github.com/silasfelinus/kind_robots/pull/4894) seeded three-floor simulator and tests; [#4801](https://github.com/silasfelinus/kind_robots/pull/4801) interrupted-bout reload | Verify complete reducer, Classic adapter and all save/restore flows; simulator alone is insufficient. |
| t-007 RPG combat masks | [#4896](https://github.com/silasfelinus/kind_robots/pull/4896) 640 seeded combat-room oracle replays | Verify live combat-mask UI, enemy telegraphs and player-facing behavior; test coverage is not full acceptance. |
| t-009 story and cast | [#4530](https://github.com/silasfelinus/kind_robots/pull/4530) Vesper childhood; [#4577](https://github.com/silasfelinus/kind_robots/pull/4577) Char agency | Audit twelve-world continuity, companion consequences and interstitials. |
| t-013 art pipeline | [#4860](https://github.com/silasfelinus/kind_robots/pull/4860) authored-choice and collectible manifest checks | No verified durable ArtJob IDs, delivered ArtImages or per-world coverage in this audit; require delivery evidence. |
| t-019 screen mockups | No matching delivered visual artifact verified in inspected patches | Locate actual five scene-family mockups and compare with implemented UI. |
| t-020 twelve-world canon | [#4531](https://github.com/silasfelinus/kind_robots/pull/4531) campaign and persistence | Verify intro/prologue and legacy e13–e16 archival saves, never treat old 16-world routing as current. |
| t-023 Chronicle | [#4442](https://github.com/silasfelinus/kind_robots/pull/4442) Briar photographs; [#4482](https://github.com/silasfelinus/kind_robots/pull/4482) Hoshimori first photo | Audit 24 playable-world beats, retired archival beats and spoiler gates; do not delete older photos. |
| t-025 Act I maps/dungeons | [#4177](https://github.com/silasfelinus/kind_robots/pull/4177) Dark Briar; [#4180](https://github.com/silasfelinus/kind_robots/pull/4180) 64 Dark Briar sites; [#4189](https://github.com/silasfelinus/kind_robots/pull/4189) House | Cross-check each of e01/e02 64 authored sites, linked dungeons, transitions and tests before closeout. |
| t-029 economy | [#4429](https://github.com/silasfelinus/kind_robots/pull/4429) replay-safe earned loot | Verify full enemy, item, achievement, unlock, and balancing matrices. |
| t-030 art manifest | [#4860](https://github.com/silasfelinus/kind_robots/pull/4860) art-manifest validation | Twelve-world 30+2 galleries, ArtJob queue IDs and delivered images still need per-world verification. |
| t-034 World One console | [#4379](https://github.com/silasfelinus/kind_robots/pull/4379) map art and choice controls; [#4681](https://github.com/silasfelinus/kind_robots/pull/4681) smaller beacons | Confirm rendered single-screen 390/768/1440 UI, save slots and end-to-end World One acceptance. |
| t-037 consequence ledger | [#4531](https://github.com/silasfelinus/kind_robots/pull/4531) campaign persistence; [#4578](https://github.com/silasfelinus/kind_robots/pull/4578) earned fragments | Prove bounded replay-backed cross-world outcomes and restoration. |
| t-038 story bible | [conductor #7145](https://github.com/silasfelinus/conductor/pull/7145) e12 writer packet; [kind_robots #4531](https://github.com/silasfelinus/kind_robots/pull/4531) finale foundation | Reconcile narrative bible against 12-world canon, final POV and Char causality. |
| t-039 Forge prompt repair | [#4911](https://github.com/silasfelinus/kind_robots/pull/4911) completeness reflects actual prompts | Re-run missing/failing prompt inventory; no proof all 195 failures and six missing prompts are resolved. |
| t-040 painted House floorplans | [#4189](https://github.com/silasfelinus/kind_robots/pull/4189) playable House map | Gameplay geometry is not painted art; require delivered 6×6 floorplan images and visual acceptance. |
| t-044 e08 64 sites/dungeon | [#4869](https://github.com/silasfelinus/kind_robots/pull/4869) two night crossings; [#4839](https://github.com/silasfelinus/kind_robots/pull/4839) Furnace of Names dungeon; [#4700](https://github.com/silasfelinus/kind_robots/pull/4700) four nightmare encounters | Verify 64 distinct authored e08 sites, 36-room dungeon, consequences, Vesper POV, full route. |
| t-045 Hoshimori art | [#4839](https://github.com/silasfelinus/kind_robots/pull/4839) playable dungeon implementation | No verified delivered style proofs, 2×(30+2) collectible galleries or atlas ArtJob IDs. |
| t-047 collision finale | [#4531](https://github.com/silasfelinus/kind_robots/pull/4531) campaign reducer; [#4821](https://github.com/silasfelinus/kind_robots/pull/4821) e09 scenes | Prove four *playable* 64-site maps, four dungeons, 8 fragments, 32 reachable core endings; reducer != playable campaign. |
| t-049 zero-image character decks | [#4807](https://github.com/silasfelinus/kind_robots/pull/4807) lazy batched linked-art source and regression tests | Verify character with existing art displays actual matches in live UI, including no-art fallback and saved deck. |
| t-051 Briar pacing | [#4722](https://github.com/silasfelinus/kind_robots/pull/4722) instant discoveries; [#4785](https://github.com/silasfelinus/kind_robots/pull/4785) one-beat House lore rooms | Independent 64-site/36-room pacing run, choice density and fun acceptance. |
| t-055 Vesper e08 rewrite | [#4530](https://github.com/silasfelinus/kind_robots/pull/4530) Vesper origin; [#4869](https://github.com/silasfelinus/kind_robots/pull/4869) night crossings | Audit every authored night site for Vesper's POV, original horror and earned consequences. |
| t-057 e09 Rowan/Pip | [#4821](https://github.com/silasfelinus/kind_robots/pull/4821) e09 Rowan scenes; [#4811](https://github.com/silasfelinus/kind_robots/pull/4811) Rowan callbacks | Verify playable Rowan-led e09 route, Pip companion, earned memory fragments, ending callbacks. |
| t-063 Choking Works browser | [#4835](https://github.com/silasfelinus/kind_robots/pull/4835) dungeon implementation | Actual rendered button click, measured layout at 390/820/1440, mid-dungeon save/restore still required. |
| t-064 Earth letters/Last Train | [#4957](https://github.com/silasfelinus/kind_robots/pull/4957) Pinia Earth letters; [#4959](https://github.com/silasfelinus/kind_robots/pull/4959) Last Train reducer | **Highest-value immediate code gap:** bind Last Train to actual e03/e04 encounters and replay-validated reachability; reject forged/out-of-order saved decisions. |

## Cross-world acceptance matrix

| Worlds | Evidence in this audit | Acceptance status |
| --- | --- | --- |
| e01–e02 | Briar/Dark Briar, House, Chronicle and pacing PRs | Partial: 64-site, dungeon, delivered-art and visual end-to-end proof still needed. |
| e03–e04 | Earth letters Pinia + Last Train reducer | Partial: Last Train encounter binding/reachability and art still needed. |
| e05–e06 | Choking Works dungeon PR and earlier sea chapter PRs | Partial: rendered dungeon entry and Scylla/Char causality acceptance needed. |
| e07–e08 | Warm Hoshimori and nightmare sites, Furnace of Names | Partial: e08 64-site audit, Vesper continuity, galleries and art. |
| e09–e12 | Campaign persistence and e09/e12 narrative packets | Partial: four fully playable 64-site maps/dungeons, fragments and ending routes unverified. |

## Audit disposition

- **0 of 24 tasks closed**: title-matching PRs do not establish complete task acceptance. Leave all 24 available for fresh claims rather than falsely declaring them done.
- **No art jobs submitted** by this audit, and no claim that prompt manifests represent delivered images.
- This is an **evidence-backed gap ledger**, not executed adversarial gameplay or a UI screenshot review.
- Next: claim t-064 for executable Last Train binding and forged-history tests; t-044/t-055 for e08 completion; t-047 for playable collision maps. Separately track actual ArtJob IDs for t-013/t-030/t-045.
