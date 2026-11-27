# Roadmap history — 2026-11-26 PT

Exact source YAML blocks moved from the live roadmap. These are historical, not current directives. Original source commit: `4f702ecc057f98604605a9b2bd01cee2c8aa4984`; blob `841d42f6976eabab70ce1191d305f52950f567b6`. No statuses or evidence were removed. Each block is delimited for exact recovery.

## goal

<!-- raw:begin goal -->
goal: >-
  Ship a lavish, complete original side-scrolling bullet-shmup campaign in the
  Kind Robots Arcade: pink and pastel-rainbow future-tech oceanic space opera,
  1–4 simultaneous local browser players (no online co-op), fair readable
  but demanding combat, at least eight authored multi-phase stages, distinct
  branching routes, eight end-stage bosses and a final boss, sea-life-inspired
  enemy fleet, varied upgradable weapons, shields, pickups, limited supers,
  foreground/midground/background parallax, animation, cinematic opening,
  interludes, multiple endings, and save/continue/leaderboard integration.
  No online rooms, matchmaking, network sync, or multiplayer servers. No runtime LLM.
  Accept only after measured end-to-end gameplay, local 1/2/3/4
  player soak, art and accessibility review, and Silas's hands-on verdict.
<!-- raw:end goal -->

## t-042

