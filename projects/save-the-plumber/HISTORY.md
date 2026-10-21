# save-the-plumber — task history archive

Full `note:` prose for completed save-the-plumber tasks, moved out of `roadmap.yaml` so the
Kind Robots projection payload (`scripts/sync_kind_robots_projection.py`, hard limit
4,000,000 bytes) stays well clear of its ceiling. See conductor/t-158.

Each note below is the **verbatim** original — nothing is summarized or trimmed. The
`roadmap.yaml` task keeps its own first sentence plus a pointer here. The HTML comment
markers delimit each note exactly; `archive_done_task_notes.py --verify-only` re-extracts
every note and checks it byte-for-byte against what the roadmap recorded.

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
