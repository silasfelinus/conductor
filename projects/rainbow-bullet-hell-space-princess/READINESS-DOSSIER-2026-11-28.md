# Rainbow Bullet Hell Space Princess: playtest readiness dossier

Date: 2026-11-28 (Pacific). Master issue: [kind_robots#4146](https://github.com/silasfelinus/kind_robots/issues/4146).
Governing direction:
- CONTROL.md game readiness (2026-11-26);
- [main-game-standard.md](../../docs/agents/main-game-standard.md), including the 2026-11-27 owner direction that
  finite acceptance rests on delivered, reviewed implementation with passing automated checks, while live,
  physical-device, signed-in and audible observations transfer to human playtest;
- #4146 §9: "repeat adversarial passes after the last significant art/gameplay rewrite".

Silas asked in session on 2026-11-28 PT to finish the roadmap so the project can close and be ready for human
playtests.

**Verdict: ready for human playtesting.** Every finite build, art, content and QA task is done. Independent round-2
review found no blockers, and every major finding is fixed and merged. No mandatory render is queued. This is not
creative signoff, deployment or publication approval. Public `/play` registration, Arcade promotion and deployment
stay separate explicit approvals.

## 1. Roadmap reconciliation

67 tasks: 65 done, 2 cancelled by Silas:
- t-006: online co-op, dropped 2026-11-19;
- t-034: the standalone thrash-metal music video.

Nothing is ready, waiting or in review. Closing receipts this session:

| task | scope | receipt |
| --- | --- | --- |
| t-044 | main-game standard | Every row has merged work (#5547, #5628, #5670, #5679; achievements t-045). Closed in conductor#8149. |
| t-030 | Gen-2 animation | Every subject in ANIM-BACKLOG-2026-11-24 has a review verdict (177 subjects: 53 kept, 120 rejected takes). 46 idle atlases ship, plus living Act cards for all eight Acts, pilot poses and cut-ins, and moving endings. Final loops this session: kind_robots#6025, #6031, #6037. |
| t-013 | fairness, co-op and campaign QA | Campaign matrix (#5689), fail/retry personas (#5709), every Rainbow verifier gating each PR (#5666), and round-2 independent review with all majors fixed (section 2). |
| t-042 | master reconciliation | This dossier. |
| t-014 | readiness handoff | Lifecycle set to playtest/normal; #4146 flagged and closed. |

29 subjects have no kept loop and show their reviewed shipped stills, per ANIM-BACKLOG-2026-11-24:
- boss phases: b02 phase 1 (phases 2–3 were redrawn under P-12), b03 phase 1, b04 phases 1 and 3, b07 phases 1
  and 3, b09 phase 1, and the phase-2 flagship;
- ships: petal-wing, prism-lance and comet-crown;
- enemies: brood, eel, pistol, relay, salvager, skimmer, spiral, squid and turret;
- guardians: clawstrike, kelp-warden, lantern and urchin;
- harbinger;
- pickups and props: charge, shield, coral-asteroid and lighthouse-lamp.

All but squid and turret failed three or more takes, as the quality contract allows. Squid and turret had one
valid take each, because their first takes rendered from a stale source. With the queue drained, Silas said on
2026-11-28 PT that there was no more relevant work to wait for, so they keep their stills; a retake is optional
polish.

## 2. Independent review, round 2 (after the last art change)

Three fresh read-only sessions reviewed kind_robots `main` at `459343a2`. Silas ruled on 2026-11-23 PT that fresh
sessions count as independent. Their reports are on kind_robots branches `claude/rainbow-review2-{gameplay,story,presentation}`.

| lens | verdict as reviewed | blockers | majors | minors |
| --- | --- | --- | --- | --- |
| gameplay and fairness | not yet ready (5 majors) | 0 | 5 | 4 |
| story, routes and endings | ready | 0 | 2 | 8 |
| art, motion, access and devices | ready | 0 | 4 | 6 |

All 11 majors are fixed and merged:

| id | finding | fix |
| --- | --- | --- |
| G1 | Halo revive keyed to seat 3, not to Solenne's ship | #6041: the revive follows the pilot; tested through real cabinet games with Halo in seats 1, 2 and 4 |
| G2 | co-op keyboard and touch seats had no X or Y | #6041: four-button keyboard maps for P1 and P2; X/Y on tablet pads and 2p phone pads, still off the stage; help says P3 and P4 use gamepads |
| G3 | Petal Wing solo deals about half the others' DPS; Halo dominates | #6041: worst/best ratio for campaign, B04 and B09 went from up to 2.0× to 1.11 / 1.34 / 1.13; Halo is best in no column |
| G4 | the Eclipse Crown is a difficulty wall and a sponge | #6041: novice solo Crown wipes went from 7–17 to 1–5; typical solo fight 172–194 s; still the longest fight |
| G5 | Clawburst phase-1 safe pocket at (20,60) | #6041: the rail shot aims at the pilot's real x; verifyRainbowBossCamping now parks at the left edge |
| R2-1 | stood-down crew credited with defeating the flagship | #6029: `SPARED · B09 Eclipse Crown` |
| R2-2 | Vivi closes 8 of 15 endings; duplicate closing lines | #6029: voices rotate round the crew, the send-off plays last, solo crews get no duplicate |
| R2-01 | HUD legend runs into pilot status | #6034: measured HUD layout (verifyRainbowHudLayout) |
| R2-02 | segment banners overprint, including the allegiance choice | #6034: a single banner queue |
| R2-03 | subtitles about 5 px on an upright phone | #6034: comms mirrored into the 14.4 px aria-live readout |
| R2-04 | co-op ship labels pile up over the play area | #6034: collision-free seat discs; SUPER shown in the HUD |

Minors fixed alongside them: R2-4, R2-5, R2-7, R2-9 and R2-10 (story), and R2-06, R2-10 and the Classic-path 404s
(presentation).

Open minors are recorded in section 4 as playtest notes. None is a material gap under the main-game standard.

## 3. Automated evidence

- On the combined branch (main plus the gameplay fixes, #6041), all 72 `utils/scripts/verifyRainbow*.test.ts` pass. CoopLoad
  was confirmed alone after a parallel-load timing miss.
- On the same branch, TouchLayout, CoopCabinet, SettingsCabinet, Cabinet and Touch Chromium contracts pass.
- CI on each merged PR completed green: "Every Rainbow verifier", TypeScript, cabinet-viewport, the contract shards
  and the Rainbow cabinet browser jobs.
- Campaign (#5689): 16 fresh campaigns across crews 1–4, two seeds and both dock settings reach THE END. Together
  they cover every detour, both sides of every fork, both roads, the stand-down and all three choices, with
  deterministic replay. Median clean campaign 51.6 min.
- After the G3 retune, typical solo campaigns run 50.1–55.4 min.
- Performance: four pilots in Act I's boss fight with real art, engine p50/p95 0.2/0.4 ms and frame pacing 16.7 ms.

## 4. Handoff notes for human playtest (nonblocking)

**Not observed here:** physical devices, DPR 2/3, audible playback, H.264 clip playback inside the canvas, and the
signed-in production build. These move to human playtest under the 2026-11-27 direction.

**Owner call, unchanged:** G6/D8. Unlimited continues with boss-HP carry-over let a parked 4p crew progress. A
phase-reset alternative was tried and reverted in round 1.

**Remaining minors:**
- Gameplay:
  - G7: evade-dash favours Prism and Comet at bosses.
  - G8: a fallen co-op seat waits for a crew wipe.
  - G9: one mortar creature across seven Acts, though shells differ per Act.
  - Comet Crown at power 3 is unmeasured by the personas.
- Story:
  - R2-3: duo/solo call-and-response folds into self-replies in some detours.
  - R2-6: middle seats speak less in 3–4p crews.
  - R2-8: the Act VII echo names Azure's old designation whoever flies.
  - The stood-down scrapbook page shows the restore plate.
- Presentation:
  - R2-05: 1p pads at 844×390 overlap the stage edges by design.
  - R2-07: Classic look is all stills.
  - R2-08: motion coverage is patchy where stills remain.
  - R2-09: some interlude clips barely move.

## 5. Not in scope

Online co-op (cancelled), public `/play` and Arcade cabinet publication, deployment, and any creative signoff.
