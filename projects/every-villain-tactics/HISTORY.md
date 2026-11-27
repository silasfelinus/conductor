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

## t-007 — Write and implement all six distinctive tactical story missions

<!-- note:begin t-007 -->
First Bell: basic combat; Science Wing Lockdown: doors and destructible cover; Crosswalk Crisis: civilian rescue/split objectives; Rooftop Broadcast: elevation/overwatch/betrayal; Under-Comet Breach: hazards/timer/multi-squad; Prom Night Everybody's Villain: three-phase finale. Each needs original opening, branching mid-fight, closing scenes, story callbacks and losses.

First Bell post-match navigation and terrain legibility increment is staged for review in Kind Robots. An art-led result panel links to playable One-Shots, replays, and the main menu without pretending the six story chapters are implemented. Existing Comet City illustrations now fill the arena and unit cards. The wider six-mission task remains unfinished after this slice.

Merged reversible First Bell post-match/art/terrain UX slice in kind_robots PR #4855 (merge ea4c4c811f83b7cee7318dea7657df6bf65f3e01) after all eight commit suites completed successfully, including all four contract shards. The six bespoke story missions are NOT complete; return t-007 to ready for continued development and keep the authored map art backlog visible.

Authored 12 private Unstable Diffusers tactical art subjects in art/TACTICAL-ARENAS-ROUND-1.yaml: six campaign location plates, four existing one-shot location plates, and two illustrated First Bell outcomes. Auto-submit starts only after main merge and real ArtJob receipts must be verified separately. The six distinct story missions are still unfinished.

Merged internal tactical art queue PR silasfelinus/conductor#7120 (8ea4ace24521d0f2e1fedec182b5ee3aadecdbda) with all PR checks completed successfully. Twelve private painted arena/result prompts now auto-submit through Auto Art Generate; accepted ArtJob IDs and rendered delivery still require receipts. The remaining authored six-mission story work remains ready and uncompleted.

Scoped authored Science Wing Lockdown encounter: distinct hero/villain opening, eight-round shutter deadline, destructible lab benches, live coolant-water hazard, turn-two rescue-or-evidence choice with real heal/suppression effects, flags and ending callbacks. Target repo implementation branch worker/every-villain-tactics-t-007-science-lockdown-5c91. Remaining multi-mission authored campaign work stays open.

Merged reversible Science Wing Lockdown authored story encounter to kind_robots main in PR #5107 (57e9fbc) after all seven CI workflows passed. Seven scenes, hero/villain testimony, turn-two rescue/evidence decision with real heal/suppress effects, branching callbacks, laboratory cover/hazard rules and regression coverage. Fixed rejected first-six-cast reveal prompts in Conductor PR #7340 (3b09526); generated ArtJobs remain unconfirmed until the triggered Auto Art Generate run records numeric receipts. Remaining work: Crosswalk Crisis, Rooftop Broadcast, Under-Comet Breach, Prom Night finale, linked six-mission campaign transitions, QA and art delivery.

Crosswalk Crisis authored rescue stage staged in Kind Robots branch worker/every-villain-tactics-t-007-crosswalk-e8f2. Uses existing generated harborline map ArtImage 265022, three civilians at opposite ends, eight-round evacuation objective, traffic props, electrified runoff, wind-up reinforcements, seven cinematic scenes with hero/villain branches, first-rescue beat and choice consequences. Contract tests include knockout-does-not-win and actual extraction. Awaiting PR CI.

2026-11-13 PT: Merged Crosswalk Crisis in Kind Robots #5121 (c310b0d) after all seven workflows passed. A real three-civilian eight-round rescue stage with traffic cover, runoff hazard, licensed mascot reinforcements, seven branching comic scenes, 48-identity support and authored outcome is playable from One-Shots using generated Crosswalk ArtImage 265022. The dedicated tactics, layout, TypeScript, formatting, architecture, schema, and four contract shards were green. Remaining t-007: connected six-chapter progression, Rooftop Broadcast, Under-Comet Breach, Prom Night finale, and full mission playthrough QA. Separately, all twelve first-six-cast hero/villain reveal ArtImages (270741–270752) are DONE but need attachment/visual verification under the art task.

2026-11-19 PT recovery: prior claim from 2026-11-19T20:25:00Z exceeded Conductor's 90-minute lease. GitHub branch search found no worker/every-villain-tactics-t-007 branch and open PR searches found no Rooftop Broadcast or Crossfire implementation PR. Releasing the stale reservation without changing any accepted mission content; First Bell, Science Wing and Crosswalk progress remains preserved on main.

