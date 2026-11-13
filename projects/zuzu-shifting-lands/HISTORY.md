# zuzu-shifting-lands — task history archive

Full `note:` prose for completed zuzu-shifting-lands tasks, moved out of `roadmap.yaml` so the
Kind Robots projection payload (`scripts/sync_kind_robots_projection.py`, hard limit
4,000,000 bytes) stays well clear of its ceiling. See conductor/t-158.

Each note below is the **verbatim** original — nothing is summarized or trimmed. The
`roadmap.yaml` task keeps its own first sentence plus a pointer here. The HTML comment
markers delimit each note exactly; `archive_done_task_notes.py --verify-only` re-extracts
every note and checks it byte-for-byte against what the roadmap recorded.

## t-003 — Build typed, versioned world/resource and encounter manifests

<!-- note:begin t-003 -->
Encode 5 lands, three location encounters each, land boss slots, source- verified art refs, ecology, named exceptions, species vs occupation vs disposition/secret vs scenario vs reward. Validate schema and ensure in-game player-facing data reveals lore at the intended moment, not from a prematurely visible card. The source game manifest should not duplicate world Book One or import LLM filler as canon.

Implemented v2 authored five-land world contract with verified repository-art pointers, typed Facet/Scenario/Reward refs, spoiler-safe player projections and CI tests on worker/zuzu-shifting-lands-t003-world-contract-20261009-b7e9. Reviewing and running contract checks before merge.

Merged Conductor PR #5838 (438ab15) with WORLD-DECKS.json v2, typed contract, verified source-file art pointers, validated independent Facet/Scenario/Reward design refs, spoiler-safe public DTO and dedicated Node contract tests. Final head passed Shifting Lands Manifest Contract, Security Audit, Worker PR CI, process-task-events, and Worker PR handoff checks. No production deployment or live resource imports performed.
<!-- note:end t-003 -->

## t-005 — Kind Robots: create private preview route, project registration and illustrated board shell

<!-- note:begin t-005 -->
/admin/zuzu-shifting-lands with a visible Admin-channel tab, requiredRole ADMIN, and a correct Zuzu World Studio link until Silas accepts; never locate an admin-only page under /play or Projects navigation. Use store-owned state/API; root-first Nuxt conventions. World map and three-card encounter strip are image-heavy with re-used locked/cross-project visuals, inspectable art provenance and error/placeholder handling, and navigation links to World Studio.

Admin-only Homestead board shell, Admin nav channel, and World Studio link merged in kind_robots PR #3400 (4c3e994); all 33 head workflows passed. This covers the scoped private preview shell, not five-land gameplay or deployment. No public release.
<!-- note:end t-005 -->

## t-006 — Pure seeded journey reducer, five land/three encounter traversal and boss gates

<!-- note:begin t-006 -->
Full board route graph with exactly five land challenges and 3 encounter resolutions each; deterministic seeded draws, stable location mutations, journal, game over, win/retire, stat/health checks and testable transitions. No play-time untrusted LLM permitted to decide state.

Implemented Kind Robots five-land journey reducer on worker/zuzu-shifting-lands-t006-journey-20261009-f83c: manifest-v2 generated geography snapshot, deterministic 15 encounters, causal tile shifts, traversal history, five boss gates, full replay, terminal states and guarded restore. Homestead saves intentionally unchanged. Preparing CI-gated PR.

Merged Kind Robots PR #3406 as b2723c4 after 28/28 completed passing GitHub workflows. Pure deterministic five-land reducer: 15 encounter locations, independent seeded map layouts, replayable dice/skill outcomes, causal prospective shifts with history preservation, five boss trials, win/fallen/retired endings, source-blob-pinned safe geography snapshot, strict restore validation and multi-seed balance regression tests. Existing Homestead v2 saves and admin UI are unchanged. Clean scoped formatting pass applied and temporary workflow removed; no production deployment claimed.
<!-- note:end t-006 -->

## t-007 — Authored fixed-cast encounter pack schema and first-land sample content

<!-- note:begin t-007 -->
Versioned authored encounter schema and 12 Homestead sample scenes:
four good/bad/mixed options per each of three canonical locations,
fixed illustrative cast, flavor text, 2+ dice choices and written
outcomes, deterministic pool selection and CI tests. Revise old
species x role direction and hand off integration tasks for the board,
card backs, save/replay, art and visual acceptance.

Applying Silas's newer authored-encounter direction: replace independently rolled species and jobs with predetermined illustrated cast per encounter; design the schema, twelve Homestead cards, and Conductor-ready implementation plan.

Authored 12 fixed-cast Homestead encounter cards (four per canonical location), each with a flavor paragraph, two checked choices and distinct success/failure text. Added Draft 2020-12 schema, deterministic seeded pool selection design validator/tests, ArtImage provenance guards, implementation order, current CONTROL override, and six source-owned Conductor follow-up tasks. Preparing reviewed PR and CI.

Merged Conductor PR #5865 (184e73f) after seven green head workflows including full Python suite, Roadmap Audit, Worker PR CI, Security Audit, and Shifting Lands Manifest Contract. Shipped authored encounter schema v1, 12 draft Homestead scenes (four per existing location), 24 distinct dice-checked choices and 48 written success/failure outcomes, fixed casting/art briefs with no invented live ArtImage references, deterministic pool contract/tests, project steering override and task-ready implementation plan. Source-only: no runtime migration, generation, deployment or publication. New t-019 through t-024 track gameplay/UI/art work, and t-018 human public-release gate remains intact.
<!-- note:end t-007 -->

## t-008 — Stats, dice/skill checks, HP, item/technique Rewards and companion relationships

<!-- note:begin t-008 -->
Implement original 2d6 check and consequence table with combat/noncombat options, character sheet, reward gating, inventory and persistent conditions; protect stat balance from infinite farming; reuse gamebook pure utilities where compatible, not its state machine.

Pure provenance-checked character progression and store projection are committed with a dedicated anti-farming/skill-check test. Existing v2 authored encounter dice and saved games remain unchanged; reward spending and applying earned techniques to live checks require the t-009 replay/save migration.

Merged Kind Robots PR #3486 at 95e0968 after all 29 implementation workflows completed successfully, including TypeScript, dedicated Shifting Lands progression contract and the repository-wide contract suite. Pure character sheet derives bounded learned skills, item Rewards, persistent authored injuries and named NPC bonds from verified saved outcomes, with anti-farming and eligible-use guards. No existing v2 roll was rescored and no save migration or production deploy was performed. Applying new perks to live rolls and persisting item spending is deferred to t-009; inventory overlay is t-016.
<!-- note:end t-008 -->

## t-009 — Safe versioned save/resume, pinned run seed, history and deterministic replay tests

<!-- note:begin t-009 -->
Durable, schema-versioned serialized run; preserve choices, hidden roles, map events, used Rewards, companion identity and both roll dice; reject corrupted saves; no re-roll by refresh.

Implemented isolated V3 event replay ledger, source-pinned seed and deterministic validation of card identity, dice, map shifts and spent Rewards, plus V2 save migration as an explicit legacy checkpoint. Private preview store now persists only V3 after migration and refuses rollback from invalid V3. Dedicated replay and board contract tests added; implementation PR and CI pending.

Merged Kind Robots PR #3499 as b8fd9f7 after all 29 completed green checks, including the Shifting Lands Gameplay Contract, TypeScript, repository-wide Contract Tests and Prettier ratchet. V3 source/seed-pinned save ledger replays exactly authored choices, dice, bosses, shifts and reward spends; V2 migration preserves legacy rolls as explicit checkpoints. New private board saves use V3; old key remains untouched; invalid V3 cannot silently fall back. No live deployed version, public publication or production schema change claimed. Companion/inventory UI remains t-016.
<!-- note:end t-009 -->

## t-010 — Author five land encounter decks, three locations each, alternate outcomes

