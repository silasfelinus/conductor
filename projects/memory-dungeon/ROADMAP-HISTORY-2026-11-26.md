# Roadmap history — 2026-11-26 PT

Exact replaced YAML blocks, not live directions. Source commit `06538af28ab1f75f8ad7cc206f80d357d382251d`, blob `2fc062eacf846b3706d9256e51e12fe650044759`. Existing archive files remain untouched.

## goal

<!-- raw:begin goal -->
goal: >-
  Evolve the existing Kind Robots Memory Dungeon at /play/memory into a
  replayable art-led narrative roguelite RPG with persistent explored overworld,
  geographically anchored procedural dungeons and Edgeworlds, character creation,
  independently chosen difficulty and depth, an authored intro, seeded
  procedural encounter/monster/treasure piles, spatial weapon shapes that
  change how memory-matching combat works, fair logic minigames and riddles,
  consequential choices, recurrent characters, recruitable and evolving
  companions, run-specific upgrades, save/resume and cross-run Chronicle
  discoveries. Preserve Classic Match and the existing game route/links.
  Finish only after adversarial seeded playtests, meaningful endings,
  balance/accessibility QA and Silas's subjective gameplay verdict.
<!-- raw:end goal -->

## t-023

<!-- raw:begin t-023 -->
    note: |-
      2026-11-11 PT remaining: Audit 24 playable-world beats, retired archival beats and spoiler gates; do not delete older photos. Evidence: RESET-TASK-EVIDENCE-AUDIT-2026-11-10.md (t-023 row).
      Author 32 fixed collectible photo beats, two per world, with out-of-order journal reconciliation, once-only claims, proper Earth chronology, and meaningful hero reactions. World 1 photos occur at 2,5 (dismissal) and 8,6 (friend's humiliation). Morrow later builds authentic work, friendship and romance; do not unmistakably reveal their children before World 16.
      Prepared the independent Earth Chronicle source and playable recovery slice: 32 authored Earth-side photo beats, two for each of 16 internal experiences; four are collectible now across original and Dark Briar by scene decisions, later photos cannot appear before their experiences are implemented. Unique response choices persist across runs, legacy saves backfill earned entries, chronological ordering is independent of discovery order, and no future world/photo totals are exposed in the UI. Added responsive photo-led Chronicle console with missing-art fallback, plus automated contract tests. Kind Robots review PR follows; do not claim later 28 photos playable.
      PR kind_robots#4199 merged at ff450bff51bcbc74cd4b2c8e8af81279bdd90cbb with all 14 CI workflows green. The independent Earth Chronicle now has 32 authored photo beats and persistent player interpretations, with only the 4 original/mirrored Briar photos collectible. Earlier saves backfill their discoveries, ordering stays chronological across repeated expeditions, future photos remain hidden without playable scene hooks, and the game does not expose its internal realm count. Return to READY for implementing the remaining 28 photo pickups in future realities, completing rendered-image QA and the final cross-reality ethical endings. No human gate or final art acceptance.
      Earth Chronicle photo-continuity increment: original and mirrored Briar photo backfills now require real authored scene decisions, rejecting forged choices. Dark Briar's Knight at the Wrong Bridge now physically reveals the previously disconnected Unsent Reply photograph through both outcomes. Four-photo narrative/choice and 24-order save/replay regression cases added; Kind Robots focused PR and exact-head CI verification follow. Future 28 photos, delivered artwork and final ethical ending acceptance remain unfinished.
      2026-10-27 PT: Merged Kind Robots PR #4334 at 78dfb30756768aacb0f3a842df6052c5855431d5 after all 18 exact-head checks and 13 workflows passed on 7703c413143b3d0008244cc1e04bbb50797bdc94. [...]
      [Earlier history (6,350 chars) archived verbatim to projects/memory-dungeon/T023-HISTORY.md -- read it there only when you need a specific past cycle. Append new cycles below, one short paragraph each.]
      Scoped e07 Earth Chronicle pickup: Hoshimori site 2,3 earns the first authored photo after a replay-validated decision and the e06 campaign gate; the second e07 photo and all unbuilt realities remain hidden. Shared Chronicle opens from the Hoshimori console. Five-file Kind Robots PR and exact-head CI follow.
      2026-10-30 4:00 AM PT: Merged Kind Robots PR #4482 (squash 6388cf362e43e5e45623ed9ca1928ffa5dab737b) after 21/21 exact-head checks and all 16 Actions workflows passed on b6edf50a30169d54fb0297da72b295d4de42790c. Hoshimori e07 site 2,3 now earns earth-13 once through replay-validated choice and e06 campaign gate, preserving chronology and immutable responses. The shared Chronicle is reachable from the Hoshimori console. New tests cover both legal choices, forged choices, restoration, once-only claims, ordering and future photo exclusion. Master issue #4136 comment 6521059791. No new ArtJobs, deployment or rendered acceptance. Return READY for e07 7,5 second photo, remaining 27 future pickups, delivered art, full endings and device QA. Not For Human Gate.
      Prepared a four-site Hoshimori mountain road to the fixed e07 7,5 photograph, two authored choices at each new site, and replay-validated earth-14 Chronicle pickup. Kind Robots focused PR and exact-head CI follow. No ArtJobs or deployment.
      2026-10-30 5:00 AM PT: Merged Kind Robots PR #4486 (squash 3a08044dcfd7b7d1a472b05b79e2ae513f99750d) after all 16 exact-head workflows passed on 0acc702cf5601bdb8d37ff0d36812acb54938518. Added four connected e07 mountain sites (20/64 total, 40 choice outcomes) and earned earth-14 at fixed 7,5 through replay-validated choices, once-only chronological Chronicle recovery and e06 gate. Contract Tests #41051280666 (four shards), TypeScript #41051280608, formatting #41051280827, layout #41051280611 and Memory browser #41051280760 succeeded. Master issue #4136 comment 6522185097. No new ArtJobs or deployment. Return READY: remaining 26 future Earth pickups, delivered image verification, campaign endings and rendered device QA are unfinished; Hoshimori still needs 44 sites, 33 Oven rooms and 30+2 gallery. Not For Human Gate.
      Scoped e08 Earth Chronicle increment: first night-procession photo at fixed 1,4 now follows either replay-validated authored decision after the e07 campaign gate. Existing e07 photos, Earth chronology, immutable reactions and old saves remain. e08 6,7 photo and all later unbuilt scenes remain spoiler-locked. Focused Kind Robots PR and exact-head CI pending; no ArtJobs or deployment.
      2026-11-04 PT cleanup pass: stale review with an expired claim; the recorded slice landed (or was superseded) and the note itself lists remaining scope, so back to ready for the next slice rather than done.

      2026-11-06 PT: Confirmed e08 earth-15 at 1,4 has replay-validated choice and chronology coverage; earth-16 at 6,7 remains intentionally spoiler-locked because its authored scene is not present. No implementation shipped this pass; retain READY for a playable 6,7 route and actual image delivery verification.

      Added e08 5,7 to 6,7 authored route, replay-gated earth-16 pickup and seeded southern-route forgery tests; Kind Robots PR/CI pending. Further photos and art delivery remain.

      2026-11-06 PT: PR kind_robots#4861 merged (23fbe3ed) after all eight exact-head checks passed on a63e8257. e08 Hoshimori 5,7 and 6,7 authored, earth-16 now recoverable with replay and forged-choice tests. Remaining Chronicle pickup routes, delivered art and ending validation. No ArtJobs or deployment.

      Added two authored e08 crossings at 5,5 and 6,5 with distinct choices and replay-safe flags; expanded site-count validator and regression assertions to 48. Kind Robots PR pending exact-head CI. Remaining Hoshimori sites, Chronicle photos and art not complete.

      2026-11-20 PT: stale claim/review released to ready (Silas, in session: "you are likely
      the only agent working on this project currently, so any claimed roadmap items are
      likely stale"). Playtest-ready means the complete twelve-world game; see
      ASSESSMENT-2026-11-20.md for this task's gap.
<!-- raw:end t-023 -->

## t-037

<!-- raw:begin t-037 -->
    note: |-
      2026-11-11 PT remaining: Prove bounded replay-backed cross-world outcomes and restoration. Evidence: RESET-TASK-EVIDENCE-AUDIT-2026-11-10.md (t-037 row). Preserve all World One choices in the Chronicle, but promote only compact resolution, relationship, portable discovery and cross-realm collaboration facts into future-world conditions. Give those effects real dialogue, route, reward or ending changes; retire paid debts, prevent old flags softlocking the main path, and test incompatible decisions. Reuse one interpreter and published story contracts instead of enumerating every 16-realm choice permutation.
      First-two-reality adversarial slice: initial minefield exit was guaranteed safe and immediately awarded victory; now requires full safe-floor clearance. Added recovery from exhausted 600-move logs, dropped no-op actions and blocked double-purchase of an unchanged lantern hint. Added 24 greedy/expert seed checks, 16 cross-map seal combination checks and 24 first-two-reality Earth photo collection order checks. Source-backed findings and remaining device, narrative and art-delivery gaps documented in Kind Robots. PR review underway; do not close full t-037 cross-realm ledger work or t-036 full-world QA.
      Early adversarial first-two-world gameplay pass merged as Kind Robots PR #4202, squash b0b40d940b401bf125dbd026ecba79bb812285bf, all fourteen required PR workflows green. Repaired P0 instant-win minefield exit (exit is intentionally safe), P1 600-move save softlock/repeated no-op logging (now restartable) and P2 duplicate lantern hint charges. Added 24 seed-scoped greedy/expert archive runs, 16 reflected/original seal inspection combinations and 24 ordered cross-reality photo collections plus a reproducible findings/limitations report. Master issue #4136 updated with commit and precise scope. Return t-037 to READY because full bounded cross-realm consequence ledger is not complete. Keep t-036 full human/device/art-dependent adversarial acceptance blocked until its separate prerequisites; do not imply browser image review or final release.
      Second adversarial pass on the 36-room mirrored House uncovered skip-through progression: rooms without memory/logic mini-challenges let players advance into unvisited rooms without making their authored decisions. Updated darkHouseExits to require both solved challenges and committed consequences before first-entry advancement, preserving visited retreat and old saves. [...]
      [Earlier history (9,572 chars) archived verbatim to projects/memory-dungeon/T037-HISTORY.md -- read it there only when you need a specific past cycle. Append new cycles below, one short paragraph each.]
      Scoped two-reality courier resource consequence implemented on a focused Kind Robots branch: sheltering the mirrored courier earns a one-time lantern or wildflower based on the actual original courier choice. Invalid and missing history earn nothing. PR and exact-head CI pending; full cross-realm ledger remains unfinished.
      2026-10-27 PT: Merged Kind Robots PR #4302 at 67f4c79fa255581ba366887896bf14ed75fef438 after all 18 exact-head checks and 13 Actions workflows passed on ed3883f3e86b82048a0113edcdcc0e6a84e212dc (Contract Tests #40535382165, TypeScript #40535382102, Prettier #40535382281). Sheltering the mirrored courier at 3,4 now awards one once-only resource determined by the actual original 2,4 choice: lend earns a wildflower, copy earns a lantern. Missing/invalid choices and alternate mirrored decision award nothing; authored callback names the earned resource. Three-file diff; no ArtJobs or deployment. Master issue #4136 updated. Return READY for deeper later-reality resource, route, and relationship consequences; browser/device and art acceptance remain outstanding. Not For Human Gate.
      Scoped Pip/borrowed-voice cross-reality consequence: four source-validated traveler responses, corrected invented original history, persisted mirrored choices and distinct House callbacks. Kind Robots worker branch prepared; PR CI pending. No new ArtJobs or deployment; later-world ledger, rendered visual QA and campaign remain open.
      2026-10-27 10:58 AM PT: Kind Robots PR #4307 merged at 7f5b1578c9a201cb731a1f3d8ba4652e6413ffa3 after all 18 exact-head checks and 13 workflows passed on 45c3d31d32516401281d69bd82606a8ff26ee5ed (Contract Tests #40554278280, TypeScript #40554278258, formatting #40554278484). Corrected fabricated original history at Dark Briar 3,5 and authored four Pip/borrowed-voice traveler resolutions from real original and mirrored choices, with distinct earned House epilogues and save/invalid-choice tests. Master issue #4136 comment 6449671345 documents evidence. No ArtJobs, deploy or visual acceptance. Return READY: later-world consequence hooks, art and browser/device QA remain. Not For Human Gate.
      Scoped royal-sisters consequence increment: original Briar escort/question and mirrored Scylla/Char testimony now yield four distinct earned scene resolutions and later House epilogue callbacks. Corrected the mirrored lantern callback to the actual original question. Kind Robots focused PR and exact-head CI pending; full later-realm ledger remains unfinished.
      2026-11-04 PT cleanup pass: stale review with an expired claim; the recorded slice landed (or was superseded) and the note itself lists remaining scope, so back to ready for the next slice rather than done.

      Added six serialized original/mirrored House worldframe restoration regressions in Kind Robots; CI and PR review pending. Broader consequence-ledger acceptance remains open.

      2026-11-15 PT: Merged focused six-worldframe serialized restoration regression PR #5205 (squash c1e56e93); six exact-head workflows green, including Contract Tests. Full bounded cross-realm ledger and adversarial acceptance remain open; return to ready for next scoped increment.

      Added six adversarial forged original/mirrored House ending combinations to the existing first-two-world consequence contract. Tests assert restored labels remain unset and physical aftermath cannot be manufactured. Focused Kind Robots PR pending exact-head CI; broader ledger remains unfinished.

      2026-11-20 PT: stale claim/review released to ready (Silas, in session: "you are likely
      the only agent working on this project currently, so any claimed roadmap items are
      likely stale"). Playtest-ready means the complete twelve-world game; see
      ASSESSMENT-2026-11-20.md for this task's gap.
<!-- raw:end t-037 -->
