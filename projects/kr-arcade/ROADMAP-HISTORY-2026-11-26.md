# Roadmap history — 2026-11-26 PT

Exact replaced YAML blocks, not live directions. Source commit `06538af28ab1f75f8ad7cc206f80d357d382251d`, blob `db87d5d5bc3a7cadac9fe64723c345942aa5dc57`. Existing archive files remain untouched.

## t-076

<!-- raw:begin t-076 -->
    note: |-
      CABINETS.md section 10, Ribbon Riders (Tron light cycles riff), slice 3 of 4: The last two fairgrounds and the endings. The upgrade is "The Lantern Festival Circuit". Spec: projects/kr-arcade/depth-pass/CABINETS.md -- read the game's section first; this slice's scope is item 3 under its '#### Slices', and 'Rules for every slice' at the top applies. Code: kind_robots utils/arcade/games/ (registry slug ribbon-riders). Silas, 2026-10-11: "I need an assessment done of the other arcade games. I want the same level of quality improvements, they should not just be thin veneers of the old games. But newer, better, even more awesome."

      Added ten authored late-circuit arenas and four rival steering profiles on worker/kr-arcade-t-076-fairgrounds-f4c9. Partial slice: bespoke marshals, hazards, ending and Encore still outstanding. Verify CI before merge.

      2026-11-22 PT: Kind Robots PR #5566 merged after all latest-head substantive checks completed green. Partial campaign slice delivered; remaining documented scope stays ready.

      2026-11-23 PT: implemented six-second comet trail expiry and champion-unlocked mirrored Encore with compatible saves on worker/kr-arcade-t-076-comet-encore-9d3f6b. Partial slice; Rainbow Spool and remaining hazards still outstanding. CI pending.

      PR kind_robots#5694 merged at fe3406648447fdfcdd4189adc26315327dfab57b; eight final-head workflows passed. Comet trail expiry and Encore shipped. Rainbow Spool, remaining hazards and campaign QA remain.
<!-- raw:end t-076 -->

## t-118

<!-- raw:begin t-118 -->
    note: >-
      CABINETS.md section 20, Petal Post (Paperboy riff), slice 1 of 4: Street engine and Primrose Lane. The upgrade is "A Season in Blossom Valley". Spec: projects/kr-arcade/depth-pass/CABINETS.md -- read the game's section first; this slice's scope is item 1 under its '#### Slices', and 'Rules for every slice' at the top applies. Code: kind_robots utils/arcade/games/ (registry slug petal-post). Silas, 2026-10-11: "I need an assessment done of the other arcade games. I want the same level of quality improvements, they should not just be thin veneers of the old games. But newer, better, even more awesome."

      Implemented persistent house bloom, two-gift neighbour signups, wilting before cancellation, and visible garden growth in Petal Post. Further Primrose Lane route work remains.

      PR silasfelinus/kind_robots#5676 merged at 28514e531cdcdd2f4e0099e7e63b917a95d2848d; nine CI workflows passed. Bloom persistence, wilting and flower-gift subscription recruitment shipped. Remaining authored Primrose Lane encounters, two-sided street layout, day/week structure and gameplay tests remain.

      [Earlier history (1,126 chars) archived verbatim to projects/kr-arcade/T118-HISTORY.md -- read it there only when you need a specific past cycle. Append new cycles below, one short paragraph each.]

      Added stable authored crossings, side roads, shops and park landmarks with weekday unlocks and guaranteed shop refills. Park Loop has two ramps, eight timed targets including two airborne rings, supply reset, jump-dependent parcel range, gold course stamp and Gazette recap. Input-level regression coverage added. Branch worker/kr-arcade-t118-park-93ac; pending CI and rendered playtest. No release or deploy initiated.

      PR kind_robots#5690 squash-merged at e62e1e464824e03b35c35bd05bb2b599cc58420c. All eight workflows returned for exact head 8c2655954593bb47164e0e58880c47b6c81a5b75 completed successfully; job results include TypeScript, four contract shards and aggregate, Chromium arcade and Rainbow browser contracts, formatting, layout, architecture and migration parity. Park Loop, ramp throws, seven authored landmarks and shop refills shipped. Keep ready for remaining authored segment/slope audit, deterministic week and pilot evidence, and rendered device QA. No deployment or human playtest claimed.
<!-- raw:end t-118 -->

## t-155

<!-- raw:begin t-155 -->
    note: >-
      Silas, 2026-10-19, verbatim: "generating better audio should absolutely not require human approval, fyi". The money gate is lifted: agents queue ACE-Step renders themselves through /api/art/enqueue (enqueueArcadeSoundtrack.ts, enqueueRainbowScore.ts; Rainbow's 21 score cues went in as ArtJobs #40796-#40816 the same day while the render box's queue was idle). Remaining agent work: drop the per-cue approval and ARCADE_AUDIO_JOBS_ENABLED gates from POST /api/arcade/audio-jobs (or retire it for the direct path), then ingest renders as below. [...]

      [Earlier history (1,485 chars) archived verbatim to projects/kr-arcade/T155-HISTORY.md -- read it there only when you need a specific past cycle. Append new cycles below, one short paragraph each.]

      Removed the obsolete per-cue approval, environment flag and relay-readiness gates from the admin audio enqueue route. The PR retains job deduplication and uses the existing ACE-Step ArtJob pipeline. Render ingestion and audible verification remain open.

      Reviewer (scheduled, 2026-11-23 PT): kind_robots#5663 merged on all-green CI (989b6f37).
      The admin audio enqueue now submits deduplicated ACE-Step jobs without the retired
      approval, env-flag and relay gates, and it stays admin-guarded. Ingesting renders, an
      audible cabinet check and cue activation remain, so t-155 goes back to ready. The new
      path only works on production after a Force Update.
<!-- raw:end t-155 -->
