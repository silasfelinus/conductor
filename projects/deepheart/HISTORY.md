# deepheart — task history archive

Full `note:` prose for completed deepheart tasks, moved out of `roadmap.yaml` so the
Kind Robots projection payload (`scripts/sync_kind_robots_projection.py`, hard limit
4,000,000 bytes) stays well clear of its ceiling. See conductor/t-158.

Each note below is the **verbatim** original — nothing is summarized or trimmed. The
`roadmap.yaml` task keeps its own first sentence plus a pointer here. The HTML comment
markers delimit each note exactly; `archive_done_task_notes.py --verify-only` re-extracts
every note and checks it byte-for-byte against what the roadmap recorded.

## t-006 — Main-game standard: title, settings, save/load, 20 achievements, chronicle; verify one award live

<!-- note:begin t-006 -->
Audit table lives in kind_robots#5256. Shipped: title screen, kit settings, autosave +
3 versioned slots, chronicle (run pages, delvers met, endings, supports), 20 achievements
awarded through rewardAchievementByCode. Remaining: seed the catalog rows and verify one
award live after deploy.

Scoped Deepheart user-reported tutorial fix in Kind Robots: register /admin/deepheart/bible as a hidden Admin content tab with its own image and contextual help; repair the outdated main-game tutorial copy; add a route resolution regression test against the prior ArtJob tab. The remaining task t-006 live achievement award audit is not complete: return t-006 to ready after the scoped PR merges.

2026-11-25 PT reconciliation: scoped tutorial repair #5650 merged eb61724b; original catalog seeding and live award acceptance still outstanding. Release abandoned review ownership for the remaining work.

Scoped achievement fix at kind_robots commit 3cd2b40b: custom hero classes now contribute to Well Matched correctly. Regression covers original ranger versus warrior with identical companions. CI and live catalog/award verification remain outstanding; return ready after partial implementation merges.

Kind Robots #5839 merged 0013c4ed after all seven latest-head workflows passed (Playbook Kit 45712070183, Contract Tests 45712070144). Original ranger/warrior achievement regression shipped. Live catalog and earned-award acceptance still outstanding; release review ownership.

App commit 4b480ec2 fixes shared achievement retry loss affecting Deepheart: retain known codes after unsuccessful award writes, remove only confirmed awards during retry and guest migration, and add mixed-success/failure regression coverage. Live catalog and account award verification remain outstanding; no KR_API_TOKEN and local DNS cannot reach production. Return ready after verified partial merge.

Kind Robots #5873 merged e675ea28 after all seven completed successful CI workflows, including Contract Tests 45745064790 and Boot Achievement Budget 45745064728. Per Silas's direction to close t-006 when implementation checks pass, complete the implementation milestone and unblock saves, audio and QA; live catalog coverage and authenticated earned-award acceptance remain required in t-013 final QA and were not verified here.
<!-- note:end t-006 -->

## t-007 — Two-tier support scenes for all 35 pairs; three campfire beats per romance and oath

<!-- note:begin t-007 -->
Today each support has one scene and each companion has blurb, secret and heart lines.
Write a second support tier and a three-beat arc per romanceable preset, keeping the
romance setting able to hide every romance beat.

Art-first playable support and relationship progression implemented on worker/deepheart-t-007-camp-stories-d4a2. 35 distinct sequel scenes, second support tier earned after trust at a subsequent campfire (with a stronger real combat bonus), two personal conversations before a third commitment beat, platonic oath route when romance is off, hidden first-time relationship labels, anti-skip validation, old-save compatibility, UI tier labels, and regression tests. Await latest-head CI and PR merge. No new art jobs queued; existing approved portraits illustrate the camp scenes.

2026-11-25 PT reconciliation: #5658 merged d9c918f6; all eight recorded head workflow runs completed successfully, including Playbook Kit 45161520354 and Contract Tests 45161520305. All 35 sequel scenes and three-beat relationship progression delivered; art and full playtest QA remain separately tracked.
<!-- note:end t-007 -->

## t-008 — Room variety and balance from seeded sims

<!-- note:begin t-008 -->
More choice events and puzzle variants per layer; tune so auto-play survival stays
near 75-85% across party sizes and the Gilded threshold needs real greed.

Vertical-world and fairy-court setting implementation drafted: six human-faced deities, twelve kinship/affair/grudge relationships, six inhabited-community choice events, six deity encounters with visible seeded d20 negotiation, and a playable optional final court audience (bargain/expose/defy) layered over nine original endings. Court connections become a real unlockable scrapbook node-and-edge diagram. Kind Robots and Conductor branches are being reviewed and verified by CI; not complete until green and merged.