<!-- note:begin t-010 -->
Author three or more whole fixed-cast illustrated scene identities per location with at least two checked choices and good/bad/mixed possibilities, including rescue/bargain/stealth/combat. Land one: Homestead, watering holes, roadside chapel and ambiguous hospitality. Cave witches in higher lands, gorilla encounters in high-tier. Do not misstate the Abbess agenda or invent causes for the lost-humanity mystery. Document existing lore in source; pace its reveal in game.

Authored all 36 later-land design-only fixed-cast scene cards with 72 distinct checked choices and 144 outcomes at twelve canonical locations. Each pool includes good/bad/mixed situations; art provenance and live resource IDs remain unverified and null. Added cross-land CI contracts, seed draw checks, causal prospective shifts and an explicit runtime V4 migration handoff. PR and CI review underway. New content is source draft, not yet playable.

Merged Conductor PR #5950 at 3c45f97 after six completed green workflows, including Shifting Lands Manifest Contract, Worker PR CI full pytest, Roadmap/worker handoff and Security Audit. Authored 36 later-land fixed-cast scenes across 12 canonical locations (72 checked choices and 144 outcomes), with 4 causal prospective route shifts and source-only visual art briefs. Complete source library has 48 cards at all 15 locations. Source status remains draft-not-imported; a separate Kind Robots runtime integration and V4 replay-compatible migration are still required before gameplay.
<!-- note:end t-010 -->

## t-011 — Boss encounters and alternative noncombat solutions for all five land gates

<!-- note:begin t-011 -->
Every land boss has a build-up and multiple earned outcomes, plus a failure state. The first land's major challenge centers on the convent/Abbess authority; the longstanding ritual motivation is openly documented in source; reveal it to players via earned clues.

Authored all five boss trial scenes with three choices each: combat, nonviolent terms, and unlocked evidence-led passage requiring actual earlier earned flags. Implemented V5 isolated action/replay ledger so prior V4/V3/V2 saves and their original rolls remain unchanged, plus private Admin reading interface and seeded regression checks. Kind Robots PR #3510 open for repository-wide checks and review. No public publishing, paid art, migrations or deployed UI claimed.

Merged Kind Robots PR #3510 as 77f435f after all 30 GitHub head workflows succeeded, including TypeScript, Shifting Lands Gameplay, and the repository-wide 475-step Contract Tests with ESLint/Prettier ratchets. Authored five 3-route boss trials: physical confrontation, a nonviolent bargain, and evidence-led alternatives requiring actual earned encounter flags. Recorded dice, success/failure passages, wounds, provisioning, progress and history in replay-verified V5 saves. V4/V3/V2 journeys retain their original reducers and saved rolls. No live deployment, public route, paid ArtJobs, schema changes, or bespoke boss illustrations claimed.
<!-- note:end t-011 -->

## t-013 — Reuse accepted Zuzu ArtImages and enqueue missing illustrated scene variants

