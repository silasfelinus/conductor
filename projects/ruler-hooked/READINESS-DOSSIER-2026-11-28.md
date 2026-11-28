# The Ruler Is Hooked — playtest readiness dossier (t-051)

Date: 2026-11-28 (Pacific). Master issue: [kind_robots#4144](https://github.com/silasfelinus/kind_robots/issues/4144).
Governing direction: CONTROL.md game readiness (2026-11-26) and
[main-game-standard.md](../../docs/agents/main-game-standard.md) owner directions of 2026-11-26 and
2026-11-27: finite acceptance rests on delivered, reviewed implementation with passing automated
checks; live, physical-device, signed-in and audible observations transfer to human playtest.

**Verdict: ready for human playtesting.** All finite build, art, content and QA tasks are done, no
known critical/high defect is open and no mandatory art is queued. This is not a creative signoff,
deployment or publication approval; those remain separate.

## 1. Roadmap reconciliation

- 78 tasks: 77 done after this handoff, 1 cancelled (t-032, the obsolete subjective vertical-slice
  gate, retired by Silas on 2026-11-26 — not an approval). Nothing ready, waiting or in review.
- t-051 dependencies, all done: t-031 (42-species roster), t-046 (editorial depth), t-047 (art
  delivery), t-048 (fishing fairness/economy), t-049 (policy matrix and ending graph), t-050
  (combined console acceptance), t-057 (console art lane), t-058 (expression sets), t-061 (responsive
  audit), t-067 (main-game standard). Receipts in [HISTORY.md](HISTORY.md).
- Open PRs: none for Ruler Hooked in kind_robots or conductor at audit time.

## 2. Independent rerun of the full automated suite

All 16 steps of Kind Robots `.github/workflows/ruler-hooked.yml` were rerun locally on Kind Robots
main `0d0ee2f3` (#6019 merge) on 2026-11-28. Every step exited 0.

| Suite | Result |
|---|---|
| game / engine / advisor / incidents | ALL PASS (incidents: 12/15 drawn in four seeded reigns) |
| encounter | 491 attempts, 420 catches, 71 escapes |
| simpleFishing / timingBar | pass |
| quiz (geography, Mandarin, answer sheets) | pass |
| consolePOV | 16 input-latency/frame-pacing scenarios; unseen-player POV contract pass |
| economy | pass |
| quests (policy matrix) | 144 reigns × 12 policies, 16,959 attempts, 152/152 authored choices, 0 uncovered, 142 distinct worlds, 5 destinations opened, 3 closures observed, 10 targeted choice witnesses |
| artPrompts / cardArt / console | every card, fish, character, ruler, reward, shop item and ending is prompted and bound |
| audio | interruption and lifecycle pass |
| achievements | 18 achievements wired and awarded at the deed |

## 3. Legal ending witnesses (from New Game, no injected state)

| Ending | Finale | Seed | Casts |
|---|---|---|---|
| druid-utopia | The Angler's Grove | `ending-druid-utopia-0` | 35 |
| warlock-metropolis | Boomtown by the Lake | `ending-warlock-metropolis-0` | 35 |
| thistlewood-empire | The Thistlewood Empire | `ending-thistlewood-empire-0` | 36 |
| fishers-peace (secret) | The Ruler Who Never Ruled | `ending-fishers-peace-0` | 36 |

Editorial catalog: 60 narrative cards, 6 arcs, 4 finales; 25 terminal arc transcripts (t-046, #5891).

## 4. Fish ecology reachability (new audit check)

Question: can every species legitimately appear at an unlocked location in real play?

- Instrumented the policy matrix to record `fishAtLocation` pools each turn: 41/42 species become
  available, including the gated EPIC Ironmandate Skate (exclusive pier + order ≥ 60 + joy ≤ 45).
- The remaining species, Tarflower Catfish (river concession, treasury ≥ 60, nature ≤ 45), appears in
  a separate 3,000-seed random-choice sweep: seed `reach-802`, turn 43, lake.
- Result: **42/42 species reachable** through legal choices. No unreachable fish; no defect filed.
  The audit harness was temporary and not committed.

## 5. Main-game standard (rechecked against current main)

| Row | Status | Evidence |
|---|---|---|
| Title screen | Met | `ruler-hooked-slots.vue`: new/continue reign, Settings, Scrapbook, Achievements (#5701, #5702, #5723) |
| Settings | Met | display settings (text size, reading speed, contrast, reduced motion, restore defaults) and audio settings (music, sound, mute), persisted (#5701, #5702, #5723) |
| Save/load | Met | versioned saves with migration, autosave, account archive sync and retry (#5735, #5814, #5869, #5875, #5917, #5985); per-reign delete with confirmation |
| Achievements 12+ | Met | 18 in `utils/achievements/catalog/main/ruler-hooked.ts`; selftest asserts award and deduplication (t-068) |
| Scrapbook | Met | `ruler-hooked-scrapbook.vue` + `utils/rulerHooked/scrapbook.ts` reign keepsakes persist across reigns; Fishopedia collection |
| Multiple endings with plates | Met | 4 endings, 4 painted plates (#5595) |
| Customizable characters | Met | name, honorific, 12 ruler presets, custom portrait |
| Replay hooks 3+ | Met | seeded reigns, multiple saves, branching arcs/endings, 42-species collection, quiz difficulty modes |
| Art-first single-screen console | Met | production audit 45901306030: 36 screenshots at four viewports, no document flow or clipped galleries; audit coverage extended in #5920, #5954, #6008 |
| Original generated art and icons | Met | 299/299 ruler-hooked rows in `projects/art-prompts.yaml` done, 0 pending; 120 vista combinations and 52 candidate paintings checked (#6000) |
| Sound and music | Met | original scene audio and recovery (#5692, #5960); audio selftest pass |
| Complete gameplay and adversarial testing | Met | sections 2–4 above |

## 6. Remaining risks (non-blocking, for playtest)

- No current-head deployed browser run: scheduled audit 46071531242 was cancelled. Visual,
  physical-device, signed-in cross-device and audible playback observations are playtest items and
  were not claimed as executed.
- Earlier deployed build (audit 45901306030) showed older/mixed art in coronation and lake scenes; the
  current ledger and runtime bindings address this, but the live build has not been re-observed.
- Five done art rows lack explicit ArtJob IDs and three card URLs lack source metadata (t-047); no
  evidence any asset is missing.
- Fish roster growth from 42 toward 60 is optional catalog work, not a gap.
- Subjective fun, pacing and long-form depth are the human playtest's question.

## 7. Handoff

- `project-overrides.yaml`: `ruler-hooked` → `status: playtest`, `priority: normal`.
- Milestones m4 and m6 done; t-051 done.
- Master issue #4144 → title prefixed `[FLAGGED FOR HUMAN TESTING]`, closed as completed (via
  `sync-playtest-master-issues`, or manually if the workflow cannot).
- Later fixes use `playtest_iteration: true`. Deployment, publication and creative signoff need
  separate explicit approval.
