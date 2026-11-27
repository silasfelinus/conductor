# Roadmap history — 2026-11-26 PT

Exact replaced YAML blocks, not live direction. Source commit `06538af28ab1f75f8ad7cc206f80d357d382251d`, blob `f913ecc052120b5c4b6bc3c2cd1a3e4483543985`.

## goal

<!-- raw:begin goal -->
goal: >
  REOPENED FOR THE GAME HALF, 2026-09-11, after Silas played it: "we still have ruler is done at 85% and 21/22 done on projects, which is ABSURD". He was right, and the cause was structural rather than anyone overclaiming. FULL-GAME-GAP-AUDIT.md (2026-08-26) recommended two new milestones -- m4 full-game vertical slice and m5 art production. m5 was created; m4 was deliberately not filed, with a roadmap comment explaining the sequencing. The effect was that the whole game half sat outside the denominator, so 21 of 22 tasks done described a PoC while reporting a finished product. m4 is filed now (t-023..t-032) and carries Silas's specific 2026-09-11 findings: no ruler portraits, a text-menu fishing panel where a timing minigame belongs, a scrolled document instead of one screen, conductor scaffold chrome shown to players, no catch art, no advisor or opening, no shop or treasures, no visible kingdom or populace, and a 15-fish roster surfaced to the player as if it were the catalog. USE THE AUDIT'S COMPLETION LANGUAGE: "PoC complete" is true; "full game mostly developed" is not, and must not be reported until t-032 passes. A full offline-playable slideshow fishing/kingdom-management game. The PROOF OF
  CONCEPT half is complete (m1–m3, 2026-08-18): fish at the lake while kingdom
  event-cards prompt choices that move kingdom-health sliders and visibly
  recomposite the landscape, with multiple named save slots, shipped as an
  installable PWA. The GAME half is not — see FULL-GAME-GAP-AUDIT.md (2026-08-26)
  for what "PoC complete" does and does not mean. Reserve "finished" for the
  product, not the task count.
<!-- raw:end goal -->

## t-061

<!-- raw:begin t-061 -->
  note: |-
    After kind_robots#4828 and #4834 reach kindrobots.org (Force Update), screenshot every screen at 390, 820 and 1440 widths: title, coronation, crier, lake idle/fight/reveal, court petition/ending, map, gear, fishopedia and chronicle. Confirm the art loads through the /images media fallback, and fix spills or crushed panels. Repeat after t-054's restyle, and attach the shots for Silas's t-032 acceptance.

    Added the canonical /play/ruler-hooked route to the production responsive audit, with guest-only title/settings/scrapbook/achievements/coronation/crier/lake/fishing navigation and per-stage rendered geometry and screenshots at phone, tablet portrait, tablet landscape and desktop. App branch worker/ruler-hooked-t061-rendered-audit-8a2e at 6d385a50. Local HTTPS attempt failed DNS resolution; no rendered pass or completed art inspection claimed. Remaining catch/court/finale/map/gear/fishopedia/chronicle device coverage is not done. CI and actual scheduled live audit required.

    Kind Robots #5862 merged cfc7cdec; six exact-head PR workflows passed including Contract Tests 45731351686 and Layout Contract 45731351690, branch janitor 45734187832 passed. Instrumentation is not a rendered acceptance pass; remaining screen coverage and actual self-hosted screenshots are required.
<!-- raw:end t-061 -->
