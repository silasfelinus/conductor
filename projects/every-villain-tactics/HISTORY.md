# every-villain-tactics — task history archive

Full `note:` prose for completed every-villain-tactics tasks, moved out of `roadmap.yaml` so the
Kind Robots projection payload (`scripts/sync_kind_robots_projection.py`, hard limit
4,000,000 bytes) stays well clear of its ceiling. See conductor/t-158.

Each note below is the **verbatim** original — nothing is summarized or trimmed. The
`roadmap.yaml` task keeps its own first sentence plus a pointer here. The HTML comment
markers delimit each note exactly; `archive_done_task_notes.py --verify-only` re-extracts
every note and checks it byte-for-byte against what the roadmap recorded.

## t-001 — Build Playbook Kit Vignette spec and designed console front screen

<!-- note:begin t-001 -->
npm run playbook:new in kind_robots; one-screen illustrated stage at /admin/every-villain-tactics, a real map, cast cards and tutorial battle instead of forms/status copy. Reuse real existing Prom of Doom character art and stable IDs. Queue painted new art with provenance, not fake coverage. Test 390/768/1440 widths, touch/keyboard/controller, reduced motion.

First Bell training console and Playbook Kit Vignette implemented on Kind Robots worker/every-villain-tactics-t-001-20261028-k7p2. Includes the existing Comet City art, 48-identity roster, playable seeded demo, LOS and odds preview, perspective scene sketches, full-screen admin tab and focused CI test workflow. The full tactical engine, 6 campaigns and actual delivered character art remain separate follow-on tasks. Awaiting CI and reviewer verification before merge.

Kind Robots PR #4409 merged as c1587ff; 26 head checks successful. First Bell playable admin console, canonical 48-identity roster, Vignette kit, seed-combat prototype and responsive UI merged. Dedicated full engine, authored four-role narrative and asset delivery remain separate roadmap tasks.
<!-- note:end t-001 -->

## t-002 — Create deterministic movement, cover, LOS and accuracy mechanics

<!-- note:begin t-002 -->
Pure seeded tile/elevation combat engine: pathfinding, AP, directional half/full cover, line blockers, high ground, range, flank, statuses, overwatch, attack hit and damage. Show LOS/available targets/hit percentages from a hovered destination BEFORE moving; display formula breakdown and use exactly that formula for resolved attacks and enemy AI.

Pure seeded combat system implemented in kind_robots branch worker/every-villain-tactics-t-002-20261029-c9v4. Integrates movement AP and dash cost, direction-sensitive half/full cover, flank/elevation, obstructed LOS, suppression/guard statuses, overwatch reactions and cover-aware deterministic AI. First Bell now exposes exact projected hit formula and AP on the command deck, including mobile odds preview. Added combat regression tests and CI runner; review and final CI required.

Kind Robots PR #4430 merged at 3aa72a1; all 23 head checks completed successfully. Pure AP/movement/pathfinding, directional cover, flank/high-ground LOS, deterministic attack previews and resolution, suppression, overwatch reactions, cover-aware rival AI, UI controls, target list, and regression suite. No production deployment or rendered cross-device acceptance claimed.
<!-- note:end t-002 -->

## t-003 — Playable First Bell battle in all four authored perspectives

<!-- note:begin t-003 -->
One complete start-to-ending seeded battle with two tactical approaches, independently authored hero/villain/henchman/sidekick dialogue, cinematic opening, multiple triggered exchanges, closing/ending, and a first bespoke fixed-cast route. Correct flip/strike/hit/death animations and accessible alternatives. Treat this as Playbook Kit Vignette, not full Saga.

Implemented First Bell campaign vignette with distinct authored hero/villain/henchman/sidekick opening, alarm, first-down turning-point, victory and defeat scenes; two approach routes and meaningful battle effects for rescue, containment, mercy and pressure. Backdraft's default fixed-cast route includes personal origin dialogue; other chosen leads remain exploratory roster previews, not counted as completed personal routes. Cinematic choice overlay, accessibility keyboard, card strike/hit/dodge/defeat animations and reduced-motion support implemented. Awaiting PR and full CI; rendered multi-device QA unverified.

