# kr-arcade — task history archive

Full `note:` prose for completed kr-arcade tasks, moved out of `roadmap.yaml` so the
Kind Robots projection payload (`scripts/sync_kind_robots_projection.py`, hard limit
4,000,000 bytes) stays well clear of its ceiling. See conductor/t-158.

Each note below is the **verbatim** original — nothing is summarized or trimmed. The
`roadmap.yaml` task keeps its own first sentence plus a pointer here. The HTML comment
markers delimit each note exactly; `archive_done_task_notes.py --verify-only` re-extracts
every note and checks it byte-for-byte against what the roadmap recorded.

## t-002 — Curate the cabinet and launch art once it renders

<!-- note:begin t-002 -->
The scaffolding session queued the launch art as `requests:` in projects/art-prompts.yaml (ids prefixed `kr-arcade-`), targeting kind_robots public/images/arcade/. auto-art-generate.yml drains them on push and every 6 hours. This task: confirm each request reached status done and its file landed in kind_robots; view every image; re-stage (status: pending, force: true, corrected prompt) any that carry lettering, a garbled cabinet, the wrong palette, or a collage. If a request is still pending, close as a no-op re-arm rather than waiting. Generated art is pre-approved (AGENTS.md "Project art"). Also check the project icon/card/hero in projects/images/.
DONE 2026-10-06: reviewed all launch art on kindrobots.org (hall backdrop, marquee, bezel, control panel, side art, attract splash, three game title pieces) -- on-palette, lettering-free, logo androids recognisable. Re-staged two: butterfly-blaster-title (AMI rendered as the Android mascot lookalike) and cabinet-hero (garbled marquee lettering; image not yet used by the UI). Future cabinets' art is curated inside t-009 cycles.
<!-- note:end t-002 -->

## t-003 — Arcade tab + cabinet front end (hall, cabinet select, cabinet chrome, attract shell)

