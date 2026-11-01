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
