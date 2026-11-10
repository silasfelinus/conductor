# Memory Dungeon: twelve-world delivery roadmap
Updated: 2026-11-10 PT. Source of truth: CONTROL.md's October 30 twelve-world canon.

## Production contract
- Exactly **12 playable 8×8 overworlds**, e01–e12, **64 distinct reachable authored coordinates each** (768 sites total).
- e01/e02 Briar original/twisted, e03/e04 Morrow Earth original/twisted, e05/e06 Scylla shore/undersea original/twisted, e07/e08 Vesper Hoshimori warm/yōkai horror. e09/e10/e11/e12 return to established geographies as cross-world collisions, with playable Pip/Morrow/Char/Vesper respectively.
- One meaningful geographically anchored dungeon per overworld, including route variety, shortcuts, rewards, optional resolutions and save/restore; validate exact room counts against each world design (36 rooms where specified), not a generic copied dungeon.
- Each world has a 30-local + 2 cross-realm illustrated collectible gallery (384 face slots overall), unlocks and replay access. All imagery must be traceable ArtJobs with verified delivered ArtImages and attachments, not prompt-only or placeholder-only coverage.
- Preserve Classic Match, existing IDs, prior saves, and archival e13–e16 records. Do not route new players into e13–e16 or count archival entries toward the twelve.
- The earlier 32-photo Chronicle remains valid historical data; playable e01–e12 should expose only their 24 chronological beats, with future/retired entries archived and spoiler-safe. No destructive save rewrite.
- Approximately 32 **distinct playable core endings** from four earlier pair hinges and a final choice, with conditional Char agency, e10/e12 crossroads, Scylla departure epilogues and replay verification. An ending title or reducer alone is not a playable ending.
- Each playable scene must have clear narrative, meaningful consequences, one-screen art-first console presentation, accessible controls and independent adversarial coverage.

## Release gates by tranche
| Tranche | Worlds | Work needed | Acceptance |
| --- | --- | --- | --- |
| 1. Vertical slice | e01–e02 | Reconcile protagonist/Pip canon, 64-site maps, House/paired dungeon, intro, story beats, Chronicle, art, 30+2 galleries | Both full seeded routes, alternate resolutions, reloads, mobile/tablet/desktop UI |
| 2. Earth | e03–e04 | Complete authored maps/dungeons, Unsent Letters and Last Train playable bindings, reachability validation, gallery/art | Both routes and all scene choices, restore/forgery tests, visible art |
| 3. Mermaid | e05–e06 | Full map/dungeon traversal, Scylla/Char causality, Choking Works live click, art and gallery | Three-way departure, save/restore, rendered 390/820/1440 checks |
| 4. Hoshimori | e07–e08 | Vesper origin and accountability, yōkai mirror, 64-site e08, oven dungeon, art and gallery | Vesper POV, distinct endings, full paired routes and visual tests |
| 5. Collision finale | e09–e12 | Four genuinely playable 64-site collision maps and linked dungeons, displaced fragments, cross-world consequences, character POV, endings | 256 sites, four dungeons, 8 fragments, ~32 complete reachable ending routes |
| 6. Whole-game QA | e01–e12 | Gallery/ArtJob delivery audit, 768-site validator, all routes, balanced combat, accessibility, save migration | Independent seeded playthrough matrix, no blockers, human visual/design verdict only after complete |

## Task coordination reset
All stale unfinished `claimed` and `review` entries from before this session are released to `ready`, except those whose declared prerequisite is not `done` which become `waiting`. Completed tasks stay `done`; human gates stay gated. This is Silas-authorized queue recovery, not evidence old work is complete. Historical notes and claim audit trails in HISTORY remain unchanged. New workers must claim freshly, obey 90-minute expiry, and avoid duplicate open PRs.

## Immediate work order
1. Audit merged PRs for every reset task and close only proven-complete scope; do not reimplement finished code.
2. Complete t-064 Last Train registry/Pinia integration and adversarial reachability tests; t-044/t-055 e08 content; t-047 e09–e12 authored map/dungeon coverage. Keep tasks small enough for focused PRs.
3. Move t-030/t-013 art production from manifests to real queued/delivered ArtJobs, then t-033/t-035 and world galleries. Track job IDs, final URLs and missing coverage.
4. Reconcile t-023 Chronicle against twelve playable worlds without deleting archival records; complete ending and transition reachability.
5. Execute tranche-by-tranche adversarial runs, UI geometry checks and final twelve-world acceptance before marking the project ready for Silas.

## Definition of done
No acceptance based solely on YAML `done` statuses. Require executable 12×64 coordinate coverage, all 12 dungeons, transitions, character arcs, meaningful endings, delivered production art and galleries, save/backward compatibility, and passing tests at 390/768/1440 before the final human gate. No deployment or publication is authorized by this roadmap.