Merged Kind Robots PR #4447 as af3a9cfe on main; 23/23 checks passed. Four authored perspectives with opening, turn alarm, rival-down reckoning, victory/defeat scenes, two infiltration routes, rescue/evidence/mercy effects, one bespoke Backdraft route and accessible animated card combat. No production deploy or public publishing claimed. Remaining 48 personal routes and six-level expansion stay roadmap work.
<!-- note:end t-003 -->

## t-004 — Map designer with terrain, cover, spawns, objectives and testing

<!-- note:begin t-004 -->
Admin in-browser paintable tile/elevation/obstacle editor with destructible props, squad spawn areas, victory/fail criteria, reinforcements, hazards, timings and AI behavior. Playtest in editor with exact game rules.

Submitted editable 9x6 studio implementation: fountain/quad, lab, plaza and First Bell stage presets; wall/cover/elevation/spawn/secret/hazard brushes, legality and accessible UI, seeded combat playtesting and regression CI. Initial editor is intentionally a Vignette slice. Fully interactive hazards, reinforcements, scripted triggers and saved/community-level editing remain t-004/t-005/t-011 follow-on scope; do not call them complete.

Merged Kind Robots PR #4451 as 3dfd9ace on main with all 16 head checks completed successfully. Delivered editable 9x6 walls, directional cover, elevation, squad/rival lead spawns, objective and turn limit, secrets and hazard markers, First Bell/fountain quad/science lab/plaza presets, validation and seeded battle playtests using the actual stage map, LOS, deterministic hit math and AI. This is a t-004 Vignette increment, NOT the full editor deliverable. Remaining t-004 work includes runtime destructible props, actual hazard and secret effects, reinforcement waves/AI scripting, flexible victory/failure criteria, and editor playtest coverage for each. Stage drafts are not persisted/shared yet; the linked t-005/t-006/t-011 tasks own cinematic editing, save-state and community sharing. No authentic new art, authored Picnic Panic battle, production deployment or final visual acceptance claimed.

Submitted a scoped live-enemy editor increment: Picnic Panic preset now uses Cornerstone's three named one-hit Warren Wreckers instead of generic rival heroes. A real deterministic two-turn burrow telegraphs safe tile destinations, supports blocked-tunnel counterplay, and applies normal attack, overwatch and shared LOS rules on emergence. The board displays accessible dust warnings. Added seeded studio regression tests; the six-mission editor, destructible props, hazard effects, expanded waves, civilian rescue and ArtJobs remain separate unfinished work.

Merged Kind Robots PR #4454 as cbb6bb5796728627c1943b844bd739b2dbecd3fd after all 16 final head workflows passed. Picnic Panic now spawns Foreman Thumpkin and two one-hit Warren Wreckers with deterministic next-turn burrow warning rings, blocked-emergence counterplay and real combat/LOS/overwatch rules. New seeded tests prove the behavior. This is a scoped t-004 live encounter increment; stage sharing, destructive scenery, active hazards, civilian rescue, lieutenant boss AI, original art, 96 personalized levels and narrative cinematics remain unfinished and separately tracked. Return READY.

Bounded map-studio battle increment: use the actual 48-signature villain lieutenant catalogue, add a Quarry lair playtest with Cornerstone's powered four-HP Mags Hardpan, distinct from 1-HP Warren Wrecker henchmen and Foreman Thumpkin's minor-captain role. Implement telegraphed seismic mechanic with actionable shot/move counter, battle UI and deterministic playtest. Keep 48 levels and bosses unfinished.

Added an actual seeded playable Quarry lieutenant editor preset, sharing existing tactical movement, LOS, hit chance, overwatch and burrowing. Mags Hardpan from canonical Cornerstone dossier is an independent four-HP seismic lieutenant; Foreman Thumpkin remains the 1-HP Warren Wrecker species captain, accompanied by a second 1-HP burrower. Mags marks 3x3 danger one turn ahead; squad can dodge or interrupt with normal hit. Added accessible tile highlights, clear authored dialogue and seeded mechanic tests. One boss prototype only: 48 lieutenants and 96 story stages remain authored concepts, not playable or painted. Kind Robots PR/CI pending.

