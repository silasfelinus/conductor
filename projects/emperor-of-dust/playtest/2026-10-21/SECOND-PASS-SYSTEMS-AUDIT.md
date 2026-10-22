# Emperor of Dust: systems and hidden-follower playtest follow-up
**Recorded:** 2026-10-21 PT · **Status:** implemented systems verified; editorial five-act re-scoring still open

## Scope and verified changes
A second pass on the 50-day court game focused on available follower labor, costly recovery, NPC agency, varied daily surprises and the shape of player choices. This does **not** substitute for the requested per-act scored editorial rubric or live playthrough; see t-044.

- **Baseline:** four starting followers. On scripted early crisis days, posting one more random chore made perfect/near-perfect quest completion a scheduling impossibility. **Correction:** optional chores are suppressed when the board/active roster is full and on early or decadal crisis days, instead of always adding load.
- **Danger kept:** injury rates remain calibrated by the existing danger bands; the balance simulator objected when lowering risk globally made reckless play indistinguishable from careful play. **Correction:** preserve genuine costly expedition consequences, but add Kiyo's brass-funded full treatment alongside existing single-day surgeon and herbal poultice care.
- **Friendship and romance:** the already-established koala healer Kiyo gets a self-directed route with friendship, romance, realistic boundaries and mutually chosen endings. Romance is one branch, not the only reward for affection.
- **Daily unexpected happenings:** 26 distinct motif events per act and a secret visitor per act, **135 unique events** per 50-day campaign, seeded/reproducible, never repeating within a save. Five additional followers are gated by encounters and still require recruitment, rather than being given away as a reward.
- **Companion substance:** eleven new branching conversations across Nettle, Tiller, Sera, Tarn and Odo, with thirteen epilogue variations keyed to choices, four rare existing items in specific branches and lasting faction/brass effects.
- **Early-event editorial fix:** the first act's 26 surprise events received **52 bespoke decisions/outcomes**, replacing repeated generic trading-or-charity phrasing. The later 104 regular events still reuse motif-level mechanics and are next in the editorial queue.

## Evidence: checks that actually ran
- Kind Robots **#4013**, squash `002555303504d80b7feecf03828afa5f7e21f953`: all 16 GitHub Actions workflows and 21 check runs passed, including `verifyEmperorFortress.test.ts`, `verifyEmperorFortressBalance.test.ts`, `verifyEmperorFortressStore.test.ts`, `verifyEmperorFortressChanceEvents.test.ts`, TypeScript, layout and repository contract shards.
- Kind Robots **#4015**, squash `1a54b174517b10a8bf3b7e28b285874369acb20e`: all 14 workflows passed, including `verifyEmperorFortressSecretTalks.test.ts`, existing fortress/balance regressions, formatting and TypeScript.
- Kind Robots **#4016** (pending at note creation): Act I's 26 replacement choice-pairs, with a uniqueness and persistent-flag contract; its check status must be reverified before merge.

## Art pipeline: distinct lifecycle stages
- Conductor's **SECRET-FOLLOWERS-ROUND-1.yaml**: 40 ArtJobs **43119–43158** submitted and recorded. Status seen at this writing: one `RUNNING`, 39 `PENDING`; none claimed delivered.
- Conductor's **QUESTS-MISSING-ROUND-2.yaml**: 63 new quest notice/result ArtJobs were recorded as `DONE`, but image export and runtime wiring must still be verified independently.
- This follow-up stages **CHANCE-ACT1-ROUND-1.yaml** (78 compositions: notice/branch A/branch B for each Act I surprise) and **SECRET-STORY-SCENES-ROUND-1.yaml** (43 compositions: three per new talk, two per secret first visit). The Conductor Auto Art Generate workflow will enqueue them privately and record job IDs idempotently after merging the ledger, provided render-box/API health gates pass. New ledger requests are not equivalent to finished images.

## Remaining tests and editorial risks
1. The 2026-10-21 five-act editorial rubric still needs direct scores for mood, choice quality, clarity, originality and aftermath by act, with careful/cynical/reckless persona comparisons. This report is an honest engine-and-art audit, **not** the entire t-044 closeout.
2. Act II-V daily motif events have diverse opening fiction but repeated branch structures. They need 104 authored choice-pairs with distinct consequences, rather than statistical restyling.
3. The five secret followers' visual scenes and regular event images need actual renderer completion, image QA, export and manifest wiring. Prompt submission alone cannot fill a player-visible blank.
4. Track player agency through quests and weekly follower availability. The design target is most ordinary quests completable by thoughtful play, with deliberate scarce-resource crises at act endings, rather than an unannounced mathematical impossibility.
5. Recheck the secret follower recruit flow for free bed, late discovery and carried-over saves; target one actual in-game preview after the private art is published to the frontend.

**Current disposition:** keep Conductor t-044 at review until the per-act scored playtest is completed. The completed software and art-queue work is independently mergeable.
