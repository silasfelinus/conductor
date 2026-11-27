# Roadmap history — 2026-11-26 PT

Exact replaced YAML blocks, not current instructions. Source commit `f8f7fee43a95086fb030e50323770d822ca1ce10`, blob `212cbd2ae670e4857080babda69a0852506f57f6`.

## goal

<!-- raw:begin goal -->
goal: >-
  Build a full original browser platforming adventure in the Kind Robots
  Arcade in which a randomly generated young adult woman sets out to
  rescue her plumber boyfriend. Eight visually distinct authored worlds
  with at least four substantial stages apiece (32 total), eight world
  bosses, hidden exits and rewards, original memorable foes, responsive
  platforming, layered levels, meaningful powerups and abilities,
  varied traversal and puzzle-combat encounters, checkpoints, secrets,
  introductory sequence, world interludes, ending and credits. Target
  campaign length, level design and depth comparable to Super Mario Bros 3
  and Super Mario World (Gen-2 bar, 2026-10-22), with walkable world maps,
  secret exits, persistent save slots and more original world and enemy variety. Reuse Arcade
  plumbing where appropriate; no runtime LLM or borrowed Nintendo IP.
  Completion requires whole-campaign play, fairness metrics, visual
  acceptance and Silas's hands-on verdict.
<!-- raw:end goal -->

## t-028

