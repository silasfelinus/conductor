# Zuzu Gamebook: playtest handoff evidence packet

**As of:** 2026-11-15 PT
**Decision:** READY FOR HUMAN PLAYTEST. Silas asked on 2026-11-15 PT: *"Help us get Zuzu Gamebook through the
final lap on its roadmap … ready for human playtests … the issue will be closed, and the project on kind robots
will be set to 'playtest' and normal."*
Every finite agent-owned task is done or cancelled. `t-017` waits at `needs-human` (subjective-acceptance, **not**
approved) and the recurring `t-011` continues as bounded playtest iteration. This is not approval for public release,
billing or production side effects. It closes out the plan in
[PLAYTEST-READINESS-2026-11-14.md](PLAYTEST-READINESS-2026-11-14.md).

Play it at **https://kindrobots.org/play/zuzu-gamebook** (self-hosted Kind Robots).

## Counts on current source
| Measure | Value | Source |
| --- | --- | --- |
| Authored Book One sections | **385** (nine acts) | `verifyZuzuGamebook.test.ts` contract line |
| Endings | **15**, every one reachable from `the-crossing` | same |
| Sections with their own exact painted plate | **385 / 385** (was 371) | new contract assertion, kind_robots #5192 |
| Temporary SVG stand-ins | **0** (bell-view and desert-bloom painted) | new contract assertion |
| Golden full-route replay witnesses | **15**, one per ending | `utils/scripts/fixtures/zuzuGamebookGolden.json` |
| Achievements | 17 | #5059 |

## P0. Art (`t-006`, `t-012`) - done
The 14 sections without an exact plate on 2026-11-14 were all resolved after review of the real rendered pixels.
Per-image verdicts are recorded in `art/ROUND-20`, `ROUND-22` and `ROUND-23` ledgers.

| Section | Shipped plate | ArtImage |
| --- | --- | --- |
| a1-ridge-retreat | Zuzu climbs out of the reeds, katana in paw | 270447 |
| a4-well-scatter | spilled cookpot, jackal at the cleft mouth | 270439 |
| a4-well-slip | bandaged-throat jackal watching the cleft | 270444 |
| a8-under-the-wall | Zuzu flat in the scrub at the wall opening | 270448 |
| a8-wounded-flight | blood trail down the altar steps | 270442 |
| a8-give-ground | wounded Zuzu, back to the wall, sword low (tall) | 270450 |
| a2-bell-view | inked house-style pass of Krea 252193 (bell, rail, pale tower, tracks) | 272618 |
| a4-bloom | inked house-style pass of Krea 252199 (yellow/white/violet carpet, standing rain) | 272620 |
| a2-wax | purpose-painted black wax on the threshold | 243524 |
| a3-apples-reach | purpose-painted sister feeding her brother an apple | 243533 |
| apple-tree | purpose-painted lone apple tree, small fox beneath | 242569 |
| ending-water | purpose-painted kasa floating on black water | 243308 |
| a5-wellhouse-reckoning | canteen-and-silver still life ("The Price of Water") | 245125 |
| a8-behind-the-altar | black-candle still life | 243524 |

Rejected on review: human-faced nuns (270440/270441), a dog drawn as Zuzu (272577), a human woman (272578), a human
child (272625), a hearth (272624), a face carved into an altar (272628), dim interiors that lost the scene
(272622/272623/272627), and the photographic Krea originals as final art.

**t-012 (two-character LoRA fusion):** resolved at the rendered-frame level, not by retrying stacked LoRAs. Rounds
13-16 already replaced 107 plates with on-model single-figure or recomposed frames and kept the live plate wherever
a paired candidate fused or drew human faces. This pass made no new paired-cast plates. Every scene added here is a
single figure, an empty scene or a still life, each checked against its section text. No fused or human-faced
figure ships. Regional-mask or composite two-character art stays available as `t-011` polish if Silas wants it.

