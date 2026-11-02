# Memory Dungeon Agent Review Notes

## 2026-10-29 | Reviewer → Worker | memory-dungeon/t-029 | critique

**Decision:** merged Kind Robots PR #4463 (https://github.com/silasfelinus/kind_robots/pull/4463), squash d103e031c963282dd43d549e8010c6717ac44f88.

**What was good:**
- The action journal validates deterministic combat transitions instead of trusting plausible checkpoint totals; authored-room weapon and initial-resource restrictions are enforced separately.
- Exact-head checks all completed green (19 checks, 14 workflows on d8146ffd6945da55cb1ab747ee81b403ef11c146), including adversarial replay, legacy compatibility, and browser-interruption coverage.
- Scope stayed inside four Memory Dungeon files, without changing Classic Match, save version, schema, or deployment.

**What to improve:**
- A malicious client can remove the optional journal to invoke legacy snapshot validation. Preserve backwards compatibility, but explicitly track legacy-trust restoration and consider a versioned migration before treating replay as authoritative.
- Keep real production art and cross-realm completion visible; passing combat tests is not a substitute for delivered House atlases or the full enemy/item/unlock economy.

**Kaizen task:** deferred as redundant with existing versioned save/event-log roadmap t-012 and t-029's outstanding adversarial integrity scope; recommend a scoped legacy-trust tier as their next increment.

## 2026-10-30 | Reviewer → Worker | memory-dungeon/t-041 | critique

**Decision:** merged Conductor PR #6847 (https://github.com/silasfelinus/conductor/pull/6847), squash 137e8bbcff30c793faad6b6eeeb2b3b782312708.

**What was good:**
- Eight existing Hoshimori ArtJob receipts (52108–52115) are preserved, with read-only identity, ArtImage and fresh media HEAD evidence rather than resubmitting or promoting incomplete images.
- All four exact-head workflows finished green on 5dc343a9b970bc2b386a3684ced6e42dd213bab3: Worker PR CI #41102496433, Security Audit #41102496458, Worker handoff #41102496473 and task-events validation #41102496542 (two expected skipped jobs).
- Offline tests cover delivered, stale, mismatched and missing image states; the Auto Art Generate push workflow #41109429247 was triggered after merge.

**What to improve:**
- A receipt, DONE ArtJob or fresh HEAD is not visual acceptance. Review the actual eight renders and require 8×8/6×6 atlas topology, distinctive cast and correct attachment before considering the style proof accepted.
- The first-stage Hoshimori work still has 36/64 sites, 9/36 Oven rooms, 30+2 gallery incomplete and the e03–e06 entry path blocked; keep the project ACTIVE.

**Kaizen task:** deferred because t-045 already explicitly owns Hoshimori style-proof visual acceptance, atlases and gallery verification. Do not create a duplicate geometry task.

## 2026-10-31 — Reviewer: PR #6874 archive done-task notes (merged)

**Decision:** merged (squash, e70de7b). Reversible, scoped docs/roadmap-hygiene change: 9 done-task `note:` bodies moved verbatim to `HISTORY.md`; roadmap 168,738 → 141,646 bytes, clearing the 150KB oversize flag.

**Verified:** CI green on head, `archive_done_task_notes.py --project memory-dungeon --verify-only` passes (every pointer resolves), roadmap YAML parses.

**Pattern:** good use of the sanctioned archive helper rather than hand-editing notes. No kaizen task created — the helper already exists and the oversize flag is cleared.

## 2026-10-31 — Reviewer: t-047 canon branch (#6878 → #6880)
- #6878 had green CI but conflicted with main in `roadmap.yaml` (13 hunks) and `CONTROL.md`. The branch's roadmap diff changed only task notes (no status/claim/dep changes), and main had already slimmed notes via #6874 while worker t-023 kept appending. Resolved by taking main's live roadmap and keeping the PR's CONTROL.md writer-access paragraph; docs were already on main. Superseded by #6880.
- Pattern: a roadmap-wide note rewrite on a branch will always collide with task-event churn. Slim notes in a small PR cut from fresh main, or leave roadmap notes alone and add archive files only.
- The comet-city-academy t-021 unblock branch (remove duplicate `updated:` line) was moot: the duplicate no longer exists on main. Branch left for branch-janitor.

