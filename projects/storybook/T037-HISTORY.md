# storybook/t-037 — full note history archive

This file is the archaeology index for storybook/t-037 ("Delete the client-side beat loop and rewrite its ~25 verifyStorybook*Guard scripts"). Its `note:` field in `roadmap.yaml` grew past `check_roadmap_note_size.py`'s 50,000-byte single-note threshold through ordinary recurring-cycle accumulation. The complete verbatim history through the archival point is preserved below; `roadmap.yaml` keeps only a short current-status pointer going forward. Do not restore this text into the live roadmap — read it here when you need to know what a specific past cycle found or did.

Archived under the AGENTS.md archival carve-out (byte-for-byte verified round-trip, pointer left behind, no history lost).

<!-- note:begin t-037 -->
Part C6's second half, split down to its landable core (conductor/t-158-era scope triage, 2026-09-17: the original t-037 bundled a localStorage migration, a 4-file deletion, ~25 verifyStorybook*Guard rewrites, 13 verifyDaVinci*Guard rewrites and ~29 workflow files into one task -- too large to land in one pass per AGENTS.md's Failure triage "scope" category, and genuinely sequenced: deleting the beat loop before its localStorage sessions have anywhere to go strands real reader data).
This task now covers ONLY: delete the beat loop in stores/storybookStore.ts, storybookLibraryHelper.ts, conductor/storybook-page.vue and storybook-visual-setup.vue (confirmed dead once t-052 lands -- already reachable only at components/pages/storybook-library-page.vue's `?legacy=1`), and rewrite the ~25 verifyStorybook*Guard.mjs/.ts scripts plus their storybook-*-contract.yml workflows against the new storybookRunStore.ts surface (the design doc's C6 section lists every one; do not skip or quarantine a guard to get green -- rewrite it). The 13 verifyDaVinci*Guard.ts scripts pinning storybook-life-run.vue are t-053's, not this task's -- they pin a different file with a still-open question about whether it is even in scope for deletion (see t-053's note).


Dependency reconciliation: t-052 is done and t-034/t-035/t-036 were already done, so every declared dependency for t-037 is satisfied. Promoting the stale waiting task to ready per the roadmap audit and resolver contract.

Connector dependency audit before deletion found a sequencing hazard that the current t-037/t-053 notes do not fully encode. stores/storybookStore.ts is still imported directly by components/storybook/storybook-life-run.vue, while t-053 deliberately keeps that component until after t-037 and itself depends on t-037. Therefore t-037 must not delete storybookStore.ts wholesale: it should remove the short/chaptered/episodic beat-loop state/actions and legacy setup callers, but preserve the life-only exports still consumed by storybook-life-run.vue until t-053 retires that component and its 13 Da Vinci guards. Direct-import search also found narrativeArtMilestones.ts, narrative-milestone-art.client.ts, storybook-state-panel.vue, storybookLibraryHelper.ts, storybook-library-page.vue, storybook-page.vue, storybook-life-run.vue, and storybook-visual-setup.vue referencing the store, so the implementation must migrate/remove each relevant dependency rather than treating the four files named in the older note as the complete deletion graph. No code was deleted in this cycle because doing so before reconciling these live dependents would break the ?legacy=1 life path that t-053 explicitly says must survive until t-037 lands. The task is returned to ready with this concrete implementation constraint; no human decision is required.

First bounded t-037 implementation slice: rewrote verifyStorybookSessionStorageRecoveryGuard.mjs against the server-backed storybookRunStore active-run pointer, preserving SSR safety and fail-soft blocked-storage behavior. Remaining beat-loop deletion and guard migration stays in t-037.

Reviewer merged kind_robots#2801 (silasfelinus/kind_robots@e6b3334) 2026-09-17: rewrote
verifyStorybookSessionStorageRecoveryGuard.mjs against storybookRunStore.ts's
readStoredRunId/writeStoredRunId, preserving SSR-safety and fail-soft blocked-storage
behavior for both read and write paths. All 45 kind_robots CI checks green,
mergeable_state clean, squash-merged. This was only the first bounded slice -- remaining
beat-loop deletion and the ~25 other verifyStorybook*Guard rewrites are still unclaimed
scope under this task id. Returning to ready (not done) for the next slice.

Second bounded t-037 slice: moved verifyStorybookAnswerRollbackGuard.mjs from the retired client answerCurrentBeat rollback implementation to the server-backed storybookRunStore submitMove contract. The guard now proves failed responses mutate no local turn state and successful responses append/apply state only after the success check.

Reviewer merged silasfelinus/kind_robots#2803 (squash
8085c43089ae887b8a0ea20666c6bce4a0665a6b) 2026-09-17: moved
verifyStorybookAnswerRollbackGuard.mjs from the retired client answerCurrentBeat
rollback implementation to the server-backed storybookRunStore submitMove contract,
proving failed responses mutate no local turn state and successful responses
append/apply state only after the success check. All 45 kind_robots CI checks green,
mergeable_state clean, squash-merged. This was the second bounded slice -- remaining
beat-loop deletion and the ~24 other verifyStorybook*Guard rewrites are still unclaimed
scope under this task id. Returning to ready (not done) for the next slice.