2026-11-19 PT: Staged playable Rooftop Broadcast tactical chapter four as a distinct selectable one-shot on Kind Robots branch worker/every-villain-tactics-t-007-rooftop-20261120T010620Z-m7b2. Elevated 9x6 antenna hold, catwalk collapse, cover and telegraphed Licensed Legends reinforcement; nine hero/villain-aware scenes with gameplay-altering warning versus jamming decision, conditional closing consequences and deterministic studio tests. Uses existing finished ArtImage 265023. This is a vertical slice, not linked six-chapter progression. Rooftop test CI and final PR review remain required, then return umbrella t-007 to ready.

2026-11-19 PT: Rooftop Broadcast (Crossfire chapter four, real hold-zone gameplay and nine authored scenes) merged into kind_robots main via PR #5377, merge 0cd2bc15 after all required checks passed. Release its review reservation and return t-007 to ready for Under-Comet Breach, the Prom Night finale and connected six-chapter progress. No full campaign or completion is claimed.

2026-11-19 PT: Under-Comet Breach authored stage five committed to Kind Robots branch worker/every-villain-tactics-t-007-under-comet-breach-q9r4. New separate split-entrance battlefield with a seven-round defeat-seal-keeper objective, three active hazards, two telegraphed reinforcement waves, nine opening/choice/closing scripted scenes, two real choice effects, and seeded combat/story assertions. Reuses existing verified ArtImage 265024, no new art or route/save mutation. This is a partial six-mission task; Prom Night finale and durable linked progression are not done. Await full CI and merged PR, then return to ready.

2026-11-19 PT: Under-Comet Breach, Crossfire chapter five, merged into silasfelinus/kind_robots main via PR #5381 (d7cafdd) after all seven latest-head workflow suites passed. Distinct timed seal-keeper battle, split entry, hazards, waves, nine authored branching scenes and seeded QA. Return unfinished six-mission umbrella t-007 to ready: Prom Night finale and durable linked chapter progression still need implementation. This is not full campaign or human-playtest readiness.

2026-11-19 PT: Staged playable Prom Night: Everybody's Villain chapter-six finale on Kind Robots worker branch worker/every-villain-tactics-t-007-prom-night-finale-20261120T040500Z-k6p9. Distinct 9x6 ballroom, three phases of rival/borrower/mascot pressure, round-three and round-five waves, collapsing dance floor, hazard/cover rules, eleven hero/villain-aware scenes and consequences. Reuses finished ArtImage 265025. Fixed survive-round victory shortcut so players cannot win by clearing early rivals. New seeded gameplay assertions cover phases, choice effects, and earned round-six victory. Pending PR verification. Umbrella remains unfinished until the six missions form a persistent campaign with real postbattle advancement, callbacks and acceptance QA.

2026-11-19 PT CI recovery: Crossfire's authored sixth Prom Night finale merged in kind_robots PR #5386 as c4e9282 after all seven latest-head workflows completed green. Corrected the unrelated Slime City PvP reconnect regression to schedule two simultaneous host-tab races by host action, preserving the strict one-winner assertion and full Slime City contract coverage. Earlier Prom patrol rescue PR #5385 had already merged as fee5f93; obsolete failing PR #5370 is closed. All six Crossfire battle stages are independently selectable and playable, but the six-chapter persistent progression, carryover and full end-to-end acceptance testing are still incomplete. Return umbrella t-007 to ready for campaign linking; do not close canonical issue #4407 or mark Playtest.

Focused Crossfire campaign connection on worker/every-villain-tactics-t-007-crossfire-journal-a6bf: six authored chapters now have an ordered replayable progression journal, separate v1 Crossfire key with embedded validated v2 battle checkpoints, first-bell ending requirement, next-stage advancement and resume UI. Script-specific scenes, shared 48 identities and old slot keys are preserved. Full six-chapter adversarial acceptance, cast-specific branching, art and 48-route completion remain pending. Kind Robots PR/checks to follow.