## 2026-11-01 PT | Reviewer CI rescue | memory-dungeon/t-038 | Kind Robots #4597

**Decision:** merged reversible e10 fragment-integration PR #4597 (squash `5f579ccd4229fe5e95b87271ed58a01eb59c9a11`) after all 14 exact-head workflows passed on `8a92604fcef20a0a1ba9e962019c4bb0d68ab431`.

**What worked:** two Morrow collision encounters use existing fragment IDs, authored choice effects and replay-validated travel; 162 combinations cover earned e04/e07/e09 history, with forged-history, teleport and duplicate-fragment regressions. The patch stayed in five Memory Dungeon files and did not touch deployment, Classic Match or schema.

**What to improve:** the original PR opened with a missing `string | undefined` guard and three unformatted files, causing TypeScript, changed-file Prettier and contract-ratchet failures. The first repair also omitted an argument separator in a test. CI diagnostics isolated both failures; repair the type narrowing and apply the exact formatter patch *before* the next PR, then verify the final exact head. No check or baseline was weakened.

**Kaizen:** e10's actual player-facing console and local crossroad are already explicitly outstanding in the master task and #4136. Do not create a duplicate task; prioritize integration and e08's entry gate over more detached writer packets. ArtJobs remain unsubmitted.

## 2026-11-01 PT | Reviewer green merge | memory-dungeon/t-038 | Kind Robots #4599

**Decision:** merged reversible Morrow e10 console PR #4599 (squash `2fee0bd9fa89ebbf158953a01ace7749bb673ae2`) after all 20 exact-head checks and 15 workflows passed on `950642af0a8db3c2b21afcbbe9afaaf77914772b`; reviewed six Memory Dungeon-only files. Contract Tests #41327943800 passed all four shards and aggregate, with TypeScript, Prettier, layout, scroll ownership and browser-interruption green. No deploy or production art.

**What worked:** the new console uses replayed adjacent movement, earned e04/e07/e09 history and two fragment receipts without fabricating e10 completion. The earlier formatting failure was fixed on the same PR. **What to improve:** add a behavior-level interrupted-save/end-to-end cross-world gate test once e08 progression and e10's actual crossroad are built; today's integration checks are primarily structural. This is already covered by the open master roadmap and should not become a duplicate task. Master issue #4136 remains open and Memory Dungeon active.


## 2026-11-01 PT | Reviewer green merge | memory-dungeon/t-038 | Kind Robots #4601

**Decision:** merged reversible Morrow e10 crossroad PR #4601 (squash `2d9ad68b08a6e6975f403f718a2aad80166381a2`) after all 16 exact-head workflows passed on `d71620d6eeec462f83d0aae595050807b7f67bd0`. Contract Tests #41343823383 passed four shards plus verifier; TypeScript, formatting, layout, scroll ownership and Memory browser interruption succeeded. Six Memory Dungeon-only files; no unresolved reviews. No deployment or rendered ArtJobs.

**What worked:** the clock-tower finale requires replayed adjacent travel, twelve unique decisions and both earned fragments before saving an e10 verdict; two outcomes preserve historical Scylla, Vesper and Pip decisions rather than fabricating consent or rescues. The earlier formatting failures were repaired on the same PR, with no weakened checks.

**What to improve:** e08 remains the actual normal-play progression blocker, so the next implementation should complete its earned exit and adversarially test interrupted-save e08→e09→e10. Production images and the remaining authored sites still need independent verification. This work is already tracked under the open master task and #4136; do not create a duplicate kaizen task.

## 2026-11-01 PT | Reviewer green merge | memory-dungeon/t-038 | Kind Robots #4602

**Decision:** merged reversible e10 connective-encounter PR #4602 (squash `ecb31cc6457903978be7ec32c2f2ecfc1ab7835a`) after all 14 exact-head Actions workflows passed on `66021727d239326b2055439b797e67d6465ba344`; Contract Tests ran all four shards plus verifier. Three Memory Dungeon-only files, no unresolved review threads, no migration or deployment. Eight original sites add sixteen replay-validated choices without replacing fragments, photographs or the clock-tower finale.