<!-- note:begin t-013 -->
Prioritize custom Zuzu encounter/boss card backs from t-022; reuse image references/cast angles from worlds/zuzu ledger and World Studio ProjectArtImage links; create durable scoped ArtJobs only if missing; track queued vs rendered vs delivered vs verified. Observe mature/private rights and locked frame requirements.
2026-10-11 (Silas): the Zuzu character LoRAs are the default for Shifting Lands art. Give each new art ledger `series: zuzu-koala-assassin` and the Arthemy house lane; enqueue_art_requests.py then adds the right character LoRAs per subject (projects/comic-creator/cast-loras/zuzu-koala-assassin.yaml).
Done 2026-10-11 (kind_robots#3546): every one of 48 encounters, 15 roads and 5 trials now resolves to a hand-picked, git-tracked Zuzu Gamebook/Showdown illustration via utils/shiftingLands/sceneArt.ts (presentation only; authored packs keep art: null for t-023). Card backs moved out of /images (Alexandria mounts the media share over it, which hid them). Also fixed the unresolved NavigationFlipCard (components use pathPrefix: false) that left every drawn encounter blank. No ArtJobs enqueued; bespoke later-land paintings tracked as t-026.
<!-- note:end t-013 -->

## t-015 — Illustrated responsive hex/card board and current encounter reader

<!-- note:begin t-015 -->
Launch gate (spec: BOARD-CARD-ARCHITECTURE.md): genuine face-down stack, click-to-draw, animated deal, front/back persistent reveal, discard and inspect flows. Reuse existing KR visual card components without hijacking the Storybook run store, global navigation hand, or flipStore. Main board visual dominates screen at phone/tablet/desktop. Three current encounter cards with routes, full art inspector, location state changes, selected path and discovered history; mobile bottom sheet and keyboard/screen-reader usability.

Built private five-land illustrated board with state-owned travel/draw/discard, real NavigationFlipCard deals and kr-card-flip inspection, guarded boss and skill choices, browseable past-land history, responsive route cards and provisional source-backed Zuzu art. Separate Pinia store/local save preserves old Homestead. Opening CI-gated implementation PR for review; live visual acceptance and public route remain separate.

Responsive illustrated private Admin five-land board from superseded PR #3411 was fully integrated into merged Kind Robots PR #3424 (428d6b6). Preserved travel/deck/discard, prior visit inspection, playable location and boss controls, state-owned save, source-backed provisional scenery, keyboard-accessible choices, and Admin tab. Former PR #3411 closed as superseded. Dedicated flip polish, custom encounter faces, authenticated visual approval and public publishing remain separate tasks. All 33 source PR checks green; production deployment not independently verified.
<!-- note:end t-015 -->

## t-016 — Companion rail, inventory/skills overlay, dice/motion/sound and journey log

<!-- note:begin t-016 -->
Show specific named character relationships and Rewards without hiding art beneath CRUD controls; reduced-motion and mute settings.

Implemented illustrated character sheet rail, actual earned one-use inventory, history-grounded skills and injuries, named nontravelling relationships, journal filters and optional accessible dice cues. Presentation preferences are separate from versioned V5 ledger; no existing dice or save rules change. Kind Robots PR #3530 awaits all repository checks after successful scoped formatting. No public publishing, paid art or live production deployment claimed.

Merged 2026-10-11 via kind_robots#3546, which carried #3530 and repaired its two stale
contract regexes (attemptTrialWithCue rename; Prettier trailing comma in matchMedia).
Gameplay contract CI green. Merged != deployed: live after the next Alexandria deploy.
<!-- note:end t-016 -->

## t-019 — Make Shifting Lands persistent encounter flip readable

<!-- note:begin t-019 -->
Use KR kr-card-flip or scoped persistent face adapter, not NavigationFlipCard full 360 spin for reading. Reveal must rest face-up with legible prose, keyboard/touch, focus and reduced motion; animation callbacks never mutate game state.

After PR #3424 merged, harden the persistent Zuzu encounter reveal with predictable narrative reading focus, live-result announcement, reduced-motion support and no double transition from animation events. Keep Admin-only board, v2 saves and other KR flips intact.

Added keyboard/screen-reader reading focus to authored scene title after a newly drawn/traveled card and to saved result passage after a checked choice. Existing opt-in back-to-front animation still settles face-up; reduced-motion CSS and animation-only contract verified. Dedicated source guard tests; preparing PR and full CI. Public launch remains separate.

Merged Kind Robots PR #3427 at faa79a8f6bf9fc7615dff9d8a5e0bb3e0ae573b9 after 30/30 green checks. Authoritative read focus now moves to encounter title after a user-initiated card draw/travel, and to the persisted consequence paragraph after a committed authored dice choice. Existing stable face-up flip and reduced-motion CSS remain; invalid/double rolls do not refocus, animation events do not mutate state. Admin-only preview, saved games, and public release gate unchanged; Alexandria production deploy still unverified.
<!-- note:end t-019 -->

## t-020 — Integrate seeded fixed-cast encounter pools into pure journey reducer

<!-- note:begin t-020 -->
Import validated authored encounter pack with frozen species and occupation per card. Persist chosen encounterId, revision, seeded roll, choice, flags and outcome on explicit versioned save; preserve 15 location slots, five bosses and no reroll farming.

Implement seeded authored fixed-cast Homestead encounter pools, persistent meaningful choice rolls/outcomes and five-land private Admin preview integration. Preserve existing Homestead saves and public launch gate.

Integrated authored Homestead v2 source pack into an isolated playable five-land private Admin board: deterministic 12-card selection, fixed cast, full flavor and two checked choices, persisted roll/outcome/history and map effects, 2:3 custom card backs and stable face-up flip. Rebased green but conflicted prior t-015 PR into a fresh integration branch. CI/review ongoing; no public release or deployment asserted.

Merged Kind Robots PR #3424 at 428d6b685186ee1d37cb4038727326f0cc05a30e after 33 green checks. Playable private Admin five-land board with twelve deterministic authored Homestead cards, two checked decisions per card, persisted dice/flags/journal and isolated source-pinned v2 saves. Included Zuzu encounter and trial backs plus persistent readable reveal. Source merged; Alexandria container deploy not yet independently verified. Later lands retain prototype rules and encounter-specific face art pending.
<!-- note:end t-020 -->

## t-021 — Render authored flavor, two or more checked choices and outcomes

<!-- note:begin t-021 -->
Show a legible paragraph, distinct intent/risk/target for 2+ checked choices, reveal skill roll and separate written success/failure. Persist selected choice, dice, changed flags/resources and narrative in journal; prevent double-tap rolls or spoiler leaks.

Reconcile the authored encounter reader task against already merged Kind Robots PR #3424, with accessible story/result focus polished in #3427. Verify all first-land cards display flavor, at least two meaningful checked choices, persisted dice/outcome and inspectable journal without double resolution. Later-land bespoke packs remain t-010.

Authored Homestead reader already shipped in Kind Robots PR #3424 and focus polish PR #3427; source tests check two per-card dice choices, flavor text, result persistence, and invalid-action guard. Review complete; later-land content remains t-010.

Done by previously merged Kind Robots PR #3424 (428d6b6) with 33 green checks and PR #3427 (faa79a8) with 30 green checks. Twelve first-land encounter cards display authored flavor and two distinct skill/risk decisions, and the reducer saves exact dice, per-choice prose, flags and resource deltas without reroll farming. Separate readable keyboard focus and journal inspection tests pass. Four later lands still await bespoke content from t-010; new per-encounter face art remains t-023.
<!-- note:end t-021 -->

## t-022 — Create custom Zuzu encounter and boss card backs

<!-- note:begin t-022 -->
Produce source-tracked 2:3 illustrated Encounter and Boss/Trial backs with weird-west and Edo visual identity, iconography not reliant on color, reviewed at small size; no paid generation or public release without appropriate gates.

Audit the two source-backed bespoke encounter/trial SVG card backs already merged with playable PR #3424 for 2:3 geometry, distinct motifs at thumbnail size, accessible labels, safe local-only SVG and deck integration; finish only on satisfactory validation.

Reviewed first-draft bespoke encounter and trial source assets already merged in Kind Robots PR #3424: two separate 600x900 (2:3) SVGs with unique sun/katana versus moon/crossed-swords crests, Edo/frontier border ornament and legible silhouette geometry, intrinsic accessible titles/descriptions and no external or script content. Referenced by live-board source; encounter faces remain distinct pending t-023. Human visual approval and Alexandria deployment not asserted.

Completed source-backed Zuzu Encounter and Trial card backs shipped in Kind Robots PR #3424, merged as 428d6b6 after 33 green checks. Both 600x900 SVGs are authored with separate crest imagery, titles, accessible descriptions, safe local-only vector shapes and responsive 2:3 format; private board references them instead of generic card backs. Human taste-level visual vetting and actual Alexandria production deployment remain unverified; individual bespoke encounter faces are separate t-023 work.
<!-- note:end t-022 -->

## t-023 — Map twelve bespoke authored Homestead card illustrations

<!-- note:begin t-023 -->
Deliver or link approved per-encounter art matching each fixed cast, preserving source Image IDs and resource rights/rating/continuity. Clearly label pending assets, never invent live references or independently reassign species.
2026-10-11 (Silas: "keep working on future upgrades, 23 and 26"): art round 1 in flight, projects/zuzu-shifting-lands/art/ROUND-1.yaml, ArtJobs 37401-37504. Two Arthemy house-lane seeds per card for all 48 authored encounters and the four later trials, prompts from each card's fixed cast in encounters/*.json, so t-026 rides the same round. Keepers get `verdict: keep`, export with scripts/export_shifting_lands_cards.py to kind_robots public/shifting-lands/cards/<card>.webp and are listed in sceneArt.ts BESPOKE_CARDS. rest_until holds the claim while the shared render queue drains.
Done 2026-10-12: art round 1 (projects/zuzu-shifting-lands/art/ROUND-1.yaml) plus rerolls painted 51 of 52 Shifting Lands cards, two Arthemy house-lane seeds each, reviewed against each card's cast and brief and exported to kind_robots public/shifting- lands/cards (BESPOKE_CARDS). Shipped in kind_robots#3572 and #3586. A Road of Bones missed twice and deliberately keeps its reused bone-valley plate; the Homestead trial keeps the gamebook abbess-welcome plate.
<!-- note:end t-023 -->

## t-025 — Integrate four later-land authored packs with V4-safe replay into private board

<!-- note:begin t-025 -->
Import the 36 design-only fixed-cast encounter identities from encounters/DUSTWATER-9.json, TABLELANDS-9.json, STORM-CROW-9.json, and BLACK-VERGE-9.json into typed, validated player-safe Kind Robots manifests while preserving exact canonical location IDs, encounter identities, weighted seeded draw and source provenance. Upgrade the pure authored journey reducer to provide two distinct 2d6-checked choices with result prose/effects at each of the remaining twelve locations; remove prototype RESOLVE only for new-version runs. Introduce an explicit V4 saved-run/replay compatibility boundary: existing V2 and V3 checkpoints and later-land prototype rolls must remain reconstructible without rescore or surprise re-draw. Revisit cannot reroll or farm. Shift only unvisited places for source-authored reasons. Wire the existing private Admin board and persistent flip reader/journal to new fixed-cast cards with visibly pending art slots; no invented ArtImage references, public /play route, or paid art generation. Test all 15 location paths and five boss transitions, malformed-save rejection, old-run migrations and balanced seed distributions. Source packs are documented in encounters/LATER-LANDS-IMPLEMENTATION.md. Coordinate with t-011 for final named boss-story alternatives and t-016 for character/inventory UI; do not silently make those tasks complete.

Imported 36 source-pinned, player-safe later-land encounter cards and implemented separate V4 rules/replay, fixed draws, checked decisions, journaled outcomes and causal prospective shifts. Existing V3/V2 saves remain on original keys and reducers. Private Admin board gains V4 play, old V3 runs retain prototype later-land rules. Seed/property contract suite and all repo CI pending before reversible merge.

Merged Kind Robots PR #3506 as 3aea16a after all 30 head workflows completed successfully, including dedicated Shifting Lands Gameplay, TypeScript, Prettier/ESLint and repository-wide Contract Tests (473 steps). Imported 36 player-safe, source-pinned later-land authored cards to the private Admin board with seeded whole-card draws, 2d6 checked choices, recorded consequences and prospective causal shifts. V4 new journeys replay exact dice/card/flags/Rewards; existing V3 and V2 saves retain their previous reducer, results and localStorage keys. No public play route, ArtJobs, production deploy or boss-variant/companion UI claimed.
<!-- note:end t-025 -->

## t-026 — Bespoke illustrations for the 36 later-land encounters and four later trials

<!-- note:begin t-026 -->
Opened 2026-10-11 after t-013's reuse pass (kind_robots#3546). Every later-land card currently shows a hand-picked existing Zuzu Gamebook/Showdown scene from utils/shiftingLands/sceneArt.ts; the authored packs keep art: null so this task can see what it owes. Paint one fixed-cast illustration per encounter in DUSTWATER-9, TABLELANDS-9, STORM-CROW-9 and BLACK-VERGE-9 plus the Crossing Gate, Canyon Warden, Deep-Cave Judgement and Beyond the Verge trials, following the t-023 Homestead pattern once it lands (same frame, LoRA and rights rules). Durable ArtJobs only; queued != rendered != delivered != verified. Ship delivered art from a path the image serves (never under /images, which Alexandria mounts over), then swap the sceneArt entries and keep verifyShiftingSceneArt.test.ts green.

Done 2026-10-12: art round 1 (projects/zuzu-shifting-lands/art/ROUND-1.yaml) plus
rerolls painted 51 of 52 Shifting Lands cards, two Arthemy house-lane seeds each,
reviewed against each card's cast and brief and exported to kind_robots public/shifting-
lands/cards (BESPOKE_CARDS). Shipped in kind_robots#3572 and #3586. A Road of Bones
missed twice and deliberately keeps its reused bone-valley plate; the Homestead trial
keeps the gamebook abbess-welcome plate.
<!-- note:end t-026 -->

## t-027 — Zoomed consequence reveal after every choice and trial

<!-- note:begin t-027 -->
Silas, 2026-10-13: "when we make a choice between the two paths, we need to see a real display and new art showing the consequence of our action ... definitely needed for immersion and to really pay off the experience."
kind_robots#3611: after a checked choice or trial attempt the private Admin board stays zoomed in on the consequence (outcome plate flips in with a Success/Failure ribbon, pip dice with skill/modifier/total/target, the authored result at display size, health and provision chips) and a context-aware Continue (down the road, face the trial, return to the gate, enter the next land, see how it ends). Painted plates come from sceneArt BESPOKE_OUTCOMES (t-028); unpainted outcomes fall back to their card art with a success/failure grade. Presentation only; no reducer or save change. Builds on the single-screen tabbed board from kind_robots#3610.
Done 2026-10-13: kind_robots#3611 merged as 872b2ae after all 31 head checks passed (TypeScript, Shifting Lands gameplay contract, layout contract, Contract verifiers). Admin-only preview; no production deploy claimed.
<!-- note:end t-027 -->

## t-028 — Art round 2: one consequence painting per choice and result (222 plates)

<!-- note:begin t-028 -->
Silas, 2026-10-13, asking for new art that shows the consequence of each choice (see t-027). art/ROUND-2.yaml holds 222 subjects: every choice of the 48 authored encounters (192) and of the five major trials (30), success and failure, one Arthemy house-lane seed each, prompts written from each outcome's authored text with identity tags copied from the card's ROUND-1 keeper (fixed cast, Zuzu out of frame, injury implied and non-graphic, no lettering). All 222 passed the prompt contract dry run and were queued 2026-10-13 as ArtJobs 37665-37886. Queued != rendered != delivered != verified.
Next (after rest_until, once the shared render queue drains): enqueue_art_requests.py art/ROUND-2.yaml --status, review with the shifting-lands card exporter's --sheet mode land by land, mark keepers `verdict: 'keep: ...'` (success and failure of one choice must read differently; cast must match the card), reroll misses as sl2r2-* subjects, then run the exporter with --kind-robots ../kind_robots (subjects with `outcome` write public/shifting-lands/outcomes/<card>--<choice>--<result>.webp) and list the printed keys in kind_robots utils/shiftingLands/sceneArt.ts BESPOKE_OUTCOMES; verifyShiftingSceneArt.test.ts checks each one. Can ship land by land.
2026-10-13 review: all 222 rendered. 173 keep (homestead 49/54, dustwater 33/42, tablelands 30/42, cave 29/42, verge 32/42), exported and shipped in kind_robots#3623 (BESPOKE_OUTCOMES). 49 rejects (wrong species, cloned figures, a gore-looking puddle, stray lettering, a modern road, success/failure reading the same) rerolled as sl2r2-* with targeted prompt fixes, queued as ArtJobs 38223-38271. Next: --status, review the rerolls, export keepers, add to BESPOKE_OUTCOMES; a second miss may keep its card-art fallback.
Done 2026-10-13: rerolls reviewed, 27 of 49 keep, shipped with kind_robots#3623 (173) for 200 of 222 painted consequence plates. The 22 outcomes that missed twice keep the graded card-art fallback and can be revisited in a later art round: the-locked-dormitory--search-lock--failure, a-crust-for-the-road--offer-help--failure, the-silent-bell--climb-stairs--success, the-mended-compass--compare-the-two-charts--failure, three-cups-on-the-table--question-the-armed-patrons--failure, footprints-in-the-silt--follow-the-wet-prints--failure, hammer-under-the-stone--brace-the-loosened-wall--success, hammer-under-the-stone--inspect-the-fresh-cuts--success, hammer-under-the-stone--inspect-the-fresh-cuts--failure, the-empty-pay-cart--read-the-pay-sheet-aloud--success, the-glass-vein--cut-a-safe-sample--failure, the-watchful-overhang--test-the-ledge-alone--success, the-toll-without-a-keeper--challenge-the-false-toll--success, the-map-in-ashes--persuade-her-to-stop--failure, the-third-shadow--count-the-lantern-positions--success, the-cooling-stones--mark-the-unsafe-seam--success, ashes-at-the-border--offer-to-scout-the-tower--failure, the-last-watchfire--volunteer-for-the-search--failure, the-closed-infirmary--inspect-the-sealed-room--failure, the-price-of-silence--refuse-the-secret-bargain--success, trial-verge--confront--success, trial-verge--parley--success.
<!-- note:end t-028 -->

## t-030 — Second-person, hero-agnostic prose; one-screen reader; Risky-N dice chip

<!-- note:begin t-030 -->
Silas, 2026-10-18 (see notes_from_silas). kind_robots#3830: all 48 cards, 5 trials and journal lines in second person, present tense, never naming/gendering the hero; boilerplate intents and mechanical risk lines replaced; flavors show what titles promise. Restores compare mechanics not prose (sameReplay) so V3-V5 saves survive; trial rules fingerprinted. Readers fit one screen with the whole painting (contained over a blurred fill); dice chip reads "Risky 7" (difficulty word + dice needed, tap explains). Verified with all 10 verifyShifting* contracts and screenshots at 1180x820, 1440x900, 390x844, 844x390. Merged 2026-10-18 as kind_robots 89c419cba46331d86fe7ea761621c07698580a92 after 21/21 green checks.
<!-- note:end t-030 -->

## t-031 — V6 deck engine: certain, gated and costed choices, moral ledger, 8-card pools, V6 save

<!-- note:begin t-031 -->
Match Shifting Desks' card mechanics (DEPTH-ASSESSMENT-2026-10-18.md): choices may be certain (roll null, success only), gated on shared deed flags (requires.anyFlags, shown locked with the reason), and carry an up-front hp/provisions cost; outcomes record moral marks (mercy, honesty, courage, cunning, ruthlessness). One reducer for all five lands, pools of 8 per location, new kr.shiftingLands.journeyLedger.v6 key with full replay verification. V2-V5 saves keep the frozen 48-card / two-choice rules (additions carry since: 6). Board shows locked routes, costs and the Risky-N chip for every kind of choice.
Done 2026-10-18: kind_robots#3836 merged as 6d6852433b5c6be80f34eb42300022f8ed40784a after 20/20 green checks. deckV6.ts (certain/gated/costed choices, choiceLock reasons, marks ledger, validator incl. every card keeps a free route), saveLedgerV6.ts (journeyLedger.v6, full replay, prose-tolerant), board chips for Certain / costs / locked routes. verifyShiftingV6.test.ts in CI: 320 seeded runs over four policies, forged dice/marks rejected, deck-rules fingerprint pinned (bump schemaVersion on any rules change).
<!-- note:end t-031 -->

## t-032 — Author 24 cards per land (72 new) and a third/fourth choice on the existing 48

<!-- note:begin t-032 -->
Eight cards per location in every land (Homestead +12, other lands +15 each), 3-4 choices per card, at least half the cards with a certain sacrifice/refusal choice, about a third with a route gated on the ten shared deed flags, in the 2026-10-18 voice: hard decisions, the cost of sacrifice, doing good that is not always rewarded. Second person, hero-agnostic. Each new card ships an art brief for t-033.
Done 2026-10-18 in kind_robots#3836 (6d6852433b5c6be80f34eb42300022f8ed40784a): 72 new cards (8 per location, 120 total), 81 added choices on the original 48, 444 choices; 108 cards with a certain route, 43 gated on the ten deed flags. Balance at merge (400 seeds): V5 random 29% complete; V6 random 40%, cautious 45%, ruthless 46%, kind 28% (kindness costs, by design; t-034 should make it pay in endings). Art briefs: art/V6-CARD-BRIEFS.json.
<!-- note:end t-032 -->

## t-034 — Endings from the moral ledger and trial outcomes (Desks-level ending variety)

<!-- note:begin t-034 -->
Shifting Desks has 10 authored endings with variants and 6-9 outcomes per department boss; Shifting Lands has victory / fallen / retired. Read the V6 marks ledger and trial results into authored endings so a merciful run that falls and a ruthless run that wins read differently, in the voice of sacrifice and unrewarded good. Trials may gain ledger-aware outcomes under the V6 rules version.
Ready 2026-10-18 (V6 merged). Inputs: JourneyStateV6.marks and flags. Deck writers' notes: Homestead V6 cards earn Abbess evidence flags not yet in her trial's requiredAnyFlags (the-infirmarys-last-cot-empty-wing, the-guest-book-on-the-lectern-page-taken, the-guest-book-on-the-lectern-blank-departures, the-refuge-lantern-at-midnight-cart-track, gate-midnight-cart-seen, dormitory-chalked-name); Tablelands outcomes hint the missing travelers are held at the Warden's bridge. Extending trial gates changes V5-pinned trial rules, so do it as a V6-only trial layer with a deck schemaVersion bump.

Authored ten moral-ledger epilogue identities with three phase-specific variants each, honest callbacks to completed trials and recorded deeds. Wired V6 terminal card through Pinia; legacy saves keep their prior ending display. Added gameplay contract assertions for 10 identities, 30 phase texts, terminal guards, pure state reads and trial veracity. Kind Robots PR opening for checks. Trial gameplay mechanics, source decks and replay schema unchanged.

Completed ledger-aware endings in Kind Robots PR #3935, squash merge 52e56f0b238d3cae8fb2120b36f60923760035dc. Ten authored moral-path endings, three phase-specific stories each (30 terminal variants), plus only actually earned deed and trial callbacks. Derived by pure helper in Pinia and shown in the current bounded terminal reader. Existing V2-V5 display remains fallback, V6 replay schema and mechanics unchanged. All 16 latest-head GitHub CI workflows succeeded including Shifting Lands Gameplay Contract, TypeScript, formatting, and four-shard Contract Tests. No production deployment or visual acceptance verified; no art generated. Separate prose task t-036 and art task t-033 continue independently.
<!-- note:end t-034 -->

## t-035 — V6 balance report: survival, death causes and gate reachability by land

<!-- note:begin t-035 -->
Port the idea of kind_robots utils/scripts/shiftingDesksBalanceReport.ts: simulate many seeds with simple policies (always kind, always safe, greedy, random), report survival per land, the cards that kill most, how often each gated route is reachable, and provisions curves; tune targets/costs where a land is a cliff.
Ready 2026-10-18: kind runs complete 28% vs ruthless 46% at V6 merge; a starting harness lived in the session scratchpad (policy by marks/targets, 400 seeds each). Decide with t-034 how much of the kindness penalty is tone and how much is a cliff.

Built deterministic V6 real-engine balance harness across kind, safe, greedy, ruthless, and random policies, with 300 seeded journeys per policy in the Shifting Lands CI contract. Measures per-land arrivals, trial reach/clearance, deaths, provisions/health curves, deed-gated routes, evidence choices, and top fatal choices. CI and final measured report pending; all V6 gameplay rules and save schema untouched.

Completed real V6 balance simulation in Kind Robots PR #3944, merged fc7bb4d490b620eaff719035947b1033e784fa91 after all 13 latest-head workflows green (including Shifting Lands gameplay, TypeScript, formatting, and full four-shard contracts). Authored script utils/scripts/shiftingLandsV6BalanceReport.ts, CI command runs 300 seeds each for five kind/safe/greedy/ruthless/random heuristics, and committed measured tables and editorial findings in docs/shifting-lands/V6-BALANCE-REPORT.md. Completion 42.3/59.3/36.0/41.7/39.3 percent by policy, respectively; 524 of 844 deaths in Verge, 44.4 percent of final-land arrivals falling there. Very low deed-gated and investigative trial route availability for several policies. Follow-up replay-safe, explicitly versioned V7 tuning in kind_robots issue #3946. No runtime mechanics, saved-game schema, art or production deploy touched. One-line unrelated Conductor validation repair PR #6423 unblocked review transition, preserving other worker claim. Leave t-036 prose and t-033 art independent.
<!-- note:end t-035 -->

## t-036 — Shifting Lands V6: comprehensive encounter line edit for voice, stakes and readable choices

<!-- note:begin t-036 -->
[HISTORICAL EDITORIAL SUBTASK; GITHUB MASTER ISSUE NOW MAPS TO t-018]\n      FROM GITHUB ISSUE silasfelinus/kind_robots#3917 (https://github.com/silasfelinus/kind_robots/issues/3917), opened by @silasfelinus on 2026-10-20. Imported by scripts/sync_github_issues.py. Reference the issue in the implementing PR (`Closes silasfelinus/kind_robots#3917`) so it closes on merge; the bridge closes it otherwise once this task is done.

## Direction (Silas, 2026-10-20 PT)
Accelerate Shifting Lands beyond quantity toward **finished creative content**, including polished second-person narrative text, engagement, and art fidelity. Art prompt production is under conductor PR #6401. This issue covers the separate **runtime/player-visible** writing pass, not a discussion-only style proposal.

## Scope
- Audit all **120 authored encounter cards / 444 choices** for repetitive formulations, stilted dialogue, flat outcomes and mismatch with art. Include five major trials and player-facing journal lines where necessary.
- Keep the narrator **second person, present tense, hero-agnostic**. Zuzu's distinctive values can inform world reactions without tying every line to his name/pronouns; eventual alternate protagonists must fit.
- For each encounter: a concrete opening image, a morally consequential dilemma, action-led concise choice labels, outcomes that pay off what was promised and reveal consequences. Prioritize sacrifice, kindness with costs, broken bargains, earned trust and consequences carried across lands. Avoid moral lectures and identical 'choose/decide' boilerplate.
- Edit prose only unless explicitly versioning new mechanics. Preserve card IDs, choice IDs, roll targets, costs, deed flags, marks, eligibility, schema and save replay; verify V2–V6 restorations. Existing source-authored species/cast stay fixed.
- Compare story descriptions to ROUND-4 art anchors and titles. The 'Three Cups on the Table' scene must explicitly show three cups both in the text and its rendered illustration. Leave art rendering and keeper exports to Conductor t-033.
- Ship edits in **reviewable batches by land**, with focused playbook/contract tests and real examples of before/after writing quality. Merge each green batch, not a single giant unreviewed blob. No publication or deployment without its separate gate.

## Creative acceptance
Do not mark complete when only a style guide or new tasks exist. Gameplay text itself must be edited and replay-tested; player can tell what each choice does, whom it affects, and why the outcome feels different from another choice.

Linked project: `zuzu-shifting-lands`, editorial counterpart of conductor t-034 (ledger-aware endings).

First-land prose implementation: 24 Homestead cards edited (32 old-pack and 40 V6 text fields); original card identity, dice, costs, flags, reward effects and save fingerprint unchanged. Opening Kind Robots PR for scoped review, with 96 cards in other lands still pending.

First-land editorial milestone merged as kind_robots PR #3928 at a937281, all 14 current-head workflows successfully completed (Shifting Lands Gameplay Contract, TypeScript, full Contract Tests, formatting and all other jobs). 24 Homestead encounter cards received 72 targeted prose edits across original and V6 decks; exact source-level comparison confirmed no mechanics changes. The ticket and task remain open for remaining 96 cards and five trials; next batch should take Dustwater, review its original 9 and V6 15 cards plus Crossings Gate trial separately. No deployment or new art was performed.

Dustwater editorial batch 2 prepared in Kind Robots. All 24 Dustwater encounter cards (nine existing and 15 V6) have focused prose revisions plus nine older cards' extra V6 choices. Original choice ids, dice, costs, flags, and V6 save fingerprint are preserved. PR/checks pending. Tablelands, Deep Cave, Verge and five trials remain unedited by this batch.

2026-10-24: #3917 is now the whole-game master roadmap, not an auto-close\n      trigger when prose alone completes. t-036 remains independently claimed\n      for 72 encounter cards, five trials and global prose review. Completion\n      of t-036 never bypasses t-043..t-048 or final signoff t-018.\n\n      Dustwater prose batch merged to kind_robots main in PR 3930 (2d35a70259cbe2ff1fe3076c0fdb4b98e7a287e7), all 14 current-head CI workflows completed successfully including dedicated Shifting Lands gameplay and 4-shard Contract Tests. Edited all 24 Dustwater encounter cards (nine older plus 15 V6), plus extra choice text on all nine older cards, 85 targeted prose changes. Exact mechanical projections from original and branch matched. First two lands now through editorial passes (48/120); remaining Tablelands, Deep Cave, Verge (72 cards), five trials and final journal/voice audit. Keep issue 3917 open and task ready for another land batch. No art generation or production deployment.

2026-11-01 PT intent audit: claim released after 11 days idle; last note (2026-10-24)
says the task is ready for another land batch (Tablelands, Deep Cave, Verge, five trials
remain).

2026-11-04 PT: Tablelands batch (24 cards + Canyon Warden trial and its V7 solidarity
scene, 30 prose edits, mechanics byte-identical in projection) in kind_robots #4768.
72/120 cards edited. Remaining: Deep Cave and Verge batches (48 cards), the four other
trials, and the final journal/voice audit. Returned to ready because the line edit
continues land by land.

2026-11-04 PT: Deep Cave batch (24 cards + Deep-Cave Judgement trial and its V7
witness/solidarity scenes, 32 prose edits on 15 cards, mechanics byte-identical in
projection, V6 deck and trial fingerprints unchanged; all 19 shifting-lands-gameplay
workflow steps pass) prepared as a patch against kind_robots a13933a7: sets up the
storm-reader's question, the guide's brother's debt and the trial's chalk circle; fixes
a herbs-spent failure that leaves deed-carries-medicine set, three unspoken deed-owed-
favor grants, and count/pronoun tangles; verifyShiftingV6 gains a Deep Cave block.
96/120 cards edited. Remaining: the Verge batch (24 cards), the Homestead, Dustwater and
Verge trials, and the final journal/voice audit. Task returns to ready.  Merged as
kind_robots #4787. Back to ready for the remaining scope.

2026-11-05 PT: Verge batch and the last three trials (29 prose-only edits: 18 on 15 of
the 24 Verge cards, nine across the Homestead, Dustwater and Verge trials, two V7 scene
strings; mechanics byte-identical in projection, V6 deck and V5 trial fingerprints
unchanged; all 19 shifting-lands-gameplay workflow steps pass) prepared as a patch
against kind_robots 7957faab. It sets up the Abbess's guards and the children's
dormitory, the Crossing Gate's jam and its one "safe" channel, and the Verge seal. It
stops promising an empty medicine pouch and a spent favor while deed-carries-medicine
and deed-owed-favor stay set, and it no longer assumes the player kept every promise.
verifyShiftingV6 now checks length floors and the map-shift regex in one loop over every
land, keeps every land's pins and adds 18 new ones. With this, 120/120 cards and all
five trials are edited. Remaining: the final journal and voice audit. Candidates are
listed in the PR body; the main one is whether spent deed flags should be consumed,
which would need a new rules and save version.  Merged as kind_robots #4797; back to
ready for the remaining scope.

2026-11-05 PT: Final journal and voice audit, prepared as a patch against kind_robots
0d132816. It is prose and tests only; the mechanics projection of all four content JSON
files is unchanged, the V6 deck and V5 trial fingerprints pass, and all 19 shifting-
lands-gameplay steps exit 0. It makes 37 stock-phrase edits on 34 cards: "road ahead"
drops from 40 to 20 and stays the map-shift refrain, "without a word" drops from 18 to
11, and pressed-into-your-hand gifts from 25 to 13. verifyShiftingV6 now caps each
phrase per land. The V7/V8 shared trial intents now read as second-person story prose,
and the board's odds, check and lock text is pinned beside them. This also fixes the V8
scout intent, which asked the player to pay an HP they had already paid. The Verge
evidence success is now neutral about which clue opened the route. On the journal:
failed trial checks were already written to it. The coarse bosses[].approach `parley` is
kept for save replay, because trialResults[].choiceId holds the real route; a V7 guard
test pins all of this. Remaining: spent deed flags (deed-carries-medicine, deed-owed-
favor) never clear. The rail never shows them, but the gated choices stay open, so one
medicine can be spent once per land. Clearing them needs `consumes` plus deck
schemaVersion 2 and a new ledger version; the design note is in the PR body. With this
patch, t-036's editorial scope is done; the deed-consumption fix should be its own task.
Merged as kind_robots #4813. Editorial scope complete (120 cards, 5 trials, voice
audit); spent-deed consumption split out as t-049.
<!-- note:end t-036 -->