Slice 3 merged as silasfelinus/kind_robots#2806: migrated
verifyStorybookAnswerInputPreservationGuard.mjs off the retired client beat loop onto
the new engine's submitWritten()/writeMove() path. Re-armed to ready (recurring multi-
slice task) -- ~10 verifyStorybook*Guard scripts still reference the retired client
store and remain the next bounded slices (see kaizen list on kind_robots#2806).

Cycle 24 (conductor scheduled sweep, claude-
scheduled-20260917T1930Z-storybook-t037-slice4): investigated the kaizen list from #2806
before picking a 4th slice and found it names guards inaccurately -- grepped all
utils/scripts/verifyStorybook*.{mjs,ts} in kind_robots for real references (not just
comment mentions) to the retired storybookStore.ts/storybook-page.vue beat loop rather
than trusting the PR-authored list blind. Bigger finding: components/pages/storybook-
library-page.vue already gates on a `legacy` flag -- `!legacy` (the default, live path)
mounts StorybookStorymaker/StorybookTable on the new server-backed storybookRunStore
(openStory/loadRun/resumeActiveRun/fetchAdventures), `legacy` (only via ?legacy=1, per
t-053) still mounts the old StorybookPage/StorybookVisualSetup/StorybookLifeRun on
storybookStore.ts. So the new engine is not still-unbuilt scope -- it is already the
default, and t-034..036/t-052 (this task deps) are done. What remains splits three ways,
not one flat guard-by-guard list: (1) DONE -- 3 guards (AnswerRollback #2803,
SessionStorageRecovery #2801, AnswerInputPreservation #2806) pinned transferable
optimistic-update properties and were safely rewritten against
writeMove()/submitWritten() ahead of any deletion. (2) LEGACY-ONLY, no server-side
equivalent -- verifyStorybookLibraryPhantomSessionGuard,
verifyStorybookLibraryStorageRecoveryGuard,
verifyStorybookLibrarySessionConsistencyGuard, verifyStorybookSessionLibrary,
verifyStorybookDuplicateResumeGuard, verifyStorybookDuplicateArtCarryoverGuard,
verifyStorybookRestartScenarioFrameGuard, verifyStorybookRestartInputCompletenessGuard
all pin stores/helpers/storybookLibraryHelper.ts (a client localStorage recent-stories
cache with restart/duplicate). storybookRunStore.ts has no such client cache --
StorybookTable/fetchAdventures reads the library from the server instead. These 8 cannot
be faithfully "rewritten" one at a time against a feature that does not exist server-
side; they get deleted together with
storybookLibraryHelper.ts/storybookStore.ts/storybook-page.vue when the legacy path
itself is finally removed -- that removal (also dropping the ?legacy=1 flag t-053
pinned) is a single larger, riskier cutover PR, not a bounded slice, and needs
confirming no other live surface still imports storybook-page.vue first
(components/dreams/dream-narration.vue, components/rewards/reward-encounter.vue,
components/brainstorm/brainstorm-manager.vue, components/facets/facet-profile.vue, and
storybook-life-run.vue all currently reference it -- unchecked this cycle whether those
are real imports or comment/text mentions, that check is the right next investigative
step). (3) SETUP/DEEP-LINK, unknown new-engine parity --
verifyStorybookCharacterDeepLinkGuard, verifyStorybookConfirmArmScopeGuard,
verifyStorybookLibraryNewStoryConfirmGuard, verifyStorybookLocationDeepLinkGuard,
verifyStorybookObjectEntryLinks, verifyStorybookPickerRestoredSelectionGuard,
verifyStorybookPickerSearchResetGuard, verifyStorybookRestoreIdempotencyGuard,
verifyStorybookSeedQueryCapGuard, verifyStorybookSeedQueryRaceGuard all pin storybook-
page.vue setup-screen behavior (seedFromQuery deep links, picker state, restart/new-
story confirm arming) that is a different concern from the beat loop itself -- whether
StorybookStorymaker/StorybookTable has equivalent deep-link/query-seeding support is not
yet checked. (4) verifyStorybookBranchState and verifyStorybookStudio pin the whole
legacy studio surface broadly (setup shell art-first layout,
branch/consequence/inventory state via client-parsed [STORY_STATE] markers) and will
need a full rewrite once/if that shell moves, not a small patch -- storybookRunStore.ts
explicitly states "THE SERVER OWNS THE NUMBERS," so the STORY_STATE-marker mechanism
itself has no new-engine equivalent by design. No safe bounded slice this cycle that
would not mean fabricating an invariant for a feature that may not carry over --
attempting one blind risks a quality-category rejection (a guard that either passes
trivially or wrongly pins doomed legacy-only behavior as if it were the target). Next
cycle: check the 5 named components for real storybook-page.vue imports, then decide
whether category (2)/(3) is one bulk cutover PR (kill legacy code + delete these guards
together) or has any further genuinely portable sub-slice. No Kind Robots mutation this
cycle. Releasing the claim, re-arming to ready (recurring multi-slice task).

Cycle 25 (claude-scheduled-20260917T233141Z-storybook-t037-slice5): resolved cycle 24's open investigative question. Checked the 5 named components for real (non-comment) references to components/conductor/storybook-page.vue via git grep against origin/main: dream-narration.vue, reward-encounter.vue, brainstorm-manager.vue, and facet-profile.vue have none -- all mentions are code comments. storybook-life-run.vue's one mention is also comment-only. Repo-wide grep for real importers/consumers of storybook-page.vue found only: components/pages/storybook-library-page.vue (the known, intended <StorybookPage v-if="legacy" /> mount) and three utils/scripts/verify*.ts files that read its source text as part of a contract check (verifyGalleryIndexHydration.ts, verifyNarrativeRoles.ts, verifyNarrativeKit.ts -- these will need updating whenever storybook-page.vue is actually deleted, separate from the ~25 verifyStorybook*Guard list already tracked). So category (2)/(3)'s premise holds: the 5 named components are not part of the deletion graph and do not block a bulk cutover on their own account.

However, chasing category (3)'s deep-link/query-seeding parity question (does StorybookStorymaker/storybookRunStore have an equivalent to storybook-page.vue's seedFromQuery()?) surfaced a live product bug, not just a guard-migration risk: dream-narration.vue, reward-encounter.vue, and facet-profile.vue each navigateTo('/storybook', { query: { location|reward|character } }) with no legacy=1, so all three CTAs land on the NEW engine by default -- and storybook-storymaker.vue/storybook-table.vue have zero route.query/useRoute handling (confirmed via grep). The query param is silently dropped today, in production, for any reader using these three real CTAs. Filed as storybook/t-055 (new task, ready, stakes: reversible) rather than folding new-engine feature work into this already-large cutover task, per AGENTS.md scope discipline -- t-055 also directly unblocks category (3)'s ~10 verifyStorybook*Guard rewrites once it lands, since there would then be a real new-engine behavior to pin instead of a doomed-legacy one.

Still no safe bounded code-deletion slice this cycle for t-037 itself: the LEGACY-ONLY (8 guards + storybookLibraryHelper.ts) and SETUP/DEEP-LINK (10 guards) categories both remain blocked on decisions/work outside this task's own scope (the former on deciding whether the bulk cutover is one PR or has a further sub-slice; the latter on t-055 landing first). No Kind Robots mutation this cycle. Releasing the claim, re-arming to ready.

Investigated the next bounded slice (conductor scheduled sweep) before touching any file. Read the C6 authoritative guard list (projects/storybook/docs/storymaker-redesign.md) against the current kind_robots tree and traced three of the remaining storybookStore.ts-pinning guards to their new-engine equivalents:

- verifyStorybookRestartScenarioFrameGuard (protects storybookLibraryHelper.ts's restartInput() forwarding scenario: bible.scenario): the new engine's playAgain() (components/storybook/storybook-storymaker.vue) just calls runStore.leaveRun() and drops back to the Table -- there is no automatic rebuild-and-resubmit of a prior bible, so this specific hazard (a silent field-forwarding bug in an auto-restart function) has no new-engine code to attach to yet. Separately found: playAgain()'s own comment claims the reader returns "with their board still dealt", but storybook-table.vue's board ref (~line 344) is a fresh component-local ref with no persistence (no localStorage/sessionStorage/store-lift found), and the parent's v-if/v-else-if/v-else chain unmounts/remounts StorybookTable on every transition -- so the board is actually cleared on Play Again today, contradicting its own comment. Filed as storybook/t-059 rather than fixed here; out of this task's scope (guard migration, not new-engine feature work).
- verifyStorybookDuplicateResumeGuard (protects storybookLibraryHelper.ts's duplicateStory() resuming art polling on the copy): searched the whole new-engine surface (storybookRunStore.ts, storybook-storymaker.vue, storybook-table.vue) for "duplicate" -- no matches anywhere. The "Duplicate story" feature itself was not rebuilt in the new engine; there is nothing to rewrite this guard against.
- verifyStorybookSeedQueryRaceGuard (protects a route.query race between storybook-page.vue's seedFromQuery() and storybook-library-page.vue's updateStoryQuery(), both mutating query on the same mount): confirmed updateStoryQuery()'s call site is gated on storyStore.session (the OLD useStorybookStore()), which the new engine never populates -- StorybookStorymaker uses useStorybookRunStore() exclusively. The race structurally cannot fire once ?legacy=1 is gone. storybook-table.vue's own seedFromQuery() (added t-055) has no sibling component racing on route.query in the new tree.

All three guards' hazards are legacy-architecture-specific with no new-engine code to attach a rewritten assertion to right now -- recommend deleting them alongside storybookLibraryHelper.ts/storybook-page.vue when those files are actually removed, rather than force-migrating them to a vacuous assertion against unrelated files. Did not touch these three guards or the files they protect; no pass consumed (investigation only). Remaining unexamined slices: verifyStorybookLibrarySessionConsistencyGuard, verifyStorybookRestartInputCompletenessGuard, verifyStorybookRestoreIdempotencyGuard, verifyStorybookSessionLibrary, verifyStorybookStudio, verifyNarrativeArtPersistence (large -- spans 6+ shared narrative-art files beyond storybookStore.ts itself, likely its own multi-cycle slice), verifyStorybookConfirmArmScopeGuard, verifyStorybookLibraryMountReopenGuard, verifyStorybookLibraryNewStoryConfirmGuard, verifyStorybookAnswerInputPreservationGuard, verifyStorybookComposerImeCompositionGuard. Re-arming to ready; releasing the claim.

Cycle 26 (2026-09-22, scheduled Conductor Agent run, session 2026-09-22T220116Z-storybook-t037-hero-scenario-guard): picked up cycle 25's remaining-unexamined list before touching any file. Corrected two stale entries in that list against the live kind_robots tree: verifyStorybookAnswerInputPreservationGuard.mjs was already migrated to the new engine in an earlier slice (PR #2806, pins storybook-reading.vue/runStore.writeMove(), not the legacy store) -- it should never have carried over into "remaining unexamined". verifyStorybookLibraryMountReopenGuard.mjs and verifyStorybookComposerImeCompositionGuard.mjs never pinned the legacy store/page at all (they pin storybook-library-page.vue and narrative-response-composer.vue, both live new-engine files, from unrelated storybook/t-010 polish work) -- neither is in this task's scope.

Confirmed 7 more guards as LEGACY-ONLY (pin storybookStore.ts/storybook-page.vue/storybookLibraryHelper.ts directly, no new-engine equivalent, same bucket as cycle 24's original 8): verifyStorybookLibrarySessionConsistencyGuard, verifyStorybookRestartInputCompletenessGuard, verifyStorybookRestoreIdempotencyGuard, verifyStorybookSessionLibrary, verifyStorybookStudio, verifyStorybookConfirmArmScopeGuard, verifyStorybookLibraryNewStoryConfirmGuard. Also confirmed verifyStorybookSeedQueryCapGuard and verifyStorybookPickerRestoredSelectionGuard/verifyStorybookPickerSearchResetGuard are LEGACY-ONLY for a more specific reason than "unknown parity": they pin the old NarrativeIngredientMultiPicker widget's search-box/expand/selection-cap mechanics, and storybook-table.vue (grepped directly) has zero references to that widget or those concepts -- the new card-based Table has no equivalent UI to rewrite these against, so join the legacy-only bucket rather than bucket 3 (SETUP/DEEP-LINK). verifyStorybookCharacterDeepLinkGuard and verifyStorybookLocationDeepLinkGuard both hard-pin PAGE_PATH = components/conductor/storybook-page.vue directly (confirmed via grep for the PATH constants) -- also legacy-only for their "engine consumes it" half, though their CTA-side assertions (character-manager.vue / dream-narration.vue navigate correctly) remain live properties worth preserving in whatever guard covers those files after the legacy page is deleted.

Landed one real bounded slice rather than only investigating: verifyStorybookTableDeepLinkGuard.mjs (storybook/t-055's new-engine deep-link guard) only covered the three keys t-055 fixed a live bug for (location/facet/reward) -- but storybook-table.vue's seedFromQuery() has always also read ?character= (-> hero slot) and ?scenario= (-> thread slot), with zero guard coverage on the new-engine side for either. Extended the guard to assert both keys are read and resolved through cardForSlug()/playCardIfAbsent(), plus a withCharacterLock() gating check mirroring the existing genre-lock one (a locked character must not bypass the board's gate via a deep link). Verified non-vacuous (broke ?scenario= handling, confirmed the guard fails, restored and reconfirmed it passes), verified prettier/eslint clean using kind_robots' own lockfile-pinned toolchain (provisioned via conductor/scripts/provision_kind_robots_deps.sh, not an ambient npx resolution -- see storybook/t-063's prettier-version-drift finding), and ran the full verifyStorybookTable.mjs suite clean. PR: silasfelinus/kind_robots#2991 (open, CI pending at write time).

verifyStorybookObjectEntryLinks.mjs is a genuine split case worth flagging for the eventual bulk cutover: it checks facet-profile.vue/reward-encounter.vue/character-manager.vue/scenario-manager.vue CTAs (engine-agnostic, must survive) in the same file as a storybook-page.vue seedFromQuery() consumption check (legacy-only, must go). The bulk cutover should split this file rather than delete it outright, keeping the CTA-side assertions.

t-053 status check this cycle: still status=waiting (life-run.vue retirement not yet cleared) -- the bulk cutover of storybookStore.ts/storybook-page.vue/storybookLibraryHelper.ts + their ~13 confirmed-legacy-only guards remains blocked on that, not on any further per-guard investigation. Re-arming to ready (recurring multi-slice task); releasing the claim once PR #2991 merges.

Both companion PRs merged clean: silasfelinus/kind_robots#2991 (7f8935d) and
silasfelinus/conductor#5055 (03f705a). Re-arming to ready (recurring multi-slice task);
releasing the claim.

Cycle 27 (session 20260923T075757Z-storybook-t037-narrart-persist): closed out cycle 25's last remaining-unexamined item, verifyNarrativeArtPersistence.mjs (flagged then as "large -- spans 6+ shared narrative-art files beyond storybookStore.ts itself, likely its own multi-cycle slice"). Investigation only this cycle; no kind_robots code touched.

What the guard actually pins, traced line by line: it asserts across 10 files -- utils/narrativeArtProfiles.ts, utils/narrativeArtJobs.ts, stores/helpers/narrativeArtJobsHelper.ts, stores/artStore.ts, server/api/art/enqueue.post.ts, server/api/art/queue/narrative.get.ts, utils/narrativeTurns.ts, components/narrative/narrative-art-status.vue, plus TWO beat-loop-specific checks: a `for (const storePath of [storyStorePath])` includesAll loop against stores/storybookStore.ts, and a components/conductor/storybook-page.vue includesAll block. The taskmasterStore.ts leg of that loop was already dropped in storybook/t-047 (2026-09-14) per the guard's own comment.

Confirmed the first 8 files are NOT beat-loop scope -- they are the shared narrative-art job pipeline (centralized four-step Krea profile, enqueue idempotency/dedupe key, authenticated recovery-before-resubmit, poll-attempt cap with resume messaging) that components/storybook/storybook-life-run.vue -- the still-live "life" shape component, t-053's scope, currently status: waiting -- depends on directly: it imports createPersistedNarrativeArtJobsController() from stores/helpers/persistedNarrativeArtJobsHelper.ts (which wraps narrativeArtJobsHelper.ts) at its own component level (line 802) and calls POST /api/storybook/life/runs/[id]/art (attachLifeRunArt, server/utils/davinci.ts) directly -- it does NOT go through storybookStore.ts's art functions at all. So 8 of this guard's 10 pinned files protect code that survives t-037 and t-053 both; touching them here would be out of scope, not a legacy rewrite.

The beat-loop-specific remainder -- the storyStorePath loop (asserting storybookStore.ts keeps `art?: NarrativeArtJobState`, createPersistedNarrativeArtJobsController(), updateBeatArt, requestBeatArt, resumeNarrativeArtJobs, resumeEntries, retryBeatArt, the finale/opening ternaries), the adjacent `!storyStore.includes('await requestBeatArt(')` non-blocking-narration assertion, the persist()-writer try/catch-swallow check on storyStore, and the storybook-page.vue NarrativeArtStatus-slot checks -- genuinely has no new-engine code to attach a rewritten assertion to. Verified two ways: (1) grepped storybookRunStore.ts/storybook-reading.vue/storybook-storymaker.vue/storybook-table.vue repo-wide for NarrativeArtStatus, narrativeArtJobsHelper, retryBeatArt, requestBeatArt, updateBeatArt, resumeNarrativeArtJobs, enqueueArtGeneration, art.status -- zero matches in any new-engine file; (2) cross-checked against storybook/t-058 (filed 2026-09-21, still status: needs-human, unresolved), whose own independent trace concluded the same thing from the server side: server/utils/storybookRuns.ts's narrateInto() only stores pendingTurn.artPrompt as a string and never enqueues/attaches art, submitStoryTurn's response never includes an art field, and storybookRunStore.ts's `art` ref is only ever set from the server's initial load response or cleared to [] -- never grown as turns are played. t-058 is exactly the product decision (does new-engine in-scene art exist at all, yes/no) that would have to land before this guard's beat-loop remainder could be rewritten against anything real; forcing a rewrite now would mean fabricating an invariant for a feature t-058 says may not exist.

Disposition: verifyNarrativeArtPersistence.mjs is a SPLIT case, same shape as verifyStorybookObjectEntryLinks.mjs (cycle 26) -- most of the file (8 of 10 pinned paths) is live shared infrastructure t-037 must not touch; only the storyStorePath loop + the 3 adjacent storyStore/storybook-page.vue checks are LEGACY-ONLY and join the existing bucket (verifyStorybookLibraryPhantomSessionGuard and the ~14 others already confirmed across cycles 24/26) to be deleted -- not rewritten -- alongside storybookStore.ts's beat-loop remnants and storybook-page.vue in the eventual bulk cutover PR. Whoever does that cutover should trim only those specific lines out of verifyNarrativeArtPersistence.mjs, not delete the file: the profiles/jobs/controller/artStore/enqueue/recovery/turns/status-component assertions must keep running against storybook-life-run.vue's still-live pipeline.

This closes out cycle 25's remaining-unexamined list in full -- cycle 26 already resolved the other ten names on that list (one already migrated, two never in scope, seven confirmed legacy-only); this cycle resolves the eleventh and last, verifyNarrativeArtPersistence. No further per-guard investigation is independently pickable right now: what remains under t-037 is the bulk legacy cutover itself, still blocked on t-053 (status: waiting, life-run.vue retirement not cleared), and the split-file trims (this guard, verifyStorybookObjectEntryLinks.mjs) that ride along with that same cutover. No Kind Robots mutation this cycle -- investigation only, no pass consumed. Re-arming to ready; releasing the claim.

Cycle 28 dependency reconciliation: the previous cycle's conclusion that the bulk t-037 cutover is blocked on t-053 is backwards. t-053 explicitly depends_on t-037 because storybook-life-run.vue remains reachable only through storybook-visual-setup.vue until t-037 removes that legacy setup path. Therefore t-037 must proceed first, preserving only the life-only storybookStore exports consumed by storybook-life-run.vue; then t-053 can retire life-run.vue and its 13 Da Vinci guards. No code mutation this cycle because the claimed slice's latest handoff incorrectly described a circular blocker; corrected the implementation order instead of deleting code against that false premise. Next t-037 slice should perform the legacy setup/page/helper cutover and split-file guard trims already enumerated in cycles 26-27, while retaining the life-only store surface for t-053.

Cycle 29 (2026-09-23T14:00Z, scheduled Conductor Agent run, session claude-scheduled-2026-09-23T140000Z-storybook-t037-cutover): attempted to land the full bulk cutover cycle 28 called for. Did NOT execute a code deletion this cycle -- found a real blocker plus several corrections to the accumulated investigation that change the actual scope. Investigation only, no pass consumed.

CORRECTIONS to prior cycles' understanding (verified fresh against origin/main via direct grep, not trusted from notes):

1. storybook-life-run.vue is NOT an independently-live component that merely happens to import storybookStore.ts -- it is itself one of "the three branches" the THE STORYMAKER IS THE FRONT DOOR comment block in components/pages/storybook-library-page.vue (lines 249-266) explicitly groups with the outgoing client beat loop, reachable only at ?legacy=1. Its only entry point is storyStore.beginLife() called from components/storybook/storybook-visual-setup.vue:550 -- one of the four files t-037 itself deletes. This matches t-053's own already-recorded finding (its note's "BUT actual deletion is not safe yet" paragraph) but cycles 24-28 of THIS task's notes kept describing life-run.vue as surviving t-037 independently and needing its storybookStore.ts exports (art functions, etc.) preserved for its own sake. Checked directly: storybook-life-run.vue's only real storybookStore.ts usage is `useStorybookStore`, the `StorybookLifeSeed` type, and one call to `.endLife()`. It does NOT call updateBeatArt/requestBeatArt/resumeNarrativeArtJobs/retryBeatArt/resumeEntries on the store (it manages its own art via createPersistedNarrativeArtJobsController from persistedNarrativeArtJobsHelper.ts directly, confirmed by import list) -- those five were legacy beat-loop-only functions the guard-list note conflated with "what life-run.vue needs." Net effect: the "life-only surface to preserve" in storybookStore.ts is much smaller than previously assumed -- just beginLife/endLife/lifeSeed/StorybookLifeSeed plus base composable scaffolding -- and the post-cutover StorybookLifeRun branch in storybook-library-page.vue only ever mounts for a reader who already has a lifeSeed persisted in localStorage from before this deploy (a genuine in-flight-migration case, not a route anything can newly reach once storybook-visual-setup.vue -- the only beginLife() caller -- is deleted). This confirms and narrows the original scope-split note's own concern ("deleting the beat loop before its localStorage sessions have anywhere to go strands real reader data") down to exactly the life-run case, nothing broader.

2. The guard inventory is larger than "~25" and larger than docs/storymaker-redesign.md's own C6 list (17 named there, excluding the 13 DaVinci ones). Fresh grep for real (non-comment) references to storybookStore.ts / storybookLibraryHelper.ts / storybook-page.vue / storybook-visual-setup.vue / storybook-state-panel.vue across the whole tree found several guards and one whole plugin file no prior cycle's note or the design doc mentions:
   - components/storybook/storybook-state-panel.vue: only consumer is storybook-page.vue (grepped repo-wide) -- dead once storybook-page.vue goes, delete alongside it.
   - plugins/narrative-milestone-art.client.ts: its own header comment already says "scheduled for the same treatment by storybook/t-037" -- it is a global Nuxt plugin watching storyStore.session (beat-loop only) to enqueue scene art. Still fully LIVE today (serves any reader currently on ?legacy=1), so it cannot be deleted independently of storybook-page.vue -- must go in the same PR as the rest, not before.
   - utils/narrativeArtMilestones.ts: used only by the plugin above and its own guard verifyNarrativeArtMilestones.ts (grepped repo-wide, both confirmed) -- delete both alongside the plugin.
   - utils/scripts/verifyStorybookPageChoiceGroupGuard.ts (+ .test.ts) and verifyStorybookVisualSetupChoiceGroupGuard.ts (+ .test.ts): read components/conductor/storybook-page.vue and components/storybook/storybook-visual-setup.vue source directly by path (COMPONENT_PATH const) -- neither appears in the design doc's C6 list or any prior cycle's guard enumeration. Delete both pairs alongside the components they pin.
   - utils/scripts/verifyStorybookConfirmArmScopeGuard.mjs: reads BOTH components/pages/storybook-library-page.vue (live, staying) AND components/conductor/storybook-page.vue (legacy). Traced its actual assertions against the fresh read of storybook-library-page.vue below -- it pins the restartArmed/newStoryArmed "session-id watcher" reset behavior that lives entirely inside the `v-if="legacy"` header block. Delete.
   - utils/scripts/verifyStorybookLibraryMountReopenGuard.mjs: reads ONLY storybook-library-page.vue, but the onMounted() behavior it pins (`storyStore.openStory(directId)`) is itself inside the legacy-band script logic being removed (see finding 3 below). Delete.
   - utils/scripts/verifyStorybookLibraryNewStoryConfirmGuard.mjs: reads ONLY storybook-library-page.vue, pins the "New story" armed-confirm button -- also legacy-band (see finding 3). Delete.
   - utils/scripts/verifyStorybookSeedQueryRaceGuard.mjs: reads both storybook-library-page.vue and storybook-page.vue; cycles 25-26 already confirmed this race structurally cannot fire on the new engine. Delete.
   - utils/scripts/verifyStorybookComposerImeCompositionGuard.mjs: reads ONLY components/narrative/narrative-response-composer.vue -- confirmed (again, matching cycle 26) completely unrelated to this task, pins live narrative-response-composer.vue IME behavior. NOT in scope, do not touch.

3. Fresh full read of components/pages/storybook-library-page.vue (476 lines) confirms the ENTIRE `<header v-if="legacy">` block (15-119, the story-library toolbar: recent-stories count, Duplicate/Export/Restart/New-story buttons), the `<section v-if="legacy && libraryOpen">` block (121-207, the recent-stories grid), and every script-side function that exists only to serve those two blocks (openStory, duplicateStory, duplicateCurrent, restartCurrent, downloadStory/triggerDownload/downloadStoryAsMarkdown/downloadStoryAsJson/closeExportMenu, startNewStory, formatStoryDate, the two watch() blocks on storyStore.session.id and route.query.story, and the onMounted() lines calling restoreFromLocalStorage/initializeLibrary/openStory(directId)) are 100% legacy-band, safe to delete in the same PR as storybookStore.ts's beat-loop functions. Post-cutover this file reduces to: `useStorybookStore`, `legacy` (kept only to decide whether to show a lingering StorybookLifeRun), `storyStore.lifeSeed`-gated StorybookLifeRun branch, StorybookStorymaker as the unconditional default otherwise.

4. NEW FINDING, the actual reason nothing was deleted this cycle: the "LEGACY EXPORT NOTICE" block (lines 209-247, storybook/t-052) exists specifically to warn a reader with old localStorage-only beat-loop stories to export them "before it's removed" -- and this PR removing storybookLibraryHelper.ts + the recent-stories UI is that removal. Checked when the notice actually went live: `git log -S "storybook-legacy-notice-dismissed" -- components/pages/storybook-library-page.vue` finds exactly one commit, bbf9f91, dated 2026-09-21 20:31 -07:00 -- roughly 2 days before this cycle (2026-09-23). Deleting the legacy library/export access this soon gives real readers a very short window to have noticed and acted on that warning; the underlying raw localStorage bytes are not wiped by this deletion (only the app's UI/JS path to read them goes away), so this is a functional-access loss for the reader, not literal byte destruction, but it reads as data loss from their side either way. This is a genuine product-timing judgment (how long is long enough) rather than a code-correctness question, so did not execute the deletion. Recommend NOT landing the destructive half of t-037 before the notice has been live at least a reasonable while longer (no stated policy exists; flagging for a decision rather than picking an arbitrary number) -- OR, if Silas confirms 2 days is an acceptable window for this low-stakes legacy data, the cutover below is ready to execute as specified.

Everything above is investigation, not implementation -- storybookStore.ts, storybook-library-page.vue, and every guard file are unchanged this cycle. No pass consumed. Re-arming to ready; releasing the claim.

READY-TO-EXECUTE PLAN for the next cycle (once the export-notice timing question is resolved), so it does not need to be re-derived:
- Delete: components/conductor/storybook-page.vue, components/storybook/storybook-visual-setup.vue, components/storybook/storybook-state-panel.vue, stores/helpers/storybookLibraryHelper.ts, plugins/narrative-milestone-art.client.ts, utils/narrativeArtMilestones.ts.
- Edit stores/storybookStore.ts: remove weaveBeat, beginStory, answerCurrentBeat, finishStory, parseGeneratedBeat, applyStateDelta, buildBible, biblePrompt, buildRecap, statePrompt, phaseGuidance, updateBeatArt, narrativeArtContext, requestBeatArt, resumeNarrativeArtJobs, retryBeatArt, resetSetup, resetSession, restoreFromLocalStorage's session/library halves, library, recentStories, initializeLibrary, archiveCurrent, openStory, duplicateStory, restartStory, buildExport, setupDraft, session, isWeaving, errorMessage, streamingText, currentBeat, awaitingAnswer, isComplete, canFinish, and the StorybookSession/StorybookStartInput/StorybookBible/StorybookBeat/StorybookAnswer/StorybookStateDelta/StorybookBranchChoice/StorybookConsequence/StorybookInventoryItem/StorybookIngredient/StorybookSetupDraft/StorybookStructure/StorybookNarratorStyle/isBeatStructure/STORYBOOK_NARRATOR_STYLES/STORYBOOK_STRUCTURES types/consts they depend on. Keep: the store scaffolding (userStore, mode/setMode/dataTheme/isStoryStyled/modes/hydrateStorybookMode -- confirm these are UI-theme-only and not beat-loop-coupled before keeping, not yet independently verified this cycle), persist()/watch() trimmed to lifeSeed only, lifeSeed, beginLife, endLife, StorybookLifeSeed.
- Edit components/pages/storybook-library-page.vue per finding 3 above.
- Delete guards (confirmed legacy-only, no live counterpart): verifyStorybookBranchState.mjs, verifyStorybookDuplicateResumeGuard.mjs, verifyStorybookLibrarySessionConsistencyGuard.mjs, verifyStorybookRestartInputCompletenessGuard.mjs, verifyStorybookRestartScenarioFrameGuard.mjs, verifyStorybookRestoreIdempotencyGuard.mjs, verifyStorybookSessionLibrary.mjs, verifyStorybookStudio.mjs, verifyStorybookConfirmArmScopeGuard.mjs, verifyStorybookLibraryNewStoryConfirmGuard.mjs, verifyStorybookSeedQueryRaceGuard.mjs, verifyStorybookLibraryMountReopenGuard.mjs, verifyStorybookLibraryPhantomSessionGuard.mjs, verifyStorybookLibraryStorageRecoveryGuard.mjs, verifyStorybookDuplicateArtCarryoverGuard.mjs, verifyStorybookSeedQueryCapGuard.mjs, verifyStorybookPickerRestoredSelectionGuard.mjs, verifyStorybookPickerSearchResetGuard.mjs, verifyStorybookCharacterDeepLinkGuard.mjs, verifyStorybookLocationDeepLinkGuard.mjs, verifyStorybookPageChoiceGroupGuard.ts (+.test.ts), verifyStorybookVisualSetupChoiceGroupGuard.ts (+.test.ts), verifyNarrativeArtMilestones.ts. Explicitly NOT in scope: verifyStorybookComposerImeCompositionGuard.mjs (unrelated file, narrative-response-composer.vue), verifyStorybookAnswerRollbackGuard.mjs / verifyStorybookSessionStorageRecoveryGuard.mjs / verifyStorybookAnswerInputPreservationGuard.mjs (already migrated, slices 1-3), the 13 verifyDaVinci*Guard.ts (t-053's).
- Trim (not delete): verifyNarrativeArtPersistence.mjs (remove only the storyStorePath loop + adjacent storyStore/storybook-page.vue-specific checks, per cycle 27's line-level trace -- keep the 8 shared narrative-art-pipeline assertions), verifyStorybookObjectEntryLinks.mjs (remove only the storybook-page.vue seedFromQuery() check, keep the CTA-side assertions per cycle 26).
- Update (read storybookStore.ts/storybook-page.vue source text, will break once those shrink/disappear): utils/scripts/verifyNarrativeRoles.ts, utils/scripts/verifyGalleryIndexHydration.ts, utils/scripts/verifyNarrativeKit.ts, utils/scripts/verifyNarrativeStreamingTextIsolationGuard.mjs (pins weaveBeat, being deleted), utils/scripts/verifyStorybookActiveStoryResumeGuard.ts (imports type StorybookSession, being deleted) -- not yet individually traced line-by-line this cycle, do that before touching.
- Remove dead `.github/workflows/storybook-*-contract.yml` `paths:` entries for every deleted guard file (per the design doc's own instruction).
- Full verification: provision_kind_robots_deps.sh, vue-tsc, eslint, the full guard/contract suite -- do not trust a plausible-looking diff.

Cycle 30 (2026-09-23T16:25Z, scheduled Conductor Agent run): executed the first bounded
slice of cycle 29's READY-TO-EXECUTE plan -- the guard-deletion portion only,
deliberately split off from the destructive store/component cutover, which still needs
the export-notice timing question resolved (notice went live 2026-09-21 20:31 -07:00 per
cycle 29's git-log trace; the plan's 'reasonable while longer' is still a subjective
call worth Silas's confirmation rather than an agent picking an arbitrary number). This
slice touches zero production files and zero user-facing behavior -- it only deletes CI
guard scripts (and their workflow wiring) that 24-29 already confirmed protect
exclusively legacy beat-loop code with no new-engine counterpart, so it carries none of
the data-access timing risk.\n\nDeleted all 23 confirmed-legacy-only guards plus their 2
paired .test.ts files (verifyStorybookBranchState, verifyStorybookDuplicateResumeGuard,
verifyStorybookLibrarySessionConsistencyGuard,
verifyStorybookRestartInputCompletenessGuard, verifyStorybookRestartScenarioFrameGuard,
verifyStorybookRestoreIdempotencyGuard, verifyStorybookSessionLibrary,
verifyStorybookStudio, verifyStorybookConfirmArmScopeGuard,
verifyStorybookLibraryNewStoryConfirmGuard, verifyStorybookSeedQueryRaceGuard,
verifyStorybookLibraryMountReopenGuard, verifyStorybookLibraryPhantomSessionGuard,
verifyStorybookLibraryStorageRecoveryGuard, verifyStorybookDuplicateArtCarryoverGuard,
verifyStorybookSeedQueryCapGuard, verifyStorybookPickerRestoredSelectionGuard,
verifyStorybookPickerSearchResetGuard, verifyStorybookCharacterDeepLinkGuard,
verifyStorybookLocationDeepLinkGuard, verifyStorybookPageChoiceGroupGuard+.test.ts,
verifyStorybookVisualSetupChoiceGroupGuard+.test.ts, verifyNarrativeArtMilestones). Each
was re-verified (grep+read) to reference only legacy files and never a new-engine file
before deletion -- none needed to be skipped. Deleted 20 now-empty single-guard workflow
files; trimmed (not deleted) narrative-art-milestone-contract.yml and the shared
contract-tests.yml, which still cover unrelated live checks. Cleaned the corresponding
package.json script entries and the test:storybook aggregator.\n\nVerified: npm run test
(vue-tsc) PASS; npm run test:lint-ratchet PASS (329 problems/25 rules, -1, no rule
worse); npm run test:prettier-ratchet PASS (1032 unformatted/11 dirs, -15, no dir
worse); npm run test:storybook (edited aggregator) PASS including every remaining new-
engine storymaker/table/reading/ending guard; all workflow YAML still parses; final
repo-wide grep for all 23 filenames found zero functional references. All 29 kind_robots
CI checks green (0 failed), squash-merged.\n\nPR: silasfelinus/kind_robots#3023
(86555b8). No production code (storybookStore.ts, storybook-page.vue, storybook-visual-
setup.vue, storybookLibraryHelper.ts, etc.) touched -- the actual beat-loop/legacy-
page/component cutover from cycle 29's plan remains the next slice, still pending the
export-notice timing call. Re-arming to ready (recurring multi-slice task); releasing
the claim.

Cycle 31 (2026-09-23T20:01Z, scheduled Conductor Agent run): bounded slice migrating verifyStorybookObjectEntryLinks.mjs off the legacy storybook-page.vue. That guard's receiving-side assertion (that seedFromQuery() seeds a card from each query key) was pinning a dead end -- storybook-page.vue is reachable only at ?legacy=1 now, and the equivalent new-engine coverage already exists in full in verifyStorybookTableDeepLinkGuard.mjs (all 5 keys, cardForSlug()/playCardIfAbsent() resolution, genre/character gating, query clearing, mount ordering). Kept the guard's still-live, still-uncovered half: that facet-profile.vue/reward-encounter.vue/character-manager.vue/scenario-manager.vue's CTAs still fire and navigate to /storybook with the right query key. No production code touched. Verified: node utils/scripts/verifyStorybookObjectEntryLinks.mjs PASS; npm run test:storybook (17-guard aggregate) all PASS; eslint clean; prettier clean. All 27 kind_robots CI checks green, squash-merged as silasfelinus/kind_robots#3025.

Filed storybook/t-066 for a small kaizen: verifyStorybookTableDeepLinkGuard.mjs's header comment still points at verifyStorybookLocationDeepLinkGuard.mjs and verifyStorybookCharacterDeepLinkGuard.mjs, both deleted in the cycle-30 guard-cleanup pass (kind_robots#3023) -- stale reference, not a functional issue.

Remaining verifyStorybook*Guard scope: verifyStorybookActiveStoryResumeGuard.ts still functionally imports storybookLibraryHelper.ts/storybookStore.ts (the legacy library-resume behavior) and cannot migrate to a new-engine equivalent -- it is destined for deletion alongside the beat loop itself, not rewrite, so it stays blocked on the same t-065 (export-notice-timing) gate as the destructive cutover. No other guard files referencing the legacy store/helper/pages were found this cycle. Re-arming to ready (recurring multi-slice task); releasing the claim.

Cycle 32 (2026-09-26T07:00Z, scheduled Conductor Agent run): re-verified via this
session's audit_human_gates.py that storybook/t-065 (export-notice-timing confirmation)
is still status: needs-human, unchanged since cycle 31. Re-read cycle 31's conclusion:
all guard migration/rewrite work reachable without the destructive cutover was already
completed by cycle 31 (verifyStorybookActiveStoryResumeGuard.ts is the sole remainder
and is destined for deletion alongside the beat loop, not a rewrite target -- it stays
blocked on the same t-065 gate). No new bounded slice available this cycle; genuinely
blocked, not a quality/scope failure. Re-arming to ready; releasing the claim.

Cycle 33 (2026-09-26T13:58Z, scheduled Conductor Agent run): re-verified via this
session's audit_human_gates.py that storybook/t-065 (export-notice-timing confirmation)
is still status: needs-human, unchanged since 2026-09-23T16:25:27Z. Cycle 32's
conclusion stands: all guard migration/rewrite work reachable without the destructive
cutover was already completed by cycle 31; verifyStorybookActiveStoryResumeGuard.ts
remains the sole remainder and is destined for deletion alongside the beat loop, not a
rewrite target -- it stays blocked on the same t-065 gate. No new bounded slice
available this cycle; genuinely blocked, not a quality/scope failure. Re-arming to
ready; releasing the claim, moving to other priority-order work.

Cycle 34 (2026-09-26T14:59Z, scheduled Conductor Agent run): re-verified via this
session's audit_human_gates.py that storybook/t-065 (export-notice-timing confirmation)
is still status: needs-human, unchanged since 2026-09-23T16:25:27Z. Cycle 32/33's
conclusion stands: all guard migration/rewrite work reachable without the destructive
cutover was already completed by cycle 31; verifyStorybookActiveStoryResumeGuard.ts
remains the sole remainder and is destined for deletion alongside the beat loop, not a
rewrite target -- it stays blocked on the same t-065 gate. No new bounded slice
available this cycle; genuinely blocked, not a quality/scope failure. Re-arming to
ready; releasing the claim, moving to other priority-order work.

Cycle 35 (2026-09-26T16:56Z, scheduled Conductor Agent run): re-verified via this
session's audit_human_gates.py that storybook/t-065 (export-notice-timing confirmation)
is still status: needs-human, unchanged since 2026-09-23T16:25:27Z. Cycles 32-34's
conclusion stands: all guard migration/rewrite work reachable without the destructive
cutover was already completed by cycle 31; verifyStorybookActiveStoryResumeGuard.ts
remains the sole remainder and is destined for deletion alongside the beat loop, not a
rewrite target -- it stays blocked on the same t-065 gate. No new bounded slice
available this cycle; genuinely blocked, not a quality/scope failure. Re-arming to
ready; releasing the claim, moving to other priority-order work.

Cycle (conductor scheduled sweep, investigative slice per prior cycle's "next cycle" instruction): checked the 5 named components (components/dreams/dream-narration.vue, components/rewards/reward-encounter.vue, components/brainstorm/brainstorm-manager.vue, components/facets/facet-profile.vue, components/storybook/storybook-life-run.vue) for real storybook-page.vue imports. Four are comment-only mentions (no real import) -- safe, no action needed for them. storybook-life-run.vue has a real import of stores/storybookStore.ts (useStorybookStore(), storybookStore.endLife()), which is the already-known t-053 blocker (t-053 stays waiting on this task).

Bigger finding while grepping repo-wide for storybook-page.vue references: three guard scripts OUTSIDE the previously catalogued ~25 verifyStorybook*Guard / 13 verifyDaVinci*Guard sets also read components/conductor/storybook-page.vue directly and pin real behavior against it -- utils/scripts/verifyGalleryIndexHydration.ts (asserts the cast picker uses lightweight Character browse rows and excludes personality/backstory), utils/scripts/verifyNarrativeRoles.ts (asserts NarrativeRoleAssigner mounts, isNarrativeRoleKey validation, and query-based deep-link seeding), and utils/scripts/verifyNarrativeArtPersistence.mjs (asserts the <NarrativeArtStatus> beat-art integration: queueing/queued/rendering/done/failed/cancelled states plus retryBeatArt). A fourth, verifyNarrativePrimitives.mjs, reads the file for a negative assertion only (no useTaskmasterStore) -- trivially satisfied once migrated but its readFileSync has no try/catch, so it will crash (not just fail) once the file is deleted unless repointed first. verifyNarrativeKit.ts also lists the file but already filters missing files gracefully -- no action needed there.

Checked whether the new engine (storybook-table.vue / storybook-storymaker.vue / storybook-reading.vue) already carries equivalent behavior for each: the cast-picker property (verifyGalleryIndexHydration) DOES already hold in storybook-table.vue -- it casts via characterStore.browseCharacters.map(toHeroCard).map(withCharacterLock), the same lightweight-DTO pattern, so that guard is a straightforward repoint once storybook-page.vue goes away, not a feature gap. The beat-art property (verifyNarrativeArtPersistence) is a REAL GAP, not just a guard-migration chore: storybook-reading.vue's sceneArt only renders via `v-if="sceneArt"` when an ArtImage already exists on the run -- there is no queueing/rendering/failed/cancelled status indicator and no retry control in the new engine at all. A beat whose art generation fails or is still queued currently just shows no frame, silently, with no way for the reader to retry. Filed storybook/t-070 to close this gap (or have Silas explicitly accept the silent-no-frame behavior as intentional) before the bulk cutover PR deletes storybook-page.vue and verifyNarrativeArtPersistence.mjs's pinned behavior with it -- deleting first would ship a real regression, not just remove a redundant guard.

No Kind Robots mutation this cycle (pure investigation + one new roadmap task filed). Re-arming to ready. Next cycle: decide the verifyGalleryIndexHydration/verifyNarrativeRoles/verifyNarrativePrimitives repoint (mechanical, low-risk) versus wait on t-070 (blocks safely deleting the beat-art guard's pinned behavior) as the next bounded slice, or split them.

Silas, 2026-09-30 (via t-065): the destructive beat-loop slice may land on or after
2026-10-05. Not before.
<!-- note:end t-037 -->
