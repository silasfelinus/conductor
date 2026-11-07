# memory-dungeon — task history archive

Full `note:` prose for completed memory-dungeon tasks, moved out of `roadmap.yaml` so the
Kind Robots projection payload (`scripts/sync_kind_robots_projection.py`, hard limit
4,000,000 bytes) stays well clear of its ceiling. See conductor/t-158.

Each note below is the **verbatim** original — nothing is summarized or trimmed. The
`roadmap.yaml` task keeps its own first sentence plus a pointer here. The HTML comment
markers delimit each note exactly; `archive_done_task_notes.py --verify-only` re-extracts
every note and checks it byte-for-byte against what the roadmap recorded.

## t-006 — Spatial weapon combat specification and shape-playtest prototype

<!-- note:begin t-006 -->
Use COMBAT-PATTERNS.md. Test targetable two-cell vertical sword, three-cell diagonal hammer, cross and precision tools on 4x4, 4x6 and 6x6 boards. Define reveal-vs-match-vs-damage, cooldown and Focus costs, edge clipping/rotation, enemy intent and accessibility. Validate that a wider reveal isn't always optimal and that memory placement remains the deciding skill. Build pure engine plus adversarial tests before visual polish.

Pure engine and adversarial contract merged in kind_robots#4047 (utils/memoryDungeon/combat.ts, verifyMemoryDungeonCombat.test.ts, wired into contract shard 4). Twinblade, Hammer, Spear, Staff, Lantern and Rapier masks with rotation, bullseyes and no silent clipping; Focus, cooldowns, 2-pair strike cap, Guard, stagger, telegraphed tempo and redeal. 200-seed simulations on 4x4/4x6/6x6: memory wins 100%, 60% memory 86-100%, blind 0-6%, wide-shape spray 37%/6%/0%; aiming shapes at remembered pairs is fastest. Twinblade no-pair Guard broke the economy and is now earned by a hit. Results and the accessibility contract for t-007 are in COMBAT-PATTERNS.md.
<!-- note:end t-006 -->

## t-016 — Build bullseye sweet spots and solver-verified minefield challenge floors

<!-- note:begin t-016 -->
Implement visible sweet-spot cell(s) per weapon mask: a correctly remembered match at the bullseye earns crit/stun/guard effect, not automatic matching. Prototype rare 8x8/10x10 Minesweeper-like challenge rooms with clue numbers, flags, hazard-safe route goals, zoomable bounded grid, and exact disarm footprints. Require an algorithmic no-mandatory-guess solvability check across seeds, fair recoverable failure, and full keyboard/screen-reader support. See COMBAT-PATTERNS.md. Integrate after spatial rules proven.

Engine half merged in kind_robots#4050 (guess-free 8x8/10x10 floors, provenCells hints, exact disarms); bullseye crits live in combat.ts. Floor UI next.

Engine merged in kind_robots#4050 (utils/memoryDungeon/minefield.ts): seeded 8x8/10x10 floors kept only when a deduction solver clears them with no forced guess (40-46% of draws redrawn), recoverable missteps, exact one-cell disarms, provenCells hints from visible state, leak-free screen-reader text. Bullseye crits are live in combat.ts (+2 on a sweet-spot pair). Remaining for done: the floor UI (zoomable bounded grid, keyboard map) and a site on the map that opens it.

Built the playable Minefield Archive UI as an optional side chamber of Briar Three Quiet Stones (2,7), unlocked after solving the existing leaf-leaf-sun puzzle. Includes the proven guess-free engine's 8x8 and later 10x10 floors, exact-cell disarms, clue-preserving flags, paid non-leaking lantern hints, zoomable one-screen game-board, touch and keyboard navigation, deterministic replay/safe save migration, once-only rewards and new tests. Kind Robots PR follows; hold for CI, merge and final review. Artwork render acceptance stays separate.

Completed and merged playable minefield archive t-016 in Kind Robots PR #4197 at squash commit 9a1c0a09224443dd6dfff306a79e4c88befc55f1; all 14 required workflows green, including TypeScript, full contract tests and changed-file Prettier. Three Quiet Stones at 2,7 now opens 8x8 and later 10x10 solver-verified no-mandatory-guess archive floors, with touch/keyboard tools, zoom, exact cell disarms, non-leaking lantern hints, recoverable failure, versioned move-replay save/resume and once-only progression rewards. Existing rune quest, Briar save IDs, main exploration, Dark Briar and Classic remain intact. Browser device-width visual checks and image delivery still require separate acceptance; final game release and human gate remain closed.
<!-- note:end t-016 -->

## t-017 — Define fixed fantasy overworld coordinate contract and modular lore boundaries

<!-- note:begin t-017 -->
WORLD-AND-EXPLORATION.md is authoritative over initial linear-rooms pitch. Define geographically stable coordinates, terrain and fog, discoverable site IDs, portal ancestry, terrain-rune sequence rules, overworld-vs-combat state machine, geography-safe procedural expansions, and future worldbuilder interoperability. World name/cosmology/cast are deliberately not fixed: this is a special dungeon in a not-yet-created original comic fantasy universe.

Completed fixed starter-region geography and world/character/run/Chronicle design deliverable in projects/memory-dungeon/STARTER-REGION-DESIGN.md. Includes 11x11 map with reachable roads, authored landmarks, gated paths, thematic puzzle families, reset thresholds, find-the-difference, five earned tools, anchored procedural chambers and future art shot list. Submitted as a scoped Conductor document PR; no concept art requested yet.

Merged silasfelinus/conductor#6499 as the first-region implementable design. Draft covers the fixed 11x11 overworld, themed sublevels, geometric combat, reset and difference rooms, progression tools, durable save layers and future art-direction inventory. All PR checks passed, including full 2,939+ test suite. No app or art implementation happened in this document-only task.
<!-- note:end t-017 -->

## t-018 — Build playable overworld reveal/explore and nested encounter transition

<!-- note:begin t-018 -->
On the EXISTING /play/memory stage, ship the first small static world with terrain revelation, named anchor sites and stateful return. Opening an encounter switches the same game camera into match combat, treasure/puzzle or dialogue; on resolution the player returns to exactly the same world position. Include a paired terrain-sequence secret and one procedural dungeon instance anchored to the map. Autosave world and run state across reload.

First Briar Camp vertical slice implemented on Kind Robots worker branch: fixed 8x8 authored map, progressive 1-2-square frontier, merchant, chests, clue/puzzle, optional duels, two gallery-image match rooms in Rootbound Vault, one-run total two-card attempt counter, Bramble Chime and eastern gate payoff, and versioned browser save/resume. Preserved existing /play/memory Classic Match. Art is clean SVG underlay without baked cards or hero. Submitted for PR CI; no production deployment or Page 02 promised.

