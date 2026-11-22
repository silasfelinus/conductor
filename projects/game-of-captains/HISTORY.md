# game-of-captains — task history archive

Full `note:` prose for completed game-of-captains tasks, moved out of `roadmap.yaml` so the
Kind Robots projection payload (`scripts/sync_kind_robots_projection.py`, hard limit
4,000,000 bytes) stays well clear of its ceiling. See conductor/t-158.

Each note below is the **verbatim** original — nothing is summarized or trimmed. The
`roadmap.yaml` task keeps its own first sentence plus a pointer here. The HTML comment
markers delimit each note exactly; `archive_done_task_notes.py --verify-only` re-extracts
every note and checks it byte-for-byte against what the roadmap recorded.

## t-001 — Build polished private bridge console and complete playable first voyage

<!-- note:begin t-001 -->
Initial PR delivers original title art, six-style captain choice, crew selection, star-chart mission, 0-3 away assignments, ethical consequence, one seeded antagonist complication, debrief and saves with tests. No generic website. Matching conductorSlug Kind Robots Project record.

Implemented captain/crew selector, three-mission star-map voyage, away team staffing, persistent randomized antagonist, differentiated intervention dilemmas, multiple short-voyage finales and Pinia save/resume on Play. Original vector bridge art, Play tab and project placement, and both home highlight cards included. Pending implementation PR and CI; painted ArtJobs and full 3-act content remain separate tasks.

Merged the fully checked first Play voyage in kind_robots PR #4185, commit 29af913e95dad4719137c4bfbc6292ba76e74fb8: select captain and crew, run three missions, assign away-team, interact with random antagonist, debrief, save/resume and follow two dashboard featured links. All 24 checks completed successfully. This is a short playable slice with concept vector art, not the complete 3-act game. Next ready branding task t-013 sets display title This Means Warp without changing routes or saves.
<!-- note:end t-001 -->

## t-002 — Write This Means Warp captain, crew, location, antagonist and ethics bibles

<!-- note:begin t-002 -->
Lock the This Means Warp title and original sci-fi comedy voice. Confirm Vox, sentient Serendipity and Fluke narrator seeds without rewriting them; author six captain perspectives, sixteen crew arcs, twelve substantial systems, eight antagonists, faction ethics doctrine, three-act clue graph and sixteen ending prerequisites.

Authored six distinct captain arcs, sixteen three-stage crew journeys, twelve destination hubs, eight seeded three-act antagonists including an evil AI planet-wide game dungeon, and sixteen ending families with captain-multiplied epilogues. Editorial source is linked from DESIGN-BRIEF; actual quests, art and full ending coverage remain later roadmap tasks. Conductor scoped PR forthcoming.

Merged the complete authoring bibles in Conductor PR #6705 (dbd510a08255357df6fb4dff64765daafc300662). Six captain dossiers, sixteen crew multi-system arcs, twelve star systems, eight seeded three-act nemeses including the Showrunner AI dungeon planet, nuanced intervention doctrine and sixteen earned ending families with six authored captain variant requirements are linked in DESIGN-BRIEF.md. The compatible first-slice captain/crew screen and eight seeded rivals merged to kind_robots PR #4263 (8d584ecbddf9f4e34d137fb0cd9991225fb04361). Full runtime quests, ninety-six epilogues, rendered art and QA remain explicitly open on successor tasks; no publication or final human gate.
<!-- note:end t-002 -->

## t-003 — Implement deterministic voyage, ship/away staffing, ethics and persistence engine

<!-- note:begin t-003 -->
Seeded ship and away assignments, crew skill/injury/trust/absence, intervention consequences, antagonist effects, star-map unlocking, resources, saves/migration and battle-tested fail paths; no LLM at play time.

Submitted persistent crew-driven star-chart detours integrated with the three-stop voyage. All 12 existing crew have three original world encounters, two ethically different approach choices, return consequences and save-safe progress. Eight nemeses receive named specialist counterplay unlocked by two witnessed stages, adding an earned final council option. Six captains add distinctive outcome-specific reckoning; exact full sixteen ending families, four more crew, painted art and multi-act campaign remain sequel tasks. App PR upcoming with seeded replay and scarce-supply tests.

Merged Kind Robots PR #4266 as 5705e103e4b16ea202fde80ae57da942ab4a8071, with 16 of 16 completed green workflow checks on head 2cff7186898c19d2af66d5bdaeef5b766d32f191. New deterministic crew-directed chapter detours, 36 authored personal encounters for 12 playable crew, eight nemesis-specific earned counterplay routes, six captain epilogues, scarcity and save safety checks. The existing main missions still work. Full campaign, remaining four recruitable crew, art delivery, and comprehensive ending routes remain follow-up work.
<!-- note:end t-003 -->

## t-004 — Write 30 substantial space and away missions with consequence layers

<!-- note:begin t-004 -->
Varied diplomacy, exploration, rescue, scientific hazards, trade, first contact, crew disagreement and ship trouble, each with original success/mixed/fail/withdrawal, remembered people and policies.

Triage 2026-10-30 (verified on kind_robots main 0bb3088): rules MISSIONS = 30 (Act I 9, II 12, III 9; CI asserts MISSIONS.length 30), 12 systems, 90 per-policy aftermaths, via #4286/#4313/#4327. Small follow-up: flawless/costly/disaster result text is generic in rules.ts rather than per-mission.
<!-- note:end t-004 -->

## t-005 — Write 40 distinctive location, faction and shipboard encounter cards

<!-- note:begin t-005 -->
At least 12 locations; evolving local decks, Vox/Serendipity callbacks, consent/intervention complexities, crew arcs and alternative solutions without universal perfect specialist.

Triage 2026-10-30 (verified on kind_robots main 0bb3088): 53 expedition encounter cards (36 local across 9 worlds + 17 galactic) plus planet, casino and Serendipity decks via #4336/#4366/#4369. Note the Playbook Forge counts encounters from MISSIONS (30/40) and under-reports; fix the Forge metric, not the game.
<!-- note:end t-005 -->

## t-006 — Build eight personalized alien antagonist arcs and interrupt decks

<!-- note:begin t-006 -->
Each seed picks unique alien goal/method/complications/clues and interference, with nontrivial bargain/defeat/reconciliation/complicity resolutions and captain/crew combination coverage. Silas 2026-10-26: this is the randomized galactic enemy, one principal nemesis drawn per run.

