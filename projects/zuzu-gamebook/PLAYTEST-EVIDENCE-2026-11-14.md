# Zuzu Gamebook: measured playtest evidence and final art selection worklist
**As-of:** 2026-11-14 PT. **Decision:** not yet certified for human playtest. Keep [#4139](https://github.com/silasfelinus/kind_robots/issues/4139) open, Conductor active/high.

This is a source-and-CI-backed replacement for the stale 2026-11-12 art **count**, not a replacement for the [readiness exit contract](PLAYTEST-READINESS-2026-11-14.md). Do not promote ArtJobs based on their prompt, completion status or candidate number alone.

## Current reproducible baseline

| Measurement | Observed result | Source and verification |
|---|---:|---|
| Book One scenes | **385** | Unique `s('id', ...)` declarations in `kind_robots/utils/zuzuGamebook/book.ts` and `acts/act1..9.ts`; app main commit `b21e751be9722d499b08d6f9660ca0781f9c6674` |
| Endings | **15** | Kind Robots contract suite at commit `1d366b4fa9d06293684e0ce9c0893222de76ba57`, completed success 2026-11-14 |
| Endings with legal seeded witnesses | **15/15** | Contract Tests run `43649658318`, shard 1 job `132615157202` logged all 15 `Gamebook witness` results and passed |
| Existing exact section plate registrations | **371** | Unique keys in `utils/zuzuGamebook/sectionArt.ts` |
| Corresponding exact section WebPs present in repo | **371/371** | Git tree `public/zuzu-gamebook/scenes/sections/*.webp`: no missing or orphan image files |
| Scene IDs lacking their *own* exact section plate registration | **14** | Compare all 385 scene IDs against the 371 exact keys |
| Current graph and combat QA | **passes** | Same contract run: graph acyclic, act pacing, route choices, combat replay, wound retreats, dice, inventory, saves, resource costs |
| Main-game Continue | **merged / CI green** | Kind Robots [#5179](https://github.com/silasfelinus/kind_robots/pull/5179), 16 completed-success workflows; actual Unraid deployment/schema verification remains outside GitHub |
| Achievements | **17 authored** | Kind Robots [#5059](https://github.com/silasfelinus/kind_robots/pull/5059); do not confuse CI with a fresh live award test |
| Persistent cast gallery | **merged / CI green** | Kind Robots [#5158](https://github.com/silasfelinus/kind_robots/pull/5158) |

A registered file is **not** proof of good scene composition; a missing registration is **not** necessarily a missing image. The roster below is the exact unresolved acceptance set on source `main`. The 2026-11-12 report listed 35, but subsequent PRs delivered more exact entries.

## Remaining 14 registrations: known candidate evidence

| Section ID | Candidate ArtImage IDs or accepted legacy context | Next action |
|---|---|---|
| `a1-ridge-retreat` | Round 20: **270446, 270447** (both DONE) | Inspect Zuzu's wounded withdrawal, waterhole and one-eyed coyote; export approved WebP and exact registration |
| `a4-well-scatter` | Round 20: **270438, 270439** (DONE) | Check supplies fly toward well; children escape toward rock cleft |
| `a4-well-slip` | Round 20: **270444, 270445** (DONE) | Check sister's earned distraction, bandage and escape |
| `a8-under-the-wall` | Round 20: **270448, 270449** (DONE) | Check solitary Zuzu entering the dry drain, not a generic battle pose |
| `a8-behind-the-altar` | Round 20: **270440, 270441** (DONE) | Check black candles, rope, deep dark gap, alone/stealth |
| `a8-wounded-flight` | Round 20: **270442, 270443** (DONE) | Check rope cut, children flee up stair, wounded hero |
| `a8-give-ground` | Round 20: **270450, 270451** (DONE) | Check wounded Zuzu withdraws alone on low stair |
| `apple-tree` | Round 17: **251964–251966** (DONE); existing shared purpose-painted `apple-tree` plate | Inspect against fruit on flat rock and watching Ling/Bao; select own section asset if accurate |
| `a2-wax` | Round 17: **251958–251960** (DONE) | Inspect exact wax detail before acceptance |
| `a3-apples-reach` | Round 17: **251970–251972** (DONE) | Inspect the sister reaching for the offered apples on the rock |
| `a2-bell-view` | Round 17 **252179–252181**; Round 18 Krea **252193–252195** (DONE) | Follow the explicit 2-stage critical-object rubric: bell, high overlook, distant pale tower, tiny tracks; `ROUND-18-SELECTIONS.yaml` is **not approved** |
| `a4-bloom` | Round 17 **252185–252187**; Round 18 Krea **252198, 252574, 252199** (DONE) | Verify dense yellow/white/violet bloom and preserve composition through Arthemy; no approved stage-two selection |
| `a5-wellhouse-reckoning` | New scene in Act V, formerly *no* candidate; [Conductor #7409](https://github.com/silasfelinus/conductor/pull/7409) added two **private priority-1000** Round 22 candidate requests | Verify queued ArtJob IDs, DONE private images, genuine maternal well-house moral choice; integrate exact WebP |
| `ending-water` | Existing purpose-painted legacy **243308**, `kasa-on-water.webp` via `PLATES['kasa-on-water']` | Check loaded dedicated ending image on device; do not fabricate a `sections/ending-water.webp` registration or needlessly rerender |

### Important non-blocking rendered assets
Round 21's **20/20 DONE** ArtJobs 69323–69342 / ArtImages 272202–272221 are candidates for ten earlier scenes, but this latest exact-registration comparison **already finds those ten IDs registered** (from older art). Do not overwrite a currently accepted plate merely because a newer candidate is DONE. Verify frame-by-frame before any replacement.

Round 19 staged Arthemy img2img remains intentionally dormant until Krea selections with real image hashes and score ≥7/8. Keep the paired-character fusion / Abbess human-face failure under `t-012`, separate from numeric section coverage.

## Remaining finite acceptance actions
1. **t-006 / t-012:** the art operator with authenticated private image access inspects rendered pixels, chooses or rerolls under canon; exports actual verified WebPs, registers each exact plate with real `artImageId`/source and alt; fixes multi-character composition failures; reruns art file and layout tests. No scene-coverage waiver for generic art.
2. **t-007 / t-008 / t-013:** editorial review of the now-expanded Act V `deliver` reckoning and later consequences, full-route choice agency, fight win-rate/retreat matrix; inspect responsive fight-warning cues at 390/768/1440.
3. **t-015 / t-009:** run fresh end-to-end authenticated account save/reload across devices on **self-hosted** `kindrobots.org`, validate signed-in storage and migrations; run actual reader screenshots in phone/tablet/wide-short/desktop with reduced motion, keyboard and screen reader. GitHub's production image publication is not proof the Unraid container and schema are live.
4. **t-009:** rerun all 15 legal ending witnesses and full contract suite after final art/UX PRs land. Add dated screenshots + an empty unresolved defect list to this packet.
5. **t-017:** only **after** all above, hand off with `needs-human` (never `approved_by_human`), move `project-overrides.yaml` to `playtest/normal`, verify the Kind Robots projection, flag [master issue #4139](https://github.com/silasfelinus/kind_robots/issues/4139) for human testing and close it as completed. This is not public launch authorization.

**Evidence rule:** DONE ArtJobs, source compilation and green automated contracts do not establish visually correct art or a verified live mobile experience. Keep the genuine final blockers visible instead of renaming them “human playtest.”