Continuity increment staged in Kind Robots: completed Crossfire mission choices grant a first-volley guarded squad leader after mercy/rescue or mark the enemy lead after gathering evidence. Surviving squadmates carry at most one wound into the next chapter. All effects derive from completed v2 battle snapshots and are persisted in the existing v1 Crossfire journal; 11 branch scenarios plus wounded/downed ally and save-validation tests added. A compact HUD disclosure shows the prior chapter callback. Remaining authored dialogue, visual acceptance, original art and 48 bespoke routes are not yet complete.

Canonical Crossfire rival continuity staged: the chosen First Bell foil now commands the remaining five stage battles (without changing the separate one-shot cast), and each checkpoint keeps the optional saved foil signature. A duplicate supporting rival gets a stable alternate identity. Old journal stages without foil metadata still load, recovering the chosen opponent on subsequent chapters. Test expanded across all 48 canonical leaders, 5 chapters, legacy migration, forgery and stand-alone compatibility. App PR and completed CI checks required before this can be considered merged.

Six authored Crossfire chapter debriefs now branch on actual rescue, evidence or command choices; four Prom Night conclusions derive from the completed first five battles plus the final shelter/command choice, rather than the HERO/VILLAIN menu selection. Story beats reuse 48 canonical identities, the stable foil, the old Crossfire save key and the existing battle-result art. Added 6x3 chapter-choice checks, all 48 lead aliases, all four earned finales and loss/skip guards in the dedicated Tactics test. Implementation PR pending CI. Full 48-route authoring, cinematic art and whole-run acceptance remain pending.

PR silasfelinus/kind_robots#5449 was already merged; the first Tactics workflow run 44825830068 failed with no jobs, but the subsequent run 44825892656 on the same head completed successfully. Six choice-aware chapter reports and four earned conclusions shipped; personal routes, art and adversarial complete-campaign acceptance remain unfinished. Return to ready.

Scoped Crossfire sixth-chapter gameplay increment staged as kind_robots commit ee07c64. Cumulative five-chapter rescue evidence now changes the final tactical opening: 3 earned rescue decisions guard all surviving squadmates, and 2 evidence branches mark all starting rivals. Preserves legacy saves, seeded campaign structure and canonical identities. New regression covers cumulative branch thresholds, losses and v2 save/load. 48 bespoke fixed-identity routes, art completeness and full QA remain.

Reopen the remaining Crossfire campaign continuity scope for independent production. No open matching implementation PR was found; preserve previously merged contributions and all acceptance requirements. Do not count partial implementation as done.

Crossfire rescue and evidence now independently grant earned tactical carryover and finale allies, including both in First Bell. Preserve existing single debrief classification and save schema. Regression tests for simultaneous statuses, save round trip and finale threshold committed at f9e4c7b03cd5468f21c7794e39af0a7ca86876ad, branch worker/every-villain-tactics-t-007-dual-callback-92b6. Full CI and full campaign QA remain pending; partial scope.

2026-11-24 PT: PR #5799 merged into kind_robots main at 7099e20291fb3785148d4f8e7af2b8b7050c1903 after all seven latest-head workflows passed (including Tactics gameplay and four contract shards). Rescue and evidence independently earn carryover and finale support; full campaign QA remains open. Returning partial umbrella scope to ready.

Crossfire finale now uses shared tactical support thresholds, preserving both rescue and evidence earned on First Bell and rejecting a defeated prior chapter. Rescue ending takes precedence if both thresholds are reached. Kind Robots 3045a23e8983a1f34d9aa1c40cd77a7d16939496; six isolated finale cases passed with stubbed helpers, real-save regression committed for CI. Partial umbrella; full campaign QA remains open.

2026-11-25 PT review reconciliation: Verified #5841 merged ad094b84643b; six chapter continuity fix landed, full campaign acceptance remains. Release partial scope for independent continuation. No open matching implementation PR or worker branch found in either repository.

Campaign replay repair committed to Kind Robots 411c831ca9d1999540f941e6985daa03ce7ebd57: retries reconstruct deterministic chapter opening from verified history, preserving prior injuries and guard/intel/finale support, persisting retry checkpoint and rejecting finished journal replay. Six real-save chapter retry regressions committed. Full CI and adversarial playthrough acceptance pending.

Verified #5860 merged at 95834809244ee8949b0fa75d9363f374e8e02b0f, nine latest-head workflows successful including branch janitor. Chapter retry preserves deterministic campaign opening and prior support. Full adversarial campaign acceptance remains open.