## t-037 — V7 kindness, preparedness and evidence-gate balance upgrade

<!-- note:begin t-037 -->
Silas (2026-10-20 PT): approve balance findings and upgrade so kindness remains viable and careful planning pays off. Implement an isolated V7 rules/save pathway that preserves V2-V6 replay, adds earned moral and scouting alternatives to boss trials, and reduces the repeated Verge trial failure cliff without making all choices equal. Verify with seeded kind, safe, greedy, ruthless, random baselines and device-sized UI acceptance, keep public deployment separately gated. Avoid collisions with t-036 prose and t-033 art. Related kind_robots issue #3946.

V7 rules implemented in a separate Kind Robots ledger/save namespace without changing V5/V6. Added earnable witness approaches (two mercy or honesty marks), one-HP one-time gate scouting opening a safer approach, additional evidence flags from actual V6 encounters, UI trial choices, and seeded comparative V6/V7 simulations. Dedicated V7 restore and forgery assertions included. Kind Robots PR pending CI and measured updated baseline. Production deployment and visual acceptance not claimed.

Completed user-directed V7 moral economy in Kind Robots PR #3950, squash merge abc278d2bb9219b40f83b4d68c53c6f4fa014141, all 16 latest-head CI workflows green including dedicated 1500-journey gameplay simulation, TypeScript, formatting and all four contract shards. Greedy (59.7 percent) and ruthless (62.0 percent) easiest, careful (52.7 percent), random (47.3 percent), kind (42.0 percent) hardest over identical 300 seeds per policy. Implemented V7-only tribute/coercion shortcuts with permanent moral marks and bittersweet ending accountability; genuine witness, costly per-gate scouting and high-mark solidarity actions grant richer collective endings, including mixed-repentance variants. V5/V6 saves and trial rules remain separate, replay verified; new V7 save key and source-committed measured report at docs/shifting-lands/V7-BALANCE-REPORT.md. User clarified easy-to-do-harm/hard-to-do-good narrative direction. No image render, production deploy, or manual mobile/tablet/desktop acceptance claimed; independent art t-033 and editorial t-036 remain unmodified.
<!-- note:end t-037 -->

