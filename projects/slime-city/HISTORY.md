# slime-city — task history archive

Full `note:` prose for completed slime-city tasks, moved out of `roadmap.yaml` so the
Kind Robots projection payload (`scripts/sync_kind_robots_projection.py`, hard limit
4,000,000 bytes) stays well clear of its ceiling. See conductor/t-158.

Each note below is the **verbatim** original — nothing is summarized or trimmed. The
`roadmap.yaml` task keeps its own first sentence plus a pointer here. The HTML comment
markers delimit each note exactly; `archive_done_task_notes.py --verify-only` re-extracts
every note and checks it byte-for-byte against what the roadmap recorded.

## t-001 — Build three playable square-grid prototypes, teams, city and special cards

<!-- note:begin t-001 -->
SILAS 2026-10-30 PT overrides earlier pentagonal rules. Create a discoverable ADMIN-only /admin/slime-city single-screen comparison console with 8x8 hidden-army BLACKOUT (Stratego-like), 12x6 turn-based lane MEATBALL and 14x6 real-time BLOODRUSH. Orthogonal square movement, simple adjacent simultaneous combat, mana, concealed units, card targeting and win paths. Six named teams including gene-catgirls, punk bloodfairies and cyber-ogres, seven illustrated/stylized districts, creature/spell/trap/ equipment examples. Implement testable pure TypeScript engine, Pinia lab state and timer; no reward persistence or public launch. Do not call CSS art generated artwork. Seeded tests, TS checks and phone/tablet/desktop visual QA required before marking ready for final subjective feedback. Shared external-facing release remains gated.

MERGED: Kind Robots PR #4478 (361faeecc3998e73ef44c22299623e05901540e5) implemented the private /admin/slime-city lab with Blackout 8x8, Meatball 12x6 and Bloodrush 14x6, six teams, thirty-six prototype cards, seven district selections, square-grid simulation, admin navigation and repeatable sample match controls. All 23 app checks passed, including TypeScript, Nuxt production build, four contract shards and the new Slime City deterministic contract. Conductor PR #6809 merged the superseding design, roadmap, CONTROL direction and square-grid art prompts after all 26 checks completed. This completes the implementation slice, NOT generated art, actual campaign/economy or public launch. The self-hosted site has no PR preview or automatic deploy; rendered 390/768/1440 screenshot acceptance is still outstanding and belongs to t-016, with additional actual art provenance in t-017. Neither is counted as delivered. No secrets, production economy or outward-facing publishing were touched.
<!-- note:end t-001 -->

## t-002 — Harden square movement, fog-of-war, action costs and three cadences

<!-- note:begin t-002 -->
Validate 8x8, 12x6 and 14x6 coordinate topology, only four orthogonal neighbors, occupied collision, hidden placement and fair reveal/attack, movement AP, per-round mana and card timing. Test simultaneous adjacent damage minus armor, double knockout, real-time pause/resume consistency, football scoring, AI spawn fairness and ghost/pile-up exploits, seeded command replays. Remove old pentagon/facing/twist logic everywhere in this game. Honest proof-of-concept limitations belong in the UI tutorial.
MERGED 2026-10-30: Kind Robots PR #4496 (f5269545), all 23 checks green. The CPU (utils/slimeCity/cpu.ts) decides only from the redacted observe() view and plays creature, spell, trap and equipment cards with its own mana. It respects AP and runs, escorts and hunts the flag in BLACKOUT, defends lanes, and banks for BLOODRUSH waves. BLACKOUT: 20-round limit with HP tiebreak; end-of-round flag pickup; carrier walks 1 AP; a fallen carrier drops the flag in place; back-column return; seeded armies and flag square; hidden fighters fight back; alternating initiative. Lanes: front-to-back flow plus sidesteps (no pile-ups); 3+ AP sprint; field cap 6; one armed trap; each card once per round; MEATBALL 30 rounds. BLOODRUSH: fixed 1 s ticks, banked mana, board beat every 2 ticks, 4-tick card rest, 150 ticks; pause/resume and between-tick plays tested through the real Pinia store with mock timers. Also: command record + replayMatch, 60-line log, per-match seeds with SAME SEED, hidden-info leak tests (CPU view byte-identical under hidden perturbation, no enemy secrets in the log), and per-format HOW TO PLAY panels with prototype limits. Pentagon/facing code is absent and the test asserts it. Tests: verifySlimeCityLab + verifySlimeCityStore.
<!-- note:end t-002 -->

## t-003 — Experiment with flag, monster and rout objectives across prototype boards

<!-- note:begin t-003 -->
After initial comparative playtests, create toggles or authored scenarios for flag capture/return, neutral beast kill, and fighter rout with reversible rules; assess whether they belong in hidden army games, advancing lanes, timed waves, or a deliberate hybrid. Test victory ties, early board emptiness, carrier rules, target counterplay, score pacing and accessibility. Do not lock this into all modes without evidence or a human design verdict.
DONE 2026-10-30: Kind Robots PR #4520 (3688a309) merged, all 21 checks green. Six reversible rule variants, all OFF by default and selectable in the /admin/slime-city lab (RULE VARIANTS toggles, aria-pressed, restart on the same seed): GIANT MONSTER (neutral centre beast for all three boards; blocks its square, swats the weakest neighbour, damage spells can target it; killing blow wins, ties by final-exchange then match damage), lane ROUT (26/18 KOs), LANE MOMENTUM (scoring drought makes upfield runners surge a square), SUDDEN DEATH extra time, YARDAGE TIEBREAK and a BLOODRUSH initiative swap. CPU hunts the monster in BLACKOUT and finishes it with spells. Replays with variants are tested (verifySlimeCityCrews). Measured effects (10 seeds, conductor PLAYTEST-COMPARISON 'After rebalance'): MEATBALL momentum+sudden death+tiebreak draws 44 -> 1.3%, seats 49/49; BLOODRUSH momentum draws 17 -> 3%, seats 50/46; monster ends 69% of BLACKOUT matches and halves length; rout widens lane crew spread to 9-84% (not recommended); rush swap and BLOODRUSH monster worsen the seat split (34/53, 25/64). Recommendations recorded; final rules stay with Silas in t-013.
<!-- note:end t-003 -->

## t-004 — Expand five mana colors into six distinct authored crews and special decks

<!-- note:begin t-004 -->
Six crews (Gene Riot Catgirls BLUE, Punk Bloodfairies PURPLE, Ironjaw Chrome Ogres GREEN, Riot Saints RED, Undertow Intelligence BLUE, Meat Exchange GOLD) retain independent character and campaign identities. Extend starter 3-creature/ 3-special POC roster into legitimate legal decks with creature, spell, trap and equipment types, intuitive game rules, named counters, collectible artwork provenance and tests. Five colors need not mean five teams. Inspect role coverage, swarm, control, armor, mana economy and RNG readability.
PARTIAL 2026-10-30, back to ready: Kind Robots PR #4520 (3688a309) merged, all 21 checks green. Six legal ten-card crew decks (60 authored cards; 4 creatures + 6 specials, one signature each, deckProblems() enforced) with distinct keywords and named counters: catgirls AMBUSH/REGEN (out of reach)/rearming Catnip Overdrive/Laser Pointer root; bloodfairies SWARM/LEECH/enemy-only Moshpit; Ironjaw armor/BULLDOZE; Riot Saints VOLATILE chains and friendly-fire Confetti Cannon; Undertow two armed traps/SNARE/PIERCE/Drain Sonar; Meat Exchange COLLECT mana debt (cap 2), Foreclosure, Hidden Fees, 6-mana Mogul. Per-crew BLACKOUT armies; CPU values every keyword and effect; hidden keywords redacted. Tests: new verifySlimeCityCrews contract plus lab/store/overworld. Balance (20 seeds, default rules, conductor PLAYTEST-COMPARISON 'After rebalance'): 15 of 18 crew-format cells inside 40-60% (was 7); Meat Exchange 72/75/82 -> 43/64/44; catgirls MEATBALL 24 -> 41.5; BLOODRUSH seats 40/52 -> 40/42. REMAINS: catgirls BLACKOUT 76%, Undertow BLACKOUT 32% (CPU barely uses traps in BLACKOUT), Meat Exchange MEATBALL 63.5%, strongly intransitive BLOODRUSH pairs (Ironjaw 99-1 vs Exchange, 7.5-92.5 vs Undertow); MEATBALL default draws rose 27 -> 44% (t-003 variants address it). Card art provenance stays t-017 (glyph stand-ins only).

Blackout-first overhaul linked to kind_robots issue #4535: open 10x6 arena, four seeded cards drawn from each ten-card crew deck per round, true played card consumption and discard cycling, full card inspection, manual attack commands with range highlights and summon delay, and CPU explicit attacks. Legacy concealed-army combat retained only for opt-in regression fixtures. Kind Robots implementation PR and CI pending; this is a partial t-004 slice, not 50-card-per-crew expansion or delivered Krea artwork.

PARTIAL Blackout-first increment shipped. Kind Robots PR #4537 merged at 15fd7e954e63ef442cba2c1e7a0ed84d6b2edf01 after 23/23 checks success (TypeScript, production image, mandatory Slime City contract, layout and Prettier). The open 10x6 arena starts empty and visible, faction decks of ten deal seeded four-card round hands, played cards leave the hand and cycle through the discard pile, and each side obeys identical card legality. Blackout uses explicit targeted attack commands with range and once-per-round summon-delay rules; enemy CPU chooses attacks from its observed view; action histories replay deterministically. Large card inspection and move/target highlighting are included. Old concealed-army setup remains opt-in test-only via classicFog. Conductor design directive PR #6868 merged, source master GitHub issue #4535 remains OPEN. REMAINS: authentic generated art integration and attack icons (ArtJob statuses in t-017), paced opponent action animation, Bloodrush cause-of-death UI, full art-first home screen, fifty extra cards per faction and final deck builder. No public deploy, production currency, or generated art completion claimed.

Reviewable partial progression/collection increment for user-directed Slime City design: browser-local XP/virtual Meat from CPU battles, daily/weekly Pacific challenge claims, ten paid-bout cap, one guaranteed rare and two unowned other cards per 100-Meat pack, immutable 60-card founder pool and gallery ownership badges. A six-faction counterplay matrix, 300-card next-set proposal and secure-ledger prerequisites are in Conductor PROGRESSION-AND-SETS.md. Not the t-008 server ledger nor production-safe t-010 persistent missions; no real money. Kind Robots implementation review and CI not yet finished.

