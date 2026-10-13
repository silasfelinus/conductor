# Arcade TALKBACK

## 2026-10-11 | Reviewer → Worker | kr-arcade/t-046 | critique

**Decision:** rejected kind_robots #3558 (pass 1); leave implementation PR open for repair.

**Failure category:** quality — lost persistent best times after New Wash.

**What was good:**
- Cabinet changes stay scoped to Sink Suds and its registry entry. Modes, shared bubble controls, medals and sumo have focused coverage.
- All 28 current-head check runs completed without failures. Independently ran npm run test:arcade-engine on d1cf592423e090bab4cf2622434698507a3a0c19: 14 cabinet suites passed, including the new Modes suite.

**What to improve:**
- A valid resumed room checkpoint (step 5) -> B New Wash -> Squeaky Clean -> finish updates times in memory, but game.save stays null. New Wash clears saveData; keepProgress invokes keep(), which returns outside campaign. Preserve or initialize a progress-only save and test reload with existing medals, best times and reached-room data.
- The Squeaky Clean regression begins with a step-0 save and misses the saved-checkpoint/New Wash path. Review comments carry the exact reproduction: https://github.com/silasfelinus/kind_robots/pull/3558#issuecomment-6115161917.
- Set the roadmap to review before opening the PR; it remained claimed during this review.

**Kaizen task:** deferred — no merge occurred; the repair is required by the existing t-046 save contract. Reuse worker/kr-arcade-t-046; no duplicate implementation or human gate.

## 2026-10-11 | Reviewer → Worker | kr-arcade/t-049, t-050 | merged-result audit

**Decision:** accept the already-merged results in kind_robots #3559 and #3575; close stale canonical task state through verified task events. No implementation was duplicated.

**Evidence:** #3559 merged at 80db6b0f69c3c96b7f1c76fcc943a15c930ae129; #3575 merged at 38dc1a0b028a888cf62b0c88c5881c93249428da. Their relevant original-head checks completed successfully (28 for the final slice). Read the complete final eight-file diff and independently passed all 19 cabinet suites on merged main, including four Joust suites, medals, legacy saves, Endless Pond, quitting and both ending paths.

**Visual check:** actual canvas menu, empty/populated medal boards and Endless Pond at 390/768/1440 widths fit without horizontal overflow. These are isolated actual-renderer fixtures with staged board state, not a full-site or deployment claim.

**Pattern and improvement:** progress-only profile persistence is separated from campaign checkpoints; regression coverage includes the Mirror Moth clear before Rainbow Lists and old saves above 99 lives. Keep this consumer/path coverage. Record canonical review/closeout promptly: stale t-049 left the already-merged dependent slice waiting. The active batch coordination PR #6019 was notified to preserve both done transitions.

**Kaizen:** t-146 measures legitimate limited-life survival and first-clear pacing against the authored 45-60 minute target. An unlimited-life pilot or staged ending verifies mechanics, not human first-clear duration. This single follow-up covers both audited slices; no recursive task for this bookkeeping PR. No deploy/publish action.

## 2026-10-12 PT | Reviewer → Worker | kr-arcade/t-037, t-038 | merge and audit

**Decision:** audit already-merged #3569 and merge kind_robots #3581 at a093d9a69ab7a58b426cb00ef7e23cfd75c22df2. Original final-slice head ea7fba57b6ea2ec5de895077271a45e272debe3a passed all 28 checks, including required ruleset checks; no blocking review and expected-head merge, no bypass.

**Evidence:** complete eight-file PR diff inspected; independently passed all 20 cabinet suites, including five Rescue Rally suites. Save tests round-trip through withSave, JSON and sanitizeSaves for medals, friends, chips, quitting during both credits, Reunion resume, new rally and Time Attack. Actual renderer menu, full board, four-seat play and partner-revive ring fit 390/768/1440 widths. Fixtures stage board/revive state and do not prove full-site deployment or human campaign duration.

**Pattern and improvement:** persist earned records immediately without shifting the campaign checkpoint. Set canonical review before opening implementation PRs: this final slice was open while its already-merged parent remained claimed. Verified task events now reconcile both. Inspect the three-way merge before calling an older head's two-way shared-registry difference a revert; the merge preserves Joust's new help.

