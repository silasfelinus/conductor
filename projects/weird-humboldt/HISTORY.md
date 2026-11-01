# weird-humboldt — task history archive

Full `note:` prose for completed weird-humboldt tasks, moved out of `roadmap.yaml` so the
Kind Robots projection payload (`scripts/sync_kind_robots_projection.py`, hard limit
4,000,000 bytes) stays well clear of its ceiling. See conductor/t-158.

Each note below is the **verbatim** original — nothing is summarized or trimmed. The
`roadmap.yaml` task keeps its own first sentence plus a pointer here. The HTML comment
markers delimit each note exactly; `archive_done_task_notes.py --verify-only` re-extracts
every note and checks it byte-for-byte against what the roadmap recorded.

## t-002 — Build v1 encounter contract, seeded deck schema and 18 complete text cards

<!-- note:begin t-002 -->
Implement Conductor-only JSON Schema/validator with 2d6 options, success/fail prose, provenance tiers, flags and dependencies, archetype-specific reactivity, plus PRELUDE-STATE-CONTRACT.md opening/current lens and Clarity fields. and a text-only hand-playtest. Include voluntary opening_state, changeable current_state, Clarity and per-state authored alternative narration/choices, as specified in PRELUDE-STATE-CONTRACT.md. Keep one immutable canonical reality per seed and sober routes to key evidence. Use 18 different encounter seeds spanning six chapters, human-edit for comedic timing, retain fixed authored cast per card. No Kind Robots runtime changes or art generation in this task.
PR 6479 merged (d806353): card.schema.json, validator + seeded playtest, 18 text cards (3/chapter, 7 four-state), HAND-PLAYTEST.md, 5 tests. Provisional drafts; human comedic- timing edit still welcome.
<!-- note:end t-002 -->

## t-003 — Author and test all 120 complete encounter records, callbacks and chapter anchors