## t-038 — V7 world remembers: cross-land consequences, returned witnesses and readable journey callbacks

<!-- note:begin t-038 -->
User approved continuing Shifting Lands development after the merged V7 moral economy. Build source-backed in-journey cross-land callbacks: people helped or harmed should reappear in authored read-only vignettes, gate/bargain choices should change how later communities greet the traveler, and hopeful paths should be legible in the Journal before the epilogue. Implement a deterministic V7-only narrative consequence layer derived from real earned marks, flags and successful/failed trial outcomes. Include particular choices and witnessed costs in the later lands, rather than generic morality banners. Keep per-land arrival surface bounded in one-screen board UI; longer consequence history lives in the scrollable journal. Do not alter V7 gameplay rules, replay/save fingerprint, cast/species or V6 authored encounters. Keep t-036 encounter line editing and t-033 artwork independent. Test no spoilers, cause-accurate triggers and V2-V7 fallback, then merge only on green CI. No production deploy or manual visual acceptance assumed.

Implemented V7 read-only world reaction layer in Kind Robots PR #3971. Added 32 authored land-arrival callbacks for eight prior trial approaches over four later lands, plus ten returns from exact successfully resolved encounters. Reactive Pinia store, compact expandable road announcements and an accumulated journal narrative, plus source-accurate no-spoiler replay-safe tests in dedicated Shifting Lands CI. Shifting Lands gameplay and formatting current-head green; TypeScript and complete contract suite pending. No old save, trial, original encounter/prose, artwork, live deployment or visual approval altered. t-036 and t-033 remain separately owned.