Kind Robots PR #5274 and Conductor PR #7522 have merged after full green CI. The twelve deathless human-faced fairy rulers, thirty-two relationship links, six populated strata events, seeded d20 nonviolent choices, optional fairy finales, and interactive scrapbook graph are implemented. All forty separate high-priority anthro style-test jobs are recorded DONE with art_image_id in the Conductor ledger (ArtJobs 69682-69721). Return t-008 to ready for the remaining original quantitative acceptance: verify the 75-85 percent survival target across party sizes and tune the Gilded ending threshold. Do not reopen or duplicate merged changes. Human style selection and the held 94-image repaint belong to the art review work, not a claim that images are approved.

Silas directed a difficult-but-possible moral roguelike, stat-relevant parties, and independent custom hero alongside 50 presets. Kind Robots PR #5306 implements a separate original hero slot, selectable class/identity/appearance, four stat points, seeded party-assisted checks, sacrifice costs before rolls, moral finale prerequisites, and regression tests. Conductor Design Brief/CONTROL direction PR follows. Awaiting tests/merge; task remains open for the original quantitative survival and greed tuning.

Shipped verified Deepheart roguelike direction in Conductor PR #7570 (71eb9105) and custom-hero/hard-won mercy/party d20 gameplay in Kind Robots PR #5306 (4f7d3484). All seven Kind Robots checks completed successful, including Playbook Kit, TypeScript, lint ratchet and four-shard contract tests. The custom hero is independent of fifty canonical presets and survives the existing save record; charitable options incur real up-front costs and Redemption requires two paid sacrifices alongside successful mercy. No new art jobs added. Remaining t-008 original balance work: targeted seeded simulations of 75-85 percent survival by party size/class, Gilded ending requiring real greed, and verification of compassionate non-holy paths. Remain ready rather than claiming the full playtest balance milestone done.

Kind Robots commit 330cc099 requires a recorded greedy choice as well as the existing 600 gold threshold for Gilded, adds regression coverage for both gates and non-holy Redemption, and directs the seeded ending trace toward greed. CI pending. Survival calibration by party size/class remains outstanding; return ready after this scoped fix merges.

Kind Robots #5845 merged e7893e29 after seven completed successful checks, including Playbook Kit 45719267042 and Contract Tests 45719266906. Gilded requires a greedy narrative choice and 600 gold; non-holy Redemption gate covered. Remaining scope is quantitative survival calibration by party size and class.

Previous Playbook Kit log 45730520383 proves 49/60 survival and all nine endings reachable. New app commit 1cee445b expands the suite with 300 seeded delves across all fifty presets, three party sizes and two trials per combination, reporting party size, hero role and joint rates. Retains the existing baseline. Await actual CI measurements and tune only if indicated; task not complete yet.

App PR #5864 merged 52d531ea; all seven CI workflows and branch janitor passed. Matrix survival 77/65/95 percent for party sizes 2/3/4. Return ready for remaining scaling calibration.

App commit 6e75e609 adjusts enemy HP and attack by original party size, preserves duo values, and adds a 300-run independent validation sample plus strict 75-85 percent acceptance on the original matrix. Await actual CI results, including all nine endings; do not close until verified.

Kind Robots #5871 merged 782b7336; all seven latest-head CI workflows passed. Playbook Kit 45741692123 job 139647991283 measured party 2/3/4 survival 77/81/80 percent (300 original runs) and 74/87/78 percent (300 independent runs, within 70-90 guard). Baseline 48/60, all nine endings reachable, 50 presets, 35 supports, 20 achievements. Earlier #5845 verified Gilded greed gate and secular Redemption. Original t-008 scope complete.
<!-- note:end t-008 -->

## t-009 — Account-backed save for signed-in players with local fallback

<!-- note:begin t-009 -->
Main-game standard item 3. Keep the versioned local record as the fallback.

App commit 1c38b4db implements explicit account backup/restore of autosave, three slots, and chronicle via a private revision-checked archive, retaining local saves. Added round-trip and invalid payload regressions; CI and authenticated live verification pending. No schema migration.

Kind Robots #5878 merged 90e8d8ae after all ten completed successful CI workflows, including Playbook Kit 45749360796 and Contract Tests 45749360778. Explicit revisioned account backup/restore of run slots and chronicle landed. Return ready for scrapbook/settings integration and live two-device verification.