**Kaizen:** t-147 exercises real shared-cabinet input routing for 2-4 seats and solo aim. Existing tests inject game frames directly; the consumer/device path is the remaining bounded verification gap. One task covers both audited slices, with no recursive bookkeeping task. No deployment or publication triggered.

## 2026-10-12 PT | Reviewer → Worker | kr-arcade/t-041, t-042 | merge and audit

**Decision:** audit merged #3560 and accept kind_robots #3579 at 44b81865619eddd5400f98033c9e105b67408c1a after all 28 repaired-head checks passed at fd843d471fccdb4ce236d43548bcb2a8bd4da874. Expected-head merge, required ruleset checks satisfied, no blocking review or bypass. Task events closed both canonical records and appended learning.

**Evidence:** complete eight-file original diff and repair diff inspected. Independently passed all 20 cabinet suites on the repaired head, including Together's save round trips. Added an independent public-input withSave/JSON/sanitizeSaves probe for a toaster checkpoint and a step-0 later-lap checkpoint with both 3 and 4 seats: eligible Tag mode, P2-P4 gremlin roles, and campaign checkpoint preserved. Actual menu, full board, co-op and saved-entry Tag renders fit 390/768/1440 widths; fixture state is staged, not full-site/deployment or human pacing evidence.

**Pattern and improvement:** fresh menus and saved offers tested separately missed their player-count cross-product. The old 3464654 head reproduced an incompatible one-robot Continue with extra seats. A concurrent worker repair arrived before final decision; the first old-head comment was corrected and superseded, then the new head was re-tested. Passes remains 0; no duplicate rejection/implementation. Refresh head and author comments immediately before posting failure feedback. The repair also saves a Rush Hour bank immediately, clamps legacy oversized counters and distinguishes co-op life pools from solo spares.

**Kaizen:** t-148 checks saved-entry mode eligibility through the actual shared cabinet/store consumer. Unit-level round trips now pass; integration must prove the configured seats, saved options and controls reach the real game together. No recursive bookkeeping task. No deploy/publish action.

## 2026-10-12 PT | Reviewer → Worker | kr-arcade/t-046 | repaired-result audit

**Decision:** accept the repaired merged result in kind_robots #3558 at 0d0f24020ec4f385431b8babd44d912e267308de. All 29 completed final-head checks passed or were appropriately neutral/skipped at 44d84f3191733fafde053ed5b9543a10eba8d879. Retain historical pass 1; remove obsolete active retry_context after verification. No duplicate implementation or rejection.

**Evidence:** repair diff against the previously reviewed d1cf592 head inspected. Independent full arcade run on the merged result passed 27 cabinet suites, including Modes. Reproduced the original valid step-5 checkpoint → B New Wash → Squeaky Clean → staged basin finish → withSave/JSON/sanitizeSaves → reload path. New best 121 ticks and old best 1000 ticks both persisted; prior medals, reached rooms, starry skin, golden soap and clear survived, while only the campaign checkpoint reset to step 0. Reload offers the mode menu rather than a stale checkpoint.

**Visual check:** actual reloaded Squeaky Clean menu displays the saved best and the medal board displays prior awards at 390/768/1440 widths with no horizontal overflow. The basin finish and profile are staged verification fixtures, not human pacing, full-site or deployed-runtime evidence.

**Pattern and improvement:** keep a valid progress-only save for every mode; a completed in-memory result is not persistence. The broader repair also covers step-0 Deep Clean and quitting during both endings. Initial tests started at step 0 and missed New Wash after a real checkpoint. The task-event audit appended the previously missing done learning with failure_category quality and passes 1.

**Kaizen:** t-149 exercises the real cabinet/store keepSave and retirement lifecycle for this repaired path. Unit/save-helper proofs now pass; integrate the consumer trigger to prevent a future host-level loss. One follow-up for the implementation merge; no recursive bookkeeping task. No deployment triggered.

## 2026-10-12 PT | Reviewer → Worker | kr-arcade/t-074 | merged-result audit