Completed Kind Robots PR #3971, squash merged 37c8cf5beb119de830d219347ae7e065e1cc4891 after all 16/16 latest-head CI workflows green, including Shifting Lands gameplay, TypeScript, formatting and four-shard Contract Tests. Shipped 32 distinct previous-trial arrival scenes and 10 encounter-specific across-land reprisals, with exact recorded-success predicates, read-only V7 reactive state, compact open arrival reveal, full journal history and regression tests for false success, forged boss turn, conflicting moral choices, deterministic projection and future spoilers. No V2-V7 saves, mechanics, original encounter prose, art, production deployment or manual visual acceptance changed. Independent t-033 art and t-036 editorial remain open.
<!-- note:end t-038 -->

## t-039 — V7 compounded moral consequences in later lands

<!-- note:begin t-039 -->
Silas, 2026-10-20 PT: keep building after V7 balance and world-memory work. Add a compact, read-only authored continuity beat in later lands for specific pairs of verified prior completed major-trial choices (compassion, exploitation, restitution, betrayal, collective resistance). One cause-accurate optional chain echo per arrival, with explicit past action references and earned social consequences. Preserve existing V2-V7 saves, fixed narrative casts, no mechanics or new boss rules, no art ownership overlap with t-033 and no original encounter prose overlap with claimed t-036. Validate true boss/turn/outcome matching and absence of future spoilers, and measure reachable chains over deterministic live-reducer seeded journeys before merge. New narrative branches must not invent deeds or claim moral redemption is automatic. No deployment or manual visual approval implied.

