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