kind_robots#4044 merged 2026-10-23T00:39Z (merge recorded under silasfelinus): Briar Camp 8x8 overworld with progressive reveal, named sites, Rootbound Vault gallery-image match rooms, Bramble Chime and east-gate payoff, versioned browser save/resume, and one shared deck launcher for Classic Match and the RPG. Classic Match preserved; verifyMemoryWorld.test.ts in contract CI. No production deploy claimed.
<!-- note:end t-018 -->

## t-021 — Implement Briar Marches 64-square authored map and reachable graph

<!-- note:begin t-021 -->
Convert all 64 stable 1..8 coordinates in BRIAR-MARCHES-FIRST-WORLD.md to distinct interactive authored scene/site records. Expand BRIAR_LINKS only with adjacent, bidirectionally reachable routes while preserving current fixed sites, choice states and saved progression. Each tile must reward interacting, have unique atmosphere/art contract and a consequence or discovered fact; remove generic no-op squares. Deliver in tested batches (16 cells per PR acceptable), with scene tests for availability, no duplicate resources or softlocks.

First scoped batch authors 16 reachable and formerly generic Briar encounter sites with two persistent choices each, callbacks, art prompts, and save/reachability regression tests. The remaining 64-location map work is not complete.

First sixteen additional authored Briar scenes merged in kind_robots PR 4091 at 9b0cd4ed7801484ccec61404adb7fbd86b0f3c72, with persistent branch choices, linked callbacks and reachable tile tests. All 12 PR workflows passed including TypeScript, formatting and full contract tests. t-021 remains incomplete: 64 locations still need full authored interaction and every coordinate must become reachable, save-safe and visually checked.

Second scoped Briar map installment on a Kind Robots worker branch: all 64 fixed coordinates connected by legal map paths, 16 additional decision-bearing scenes bringing authored count to 47, and named map markers for story-only sites. Contains save/graph/reaction tests. Full 64-site narrative completion remains outstanding.

Second map batch merged in Kind Robots PR 4098 at 7ae63c06a9e5a4be470e60a0d3911b579fd4d87f. The fixed 8x8 Briar graph now has 64 legal reachable coordinates with at most two new routes per source. Added 16 more authored scene choices, conditional consequences, visual briefs and visible scene map names, bringing the total to 47 scripted sites. All 14 GitHub workflows passed. This remains an incomplete map milestone: 17 locations need additional authored encounters or integration, four cross-world sigils remain intentionally outside the Briar reveal waves, and real art delivery and rendered mobile/tablet/desktop QA are not verified. Continue next with remaining 17 sites and save-safe cross-world unlocks.

Final 17 authored site and sigil locations, two choice outcomes each, persistent fourth-wave regional sigil inspections, and chronological first-world Earth photo Chronicle. All 64 stable coordinates have unique scene writing and illustration briefs. The four cross-world partner seals remain intentionally unresolved until their paired future realms exist. PR validation still required.

Completed 64/64 authored Briar locations, map paths, unique decisions and art prompts with reserved region-sigil inspections, first two chronological Earth photos, save-roundtrip/graph tests, and existing special-site reward compatibility. Merged Kind Robots PR #4121, commit 7a9ac01e4dad24a8a083749a7d79c5e2fd5bf146, with all 14 workflows green. Future-region sigil counterparts and rendered art delivery intentionally await later tasks. Proceed with 36-room House t-022.
<!-- note:end t-021 -->

## t-022 — Build the House That Remembers 36-room dungeon and alternate resolutions

<!-- note:begin t-022 -->
Expand fixed 6,2 Rootbound Vault site to a 6x6, 36-room graph using House design in BRIAR-MARCHES-FIRST-WORLD.md; preserve existing vault-1/vault-2 save IDs, include shortcuts, four exits/ safe loops, clue logic, 2-card matching combat, Warden's optional nonlethal resolution, informed-consent dilemmas and at least three distinct end states. Seed replay, complete graph reachability, failure continuations and save/reload tests required.

First complete playable House prototype on a Kind Robots worker branch: all 36 named rooms with original art briefs, branching room graph, safe loops and conditional shortcuts, persistent choices and loot, optional matching Echo Chamber and fair duels, proof-based Warden negotiation or combat, three documented consent consequences, and once-only Bramble Chime reward. Legacy vault-1/vault-2 save IDs remain accepted. Await CI, merge and rendered visual QA.

Kind Robots PR 4126 merged to main at 25bea52c02ed05d0c2472f2381db6441d4469db9 after all 14 workflows passed. The 36 authored House rooms, conditional shortcuts, save-safe state, fair matching combat, Warden alternatives and three ending consequences are merged. A genuine bug exposing the HD-06 shortcut before discovery was repaired and regression-tested; new files fully formatted. Room ArtJob prompts are not proof of delivered artwork and rendered 390/768/1440 QA or production deployment is not yet verified; keep those in separate art/visual delivery tasks.
<!-- note:end t-022 -->

## t-032 — Add a per-realm manifest validator (duplicate coordinates, unreachable tiles, missing choice outcomes, unmet art needs)

<!-- note:begin t-032 -->
Kaizen from conductor#6561. Parse BRIAR-MARCHES-FIRST-WORLD.md style registries and fail CI on duplicate coordinates, tiles unreachable from the start, sites without a persistent consequence, or art requirements with no ArtJob/placeholder, so later realm PRs stay honest.

Added a reusable runtime realm-manifest validator and CI contract for all 64 Briar sites and 36 House rooms, with malformed graph, choice, persistence and art fixtures. Implementation PR pending tests and review.

Completed reusable runtime content-manifest validation for all 64 Briar locations and 36 House rooms, covering duplicate coordinates/sites, unreachable nodes, choices and persistent outcome keys, scene-specific art briefs and honest pending/queued/delivered ArtJob claims. Broken-manifest regression fixtures are part of the required CI shard. Merged Kind Robots PR #4215 at e680afb0f7749fa7fa282bfa0115b0b11415174f; all 12 PR workflows, including four contract shards, TypeScript and Prettier, completed successfully. This uses executable Kind Robots registries instead of duplicating Conductor's editorial Markdown registry; editorial drift is a separate follow-up. No actual image delivery, visual QA or production deployment was verified.
<!-- note:end t-032 -->

## t-041 — Hoshimori e07 warm folklore: playable 16-site proof, Pip youth thread and first oven rooms

<!-- note:begin t-041 -->
Implement the first tested slice in HOSHIMORI-YOKAI-PAIR.md using existing hearth/e07 machine IDs and current earth-protagonist POV. Provide 16 geographically connected individually authored map sites, a consequential encounter introducing Pip's youth apprenticeship (proposed backstory, verify continuity first), a real offering/lantern puzzle and first reachable oven rooms. Keep e07 photos fixed at 2,3 and 7,5 and retain original alias for saved data. Test fresh game, no-blind-guess route, choice restoration, scene uniqueness and Classic preservation. This is a 16-site increment, NOT a 64-site / 36-room completed world or verified art.