Finite six-mission acceptance audit: 976 assertions passed across 72 paths using extracted actual First Bell and five authored script/scene engine implementations, with synthetic combat events. Permanent regression committed in kind_robots cb2228a68b32b5fc17761fc597702c9ee0bf8360. Existing linked campaign, objective, carryover and retry checks are present; dedicated latest-head CI must pass before closing t-007. Broader all-identity adversarial gameplay and rendered QA remain t-013, personal routes t-008/t-009 and original art t-012. No claim of full live playthrough.

Finite six-mission scope verified and merged in kind_robots#5867, squash 2b1f4bc7148f957c7d314190ccfc71658f35ce52. Latest head 39c50c60b836a5e20cd63cbbde73e4de754a9c20: all seven workflows completed successfully, including dedicated Tactics run 45738017537 and all four contract shards in 45738017440. Reviewed the 72 narrative path regression, both perspectives, branching choices and victory/defeat closure; existing objective, linked chapter and save/retry tests also passed. Full adversarial gameplay and device QA remain t-013; personal routes t-008/t-009 and art t-012. No production deployment or human approval claimed.
<!-- note:end t-007 -->

## t-008 — Author 48 hero and villain playable arcs with distinct supporting cast

<!-- note:begin t-008 -->
For every permanent Prom of Doom identity, author two genuinely different playable routes: protagonist HERO or VILLAIN. Maintain independent characterization, dialogue and consequences for their supporting sidekicks and henchmen as NPCs, not extra starting modes. Audit 96 distinct playable arcs and meaningful supporting-actor agency; reject string replacements and renamed identities. Retain compatibility with saves made under the historical four-role preview. This supersedes the original 192-player-arc target.

Scoped playable increment: Kind Robots commit 2792765c3e3e4a31cc42b2790ed9d731d59bc846 implements 16 hero/villain First Bell arcs for the eight accident identities, with 80 distinct authored scenes and independently voiced squad support. Actual cast names are resolved from battle state; choices and legacy save schema remain intact. Source audit passed 80 unique nonempty scenes; integrated gameplay regression committed, latest-head CI pending. Partial: 40 identities remain, plus deeper supporting-cast agency and full route acceptance.

PR #5877 merged as 331f1c114a62610f86943088cae39fae664667cd after all seven latest-head workflows passed. 80 First Bell routes, 400 authored scenes, 2644 isolated assertions, permanent regression coverage; no remaining worker branch. Release incomplete scope for the final Psychic family and supporting-actor consequences. No full campaign acceptance claimed.

Kind Robots commit aede3283b4bc72ccfc4c77689160e1ce965baca1 adds all 16 Psychic First Bell arcs. All 48 identities now have 96 distinct hero/villain First Bell narratives, 480 unique authored scenes, and roster-wide permanent regression coverage. Extracted selector audit passed 3172 assertions with real roster and authored catalogs, stubbed generic base scenes. CI pending; supporting-actor mechanical consequences and full acceptance remain open, so do not close umbrella t-008.

PR #5885 merged at fea5beec98992795928e7d00a2374f0eea5ad1a1 after all seven latest-head workflows passed. All 96 First Bell narratives now on main. Remaining scope is independent supporting-actor mechanical consequences and full route acceptance; release for next increment.

Reclaimed existing PR #5898 after stale-claim sweep released the previous session during implementation. Commit 9c277f4adc5214f90af7261780ddf9cf1caa4794 adds deterministic independent companion actions, save receipts and field reports, with 1536 isolated story paths passing 19972 assertions and 384 permanent integration paths. Latest-head CI pending. No competing Tactics PR and no production deployment.

2026-11-26 PT: PR #5898 marked ready and squash merged as ef929e6d1d9e37d564718ae0ebdfc9bd63510772 after verifying all seven latest-head workflows at bcd1882606acf5632bfcdad0a0ff19438998fe5d. Tactics gameplay run 45823718109 passed. All 96 distinct hero/villain First Bell arcs and 480 authored scenes were previously delivered in #5877/#5885; supporting NPCs now have independently previewed and applied combat consequences, living-actor checks, refusal, field reports, and backward-compatible save validation. Permanent 384-path regression covers all identities and both player roles. Finite t-008 scope complete; bespoke six-level personal routes remain t-009 and full campaign/device QA remains t-013. No human acceptance, live deployment, or art approval claimed.
<!-- note:end t-008 -->

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

## t-019 — Deterministic post-battle points and earned scrapbook achievements

