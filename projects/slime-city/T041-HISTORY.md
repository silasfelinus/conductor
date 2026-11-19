# slime-city/t-041 — full note history archive

This file is the archaeology index for slime-city/t-041 ("CLASH 300: individually crafted L1/L2/L3 effects for every existing card"). Its `note:` field in `roadmap.yaml` grew past `check_roadmap_note_size.py`'s 50,000-byte single-note threshold through ordinary recurring-cycle accumulation. The complete verbatim history through the archival point is preserved below; `roadmap.yaml` keeps only a short current-status pointer going forward. Do not restore this text into the live roadmap — read it here when you need to know what a specific past cycle found or did.

Archived under the AGENTS.md archival carve-out (byte-for-byte verified round-trip, pointer left behind, no history lost).

<!-- note:begin t-041 -->
Silas, 2026-11-07 PT: "The ultimate goal will be crafted redesigns of all 300 cards." The authoritative full inventory is projects/slime-city/CARD-REDESIGN-300.md. Each existing catalog identity must have an individually authored journey, not generic L2/L3 stats or duplicated effects. One interesting payoff per card, strategic counterplay, deterministic battle fixture and replay, and CPU reachability audits. Keep all 300 IDs and six distinct crew identities; do not add cards, faction-hate, economy mutations, art or a publication without authorization. Finish original t-037's 70 designs first, then this umbrella governs the remaining 230 redesigns, tracking progress against the full roster.