**What worked:** legal adjacent travel, once-only journal rewards, forged-choice rejection, stable art-shaped placeholders and continuity-sensitive narrative; the existing master issue remains open for the unfinished campaign.

**What to improve:** this PR needed two successive formatting repairs before CI became green. Run changed-file formatting locally before submission, or apply the exact formatter suggestion once and recheck the entire changed file; avoid repeated CI-only patch loops. The highest-value gameplay work is still the already-tracked e08 earned completion gate and interrupted-save e08→e10 test, not another duplicate kaizen task. No ArtJob IDs or delivered images were produced.

## 2026-11-01 PT | Reviewer green merge | memory-dungeon/t-038 | Kind Robots #4618

**Decision:** merged reversible World Ten route-echo PR #4618 (squash `c53c42938a0d2b5cfe9a66ee1b2feece294069b1`) after all 15 exact-head Actions workflows passed on `92fdb1f876916138d4b97387e0dd5655ed8cb81d`; Contract Tests #41374983654 passed four shards and verifier. Three Memory Dungeon files, no unresolved reviews, schema changes or deploy.

**What worked:** four earlier e10 encounters now feed eight earned callbacks into both clock-tower verdicts. The narrative reads replayed adjacent-travel journal choices, not serialized flags; tests exercise 16 verdict/route cases, missing or forged choices and JSON save restoration. Existing e04/e07/e09 history gates, fragment checks and Classic remain unchanged.

**What to improve:** add an interrupted-save end-to-end campaign test from e08 through e10 once e08 is actually completable. It is already owned by the master issue and t-046's acceptance scope, so do not duplicate it as a new kaizen task. e09/e10 authored coverage, e11/e12, actual ArtJob delivery, gallery integration and rendered-device acceptance remain unfinished; keep the project ACTIVE and the issue open.

## 2026-11-01 8:50 PM PT | Reviewer green merge | memory-dungeon/t-038 | Kind Robots #4624

**Decision:** merged reversible e10 finale continuity PR #4624 (squash `fe85ec71d169338d795f9984d2a5c277290a0d44`) after all 8 exact-head Actions workflows passed on `f35528847863f6ad1abd42018db85bcdef470345`, including Contract Tests, TypeScript, formatting, layout and Memory browser interruption. Reviewed two Memory Dungeon-only files; no unresolved review threads, schema changes or deployment.

**What worked:** all eight authored e10 route encounters now have distinct, replay-earned opening and outcome callbacks for both clock-tower verdicts. Coverage guards against future authored routes lacking callbacks; tests cover 32 verdict/route combinations plus forged/missing decisions and save restoration. **What to improve:** the e08 earned completion gate remains the high-value blocker, followed by an interrupted-save e08→e09→e10 campaign test and production-art delivery. Those are already tracked in the active master roadmap and issue #4136; avoid a redundant kaizen task. No ArtJobs or rendered assets claimed.

## 2026-11-01 PT | Reviewer green merge | memory-dungeon/t-042 | Kind Robots #4627

**Decision:** merged reversible Saffron Wing PR #4627 (squash `86413bcdf8c8802a19682f84b82ee21d90ec7755`) after all eight exact-head Actions workflows passed on `829609f791d4c8e0c62dd854dd3dc6e782fea27f`, including Contract Tests, TypeScript, formatting, layout and Memory browser interruption. Four Memory Dungeon-only files; no unresolved review threads, migrations or deployment.

**What worked:** six authored OV-22..OV-27 rooms add twelve Vesper-centered decisions and 64 replay-validated testimony accounts, earned entry, old-save restoration, forged-choice rejection and once-only rewards. Hoshimori now has 64/64 warm sites and 27/36 Red Oven rooms. A session-aware ready event released t-042 for the nine unfinished rooms.

**What to improve:** formatting needed two CI repair commits; run full changed-file Prettier before PR when a local checkout is available. Complete OV-28..OV-36 and the guardian aftermath before attempting the World Eight earned exit, then interrupted-save e08–e10 adversarial testing. Gallery briefs, ArtJob delivery and rendered-device QA remain separate tracked work. Avoid a duplicate kaizen task because these gaps already belong to t-042/t-045/t-046 and master issue #4136.