Stale 2026-10-31 review reconciled after validating six distinct 10-card fully playable founder rosters, signature cards, ability/counterplay variety, 112 crew contract assertions and merged Blackout-first source PR #4537 (15fd7e9, 23/23 checks green). Original t-004 six-crew starter scope is complete. Additional Gutter Crown 300-card expansion and full deck editor remain t-006; CPU matchup/fog balance is t-005, server economy is t-008, illustrative card delivery is independent t-017. Closing stale review unlocks those worktracks; no art-ready or public release claim.
<!-- note:end t-004 -->

## t-007 — Expand seven-district city map into navigable authored overworld

<!-- note:begin t-007 -->
Replace prototype responsive stylized skyline with traceable generated painted panoramas, selectable streets/districts, NPC rival bouts, faction campaigns and deck/shop navigation. Distinct neighborhoods for engineered catgirls, punk bloodfairies, chrome ogres, spies, rioters, market and Pitworks; player choices should matter. Viewport screenshots at 390/768/1440/XL, no dead buttons or clipped accessible content. PARTIAL 2026-10-30, back to ready: Kind Robots PR #4499 (5247328c) merged with all 23 checks green. It shipped a session-only walkable overworld (utils/slimeCity/city.ts). Nine named streets join the seven districts and travel follows streets. There are 7 original named rivals, covering every crew and all three formats. Each district has one two-option street decision that moves standing and heat and changes that rival's bout terms (mana, armor, HP, one fewer sentinel, an armed trap, or the clock). Wins clear champions and raise standing; losses raise heat; heat 3 gives every rival +1 mana. Needle Alley and Crown Market are gated by citywide standing, and three champions open the Grand Pit. The UI has lit streets, pin status, a dossier below the map, WALK/FIGHT/QUICK MATCH, a city status bar and BACK TO THE CITY. Rendered at 390/768/1440 in Chromium with no overflow. Tests: verifySlimeCityOverworld (connectivity, gates, heat, terms on real matches, full store flow). REMAINS: painted generated district panoramas (needs real ArtJobs, t-017), deck/shop navigation, faction campaign chapters (t-009), and persistence (deliberately none yet).
Continue the Slime City city-overworld milestone from its existing partial state. Focus on substantive playable district progression and high-quality console interaction while other sessions own t-003/t-004 and t-017 art.
A focused follow-on overworld increment adds nine authored first-crossing street decisions with gameplay consequences, city panel presentation, session-only memory, and a deterministic contract expansion. Pending CI, preview verification, and review before this partial task returns ready.
PARTIAL 2026-10-30 PT: Kind Robots PR #4518 merged to main at dbf28b9794b275020a002d3a00e79b7caa429737 after 20 successful checks, including TypeScript, layout, formatting and mandatory Slime City prototype/store/overworld game contracts. Nine named streets now have first-crossing authored scenes with two distinct player decisions each, 18 total outcomes. [...]
[Earlier history (11,604 chars) archived verbatim to projects/slime-city/T007-HISTORY.md -- read it there only when you need a specific past cycle. Append new cycles below, one short paragraph each.]
PARTIAL 2026-10-31 PT: Kind Robots PR #4574 merged to main as 5f25e6176cfb26cc88a99ca2dd1e3b444140dbdc after ALL 15 latest-head GitHub Actions workflows succeeded, including TypeScript, changed-file formatting, layout and the four-shard contract suite. Seven distinct district championship aftermath stories now offer two exclusive choices each. Choice updates citywide standing and heat plus actual district follow-up bout terms; navigation, district contracts and local campaign shortcuts wait until the choice is resolved. Added deterministic city/store tests for one-time outcomes, invalid choices, travel blocking and follow-up battles. Admin-only source merge, not production deployment or new art. Further t-007 work remains: complete verified painted city art integration, deeper authored encounters, account-backed campaign saves and rendered visual QA. Keep umbrella kind_robots#4535 open; economy and art tasks remain separate.
Three authored citywide crises at champion totals two, four and six each demand a meaningful one-time decision before further city travel or battles. Choices alter standing, heat and persistent local-city combat terms, while direct STORY quick-start remains independent. New store/UI presentation and deterministic city/campaign contract coverage in Kind Robots branch worker/slime-city-t007-civic-crises-20261101-p7x4, pending PR CI.
PARTIAL 2026-10-31 PT: Kind Robots PR #4575 merged to main at 28e2ff2e23abc07174ec1d075119adddc568ebcd. All 15 latest-head GitHub Actions checks passed, including TypeScript, Prettier, layout, scroll ownership and four gameplay contract shards. Slime City now stages three citywide civic crises after 2/4/6 champion victories, with six authored exclusive outcomes that alter reputation, heat, and persistent opening battle modifiers for subsequent city rivals, contracts and city-launched faction missions. Players must resolve each crisis before walking or fighting; chapter quick-start from STORY remains an independent route. Seeded tests cover crisis thresholds, one-time effects, non-bypass travel, deterministic match setup and campaign integration. No server account currency, art generation, migrations or external publication. This is an admin-only source merge, NOT a verified self-hosted deployment. Remaining t-007 scope: validated painted city panoramas, richer cinematic presentation, account-backed city/campaign saves and cross-width rendered UI QA. Keep master kind_robots#4535 open; t-017 retains artwork provenance work.
Grand Pit ending branch and illustrated epilogue integrated into city UI, typed city state and Pinia store with story-priority gates, choice effects, replay navigation and deterministic tests. Source branch worker/slime-city-t007-grand-pit-finale-20261101-9d42. Pending PR review and full CI; partial t-007 only.
PARTIAL 2026-11-01: Kind Robots PR #4579 merged to main at baf2bff763bc00ac277b774799c1755ca5c84dba after all 15 latest-head workflows passed, including TypeScript, changed-file formatting, viewport/layout contracts and all four gameplay contract shards. Added an authored Grand Pit finale after champion victory/aftermath and pending city crises. The two mutually exclusive resolutions (neighborhood charter versus new Pit Boss) change standing, heat and persistent session-only battle modifiers. Authored epilogues reflect earlier solidarity choices. The illustrated internal-city screen displays the finale and supports continued exploration, revisiting the ending and explicitly starting a new city run. Regression contracts exercise gating, irreversible session choices, contract availability only after final choice, battle impact and store navigation. This is a source merge, not a verified self-hosted production deployment or actual new ArtJob/ArtImage delivery. Remaining t-007 scope includes real generated panoramas (t-017), account-backed overworld saves and post-deployment responsive visual verification; keep kind_robots master issue #4535 open.

Non-art city/campaign persistence increment: account-backed snapshots, admin-only GET/POST routes, cross-tab revision conflict protection, shared wallet preservation, pure schema validation, and contract tests. Implementation PR and full CI follow; no art wait, no deployment claimed.

Non-art overworld milestone delivered on main: Kind Robots PR #4596 merged as 59e3a83 after source, TypeScript, layout, and game-contract checks. Saved city routing, 9 street decisions, 7 districts, championship aftermaths, 3 crises, final city endings, and 6 faction campaigns now persist to the authenticated admin account with revision-CAS, strict validation, wallet preservation and sync recovery. Generated illustration receipts and placement remain separate art track t-017; cross-width post-deployment visual acceptance belongs to t-012/t-014. No public publishing or human approval implied.
<!-- note:end t-007 -->

## t-013 — Optional scope/course correction, final rules chosen after prototype comparison

<!-- note:begin t-013 -->
FOR SILAS: Play /admin/slime-city after the next self-hosted rollout and compare BLACKOUT (hidden turn-based army), MEATBALL (football lane turns), and BLOODRUSH (timed real-time). Tell us which cadence/board you prefer or request a hybrid. The Slime City name, colors and mana are still adjustable. This is an optional design conversation, not a blocker: continue building and testing while awaiting your verdict.

DECIDED by Silas 2026-11-02 PT (first-impressions playtest, verbatim excerpts): "Combat and movement on the blackout board should be automatic. … creatures can be set for attack, defense. I'm not sold on the flag part of the game, I think having a base that gets attacked makes more sense." Then: "base and capture the flag should be different elements. but we need clear notice of where the flags are, and there should be two, each on opposite ends inside their base. bases should be in far back row as well. same improvements made to bloodrush, who should be able to be feature parity with blackout. Since bloodrush should act like it but with timer released mana real time play." Final rules: BLACKOUT and BLOODRUSH share one auto-battle arena (cards + ATTACK/DEFEND stance orders; creatures march and fight on their own), each side has a base along its far-back column with its own flag planted inside; win by smashing the base or carrying the enemy flag home. BLOODRUSH is the same arena on a live clock with dripped mana. MEATBALL stays retired. Implemented in Kind Robots silasfelinus/kind_robots#4685.
<!-- note:end t-013 -->

## t-016 — Adversarially playtest and compare the three square-grid rule variants