<!-- note:begin t-003 -->
kind_robots. Add the Arcade tab to the Projects channel: a content/channels/projects tab document, a PROJECT_PLACEMENTS entry 'kr-arcade' -> { channelKey: 'projects', tabKey: 'arcade', route: '/play/arcade' }, and the page. The page is the arcade hall (art: /images/arcade/arcade-hall-backdrop.webp) with a row of cabinets; picking one opens it in a shared <arcade-cabinet> frame (marquee, bezel around the canvas, control panel, FREE PLAY coin door) built from /images/arcade/cabinet-*.webp with a CSS fallback when art is missing. All text rendered in a pixel font over the art. Show "coming soon" cabinets for queued games. Optional CRT scanline overlay (off under prefers-reduced-motion). Then set liveUrl / channelKey / tabKey on kr-arcade in project-overrides.yaml to match. Read docs/agents/frontend-verification.md: verify phone (portrait, touch), tablet and desktop before merging. Can land before any game exists.
DONE 2026-10-06 (kind_robots#3265, merged, all 40 checks green incl. Replay migrations on MariaDB): Arcade tab (content/channels/projects/arcade.md, route /play/arcade, sort 115), cabinet + hall components, kr-arcade placement in kind_robots utils/projectPlacements.ts. Cabinets open at /play/arcade?game=<slug> because the shell header matches tabs by exact route. Correction to the original note: per kind_robots AGENTS.md, presentation fields (liveUrl/channelKey/tabKey) live in kind_robots, NOT in conductor project-overrides.yaml -- none were added there. Verified with nuxi dev + Playwright at 390/820/1440 widths.
<!-- note:end t-003 -->

## t-004 — Shared arcade engine kit (loop, input, attract/initials state machine, HUD, sound, registry)

<!-- note:begin t-004 -->
kind_robots utils/arcade/ per DESIGN-BRIEF.md "Engine kit contract": fixed-timestep loop, integer canvas scaling, unified keyboard/gamepad/touch input, BOOT->TITLE->ATTRACT->PLAYING-> GAME_OVER->INITIALS->SCORES state machine, pixel font + sprite helpers, difficulty-curve helper, WebAudio chiptune helper (muted until first interaction, persisted mute), and the games.ts registry. Unit-test the pure parts (curve, state machine, input mapping). Pure client-side; no LLM. Independent of t-003 -- either can land first.
DONE 2026-10-06 in kind_robots#3265 alongside t-003: utils/arcade/ engine kit (fixed- timestep loop, keyboard/gamepad/touch input, flow reducer, curves, 5x7 bitmap font, WebAudio sound, initials filter, registry) + utils/scripts/verifyArcadeEngine.test.ts wired into Contract verifiers.
<!-- note:end t-004 -->

## t-005 — Leaderboard: additive ArcadeScore model + scores API + initials entry

<!-- note:begin t-005 -->
kind_robots. Additive Prisma model ArcadeScore (id, gameSlug, initials char(3), score, level, userId optional FK, createdAt; index gameSlug+score desc). GET /api/arcade/scores/[game]?range=all|today (top 10) and POST /api/arcade/scores with validation: initials A-Z0-9 x3 plus a small blocklist, gameSlug in the registry, score <= maxPlausibleScore, per-IP rate limit, userId attached when signed in. Local-storage fallback board when the API fails. The migration must be CREATE TABLE / CREATE INDEX only -- Reviewer audits migration.sql line by line before merge (AGENTS.md Reviewer CAN). If the registry from t-004 has not landed yet, stub the slug list for the two launch games.
DONE 2026-10-06 in kind_robots#3265: ArcadeScore model + additive migration 20261006120000_add_arcade_scores (schema-affecting; live after the normal Alexandria deploy), GET /api/arcade/scores/:game, POST /api/arcade/scores, store-owned per-browser fallback board.
<!-- note:end t-005 -->

## t-006 — Launch game 1: Battery Maze (maze chase, riff on Pac-Man)

<!-- note:begin t-006 -->
See games.yaml battery-maze. A small kind robot gathers energy sparks through a maze while four glitch gremlins with distinct personalities (chaser, ambusher, patroller, wanderer) hunt it; a power cell turns them sleepy-blue and bumping one "reboots" it back to the charging dock. Levels raise speed and shorten power time, with a bonus item per level and an intermission every few levels. Original maze layouts. Must meet the per-game checklist in DESIGN-BRIEF.md (splash, attract, ramp, leaderboard, touch/gamepad/keyboard, sound, cabinet frame). Title-card art: /images/arcade/games/battery-maze-title.webp.
REVIEW 2026-10-06: Battery Maze built in kind_robots#3268 (maze chase, four gremlin personalities, power cells, bonus items, coffee-break intermission, maze-integrity test).
DONE 2026-10-06: kind_robots#3268 merged (all 28 checks green). Battery Maze is live at /play/arcade?game=battery-maze after the next deploy.
<!-- note:end t-006 -->

## t-007 — Launch game 2: Rescue Rally (twin-stick arena, riff on Robotron)

<!-- note:begin t-007 -->
See games.yaml rescue-rally. Move with one stick and fire a kindness beam with the other. The beam reboots glitched drones into friendly ones. Rescue wandering humans, pets and little bots for a rising multiplier. Waves add spawners, seekers and slow tanks on the difficulty curve. Touch gets dual virtual sticks. Keyboard is WASD to move and arrows to fire. Must meet the per-game checklist in DESIGN-BRIEF.md. Title-card art: /images/arcade/games/rescue-rally-title.webp.
DONE 2026-10-06: kind_robots#3269 merged (all checks green). Rescue Rally live at /play/arcade?game=rescue-rally after the next deploy. One-stick adaptation: move aims, A fires, hold B strafes; curves tuned so a perfect-aim pilot dies on wave 4-5.
<!-- note:end t-007 -->

## t-008 — Launch check, then hand the arcade to the continuous game factory

<!-- note:begin t-008 -->
Verify the whole launch on main at phone, tablet and desktop widths. Check: the hall, both cabinets, attract loops, a full game to the initials screen, the score appearing on the board, gamepad, and mute. Fix what breaks. Then carry out Silas's 2026-10-06 instruction: once the front end, leaderboard and two games exist, the arcade becomes standing "make this when you have no other task" work. Flip kr-arcade to `status: continuous` in project-overrides.yaml and add it to CONTROL.md's continuous fallback order (animation-manager, then kr-arcade, then dream-cycle). Set milestone m2 done; t-009 then unblocks through resolve_deps.py.
DONE 2026-10-06. Launch check on kind_robots main (local nuxi dev + Playwright; production deploy is still pending, so the live-site check rides the first t-009 cycle): hall shows 3 live cabinets at 390/820/1440 widths; Butterfly Blaster, Battery Maze and Rescue Rally each start and play by keyboard and by the on-screen touch controls; full loop played Butterfly Blaster to game over with 1680 points, entered initials, submitted, and (no DB in the sandbox) the score landed on the per-browser fallback board with initials remembered; the initials filter rejected XXX; no page errors, no horizontal overflow. Gamepad not exercised (no device). Flipped kr-arcade to continuous and added it to CONTROL.md's fallback order after animation-manager, per Silas's 2026-10-06 instruction.
<!-- note:end t-008 -->

## t-010 — Launch game 0: Butterfly Blaster (Asteroids riff, rainbow butterflies vs mosquitoes)

<!-- note:begin t-010 -->
Silas, 2026-10-06 (verbatim): "add one more: an Asteroids riff, but using rainbow butterflies to kill mosquitoes, a la our malaria project". See games.yaml butterfly-blaster. A rainbow butterfly rotates, flutters (thrust), drifts and wraps the screen and fires sparkles; mosquito swarms split large -> small -> single. AMI drops a bed net that works as a shield. A malaria cloud hunts the player from wave 3. Each cleared wave counts as a village protected, and game over links to https://againstmalaria.com/amibot. Must meet the per-game checklist in DESIGN-BRIEF.md. Art: /images/arcade/games/butterfly-blaster-title.webp.
DONE 2026-10-06 in kind_robots#3265: Butterfly Blaster shipped as the first live cabinet (/play/arcade?game=butterfly-blaster). Title art request queued via conductor#5638.
<!-- note:end t-010 -->

## t-011 — Global leaderboard for every game: hall of fame + guaranteed uploads

<!-- note:begin t-011 -->
Silas, 2026-10-06 (verbatim): "global leaderboard is a high priority for all games". The per-game boards were already global and live (ArcadeScore + /api/arcade/scores, checked in production). DONE in kind_robots#3277: GET /api/arcade/leaderboard (hall of fame for every registered cabinet: top 3, today's best, scores on the board; new cabinets join automatically), a Hall of Fame section in the hall, and a pending-upload queue so a score that fails to post retries until it reaches the global board instead of staying in one browser. The per-game checklist in DESIGN-BRIEF.md now requires every cabinet to post through the arcade store. zuzu-lair/t-009 reuses the same board.
<!-- note:end t-011 -->

## t-012 — Resolution system + render styles for every cabinet (pixel / HD / fun extras), pinball first

<!-- note:begin t-012 -->
Silas, 2026-10-06 PT (verbatim): "as a note: our original arcade uses a very slimmed down resolution...we should both be able to upgrade that anyway (pixel is a style choice, users should be able to select pixel or hd or others if they are fun), but after working with pinball, it's clear we also need a much better resolution system for the higher quality games". Today: each game declares a small logical size (320x240 is the most common; the largest are 480x360 and 288x488), arcade-cabinet.vue sizes the canvas to its box at up to 2x DPR and scales the logical drawing up. Vector drawing is sharp, but art, pixel fonts and pre-rendered layers are authored at the logical size, so nothing can gain detail, and a game cannot be "HD". Build one display layer the cabinet (and the stand-alone games: Zuzu Showdown, pinball) share: (1) logical world size stays per game, separate from the render target; (2) render styles chosen by the player -- Pixel (logical size x the largest integer scale that fits, nearest filtering, pixel font), HD (device resolution, smooth filtering, HD art, a vector font), and room for fun extras (CRT scanlines, the pinball DMD look); (3) assets keyed by style, so a game ships HD masters and a derived pixel set (zuzu-showdown t-007's pipeline does the derivation); (4) one arcade display preference in a Pinia store (the store owns localStorage), with a per-game override; (5) DPR cap raised or made per-style so HD is crisp on 3x phones without melting low-end ones. Pinball is the motivating case and the first heavy consumer; port two existing cabinets as proof. Done when the cabinet shows the style picker, two cabinets plus pinball render in Pixel and HD, a contract test covers the transform math (logical to canvas at DPR 1/2/3, integer pixel scale, letterboxing), and DESIGN-BRIEF.md's engine-kit contract documents it.
DONE 2026-10-09: shared display layer (utils/arcade/display.ts: Pixel/HD fit, MAX_DPR 3), cabinet style picker with per-game override in arcadeStore (kind_robots#3386, #3350), pinball takes dpr 1 in Pixel and device ratio in HD, contract test verifyZuzuShowdownDisplay covers fit at DPR 1/2/3, engine-kit contract documented (#5808). CRT scanlines already a separate cabinet toggle.
<!-- note:end t-012 -->

## t-013 — Ghost Trail art references: inspect nine ArtJobs and produce playable Zuzu/enemy sprite atlases

<!-- note:begin t-013 -->
2026-10-10: Silas accepted the moonlit town, haunted ravine, and Bell Heretic mockups as the new finish line. Use ghost-trail/CAMPAIGN-BLUEPRINT.md. Nine reference requests queued in projects/art-prompts.yaml (kr-arcade-ghost-trail-*). Check actual ArtJob IDs, delivered URLs and visual quality, repair bad art, create Zuzu and bone-coyote animation atlases with pivots and the intact/exposed poncho states using the Zuzu Showdown rig pipeline. Keep vector fallback until assets work in-game.
DONE 2026-10-10: all nine ArtJobs verified delivered at their final URLs (6 plates 1280x960, 3 concepts 1024x1024; inspected, quality good). Instead of rigging atlases from the single-pose concepts, Zuzu, the foes and bosses are drawn by code at high density (utils/arcade/ghostTrail/heroArt.ts, foeArt.ts) via bake.ts, with full animation sets incl. intact/exposed poncho states; the plates are used directly as the far layer (stageArt.ts). The Zuzu Showdown rig was inspected and not reused: its fighter stance and headband do not match Ghost Trail's kasa/poncho canon. silasfelinus/kind_robots#3466.
<!-- note:end t-013 -->

## t-014 — Ghost Trail visual vertical slice: large sprites, parallax town and detailed HUD

<!-- note:begin t-014 -->
Replace tiny vector hero/enemies and repetitive color blocks in stage 1 with 40–48px readable Zuzu, real sprite animation, three-layer parallax, hand-built gameplay tiles, clear collision silhouettes, boss telegraph animations, coordinated Pixel/HD masters and HUD. Keep the accepted title splash, cabinet and leaderboard. Verify real screenshot renders at phone/tablet/desktop widths and pixel/HD modes.
2026-10-10: vertical slice in silasfelinus/kind_robots#3466 -- delivered plates as panned far layers + procedural parallax midground, fog and animated lights; hand-built terrain matching collision per stage; canon Zuzu with idle/walk/jump/fall/throw/iai-cut in both poncho states (~30 px, matching mockup scale and hurtboxes); bone coyotes, ghosts, storm crows, Dust Devil and Bone Bull with clear telegraphs; mockup HUD with bottom boss bar and banners. Render only. Verified engine/farm/campaign tests, vue-tsc, HD 4x and Pixel renders. Device widths: the cabinet's display layer only changes the whole-number scale, and renders were checked at 1x/2x Pixel and 4x HD; a hands-on phone pass in the live cabinet is still worth doing in t-020. The Bell Heretic itself is a t-018 boss.
<!-- note:end t-014 -->

## t-015 — Ghost Trail authored encounter and campaign systems: secrets, progress, checkpoints and victory

<!-- note:begin t-015 -->
Implement data-defined finite encounters (no idle score farming), two acts per stage, authored branches, unique loot/secret keys, checkpoint semantics, saved/resumable progress and real credits/victory instead of endless loops. Preserve seed-deterministic updates, input abstraction, hit/poncho mechanic and score API.

First incremental campaign-system slice: four one-time stage relic discoveries with checkpoint-safe rewards, a finite victorious preview ending, and deterministic tests. The six-stage Act I, authored encounters, save/resume and full ten-hour campaign remain follow-up work.

PARTIAL SLICE SHIPPED 2026-10-10 PT: kind_robots#3450 merged after 29/29 completed CI workflows passed. Four reachable one-time relics now survive checkpoint retries, the HUD tracks relics, and the fourth current trail has a visible three-second PREVIEW CLEARED victory before leaderboard handoff. New tests added to test:arcade-engine and passed. conductor#5900 merged after all CI, recording Silas's ten-hour five-book north star in CONTROL.md and ghost-trail/TEN-HOUR-ROADMAP.md. REMAINING t-015: data-driven authored encounters, two acts per stage, branches, save/resume/checkpoint persistence and a six-stage Act I ending. Do not mark done or unblock dependent tasks yet.

DONE 2026-10-10: the campaign engine shipped in silasfelinus/kind_robots#3469 and #3470. Data-defined acts (ghostTrail/world.ts, campaign.ts, acts/stage1-6.ts) with ground/pits, ledges, solid blocks, movers, timed hazards, updrafts and a tide; finite authored squads with stable member ids and a run-wide defeated ledger (death and checkpoint retries never revive them; ambush camera locks); the progress-gated ambient budget kept (farm test still passes); 2-3 acts per stage with multiple checkpoints and authored branches (rooftop vs street, tide passages, high routes); unique relic ids; title cards, stage pages, credits and a real victory. Save/resume: saves at each act start through the arcade store (utils/arcade/saves.ts), CONTINUE / NEW RUN card, continues after a game over keep relics but not score. New Game+ unlocks on a clear, and finding every relic earns the true ending. Tests: verifyZuzuGhostTrailCampaign.test.ts.
<!-- note:end t-015 -->

## t-016 — Ghost Trail stage 1: Silver Gulch authored encounter graph and Grave Marshal boss

<!-- note:begin t-016 -->
Ship two long real gameplay acts, hidden saloon crawlspace, rooftop/street split, Grave Marshal multi-tell boss and level complete/return path. Verify encounter budgets, secret accessibility and 9–11 minute target before declaring stage done.
DONE 2026-10-10 (content): Stage 1 shipped in silasfelinus/kind_robots#3473 -- s1a1 MAIN STREET (tutorial street, 6400 px, 13 squads) and s1a2 THE COURTHOUSE (7000 px, 15 squads, rooftop/street split, saloon crawlspace relic) ending at the Grave Marshal (#3471: cover, two telegraphed bullet lanes, dynamite, deputies; boss test). Bot (endless lives) clears both acts. NOT VERIFIED: the 9-11 minute human target -- bot times are not human first-clear times; the timed playtest is carried by t-020.
<!-- note:end t-016 -->

## t-017 — Ghost Trail stages 2–3: Bone Yard, Drowned Watering Hole and unique bosses

<!-- note:begin t-017 -->
Bone Yard vertical haunted ravine/crypts with Bone Bull and bell sigil; water-level/raft/secrets at the Drowned Watering Hole and Drowned Ferryman boss; River Croc cameo/conditional ally. Distinct authored geometry, enemies and backgrounds, not colored copies of Stage 1.
DONE 2026-10-10 (content): Stage 2 (Bone Yard: crypts with spikes and tomb ambushes; the Broken Bridge with 24 pits, terraces, beams and bell lifts; first bell sigil relic; Bone Bull) in silasfelinus/kind_robots#3473, and Stage 3 (Drowned Watering Hole: telegraphed tide cycles, rafts, a crypt passage walkable only at low tide, ferry escape run; Drowned Ferryman with two water phases, #3471) in #3479. River Croc does not appear as an enemy (the cameo/ally idea is not built). Painted roster for the new foes in #3471. Bot clears every act. NOT VERIFIED: human stage times (t-020).
2026-10-11: River Croc built as the blueprint's conditional ally (silasfelinus/kind_robots#3496): in s3a2 he surfaces only once the squad bothering him is down and ferries Zuzu across a pool too wide to jump; he never hurts Zuzu.
<!-- note:end t-017 -->

## t-018 — Ghost Trail stages 4–5: Storm Crow Pass and Mission Bell Tower

<!-- note:begin t-018 -->
Wind, updrafts, lightning tells, canopy passage and Storm-Crow Matriarch boss; stone bell lifts/rope puzzle/burning braziers and giant Bell Heretic fight. Match accepted screen concepts without breaking readable hitboxes.
DONE 2026-10-10 (content): Stage 4 Storm Crow Pass (updraft columns tuned to settle, rope lifts, canopy, cave cache, Dust Devil mid-boss, Storm-Crow Matriarch with perches, summons and armed lightning) in silasfelinus/kind_robots#3479; Stage 5 Mission Bell Tower (stairways, bell lifts, timed braziers, falling-masonry ambushes, the Bell Order relic climb) in #3474 and the Bell Heretic (chained bell swing, slam waves, ritual circles, masonry, robe-fire phase) in #3476. New stormpass art world in #3473. Lightning as a stage hazard (separate from the Matriarch) is not built. NOT VERIFIED: human stage times (t-020).
2026-10-11: lightning as a Storm Crow Pass stage hazard with a 40-tick tell, and a second vertical act, THE CLIFF ROAD (Stage 4 act 3, ~956 px of climb), in silasfelinus/kind_robots#3497. Stage 5 also gained the vertical act THE BELL STAIR (#3488).
<!-- note:end t-018 -->

## t-019 — Ghost Trail final stage: Abbey undercrypt, Abbess finale and alternate ending

<!-- note:begin t-019 -->
Connect the cosmic-horror ritual plot to the established Zuzu canon. Build two final boss phases, ending and credit sequence, optional rescue, relic-dependent secret ending and unlockable New Game+. The first clear must end the campaign rather than silently wrap back to Ghost Town.
DONE 2026-10-10 (content): Stage 6 The Abbey Beneath the Bell (three acts, 8000-9000 px, ritual tunnels, wind shafts, ambushes in series, six lore relics) in silasfelinus/kind_robots#3474; the Abbess final boss with two real phases (a refusal of death, transformation and refilled bar) in #3476; ending page and credits roll in #3474; the run ends the campaign (no wrap to Ghost Town); relic-dependent true ending and New Game+ in #3470; abbey art world in #3473. Not built: the optional rescue. NOT VERIFIED: human stage times (t-020).
2026-10-11: the optional rescue is built (silasfelinus/kind_robots#3496): a caged novice in s6a1 freed by breaking the lock and clearing the ambush it springs; a freed novice adds lines to the ending and is saved with the run.
<!-- note:end t-019 -->

## t-021 — Upgrade the next cabinet to the 16-bit (Super NES) style (recurring, ahead of new games)

<!-- note:begin t-021 -->
Silas, 2026-10-10 (verbatim): "for now, we have a lot of arcade games, and I appreciate the variety. I want to make one excision. the request timber falling game is questionable ethics, and I think we should kill it. beyond that, rather than focusing on building new games (though I do want knew games to come in, I want games to get style upgrades. Right now they all look like they could have come from an atari, and I want Super nes."
STANDING CONTRACT: fallback work for kr-arcade, taken BEFORE t-009's new-game cycles. Each cycle upgrades one shipped cabinet whose games.yaml row has no `style: snes`, in games.yaml order (skip `retired` rows and the WebGL pinball table). Rebuild its render pass on kind_robots utils/arcade/snes.ts to meet every point of DESIGN-BRIEF.md "16-bit style bar"; extend the kit when a cabinet needs something shared (parallax for a scroller, Mode-7 floors) rather than drawing a one-off. Render only: gameplay, the seeded rng, scores and difficulty curves stay as they are (cosmetic effects roll their own dice, as Sink Suds' sparkles do). Verify with test:arcade-engine, eslint/prettier, vue-tsc, and before/after screenshots of the attract demo, checking both Pixel and HD styles; attach them to the PR. Then set the row's `style: snes` and `style_in: <PR>` and re-arm here with a RAN <date> line. Big cabinets (Kindness Gauntlet, Station Sweep, Zuzu Ghost Trail) may take two cycles; Ghost Trail's visual work lives in m5 (t-013/t-014), so it counts as upgraded when t-014 lands. Done when every non-retired 2D cabinet is `style: snes`; then flip to done and close m6.
RAN 2026-10-10: kit built (snes.ts: 15-bit ramps, HDMA bands, outlined pixel sprites, orbs, bevels, glows, sparkles, parallax, HUD panels, cached layers; font outline) and Sink Suds upgraded first, in silasfelinus/kind_robots#3438, which also retires Timber Bot. Next in order: butterfly-blaster.
RAN 2026-10-10: batch 1 (Silas: "keep going, upgrade each until completed") -- Butterfly Blaster, Battery Maze, Rescue Rally, Pipe Pals, Butterfly Joust, Gloom Invaders, Hedgehog Crossing upgraded in silasfelinus/kind_robots#3451 (render only; seeded play verified unchanged). Batches 2-4 in flight in the same session.
RAN 2026-10-10: batch 2 -- Ribbon Riders, Burrow Buddy, Repair Rampage, Prize Show Panic, Rain Catcher, Brick Bloom, Seed Lander upgraded in silasfelinus/kind_robots#3453 (render only; three verified tick-for-tick against origin/main).
RAN 2026-10-10: batches 3-5 -- Pixel Hop, Glitch Garden, Quilt Quest, Cocoa Counter, Seed Burst, Lantern Swarm (silasfelinus/kind_robots#3454); Rover Ramble, Cable Crawler, Petal Post, Bumper Bubbles (#3455); Kindness Gauntlet, Station Sweep (#3456). Render only, with tick-for-tick parity runs against origin/main on eight cabinets.
DONE 2026-10-10: every 2D cabinet the contract covers is `style: snes` (27 of them, Sink Suds included). Two carry-outs, per the contract: Zuzu: Ghost Trail's visual upgrade is m5 t-013/t-014; Kind Pinball's WebGL table was never in scope, and its rarely seen 2D no-WebGL fallback is follow-up t-022. New cabinets (t-009) ship at the 16-bit bar.
<!-- note:end t-021 -->

## t-022 — 16-bit pass for Kind Pinball's 2D fallback table (devices without WebGL)

<!-- note:begin t-022 -->
Follow-up from t-021 (2026-10-10). The hall plays Kind Pinball as the WebGL 3D table; utils/arcade/games/kindPinball.ts (Canvas 2D, ~2300 lines) is only served where WebGL is missing, and still has the flat early look. Give it the DESIGN-BRIEF.md "16-bit style bar" render pass on utils/arcade/snes.ts, render only, the same way the other 26 cabinets were done (the session's brief and screenshot harness are described in t-021's notes). Low priority: few players ever see this table. Then set kind-pinball's games.yaml row `style: snes` and close m6.

2026-10-11 PT: SNES render-only pass for the Canvas pinball fallback is committed on worker/kr-arcade-t-022-20261011T211248Z-3m8n, alongside the games.yaml style marker. Companion PRs will follow after this review transition is verified.

2026-10-11 PT: Canvas Kind Pinball fallback SNES render-only pass merged in silasfelinus/kind_robots#3538 (commit 43a4c137), followed by catalog style marker silasfelinus/conductor#5993 (commit 78f20a76). Initial Prettier ratchet identified the modified file; formatting follow-up passed. Final implementation CI: 27 of 27 checks completed successfully. No production deployment or human visual acceptance is claimed.
<!-- note:end t-022 -->

## t-023 — Pipe Pals depth slice 1: bigger actors, recovery tiers, chains, kick bowling, turnaround and the tool belt

<!-- note:begin t-023 -->
ASSESSMENT.md section 1, "Systems that run through the whole campaign" plus the first new threats. Bigger actors (hero ~24-28 px, critters ~18-22 px, 3+ walk frames, flip/kick squash); calm/cross/furious recovery tiers and a last-critter rush; walkers turn round when they meet; kick chains 800/1600/2400/3200/5000; kick bowling; a coin out of a pipe on every kick; the Tool Belt pickups (Wide Wrench, Kick Boots, Bubble Wand, Magnet Cap); the spring flea, shell knight and the ember spark / lurker ember pair, used in the current board until t-024 brings districts. Pipe Pals goes first: Silas called it the weaker riff. Silas, 2026-10-11: "We don't need to be 1:1 copies of these games, but we should be equally complex or more so", then on the plan: "expand both pitches to add even more to each, so we really are homages with even more inspired levels and gameplay depth." Spec: projects/kr-arcade/depth-pass/ASSESSMENT.md (read the game's section first). Riff on mechanics only; original layouts, names and lines; cartoon bonk/cheer only; no real money, no runtime LLM. Gameplay changes ARE in scope here (unlike t-021). Keep the 60 Hz seeded simulation, the score API and the attract pilot working (update the pilot for new mechanics). Content is data (district/episode/room definitions), not branches in the update loop. Verify: test:arcade-engine plus a deterministic campaign test, eslint/prettier, vue-tsc, Pixel and HD screenshots on the PR, and a pilot probe that shows runs still end.
DONE 2026-10-11: silasfelinus/kind_robots#3512 merged after all 30 CI checks passed. Bigger actors (pal ~24 px, critters ~20 px, 3 walk frames + squash), calm/cross/furious tiers and last-critter rush, walker turnaround, kick chains 800..5000, kick bowling, a coin on every kick, spring flea and shell knight, ember sparks and lurker embers snuffed from below, the tool belt (Wide Wrench, Kick Boots, Bubble Wand on B, Magnet Cap), KIND block refills, new utils/scripts/verifyPipePals.test.ts in test:arcade-engine. Pilot probe with endless lives: phases 11-16 in 20 min, every mechanic exercised.
<!-- note:end t-023 -->

## t-024 — Pipe Pals depth slice 2: Day Shift -- Rooftop Reservoir, Greenhouse Mains, Suds Works, the Big Shell and the Workshop

<!-- note:begin t-024 -->
ASSESSMENT.md section 1, Shift 1. The data-defined district engine (board segments incl. vine/sagging and soapy ledges, lifts, backdrop, tiles, roster, curves, special phase, bonus twist, title card); 5 phases + bonus per district; the special phases First Fix, Seedling Rescue and Lost Socks; lint moth, sock puppet and bubble traps; the Big Shell boss (tip-and-kick, shed crawlers, rolling final phase); the Workshop between districts (coin-priced extra pal, KIND charge, starting tool, Lucky Pipe, valve hint); golden valve handles placed for districts 1-3. Silas, 2026-10-11: "We don't need to be 1:1 copies of these games, but we should be equally complex or more so", then on the plan: "expand both pitches to add even more to each, so we really are homages with even more inspired levels and gameplay depth." Spec: projects/kr-arcade/depth-pass/ASSESSMENT.md (read the game's section first). Riff on mechanics only; original layouts, names and lines; cartoon bonk/cheer only; no real money, no runtime LLM. Gameplay changes ARE in scope here (unlike t-021). Keep the 60 Hz seeded simulation, the score API and the attract pilot working (update the pilot for new mechanics). Content is data (district/episode/room definitions), not branches in the update loop. Verify: test:arcade-engine plus a deterministic campaign test, eslint/prettier, vue-tsc, Pixel and HD screenshots on the PR, and a pilot probe that shows runs still end.
DONE 2026-10-11: silasfelinus/kind_robots#3514 merged after all CI passed. Data-defined districts (utils/arcade/pipePals/districts.ts, scenes.ts): Rooftop Reservoir, Greenhouse Mains (sagging vines, top-gap trolley lift), Suds Works (soapy ledges blow trapping bubbles); First Fix, Seedling Rescue and Lost Socks special phases earning golden valves; static/sprinkler/bubble bonus twists; lint moth and sock puppet; the Big Shell boss; the Workshop (coin-priced extra pal, KIND charge, starting tool, Lucky Pipe, valve hint); district title cards. Probes fixed an unbumpable leak, a greenhouse layout that dropped critters to the bottom floor, and fleas that never left the bottom floor.
<!-- note:end t-024 -->

## t-025 — Pipe Pals depth slice 3: Swing Shift -- Cold Storage, Boiler Works, Clockwork Water Tower and the Thermostat

<!-- note:begin t-025 -->
ASSESSMENT.md section 1, Shift 2. Icy low-friction ledges, icicles, frost bot, snowball roller, Thaw Run; steam vents, crumble ledge, Pressure Valves; gear and conveyor ledges, gear bug, cuckoo, Valve Routing (switchable pipe routes); the Thermostat boss (FREEZE/HEAT dial, bump the lit ledge, three phases); golden valves for districts 4-6. Silas, 2026-10-11: "We don't need to be 1:1 copies of these games, but we should be equally complex or more so", then on the plan: "expand both pitches to add even more to each, so we really are homages with even more inspired levels and gameplay depth." Spec: projects/kr-arcade/depth-pass/ASSESSMENT.md (read the game's section first). Riff on mechanics only; original layouts, names and lines; cartoon bonk/cheer only; no real money, no runtime LLM. Gameplay changes ARE in scope here (unlike t-021). Keep the 60 Hz seeded simulation, the score API and the attract pilot working (update the pilot for new mechanics). Content is data (district/episode/room definitions), not branches in the update loop. Verify: test:arcade-engine plus a deterministic campaign test, eslint/prettier, vue-tsc, Pixel and HD screenshots on the PR, and a pilot probe that shows runs still end.
DONE 2026-10-11: silasfelinus/kind_robots#3515 merged after all CI passed. Swing Shift: Cold Storage (ice ledges, icicles, frost bots, snowballs, Thaw Run), Boiler Works (steam vents, crumble ledge, thicker embers, Pressure Valves), Clockwork Water Tower (conveyors, gear ledges, gear bugs, the cuckoo, Valve Routing); ice/steam/gear bonus twists; the Thermostat boss. Difficulty now keyed to district+phase; walker speed capped at 2.5 px/tick.
<!-- note:end t-025 -->

## t-026 — Prize Show Panic depth slice 1: season map engine, authored rooms and modifiers, Episode 1 Opening Night, golden tickets

<!-- note:begin t-026 -->
ASSESSMENT.md section 2, "Structure", room types and modifiers, and episode 1. Data-defined episodes of 12-14 rooms on a grid; the map screen (visited rooms, what each door leads to, danger rating and reward icons, chosen route; a safe and a rich branch side by side); room scripts replacing the random spawn stream; all ten room types incl. sponsor challenges and secret rooms; the six modifiers; golden ticket placement. Episode 1 Opening Night fully authored with the Parade Float (now two phases) as its mid-boss; the Big Wobble lands in t-029. Silas, 2026-10-11: "We don't need to be 1:1 copies of these games, but we should be equally complex or more so", then on the plan: "expand both pitches to add even more to each, so we really are homages with even more inspired levels and gameplay depth." Spec: projects/kr-arcade/depth-pass/ASSESSMENT.md (read the game's section first). Riff on mechanics only; original layouts, names and lines; cartoon bonk/cheer only; no real money, no runtime LLM. Gameplay changes ARE in scope here (unlike t-021). Keep the 60 Hz seeded simulation, the score API and the attract pilot working (update the pilot for new mechanics). Content is data (district/episode/room definitions), not branches in the update loop. Verify: test:arcade-engine plus a deterministic campaign test, eslint/prettier, vue-tsc, Pixel and HD screenshots on the PR, and a pilot probe that shows runs still end.
DONE 2026-10-11: silasfelinus/kind_robots#3516 merged after all CI passed. Data-defined season (utils/arcade/prizeShow/season.ts) with Episode 1 Opening Night: 13 rooms on a 5x3 grid with safe/rich forks and an off-map Backstage secret; map screen between rooms (prizeShow/mapScreen.ts); all ten authored room types incl. mine sets, light rig, camera wall, vault, sponsor challenge; six modifiers; golden tickets (12 in the season, 10 open the vault later); Parade Float second phase; Encore loops so runs end. New verifyPrizeShowPanic.test.ts.
<!-- note:end t-026 -->

## t-027 — Prize Show Panic depth slice 2: the 19-crasher roster, the 10-item arsenal and true twin-stick aim

<!-- note:begin t-027 -->
ASSESSMENT.md section 2, roster and arsenal tables, the boom mic hazard and the twin-stick bullet. All new crashers with their tells, the seven new power-ups with stacking HUD timers. Engine: an optional aim vector on InputFrame (gamepad right stick axes 2/3, a second touch stick, split keyboard), shared through utils/arcade/input.ts so Kindness Gauntlet and Rescue Rally can adopt it; hold-B lock stays for single-stick players; input contract tests. Silas, 2026-10-11: "We don't need to be 1:1 copies of these games, but we should be equally complex or more so", then on the plan: "expand both pitches to add even more to each, so we really are homages with even more inspired levels and gameplay depth." Spec: projects/kr-arcade/depth-pass/ASSESSMENT.md (read the game's section first). Riff on mechanics only; original layouts, names and lines; cartoon bonk/cheer only; no real money, no runtime LLM. Gameplay changes ARE in scope here (unlike t-021). Keep the 60 Hz seeded simulation, the score API and the attract pilot working (update the pilot for new mechanics). Content is data (district/episode/room definitions), not branches in the update loop. Verify: test:arcade-engine plus a deterministic campaign test, eslint/prettier, vue-tsc, Pixel and HD screenshots on the PR, and a pilot probe that shows runs still end.
Merged as kind_robots#3518: the 19-crasher roster with tells and answers (poppers through fluffballs, mascot mini-boss, camera cranes unified with the camera wall), the boom mic, the 10-item arsenal with stacking timed powers, and opt-in twin-stick aim (InputFrame.aim, right stick, on-screen aim stick, WASD+arrows). Touch aim stick still needs an on-device look.
<!-- note:end t-027 -->

## t-028 — Prize Show Panic depth slice 3: the host and co-host, the ratings meter, cheer chains, prize tally, Prize Swap and the studio audience

<!-- note:begin t-028 -->
ASSESSMENT.md section 2, "The show". Host portrait with original speech-panel lines and style reactions, the dry co-host from episode 3, WebAudio bleep-speak (no speech synthesis, no LLM); the four-tier ratings meter with multiplier, sponsor care packages and plot twists; cheer chains; the end-of-episode prize tally screen and the season haul on game over; the Prize Swap (in-game prizes only); APPLAUSE sign, audience band and camera-flash juice. Host art can be a pixelSprite portrait; if generated art is used, queue it as a kr-arcade- request and verify the delivered URL. Silas, 2026-10-11: "We don't need to be 1:1 copies of these games, but we should be equally complex or more so", then on the plan: "expand both pitches to add even more to each, so we really are homages with even more inspired levels and gameplay depth." Spec: projects/kr-arcade/depth-pass/ASSESSMENT.md (read the game's section first). Riff on mechanics only; original layouts, names and lines; cartoon bonk/cheer only; no real money, no runtime LLM. Gameplay changes ARE in scope here (unlike t-021). Keep the 60 Hz seeded simulation, the score API and the attract pilot working (update the pilot for new mechanics). Content is data (district/episode/room definitions), not branches in the update loop. Verify: test:arcade-engine plus a deterministic campaign test, eslint/prettier, vue-tsc, Pixel and HD screenshots on the PR, and a pilot probe that shows runs still end.
Merged as kind_robots#3520: host TINSEL and co-host LENS cut-ins (15 cues, original lines, bleep-speak, own cosmetic rng), the four-tier ratings meter with care packages and Off Air plot twists, cheer chains to x4 with the APPLAUSE sign, the studio audience, the between-episode prize tally and Prize Swap, and the game-over season haul.
<!-- note:end t-028 -->

## t-029 — Prize Show Panic depth slice 4: Episodes 2-3 -- Cooking Showdown and Countdown Concert, their sets, mid-bosses and bosses

<!-- note:begin t-029 -->
ASSESSMENT.md section 2, episodes 2-3 and bosses 2-6. Hot-plate tiles, flour clouds, conveyor counters; beat-synced speaker bass rings, strobes and mosh pits; the Big Wobble (episode 1 boss), the Pie Cart, the Soufflé Supreme (rise/fall, cupcake split), the Mosh Mascot and the Jumbotron. Each set with its own palette, props and music loop. Silas, 2026-10-11: "We don't need to be 1:1 copies of these games, but we should be equally complex or more so", then on the plan: "expand both pitches to add even more to each, so we really are homages with even more inspired levels and gameplay depth." Spec: projects/kr-arcade/depth-pass/ASSESSMENT.md (read the game's section first). Riff on mechanics only; original layouts, names and lines; cartoon bonk/cheer only; no real money, no runtime LLM. Gameplay changes ARE in scope here (unlike t-021). Keep the 60 Hz seeded simulation, the score API and the attract pilot working (update the pilot for new mechanics). Content is data (district/episode/room definitions), not branches in the update loop. Verify: test:arcade-engine plus a deterministic campaign test, eslint/prettier, vue-tsc, Pixel and HD screenshots on the PR, and a pilot probe that shows runs still end.
Merged as kind_robots#3522: Episode 2 Cooking Showdown and Episode 3 Countdown Concert with their sets, hazards (hot plates, flour clouds, conveyors; bass rings, strobes, mosh pits) and music loops; bosses the Big Wobble, the Pie Cart, the Souffle Supreme, the Mosh Mascot and the Jumbotron; LENS now joins on Episode 3. Real-run bound raised to 75 min for three episodes.
<!-- note:end t-029 -->

## t-030 — Pipe Pals depth slice 4: Night Shift -- Flooded Mains, Storm Drain, the Clog King and the flush, the Golden Main, endings, save/resume

<!-- note:begin t-030 -->
ASSESSMENT.md section 1, Shift 3, finale and secret district. Rising/draining water with underwater movement and bobbing flipped critters, pipe eel, bubble jelly, Pump Station; the dim board with lamp pools and lightning tells, grease beetle, mimic coin, Lights Out; the Clog King in three phases plus the rooftop escape climb; golden valves 7-8 and the Golden Main secret district with the true ending; credits and Overtime NG+; saves at each district start via utils/arcade/saves.ts (Ghost Trail is the reference). Target: first clear 45-60 minutes. Silas, 2026-10-11: "We don't need to be 1:1 copies of these games, but we should be equally complex or more so", then on the plan: "expand both pitches to add even more to each, so we really are homages with even more inspired levels and gameplay depth." Spec: projects/kr-arcade/depth-pass/ASSESSMENT.md (read the game's section first). Riff on mechanics only; original layouts, names and lines; cartoon bonk/cheer only; no real money, no runtime LLM. Gameplay changes ARE in scope here (unlike t-021). Keep the 60 Hz seeded simulation, the score API and the attract pilot working (update the pilot for new mechanics). Content is data (district/episode/room definitions), not branches in the update loop. Verify: test:arcade-engine plus a deterministic campaign test, eslint/prettier, vue-tsc, Pixel and HD screenshots on the PR, and a pilot probe that shows runs still end.
Merged as kind_robots#3517: Flooded Mains and Storm Drain at Midnight (tide, eels, jellies, dark board, lamps, beetles, mimics), Pump Station and Lights Out, the three- phase Clog King and the flush, endings, the Golden Main and true ending, and district- start saves with CONTINUE/NEW RUN.
<!-- note:end t-030 -->

## t-031 — Pipe Pals depth slice 5: two pals with their own feel, co-op and Versus, Overtime and Time Trial modes, medals

<!-- note:begin t-031 -->
ASSESSMENT.md section 1, last bullets of "Systems". Teal pal (longer bump reach) and pink pal (higher, floatier jump), selectable solo; same-device co-op through the cabinet players frames; Versus with playful bump-steals; Overtime endless score attack as the leaderboard main event; per- district Time Trial; Clean Sweep / Chain Master / Swift Fix medals with a medal board. Then update games.yaml (drop the old co-op/icy-platform follow-up comment) and the registry howTo. Silas, 2026-10-11: "We don't need to be 1:1 copies of these games, but we should be equally complex or more so", then on the plan: "expand both pitches to add even more to each, so we really are homages with even more inspired levels and gameplay depth." Spec: projects/kr-arcade/depth-pass/ASSESSMENT.md (read the game's section first). Riff on mechanics only; original layouts, names and lines; cartoon bonk/cheer only; no real money, no runtime LLM. Gameplay changes ARE in scope here (unlike t-021). Keep the 60 Hz seeded simulation, the score API and the attract pilot working (update the pilot for new mechanics). Content is data (district/episode/room definitions), not branches in the update loop. Verify: test:arcade-engine plus a deterministic campaign test, eslint/prettier, vue-tsc, Pixel and HD screenshots on the PR, and a pilot probe that shows runs still end.
Merged as kind_robots#3519: teal (longer bump reach) and pink (higher, floatier jump) pals chosen on a mode menu; same-device co-op (maxPlayers 2, shared pool of 6, partner bonks); Versus (one district, own tallies, STEAL!, fall costs points, winner card); Overtime endless score attack; per-district Time Trial with saved best times; Clean Sweep / Chain Master / Swift Fix medals (135) with a medal board, all kept in the save. Completes the Pipe Pals depth pass.
<!-- note:end t-031 -->

## t-032 — Prize Show Panic depth slice 5: Episode 4 Galaxy Parade, the Live Finale, the Grand Prize Vault, endings and save/resume

<!-- note:begin t-032 -->
ASSESSMENT.md section 2, episode 4, the Live Finale and bosses 7-9. Low-gravity momentum rooms, the rotating ring room, teleport doors; the Saucer Cam Mothership and the Conga Dragon; the Live Finale run with the Host's Prize Machine (wheel-chosen attack sets, telegraphed next spin, the host's dance-off last phase); the Grand Prize Vault for ten golden tickets and the true ending; credits, Rerun unlock, saves at each episode start. Target: first clear 60-75 minutes. Silas, 2026-10-11: "We don't need to be 1:1 copies of these games, but we should be equally complex or more so", then on the plan: "expand both pitches to add even more to each, so we really are homages with even more inspired levels and gameplay depth." Spec: projects/kr-arcade/depth-pass/ASSESSMENT.md (read the game's section first). Riff on mechanics only; original layouts, names and lines; cartoon bonk/cheer only; no real money, no runtime LLM. Gameplay changes ARE in scope here (unlike t-021). Keep the 60 Hz seeded simulation, the score API and the attract pilot working (update the pilot for new mechanics). Content is data (district/episode/room definitions), not branches in the update loop. Verify: test:arcade-engine plus a deterministic campaign test, eslint/prettier, vue-tsc, Pixel and HD screenshots on the PR, and a pilot probe that shows runs still end.
Merged as kind_robots#3523: Episode 4 Galaxy Parade (low-gravity rooms, the turning ring, teleport doors), the Saucer Cam Mothership and the Conga Dragon, the Live Finale with the Host's Prize Machine (wheel of attack sets, dance-off), the Grand Prize Vault for ten golden tickets, both endings and credits, the Rerun loop, and saves at each episode start with a continue card. Commercials! is a placeholder prize room until t-033.
<!-- note:end t-032 -->

## t-033 — Prize Show Panic depth slice 6: commercial-break mini-games, four contestants and co-op for up to four

<!-- note:begin t-033 -->
ASSESSMENT.md section 2, commercial breaks and contestants. Spin the Wheel, Catch the Prizes, Pie Dodge and Higher or Lower between episodes; Sparkle, Zippy, Boomer and Glimmer with their own sprites and feel; up to four contestants through the cabinet players frames. Silas, 2026-10-11: "We don't need to be 1:1 copies of these games, but we should be equally complex or more so", then on the plan: "expand both pitches to add even more to each, so we really are homages with even more inspired levels and gameplay depth." Spec: projects/kr-arcade/depth-pass/ASSESSMENT.md (read the game's section first). Riff on mechanics only; original layouts, names and lines; cartoon bonk/cheer only; no real money, no runtime LLM. Gameplay changes ARE in scope here (unlike t-021). Keep the 60 Hz seeded simulation, the score API and the attract pilot working (update the pilot for new mechanics). Content is data (district/episode/room definitions), not branches in the update loop. Verify: test:arcade-engine plus a deterministic campaign test, eslint/prettier, vue-tsc, Pixel and HD screenshots on the PR, and a pilot probe that shows runs still end.
Merged as kind_robots#3525: four contestants (Sparkle, Zippy, Boomer, Glimmer) with a pick card; co-op for up to four seats (maxPlayers 4; twin-stick stays solo, co-op seats aim where they move or B-lock); four commercial-break mini-games between episodes and mid-finale; team scaling with a 250M clamp; the season ends after its third rerun.
<!-- note:end t-033 -->

## t-034 — Prize Show Panic depth slice 7: Rerun and Marathon modes, episode select and medals

<!-- note:begin t-034 -->
ASSESSMENT.md section 2, modes. Rerun NG+ with remixed scripts and modifiers; Marathon endless rooms as the leaderboard main event; episode select after a clear; Flawless / Full Haul / Prime Time room medals with a medal board. Then update games.yaml and the registry howTo for the finished season. Silas, 2026-10-11: "We don't need to be 1:1 copies of these games, but we should be equally complex or more so", then on the plan: "expand both pitches to add even more to each, so we really are homages with even more inspired levels and gameplay depth." Spec: projects/kr-arcade/depth- pass/ASSESSMENT.md (read the game's section first). Riff on mechanics only; original layouts, names and lines; cartoon bonk/cheer only; no real money, no runtime LLM. Gameplay changes ARE in scope here (unlike t-021). Keep the 60 Hz seeded simulation, the score API and the attract pilot working (update the pilot for new mechanics). Content is data (district/episode/room definitions), not branches in the update loop. Verify: test:arcade-engine plus a deterministic campaign test, eslint/prettier, vue-tsc, Pixel and HD screenshots on the PR, and a pilot probe that shows runs still end.
Merged as kind_robots#3526: the mode card (Season, Rerun, Marathon, Episode select, Medal board); Rerun NG+ with deterministic per-room remixes; Marathon endless legs as the leaderboard main event; episode select after a clear; Flawless / Full Haul / Prime Time medals in every room (201) with a medal board; save v2 (v1 still reads); registry blurb and howTo for the finished season. Completes the Prize Show Panic depth pass.
<!-- note:end t-034 -->

## t-035 — Rescue Rally depth slice 1: Twin-stick and teeth

<!-- note:begin t-035 -->
CABINETS.md section 1, Rescue Rally (Robotron riff), slice 1 of 4: Twin-stick and teeth. The upgrade is "Citywide Reboot". Spec: projects/kr-arcade/depth-pass/CABINETS.md -- read the game's section first; this slice's scope is item 1 under its '#### Slices', and 'Rules for every slice' at the top applies. Code: kind_robots utils/arcade/games/ (registry slug rescue-rally). Silas, 2026-10-11: "I need an assessment done of the other arcade games. I want the same level of quality improvements, they should not just be thin veneers of the old games. But newer, better, even more awesome."
Merged as kind_robots#3540: twin-stick aim (registry twinStick), stompers, hypnos with glitched friends, sparkers, pylon shapes, escort-to-beacon rescues for a double bonus, 16 data-defined wave scripts and bigger actors; real-life pilot runs end in 7-10 min.
<!-- note:end t-035 -->

## t-036 — Rescue Rally depth slice 2: Neon Plaza, Toy Factory and the Shelter

<!-- note:begin t-036 -->
CABINETS.md section 1, Rescue Rally (Robotron riff), slice 2 of 4: Neon Plaza, Toy Factory and the Shelter. The upgrade is "Citywide Reboot". Spec: projects/kr-arcade/depth-pass/CABINETS.md -- read the game's section first; this slice's scope is item 2 under its '#### Slices', and 'Rules for every slice' at the top applies. Code: kind_robots utils/arcade/games/ (registry slug rescue-rally). Silas, 2026-10-11: "I need an assessment done of the other arcade games. I want the same level of quality improvements, they should not just be thin veneers of the old games. But newer, better, even more awesome."
Merged as kind_robots#3552: districts as data with Neon Plaza and the Toy Factory (conveyors, breakable crates), bosses The Big Wind-Up and The Jack-in-the-Box, the Reboot Squad chain, eight power-ups, the Shelter with thank-you hearts, save/resume per district, original music loops; maxPlausibleScore 5M to 20M from 60-minute probes.
<!-- note:end t-036 -->

## t-037 — Rescue Rally depth slice 3: Districts 3–5, the Glitch Core and the endings

<!-- note:begin t-037 -->
CABINETS.md section 1, Rescue Rally (Robotron riff), slice 3 of 4: Districts 3–5, the Glitch Core and the endings. The upgrade is "Citywide Reboot". Spec: projects/kr-arcade/depth-pass/CABINETS.md -- read the game's section first; this slice's scope is item 3 under its '#### Slices', and 'Rules for every slice' at the top applies. Code: kind_robots utils/arcade/games/ (registry slug rescue-rally). Silas, 2026-10-11: "I need an assessment done of the other arcade games. I want the same level of quality improvements, they should not just be thin veneers of the old games. But newer, better, even more awesome."

Reconciled merged kind_robots#3569 at 4641ea14c26bef88b3b2841e5410a389d68e0025. Authoritative merge and all 29 completed original-head checks verified at 3e3efa4a6b0605b9367f349c6c69fbadad81b42d. Current code includes the three later districts, Glitch Core, golden chips, Reunion and endings. The dependent t-038 PR #3581 is receiving a separate complete-diff, save-path and rendered-controls review. This closes stale bookkeeping without claiming or duplicating implementation.
<!-- note:end t-037 -->

## t-038 — Rescue Rally depth slice 4: Co-op and the long rally

<!-- note:begin t-038 -->
CABINETS.md section 1, Rescue Rally (Robotron riff), slice 4 of 4: Co-op and the long rally. The upgrade is "Citywide Reboot". Spec: projects/kr-arcade/depth-pass/CABINETS.md -- read the game's section first; this slice's scope is item 4 under its '#### Slices', and 'Rules for every slice' at the top applies. Code: kind_robots utils/arcade/games/ (registry slug rescue-rally). Silas, 2026-10-11: "I need an assessment done of the other arcade games. I want the same level of quality improvements, they should not just be thin veneers of the old games. But newer, better, even more awesome."

Reviewer reserved kind_robots#3581 with marker conductor-cycle-20261012T065000Z-rally-r9k2. Current head ea7fba57b6ea2ec5de895077271a45e272debe3a has all 28 checks completed green. Complete eight-file PR diff inspected, independently passed 20 cabinet suites including all five Rescue Rally suites, and actual menu/medal-board/co-op/revive renders fit 390/768/1440 widths. Parent t-037 was verified done through the task-event processor; no duplicate implementation. Await final fresh reviews/comments/head and merge using expected head SHA.

Merged kind_robots#3581 at a093d9a69ab7a58b426cb00ef7e23cfd75c22df2 using expected head ea7fba57b6ea2ec5de895077271a45e272debe3a after all 28 head checks completed green, required ruleset checks passed, and no blocking review remained. Full eight-file diff inspected; independent 20-cabinet suite and save round trips passed. Actual menu, full medal board, co-op and revive renders fit 390/768/1440 widths. Merge preserves Joust's separately merged registry. Catalog/TALKBACK and one bounded consumer-control kaizen follow. Fixture state is staged; full-site, deployment and human campaign duration are not claimed.
<!-- note:end t-038 -->

## t-039 — Battery Maze depth slice 1: The rules engine and the Friend Train

<!-- note:begin t-039 -->
CABINETS.md section 2, Battery Maze (Pac-Man riff), slice 1 of 4: The rules engine and the Friend Train. The upgrade is "The Charging Network". Spec: projects/kr-arcade/depth-pass/CABINETS.md -- read the game's section first; this slice's scope is item 1 under its '#### Slices', and 'Rules for every slice' at the top applies. Code: kind_robots utils/arcade/games/ (registry slug battery-maze). Silas, 2026-10-11: "I need an assessment done of the other arcade games. I want the same level of quality improvements, they should not just be thin veneers of the old games. But newer, better, even more awesome."
Merged as kind_robots#3543: mazes as data (3 layouts) with per-maze heat tables, four original hunter rules replacing the classic's, overclock, shield cells, cornering and the eating slowdown, 10 roaming prize kinds, the Friend Train and Rewire switches.
<!-- note:end t-039 -->

## t-040 — Battery Maze depth slice 2: Power Phase 1 and the Charging Bay

<!-- note:begin t-040 -->
CABINETS.md section 2, Battery Maze (Pac-Man riff), slice 2 of 4: Power Phase 1 and the Charging Bay. The upgrade is "The Charging Network". Spec: projects/kr-arcade/depth-pass/CABINETS.md -- read the game's section first; this slice's scope is item 2 under its '#### Slices', and 'Rules for every slice' at the top applies. Code: kind_robots utils/arcade/games/ (registry slug battery-maze). Silas, 2026-10-11: "I need an assessment done of the other arcade games. I want the same level of quality improvements, they should not just be thin veneers of the old games. But newer, better, even more awesome."
Merged as kind_robots#3554: Power Phase 1 as a board campaign (Cozy Charger, Toaster Works with conveyors and pop-up toast), DASH and MUNCH gremlins, the Gremlin Mama trap- bay boss, story comics as data, golden bolts, four power-ups, bolts and the Charging Bay shop, save/continue at each board card, original music loops.
<!-- note:end t-040 -->

## t-041 — Battery Maze depth slice 3: Power Phases 2 and 3, the Overload and the endings

<!-- note:begin t-041 -->
CABINETS.md section 2, Battery Maze (Pac-Man riff), slice 3 of 4: Power Phases 2 and 3, the Overload and the endings. The upgrade is "The Charging Network". Spec: projects/kr-arcade/depth-pass/CABINETS.md -- read the game's section first; this slice's scope is item 3 under its '#### Slices', and 'Rules for every slice' at the top applies. Code: kind_robots utils/arcade/games/ (registry slug battery-maze). Silas, 2026-10-11: "I need an assessment done of the other arcade games. I want the same level of quality improvements, they should not just be thin veneers of the old games. But newer, better, even more awesome."

Reconciled already-merged kind_robots#3560 at c7cc4c1a26478ea2788c649b58ddce9d7cfdbb87. Verified authoritative merge and all 29 completed original-head checks at bc254854c78eb3fbd4861268e8e2d5bc33c80549. Code includes all six boards, three bosses, golden bolts, Battery Garden, both endings and Overclocked. This closes stale bookkeeping and unblocks t-042, whose open #3579 receives a separate full diff/save/input review. Unlimited-life pilot estimates are not evidence of human first-clear duration.
<!-- note:end t-041 -->

## t-042 — Battery Maze depth slice 4: Together and versus

<!-- note:begin t-042 -->
CABINETS.md section 2, Battery Maze (Pac-Man riff), slice 4 of 4: Together and versus. The upgrade is "The Charging Network". Spec: projects/kr-arcade/depth-pass/CABINETS.md -- read the game's section first; this slice's scope is item 4 under its '#### Slices', and 'Rules for every slice' at the top applies. Code: kind_robots utils/arcade/games/ (registry slug battery-maze). Silas, 2026-10-11: "I need an assessment done of the other arcade games. I want the same level of quality improvements, they should not just be thin veneers of the old games. But newer, better, even more awesome."

Reviewer marker conductor-cycle-20261012T083000Z-battery-b7m4 reserves kind_robots#3579. Complete original eight-file diff and current head fd843d471fccdb4ce236d43548bcb2a8bd4da874 repair diff inspected. Independent full arcade suite passed 20 cabinets. Public-input save-consumer round trips verify 3/4-seat Tag gating for a toaster checkpoint and a step-0 later-lap save, including correct gremlin seats and preserved campaign checkpoint. Actual menu, full medals, co-op and saved-entry Tag render at 390/768/1440 without overflow. Old-head reproduction was superseded by the worker's concurrent repair, so passes stays 0. Await fresh current-head checks and blocking-review inspection before expected-head merge.

Merged kind_robots#3579 at 44b81865619eddd5400f98033c9e105b67408c1a using expected repaired head fd843d471fccdb4ce236d43548bcb2a8bd4da874 after all 28 checks completed successfully, required ruleset checks passed and no blocking review remained. Independent 20-cabinet suite passed; public-input save-consumer round trips verify toaster and step-0 later-lap checkpoints with both 3/4 seats, proper Tag actor assignment and preserved campaign checkpoint. Actual menu/full medal-board/co-op/saved Tag renderer fixtures fit 390/768/1440 widths. The older-head finding was superseded by a concurrent worker repair before final decision, so passes stays 0. Catalog and critique follow in a focused Conductor PR. No full-site, deployment or human campaign pacing claim.
<!-- note:end t-042 -->

## t-043 — Sink Suds depth slice 1: The basin engine and size-as-ammunition

<!-- note:begin t-043 -->
CABINETS.md section 3, Sink Suds (Bubbles riff), slice 1 of 4: The basin engine and size-as-ammunition. The upgrade is "The Big House Wash". Spec: projects/kr-arcade/depth-pass/CABINETS.md -- read the game's section first; this slice's scope is item 1 under its '#### Slices', and 'Rules for every slice' at the top applies. Code: kind_robots utils/arcade/games/ (registry slug sink-suds). Silas, 2026-10-11: "I need an assessment done of the other arcade games. I want the same level of quality improvements, they should not just be thin veneers of the old games. But newer, better, even more awesome."
Merged as kind_robots#3536: six data-defined basins with their own water physics, the grime layer and CLEAN %, soap shots that trap pests on chains, beatable brushes, the Sponge, the Drain Gremlin and a size-faced bubble.
<!-- note:end t-043 -->

## t-044 — Sink Suds depth slice 2: Wash Cycle 1 and the Soap Shop

<!-- note:begin t-044 -->
CABINETS.md section 3, Sink Suds (Bubbles riff), slice 2 of 4: Wash Cycle 1 and the Soap Shop. The upgrade is "The Big House Wash". Spec: projects/kr-arcade/depth-pass/CABINETS.md -- read the game's section first; this slice's scope is item 2 under its '#### Slices', and 'Rules for every slice' at the top applies. Code: kind_robots utils/arcade/games/ (registry slug sink-suds). Silas, 2026-10-11: "I need an assessment done of the other arcade games. I want the same level of quality improvements, they should not just be thin veneers of the old games. But newer, better, even more awesome."
Merged as kind_robots#3548: the room engine with save and continue, Kitchen Sink and Bath Time with their special basins (Dish Stack, Duck Round-up), the scum slug and loofah, six power-ups, soap bars, the Soap Shop, golden soaps and the Bristleton boss.
<!-- note:end t-044 -->

## t-045 — Sink Suds depth slice 3: Wash Cycles 2 and 3, the Grime King and the endings

<!-- note:begin t-045 -->
CABINETS.md section 3, Sink Suds (Bubbles riff), slice 3 of 4: Wash Cycles 2 and 3, the Grime King and the endings. The upgrade is "The Big House Wash". Spec: projects/kr-arcade/depth-pass/CABINETS.md -- read the game's section first; this slice's scope is item 3 under its '#### Slices', and 'Rules for every slice' at the top applies. Code: kind_robots utils/arcade/games/ (registry slug sink-suds). Silas, 2026-10-11: "I need an assessment done of the other arcade games. I want the same level of quality improvements, they should not just be thin veneers of the old games. But newer, better, even more awesome."
Merged as kind_robots#3555: Laundry Drum, Fish Tank, Birdbath and Car Wash rooms with their pests and special basins, the Mossback and Grime King bosses, the endings and credits, the golden-soap palace true ending and Deep Clean; maxPlausibleScore 3M to 10M (probes topped at 2.2M after 80 min).
<!-- note:end t-045 -->

## t-046 — Sink Suds depth slice 4: Bubble Buddies and Suds Sumo

<!-- note:begin t-046 -->
CABINETS.md section 3, Sink Suds (Bubbles riff), slice 4 of 4: Bubble Buddies and Suds Sumo. The upgrade is "The Big House Wash". Spec: projects/kr-arcade/depth-pass/CABINETS.md -- read the game's section first; this slice's scope is item 4 under its '#### Slices', and 'Rules for every slice' at the top applies. Code: kind_robots utils/arcade/games/ (registry slug sink-suds). Silas, 2026-10-11: "I need an assessment done of the other arcade games. I want the same level of quality improvements, they should not just be thin veneers of the old games. But newer, better, even more awesome."
2026-10-11 PT review: kind_robots#3558 remains unmerged. All 28 head checks passed/allowed skips and npm run test:arcade-engine passed (14 cabinet suites), but a direct behavior probe reproduced lost best-time persistence after New Wash from a valid saved room checkpoint. See PR comment https://github.com/silasfelinus/kind_robots/pull/3558#issuecomment-6115161917. Quality rejection, pass 1; reuse the existing implementation branch, repair persistence and verify reload. No human action required.

Kind Robots Sink Suds PR #3558 merged as 0d0f24020ec4f385431b8babd44d912e267308de after all 27 final-head workflow checks passed. The previously documented New Wash to Squeaky Clean persistence defect was fixed and a reload regression case added. This concludes depth slice 4 on main; a self-hosted deployment is not established by the merge.

Reviewer verified the repaired merged Sink Suds result at 0d0f24020ec4f385431b8babd44d912e267308de, original final head 44d84f3191733fafde053ed5b9543a10eba8d879, all 29 completed head check runs without failure. The independent original saved-checkpoint New Wash -> Squeaky Clean -> finish -> withSave/JSON/sanitizeSaves -> reload probe now preserves the new best, old time, medals, reached rooms, golden soap, skin and clear, and resets only the campaign checkpoint. Repair diff against the reviewed old head inspected. Keep passes 1 as historical quality rejection; remove obsolete retry_context through the focused reviewed closeout PR. This adds missing completion learning without duplicating implementation or a claim. No deployed runtime or 40-50 minute human campaign target is inferred.
<!-- note:end t-046 -->

## t-047 — Butterfly Joust depth slice 1: Party and pond

<!-- note:begin t-047 -->
CABINETS.md section 4, Butterfly Joust (Joust riff), slice 1 of 4: Party and pond. The upgrade is "The Four Gardens Tourney". Spec: projects/kr-arcade/depth-pass/CABINETS.md -- read the game's section first; this slice's scope is item 1 under its '#### Slices', and 'Rules for every slice' at the top applies. Code: kind_robots utils/arcade/games/ (registry slug butterfly-joust). Silas, 2026-10-11: "I need an assessment done of the other arcade games. I want the same level of quality improvements, they should not just be thin veneers of the old games. But newer, better, even more awesome."
Merged as kind_robots#3539: the Jousting Party for 2-4 riders (Co-op with team bonus and knock-and-rescue, 3-minute Last Butterfly Flapping), announced Survival / Gladiator / Cocoon / Storm / Team waves, the Pond Frog, Carriers, Air Combo and Charge Joust (B), and the Thundercap's open-eye check; registry maxPlayers 4.
<!-- note:end t-047 -->

## t-048 — Butterfly Joust depth slice 2: Arena engine, Sunset Pond and Spring Meadow

<!-- note:begin t-048 -->
CABINETS.md section 4, Butterfly Joust (Joust riff), slice 2 of 4: Arena engine, Sunset Pond and Spring Meadow. The upgrade is "The Four Gardens Tourney". Spec: projects/kr-arcade/depth-pass/CABINETS.md -- read the game's section first; this slice's scope is item 2 under its '#### Slices', and 'Rules for every slice' at the top applies. Code: kind_robots utils/arcade/games/ (registry slug butterfly-joust). Silas, 2026-10-11: "I need an assessment done of the other arcade games. I want the same level of quality improvements, they should not just be thin veneers of the old games. But newer, better, even more awesome."
Merged as kind_robots#3551: the arena engine as data (crumbling, folding and drifting ledges, puffs, thermals, wind), Sunset Pond retuned and Spring Meadow, the glider, twin riders and pollen bomber, champions Sir Bumbleton and the Dandelion Duchess, the Wing Garden pollen shop, save/resume at each arena and a Tourney / Classic Pond / Versus mode card.
<!-- note:end t-048 -->

## t-049 — Butterfly Joust depth slice 3: Heights, Orchard, Snowfield and the Moon Garden

<!-- note:begin t-049 -->
CABINETS.md section 4, Butterfly Joust (Joust riff), slice 3 of 4: Heights, Orchard, Snowfield and the Moon Garden. The upgrade is "The Four Gardens Tourney". Spec: projects/kr-arcade/depth-pass/CABINETS.md -- read the game's section first; this slice's scope is item 3 under its '#### Slices', and 'Rules for every slice' at the top applies. Code: kind_robots utils/arcade/games/ (registry slug butterfly-joust). Silas, 2026-10-11: "I need an assessment done of the other arcade games. I want the same level of quality improvements, they should not just be thin veneers of the old games. But newer, better, even more awesome."

Reconciled already-merged kind_robots#3559 at 80db6b0f69c3c96b7f1c76fcc943a15c930ae129. Authoritative merge and all relevant original-head checks at de8d7a945aa6d63f8ad0f18d9021d8ec09fb756f verified. Current main includes Heights, Orchard, Snowfield, Moon Garden, champions, petals/endings and Circuit. This closes stale bookkeeping, not new work or a deployment. Unblock t-050, whose implementation is also already merged and is receiving a separate complete-diff/current-main audit.
<!-- note:end t-049 -->

## t-050 — Butterfly Joust depth slice 4: Medals and the endless pond

<!-- note:begin t-050 -->
CABINETS.md section 4, Butterfly Joust (Joust riff), slice 4 of 4: Medals and the endless pond. The upgrade is "The Four Gardens Tourney". Spec: projects/kr-arcade/depth-pass/CABINETS.md -- read the game's section first; this slice's scope is item 4 under its '#### Slices', and 'Rules for every slice' at the top applies. Code: kind_robots utils/arcade/games/ (registry slug butterfly-joust). Silas, 2026-10-11: "I need an assessment done of the other arcade games. I want the same level of quality improvements, they should not just be thin veneers of the old games. But newer, better, even more awesome."

Reviewer audited already-merged kind_robots#3575 at 38dc1a0b028a888cf62b0c88c5881c93249428da after reconciling dependency t-049. Complete eight-file diff inspected; all 28 original PR-head checks completed successfully at 2639814ee0a7acf75716b55707d4ab2431078cd5. Independently passed all 19 cabinet suites on current main, including medal/save/endless and both ending paths. Actual canvas menu, empty/populated medal boards and Endless Pond rendered at 390/768/1440 widths without horizontal overflow. Isolated renderer fixtures are not full-site or deployed-runtime verification. Catalog and TALKBACK closeout follows in a focused Conductor PR. No deployment performed; full-campaign pacing remains separately measurable.
<!-- note:end t-050 -->

## t-051 — Kindness Gauntlet depth slice 1: A menagerie

<!-- note:begin t-051 -->
CABINETS.md section 5, Kindness Gauntlet (Gauntlet II riff), slice 1 of 4: A menagerie. The upgrade is "The Deep Archive". Spec: projects/kr-arcade/depth-pass/CABINETS.md -- read the game's section first; this slice's scope is item 1 under its '#### Slices', and 'Rules for every slice' at the top applies. Code: kind_robots utils/arcade/games/ (registry slug kindness-gauntlet). Silas, 2026-10-11: "I need an assessment done of the other arcade games. I want the same level of quality improvements, they should not just be thin veneers of the old games. But newer, better, even more awesome."
Merged as kind_robots#3537: eight new glitch kinds with three-tier generators, the Mainframe's voice panel, sparkable snacks, spark-to-share, the Hug Token and seat scores; real-life pilot runs end on floors 6-17.
<!-- note:end t-051 -->

## t-052 — Kindness Gauntlet depth slice 2: The first two wings

<!-- note:begin t-052 -->
CABINETS.md section 5, Kindness Gauntlet (Gauntlet II riff), slice 2 of 4: The first two wings. The upgrade is "The Deep Archive". Spec: projects/kr-arcade/depth-pass/CABINETS.md -- read the game's section first; this slice's scope is item 2 under its '#### Slices', and 'Rules for every slice' at the top applies. Code: kind_robots utils/arcade/games/ (registry slug kindness-gauntlet). Silas, 2026-10-11: "I need an assessment done of the other arcade games. I want the same level of quality improvements, they should not just be thin veneers of the old games. But newer, better, even more awesome."
Merged as kind_robots#3550: the first two wings (12 floors plus 2 Lost & Found floors), Vault and Library tricks, the Worm, the Big Bluescreen, the Card Sorter and Twin Reels, charms and chips, floor secrets and per-wing save with a continue offer.
<!-- note:end t-052 -->

## t-053 — Kindness Gauntlet depth slice 3: The middle wings

<!-- note:begin t-053 -->
CABINETS.md section 5, Kindness Gauntlet (Gauntlet II riff), slice 3 of 4: The middle wings. The upgrade is "The Deep Archive". Spec: projects/kr-arcade/depth-pass/CABINETS.md -- read the game's section first; this slice's scope is item 3 under its '#### Slices', and 'Rules for every slice' at the top applies. Code: kind_robots utils/arcade/games/ (registry slug kindness-gauntlet). Silas, 2026-10-11: "I need an assessment done of the other arcade games. I want the same level of quality improvements, they should not just be thin veneers of the old games. But newer, better, even more awesome."
Merged as kind_robots#3556: the Arcade Basement and Cloud Atrium wings (16 floors, all six tricks), the Blinker and Pop-up wizard, helper drones, the Attract Mode and Cloud Bank bosses with phase tests, and Memory Cards in the save.
<!-- note:end t-053 -->

## t-054 — Kindness Gauntlet depth slice 4: The Core and the modes

<!-- note:begin t-054 -->
CABINETS.md section 5, Kindness Gauntlet (Gauntlet II riff), slice 4 of 4: The Core and the modes. The upgrade is "The Deep Archive". Spec: projects/kr-arcade/depth-pass/CABINETS.md -- read the game's section first; this slice's scope is item 4 under its '#### Slices', and 'Rules for every slice' at the top applies. Code: kind_robots utils/arcade/games/ (registry slug kindness-gauntlet). Silas, 2026-10-11: "I need an assessment done of the other arcade games. I want the same level of quality improvements, they should not just be thin veneers of the old games. But newer, better, even more awesome."
Merged as kind_robots#3561: the Core (floors 33-40), the Old Mainframe finale in three phases, the plain and true endings, Descent, Reboot (New Game+), the Endless Archive, Lost & Found, Score Duel and the medal board. A save review before merge found that quitting during the credits lost the clear and the Reboot unlock; the fix records the clear as the ending starts and keeps the Endless best depth per floor, with round-trip tests. Kindness Gauntlet's m8 depth pass is complete.
<!-- note:end t-054 -->

## t-055 — Butterfly Blaster depth slice 1: Flight and the living swarm

<!-- note:begin t-055 -->
CABINETS.md section 6, Butterfly Blaster (Asteroids riff), slice 1 of 4: Flight and the living swarm. The upgrade is "The Rainy Season". Spec: projects/kr-arcade/depth-pass/CABINETS.md -- read the game's section first; this slice's scope is item 1 under its '#### Slices', and 'Rules for every slice' at the top applies. Code: kind_robots utils/arcade/games/ (registry slug butterfly-blaster). Silas, 2026-10-11: "I need an assessment done of the other arcade games. I want the same level of quality improvements, they should not just be thin veneers of the old games. But newer, better, even more awesome."
Merged as kind_robots#3576: swarms flock to lit huts and regroup when split, huts take bites with a dawn tally, the Rainbow Lasso, chains, anti-lurk, the flutter-dash and long hop with Brave Hop, the heartbeat score with the last-mosquito sprint, and the wriggler, skimmer and needle with breeding pools.
<!-- note:end t-055 -->

## t-056 — Butterfly Blaster depth slice 2: Moon 1, the river map and the Clinic

<!-- note:begin t-056 -->
CABINETS.md section 6, Butterfly Blaster (Asteroids riff), slice 2 of 4: Moon 1, the river map and the Clinic. The upgrade is "The Rainy Season". Spec: projects/kr-arcade/depth-pass/CABINETS.md -- read the game's section first; this slice's scope is item 2 under its '#### Slices', and 'Rules for every slice' at the top applies. Code: kind_robots utils/arcade/games/ (registry slug butterfly-blaster). Silas, 2026-10-11: "I need an assessment done of the other arcade games. I want the same level of quality improvements, they should not just be thin veneers of the old games. But newer, better, even more awesome."
Merged as kind_robots#3587: the season engine and river map, Riverbend (Lantern Walk) and Rice Terraces (wind, Tip the Pots), AMI's six-item kit, the Clinic with thank-you beads and the Hum in three phases; saves at every night, boss, Clinic and purchase with round-trip tests.
<!-- note:end t-056 -->

## t-057 — Butterfly Blaster depth slice 3: Moons 2 and 3, the bosses and the endings

<!-- note:begin t-057 -->
CABINETS.md section 6, Butterfly Blaster (Asteroids riff), slice 3 of 4: Moons 2 and 3, the bosses and the endings. The upgrade is "The Rainy Season". Spec: projects/kr-arcade/depth-pass/CABINETS.md -- read the game's section first; this slice's scope is item 3 under its '#### Slices', and 'Rules for every slice' at the top applies. Code: kind_robots utils/arcade/games/ (registry slug butterfly-blaster). Silas, 2026-10-11: "I need an assessment done of the other arcade games. I want the same level of quality improvements, they should not just be thin veneers of the old games. But newer, better, even more awesome."

Reviewer quality pass 1 on October 12, 2026 at 3:46 AM PT. Conductor#6040 records the independently reproduced earned cleared/zero flag loss on B New Season, exact retry_context and TALKBACK. Return the task to ready and release ownership; retain kind_robots#3596 for the original worker's focused repair. Existing full arcade command passed 30 cabinet suites and 28 head checks were green, but the public New Season save-consumer transition loses earned ending history. No duplicate implementation, new human gate or deployment. Read retry_context and PR feedback before re-claiming, preserve completion flags and test both endings.

Recovery of quality pass1 from already-merged kind_robots#3596: preserve earned cleared/zero/threads before the first checkpoint, including B New Season and step-zero reload. Focused runtime and actual input/save-consumer regressions prepared on worker/kr-arcade-t057-profile-recovery-c9f2. Original-code red reproduced; Finale, full arcade engine (33 cabinet suites), targeted ESLint/Prettier, and six native Chromium actual keyboard/touch/localStorage/reload/play renders at390/768/1440 passed. Browser uses staged earned ending profiles, not a claimed full human campaign playthrough. Existing Moons/bosses/endings retained; CI/merge still pending. Daily five ledger unchanged.

Merged silasfelinus/kind_robots#3646 at a4196c625b03be48bcc468b4de0848ef8bb236f5 using expected head f3d4acf4fbdbfc5eaa86a5358a8f1709d29f38a6 after all28 actual head checks completed success, including required TypeScript/Contract verifiers/verify. Complete final diff and reviews checked; no blocking review or approval requirement, no bypass. Main runtime matches repaired blob12b55a257 and obsolete branch verified404. New Season and step-zero reload retain earned dawn/Zero Night history; Continue retains current-run resources. Original runtime red and B-only mutation fails intended reload assertion. Focused strict tsc/Finale/ESLint/Prettier/full33cabinet engine and six actual Chromium keyboard/touch/storage/reload/play cases passed. Existing audited later regions/bosses/endings retained; slice3 complete, co-op/modes remain t058. Staged fixtures are not human45-60minute pacing or deployment evidence. Historical quality pass1 retained; retry_context resolved, implementation link3646, one targeted retirement kaizen t152 awaits dependency release. Daily five ledger untouched.
<!-- note:end t-057 -->

## t-058 — Butterfly Blaster depth slice 4: Together and forever

<!-- note:begin t-058 -->
CABINETS.md section 6, Butterfly Blaster (Asteroids riff), slice 4 of 4: Together and forever. The upgrade is "The Rainy Season". Spec: projects/kr-arcade/depth-pass/CABINETS.md -- read the game's section first; this slice's scope is item 4 under its '#### Slices', and 'Rules for every slice' at the top applies. Code: kind_robots utils/arcade/games/ (registry slug butterfly-blaster). Silas, 2026-10-11: "I need an assessment done of the other arcade games. I want the same level of quality improvements, they should not just be thin veneers of the old games. But newer, better, even more awesome."
Co-op Flight (2-4 seats, team lasso) shipped via kind_robots#3702 (CI 17/17 green, merge 3204971); modes/medals via #3699.
<!-- note:end t-058 -->

## t-059 — Bumper Bubbles depth slice 1: Bubble physics and the first two wings

<!-- note:begin t-059 -->
CABINETS.md section 7, Bumper Bubbles (Bubble Bobble riff), slice 1 of 5: Bubble physics and the first two wings. The upgrade is "The Hundred Floors of Fizzwick Tower". Spec: projects/kr-arcade/depth-pass/CABINETS.md -- read the game's section first; this slice's scope is item 1 under its '#### Slices', and 'Rules for every slice' at the top applies. Code: kind_robots utils/arcade/games/ (registry slug bumper-bubbles). Silas, 2026-10-11: "I need an assessment done of the other arcade games. I want the same level of quality improvements, they should not just be thin veneers of the old games. But newer, better, even more awesome."
Merged as kind_robots#3580: Fizzwick Tower's floor engine with wings 1-2 (floors 1-20) as ASCII data with air currents and screen wrap, bubble riding, cluster pops on the 1k-to-64k treat ladder, Old Flat Fizz, FRIEND letter bubbles, six grumps, gumdrop springs, the Gum tap and a save at every wing start.
<!-- note:end t-059 -->

## t-060 — Bumper Bubbles depth slice 2: Special bubbles, flavours, items and Wings 3–4

<!-- note:begin t-060 -->
CABINETS.md section 7, Bumper Bubbles (Bubble Bobble riff), slice 2 of 5: Special bubbles, flavours, items and Wings 3–4. The upgrade is "The Hundred Floors of Fizzwick Tower". Spec: projects/kr-arcade/depth-pass/CABINETS.md -- read the game's section first; this slice's scope is item 2 under its '#### Slices', and 'Rules for every slice' at the top applies. Code: kind_robots utils/arcade/games/ (registry slug bumper-bubbles). Silas, 2026-10-11: "I need an assessment done of the other arcade games. I want the same level of quality improvements, they should not just be thin veneers of the old games. But newer, better, even more awesome."
Merged as kind_robots#3591: Splash, Zap and Toasty special bubbles, the Float, Fizz and Frost taps, ten hidden-condition items, Wings 3-4 with water channels, low gravity and four new grumps, THE BIG CORK on floor 25, and the floor-20 and floor-40 pantries with recipe cards saved when found.
<!-- note:end t-060 -->

## t-061 — Bumper Bubbles depth slice 3: Wings 5–7

<!-- note:begin t-061 -->
CABINETS.md section 7, Bumper Bubbles (Bubble Bobble riff), slice 3 of 5: Wings 5–7. The upgrade is "The Hundred Floors of Fizzwick Tower". Spec: projects/kr-arcade/depth-pass/CABINETS.md -- read the game's section first; this slice's scope is item 3 under its '#### Slices', and 'Rules for every slice' at the top applies. Code: kind_robots utils/arcade/games/ (registry slug bumper-bubbles). Silas, 2026-10-11: "I need an assessment done of the other arcade games. I want the same level of quality improvements, they should not just be thin veneers of the old games. But newer, better, even more awesome."

Reviewed kind_robots#3594 at 0743bd95a0053eba80182276751e883e53a67f9f on October 12 PT: complete 14-file diff, all 30 independent cabinet suites, native renderer and third-pantry save consumer at 390/768/1440 widths. All 28 current-head checks completed successfully, required checks satisfied, no blocking review. Awaiting expected-head merge and verified closeout; no deployment.

October 12 PT: kind_robots#3594 merged at 88be96280033234491863ef8227f90ce3d70b391 with expected head 0743bd95a0053eba80182276751e883e53a67f9f. All 28 current-head checks completed successfully, required checks satisfied, no blocking review. Independent 30 cabinet suites and native renderer/third-pantry save Continue at 390/768/1440 passed. The earlier done event was consumed as STALE because the review event accidentally carried a future literal timestamp; this clock-observed event follows that timestamp and must be verified applied. Slice 3 only, no deployment or human pacing claim.
<!-- note:end t-061 -->

## t-062 — Bumper Bubbles depth slice 4: Wings 8–10 and the endings

<!-- note:begin t-062 -->
CABINETS.md section 7, Bumper Bubbles (Bubble Bobble riff), slice 4 of 5: Wings 8–10 and the endings. The upgrade is "The Hundred Floors of Fizzwick Tower". Spec: projects/kr-arcade/depth-pass/CABINETS.md -- read the game's section first; this slice's scope is item 4 under its '#### Slices', and 'Rules for every slice' at the top applies. Code: kind_robots utils/arcade/games/ (registry slug bumper-bubbles). Silas, 2026-10-11: "I need an assessment done of the other arcade games. I want the same level of quality improvements, they should not just be thin veneers of the old games. But newer, better, even more awesome."
Merged kind_robots#3649 at 41a1a40680a2c6da1532a0406fb5061d181c1d9a: Wings 8-10, the Jelly Mould (75), the Grumble Fizz King (100), pantries 80/90 and the solo/co-op/true endings. All 28 PR checks green on head 9cb4831. Local suites for slices 1-4 pass; no Chromium screenshots or human pacing claim. Co-op endings need slice 5 (registry maxPlayers). Registry maxPlausibleScore raised to 20M.
<!-- note:end t-062 -->

## t-063 — Bumper Bubbles depth slice 5: Co-op and the extra modes

<!-- note:begin t-063 -->
CABINETS.md section 7, Bumper Bubbles (Bubble Bobble riff), slice 5 of 5: Co-op and the extra modes. The upgrade is "The Hundred Floors of Fizzwick Tower". Spec: projects/kr-arcade/depth-pass/CABINETS.md -- read the game's section first; this slice's scope is item 5 under its '#### Slices', and 'Rules for every slice' at the top applies. Code: kind_robots utils/arcade/games/ (registry slug bumper-bubbles). Silas, 2026-10-11: "I need an assessment done of the other arcade games. I want the same level of quality improvements, they should not just be thin veneers of the old games. But newer, better, even more awesome."
Shipped silasfelinus/kind_robots#3703 (squash fee28b2, 17/17 checks green): mode menu (Floor Select, Pop Party, Endless Fizz, Time Trial, Star Board), stars/wing medals/best times in the save, maxPlayers 4. Slice 5 of 5; registry blurb/howTo updated.
<!-- note:end t-063 -->

## t-064 — Cable Crawler depth slice 1: Maze engine, surge and the Power Strip

<!-- note:begin t-064 -->
CABINETS.md section 8, Cable Crawler (Nibbler riff), slice 1 of 5: Maze engine, surge and the Power Strip. The upgrade is "The Mainframe Odyssey". Spec: projects/kr-arcade/depth-pass/CABINETS.md -- read the game's section first; this slice's scope is item 1 under its '#### Slices', and 'Rules for every slice' at the top applies. Code: kind_robots utils/arcade/games/ (registry slug cable-crawler). Silas, 2026-10-11: "I need an assessment done of the other arcade games. I want the same level of quality improvements, they should not just be thin veneers of the old games. But newer, better, even more awesome."
Merged as kind_robots#3585: authored mazes, the Plug-In Surge, three glitches, golden bytes, the Starfield Screensaver and the Surge Protector boss; maxPlausibleScore 2M to 25M from a 2-hour probe that peaked at 9.3M.
<!-- note:end t-064 -->

## t-065 — Cable Crawler depth slice 2: RAM Rows and the Cooling Fan

<!-- note:begin t-065 -->
CABINETS.md section 8, Cable Crawler (Nibbler riff), slice 2 of 5: RAM Rows and the Cooling Fan. The upgrade is "The Mainframe Odyssey". Spec: projects/kr-arcade/depth-pass/CABINETS.md -- read the game's section first; this slice's scope is item 2 under its '#### Slices', and 'Rules for every slice' at the top applies. Code: kind_robots utils/arcade/games/ (registry slug cable-crawler). Silas, 2026-10-11: "I need an assessment done of the other arcade games. I want the same level of quality improvements, they should not just be thin veneers of the old games. But newer, better, even more awesome."

October 12 PT: Conductor#6046 merged retry metadata at a09034fea3e02848026036d6fbf010896813a898 after 25 completed current-head checks passed. Quality pass 1: legitimate earned spare count exceeds its own save reader domain, dropping Continue at 100 lives below the 60M score ceiling; exact reproduction and repair requirements in retry_context and kind_robots#3593 comment 6126370861. Release ownership, retain the original implementation PR for its worker's scoped repair; no duplicate implementation or human gate. Independent full arcade run passed 30 cabinet suites, but this boundary remains unresolved. No deployment or publication.

Focused recovery of recorded quality pass1: original kind_robots#3593 is already merged, but live source still awards unbounded spare cables and its strict save reader rejects above99/clamps accepted earned counts to the Workbench purchase cap9. No open Cable PR or overlapping task claim. Preserve existing RAM/Fan mechanics, strict validation and purchase ceiling; reproduce legitimate score-award/save/Continue boundary before repair. Daily five forOctober13PT already evidenced separately. Local role selector used stale checkout/no GitHub token, so live connected PRs/claims and current source supersede its outdated audit signal.

Quality-pass1 recovery for already-merged kind_robots#3593 prepared on worker/kr-arcade-t065-save-recovery-d7p2. Score-awarded spares use the existing strict99 save domain; Workbench purchases remain capped9, earned10..99 survive reload without clamping. Actual score-path tests reproduce old10-to9 loss and100-cable overflow separately; repaired boundary matrix8/9/10/98/99, publicA/Start Continue, bytes/kit, post-cap actual battery loss and re-earn, and unchanged invalid-count rejection pass. Full35cabinet arcade command, strict scoped tsc, ESLint/Prettier and nine native Chromium actual touch/keyboard/storage/repeatedContinue/render cases390/768/1440 pass. Staged score-award/byte fixtures do not prove human50-60minute pacing or deployment. Existing RAM/Fan implementation retained; PR/CI/merge pending. Daily five ledger unchanged.

Verified merged kind_robots#3654 at 0c8684c31b732f22a8205df2c6c82a6b073b73cd; all28 actual final-head checks passed at1bec4f0a4dc6733f1c8663bde023c17045be5e77, including Contract verifiers38491262753 and full-project TypeScript38491262692. Main matches all three repaired source/test blobs and implementation branch is deleted. Scoped earned-spare recovery preserves10..99 on Continue and prevents invalid100 checkpoints without weakening save validation or changing Workbench purchase9. Full35-cabinet engine and nine native browser cases passed in implementation cycle. Conductor#6150 merged at8047a56e98a7ee828cd854abc08972d17732f79e after24 success plus one intentional skip; metadata, append-only audit and single t-153 follow-up verified. Retain historical quality pass1, release ownership and dependent work; daily five remain separately complete. No publication, deployment or human pacing claim.
<!-- note:end t-065 -->

## t-066 — Cable Crawler depth slice 3: The Sound Card and the Graphics Card

<!-- note:begin t-066 -->
CABINETS.md section 8, Cable Crawler (Nibbler riff), slice 3 of 5: The Sound Card and the Graphics Card. The upgrade is "The Mainframe Odyssey". Spec: projects/kr-arcade/depth-pass/CABINETS.md -- read the game's section first; this slice's scope is item 3 under its '#### Slices', and 'Rules for every slice' at the top applies. Code: kind_robots utils/arcade/games/ (registry slug cable-crawler). Silas, 2026-10-11: "I need an assessment done of the other arcade games. I want the same level of quality improvements, they should not just be thin veneers of the old games. But newer, better, even more awesome." PART 1 2026-10-14: the Sound Card (beat gates, speaker cones, echo, noise gnats, Equaliser, the Subwoofer, five mazes, music, art) in silasfelinus/kind_robots#3690. REMAINING for this task: the Graphics Card (picture-reveal boards, scanlines, glitch sprite, z-fighter wall, Paint Screensaver, The Glitch rival-cable boss). Keep ready until that part ships.
PART 2 2026-10-15: the Graphics Card (picture boards, scanline, glitch sprites, z-fighter walls, Paint, The Glitch rival-cable boss) shipped in silasfelinus/kind_robots#3695 after all 17 CI checks passed (squash 0b132a5). Pilot- validated mazes; new verifyCabinetCableCrawlerGraphicsCard test. Slice 3 complete (Sound Card #3690 + Graphics Card).
<!-- note:end t-066 -->

## t-067 — Cable Crawler depth slice 4: The CPU Core, the BIOS and the endings

<!-- note:begin t-067 -->
CABINETS.md section 8, Cable Crawler (Nibbler riff), slice 4 of 5: The CPU Core, the BIOS and the endings. The upgrade is "The Mainframe Odyssey". Spec: projects/kr-arcade/depth-pass/CABINETS.md -- read the game's section first; this slice's scope is item 4 under its '#### Slices', and 'Rules for every slice' at the top applies. Code: kind_robots utils/arcade/games/ (registry slug cable-crawler). Silas, 2026-10-11: "I need an assessment done of the other arcade games. I want the same level of quality improvements, they should not just be thin veneers of the old games. But newer, better, even more awesome."
PART 1 SHIPPED (kind_robots#3712, merged 7788778): CPU Core component (5 mazes, clock cycles, interrupts, rival cables, Sleepy Kernel, boot ending, no Screensaver). REMAINING for t-067: the secret BIOS component (3 green-screen mazes, text-mode self-rewriting walls, Boot Loader true boss, unlocked by all golden bytes), the true ending, and medals/medal boards (No Bites, Big Surge, Battery Saver).
PART 2 SHIPPED 2026-10-17 (kind_robots#3792, squash 63f53db, CI green): secret BIOS component (3 green-screen mazes, Boot Loader boss with 3 checksum sockets and line-by- line wall rewrites, opened by all 30 golden bytes), true ending, and No Bites / Big Surge / Battery Saver maze medals saved with the run. Test: utils/scripts/verifyCabinetCableCrawlerBios.test.ts.
<!-- note:end t-067 -->

## t-069 — Seed Lander depth slice 1: Flight core

<!-- note:begin t-069 -->
CABINETS.md section 9, Seed Lander (Lunar Lander riff), slice 1 of 5: Flight core. The upgrade is "The Great Replanting". Spec: projects/kr-arcade/depth-pass/CABINETS.md -- read the game's section first; this slice's scope is item 1 under its '#### Slices', and 'Rules for every slice' at the top applies. Code: kind_robots utils/arcade/games/ (registry slug seed-lander). Silas, 2026-10-11: "I need an assessment done of the other arcade games. I want the same level of quality improvements, they should not just be thin veneers of the old games. But newer, better, even more awesome."
Merged as kind_robots#3589: wide scrolling islands with a zoom-to-land camera, Feather/Soft/Bumpy/Bonk landing ranks with a streak, x1-x5 beds, Hop, the tether winch, sun per mission with sunflowers and a steerable parachute, Breezy/Standard/Gale tiers, the MissionSpec data format and a rebuilt Free Flight with hazard unlocks.
<!-- note:end t-069 -->

## t-070 — Seed Lander depth slice 2: Meadow Isle and Windmill Downs

<!-- note:begin t-070 -->
CABINETS.md section 9, Seed Lander (Lunar Lander riff), slice 2 of 5: Meadow Isle and Windmill Downs. The upgrade is "The Great Replanting". Spec: projects/kr-arcade/depth-pass/CABINETS.md -- read the game's section first; this slice's scope is item 2 under its '#### Slices', and 'Rules for every slice' at the top applies. Code: kind_robots utils/arcade/games/ (registry slug seed-lander). Silas, 2026-10-11: "I need an assessment done of the other arcade games. I want the same level of quality improvements, they should not just be thin veneers of the old games. But newer, better, even more awesome."

October 12 PT: Conductor#6049 merged first-mission repair metadata at 0a1877b5a2215dbf56040697936eb9bc691b7421 after 25 final-head checks completed successfully, expected-head merge and no blocking review. Quality pass 1: actual meadow-1 acorn collection saves nectar=5 at island=0/mission=0, but reload has no Continue and public A overwrites it with a new campaign's zero nectar while keeping the acorn collected. Exact reproduction and repair requirements are in retry_context and kind_robots#3595 comment 6127390759. Release ownership, retain the original implementation PR for its worker's scoped repair. Independent 30 cabinet suites and 28 implementation checks passed but miss this initial boundary. No duplicate implementation, human gate, deployment or publication.

Recover recorded quality pass1 first-mission checkpoint. Original kind_robots#3595 merged, no open Seed repair PR or overlapping task claim; live constructor still omits island0/mission0 Continue. Preserve profile-only Free Flight and explicit New Replanting semantics. Daily five separately complete; no deployment/publication.

Focused first-mission recovery implemented on worker/kr-arcade-t070-initial-save-h6p4. Actual authored acorn red reproduced nectar5-to0; validated campaign checkpoint marker preserves first-mission Continue, legacy campaign-resource inference and profile-only Free Flight distinction. Actual partial-planting, A/Start repeated Continue, Free Flight detour, explicit New Replanting and malformed-marker tests pass. Full35-cabinet arcade command, strict scoped TypeScript, ESLint/Prettier and six native actual input/localStorage/render cases390/768/1440 pass; durable screenshots committed. No deployment or human campaign pacing claim; PR/head CI pending, daily five separate.

Reconciled 2026-10-14: PR kind_robots#3595 merged 2026-10-12T21:48:23Z.
<!-- note:end t-070 -->

## t-071 — Seed Lander depth slice 3: Waterfall Gorge and Firefly Caverns

<!-- note:begin t-071 -->
CABINETS.md section 9, Seed Lander (Lunar Lander riff), slice 3 of 5: Waterfall Gorge and Firefly Caverns. The upgrade is "The Great Replanting". Spec: projects/kr-arcade/depth-pass/CABINETS.md -- read the game's section first; this slice's scope is item 3 under its '#### Slices', and 'Rules for every slice' at the top applies. Code: kind_robots utils/arcade/games/ (registry slug seed-lander). Silas, 2026-10-11: "I need an assessment done of the other arcade games. I want the same level of quality improvements, they should not just be thin veneers of the old games. But newer, better, even more awesome." PART 1 SHIPPED 2026-10-15 (kind_robots #3705, squash 698b6af): Waterfall Gorge island (waterfalls, drip stalactites, pebble rollers, Water mission, Geyser Tortoise). REMAINING: Firefly Caverns (island 4: dark caves with puff-glow light radius, relightable lanterns, crystal bumpers, spore puffballs, bumble buoys, Rescue + Lantern Run missions, Glowworm Queen boss), Free Flight use of the new hazards (BUILT_HAZARDS), and Pixel/HD screenshots. Attract pilot does not finish the tortoise boss.
PART 2 SHIPPED 2026-10-15 (kind_robots #3707, squash 5311ea4): Firefly Caverns (dark caves, crystal bumpers, spore puffballs, Lantern Run, Rescue, Glowworm Queen) and Free Flight now fields waterfalls/drips/pebbles/spores. Not done: bumble buoys, Pixel/HD screenshots.
<!-- note:end t-071 -->

## t-072 — Seed Lander depth slice 4: Storm Shelf, Moon Garden and the Seed Vault

<!-- note:begin t-072 -->
CABINETS.md section 9, Seed Lander (Lunar Lander riff), slice 4 of 5: Storm Shelf, Moon Garden and the Seed Vault. The upgrade is "The Great Replanting". Spec: projects/kr-arcade/depth-pass/CABINETS.md -- read the game's section first; this slice's scope is item 4 under its '#### Slices', and 'Rules for every slice' at the top applies. Code: kind_robots utils/arcade/games/ (registry slug seed-lander). Silas, 2026-10-11: "I need an assessment done of the other arcade games. I want the same level of quality improvements, they should not just be thin veneers of the old games. But newer, better, even more awesome."
PART 1 SHIPPED 2026-10-16 (kind_robots #3732, squash b5b2c45): Storm Shelf island (5 missions, storm sky, gravity 1.0-1.12) and the Thunderhead boss (drifting tops, telegraphed lightning, hail bounce) with pilot probe test. REMAINING: Moon Garden (low- gravity, dust devils, meteor drizzle, Old Lander towing finale), the Seed Vault secret island, credits/endings, Gale Season New Game+, free-standing lightning cloud and hail hazards, true wet-pod weight.
CLOSED 2026-10-20: Moon Garden, Old Lander, Seed Vault, Gale Season already on kind_robots main (verified by tests); Storm Shelf lightning clouds + wet-pod rain weight shipped in kind_robots#3923 (squash dac2a72).
<!-- note:end t-072 -->

## t-074 — Ribbon Riders depth slice 1: The riding feel and the wrap-up

<!-- note:begin t-074 -->
CABINETS.md section 10, Ribbon Riders (Tron light cycles riff), slice 1 of 4: The riding feel and the wrap-up. The upgrade is "The Lantern Festival Circuit". Spec: projects/kr-arcade/depth-pass/CABINETS.md -- read the game's section first; this slice's scope is item 1 under its '#### Slices', and 'Rules for every slice' at the top applies. Code: kind_robots utils/arcade/games/ (registry slug ribbon-riders). Silas, 2026-10-11: "I need an assessment done of the other arcade games. I want the same level of quality improvements, they should not just be thin veneers of the old games. But newer, better, even more awesome."
Merged as kind_robots#3592: a 48x48 grid with bigger animated bikes, brake and turbo, slipstream chains and whiskers, the wrap-up rule, six pickups, six rival personalities, the arena data format with six Midway arenas, and the music loop.

Independent reviewer audit on October 12, 2026 at 2:53 AM PT confirmed kind_robots#3592 merged at 76061205dbe9e441b91d0eb44f7ac6745238368e, current head 8b84c29e6ab32e4a78ef43f7d53d0c858aee96df with all 29 checks completed green. Read the complete ten-file diff and first-slice specification. All 29 cabinet suites passed independently; actual native renderer at 390/768/1440 widths showed public-steering wrap capturing a rival and awarding area score, plus timed-gate and Pier arenas without overflow. Fixtures use staged arena state, not live deployment or human campaign pacing evidence. First slice accepted; later fairgrounds/bosses/co-op remain separate tasks. Clear residual owner on already-done t-074 and add the missing idempotent completion learning.
<!-- note:end t-074 -->

## t-078 — Brick Bloom depth slice 1: The bloom core

<!-- note:begin t-078 -->
CABINETS.md section 11, Brick Bloom (Breakout / Arkanoid riff), slice 1 of 5: The bloom core. The upgrade is "The Glasshouse Grand Tour". Spec: projects/kr-arcade/depth-pass/CABINETS.md -- read the game's section first; this slice's scope is item 1 under its '#### Slices', and 'Rules for every slice' at the top applies. Code: kind_robots utils/arcade/games/ (registry slug brick-bloom). Silas, 2026-10-11: "I need an assessment done of the other arcade games. I want the same level of quality improvements, they should not just be thin veneers of the old games. But newer, better, even more awesome."
2026-10-13: Slice 1 shipped in kind_robots#3643 (squash 9dcf56f, Contract Tests green on attempt 2 after a 15-min job timeout on attempt 1). Authored walls (12), Bloom Bed, Pollen Chain, Last-Crate Rush with Bumble, Leaf Curl, ball heat, roof chime, sprout/hinge/puffball crates, R/T/Q seeds. Pilot probe seeds 5/9/13: last three crates 3.7-10.5 s (target <30 s). verifyCabinetBrickBloom.test.ts added; test:arcade-engine 34 suites, vue-tsc, eslint, prettier clean. No saves/co-op yet (later slices).
Reconciled 2026-10-14: slice 1 PR kind_robots#3643 merged 2026-10-13T21:48:27Z; later slices tracked as t-079+.
<!-- note:end t-078 -->

## t-098 — Rover Ramble depth slice 1: Course engine and Moon 1

<!-- note:begin t-098 -->
CABINETS.md section 15, Rover Ramble (Moon Patrol riff), slice 1 of 4: Course engine and Moon 1. The upgrade is "The Five Moons Rally". Spec: projects/kr-arcade/depth-pass/CABINETS.md -- read the game's section first; this slice's scope is item 1 under its '#### Slices', and 'Rules for every slice' at the top applies. Code: kind_robots utils/arcade/games/ (registry slug rover-ramble). Silas, 2026-10-11: "I need an assessment done of the other arcade games. I want the same level of quality improvements, they should not just be thin veneers of the old games. But newer, better, even more awesome."
Slice 1 shipped (kind_robots#3854, squash 460ecc2): authored A-Z course (roverRamble/course.ts) replacing ROVER_CURVES, outpost reports with stamps, course end at Z, rear-view HUD and pursuers, landmines, tanks, bomber and zig saucers, moon creepers, dust devils, ramps with big-air, boulder stomp. Moons 2-5 reuse the threats on harder scripts until slices 2-4. CI green (57 cabinet suites).
<!-- note:end t-098 -->

## t-149 — Verify Sink Suds earned records through the shared cabinet keepSave and retirement lifecycle.

<!-- note:begin t-149 -->
Reviewer kaizen after repaired kind_robots#3558: the game and withSave/JSON/sanitizeSaves helpers now preserve New Wash -> Squeaky Clean progress. Exercise the actual ArcadeCabinet and arcade store consumer: load a valid later-room checkpoint with prior medals/times, choose New Wash, finish a staged Squeaky Clean basin, then leave/retire and reopen the cabinet through the real keepSave path. Verify new and old best times, medals, reached rooms, skin, golden soap and clear persist while the campaign checkpoint resets. Cover immediate exit after New Wash as a separate transition. Reuse the existing consumers, scoped browser fixtures and storage boundary; fix only a reproduced integration gap. Preserve auth, alerts, validators, required checks and score ceilings. Keep staged fixture evidence distinct from deployment or human campaign timing.
RAN 2026-10-20: added utils/scripts/verifyCabinetSinkSudsSaves.test.ts (kind_robots#3892): New Wash -> Squeaky Clean -> leave/return through withSave/JSON/sanitizeSaves keeps new+old times, medals, reached, skin, golden, clear; checkpoint resets; slower run keeps best; immediate exit after New Wash covered. No integration gap found; test-only.
<!-- note:end t-149 -->

## t-156 — Achievements: three per game with badge art, an achievements section, and a refreshed jellybean catalog

<!-- note:begin t-156 -->
Silas, 2026-10-15: "our arcade needs support for achievements ... 3 achievements for each game, with art, and an achievements section. This should extend to any of our other games: Zuzu experiences, shifting desks, etc. I fully authorize making new art for anything." Shipped in silasfelinus/kind_robots#3700 (merge ca4997a): 117 game achievements across 39 games (32 cabinets judged from score/level/mastery at run end; Zuzu Showdown, Gamebook, Shifting Lands, Shifting Desks, Zuzu's Lair and Emperor of Dust fired at the deed; Zuzu Pinball through a new table feats channel), the cabinet pane and game sidebars list each game's three, /achievements gains section chips, and 14 outdated site jellybeans were re-pointed or replaced (retired rows deactivated, earned records kept). achievement-catalog-maintenance.yml seeds the rows and queues entity-backed Krea 2 badge art on merge. Rendered-art and live-earn verification is t-157.
<!-- note:end t-156 -->