Merged Kind Robots PR #4459 as 4adf16c1671d213bfb719d0d63c79655e4320885 after all 16/16 latest-head checks passed. New playable Quarry lair Stage Studio preset demonstrates Cornerstone's separate four-HP Mags Hardpan lieutenant versus two one-hit Warren Wrecker SPECIES minions, one named Foreman Thumpkin, with existing burrow AI. Mags marks the exact 3x3 quake tiles a full turn before impact. Legal normal shot hits interrupt the drum; legal player movement avoids damage. Seeded checks cover identity/HP distinction, telegraph, determinism, applied quake, dodge, interrupts, studio map, client preview and accessible warning. This remains one actual boss battle, not all 48 lieutenants or 96 stages. Remaining t-004 editor features, civilian rescue, destructible scenery, full authored scenes, SPECIES DB/ArtJob provenance, other lieutenants, save-sharing, visual screenshots, final human gates remain open. Re-arm for development.

2026-10-30: Merged kind_robots#4498 as 56d048ec after 22/22 green checks. This increment
carries t-018 scope (t-018 is still waiting on this task). It adds two more canonical
one-hit SPECIES crews as studio rival line-ups. Clockwork Wombat Ronin (Lieutenant
Teakettle) teleport: each marks a clock-face exit on its target's uncovered side, then
phases through it next turn; standing on the exit jams the portal. Licensed Legends (Sir
Cap-Permission) are wind-up toys: they swarm and block, and stamp a one-turn 'sealed'
status that locks a hero's signature power. New presets: Portal Watch at the Fountain
and Knockoff Mascot Recall; the studio gains a rival line-up selector and a Civilian
brush. Picnic Panic gains three named picnickers with a 1-AP evacuation action,
telegraphed tunnel abductions from Warren Wrecker dust rings, a defeat if every family
is lost, and original opening, three triggered and two final scenes driven by fired-
trigger history. Saves validate all of the new state. New tests:
verifyEveryVillainLackeys and verifyEveryVillainPicnic. Remaining t-004: destructible
props, active hazard/secret effects, reinforcement waves, flexible victory criteria,
saved/shared drafts. No art claimed.

2026-10-30: Merged kind_robots#4507 as f1171fad after 22/22 green checks; completes the
original t-004 scope. New stageRules.ts with live rules copied into the battle
(state.rules) and runtime field state (state.field); rule-less stages are byte-identical
to before. Breakable props: 1-3 HP all-round half/full cover, chipped by every shot at a
sheltering unit (hit or miss, incl. overwatch/AI), by quakes and by fire; at 0 the cover
is gone. Ticking hazards at round end: fire burns occupants and props and spreads one
tile per round to a tile telegraphed a round ahead (standing on it stamps it out, cap
8); water is live on even rounds; weak floors count down and collapse into impassable
rubble, shoving the occupant for 1 damage. Telegraphed reinforcement waves of canonical
one-hit crews (Warren Wreckers/Wombat Ronin/Licensed Legends) arrive on hatches marked a
round early; occupying a hatch seals it. Flexible victory: defeat all (waits for pending
waves), survive N, hold zone N, defeat named boss, evacuate N civilians (with
impossible-rescue defeat); turn limit and squad wipe still fail. Saves verify
rules/field/terrain/arrived reinforcements and reject forged props, floors, fires and
waves. Studio: 6 new brushes, victory/wave controls, presets Boiler Room Breach and Hold
the Fountain Steps (also in the front-menu One-Shot list), a local draft shelf (12) and
plain-JSON share codes imported via a strict allow-list. Fixed: Picnic Panic triggers
fired from Warren Wreckers/civilians in other stages made Quarry saves unloadable.
Verifier verifyEveryVillainStageRules (seeded tests for each feature, 8 save forgeries,
export/import of all presets). Server publishing stays with t-011; AI-behavior choice is
the existing rival line-up selector. No art claimed.
<!-- note:end t-004 -->

## t-005 — Opening/triggered/closing conversation tree and cinematic editor