<!-- note:begin t-019 -->
Mission-end scored breakdown for flawless survival, zero damage, no knockouts, optional secrets, rescues and tactical bonuses, with explicit eligible conditions. Replay-safe recorded points, scrapbook heroes won with, villains beaten and authored route discoveries. Distinguish end-of-turn summaries from mission completion.

Scored battle debriefs, save-grounded medals and replay-safe scrapbook history implemented on the scoped worker branch. Pending PR and CI review.

Merged kind_robots PR #4566 (squash 2c7258c567de71dd8f0212f330506720119986ef) after all 22 commit checks completed successfully. Shipped deterministic post-battle points, visible mission debrief, earned and de-duplicated scrapbook results, medals, score regression suite. Task remains open for true historical no-damage tracking, broader hidden-secret achievements, and hero/villain ledger.

Added durable squad-damage history across gunfire, overwatch, powers and environmental hazards. The untouched medal now requires historical zero damage rather than healed full HP. Legacy saves remain compatible, cannot claim unrecorded flawless medals. Regression tests pending PR CI.

Merged Kind Robots PR #4568 as 9d2ab94dfc87c034682818e6348941cb11bfa75c after all 18 check runs completed successfully. Tactics now records historical squad damage across attacks, overwatch, powers, area hits, fire, water and collapsed floors. Untouched is earned only on a true no-damage victory; healed extraction does not qualify and old saves cannot invent provenance. Remaining task scope: secret-route medals, hero-villain history and campaign level achievements.

After reclaiming the stale t-019 claim and verifying session ownership, authored code for secret-trigger scoring, a new verified hidden-route medal and achievement, and visible 48-identity hero/villain/supported record in the Tactics scrapbook. Reversible scoped PR kind_robots#5470 is open at b0d27fb302e1fb93c536c25dbc0afa20b7049276 with regressions committed. CI pending: no local runtime execution in this connector-only session. Not done: 6-chapter full campaign scoring QA and broader secret-route audit.

Reopen the remaining Scoring and scrapbook scope for independent production. No open matching implementation PR was found; preserve previously merged contributions and all acceptance requirements. Do not count partial implementation as done.

Scoped score integrity repair on Kind Robots worker/every-villain-tactics-t-019-score-integrity-a8e4 at daa31471f90ccc1bd4b38c40dc4c94ea77fef43d. Reject malformed lines, duplicate lines and medals, defeat medals, and medals unsupported by positive score lines without discarding valid neighboring history. Connector-extracted actual validator reproduced old crash and rejected seven corrupt fixtures while retaining two valid records. Full TS and integration suite pending PR CI; six-chapter aggregation remains open.

Verified PR #5812 merged at 1eeeb00282f267c5ea72407aa5fde73ccf347c73 with seven successful implementation workflows and successful branch janitor. Malformed and inconsistent scrapbook records are now rejected. Full campaign scoring remains open; return to ready.

Crossfire journal scrapbook restoration committed at Kind Robots f1d5b6e2856700dec991311bd9a6a85a65956ae0 on worker/every-villain-tactics-t-019-journal-recovery-f93b. Recover validated completed and active chapter saves on load without awarding achievements again; finished journal excludes duplicate finale. Nine isolated selector cases passed with a stubbed validator. Added six-chapter real-save recovery and deduplication regressions to the existing CI verifier. Full integration checks pending; umbrella remains partial.

2026-11-25 PT review reconciliation: Verified #5838 merged 7f707034d252; scrapbook recovery delivered, cumulative six-chapter scoring remains. No open matching implementation PR or worker branch found in either repository.

Cumulative Crossfire scoring and aftermath display implemented in Kind Robots afc89fbb3fed1f13af41ea89908e10709cbc338f. Validated journal only, active victory counts once, no defeat credit, stable on advancement and reload. Six chapter regression coverage committed; CI and rendered QA pending. Full adversarial campaign and secret audit remain open.

Verified PR #5849 merged at 9d1c4b2516b6437d56ada9324d28a92277212493. Cumulative scoring and replay-safe checkpoint totals delivered. Remaining secret-route audit and adversarial campaign scoring QA remain open; release for further work.

Evidence scoring repair committed to Kind Robots 037906bcf8a1905f428593aa808730e847e3dba0. Four authored tactical evidence choices now grant 25 points and victory medal, stage-specific flags only; unchanged legacy score identities. Dedicated score regression tests added. Full CI and remaining secret-route/whole-campaign acceptance pending.