Scoped Hoshimori e07 engine increment: authored a connected 16-site warm village with 32 distinct decisions, seeded three-clue lantern puzzle, alternative bakery passage, three first-oven rooms, Pip apprenticeship testimony, replay-validated save state and 96-seed adversarial contract. Implementation PR and exact-head CI follow. This is a pure engine/authoring proof, not yet connected to /play/memory; full playable UI, 64 sites, 36 rooms, art, Chronicle pickup and final QA remain.

2026-10-30 PT: PR kind_robots#4476 merged at 34e13505633108438fe1da73da06a68b5d5882fe; exact head b70f44e00bcc30871d1c48cf345beaff0ad1778c passed all 14 workflows (Contract #41016983410 including Hoshimori 96-seed verifier, TypeScript #41016983397, formatting #41016983306, Memory browser #41016983326). Sixteen connected authored e07 sites, 32 outcomes, three-clue lantern puzzle, bakery alternate Oven passage, first three Oven rooms, Pip testimony and replay-safe state now merged. No new ArtJobs or deployment. Return READY because this is engine/data only: /play/memory integration, 64 sites/36 rooms, e07 Chronicle pickup, 30+2 art and responsive acceptance remain. Not For Human Gate.

Scoped e07 /play/memory console integration in worker/memory-dungeon-t-041-hoshimori-console-8f72: separate replay-validated browser save, 8x8 exploration grid, authored choices, clue-gated lantern puzzle, three Oven rooms and return controls. e07 entry remains spoiler-gated behind completion of e06, so the current unfinished campaign cannot yet reach it naturally. Focused PR and exact-head CI pending; no new art jobs or deployment.

2026-10-30 12:57 AM PT: Merged kind_robots PR #4477 at squash commit 8e6f33583837fd5ccbd5f290fb1d0ab9d8e2edc0. Exact checked head 360f26f9cf0bde50c1846604998932f3b6cfab23 passed all 15 workflows, including TypeScript #41022519585, four Contract Tests shards #41022519528, Memory Dungeon browser #41022519395, layout #41022519417 and formatting #41022519457. e07 now has a bounded sixteen-site 8x8 console stage inside /play/memory, legal adjacent movement, authored outcomes, replay-validated dedicated browser save, lantern clue sequence and three Red Oven rooms with choice consequence feedback. Route is gated behind earned e06 completion to avoid premature middle-campaign spoilers. No new ArtJobs, no deploy, no rendered visual acceptance. Return READY: e03-e06 are not yet playable, e07's two fixed Chronicle photos are not integrated, and the remaining 48 sites, 33 rooms, 30+2 gallery, real scene art and cross-width QA remain. Do not mark For Human Gate.

Scoped Hoshimori e07 Oven hearing: eight authored consequence-backed pantry/ember/hearing outcomes, each reflecting Pip's trace/privacy/absent witness state (24 distinct endings). Added 24 legal-route replay/forged-verdict regression cases. Kind Robots focused PR and exact-head CI follow. Remaining 48 sites, 33 Oven rooms, two Earth-photo pickups, gallery, production art and rendered acceptance are unfinished.

2026-10-30 PT: Merged Kind Robots PR #4480 at 0bb30884e8fe5d1b64cf3097327f7990d38ebc3e after all 14 exact-head workflows passed on 7d5a3f4c76687d3511d98dc0ba9e26ea3438a5eb. Contract Tests #41035724240 (four shards; dedicated Hoshimori warm verifier passed), TypeScript #41035724153, formatting #41035724225, Memory browser #41035724270 and layout #41035724191 succeeded. Eight authored Oven hearing outcomes now combine pantry, ember and hearing decisions with three earned Pip testimony states: 24 distinct replay-validated conclusions. Forged verdict restoration is rejected. No ArtJobs, deployment or visual acceptance. Return READY because e07 still needs two fixed Earth-photo pickups, 48 sites, 33 Oven rooms, 30+2 gallery, production art and device QA. Not For Human Gate.

2026-10-30 PT: Ridge witness increment prepared on Kind Robots worker/memory-dungeon-t-041-ridge-witness-c7e9: eight reachable e07 mountain sites (28 total), sixteen choices, an eight-outcome testimony ledger, and 96-seed/tamper/branch regressions. Await exact-head PR CI before counting as delivered. No art jobs or deployment. t-041's first 16-site proof is met; close after implementation merges and unblock t-042 for the remaining sites, Oven rooms and gallery.

2026-10-30 PT: Merged Kind Robots PR #4503 (f85fc6b91a9092d42e1e373c96991fd6aa3f04f7). Eight new e07 mountain sites bring Hoshimori to 28 reachable authored sites and 56 unique choices. The Ridge Assembly has eight earned, three-decision witness accounts with action-replay restoration and forged-choice rejection. All 21 exact-head checks passed on 51c542d31efa8cd86c802111999ab6bae2675d44, including four Contract Tests shards, TypeScript, formatting, layout and Memory Dungeon browser interruption. Coordination PR #6834 merged (e4ab4415c27413053be1eff822acd418d32e95a8) with 24 successful checks and 2 skips. No new ArtJobs, production deployment or rendered visual acceptance. Keep t-041 READY because the art-led first-stage proof still lacks delivered concept assets and e07 remains naturally gated behind unfinished e03-e06. The remaining 36 sites, 33 Oven rooms, 30+2 gallery and full device QA belong to later milestones.

Scoped Hoshimori e07 adversarial long-run repair: raised the replay-validated action-journal ceiling from 256 to 2048 without changing v1 save IDs, route/choice semantics or photograph gates. Added a 600-move endurance route that then earns both fixed Earth photographs, tests full restoration, tamper rejection and oversized-journal refusal. Kind Robots PR exact-head CI pending. Remaining Hoshimori authored sites, Oven rooms, art delivery, e03-e06 campaign reachability and rendered QA remain open.

2026-10-30 7:09 AM PT: Merged Kind Robots PR #4511 (squash 6753254bf42385beb114c02c0dc1f19a0aafd016) after all 14 exact-head Actions workflows and 19 checks passed on 7812c16e5843df02d2fb42d6824d67f12f338595. Repaired Hoshimori e07's silent action-journal freeze at 256 events by raising the bounded replay-validated ceiling to 2048 without changing v1 save keys or choice/route semantics. New adversarial 600-move route then earns both fixed e07 Earth photographs, verifies restoration, no ration farming, forged-balance rejection and oversized-journal refusal. Contract Tests #41067862636 (four shards and verifier), TypeScript #41067862674, formatting #41067862692, Memory browser #41067862688 and layout #41067862620 passed. No ArtJobs or deployment. Return READY: concept art delivery, e03-e06 reachability, 36 missing e07 sites, 33 Oven rooms, 30+2 gallery and rendered 390/768/1440 QA remain; not For Human Gate.