<!-- note:begin t-005 -->
Author speaker/identity/role/emotion/camera, choice nodes, conditional branches, state effects and triggers for turn, tile, line of sight, health, rescue, objective, faction, kill, secret and chained conditions. Graph validator detects unreachable nodes, softlocks and missing actors/art.
2026-10-30: Shipped in two kind_robots PRs, each 22/22 green: #4510 (5e029a94) and #4513 (squash merged after it). sceneGraph.ts handles opening/triggered/closing scenes. Lines carry speaker (narrator, a stage unit or a canonical identity), an optional role tag (the hero/villain/henchman/sidekick), emotion (6, mapped to the speaker's shipped portrait) and camera (4). Choices (2-3) can set a flag, heal or suppress. Conditional branches check a flag, the player's viewpoint, whether a unit still stands, or which team outnumbers the other. Triggers: round, tile, line of sight, health, kills, rescues, secret, objective progress, faction lead, after-scene, flag (chained) and closing by outcome. Triggers latch into the save's fired history, and choice effects apply once when a scene finishes. The graph validator reports broken links, unreachable lines, softlocks, unknown actors, actors without shipped art, impossible triggers or conditions, unset flags, chain cycles and duplicate openings. Saves accept only this stage's scene ids and settable flags. The studio MAP/SCENES pane is the cinematic editor: scene list; trigger params; per-line speaker, role, emotion, camera and text; THEN targets; choices with targets and effects; IF branches; preview. Boiler Room Breach ships an original 7-scene script. Scripts travel in share codes through the strict importer. Verifier: verifyEveryVillainScenes. Scripts for the six campaign missions belong to t-007; server sharing belongs to t-011.
<!-- note:end t-005 -->

## t-006 — Save/load battle and level state including RNG and fired events

<!-- note:begin t-006 -->
Persist reproducible seeded state, unit positions/conditions, story flags, trigger history and schema version; multiple save slots, migration and tests. Do not disturb original Prom of Doom saved games.
2026-10-30: Shipped in kind_robots#4494 (squash 8a46c38d) after 22/22 green checks. utils/everyVillainTactics/saves.ts provides an auto slot plus 3 manual slots under kr- every-villain-tactics:save:*; Prom of Doom keys are untouched. Saves are schema v2: the exact seeded battle (xorshift RNG state, units, statuses, power cooldowns, burrow/seismic/signature warnings), the First Bell story run, and the new fired-trigger history (story beats, fire alarm). A tested migration from the v1 pre-role battle shape keeps legacy units on the default profile. A canonical-JSON checksum rejects edits. Each load is also rebuilt against a fresh reference roster, so 20 tested forgeries with recomputed checksums are rejected (HP, identity, role stats, power, cooldown, walls, overlaps, terrain, roster, story endings without triggers, unknown fields, slot copying, newer versions). Story and one-shot modes are isolated. Console: CONTINUE resumes the newest valid slot, per-slot SAVE/LOAD shows summaries or refusal reasons, and each round autosaves. The full t-016 splash/New/Continue/Settings/Scrapbook shell is not built; t-016 owns it and can reuse these slots.
<!-- note:end t-006 -->

## t-016 — Cinematic front menu, story/one-shot modes, settings and scrapbook shell

<!-- note:begin t-016 -->
Front-load splash with New and Continue for both story and replayable one-shot fights, Settings, and a visually explorable scrapbook. Ground Continue and awarded scrapbook tiles in t-006 saves (never fake progress); preserve the admin-only route and original Prom saves. Story supports flexible foil selection without erasing exclusive fixed-cast arcs. Phone/desktop console QA.

Scoped cinematic intro increment for both Prom of Doom and Every Villain Tactics. Shared 192 role-key reveal definitions, accessible CSS comic panel with typography over real art, image fallback, keyboard dismissal, reduced-motion support, automatic first appearances and replay via character dossiers. The default six-subject Capes checkpoint review is already under a different claimed task t-028; no duplicate art jobs created. Remaining full tactical splash/new/continue/settings/scrapbook shell and complete ArtJobs are still unfinished; return t-016 ready.

The shared comic-character introduction slice was merged to Kind Robots main in PR #4461 at 62f2ad0 after 18/18 fresh CI checks passed and a non-force conflict reconciliation. Responsive accessible 48-character role-key reveals now exist in both Prom of Doom and the Tactical training console. This is NOT completion of tactical New/Continue/Settings/Scrapbook, saved first-seen ledger, verified original art delivery, or human visual QA. Return t-016 to ready for its remaining named shell work. Art export issue kind_robots#4470 tracks the already-rendered but unshipped six origins and eight affinities.