<!-- raw:begin t-028 -->
    note: |-
      Silas 2026-11-11 PT, in session: "Our games should all have a base standard of quality ... We want our main games to have 12 plus achievements." Standard: docs/agents/main-game-standard.md; CONTROL.md global overview.

      AUDIT DONE 2026-11-12: projects/save-the-plumber/STANDARD-AUDIT-2026-11-12.md holds the Met/Partial/Missing table, a proposed achievement list with award points, character-fit notes and the three smallest next PRs. Start there.

      Start with the audit table from docs/agents/main-game-standard.md (title screen; settings menu; save/load and persistent progress; 12+ achievements; scrapbook; multiple endings with painted plates; customizable characters; 3+ replay hooks), marking each Met / Partial / Missing with evidence (file, route, live record). Put the table in this note and the first PR. Then close each gap in small CI-tested PRs; queue any needed ending, scrapbook or portrait art in an auto_submit ledger.

      Item 7 (customizable characters) applies "in most cases": if this genre makes it a poor fit, say so in the audit with the reason and leave it for Silas rather than skipping silently.

      Achievements are tracked by their own task; this one covers everything else.

      Added first progress-aware world scrapbook slice: per-world cleared stages, collected Golden Gears and discovered secret exits, derived from the active versioned save. Further settings, endings and art remain.

      2026-11-24 PT intent audit: the increment's PR silasfelinus/kind_robots#5076 merged; the claim from 2026-11-12 was never released and the note says the wider scope is still partial. Returned to ready with the claim cleared so the next worker can pick it up. No scope change.

      Added title settings, shared saved audio preferences, functional still-camera option and high-contrast terrain edges with regression tests. Branch worker/save-the-plumber-t-028-settings-v6m2, head d494f77. Partial main-game standard scope; CI and visual acceptance pending.

      Merged kind_robots#5722 at 964816b after 12/12 exact-head workflows passed. Settings and contrast shipped; remaining main-game standards and visual verification. Return to ready.

      Added title-menu Achievements pane using the shared registered badge browser, internal viewport scrolling and existing back controls. World scrapbook now shows collected gears and secret exits independently of normal clears. Added source wiring and twelve-plus achievement registry regression assertions. Branch worker/save-the-plumber-t-028-scrapbook-z8k2 head b3836722. Partial main-game scope; CI and visual acceptance pending.

      Verified kind_robots#5772 merged at 28bc1c7b; latest head d6110b2b has eight completed successful workflows and branch janitor queued. Achievement browser and independent scrapbook labels merged. Remaining separate New Game/Continue, endings and accessibility. Return to ready.

      Separated title New Game and Continue shortcuts using a scoped cabinet launch intent, safe eligible file selection, no erase in shortcut modes, and retained Files / Endless access. Added runtime regression scenarios for existing-slot isolation, stale Continue and choosing another saved file. Branch worker/save-the-plumber-t-028-newgame-k7d3 head 69c11cba. Partial main-game scope; full CI and rendered viewport acceptance pending.

      Merged kind_robots#5773 at 85a864ba after 14/14 exact-head workflows completed successfully. Separate New Game and Continue delivered; remaining endings, customization and accessibility. Production visual acceptance unverified.

      2026-11-25 PT: three completion endings (base, every Golden Gear, every secret exit) in
      finale and Ending Gallery, monotonic album, regression tests; kind_robots#5832 on
      worker/save-the-plumber-t-028-endings-qk7. Plates finale-clockwork-gift and finale-open-
      tap queued in art-prompts.yaml (auto_submit). Remaining: customization, accessibility,
      rendered gallery screenshots.

      Merged kind_robots#5832 at 5246ebfa after 17/17 exact-head checks passed. Three endings
      live; plates queued. Remaining: customization, accessibility, rendered gallery
      screenshots. Return to ready.

      2026-11-25 PT: per-heroine finale epilogue (8 lines, one per special) under the ending
      copy; roster test asserts unique, named, <=72 chars. Merged kind_robots#5843 at 11b95035
      after 16/16 exact-head checks. Remaining: name entry, boss taunts, accessibility (text
      size/reset), rendered finale + gallery screenshots. Return to ready.

      2026-11-26 PT: Settings pane gains RESTORE DEFAULTS (arcadeStore.resetCabinetSettings:
      sound on, full volume, high contrast off, still camera follows reduced motion;
      keys/saves/initials untouched). Merged kind_robots#5883 at 2e694b0a after all exact-head
      checks passed. Remaining: name entry, boss taunts, text size, rendered finale + gallery
      screenshots. Note: verifySavePlumberFrontPage.test.ts fails on main (console
      ArcadeCabinet assertion), pre-existing. Return to ready.

      2026-11-26 PT: boss taunts. Each of the eight bosses has four original lines (gate
      closes, first two hits, defeat) on a HUD speech plate; verifySavePlumberBossTaunts
      covers data, cueing, fade and drawing. Repaired the stale front-page contract test
      (failing on main) and put both in Arcade Cabinet Browser Contracts on PRs. Merged
      kind_robots#5884 at 782e9dda after 19/19 exact-head checks. Pre-existing on main,
      outside PR CI: verifySavePlumberLevels ('3-4 is cleared losing 4 lives') and
      verifySavePlumberKeys ('the top rung releases the heroine'). Remaining: name entry, text
      size, rendered finale + gallery screenshots. Return to ready.

      2026-11-26 PT: reading options. Settings gains Large text (story, banner, victory,
      finale and boss lines draw 1.25x, shrink to fit, never below normal) and Slow reading
      (story panels and boss plates hold 1.6x). Both persist, reset with RESTORE DEFAULTS and
      reach the game via the cabinet. verifySavePlumberReading added to arcade-engine and
      cabinet-contracts CI. kind_robots#5890. Remaining: name entry, rendered finale + gallery
      screenshots.

      Merged kind_robots#5890 at 5ae6b7bd after 21/21 exact-head checks passed. Reading
      options live. Remaining: name entry, rendered finale + gallery screenshots. Return to
      ready.

      2026-11-26 PT: name entry at heroine select. A new file opens an arcade letter wheel
      prefilled with her roster name (up to 10 letters/hyphens, family filter); the name saves
      on the file and drives story, HUD, file select, finale and the front-page crew card.
      verifySavePlumberNameEntry in arcade-engine and cabinet-contracts CI. kind_robots#5896.
      Remaining: rendered finale + gallery screenshots.

      Merged kind_robots#5896 at 76c1b47d after all 19 exact-head checks passed. Name entry
      live. Remaining: rendered finale + gallery screenshots. Return to ready.

      2026-11-26 PT: repaired the two engine tests red on main. ropeX now scans the whole
      ladder above her, so on 1-2's key ladder she hangs flush to the brick beside the upper
      rungs instead of bumping her head (verifySavePlumberKeys). Boss autopilot hops the
      slam's landing shockwave (3-4: 1 life lost, was 4) and leans into the gale's gust so it
      reaches the recover window (5-4 now clears; this failure was hidden behind 3-4).
      verifySavePlumberLevels passes. kind_robots#5901. Remaining: rendered finale + gallery
      screenshots.

      Merged kind_robots#5901 at 9debf882 after all 17 exact-head checks passed.
      verifySavePlumberKeys and verifySavePlumberLevels green again. Remaining: rendered
      finale + gallery screenshots. Return to ready.
