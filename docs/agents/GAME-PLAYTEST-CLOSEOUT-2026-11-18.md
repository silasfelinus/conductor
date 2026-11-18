# Kind Robots game playtest closeout — 2026-11-18 PT

**Decision:** Silas confirms that **100% means ready for human playtesting**, not
human-tested, human-accepted, released, or publicly promoted. Complete the finite
agent-owned roadmap first; only then flip Conductor to `playtest/normal` and let
`sync-playtest-master-issues` flag and close the indexed issue. A closing human
verdict cannot be added to the build denominator. Preserve genuine publication,
security, billing, and release permissions separately.

This is an evidence-based reconciliation of the sixteen currently open Kind Robots
game roadmap master issues (Conductor roadmaps and project-overrides as read on
2026-11-18 PT). Counts are task statuses, **not** percentages of shipped gameplay.
No open-issue project passed finite production readiness in this pass. Do not flip
a lifecycle or close an issue merely to improve the count.

## Closeout queue

| Project (Conductor slug) | Issue | Lifecycle/priority | Done/total | Concrete remaining finite work |
| --- | --- | --- | ---: | --- |
| Ecotone (`weird-humboldt`) | [#4145](https://github.com/silasfelinus/kind_robots/issues/4145) | active/high | 64/75 | t-072 main-game standard: 15 missing ending plates, guides-met and per-run scrapbook; t-020 ending prose review, t-021/t-025/t-028 reachability, t-016 real widths, t-070 production umbrella |
| Slime City (`slime-city`) | [#4535](https://github.com/silasfelinus/kind_robots/issues/4535) | active/high | 62/71 | t-041 constructed 300-card evolution balance and art; t-012 full CLASH/crew/end-to-end QA; t-069 authenticated real-browser 390/768/1440. t-009 subjective fun testing must **not** block automated QA or graduation by itself |
| Space Couch (`game-of-captains`) | [#4182](https://github.com/silasfelinus/kind_robots/issues/4182) | active/high | 32/41 | t-008/t-009 curated painted art and redos, t-033 redshirt plates, t-031 alien collection, t-032 remaining Act III, t-039 planet outcomes, t-011/t-041 editorial/standard QA |
| Cthulhuquarium (`cthulhuquarium`) | [#4140](https://github.com/silasfelinus/kind_robots/issues/4140) | active/normal | 88/101 | t-099 consistent sprite overhaul for 151 species; t-090/t-093 art, t-092 editorial, t-094 economy and exploits, t-091/t-095/t-096 evidence-based device QA |
| Hybridizer (`hybridizer`) | [#4876](https://github.com/silasfelinus/kind_robots/issues/4876) | active/high | 6/11 | t-007 verified 4,000 launch hybrids (36/4,000 delivered in last documented checkpoint, 2026-10-30; re-query live ledger), t-008 secure user image upload, t-009 adversarial/private-upload and viewport QA |
| Deepheart (`deepheart`) | [#5256](https://github.com/silasfelinus/kind_robots/issues/5256) | active/high | 6/14 | t-007 35 party-pair supports/romance, t-008 room tuning, t-009 account-backed saves, t-010 audio, t-012 final rendered art/URL wiring, t-013 seeded and viewport QA |
| Emperor of Dust (`emperor-of-dust`) | [#4142](https://github.com/silasfelinus/kind_robots/issues/4142) | active/high | 52/67 | t-063 ~430 rendered-image export/wiring, t-046–t-052 five-act authored story/art and coverage, t-064 scrapbook, t-066 new-reign carryovers, t-044/t-067 QA |
| The Ruler Is Hooked (`ruler-hooked`) | [#4144](https://github.com/silasfelinus/kind_robots/issues/4144) | active/normal | 52/68 | t-045/t-046 kingdom branches, t-047/t-057–t-059 art/compositing, t-048–t-051 fishing and policy matrix/device QA |
| Chessweeper (`chessweeper`) | [#5304](https://github.com/silasfelinus/kind_robots/issues/5304) | active/normal | 0/6 | t-001 first playable three-mode frontend (outward-facing PR #5305 still gated), t-002 campaigns, t-003 actual art, t-006 testable engine, t-004 real QA |
| Rainbow Bullet Hell Space Princess (`rainbow-bullet-hell-space-princess`) | [#4146](https://github.com/silasfelinus/kind_robots/issues/4146) | active/high | 31/45 | t-006 real online co-op, t-011/t-012 stages/audio, t-027/t-028 branching progression, t-030 animated cut-ins, t-013 fairness/device tests |
| Save the Plumber (`save-the-plumber`) | [#4873](https://github.com/silasfelinus/kind_robots/issues/4873) | active/high | 15/29 | t-005 enemy/powerup mechanics, t-020–t-023 authored world/level engine, t-024/t-025 rendered art/animation, t-027 editor, t-013 campaign QA |
| Prom of Doom (`comet-city-academy`) | [#4181](https://github.com/silasfelinus/kind_robots/issues/4181) | active/high | 12/35 | t-002/t-004–t-006 thirty-day arcs, t-017/t-021/t-025/t-026 48-identity origins/routes, t-007/t-008/t-031 art, t-009/t-010 adversarial QA |
| Every Villain Tactics (`every-villain-tactics`) | [#4407](https://github.com/silasfelinus/kind_robots/issues/4407) | active/high | 9/26 | t-007 six campaigns, t-008/t-009 48 individual routes, t-010 tactical AI, t-011 level sharing, t-012 painted art, t-013 campaign QA |
| Memory Dungeon (`memory-dungeon`) | [#4136](https://github.com/silasfelinus/kind_robots/issues/4136) | active/high | 29/73 | Many currently claimed/blocked tasks for twelve overworlds, dungeons, e09–e12 finale, 32-card decks per world, save/Chronicle, authored endings and full adversarial QA; **do not** mistake the original match-game slice for RPG completion |
| MONSTRIQUE (`monstress-convention`) | [#4874](https://github.com/silasfelinus/kind_robots/issues/4874) | active/high | 3/16 | t-003 inventory/hotspot room engine and saves; t-004–t-010 authored murder/case arcs, art, collectibles; t-011 maturity/child security; t-012 full QA |
| Kind Robots Arcade (`kr-arcade`) | [#4062](https://github.com/silasfelinus/kind_robots/issues/4062) | active/normal | 109/172 | Multiple unfinished cabinets and dependencies; this shared factory cannot be marked playtest-ready on the strength of one or two polished games |

## Gate reconciliation

- **Human-playtest feedback, subjective fun verdict and design acceptance** belong
  after the handoff. Historical waiting or needs-human tasks for these judgments
  must not be invented as build prerequisites. Reconcile their dependencies before
  full-run QA. In particular, Slime City's t-012 currently depends on human-fun
  t-009 even though all six authored campaigns are merged. Remove that dependency
  in a scoped roadmap PR; do not declare the actual QA done.
- **Ecotone's t-070** contains stale language saying the master issue should remain
  open for a final creative verdict. The 2026-11-15 CONTROL.md directive wins:
  verify finite readiness, then flag and **close** the issue at handoff, with
  post-handoff subjective review outside the finite roadmap.
- **Gameplay, art, save, accessibility, and adversarial-test work** never becomes a
  `playtest_iteration` merely to escape the handoff gate. Rendering requests and
  ArtJob submissions are not proof of delivered and URL-verified art.
- **Release/promotion, account/secret creation, legal and security approval** remain
  real human gates. A `playtest` lifecycle is coordination readiness only, never
  authorization to deploy or advertise.
- **100% must be fail-closed:** milestone weights alone cannot report completion
  when an agent-owned finite task is open. The 100% invariant is mirrored between
  Conductor's build_status and the Kind Robots projection parser and protected by
  regression tests.

## Next graduation sequence

1. Ecotone: complete 15 ending plates and collection gaps; reconcile t-020/t-027
   review evidence, verify seeded 56-route endings and responsive screens.
2. Slime City: keep the verified 300-card constructed balance work bounded,
   resolve t-012's stale dependency on subjective feedback, and finish real
   authenticated browser testing without using a production admin credential.
3. Space Couch: curate the last redos and redshirt plates, finish Act III, verify
   full voyages and device presentation.
4. Then Cthulhuquarium and Hybridizer art-integrity/QA lanes while Deepheart
   production continues. Preserve Conductor's protected owner-priority order as
   an official scheduling tie-breaker until explicitly changed.

For each game, the graduation reviewer should capture tested commit/check runs,
delivered ArtImage IDs, the full-run fixtures, 390/768/1440 screenshots, a game
URL, and any distinct real human publication gate. Set `status: playtest` and
`priority: normal` only then. Let the sync workflow prefix and close the
single master issue, and verify the committed Conductor projection. New
post-handoff fixes are narrowly labeled `playtest_iteration: true`.