2026-10-30 PT: Scoped lower-river e07 follow-up on worker/memory-dungeon-t-041-lowlands-b7c83e: eight flood-region sites (36/64), sixteen distinct choices, eight earned lowland council accounts, 96-seed reachability and forged-save checks. Kind Robots PR exact-head CI and merge pending. No ArtJobs, deployment or rendered visual acceptance. Leave the game ACTIVE and the task eligible for remaining concept-art proof after the slice merges.

2026-10-30 8:04 AM PT: Merged Kind Robots PR #4514 at 6cde9da05dbed34850741e608929510b5371617d after 16/16 exact-head workflows passed on 801fd5355931bb3d74b538ea715f7df15c3244c2. Eight lowland scenes bring Hoshimori to 36/64 authored sites and 72 unique outcomes; eight council accounts are earned from three earlier choices with replay/tamper tests. Conductor PR #6845 merged the review transition. Master issue #4136 comment 6525967608 has evidence. No new ArtJobs or deployment. Return READY for first-stage concept art, 28 remaining sites, 33 Oven rooms, 30+2 gallery and rendered acceptance; not For Human Gate.

2026-10-30 PT: Six optional Red Oven ash-wing rooms (OV-04..OV-09) and 64 earned account combinations implemented on worker/memory-dungeon-t-041-ovenwing-f7c2. Existing three-room first hearing and v1 saves remain intact; retreat/reentry and forgery regressions added. Exact-head PR CI and merge still pending. No new ArtJobs, no deployment. Warm e07 still has 36/64 map sites, 9/36 Oven rooms, and no verified 30+2 gallery or style art.

2026-10-30 PT: Merged Kind Robots PR #4515 at 4e5f161c411d7cc9a6e41ed079e59332f7569570. Added six optional Ash Wing rooms OV-04..OV-09, each with two consequence-backed choices and 64 distinct earned account combinations; the first hearing, e07 photo sites, v1 saves and Classic remain intact. Exact head 2ef0f40e33b7e3522d210abb1613e2c9acc41f3e passed all 16 GitHub Actions workflows (Contract #41085096770 all four shards and verifiers, TypeScript #41085096814, formatting #41085096959, Memory browser #41085096694, layout #41085096969). No new ArtJobs, deployment or rendered visual acceptance. Return READY because t-041's concept-art style proof remains unfulfilled; e07 still has 36/64 sites, 9/36 Oven rooms, 30+2 gallery pending and e03-e06 campaign gate unfinished. Not For Human Gate.

Scoped e07 Hoshimori first-stage art proof: eight private Krea2 requests (warm 8x8 map, 6x6 Oven concept atlas, Pip and baker portraits, two yokai, lantern supper scene, Borrowed Hearth collectible sample), with distinct direct-media destinations, receipt audit, regression tests, and early ArtJob-ID checkpoint before long rendering. Production submission, exact-head CI, ArtImage/media delivery and visual acceptance remain to verify.

2026-10-30 9:55 AM PT: Merged Conductor PR #6846 (df61b116cfb7c24640345e737dbf1278ad12405b) after 22 successful and two intentionally skipped exact-head checks on b1ba0223aaf06bef9dd913d5b6106edbc368e487 (Worker CI #41093450555). Auto Art Generate #41093935020 submitted and checkpointed eight distinct private Hoshimori e07 Krea2 style ArtJobs: 52108 map, 52109 Oven atlas, 52110 Pip, 52111 baker, 52112 kitsune, 52113 tanuki, 52114 lantern supper and 52115 Borrowed Hearth card sample. Submission, checkpoint and eight-ID receipt audit steps passed. Issue kind_robots#4136 comment 6528402585 records evidence. These remain pending: ArtImage delivery, media URL HEAD and visual geometry/cast acceptance are unverified; no art attached, no deployment or human gate. Return READY for delivery QA; e07 still has 36/64 sites, 9/36 Oven rooms, 30+2 gallery missing and e03-e06 natural progression blocked.

Scoped Hoshimori e07 live ArtJob/ArtImage/media delivery audit and durable status checkpoint prepared. Eight existing job IDs preserved; exact-head CI and merge pending. This does not establish visual QA or completion of the remaining village, Oven and gallery.

2026-10-30 11:45 AM PT: Reviewed and merged Conductor PR #6847 (squash 137e8bbcff30c793faad6b6eeeb2b3b782312708) after all four exact-head workflows succeeded on 5dc343a9b970bc2b386a3684ced6e42dd213bab3 (Worker CI #41102496433, Security #41102496458, handoff #41102496473, task-events #41102496542). Hoshimori e07 now has a live read-only audit for eight existing ArtJobs 52108-52115, ArtImage associations and fresh media HEAD, plus early durable JSON checkpoint. Auto Art Generate #41109429247 started on the merge. No duplicate jobs, production deploy or art acceptance claimed. Return READY for actual delivery/visual QA and e07 remaining 28 village sites, 27 Oven rooms, 30+2 gallery and e03-e06 campaign reachability. Not For Human Gate.

Windward district e07 scoped increment implemented on worker/memory-dungeon-t-041-windward-4b91f: eight connected authored locations, sixteen persistent decisions, eight earned Windward Council accounts, 96-seed traversal and replay/tamper regression additions. Focused Kind Robots PR and exact-head CI to follow. Existing 8 Hoshimori ArtJobs 52108-52115 remain pending delivery; no new art jobs, deployment or human gate.

2026-10-30 1:01 PM PT: Merged Kind Robots PR #4516 (squash b4e2dcc863aaa97147e9e74cdbb164ec0a6b09f1) after all 21 exact-head checks and 16 workflows passed on 46aea0df1d8bea4a7e011fae653f91ed1ee1cb05 (Contract Tests #41119161832 including Hoshimori 96-seed, eight earned windward accounts, replay/forgery tests; TypeScript #41119161767; Formatting #41119161659; Memory browser #41119161671). Eight new windward sites bring e07 to 44/64 village sites, 88 distinct site decisions and eight new earned council accounts, displayed in the existing bounded console. Red Oven stays 9/36. No new ArtJobs; existing 52108-52115 remain 0/8 delivered in latest status JSON despite successful Auto Art Generate #41109429247. Master issue kind_robots#4136 comment 6532338311 records evidence. Return READY for 20 missing village sites, 27 Oven rooms, 30+2 gallery, rendered art/device QA and unfinished e03-e06 campaign reachability. No deploy or human gate.

Scoped Hoshimori e07 64-site completion branch: twenty new southeastern authored scenes and forty decisions, southern Pip assembly callbacks, browser-stage consequence panel and eight-route adversarial replay tests. Kind Robots focused PR/CI forthcoming. The earlier 16-site vertical slice and Earth Chronicle are merged; 36 Oven rooms, final real art and visual device acceptance remain separate work.