Verified and merged kind_robots#5866 at 43161967c9787864812dfb544a3655a152a674e6. All seven latest-head workflows completed successfully at 037906bcf8a1905f428593aa808730e847e3dba0, including Tactics run 45737097078 and contract run 45737097048. Authored evidence choices in four stages now earn 25 points, duplicate and wrong-stage flags cannot inflate points, defeat cannot earn the medal. Partial: historical scores remain unchanged; secret-route scoring audit remains open. Release for finite acceptance without duplicating t-013 QA.

2026-11-26 PT finite scoring acceptance: rechecked merged #5849 and #5866 and all returned latest-head workflows successful (Tactics runs 45722233951 and 45737097078). Reviewed existing six-chapter journal regression, including defeat exclusion, reload and advance deduplication. Executed 80 passing isolated assertions against current scoreFromSave source with type-only annotations removed, real authored scene IDs from all ten shipped stage scripts and synthetic save fixtures (checksum and flag helper stubbed). All four authored secret routes in Crosswalk, Rooftop, Under-Comet and Prom finale award 125 points and secret-route medal on victory only; unrelated/duplicate trigger IDs cannot increase points, active or defeated fights cannot earn that medal, both allegiances covered. Stages without authored secret scenes award none. The merged integration suite covers evidence, damage history, scrapbook validation, and replay protection. Scoring implementation and finite audit complete; full adversarial campaign and rendered QA remain t-013, not duplicated here. No production playtest or deployment claimed.
<!-- note:end t-019 -->

## t-026 — Every Villain Tactics achievement upgrade: 12 or more live achievements

<!-- note:begin t-026 -->
Silas 2026-11-11 PT, in session: "Our games should all have a base standard of quality ... We want our main games to have 12 plus achievements." Standard: docs/agents/main-game-standard.md; CONTROL.md global overview.

Live today: 0 Achievement record(s) with this game's triggerCode prefix (checked against /api/achievements 2026-11-11). Target 12+ (usually 12-30; tie some to endings but don't go overboard). Mix story, skill, discovery and completion. Create the live records through the existing achievements API (label, message, icon, karma, triggerCode prefixed with the game slug), award them from the game store, show them with components/achievements/game-achievement-strip.vue, and verify one award live after deploy.

Achievement upgrade merged in kind_robots#5037 (aff3ebd), all checks green: 17 live achievements awarded from one scrapbook diff in recordMoments() on live saves only (never on load), plus the stage-studio award in saveDraft(). Catalog seed workflow run 43138740407 succeeded. Contract test verifyEveryVillainAchievements.
<!-- note:end t-026 -->

## t-027 — Record the post-merge media-proof run's per-image aspect/blank/bytes outcome on the t-018 art ledger

<!-- note:begin t-027 -->
Kaizen from reviewer of conductor#7820 (2026-11-22). After the prom-tactics-media-proof workflow runs on main, record each Tactics telegraph ArtImage's actual result (downloaded bytes, aspect match, blank check) against its ledger receipt, so receipt-only rows stop counting as delivery. Never publish private art or switch is_public.

Scoped art QA implementation: authenticated private byte length, decoded image dimensions, blank and aspect check, pixel checksum and safe per-image media_proof metadata on the twelve t-018 receipts. CI workflow checkpoints only metadata with exact ArtJob/ArtImage identities and preserves the original private images and is_public=false. Branch worker/every-villain-tactics-t027-private-media-evidence-20261122-k5r8; pending full CI, merge and production API-run evidence before completion.

Verified completed finite QA scope: Conductor #7837 merged at 957cfd62e13375439a666c4c45f7e06cc2f00640 with four successful latest-head workflows. Main ledger records twelve matching ArtJobs 74393–74404 / ArtImages 277786–277797, all VERIFIED with nonzero downloaded bytes, decoded dimensions, aspect_match true, blank_check PASS and pixel hashes. Production proof run 45118667491 job 137507202611 completed successfully, including Tactics gameplay media and private access. Artistic approval and remaining gameplay work are separate.
<!-- note:end t-027 -->

## t-028 — Generate the tactical arena receipt map from verified ledger keys so fallback paintings drop out once an original venue render is proven