## P1. Editorial and mechanics (`t-007`, `t-008`, `t-013`) - done
- `t-007`: the Act V "deliver" shortcut now carries a moral aftermath (`a5-delivered` → `a5-wellhouse-reckoning`,
  kind_robots #5176). Act IV length (15-25 sections) and the five-page Night Road slog are kept as deliberate pacing,
  pinned by the act-pacing contract (no backward act edges, act-skips land on bridges, at most 5 single-way pages).
- `t-008`: combat calibration is pinned by a seeded test (400 seeds per fight, kind_robots #5192):
  Guard is the best answer to the Abbess (66% vs 44-56%), Quiet Draw beats beasts and packs (crocodile 93%,
  jackal band 50%), Feint is the best free answer to the band once Resolve is spent, and plain Strike is never the
  best move. Combat log, odds, hit feedback, character-sheet drawer and save codes were already shipped (#4826, #4864).
  Outcome scenes after every fight now show painted plates (385/385). A shorter save code is optional polish.
- `t-013`: earned wounded retreats (#4780), crocodile risk cues (#5166). Responsive check of the fight cue on the
  live reader: the "FIGHT" chip and "Wounded, 1 HP: losing ends the journey" render on the wounded-Abbess choice at
  390×844, 768×1024, 1024×768, 1440×900 and 1280×600. The earned "give ground to the cellar stair" exit is
  offered beside it.

## P2. Main-game floor (`t-015`) - done
Account-backed Continue with local fallback and two-device conflict resolution (#5179), corrupt-slot isolation
(#5154), persistent cast-discovery scrapbook (#5158), confirmed full-progress reset distinct from New Journey (#5185),
title, reading settings and painted endings (#5070), 17 achievements (#5059). Character customization is exempt
because Zuzu is the fixed protagonist.

## P3. Independent QA (`t-009`) - done
- `npm run test:zuzu-gamebook` on the #5192 head: graph, reachability, acyclicity, act pacing, stateful exploration,
  plates, items, dice, combat replay, saves, power costs, title/settings/endings and scrapbook all pass. Batteries
  include 15 golden witnesses, a 1,500-walk forced-fight battery, a 12,000-walk hopeless-fight battery, seeded
  wounded/exhausted fight matrices (health 3/12 × Resolve 0/2/4 for every battle) and the 120-seed crocodile
  approach.
- Live device pass (Playwright against kindrobots.org, current main) at 390×844, 768×1024, 1024×768, 1440×900 and
  1280×600 for a fresh title screen, a wounded Act VIII save and an Act VIII altar save: no horizontal overflow, no
  page errors, scene plates load, keyboard Tab reaches the choice cards (role=listitem). Screenshots:
  [playtest-evidence-2026-11-15/](playtest-evidence-2026-11-15/).
- Known minor observation: on phones the choice-card captions are small (about 9px). Their full text is in the card
  and readable to screen readers. A good first playtest question.

## P4. Handoff (`t-017`)
- `t-017` → `needs-human`, `approved_by_human` left unset. Silas's verdict drives new `playtest_iteration` tasks.
- `project-overrides.yaml`: `active/high` → **`playtest/normal`**. `priority.yaml`, the CONTROL.md band and the
  priority contract test move together. The other five focus projects keep their order.
- Master issue [kind_robots#4139](https://github.com/silasfelinus/kind_robots/issues/4139): prefixed
  `[FLAGGED FOR HUMAN TESTING]` and closed as completed (also enforced by `sync-playtest-master-issues`). The URL stays
  in `docs/agents/master-issues.yaml`.

## What to try first (review asks for Silas)
1. Play one full journey from a fresh start. Does the nine-act shape feel like a complete book?
2. Take a wounded route into Act VIII. Are the fight warnings and the earned retreats fair?
3. Try Guard against the Abbess and Quiet Draw against the crocodile. Do the moves feel distinct?
4. Look at the bell view (Act II) and the desert bloom (Act IV): do the new inked plates sit right among the rest?
5. On a phone, are the choice-card captions readable enough?