<!-- raw:end t-028 -->

## t-005

<!-- raw:begin t-005 -->
    note: |-
      Patrol/chase/ambush/flyer AI, jump/throw/carry interaction with original enemies, moving platforms, slopes, ladders/lifts, switches, destructibles, three meaningful powerup tracks, damage/knockback, invulnerability frames, lives/continues and checkpoint semantics. Source-verified deterministic collision and softlock tests.
      2026-10-22 Gen-2 scope addition (GEN2-STANDARD.md section 4): grow from three tracks to 5-7 powers with movement consequences (glide or flight, a water or fire suit, a heavy form, carry), an SMW-style reserve item, map-usable item inventory, and an original ride/companion creature that changes traversal. Remaining Gen-1 items (slopes, ladders, carrying enemies and keys) still apply.
      2026-10-16 progress: the three powerup tracks shipped and merged (silasfelinus/kind_robots#3758). Springstep gives a higher jump and a float. Bottled Storm adds a ranged gust that strikes foes, valves, crates and open bosses. Pocket Lift lifts and throws crates, which land as new steps. Water hearts restore a heart, and a hit costs the power before a heart. Also in place from Worlds 1 to 8: patrol, chase, ambush and flyer foes; moving pistons, lifts, rafts and cargo; valve switches; destructible crates; knockback, i-frames, lives and checkpoints; and an autopilot that finishes all 32 stages. Still to build: slopes and ladders, carrying enemies and keys, and dedicated softlock tests.
      2026-11-04 PT adversarial interaction slice: added verifySavePlumberInteractions.test.ts (in test:arcade-engine). It has scripted regressions plus a seeded fuzz of about 674k frames that drops the heroine beside foes, crates, valves, lifts and pickups with random powers across all 32 stages, and a guard that nothing adds height at a closed valve gate. The hunt found and fixed eight interaction defects in savePlumberPreview.ts. A flat moss lantern knocked out by a thrown crate or kicked shell, or cleared when a boss arena locked, left an invisible floor. Glass gulls and gull gliders that stole tokens flew off the stage for good, breaking "catch it and it drops them all". Fleeing gulls are now cornered at the edge, thief gliders patrol edge to edge, and all 10 campaign gliders are proven catchable with no power. An arena lock dropped a stray thief's tokens. Tokens from crates, gusts and thieves could pass 99 without giving a life. A jump pressed while falling into a pit fired as a phantom hop on respawn. A Bottled Storm gust turned valves on other floors through the ground. No closed-gate crossing turned up, so row 0 was left open. An offline powered-reachability probe found no trap pockets in any stage. Remaining: slopes, ladders/climbing and carrying keys or enemies are still unbuilt, so they have no adversarial coverage yet. The Gen-2 powers, reserve item and ride creature are also still to build. The Gears suite (about 6.5 minutes) could snapshot tiles so trap analysis could run in CI.  Merged as kind_robots #4804; back to ready for the remaining scope.

      2026-11-22 PT: Rope ladders and climbing shipped in kind_robots#5615 (1f9ac06). The new | glyph (SOLID_LADDER) works like this: up or down grabs the ladder, including mid-jump. There is no gravity while she holds on, left/right shuffles and A hops off. The top rung is a one-way ledge, and climbing down onto a floor lets go. She hangs flush to a wall beside the ladder, because her 18px hitbox is wider than a 16px tile. The glyph is in the Maker palette. verifySavePlumberLadders.test.ts covers ten scripted cases plus a seeded 40k-frame fuzz and is wired into test:arcade-engine. All 16 save-plumber suites pass, Gears included, and CI was green. Remaining: placing ladders in campaign stages (with Levels/Gears reachability), slopes, carrying keys or enemies, the Gen-2 powers, the reserve item and the ride creature. Back to ready.

      2026-11-23 PT: brass keys and padlocked bolts merged in silasfelinus/kind_robots#5617
      (770bdf1). The new 0 glyph is a brass key. She picks it up by touch and holds one at a
      time, and a hit sends it home. The new [ glyph (SOLID_LOCK) is a padlocked bolt. It is a
      wall until she touches it holding a key, from the side or with a head bump. That spends
      the key and opens the whole connected bolt. A death reloads keys and bolts with the
      stage. Both glyphs are in the Maker palette. verifySavePlumberKeys.test.ts covers 7
      cases plus a seeded 36k-frame fuzz and is wired into test:arcade-engine. CI was green.
      Remaining: placing ladders and keys in campaign stages (with Levels/Gears reachability),
      slopes, carrying enemies, the Gen-2 powers, the reserve item and the ride creature. Back
      to ready.

      Implemented a new authored World 1-2 optional high route: a floor-level brass key at column 35, a seven-rung ladder at column 39, and a padlocked upper passage at column 42. The existing fast lower corridor remains unobstructed. Added real PlumberRun campaign replay assertions for key collection, climb-to-top, bolt unlock, key consumption and lower-route accessibility. Source branch worker/save-the-plumber-t-005-campaign-route-k4v2. Remaining scope includes slopes, carryable enemies, Gen-2 reserve/powers/companion, plus further campaign gadget placements; t-005 is not fully done.

      Verified kind_robots#5633 merged at 4c0f092b. Brass-key ladder route shipped; remaining slopes, carryables and powers. Return to ready.

      Implemented one-way 45-degree walkable ramps, bounded grounded slope adhesion, flat transitions, slope landing, foe traversal, contrast edges, Maker palette and first World 1-1 ramp pair. Added bidirectional sprint replay assertions for height, contact, collision and momentum. App branch worker/save-the-plumber-t-005-slopes-q8m4 head 67d1d06e. Full CI pending; remaining powers, carryables and expanded slope placements remain.

      Merged kind_robots#5806 at 67315e6f after 11/11 latest-head workflows passed, including full contracts and Maker browser coverage. Ramps, slope adhesion, terrain rendering and first campaign hill delivered. Return to ready for carrying enemies, Gen-2 powers, reserve item and companion. Production deployment unverified.

      2026-11-25 PT: SMW-style reserve box merged in kind_robots#5833 (2dcd1163) after all 19
      checks passed. A power picked up while she carries one banks the old one; a hit that
      costs her power drops the reserve from above, drifting toward her for 300 frames; heart
      hits drop nothing, death keeps it, new game/file/Endless clear it; HUD frame under the
      power badge. verifySavePlumberReserve.test.ts (banking, catch, steering, expiry, death,
      seeded fuzz) is in test:arcade-engine. Remaining: carrying enemies, Gen-2 powers (glide,
      suit, heavy form), map-usable inventory, ride companion. Return to ready.

      Added Down + Wrench pickup of stunned regular Rivet Rollers, carried-state isolation, directional throw using existing kicked-roller collision, blocked overhead release, damage return and death cleanup, plus guide and movement regressions. Isolated committed-method tests passed. App branch worker/save-the-plumber-t-005-roller-j8w2 head 282a4762; full CI pending. Partial scope; remaining expanded powers, inventory and ride companion.

      Reviewed and merged kind_robots#5840 at 69d3e262 after all 12 workflows on c6c1b6c6 completed successfully. Carry and throw stunned Rivet Rollers, blocked release and cleanup regressions shipped. Partial scope only; expanded powers, map inventory and ride companion remain. Production deployment unverified.

      Implemented fourth power Sailwing: ordinary jump height, 1.8 px/tick controlled descent and 0.99 neutral air drag while holding jump, instant release, pound compatibility, pickup in Ropeway Home 5-1 and Maker glyph 4, reserve/HUD feedback, tutorial and deterministic bilateral movement/collection regressions. App branch worker/save-the-plumber-t-005-sailwing-h8q3 head 17727401. Full CI pending; painted prop delivery and elemental suits, heavy form, map inventory and ride companion remain. Partial t-005 scope.

      Verified kind_robots#5850 merged at 396726f6 after 12/12 exact-head workflows passed on 880ccb33. Sailwing is the fourth collectible movement power with campaign and Maker coverage. Conductor#8035 merged the private painted prop request; delivery remains unverified. Partial scope; remaining elemental suit, heavy form, inventory and ride companion. Production deployment unverified.

      2026-11-26 PT: Ballast Boots, the fifth power (heavy form), merged in kind_robots#5886
      (87857259) after all 19 exact-head checks passed on 48b4e09f. Headwinds and Admiral
      Gust's gale cannot push her, ice grips like solid ground, and a fall with Down held
      breaks the crates underfoot. Jump is unchanged and the jump planner's wind matches.
      Pickup is in Windmill Platform 5-2, Maker glyph 5. verifySavePlumberBallast.test.ts is
      in test:arcade-engine and ballast joins the MovementReplay fuzz. Remaining: elemental
      suit, map-usable inventory, ride companion, painted Ballast prop. Production deployment
      unverified. Partial scope; return to ready.

      Implemented sixth movement power Tidecoat, with direction-controlled swimming, dive, neutral buoyancy and surface breach, ordinary water lethality without the suit, campaign pickup in Floating Wharves, Maker glyph 6, HUD/reserve indicators and guide. Added custom pool input regression and campaign collectible checks. Extracted committed swimming method passed a dive/ascent probe (108px ascent). Branch worker/save-the-plumber-t-005-tidecoat-n3q8 head 9bad0388; full CI pending. Remaining map inventory, ride companion, painted prop and full campaign water course scope stay open.

      Reviewed and merged kind_robots#5899 at baa1b62c after 18/18 latest-head checks passed
      on fddc1e16. Tidecoat is the sixth movement power: Up/A swims and breaches, Down dives,
      release floats, water stays lethal without the suit; pickup in Tideglass Marina 2-1,
      Maker glyph 6, HUD/reserve labels, guide text and Maker/campaign regressions.
      Conductor#8062 carries the private painted prop request; delivery unverified. Partial
      scope; remaining map-usable inventory, ride companion, dedicated water courses and
      painted Ballast/Tidecoat props. Production deployment unverified. Return to ready.

      Added validated equipped power and reserve save fields, slot isolation, map Y equip/swap with immediate persistence, and a shared cabinet regression suite. App branch worker/save-the-plumber-t-005-inventory-31c9 head 1ae51f90. Partial scope; full CI pending and ride companion, water courses and painted prop delivery remain.

      2026-11-26 PT: kind_robots#5910 merged at 835f9aca. Map inventory and save-slot isolation shipped; 11 implementation workflows and janitor passed. Remaining ride companion, water courses and prop delivery. Partial scope; production deployment unverified.
<!-- raw:end t-005 -->