<!-- note:begin t-028 -->
Kaizen from reviewer of conductor#7853 (2026-11-22). The three dedicated venues (Last Order diner 71163/276806, Sunken Street 74323/277221, Valcourt Library 74324/277330) are pinned by hand in tests and the workflow. Source the arena→receipt map from ledgers whose media proof passed, and keep explicit art-review decisions separate, so a fallback painting cannot linger after an original render is verified.

Proof-backed generator, generated receipt map and runtime override implemented on scoped Conductor and Kind Robots worker branches. Existing 71163/276806, 74323/277221 and 74324/277330 authenticated media receipts are reused, not resubmitted. Cross-repo PRs and CI validation follow; no new jobs.

Implementation and verification contracts merged: conductor#7862 at e472637135cb06dac9b18b46c533ec736cd8d370, kind_robots#5604 at ec7e0988651e60d42767ea0282f9556d67e5c87b. Tactics' stage lookup now consumes generated proof-backed private receipt records for last-order, sunken-street and unlicensed-rescue, and preserves all other existing maps. Both original PR heads completed every relevant CI check green. No new ArtJobs, no invented visual-curator approvals. Self-hosted rollout and final browser proof remain separate from this generator task.
<!-- note:end t-028 -->

## t-029 — Ship original tactical music and contextual combat SFX with accessible persistent mixer before human playtests

<!-- note:begin t-029 -->
Silas's explicit 2026-11-22 PT pre-playtest requirement. Dedicated audio was absent from the finite tactical roadmap and page implementation. Compose original title, planning, action, danger, victory/defeat and cinematic/ending themes without borrowed franchise material. Hook meaningful sound to selecting, moving, shooting, ability counters, hit, damage, defeat, rescue, objectives, turn change, villain-reveal and mission outcomes; keep gameplay deterministic and never play during headless tests. Offer separately persisted master/music/SFX levels, mute, browser gesture unlock, SSR/hidden-tab cleanup and accessible visual equivalents. Verify cue mapping and preferences with tests plus at least one real browser playback, mobile mute/resume and cross-route cleanup check. Before claiming completion confirm original score and audible assets/oscillators are actually usable in the live game.

Original seven-mood WebAudio score and 13 context-mapped tactical sound effects implemented on a scoped Kind Robots worker branch. The game now unlocks playback from real gestures, follows battle/scene/turn/impact state with pure deterministic cues, persists master/music/effects/mute controls, pauses on hidden tabs, and disposes the player on route exit. Dedicated Node regression and source integration checks are included in the Tactics test command. PR CI and real post-merge browser/mobile playback proof are pending, so t-029 remains in review rather than being marked delivered.

Merged original sound implementation Kind Robots #5608 as 91f146a048a1188fa253c4f2df1f1c58b492b214 after all ten required latest-head workflows completed successfully. Seven original synthesized score themes, 13 contextual cues, gesture unlock, persistent mixer and reduced-interruption route cleanup are on main. Final self-hosted deployment, actual playback, phone mute/resume and speaker audition remain unverified; t-029 is partial and must return ready, not done.

Scoped scheduler repair committed to Kind Robots worker/every-villain-tactics-t-029-audio-lifecycle-4e9d at 6425d131446ae4637b007719f2d52bea8b531478. Cancel active and queued voices on mood/mute/visibility/disable/disposal, stop scheduling inaudible channels, prevent suspended-context cue buildup, preserve independent mixer channels, and add deterministic active WebAudio stand-in regression. CI and actual browser playback pending; this does not close t-029.

2026-11-25 PT: verified merged Kind Robots PR #5770 at d93c234ea958963bd3a696a32bb389e8c0b283cc; all seven implementation workflows and their required jobs passed, branch janitor also succeeded and no t-029 branch remains. Audio lifecycle regression is merged; browser/mobile playback and audible audition remain open. Return partial task to ready rather than done.

2026-11-26 PT explicit Silas direction: "If we have audio made, then that’s good enough until human testing." Verified merged Kind Robots #5608 and #5770, including original seven-theme score, contextual cues, persistent accessible mixer and lifecycle regressions. All returned latest-head Actions workflows completed successfully, including game tests and branch janitor; repair head 7b568b7b19e122fb587388eed4de5d02ccbbd77b. Actual speaker/browser/mobile playback and subjective audition are deferred to human playtesting by explicit user direction, not claimed verified. Finite audio implementation accepted for roadmap closure; no publication or broader game acceptance implied.
<!-- note:end t-029 -->