App commit da815ccd includes the shared Kit scrapbook unlocks and settings in the account archive, restores only Deepheart's Kit record, preserves legacy archives without a Kit payload and protects unreadable local records. Added round-trip and invalid Kit data regressions. CI and authenticated two-device verification pending.

Kind Robots #5892 merged at 4a64c8bb; all seven latest-head CI workflows passed including Playbook Kit 45809076695 and Contract Tests 45809076749; branch janitor 45810888561 succeeded. Account slots, chronicle, scrapbook and settings implementation complete. Authenticated two-device verification remains in final t-013 QA.
<!-- note:end t-009 -->

## t-010 — Sound and music behind the kit sound setting

<!-- note:begin t-010 -->
Torchlit ambience per layer, combat stings, a campfire theme; respect the kit's
sound setting and reduced motion.

Kind Robots #5882 (778e4949) implements seven original synthesized themes and state-driven cues, gesture gating, shared kit sound/reduced-motion controls, tab visibility and cleanup, with loop/cue/lifecycle regressions. CI pending; actual browser playback unverified.

Kind Robots #5882 merged at 7975cce5; all seven latest-head workflows completed successfully, including Playbook Kit 45776917453 and Contract Tests 45776917406. Audio implementation and regression coverage complete. Actual browser playback remains unverified and belongs in final t-013 QA, not a separate subjective gate.
<!-- note:end t-010 -->

## t-011 — Art ledger: queue every brief auto_submit

<!-- note:begin t-011 -->
projects/deepheart/art/WRITTEN-BACKLOG-2026-11-16-KIT-DEEPHEART.yaml queues the 139
unpainted kit pictures (key art, 57 portraits, 41 romance plates, 9 ending plates, 31
scene/support plates) auto_submit at priority 1, from scripts/scan_written_art.py.
Still to queue: 3 faction emblems, 6 room plates (utils/deepheart/art.ts ROOM_ART) and
the 20 achievement badges (kind_robots scripts/generate_achievement_art.ts after the
catalog rows are seeded). Queued is not rendered: t-012 verifies delivery.

Deepheart foundation merged as Kind Robots #5257. The 139-item written art backlog exists, but t-011 remains unfinished: 3 faction emblems, 6 room plates and 20 achievement badges still need submission; queue completion cannot be inferred from prompt files.

Authored 29 remaining Deepheart asset prompts in worker/deepheart-t-011-missing-art-6b4278fa: 3 factions, 6 room plates and 20 achievements, sourced from the live Kind Robots catalog and art spec. The idempotent auto_submit queue will run after a green merge; review status pending verification of accepted ArtJob IDs.

Merged Conductor #7505 as fae31db; Auto Art Generate 43983771297 successfully submitted and checkpointed 29 unique Deepheart ArtJobs 69628-69656 in projects/deepheart/art/MISSING-ASSETS-2026-11-16.yaml (3 emblems, 6 rooms, 20 achievements). Previously queued original 139 jobs 69460-69598 are all DONE with ArtImage IDs. No duplicates. Submission is complete; t-012 now owns rendered media URL verification and wiring, including association of the badge ArtImages with live Achievement records.
<!-- note:end t-011 -->

## t-015 — Expand enemy roster to 40 distinct types and recalibrate seeded encounter variety

<!-- note:begin t-015 -->
Silas 2026-11-26 PT: double enemy variety so runs are not repetitive. Target twelve ordinary enemies per layer, three existing bosses and Mimic (40 total). Give newcomers distinctive names, silhouettes, traits and balanced stats. Prove each type is reachable in seeded combat, keep nonviolent routes and all nine endings, repeat the existing survival calibration. Preserve fixed-seed determinism.

App commit 72fd0bcd expands the three live encounter pools to twelve ordinary enemies each, preserves the three bosses and Mimic, and adds seeded door reachability tests for all 36 ordinary enemies. Existing survival and ending tests remain unchanged; CI results pending.

2026-11-26 PT: Kind Robots #5907 merged c23c16cd; seven latest-head workflows passed, including Playbook Kit 45902870505, TypeScript 45902870420 and branch janitor 45904314464. Forty enemy types, seeded reachability and existing survival/ending calibration shipped. Unlock t-016 for bestiary art.
<!-- note:end t-015 -->

## t-016 — Paint and integrate the full bestiary and three boss encounter plates

<!-- note:begin t-016 -->
Every one of the forty enemy types has unique Krea 2 artwork in target cards, including the three bosses and Mimic; reuse canon-compatible delivered assets. Each guardian also has an appropriate full-width battle plate. Record ArtJob and ArtImage IDs and verify final authenticated media URLs. No skull/crown glyphs as final combatants. Keep targeting, HP and statuses readable.