<!-- note:begin t-016 -->
Produce multiple seeded and manual runs of BLACKOUT 8x8, MEATBALL 12x6 and BLOODRUSH 14x6. Measure first meaningful decision, clarity, tension, match duration, 6-team counterplay, clogged lanes, stalemates, comeback frequency, card usefulness, input reachability and real-time burden. Deliver a concise comparative report with desktop/phone screenshots and retain each playable variant. No agent unilateral final-mode decision.
DONE 2026-10-30: projects/slime-city/PLAYTEST-COMPARISON.md compares 1,800 seeded CPU- vs-CPU matches (600 per format; all 30 ordered crew pairings x 20 seeds) on the Kind Robots f5269545 engine. Reproduce with: npx tsx utils/scripts/slimeCityPlaytest.ts 20. Headlines. BLACKOUT: mean 12.4 rounds; 69% flag runs, 30% clock; first-initiative 53/46; 48% comebacks; 14% decided by round 4. MEATBALL: 27% draws and 44.5% reach round 30; most card play and lead changes; crews most polarised. BLOODRUSH: median 44 ticks; 82% breakthroughs; second side 52/40. Meat Exchange over-performs in all three (72/75/82%) and Catgirls sit at 24% in MEATBALL. Rule-sensitivity runs are included. Nine screenshots (projects/slime-city/playtest/*.webp) are Chromium renders of the real page component, store and engine at 390/768/1440 in a Vite harness. The deployed admin site was NOT captured: it needs the DB and admin auth. No mode was chosen; the verdict stays with Silas in t-013.
<!-- note:end t-016 -->

## t-018 — Build 60 playable neutral mercenaries with legal faction mixing

<!-- note:begin t-018 -->
Silas's 2026-11-01 PT revised 300-card roster: 40 cards per faction (240 including permanently free founders) plus 60 distinct neutral mercenary cards compatible with any of the six crews. Build neutrals as genuine executable CREATURE/SPELL/TRAP/EQUIPMENT cards with art slots, signed-in ownership, rare-guaranteed packs and one mandatory crew signature; initial deck cap is three mercenaries, reversible after adversarial testing. The adjacent Blackout rules revision is a three-mana per-turn grant with banking and a five-card hand that retains unplayed cards, voluntarily discards marked cards and refills to five; never immediately recycle played cards. Art delivery is not a blocker for tests, mechanics or text. Add exact deterministic replays, no-duplicate inventory, six-faction compatibility, rare exhaustion, constructed matches and explicit counterplay. Internal preview only; no production database resets or public publishing.

PARTIAL: 60 neutral mercenary cards authored in Kind Robots worker branch: 20 creatures, 18 spells, 12 traps and 10 equipment; 20 rare and 40 other. Deck and collection wiring, legal neutral cap, account ownership and replay smoke tests are in code review; art remains separate. The rules revision for banked mana/five-card cycling is a separate follow-on slice and must not be considered implemented here.

DONE: Kind Robots #4626 merged at 50bd1df after 9/9 latest-head workflows completed successfully, including TypeScript, all contract shards and the container build. 60 original mercenaries (20 creatures, 18 spells, 12 traps, 10 equipment; 20 rares), any-faction legal mixing with max three neutrals, account ownership and rare-safe 168-card catalog. Gutter Crown #4620 merged first at 8972da4; synthetic two-parent merge preserved its Ogre shove changes. Art is separately pending; 3-mana banking and five-card hand are tracked as t-019.
<!-- note:end t-018 -->

## t-019 — Implement Blackout banked 3-mana turns and strategic five-card cycling

<!-- note:begin t-019 -->
Silas 2026-11-01 PT: In primary Blackout each ten-card deck deals five cards initially. Unplayed cards stay in hand across rounds by default. The player can select any surviving hand cards to discard on END ROUND; refill to five, never drawing cards actually played on the immediately preceding turn even after a seeded reshuffle. The CPU receives the same cycle and must choose its discards by a deterministic visible-board policy. Start with three mana; each new round adds up to three mana, banking unspent mana up to ten. Mana debt reduces the new allowance, not the existing bank; any debt beyond one allowance rolls forward. Rebalance 4-6 mana cards against banking, update tutorial/hand labels, in-hand discard affordance, server-verified command replay, tests for exhaustion and invalid discard commands. Preserve legacy classicFog, Gridiron, BLOODRUSH and their tests. Internal preview only.

Implemented banked Blackout 3-mana turns, five-card retained hands, manual end-round discard selection, one-turn played-card exclusion, deterministic CPU cycling, secure replayed discard commands and regression tests on Kind Robots worker branch. Awaiting latest-head CI validation and QA before merge.

DONE: kind_robots PR #4630 merged at ae15dcc after all eight latest-head workflows passed including all four contract shards and TypeScript. Blackout now starts with three mana, banks up to ten, carries debt against future allowances, retains five cards with voluntary cycle toggles, excludes played cards from the immediately next draw and replays discard commands through server validation. Classic-fog, Gridiron and BLOODRUSH stay compatible. No self-hosted deployment claim.
<!-- note:end t-019 -->

## t-020 — Finish 132 faction cards at 40 per crew with diverse counterplay

<!-- note:begin t-020 -->
After the 60 founder cards, 12 reserve cards and 36 Gutter Crown wave-two faction cards, six factions each have 18 playable cards. Add exactly 22 distinct faction cards per crew, 132 total, yielding 40 per faction and 240 faction-specific total. The separate 60 mercenaries make a 300-card collection. Add 44 additional rares and 88 nonrares to retain exactly one rare and two others per pack, no duplicates or exhausted-bucket inventory bugs. Require at least three viable different ten-card archetypes per faction, flavorful unique mechanics or synergistic consequences, readable counters, legal faction ownership, verified seeded ability resolution and adverse balance tests. Ship in coherent playable waves, art queue separate and never a gameplay blocker. Do not count unmerged cards as done.

PARTIAL WAVE: 36 additional playable faction cards (six per crew), two rares per crew. The catalog rises from 168 to 204 cards, with exactly 24 faction cards per crew and 60 shared mercenaries. Wrote and wired all effects plus a mandatory six-crew integration/playability test. The remaining 96 cards (16 per faction) are still unfinished and this task MUST NOT be marked done until they are delivered. Awaiting CI.

WAVE THREE MERGED: Kind Robots PR #4633 merged at 41eb163b6cba0ece after all eight latest-head CI workflows passed, including TypeScript, 4/4 contract shards, formatter and container build. Added 36 executable faction cards (six per crew, twelve rares), bringing the pool to 204 (144 faction plus 60 mercenary; 68 rares, 136 nonrares). This is only 36 of this task's 132 new cards: 96 more are needed, exactly 16 per faction. The full t-020 milestone remains INCOMPLETE; return to ready for the next worker to claim. Art remains a separate queue; no user production deployment or human acceptance is claimed.

Complete remaining 96-card finale drafted on worker branch: exactly 16 per crew (6 creatures, 5 spells, 3 traps, 2 equipment). The full 300-card catalog and 100-rare pack economy are wired; test verifies every effect, three archetype decks per faction, account collection and 100 no-duplicate pack openings. Awaiting latest-head CI and merge. Artwork and human playtesting remain independent; no production deployment requested.

Kind Robots PR #4636 merged at acd792e with all latest-head workflows completed successfully. 300 original cards now in main: 40 per faction across six crews plus 60 mercenaries. Core deck legality, 100-pack exhaustion and individual playable effects passed contract tests. 192 new illustration requests are separately in conductor PR #6951. Artwork delivery and adversarial fun-testing are independent.
<!-- note:end t-020 -->

## t-021 — Adversarial constructed-deck matchup audit for all six 300-card crews

<!-- note:begin t-021 -->
Silas 2026-11-02 PT: Once private card art has been submitted, playtest the complete 300-card Blackout roster without waiting for renders. Construct at least three different legal ten-card decks per faction drawn from the actual account-collectible pool; use multiple seeded CPU playthroughs against several rival crews and both seating orders. Record first combat, dead turns, flag wins, knockouts, debt, roots, shoves, card deployment frequency, deterministic replay, and high-cost mana-banking viability. Detect overpowered loops, stalled/boring turns, useless expensive cards, and missing hard counters. Fix verified code, surface actual adversarial evidence and distinguish numeric balance from subjective human fun and rendered art QA.

Implemented 180 deterministic constructed-deck headless games: three legal ten-card archetypes for each crew versus all five rivals across two seeds. Captures win paths, first contact, dead rounds, banking, unit/card-use statistics, and validates 18 exact replays. Each round checks cards are neither duplicated nor lost. Awaiting latest-head GitHub CI before merge and concrete balance report.

PARTIAL MERGED 2026-11-02 PT: Kind Robots PR #4645 merged cc6fb3cbb18db2d2c2e61985a51ab0ca7c03bdff. Reconciled parallel campaign and constructed test harness changes with a true non-force merge commit, preserving both. 180 constructed matches across 18 decks, 60 distinct founder same-seed controls, 18 replay verifications, and mana/deck conservation coverage executed. Current engine: constructed 70 player wins and 110 enemy wins; founder controls 23 first-side and 37 second-side wins, 45 changed constructed-versus-founder outcomes, 109 of 180 games observed six banked mana. Distinct founder control matchups show larger faction disparity than deck-customization delta. All eight latest-head workflows passed. Further multi-seed seating symmetry and constructed-opponent comparisons remain.

Follow-up after merged PR #4645: added a ten-seed constructed-independent Blackout founder tournament for the six playable factions, exercising all thirty ordered rival pairs (300 actual CPU-versus-CPU bouts). Explicitly compares fifteen unordered matchups in both seating orders across all ten seeds, counts opening contact, stalls, faction win paths, first and second side wins, comebacks and round lengths, and replays six complete matches from command logs. Diagnostic warnings report significant skew without hardcoding balance targets or changing user card/wallet state. GitHub Actions full latest-head verification required before merge; multi-seed constructed-vs-constructed and subjective fun playtesting remain future scope.

PARTIAL MERGED 2026-11-02 PT: Kind Robots PR #4690 merged as 4feb990b8fb067276309007f8312dc597a5d1a4a. Ten-seed symmetric Blackout founder tournament ran 300 actual bouts, all fifteen rivalry pairings in both seating orders, and six exact command replays. All eight latest-head CI workflows passed. Results: Catgirls 95/100, Bloodfairies 20/100, Ironjaw 36/100, Riot 39/100, Undertow 46/100, Exchange 64/100. First-side 141, second-side 159, zero no-contact. Catgirls swept four crews 20-0 across both seats. Strong candidate cause identified in code: AMBUSH bypasses default summon sickness even though keyword documents first-blow bonus only. Follow-up needs paired A/B verification of a conservative counterplay fix and human subjective balance QA.

Narrow engine issue isolated after 300-bout mirrored faction audit: all Catgirls AMBUSH attackers were allowed to deal an immediate first-strike during summoning while other crews obeyed summon sickness, despite the published keyword promising only +2 on the first eligible blow. Changed Blackout/Bloodrush automatic arena clash to make all fresh fighters wait the same turn, retaining AMBUSH first-hit bonus after the wait. Added an explicit both-sides, two-round HP and keyword-replay regression in Slime City crew contract. The ten-seed 300-bout CI report will provide reproducible A/B evidence versus 95 Catgirl wins and 20 Bloodfairy wins from the old rules. No card ownership, game economy, schemas or outward-facing publish changes. This remains partial until CI is green and human fun QA later.

PARTIAL MERGED 2026-11-02 PT: Kind Robots PR #4692 merged ddc08c07e87277d699d82e2133fa7226d165ed4e. Root cause of runaway Catgirls faction advantage: AMBUSH bypassed automatic Blackout summon sickness despite only promising +2 on its first eligible blow. Fixed the exemption while retaining the first-strike bonus; added mirrored same-turn and next-turn regression. All six current-head GitHub Actions workflows and four contract shards passed. Repeated identical 300-bout ten-seed matchup matrix: Catgirls 95 to 65 wins, Bloodfairies 20 to 30, Ironjaw 36 to 38, Riot 39 to 44, Undertow 46 to 53, Exchange 64 to 70. Catgirls versus Bloodfairies shifted from 20-0 to 10-10; still 18-2 versus Ironjaw. Constructed-on-constructed mirror balance, Ironjaw matchup counters, and human fun approval remain open; no public launch or self-hosted deployment triggered.

PARTIAL MERGED 2026-11-05 PT: Kind Robots PR #4800 merged
ddcddce26d4e370d30d7e911e641ab6431414288 (11/11 latest-head checks). Re-measured on 60
held-out seeds: Exchange 71%, Catgirls 63%, Undertow 47%, Riot 43%, Ironjaw 41%,
Bloodfairies 34% (spread 0.142). Tuned with a scratch held-out tuner; four founder stat
changes: Broker armor 1->0, Chimera armor 2->1, Pogo HP 2->3, Welder armor 0->1. Two
independent 1,800-game held-out sets: spread 0.149 -> 0.048 / 0.058, every crew 44-58%.
verifySlimeCityFactionBalance now guards spread <= 0.11 and crews 35-70% (old stats fail
at 0.156). Full test:slime-city-lab passed. BLOODRUSH stays skewed (0.206 -> 0.191) and
is queued as slime-city/t-025. Remaining here: constructed-vs-constructed matchups
beyond founders and human fun QA.

DONE 2026-11-11 PT: kind_robots#5021 squash 1943261 (13/13 checks). New
verifySlimeCityClashConstructed (in test:slime-city-lab): five legal 20-card Solo decks
per crew (starter, fighters, specials, mercs, heavy), 870 CPU bouts covering every
cross-crew ordered pair (both seats) plus same-crew mirrors, six exact replays,
conservation. Results: first seat 51%, no draws or round-limit games; archetypes
fighters 0.62-0.64, starter 0.61, mercs 0.56, heavy 0.45-0.47, specials 0.22-0.25;
Exchange ~0.60 and Riot 0.41-0.44 across the constructed field. Finding for t-051: 17
two-slot cards (crew heavy spells/gear plus merc Grease Oracle) are never played. A/B
shows card weakness, not a CPU blind spot (forcing them 0.55 -> 0.19; repricing to one
slot still 0.43 -> 0.34). Guard pins the dead set to two-slot cards. Human fun QA is
Silas's to do; no deploy claimed.
<!-- note:end t-021 -->

## t-023 — TURF: a Go-style mode where every card is one token

<!-- note:begin t-023 -->
Silas 2026-11-03 PT, verbatim: "give me a new version of this game, modeled after go. each turn you play a single token, but go rules apply. this needs a modified effect...which theoretically already exists due to the different games."

DONE in Kind Robots silasfelinus/kind_robots#4696. TURF is a third player mode on a 9 x 9 board. Each turn a side places exactly one card from its hand on an empty point, or passes. Go rules: zero-liberty groups are captured, suicide is illegal unless it captures, a small superko forbids recreating any of the last eight positions, and two passes (or round 45) end on area score with 2.5 komi to the CPU. Every card is a token with a Go-native TURF effect (turfText): creature keywords become stone traits (VOLATILE explodes on capture, REGEN survives once, AMBUSH retakes ko, PIERCE/SNARE beat wards, BULLDOZE shoves, LEECH/COLLECT pay on captures, SWARM counts double); attack spells slime an enemy liberty with a puddle that can capture; heal, armor and equipment ward their group; traps capture a stone played on them; boost scrubs slime; scan disarms traps. The CPU is a beginner Go reader. Covered by verifySlimeCityTurf in test:slime-city-lab.

Open follow-ups: art/TURF-BOARD-ROUND-7.yaml queues TURF's own square board (until then it plays on each district's Blackout floor); human fun-testing; CPU strength (games usually run to the 45-round clock rather than ending on passes).
<!-- note:end t-023 -->

## t-024 — TURF CPU: make the Go-reader end games on passes instead of the 45-round clock

<!-- note:begin t-024 -->
Reviewer kaizen from PR #6986 (2026-11-03 PT). t-023's note says TURF games usually run to the round-45 clock rather than ending on two passes. Teach the CPU to pass when no placement improves area score (or when all its groups are alive), cover it in verifySlimeCityTurf in kind_robots test:slime-city-lab, and report the average game length over a seed sweep.

REVIEW 2026-11-04 PT: Kind Robots PR #4784. Root cause: all 108 sweep games hit the
45-round clock while the board was still contested (~37 captures/game); the CPU never
counted area the way the engine scores it. Fix: once 1/4 of the board holds stones and
30% of empty points are decided, the CPU counts exact area and plays only safe moves
that gain area, capture or rescue an atari group (no endgame invasions), otherwise
passes. TURF safety clock 45 -> 70 (an agent-set cap from t-023; natural games run ~57).
Sweep 108 games: before 0/108 ended on passes; after 104/108, avg 56.7 rounds, median
57. verifySlimeCityTurf covers settled-board pass, dame fill and whole games ending
before the clock; full test:slime-city-lab passed locally. Next: merge when CI green,
then done. Follow-up idea: ladder/atari-escape read to cut ~50 captures/game.

DONE 2026-11-04 PT: Kind Robots PR #4784 merged be8b7efe8d5a0b37817e0fb0d7fde48d6749c058
after all 11 latest-head checks passed (TypeScript, four contract shards, contract
verifiers, Prettier, layout, verify x2, GitGuardian). Review close-out conductor #7056
merged 98f11c1. TURF games now end on two passes in 104/108 sweep games (avg 56.7
rounds); safety clock 70.
<!-- note:end t-024 -->

## t-025 — BLOODRUSH crew balance: bring the six founder crews within the Blackout band

<!-- note:begin t-025 -->
Found during slime-city/t-021 (kind_robots#4800, 2026-11-05 PT). After the four founder stat changes that evened Blackout (held-out spread 0.149 -> 0.05), the secondary BLOODRUSH arcade mode stays skewed: on 30 held-out seeds its spread went 0.206 -> 0.191, with Catgirls 75%, Ironjaw 63%, Bloodfairies 56%, Undertow 52%, Exchange 28%, Riot 27%. BLOODRUSH cannot reuse Blackout card stats as its lever without undoing that pass, so look for a mode-level lever (for example per-crew BLOODRUSH tuning the way PARITY_CREW_EDGE does it, or a keyword that behaves differently on the timed lane). Measure on held-out seeds, then add a fixed-seed guard like verifySlimeCityFactionBalance. Internal preview only.

DONE 2026-11-05 PT: Kind Robots PR #4816 merged (11/11 latest-head checks).
BLOODRUSH_CREW_HP: dithered per-crew HP offsets in playedCard, BLOODRUSH (non-PARITY)
only, crew creatures only: Catgirls -0.25, Riot +0.25, Exchange +0.25 (founders: Chimera
5->4 HP, Kaboom and Bomber 4->5, Repo 2->3). Two 40-seed held-out sets: spread 0.191 ->
0.064 and 0.169 -> 0.068, crews 40-60%. verifySlimeCityFactionBalance guards BLOODRUSH
(spread <= 0.12, crews 30-70%). Full test:slime-city-lab passed.
<!-- note:end t-025 -->

## t-026 — TURF CPU: read simple ladders and atari escapes to cut capture churn

<!-- note:begin t-026 -->
Kaizen from slime-city/t-024 (kind_robots#4784, 2026-11-04 PT). The endgame pass logic now ends 104/108 sweep games on two passes, but games still average ~57 rounds because about 50 stones a game are captured: the one-move CPU loses groups it could save. Teach the TURF CPU a short read: extend or connect a group in atari when it can escape, and avoid playing into a working ladder. Report captures per game and average length over the same 108-game sweep before and after, keep the TURF crew-balance guard (verifySlimeCityTurfCrews) green, and keep every game ending on passes.

DONE 2026-11-05 PT: Kind Robots PR #4806 merged 1707445b05e0b3f45cd293fda8a063bac82e70e9
(11/11 latest-head checks). Audit: 163 of 183 lost stones sat in atari at the start of
the CPU's turn. Added an atari-escape bonus (3+ liberties: 2.2/stone +0.8; 2 liberties:
0.6/stone) and a one-step ladder read (turfChased: 1.6/stone cost). 108-game sweep:
captures 49.5 -> 37.0 a game, length 56.7 -> 50.6 rounds, two-pass endings 104 -> 108.
verifySlimeCityTurfCrews (normal and PARITY) and full test:slime-city-lab passed.
Follow-up idea: head-to-head new-vs-old CPU strength harness.
<!-- note:end t-026 -->

## t-027 — FIVE ALLEYS: a slow, turn-by-turn lane mode with Hearthstone-style chosen attacks

<!-- note:begin t-027 -->
Silas, 2026-11-05 PT, verbatim: "This game is still missing an actual fun play by play experience. The art is amazing, the style is great, the cards are interesting, but we still lack the GAME. Decks should be 20 cards, not 10. We need a new version that is slow position rules. (Solforge style, you have five rows and you can only attack or defend in the row you placed, without a modifier), and non-grid, you chose to attach someone or the opponent, hearthstone style."

Working assumptions (reversible; written down so Silas can correct them): a new mode alongside BLACKOUT/BLOODRUSH/TURF, not a replacement. Five lanes, one creature slot per side per lane, no grid movement. Alternating turns. Hearthstone mana crystals (1 on turn one, +1 a turn, cap 10), start with four cards, draw one a turn, each crew boss has 20 HP. A creature cannot attack the turn it lands unless a keyword says so. On your turn each ready creature attacks once, in its own lane only: if an enemy creature holds that lane it must fight it (both deal attack minus armor at once), and if the lane is empty it hits the enemy boss. Modifiers break the lane rule: ranged creatures (range 2+) can reach an adjacent lane, BULLDOZE tramples excess damage to the boss. Existing keywords keep their meaning where they can (AMBUSH +2 first blow, REGEN, LEECH heals your boss, SWARM +1 per ally in a neighbouring lane, VOLATILE bursts on the creature across, PIERCE ignores armor, SNARE stops the target's next attack, COLLECT gains mana on damage). Spells, traps and equipment reuse their effects aimed at a creature or a lane. 20-card crew decks: the ten founders plus ten more from the crew's own pool. Ship engine plus CPU plus a designed board (lanes, bosses, hand, attack arrows, a play-by-play log) in /admin/slime-city, with replayable seeded tests, a CPU round-robin, and screenshots at 390/768/1440. Internal preview only.

DONE 2026-11-05 PT: FIVE ALLEYS shipped as a new ALLEYS tab in /admin/slime-city. Kind
Robots PR #4818 merged 861e024 (13/13 checks incl. TypeScript and production image):
pure seeded engine utils/slimeCity/alleys.ts (five alleys, alternating turns, mana ramp
to 10, card a turn, 20 HP bosses, alley rule with range/BULLDOZE modifiers, keywords,
spells, traps, equipment, 20-card crew decks, exact replays), greedy step-by-step CPU
alleysCpu.ts, board components/slime-city-alleys.vue (bosses, lanes, hand, PLAY HERE and
target highlights, held card, play-by-play log, rival plays one step every 0.75 s),
verifySlimeCityAlleys in test:slime-city-lab. Checked by playing turns through the real
UI at 1440/768/390. Kind Robots PR #4819 merged 104b345 (11/11 checks): ALLEY_CREW_HP
dithered crew HP offsets and a one-time 2-mana coin for the second seat (the first
version's coin wrongly raised max mana); two 30-seed held-out sets: spread 0.238 ->
0.038 and 0.237 -> 0.032, first seat 49-50%, crews 45-57%; ten-seed guard in the test.
Open for Silas: every rule number (20 HP, ramp to 10, start hand 4, 30-turn cap, coin 2)
is a documented assumption to correct after playing; t-028 moves the rest of the game to
20-card decks.
<!-- note:end t-027 -->

## t-029 — Commit one shared balance tuner covering founders, PARITY and BLOODRUSH

<!-- note:begin t-029 -->
Kaizen from t-025 (kind_robots#4816). Tuning passes used scratch held-out scripts; commit one reusable tuner so t-028's 20-card re-measure reuses the same method. Internal preview only.

MERGED 2026-11-09 PT: kind_robots#4934 (1378be20, 13/13 checks) adds
utils/scripts/slimeCityFactionTuner.ts and npm run balance:slime-city-factions: held-out
Blackout + BLOODRUSH founder measurement (60 seeds from 1000, spread metric matches the
guards). PARITY lane not covered yet; t-028 can reuse it.

2026-11-11 PT: reconciled to done -- kind_robots#4934 merged 2026-11-09 (13/13 checks);
tuner shipped. PARITY-lane coverage, if wanted, is a new task.
<!-- note:end t-029 -->

## t-030 — CLASH: fun-first automatic five-lane prototype

<!-- note:begin t-030 -->
Silas, 2026-11-06 PT: Build Slime City's new core around automatic five-lane
combat, as a small fun-first playable prototype. Two static rows of five,
opponents alternate two card plays each, simultaneous automatic clashes,
banked mana, 20-card curated decks, replacement of occupied friendly slots,
readable damage forecasts and short CPU duels. Preserve all existing
BLACKOUT/BLOODRUSH/TURF/ALLEYS modes and economy; no public launch or live
rewards. Add deterministic replay and focused tactical tests. Human playtest
approval is a separate gate.

Playable standalone Clash engine, illustrated five-lane screen and focused deterministic rules tests committed on worker/slime-city-t-030-clash-20261106T1001-k4n8. Awaiting CI and merge; no account economy or public publication.

Kind Robots #4850 merged as c4bd12d0f35cdc9bb31a910df127dc7f221747b2 after 8/8 latest-head GitHub workflows completed successfully: formatting, TypeScript, four contract shards (including Clash replay/CPU), layout, architecture, schema parity, facet smoke and container image. New standalone automatic five-lane Clash practice mode with illustrated UI, seeded 20-card decks, simultaneous combat, two alternating card plays, creature replacement, equipment/traps, banked mana and CPU. Admin-only; no rewards or database mutation. Conductor direction PR #7105 also merged e136bab7fb9bb8a094b488480d9c3f81e1613bec. Human fun acceptance and live deployment remain unverified, separate gates.
<!-- note:end t-030 -->

## t-031 — Expose Clash in the normal Slime City Play interface

<!-- note:begin t-031 -->
Silas, 2026-11-06 PT: "huh, this should be accessible in the normal version,
not a special admin lin". Undo t-030's admin-only Clash restriction in the
shared game interface so players can access Clash via /play/slime-city.
Make the regular Play tab work for guests and signed-in non-admins, and
update the route/access regression test. The user explicitly authorized
normal-game access in this session. Do not change progression, rewards,
purchases, account data, marketing launch, or subjective-fun approval.

Removed mistaken admin-only checks from the shared game UI. Added a regression test requiring CLASH on the public normal Play route. Working branch worker/slime-city-t-031-normal-clash-play-20261106-v7q2. Explicitly requested normal game availability; no marketing launch or rewards.

Merged Kind Robots #4851 (f7f4eb858b20151e5ae48d9ec416d4385e4e0c6e) and Conductor #7106 (48bac78f37be355243b4aba56d4c9c97034ebf29); all latest-head checks green; normal Play route now shows ungated Clash tab.
<!-- note:end t-031 -->

## t-032 — CLASH canonical rules: two plays, tactical attacks, fresh draws, healing and exclusive balance

<!-- note:begin t-032 -->
Silas, 2026-11-06 PT: CLASH is now the MAIN Slime City combat mode;
ARENA, ALLEYS, BLACKOUT, BLOODRUSH, TURF and other modes become Legacy.
All development, gameplay playtests and card rebalance target CLASH
exclusively. A turn gives two card plays; marked powerful/special cards
cost both plays. Each round draw from a shuffled 20-card deck; discard
every unplayed hand card at end of turn, never hold them over. After
placement choose attacks: followers trade their power damage on attack,
any enemy follower is targetable, boss only when no enemies remain.
Heal every surviving follower for one at end of full round. Rebalance
Clash-specific stats and actions without changing legacy modes. Update
normal Play UI/navigation and deterministic CPU, replay, deck tests.
No account rewards, DB migration or unrelated publication changes.

Canonical CLASH engine in worker/slime-city-t-032-canonical-clash-20261106-9r4z: deterministic two-play placement, selectable follower trades/face locks, full-hand discard and redraw, follower healing, all-card Clash-only balance, smarter CPU, portrait hand and readable primary Play navigation. Tests cover all crews and seeded complete matches. Awaiting Kind Robots and Conductor CI.

Kind Robots PR #4852 merged as f5e164e1b27d909b9153c7a7288126592b4d4d8a. Eight latest-head CI workflows all completed successfully: Contract Tests, TypeScript, Prettier formatting, Layout Contract, Project Architecture, Schema Migration Parity, Facet Alias Smoke Test and Publish Production Container. Canonical two-play CLASH with manual power-for-power attacks, 20-card decks, fresh five-card draws and discards, end-round follower healing, all-roster Clash-only stat/action profiles and deterministic cross-crew CPU replays. Default Play route launches Clash; other formats are behind Legacy. Conductor direction PR #7108 merged as c8b4577e4b05e40e982ec146282932c9ff5dbf4e. No new art jobs, account rewards, database writes or production deployment. Self-hosted Force Update and human fun/art acceptance remain distinct steps.
<!-- note:end t-032 -->

## t-033 — Clash art-first presentation: board focus, compact hand, one collection, verified artwork/Comfy queue

<!-- note:begin t-033 -->
Silas, 2026-11-06 PT: On normal Play Slime City Clash, remove all redundant
scene titles, stage subtitle, round/turn header, duplicate rules button
and playmat-to-hand empty space. Make the playboard the primary full-width
art stage and scale the hand down to supplementary playable 2:3 cards.
Unify Cards and Rewards behind an art-first Collection destination and
replace the in-row Legacy expansion with a proper popover dropdown.
Apply SLIME CITY wordmark styling to the real workspace navigation title,
not a second duplicate title block. Diagnose missing card art (current
manifest maps only 73 of 300, and private image auth further filters),
prioritize existing and new Comfy art jobs at maximum priority, preserve
secure image access, and distinguish queued from delivered art. Keep
Clash canonical. No undocumented public art permission escalation.

UI fix under worker/slime-city-t-033-art-first-clash-20261106-s5q8: compact card rail, dominant illustrated board, no duplicate game wordmark, native Legacy dropdown, unified Collection and Bounties subnav, honest card coverage display and authorized art fallback. Art ledger worker/slime-city-t-033-comfy-art-20261106-s5q8 contains 70 missing default-deck card requests + one Clash mat followed by 157 remaining cards; max priority 1000, local Comfy engine, private until approved, distinct scene prompts with mechanical-jargon checks. Awaiting CI.

Kind Robots #4856 merged into main as cd1c8f7f60b46d401d92d3a08aebcedc17f0ed06 after eight of eight completed latest-head green CI checks: navigation, tablet navigation, TypeScript, formatting, architecture, schema parity, layout and all project contract tests. Clash now leads with a larger overhead-art board and compact hand; a single workspace SLIME CITY wordmark removes duplicate stage header; game help is not duplicated; compact action rail holds Rematch; Collection consolidates cards and legacy rewards; Legacy is a true dropdown. ArtImage fetch now tries already-public media without requiring login and provides authorized crew-art fallback for missing card art without widening any image permissions. Conductor art #7110 merged as 9b8eed736444045ba2d3301cca80389053c5817d, with 228 max-priority auto_submit Comfy requests (70 default-deck cards plus one board in first wave; 157 remaining cards in second). These are authored requests, not yet confirmed ArtJobs or delivered image bytes. Self-hosted Force Update and public-art permission review remain separate human gates.
<!-- note:end t-033 -->

## t-034 — Clash automatic animated alley strikes, readable card text and Clash-format balance run

<!-- note:begin t-034 -->
Silas, 2026-11-06 PT (iPad playtest of normal Play Clash): "The new clash
version of slime city is actually fun. Attacks should have animation and
happen lane to lane automatically after the second play. We can't see what
cards do! And the card balance needs a new run now that this is the format,
we built the cards originally after a turn based grid combat game, this is
different. It feels like characters are important, but we're moving in the
right direction."

Kind Robots PR #4883 (branch claude/keen-hopper-enpgbu): after the second
play (or FIGHT) each fighter strikes straight across its own alley, left to
right, one replayable strike command per alley; blockers trade, open alleys
hit the boss; fresh fighters brawl but reach the boss next turn; unblocked
strikes spring traps. Board animates lunge, shake and damage floaters per
alley. Hand cards show effect badges and a rules panel explains the held
card or tapped fighter with trait text. Clash budgets (power 2, armor 2,
priced traits, remainder life), traps +2, boss 20 with +5 second-seat coin.
CPU sweep 4500 held-out games: first seat 72% -> 51.3%, crews 34.5-66% ->
45.6-52.9%, avg rounds 3.6 -> 6.3. Not browser-verified in the agent
container (no DB); Silas's tablet playtest is the fun acceptance.

Silas, 2026-11-07 PT follow-up: "The cards shift the layout in and out
during turns and it's awkward ... a floating icon when closed, and a hand
of fanned out cards that grow large and show the text when selected. This
needs great and fluid animation. We can consider upping the hit points of
the main character, we want creatures to feel fun and beefy. Slime city
can get top priority for any art in the art queue. These missing cards are
distracting."

Same PR: SlimeCityClashHand floats over a fixed zone (no layout shift),
closes to a bobbing deck icon, deals cards out of it into an arc, grows a
selected card to full size with rules, supports drag-to-alley, and shows
tapped fighters as the same big card. Beefier balance: boss 28 (+8 second
seat), fighter budgets 14/25, armor/leech 3, round limit 18; sweep of 4500
held-out games: crews 46.9-56.5%, first seat 57.4%, 8.6 rounds. Verified
in a standalone Vite harness at 834px and 390px with Playwright.

Art: Slime City already held the queue maximum (1000; next highest 940),
but 188 of 228 round-6/7 cells were contract-rejected for doubled full
stops (and two for "only when" rules text), and every Auto Art run timed
out before committing job ids, so the same 40 cells were resubmitted as
duplicate ArtJobs (64607-64646, 64705-64744, 64779-64818). Fixed all 228
prompts (0 rejected by the Kind Robots contract) and added a ledger
checkpoint commit right after the sweep in auto-art-generate.yml.
Cancelling the duplicate PENDING jobs needs a Kind Robots admin token.

Kind Robots #4883 merged as ddb26fe7a261e49314800ae0d8b904998894b0bb after
13/13 latest-head checks passed (four contract shards, contract verifiers,
TypeScript, changed-file Prettier, layout, facet smoke, production image,
verify x2, GitGuardian). Merged is not deployed: the Unraid schedule picks
up the published image. Fun acceptance remains Silas's tablet playtest;
duplicate ArtJob cancellation remains a human token step.
<!-- note:end t-034 -->

## t-035 — Clash Solforge-style card leveling and 40-life bosses

<!-- note:begin t-035 -->
Silas, 2026-11-07 PT: "Hit points should be higher I'm thinking 40.
Something we should borrow from solforge: cards that evolve as you play
them. So something might be weak first round, but have a great round
three."

Kind Robots PR #4884: every card starts a match at level 1 and returns one
level stronger each time its crew plays it, up to 3 (per-level fighter
budgets 11/14/18 and 21/25/30, +1 power at L3, spells/traps +power per
level, bigger gear at L3; levels in match state so replay stays exact).
Boss 40 (+8 second seat), round limit 24. Cards show level pips and
next-level stats, L3 glows gold, fighters wear stars, plays pop a LEVEL UP
toast. Rebalanced (armor 2.5, leech 2, swarm 2, volatile 0); CPU sweep of
4500 held-out games: crews 45.4-55.4%, first seat 53.5%, 9.5 rounds, about
10.6 cards to L2 and 4.8 to L3 per crew per game.

Kind Robots #4884 merged as 793509c4bb7e13d4406f5b2abb7e9da3e066cd35 after
11/11 latest-head checks passed (four contract shards, contract
verifiers, TypeScript, changed-file Prettier, layout, verify x2,
GitGuardian). Merged is not deployed; Silas's tablet playtest remains the
fun acceptance.
<!-- note:end t-035 -->

## t-036 — Publish Slime City art

<!-- note:begin t-036 -->
Silas, 2026-11-07 PT: "The art should be public." This closes the
public-art permission gate left open by t-033.

Set isPublic=true on all 775 ArtImages referenced by kind_robots
utils/slimeCity/artManifest.ts (main after #4886) via the admin
PATCH /api/art/image/{id}; a re-read shows all 775 public, none mature,
and a logged-out fetch of an image file returns 200. Renders left out
of the manifest (curation redo verdicts and the 30 excluded in the
2026-11-07 art pass) stay private. Every Slime City art ledger now says
is_public: true, so curation redo 2 (31 cells at priority 1000) and any
future re-run renders public.
<!-- note:end t-036 -->

## t-037 — CLASH: 70 meaningful evolution designs and gameplay implementation for six crews plus mercenaries

<!-- note:begin t-037 -->
Silas, 2026-11-07 PT: research fun CCG card design, propose ten evolutionary redesigns per existing faction plus mercenaries (70 named existing cards), and implement actual version-specific gameplay with emphasis on weak-to-monster transformations, death growth, honest seeded inconsistency, nonattackers, adjacent synergy, multiple lanes and sacrificial effects. No new collectible card IDs and no faction-hate rules. CLASH only; legacy untouched. Design specification: projects/slime-city/CLASH-EVOLUTION-DESIGN.md. Require deterministic replay, readable card text, and adversarial six-crew balance before marking done.

Review checkpoint for the first live Clash evolution slice. Seventy named redesign concepts merged in Conductor #7153. Kind Robots implementation branch adds stage-specific rules for 15 existing cards across six factions and mercenaries: death marks, weak-to-apex, pacifists, aura support, adjacent token summons, seeded variance, sacrifice by replacement and healing. Contract fixtures and CI review next. Remaining planned redesigns stay open under t-037.

First implementation increment merged in kind_robots PR #4895 (squash 1207cca9de759e95c6ee616ee102b0e1e43b9e76) after all 11 latest-head checks passed. Fifteen existing cards across six factions and mercenaries have mechanically distinct level variants: weak-to-apex, pacifist healers and spies, adjacency anthems, deterministic randomized attacks, knockout memory, ally replacement as sacrifice, multi-lane tokens, and L3 snares. All 70 existing-card concepts are documented in merged conductor PR #7153 and projects/slime-city/CLASH-EVOLUTION-DESIGN.md. KEEP task ready for implementing the remaining 55 concepts, improving CPU tactical utilization, L3 reachability and fun-focused adversarial balance. No new collectible IDs, faction hate, economy, artwork changes or publication.

User-directed theatrical Clash presentation increment in review. Existing 15 evolving-card mechanics remain untouched. Proposed Kind Robots branch adds pure command-to-spectacle cues, stage-confined illustrated FX for entrance, L2, L3, traps, knockouts, hits, alliance powers and victory, pacing holds for milestone moments, and reduced-motion behavior. No external publication, catalog changes, background rendering or RNG outside seeded replay.

User-requested cinematic Clash presentation shipped: kind_robots PR #4899, squash 1c72ad2ec7a0caf2dc08a93c624fd607deada3ab, merged after all 11 final-head GitHub checks completed successfully. Command-derived, card-art-led Level 2/3 reveals, distinct summon/heal/explosion/trap/gear/lockdown bursts, impact/knockout/boss-finish and alliance-power VFX, keyed remounts, moment-aware pacing and reduced-motion support. Four scoped files, deterministic cue/replay tests. No game-rule, card roster, collection/economy, artwork rights or production deploy changes. KEEP t-037 ready for the remaining 55 card evolution designs and broader fun/balance/human visual testing; no subjective acceptance implied.

Review checkpoint: second wave of Clash-only stage-specific evolution mechanics, 24 existing catalog IDs across all six crews and three mercenaries, with deterministic recorded ability cut-ins; casualty, entry, spell, trap, attack and turn-start effects. Existing 15 designs preserved. Reconciled concurrently merged Clash-only / selectable decks / custom boss caps PR #4900 using a real two-parent git merge (no force push). Contract fixtures for each upgraded card, replay, and cinematic cues are committed to the implementation branch; final CI pending. Total 39 authored evolving cards implemented after this wave, leaving 31 of the original 70 concepts. No new cards, economy changes or production publication.

Merged kind_robots PR #4901 (squash 8440a642c4f4719c42b7fcb5ab2a96c1d2dfc755) after all 11 latest-head checks completed green: TypeScript, format, layout, schema, architecture, security and four contract shards including seeded replay/CPU balance. Added 24 existing cards with genuine, different L1/L2/L3 mechanics across all six crews and three mercenaries; 39 of the 70 authored evolutions are now implemented, 31 remain. New effects include real sacrifices, trap-safe one-lane echoes, true fallen-only once-per-entry revival, global healing/protection, surprise double strikes, seeded chaos, trap chains, death-growing allies and boss dividends. Named combat procs get replay-safe artwork cut-ins. Properly merged concurrent PR #4900 (Clash-only decks and variable boss caps), no force-push. Exactly four Clash files changed, no cards added, no economy or publication writes. KEEP t-037 ready to finish the 31 remaining authored cards and broader 300-card quality review; user visual/fun acceptance and self-hosted deployment are not verified.

Review checkpoint: expanding ultimate scope to 300 distinct bespoke card evolutions. New Conductor 300-ID ledger and follow-on umbrella task t-041 created on a worker branch; 20 more source-authored mechanical arcs and distinct battle fixtures across six factions and mercenaries are on the Kind Robots wave-three branch. Preserves old 39, targets 59/70 original concepts, 11 remaining. New rules for true fatal rescues, trap-copy non-inflation, seeded criticals, splash combos, telegraphed risky boosters, defensive wards, convoy repositioning and knockout-ledger revival. Final CI pending; no art/economy/deploy action.

2026-11-07 PT: User expanded the ultimate goal to individually crafted evolution arcs for all 300 existing Slime City cards, no new collectible IDs. Merged Kind Robots PR #4904 (squash 571115711b121b3860662544346bfaca72380535) with all 11 latest-head checks completed green, implementing 20 distinct new mechanical L1/L2/L3 arcs across the six factions and mercenary roster; 59 of original 70 are now playable with scripted battle fixtures, deterministic replay and six-crew CPU coverage. Merged Conductor PR #7158 (squash 34db3c72afa72bc3c91930334e6f1d98c8720408) for verified 300-row inventory and waiting follow-on t-041, and PR #7160 (squash d3a4768b8d322cce6dc0ae66891bcc128543fb37) for accurate 59 MERGED, 11 DESIGNED, 230 TODO statuses. Keep t-037 ready for 11 remaining original concepts; t-041 governs the other 230. No schema, economy, art queue, production deploy or outward publication. Subjective human fun and visuals not yet reviewed.

Final 11 curated evolution arcs implemented in Clash-only branch, with per-level text and focused fixtures; total authored arcs now 70. Awaiting Kind Robots PR CI, seeded balance and review. Follow-on t-041 remains pending.

Finished 70/70 originally requested handcrafted Clash evolutions. Kind Robots PR #4905 merged as 0e3cc3149644fe457333eae560a1c7a681c1adc4 after 11/11 final-head green checks; Conductor inventory PR #7163 merged as 6a4267b89b1b65ffd8bb2c85b99f4d4df76b830e (70 MERGED, 230 TODO). Includes deterministic battle fixtures, no new card IDs, no economy/art/legacy rules changes. Future 230 cards belong to t-041; human fun acceptance and deployment not claimed.
<!-- note:end t-037 -->

## t-038 — CLASH ALLIANCE: two-faction 30-card decks with one-time general faction powers

<!-- note:begin t-038 -->
Silas, 2026-11-07 PT: "I want a new mode where the factions can be combined. 30 card decks. Needs to be supported in clash and in deck builder modes. Also want the idea of a faction power. So if you have two factions, one is the general and the deck uses their power. Power should be one time use during a match." Clarified: "Factions combined means you pick two factions, one of them is general, and you can make a 30 card deck using either faction or mercs."

Shipped in kind_robots PR #4897 (squash 0829df42d7e20a289024f76ee127d4e1450a2071) after all 13 latest-head checks passed. utils/slimeCity/alliance.ts: two different factions, any 30 unique cards from either or mercenaries (only guard: 12+ creatures), starters for every pairing, swap-general. Six one-time faction powers (Nine Lives, Mosh Pit, Union Wall, Fuse Box, Sewer Snipe, Call in the Debt) as a replayable Clash `power` command that costs no card play; CPU timing from public facts. Collection CLASSIC 10 / ALLIANCE 30 builder with second-faction picker, swap button, server-validated story save; Clash STANDARD / ALLIANCE switch, power button and rival power chip. CPU sweep 1,800 games: every general 46-54%, first seat 48-51%. Not visually verified pre-merge (local dev needs a DB); look at Collection > ALLIANCE 30 and Clash > ALLIANCE on main. Fun of the power numbers is Silas's call.
<!-- note:end t-038 -->

## t-039 — Everything is Clash: Solo and Alliance decks, City/Story bouts as Solo Clash, verified CPU reward matches, legacy modes retired

<!-- note:begin t-039 -->
Silas, 2026-11-08 PT: "drop the 12 creature minimum. solo should not have been gone, it should have been an independent mode with the solo gamemode. speaking of though, when i select city, it launches the old game system. we don't need the legacy modes, period, everything should be clash, either in city mode which is Solo Clash, or the deckbuilder mode when a user can make a solo or alliance clash deck and play against cpu or human opponents, earning rewards and opening packs." Then: "deck display still doesn't have support for evolutions."

Kind Robots PR #4900 (branch claude/pensive-albattani-ibljzj): SOLO CLASH format (one faction 20 cards + mercs, any mix, story.soloDecks); Alliance drops the creature minimum; armory SOLO 20 / ALLIANCE 30 (classic 10 retired); City rival/contract and Story bouts launch Solo Clash with terms moved onto boss life (20-60) and settle the ledgers once; CLASH tab SOLO/ALLIANCE vs CPU as server-issued reward matches (deck kept with the match, TRICKLE ownership, transcript replay with CPU moves checked against the server CPU, usual XP/Meat, "Win a Clash battle" bounty); LEGACY menu, Arena, Five Alleys, arena hand and legacy card face deleted; Collection and pack cards show the Clash face with an EVOLUTION LV 1/2/3 switch; fixes #4897's server story save dropping alliances. Not built: human opponents (t-011). Legacy engine code (BLACKOUT/BLOODRUSH/TURF/FIVE ALLEYS in utils/slimeCity) remains unreachable and is a cleanup follow-up.

2026-11-08 PT: merged as kind_robots PR #4900 (squash 5379f9f2703494ab51f09c8f1c82229875bf0892) after all 16 latest-head checks passed; includes the Collection/pack Clash card faces with the EVOLUTION LV 1/2/3 switch and deletion of the arena, alleys, arena-hand and legacy card-face components (component-reachability guard). Visual check on main still owed (local dev needs a DB).
<!-- note:end t-039 -->

## t-040 — Wire the ogre redo-2 board tokens (no more Shrek look) into the Clash board

<!-- note:begin t-040 -->
Silas, 2026-11-08 PT: "we've still got a lot of orcs that look like shrek in their character token in game." projects/slime-city/art/BOARD-TOKENS-OGRE-REDO-2.yaml queues 45 Krea re-renders (auto_submit): 14 Ironjaw ogre creatures and the Picket Line Troll mercenary x fierce/guard/hurt, each with a distinct non-green skin, angular industrial face, riveted chrome lower jaw and small bolted ears. Once the sweep writes art_image_ids back, curate them (reject any that still read as a green round-faced movie ogre and re-queue with a stronger look) and replace the matching SLIME_CITY_ART.tokens['<cardId>/<mood>'] ids in kind_robots utils/slimeCity/artManifest.ts. Foundry Lion keeps its token.

2026-11-09 PT: curated all 45 redo-2 renders (ArtImage 265992-266036) on a contact
sheet. Kept 36 non-green angular chrome-jawed faces and wired them in kind_robots PR
#4926: 25 replace Shrek-era token ids, 11 fill missing moods (SLIME_CITY_ART_COUNT
775->786); verifySlimeCityOverworld PASS. Rejected 9: Picket Line Troll (still
green/mossy/round), Coal Cart Racer (grey-green round), Union Lunch Lady (painted as a
human woman). They re-render in projects/slime-city/art/BOARD-TOKENS-OGRE-REDO-3.yaml
(auto_submit); wiring those is slime-city/t-042. Done after #4926 merges.

DONE 2026-11-09 PT: kind_robots#4926 squash-merged
dbd5d70151ce9cacd7d2114c57ba3bdaedd082d5 after all 11 checks passed (TypeScript, 4
contract shards + verifiers, layout-contract, Prettier, verify x2, GitGuardian). Live on
kindrobots.org after the next Unraid Force Update. Redo-3 for the 9 rejected tokens is
t-042.
<!-- note:end t-040 -->

## t-043 — Lizard people replace the ogres: reskin the Ironjaw crew's names, flavor and rules text

<!-- note:begin t-043 -->
Silas, 2026-11-09 PT: "we should have lizard people instead of orcs." Rewrite the Ironjaw Chrome Ogres as cold-blooded chrome-jawed lizard people in kind_robots utils/slimeCity (crew name, hook, pattern, counters, card names and text, campaign/story copy, CPU and UI strings), plus ogre/troll-looking mercenaries such as the Picket Line Troll. Keep the crew id `ironjaw`, every card id, stats and mechanics, so saves, decks and balance are unchanged. Tests guard that no player-visible ogre/orc/troll wording remains for the crew.

DONE 2026-11-09 PT: kind_robots#4928 squash-merged
f0ec7ccd81343a20791a4ad6dc866073ba4ffdea after all 11 checks passed (TypeScript, 4
contract shards + verifiers, layout-contract, Prettier, verify x2, GitGuardian); full
test:slime-city-lab passed locally. IRONJAW CHROME OGRES -> IRONJAW CHROME LIZARDS;
Bulld-Ogre -> Bulldozard, Bridgebreaker Ogre -> Bridgebreaker Monitor, Picket Line Troll
-> Picket Line Komodo; all story/city/campaign copy rewritten; ids, stats and balance
unchanged; a verifySlimeCityLab guard blocks ogre/orc/troll wording. Art still shows
ogres until t-044.
<!-- note:end t-043 -->

## t-045 — The Punk Bloodfairies become Slime City's band crew

<!-- note:begin t-045 -->
Silas, 2026-11-09 PT: "There needs to be a band centered group"; he chose the Punk Bloodfairies over a 7th crew or a mercenary band. Rework them into a touring punk band (frontwoman boss, rhythm section, roadies, merch, setlist and encore play) through names, flavor, story and the existing choir/encore/mosh mechanics, keeping card ids, the 40-card count and balance. Queue band-styled art in t-044's pattern once names settle.

2026-11-09 PT: kind_robots#4929 makes the Punk Bloodfairies QUEEN PIN & THE
BLOODFAIRIES, Needle Alley's loudest punk band plus its fans, roadies and backup singers
('Small wings. Big amps.'). Founders play parts: Queen Safety Pin frontwoman, Razorwing
lead guitar, Bloodsprite backup screamer, Pogo Brat stage diver; campaign/tower/crew
copy follow; ids, stats and balance unchanged; verifySlimeCityLab pins name and roles.
projects/slime-city/art/BLOODFAIRY-BAND-ROUND-1.yaml queues a new band-on-stage crew
poster (auto_submit) to replace crews.bloodfairies once curated. Done after #4929
merges.

DONE 2026-11-09 PT: kind_robots#4929 squash-merged after all 11 checks passed
(TypeScript, 4 contract shards + verifiers, layout-contract, Prettier, verify x2,
GitGuardian); full test:slime-city-lab passed locally. Band crew poster queued in
BLOODFAIRY-BAND-ROUND-1.yaml; wire crews.bloodfairies when curated (t-044's curation
pass can take it).
<!-- note:end t-045 -->

## t-046 — Lean into the meat world: make the meat economy and city weirdness central

<!-- note:begin t-046 -->
Silas, 2026-11-09 PT: "we need to lean into the world. We exchange meat, for chrissakes." Pass over Slime City's player-visible copy (title screen, HUD, rewards, shop, collection, story and card flavor) so meat as currency and the megacity's absurdity are front and center. Copy and presentation only; no economy, wallet or DB change.

2026-11-09 PT: kind_robots#4930 makes Meat the city's money out loud. Quests: Punch the
Meat Clock, Fresh Cut, Stock the Freezer, Prime Cut Champion, Mixed Grill, Butcher-Paper
Riot (same metrics/payouts). Rewards: 'your cut: +45 Meat', butcher-paper packs, 'In
Slime City, Meat is money.' The Meat Exchange are butchers-turned-bankers who mint the
city's Meat (hook, Mogul, Collector, Repo, Collection, Foreclosure, Hush Money, Crown
Market). Copy only; wallet, payouts, rules and ids unchanged; verifySlimeCityProgression
pins it. Avoided every file the open #4924 touches. Further meat passes (title
screen/HUD/shop copy) should follow once #4924 lands.

DONE 2026-11-09 PT: kind_robots#4930 squash-merged after all 11 checks passed
(TypeScript, 4 contract shards + verifiers, layout-contract, Prettier, verify x2,
GitGuardian); full test:slime-city-lab passed locally. Live after the next Unraid Force
Update.
<!-- note:end t-046 -->

## t-047 — CLASH crew balance: lift the Ironjaw lizards, trim Riot volatile spikes

<!-- note:begin t-047 -->
Related: t-041 (the 300-card evolution QA umbrella); this is a focused balance slice of it
and does not wait on it.

2026-11-09 PT, from the Slime City hourly playtest run (1:00 PM PT, read-only, could not
push) and re-run on kind_robots main 1378be2 this session: `npx tsx
utils/scripts/slimeCityClashBalanceReport.ts 40 9000` (1,200 CPU-vs-CPU CLASH games,
deterministic) gives Riot 64.0%, Bloodfairies 60.5%, Undertow 49.3%, Catgirls 47.8%,
Exchange 43.5%, Ironjaw 35.0% (29-point spread; first seat 53.2%, 0% draws, 8.5 avg
rounds; L3 is reachable, 4.3 cards per crew per game). Ten of the bottom twelve cards are
Ironjaw: Hydraulic Slap 28%, Forge Lightning 31%, Shock Plate 32%, Night Shift Welder and
Foundry Plating 34%, Bulldozard, Coal Cart Racer and Chrome Scrapper 35%, Spark Welder and
Spare Pistons 36%. The top is Riot volatile: Grand Detonator 80%, Thermite Archangel 72%,
Detonation Deacon 67%, Matchstick Mime 65%; Bloodfairy swarm+leech (Queen Safety Pin 74%,
Blood Moon Headliner 72%) is next.

Scope: bring every crew into roughly 42-58% in CLASH without generic stat inflation.
Prefer giving Ironjaw's armor/zap/snare cards a real decision or payoff (per
PLAYABLE-EVOLUTION-CONTRACT.md) over raw HP/attack bumps, and trim Riot volatile's
ceiling with counterplay rather than flat nerfs. Check whether the lizard reskin (t-044,
kind_robots#4928) changed anything mechanical first. Keep all 300 card ids. Verify with a
held-out seed set (not the tuning seeds), the existing test:slime-city-lab suite, and add
a CLASH spread guard alongside verifySlimeCityFactionBalance once the spread is fixed.
No art, economy, wallet or release change.

REVIEW 2026-11-09 PT: kind_robots#4936. Root cause: CLASH armor cost 2.5 budget, which
life rounding made 2 life per point, while one point of block is worth ~1 life in fixed
alleys. Re-priced armor to 1.5 (CLASH_ARMOR_COST, one life per point), priced a 2-damage
volatile burst at one budget point (CLASH_BURST_COST; Grand Detonator 80->66%), and
clamped crafted L3 life bonuses to the tier cap. Held-out 3,000-game sweeps: seeds
120000 spread 7.3 points (crews 45.8-53.1%), seeds 200000 spread 6.2 (47.5-53.7%);
before: ~30. Snare-fizzle and armor-scaled Ironjaw zaps measured as no-ops and were
dropped; flat Ironjaw +1 overshot to ~60%. verifySlimeCityClash now guards each crew at
42-58% and spread <=12 points. test:slime-city-lab and vue-tsc green locally. Next:
merge when CI is green, then done. Possible follow-up: 1-play snare traps now fill the
bottom of the card table (Moshpit Tripcord 29%, Bloodwire 35%).

DONE 2026-11-09 PT: kind_robots#4936 squash-merged as c719ac339b9d after all 10 checks
passed (TypeScript, 4 contract shards, layout-contract, Prettier, verify x2,
GitGuardian). Live on main after the next Unraid Force Update. Follow-up: slime-
city/t-048 (weak 1-play snare traps).
<!-- note:end t-047 -->

## t-048 — CLASH card tuning: give the weak 1-play snare traps a real payoff

<!-- note:begin t-048 -->
Follow-up from t-047 (kind_robots#4936, 2026-11-09 PT). After armor was re-priced to one
life per point, crews sit at 45-54% in CLASH, but the bottom of the per-card table is now
mostly 1-play snare traps that armor blunts: Moshpit Tripcord 29%, Bloodwire 35%, Leech
Grate 38%, Escrow Snare 40%, Culvert Tollwire 40%, Floodgate Clamp 43% (win rate when
played, `npx tsx utils/scripts/slimeCityClashBalanceReport.ts 40 9000`). Give them a real
decision or payoff per PLAYABLE-EVOLUTION-CONTRACT.md (e.g. what springing on an armored
or volatile fighter does) rather than flat power bumps. Keep the t-047 crew guard in
verifySlimeCityClash green (each crew 42-58%, spread <= 12 points) and confirm on a
held-out seed set. Keep all card ids. No art, economy, wallet or release change.

Added focused deterministic CLASH regression for one-play Bloodwire detonation on armored Ironjaw Scrapper: real card entry, permanent plating removal, damage, consumed trap and replay identity. PR pending complete CI; broader six-trap balance and held-out sweeps remain.

2026-11-09 PT: merged Bloodwire-vs-armored-Scrapper deterministic snare regression in kind_robots PR #4943 at 47ad75314c97ee85fa39b1cb201d7d07e6bad85e. All six GitHub Actions workflows completed successfully on head c3d55ba. This is a partial t-048 increment: six-snare tactical payoff tuning and held-out balance sweeps remain. Return task to ready for the next worker.

Opened kind_robots PR #4950 at 136c10b for six cheap snare armor-counter deterministic fixtures; awaiting latest-head CI. Broader six-card tuning and held-out balance sweep remain.

2026-11-10 PT (branch-medic, 2026-11-11 00:58Z): kind_robots PR #4950 (six-snare armored
fixtures, head feb9a0a1) was closed unmerged by the prune job at 09:22Z after its
TypeScript check failed; all other checks passed. Expired claim released. Next worker:
reuse branch worker/slime-city-t048-six-snare-20261110-7c92 and fix the TypeScript error
before reopening, or drop it if the t-051 fighters-first redesign retires these snares.

2026-11-11 PT (branch-medic): stranded branch worker/slime-city-t048-six-
snare-20261110-7c92 verified superseded — its six-snare armored fixture already landed
on kind_robots main via #4954 (923a6a2) with the same mercenary type guard. Branch
cleared via branch-janitor force_delete. Do not reuse it; remaining t-048 scope is six-
snare payoff tuning plus held-out balance sweeps.

DONE 2026-11-11 PT: kind_robots #5018 squash-merged at 3031d09, all 11 checks green.
One-play snares now defuse as well as cut armor: a VOLATILE fighter caught by one loses
its death burst (log line, card text 'Cuts armor, defuses VOLATILE.', also on twist-text
snares). CPU scores snare payoffs (+1.5 armored, +1.5 volatile, 0.4x foe power for
rooting). Held-out 3,600 games (seeds 31000+): crews 45.1-54.6%, spread 9.5 (guard
<=12), unchanged vs main; snares played more (Scent Mine 54->189, Bloodwire 82->110),
Bloodwire win-when-played 33->38%. The six named snares had left the default starters
under t-051, so the payoff mostly reaches constructed decks. Deterministic defuse, two-
play contrast and CPU-target tests added to verifySlimeCityClash.
<!-- note:end t-048 -->

## t-049 — Title screen and CLASH versus console: generated splash art, big fighter stats, boss reactions, battle log, hover cards

<!-- note:begin t-049 -->
Silas, 2026-11-10 PT, after hands-on play (screenshots in session): "that front end splash
image needs to be a generated image, not svg. also, we should not be scrolling that display,
single page design, always ... the city story and the faction mode distinction is not clear.
... the attack and heart values need to be at the top, not bottom of the token, and much
bigger, with stylish display. we should be able to see a log of an active game ... assign
some more space for the matchup pictures, so there are reactions ... When we hover over cards,
we should see them bigger and have the full info of the card ... The floating hand icon is
blocking another button, that lower section should be combined with the versus image, hp
counters, play counters, and floating hand button to one interface and versus section."

Scope (kind_robots): title screen paints generated art (title key art once rendered, the
chosen crew's home district until then), fits one screen with no scroll, big crew poster,
art-led QUICK BATTLE / CAMPAIGN / CITY MAP cards with one-line explanations; "STORY" renamed
CAMPAIGN in tabs and city. CLASH: one versus console (rail on wide screens, top/bottom strips
on narrow) holding both boss portraits with mood reactions and quips, life, play pips, the
general power, the hand button (no longer floating over FIGHT), FIGHT/REMATCH and a battle
log; fighter attack and life as large badges at the top of each token; mouse hover shows the
full card docked beside the board. Faction one-shot powers already exist but only in
ALLIANCE format (Silas's 2026-11-07 spec: the general's power) — whether SOLO should get them
too is Silas's call. Art: projects/slime-city/art/TITLE-AND-BOSS-REACTIONS-ROUND-1.yaml
(1 title key art + 24 boss mood portraits, auto_submit); wiring keepers into
SLIME_CITY_ART.ui / .bosses is a follow-up after curation. No rules, economy or release change.

DONE 2026-11-10 PT: kind_robots#4939 squash-merged as 9be0cdf424e3 after all 11 checks
passed (TypeScript, 4 contract shards + verifiers, layout-contract, Prettier, verify x2,
GitGuardian). Art ledger merged in conductor#7208 (cd7602bf). Live on main after the
next Unraid deploy. Follow-ups: curate and wire the title key art into
SLIME_CITY_ART.ui['title-splash'] and the 24 boss mood portraits into
SLIME_CITY_ART.bosses once rendered; Silas to decide whether SOLO Clash gets the one-
shot faction powers.
<!-- note:end t-049 -->

## t-050 — Alliance deck library on COLLECTION; SOLO story deckbuilding from encountered cards

<!-- note:begin t-050 -->
Silas, 2026-11-10 PT: "we should have a deck focused build for the collection page. the user adds,
copies, deletes, edits decks, new ones are solo or alliance, no other building rules, can be loading
into the various game modes as appropriate" and then "this solo alliance divide really shouldn't be
there ... the collection deckbuilder ... should be treated as alliance default. the single faction
story should allow deckbuilding based on encountered cards, but should not be treated like the
default experience. a LOT of the pictured stuff can be trimmed away or essentialized."

Scope (kind_robots): COLLECTION becomes a named Alliance deck library (add, copy, rename, delete,
edit; 20 cards from two crews + mercenaries; the only rules are the format's crews, size and no
repeats) stored in the story save, with legacy per-crew decks migrated in. Loading a deck makes it
the deck PRACTICE, CAMPAIGN and TOWER deal. Solo deck editing moves into the SOLO story and draws
only on that crew's base cards plus the cards the story has awarded. Trim the collection header
to essentials: drop the crew dossier, art-mapping counters and the SOLO/ALLIANCE format switch;
keep the card grid as the one scroll region. Default Clash format becomes Alliance.

2026-11-10 PT: shipped in silasfelinus/kind_robots#4955. COLLECTION opens on a named
Alliance deck library (new/copy/rename/two-tap delete, up to 12, unfinished decks
saved); picking one makes it the deck Practice, Campaign and Tower deal. The
SOLO/ALLIANCE switch is gone; SOLO story's CREW DECK opens its single-crew deck. Story
bouts already fold story-earned cards into the crew deck (campaignSoloDeck); a deck pool
limited to only cards encountered in the story is not built — open a follow-up if Silas
wants that stricter rule. Follow-on: silasfelinus/kind_robots#4956 makes
story/campaign/tower fights pay rewards.
<!-- note:end t-050 -->