Completed t-041 warm Hoshimori proof and its first-world expansion: Kind Robots PR #4519 merged at f3b069b8bc1bdc592d3db279c663db3ed4c2c746 after all 16 exact-head workflows and 21 checks passed, including all four contract shards, TypeScript, changed-file Prettier and Memory browser. Added twenty southeastern and southern authored locations, bringing e07 to 64 unique connected sites and 128 distinct outcomes. Added Pip's River Archive, Guestbook and southern assembly earned eight-way account, browser panel, save/forgery/once-only tests. Earlier 16-site console, lantern and first nine Oven rooms and two Earth photos remain operational in source. Do not claim the 36-room Oven, painted art, e08 horror mirror, natural e03-e06 campaign traversal or rendered device acceptance. Unlock t-042 and t-043 as separate next work; public deploy remains gated.
<!-- note:end t-041 -->

## t-042 — Hoshimori e07: finish 64 authored sites, 36-room oven, and distinct outcomes

<!-- note:begin t-042 -->
Extend warm e07 proof to all 64 reachable stable coordinates, 36 navigable Red Oven rooms, 3 materially different guardian resolutions, authored consequences and 30+2 scene-grounded gallery briefs. Keep Earth photos, route prerequisites, companion agency and spoiler-safe Chronicle intact; validate exact graph, seed replay, refusal and save reload. ArtJob submission and final rendered verification remain in t-045.

Scoped Ember Wing implementation on worker/memory-dungeon-t042-emberwing-c9e7: OV-10..OV-15 with twelve distinct decisions, three earned guardian dispositions, 64 outcome combinations, save-compatible entry, retreat/reentry and adversarial replay tests. Await exact-head PR CI and merge. Existing ArtJobs 52108-52115 unchanged; no deploy or final art acceptance.

2026-10-30 PT: Merged Kind Robots PR #4525 (46db7d53ef85df2843f630f9c102ebe4a7f0ae40) after all 16 exact-head GitHub Actions workflows succeeded on 0b651b208ff56c90ae3c9d4447a5ebcc9c1d11ef, including all four Contract Test shards, TypeScript, formatting, layout and Memory browser interruption. Added six optional Red Oven Ember Wing rooms OV-10..OV-15, 12 unique choices, 64 earned accounts and three provisional guardian dispositions; maintained old OV-03/OV-09 terminal save journals, retreat/resume, forgery and once-only guards. Hoshimori e07 now has 64/64 authored village sites and 15/36 Oven rooms. Return READY for 21 remaining rooms, final guardian consequences and 30+2 gallery briefs. ArtJobs 52108-52115 remain 0/8 delivered in latest committed audit, no new jobs, no deployment or rendered acceptance. Memory Dungeon remains ACTIVE; not For Human Gate.

Scoped Cinder Wing OV-16..OV-21, earned restitution accounts and replay regression implemented on worker/memory-dungeon-t042-cinderwing-k7f3. Kind Robots PR and exact-head CI to follow; preserve prior OV-15 terminal saves.

2026-10-30 2:55 PM PT: Merged Kind Robots PR #4526 (squash 4c6f29a784e9428f2fc744ad57a8424689efaf0f) after all 21 exact-head checks across 16 workflows passed on 457a4dc861a92b60aca2516a99e0537c05bc26de (Contract Tests #41133786533, TypeScript #41133786619, formatting #41133786673, Memory browser #41133786624). Six Cinder Wing rooms OV-16..OV-21, twelve choices, 64 earned restitution accounts, save-compatible OV-15 terminal and replay/forgery/retreat tests. Issue kind_robots#4136 comment 6534327461 documents evidence. Return READY for 15 remaining Red Oven rooms, final aftermath and 30+2 gallery. Existing ArtJobs 52108-52115 not rechecked; no new jobs, deploy or rendered visual acceptance. Memory Dungeon stays ACTIVE.

Hoshimori e07 Vesper character-center correction, while retaining all 64 authored site keys, original choice/flag IDs, 21 current Oven rooms, two fixed Earth photos, Pip's independently earned ledger/Oven subplot, and e06 entry gate. The first bridge, orchard, sold road, paper theatre, oathboat and southern assembly now resolve Vesper's childhood map-making, rescue, betrayal, confidential restitution or public accountability. Prior Briar earned Vesper rookery evidence appears only if the player made the prerequisite choices. Sixteen Vesper payoff combinations are covered by map-replay tests. Conductor gains updated CONTROL, the Hoshimori plan override and detailed original ink-body-horror World Eight mirror design with sixteen coordinate-anchored briefs. This is partial t-042 progress; the remaining 15 Oven rooms, full e08 playable map, generated art and visual acceptance remain outstanding.

2026-11-01 9:43 PM PT: Reconciled stale REVIEW from the 2026-10-30 merged Oven work. Kind Robots #4525 and #4526 are merged; no open t-042 PR or worker branch remains. Fifteen Oven rooms OV-22..OV-36 are still unfinished, so return READY for another scoped room batch, not DONE.

2026-11-01 PT: Authored Red Oven Saffron Wing OV-22..OV-27 with twelve distinct Vesper-centered outcomes, an earned fifth testimony account, replay-safe entry/retreat and 64 adversarial choice/save combinations. Focused Kind Robots PR and exact-head CI follow. Nine Oven rooms OV-28..OV-36, e08 full horror mirror, production ArtJobs and visual acceptance remain; no deployment or human gate.

2026-11-01 PT: Merged Kind Robots PR #4627 (squash 86413bcdf8c8802a19682f84b82ee21d90ec7755) after all eight exact-head workflows passed on 829609f791d4c8e0c62dd854dd3dc6e782fea27f, including Contract Tests, TypeScript, formatting and Memory Dungeon browser interruption. Saffron Wing OV-22..OV-27 adds 12 earned choices and 64 replay-validated accounts; Hoshimori now has 27/36 Oven rooms and 64/64 warm sites. Nine rooms OV-28..OV-36, earned guardian aftermath, 30+2 gallery briefs, actual art delivery and device QA remain. No new ArtJobs, deploy or human gate. Return READY for the remaining nine rooms.

Authored playable Hoshimori Glass Wing OV-28..OV-33 with 12 distinct choices, earned sixth consequence account, replay-safe entry and retreat, legacy OV-27 compatibility, and 64 seeded route/forgery tests. Focused Kind Robots PR and exact-head CI follow. Three final Red Oven rooms OV-34..OV-36, e08 earned exit, gallery art delivery and device QA remain; no new ArtJobs or deployment.

2026-11-02 1:09 AM PT: Kind Robots PR #4632 merged as 439a90682e5bd1be135550e6edc35f7b29323681 after 8/8 exact-head Actions workflows passed on 84d52b4d234413bc37a86e99c211ddc2024cd5be. Glass Wing OV-28..OV-33 delivers twelve decisions and replay-safe sixth testimony; 33/36 Red Oven rooms. Return READY for final three rooms OV-34..OV-36 and earned guardian resolution. ArtJobs 0; art delivery, e08 gate, device QA and final acceptance remain unfinished.