2026-11-08 PT: Silas reviewed a first data-driven pass (kind_robots branch claude/pensive-albattani-ibljzj, commits b5a4093/5e7659b, never PR'd) and rejected the approach: "doing it programmatically has a big risk of just giving stat boosts to later game cards ... Do some research on good ccg design before moving forward and creating a plan." Also: "We should have fresh art on the evolutions, not just frame effects." Plan with research, design rules (trajectories instead of a universal stat ramp, L2 = new decision, L3 = named transformation with counterplay, faction tool ownership), per-level Flux Kontext art for all 300, and a 10-card Catgirls pilot gate: projects/slime-city/CLASH-EVOLUTION-PLAN.md. Awaiting Silas's answers to the plan's open questions before the pilot starts; the parked branch keeps only its engine hooks for reuse.

Audit checkpoint: kind_robots #4907 has 300 merged custom evolutions. The default CPU sweep only uses fixed 20-card decks, so this session adds 300-card constructed-deck matchup coverage, mirrored seeds, reachability, duplicate-mechanic reporting and deterministic replays on a worker PR. Continue per-card balance and fun QA before accepting the full catalog.

2026-11-08 PT: Audited the merged 300 custom evolution arcs and shipped reproducible 1,230-match constructed Solo/Alliance QA in Kind Robots #4908 (squash f2a7a6e, all eight final-head workflow runs green). Solo first seat 49.6%, Alliance first seat 40%; 279/300 cards used, 160 at L3, 21 never selected, two exact mechanical arc duplicates. Conductor #7176 (squash 2e88f66) updates the 300-row ledger to 70 MERGED and 230 LIVE_QA and records findings in CLASH-EVOLUTION-QA-2026-11-08.md. Remain ready: resolve unplayed cards and duplicate paths, assess CPU evolution valuation, run larger constructed matchups and bespoke 230-card payoff fixtures. Human fun acceptance, art delivery and production deployment not claimed.

Tactical evolution increment in review: CPU now values actual board-relevant staged effects and lasting gear instead of a generic arrival bonus; Bloodfairy Banana Bouncer becomes a swarm encore rather than an Ironjaw boss/heal clone, and Undertow Backwater IOU becomes three-lane stun rather than an Exchange splash clone. Adds focused CPU decision and real battle fixtures plus existing 1,230-match regression. Verify CI and quantitative changes before merge.

2026-11-08 PT: Merged Kind Robots PR #4910 (squash 3e053c17b339704a12083b37c92a4932fd84800f) after all eight final-head checks completed green. Solo CPU now estimates actual L2/L3 board payoffs, lasting gear and card investment while preserving Alliance baseline AI; fixes RNG mutation during random-target evaluation, with a replay/immutability regression. Bloodfairy Banana Bouncer L3 summons a SWARM encore; Undertow Backwater IOU L3 stuns adjacent foes, removing both prior exact mechanical duplicates. Verified 1,080 Solo seeded matches (48.7% first-seat, 9.5 average rounds, 135 exact replays), 150 Alliance matches (40% first-seat), all solo and alliance general acceptance thresholds, and named ability fixtures. Still 25/300 cards never selected in constructed CPU games (previous 21), 144 reached L3 (previous 160); keep task ready for creative individual payoff QA, CPU utility/card-reach improvement, deeper deckbuilding matchups and pending art curation. No deployment or human fun acceptance claimed.

2026-11-08 PT evolution art redo. Silas: "Flux dev is a slow generator, and we're getting a lot of the same looking images three times over. We shouldn't use it for the main gen, but we also need a much larger and fun escalation between evolution 1 and evolution 3." The Kontext dev evolution ledgers are superseded by nine Krea 2 ledgers (projects/slime-city/art/EVOLUTIONS-*-KREA.yaml, 481 stages, one render each, auto_submit) on the escalation ladder in CLASH-EVOLUTION-PLAN.md section 4. Silas's standing direction, also in section 4: "these gens evolutions are supposed to look bigger and more impressive. They might tell a story." The hero grows in the frame at every step, and one L1 story thread pays off at L3. With Silas's OK, 700 PENDING Kontext jobs were cancelled in the Kind Robots queue (reversible via re-enqueue); 88 had already rendered and 4 were running. Mechanics scope of t-041 is unchanged; return READY.

2026-11-08 PT: Constructed Clash Alliance adversarial suite in kind_robots worker/slime-city-t-041-alliance-qa-20261108-x7q4. Tests all 30 ordered faction pairings across nine legal 30-card strategies with matched-seat seed swaps, separate same-deck general-power swaps, L2/L3 use and full 300-card legal deck coverage. Source PR and CI validation pending; t-041 remains a partial QA umbrella with human fun acceptance outstanding.

PARTIAL MERGED 2026-11-08 PT: Kind Robots #4913 merged to main as a72a25c374c568ef49405de44f80c0d8e4b66b86 after all eight final-head workflows completed green (four contract shards, TypeScript, formatting, layout, architecture, schema, facet and container build). 1,140 real-CPU constructed ALLIANCE matches across all 30 ordered general/ally pairs, nine legal 30-card deck strategies, both-seat matched seeds and 60 general-swap controls; 54 full deterministic replays. All 300 cards appear in simulated legal decks, 285 were played, 104 reached L3, 15 never played. First seat 51.4% across all games (includes unpaired general-swap controls), 6.2% draws overall. Important design risk: specials-only decks hit 24 rounds in every one of 120 matches, drawing 59.2%, despite being intentionally legal with no creature minimum. No rule change or deck restriction made. Next work: targeted payoff/counterplay fixtures for the 15 unplayed cards, improve L3 availability in 30-card Alliance without generic stat inflation, analyze specials-only nonterminating offense without restoring the rejected creature minimum, and report controlled general-power deltas separately. Human fun approval, art and production deployment remain unverified. Keep t-041 READY for continued QA.

Thundersaur-inspired targeted evolution increment: existing Ironjaw Dreadnought keeps its L2 hit-driven hull growth; L3 trades four starting life for an arrival avalanche and permanent attack/life growth for each complete round survived. Added real round-end engine, level contrast, counterplay and immutability regression tests. No new card IDs, deck restrictions, art publishing or economy changes. Gameplay test checks required before merge.

Reconciled stale review after Kind Robots #4916 merged at 2026-11-09T07:24:55Z and branch was removed. User explicitly authorizes redesigning the existing 300 cards and introducing new gameplay abilities. Reopen t-041 for a focused, tested rules increment, preserving the 300 card IDs and separate art/release gates.

Scoped three new CLASH effect families onto existing card IDs: deterministic cross-card L1-L3 promotions from hand/deck; at most one conditional zero-slot play per turn with UI eligibility; and a wounded-heavy-only execute capped at four remaining HP. Added focused rules and CPU valuation regression fixtures. Review source PR and latest-head CI before merging; all 300 IDs remain intact, artwork, economy and public release untouched. Full catalog fun QA and larger Alliance matchup sweeps still remain.

Kind Robots PR #4920 merged squash 3597e0c0d344e8c6a8de9b0e65c6280ddc98e456 after all six latest-head check workflows completed successfully (TypeScript, changed-file Prettier, schema parity, architecture, layout, all four contract shards). Existing cards gained three novel CLASH mechanic families: deterministic cross-card promotion (Undertow Backwater IOU), one conditional no-slot play per turn (Bloodfairy Feedback Burst), and conditional execution of wounded non-token heavy foes (Undertow Wiretap Order). Floating hand eligibility and earned-FREE chip reflect runtime cost; source contracts, immutable replay and anti-loop/anti-invalid-target tests added. 300 card identities unchanged. Adversarial CPU suite confirms 1080 Solo games and 1140 Alliance games; 25 Solo unused, 8 Alliance unused, and weak L3 reach remain quality gaps; please continue t-041 with targeted decision-quality, choice agency, and individual authored arc improvements. No art jobs, economy, deployment or human fun acceptance claimed.

Design contract review: codify Silas's latest useful-but-fragile L1 principle as default for all 300 card arcs; one core verb, immediate L1 value, answerable investment, named concrete faction combo, synergistic L2, meaningful distinct L3 and per-format reachability/CPU/counterplay fixtures. Clarify fragility need not mean low health: a durable Tim-like defender can have a fragile plan. New PLAYABLE-EVOLUTION-CONTRACT.md plus references from evolution plan and 300-card QA ledger; master Kind Robots roadmap issue #4535 updated. No engine, economy, card ownership or publication change.

PARTIAL MERGED 2026-11-09 PT: Conductor PR #7187 squash 7e114699314255a345fae38d7ea8c82e9d6be79f. Useful-but-fragile three-stage card interaction rubric now lives in PLAYABLE-EVOLUTION-CONTRACT.md and is linked from CLASH-EVOLUTION-PLAN.md, CARD-REDESIGN-300.md and Kind Robots master issue #4535. L1 performs a useful action even if the opponent answers the setup; an early sturdy defender can still have a fragile investment plan. L2 grows one recognizable job through concrete synergy, L3 compounds into a named counterable payoff. All eight Conductor Worker PR CI jobs, security audit and latest handoff check passed. t-041 remains READY for actual per-card redesign, matchups, CPU and Solo/Alliance reachability fixtures, evolution art and human fun acceptance. No combat engine, card IDs, account economy, generated art or deployed game changed.

First playable evolution pilot in Kind Robots review. Generalized the evolution interpreter to support optional authored useful Level 1 actions and accurate card rules. Union Bridgebearer produces an immediately useful fragile worker at Level 1, then a protected worker plus aura, then a pacifist two-worker assembly line. Ironjaw Scrapyard Dreadnought shields adjacent workforce from L1, compounds protection at L2, and becomes a growing, counterable Thunderhead at L3. The previously underplayed Bloodfairy Encore or Die is one-slot in CLASH only, progresses from single-target LEECH to adjacent allies to a true full-choir revive or riskier VOLATILE fork. Dedicated fixtures test early counterplay, actual cards, CPU choices, legal 20/30 decks, deterministic Solo/Alliance replay; full CI and merged PR required. No inventory, account, database, art, publishing or other mode rules changed.

PARTIAL MERGED 2026-11-09 PT: Kind Robots #4925 squash-merged at 19add28 after eight latest-head CI workflows succeeded. Level-one authored-stage interpreter and Bridgebearer, Dreadnought, Encore journeys survived reconciliation with 20-card Clash and new faction work. Return task to ready: three pilots are not acceptance of all 300; continue hand-authored quality, constructed CPU reachability, and evolution art QA. No deployment/public release claimed.

Focused mercenary L3 engine regression in kind_robots worker branch: Flashmob Diversion and Living Scaffold summon distinct fragile attackers versus non-attacking defensive wings; full allied board denies flashmob. PR and CI follow; t-041 remains a broader 300-card QA umbrella.

2026-11-13 PT intent audit (INTENT-AUDIT-2026-11-13.md): status was review for ~36h with
no open PR in kind_robots or conductor and remaining scope listed above; returned to
ready so pickers can take the next slice. No work discarded.

In review: deterministic replayable fighter tap actions, chosen attack tradeoff, Catgirls pilot and one starter for each of the other five factions; Solo and PvP controls, reward transcripts and regression tests. CI verification pending.

2026-11-13 PT: merged kind_robots PR #5139 as squash 898c0c8 after six completed successful workflows on head 08e499b. Adds chosen tap activations with strike cost, PvP validation, CPU evaluation, six-crew pilot and replay tests. Partial 300-card umbrella; return ready for full-roster individual ability and constructed matchup audit.

Reviewing full 300-card CLASH editorial audit: standalone L1/L2/L3 and 22 alternate evolution texts; targeted bespoke copy rewrites, generator grammar, PvP chooser and exact rendered-copy CI ledger. More mechanical and QA work remains.

2026-11-14 PT: Full 300-card editorial audit merged as kind_robots PR #5153 (squash 69513002df80d77a827b34ab240707dbd834f8d7), after all 11 latest-head checks passed, including TypeScript, formatting and 4 contract shards. Audited 922 card faces (300 x 3 plus 22 L3 A/B branches), rewrote 52 bespoke card evolution descriptions, fixed card-face grammar, A/B previews in Solo/PvP/Collection, and added permanent source/length/independence contract plus docs/slime-city-card-copy-audit-2026-11-14.md. Remaining t-041 scope: individual gameplay payoffs, counterplay, CPU reachability, constructed balance QA, pending art and human fun acceptance.

Added 300-card structural evolution-signature diagnostic on worker branch ac6eac9; PR and CI pending. This is one bounded increment of the larger 300-card editorial task, not completion.

2026-11-14 PT: Opened kind_robots PR #5181 (head ac6eac9) with a runnable audit of all 300 card evolution signatures and duplicates. CI not yet reported; PR remains unmerged. This bounded diagnostic does not finish the full 300-card redesign; next worker should review CI and audit output before changing individual cards.

First Catgirls rewrite committed as kind_robots 1f519b2: Clone Salvage L2 now builds a conditional echo; Emergency Molt L2 heals after hits; Spare Lives L2/L3 introduces tap triage and adjacent rescue. This is an initial implementation slice, NOT the full 900-stage editorial completion.

First two full-faction manually authored editorial implementations are in Kind Robots: Catgirls PR #5182 (40 cards/120 stage roles, direct mechanics, stage copy, deterministic fixtures) and stacked Bloodfairies PR #5186 (40 cards/120 stage roles, 30 authored L1 descriptions, 30 legacy stage rewrites, 13 modified evolution arcs, targeted combat fixtures). Both PRs are open, undergoing CI; #5186 is temporarily based on #5182. Do not close t-041: 220 cards/660 stage roles still need the same manual pass, plus full seeded playtest/replay acceptance. After both PRs merge, release t-041 to ready for the next faction rather than leaving a stale claim.

Partial work delivered, not complete: Catgirls implementation PR #5182 covers a manual 40-card/120-stage review and live combat fixes, and Bloodfairies stacked PR #5186 covers the next 40-card/120-stage pass. Both have source changes, card-by-card editorial ledgers, and targeted tests. CI is not yet green; #5186 must be retargeted to main after #5182 merges, checked at its final SHA, and merged only on completed green checks. Remaining scope: 220 cards and 660 stages across Ironjaw, Riot, Undertow, Exchange, Mercenaries, plus independent balance and seeded-replay QA. This release clears the current worker claim; next worker must first triage these two PRs, avoid editing their files concurrently, then claim t-041 before working a new non-overlapping faction. Never label the 900-stage task done on the basis of these first two passes.

Rescued Catgirls and Bloodfairies 40-card editorial passes from diverged kind_robots#5182 into a fresh main-based branch (nine Slime City files only), preserving 13 unrelated main commits. Shortened generated trap card-face copy after Contract shard 1 found overlong Banana Bouncer L2. CI on rescue PR pending; broader 300-card editorial program remains open.

PARTIAL MERGED PT 2026-11-14: kind_robots#5188 (fc4e78df) restores 40 Catgirls and 40 Bloodfairies individually reviewed evolutions and deterministic battle fixtures from stale #5182, plus card-face copy fixes, Calico rules wording, Glasswalker/Tiger counterplay balance, and exact-count 12-point parity assertion. All six CI workflows completed green at head 733d78b; 40-seed seeded match sweep: Catgirls 56%, Bloodfairies 44%, 12-point crew spread. #5182 closed as superseded. Remaining 220 cards, 660 stage roles, constructed matchups, balance and playtest QA stay ready.

Ironjaw continuity fix opened in kind_robots PR #5203, head 80578d8. Three L3 abilities now preserve their L2 utility. Await complete CI and battle fixtures; 300-card umbrella remains unfinished.

Partial Ironjaw forty-card review submitted as kind_robots PR #5204; thirty authored L1 roles, nine L3 continuity improvements, six actual-engine fixtures, and a forty-row counterplay ledger. Latest head dbf4a77 has five of six workflows completed green; Contract Tests still running at last check following correction of illegal enemy faction in two trap fixtures. Do not mark all three hundred finished or merge before CI green. PR #5203 is an overlapping green subset and must be reconciled rather than duplicated.

MERGED partial Ironjaw editorial increment: kind_robots PR #5204, main squash 4267deef61404f900f6d698b7fc91b6efac0847c, final head dbf4a77. Verified all six latest-head GitHub workflows completed success, including four Contract Test shards, TypeScript, formatting, layout, architecture and schema. 40 Ironjaw cards reviewed, thirty authored L1 role texts, nine targeted L3 continuity improvements, six battle-state fixtures, forty-row counterplay ledger. Overlapping PR #5203 closed as superseded after validating its three changes on main. Task remains INCOMPLETE: 180 cards in Riot, Undertow, Exchange and shared Mercenaries still need independent editorial and gameplay audit, plus constructed match balance, seeded replays, art and human fun acceptance. Release for next pass.

2026-11-15 PT: Scoped three Mercenary L3 continuities: Traffic Witch retains L2 Green Wave on hit alongside one-shot Gridlock, Crowd-Sourced Lightning retains L2 crowded target zap alongside boss pressure, and Streetlight Confession retains L2 adjacent fighter power alongside its piercing hit across. Added real Clash board fixtures and deterministic repeatability coverage. Implementation commit ab398069 on worker/slime-city-t-041-mercenary-payoff-20261115T1337Z-c8a4; PR and CI pending. Task remains partial: 300-card editorial, low-selection QA, art and constructed balance still open.

2026-11-15 PT: Merged kind_robots PR #5221, squash 77fee2a7cf88e65390e10e330a3eabe1828a8d9f. Three shared Mercenary Level 3 evolutions retain their prior strategic Level 2 utility: Traffic Witch keeps a neighboring-fighter rally with its once-per-hit gridlock, Crowd-Sourced Lightning keeps crowd-powered target zap alongside boss pressure, and Streetlight Confession keeps neighbor attack surge alongside a piercing hit. Battle-state and deterministic regression fixtures pass. Current head 3cfa0ce3 had six completed successful workflows including all four Contract Test shards and verifier. This closes one independent increment only. Return t-041 to ready for remaining 300-card curation, underselected cards, constructed balance and art QA; no production deploy or subjective acceptance claimed.

2026-11-15 PT: kind_robots PR #5226 (head 2fca9fd): three L3 evolutions keep the L2 job
their design notes promise -- Midnight Janitor keeps Mops Up heal before Closing Time
duel, Secondhand Halo keeps Still Warm mend (no weaker L3 without a fallen ally), Long
Drain Sting keeps Long Reach weakest-foe sting alongside the strongest-foe stun. Real-
board fixtures fail on old defs; 11 related Slime City suites pass locally. Audit
method: compared L2 vs L3 action shapes across riot/undertow/exchange/mercA/mercB and
flagged only cards whose own arc comment contradicts the code; most remaining drops are
documented ROLE SHIFTs. Partial increment; umbrella stays open.

2026-11-15 PT: MERGED kind_robots #5226, squash 257dcbb4, head 2fca9fd; all 11 check
runs green (4 contract shards, verifiers, TypeScript, Prettier, layout, verify x2). One
increment only; return to ready for remaining 300-card curation, constructed balance and
art QA.
<!-- note:end t-041 -->

## Round 2 (archived 2026-11-19)

<!-- note:begin t-041 round 2 -->
Silas, 2026-11-07 PT: "The ultimate goal will be crafted redesigns of all 300 cards." The authoritative full inventory is projects/slime-city/CARD-REDESIGN-300.md. Each existing catalog identity must have an individually authored journey, not generic L2/L3 stats or duplicated effects. One interesting payoff per card, strategic counterplay, deterministic battle fixture and replay, and CPU reachability audits. Keep all 300 IDs and six distinct crew identities; do not add cards, faction-hate, economy mutations, art or a publication without authorization. Finish original t-037's 70 designs first, then this umbrella governs the remaining 230 redesigns, tracking progress against the full roster.
2026-11-08 PT: Silas reviewed a first data-driven pass (kind_robots branch claude/pensive-albattani-ibljzj, commits b5a4093/5e7659b, never PR'd) and rejected the approach: "doing it programmatically has a big risk of just giving stat boosts to later game cards ... Do some research on good ccg design before moving forward and creating a plan." Also: "We should have fresh art on the evolutions, not just frame effects." Plan with research, design rules (trajectories instead of a universal stat ramp, L2 = new decision, L3 = named transformation with counterplay, faction tool ownership), per-level Flux Kontext art for all 300, and a 10-card Catgirls pilot gate: projects/slime-city/CLASH-EVOLUTION-PLAN.md. Awaiting Silas's answers to the plan's open questions before the pilot starts; the parked branch keeps only its engine hooks for reuse.
Audit checkpoint: kind_robots #4907 has 300 merged custom evolutions. The default CPU sweep only uses fixed 20-card decks, so this session adds 300-card constructed-deck matchup coverage, mirrored seeds, reachability, duplicate-mechanic reporting and deterministic replays on a worker PR. Continue per-card balance and fun QA before accepting the full catalog.
2026-11-08 PT: Audited the merged 300 custom evolution arcs and shipped reproducible 1,230-match constructed Solo/Alliance QA in Kind Robots #4908 (squash f2a7a6e, all eight final-head workflow runs green). Solo first seat 49.6%, Alliance first seat 40%; 279/300 cards used, 160 at L3, 21 never selected, two exact mechanical arc duplicates. Conductor #7176 (squash 2e88f66) updates the 300-row ledger to 70 MERGED and 230 LIVE_QA and records findings in CLASH-EVOLUTION-QA-2026-11-08.md. Remain ready: resolve unplayed cards and duplicate paths, assess CPU evolution valuation, run larger constructed matchups and bespoke 230-card payoff fixtures. Human fun acceptance, art delivery and production deployment not claimed.
Tactical evolution increment in review: CPU now values actual board-relevant staged effects and lasting gear instead of a generic arrival bonus; Bloodfairy Banana Bouncer becomes a swarm encore rather than an Ironjaw boss/heal clone, and Undertow Backwater IOU becomes three-lane stun rather than an Exchange splash clone. [...]
[Earlier history (15,073 chars) archived verbatim to projects/slime-city/T041-HISTORY.md -- read it there only when you need a specific past cycle. Append new cycles below, one short paragraph each.]
MERGED partial Ironjaw editorial increment: kind_robots PR #5204, main squash 4267deef61404f900f6d698b7fc91b6efac0847c, final head dbf4a77. Verified all six latest-head GitHub workflows completed success, including four Contract Test shards, TypeScript, formatting, layout, architecture and schema. 40 Ironjaw cards reviewed, thirty authored L1 role texts, nine targeted L3 continuity improvements, six battle-state fixtures, forty-row counterplay ledger. Overlapping PR #5203 closed as superseded after validating its three changes on main. Task remains INCOMPLETE: 180 cards in Riot, Undertow, Exchange and shared Mercenaries still need independent editorial and gameplay audit, plus constructed match balance, seeded replays, art and human fun acceptance. Release for next pass.
2026-11-15 PT: Scoped three Mercenary L3 continuities: Traffic Witch retains L2 Green Wave on hit alongside one-shot Gridlock, Crowd-Sourced Lightning retains L2 crowded target zap alongside boss pressure, and Streetlight Confession retains L2 adjacent fighter power alongside its piercing hit across. Added real Clash board fixtures and deterministic repeatability coverage. Implementation commit ab398069 on worker/slime-city-t-041-mercenary-payoff-20261115T1337Z-c8a4; PR and CI pending. Task remains partial: 300-card editorial, low-selection QA, art and constructed balance still open.
2026-11-15 PT: Merged kind_robots PR #5221, squash 77fee2a7cf88e65390e10e330a3eabe1828a8d9f. Three shared Mercenary Level 3 evolutions retain their prior strategic Level 2 utility: Traffic Witch keeps a neighboring-fighter rally with its once-per-hit gridlock, Crowd-Sourced Lightning keeps crowd-powered target zap alongside boss pressure, and Streetlight Confession keeps neighbor attack surge alongside a piercing hit. Battle-state and deterministic regression fixtures pass. Current head 3cfa0ce3 had six completed successful workflows including all four Contract Test shards and verifier. This closes one independent increment only. Return t-041 to ready for remaining 300-card curation, underselected cards, constructed balance and art QA; no production deploy or subjective acceptance claimed.
2026-11-15 PT: kind_robots PR #5226 (head 2fca9fd): three L3 evolutions keep the L2 job their design notes promise -- Midnight Janitor keeps Mops Up heal before Closing Time duel, Secondhand Halo keeps Still Warm mend (no weaker L3 without a fallen ally), Long Drain Sting keeps Long Reach weakest-foe sting alongside the strongest-foe stun. Real- board fixtures fail on old defs; 11 related Slime City suites pass locally. Audit method: compared L2 vs L3 action shapes across riot/undertow/exchange/mercA/mercB and flagged only cards whose own arc comment contradicts the code; most remaining drops are documented ROLE SHIFTs. Partial increment; umbrella stays open.
2026-11-15 PT: MERGED kind_robots #5226, squash 257dcbb4, head 2fca9fd; all 11 check runs green (4 contract shards, verifiers, TypeScript, Prettier, layout, verify x2). One increment only; return to ready for remaining 300-card curation, constructed balance and art QA.

2026-11-15 PT: kind_robots #5228 merged as 306915b4e185989d6afb3f57236aea7d11d595c4. Final head ed6348e: six PR checks (Contract Tests, TypeScript, formatting, layout, architecture, schema parity) completed successfully; branch janitor also succeeded. Added 25 lowest-selection cards, L2/L3 reachability, and exact replay coverage of 30 archetypes. No combat or card balance changed. Partial QA increment only; return t-041 to ready for remaining 300-card editorial and balance work.

Constructed QA selection rates previously used total play commands divided by card deck appearances; repeated plays inflated the ranking. New scoped Kind Robots branch counts distinct card-selected bouts by side and denominator, preserving raw play counts and adding bounded-rate assertions. Implementation PR and CI follow; umbrella remains partial.

2026-11-15 PT: kind_robots PR #5230 merged as dba90f251b8e15cd0e7fa450899a0982076fa246 from head 73b84ea80d667ddf2947cf867642d166fa6ad96e. Six final-head GitHub workflows completed successfully (Contract Tests with four shards, TypeScript, formatting, layout, architecture, schema). Corrected constructed low-selection report to count distinct player bouts per card, rather than repeat play commands, retaining raw plays and evolution reachability. Bounded selection assertions added. This is partial QA only; t-041 remains open for targeted underselected-card and evolution design work.

2026-11-15 PT: Scoped L3 open-lane payoff repair on branch worker/slime-city-t-041-l3-openlane-20261116T0245-f6b83c, commit 53e1d2f. Catgirls Roof Phantom retains its L2 open-lane boss shot when the L3 tap moves it to safety; Anarkiss Wall-of-Death Rider retains its open-lane ambush surge alongside its L3 retreat. Real-board fixtures cover enemy blocking, denied escape, and deterministic pure-command replay. Full seeded constructed matchup and CI results pending.

2026-11-16 PT: MERGED kind_robots #5232, squash 0f35a194, head 2b76f0d. Rooftop Phantom
L3 keeps its L2 open-lane 2-point boss chip before the safe sidestep; Riot Bike
Messenger L3 keeps the open-lane +2 ambush surge before retreating. Reviewer fix: CI
shard 1 failed the 160-char face contract (Skyline Specter rendered 165), so the shared
shift phrase now reads 'a free adjacent alley' (160). All 12 check runs green. One
increment only; return to ready for remaining 300-card curation, constructed balance and
art QA.

2026-11-16 PT: released claim 2026-11-16T0730Z-t041-pd5v7b without changes. The constructed report (3120 bouts) still shows 14 dead two-slot cards, e.g. s3-catgirls-stolen-saw and s3-catgirls-spare-lives. Cause: chooseClashCpu divides every score by b.plays, and a cost-4 grant spell scores roughly half a fighter. Fixing it means changing cards or the CPU comparator, which the test output attributes to t-051 (candidate list goes to Silas first), so this session switched to interface-vision/t-154. No work discarded.

2026-11-16 PT: MERGED kind_robots #5258, squash 1046f3cf, head 98adde1; all 12 check
runs green. Undertow editorial pass: 30 authored L1 roles (distinct even where four
disarm spells share native text) and four L3 continuity repairs whose arc comment still
named the dropped L2 job: Needle Rain Agent keeps its arrival chip, Basement Watchdog
its dying bark, Periscope Lens its spotter aura, Tunnel Harpoon its barbs. Real-board
fixtures fail on the old definitions. Quiet Room Listener's shield retention was backed
out after CI shard 1 failed the 12-point CLASH crew spread (main already sits at exactly
12.0: Catgirls 44.8%, Ironjaw 56.8%); its comment now documents the trade. Review doc:
docs/agents/slime-city-undertow-evolution-review.md. One increment only; Riot, Exchange
and Mercenary editorial passes, constructed balance, art and fun acceptance remain open.
Return to ready.

2026-11-16 PT: MERGED kind_robots #5259, squash f4faf3d, head e3bf700; all 12 check runs
green. Riot editorial pass: 30 authored L1 roles, distinct where eleven cards share the
bare VOLATILE line and five spells share the deal-plus-neighbors template. A test
asserts rendering, distinctness and the 160-char face at L1-L3. The arc comments already
matched the L3 code, so there are no rule changes and CLASH balance is untouched. Review
doc: docs/agents/slime-city-riot-evolution-review.md. One increment only; Exchange and
Mercenary editorial passes, constructed balance, art and fun acceptance remain. Return
to ready.

2026-11-16 PT: MERGED kind_robots #5260, squash b34930b, head 4984554; all 12 check runs
green. Exchange editorial pass: 30 authored L1 roles, distinct where seven cards share
the bare COLLECT line, five spells 'Deal N and stun' and five traps the next-foe
template. A test asserts rendering, distinctness and the 160-char face at L1-L3
(longest: golden-bailiff 154). No rule changes; CLASH balance untouched. Review doc:
docs/agents/slime-city-exchange-evolution-review.md. One increment only; Mercenary
editorial passes, constructed balance, art and fun acceptance remain. Return to ready.

2026-11-16 PT: MERGED kind_robots #5261, squash 210e884, head 60d1c81. All check runs
green (11 passed, 1 skipped). This is the Mercenary editorial pass: 50 authored L1 roles
across mercenaryA/B. Each role is distinct where 15 traps share the Next-foe template
and fighters, spells and gear repeat keyword lines. A test asserts each role renders, is
distinct and fits the 160-char face at L1-L3 (longest: market-tripwire 126). No rule
changes, so CLASH balance is untouched. Review doc: docs/agents/slime-city-mercenary-
evolution-review.md. All six crews plus Mercenaries now have their editorial pass.
Remaining: constructed balance (the dead two-slot cards are tracked in t-051), art and
fun acceptance. Back to ready.

2026-11-16 PT: Constructed checkpoint on kind_robots main c843ad9: 3,120 bouts, PASS.
Crews 44.3-55.7%, first seat 51%. Every never-played or low-selection card costs two
slots, which is t-051's redesign scope. Ironjaw/fighters is the top deck at 82.7% from
extra one-slot fighters, consistent with fighters-first; no nerf. See projects/slime-
city/CLASH-CONSTRUCTED-CHECKPOINT-2026-11-16.md. Now waits on t-051. Art is tracked in
t-044, t-052, t-053 and t-054; the fun verdict is outside the roadmap. After t-051
merges, rerun test:slime-city-clash-constructed.

2026-11-18 PT: Reconciled. All six faction editorial passes are already merged (Exchange
and Mercenary #5261 included; 30 levelOneText per crew file and 25+25 Mercenary). On
main, constructed QA reads 3120 bouts, crews 42.4-55.6%, and 13 dead two-slot cards,
every one a 2-slot spell or gear (blast, debt, root, grant, boost). Experiment, not
shipped: chooseClashCpu's generic damage-spell score ignores blast neighbor splash and
debt/root stun, so I added a read-only rider valuation. Dead stayed at 13 (two revived,
two new: posthumous-saint, collection-badge) and Riot fell to 42.0%, under the 42% band,
so I reverted it. The binding cause is score /= b.plays: a two-slot spell must beat the
best one-slot fighter at half value. Next step: replace the per-slot halving with a
comparison against the best pair of one-slot plays, scored on full matchups. Then re-
tune the crew bands, since Riot already sits at the lower edge. Remaining after that:
art and human fun acceptance. Released for the next pass.

2026-11-18 PT: MERGED kind_robots #5310, squash 9223dbf, head b15e793; all 12 check runs
green. CPU two-slot valuation: chooseClashCpuPlay judges a two-slot spell/gear against
the best pair of one-slot plays (distinct card and alley) plus
CLASH_CPU_TWO_SLOT_MARGIN=2 instead of halving it. Two-slot fighters keep the per-slot
rule (full-value pairing dropped the Catgirls starter to 35.8%). Constructed QA, 3,120
bouts: dead two-slot cards 13 -> 6, crews 42.6-55.7%. Starter guard unchanged; the suite
now fails above 6 dead. Margins 0/1/3 read 3/5/10 dead, and margin 0 put Riot at 41.6%,
under the band. The six still dead (ironjaw reallocation/furnace-overdrive, riot wrong-
side-of-blast, exchange compound-interest-notice/acquisition-clause, catgirls stolen-
saw) lose when played, so they need card buffs, not CPU work. That is the next step.
Kaizen: in CLASH, a splash:'all' blast only hits enemy neighbors, which contradicts its
card text. Back to ready.

2026-11-18 PT: MERGED kind_robots #5311, squash 3e5fd8a, head 3c934dd; all 12 check runs
green. The last six dead two-slot specials each got an authored level-one stage, carried
into L2/L3 so a level-up never loses it. Union Reallocation: all allies +1 lasting
power. Furnace Overdrive: +2 lasting power and +3 life. Wrong Side of the Curtain: 2
damage to the rival boss. Breeding Hunger: draw 1. Mark of the Procession: +2 lasting
power and boss +2. Stolen Bone Saw: 1 damage across and +1 lasting power. Constructed
QA, 3,120 bouts: dead two-slot cards 6 -> 0. Crews 42.7-55.6% (unchanged), first seat
51.7%. Suite ceiling is now 0. Real-board L1 fixtures are in verifySlimeCityEvolutions.
Remaining: the splash:'all' blast hits only enemy neighbors, contradicting its card text
(kaizen). Also open: Riot sits at the 42% band edge, plus art and human fun acceptance.
Back to ready.

2026-11-18 PT: MERGED kind_robots #5312, squash d738209, head 5e77379; all 12 check runs
green. Kaizen fixed: in CLASH, splash:'all' blasts (nine cards whose text says
'including your own') now also deal 1 to the caster's fighters in adjacent alleys;
Confetti keeps its authored pattern. Regression fixture covers three splash:'all' cards
plus an enemies-only control. Constructed QA, 3,120 bouts: dead two-slot cards 0, crews
42.4-55.6%, first seat 51.7%. Open: Riot near the 42% band edge, CPU blast valuation
ignores friendly splash, art and human fun acceptance. Back to ready.

2026-11-18 PT: MERGED kind_robots #5313, squash 5501d59, head 17132dc; all 12 check runs
green. CLASH CPU now scores blast splash (cpuBlastSplashValue mirrors the resolver:
rival neighbors, splash:'all' friendly fire, Confetti/Mosh patterns, armor/guard soak),
so it no longer blasts its own wounded fighters. Regression fixture in
verifySlimeCityClashCpuEvolutions. Constructed QA, 3,120 bouts: dead two-slot cards 0,
crews 42.4-55.8%, first seat 51.9%. Open: Riot at the 42% band edge, art and human fun
acceptance. Back to ready.

2026-11-18 PT: MERGED kind_robots #5314, squash 2721828, head 8ef7ae3; all checks green.
Riot moved off the 42% constructed band edge. Fireworks Strongman (s3-riot-firework-
bishop), Riot's only off-starter two-slot fighter, gets +1 strike at L1 and L3 (L3 keeps
the 1.6x ramp). Decks with him unplayed won 39.6% of bouts; decks that played him won
51.2%. Constructed QA, 3,120 bouts: Riot 42.4 -> 44.6%, crew spread 13.4 -> 10.7 points,
dead two-slot cards 0, first seat 51.9%. Two held-out seed families: Riot +2.9 and +1.5
points. Starter sweep unchanged (Riot 49.8%). Levers tried and dropped: FUSE BOX 3/5
gave +1 point; FUSE BOX 4/5 stranded a dead card; a CPU trap penalty gave +0.9 and cost
Undertow; CLASH_CREW_BUDGET riot is all-or-nothing (0.5 put Riot at 67.5% in the starter
sweep). Open: Undertow, now the lowest constructed crew at 44.9%; art; human fun
acceptance. Back to ready.

2026-11-18 PT: MERGED kind_robots #5315, squash b4ccfa9, head 85f8da0; all 12 check runs
green. Undertow lifted off the bottom of constructed CLASH. Rubber Drysuit (played in
598 of 600 non-starter Undertow bouts, 33% win) now adds +2 armor in CLASH (+3 at L3)
via a shared clashArmorGain helper that also drives the badge and rules text; catalog
text is untouched because other modes keep +1. Long Drain Sting (L1 Drain Line: boss 2)
and Backwater IOU (L1 Fine Print: draw 1) get authored L1 stages carried into L2/L3;
both went dead without them. Constructed QA, 3,120 bouts: Undertow 44.9 -> 49.6%,
undertow/fighters 45.2 -> 57.0%, crews 43.6-54.4%, first seat 52.4%, 0 dead two-slot
cards. Held-out families +5000/+9000: Undertow +5.6/+4.2, Riot -1.5/-0.8. Dropped
levers: global CPU armor valuation x1 (Riot 41.5%, under the band); +1 attack on
Interrogation Eel (stranded Long Drain Sting). Open: Riot is again the lowest crew at
43.6%; art and human fun acceptance. Back to ready.

2026-11-18 PT: kind_robots #5316 adds a near-dead ratchet to constructed CLASH QA. The
dead-card ceiling of 0 only means played once: on suite seeds 18 two-slot cards are
chosen in under 3% of their bouts (Dress Rehearsal Pyro, Breeding Hunger, Glitterglass
Flood, Twin Omens, Mark of the Procession, Bone Tithe Sigil, Juggernaut, Chimera,
others; many 1-3 of 208-416). Held-out families +5000/+9000 read 17/19, and Twin Omens
and Spare Nine Lives drop to zero plays there. Suite now fails on any one-slot card
under 3% (lowest: Floodlight Leak, 3.4-4.3%) and caps near-dead two-slot cards at 18.
Tried and dropped: Dress Rehearsal Pyro L1 stages (Riot +/-0.3 pts); Twin Omens L1
second omen (2 to weakest foe) revives it off-suite but strands Breeding Hunger on suite
seeds. The Exchange two-slot spells crowd each other out, so they need a design pass,
not per-card nudges. Riot is 43.6% (45.8/44.9 held-out), inside the band. Next: a two-
slot special redesign to push the 18 down. Back to ready.

2026-11-19 PT: MERGED kind_robots#5347 (squash e894b7e, head aa521ae; all 12 checks
green). CLASH_CPU_TWO_SLOT_MARGIN 2 -> 0: the margin, not the cards, was starving most
two-slot specials once #5315 lifted Riot. Constructed QA 3,120 bouts: near-dead two-slot
18 -> 8; held-out +5000 dead 2 -> 0, near-dead 16 -> 7; +9000 dead 2 -> 0, near-dead 17
-> 6. Crews 43.3-55.0% (Riot 43.3%), first seat 52.3%; riot/heavy 32.2 -> 27.9% is the
deck to watch; 4,500-game starter balance report unchanged; ceilings ratcheted (18->8,
held-out 2->0, 16->7). Still near-dead: Juggernaut, Chimera, Grease Oracle, Spare Nine
Lives, Glitterglass Flood, Breeding Hunger, Compound Notice, Acquisition Clause. Next:
CLASH-only L1 stage sparing the caster's adjacent fighters for the self-splash blasts
(Glitterglass Flood, Dress Rehearsal Pyro), then per-card passes on the rest. Back to
ready.

2026-11-19 PT: kind_robots#5349 (head e4a813ab) adds CLASH_L1_CLEAN_SPLASH: level-one
Glitterglass Flood and Dress Rehearsal Pyro spare the caster's adjacent fighters;
friendly splash returns at L2/L3 where crafted stages already cut allies. Resolver and
CPU splash valuation share clashSplashHitsAllies. Constructed QA: suite near-dead two-
slot 8 -> 7; held-out +5000 7 -> 5, +9000 6 -> 5; 0 dead; crews/first seat unchanged;
ceilings ratcheted. Still near-dead: Juggernaut, Chimera, Grease Oracle, Spare Nine
Lives, Acquisition Clause, both Compound Notices (next: the Exchange notice cluster).
Awaiting exact-head CI.

MERGED kind_robots#5349 (squash 004e373, head e4a813a; all 12 checks green). Back to
ready for the remaining near-dead cards.
<!-- note:end t-041 round 2 -->