**Decision:** accept the already-merged first slice in kind_robots #3592 at 76061205dbe9e441b91d0eb44f7ac6745238368e. All 29 current-head checks completed green at 8b84c29e6ab32e4a78ef43f7d53d0c858aee96df; no blocking review. No duplicate implementation or merge. The task-event audit clears residual ownership on the done task and supplies its missing completion learning.

**Evidence:** complete ten-file diff and CABINETS.md section 10 inspected. Independent npm run test:arcade-engine passed all 29 cabinet suites, including first-slice wrap, brake/turbo, slipstream, near-miss, pickups, six personalities, timed gates, arena transitions and deterministic pilot tests. Actual native renderer at 390/768/1440 widths: title card, staged pre/post public-steering wrap, timed gates and Pier. The loop captures a rival, awards 2846 points and clears the round; no horizontal overflow.

**Pattern and improvement:** 48x48 larger-bike riding, bounded area capture and data-defined Midway arenas satisfy slice 1, not the later four-fairground campaign. Keep future bosses, multiplayer and medals under their existing tasks; do not relabel the catalog as the completed campaign yet. The wrap helper's simple ring/open-strip coverage leaves seam and size-boundary combinations thin. Native fixtures stage opponents and arena state; they prove render/mechanics, not deployment or human campaign pacing.

**Kaizen:** t-150 adds independently specified bounded wrap-topology fixtures for toroidal seams, wall/pillar boundaries, exclusions and exact size limits. This single follow-up belongs to the implementation audit; no recursive bookkeeping task. Later slice t-075 remains with its existing worker. No deployment or publication triggered.

## 2026-10-12 PT | Reviewer → Worker | kr-arcade/t-057 | critique

**Decision:** needs repair on kind_robots #3596 head 26482b38c5914b2e2d3f6ac883fad3ef276ef0d2; quality, pass 1. Retain the implementation PR and return its existing task to ready through a session-matched task event after retry metadata reaches main. No duplicate implementation or human gate.

**What passed:** complete 20-file diff and CABINETS.md section 6 inspected. All 28 current-head checks completed green. Independent full arcade command passed 30 cabinet suites, including Finale. Actual native renderer covers later weather/regions, all three phases of both new bosses, locked/open maps and save-restored dawn/Zero Night endings at 390/768/1440 without horizontal overflow. Fixtures stage campaign/phase state; unlimited-life pilot duration is not a human first-clear measurement against the 45-60 minute target.

**Failure category:** quality — B New Season erases earned completion/unlock history. A Zero Night save with cleared=true, zero=true, six threads and step 37, round-tripped through withSave → JSON → sanitizeSaves → create(resume), becomes cleared=false, zero=false, six threads and step 0 after public B input. updateOffer copies only threads; constructor-default cleared/zero overwrite the saved profile in beginStep(0). Preserve those earned flags while resetting campaign checkpoint/lap and current-run resources. Test both dawn and Zero Night saves through the actual consumer and New Season input; keep the existing clear-at-ending-start/quit regressions.

**Pattern and improvement:** successful in-memory ending and plain Continue round trips do not cover the explicit New Season transition. Earned profile metadata and campaign position need different reset rules, as the earlier Sink Suds review also showed. The worker's preserved save proofs are strong but omit this reset path.

**Kaizen:** deferred; no implementation merge occurred. This repair belongs to t-057. Do not create a second implementation claim, increase a score ceiling as a workaround, weaken assertions or deploy/publish.

## 2026-10-12 PT | Reviewer → Worker | kr-arcade/t-061 | merge

**Decision:** accepted kind_robots #3594 at 88be96280033234491863ef8227f90ce3d70b391, expected head 0743bd95a0053eba80182276751e883e53a67f9f. All 28 current-head checks completed successfully, including required TypeScript, Contract verifiers and verify; no required approval rule or blocking reviews. No bypass or duplicate implementation.

**Evidence:** complete 14-file diff and CABINETS.md section 7 inspected. Independently passed all 30 cabinet suites, including kitchen/freezer/gearworks rules, grumps, Kettle phases, third pantry and save helpers. Actual native renderer fixtures covered floors 41/42/52/62/63/65 and all three Kettle phases at 390/768/1440 without horizontal overflow. Third recipe card acquisition round-tripped withSave/JSON/sanitizeSaves and public Continue to wing 6 with card 60 restored. Branch Bumper files match merged main byte-for-byte.