2026-11-02 1:58 AM PT: Final Red Oven OV-34..OV-36 authored with six consequential choices, a replay-earned seventh account, and three distinct guardian aftermaths respecting earlier consent/quench choices. Added legacy Glass save, retreat/reentry, forgery and 24 guardian-route regression cases. Focused Kind Robots PR pending exact-head CI; 30+2 gallery, art delivery, e08 gate and device QA remain.

2026-11-02 3:46 AM PT: Merged Kind Robots PR #4640 (squash 9a90681b63b9d1c928c3fb42cb9e05f00f1cfd9e) after all eight exact-head Actions workflows passed on 34aafd1371ed47ffa8f460c51d25037f287dcdd5, including Contract Tests, formatting, TypeScript, Memory Dungeon browser interruption, layout and schema parity. Hoshimori now has 64/64 authored village sites and 36/36 Red Oven rooms, with 24 seeded final guardian/choice routes, three distinct guardian dispositions and legacy save restoration. Return READY for outstanding 30+2 scene-grounded gallery briefs; art delivery and rendered QA belong to t-045, e08 earned gate is unfinished. New ArtJobs 0, deployment none, human gate not appropriate.

2026-11-02 4:50 AM PT: Existing 30+2 e07 gallery briefs verified against all 64 Hoshimori source sites (32/32 exact source-title matches). Added a separate source-backed 32-card earning/reveal handoff with 6+7+8+9 local waves, two collaboration gates, earned-photo guards, and contract tests. World Seven 64/64 warm sites and 36/36 Red Oven rooms already merged in kind_robots #4640. This is planning/validation, not art delivery or runtime gallery integration (t-045/t-033). Focused Conductor PR and CI follow; no deployment or human gate.

2026-11-02 PT: Closed e07 Hoshimori 64/64 warm sites, 36/36 Red Oven rooms and source-verified 30+2 gallery briefs after Kind Robots #4640 and Conductor #6961 merged. Conductor #6961 exact-head 7d9347cb passed Worker PR CI, Security Audit, handoff and task-event workflows (41448223490/41448223460/41448223470/41448223474). Gallery runtime persistence and production art remain separate t-033/t-045 tasks; e08 t-044 should unblock. No deploy or human gate.
<!-- note:end t-042 -->

## t-043 — Hoshimori e08 horror mirror: first 16 sites, Scylla POV and yōkai night procession

<!-- note:begin t-043 -->
Build the first 16 connected mirrored e08 sites on e07's actual fixed village geography, preserve Scylla viewpoint, reveal Pip's unresolved debt, and make unbind/testify mechanics and fair route alternatives playable. Distinguish visual grammar and protect Char/Oren agency. Keep photos at e08 1,4 and 6,7, same machine IDs, original title alias and save keys. Include seeded contract tests and real choices; do not count a metadata change or 16 art prompts as a playable full realm.

First e08 horror proof implemented on Kind Robots worker/memory-dungeon-t-043-night-procession-8fd21: sixteen coordinate-matched authored sites, Scylla and Vesper/Char/Oren/Pip witness choices, a fair alternate crossing and earned three-sign Nurikabe unbinding, independent replay-validated browser save, bounded console stage and eight council accounts. Exact-head CI and PR merge pending. e07 must be earned before this preview unlocks; e03-e06 remain incomplete. No new ArtJobs, rendered art, deployment, final e08 dungeon or human acceptance.

2026-10-30 PT: Merged Kind Robots PR #4532 (squash 1a8440687b71bf4165d6199d56cfa3bd73b16bd2) after all 21 exact-head checks passed on 8c7b3f18ec481052fc09ef65e40083bb6a9d1e78. Sixteen individually authored coordinate-matched e08 night-procession sites, 32 outcomes, Scylla/Vesper/Char/Oren/Pip agency, seed-derived three-sign Nurikabe unbinding, surveillance bargain and fair shrine bypass, eight earned council accounts, independent replay-validated v1 saves, bounded console stage and campaign-gated entry. Dedicated 96-seed night verifier passed in Contract shard 1/4 of workflow #41141905288; TypeScript, formatting, layout and browser checks also passed. Corrected e08 photo 1,4 to existing Chronicle canon, but actual photo pickup and 6,7 remain unimplemented. This completes only the t-043 first-sixteen-site proof, not the full e08 realm: 48 more sites, 36-room twisted Oven, 30+2 gallery, real art, e07 finish, e03-e06 natural access and rendered 390/768/1440 visual QA remain. No new ArtJobs, deployment or final human gate.
<!-- note:end t-043 -->

## t-048 — Polish Briar overworld fog and centered exploration beacons

<!-- note:begin t-048 -->
Silas's 2026-11-02 PT screenshot feedback: keep the right-hand scene panel, replace clinical unrevealed map-cell tiles with cohesive illustrated fog, remove generic explored-story diamond, center and enlarge 3D actionable exploration icons. Preserve map progression, story/location icons, reduced-motion and accessibility. Implement and validate independently of queued ArtJobs.

Scoped illustrated-fog, center-beacon and hidden-story-diamond changes prepared on worker/memory-dungeon-t-048-fog-beacons-c42a91. Source contract checks added; exact-head GitHub PR CI and visual acceptance still to be checked. Right-hand encounter pane and save logic unchanged.

2026-11-02 11:50 AM PT: Reviewer merged Kind Robots PR #4642 (squash 73f7f8004e69e24c66f863730c81a175d718a836) after seven completed exact-head green workflows on 37c06b07890e1ca90c5973617a0bd73c01b01ee7. Fog is a cohesive coordinate-aligned SVG fallback, action beacons are larger and centered, story diamonds removed, reduced motion retained; 390/768/1440px post-deploy pixel QA and production-painted map art remain in t-046/t-045. No ArtJobs or deployment.
<!-- note:end t-048 -->

## t-050 — Make Oren's House rest shortcut traversable and save-safe