Implemented 18 authored two-deed V7 cross-land consequences in Kind Robots PR #3973. Six choice-pair vignettes each in Tablelands, Cave, and Verge, derived only from two independently verified completed trial choices and boss turns, with presentation-only integration to the existing road/journal surface. Added truth-guarded static coverage tests and 1,000 real-reducer policy playthroughs in gameplay CI. PR checks and measured reachability pending. No saved-run mechanics, art, original encounter prose or production deployment touched.

Completed V7 compounded moral consequences in Kind Robots PR #3973, squash merge 5b38681bba5ffef19c149b44f8d33dca290f0ed5. All 14/14 latest-head CI workflows green, including Shifting Lands 1000-journey reducer test, formatting, TypeScript and four contract shards plus verifier. Implemented 18 two-trial authored cross-land scenes for Tablelands, Cave and Verge, verified with original boss/turn/roll matching and anti-forgery and future-spoiler tests. Thirteen of 18 scene combinations appeared in 1000 deterministic bot runs; remaining rare paths are authored and source-guarded but not observed in that sample. V6/V7 gameplay and save schema unchanged; no art generation, production deploy or manual device visual acceptance. Left issue #3917 open because independent claimed t-036 120-card prose work remains in progress; V7 balance issue #3946 already closed.
<!-- note:end t-039 -->

## t-040 — V7 special moral constellation endings and distinct bitter victories

<!-- note:begin t-040 -->
Continue implementing the world where greedy and ruthless passage is mechanically easier, but costly in what remains behind. Add several hard-earned, distinct optimistic V7 epilogues based on actual successful trial combinations and true encounter deeds, and contrasting specific, bitter victory outcomes for exploitative runs. The new finale must distinguish outcomes beyond a generic virtue/vice banner; none may invent deeds or absolve harm by selecting one late kind option. Preserve authoredEndingV6, V2-V7 replay, and no mechanics/save/roll edits. Test high-road, mixed, coercive, transactional and fallen/retired paths, including impossible/future/failed choices and exact trial-to-boss evidence; measure case availability with the seeded real engine when feasible. Do not overlap t-036 encounter prose or t-033 card art. Leave production and phone/desktop visual acceptance separately gated.

Seven special sourced V7 finale constellations (three high-road, three bitter dark, one limited restitution), each with three terminal variants, implemented in Kind Robots PR #3978. Added pure boss/turn/roll/target verification, anti-forgery and future-land tests, gameplay CI, docs. Original V6/V7 saved rules, encounter prose and art untouched. Current-head formatting, TypeScript, Shifting Lands gameplay and full contract checks pending before merge.

Completed seven distinct V7 authored finale constellations with three terminal phase narratives apiece, grounded against matching successful trial and boss turn/roll/target. Includes three harder hopeful legacies, three specific bitter exploitative conclusions, one restorative ending that does not erase prior harm, and tests for forged/duplicated/future results, legacy V6 fallback and no mid-run spoilers. Kind Robots PR #3978 squash merged 801b21d6e6b166359bb475203030f157ee69c167 after all 14 latest-head CI workflows succeeded including Shifting Lands Gameplay, TypeScript, formatting and four contract shards. Documented in docs/shifting-lands/V7-MORAL-CONSTELLATIONS.md. Independent t-033 artwork and t-036 card prose remain open. No change to V2-V7 save rules, art, production deploy or manual visual QA.
<!-- note:end t-040 -->

## t-041 — Adversarial Shifting Lands V7 playtests, simulated reviews and targeted gameplay fixes

<!-- note:begin t-041 -->
Silas requested adversarial playtests, reviews and implementation improvements. Test actual reducer playthroughs with incompatible strategies, unlucky seeds, save/replay integrity, resource scarcity, route/ending reachability and narrative causality. Preserve separate t-033 art and t-036 prose ownership. Publish evidence and prioritized simulated-review findings with a scoped, verified implementation PR; do not treat scripted strategies as human playtesters.