Triage 2026-10-30 (verified on kind_robots main 0bb3088): 8 antagonists, each with 9 act moves, a clue and interference, nemesis card every second episode, 24 nemesis endings (#4316). Goal/method stay fixed per antagonist rather than reshuffled per seed.
<!-- note:end t-006 -->

## t-008 — Deliver Space Couch painted red-sofa ship, pocket-room, shield, crew and world art

<!-- note:begin t-008 -->
Deliver branded Space Couch project icon/card/hero, detailed red couch/force bubble/pocket room/starmap, original personnel and emotional portraits, Vox/Serendipity/Fluke continuity plates, twelve worlds and eight antagonist identities; verify final URLs, ArtJobs and render provenance rather than SVG/placeholders.
Canonical cast portrait redesign round submitted for code/art review. 66 new Krea2 requests in CAST-REDESIGN-ROUND-2.yaml, with a Kind Robots v2 art-slot preference and legacy fallback. This is only the first art tranche: rendered delivery, runtime exports, ship/world/outcome coverage and visual review remain open.
2026-10-27 PT cast redesign tranche merged: Conductor PR #6759 (9f39f1e849164660dedc42108cc277f029755fb8), app PR #4353 (d1ed41f468944a765edb58022f048ea14b6bdaff). All 4 Conductor and 17 Kind Robots current-head workflow groups passed. The 66 Krea2 canonical portraits (6 captains, 12 playable plus 4 future crew, three expressions each) are authored at CAST-REDESIGN-ROUND-2.yaml with auto_submit, versioned portraits/v2 keys and legacy fallback. Post-merge audit found 0/66 ArtJob IDs, 0/66 DONE and 0 exported v2 assets at that time. Continue via automatic art sweep, reconcile actual ArtJob IDs, inspect render quality, export .webp and update app generated art manifest, validate crops at phone/tablet/desktop, then finish remaining title/icon, couch room, 12 worlds, antagonists and story consequence art. No art-complete or human design gate.
Triage 2026-10-30: cheapest visible win is export, not generation. CAST-REDESIGN-ROUND-2 has 66/66 DONE v2 captain/crew portraits (ArtImage 257797+), but none are under kind_robots public/game-of-captains (only 21 legacy renders). Run scripts/export_round_art.py with --max-edge, rebuild utils/gameOfCaptains/artManifest.ts, then render the 12 worlds, 8 antagonists, couch, pocket room, starmap and 20 casino venues (t-027 handoff).
2026-10-30 PT art export (no new generation): kind_robots PR #4483 merged at fd9bd2396382fbe159d6fb1ecd0d44d4afe27e06, all 21 checks green. Shipped 18 CAST-REDESIGN- ROUND-2 v2 portraits (6 captains + 12 playable crew, 640px) that portraitArt() prefers over legacy faces, plus 10 RUNTIME-BEATS-ROUND-1 scenes (missions refugees/archive/bar, antagonists auditor/moth/curdle, 4 base endings, 960px); WARP_ART 21 -> 49. [...]
[Earlier history (2,679 chars) archived verbatim to projects/game-of-captains/T008-HISTORY.md -- read it there only when you need a specific past cycle. Append new cycles below, one short paragraph each.]
Scoped Space Couch art delivery: 44 DONE expression portraits are now served through the existing access-filtered ArtImage endpoint. Captain and crew dossiers expose three portraits, the away team shows defiant or vulnerable images based on assignment and injury, and briefing choices display the completed Holodeck, War Room and Infirmary artwork. Static contract tests include all unique keys. PR and CI pending. Do not mark the broader t-008 art campaign complete.
October 31 PT continuation merged Space Couch PR #4572 at fbd7f753a729e3c08da64147c7c084c540040eec with 20/20 exact-head workflow groups green. Delivered authenticated lookup for 44 completed Krea2 defiant/vulnerable portrait plates (CAST-REDESIGN-ROUND-2, ArtImage IDs 257798-257862, corresponding selected ArtJobs 50300-50364). Players can preview three expressions for each captain and crew member; away-team cards use defiant expressions, injured officers show vulnerable expressions. Pocket-room options display completed 09-holodeck, 10-war-room and 11-infirmary art; the selected room updates the briefing-stage painting. Main verified, branch deleted. Do not close t-008: final authenticated image reachability, responsive screenshots, couch/force-bubble/world art continuity and remaining illustrated consequences still need independent acceptance. No production deploy.
User requested continued Space Couch development. Connect the remaining 18 completed opening-title paintings to a full-screen player-stepped illustrated opening reel with original lines, accessible navigation, art fallbacks and contract tests; keep deployment and remaining t-008 art work separate.
Scoped delivery of 18 completed Space Couch OPENING-TITLES-ROUND-1 paintings: built accessible full-screen, player-stepped opening sequence inside existing main menu. Every frame has authored original dialogue, recorded art key and meaningful alt text; keyboard controls, reduced motion and image-failure fallback are covered by new static contracts. Game saves and private image access are unchanged. Opening PR/CI is in progress; larger t-008 art inventory remains unfinished.
Merged Kind Robots PR #4576 at c3b5d541401f76f81c4d27b67f72577e111da2e1 after all 17 exact-head GitHub workflow groups completed SUCCESS.  Added a playable 18-frame illustrated opening reel using the previously DONE OPENING-TITLES-ROUND-1 ArtImages 255479-255496 and original script; responsive full-screen presentation, player navigation, keyboard arrow/Escape support, reduced-motion handling, safe missing/private image fallback and clear exit/captain creation. No new ArtJobs, database changes or permission changes. Verified main commit and auto-deleted PR branch. Continue t-008 for ship/force-bubble art, authenticated image delivery and real 390/768/1440 visual checks; no self-hosted deployment or public release was authorized.
2026-11-02 PT curation: 5 crew pairs, 3 cast redesigns and the alt dashboard highlight are kept and shipped under public/game-of-captains (WARP_ART) in kind_robots#4661. 4 redo (gold delta badges read as a logo; Edda came out human), queued in art/GAME-OF- CAPTAINS-CURATION-REDO-1.yaml.

2026-11-12 PT, Silas: "whatever horoscope i get, there is no original art" and "there needs to be a wild break possible to avoid the horoscope, with at least 32 endings". Merged kind_robots#5082 (fc9ee12, 16/16 checks green): wired the 19 DONE COUCHSCOPE-AND-OPENING-ROUND-1 ArtImages 261262-261280 that had been rendered but never connected (all 12 constellation reveal plates, trolley question + 3 answers, red-couch mission cards for refugees/archive/bar, so The Last Lifeboat no longer shows the SVG title card). Added the Couchscope WILD BREAK: refuse the screening at any time, 4x2x4 branching escape through 13 scenes to 32 distinct endings, each with its own text, +1 starting perk and finale coda; launch unsigned, per-browser found-endings ledger; VoyageRun.wildBreak validated on restore. Queued 45 matching plates in conductor#7318 (WILD-BREAK-ROUND-1, priority 950), not yet submitted at merge time. Next: once DONE, curate a contact sheet and wire couchscope/wild/<scene> and couchscope/wild-end/<ending> ids into kind_robots utils/gameOfCaptains/onboardingArt.ts. Art remains incomplete; no deploy or human gate.

2026-11-13 PT: all 45 WILD-BREAK-ROUND-1 plates rendered DONE (ArtImages 270132-270176). Curated on a contact sheet: kept 43 (all 13 wild break scenes, 30 of 32 endings) and wired them into kind_robots utils/gameOfCaptains/onboardingArt.ts in kind_robots#5119. Rejected the-long-way-round (Nighthawks pastiche with legible lettering) and nothing-in-particular (legible GIFT sign); redos queued in art/WILD-BREAK-REDO-1.yaml, wire them under the same couchscope/wild-end keys once DONE. Remaining t-008 art scope is unchanged; no deploy or human gate.

Scoped artwork-recovery improvement: make failed alien, redshirt and voyage painting lookups retryable instead of permanently marked loaded. Add an accessible refresh control in Ship Settings and run a new regression in test:game-of-captains. Review only; authentic art URLs and visual curation still block completion.

Partial art-delivery reliability fix. Space Couch now has an explicit player control to refresh curated alien, redshirt and voyage paintings without resetting the voyage. Failed artwork fetches preserve already delivered images, pending refreshes cannot cross account changes, and the existing fallback remains. Branch worker/game-of-captains-t-008-art-refresh-z7p4n2. Do not mark t-008 DONE: painting acceptance, URL checks and 390/768/1440 browser evidence remain.

Old 12:46 UTC review claim is stale; legacy art-refresh PR #5437 was closed superseded, with retry handling merged through green PR #5442. Real painted asset acceptance and responsive URL checks remain. Return to READY, not DONE.

Eight new physically explicit red-couch shield and folding-pocket-room scene requests authored in SHIELD-POCKET-CONTINUITY-ROUND-1. Submission, original render review, accepted image IDs and runtime integration remain outstanding. This is partial t-008, not art delivery.

https://github.com/silasfelinus/conductor/pull/7707 merged to main as an authored private image-request ledger. This was a partial increment, NOT visually delivered art: authenticated original ArtImage review, ArtJob provenance, accepted render export, and actual playable UI integration remain open. Return finite art task to ready for curation.

Repaired shared art exporter to recognize curator ACCEPTED imagery and fail closed on REJECTED records even with contradictory legacy keeper text. Added strict-export and offline-audit regressions for Space Couch plate IDs. Branch commit adb4e69b71e200435906af42a540b9307bc474de; broader painted art delivery, authenticated inspection and 390/768/1440 checks remain open.

2026-11-22 PT closure (Silas-directed session; no other workers). All 8 SHIELD-POCKET-
CONTINUITY plates are curated keepers (6 from round 1; council and asteroid re-rendered
in CURATION-REDO-2 after round 1 showed franchise-style uniforms) and linked in the
access-filtered onboarding art (ArtImages 277779-277785, 278539-278540). The ship-prep
step shows them (Just-the-couch observation plate, infirmary pocket room, force-bubble
recharge) via kind_robots #5548 (eef3416) and #5553 (b6d4d05), both merged with all
exact-head checks SUCCESS. Painted couch/bubble identity confirmed across three full
signed-in voyages at 390/768/1440 (every screen painted, 0 broken images).
<!-- note:end t-008 -->

## t-010 — Run antagonist-by-captain-by-crew adversarial and every-ending seeded traces

<!-- note:begin t-010 -->
From-new-game action logs for all 16 endings, noninterventionist/exploiter/legalist/rescuer, depleted fuel/hull, absent and wounded crew, missed calls, low-trust diplomacy, strange event orders, old saves and softlock probes.
2026-10-30 (session 2026-10-30T14:02:23Z-goc-t010-q7m3): DONE via kind_robots#4522. - spaceCouchTraceHarness.ts plays the page's own path from a new game, using the store's compositions: background and star chart, travel, expedition quests, episode decks, call, transit, order, errands, romance, trio interludes and finale. - Every state it reaches must save and load intact, keep finite and in-range stats, read without template leaks, and leave at least one control that moves the voyage (softlock probe). - verifyGameOfCaptainsTraces.test.ts runs in test:game-of-captains (184 voyages, about 15s):
  - 8 antagonists x 6 captains with a counter officer aboard, under rotating rescuer, noninterventionist, exploiter, legalist, misser and depleted/absent-crew styles;
  - all 16 endings x 6 captains, with pinned seeds;
  - the counter council for all 8 nemeses, plus its refusal when no counsel is aboard;
  - 12 random-press walks;
  - 6 real saves written by engine a34da8fa (before today's merges), played on to endings;
  - bare version-1 saves.
- npm run test:game-of-captains:traces (--full) played 2,116 voyages, including one walk for each of the 220 parties. All OK, no softlock. - Defect fixed: a star or clone coda suffix on the ending title broke the ending-art lookup (endingFamilyTitle). - Findings left for Silas or t-011:
  - Trust is dominated by the episode decks, so A MOTION OF NO CONFIDENCE needs a deliberately mutinous plan.
  - Acts II and III reuse a 17-card galactic quest deck, so about 36 of 59 cards repeat per voyage.
  - The playbook run review stores coda-suffixed ending titles.
<!-- note:end t-010 -->

## t-013 — Replace Warp display identity with Space Couch across app and Project row

<!-- note:begin t-013 -->
Once kind_robots PR #4185 has passed all checks and merged, update visible captain title, title-screen lettering, Play navigation, dashboard featured experience and owned Project presentation to This Means Warp. Keep Conductor slug game-of-captains, existing /play/game-of-captains deep link, save key, user progress and Fluke/Vox/Serendipity narrator entities unchanged. Ensure working captain/crew/away/log/settings navigation, no broken route, and screenshot plus seeded test coverage. If PR #4185 is still in review, do not clobber its branch; coordinate on merge order.

Submitted save-compatible in-game display-brand update with Play title/menu, main home highlighted game cards, and tests. For Capes & Tassels this is only the title and week-one simulation clarification part of the larger map/day-night t-012; subsequent gameplay work remains open.

Merged kind_robots #4188 as 0f9c4843 after all 22 checks green. Visible This Means Warp title, full-screen page, Play tab, home highlight and browser title now renamed; old route and save keys preserved. The existing Kind Robots Project database title field was not updated or verified in production (KR_API_TOKEN unavailable). This last metadata/API verification remains to be done under t-013. No further frontend rename required. Production self-hosted deploy has not been verified.

Space Couch user-directed renaming and couch-vessel gameplay shipped to kind_robots PR #4248, plus Conductor canon and Krea2/Arthemy art requests. Preserve game-of-captains routes and saves. Project database title and painted ArtJobs still unverified; mark incomplete rather than falsely done.

DONE 2026-10-26 PT: kind_robots #4248 merged 2026-10-26T23:35Z (Space Couch identity, share preview and covers from painted art). Production Project 2159 (conductorSlug game-of-captains) read "space-couch"; set to "Space Couch" through PATCH /api/projects/2159 and read back. Painted ArtJobs are tracked by t-008 and the RUNTIME-BEATS round, not this rename.
<!-- note:end t-013 -->

## t-014 — Rewrite all authored scenes and outcomes for the literal couch-ship premise

<!-- note:begin t-014 -->
Audit every existing and new voyage, planet, away-team and antagonist script to make the red couch the spaceship. Integrate miniaturized rooms, persistent vacuum bubble, docking and seating constraints in meaningful mission branches; no old conventional bridge/cockpit or ordinary cruiser illustrations. Coordinate with claimed t-002 and t-003, preserving Vox/Serendipity/Fluke seeds. Adversarially verify couch resource choices and art/script consistency.

Triage 2026-10-30 (verified on kind_robots main 0bb3088): the literal red-couch premise runs through all three acts (tone pass in #4327; rules.ts states no hull/bridge). Stage art is still SVG and is tracked under t-008.
<!-- note:end t-014 -->

## t-015 — Crew personal quests: every crew member's three-step quest crosses the galaxy

<!-- note:begin t-015 -->
Silas 2026-10-26: "individual crew quests that take you around the universe." Each of the sixteen crew carries a personal quest of three steps set in different star systems; the away-team trio chosen decides which quests are live and so where the couch goes. Quest outcomes feed the crew epilogue lines in every ending (t-016). Dry absurdist register: crew grievances treated with total procedural seriousness. Forge plan: followerQuestSteps 3, locations 12 (kind_robots#4255); the ledger reads 0 of 3 steps built until this lands.

Kind Robots PR #4289 implements twelve authored original three-world crew odysseys with 36 substantial episode scenes, 36 earned plot reversals, 72 stage-two decisions, 36 relics and individual conditional epilogues. Two player choices per stop, witnessed first gambits and saved consequences replace one-click errands. Existing quests, nemesis counterplay, romances, Act I mission board and save key remain compatible. Companion atlas Conductor PR #6727 merged as d8f9ec7 with passing full CI. Game PR is awaiting final CI verification, merge and live runtime quality review. Paintings, 220/560 trio adventures, 16 total playable crew and later acts remain separate requirements.

Merged the complete playable 12-person first tranche of the sixteen-crew quota in Kind Robots PR #4289, squash commit 667a4729cdb02181a46535c2c5683cd45f1c411f. All 16/16 PR workflow groups green on head 12f50ee08cd058415ae8b647dec6304ec5e3209b. Each current officer now has three original multiworld epic episodes, two-stage gambit/reversal/resolution choices, 36 relics and individualized earned protected/public/unfinished epilogues. Conductor writing atlas PR #6727 merged d8f9ec7289f695b04f4ce7ff262f7f3a98c3d551. The original task explicitly requires SIXTEEN crew. FOUR prospective cast members remain to be made recruitable and receive equally substantial three-stage quests; do not mark the full t-015 quota done yet. Painting the roughly 156 slots proposed for the first twelve, device QA and the 220/560 trio-only adventures are independent downstream gates.

Triage 2026-10-30 (verified on kind_robots main 0bb3088): 12 crew x 3-step personal quests = 36 (#4289). The task text says 16 crew, but the shipped roster, Silas's 2026-10-27 220-trio math (C(12,3)=220) and the Forge plan all use 12. Reopen only if Silas still wants 16.
<!-- note:end t-015 -->

## t-016 — Per-captain ending versions and crew epilogues (16 endings x 6 captains)

<!-- note:begin t-016 -->
Silas 2026-10-26: "different opening combos will create different end game endings ... a set of three crew members isn't remarkably complex, but adding a captain to the mix will multiply it." Write and paint each of the sixteen endings once per captain (96 versions); the crew trio adds one epilogue line per crew member, not separate endings. Forge plan endingVersions per-hero with followerEpilogues (kind_robots#4255). Seeded traces in t-010 must cover every captain version.
All 16 galactic endings now have a version for each of the 6 captains (96/96): the 12 earned families from galacticEndings.ts plus 36 new lines for the 4 base logs and 2 counter logs (baseEndingCaptains.ts, kind_robots #4501, merged 69dfacb). Tests replay every seeded ending trace under each captain and assert the captain's own line; all 96 versions are distinct. Crew epilogues already existed. Per-mission flawless/costly/disaster text follows in #4502. Painted ending art remains art-queue work (t-009).
<!-- note:end t-016 -->

## t-017 — Ship the consent-first alien fourple and branching romance prototype

<!-- note:begin t-017 -->
User-directed adult romance: three authored scenes for a four-person relationship with captain, Vela, Taal and Omi, individual consent, boundaries, earned commitment, principled rejection and breakups; additional individual Rue and Tess relationship routes that may fail. Save choices under the existing voyage key, without stat penalties for romantic refusal or forced relationships. Add visual bounded-screen story encounters and deterministic tests for all routes, rejection, old-save restoration and earned epilogues. Isolate a pure romance module from the concurrently claimed core-voyage engine t-003. Additional rendered art remains t-008. See content/RELATIONSHIPS-BIBLE.md.

Authored and wired an optional three-chapter four-person alien romance with Vela, Taal and Omi, plus conditional Rue/Tess romance arcs, separate consent, pressure rejection and amicable breakups. Saves store relationship decisions on the existing VoyageRun object and original local key; finite ending epilogues respect the primary galactic finale. Added consent, save and seeded tests. Kind Robots implementation PR opening after this review event.

Merged complete optional first-voyage romance slice in Kind Robots PR #4268, commit f21510f6ad61ec5094b69f278599e5a03ed7b8c5. It adds the Three-scene Four-Cushion Accord among the captain, Vela, Taal and Omi, with independent consent, ethical rejection, amicable breakup and a committed four-person path. Optional Rue and Tess romantic stories have separate doctrine restrictions and non-happy branches. Pure story code, bounded-screen debrief dialogue with portrait fallbacks, saved relationship decisions and distinct final epilogues preserve the existing game-of-captains-voyage-v1 local storage key, mission stats and 3-officer roster. All 16/16 GitHub Actions workflows completed green on final PR head de17669cd28bd9ead15150d89ce6a23c6e8bb254, including game seeded tests, TypeScript, Prettier and contract shards. Original design brief and ROMANCE-BIBLE merged through Conductor #6711, commit c141f538a4c0f2140f49d5b012727f5eae7f96b7. Rendered romance illustrations, wider campaign consequences and real self-hosted deployment remain later art/quality tasks; no ArtJob IDs or production release verification claimed.
<!-- note:end t-017 -->

## t-018 — An interstitial adventure for every crew trio (220 trios x 3 steps)

<!-- note:begin t-018 -->
Silas 2026-10-27: "there are 220 different combinations of 3 crew members with 12 options. that means each crew combo can get ... an interstitial unique multiple step adventure ... this is an adventure across an insane universe, and we're just along for the ride." Each trio gets its own three-step adventure between the main beats (660 scenes), written dry, with authored art prompts. Forge plan partyAdventureSteps 3 (kind_robots #4272).
2026-10-30 (session 2026-10-30T11:47:12Z-spacecouch-q7r2): all 220 = C(12,3) trios authored and on main. The 100 previously missing parties were written as batches D (kind_robots#4487, a2ea530), G (#4493, 2799be8), I (#4497, 4bbec7d) and J (#4500, be9657c), 25 each in CrewId combination order. Each has a three-step Act II interlude built from those crew members' dossiers, two endings and five literal Krea 2 prompts; prompts pass verifyPlaybookArtPrompts. verifyGameOfCaptainsTrios now asserts 220/220, and the Forge factors partyAdventureSteps/partyEndings read 3/2. No art submitted: 500 new trio art slots are prompted and unrendered.
<!-- note:end t-018 -->

## t-019 — Endings of their own: two per crew trio (440) and three per galactic boss (24)

<!-- note:begin t-019 -->
Silas 2026-10-27: "each crew combo can get 2 unique endings ... even just the endings for each galactic boss ... we should just have more interesting things than four endings planned anyway." 440 trio endings and 24 boss endings, each written and painted, on top of the sixteen per-captain endings (t-016). Forge plan partyEndings 2, villainEndings 3 (kind_robots #4272).
2026-10-30 (session 2026-10-30T11:47:12Z-spacecouch-q7r2): 440/440 trio endings exist (2 per party across all 220 parties, batches A-J; the last 200 via kind_robots#4487, #4493, #4497, #4500). Every ending is reachable by some run of three choices (contract-tested) and has a literal Krea 2 prompt. Boss endings were already 24/24. Painting remains art- queue work, not part of this close-out.
<!-- note:end t-019 -->

## t-020 — Space Couch: captain-first illustrated onboarding

<!-- note:begin t-020 -->
FROM GITHUB ISSUE silasfelinus/kind_robots#4533 (https://github.com/silasfelinus/kind_robots/issues/4533), opened by @silasfelinus on 2026-10-30. Imported by scripts/sync_github_issues.py. Reference the issue in the implementing PR (`Closes silasfelinus/kind_robots#4533`) so it closes on merge; the bridge closes it otherwise once this task is done.

Track the user-requested Space Couch mobile onboarding changes: captain selection first, background second, illustrated options, and a revised corporate Couchscope.

Kind Robots PR #4534 implements captain-first onboarding, compact phone dossier, rewritten corporate Couchscope, and secure store-owned ArtImage lookup. Conductor PR #6866 merged with 22 DONE ArtJobs 52152-52173 and ArtImages 258444-258465. App final-head CI underway; merge only after all checks pass. Authenticated device screenshots and production deploy remain separately unverified, so do not mark accepted or publicly released.

2026-11-04 PT reconciliation: captain-first illustrated onboarding merged as kind_robots
#4534 (10-31). Device QA belongs to t-011/t-012, so this task is complete.
<!-- note:end t-020 -->

## t-021 — Deepen all 12 crew courtships and six crew-to-crew relationship pathways

<!-- note:begin t-021 -->
Silas 2026-10-26: expand and deepen each romance, at least one path for every crew member, and cross-crew paths. Extend t-017's consent-first three-scene romance engine to 12 individual courtships and six original crew-pair routes covering all 12 officers, preserving the Four-Cushion Accord, v1 saves and optional/non-punitive refusal. Give every route distinctive dialogue, incompatibilities, earned success, friendship, heartbreak and epilogue. Author the four not-yet-playable expansion crew paths separately, never count unimplemented art or cast as available. Validate seeded replay for each route and pair, old saves, duplicate actions and multi-role outcomes. Coordinate with independently in-flight Forge plan/roadmap PR #6714.

Authored 12 individual and six crew-pair three-part romance paths and preserved the four-person agreement. Kind Robots PR #4274 contains the reusable story engine, typed text catalogue, distinct negotiation and endings, off-duty autonomy and from-new-game coverage. Conductor #6716 adds readable canon for the twelve live officers and four future non-playable recruits. All merged work requires completed green checks.

Kind Robots PR #4274 merged to main as 1041ac7f9bd07991865ea9dd63d542919030289d. All thirteen pull-request workflow groups were completed and passed on final head f4989fa08b21b3de2373e8a56b6752d884cf3697, including game tests, TypeScript, formatting and all contract shards. Twelve solo three-stage romances, six additional cross-crew paths and the original four-person agreement are authored, playable, save compatible, consent-first and tested. Story atlas Conductor PR #6716 merged as de8b917d3e00f3a9c8bc89d320566a1bfac1d0ba with four green workflow groups. ArtJob portrait/outcome coverage, future four recruits and longform relationship continuity remain downstream work; self-hosted deployment not verified.
<!-- note:end t-021 -->

## t-022 — Branching Act I: mission board, conditional galaxy routes and remembered consequences

<!-- note:begin t-022 -->
Silas 2026-10-26 PT approved building a substantial branching Act I after gameplay-depth audit in kind_robots#4182. Deliver a replayable, choice-led Act I mission board with materially different reachable destinations, eight or more distinctive missions, persistent civilian/faction consequences, crew-enabled special routes, adversary callbacks, and a map-like choice interface in the art-forward couch game. Preserve v1 saved voyages, personal quests, romance scenes, ethical intervention and game result math. Test seeded trajectories from different crews, captains and decisions, expiration, reload and genuine state-dependent payoffs. This is an Act I milestone, not completion of t-004's 30 missions or t-007's full 3 acts.

Added a playable three-stage branching Act I mission board with nine original mission families (six beyond the existing first voyage), twenty-seven unique ethical commands, persistent local-world decision flags, seeded villain mission sabotage, seven new crew synergies, world echoes and contextual final-epilogue memories. Compatible with prior version-one save keys and legacy original mission IDs. Branching and old-save seeded tests plus single-screen chart controls ready for CI review.

Kind Robots PR #4286 merged to main as 46264ddbc53ab50589c399114d66fc9694eba39e. All sixteen of sixteen GitHub Actions workflows completed green on final PR head f518166f64dbe36cabce569ed2fdef09999987af, including deterministic Space Couch seeded game replay, TypeScript, formatting, layout and four contract shards. Act I now has 9 distinct mission families and 3 selectable chapter boards, 27 world-specific ethical actions with saved civic flags and distinct aftermath prose, seeded antagonist-specific mechanical penalties, 7 additional pair synergies, changed subsequent access/odds and final civilian callbacks. Old voyage key and earlier mission identifiers remain compatible. No ArtJobs or production deploy/physical screen QA claimed. Full 30 mission, 40 encounter, 16 ending and 220+ trio adventure production tasks remain open.
<!-- note:end t-022 -->

## t-023 — Space Couch: six unmistakable captain archetypes and twelve character-forward crew dossiers

<!-- note:begin t-023 -->
Silas 2026-10-26 PT requests six specific highly comic captain archetypes (genius punkette, bombastic wannabe hero, velvet horror-show host, stuttering bored time traveler, severely gothic recycled-fluid drinker, paranoid final girl promoted from janitor four weeks ago), and equally distinctive crew. Preserve all IDs, art keys, shared save format, roles and existing branching quests/romances. Rewrite selection sheet voice, folly, narrative promises, strengths and dramatic price for all 18. Make Mox-9 visibly an embodied sentient android struggling with its autonomy. Include captain-specific gameplay variation and crew counterpoints. Test unique hooks, saved games, opening identities and all playbook contracts before merging. No new art/render/deploy is claimed.

Rewrote six captain archetypes and all twelve crew dossier hooks, comic objects, character flaws, narrative promises and role-specific dialogue; Mox-9 now explicitly an embodied sentient android. Added six character specific once-per-chapter player decisions with tactical risk/reward and named crew rebuttals, save and finale callbacks. Revised game selection sheets and added seeded CI verification. Independent cast art/voice atlas on Conductor design branch; painted portraits still pending.

Triage 2026-10-30 (verified on kind_robots main 0bb3088): rescue PR #4413 merged six captain archetypes and twelve crew dossiers with once-per-chapter decisions. Painted portraits belong to t-008.
<!-- note:end t-023 -->

## t-024 — Miniaturized redshirt expedition corps: 100 alien hires, travel encounters, command staffing and fatalities

<!-- note:begin t-024 -->
Silas 2026-10-27 PT requests a grander cosmic-satirical adventure format drawing on original comedic pulp SF, bizarre galactic satire, fatalistic shipboard humor and surreal speculative fiction. Add a travel/quests expedition phase alongside existing Act I mission/crew-quest loops. Each destination has 1-4 main encounters and several minor local or galaxy-wide encounters, allocated among captain plus three officers; distinct secrets emerge from officer assignments to minor errands and from delegating consequential diplomacy to unskilled redshirts. Add a miniaturized couch redshirt dorm, hire/survival/fatality mechanics targeting 1-in-3 deployment fatality, and 100 explicitly unique named redshirts with visually diverse alien bodies, redshirt uniforms, differentiated stats, latent power, and character backstory. Preserve save format and autonomous crew/romance story paths, and document separately generated character portrait/encounter art queue slots. Seeded tests for exact authored roster count, reproducible missions, crew exclusivity, consent/skill checks, fatality, recruitment, and old-save restoration. Not a claim that portraits are painted.
CLAIM RETURNED 2026-10-27 PT: a Forge-upgrade agent re-claimed this task (session 2026-10-27T19:30:00Z-sc-rescue) to rescue the stale red PR #4305. It then saw the original redshirt session push e85855d and ce346dd at 19:31Z, stopped without pushing, and handed the claim back to that session. claimed_at is set to its 19:31Z push.

Triage 2026-10-30 (verified on kind_robots main 0bb3088): stale 10-27 claim. Work merged via #4336 + #4366: 100 unique redshirts (test asserts unique names/bodies/powers), dorm, 1-in-3 fatality roll, expedition phase, saves. Closed-unmerged #4305/#4414 are superseded; remote branch worker/space-couch-t024-redshirts-travel-e62b holds only older text and is safe for branch-janitor. 200 redshirt portraits are art work under t-008.
<!-- note:end t-024 -->

## t-025 — Submit 200 distinctive redshirt portraits and secret-power mission plates

<!-- note:begin t-025 -->
User on October 27 PT explicitly requested immediate redshirt art submission while the home art generator has capacity. Reuse the exact 100 stable identities, anatomy, histories and powers in Kind Robots PR #4305; submit 100 recruitment portraits plus 100 secret-power action paintings to the authenticated Kind Robots ArtJob queue using an auto-submit Conductor ledger. Ensure consistent bright red uniforms with radically diverse alien body plans, unique seeded prompts and persistent ArtJob IDs, idempotent reruns and real provenance before calling art delivered. Render results and production manifests require separate verification.

User explicitly requested live redshirt art batch submission on October 27 PT. Created and merged Conductor PR 6736, the 200-request Krea2 ledger, dedicated deduplicating credentialed submit script, safety tests and trigger workflow. Actual run 40556939008 completed successfully; fetched ledger from main afterward and verified exactly 200 unique accepted ArtJob IDs 48128-48327, one recruitment portrait and one secret-power plate for each of 100 stable rs-001..rs-100 aliens from Kind Robots PR 4305. The requested deliverable is authenticated ArtJob submission only. Images are not marked rendered, approved or wired to the client.
<!-- note:end t-025 -->

## t-026 — Playbook Forge upgrade: literal Krea 2 prompts for every Space Couch beat and Act II-III missions in dry space-comedy satire

<!-- note:begin t-026 -->
Silas, 2026-10-27 PT: "Anything that is in playbook forge and has quests unwritten or art prompts unwritten should be upgraded. (Memory dungeon will take the longest and should be last). Space couch has a lot of fresh writing still in need and still looking to capture that right blend of space comedy and satire. All art prompts should be written for the appropriate engine, no metaphors for krea2." Shared bar: kind_robots PR #4308 (verifyPlaybookArtPrompts, artPromptsComplete). Forge 2026-10-27: 21 unpainted beats have no prompt; plan gaps quests 9/30, encounters 9/40, locations 9/12, endings 4/16, villain endings 0/24. Write new missions and encounters that lean into the literal red-couch starship and deadpan bureaucratic satire, wired into play with saves preserved. Advances t-004, t-005 and t-014 without closing them.

Triage 2026-10-30 (verified on kind_robots main 0bb3088): stale 10-27 claim. Forge gaps named in the task are closed (quests 30/30, locations 12/12, endings 16/16, villain endings 24/24); #4309 wrote literal Krea 2 prompts and artPromptsComplete is true.
<!-- note:end t-026 -->

## t-027 — Seeded finite solar-system circuits with sentient blue-giant casinos and themed Serendipity franchises

<!-- note:begin t-027 -->
Silas 2026-10-27 PT: keep each Space Couch voyage within a randomized bounded number of distinct solar systems, each with its own systemic conflict and revisitable identity. Every selected system has one casino built ON and AROUND a living Galactus-scale blue alien person, with its Serendipity franchise physically INSIDE or ON that casino. Never treat the bar and casino as separate destinations. Author at least twenty distinctive Serendipity themes (including Tex-Mex cantina and crumbling arcade- sports-bar variants), EACH with an independently illustrated venue and unique playable questline, not recolors or shuffled identical quest text. The blue giants' homeworld was colonized; the colonists call the use of their bodies as casinos a "fair" compromise. Treat the power imbalance and host consent as dramatic conflict, not a settled moral fact. Each visit draws randomized playable encounters within the combined casino/bar venue, with real decision/consequence differences, enduring system identity and seed/save compatibility. Keep Serendipity the separate sentient establishment and Vox its own voice. Update the game map/arrival/expedition UI, give honest art-prompt backlog, and add seeded replay/regression tests. Human art and release gates remain separate.

The implementation is open as kind_robots PR #4351 with twenty authored franchise questlines, finite seeded star circuits, preserved old saves and the living casino UI. Conductor #6757 merged with the private Krea 2 twenty-image ledger, deduped art submitter and internal workflow. Await current-head game PR checks, review, merge, image queue checkpoint, and later rendered/attached artwork verification.

Triage 2026-10-30 (verified on kind_robots main 0bb3088): 20 franchises x 3 beats, 12 system seeds, 4-7-system circuits (#4351, ledger conductor #6757). The 20 venue renders (0 DONE) move to t-008.
<!-- note:end t-027 -->

## t-028 — Build single-screen episodic dispatch board, fog-of-war redshirts and three encounter decks

<!-- note:begin t-028 -->
Silas 2026-10-27: make the quest/encounter loop feel like a console game, not stacked web forms. Each episode: arrange captain, crew and miniaturized redshirt cards adjacent to visible quest cards to maximize forecast success; conceal untested redshirt stats and talent, reveal competence only after their first resolved field encounter. Quests take 1-3 days (mostly one), including carried assignments and deadlines. Then draw one each from distinct seeded planet, occupied blue-giant casino and Serendipity franchise encounter decks; include recurring plot/crew stories, daily inciting incidents, at least one nontrivial deterministic choice, faction consequences and replay-safe saves. Principal nemesis interrupts at least every second episode and returns in an earned finale; create faction/quest ending gates. Show one-screen compact TV-episode console with readable cards, focus/touch/keyboard selection, a clear resolution step, episode recap and cheesy 'tune in next week' stinger. Reuse existing 100 redshirts, Act I-III missions, living casino venues, Serendipity questlines, nemeses and legacy saved VoyageRun IDs. Coordinate with active t-024 expedition engine and t-026 campaign work, avoid rewriting their owned data or corrupting existing run saves. Ensure CI, seeded full-cycle tests and phone/tablet/desktop geometry; final creative approval only after other agent-owned coverage is actually complete.

Space Couch's first episodic dispatch/deck console implemented on app branch worker/space-couch-t028-episode-console-7b4f2. Card-based full-screen quest assignments, redshirt hidden talent until first encounter, seeded mission forecast and duration, parallel dispatch, planet/casino/Serendipity decks, every-other-chapter nemesis interrupt, earned faction-ending codas, legacy v1 saves and deterministic tests. Pending app PR CI and source/visual review. Remaining scope may require a subsequent task increment after verification.

2026-10-27 PT Space Couch episodic dispatch console first playable increment MERGED in kind_robots PR #4356 (b387db38ac2eec6b8177af8f42925404d0c5bfd8). All 19/19 PR workflow groups completed green (TypeScript, full contract, gameplay slice, format, layout contract, Docker container build). Implemented one-screen redshirt/crew/captain card assignments with classified redshirt skills until first encounter, 1-3-day majority-one-day contracts, seeded simultaneous resolution and consequences, authored planet inciting cards, unique planet/casino/Serendipity encounter decks, every second-episode persistent nemesis card, faction-conditioned ending codas and tune-in-next-week stingers; saved VoyageRun v1 compatible. Next agent-owned work: live rendered phone/tablet/desktop cross-width assessment once manually deployed, test a whole episode from fresh save and after resume, audit visual/card legibility, balance and mission-result prose consistency, extend deck variations and finale conditions and adversarially test long-run pacing. The app PR merged without a production deploy; do not mark the full t-028 creative or device-test objective complete until these checks pass. Do not park at final human approval yet.

2026-10-27 PT: Player-requested episode pacing refinement: replace 1-3-day redshirt quest contracts with one-round resolution, cap unique recruits at 8 originals per voyage including fallen identities, and remember tested per-skill stats across new voyages on this browser. Solar-system plot deck cards receive explicit captain/three-officer casting, seeded one- or two-seat capacity, skill forecasts and single-round results, preserving constellation/clone/venue story systems. Implementation branch worker/space-couch-t028-one-round-c31f, pending PR and full CI. No cloud-profile sync or deployed visual verification claimed.

User-requested one-round Space Couch encounter and redshirt scarcity pass merged in silasfelinus/kind_robots PR #4366 (squash commit 93b31f7d793e5b65dc53126750b0439bc6f2ff05), with 19/19 head-SHA GitHub Actions workflows green, including seeded gameplay, TypeScript, full four-shard contract suite, changed-file formatting, layout and production-container build. Six starter originals and only two additional unique recruitment contracts per voyage; casualty history still counts against the eight-original cap. Per-person, per-skill field reports saved in independent local-browser knowledge ledger across new voyages, without changing v1 saves. Every expedition quest now resolves in one simultaneous round; planet, casino, Serendipity, constellation and nemesis plot cards require named 1 or occasionally 2 command officers from captain + selected three crew, with seeded skill forecast, persisted outcome, consequence and recap. Reused prior clone and 12-sign story. Remaining creative/release gaps: visually inspect actual deployed phone/tablet/desktop card layout and long-play pacing, verify persona/device persistence expectation, review plot narrative consequences and delivered portraits; no live deploy or final human approval claimed. Return t-028 to READY rather than DONE.

Additional Space Couch polish increment in worker/space-couch-t028-interleaved-quests-b72c: allow unfinished minor redshirt quests to reopen after mandatory main quest dispatch and between successive planetary, blue-giant casino and Serendipity plot cards; retain completed deck state and one-round timing. Remove fictional successful-outcome prose and unearned venue credit when a command team fails its seeded check, preserve the attempt record without advancing host consent or bar stage, and gate earned faction standings on successful outcomes while retaining legacy save credits. Added deterministic failure, side-quest, resume and UI contract regression tests. Pending PR/CI; no device screenshot or live deploy claimed.

2026-10-27 PT: Kind Robots PR #4368 squash-MERGED into main at 0e332bed4502104b2b8f213e0c5a63c403cfac56 after 18 of 18 exact-head Actions groups completed successfully (TypeScript, seeded Space Couch gameplay, 4 contract shards, changed-file Prettier, layout and production-container build). Shipped UI access to unresolved minor redshirt quests after mandatory main quest dispatch and between subsequent planet/casino/Serendipity/constellation/nemesis plot scenes; existing one-round dispatch and deck draw histories survive interruption and v1 restoration. Fifteen authored choice-specific setback responses distinguish failed command objectives from earned successes. Failed blue-giant casino and Serendipity visits preserve an attempt record but cannot pretend host consent, award a completed venue beat or unlock undeserved reputation; faction finale scoring now ignores failed contemporary results while respecting old draw records. New interleave/failure/legacy regression suite passed. Verified code on main and merged PR state; successful container build is not evidence of live deployment. Keep READY for genuine rendered multi-device playtesting, long-run adversarial pacing, painted art verification and later final approval, not HUMAN GATE.

Continuation after merged Space Couch PR #4368 (0e332bed4502104b2b8f213e0c5a63c403cfac56, 19/19 CI green): authored encounter skill/crew spotlight pass in Kind Robots PR #4369. Episode opening teaser now matches the actual planet card; all 10 planet scenes and 8 casino incidents have theme-specific skill checks; the 20 Serendipity settings, 12 signs and 8 nemeses get consistent thematic requirements. A named crew specialist grants +12 chance on their connected planet plot; recurring successful two-person teams earn a capped +15 rapport bonus with Lead/Support labels and readable recaps. Full seeded regression and TypeScript/contract CI pending; no live device or art approval claimed.

2026-10-27 PT: Two Space Couch gameplay increments merged and verified. PR #4368 squash 0e332bed4502104b2b8f213e0c5a63c403cfac56 with 19/19 workflow groups green: side redshirt quests remain playable between seeded one-round plot encounters, failed casino/Serendipity attempts no longer advance completed venue objectives or fabricate outcomes, and new adversarial resume tests cover the transition. PR #4369 squash dd5c9e2d4fa526fc920d61b00cbad1463a9fbabc with 18/18 groups green: opening teaser references the actual planet story, 10 planet and 8 casino encounters plus 20 Serendipity venues, 12 star signs and eight nemeses have coherent thematic skill checks; connected officer +12 specialty and prior successful lead/support pairing +5 per win (capped +15), with display and seeded regression. Main verified. Master issue #4182 updated. Remaining: real device screenshot review, original delivered art, full multivoyage adversarial narrative balance, and possible account-backed redshirt memory; task remains READY, not DONE or human-gated. No independently verified live production rollout.

Scoped episode dispatch follow-up: added a mission-by-mission casting comparison console with known skill forecasts, explicitly classified untried redshirt aptitudes, safe one-to-one crew swaps, clear and undo, and deterministic tests. No saved VoyageRun schema or encounter mutation. Implemented on worker/space-couch-t028-compare-cast-6bd4; pending PR and exact-head CI before merge. Final rendered device QA, painted images and long-play analysis remain for future increments.

Merged Kind Robots Space Couch tactical assignment console PR #4391 into main as af716434141f483ed2c59c6f10231c6801bf230f. All 16 of 16 exact-head GitHub workflow groups passed at 275f1043044937c63e145c58446bfce2152f7e48 including TypeScript, seeded gameplay, layout, formatter, and full contract shards. Cypress binary download in Comment Migration check initially failed with a corrupted upstream 34 MB download versus expected 249 MB; retry passed. New compare-cast panel presents known quest forecasts but redshirt untried talents remain classified; moves between occupied quest cards swap the assigned actors, and REMOVE / UNDO afford safe planning. Pure immutable planning helper and deterministic regression coverage included. No save-schema modification. Return task READY for visual phone/tablet/ desktop screenshot QA, long-run narrative balancing, and final original painted ArtJob delivery; no deployment or final human gate claimed.

Triage 2026-10-30 (verified on kind_robots main 0bb3088): one-screen dispatch board, hidden redshirt stats and encounter decks via #4356/#4366/#4388/#4391/#4467. Rendered phone/tablet/desktop QA belongs to t-011.
<!-- note:end t-028 -->

## t-029 — Redshirt cloning saga: persistent generations, memorial quests and earned endgame

<!-- note:begin t-029 -->
Silas 2026-10-27 continuation: dead miniaturized redshirts can be recovered in later episodes as clones, but never as an unpriced resurrection. Track a stable original identity, generation count, clone history, field memories, accumulated discoveries, death memorial, abilities and consequences across save/restore. Original death still matters; the clone must become a distinct continuing character, not just an identical reset. Build escalating clone tiers, each requiring earned research, missions, scarce supplies and ethical choices. Introduce a substantial multi-episode authored clone questline that unlocks one tier at a time and requires increasingly advanced living clones for its later story beats; allow refusal, consent and non-clone alternatives. Future expeditions can bring back fallen personnel and use differentiated clone abilities, with player-visible generations, memories and mission consequences. Include clone-dependent faction reactions and unique finale/epilogue, not purely cosmetic progression. Preserve one hundred existing redshirt IDs, fog-of-war learning, independent casualty outcomes, seeded episode boards, old v1 save compatibility and the separate outstanding t-024/t-028/t-026 workers' changes. Reconcile those PRs rather than overwriting their files; ship tested staged playable progress and keep unfinished story/art scope open.

First playable Red Thread clone-story tranche in Kind Robots PR #4357. Five authored chapters with branching consent/evidence/shortcut choices, 4 generations, field-experience/episode gating, memorial and lineage records, generation bonuses and unique clone-rights or coerced-copy finale codas. A versioned v1 save extension retains existing IDs. Compact clone lab integrated with the new episode console and tested in seeded gameplay and save restore. CI currently being verified. Concurrent t-034 duplicate-key blocker was surgically corrected before this event's retry. Art variants, UI geometry post-deploy and further adversarial whole-run review remain to complete before any human gate.

Kind Robots Space Couch PR #4357 merged at df1ccd739206ad2deb587211a73581a2bb2edbfd after 19 of 19 current-head workflow groups finished successfully (head b48b528b66093e59e73fc65038de62accb3c310c). Implemented a 5-act branching Red Thread storyline, four increasingly expensive and capable clone generations, previous-episode field experience and story gating, original memorial continuity, additive v1 save validation, console lab and crew-card badges, clone-rights/consent endings and seeded regression tests. Future t-029 increments remain: produce and verify each clone generation's distinct character artwork, visually inspect deployed phone/tablet/desktop geometry, and run longer adversarial whole-run/branch-ending simulations. No new clone portraits, live deployment or final human acceptance claimed.

Scoped next clone-saga increment under review: living-witness only story gates; paid same-generation reprints for clones killed before earning a later act; four generation-specific tactical mission traits; one-time mission breakout effects for reputation, trust, nemesis pressure or supplies; named personal memory testimony; visible signature and iteration hints in the console. Adversarial test covers failure, mortality, rerolls, save reload and reward farming. Kind Robots branch worker/space-couch-t029-clone-afterlives-6fa4b, PR and exact-head CI required before merge. Art generation and device QA remain outstanding. No production deployment approved.

Kind Robots Space Couch PR #4374 merged as d39b265575c57e45cc0314144132a8d7fef0bb23 with all 18 of 18 exact-head CI workflow groups green at ee2faf67064169cb9949be0eb29b27835989b45e. Living named clone witnesses must survive earlier-episode assignments to unlock the next research act. After an untimely clone death, later episodes offer a paid same-tier reprint with unique printing records rather than a free upgrade or unwinnable dead end. Four generation skills have matching assignment odds and distinct nonfatal success benefits: evidence/reputation, diplomacy/trust, villain counterplay and rescue/supplies; individual memory testimony and clone-history UI add continuity. Tests now cover death/return, no-farm mission rewards, reprint save/restore and existing star-sign/episode compatibility. No new clone-art renderings or production deployment claimed. Further 100-person multi-generation art coverage, rendered phone/tablet/desktop QA and longer seeded ending/red-team playthroughs remain open under t-029; not For Human Gate.

Triage 2026-10-30 (verified on kind_robots main 0bb3088): 4-generation redshirt cloning saga with reprints, memorials and clone-rights endings via #4357 + #4374. Clone art is under t-008.
<!-- note:end t-029 -->

## t-030 — Space Couch opening constellation personality test and sign-exclusive quest arcs

<!-- note:begin t-030 -->
User direction 2026-10-27 PT: Start every fresh Space Couch voyage with three or four distinct personality choices. Reveal one of a complete original fictional constellation zodiac (e.g. Northern Sloth and Princess Mantic Shrimp), allow returning to change answers before accepting the result, then retain the assessment and sign with the captain's saved voyage. No silent skip, fixed sign by captain choice, real-world horoscope, or unrelated form-driven website UI. Provide story-rich sign-gated exclusive quest cards on the actual episode board so only captains with the corresponding matching sign see and resolve their quests. Choices alter flags, narrative and finale recognition, with seeded deterministic eligibility and replay/farming guards. Preserve old v1 saves, existing captain/crew selections, persistent clone saga and other currently active PR authors. Test all reachable signs, redo/accept boundaries, profile restore, cross-sign quest exclusion, gating, draw sequencing, and endings. No publication or human gate until final design and visual QA.

Four-question original constellation assessment and cinematic full-screen opening implemented in Kind Robots PR #4361. The twelve fictional signs include Northern Sloth and Princess Mantic Shrimp. All twelve are reachable through valid 4-choice responses; explicit reveal and keep/change answers gate captain/crew launch. Thirty-six sign-exclusive episodic quests (three per sign; chapters 1/4/7) persist world flags and earn separate constellation finale codas. Existing version-1 voyage saves remain valid. Concurrent clone saga PR #4357 was merged into the exact PR branch by a normal two-parent reconciliation commit, preserving clone features. Seeded gameplay, changed-file formatting, TypeScript and other CI passed; remaining contract/container checks pending, then PR may merge if green. Further rendered phone/tablet/desktop visual QA and bespoke constellation paintings remain future acceptance gates, not a human gate yet.

2026-10-27 PT: Merged Kind Robots PR #4361 on main with squash commit 5f5090dc0c974d4659366c6e8325ea4707b3e024 after 19 of 19 exact-head CI workflow groups passed at ff99c55aee79d027d50786464139c110005111ec. Original four-question cinematic Couchscope now gates first captain/crew selection, scores 12 valid original constellation signs, offers explicit reveal, retake and keep. Three sign-only quests per constellation create 36 unique episodes unlocking on chapters 1/4/7; choices, flags and complete/unfinished constellation codas persist in validated v1 saves. Reconciled concurrent clone-saga PR #4357 via non-forced two-parent merge; clone lab and generation bonuses kept intact. Master issue #4182 has details. No claim of bespoke generated constellation paintings or live deployed device rendering. Return READY for phone/tablet/desktop QA, missing artwork, adversarial whole-run polish and final design acceptance; not For Human Gate.

Built the Space Couch console opening and six origin choices before Couchscope, added saved settings and title-screen captain log, guarded new game replacement, illustrated each question with unique fallback art and painted-render slots, and made question layouts size to the available single-screen shell. Kind Robots PR pending verification; painted ArtJob IDs and rendered phone/tablet/desktop review remain open.

Merged Kind Robots Space Couch opening console PR #4375 on main (squash commit 34d79cb13d69ae0d7fddf659d506ba9b3fedd3e3) after all 17 of 17 exact-head CI workflow groups completed successfully on branch head 41afade83b7befcf0432da8cf2c74c30972e234b. Shipped opening intro title screen, Start New Game / Continue / Settings / Captain's Log, six independent persisted captain origins, four-question illustrated bounded-height Couchscope, four original SVG fallback plates and durable painted-art slots. Preserved simultaneous clone-saga work from PR #4374 through non-forced two-parent reconciliation. No painted Krea2/Arthemy ArtJob IDs, final WebP render deliveries or live phone/tablet/desktop device screenshots verified. Return task READY for paintings, real-device visual QA and adversarial full-run polish, not For Human Gate. Track art task t-008 and game master issue #4182.

Space Couch follow-up: refactored background, captain and crew onboarding to a bounded single-screen, art-backed personnel console. A six-per-page crew roster makes all 12 officers selectable without scrolling; captain and crew dossiers have paged story/stats/route content. Changes and seeded UI contract tests are on branch worker/space-couch-t030-personnel-console-4e83. Review CI before merging. Painted ArtJobs and live three-device visual acceptance remain outstanding.

Merged Kind Robots Space Couch PR #4388 on main, squash commit 744c0383f1a0a634e8d4bb8ced44904812300c20, after 16/16 exact-head CI workflows completed successfully on c5cc0fe091c09d75c83c190d9a9e78611a519114. Background, captain and crew selection now have no-scroll full-height art-backed personnel layouts; all 12 crew are reached in two six-officer pages; dossier story/route/skills views and primary actions stay in the fixed console. Live 390/768/1440px screenshot acceptance and delivery of painted Krea2/Arthemy Couchscope imagery remain outstanding; no ArtJob URLs verified. Reopen t-030 for those final acceptance tasks, not For Human Gate yet.

Image-first Space Couch captain and crew selector: full-size delivered portrait panels, always-visible statistics, crew choices confined to the opposite column, bounded mobile roster and content, retained 12-person pagination. PR branch: worker/space-couch-t030-image-first-5fe2. Artwork delivery and rendered 390/768/1440px acceptance remain outstanding.

2026-10-29 PT: Image-first captain and crew personnel console merged through Kind Robots PR #4467 (squash 867c084300efcfb8418e9e0d1b6cb1aa6264b464) after all 16/16 final-head Actions workflow groups passed, including TypeScript, Prettier, seeded gameplay, and full contract tests. The six existing captain and twelve existing officer portraits now anchor large responsive dossier figures; choices stay in the opposite column and four skill statistics are always shown. No saved-game or database changes. Continue t-030 for rendered 390/768/1440px visual QA and unverified new painted assets under art task t-008. Do not mark human-accepted or published.

Triage 2026-10-30 (verified on kind_robots main 0bb3088): Couchscope personality test with 12 signs and 36 sign-exclusive quests at chapters 1/4/7 (#4361). The 4 question images are SVG placeholders (t-008).
<!-- note:end t-030 -->

## t-031 — Space Couch: 101 absurd alien species, three-choice sightings, and escalating scrapbook oddities

<!-- note:begin t-031 -->
FROM GITHUB ISSUE silasfelinus/kind_robots#4592 (https://github.com/silasfelinus/kind_robots/issues/4592), opened by @silasfelinus on 2026-11-01. Imported by scripts/sync_github_issues.py. Reference the issue in the implementing PR (`Closes silasfelinus/kind_robots#4592`) so it closes on merge; the bridge closes it otherwise once this task is done.

## Direction (Silas, 2026-11-01 PT)
Space Couch needs a silly, low-friction **101-species Alien Scrapbook**. Discovery must be attached to ordinary solar-system, planetary, Serendipity, expedition and late-voyage experiences, with a reusable three-choice micro-encounter. **Never offer seven interaction options**: three distinct dramatic outcomes are the sweet spot. At least two routes can create the scrapbook record (e.g. an absolute-chaos accident and unexpected friendship); a third may cause the creature to flee. A failed encounter is funny, never punishing.

**101 species**: 12 zodiac/horoscope oddities, 24 two-Earth-creature mashups, 20 earth-creature + cosmic-condition hybrids, 20 emotional/social oddballs, 15 ecology/colony/symbiosis designs, 10 legendary exceptions. Intentionally vary age, size, mood, palettes, body plan, predator/prey, social arrangement, ecology, identity and habitat. Full-sized splash illustration for each species via traceable non-public ArtJobs. Art must appear in the collectible gallery, with dignified image-sized fallbacks while rendering.

**Sticky but merciful**: Some are hard to find, none require a pixel hunt or infinite rerolls. Seeded reproducible sightings, gentle rarity ramps/pity, discovery across voyages, clear hints and near-miss callbacks. At milestones (e.g. 5, 12, 25, 50, 75, 100) unlock genuinely new absurd encounters and world callbacks, not merely +1 counters. All three options have distinctive prose and an actual consequence.

## Implementation slices
- First: authored 101 catalogue and art slots, seeded encounter/discovery logic, 3-choice modal and reachable 101-card scrapbook, persistence across new voyages; start with illustrated pilot batch.
- Then: attach to episode decks and other genuine encounter families, server-backed user account persistence where available, complete 101 ArtJobs and verified URL/art delivery, milestones and rare species rules, seeded adversarial tests and browser QA.
- Keep separate final narrative + balance red-team and human acceptance gate; no public publication.

Creative baseline for future games: **three high-contrast choices with distinct tones, at least two paths to narrative reward, and collection growth that mutates the world**. Prefer memorable authored consequences over choice count or grind.

project:game-of-captains

Follow-up collector slice: six playable three-choice collection milestone incidents with 18 distinct endings, persistent incident decisions, future-galaxy rumors and scrapbook discovery affordance. Kind Robots PR will be verified and merged only after exact-head CI. Still not complete: 101 painted assets, account-based cross-device persistence, full 101 bespoke story polish and authenticated viewport QA.

Substantial alien collector slices merged to kind_robots main: #4594 101 described species/three hidden emotional choices, #4603 six independent playable milestones with 18 written outcomes, #4605 107 real ArtJob IDs with viewer-gated DONE ArtImage loading, and #4617 user-owned versioned scrapbook persistence with cross-device monotonic merge and guest isolation. Kind Robots #4617 exact-head CI passed 25/25 and merged as 1032cf80. Conductor #6927 corrected 101 blocked prompts and queued six event illustrations; 107 ArtJobs exist, all currently PENDING, no DONE ArtImages verified. Remains partial: production schema deployment verification, authenticated device/viewport QA, finished image reconciliation, 101 fully individual encounter stories, and final human design gate. Return to ready, not done; do not close source issue #4592.

2026-11-01 PT: Space Couch adversarial QA slice on worker/game-of-captains-t-031-qa7f2: isolate transient encounter/collector overlays and viewer-scoped alien art across account switches; fix false synced status on remote read failure; stress-test all 101 cross-device discoveries, stale replay and merge idempotence. Art remains independent and t-031 stays open for deliverables and authenticated browser QA.

2026-11-01 PT: Follow-up reliability slice landed as kind_robots #4619 (fa398f7); all exact-head workflows passed. Cross-account alien encounter and artwork isolation, offline first-account guest import and 101-species merge stress covered. The species-writing, image-delivery, and authenticated viewport QA portions remain agent-owned; return to ready, not done.

Zodiac narrative increment: 12 original species incidents and 36 distinct bond/chaos/retreat results, using the existing 3-choice matrix and v1 saved guide without changing data shape. Regression contracts added. Full 101-species art, encounter writing, authenticated responsive verification and final creative acceptance remain open; return to ready after the scoped app PR merges.

Zodiac narrative slice merged to kind_robots main via #4723 at 5ec5ac71, all nine exact-head workflows successful. Twelve encounters carry individual incident, three mood cues and three outcomes each, with preservation of deterministic and version-one scrapbook contracts. Remaining 89 species story coverage, art delivery and authenticated visual QA still open; continue agent writing.

Completed authored coverage for the remaining 89 alien lifeforms: 89 individual situations, 267 mood-specific clues and 267 individual consequences (623 distinct pieces), bringing the 101-species catalogue to full 101/303/303 writing coverage. The existing three-choice matrix, rarity, seed selection and saved account guide remain intact. Programmatic source audit found zero missing species IDs, zero duplicate species keys, zero duplicate prose, and no underlength story fields. Open a scoped kind_robots PR and verify exact-head tests; art and authenticated device QA remain separate.

2026-11-03 PT: Merged the complete 89-species writing expansion to Kind Robots main through #4728 at b1d00de193bd31dfe7cbafffe274f73e7ac1007e, all nine exact-head workflow groups finished SUCCESS. Together with merged zodiac #4723, all 101 species now have unique incidents, three mood clues and three outcomes (101/303/303). Source audit found no missing IDs, duplicate keys, duplicate prose, or short fields; seeded gameplay, saved guide, rarity and emotional-choice matrix unchanged. User still awaits verified art delivery, authenticated phone/tablet/desktop QA and independent narrative acceptance. Do not close #4592 or park at final human gate yet.

Playtest and fun QA slice: sourced the prior exact-head 2,116-voyage complete matrix and found five archetypes locked to one ending family each plus 1,497/1,728 balanced-style runs with empty holds. Fixed all 101 bespoke alien outcomes so generic emotional prefaces no longer contradict specific lore; added a five-persona, 25-complete-voyage plus three cross-voyage 101-species collector marathon verifier, registered to game tests and full adversarial workflow. Await exact-head CI for run results. Narrative confidence/fun gate remains separate from art delivery and human approval.

2026-11-04 PT: Merged scoped Space Couch adversarial fun QA as kind_robots#4749 at 99ba5a548a5508b5d9934ed9eb314081d7be9219 after all 11 exact-head workflow groups completed SUCCESS. Ran 2,116 seeded full voyages, 25 additional full persona voyages and three cross-voyage 101-species collector marathons: 19 voyages/151 contacts for greeting, 21/162 for cycling, 13/101 for hidden-mood oracle. Fixed repetitive contradictory mood prefaces for all 101 bespoke species; added durable test coverage. Editorial fun verdict about 7/10, caveats include agency mismatch between chosen action and bespoke outcome, 101-word encounter preambles, slow collector completion, ending family predictability and widespread endgame supply depletion. Findings linked on kind_robots#4592 and #4182. Art, authenticated viewport QA, causal-choice polish and human acceptance still unfinished, so leave this task ready.

Space Couch player-agency and pacing increment: six representative aliens from all six species families now have all nine distinct mood-by-actual-choice written outcomes (54 authored causal scenes); keeps the original fair 3x3 matrix, saved scrapbook and species rarity. All 101 alien initial encounters remove repeated appearance/field-guide/callback scaffolding, keeping the authored problem and mood clue; prior same-family reports still live in the scrapbook and the collector radio milestones remain. Added regression checks for all 54 action branches, canonical species keys, nine-way coverage, unique scenes and average first-sighting reading budget, then re-ran prior full-voyage and collector test registration. Kind Robots PR to open and exact-head CI pending; remaining 95 species need action-specific review, art and authenticated UI QA remain open.

2026-11-04 PT: Merged Space Couch causal-choice and pacing improvement as Kind Robots #4753 at 68f4fa7399f857c7f498951764a09b95f85010b1; all nine exact-head workflow groups passed, including full 2,116-voyage matrix, 25 persona voyages and three 101-species collection marathons. All 101 introductions were trimmed from a verified 101-word mean to 52 words without sacrificing original dilemma/mood clues, and six creatures across all six families have 54 authored mood-by-actual-action outcomes. Saves, 3x3 hidden choices, rarity and collector counts remain identical. Leave 95 species action-causality coverage, ~19-21-voyage collector grind, endings and resource balance, unverified art/image/device QA and human acceptance open. Do not close source issue #4592. This event omits a manually guessed UTC timestamp so the processor can stamp actual time.

Completed all 95 remaining alien story records across zodiac (11), hybrid (23), cosmic (19), social (19), ecology (14) and legendary (9). Each records three original things the captain can actually do, three original mood interpretations and three outcome-specific consequences; the canonical Latin-square yields 855 unique action-by-mood narratives. The six full-form pilot encounters remain unchanged, bringing coverage to 909 unique alien paths across 101 species. Automated source audit confirmed no missing species, duplicate IDs, duplicate authored beats, undersized lines or missing player-action verbs. Added exact nine-way coverage regression. App PR and exact-head gameplay/format/type/contract CI remain to verify; retained save schema, rarity, choices and six collector milestones. Art, responsive live QA and human acceptance remain separate unfinished work.

2026-11-04 PT: Merged kind_robots#4760 at de69fbc5f79697be56a6276f31b005b279973a73 after all nine exact-head workflow groups completed SUCCESS. Completed action-specific stories for the remaining 95 species, with three original captain actions, three mood interpretations and three species outcomes per creature, combined into 855 unique branches. Along with the prior six full-form entries, all 101 alien species now have 909 unique mood-by-action outcomes. Source audit: zero missing IDs, duplicate entries, duplicate text or undersized beats. CI verified 101/101 species, 909/909 unique outcomes, saved scrapbook contract, hidden rock-paper-scissors balance, six milestones, full 2116-voyage matrix and collector/persona playthroughs. Original art queue and delivery, authenticated responsive art checks, human acceptance and collector grind/balance polish remain open; return task to ready, do not close kind_robots#4592. No ArtJobs submitted or production deployment performed.

2026-11-04 PT: Near-miss mercy slice opened as silasfelinus/kind_robots#4771 (head
266c2df on main 050b23e, unmerged). Escaped aliens now really do return. An unrecorded
runaway comes back on an even-numbered sighting after a different creature; odd
sightings keep the rare/legendary cadence. It returns with a short callback naming what
the crew tried. A second getaway still files a blurry near-miss record, and the
scrapbook names escaped species with a near-miss hint. Collector marathons: greet 19 ->
18 voyages, cycle 21 -> 18, oracle 13; every first escape returned once, longest wait 8
sightings; average scene words 52 -> 57. Save schema, 909 branches, rarity and
milestones unchanged. npm run test:game-of-captains passes all 20 files; strict tsc and
prettier clean. Open: art delivery, authenticated viewport QA, human acceptance, and
Silas's balance call on the blurry-record rule. Do not close #4592. Merged as
kind_robots #4771 (squash 0af1dad); back to ready for polish, species plates, device QA
and acceptance.

Silas, 2026-11-04 PT, in session: "Space couch two encounters give blurred is fine." The
blurry-photo record for a runaway that escapes twice (relaxing the two-of-three-choices-
record rule for returning runaways only) is accepted as designed.

Verified the original alien-ledger curation held 20 species and two milestone paintings. The original 22 rejected ArtJobs were still in the runtime mapping. On app branch worker/game-of-captains-t-031-alien-curation-20261119T044345Z-r8v5, removed those rejected jobs from viewer delivery, retained 85 curated original jobs, recorded 22 DONE redo candidates (ArtJobs 60625-60646, ArtImages 262131-262152), and added a regression test for complete coverage and review holds. Redos are not certified without actual pixel review; the existing fallback stays. CI pending.

Scoped safety fix quarantines 22 rejected original alien plates and holds 22 completed redo candidates for visual curation. Exact-head CI and PR review pending; t-031 is not done.

2026-11-18 PT: kind_robots PR #5333 merged at 4af5104 after nine exact-head Actions workflows completed success. Quarantined 20 rejected original species plates and two rejected milestone plates, retaining 85 approved mappings and 22 DONE redo candidates (ArtJobs 60625-60646) on review hold. Partial safety fix only: authenticated image URLs, visual curation, and responsive delivery still unverified; do not mark t-031 done or restore rejected originals.

2026-11-18 PT: Kind Robots PR #5333 merged at head 9be772479df783edd9952ce9c33a50f42d8c7afb; ten exact-head workflow runs completed successfully. Quarantine of 20 original species and two milestone plates remains intact. The 22 DONE Krea2 redo candidates (ArtJobs 60625-60646, ArtImages 262131-262152) are not visually accepted; authenticated URLs and creature anatomy remain unverified. This is READY partial, not DONE. Next independently inspect candidate images and promote only approved replacements.

Scoped visual-curation delivery path: authenticated curator-only registration of 22 ledger-pinned DONE alien redo candidates into unselected ArtSlots, plus liked-and-selected runtime overrides under existing viewer access checks. No candidate autoaccepted, no rejected original restored. App worker branch and exact-head PR CI are pending. This is PARTIAL t-031; original pixel acceptance and authenticated media checks remain open.

Merged Kind Robots PR #5422 as 708a0f8c893dead1bf31f897f9dfc2feefbb7bba, after all 12 exact-head Actions workflow groups completed SUCCESS including TypeScript, formatting, four contract shards, and Space Couch full adversarial voyages. Added curator-only registration of the 22 known DONE Krea2 alien redo candidates (ArtJobs 60625-60646; ArtImages 262131-262152), an admin Art Slots review entry, and liked-plus-selected runtime delivery respecting existing viewer image permissions. Rejected originals remain quarantined, and none of the 22 candidates were autoaccepted. This is PARTIAL t-031: physical pixels, authenticated image URLs, 390/768/1440 viewport QA and final visual curation remain unverified. Keep t-031 READY and source issue #4592 plus master #4182 open, no human approval.

Scoped partial alien scrapbook navigation upgrade: show recorded, escaped, and unseen counts with a four-mode filter, searchable known-name and stable catalogue-number index, private hidden species names, and useful empty states. Source and static Vue contracts plus regression cases added in Kind Robots worker/game-of-captains-t-031-scrapbook-shelf-b4e9. Original image curation, authenticated asset delivery, and 390/768/1440 live viewport QA remain open; t-031 is review partial, not done.

2026-11-22 PT closure. Alien art curation finished: of the 22 earlier redo candidates, 8
were accepted in Kind Robots Art Slots (liked + selected) and 14 that were still
ordinary Earth animals were re-rendered as true hybrids in CURATION-REDO-2, reviewed
full-size and kept, then linked through COUCH_ALIEN_ART_IDS (ArtImages 278518-278531) in
kind_robots #5553 (b6d4d05, all checks SUCCESS). Live alien-art endpoint already served
93 keys; the 14 missing keys are exactly those added, so all 107 alien art keys (101
species plus milestone plates) resolve after deploy.
<!-- note:end t-031 -->

## t-033 — Curate, re-render and ship the 100 redshirt portraits and secret-power plates

<!-- note:begin t-033 -->
Silas, 2026-11-02 PT, on the Forge's 100 Redshirts page showing 0 portraits: "do we still have redshirt art gens to do? ... yes go ahead". t-025 submitted all 200 cells on 2026-10-27 but no task owned review or delivery, so nothing reached the game. 2026-11-02 review of REDSHIRTS-200-ROUND-1 (195 DONE, 5 cancelled): keep 20 of 98 portraits and 39 of 97 power plates (verdict on every subject); nearly every miss is an ordinary human in the tunic, because the prompts led with a human name and asked for "the person ... individual face". REDSHIRTS-ROUND-2.yaml (auto_submit, 141 cells, all pass the live contract) re-renders the misses and the five cancelled cells creature-first. The 59 keepers ship to public/game-of-captains/redshirts/{portraits,secret-powers}/rs-NNN.webp, listed in WARP_ART, and the Forge redshirt page falls back to them. Next: curate ROUND-2 the same way, export keepers, then wire the portraits into the dispatch board (t-026 family) when it lands. Done when every rs-001..rs-100 has a shipped portrait and plate. 2026-11-11 PT: curated all 141 ROUND-2 renders on contact sheets. Kept 57 of 80 portraits and 60 of 61 plates. Portrait misses: 13 with a large gold arrowhead chest badge that reads as a franchise insignia, 7 ordinary animals or no creature, 2 near-human faces, 1 literal soft-drink trademark can; plate miss rs-007 (an ordinary dog). Shipped totals 77/100 portraits, 99/100 plates; the daily console's personnel cards now show the portrait when one has shipped (kind_robots PR follows #5026 on the session branch). REDSHIRTS-ROUND-3.yaml (auto_submit, 24 cells, 24/24 pass the live contract) re-renders the misses with an explicit ivory sofa-silhouette chest badge and 11 re-described creatures. Next: curate ROUND-3 and export keepers.
2026-11-11 PT: merged kind_robots#5028 as ef67f9da2826c334392b19aa21816ae12d217d04 after all 14 exact-head checks passed: 117 round-2 keepers shipped (77/100 portraits, 99/100 plates) and redshirt portraits now show on the daily console personnel cards. REDSHIRTS- ROUND-3.yaml (24 cells, auto_submit) is on main and awaits rendering. Back to ready: next session curates ROUND-3 on contact sheets (reject gold arrowhead chest badges, ordinary animals, human faces, trademarks), exports keepers with export_round_art.py --only, and closes when rs-001..rs-100 all ship both images.

2026-11-19 PT: scoped redshirt art delivery integration on worker/game-of-captains-t-033-curated-redshirt-slots-j8q4. The game's daily personnel deck now reads curator-selected ArtSlot images from a dedicated guest-safe endpoint, retaining the existing static portraits and glyph fallback on missing or broken URLs. An exact selected candidate MUST have verdict liked and its ArtImage must be public, active and non-mature. DONE ArtJobs are never autoaccepted; 24 uncurated Krea2 round-three cells and missing source WebPs remain REVIEW HOLD. Pure parser and source-level safety regression added to the seeded test suite. Await exact-head CI, manual rendered image review, and authenticated delivery checks; this is partial t-033, not DONE or human approval.

2026-11-19 PT: Kind Robots PR #5387 merged to main as a45ae0501aa77bca0358447429d1352f36136afb after all 14 exact-head GitHub Actions workflows completed SUCCESS, including TypeScript, seeded gameplay, full Space Couch adversarial voyages, image privacy regressions, PR-only container validation, and all four Contract Tests shards. Introduced publicly readable liked-plus-selected ArtSlot runtime art for redshirts with shipped-file and glyph fallback, plus 24 immutable DONE round-three ArtJob/ArtImage references and an explicit curator-only, idempotent registration action in the Forge. No render auto-liked, auto-selected or auto-published. The existing 77/100 shipped portraits and 99/100 plates remain; 23 new portraits and one plate are still unreviewed candidate renders. Actual source-image pixel acceptance, authenticated media URLs, and final shipment are unverified. Return t-033 to READY (partial), not DONE; no human approval implied. Replayed after unrelated emperor-of-dust roadmap duplicate-key repair.

Scoped redshirt review UX fix committed as app 04fe607: Forge links to the exact game-of-captains/redshirts/ ArtSlot set, with single-candidate slots visible instead of hidden by the default multiple-only filter. Added regression assertions. This is a PARTIAL t-033 implementation; 23 portraits and one power plate are still unapproved, and authenticated final image delivery remains unverified. Await PR and exact-head CI, then return this nonrecurring task to READY unless real artwork is independently accepted.

PR #5446 repairs the Forge redshirt curation link so 24 candidate slots appear even with one render. Artwork remains unapproved pending visual and authenticated delivery verification.

Partial: PR #5446 fixes redshirt curation deep-link, including single-candidate slots. Await exact-head CI and merge; 23 portrait renders and one secret-power plate still require actual visual acceptance and authenticated delivery before t-033 can be done.

Scoped t-033 runtime art delivery safety fix on worker/game-of-captains-t-033-curation-scope-s9d2: only art slots genuinely owned by game-of-captains (or legacy canonical null-project slots) may override redshirt images; deterministic canonical-over-legacy precedence with public, liked and active fallback. Added ownership, order, legacy and source-contract regression tests. This is partial, not actual curation. 23 portraits and one power plate still require pixel-by-pixel original image acceptance, shipped URLs and responsive browser QA. No rendered asset was autoaccepted, and task t-033 must return to ready after merge.

Kind Robots PR #5482 merged to main as 0d422b75df3f515f655587a1b5c39e2b3ad4f9f9 with all 12 exact-head workflow groups successful. Redshirt ArtSlot ownership and canonical/legacy precedence are guarded, with regression tests. Partial t-033: 23 portraits and one secret-power plate still need original image curation, accepted delivery, authenticated URLs and responsive verification. Return READY, not DONE.

Partial delivery verification increment: a deterministic 200-file redshirt WebP audit and three regression tests are in a scoped Conductor PR. Original-image visual acceptance and missing asset exports remain outstanding; do not mark DONE.

2026-11-22 PT closure. All 24 round-3 redshirt cells are curated and shipped: 17 kept
from REDSHIRTS-ROUND-3 (16 portraits plus the 100th secret-power plate) in kind_robots
#5548, and the 7 rejects (near-human faces, franchise-style delta insignia, ordinary owl
and bat, empty uniform) re-rendered in CURATION-REDO-2, kept and shipped in #5553.
WARP_ART now lists 100 portraits and 100 power plates; the guard test requires exactly
the curated keepers to ship.
<!-- note:end t-033 -->

## t-034 — Space Couch editorial readability pass: rotating transit prose, 30 success returns, sectioned final log

<!-- note:begin t-034 -->
Silas, 2026-11-04 PT, in-session: finish up Space Couch and assess text quality, mission uniqueness, fun, clarity, diversity of playthroughs and stickiness. Assessment: projects/game-of-captains/EDITORIAL-ASSESSMENT-2026-11-04.md (240-voyage scratch harness plus the 2,116-voyage matrix). kind_robots#4755 adds seeded no-repeat connective prose pools (within-voyage repeated sentences 34.4% -> 16.2%), a plain-success return for each of the 30 calls, rotating casino/bar reactions and plural fixes, plus optional endingSections rendered as labelled ending parts with the raw log collapsed. v1 saves remain compatible. Local game suite, vue-tsc, eslint and prettier pass; ending block checked as a CSS mock at 390/1280 px only. Merge when exact-head CI is green, then set done. Seeded default route split to t-035.

2026-11-04 PT: Merged kind_robots#4755 as fdbab276d158b5bfc0484ef42073ad3461c1b39a after all 16 exact-head checks passed, including the full captains/antagonists/crews/endings matrix, TypeScript, four contract shards and production image build. Hydrated ending screen still unverified until the next Force Update; next is t-035.
<!-- note:end t-034 -->

## t-035 — Seeded pre-charted route for chapters 2-9 and reachable destination ending families

<!-- note:begin t-035 -->
2026-11-05 PT explicit human handoff: the previous claim `2026-11-05T224212Z-game-of-captains-t-035-r6` had no open Kind Robots/Conductor PR, game feature branch, or pending task event after 68 minutes. Silas explicitly directed pickup. Transferred the same claimed task to `20261105T235000Z-game-of-captains-t035-human-handoff-79f2` by exact-SHA compare-and-swap, preserving all prior work and notes. This is an intentional single-claim takeover, not a second competing claim.

From EDITORIAL-ASSESSMENT-2026-11-04.md. The route board always pre-charts VOYAGE_BOARDS[ch][0], so a captain who accepts the default flies refugees -> archive -> bar ... on every seed (22 distinct nine-chapter sequences in 228 voyages), and the six destination ending families (Sanctuary Without a Map, Names on the Hull, Unlicensed Cure, Right to Refuse, A Table for Every Guest, Courtesy Accord) were reached 0 times in 240 mixed voyages. Keep chapter 1 on The Last Lifeboat; pre-chart a seeded call from missionBoard(run) for chapters 2-9 (prototype: rules.ts chartedCall used from nextDestination). The 2026-11-04 prototype broke pinned assumptions in verifyGameOfCaptains (report missionId == board[0]; synergies), AuthoredExpansion/AuthoredRemainder (concord-intake expected), ActThreeOpening, Scarcity (57 vs 60 authored scenes) and Traces (pinned ending per captain); re-pin those deliberately via the harness `chart` driver rather than weakening them. Then audit each destination family's earned() gate against real reachable flags and add a pinned trace per family.

Seeded route diversity increment: after chapter one, nextDestination now chooses a reproducible mission among the actual eligible missionBoard offers, including prior world choices, crew and captain, without mutating saved missionId. The player may always override before travel. Added 42 complete seeded real-voyage tests for route variety, saves, chapter-by-chapter reachability and manual override. Existing trace and authored-case tests now explicitly chart their fixed legacy story routes rather than assuming an always-first default. Implementation branch worker/game-of-captains-t035-seeded-routes-9c72, PR and exact-head CI pending. Destination ending family organic reachability and verified browser/art QA remain separate independent acceptance.

2026-11-05 PT: The seeded eligible-route fix landed in Kind Robots PR #4767 (squash 0eca96cd577a0762004d1b85d136206c56c94870), with all exact-head check groups passing, including the 42 full-voyage default-route tests, canonical gameplay suite, and full adversarial voyage matrix. Our implementation branch was deleted after merge. The original t-035 claim remained in review; releasing it to ready because destination-specific earned-ending organic reachability and balance are not yet independently measured or proved. Do not mark the destination-ending milestone done or infer human acceptance from the route fix. No production DB changes or new ArtJobs.

2026-11-05 PT: Silas expressly asked us to resume this stalled claim. Scoped follow-through implementation: the route planner now favors eligible world-specific sequel calls from actually earned flags, while retaining a seeded chance to choose other missions and always allowing manual charting. Five destination threads have authored reminders in the briefing and visible return-call labels on mission cards. The Archive's consent and Hollow Lantern rescue now unlock the corresponding foundry and Windglass follow-ups even without specific crew, without weakening any other eligibility or save requirements. Expanded 42-voyage seeded regression for continuation weighting and chart override; preexisting six-family full-voyage trace suite remains the earned-ending acceptance gate. App branch worker/game-of-captains-t035-earned-threads-79f2; CI and PR pending. No deployment or human acceptance claimed.

2026-11-05 PT: Human-authorized takeover complete. Merged Kind Robots #4838 at 6c7ef368c3113e01958f8744727f529dcda24746 after all 9 exact-head workflow groups succeeded. The existing six destination-ending families retain real player-driven pinned full-voyage traces for all captains, and 2,116 adversarial voyages passed. Seeded chart now favors earned sequel calls without forcing them; the Archive consent and Hollow Lantern rescue properly unlock their follow-up stories, and the image-led mission cards identify earned RETURN CALLs. Dedicated 42-voyage default chart regression passed with 40 distinct routes and 27 missions, preserving manual override and save replay. All scope of t-035 is complete; route-specific ending families still require deliberate choices rather than blind default policy, by design. Art/viewport review and final human acceptance belong to their own tasks. No deployment, database migration, or new ArtJobs.
<!-- note:end t-035 -->

## t-036 — Endgame supply balance: the hold should not run dry on ordinary voyages

<!-- note:begin t-036 -->
Silas, 2026-11-04 PT: "Space couch has a supplies issue, tweak it." Found by the 2026-11-04 game sprint (t-031 assessment): in the persona playtests the hold runs out of supplies by the end of 5/5 voyages for 3 of the 4 persona styles that run alien contacts; only the chaos captain avoids it. Tune the supply economy (income, costs, alien-contact drains, or a fair recovery path) so ordinary careful and kind play finishes with a thin but non-zero hold, scarcity still bites for reckless play, and pin the curve with a seeded persona battery. Do not break saves.

2026-11-04 PT: supply tweak in kind_robots #4782. Alien contacts never touched the hold;
the base voyage cost ~15/voyage in upkeep against 12 income. Now one supply refills the
whole force bubble and good returns bring crates home (flawless +2, success +1). Voyages
ending stocked: cautious 0/24 -> 18/24, completionist 0/24 -> 13/24, reckless 0/24 ->
5/24, skipper 0/24 -> 3/24, chaos unchanged 24/24. Seeded battery pins the shape.

kind_robots #4782 merged (squash f074838); CI green, seeded persona battery pins supply curve. Reviewer merge.
<!-- note:end t-036 -->

## t-037 — Show the supply swing on the mission report card (e.g. SUCCESS - +1 SUPPLY)

<!-- note:begin t-037 -->
Implemented exact actual supply swing on the Space Couch mission report, including featured consequence missions and an empty-hold regression test. App PR and checks to be verified; this is not the whole project's playtest handoff.

Merged kind_robots PR #5083 at d5a17a2ef4e7b1944cfd43d62e706161b35ebceb. The mission report now shows actual supply swing, using an exact recorded delta with an old-save fallback. Verified completed green on formatting, TypeScript, layout, Playbook Kit, architecture, schema, gameplay slices, contract tests and full Space Couch adversarial voyages (nine CI runs). Production is self-hosted and this merged commit is not independently confirmed deployed.
<!-- note:end t-037 -->

## t-038 — Space Couch comedy and freshness pass: rotate the stock lines every voyage repeats

<!-- note:begin t-038 -->
Silas, 2026-11-11 PT, in session: "Work on space couch. Update and follow roadmap, submit art as needed, and generally work on improving text, uniqueness of adventures, and humor." A 36-voyage seeded probe (varied captains, crews, orders) found 236 sentences that appear in at least half of all voyages, so a returning player rereads the same jokes. The worst offenders are the 15 fixed deck-card setback lines (episodeConsole PLOT_SETBACKS), the crew-errand stock lines in rules.ts ("The crew makes an entrance that will be difficult to apologize for", "The first explosion is still visible from orbit"), the fixed constellation-quest suffixes, and the small transit pools (9-12 lines each, nine used per voyage). Scope: rotate those into larger seed-selected pools with sharper, more specific comedy; pin a cross-voyage freshness metric in a test. Done when the probe's half-of-voyages count falls by at least half with the full test:game-of-captains suite green and saves unchanged.
2026-11-11 PT: kind_robots#5026 (review). New freshLines.ts pools rotate deck setbacks (15 -> 90 lines), crew-errand entrances/aftermaths/callbacks, constellation codas, mission-order replies, act openers and the finale line; every transit pool grows to 20 (waiting days 26); 8 new casino incidents (16 total, no repeat inside a voyage). Seeded 36-voyage probe: sentences in two-thirds of voyages 169 -> 39 (pinned <=60 by verifySpaceCouchFreshness.test.ts), in >=30/36 96 -> 21, in half 236 -> 138 (remainder mostly structural: system names, mission titles, status lines). In-voyage repeats 13.9% -> 10.5%. Full test:game-of-captains green locally. Kaizen: planet-deck success beats are flat one-liners; give the 10 planet cards specific funny success beats next.
2026-11-11 PT: merged kind_robots#5026 as a7ae88443971efe186fed71bf668fd8438d39405 after all 16 exact-head checks passed (TypeScript, Prettier, 4 contract shards, seeded playthroughs, all-captains/antagonists/endings matrix, playbook kit/forge, layout contract, production image build). No deploy, migrations or ArtJobs. Follow-up worth a task: specific comic success beats for the 10 planet cards.
<!-- note:end t-038 -->

## t-039 — Space Couch planet deck: give each of the 10 planet cards specific comic success beats

<!-- note:begin t-039 -->
From t-038 (2026-11-11 PT, kind_robots#5026). The planet card is drawn every chapter, and its success text is a short civic summary ("Tenants negotiate a public gravity guarantee.") that reads the same in every voyage (~20 of 36 seeded voyages per line). Write a specific, funny success beat for each card x order (10 cards x 3 orders), in the deadpan procedural couch voice, keeping the ethics of each order (ask = locals decide, document = the record stands, override = it works and costs consent). Keep the existing line as the first clause so saves and pinned traces stay valid; extend verifySpaceCouchFreshness.test.ts.

Authored 30 distinct second-beat planetary successes (ten cards times ask/document/override), preserving each original opening clause and its consent/record/intervention distinction. Added a deterministic freshness contract for all thirty paths in kind_robots. Implementation commit ce4bd2d730d325ee1df2ff9cddbc2f8bedbb64cd; exact-head CI pending.

Merged kind_robots PR #5329 as 98eb60873100b84f314a619413d4eff04a0be2b0; nine exact-head GitHub Actions workflows completed successfully on 6736ac4c85e86d3e2abbac08e76712beac7789ec. All 30 planetary success beats delivered without changing initial save-compatible clauses.
<!-- note:end t-039 -->

## t-040 — Space Couch achievement upgrade: 12 or more live achievements

<!-- note:begin t-040 -->
Silas 2026-11-11 PT, in session: "Our games should all have a base standard of quality ... We want our main games to have 12 plus achievements." Standard: docs/agents/main-game-standard.md; CONTROL.md global overview.

Live today: 0 Achievement record(s) with this game's triggerCode prefix (checked against /api/achievements 2026-11-11). Target 12+ (usually 12-30; tie some to endings but don't go overboard). Mix story, skill, discovery and completion. Create the live records through the existing achievements API (label, message, icon, karma, triggerCode prefixed with the game slug), award them from the game store, show them with components/achievements/game-achievement-strip.vue, and verify one award live after deploy.

Achievement upgrade merged in kind_robots#5054 (d74a7dc), all checks green: 17 live achievements, endings via recordKitUnlocks; also added the shared Playbook Kit achievements pane. Not wired: High Roller (casino has no win state) and Every Captain's Chair (no cross-voyage record yet). Catalog seed succeeded.
<!-- note:end t-040 -->

## t-041 — Main-game standard: audit and close the gaps for Space Couch

<!-- note:begin t-041 -->
Silas 2026-11-11 PT, in session: "Our games should all have a base standard of quality ... We want our main games to have 12 plus achievements." Standard: docs/agents/main-game-standard.md; CONTROL.md global overview.

AUDIT DONE 2026-11-12: projects/game-of-captains/STANDARD-AUDIT-2026-11-12.md holds the Met/Partial/Missing table, a proposed achievement list with award points, character-fit notes and the three smallest next PRs. Start there.

Start with the audit table from docs/agents/main-game-standard.md (title screen; settings menu; save/load and persistent progress; 12+ achievements; scrapbook; multiple endings with painted plates; customizable characters; 3+ replay hooks), marking each Met / Partial / Missing with evidence (file, route, live record). Put the table in this note and the first PR. Then close each gap in small CI-tested PRs; queue any needed ending, scrapbook or portrait art in an auto_submit ledger.

Item 7 (customizable characters) applies "in most cases": if this genre makes it a poor fit, say so in the audit with the reason and leave it for Silas rather than skipping silently.

Achievements are tracked by their own task; this one covers everything else.

2026-11-15 PT daily-delivery:2026-11-15/space-couch-share-card | PR:
silasfelinus/kind_robots#5209 (merged c24cef2, CI green) | /play/game-of-captains now
unfurls with a designed 1200x630 Space Couch card (public/game-of-captains/link-
preview.webp) instead of the untitled splash; verifyGameLinkPreview.test.ts pins it.
Main-game audit itself still open.

2026-11-19 PT scoped main-game standards pass on worker/game-of-captains-t-041-20261119t2251-r7q9: title (Partial: Achievements button and live strip implemented pending CI); settings (Partial: title and Kit still split); save/load (Partial: local v1 voyage, account-backed alien guide only); achievements (Partial: 12+ catalog code, live award/API unverified); scrapbook (Partial: species, moments and endings, no completed voyage pages); multiple endings (Partial: paintings incomplete); characters (Met: captain, crew and origin choices); replay (Met: constellation, randomized episodes, collectible aliens and branching). This is the first small PR for title Achievements access; more t-041 work remains. Never close as done from this slice.

2026-11-19 PT: Kind Robots PR #5359 merged as 05a100315ab9c15ac5e9115f20ef84116703d77d. Seven of seven original exact-head workflow groups completed success, including all four contract shards; title Achievements access and existing global award display landed. Partial t-041 only. Remaining: persistent finished-voyage log, unified settings, save compatibility and delivery/visual acceptance.

2026-11-19 PT: next scoped t-041 improvement on worker/game-of-captains-t-041-voyage-ledger-k8p5. Added versioned and bounded completed-voyage archive with dedicated localStorage key, final-run dossiers covering captain, selected crew, decisions, losses, ending prose, saved log and play dates, plus safe v1 restore/duplicate handling. Existing voyage v1 save key and stable game identifiers unchanged. Added source and deterministic contract tests. Implementation PR, exact-head CI and merge pending. This is a partial standard improvement; settings, account-save checks, ending plates, visual QA and final t-041 are not complete.

2026-11-19 PT: Kind Robots PR #5363 merged as 3d5e54bdd09df54c0c8dd0ba0da5ccc9542afcab. All ten latest exact-head PR workflow groups completed success, including the full Space Couch adversarial voyages and all four Contract Tests shards. The completed-voyage archive records every finished run (captain, crew, outcomes, mission and consequence choices, fallen redshirts, final text and log) without changing the active v1 save key. Restored v1 completed runs backfill; duplicate, malformed-record and no-eviction regressions covered. Task remains partial: unify title/in-game settings, account-backed voyage saves, verify live 12+ achievements and delivered ending art/viewport checks; no playtest handoff yet.

2026-11-19 PT: scoped main-game quality slice on worker/game-of-captains-t-041-shared-settings-m5v7. Title screen now mounts the same PlaybookKitSettings panel as the in-voyage settings tab. Existing Space Couch largeText and reducedMotion flags are migrated on the first Kit save only; an existing saved Kit preference always wins, unreadable legacy data does not destroy Kit or voyage data, and the legacy key is never removed or rewritten. Visible typography/motion and opening reels read reactive Kit-derived settings. Deterministic test covers migration mapping and source wiring. CI, PR and visual QA remain to verify. t-041 remains PARTIAL after merge: account voyage sync, original paintings, live achievement awards and 390/768/1440 visual evidence remain.

2026-11-19 PT: Kind Robots PR #5368 merged into main as 98bec1780a071b1b3fdbc971c2f79e16a57136d1 after all nine exact-head GitHub Actions workflow groups COMPLETED/SUCCESS, including all four Contract Tests shards, Playbook Kit, TypeScript, layout, seeded gameplay and the full Space Couch adversarial voyages suite. Title Ship Settings now reuses the Kit settings sheet and same reactive text/motion preferences as the voyage. Legacy largeText/reducedMotion flags import only on a missing Kit save; stored Kit settings always win, old preferences remain untouched, and existing v1 voyage save keys and stable game IDs are unchanged. This is PARTIAL t-041 closure; remaining authenticated voyage/achievement records, real rendered painted ending URL checks and 390/768/1440 browser QA remain. No human approval implied.

2026-11-19 PT agent-owned main-game standard slice: implemented a reversible, versioned JSON backup for Space Couch current v1 voyage and finished-run history, accessible in Captain's Log. Explicit user-controlled import preview and confirm before replacing an active run; duplicate-safe completed-run merge; corrupted, oversized or wrong-game files rejected. Existing voyage save key, game slug and account-owned guide/achievements remain untouched. CI/PR and browser evidence pending. This does not assert authenticated cloud saves, original art approval, mobile QA or playtest DONE.

2026-11-19 PT: Kind Robots PR #5378 merged into main at a4de97d2e954c64926781b5c52653eb572b42734; all nine exact-head workflow groups completed SUCCESS, including TypeScript, Playbook Kit, formatting, seeded gameplay, the full adversarial Space Couch matrix and four contract shards. Added a user-controlled versioned JSON backup of active v1 voyage and completed-run history, staged import validation, explicit replace confirmation, duplicate-safe merge and rollback on failed storage writes. Existing save keys and account-owned achievement and alien-guide data preserved. Remaining t-041 scope includes authenticated cloud-save verification, real rendered art and viewport checks, not human subjective approval. Return to READY (partial), never DONE for this slice.

Scoped achievement threshold bug fix: collector badges now award only when a threshold is crossed, with regression tests. This is partial t-041, not completion.

Kind Robots PR #5391 merged as e0e535259aa6b60c3c0a6df7ed11cc2fae27e5ea; all nine exact-head workflow groups completed success. Alien collection achievement milestones now award only upon threshold crossing, with regression coverage. This is a partial t-041 improvement; art delivery, authenticated visual QA and final main-game standard remain unfinished.

Scoped replay-dossier fix in Kind Robots: retain distinct choice paths for same-seed same-ending replays, preserve legacy IDs, add regression coverage. Partial t-041; art and full readiness still open.

Reconciled stale review after prior scoped replay-dossier PR #5398 merged as a642f737. There is no open t-041 implementation PR or branch, and the task remains PARTIAL. Account-backed voyage saves, authenticated achievement/art delivery, viewport QA, and final main-game standard are still open. Return to READY for active follow-through, not DONE.

Submitted Kind Robots PR #5430 implementing private per-account Space Couch voyage backup with strict versioned payload validation and additive schema, optimistic revision-conflict rejection, explicit account inspect/save/stage-restore actions in Captain's Log. Existing v1 device saves, alien guide and achievements are untouched. Awaiting all exact-head GitHub Actions workflow groups before safe merge. This is PARTIAL main-game standard; authenticated production database, rendered paintings and viewport QA remain unverified.

pr-medic 2026-11-20: kind_robots#5430 (account voyage backup/restore slice) merged green
after replacing a temporary CI generate step with checked-in prisma generate output and
resolving main conflicts. Additive-only migration (CREATE TABLE SpaceCouchVoyageSave).
Partial slice: t-041 stays ready for remaining save/load and verification gates per the
PR.

Old review claim from 18:51 UTC had no new task activity; account-save PR #5430 and prior main-game standard slices are merged. Remaining authenticated browser, art and viewport standards are NOT done. Return to READY for the next worker, preserving prior contributions.

Scoped recovery fix in app commit 4132e315: a failed Space Couch backup import now restores both prior browser save keys, including writes that mutate before throwing; reports when rollback itself fails. Added functional failure-injection regression tests. This is PARTIAL t-041 only; signed-in server backup, art delivery, responsive/browser checks and master handoff remain unverified. Await exact-head CI and safe PR merge, then return READY, not DONE.

Kind Robots PR #5460 merged at bdbfc0e9a91dff37ee708a092ce5f64bc5ac4237 on 2026-11-20 PT after all nine exact-head gameplay, contract, typecheck, format, layout, schema and Space Couch adversarial workflows completed SUCCESS. Backups now roll back both browser save keys after partial writes, with failure-injection regression checks. PARTIAL t-041 only: authenticated browser restoration, art verification and 390/768/1440 QA remain. Return to READY; no human approval claimed.

Partial main-game QA: the scheduled real-browser responsive audit previously omitted /play/game-of-captains and lacked the required 768px tablet sample. Added Space Couch to the daily route sweep and the targeted 768px path alongside 390/1440 with a regression test. Implementation branch worker/game-of-captains-t-041-responsive-audit-20261120-f3a9. Review/merge after exact-head CI; still needs deployed screenshots, authenticated account/achievement/painted-art checks. Keep t-041 READY after partial merge, not DONE.

Partial main-game-standard backup reliability repair. App branch worker/game-of-captains-t-041-backup-race-20261121-7b9e protects asynchronous file selection from stale reads, invalidates cancelled/account-switched staging, guards oversized portable exports, and tests out-of-order selections and cancellations. Remaining authenticated cloud-save, painted-art, and browser-width verification remain open. Review/CI pending.

Partial t-041 delivered: kind_robots PR #5528 merged into main c2db243ea66e838ec022bd9525571c3d75f05cb2 at exact head e40d331ee238e48ff3e6981d52b58ebb22e41f98. All nine GitHub Actions workflow groups COMPLETED SUCCESS, including Space Couch full adversarial voyages, seeded game-playthroughs, TypeScript, Playbook Kit, formatting, architecture, layout, schema parity and all four contract shards. Generation-aware file staging eliminates stale async import races; cancellation/account switches invalidate stale reads; bounded portable backup generation rejects >8 MB exports with behavioral tests, and an existing source contract was repaired for the moved validation call. Old save keys, v1 format, account access and achievements preserved. Remaining t-041: authenticated live account backup/restore, accepted original painted-art URLs, 390/768/1440 browser layout and final human playtest readiness. Return to READY (partial), not DONE.

Partial achievement correctness fix: Personal Business now awards only on completion of a three-stop crew quest, with regression cases for unfinished first and second stops. Remaining t-041 acceptance work is not complete.

2026-11-22 PT closure evidence (Silas-directed session; no other workers). Remaining
t-041 criteria verified on live kindrobots.org: (1) painted-art URLs: all 342
onboarding/voyage/episode paintings serve 200 to a signed-in kind-session viewer and
correctly 404 to anonymous viewers (private-art publish gate intact); (2) 390/768/1440:
three complete signed-in voyages, one per width, played captain selection through
chapter 9 finale and ending, 72 screens each, every screen painted, 0 broken images, 0
console errors, 0 horizontal overflow; defects found (HUD spill under Kit icons, meter
fill overrun, phone cast clipping) fixed in kind_robots #5548 (merged eef3416); (3)
authenticated account backup: GET /api/game-of-captains/voyage-save returns 200 for a
signed-in viewer and 401 anonymously; write/restore paths remain covered by the merged
regression suites (not exercised live to avoid overwriting a real account backup). Final
human playtest verdict stays with t-012.
<!-- note:end t-041 -->

## t-042 — Share one art-ledger status vocabulary across Space Couch ledger tests so guards stop hard-coding stale status subsets

<!-- note:begin t-042 -->
Kaizen from review of conductor#7736 (2026-11-21 PT): the new chapter-nine provenance guard allowed only PENDING/REJECTED/ACCEPTED and broke as soon as the live art sweep checkpointed the jobs to DONE. Export the canonical ArtJob status set (PENDING, DONE, ERROR, plus curator verdicts) from one helper and use it in every Space Couch ledger test; keep DONE distinct from visual acceptance.

Shared source-aligned ArtJob/curator status validator, migrated Chapter 9 and cast ledger tests, and added synthetic provenance and acceptance coverage. Implementation commit 2edf6cae34246ee3983e9c59796e00188210b8b7 pending CI.

PR silasfelinus/conductor#7742 merged as dee98964e660c273928dc39d1fe56408a4b7bad4 after all four exact-head Actions workflows completed successfully. Shared ledger-status and provenance regression coverage landed; DONE remains distinct from visual acceptance.
<!-- note:end t-042 -->

## t-043 — Fail CI on double-escaped byte literals in new scripts and tests

<!-- note:begin t-043 -->
Reviewer kaizen from the 2026-11-21 PT rescue merge of conductor#7748 (fixture wrote escaped backslashes, so every WebP fixture was invalid; the same bug hit rainbow#7747's WebM magic check in production code). Add a small lint test over scripts/ and tests/ that flags a backslash-backslash-x sequence inside a bytes literal, with an allow-list for intentional cases, so the connector Worker's escaping habit is caught before CI runs the logic.

Implemented tokenize-based CI regression guard for double-escaped hex in bytes literals across scripts and tests, with detector cases and explicit exception hook. Worker branch worker/game-of-captains-t-043-bytes-lint-b7c29; pending exact-head CI and merge.

2026-11-21 PT Reviewer: merged conductor#7753 (118588e) once exact-head CI was green;
the only red check was the handoff template, fixed by rewriting the PR body. Kaizen
t-044.
<!-- note:end t-043 -->

## t-044 — Add a matching double-escaped byte-signature guard to kind_robots TypeScript tests

<!-- note:begin t-044 -->
Reviewer kaizen from the 2026-11-21 PT merge of conductor#7753 (t-043, Python-only guard). The rainbow#7747 WebM magic-check bug was the same double-escaped hex habit, in production code. Add a small Vitest guard in kind_robots that flags a double-backslash-x hex escape inside Uint8Array/Buffer signature literals in server/ and utils/, with an exact path:line allow-list.

Added TypeScript AST-based byte-signature escape guard and positive/negative fixtures in kind_robots branch worker/game-of-captains-t-044-20261121-c8e7; pending exact-head CI.

Kind Robots PR #5515 merged as 11aced6d359ca93f10ab9a25c19ee2a62ad23169 after six exact-head workflows completed successfully on 6369d4cb15fff94e69117fd77d3be500c25ba609, including TypeScript and Contract Tests. The AST byte-signature regression guard is delivered.
<!-- note:end t-044 -->

## t-045 — Captain selection redesign: large painted portraits and an art-first layout

<!-- note:begin t-045 -->
Silas 2026-11-22 PT: "we have good large sized portraits for our fake zodiac, but then our captain selection looks a little lackluster. We really might need a redesign of that art, but in any case, it needs to be large and art first layouts." Live audit: six 55px circular thumbnails inside mostly empty cards, a 367px square hero, stats/copy dominating. Deliver tall painted 832x1216 captain portraits (art/CAPTAIN-SELECTION-ROUND-1.yaml, ArtJobs 76475-76486, two seeds per captain, curator keeps one) and a selection screen where paintings lead at 390/768/1440.

2026-11-22 PT: curated one of two renders per captain (keeps 278424, 278426, 278429, 278431, 278433, 278435; Vale B rejected as resembling a film prop). New components/gameOfCaptains/captain-gallery.vue: painted full-length lineup with the chosen captain widened, a dossier beside it, and a phone swipe carousel. Screenshots at 1274x534 / 700x760 / 322x564 panel sizes; suites, vue-templates and vue-tsc pass. Kind Robots PR #5548 (combined with t-046).

2026-11-22 PT: Kind Robots PR #5548 merged as eef341634849bd9d4d03cacbcbc662e41cd42c85
after all 17 exact-head checks completed SUCCESS (TypeScript, four contract shards,
seeded playthroughs, all-captains adversarial matrix, layout, Playbook Kit, production
image). Captain selection is now an art-first gallery of six curated 832x1216 paintings
(ArtImages 278424/278426/278429/278431/278433/278435) with a phone snap carousel;
verified at live panel sizes 1274x534, 700x760 and 322x564. Same PR made the expedition
console art-first per Silas's follow-up note (full-bleed episode painting, glass panels,
painted officer cards).
<!-- note:end t-045 -->

## t-046 — Space Couch sound and music: original score, interface and event sound, mixer settings

<!-- note:begin t-046 -->
Silas 2026-11-22 PT: "We never mentioned sound and music, but that should be expected." Ship original (procedural, rights-clean) title and voyage music, interface/event sound for choices, success, failure, redshirt loss and endings; start only after a user gesture, honor reduced motion/mute, persist music and effects volume in the shared settings sheet, and cover it with deterministic tests.

2026-11-22 PT: utils/gameOfCaptains/sound.ts adds six original procedural lounge loops by voyage phase and twelve event cues from a pure run diff. Music/Effects sliders sit under the Kit settings, Kit Sound is the master switch, and nothing plays before a gesture. verifySpaceCouchSound.test.ts (9 checks); headless Chromium audio probe confirmed signal per mood, mute and suspend. Kind Robots PR #5548.

2026-11-22 PT: Kind Robots PR #5548 merged as eef341634849bd9d4d03cacbcbc662e41cd42c85
(all 17 exact-head checks SUCCESS). utils/gameOfCaptains/sound.ts: six original
procedural space-age lounge loops cross-fading by voyage phase, cues for
launch/warp/arrival/four results/fallen and hired redshirts/new crew/chapter/ending from
a pure run diff; Music and Effects sliders under the shared Kit settings; Kit Sound is
the master switch; silent until a gesture; pauses when hidden.
verifySpaceCouchSound.test.ts (9 checks) and a headless Chromium analyser probe (signal
in every mood, mute and suspend) passed.
<!-- note:end t-046 -->