<!-- raw:begin t-042 -->
    note: >-
      FROM GITHUB ISSUE silasfelinus/kind_robots#4146 (https://github.com/silasfelinus/kind_robots/issues/4146), opened by @silasfelinus on 2026-10-25. Imported by scripts/sync_github_issues.py. Reference the canonical roadmap in implementation PRs with `Refs silasfelinus/kind_robots#4146`, never `Closes`. Keep #4146 open throughout finite build, art and QA work. Only the verified playtest handoff workflow may prefix `[FLAGGED FOR HUMAN TESTING]` and close the single master issue after Conductor lifecycle, priority, evidence and genuine `needs-human` subjective-acceptance gate are confirmed; closing the issue is not human approval or permission to publish.

      # Rainbow Bullet Hell Space Princess | Master production, adversarial testing and final-approval roadmap

      **Status: IN DEVELOPMENT. This is a standing production/completion issue, NOT a request for Silas's approval yet.**

      **Sources of truth:** [Conductor project roadmap](https://github.com/silasfelinus/conductor/blob/main/projects/rainbow-bullet-hell-space-princess/roadmap.yaml), [CONTROL.md](https://github.com/silasfelinus/conductor/blob/main/CONTROL.md), [Motherland plot spine](https://github.com/silasfelinus/conductor/blob/main/projects/rainbow-bullet-hell-space-princess/PLOT-MOTHERLAND.md), [C.A.T.S. art direction](https://github.com/silasfelinus/conductor/blob/main/projects/rainbow-bullet-hell-space-princess/DOODLE-DIRECTION.md), [Gen-2 Arcade quality bar](https://github.com/silasfelinus/conductor/blob/main/projects/kr-arcade/GEN2-STANDARD.md), and [cross-Arcade display quality issue #4062](https://github.com/silasfelinus/kind_robots/issues/4062). The issue coordinates the *whole playable-game finish line* across existing and future scoped PRs, without resetting or duplicating completed Conductor work. Reconcile conflicts in favor of the latest dated, explicit Silas direction.

      ## Mission and definition of done

      Deliver a complete, original, lavish **2D side-scrolling space-shooter campaign** that can credibly stand beside the *design depth and player delight* of classic Gradius, Darius, R-Type and Star Fox 64, without copying IP. It must feel like a polished console game rather than a survival-wave web demo: substantial authored stages, memorable animated foes, four truly different princess starfighters, fluid controls, discovery, persistent progress, consequential plot branches, dramatic audiovisual storytelling, and excellent 1–4-player play.

      The current Conductor roadmap calls eight main Acts and some engine tasks done, while **online co-op, Gen-2 save/map progression and alternate Acts, painted art and full animation, narrative/cinematics and adversarial acceptance are not all finished**. Task status ≠ quality acceptance. Audit the actual *main-branch build* and close gaps with evidence. [...]

      [Earlier history (4,123 chars) archived verbatim to projects/rainbow-bullet-hell-space-princess/T042-HISTORY.md -- read it there only when you need a specific past cycle. Append new cycles below, one short paragraph each.]

      2026-11-26 PT P-01 batch 5: only b02-phase1-v3 had finished; motion 0.81 (third static
      take), so b02-phase1 stays a still. 46 loops still rendering (incl. b03/b08 v3). Next:
      review those, then P-03 ending clips. Partial master-roadmap scope; return to ready.

      2026-11-26 PT P-01/P-03 batch 6: reviewed 5 finished renders, all rejected. flagship
      (1.58), flagship-phase2 (1.94), kelp-frond (0.69) and charge (0.70) idle loops sit under
      the 2.7 motion floor; the loyal-sever ending clip has a morphing jet and ghosted jets in
      its held last frame. -v2 retakes appended to ANIM-BACKLOG for auto-submit (verdicts in
      this conductor PR). loyal-sever is the last unshipped P-03 clip. Next: review the
      retakes and ~35 pending loops. Partial master-roadmap scope; return to ready.

      2026-11-26 PT P-01 batch 7: only the power and shield pickup loops had finished; both
      rejected under the 2.7 motion floor (1.52 and 1.39, facets/emblem barely move). -v2
      retakes with stronger hop/pulse prompts appended to ANIM-BACKLOG for auto-submit. ~38
      loops still pending plus the loyal-sever ending retake. Partial master-roadmap scope;
      return to ready.

      2026-11-26 PT P-01 batch 8: two loops had finished. Shipped idle-flagship-v2 (motion
      8.96, phase 1 only; phase 2 stays the battered still) in kind_robots#5903, routing the
      flagship draw through drawSpriteOrFrame so it actually animates. Rejected comet-cadet-
      pod (0.80, static); -v2 retake appended for auto-submit. ~38 loops still pending plus
      the loyal-sever ending retake. Partial master-roadmap scope; return to ready.

      2026-11-26 PT P-01 batch 9: three loops had finished, all rejected. flagship-phase2-v2
      (craters wander across the hull, lime smoke flecks past the outline), kelp-frond-v2
      (static, 0.71) and charge-v2 (loses the still's tilt and pink rim, green fringe). -v3
      retakes appended to ANIM-BACKLOG for auto-submit; a third failure leaves each a still.
      ~35 loops pending plus the loyal-sever ending retake. Partial master-roadmap scope;
      return to ready.

      2026-11-26 PT P-01/P-03 batch 10: three renders had finished. Kept the loyal-sever
      ending retake (jets crisp and opaque through the last frame), shipped in
      kind_robots#5904, so all six P-03 ending clips now have motion. Rejected power-v2 (melts
      into a blob mid-loop) and shield-v2 (static, 0.30). -v3 retakes appended to ANIM-BACKLOG
      for auto-submit; a third failure leaves each a still. ~37 loops still pending. Partial
      master-roadmap scope; return to ready.

      2026-11-26 PT P-01 batch 11: two loops had finished. Shipped comet-cadet-pod-v2 (motion
      14.75, nose-up/nose-down rock with bouncing cadets) in kind_robots#5905; the X2 route
      objective now animates. Rejected flagship-phase2-v3 (static, 0.84), the third failed
      take, so the battered phase 2 stays a still. ~36 loops pending plus kelp-
      frond/charge/power/shield v3 retakes. Partial master-roadmap scope; return to ready.

      2026-11-26 PT P-01 batch 12: five loops had finished. Shipped kelp-frond-v3 (motion
      7.63, the hazard strand sways) and power-v3 (6.11, the diamond bobs and tilts while
      staying solid) in kind_robots#5906. Rejected charge-v3 (blurry, rim melts) and shield-v3
      (swirl morphs into blobs); those were third takes, so charge and shield stay stills.
      Rejected coral-choir-pod (static, 0.93); -v2 retake appended for auto-submit. ~32 loops
      still pending. Partial master-roadmap scope; return to ready.

      2026-11-26 PT P-01 batch 13: two loops had finished, both rejected. lighthouse-lamp is
      static (0.69, the beam never sweeps) and brood-v2 melts into a flat blurry blob mid-
      loop, losing its highlights and crisp points. Retakes lighthouse-lamp-v2 and brood-v3
      (the brood's last take) appended to ANIM-BACKLOG for auto-submit. ~31 loops still
      pending. Partial master-roadmap scope; return to ready.

      2026-11-26 PT P-01 batch 14: two loops had finished, both rejected. bulwark-v2 only
      droops its eyelid (1.10, the body never bobs) and eel-v2 is static (1.02, no coil or
      ripple). Retakes bulwark-v3 and eel-v3 (each the last take) appended to ANIM-BACKLOG for
      auto-submit. ~29 loops still pending. Partial master-roadmap scope; return to ready.
<!-- raw:end t-042 -->