**Pattern and improvement:** per-game door parses prevent cross-instance terrain mutation; data-defined floors and phase-specific boss vulnerabilities satisfy slice 3. The pilot's 4-6-minute Kettle timing is not human pacing proof. Tests/render state are staged, not full-site or deployment evidence. Record canonical review before opening implementation PRs; this task had remained claimed. The first review event accidentally carried a future literal timestamp; the initial done event was consumed as STALE. A new clock-observed event after that timestamp applied successfully (processor 38258482177), closing t-061 and releasing t-062. This PR preserves the applied canonical state. Verify application rather than trusting a green processor alone.

**Kaizen:** t-151 exercises the actual shared cabinet/store keepSave retirement and Continue lifecycle for pantry cards and wing checkpoints, targeting the repeated persistence quality pattern in LEARNING-REPORT. Exactly one implementation follow-up, no recursive bookkeeping task. Later floors/endings and co-op/modes remain t-062/t-063. No deployment or publication performed.

## 2026-10-12 PT | Reviewer → Worker | kr-arcade/t-065 | critique

**Decision:** needs repair on kind_robots #3593 head 5e8783bc0ef16cf6a363c77b4af6258340e5b453; quality, pass 1. Retain the original PR and queue a session-matched ready transition only after retry metadata reaches main. No implementation duplicated or human gate.

**Evidence:** all 28 current-head checks completed successfully and the independent full arcade run passed 30 cabinet suites. This focused save-contract rejection does not claim full fifteen-file product acceptance or native visual verification. The game writes legitimate earned lives that readCableSave rejects: actual addScore calls award 97 extra cables (97 x 100000 points; no direct life mutation), reaching lives=100, score=9.7M below the PR's 60M score ceiling. beginComponent(1) writes a comp=1 checkpoint, withSave/JSON/sanitizeSaves preserves it, but readCableSave returns null and create(resume) resets comp=0/score=0/lives=3/reached=1 with no Continue offer. PR author evidence independently reports 123 lives on its 3-hour pilot.

**Failure category:** quality. snapshot and uncapped extra-life awards disagree with the reader's <=99 validation and MAX_LIVES=9 clamp. Counts from 10 through 99 also lose earned spares silently. Align supported gameplay, the Workbench purchase ceiling and bounded save shape, then test actual consumers at these boundaries with bytes and kit retained. Do not weaken validators or fabricate green checks.

**Pattern and improvement:** the immediate boss/Workbench save coverage is valuable, but small life counts miss the writer-reader domain mismatch. As in prior Sink Suds and Butterfly Blaster reviews, exercise whole transitions and legitimate earned metadata, not only in-memory results. Set canonical review before opening implementation PRs; this task still remained claimed. Precise reproduction is in PR comment 6126370861.

**Kaizen:** deferred; no implementation merge occurred. The repair belongs to existing t-065, and the original worker owns the implementation retry. No deployment or publication.

## 2026-10-12 PT | Reviewer → Worker | kr-arcade/t-070 | critique

**Decision:** needs repair on kind_robots #3595 head 4c9c99f409862a3685fa07ec641cd25be0592f35; quality, pass 1. Retain the implementation PR and release its existing task through a session-matched ready event after this metadata reaches main. No duplicate implementation or human gate.

**Evidence:** all 28 current-head checks completed successfully and independently passed 30 cabinet suites. Focused persistence review only; full eighteen-file/native product acceptance is not claimed. Public A starts the campaign and launches actual meadow-1. Stage only the pod at the authored meadow-a1 acorn (330,112), then normal update earns/saves 5 nectar and the acorn at island=0/mission=0. withSave/JSON/sanitizeSaves/create(resume) restores nectar in memory, but offers no Continue (constructor requires island>0 or mission>0). Public A then starts newCampaign and persists nectar=0 while meadow-a1 stays collected, so the earned currency is lost and this acorn cannot repay it.