<!-- note:begin t-050 -->
Silas-directed World One pacing work (Kind Robots #4721). Choosing Oren's route in HD-06 should unlock a two-way passage to HD-18 Quiet Bedchamber, with the alternative decision still blocking it. Preserve 36 stable room IDs and restoreHouseProgress reachability. Add automated locked/open/save-resume regression coverage.

Implemented HD-06 to HD-18 two-way route, stock-choice lock and save restoration support in kind_robots commit 2c8ad007. Added regression assertions for locked, unlocked and restored House navigation. Awaiting implementation PR CI and safe merge.

2026-11-04 PT cleanup pass: merged as kind_robots #4729 (9905878, 'make Oren's rest
passage playable and save-safe'); the HD-06 to HD-18 two-way route, stock-choice lock
and save restoration are the whole task. Done.
<!-- note:end t-050 -->

## t-052 — e03 Morrow's Shift: replace template recipe sites with 64 authored sites in the live Earth stage

<!-- note:begin t-052 -->
Silas-directed 2026-11-05 PT (CONTROL.md "TWELVE-OVERWORLD STRUCTURE RESTATED"): World One is the quality bar; develop the other ten worlds in play order. e03 today serves district x device template text from overworldEventRecipes.json ("At Lost Transit Pass, return the pass..."). Ship 64 authored e03 sites in kind_robots (utils/memoryDungeon/morrowShift/) through overworldEventCatalog: recurring Earth cast that e10 already relies on (Mara, Dr Sen, Nurse Imani, Sal), the instant-discovery/puzzle/hazard pacing mix from t-051, choice echoes that make later sites remember earlier decisions, and an 8,8 finale that seeds e04's arriving magic. Keep save compatibility: legacy care/risk ids replay, both Chronicle photograph sites (1,3 / 6,4) and their choices are untouched. Also align the campaign viewpoint contract with one lead per pair (e01/e02 Pip, e07/e08 Vesper) and the storyline-dependent e11 lead. Out of scope, next tasks: the e03 dungeon behind 6,2 Sublevel B, e04 authored revisit, painted art.

2026-11-05 PT: kind_robots#4778 serves 64 authored e03 sites
(utils/memoryDungeon/morrowShift/) in the live Earth stage: 18 instant discoveries,
puzzles, hazards, 53 choice echoes, recurring cast for e10, an 8,8 finale that seeds e04
magic, and legacy care/risk saves that still replay. The PR also sets one lead per pair
(e01/e02 Pip, e07/e08 Vesper) and adds memoryLeadFor (e11 is Scylla when Char was lost).
All verifyMemory* tests, the World One playtest and vue-tsc passed locally. Next: t-053
e03 Sublevel B dungeon, t-054 e04 authored revisit, t-055 e08 Vesper-POV rewrite, t-056
e01/e02 Pip camera reconciliation.

2026-11-05 PT: kind_robots#4778 merged (1df7185) with 13/13 checks green; close-out
conductor#7041 merged. Done. Next in play order: t-053 e03 dungeon (waiting -> ready now
that t-052 is done), t-054 e04, t-055 e08 Vesper POV; t-056 waits on Silas.
<!-- note:end t-052 -->

## t-053 — e03 dungeon: the Sublevel B after-hours archive behind 6,2

<!-- note:begin t-053 -->
Silas 2026-11-05 PT: every overworld has its own dungeon. e03's 6,2 Sublevel B threshold (authored in t-052, kind dungeon; care = signed key log with Walt, risk = borrowed Lena Kowalczyk badge) opens the locked archive under the Research Annex where the researcher's unfinished project (the sleep thread at 2,7/3,7) is stored. Build a 6x6 36-room dungeon on the House That Remembers pattern: justified room routes, treasure, rest/hazard/puzzle variety, a guardian, and alternate resolutions that read the key-log vs badge choice. Mundane Earth: no working magic. 3,6 Flats basement cages is a second threshold to decide (side wing or e04 hook).

2026-11-05 PT: kind_robots PR (claude/memory-t053-sublevel-b) ships Sublevel B with 36
authored rooms (utils/memoryDungeon/sublevelB/). Entry depends on the 6,2 escort or
badge choice. Hollis is a conversation guardian, with three endings
(return/finish/confess), two earned shortcuts, a torch-battery resource, 50 echoes and
replay-based restore. A new store and stage are entered from e03 6,2. All verifyMemory*
tests and vue-tsc pass, and real-app screenshots were taken at 390/768/1440. Follow-ups:
painted art, and e04/e10 reading the Sublevel B ending.

2026-11-05 PT: kind_robots#4794 merged (98ba734, 13/13 checks green after a one-scroll-
region layout-contract fix); review close-out conductor#7062 merged. Done. Next in play
order: t-054 e04 authored revisit.
<!-- note:end t-053 -->

## t-054 — e04 The Unbelieving City: authored revisit of e03's 64 places

<!-- note:begin t-054 -->
Replace e04's template recipe sites with authored ones on the same e03 places (same `place` names and coordinates), now haunted by arrived magic: the horror-register even world. Read e03 flags (8,8 risk = Morrow spoke the working; 3,3 Jun's letter; 4,6 Sal truth/bluff; 5,7 Imani; 8,6 Tilly's fountain). Keep photo sites 2,2 / 7,6 and the 8,8 tide-gate choice ids (open/seal/divert) unchanged: it is the e03/e04 pair's major storyline choice. Include e04's dungeon.

2026-11-05 PT: kind_robots PR (claude/memory-t054-e04) adds 64 authored e04 sites
(utils/memoryDungeon/unbelievingCity/) on e03's exact places, with 18 instants and 139
echoes that reach e03 and the Sublevel B ending. Photo sites and the 8,8 tide gate keep
their choices and flags; Char and Scylla come on screen at the gate. The catalog now has
an AUTHORED_WORLDS table. All verifyMemory* tests, vue-tsc and layout-contract pass.
Follow-ups: e04 dungeon behind 6,2, painted art.

2026-11-05 PT: kind_robots#4795 merged (13/13 checks green); review close-out
conductor#7064 merged. I checked the real app at 390/1440: e04 Mara's roll call renders
with echoes and cards. Done. Next in play order: t-055 e08 Vesper-POV rewrite (ready),
then e05/e06 authored sea, e04's dungeon.
<!-- note:end t-054 -->

## t-056 — Name the researcher (Rowan) as the e01/e02 and e09 lead; Pip stays a supporting NPC

<!-- note:begin t-056 -->
FOR SILAS: You said each of the first eight overworlds keeps one protagonist for both rounds, and the finale replays "the same four" (Pip, Morrow, Char-for-Scylla, Vesper), so e01/e02's lead is Pip. But shipped World One is told through the displaced Earth researcher who traded lives with Morrow (prologue, Chronicle photos, House endings), and Pip is a secondary character there. Kind Robots now records Pip as the e01/e02 viewpoint in the campaign contract only; no Briar text or save was changed. Decide one: (A, recommended) keep the researcher as the World One player character and make Pip the in-story lead/companion whose choices the researcher shares, so no shipped scene is rewritten; (B) rewrite World One's camera to Pip, a large rewrite touching the prologue and House endings; (C) the researcher is the true fourth protagonist and e09's finale lead becomes the researcher. Reversible; under the 2026-09-30 rule, A is adopted after 7 days unanswered.

DECIDED by Silas 2026-11-05 PT (CONTROL.md "RESEARCHER IS THE e01/e02 AND e09 LEAD"): the main character is the researcher, he/him, with an androgynous name (agent-chosen: Rowan). Not option A/B/C as written. Implement: a single name constant, the campaign viewpoint contract (e01/e02/e09 = researcher, drop the pip perspective), name him in the prologue and in e03 where Earth people address Morrow, he/his for the researcher. Pip stays the goblin courier NPC. e09 scene rewrite is t-057.

