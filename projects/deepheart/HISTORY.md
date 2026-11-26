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