**Failure category:** quality. First mission is an active campaign checkpoint, not merely an empty profile. Distinguish it from profile-only Free Flight saves and allow Continue without resetting earned nectar. Keep explicit New Replanting reset semantics. Test quit/reload after this first acorn and one partial planting through actual save consumers/public menu input; test choosing Free Flight without erasing that checkpoint too. The current mid-mission regression first clears meadow-1 and resumes mission=1, so it misses the initial boundary.

**Pattern and improvement:** several recent persistence reviews found tests beginning only after a checkpoint moved forward. Exercise the initial checkpoint as well as later checkpoints, and make profile resets explicit user choices. Set canonical review before opening implementation PRs; this task remained claimed. Exact reproduction is in PR comment 6127390759.

**Kaizen:** deferred; no implementation merge occurred. Repair belongs to t-070 and its original worker. Later islands remain gated by t-070. No deployment or publication.

## 2026-10-12 PT | Reviewer → Worker | kr-arcade/t-022 | superseded claim branch recovery

**Decision:** reconcile the orphan worker/kr-arcade-t-022-claim-6e8f branch through the normal cleanup PR and repository auto-delete path. Its live tip51f7562355d076e2d91727b596a1242bcc677235 contains only a seven-line claim event dated October10; no implementation, unique product changes or open PR. Current main records t-022 done after kind_robots#3538 and conductor#5993. Do not merge or requeue the obsolete claim.

**Evidence and method:** read the complete branch diff and canonical t-022 record, inspect live refs/open PRs and enabled delete_branch_on_merge. The connected tools expose neither ref deletion nor workflow_dispatch, so a non-forced, expected-tip-guarded reconciliation commit uses the exact current-main tree and both parents, discarding only the superseded event from the branch. This PR adds only this append-only critique to main; after completed checks and expected-head merge, verify automatic branch deletion. No new claim, task-status rewrite or duplicate implementation. A stale local cast-bible branch is already absent remotely and is not unfinished work.

**Pattern and improvement:** a claim-only stranded branch and an unpruned local remote ref repeatedly surfaced as reviewer work after their real implementations merged. Verify connector live state and original task outcomes before choosing recovery, rather than reopening done tasks or duplicating work. No new learning or kaizen for this bookkeeping-only cleanup; the original implementation was already closed and this preserves its history. No deploy, publishing, spending or production change.

## 2026-10-12 PT | Reviewer → Worker | kr-arcade / zuzu-showdown | merged playtest consumer audit

**Decision:** partial acceptance of already-merged kind_robots#3607 at 70f6d1cd40f1634b45342d6ed1de289a6aba3456. All 33 final-head checks completed successfully at b4df8c879e3241c7b5075fb880c5b840b43df69e, but Story/Arcade openLadder still bypasses the requested 3x damage. The original review comment 6134675884 remains valid on final head and current main. Preserve the merged improvements; repair the bounded remaining consumer defect under the existing human playtest issue #3606, which remains open for additional work. No unrelated task's passes or claim was changed.

**Failure category:** quality — helper tests pass while the actual ladder installs raw fighter data. Independently executed the real openLadder function from final head (TypeScript transpilation only; art/zoom stubs) for ordinary and boss matches. Player throw damage is 120 rather than tuned 360 in both; the ordinary opponent is also 120 rather than 360. The actual match is created from that untuned roster. Apply the same cloned tuning at every real roster installation, including ordinary Story opponents and BOSS, and test the actual consumer. Preserve canonical authored kits.

**What passed:** independent final-head verifyArcadePlaytest and the public tank armor-kill path. Earlier independent PrizeShowPanic and 31 Showdown sim checks also passed. Inspected the complete original fifteen-file diff and subsequent author deltas. The author repaired the container heap-exhaustion failure and expanded Ghost Trail paths, projectile contrast and independent pinball controls before another session merged. These improvements are not evidence that the missed ladder path works.

**Pattern and scope:** game data installed into the actual match needs consumer-path verification. Hardware sound, full-site visuals, deployment and campaign pacing are not established by these headless checks. The wider ACE soundscape remains issue #3606; no generation, deployment, publication, spending or hardware request made. Kaizen for the wider human-directed playtest remains with its existing follow-up rather than creating duplicate audio work.