2026-11-26 PT: commit 93c0c8ce adds BESTIARY-2026-11-26.yaml, auto_submit Krea 2 priority 200, 36 ordinary portraits and three distinct guardian chamber scenes. Existing guardian and Mimic ArtJobs 69511-69513 and 69523 retained. Validated all 36 runtime keys and distinct prompt wording; CI and ArtJob receipts pending. Return ready after merge for delivery and integration.

2026-11-26 PT: Conductor #8080 merged 483c94a6 after four successful latest-head workflows. 39 private Krea 2 requests are on main with auto_submit enabled; no new ArtJob receipts yet verified. Resume delivery, curation, integration and URL checks, preserving existing guardian and Mimic assets.

Kind Robots commit 4f615697 integrates 18 DONE Krea 2 ledger receipts (jobs 77450-77467, ArtImages 280763-280780) into the private admin-only art registry. Verified unique IDs and enemy keys against runtime definitions. Actual authenticated image URLs and visual acceptance remain unverified; token absent and site DNS unavailable in runtime. Return ready after partial merge; remaining portraits and guardian plates pending. No duplicate jobs, no mature art changes.

Kind Robots #5934 merged 42076636; seven implementation workflows completed successfully. 18 ordinary portraits wired. Remaining 18 portraits and three guardian plates now have DONE receipts; integrate and test. Owner 2026-11-26 PT explicitly accepts completed render receipts as availability evidence; manual art approval is not a gate.

App head 6d2b5e4b maps the remaining 18 ordinary portraits and 3 guardian scenes from completed jobs 77468-77488 (ArtImages 280781-280801). Guardian battle stages use their own wide plates, separate from combat target portraits. Regression requires 40 distinct enemy art sources and three distinct guardian plates. All 39 new Krea 2 receipts plus four retained boss/Mimic portraits accounted for; owner-approved render-receipt acceptance applies. Close t-016 after green merge.

Kind Robots #5944 merged 4abdae6e, corrected head 045cd9b3: all seven implementation workflows and branch janitor completed successfully, including Playbook Kit 45939168471 and Contract Tests 45939168369. All 40 enemy target portraits and three dedicated guardian scenes wired and tested. Owner-approved render receipt acceptance applies. No manual art gate.
<!-- note:end t-016 -->

## t-017 — Distinct painted environments and significant encounters in live gameplay

<!-- note:begin t-017 -->
Show recognizable Ossuary Gate, Drowned Halls and Ember Deep landscapes during exploration and appropriate backgrounds during combat and room choices. Illustrate merchants, communities and significant authored non-court encounters, not merely six generic room types. Reuse canon-compatible existing artwork and queue only missing Krea 2 briefs; verify delivered URLs and responsive gameplay.

2026-11-26 PT: commit 4582e3fc commissions 15 missing non-court choice scenes in NONCOURT-ENCOUNTERS-2026-11-26.yaml, including all six community encounters. Existing six moment plates retained. Verified all 21 authored non-court event IDs against ledgers and checked prompt specificity (58+ unique words). CI, delivery and runtime bindings outstanding.

Conductor #8101 merged b5716014 after four completed successful workflows. Fifteen missing non-court scenes are on main with auto_submit enabled. Resume after receipt and visual verification, integrating all event-specific art. No delivered-image claim.

App head 7010d7cb maps all 15 new non-court DONE receipts (jobs 77489-77503, ArtImages 280802-280816), restores three existing moment mappings (jobs 69526,69527,69530), uses distinct authored encounter plates and layer-specific ordinary combat scenery. Regression asserts 21 distinct non-court event sources. Owner-approved receipt acceptance applies; manual visual checks are not a gate. CI pending; close t-017 only after green merge.

Kind Robots #5936 merged 14c55f7b after seven completed successful workflows, including Playbook Kit 45935725057 and TypeScript 45935725118. All 21 distinct non-court encounter plates wired and covered by regression; three layer landscapes used in exploration and ordinary combat. Owner-approved render-receipt acceptance applies. No manual art gate.
<!-- note:end t-017 -->

## t-012 — Every picture rendered, delivered, URL-verified and wired (set src / RENDERED_ART)

