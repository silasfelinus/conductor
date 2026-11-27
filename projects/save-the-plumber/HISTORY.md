# save-the-plumber — task history archive

Full `note:` prose for completed save-the-plumber tasks, moved out of `roadmap.yaml` so the
Kind Robots projection payload (`scripts/sync_kind_robots_projection.py`, hard limit
4,000,000 bytes) stays well clear of its ceiling. See conductor/t-158.

Each note below is the **verbatim** original — nothing is summarized or trimmed. The
`roadmap.yaml` task keeps its own first sentence plus a pointer here. The HTML comment
markers delimit each note exactly; `archive_done_task_notes.py --verify-only` re-extracts
every note and checks it byte-for-byte against what the roadmap recorded.

## t-002 — Gen-2 world design: eight world maps, node graphs, secret exits and level-type mix

<!-- note:begin t-002 -->
REWRITTEN 2026-10-22 PT for Silas's Gen-2 direction (projects/kr-arcade/GEN2-STANDARD.md).
Write projects/save-the-plumber/GEN2-WORLDS.md: for each of the eight worlds an overworld
node graph (6-9 nodes: levels, a fortress with a mid-boss, a Hush House haunted maze, bonus
cottage, shop or item house, the world castle), which levels have a secret exit and which path
each exit opens, where the Valve Chapel switch palaces sit and which blocks they make solid
campaign-wide, the Upstream Sky special zone and its secret entrances, and a per-level beat
sheet (3-6 minute first clear, midpoint, sub-areas, the secret, the skill test). Reuse the 32
Gen-1 stages as rooms and set-pieces where they fit. The node graph must be machine-readable
enough to become savePlumberOverworld.ts data (t-011 ships World 1's graph as the template).
Overworld map plates per world are queued in art/GEN2-ROUND-1.yaml.

Original (superseded) brief:
World-by-world authored maps/beat sheets from WORLD-ATLAS.md: 32 unique level objectives and diagrams, 40+ distinct enemy behaviors, eight readable boss movesets, four-stage pacing, secrets, rewards, original soundtrack motifs, intro, chapter and ending illustrations. Plan collision/exits before painting. Use internal art pipeline and verify delivered assets.

Prior production-bible session was interrupted by Silas's more specific four-princess cast direction. No Save the Plumber production-bible deliverable was committed in that session. Return this task to ready for the next agent to author its 32-stage and 40+ behavior design catalog; retain existing WORLD-ATLAS and DESIGN-BRIEF without overwriting.

DONE 2026-10-22: GEN2-WORLDS.md (eight worlds of 7-9 nodes, 81 nodes, 13 secret exits, four Valve Chapels, the Upstream Sky zone, a Wild Tap wonder moment per course, six powers plus the Spare Thermos reserve and Gurgle the newt companion, per-course beat sheets) and gen2Worlds.json with validate_gen2_worlds.py (PASS). Next: t-011 follow-up makes savePlumberOverworld.ts data-driven from gen2Worlds.json (unlock by node, nine node kinds, save v3 keyed by node id; migrate via each node's Gen-1 stage, never by id).
<!-- note:end t-002 -->

## t-003 — Build private /admin Arcade shell and original platforming physics

<!-- note:begin t-003 -->
Inspect existing Arcade platformer and its adapters before adding code. Create requiredRole ADMIN discoverable tab at /admin/save-the-plumber, isolated game state/score namespace, fixed-step jump/fall/coyote-time and buffered input, adjustable acceleration, camera/colliders, debug replay and mobile/gamepad control maps. No premature public /play route.

Private art-forward eight-world map and Bluebell movement lab wired to the shared Arcade cabinet, local input and private unlisted game registry; admin tutorial/sidebar, project placement and regression tests implemented. The 32-stage campaign and heroine generator remain subsequent roadmap tasks.

Merged kind_robots#3564 at a4e37feb4db759122ca2057d8a1145a4f2016c47. All 34 checks succeeded on 78e88f2d3c82eb49428a19acdad5f481c4221403; cancelled image build recovered on run 38200581045 attempt 2, job 114664187785. Complete diff, Main ruleset checks and reviews inspected. Combined arcade suite and isolated actual Vue-page/engine browser fixtures passed at 390/768/1440px. Tutorial.body and real tab resolver repair verified on main. Preserved both private previews during normal merge conflict resolution. No deployment/public launch; actual shared-cabinet integration and full 32-stage acceptance remain follow-up work. Conductor review handoff #6016 also merged.
<!-- note:end t-003 -->

## t-004 — Implement run-stable heroine generator, animations and opening

<!-- note:begin t-004 -->
Seed once-per-new-run a young-adult protagonist appearance and name from authored combinations; consistent collision bounds and silhouettes, optionally reroll during new-game setup. Represent the kidnapped plumber boyfriend as an original character with agency in the cutscenes. Persist seed across save/resume. 2026-10-13: the seeded generator (createHeroine, HEROINE_HITBOX, authored name/skin/hair/outfit palettes) and its persisted kept seed exist in kind_robots utils/arcade/games/savePlumberHeroine.ts and stores/savePlumberStore.ts, driving the front page. Remaining: use the kept seed in the game engine's sprite, New Game reroll in-cabinet, and the opening cutscene.
2026-10-16: the heroine is now chosen in the cabinet (silasfelinus/kind_robots#3735): title screen with New Game / Continue, an eight-heroine painted select (B picks at random), and the choice saved in the cabinet's resume save and starred on the front page. The engine draws the chosen roster heroine's sheets. Remaining: the opening cutscene (intro-discovery / intro-capture art exists) and the plumber's cutscene agency.
2026-10-16: the opening cutscene shipped and merged (silasfelinus/kind_robots#3756). A new game opens with three painted story panels: Teo sees the rivers rise, then brass claws snatch him; he jams his wrench in their gears and scatters brass tokens as the trail the heroine follows. A turns the page, START skips, and Continue goes straight to the saved stage. With the in-cabinet heroine select (#3735), the seeded roster and the rescue finale (#3754), t-004 is complete.
<!-- note:end t-004 -->

## t-006 — Build World 1: four complete garden/pipeworks levels and boss

<!-- note:begin t-006 -->
Four substantial and independently finishable authored stages with ramping jumps, enemy combinations, hidden alternate room and a fully attackable boss. This is the vertical slice quality bar: no reused 15-second procedural platform shuffle.
2026-10-16: merged silasfelinus/kind_robots#3735 at 7c160c17eb571c5520ee74905c96b5eab4489479. Four authored tile-map stages (1-1 Rainy Courtyard, 1-2 Copper Greenhouses, 1-3 Buried Meter, 1-4 The Pump Tower) with ledges, crates, valve-opened water gates, steam vents, springsteps, pistons, brass lifts, checkpoints, two pipe-door secret rooms, pumpbugs and rivet rollers (stun then kick), hearts and lives, and a three-hit Madame Pressure boss with a gauge tell and steam waves. A predictive autopilot clears every stage in verifySavePlumberLevels.test.ts. Powerup tracks remain t-005.
<!-- note:end t-006 -->

## t-007 — Build Worlds 2–3: eight new levels and two bosses

<!-- note:begin t-007 -->
Tideglass Marina and Lantern Orchard: water currents and floating platforms, overhead fruit levers and reversals; authored 2-1 to 3-4 levels, distinct foes, alternate exits and unique boss patterns, escalating checkpoint spacing.
2026-10-16: unblocked by t-006 (World 1 playable, silasfelinus/kind_robots#3735). The stage format, engine and autopilot playthrough test in savePlumberLevels.ts / savePlumberPreview.ts are ready for Worlds 2 and 3; tonight's art batch queues their ledge and block textures.
2026-10-16: Worlds 2 and 3 shipped and merged (silasfelinus/kind_robots#3746): eight stages, Captain Barnaclejack and the Overripe Baron, water, rafts, minnows, cork crabs, glass gulls, moss lanterns, spring hares and unlit stages; the autopilot test plays every stage through.
<!-- note:end t-007 -->

## t-008 — Build Worlds 4–5: eight new levels and two bosses

<!-- note:begin t-008 -->
Clockwork Fair and Cloudrail Commons: conveyor toys, parades, lift timing and airship movement, puzzle/combat variety, multiple secret routes, originally authored boss fights.
2026-10-16: Worlds 4 and 5 shipped and merged (silasfelinus/kind_robots#3748): eight stages, the Tick-Tock Duchess and Admiral Gust, conveyor belts, wind corridors, falling cargo, gasket golems, paper kites and umbrella mites; the autopilot test plays every stage through.
<!-- note:end t-008 -->

## t-009 — Build Worlds 6–7: eight late-game levels and two bosses

<!-- note:begin t-009 -->
Crystal Underworks and Night Market Rooftops: reflecting hazards, echo paths, mirrored doors, rooftop chase, vertical platform challenge with growing but fair mastery; challenge derives from telegraphed mechanics, not cheap hits.
2026-10-16: Worlds 6 and 7 shipped and merged (silasfelinus/kind_robots#3751): eight stages, the Prism Mole and the Umbrella Dragon, crystal bridges that are solid only while lit, echo gates, unlit caverns, puddle mimics, siphon sprites, chimney spirits and tea-kettle knights; the autopilot test plays every stage through.
<!-- note:end t-009 -->

## t-010 — Build World 8: four final levels, fortress and rescue finale boss

<!-- note:begin t-010 -->
Eight-world map culminates at the Stardrain Citadel; World 8 has its own four authored stages, multiple mechanical callbacks, legible final boss and real playable rescue. Distinct victory and continued-play/secret ending paths.
2026-10-16: World 8 and the rescue finale shipped and merged (silasfelinus/kind_robots#3754): four Stardrain Citadel stages calling back every earlier mechanic, Lady Spigot (the hissing valve marks the side her water jet fires from), and a finale over the painted finale-reversal art that saves the campaign as cleared. The autopilot test plays all 32 stages through. A secret or continued-play ending path is not built; that and the wider secrets work sit with t-011.
<!-- note:end t-010 -->

## t-011 — Finish map progression, lives, secrets, challenge and save system

<!-- note:begin t-011 -->
REWRITTEN 2026-10-22 PT for the Gen-2 bar (projects/kr-arcade/GEN2-STANDARD.md sections 1 and 3). Ship in Kind Robots: (1) a pure overworld module (node graph per world, paths with normal/secret unlock conditions, walking between revealed nodes, entering a level, revisits); (2) save v2 with three slots: map position, per-level clear and secret-exit flags, Golden Gear ids, switches, revealed paths, reserve item, lives, total time, deaths and completion percent, migrating a v1 save into slot 1 rather than dropping it; (3) a walkable World 1 map screen in the cabinet between stages, with completion marks per node, and a file-select screen with per-slot percent. Later worlds' graphs come from t-002. Account sync is kr-arcade/t-163.
Pre-Gen-2 note, kept for history: World map, exits/warps, collectibles, achievements, secret rooms, coin-equivalent reward economy, save/continue, difficulty assists, score and speedrun splits. Every planned secret is mechanically discoverable in a blind run; no impossible dead-end levels.
2026-10-16: unblocked. All 32 stages are playable (t-006 to t-010 done). Already in place: per-stage checkpoints, three hearts and lives, cabinet save/continue, secret pipe rooms in 1-1, 2-2 and 3-2, and tokens with an extra life every 100. Still to build: map exits/warps, achievements, difficulty assists, speedrun splits, a secret ending, and a blind-run secrets audit.
DONE 2026-10-22: kind_robots#4030 merged (17c094c) after 23/23 checks green. Eight walkable world maps (savePlumberOverworld.ts) with normal/secret-exit path unlocks, revisits and the castle road between worlds; save v2 with three files (map node, clears, secret exits, gears, deaths, time) migrating v1 saves; file select, map screen with locked stages dimmed and newly opened paths drawn in; verifySavePlumberOverworld test. Fortresses, Hush Houses, Valve Chapels and real secret exits arrive with t-002/t-020/t-021; painted map plates with t-024.
<!-- note:end t-011 -->

## t-015 — Prove the movement lab replay and real shared-cabinet controls

<!-- note:begin t-015 -->
Reviewer kaizen after kind_robots#3564: add deterministic input replays asserting coyote time, buffered jumps, landing/camera bounds and respawn; exercise real shared ArcadeCabinet keyboard/gamepad/touch controls and visible Admin help at phone/tablet/desktop widths. Use browser fixtures with actual consumers rather than source-field matches. Keep public registry and score exclusions. Initial isolated engine pixels are not shared-cabinet/auth integration or full campaign acceptance.

2026-11-02 PT: Input-guide slice on worker/save-the-plumber-t-015-input-guide-84c7: dedicated keyboard shortcuts, controller/keyboard help, menu labeling and regression assertions. Movement replay and cross-width browser fixtures remain on this task after the PR lands; do not close as done yet.

2026-11-02 PT: Merged user-reported controller and keyboard control guide fixes in kind_robots#4689 (merge 42b3e2ba68cf8063021c6820f18b3a74cec94467). All nine GitHub CI workflows passed, including TypeScript, Arcade viewport, Chromium cabinet browser contract, lint/format and contract test shards. Remaining t-015 scope is deterministic coyote-time, buffered-jump, landing/camera, and respawn replay plus real shared-cabinet keyboard/gamepad/ touch cross-width fixture coverage; do not mark this larger task done.

2026-11-05 PT, game-sprint adversarial slice: Added kind_robots
utils/scripts/verifySavePlumberMovementReplay.test.ts, wired into test:arcade-engine.
Deterministic lab-stage replays pin coyote time (7 frames), the jump buffer (5 frames
before touchdown), variable jump height, landing snap, edge and camera bounds, and
checkpoint respawn through game over. Across all 32 stages it checks that every start
and checkpoint respawn is open and solidly floored, and a vault battery shows no heroine
with Springstep can cross a closed valve gate or leave a locked boss arena. A seeded
581k-frame fuzz (8 heroines x 4 power states) asserts finite physics, in-bounds hero and
camera, no wall clipping, sane hearts and lives, and that deaths always resolve. The
fuzz found and fixed a real clip in 12 stages: jumping or being hit while crouched under
a one-tile gap (e.g. the 1-1 slide-under pillar) stood her up inside the block. She now
stays crouched in the air under a solid tile. Patch base kind_robots 02a1a83; the
coordinator applies it and opens the kind_robots PR. The Levels, Gears, Endless, Maker
and Overworld suites pass. verifySavePlumberPreview.test.ts was already red on main
(stale Screen regex). Remaining on t-015, do not mark done: real shared-ArcadeCabinet
keyboard/gamepad/touch browser fixtures and visible Admin help at 390/768/1440.

2026-11-04 PT: movement replay battery and crouch-jump ceiling-clip fix merged as
kind_robots #4775 (squash 89bba84); also repaired the stale verifySavePlumberPreview
Screen regex and an unused-var lint regression. Back to ready for the browser half:
shared-cabinet keyboard/gamepad/touch fixtures and Admin help at 390/768/1440. Pre-
existing: verifyArcadeEngine zuzu-pinball 2D-draw assertion still fails on main.

Partial movement-feel slice: sharpened opposite-direction ground braking while preserving running momentum, with deterministic reversal replay. Implementation branch worker/save-the-plumber-t-015-turn-response-m7q4. Remaining t-015 shared-cabinet cross-width/browser acceptance; do not mark done.

PR silasfelinus/kind_robots#5627 merged at 2026-11-23T03:46:24Z. The responsive-ground-turnaround movement replay slice shipped; the shared-cabinet real-device and camera-look-ahead acceptance remains, so return this nonrecurring task to ready rather than marking it done.

Added velocity-aware, bounded, smoothed bidirectional camera look-ahead with neutral centering, arena clamp, stage-start and pipe-teleport resets in worker/save-the-plumber-t-015-camera-lead-k7p9. Extended deterministic movement replays to prove visibility lead in both directions, smooth reversals, bounds, collision safety and restart reset. This is an incremental movement slice; real shared-cabinet keyboard/gamepad/touch and viewport browser fixtures remain required before the full t-015 task is done.

PR #5632 (bidirectional camera look-ahead) was verified merged at 2026-11-23T04:57:58Z and no Save the Plumber implementation PR remains open. Restoring the nonrecurring movement-lab task to ready for remaining shared-cabinet/browser verification and responsiveness tuning; no human gate.

Implemented immediate landing-tick buffered jumps in worker/save-the-plumber-t-015-landing-buffer-j6m8, preserving spring priority, eliminating redundant landing audio, and adding deterministic replay cases for 0-5 frame buffers and held-button nonrepeat. CI pending; shared-cabinet keyboard/gamepad/touch cross-width browser verification remains on t-015.

Merged kind_robots#5680 at c97fb087 after all eleven exact-head workflows passed, including the actual Chromium cabinet keyboard, gamepad and touch test (run 45275834533). Landing-tick jump buffering and replay regressions shipped. Remaining scope includes visible tutorial/help verification at all three widths and further movement acceptance; keep ready rather than claiming complete.

Implemented neutral-air momentum retention without changing ground or ice braking, speed caps or directional steering. Deterministic two-direction sprint-jump replay asserts retained speed, two-tile travel, reversal and collision safety. Branch worker/save-the-plumber-t-015-airflow-v4n9, head 7c839cf2. CI pending; task remains partial.

Verified kind_robots#5695 merged at efec50ae. Neutral-air momentum shipped; remaining movement and cross-width verification. Return to ready.

Independent movement-tuning slice: Springstep preserves momentum during held descent with normal drag restored on release, and deterministic bilateral comparison and counter-steering regressions. App branch worker/save-the-plumber-t-015-air-steering-p7m4 head 45a6a53d; full CI pending. Distinct Gen-2 glide power remains t-005 scope; shared-cabinet browser acceptance remains t-015 scope.

Verified kind_robots#5846 merged at 3273d5b3 after all 12 pre-merge exact-head workflows passed on 8d345d5b, including real cabinet Chromium run 45721357740 and movement replay contract run 45721357777. Deterministic movement, camera, respawn, keyboard/gamepad/touch and rendered tutorial at 390/768/1440 are complete for this task; physical-device and campaign acceptance remain t-013. Branch janitor in progress; production deployment unverified.
<!-- note:end t-015 -->

## t-016 — Art-led front page: title screen, overworld map, casting, cast and framed training run

<!-- note:begin t-016 -->
Silas 2026-10-13: "all of our projects need to have an impressive front end from the get go." Replaced the placeholder admin page with an animated SVG title scene (citadel, uphill rivers, heroine mid-leap), prologue panels, an interactive eight-island overworld map with per-world stage/boss detail, a seeded heroine casting call with reroll/keep, Teo and Lady Spigot, enemy toy box, powers and a framed training run. Painted world/cast vignettes queued in art-prompts.yaml (save-the-plumber-world-*, save-the-plumber-cast-*) and overlay only once delivered; queued is not rendered. Implementation: kind_robots#3624.
Merged kind_robots#3624 at 3434300ed807a8eba9841c915372904fc4dab7fa; all 34 checks green on 8108e3b (layout-contract fixed with container-width grids). Painted world/cast art is queued, not yet rendered; drawn SVG scenes stand in until delivered.
<!-- note:end t-016 -->

## t-017 — Wire delivered art into the movement lab: stage plates, tiles, keyed sprites, animated heroine

<!-- note:begin t-017 -->
Load the ART-PLAN.md assets in the engine with code-drawn fallbacks: the 1-1 stage plate as the far layer, the World 1 ground tile as the platform fill, pumpbug/token/pennant/goal-valve sprites keyed out of their white backgrounds at load time, and a canvas port of the front page's animated heroine (run/jump poses, scarf) using the kept heroine seed. Verify in a browser at phone and desktop widths, with and without delivered art.
Merged kind_robots#3650 at 76c34fda66bb67e1005fb01f128415352937e7a7. Engine draws delivered art with code-drawn fallbacks: 1-1 plate, World 1 ground tile, keyed pumpbug/token/goal-valve sprites, and an animated canvas heroine using the kept seed. Verified in Chromium with stand-in art and with none; the 84 queued assets render through Auto Art Generate.
<!-- note:end t-017 -->

## t-018 — Painted heroine roster: eight heroines with portraits and run/action sheets in casting and the engine

<!-- note:begin t-018 -->
Silas, 2026-10-14: "Love multiple heroines, with notable differences in body type, ethnicity, etc." The roster is in ART-PLAN.md ("The heroine roster"): Pip, Marisol, Tala, Ji-woo, Odette, Hodan, Priya and Nova, each with a character select portrait and six-pose run and action sheets. Waits on those renders. Then slice every sheet, re-roll any that fail, pick the heroine from the seed, replace the code-drawn casting with the painted portraits, and draw the chosen heroine's sheets in the engine, keeping the canvas heroine as the fallback.
2026-10-14: wired in silasfelinus/kind_robots#3676 (roster module, painted casting with an 8-heroine picker, painted Starring face, per-heroine sheets at her own height in the movement lab, code-drawn fallbacks in roster colours). Delivered sheets slice 6/6 except Marisol's run (figures overlap), re-rolled as heroine-marisol-run-v2. Hodan actions, Priya and Nova were still rendering. Done when #3676 merges and every roster sheet slices.
Reconciled 2026-10-14: PR kind_robots#3676 merged 2026-10-14T05:53:28Z.
<!-- note:end t-018 -->

## t-019 — Animate enemies and bosses from their painted sheets

<!-- note:begin t-019 -->
Waits on the 20 enemy and boss sheets queued in silasfelinus/conductor#6158 (reworded to drop "frame" in the roster PR). Slice each one and wire move/tell/attack/hurt/defeat poses into the engine as enemies and bosses appear, with the single keyed sprite as the fallback.
2026-10-14: front-page half merged in silasfelinus/kind_robots#3680 (e874c1dba26edb90374707155db9984e434af93d): the toy box shows all 14 enemy families looping their painted cycles with a hover/tap move, the world map's boss panel plays the attack sheet, and the slicer joins column-stacked shapes (spring hare above its spring). 13 of 14 enemy sheets and 2 of 8 boss sheets (Madame Pressure, Prism Mole) slice 6/6; tea-kettle knight and 6 boss sheets are still rendering. Remaining: put the other families into the playable level with their behaviours.
Reconciled 2026-10-14: PR kind_robots#3680 merged 2026-10-14T06:37:47Z.
<!-- note:end t-019 -->

## t-020 — Gen-2 level engine: sub-areas, vertical rooms, midpoints, secret exits, campaign-wide switches

<!-- note:begin t-020 -->
GEN2-STANDARD.md section 2. Doors, pipes and ladders into sub-rooms with their own camera bounds; vertical shafts and climbs; a midpoint checkpoint per level; a second, hidden exit type that reports `secret` to the overworld (t-011); Valve Chapel switch state read by every level so pressed switches make outlined blocks solid campaign-wide; auto-scroll and haunted-maze (Hush House) exit logic. Deterministic replay tests for each: secret exit reachable, sub-room return position, switch persistence across levels and save/reload.

Fixed x-only checkpoint activation: pennants now require physical proximity, preventing distant upper routes from silently changing respawn. Added a deterministic upper-route bypass/contact replay in verifySavePlumberMovementReplay.test.ts. This is a partial t-020 slice; subrooms, secret exits and campaign switches remain. CI pending.

Verified checkpoint contact PR #5635 merged at dfa809b2; no open Plumber PR found. Reopen remaining Gen-2 room and secret-exit work, not complete.

Implemented the first authored alternate exit on Buried Meter (1-3), requiring deliberate grounded Down on the upper gear route, recording secret clears independently and unlocking Verdigris Chapel on the overworld. Added campaign reachability and save/reload regression assertions. Commit a62c6930, worker/save-the-plumber-t-020-secret-exit-n4b7. CI pending; subrooms, additional secret exits, switches and the chapel course itself remain incomplete.

PR kind_robots#5705 merged at 7e8b705 after all 11 exact-head workflows passed, including secret route footing, overworld, movement and save regressions. First alternate exit works; further rooms and switches remain.

Authored six additional secret exits in existing courses 3-2, 3-3, 4-3, 5-2, 6-2 and 7-3, opening their existing map links to three chapels and three Upstream Sky entrances. Added real stage clear/save roundtrip assertions and existing reachability flood covers all six. Branch worker/save-the-plumber-t-020-orchard-exits-r8c4 head 60cc223. CI pending; destination courses, subrooms and switches remain.

Merged kind_robots#5732 at 5ad37ebb after 10/10 exact-head workflows passed. Seven secret exits implemented; remaining persistent switches, destination courses and subrooms. Return to ready.

Added a playable Verdigris Chapel branch course and per-slot persistent solid switch blocks in Rainy Courtyard and Copper Greenhouses, using the existing normal-clear node memory without changing campaign indices or save format. Added map, goal-contact, reload and slot isolation regression assertions. Branch worker/save-the-plumber-t-020-valves-6f8c head b485c045. Partial engine scope; CI and further chapels/subrooms remain.

Verified kind_robots#5769 merged 2026-11-24 PT. Verdigris Chapel and persistent switch blocks delivered; remaining chapels, subrooms and vertical stages. Return partial scope to ready.

Generalized optional chapel entry, respawn, completion and backdrop; authored Brass, Cobalt and Rose Chapel courses and persistent per-slot switch blocks in Worlds 3, 4 and 6. Added map, death-reload, clear, save and fresh-slot regression coverage. App branch worker/save-the-plumber-t-020-chapels-v5c1 head d1190ef3. Full CI pending. Subrooms, vertical traversal, auto-scroll and haunted mazes remain.

Verified kind_robots#5821 merged at cdd5acb4. All four Valve Chapels are implemented with persistent per-slot switches. Return partial engine scope to ready: subrooms, vertical routes, auto-scroll and haunted mazes remain.

Implemented sealed pipe chamber detection, independently bounded camera framing, exterior masking and pipe transition cleanup across all eight existing late-world chambers. Added replay coverage for entry, camera lock, collection and return. App branch worker/save-the-plumber-t-020-rooms-x4n8 head e617951d. Partial engine scope; new vertical courses, auto-scroll and haunted mazes remain. Full CI and rendered acceptance pending.

Verified kind_robots#5861 merged at 187ed4b6 after 11/11 implementation workflows passed on a5fe62e8; branch janitor queued. Eight independently framed pipe chambers delivered. Return partial scope to ready for vertical routes, auto-scroll and haunted mazes; production deployment unverified.

Added a checkpointed forced-scroll stretch to Cottongear Coaster (4-2), 1.15px/tick, independent heroine control, front movement cap, visible and audible rear warning, life-loss and checkpoint reset, and an authored rail release. Added replay tests for lag, sprint, bounds, recovery and campaign checkpoint. Extracted committed-method probe passed (175 idle ticks to death, 321 sprint ticks to release). App branch worker/save-the-plumber-t-020-autoscroll-m7q2 head 2a8d0367. Full CI pending. Partial scope; vertical courses and haunted maze exit logic remain.

Verified kind_robots#5865 merged at 5cd16eff after all 11 implementation workflows and branch janitor completed successfully on f856915f. Coaster auto-scroll delivered. Return partial scope to ready for vertical traversal and haunted maze exit logic. Production deployment unverified.

Extended Neon Tiles (7-1) with a 224px sealed vertical chamber, 128px rope descent/ascent, intermediate ledges and three lower tokens. Retained original pipe, gear, and normal route. Added real-input regression for pipe entry, descent, reward, climb and jump back to pipe. Source geometry checks passed including preserved 32px main-route headroom and unchanged exterior. Branch worker/save-the-plumber-t-020-vertical-v9k3 head a28c63e2. Full CI pending; partial scope, haunted maze remains.

Verified kind_robots#5872 merged at 7e886a9 despite failed Maker Gameplay Contract run 45744757369: movement replay line 1097 fails on ladder descent. Reopen for urgent repair before haunted maze. The 18px heroine overlaps the ledges immediately adjacent to the 16px ladder, blocking descent. Branch janitor succeeded; production unverified.

Fixed merged vertical shaft regression by opening tiles either side of rope so the 18px heroine does not land on adjacent ledges during descent. Extracted actual updateClimb/moveY/ladder methods reproduced original failure and passed repaired descent to y=224 and ascent to y=96 (76/75 ticks). Kept full replay and added geometry assertion. Branch worker/save-the-plumber-t-020-shaft-repair-r4m8 head dfdbda93. Full CI pending. Haunted maze remains.

Verified kind_robots#5876 merged at 207116fb after 10/10 implementation workflows and branch janitor passed on dfdbda93. Full shaft replay green. Return to ready for haunted maze exit logic, final t-020 integrated acceptance. Production deployment not verified.

Implemented Drip Parlour (1-h) playable Hush House: three sealed rooms, conditional door graph with directional clues and looping wrong choices, checkpoint, normal and elevated alternate exit, independent camera framing, map unlocks and save persistence. Added overworld input regressions for false doors, normal and secret clears. Isolated committed-source geometry and all six graph transitions passed, as did actual door method probe. Branch worker/save-the-plumber-t-020-haunted-h8z4 head b244c8d4. Full CI pending; engine baseline delivered subject to integration checks, expanded authored courses and visual art remain in t-021 and later tasks.

2026-11-26 PT: kind_robots#5881 merged after pr-medic fixed its TS2532 (optional slot
secrets in verifySavePlumberOverworld.test.ts, 81aec00); TypeScript and all contract
checks green. Engine baseline complete; expanded Drip Parlour art, attic/cellar and
world variants continue in t-021.
<!-- note:end t-020 -->

## t-029 — Save the Plumber achievement upgrade: 12 or more live achievements

<!-- note:begin t-029 -->
Silas 2026-11-11 PT, in session: "Our games should all have a base standard of quality ... We want our main games to have 12 plus achievements." Standard: docs/agents/main-game-standard.md; CONTROL.md global overview.

Live today: 0 Achievement record(s) with this game's triggerCode prefix (checked against /api/achievements 2026-11-11). Target 12+ (usually 12-30; tie some to endings but don't go overboard). Mix story, skill, discovery and completion. Create the live records through the existing achievements API (label, message, icon, karma, triggerCode prefixed with the game slug), award them from the game store, show them with components/achievements/game-achievement-strip.vue, and verify one award live after deploy.

Achievement upgrade merged in kind_robots#5050 (d2de843), all checks green: 15 live arcade-prefixed achievements via a PlumberRun feat queue and mastered list (cross-session backfill; Every Heroine accumulates), Level Designer from the Maker store. Catalog run 43142839846 succeeded. Not wired: the two secret-exit achievements, because SECRET_EXITS_READY is empty so they could never be earned.
<!-- note:end t-029 -->

## t-030 — Add one water-traversal fixture that runs every heroine and the speed-route pilot through Tidecoat swimming

<!-- note:begin t-030 -->
Kaizen from the t-005 Tidecoat review (kind_robots#5899, merged baa1b62c). The Maker regression only swims the default heroine on one custom pool. Build one shared pool fixture in test:arcade-engine that runs all eight heroines (each Y special, hitbox and float) and the autopilot/speed-route pilot through dive, buoyancy, surface breach and water exit, and asserts no death, no stuck-in-tile and that unsuited heroines still die in water. Reversible test-only change unless it uncovers a defect.

Tidecoat shared pool fixture exercises every heroine, both predictive pilots, collision clearance, unsuited death, and swim exit. Fixed pilot swimming steering and surface stroke in kind_robots commit f98adccc on worker/save-the-plumber-t-030-tidecoat-8f19c2. Exact-head CI required before done.

2026-11-26 PT: PR kind_robots#5908 merged at 823dee3100d84c2f26353ac11dca8624abc967a4. All eleven implementation workflows and branch janitor completed successfully on exact head f98adccc. Shared Tidecoat fixture and predictive pilot fix satisfy t-030; no publication or deploy claimed.
<!-- note:end t-030 -->