Adversarial V7 gameplay fix and mock-review report implemented on worker/zuzu-shifting-lands-t041-playtest-20261022-1751. Awaiting Kind Robots scoped gameplay, TypeScript, formatting and contract CI.

Merged silasfelinus/kind_robots#4051 at 73349f30862a1767ed60eacd174c12052c033d12 after all 14 PR-head CI workflows completed successfully, including Shifting Lands Gameplay, TypeScript, formatting, and full Contract Tests. Fixed mixed mercy/honesty Witness qualification and documented 1,500 seeded adversarial runs, 120/120 card draw coverage, per-land trial failure counts, and prioritized synthetic reviews. No human playtest, production deployment, or generated artwork claimed.
<!-- note:end t-041 -->

## t-042 — Shifting Lands V8 replay-safe benevolence and scouting balance

<!-- note:begin t-042 -->
Address adversarial t-041 gaps: Scout costs one health but had a 16.7% chance to beat Verge; compassion routes remain punished versus coercion. Create a replay-compatible V8 ruleset preserving V7 restores, earned witness/solidarity requirements and dark-route moral consequences. Make prepared scouting materially effective, compassionate choices worth earning, and demonstrate seeded playstyle outcomes plus anti-forgery tests. Coordinate separate art t-033 and prose t-036.

Created separate V8 ruleset with earned compassionate trial odds, meaningful scouted routes, visible 2d6 success percentages, legacy V7 save isolation, and five-style seeded policy comparison. Awaiting Kind Robots PR CI before any merge, deployment or roadmap completion.

Merged silasfelinus/kind_robots#4054 as 58359c64c713864d2e51e34318166cf11a38ddd0 after all sixteen latest-head CI workflows passed, including V7/V8 gameplay, TypeScript, formatting and full Contract Tests. New V8 journeys strengthen earned Witness, Solidarity, and 1-HP Scout routes, show exact 2d6 odds, preserve all V7 save ledgers, and simulate 300 matching seeds for each of five playstyles per version. Kind completion rose from 70.7 to 87.7 percent, cautious from 77.7 to 92.7 under the corrected probability-aware policy; dark-route outcomes were unchanged. No production deployment or human playtest claimed.
<!-- note:end t-042 -->

## t-049 — Spent deeds: consume medicine/favor flags once spent (deck schemaVersion 2 + save migration)

<!-- note:begin t-049 -->
Found by the t-036 final voice audit (kind_robots #4813, 2026-11-05 PT). Deed flags such as deed-carries-medicine and deed-owed-favor are never cleared when spent, so the choices they gate stay open: one medicine can be "spent" once per land, up to five times a run. Proposed design (PR #4813 body): add a `consumes` field to choice outcomes with deck `schemaVersion: 2`; because saves are rejected when the deck version changes, ship a save migration that replays v1 runs under v2 rules or grandfathers them. Pin with a seeded battery showing each deed is spent at most once per acquisition, and keep the V6 replay/forgery guarantees. Prose already avoids promising consumption (t-036).

2026-11-05 PT: Spent deeds shipped as a patch (round r5) on base b26f0cc9. A route gated
on deed-carries-medicine or deed-owed-favor now spends it, win or lose. Eleven routes
spend; comparing herbs is exempt because it is a trade. Every route gated on that deed
then closes ("Already spent. Opens again only if ...") until a later outcome grants
another, so each deed is spent at most once per acquisition. The board chip says "spends
your medicine" or "spends a favor", and the journal records the loss. I took option (b)
instead of the proposed consumes field with schemaVersion 2: the rule lives in
deckV6.ts, so the V6 deck fingerprint and version are unchanged. Run state gains
JourneyStateV6.spentDeedsFrom (new runs 0). Pre-change V6-V9 saves replay and verify
under their own rules, then adopt the rule from their next outcome on; deeds they
already used stay used, and out-of-range values or hidden double spends are refused.
Three prose lines that promised medicine left over now match the rule. The new
verifyShiftingSpentDeeds battery (in the gameplay workflow) plays 3,000 seeded V9 runs:
0 double spends against 18 under the old rule, 27 closed and refused, re-acquisition
reopens, replay and forgery guarantees hold, old V6-V9 double-spend saves load, and all
38 endings stay reachable. 12 saves made with the unmodified base code also restore. All
19 workflow verifiers and full vue-tsc pass. Remaining: the coordinator applies, opens
and merges the PR. Optional follow-up: show the deeds you carry on the character rail.
Limit: a hand-edited save can drop the field and get the old rule for history it already
recorded, but only that.  Merged as kind_robots #4830.
<!-- note:end t-049 -->

## t-051 — Zuzu: Shifting Lands achievement upgrade: 12 or more live achievements

<!-- note:begin t-051 -->
Silas 2026-11-11 PT, in session: "Our games should all have a base standard of quality ... We want our main games to have 12 plus achievements." Standard: docs/agents/main-game-standard.md; CONTROL.md global overview.

Live today: 3 Achievement record(s) with this game's triggerCode prefix (checked against /api/achievements 2026-11-11). Target 12+ (usually 12-30; tie some to endings but don't go overboard). Mix story, skill, discovery and completion. Create the live records through the existing achievements API (label, message, icon, karma, triggerCode prefixed with the game slug), award them from the game store, show them with components/achievements/game-achievement-strip.vue, and verify one award live after deploy.

Achievement upgrade merged in kind_robots#5060 (2b2a1bc), all 13 checks green: 3 kept codes (messages rewritten to second person, no longer naming Zuzu) + 17 new = 20, including mittens-road, fennec-road and own-legend for the new character creator; awarded from journeyDeeds diffs in dispatch only, never on restore/fresh. Strip in a 'Road achievements' rail section. Ratchet file now empty: every main game is at 12+. Not wired: ending-collector (no persistent endings record yet).
<!-- note:end t-051 -->

## t-052 — Character creator: design a character, adjust stats, play as Zuzu or Jeffery Mittens

<!-- note:begin t-052 -->
Silas 2026-11-11 PT, in session: "Shifting lands should let us design a character and adjust stats. That means certain encounters change, you can't let the user play the siblings and have them encounter the siblings. But that will help differentiate it from the zuzu gamebook. Though obv zuzu should be one of the playable characters. As should Jeffery Mittens."

Build a start-of-run character creator: choose a premade (Zuzu, Jeffery Mittens the young raccoon looter from zuzu-gamebook BOOK-ONE-OUTLINE.md, and any other canon cast you choose to offer) or design a custom character (species from the approved Facets, name, portrait, and a point-buy stat spread on the existing stats). Premades have fixed stats and signature traits.

Encounters must respect identity: any encounter, follower or quest featuring the chosen character (e.g. the fennec siblings, Jeffery Mittens) is swapped, rewritten or excluded so the player never meets themselves; add a deterministic test sweep over every playable character. Stats should change check odds and some encounter options. Queue portraits for premades and custom species in an auto_submit ledger. Persist the character in saves and the scrapbook.

Character creator merged in kind_robots#5038 (bf8c03f) with all CI green: premade Zuzu (unchanged stats), Jeffery Mittens (knows the old roads; 8 existing routes) and the fennec siblings (sister with her brother), plus a 13-point custom traveler (name, species from the Book One cast, pronouns). Ledger v10 snapshots the character; V9 saves restore as Zuzu and replay byte-identically (pinned 300-seed digest). Identity-aware encounters: cast-tag sidecar, 7 cameo cards and 3 self-variants so a player never meets themselves (swept every character x seeds 1-500 x 15 locations). Portraits queued in conductor#7282 (ROUND-8-TRAVELERS, 13 portraits). Follow-ups: the 3 live achievement messages still name Zuzu (zuzu-shifting-lands achievement task), no scrapbook yet (standard task). Open for Silas: children as playable characters facing the Abbess trial and death routes (harm kept off-screen), naming the fennec sister, stat tuning.
<!-- note:end t-052 -->