<!-- note:begin t-003 -->
Convert all 120 seeds to scene + >=2 choices + check/visible stakes + authored success/failure/complication text + persistent consequences. Include 6 chapter anchors, 10+ endings, 8 playable archetype reactions, no-dead-end proof and writing review for humor, cultural care and variety. Ensure choices also create human-scale civic future flags, recurring commitments and different ecological and economic costs per ECOTONE-CORE.md. No art jobs.
2026-10-22 PT: 18 more cards authored (78 -> 96 of 120), PR #6512 merged. 24 seeds remain (WH-0xx incl. 121); next batch 3-4 per chapter.
2026-10-22 PT: 18 more cards authored (96 -> 114 of 120); validator/tests now expect 114 (19 per chapter). 7 seeds remain: WH-020, WH-038, WH-059, WH-080, WH-100, WH-120, WH-121. WH-120 (county vote finale) needs ending-grammar design; then final count 121.
2026-10-23 PT: WH-121 The Latitude Argument authored (114 -> 120 incl. earlier batch; deck now 120). Only WH-120 (county vote finale, needs ending-grammar design) remains.
2026-10-23 PT: card authoring COMPLETE (121 cards, WH-120 merged #6527, validator + no- dead-end proof #6533). Remaining scope only: 6 guaranteed chapter anchor scenes (non- card; see JOURNEY-LOOP-CONTRACT.md; Wiyot/Tuluwat anchor excluded per EXCLUDED- CONTENT-2026-10-22.md), 10+ ending records per ECOTONE-ENDING-GRAMMAR.md, 8 archetype reactions, writing review.
2026-10-24 PT: 12 ending records (8 companion cores + 4 county futures) merged via #6557 with validate_endings + tests. Remaining scope: 8 archetype reactions, writing review (confirm anchors status in anchors/anchors.yaml).

Six guaranteed chapter anchors authored (WH-A1..A6, projects/weird-humboldt/anchors/anchors.yaml): ch1 local mystery, ch2-4 the three stay/follow crossroads (each with a no-roll stay and follow route setting crossroadsN_stayed/followed), ch5 companion payoff (honour/complicate/betray), ch6 county convergence. validate_anchors() in validate_weird_humboldt_cards.py enforces one per chapter, no flag gating, a no-roll option, authored failures, four lead reactions and callbacks set by effects, and rejects Wiyot/Tuluwat terms; 3 new tests. Remaining scope: 10+ ending records per ECOTONE-ENDING-GRAMMAR.md, 8 archetype reactions, writing review. No art, no Kind Robots runtime.

2026-10-24 PT: 12 ending records (8 companion cores + 4 county futures) merged in #6557
with validate_endings() and tests. Remaining scope: 8 archetype reactions and the
writing review.

2026-10-24 PT: 8 archetype records (reactions to all six anchors) merged via #6575 with validate_archetypes + tests. Remaining scope: writing review only.
2026-10-24 PT: agent writing review in WRITING-REVIEW-2026-10-24.md (structure, variety, repetition and exclusion scans clean). One open owner question: WH-121 (Mad River / Wiyot-language naming) vs EXCLUDED-CONTENT-2026-10-22.md; t-004 human creative review still applies.

2026-10-24 PT: Wiyot naming stripped from WH-121 (#6591). All scope delivered; whether
to remove WH-121 outright is Silas's call (WRITING-REVIEW-2026-10-24.md).
<!-- note:end t-003 -->

## t-006 — Develop art direction and queue project icon, card, hero and encounter art

<!-- note:begin t-006 -->
Silas opened the art gate in session on 2026-10-19 PT ("submit the art prompts"), so this no longer waits on t-004. Round 1 is art/ROUND-1.yaml: 24 house-lane (Arthemy) cells, ArtJobs 40841-40864 originally submitted, covering project icon/card/hero, Play title art, Mara/Kit/Juniper/Cedar (two seeds each), the six chapter regions, the prologue meadow, WH-006, WH-021, WH-061 and a card back. Next: --status, review keepers, export them to kind_robots public/ecotone/ (the /play/ecotone board overlays them on its drawn scenes) and projects/images/weird-humboldt-*.webp. Ending-signature art stays behind Keep/Modify/Reject prompt review. DONE 2026-10-19 PT: all 30 cells rendered (6 were rerolls, ArtJobs 40865-40870). 19 reviewed keepers (art/ROUND-1.yaml `keepers:`) are live in kind_robots#3870 under public/ecotone/, and project icon/card/hero are in projects/images/. The ch6 dragon is a provisional keeper.
<!-- note:end t-006 -->

## t-008 — Prove festival lenses and sober story parity

<!-- note:begin t-008 -->
Validate the user-directed festival state model, four authored views of the same encounter seed (not 480 separate cards), and lens-specific choices/checks; support current-state changes and recoverable Clarity, save/reload determinism and a fully meaningful sober route to every required clue and ending. Incorporate an independently motivated nymph guide across all four branches. Text-only, no art or deployment.

Added five adversarial player-style policies over matched seeded journeys, a parity/replay and consequence-diversity contract, and an evidence-based editorial review. Implementation branch worker/weird-humboldt-t008-playstyles-7f62c; pending Kind Robots CI.

Scoped adversarial playstyle slice merged as Kind Robots PR #4045, squash SHA 6d59826cbabae0fe564b20368af92781b20ab47f. All 13 latest-head CI workflows completed successfully, including Ecotone gameplay, TypeScript, formatting, and four contract shards. Simulated 1,260 journeys across five contrasting player styles and 252 matched groups; every group showed divergent decisions, saved consequences, and ending IDs. Human fun assessment is not claimed. The original t-008 umbrella still needs evidence for full clarity recovery, lens parity across authored scenes, and independently motivated Juniper guide development. Other non-sensitive playstyle follow-up: investigate caretaker, solo and coalition policies producing 21 distinct endings each versus investigator 44 and thrill 39.

Scoped adversarial playstyle addition merged as kind_robots PR #4045 (6d59826cbabae0fe564b20368af92781b20ab47f). All 13 CI workflows completed successfully on the final head, including gameplay, formatting, TypeScript and four contract shards. The deterministic 1260-campaign matrix and editorial review are shipped, but t-008 still requires the fuller authored lens and Clarity recovery acceptance; leave remaining task READY. New owner request for a distinct prioritized editorial triage follows separately.

Continued editorial investigation after merged PR #4045. Authored a ranked evidence-backed creative/gameplay triage in the Conductor project and queued four distinct reversible development tasks (t-057 through t-060), while reusing existing t-013, t-021, t-045 and art owners for overlapping scopes. Conductor PR branch worker/weird-humboldt-t008-triage-e7c19. t-008 still has separate broader festival-lens acceptance work after merge.

Owner-requested adversarial playstyle triage completed and merged in Conductor PR #6518, SHA f0b6b6a951acda66b93a17788cd415b9851c463d, after all six current-head PR workflows succeeded. The eight-item ranked triage is projects/weird-humboldt/PLAYSTYLE-TRIAGE-2026-10-22.md; four non-overlapping implementation tasks t-057 through t-060 are READY. Separate original t-008 authored lens/Clarity parity requirements remain; return it to READY rather than falsely marking the whole task done.

User explicitly superseded seven-visible-lenses design. Implemented a smaller scene-specific offer selector for GR-2, KN-2 and QW-2, changed optional moments to appear only at two believable follow-on scenes, and eliminated the global seven-drug UI. Retains seven internal perspectives, existing save/ending identifiers, authored checks/art and old simulation fixtures. Added bounded-choice regression contract and narrative offer policy document. Kind Robots branch worker/weird-humboldt-t008-contextual-offers-84c6b pending PR/CI.

User correction implemented and merged as Kind Robots PR #4063, squash SHA 8aa2afe0aa3e1d48c6653432dfa60df4449b1968. All 15 final-head workflows completed successfully, including Ecotone Gameplay, TypeScript, formatting, layout and the full contract suite. The seven chemical perspectives are internal content IDs only; the visible opening decisions now offer sober abstention plus one or two organic scene-specific offers. Follow-on chemistry UI exists only at two grounded beats and never displays the global seven-item picker. New UI regression tests guard this constraint. No production deployment, release or art job changes. Return the umbrella to READY for remaining Clarity recovery, authored lens parity, and Juniper agency scope; do not reinstate seven simultaneous visible opening choices.

Sober-route parity slice merged as kind_robots PR

Closed 2026-10-25 after verification on kind_robots main (0ac54c6):
verifyEcotoneClarityRecovery, verifyEcotoneSoberParity (7 endings, 172 cards),
verifyEcotoneSceneOffers and verifyEcotoneJuniperAgency all pass; with playstyle matrix
(#4045), contextual offers (#4063) and sober parity (#4184) every t-008 acceptance item
has a passing contract. Human fun assessment not claimed.
<!-- note:end t-008 -->

## t-009 — Write four companion intros with Hmong Kit and grounded Mara stories

<!-- note:begin t-009 -->
Text-only four-way first-encounter authoring based on COMPANIONS-AND-PROLOGUE.md, with Juniper and Kit confirmed, and Mara (sober tattoo artist) and Cedar (younger rural logger/grower-family child with practical skills and a conspiracy-radio habit) as working names. Four distinct adult motivations, 2-4 consequential choices each, optional companionship, sober evidence parity and re-encounter scenes. Draft four personal optimism arcs per COMPANION-OPTIMAL-PATHS.md, with Cedar's parents still together through his optimal storyline. For Mara, keep the fictional independent tattoo studio and its ethics, without any tribe-specific ancestry, grant scheme or coded designs. Cedar's earlier hippie/grower/dispensary backstory is withdrawn; he is a younger working rural local from Hispanic logger father and growing-community activist mother, fictionalized as a volunteer in Luna's ground support. Include historic green/yellow ribbon complexity, worker safety concerns and Julia Butterfly Hill/Luna (1997-99) as fixed documented history; an *invented* modern CB signal handles the paranormal plot. Kit is now HMONG AMERICAN with contemporary local Hmong community context. The previous Chinese-American genealogy and expulsion ancestors are cancelled. Keep the real 1885 Eureka Chinese expulsion and 1950s Chinese American return in their OWN sourced encounter (HAPI, Cal Poly Humboldt archives, Historical Society). Develop Kit's individual family/arts story without stereotypes or inventing Hmong ancestral ties to Chinese history. Cedar's father is HISPANIC; specific background and his side of timber/grower lineage TBD. Do not turn ethnic identity or historic victims into occult plots. No art or publishing.
Merged #6640: four companion intros + Mara correction (d4c787f89).
<!-- note:end t-009 -->

## t-010 — Validate companion and perception continuity across all routes

<!-- note:begin t-010 -->
Text-only check of 8 archetypes x four voluntary initial states, including declining all first companions, later reunions, and narrative skills Rizz/Burly/Wits/Local Lore/Psyche. Preserve independently motivated adult NPCs, one objective canonical anomaly, changing current_state and recoverable Clarity. Every required clue and hopeful ending remains available sober; no drug-required victory or cultural identity bonuses. Validate companion optimal path accessibility across all opening states and all eight archetypes, plus declined-then-reconnected invitations, per COMPANION-OPTIMAL-PATHS.md. Cedar's parents_together must be invariant in every future. Coordinate with t-008; do not duplicate its seeded lens tests.
2026-10-25 PT: verifyEcotoneCompanionContinuity.test.ts (441 campaigns: 7 shipped archetypes x 7 opening states x 3 events x decline/follow/accept) merged in kind_robots#4196, CI green. Every companion reachable from every opening state; declined invitations reconnect; no card separates Cedar's parents. Gap: design lists 8 archetypes, engine ships 7 (organizer unbuilt).
<!-- note:end t-010 -->

## t-011 — Design Ecotone civic-fate core, competing factions and future consequences

<!-- note:begin t-011 -->
Text-only design follow-up based on Silas's 2026-10-19 direction. Prototype the one-weekend convergence and decision/flag contract in ECOTONE-CORE.md; distinguish actual Humboldt governance and proposals from fictional predictions. Develop morally complex fictional corporate, grassroots, ecological and workers' factions; avoid tribe-specific fictional representation or consultation dependencies. Four opening states, all archetypes, 120 encounter seed IDs and characters remain. No art.

Authored six-chapter civic promise/flag contract and a fully branched chapter-three prototype in ECOTONE-CORE.md, including faction dissent, failure repairs and deterministic replay handoff. Implementation PR pending checks; design only.

MERGED silasfelinus/conductor#6659 at 87078ad: ECOTONE-CORE.md now contains the six-chapter civic promise matrix, four internally dissenting fictional factions, authored four-choice Eureka hearing, fail-forward repairs, dawn convergence and reducer/replay acceptance criteria. The PR's exact head feedb951 passed Worker PR CI (all 8 jobs, including full Python suite), Security Audit, and handoff checks. Shared cross-task finding: Ecotone master issue comment 6407801993. This closes text-only design t-011, not runtime integration, image coverage, ending reachability, or final game approval.
<!-- note:end t-011 -->

## t-012 — Design 56 modular outcome signatures and ten county motifs

<!-- note:begin t-012 -->
Expand ECOTONE-ENDINGS.md into validated authored 1-/10-/30-year variants: ecology, housing, livelihoods, local agency and reality stability with character-specific payoff. Ten older future scenarios are noncollectible backdrops. Define 56 distinct lead/opening/hope-or-dark IDs and outcome callbacks per ECOTONE-32-ENDINGS.md, not an ideological virtue meter. Integrate companion optimal arcs and earned callbacks per COMPANION-OPTIMAL-PATHS.md. Integrate with t-003 complete cards and t-008 perspective tests. No image pipeline or publication.
<!-- note:end t-012 -->

## t-013 — Test future-state branching, sober parity and no forced ideal outcome

<!-- note:begin t-013 -->
Text-only deterministic tests proving that all initial perception states and archetypes can shape a meaningful county fate without solving the secret transmitter mystery; no ethnicity- or substance-gated endings. Excluded cultural material must not return as story flags, scorecards or mechanics. Require no unreachable endings, no single faction always winning, and callback consequences from personal cards across the region. Also test that all four personal optimal outcomes are reachable by story play without a fixed opening perception, and that Cedar's parents remain together in all endings. No art or Play deployment.
12 text-only tests in tests/test_weird_humboldt_future_branching.py: sober parity, no identity gates, hopeful outcomes reachable, no dominant vote flag, Cedar parents intact.
<!-- note:end t-013 -->

## t-017 — Author four optimistic companion routes and personal epilogues

<!-- note:begin t-017 -->
Draft and validate four distinctive earned companion paths: Juniper/shared canopy, Kit/living return, Mara/lines that last, Cedar/two ribbons one home. Use guaranteeable intro, contradiction, commitment, repair and payoff anchors across regional chapters, with 2-4 real choices and outcomes. Opening perception and declining the first invite must never lock the optimal path; every route is available sober. Cedar's grower-family/logging-family parents are still together from the start and stay together regardless of player decisions; happiness is not a reunification trophy. Keep county future families separate from companion-optimal flags and avoid simplistic pro-tech/pro-hippie moral scores. Keep Mara's route grounded in her independent studio, choices and relationships, with no nation-specific backstory or imagery. Text only, no art or deployment.

Four companion routes authored as 20 chapter anchors and 60 choices with recoverable checked failures, late-follow catch-up, earned payoff flags and hopeful/scarred epilogues. Draft in COMPANION-CHAPTER-ANCHORS.md; structural tests in tests/test_ecotone_companion_chapter_anchors.py. Text only: reducer integration, seeded runtime reachability and artwork remain.

MERGED conductor#6673 (7c692939): four authored companion routes, 20 guaranteed chapter anchors, 60 choices, 8 personal epilogues, late-follow recovery and structural tests. All exact-head checks green; Python suite 3046 passed, 53 skipped. Text-only milestone complete. Reducer integration, seeded journey verification and rendered art remain agent work under separate Ecotone roadmap tasks; no human gate yet.
<!-- note:end t-017 -->

## t-019 — Validate 56 fates through seven opening lenses and companion crossroads

<!-- note:begin t-019 -->
Define 56 stable lead.opening.fate IDs, 28 hopeful/28 dark. The original 4 states map to Mara/Kit/Juniper/Cedar; three new lenses each receive an authored first guide introduction without forcing one of the four. there is NO independent initial companion picker. Three guaranteed later first meetings of remaining main characters arrive in seeded variable order; at each, choose stay or leave previous guide to FOLLOW the newcomer. This yields 28 final companion x opening combinations with meaningful both hopeful and dark resolutions and saved route order. No substance-as-morality mechanics, no extra 10 collectible county motifs. Cedar's four optimistic storylines explicitly build ethical high-tech infrastructure with local ownership, jobs and forest care. See ECOTONE-32-ENDINGS.md. Design only, no art.

Draft PR 3889 needs integration and CI fixes; file writes blocked.

Partial implementation exists as draft kind_robots PR #3889. Before new work, inspect that PR and finish formatting, gameplay reachability, TypeScript and finale integration. No merge or public release yet.

Merged kind_robots PR #3889 after 15/15 CI workflows passed, including gameplay, TypeScript, formatting and full contract tests. Added nine quest cards, four follower-specific scenes, three staged substance-lens scenes, 36 authored ending signatures, multi-era bookends and earned callbacks. Quest prerequisites now flow through the single canonical Playbook deck. Original t-019 objective remains open: three additional adult opening lenses still need authored, playable introductions and reachability tests across all 56 core companion outcomes. No new art generation or public launch approval was granted.

Reviewer verification 2026-10-29: kind_robots main already ships seven opening lenses on
GR-2/KN-2/QW-2 (openingLensChoices.ts) and verifyEcotone.test.ts passes: auditEndingIds
deepEquals all 84 ENDING_IDS (4 companions + alone + ecotopia x 7 lenses x hope/dark)
with fully played deterministic witnesses; every lead has reachable hope and dark; save
round-trips. The 56 core companion x lens x fate fates are covered.
<!-- note:end t-019 -->

## t-026 — Specify modular finale assembly and 56 ending signatures

<!-- note:begin t-026 -->
Apply ECOTONE-ENDING-GRAMMAR.md. Keep 8 fully written final companion x hope/dark 1/10/30-year core spines, 56 distinct opening x final companion x fate signature paragraphs with art concept prompts, and a small verified selection of optional causal callbacks. The older 32 IDs remain stable; 24 new lens variants are added. Scope value-to-debt, conditional truth provenance and one-screen montage. Do not impose 56 triple epilogues or generate images without the human art gate.

Completed a 120-card Ecotone authored quest / finale iteration with companion- and substance-specific sidequests, 56 companion signatures, 1/10/30-year future bookends and causal callbacks. Repairing confirmed PR #3903 gameplay reachability and formatting regressions before merging; Silas authorized publishing iterative content on 2026-10-20 PT while keeping editorial review open.

Implemented and merged kind_robots PR #3903 (e5bc799792eff4511d32d6eed941c7d1ffdd61e5). Authored first manuscript of 120 canonical encounter seeds, distinct narrative lenses, companion signatures, 1/10/30-year modular futures, and earned callbacks. All 13 final GitHub checks passed. Further second-draft editorial uniqueness and migration checks are explicitly separate follow-up work. Silas approved iterative content release.
<!-- note:end t-026 -->

## t-029 — Ship the Ecotone Play front page and playable prologue slice

<!-- note:begin t-029 -->
Silas, 2026-10-19 PT: "get a front end, pointed to Play". kind_robots /play/ecotone in the Play (arcade) channel, labelled Work in progress: one-screen board with code-drawn redwood/fog scenes (painted art from t-006 overlays as it lands), the four voluntary festival lenses mapping to Mara/Kit/Juniper/Cedar, seeded 2d6 checks on the three sample cards (WH-006, WH-021, WH-061), five skills, Clarity, journal, the six-chapter county map and a locked Endings 0/56 gallery that grants nothing until real finales exist. Text from SAMPLE-CARDS.md and COMPANIONS-AND-PROLOGUE.md. Ensure frontend character copy says Hmong American for Kit and Hispanic father for Cedar; never repeat Kit's withdrawn 1885 ancestry or show retired 40848/40849 portraits. The full engine (t-005/t-022) and 120 cards (t-003) replace this slice later. DONE 2026-10-19 PT: kind_robots#3870 squash-merged (a7d7620), all 24 checks green, with art round 1 and the Kit/Cedar heritage updates. Playwright at 390x844, 768x1024 and 1440x900 showed 0 document overflow in every state, and the run survives a reload.
<!-- note:end t-029 -->

## t-030 — Derive validator PER_CHAPTER card counts from ENCOUNTER-SEEDS.md instead of hand-maintained constants

<!-- note:begin t-030 -->
Kaizen from WH-120 review (#6527): validate_weird_humboldt_cards.py and tests/test_weird_humboldt_cards.py hard-code deck sizes, so each new card needs three coordinated edits. Derive counts from the seeds file.

Scoped seed-catalog-driven deck counts and chapter-membership validation implemented on worker/weird-humboldt-t030-seed-counts-9f2c. Added tests for duplicate seeds, editorial-only references, wrong chapter and missing cards; awaiting PR CI before merging.

Merged conductor PR #6661 (78457fa78aab65a96a4498c173ac9201cbcd6567) after exact-head Worker PR CI run 40270863200, Security Audit run 40270863238 and handoff checks all completed successfully. Ecotone card totals and chapter membership now derive from ENCOUNTER-SEEDS.md; tests cover duplicate/missing premises and wrong chapters. No runtime deployment or ArtJobs.
<!-- note:end t-030 -->

## t-031 — Write cards for Silas's location atlas (marsh, Bayshore Mall, zoo, Fickle Hill, Ferndale, more)

<!-- note:begin t-031 -->
From LOCATIONS.md (Silas, 2026-10-19 PT). Draft text cards for the new places: - Arcata Marsh: ecology and engineering in one place. - Bayshore Mall "Anchor Stores": dark storefronts open onto the
  county futures.
- Sequoia Park Zoo "The Friends Who Aren't Here": Kit's troupe
  performs the lost animals; lens decides whether you see actors.
  Past animals never appear as current zoo residents.
- Fickle Hill, the Luffenholtz/Baker Beach detour (PG-13), a
  Heartwood-inspired SoHum card, and the Ferndale village and
  cemetery (invented dead only).
Do not add tribe-specific casino or Hupa history cards as substitutes for withdrawn content. Devil's Playground "Behind the Mall" is now located (Silas). Answer or carry forward the questions in LOCATIONS.md. Text only. 2026-10-19 PT: kind_robots#3871 (merged b5ab270) plays six of these as cards, with art round 2 (art/ROUND-2.yaml, ArtJobs 40875-40883): WH-122 Arcata Marsh, WH-123 Fickle Hill, legacy WH-121 (excluded, audit only), WH-124 the zoo tribute (actors only), WH-125 Bayshore Mall "Anchor Stores", and WH-126 Devil's Playground "Behind the Mall". The deck now draws two cards per chapter from these pools. Still to write: Luffenholtz/Baker Beach, Heartwood, the Ferndale village and cemetery. Tribe-specific locations and WH-121 are withdrawn from development. The zoo-tribute art was withdrawn as anthro; re-render it on the lane art/CHECKPOINT-BAKEOFF.yaml picks.

Authored and integrated four missing non-sensitive local atlas quests as Kind Robots PR #4020, with 12 meaningful choices, checked successes and failures, lasting flags and evidence, and no changes to the route indexing or prior save schema. Scenarios cover Baker Beach privacy and tide safety, a fictional SoHum consent-based arts clinic, a Ferndale shop's maker-credit dispute and an invented hillside cemetery future committee. Added deterministic adversarial seeded encounter and art-slot validation. Prepared 28 image-ready story and outcome briefs for the separately claimed t-042 art worker, without duplicate queue submissions or fabricated image IDs. No Wiyot/Tuluwat-dependent material, outreach or production deploy. Awaiting all PR CI gates before merge.

Kind Robots PR #4020 merged to main as ddd4bdace1a20fc6aed6e72bf3ccd3af7ee7d968, with all 13 workflows green. The existing Arcata Marsh, zoo, Fickle Hill, Bayshore and coastal/regional cards are joined by four previously uncovered atlas stories: Baker Beach, a fictional SoHum arts clinic, Victorian Ferndale's tailoring shop, and fictional Ferndale cemetery residents. Twelve new authored decisions include two checked options with actual success/failure each card, persistent flags and evidence, and a third meaningful solution. Gameplay suite completed 1764 broad seeded journeys plus 6000 added atlas choice continuations (2075 successful checks and 1925 failures), demonstrating real random draw availability, stable saves and art-slot coverage. A new 28-subject story/outcome art brief handoff is in Kind Robots docs/ecotone/ATLAS-ART-BRIEFS-PASS3.md; t-042 owns actual job enqueues and style export. Ledger has 948 DONE records but the current style art manifest is empty, so priority is verified image export and no duplicate regeneration. Respect the withdrawn Wiyot/Tuluwat subject scope and keep unrelated release gate intact. No production deploy.
<!-- note:end t-031 -->

## t-032 — Rebuild the opening: festival or Kinetic race, area then offer then companion, loner path, race conscription

<!-- note:begin t-032 -->
Silas, 2026-10-20 PT (notes_from_silas). In kind_robots /play/ecotone: the first choice is the event: a fictional cannabis festival (partner acro on the lawn leads to Kit, the drum circle in the woods to Juniper; offers sober, stoned or tripping) or the real Kinetic Grand Championship with a fictional afterparty (pit row leads to Cedar, the tattoo tent to Mara; offers sober, tipsy, or the party lenses still being written). Order is area, then the offer, then meet the companion or go alone. On the Kinetic route a racer is hurt at the afterparty and you are conscripted to ride the rest of the race with your companion, then the days that follow. Every beat offers at least two choices, each day opens with face-up "where to" cards, companions can be re-met in other capacities, the opening lens persists, and endings are the companion (or alone) x opening lens x hope/dark from end-of-journey stats. DONE 2026-10-20 PT: kind_robots#3872 squash-merged (f6e1b86), all 21 checks green. The Green Ribbon Fair and the Kinetic Grand Championship routes, Conscripted / The Bay Crossing / The Ferndale Finish, the fair's GR-4 and GR-5 spine beats, white-rabbit forks, the loner path and 70 endings with first-draft finales (bar 5 fair, 7 race; random play near 50/50). Playwright walked both routes to an ending at three widths with zero overflow. Design of record: OPENING-AND-ROUTES.md.
<!-- note:end t-032 -->

## t-033 — Playbook Manager: admin view of Ecotone beats as chained choices, with edits, comments and art requests

<!-- note:begin t-033 -->
Silas, 2026-10-20 PT (notes_from_silas). kind_robots /admin/playbook-manager with an Admin channel tab (requiredRole ADMIN): the playbook as chained choices with sub-choices; sort and filter by day, companion and lens variation; endings and story-spine beats highlighted against random encounters; edit text, comment, add choices, submit or flag images and request art for beats without it. Edits are a database overlay on the authored source, with an export so agents fold them into the code. Schema-affecting (additive tables). 2026-10-20 PT: implementation PR kind_robots#3875 (schema-affecting: additive PlaybookEdit and PlaybookNote tables), merging when CI is green. DONE 2026-10-20 PT: kind_robots#3875 squash-merged (51af450), all 30 checks green including the MariaDB migration replay. /admin/playbook-manager with an Admin tab: route chains, fork pools, crossroads, finale and the five ending storylines; filters by route, day, companion, lens variation and status; edit text, choices, variations and add choices; draft, live (applied in /play/ecotone via /api/playbook/ecotone/live) or revert; comments, image flags and submissions, art requests with job status; JSON export. Schema-affecting: additive PlaybookEdit and PlaybookNote, deployed by the normal Unraid migration step.
<!-- note:end t-033 -->

## t-035 — The Quiet Way: a third, solo opening (marsh, zoo, deer trail) and the Wild Way ecotopia endings

<!-- note:begin t-035 -->
Silas, 2026-10-20 PT (notes_from_silas). A third event at the opening: a contemplative day alone. The marsh leads to Juniper and the zoo to Kit (alternate routes to them), and a deer trail nobody knows goes straight onto the solo path. Animal-first choices are tagged across the route and the animal cards; finishing that route alone is the Wild Way: enough animal-first choices earns the ecological paradise, fewer the bittersweet hermit who never made a real choice. DONE 2026-10-20 PT: kind_robots#3877 squash-merged (dd34104), all 21 checks green. The Quiet Way: A Day to Yourself (marsh to Juniper, zoo to Kit, the deer trail straight to solo), The Bench by the Water (offer), the meeting only if the opening led to someone, The Elk Meadow and The Long Quiet. Animal-first choices are tagged on the route and the marsh, zoo-tribute and Bigfoot cards; finishing the route alone is the Wild Way: four or more is the ecological paradise, fewer the bittersweet Mad River hermit. 84 endings. A loner still meets a newcomer at the crossroads.
<!-- note:end t-035 -->

## t-036 — Playbook Manager for every story game: Shifting Lands, Shifting Desks, the Zuzu gamebook and Emperor of Dust follower and quest lines

<!-- note:begin t-036 -->
Silas, 2026-10-20 PT (notes_from_silas). Generalize /admin/playbook-manager to a game picker with adapters reading each game's authored source: Shifting Lands (lands, locations, deck pools, trials), Shifting Desks (departments, locations, encounters, window shifts, bosses), the Zuzu gamebook (chapters and scenes with explicit next pointers), and Emperor of Dust (days, audiences and options, quests, follower lines and flag-gated quest lines). Read, comment, flag and request art everywhere; text edits go live only where a game reads the overlay (Ecotone first). Emperor of Dust is read-only here, so it never collides with its own active tasks. DONE 2026-10-20 PT: kind_robots#3878 squash-merged (e278cf1), all 23 checks green. The game picker loads Ecotone, Emperor of Dust (50 days, 77 audiences, 77 quests, 20 follower lines, 20 flag-gated quest lines, 8 endings), Zuzu: Shifting Lands (15 location draws, 120 cards, 5 trials), Shifting Desks (draws, window shifts, bosses, 10 endings) and the Zuzu gamebook (377 scenes with explicit turns, no special case needed). Text edits stay Ecotone-only; notes and art requests work for every game, tagged to each game's project and preferred lane.
<!-- note:end t-036 -->

## t-037 — Playbook content layer: live text edits in Shifting Lands, Shifting Desks, the Zuzu gamebook and Emperor of Dust

<!-- note:begin t-037 -->
Step 1 of Silas's 2026-10-20 plan (notes_from_silas). Each game's single lookup (v6Card and trialForLand; encounterById and the boss in currentCard; scene(); questDef and dayDef) consults a live text overlay loaded from /api/playbook/<game>/live, so Save and go live in the Playbook Manager works for every game. Text only: titles, story text, choice labels and outcome text; ids, rolls, effects and structure stay authored, and seeded play is unchanged. Touches those games' lookup functions and stores in a few lines each (cross-project: zuzu-shifting- lands, shifting-desks, zuzu-gamebook, emperor-of-dust).
DONE 2026-10-20 PT: kind_robots#3880 squash-merged (06cc4fe), all checks green. Shifting Lands (v6Card, trialForLand), Shifting Desks (encounterById, windowApplicant, boss), the Zuzu gamebook (scene) and Emperor of Dust (questDef, dayDef with audiences) read a live text overlay loaded from /api/playbook/<game>/live, so Save and go live works in every game. Words only; ids, rolls, effects and links stay authored. verifyPlaybook proves the round trip for every editable beat in all four games. The image-first manager layout Silas asked for next follows in kind_robots#3881.
<!-- note:end t-037 -->

## t-038 — Ecotone play layout to the 2026-10-20 mockups

<!-- note:begin t-038 -->
Silas's mockups (design/2026-10-20/). The play view takes the mockup structure: - top bar: the mark, the day and event line, place and time, and Clarity
  and Endings pills;
- full-bleed scene art, with a left headline column (kind pill, serif
  title, subtitle, narration, and a companion block on encounters with
  the portrait on the right);
- a dialogue panel with a gold kicker, and a choices panel where each
  choice shows its roll and where it leads;
- a bottom nav on every width (Journey, Guides, Map, Journal, Endings). Navy, gold and cream throughout. Real stats and the real ending count replace the mockup's placeholder numbers.
DONE 2026-10-20 PT: kind_robots#3882 squash-merged (ce628a6), all 20 checks green. The play view follows the mockups: navy, gold and cream; top bar with the mark, day and event line, place and day, Nerve, Clarity and Endings pills; full-bleed scene with a left headline column (kind pill, serif title, subtitle, and on companion encounters the name, role and line with the portrait on the right); dialogue and choices panels (each choice shows its roll and where it leads); a Journey / Guides / Map / Journal / Endings bottom nav. Phones stack art, panel and choices in one scroll.
<!-- note:end t-038 -->

## t-039 — Ecotone art styles, the Shifting Desks way

<!-- note:begin t-039 -->
A player-selectable art style, like Shifting Desks. It is view-only, so runs and saves are unaffected, and the choice is remembered per browser. Styles: Painted (the current Z-Image house lane) and Storybook (the code-drawn scenes the mockups show). Each further style keeps its renders under /ecotone/styles/<id>/; any beat it hasn't drawn yet falls back to the base painting, then to the drawn scene. Which checkpoints become styles waits on Silas's bake-off review (t-034).
DONE 2026-10-20 PT: kind_robots#3882 squash-merged (ce628a6). utils/ecotone/artStyles.ts: Painted (default, the shipped paintings) and Storybook (the drawn scenes), picked from the palette button and remembered per browser; view-only, never in the run. A further style lists its renders under /ecotone/styles/<id>/ and falls back to Painted, then the drawn scene, per beat. Which checkpoints become styles is Silas's call after the bake-off review (t-034).
<!-- note:end t-039 -->

## t-040 — Playbook Studio: Story Atlas gallery and focused scene editor

<!-- note:begin t-040 -->
The Playbook Manager becomes the Playbook Studio of the 2026-10-20 mockups. - Story Atlas: a left rail (your stories with beat counts, a Collection
  of routes and sections, live story health with art requests), the
  STORY ATLAS headline with filter pills, and art cards with a numbered
  kind pill, a serif title, the place line, a status dot and an open
  arrow.
- Scene editor: a back link, a serif title, a breadcrumb, a gold-framed
  art card (scene and variant pills, a quoted line, art candidates,
  View art options), and the Edit Scene panel (draft pill, underlined
  Story / Choices / Variants / Art / Notes tabs, a summary footer and a
  gold Save draft button).
Chain view stays available from the Atlas. Every existing edit, note and art tool keeps working.
DONE 2026-10-20 PT: kind_robots#3883 squash-merged (29f1bef), all 21 checks green. The Playbook Manager is now the Playbook Studio (same /admin/playbook-manager route): navy, gold and cream; the Story Atlas (stories rail with beat counts, Collection of routes and sections, Refine filters, live story health with open art requests; art cards with numbered kind pill, serif title, place, status dot) and the scene editor (back link, title and breadcrumb, gold-framed art card with candidates and View art options, Edit Scene panel with draft pill, underlined Story / Choices / Variants / Art / Notes tabs, player choices with rolls, summary and gold Save draft / Save and go live). Chain view one tap away. The mockup's + New beat is left for Silas: adding beats needs engine routing.
<!-- note:end t-040 -->

## t-041 — Playbook Studio: + New beat

<!-- note:begin t-041 -->
Silas approved the mockup's "+ New beat" (2026-10-20). A new beat needs a home in the game's flow: the Studio creates it as an edit row (title, text, choices with roll, outcome text and effects) attached to a place the engine already deals from (a route day, a fork pool, or a choice's outcome), and the engine reads those rows like authored cards. Start with Ecotone, where cards and fork pools already carry live edits; other games follow their own content layer. Tests prove a new beat can be reached and finished in seeded play.
<!-- note:end t-041 -->

## t-043 — Temporary checkpoint review page with generation times

<!-- note:begin t-043 -->
Silas asked where to see the example generations; there was none. /admin/art-review (kind_robots) shows every Ecotone art ledger (the bake-off's 8 subjects x 8 lanes and rounds 1-3) side by side with live status, render time (claim to image saved) and queue wait, per-lane median, fastest and slowest, a lightbox with prompt and settings, and a shortlist per lane for picking the 2-4 styles. Temporary: retire it once the styles are picked.
DONE 2026-10-20 PT: kind_robots#3886 squash-merged (2825122), all 25 checks green. /admin/art-review (Admin > Checkpoint Review, admin only) shows the bake-off's 8 subjects x 8 lanes and rounds 1-3 side by side with live status, render time (relay claim to image saved, so it includes model load and upload) and queue wait; per-lane median, fastest and slowest; a lightbox with prompt and settings; and a per-lane shortlist. Retire the page (and its admin tab) once Silas picks the styles for t-042.
<!-- note:end t-043 -->

## t-046 — Second draft I: make high-leverage regional decisions genuinely distinct

<!-- note:begin t-046 -->
Silas (2026-10-20 PT): publish/review/iterate, 80% improve and test vs 20% targeted new prose. Audit 120 authored encounters for mechanical sameness. Replace the invest-or-help boilerplate at 10+ pivotal cards across the six regions with third/fourth specific alternatives, authored outcomes, surprising failures, persistent distinct flags and earned callbacks. Preserve the 2d6/save/art-slot schema, no mandatory moral/substance verdict, 2-4 choices, history/cultural gates, and add deterministic tests for uniqueness and reachability.

Scoped user-approved second-draft implementation adds 13 region-spanning bespoke third alternatives, six complete seven-lens narrated encounters, six uniquely earned future callbacks and conditional ballot/journey memory. Kind Robots PR forthcoming; retain active editing/review loop and no historical/tribal publication waiver.

Merged kind_robots PR #3908 as 8932bb0659c103e1f14c9a7b31eaf5578ede8520. Added 13 bespoke third choices across all six regional chapters, six seven-lens passages (42 path-specific asides), six earned future callbacks and conditional county ballot acknowledgments. All 13 current head workflows passed including Ecotone gameplay, TypeScript, Prettier, and full contract shards. Editorial examples are distinct wry narrative, not imitation of named authors.
<!-- note:end t-046 -->

## t-047 — Second draft II: companion continuity and chosen-family optional scenes

<!-- note:begin t-047 -->
Audit every lead/lens encounter and stay/follow relationship for contradictions; create bespoke recurring callbacks, optional scenes with former companions, and earned found-family outcomes without forcing romance or implying unseen meetings. Coordinate with t-045 chosen-family design and preserve the existing 56 primary companion signatures and 84 overall solo/Wild Way gallery slots.

Implemented four individually gated former-guide meetings and an optional two-meet community potluck, with consequential choices, seven-lens potluck narration, six earned future callbacks, and seeded-eligibility regression tests. This independent portion intentionally does not overwrite the separate pending t-045 chosen-family design from Conductor PR #6394. Kind Robots PR forthcoming.

Kind Robots PR #3910 merged at fa8ebb9d83cda4545b3b652683cb4cc27273385d. The four former-guide encounters plus optional multi-meeting potluck, six earned callbacks, and eligibility/reachability tests shipped. The final PR head passed all 13 required checks, including full contract tests, Ecotone gameplay, TypeScript, and changed-file Prettier. Branch janitor subsequently passed. The separately approved Conductor #6394 art and chosen-family plan is merged; future full seed coverage and save migration remain t-048 and editorial redline is t-049.
<!-- note:end t-047 -->

## t-048 — Second draft III: thousands of seeded journeys and save compatibility

<!-- note:begin t-048 -->
Simulate seeded campaigns across openings, routes, archetypes and switches to prove all reachable endings, safe choice offers, coherent flags, no duplicate cards, no phantom callbacks, replay variety and 45-75 minute pacing. Explicitly protect legacy WH-004/WH-037/WH-058 save IDs as LX variant cards replaced these bonus identifiers. Add regression coverage for recoverable failures, gallery counts and art-outcome identity.

Seeded QA implementation: 8400 additional deterministic playthroughs with card/result art, callbacks, continuity and save roundtrips; title-confirmed migration of older WH-004/037/058 chemical quest references. Audit found that Quiet Way has only three opening lenses while the 84-slot ending gallery includes seven, making four Wild Way lens pairs unreachable. Review PR, preserve release gates, and file a dedicated seven-lens opening fix.

Stage 3 automation complete: merged kind_robots #3932 as ddab6cc and #3939 as 351264e2bbfd83a8e24a4004503f60878ca770d5, each after full passing CI (13 and 15 workflows). The final 8400-run report witnessed all 84/84 ending slots, 564 distinct card/outcome art keys, 17408 failed checks and 1048 earned callbacks. All three routes now offer every voluntary opening lens with authored outcomes; save IDs remain stable and legacy WH-004/037/058 chemical quest references migrate only when log titles prove the old identity. Issue kind_robots #3933 fixed by the merged PR. Human 45-75-minute pacing is NOT validated by automated click counts; carry that as a manual editorial/playtest follow-up during t-049.
<!-- note:end t-048 -->

## t-049 — Second draft IV: prose, history, culture and quality redline

<!-- note:begin t-049 -->
Run chapter-by-chapter editorial review for humor, character agency, distinct mood, source provenance, sober parity, diverse lived-in identities and real-world historical care. Human consultation is required before Tuluwat/Wiyot historical player-facing text ships; do not randomize atrocity or frame history as occult explanation. Leave final publication and creative acceptance gates intact.

First editorial batch underway: twelve rewritten encounters across six regional chapters. Reconciled playable JSON with editorial chapter Markdown, added manuscript synchronization tests and a provenance-conscious redline checklist. Keep 108 other canonical cards and deeper cultural/historical review as remaining scope. No new published Indigenous historical text, production deployment or ArtJobs were included.

Editorial batch one merged on Kind Robots PR #3941 as 01bd03dd299010429f6c7201f5f4d1463ae477bf after all 13 workflows passed. Sharpened WH-001/002, 023/025, 041/044, 063/064, 081/082, 102/103 across all six regional chapters, synchronized six editable reading-kit documents with playable narrative data, and added regression checks for synchronization. Keep t-049 READY for the remaining 108 scene reviews, cultural provenance checks, chemical-path voice consistency and real 45-75-minute human-paced playtesting. Wiyot/Tuluwat player-facing history still requires living-community consultation before publication. Learning (moved from a learning: field, which the processor only accepts on done or blocked events): Prefer a small verified sample from each region and keep the playable manuscript and art-informed editorial copies synchronized. Dry comedy works best after believable details and consequences, not purple prose.

Second focused prose review adds 18 newly redlined regional encounters across six chapters (now 30 of 120 reviewed in this stage), synchronized all six chapter reading kits, and authored 42 distinct lens observations across six representative encounters. Code review and test suite are under way; 90 remaining scenes plus history/provenance and human 45-75 minute playtest gates stay open. No Wiyot/Tuluwat historical prose, image jobs or external publication changed.

PR #3943 merged after all 13 checks green as 65b2df85c831d25a5e4aa76b51969fb375d79d17. Second editorial batch completed 18 additional scenes, 42 new lens asides and storybook parity. Leave 90 canonical scenes plus human playtesting and consultation review open for subsequent sessions. Return t-049 to ready for continued work.

Third editor pass includes 18 more fictional encounters (48/120 cumulative) and 42 new lens-specific asides (84 new asides across rounds two and three). All six editable chapter manuscripts updated, gameplay parity contract extended to 48 selected cards and 12 seven-lens collections. Awaiting CI/review before merge. Cultural consultation, 72 other scene passes and human 45-75-minute gameplay pacing remain open.

Third editorial batch merged to Kind Robots main on PR #3949 as 33b9e928b99389e978cfd969e87c1763588998c6 after all 13 exact-head workflows passed, including seeded Ecotone gameplay, TypeScript, changed-file Prettier and the full contract suite. Added 18 more distinct regional scene revisions (48/120 cumulative), 42 more unique seven-path narrator asides (84 total in rounds 2-3), synchronized six playable/editorial chapter manuscripts and expanded contract tests. Return t-049 to ready for 72 remaining canonical scene line edits, provenance/consultation and measured human 45-75-minute playtesting. Indigenous historical release gates remain intact, with no new art jobs or external deployment.

Editorial completion PR prepared: 63 remaining regional scenes reviewed and revised, all six canonical chapter reading kits synchronized, nine original encounter cards audited and targeted, and test parity expanded to all 111 regional scripts. Full 120/120 encounter editorial coverage; separate historical consultation, subjective creative acceptance, and human 45–75-minute playtesting remain gated.

Editorial completion merged to kind_robots main in PR #3952 at a9cdf8cc1c09e41c9bbba159a6d82b0b1848637b. All 13 exact-head GitHub workflow checks completed successfully including Ecotone gameplay, TypeScript, Changed-file Prettier and the four Contract Tests shards. Finished 63 previously unreviewed regional encounter revisions across all six chapters, synchronized 111 of 111 playable regional scripts with their six chapter reading kits, and audited all nine legacy original encounters for 120/120 editorial coverage. Added full manuscript parity checks and seven-lens Moonstone picnic continuity. This closes the manuscript redline task only; genuine timed human playtesting, Wiyot/Tuluwat community consultation, art matching, subjective creative approval and any public release remain unapproved and tracked by the separate acceptance/creative gate tasks (t-004 and t-007). No ArtJobs or deploys.
<!-- note:end t-049 -->

## t-050 — Third pass: adversarial playthroughs, meaningful setbacks and art-brief completeness

<!-- note:begin t-050 -->
Silas-directed 2026-10-20 PT: simulate many full seeded Ecotone journeys across events, archetypes, lenses, companions, successes and failures. Add permanent quality regressions for dead ends, inert or indistinguishable options, meaningful interesting failed rolls and earned lasting consequences. Audit concept art briefs for every playable event, alternative and result; enforce unique provenance-bearing slot keys and flag weak or missing briefs without stealing the separately claimed t-042 art generation work. Repair concrete defects found, keep canonical manuscript parity and Wiyot/Tuluwat consultation and publication gates intact.

Ecotone adversarial runtime and art-brief coverage implementation staged on worker/weird-humboldt-t-050-adversarial-20261020-b7e2 for CI and review. Distinct event-choice illustration pitches, all authored win/loss branches, thousands of seeded end-to-end personas, saved-state and earned callback checks.

Merged Kind Robots PR #3972 at 55ba1daf8a29b77f7fe7432acdd5b3fe891d2b34 after all 13 GitHub Actions workflows completed green, including TypeScript, formatting, Ecotone gameplay, and four full contract-test shards. The new permanent suite simulates 1764 seeded journeys across 3 events, 7 lenses, all archetypes and six strategies per entry, verifies 566 result branches including 206 forced failures, 5540 real successful and 4145 real failed rolls, earned callback provenance and save/reload. It checks 1236 unique concept-art briefs and adds 3 missing event-choice illustration slots. No production deployment, art-generation job, public release or historic Wiyot/Tuluwat content approval performed. t-042 separately owns the production art ledger and generation; human pacing and creative acceptance remain outside this automated QA completion.
<!-- note:end t-050 -->

## t-051 — Fourth pass: six distinct failed-roll echoes across the regional chapters

<!-- note:begin t-051 -->
Silas-directed follow-up to t-050, 2026-10-20 PT: one intentionally interesting failed investigation per chapter across the six-region Ecotone journey. Strengthen the prose where needed, keep source JSON and the six chapter reading kits exactly synchronized, and give failed rolls meaningful, non-fabricated downstream finale callbacks. Each setback retains agency and consequences distinct from success; no failure should grant the winning evidence or be a disguised success. Include source-linked independent art prompts for each result and consequence, plus deterministic forced-roll and callback provenance tests. Do not interfere with separately claimed t-042 generated art or change historical Wiyot/Tuluwat consultation and publication gates.

Fourth-pass implementation staged on Kind Robots branch worker/weird-humboldt-t-051-failure-echo-29b. One grounded failed investigate result rewritten in each of six regional chapters, all six editorial chapter documents synchronized, six opt-in earned finale callbacks with distinct art moments, and explicit failed-branch art prohibitions with automated provenance tests. Awaiting complete GitHub CI.

Merged Kind Robots PR #3976 as commit 1f12e1a5dc8ecf1c7546de44bd7980fbcae1fe10 after all 13 exact-head Actions checks passed, including Ecotone gameplay, TypeScript, changed-file Prettier and all four contract shards. Rewrote the failed investigations WH-014, WH-026, WH-052, WH-074, WH-094 and WH-114 across the six regions. Synchronized six chapter manuscripts including failure art descriptions, authored six new earned future callbacks and art briefs, prohibited fake success imagery in failure-echo art pitches, and tested every new callback for provenance and absent-flag exclusion. The game suite passed 1764 end-to-end seeded journeys with 566 tested result branches including 206 forced failures, and 1242 unique editorial art briefs. No new ArtJobs, production deploy, Wiyot/Tuluwat publication or final creative acceptance was performed. Art production remains with separately claimed t-042.
<!-- note:end t-051 -->

## t-052 — Submit six failed-roll finale consequence pictures through durable YAML backup

<!-- note:begin t-052 -->
2026-10-21 PT, Silas says keep developing Ecotone and asks whether the established YAML backup can submit art prompts. Use the actively consumed projects/art-prompts.yaml requests queue for six NEW investigation-failure future callback illustration slots added by kind_robots PR #3976, one per chapter. These scenes are additional to the 237 card/outcome/ending subjects already owned by t-042; do not edit t-042's four-style art ledger or duplicate submitted ArtJobs. Use conditional provenance-bearing unique image paths, concrete diffusion-friendly prompts with canonical local scenery, and submit only through the existing queue with no code deployments, external publishing, or history-tribal gated scenes. Verify the workflow accepted the entries, distinguish queued from rendered, and leave images pending if render box unavailable.

Authored six Krea 2 callback illustrations as durable pending requests in projects/art-prompts.yaml on branch worker/weird-humboldt-t-052-art-yaml-20261021-a39c. Unique render paths under public/images/ecotone/failure-echoes and scene-grounded prompts depict only the earned failed rolls in WH-014, WH-026, WH-052, WH-074, WH-094 and WH-114. Existing t-042 four-style ledger and all prior ArtJobs are untouched. No ArtJob claimed or rendered; awaiting PR CI and merge to activate Auto Art Generate trigger.

Merged Conductor PR #6451 at 1f7e8da285e44c0eb598790d3d4fa45bda54a66b after all exact-head CI workflows green. Added six uniquely keyed pending Krea2 art requests for WH-014, WH-026, WH-052, WH-074, WH-094 and WH-114 earned failed-investigation future callbacks to projects/art-prompts.yaml. Only additive YAML rows; existing art jobs and t-042 four-style ledger untouched. The merge triggered Auto Art Generate run #39565956764. Render box and Kind Robots API health both passed, and the workflow reached its live 'Submit + wait + verify art requests' step. Actual ArtJob IDs, finished images and successful file deliveries are NOT yet verified; the six requests remain durable and retriable in the YAML queue. No production deploy or history consultation/publishing gate crossed.
<!-- note:end t-052 -->

## t-053 — Fifth editorial pass: sixteen pivotal scenes, sharp voices and costly choices

<!-- note:begin t-053 -->
Explicit user authorization 2026-10-21 PT: deepen 12-20 pivotal Ecotone scenes across all six regional chapters, the three opening event contexts and the four main companion viewpoints. Rewrite 16 canonical pressure, dilemma, result, and care beats to replace repeated bureaucratic closure with sharp dialogue, humor, surprising character agency and earned losses. Where appropriate, add optional third choices carrying genuine cost or a check rather than pretending every encounter has a binary solution. Keep the regional JSON, editor-facing chapter reading kits and provenance-specific illustration pitches synchronized; preserve intentional continuity, outcome flags, Wiyot/Tuluwat consultation and publishing gates. Regression-test representative costly third choices and rerun adversarial full-path gameplay; do not overlap separately claimed art standard (t-042) or kinetic-course task (t-044).

Fifth-pass implementation staged in kind_robots branch worker/weird-humboldt-t-053-editorial-20261021-c8f4. Sixteen rewritten regional encounter pressures, investigation win/losses and care outcomes across six chapters, mirrored to all six editorial kits; six costly optional third choices (four checks with distinct failed outcomes), conditional returning flag-lines, sixteen unique actual-lead reactions at four pivot scenes, tests enforcing paid choices and no fake companion, and a focused human editorial review packet. No generated art jobs, deploy, public release or Wiyot/Tuluwat consultation gate crossed. PR tests next.

Merged Kind Robots PR #3985 as commit e34793a18c994706acaf448bb9f61c20021305e9, after all 13 exact-head GitHub Actions workflows succeeded, including all four Contract Tests shards, TypeScript, Prettier and Ecotone gameplay. Rewrote 16 pivotal regional encounter pressures, successful and failed investigations and care outcomes, with exact synchronized chapter kits. Six costly third-way options include four checked outcomes with genuine alternative failures and downstream flag-lines. Four pivot scenes feature sixteen authored Mara, Kit, Juniper and Cedar asides gated on the actual traveling guide, plus regression tests and a human editorial packet. Dedicated Ecotone QA passed 1764 seeded journeys, 576 result branches (210 forced failures) and 1252 source-backed unique editorial art briefs. No generated ArtJobs, deployment, public release or Wiyot/Tuluwat gate approval performed. Production art standard t-042 remains separately claimed.
<!-- note:end t-053 -->

## t-054 — Editorial Ecotone art rerolls and live delivery tracking

<!-- note:begin t-054 -->
Owner asked 2026-10-21 PT to edit and submit the Ecotone art. The 237-subject, four-lane standard already contains 948 ArtJob IDs, so never reset or duplicate those requests to repair an all-PENDING reporting ledger. Editorial round 1 revises 15 independent safe card/result/ending scenes (60 additional private art variants) with clearer visual cause/effect, recurring race-machine identity, four genuinely distinct styles and a no-lettering composition. Wire the existing six-hour art workflow to enqueue these missing revisions, refresh real delivery status for both ledgers, and validate privacy, original job integrity and cultural exclusions before submission. Exclude held WH-121, Mara-specific Indigenous imagery, Wiyot/Tuluwat history and sacred designs. Distinguish requests submitted from actual completed renders. Visual curation and integration remain a separate review step; human final release and cultural consultation gates remain unchanged.

Editorial Ecotone art reroll and status pipeline shipped on Conductor PR #6466, merged as 613d58ae3ca85274145492485d52282b1bd5a23f after all six checks green. Original 237 subject x four style ArtJob IDs (948 unique requests) preserved. Authored 15 culturally independent, specifically retouched scene prompts x four distinct private style lanes (60 more requests) plus pre-submit safety validator. The merge started Auto Art Generate run #39586689813, and its "Submit private Ecotone editorial art revisions" step finished successfully. The workflow's subsequent --status pass reconciles queued versus rendered images; do not represent either batch as accepted visual keepers, integrated or publicly published. Held WH-121 and Mara/Wiyot/Tuluwat content was excluded from new art generation. Human image curation and cultural consultation gates remain open.
<!-- note:end t-054 -->

## t-055 — Seventh editorial/playtest pass: sober evidence, earned setbacks and lasting route callbacks

<!-- note:begin t-055 -->
Owner 2026-10-21: continue editing and playtesting Ecotone for dramatic and enjoyable failures, genuinely compelling sober play, companion personality, and nontrivial decisions. Scope this iteration to untouched Green Ribbon and Quiet Way fixed-story beats; improve consequences with flags echoed at later beats, without rewriting card/choice IDs, save format, or art keys. Add deterministic seeded playtest assertions for success/failure and sober continuity. Avoid the t-042 art and t-044 Kinetic ownership, and all held Wiyot/Tuluwat-dependent material. Finish as a small green PR.

Round-seven non-sensitive editorial patch on working branch: rewrote Green Ribbon loop setbacks and their closing-fire memories, Quiet Way elk failures and their later cabin memories, and river restoration outcomes. Preserved all stable IDs, rolls, art slots, and the cultural hold. Added 200-campaign sober-path contract witnesses and a written editorial playtest dossier. Merge only after all checks pass; no new art jobs submitted.

Merged Kind Robots PR #4009 as 8d1e206483dc208317cbe61c69bb8f8bd426228d. All 13 PR workflows actually completed successfully, including Ecotone Gameplay Contract, TypeScript, format, and all four contract shards. Editorially revised three fixed-journey story sequences, providing meaningful failure stories, independent sober evidence, real human-scale restoration, and saved flags whose later bonfire/cabin asides only appear if earned. Added a reproducible 200-full-campaign sober Quiet Way playtest contract and forest-loop failure tests. Did not modify the art pipeline, Wiyot/Tuluwat-held material, core signature count, saves, choice IDs or stable art keys. Future human-paced editorial and visual QA remain separate.
<!-- note:end t-055 -->

## t-056 — Eighth editorial pass: playtest consequence costs and reactive guide voices

<!-- note:begin t-056 -->
Owner 2026-10-21: implement changes in response to the seventh editorial playtest. Improve green-ribbon ending and Quiet Way choices by cutting repetitive paperwork beats, making a few failed checks genuinely costly, retaining non-moralizing solo/sober options, and giving present companions distinct reactions to the *actual outcome* of a choice, not only entrance lines. Add seeded regression tests for consequence text, no phantom guides, failure costs, and saved replay. Scope excludes Wiyot/Tuluwat review-held cultural material, art tasks t-042, Kinetic course t-044, optional shared-route infrastructure t-045, and public deployment.

Prepared an eighth Ecotone editorial iteration on a working branch, with a genuine disputed forest land-use finale and non-free failed rolls. Introduced source-compatible optional outcome-specific reaction text for the guide actually present or the solo player, then authored voices for all outcomes of GR-5 and QW-5. Added timed sober investigation callbacks, credible stream restoration stakes, deterministic contract witnesses and editorial documentation. Preserved card and choice IDs, art keys, run-state schema, and all cultural and deployment holds. Merge only after complete green CI.

Merged Kind Robots PR #4011 as f9e7190c1a5ca595a55237aff9177cbc2643e767, after all 13 PR workflows completed successfully including TypeScript, all four contract shards plus verifiers, Ecotone Gameplay Contract, format and layout. Revised Green Ribbon finale to a real forest-access versus restoration dispute with credible competing interests and consequences that include lost trust, and rewrote quiet investigation failures with nerve costs and earned future callbacks. Added the optional Outcome.leadLines engine integration to voice present-companion successes/failures and solo reflections; the six pivotal final choices have five distinct voice responses per result. Added deterministic assertions for outcome voices, absent guide gating, failures and sober continuity, plus editorial notes. Existing art keys, save state, card IDs and choice IDs remain unchanged. No Wiyot/Tuluwat held content or art jobs changed and no deployment claimed.
<!-- note:end t-056 -->

## t-057 — Ecotone P0: make seven advertised origin perks genuinely playable

<!-- note:begin t-057 -->
Triage 2026-10-22 PT: content.ts advertises seven origin-specific powers that the reducer does not track or consume; the front end displays the promises. Implement visible and replay-safe limited-use actions for each archetype (once per chapter where specified), including spent-state tracking and old-save compatibility, or remove any promise that cannot be supported. Seven origin witnesses, cap enforcement and save/reload tests required. No cultural-history changes, public deployment, or art workstream edits. Source: PLAYSTYLE-TRIAGE-2026-10-22.md.

Implemented seven individually functional player-invoked origin perks on worker/weird-humboldt-t057-origin-perks-a83f21. Includes once-per-chapter spend, visible player control and in-character consequences, safe version-4 save restore, and seven-archetype seeded witnesses. Waiting for CI, formatting and code review; no outward-facing deployment or excluded content changes.

Completed and merged Kind Robots PR #4049 as 0f48614e373e4d37d94e21873687832560216f9e. All 15 latest-head workflows completed and passed, including Ecotone Gameplay, TypeScript, changed-file Prettier, all four Contract Tests shards and their verifiers, and Layout. The seven origin actions are selectable once per chapter, have distinct mechanical consequences, and preserve legacy version-4 saves. No art or excluded content changed. Production deployment not claimed.
<!-- note:end t-057 -->

## t-058 — Ecotone P1: consequential mid-story decisions change later playable options

<!-- note:begin t-058 -->
Triage 2026-10-22 PT: mechanical ending divergence is not enough. On fixed non-sensitive route beats, create two genuinely consequential choice pairs per opening event whose successes/failures lead to different subsequent playable options or negotiated trade-offs, rather than only stats, flavor asides or finale callbacks. Document source flags and reproducible paired seeds; guard saved games and solo agency. Coordinate ownership with claimed t-003 (regional encounters) and t-044 (Kinetic race) to avoid editing their in-flight material. No extra WH-ID dump. Source: PLAYSTYLE-TRIAGE-2026-10-22.md.

Scoped Green Ribbon forest-loop consequence implementation: GR-4 seam success/failure unlock different GR-5 negotiation actions, with reducer/UI gating and seeded save tests. Kind Robots implementation PR pending exact-head CI; t-058 retains other opening routes.

Merged Kind Robots PR #4217 (5ecd732c) for the first Green Ribbon causal pair: GR-4 seam success/failure unlock distinct GR-5 negotiations. All 13 exact-head workflows passed, including four contract shards, Ecotone seeded adversarial journeys, formatting, and TypeScript. Remaining: second Green Ribbon pair; two Quiet and two Kinetic pairs; full from-new-game witnesses; dedicated art jobs. Master issue kind_robots#4145 comment 6414310883.

Scoped second Green Ribbon causal pair implemented on Kind Robots worker branch: GR-4 slug glade discovery versus rescue-marker failure unlock separate GR-5 negotiated tradeoffs, with seeded reducer, forged-choice, save/restore and from-new-game witnesses. PR and exact-head CI pending; Quiet and Kinetic remain.

Merged Kind Robots PR #4231 at 80751ce3eed16ecc631635604be1910886e62e00: second Green Ribbon causal pair, GR-4 slug success loop_glade_music versus failed rescue loop_exit_marked, unlocking separate checked GR-5 negotiations and persistent outcomes. All 13 exact-head workflows passed, including 1764 Ecotone seeded journeys, both authentic new-game witness routes, forged-choice rejection and save/restore. Master issue kind_robots#4145 comment 6416923879. No ArtJobs or deployment. Still required: Quiet and Kinetic causal pairs, dedicated scene art, broader adversarial routes and UI/device QA.

Scoped Quiet Way ranger success/failure causal pair implemented on Kind Robots worker branch: copied log or follow-up safety incident unlocks separate QW-5 checked stewardship options, with genuine seeded from-new-game witnesses, anti-forgery, and save/restore tests. Awaiting PR and exact-head CI. Remaining Quiet road pair and Kinetic pairs keep t-058 active.

Merged Kind Robots PR silasfelinus/kind_robots#4233 at e12386e6e3a19351f10f5a5bc19546f0a735c527. Quiet Way QW-2 bench success/failure now unlocks mutually exclusive QW-4 checked stewardship options, with four distinct results and QW-5 callbacks. All 13 exact-head workflows passed, including 1764 Ecotone seeded journeys, 200 genuine new-game branch witnesses, TypeScript, formatting and four contract shards. No ArtJobs or deployment. Remaining t-058: second Quiet road/photo pair, two Kinetic pairs coordinated with the separate claimed owner, and dedicated outcome art and visual QA. This task remains ready, not done.

Quiet Way second causal pair implemented on worker/weird-humboldt-t-058-quiet-road-k0v37s: QW-4 road success/failure changes QW-5 monitoring plan, with distinct checked tradeoffs, companion/solo dialogue, and 300 fresh seeded witness journeys. PR and exact-head CI pending; Kinetic and dedicated art remain.

Merged Kind Robots PR #4235 at e06230c31e1c9eab5058c7d77a2b78d7f5078c01. Second Quiet Way causal pair: QW-4 coast-road success now records elk_road_tracks_vanished; its failed future-photo history remains elk_future_photo. QW-5 monitor preserves all four saved choice IDs but offers distinct wildlife corridor survey vs consent-based photo audit, each with checked success/failure, four-Saturday commitments, solo/companion dialogue, and persistent flags. All 13 exact-head workflows passed on f5cdf7cd4cbc0aead6510d9522f6a17f31bd18b8, including TypeScript, Prettier, four contract shards/verifier and Ecotone 1764 seeded adversarial journeys. 300 fresh Quiet journeys witnessed photo success seed 1, tracks success 5, tracks failure 8, photo failure 32; save/restore and solo paths passed. No ArtJobs or deployment. Still open: two Kinetic causal pairs coordinated with t-044, dedicated outcome art, broader UI/device and adversarial QA. Keep t-058 ready, not done.

Implemented first Kinetic causal pair on worker/weird-humboldt-t-058-kinetic-dot-r8f2: KN-4 Dot aboard versus chase-bike outcome unlocks mutually exclusive checked KN-5 rescue strategies, four persistent outcomes, KN-6 callbacks and 320 fresh-seed test witnesses. Awaiting exact-head CI and PR review; second Kinetic pair and dedicated art remain open.

Merged Kind Robots PR #4241 at 2314c801fa3f75547f2c1f9d471bf5187cac9de1: first Kinetic causal pair, KN-4 Dot aboard vs shore chase unlocks different checked KN-5 rescue choices, four persistent outcomes, KN-6 callbacks, consistent Dot location, and four reserved outcome art slots. All 13 exact-head workflows passed on 6fdc2dd724470c5b0e877558b77d451633b458d8, including TypeScript, formatting, all four contract shards and Ecotone gameplay with 1764 adversarial plus 320 new-game Kinetic journeys. Witness seeds: aboard success 1, aboard failure 2, ashore success 3, ashore failure 63. Master issue kind_robots#4145 comment 6426534150. No ArtJobs or deployment. Remaining: second Kinetic causal pair, real art, full UI/device and adversarial QA; task stays active.

Scoped second Kinetic causal pair prepared in worker/weird-humboldt-t-058-kinetic-finish-c7p4: KN-5 sinking vs upright crossing unlocks different KN-6 checked rescue compromises, with four persistent results, saved-game/solo/anti-forgery and seeded-route tests, plus four reserved art slots. Implementation PR and exact-head CI to follow.

2026-10-26 PT: Merged kind_robots PR #4243 (squash cb95fb30241873122ff100d1c0ee26f74ba65fbe). Completed the second Kinetic causal pair: KN-5 slug_sank vs upright crossing unlocks mutually exclusive KN-6 shared-wheel repair vs marshal-approved tandem tow, each with a checked success/failure, meaningful finish cost, four durable flags and solo/companion dialogue. Preserved original three choice positions and versioned saves. All 13 exact-head GitHub workflows passed at 0e91b2019bc77c71576f9b620b42394eddd8f94b, including TypeScript, formatting, Ecotone Gameplay Contract (run 40399980052), and four contract shards (run 40399980283). Genuine 320 Dot plus 360 original-bay new-game journeys; witnesses upright failure seed 1, sunk success seed 2, upright success seed 4, sunk failure seed 13. 1764 seeded Ecotone journeys. This closes all six P1 causal pairs across Green Ribbon, Quiet Way and Kinetic. Four KN-6 outcome art slots are reserved but NO ArtJobs submitted/rendered; art completeness remains with t-042 and master issue #4145, along with wider editorial/adversarial and device UI QA. No deployment or human gate.
<!-- note:end t-058 -->

## t-059 — Ecotone P1: earned hopeful and bittersweet solo ecotopia repair path

<!-- note:begin t-059 -->
Triage 2026-10-22 PT: computeEnding currently uses only wild >= 4 to determine Quiet Way solo fate. Assess whether a player who makes three animal-first choices and then completes a costly, concrete ecological restoration can earn an active hopeful future without trivializing the intentional hermit/inaction ending. If so, implement a narrowly authored alternative with correct flags, outcome art keys, 7-lens reachability, tested hope/dark routes and save compatibility. Avoid ideological or sobriety morality bonuses. Source: PLAYSTYLE-TRIAGE-2026-10-22.md.

Implemented optional four-Saturday creek-monitoring commitment in Quiet Way, with a true roll and distinct success/failure costs, two outcome art slots, future callbacks, and earned one-credit Wild Way restoration scoring that preserves all seven lens/end IDs. Rewrote inaccurate dark epilogue generalization. Dedicated deterministic seven-lens/roll witnesses and save compatibility test on Kind Robots branch worker/weird-humboldt-t059-creek-commitment-c62f4a. Awaiting CI.

Implemented and merged Kind Robots PR #4052 as e12ba035924b2484df3937db911937af9d19fe75 after all 13 final-head GitHub workflows finished green (including Ecotone Gameplay Contract, TypeScript, changed-file Prettier, four full contract shards + verifiers). Quiet Way now has a fourth costly, checked volunteer monitoring commitment, distinctive failure, honest callbacks and an earned restoration-credit path to the same collectible solo endings. All seven lenses, saved games and art slots tested. No deployment, public release, image generation or excluded content changes claimed.
<!-- note:end t-059 -->

## t-061 — Add chapter-anchor scene schema to the card validator before authoring the six anchors

<!-- note:begin t-061 -->
Kaizen from #6533 review: extend validate_weird_humboldt_cards.py with a chapter-anchor scene schema check (one anchor per chapter, authored text, no-dead-end rules) so anchors are validated from their first commit.

Implemented stricter chapter-anchor validation and five adversarial regression tests on worker/weird-humboldt-t061-anchor-schema-b8e7. CI verification and PR merge pending.

Merged Conductor PR #6662 (2a56c81154624130f22396af2fe5b4ee590679c4) after all 8 Worker PR CI jobs, Security Audit and handoff checks passed on head 1fa98a9e578b85f8b5b40be2b3ae1ce41ed0219c. Python 3026 passed, 53 skipped. Five regression tests cover authored anchor schema, no-roll stay/follow and rolled failure routes. Ecotone master roadmap issue 4145 comment 6409288958. No ArtJobs or deployment.
<!-- note:end t-061 -->

## t-062 — Mysteries: twelve once-per-run local cases, three gates, true path, Real Endings and Case Files

<!-- note:begin t-062 -->
Silas, 2026-10-23 PT, in session: "a singular opportunity that occurs once a game to pursue a random local mystery" — twelve cases modeled on the zodiac without naming it ("unless it's buried in something like 'The mystery of the virgin sacrifice'"), fresh stories in Humboldt's backwoods and underbelly, "a college aged Scooby Doo vibe", unique Mystery cards with a hint of each sign in the art, a Case Files screen showing which mysteries were uncovered and which gates passed, about three gates per game told as digressions, two passes for the true path, and a final choice tree to Real Endings. Design and roster: MYSTERIES.md.

Implemented in kind_robots PR #4082 (branch claude/youthful-carson-7vs0zk): utils/ecotone/mysteries (types, compiler, validator, seeded pick preferring unopened cases, gate interludes before the first fork / crossroads / finale that keep route indexes and save v4 stable), twelve authored cases (84 scenes, 36 Real Endings), Case Files tab and ledger, code-drawn zodiac-hinted Mystery cards, digression message bubbles and Real Ending framing; verifyEcotoneMysteries contract in the Ecotone Gameplay workflow. Twelve Krea 2 card-art requests queued in projects/art-prompts.yaml (queued, not rendered).

Merged kind_robots PR #4082 as bffcc9cf2eb2ccdf91f616b8e8a0b85f7b10589c after all 21 exact-head checks green (Contract shards 1-4, TypeScript, layout-contract, Changed-file Prettier, Ecotone Gameplay incl. test:ecotone-mysteries). One CI fix along the way: the capture-group guard flagged an unguarded match index in the case validator (4c6e1cc). Merge is not deploy: live after the next Alexandria deploy. Card art is queued, not rendered. Follow-ups noted in MYSTERIES.md (Playbook Manager listing, scene art, true-path balance after real play).
<!-- note:end t-062 -->

## t-063 — Mysteries: Playbook Manager scenes, 336 art requests, and a blind pass/fail playtest of all twelve cases

<!-- note:begin t-063 -->
Silas, 2026-10-23 PT: "add the mystery scenes to the Playbook Manager, submit art requests, playtest mystery interactions, and the originality and 'funness' of the experiences, pass or fail."

kind_robots PR #4087: utils/playbook/ecotoneMysteries.ts (120 Playbook nodes, 12 Collections, live edits reach mystery cards); missed-trap reveals (reveal.afterMiss), approach memory and recall lines so gate results carry forward, validator rules for them; transcript tool; all twelve cases rewritten through three rounds of blind playtest. Final grades: 12/12 cases PASS, set originality/culprits/mechanics/companions PASS (MYSTERIES-PLAYTEST.md). Browser click-through on the final text passed (true path via missed trap to a Real Ending, cold case, ledger, zero page errors). Art: art/MYSTERIES-ROUND-1.yaml, 336 Z-Image subjects (every scene card, gate outcome and Real Ending), auto_submit, live prompt contract 376/376 — queued on merge, not rendered.

Merged 2026-10-24 PT: kind_robots #4087 squash d928b45bd4cce9df7f4d96c62a3addeb3d5d5b78 (all 20 checks green, including the Ecotone mysteries contract). Open, not blocking: Silas's editorial read, culprit gender skew (11 of 12 women), optional Case VIII pun title.
<!-- note:end t-063 -->

## t-064 — Mysteries: vary the culprit genders across the twelve cases

<!-- note:begin t-064 -->
Silas, 2026-10-24 PT: "vary the culprit genders across the twelve cases".

On the final t-063 text the person under the mask was a woman in eight cases (the "11 of 12" in the playtest record was stale), three men, one couple, and every man under a mask was a wrongdoer. Three sympathetic culprits change: Case I Bev Ostrander -> Hollis Ostrander; Case IV the widow Ione -> the widower Arne Sorensen (the yellow oilskins are Ione's, so the ghost still reads as hers); Case IX Dr. Wren Okonkwo-Barlow uses they/them, with no commentary (ending "The Arrow That Points at Wren", id unchanged). Result: five women, five men, one nonbinary, one couple; wrongdoers three men, two women. Plot, clues, gates, ids and effects unchanged; validator, test:ecotone-mysteries and test:playbook pass. Culprit-depicting art briefs in art/MYSTERIES-ROUND-1.yaml re-briefed and resubmitted (old job ids kept as superseded_jobs).

Merged 2026-10-23 PT: kind_robots #4088 squash ecb889605e8dd78a90c4106c02d6f0e9961896f4 (all 17 checks green). The 19 new art prompts are queued by the next Auto Art Generate sweep; queued is not rendered.
<!-- note:end t-064 -->

## t-065 — Create 12 coherent player-avatar portrait ArtJobs and wire character selection

<!-- note:begin t-065 -->
Silas explicitly approved 12 full character-select portraits for Ecotone and instructed us to submit them to the GitHub-backed art queue (October 23 2026 PT). Match the 12 persistent PLAYER_AVATARS IDs, generate coordinated painterly 2:3 images through the existing Conductor ArtJob pipeline with private traceable prompts, and replace emoji-only onboarding selection with responsive image-first cards, retaining accessible labels and missing-image fallbacks. Verify deduplication, durable submission, UI mapping, and CI.

Submitted 12 idempotent private Krea 2 portrait art requests under canonical public/images/ecotone/avatars/<saved-avatar-id>.webp paths in Conductor projects/art-prompts.yaml; authored matching image-first Ecotone onboarding player selection cards and 12-identity regression checks in kind_robots. Pending exact-head CI, art-queue workflow submission, and UI review.

Merged Conductor PR #6585 (0647ea1742e233c9f77d94b2f7ee1c41408dad5c): 12 distinct private Krea 2 512x768 portrait requests committed to projects/art-prompts.yaml without deleting any previous entry, keyed to stable ecotone/avatar IDs and self-hosted media paths. GitHub triggered Auto Art Generate run 40072994485; at last inspection it was still sweeping earlier art ledgers. All 12 requests remain pending with no last_art_job_id assigned yet. This is queue submission, NOT proof of rendering or final delivery. Merged kind_robots PR #4108 (710887a8e966213e92508a931e5884c5ca4c67b9) after all 15 final-head CI checks passed. Onboarding uses responsive swipeable portrait cards, image-error fallbacks, stable saved identities and path/selection regression tests. Both working branches cleaned. No production deploy or image-render completion claimed.
<!-- note:end t-065 -->

## t-067 — Grep Ecotone docs for the withdrawn Mara tribal/casino-grant backstory and correct leftovers

<!-- note:begin t-067 -->
Kaizen from t-009 (#6640): COMPANION-OPTIMAL-PATHS.md carried the stale backstory; other docs, cards or art prompts may too. Search projects/weird-humboldt for tribal, casino, grant, Indigenous-tattoo wording tied to Mara and fix per EXCLUDED-CONTENT-2026-10-22.md. Text only.

Corrected current Mara bio in three Ecotone design documents, flagged withdrawn Mara ArtJobs 40846/40847 and checkpoint candidates as noncanon audit-only, and added a regression test. PR and CI verification in progress.

Merged conductor PR #6664 (742c0f3a6adf3da1965851a25237c3eb1f2e1d18). Removed obsolete Mara biography from active Ecotone docs, flagged original portrait ArtJobs 40846/40847 and checkpoint jobs 40884-40891 as noncanon provenance, and added tests. All 23 exact-head checks completed successfully, including full Python suite; no ArtJobs generated and no deployment. Master issue master issue 4145 comment 6410038612 tracks replacement-art/export follow-up.
<!-- note:end t-067 -->

## t-069 — Playbook Forge upgrade: literal prompts for all 254 unpainted Ecotone beats

<!-- note:begin t-069 -->
Silas, 2026-10-27 PT: "Anything that is in playbook forge and has quests unwritten or art prompts unwritten should be upgraded. (Memory dungeon will take the longest and should be last). Space couch has a lot of fresh writing still in need and still looking to capture that right blend of space comedy and satire. All art prompts should be written for the appropriate engine, no metaphors for krea2." Shared bar: kind_robots PR #4308 (verifyPlaybookArtPrompts, artPromptsComplete). Forge 2026-10-27: 254 unpainted beats have no prompt surfaced to the Forge. Never anthro; Ecotone renders in four styles. The ending gap (45/56) stays behind the t-004 creative review and t-020.
DONE 2026-10-27 PT: kind_robots #4310 merged as 2cb1e80 after 19/19 checks. Forge: ecotone complete, needsArt=254 prompted=254 failing=0, artPromptsComplete on. 249 prompts ported from art/ART-STANDARD-ROUND-2.yaml by asset key (about 110 rewritten to remove similes, negations, mood tails, text props and animal clothing); 5 consultation- held beats authored without showing Mara. Endings 45/56 stay behind t-004/t-020. Prompts only; no ArtJobs queued.
<!-- note:end t-069 -->