<!-- note:begin t-012 -->
Complete all rendered/delivered/wired art: Krea 2 normal anthropomorphic cartoon art; Furrytoon Mix XL v3 separate private adult-only romance unlocks, never public. Approved 94 normal and 41 mature jobs 69761–69895 have historical DONE records; #7564/#5303 accepted them via run 44256987440. #5641 references 122 approved normal assets; #5857 binds 12 court portraits; #5874 maps boss/artifact ArtImages 273855–273858, 273872–273873, 273875 (jobs 69511–69514, 69528–69529, 69531); #5895 maps badge jobs 69637–69656. #5902 merged 2478093b with all checks green, boss/Mimic and layer art wired. Actual authenticated delivery, visual curation, all intended surfaces and mature-unlock/privacy enforcement remain unverified. Coordinate t-016 bestiary/boss plates, t-017 environments and encounters, t-018 scrapbook/relationship art; don't duplicate pending jobs or assume art accepted by old references. Preserve organically earned knowledge and save gates. Review actual ledgers and media before claiming done. Full prior note: ROADMAP-HISTORY-2026-11-26.md#t-012.

App head bb973f1a restores three completed scrapbook receipts (jobs 69533-69535, ArtImages 273877-273879) for duo and guardian victories; adds all-ending and cast art coverage assertions. Full-party historical job 69532 explicitly depicts dwarf/elf rather than current animal-folk canon; held out pending suitable replacement. No duplicate jobs or mature asset changes. Return ready after partial merge; support art and remaining canon/gate reconciliation still outstanding.

Kind Robots #5952 merged a07a0156; all seven exact-head workflows and branch janitor green. Three scrapbook plates restored; all cast and distinct ending art assertions passed. Remaining full-party canon repaint and support art reconciliation outstanding.

Conductor commit c89b27b3 commissions one private Krea 2 Four at the Stair repaint using the current animal-folk spec and the unchanged moment:full-party node. All ten existing art ledgers checked; only legacy job 69532 / ArtImage 273876 depicts the obsolete dwarf/elf group. No duplicate pending replacement. After merge return ready pending job receipt, integration and delivery verification.

Conductor #8123 merged 2d8b21e4; all four exact-head workflows passed. Canon full-party repaint brief is on main; no ArtJob receipt yet. Return ready for integration and actual delivery verification.

Kind Robots head a2d4aaf2 adds opt-in authenticated media audit for all mapped normal ArtImages, anonymous route and direct-path rejection, same-origin redirects and image signatures, plus six mocked regression cases in existing Deepheart CI suite. No new art jobs, no live media request (token missing and DNS unavailable). Full-party job 77563 remains PENDING. Return ready after green merge, not done; actual delivery and curation remain outstanding.

Kind Robots #5977 merged 286ac884; seven exact-head implementation workflows passed on f16d7a2f (Playbook Kit run 45976884012). Branch janitor run 45981473535 was cancelled. Full-party job 77563 remains PENDING. Actual live media verification remains unavailable (token absent, curl DNS failure). Return ready for delivery and curation, not done.

Full-party Krea 2 job 77563 now DONE in FULL-PARTY-REPAINT-2026-11-26.yaml, ArtImage 280883. Kind Robots commit bb1ca511 maps the original moment:full-party slot to that ID, excludes obsolete 273876, and asserts distinct nonempty sources for every scrapbook moment. No new art jobs or save changes. Return ready after green merge if live authenticated delivery, visual curation, or private romance verification remains incomplete.

Kind Robots #5984 merged fd7c854e after all seven implementation workflows and branch janitor passed (Playbook Kit 45985738848). All 95 distinct scrapbook art sources pass coverage; full-party job 77563 / ArtImage 280883 wired. Return ready solely for actual delivery, visual curation and remaining maturity verification.

Kind Robots commit 384ee946 adds a read-only Deepheart Live Media Audit workflow, restricted to trusted main, with existing CI API authentication scoped to the audit step and fixed production origin. Automatically runs after relevant main changes; no new credentials or production writes. Live audit still needs successful execution and pixel/maturity curation before closure.

Kind Robots #5987 merged e19b17ce. Main-only media audit is integrated; live run evidence is still unavailable through the PR-only workflow listing. Return ready for delivery and curation, not done.

Live audit closes delivery: Deepheart Live Media Audit run 46021674043 on main e19b17ce
verified 257/257 mapped normal ArtImages (anonymous route 404, admin-authenticated
delivery, same-origin redirect, anonymous direct path denied, valid image signatures).
Route rejects isMature images and the registry asserts no private/after-hours keys, so
mature art stays out of normal surfaces. Per main-game-standard item 10, visual curation
is not a closure blocker. Pre-anthro ending plates 273934-273942 are re-commissioned
under t-018 (ENDING-PLATES-ANTHRO-2026-11-27.yaml).
<!-- note:end t-012 -->