2026-11-05 PT: kind_robots PR (claude/memory-rowan-researcher) adds
MEMORY_RESEARCHER_NAME = 'Rowan'. It makes e01/e02/e09 the researcher's viewpoint (drops
pip), names him in the prologue, and has e03 call Morrow Rowan, with he/his for Rowan.
All verifyMemory* tests, the World One playtest and vue-tsc passed. Pip stays a goblin
NPC; e09 scene rewrite is t-057.

2026-11-05 PT: kind_robots#4779 merged (7b82a5b, 13/13 checks green); review close-out
conductor#7050 merged. Done. Next: t-057 e09 Rowan-led rewrite.
<!-- note:end t-056 -->

## t-058 — e05 Scylla's Shore: replace template recipe sites with 64 authored sites

<!-- note:begin t-058 -->
Silas 2026-11-05 PT (CONTROL.md "TWELVE-OVERWORLD STRUCTURE RESTATED"): develop the remaining worlds in play order at the World One bar. e05 is Scylla's lead: real time travel into her younger self in the sea palace, days before she and Char first ran away, with the e04 tide-gate outcome remembered (memoryCharFate: lost / alive). Follow the e03/e04 pattern: utils/memoryDungeon/<world>/ row modules wired through AUTHORED_WORLDS in overworldEventCatalog.ts, pacing mix, echoes of e04 8,8 and e03/e04 anchors, legacy care/risk saves, and fixed sites that keep their choices: Chronicle photos and 8,8 run-again / stay / tell-char (the departure choice). One 8x8 underwater palace geography (childhood/court, craft and servants, waterways, exit and shore) that e06 will revisit.

2026-11-05 PT: kind_robots PR (claude/memory-t058-e05) adds 64 authored e05 sites
(utils/memoryDungeon/scyllasShore/) with 19 instants and 94 echoes, and remembers all
three e04 tide-gate outcomes. The 4,6 Glass Throat is the dungeon threshold. Photo and
8,8 departure choices are unchanged. Sea openings now combine the campaign line with the
authored opening and its echoes. All verifyMemory* tests, vue-tsc and layout-contract
pass. Follow-ups: e05 dungeon, t-059 e06.

2026-11-05 PT: kind_robots#4796 merged (13/13 checks green); review close-out
conductor#7066 merged. Done. resolve_deps unblocks t-059 (e06).
<!-- note:end t-058 -->

## t-059 — e06 Undertide Crown: authored horror revisit of e05's palace

<!-- note:begin t-059 -->
Even world, horror register: the same e05 places, warped (rewritten testimony, coercive repetition, looping corridors that still admit a fair route). Keep 7,7 Char-agency choices (MEMORY_CHAR_AGENCY_CHOICES) and 8,8 publish-twin-testimony / protect-private-memory exactly; Chronicle photos fixed. Never silently undo a witnessed e04 death. Pattern: e04 (unbelievingCity) on e03.

2026-11-05 PT: kind_robots PR (claude/memory-t059-e06) adds 64 authored e06 sites
(utils/memoryDungeon/undertideCrown/) on e05's exact places, with 17 instants and 200
echoes. Every e05 departure and e04 gate outcome is remembered. Photos, 7,7 Char-agency
and 8,8 witness-bell choices are unchanged. The dead SEA_KEY_SCENES table is removed, so
seaNarrative now returns campaign lines only. All verifyMemory* tests, vue-tsc and
layout-contract pass.

2026-11-05 PT: kind_robots#4803 merged (13/13 checks green); review close-out
conductor#7070 merged. Done. e03 through e06 and the e03 dungeon are now authored. Next
ready: t-060 e04 dungeon, t-055 e08 Vesper POV, t-057 e09 Rowan lead.
<!-- note:end t-059 -->

## t-060 — e04 dungeon: the flooding archive behind 6,2

<!-- note:begin t-060 -->
Every overworld has its own dungeon (Silas 2026-11-05). e04's 6,2 threshold is Sublevel B flooding with seawater. Build it on the Sublevel B engine (utils/memoryDungeon/sublevelB/): ideally extract a shared authored-dungeon reducer (graph, shortcuts, gates, replay restore) first, then author 36 horror-register rooms that remember the e03 Sublevel B ending (SB-35 return/finish/confess) and the e03 6,2 entry. Wire like memory-dungeon-sublevel.vue from the e04 stage.

2026-11-05 PT: kind_robots PR (claude/memory-t060-dungeon-engine) extracts the shared
authored-dungeon engine (utils/memoryDungeon/authoredDungeon/) and store helper
(stores/helpers/authoredDungeonStore.ts), with Sublevel B rebound and behavior
unchanged. It adds the Drowned Archive: 36 flooded rooms on Sublevel B's plan, 141
echoes (34 rooms remember their dry twin), the sea's-ledger guardian, and
salvage/rescue/testify endings, entered from e04 6,2. All verifyMemory* tests, vue-tsc
and layout-contract pass.

2026-11-05 PT: kind_robots#4827 merged (13/13 checks green); review close-out
conductor#7084 merged. Done. The shared authored-dungeon engine is on main, so the
e05/e06 dungeons behind 4,6 are now content plus a binding.
<!-- note:end t-060 -->

## t-061 — e05 dungeon: the Glass Throat service tunnels under the sea palace

<!-- note:begin t-061 -->
Silas 2026-11-05 PT: every overworld has its own dungeon. e05's 4,6 Glass Throat (an intake shaft at the Tide Observatory) drops into the palace's old service tunnels, where the whole sea-works breathes. Build 36 hand-written rooms on the shared authored-dungeon engine (utils/memoryDungeon/authoredDungeon/ + stores/helpers/authoredDungeonStore.ts), like Sublevel B: warm-register, Scylla's lead, younger Char and Oren, the third-night escape timeline. Entry variants from the e05 4,6 choice; a conversation guardian; three endings that later worlds can read; echoes of e04 tide-gate flags and e05 anchors. Mount from the e05 stage at 4,6.

Breathing Works (e05 dungeon) on the shared engine; PR kind_robots#4833.

Merged kind_robots#4833 (66fb270).
<!-- note:end t-061 -->

## t-062 — e06 dungeon: the warped service tunnels under the Undertide Crown

<!-- note:begin t-062 -->
e06's 4,6 is the same Glass Throat, warped. Build the horror twin of t-061's tunnels on the same plan (as the Drowned Archive is to Sublevel B): every room remembers its e05 twin and the t-061 ending, plus e05 departure flags and e04 tide-gate flags. Coercion, repetition and erasure as dread; Char's agency first.

Choking Works (e06 dungeon), the Breathing Works warped on the same plan; PR
kind_robots#4835. Also restores Fenn Dunlin's canon name in the Breathing Works.

Merged kind_robots#4835 (30cf426).
<!-- note:end t-062 -->