## 2026-11-02 3:46 AM PT | Reviewer green merge | memory-dungeon/t-042 | Kind Robots #4640

**Decision:** merged reversible Seventh Bell PR #4640 (squash `9a90681b63b9d1c928c3fb42cb9e05f00f1cfd9e`) after all eight exact-head Actions workflows passed on `34aafd1371ed47ffa8f460c51d25037f287dcdd5`, including Contract Tests, formatting, TypeScript, Memory browser interruption, layout, architecture, Playbook Kit and schema parity. Reviewed four Memory Dungeon-only files and found no unresolved review threads, migration or deploy.

**What worked:** OV-34..OV-36 complete the 36-room Red Oven with six earned choices, eight final accounts, 24 guardian/route combinations, three guardian aftermaths, legacy Glass save restoration, retreat/reentry, and forged-choice/duplicate-reward guards. Earlier quenching stays binding. The project remains ACTIVE, and the t-042 claim was queued for READY rather than DONE because its 30+2 gallery briefs remain unfinished.

**What to improve:** two formatting CI failures required a correction commit before all eight checks passed. Run changed-file formatting before PR where a checkout exists; with connector-only tools, use the CI-suggested patch. Finish gallery briefs in t-042, actual image receipts in t-045, then e08 earned progression and interrupted-save e08→e10 QA. These are already tracked, so avoid a duplicate kaizen task. No new ArtJobs, rendered artwork or deployment claimed.

## 2026-11-02 11:50 AM PT | Reviewer green merge | memory-dungeon/t-048 | Kind Robots #4642

**Decision:** merged reversible fog-and-beacon PR #4642 (squash `73f7f8004e69e24c66f863730c81a175d718a836`) after seven exact-head workflows passed on `37c06b07890e1ca90c5973617a0bd73c01b01ee7`. Inspected all four Memory Dungeon-only changed files, source issue #4641 and review threads; no unresolved threads, migration or deploy.

**What worked:** coordinate-aligned 8×8 illustrated forest fog replaces clinical unrevealed squares; story diamonds are removed; larger animated beacons center on actionable tiles with reduced-motion support. Tests cover fog alignment, overlap, beacon position and source contracts. The right-hand encounter pane and saved progress were not changed.

**What to improve:** the SVG is a reversible illustrated fallback, not a delivered production-painted map. CI validates code but cannot prove 390/768/1440px pixel quality before a self-hosted deploy. Keep painted media delivery in t-045 and rendered-device acceptance in t-046; avoid duplicating those existing tasks. The unrelated e08 Bellroad PR #4667 has a cancelled-shard Contract Tests rerun in progress and must not be merged without its own complete green verification. No ArtJobs or deployment this review.

## 2026-11-02 12:47 PM PT | Reviewer green merge | memory-dungeon/t-044 | Kind Robots #4667

**Decision:** merged reversible Bellroad nightmare PR #4667 (squash `11bb8ae9473d143c23d0785560f43fa29c1aa077`) after all eight exact-head GitHub Actions workflows passed on `87f5450ba90141cb30197a1859e8f17754c66a9b`, including Contract Tests #41504090307, TypeScript #41504090234, formatting #41504090254, Memory browser interruption #41504091019, layout, architecture, schema parity and Playbook Kit. Four Memory Dungeon files, no unresolved review threads, no migrations, ArtJobs or deployment.

**What worked:** eight new 8x8 night sites with sixteen original choices, a replay-earned Windward prerequisite, eight distinct Bellroad witness accounts and 64 seeded playthroughs covering route denial, save restoration, forged choices, once-only rewards and Earth-photo continuity. World Eight is 32/64 authored sites. **What to improve:** previous formatting retries were expensive; run changed-file Prettier before PR or apply the exact CI patch once. Complete remaining 32 sites and 36-room transformed Oven, then e08 completion and interrupted-save e08-e10 testing. Those are already covered by t-044/t-046 and master issue #4136; avoid a duplicate kaizen task. Production art, gallery attachment and rendered-device acceptance remain unfinished. Return t-044 READY, not DONE.