2026-10-30: Merged kind_robots#4505 as b3564f33 after 22/22 green checks. Title screen
over shipped Prom art (front/splash-v2) with New Story, Continue, One-Shot, Settings,
Scrapbook and a way back to the console (HUD MENU button). New Story picks 1 of 4
viewpoints (lead outcome art) and any of the 48 leads; Backdraft is labelled the only
bespoke fixed-cast route. Continue resumes the newest valid t-006 slot. One-Shot lists
Picnic Panic plus 5 studio presets. Settings: animation speed off/fast/normal/cinematic,
confirm-before-end-turn (two-press END TURN), threat preview (reachable tiles visible to
rival shooters, exact rival formula, hovered-tile odds), restore defaults and erase
saves+scrapbook behind confirm. Scrapbook: 12 pages, one per recordable trigger,
unlocked only from validated saves; no points or medals (t-019). Keyboard roving/Escape;
Playwright-rendered at 390/768/1440 in a component harness with no page errors or
overflow. Also fixed a #4494 bug: createSave structuredClone'd Vue reactive state, so
browser SAVE/autosave never wrote; regression test added. New verifier
verifyEveryVillainFrontMenu. REMAINING for done: flexible rival-foil selection in New
Story (only the squad lead is selectable; rivals stay the First Bell trio), and the
battle console itself is still cramped at 390px (pre-existing).

2026-10-30: The last missing piece shipped in kind_robots#4517 (squash 9cfefaee; all 20
triggered checks green). New Story now has a Rival foil portrait strip (48 heroes,
villain-outcome art). Squad duplicates are disabled; the default stays First Bell's
written rival, Skyline. The foil fights with their own role and power. Saves store an
optional foilSignature only for a non-default foil, so old saves are byte-identical; a
duplicate or dropped foil is refused. Labels state honestly that a non-default foil
plays the shared script (bespoke matchups are t-020), and Backdraft's fixed-cast route
is untouched. Together with #4505 the original scope is met: front splash; New, Continue
and One-Shot (8 presets); Settings; save-grounded Scrapbook; admin route; Prom saves
untouched; Playwright QA of the menu at 390/768/1440. Known issue for t-013: the battle
board itself is still cramped at 390px.
<!-- note:end t-016 -->

## t-017 — Distinct signature hero powers and tactical range/mobility/defense roles

<!-- note:begin t-017 -->
Define actual stats, short/mid/long range weapon profiles, mobility, defenses/tanking/support and at least one named mechanically distinct power per each of the 48 canonical heroes. Seeded legal-target previews, special cooldowns/AP/status/AI parity, accessibility and encounter balance. Start with a small tested roster subset, then verify 48/48 authored powers.
2026-10-30: Shipped in kind_robots#4490 (squash 7b12e664) after 23/23 green checks. All 48 canonical heroes have a tactical role (8 roles: striker, skirmisher, tank, controller, duelist, sniper, guardian, support) with short/mid/long weapon falloff curves, aim, mobility (walk/dash), HP and defense, and one previewed signature active power with AP cost, threat/target tiles, a recharge (2-3 turns) or once-per-battle limit. 42 powers are generated from the canonical Prom origin x affinity power data (8 affinity families x 6 origin modifiers, test-verified as 48 mechanically distinct fingerprints) and 6 are hand-authored for the First Bell cast: Backdraft Flare, Updraft Catch, Heartbeat Quake, Thermite Cut, Adhesive Pad Volley, Grand Illusion. The new verifyEveryVillainPowers test runs 395 seeded preview-vs-resolution checks (only strikes roll RNG, with the displayed shot formula plus an aim bonus), confirms allies are never harmed, checks recharge limits, and checks AI determinism with rival use of powers across all 48 rosters. Console: POWER action (key P), gold target tiles and outlined threat tiles, an effect list, role lines, and role and power on all 48 dossier cards. Prom of Doom interludes opt out (roles: false), so their saves and balance are unchanged, and the EVT workflow now runs the Prom tactical suites. Balance is sanity- tested only (stat ranges, weapon ordering, AI usage); human playtest tuning is part of t-014.
<!-- note:end t-017 -->
