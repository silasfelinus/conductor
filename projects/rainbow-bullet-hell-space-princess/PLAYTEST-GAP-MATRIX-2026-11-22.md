# Rainbow Bullet Hell Space Princess: playtest-readiness gap matrix (2026-11-22 PT)

Baseline: kind_robots main `8876e627` (#5614 merged about 01:29Z; the audit read `1f9ac06b` + #5614). DoD is issue #4146 §1–10. Online co-op is cancelled; t-014 is the human gate. The 8 assets from t-059 are counted as in flight.

> **Not an approval or cancellation record.** Task cancellations (e.g. t-034, superseded by t-038) are Silas's call; section 3 lists recommendations only. Refresh this matrix when a numbered item lands rather than starting a second one.

Key: **[V]** = verified in code, ledger or API. **[I]** = inference.
Shorthand: `E` = `utils/arcade/games/rainbowPrincessPreview.ts`, `GA` = `rainbowGameArt.ts`, `T/` = `utils/scripts/`.

## 1. Matrix

| Area | Status | Evidence | Remaining agent work | Task |
|---|---|---|---|---|
| Canon/scope | Partial | DOGS removed (t-039 done). The opening ledger excludes DOGs (`OPENING-CLIPS-2-DOODLE.yaml:2`). This matrix is the first one. | Keep this matrix current; reconcile the stale claims in §3. | t-042 |
| 8 main Acts + Crown | Met (code) | A01–A09 directors each have OPEN/TURN/AFTER [V]. Per-Act verifiers and workflows exist. | Replay evidence from a fresh start only; see QA row. | t-013 |
| Alt Acts X1–X4 | Partial | Playable on main: X1 #5557/#5578, X2 #5560, X3 #5535, X4 `rainbowMirrorShoal.ts`, clears #5614 [V]. On main, alt guardians fall back to the scaled scout sprite: `rainbowGuardianSprite` lists only 8 main kinds (`GA:263-279`) [V]. | Land t-059 (5 guardians, 3 pods/lamp). Ship hazards kelp-sweep-frond 278928 and coral-asteroid 278622 (DONE). Author/render the X3 hazard, X4 pickup and X4 hazard (audit script: 3 MISSING) [V], plus Armory Siren and Lantern Matriarch art (no ledger entry) [V]. Ship alt parallax planes (GEN2-ROUND-2, MIRROR-SHOAL-X4 all DONE, none in `public/`) [V]. | t-059, t-028 |
| Route map | Partial | Seas map nodes, replay and detour launch (#5443, #5602, #5607, #5611) [V]. `freedChoir`/`cadetsHome` are stored but no dialogue module reads them [V]. `liltMemoryRecovered`, `crownEcho` and route stingers (First Rule / Whole Fleet / Kept Memory / Open Sea, ROUTE-MAP §6) are absent from code [V]. Route-map art rb2-route-map is DONE but unshipped [V]. | Build the ROUTE-MAP §5 scene variants and the §6 stingers, then ship the map art. | t-027, t-012 |
| Save slots/Hangar | Mostly met | `RAINBOW_SLOT_COUNT = 3` (`rainbowSaveSlots.ts:4`), Hangar #5423, damaged-slot recovery #5581, checkpoint resume (t-031) [V]. | Add `verifyRainbowSaveBytes.test.ts` and `verifyRainbowSeasLogbook.test.ts` to CI (no workflow references them) [V]. Ship Hangar art (rb2-hangar). Add an "erase flight log" control. | NEW, t-027 |
| 3 beats per Act | Met | Scene ids A01–A09 OPEN/TURN/AFTER plus X1–X4 (`E:1060-1085`). Assertion at `T/verifyRainbowStoryScript.test.ts:245`. | None. | — |
| 4 ships/loadouts | Mostly met | t-010 and t-017 done; 4 ship sprites ship. | Mixed-roster balance trials against every boss and branch. | t-013 |
| Pilot art + atlases | Partial | Portraits, comms, cut-ins and ships ×4 ship (CAST-MANIFEST); cut-in motion #5544 [V]. The doodle set lacks the Solenne portrait and comms [V]. No hangar, hit, victory or defeat poses and no pilot atlases exist in `public/` [V]. | Render, review and ship the pose set plus atlases per pilot; fill the doodle Solenne gaps. | t-030 |
| Enemy ecology/motion | Partial | WORLD-BIBLE "Enemy behavior atlas". `verifyRainbowCraftVariety` covers Acts I–III (t-033). Animated shots (t-032). Enemies are one still each, moved by a procedural bob/bank/stretch (`rainbowSwimMotion.ts`); no frame atlases [V]. | Idle, attack and hurt frame atlases for the main families; variety assertions for Acts IV–VIII. | t-030 |
| 9 bosses + guardians | Partial | 27 boss phase plates b01–b09 and 8 painted main guardians [V]. 7 alt guardian kinds in `rainbowGuardian.ts:14-20`. | Same alt-guardian art as the X1–X4 row. | t-059, t-028 |
| Motherland consequences | Partial | Flown choice; allegiance lines in Acts VI–VIII (`rainbowAllegiance.ts:56-92`); 6 ending roads and titles (`rainbowEclipseFinale.ts:118-222`, #5547) [V]. No allegiance effect on waves or finale target [V]. | Rebel road: Ocean craft hold fire and Motherland drones join the waves. Distinct finale target (Motherland flagship vs Ocean heart). Loyal late stand-down (PLOT-MOTHERLAND:43-50). | NEW |
| 15 masks/endings | Mostly met | 15 reveals and 15 epilogues asserted (`T/verifyRainbowStoryScript.test.ts:153-201`). Masks are reachable through the crew roster (#5360, `T/verifyRainbowPilotRoster.test.ts`) [V]. | Prove all 15 at runtime through to an ending (part of QA). | t-013 |
| Opening/cutscenes/ending plates | Partial | `RAINBOW_OPENING = null` (`rainbowOpening.ts:30`) [V]. All 8 doodle WAN clips are DONE, including the re-rendered dolphin (ArtImage 279030) [V]. Only `endings/restore` ships (`GA:596-600`). C15/C16 redos are DONE (270453, 270454) but unshipped [V]. No moving cutscenes. | Run `export_rainbow_opening.py` and open a PR. Review and ship the 2 ending plates. WAN cutscenes, plus the animated midgame/allegiance scene and endings. | t-038, t-044, t-030 |
| Art coverage ledger | Partial | CAST-MANIFEST (pilots only); `audit_rainbow_gen2_art.py` (alt Acts only). No ledger covers every category with "runtime verified". | One coverage ledger: asset → ArtImage → public path → wired → screenshot. | t-042 |
| Motion coverage | Missing | No matrix exists [V]. | Write a per-action frame matrix and check it against live frames. | t-030 |
| Music/SFX | Partial | 19 ACE-Step mp3s: act1–9 flight and boss, guardian, ending, failure [V]. The engine plays only 8 generic SFX (`pickup`, `level`, `extra`, `blip`, `pop`, `start`, `shoot`, `die`) [V]. No X1–X4 or fork cues [V]. | Alt-Act and fork cues; distinct SFX for super, shield, damage and phase tell; check the mix and priority. | t-012 |
| Local 1–4 players | Met (automated) | t-005; `T/verifyRainbowLocalCoop`; the co-op cabinet browser test with 4 d-pads; a 4-pilot load test. | Full-campaign soak only. | t-013 |
| Responsive/DPR | Partial | `T/verifyArcadeViewport.browser.test.mjs:17-30`: Rainbow at 390×844, 844×390, 1024×768 (4 seats) and 1920×1080, each at DPR 1/2/3. The cabinet test adds 768×1024 and 1440×900 [V]. Sprite CSS px is reported (`:218-232`) but not asserted for bullets. | Add Rainbow at 360×640; assert a minimum rendered CSS px for hostile shots. | NEW (t-013) |
| Performance | Partial | Node-only check: average under 2 ms, worst under 1 frame (`T/verifyRainbowCoopLoad.test.ts:~225`). No browser p50/p95, no memory figure, no adaptive detail [V]. | Browser frame-time capture in a 4-player boss phase. | t-013 |
| Accessibility | Partial | Calm motion; cabinet aria labels; ending skip (`E:4791`). Keymap is fixed (`arcade-cabinet.vue:1112`); no remap UI, no contrast or colorblind option, no comms/subtitle settings, ship identity is colour-only apart from P# text [V/I]. | Remap UI, high-contrast pellets, comms full/essential/off with text speed, a non-colour seat marker. | t-044, t-012 |
| Adversarial QA/coverage graph | Missing | No test flies input-to-ending from a fresh start. Finale tests resume at act 9 (`T/verifyRainbowFinale.test.ts:139`); Motherland and achievements use demo mode [V]. | Coverage graph; seeded full runs across routes × 3 choices × 2 allegiances × masks × 1–4 seats; fail/retry personas; length statistics. | t-013 |
| RC evidence bundle | Missing | None exists. | Build it after t-013. | t-042 |

## 2. Finite remaining list (each item fits one PR)

1. Merge the t-059 PR (5 guardians plus coral-choir/comet-cadet pods and lighthouse lamp). **t-059**
2. Ship the kelp-sweep-frond and coral-asteroid hazards (both DONE). **t-059**
3. Ledger, render and ship the X3 hazard, X4 pickup, X4 hazard, Armory Siren and Lantern Matriarch. **t-028**
4. Ship the X1–X4 parallax planes; the X4 planes need the grey-band fix first. **t-028**
5. Ship the route-map and Hangar art (GEN2-ROUND-1). **t-027**
6. Ship the 16 main-Act far/mid planes (DOODLE-STAGE-DEPTH-PLANES, DONE) in place of the mirrored strips. **t-022**
7. Export the opening and set `RAINBOW_OPENING`. **t-038**
8. Review and ship the C15/C16 plates (270453, 270454) into `RAINBOW_ENDING_PLATES`. **t-044**
9. Rebel-road wave changes in Acts VI–VIII. **NEW**
10. Allegiance-specific finale target and loyal stand-down. **NEW**
11. ROUTE-MAP §5 scene variants, including adding `liltMemoryRecovered` and `crownEcho`. **t-027**
12. ROUTE-MAP §6 route stingers. **t-012**
13. Comms/subtitle settings. **t-012**
14. Remap UI, high-contrast pellets, erase flight log. **t-044**
15. Alt-Act and fork music cues, plus distinct SFX. **t-012**
16. Enemy frame atlases for the main families. **t-030**
17. Pilot pose set (hangar, hit, victory, defeat). **t-030**
18. WAN moving cutscenes from ART-ROUND-19. **t-030**
19. Wire the two unwired tests into CI. **NEW**
20. Rainbow 360×640 viewport and a bullet CSS-px assertion. **NEW**
21. Coverage graph and seeded fresh-start input-to-ending matrix. **t-013**
22. Browser p50/p95 frame-time capture. **t-013**
23. Unified asset and motion coverage ledger. **t-042**
24. RC evidence bundle, then title, close and lifecycle per §10. **t-042**

## 3. Can be reconciled now

- **t-034 → cancel as superseded by t-038.** Both use the same exporter (`export_rainbow_opening.py`), which now cuts only OPENING-CLIPS-2-DOODLE. t-034's October clips (44645–53) predate the doodle art [V].
- **t-038: blocker cleared.** intro-dolphin-armada is DONE (ArtImage 279030) [V]. Remaining work is export, inspection and a PR, so return it to ready.
- **t-011: claim stale since 11-20.** #5428 merged 11-20 but the note still says "pending" [V]. Release the claim, and narrow the task or fold it into t-022 (planes) and t-030 (atlases).
- **t-030: note out of date.** #5544 merged 11-22T03:37 [V]. Record the merge and release the stale claim.
- **t-044: mostly met.** #5547 merged [V], achievements are done (t-045) and the scrapbook is done (#5436). Remaining: 2 plates, settings, call sign/paint. Narrow the task to that and release the stale claim.
- **t-012: claim stale since 11-20.** The roster PR is on main (`verifyRainbowPilotRoster.test.ts`) [V]. Release it.
- **t-028 and t-027.** #5614 and #5611 merged [V]. Record them and check whether the claims from 00:17–00:19Z are still active.
- **t-022: claim about 5 h old.** #5593 merged [V]. Release, or move to the plane-shipping step.
- **t-042: claim stale since 11-21.** The save-bytes test is on main but not in CI. Release.
- **t-029 is "done", but its route-map, Hangar and alt backdrop art never shipped** [V]. Add that shipping to the t-027 and t-028 notes rather than reopening t-029.
- **t-013 stays waiting** on t-011 and t-012, which are review umbrellas. Consider letting the coverage-graph harness (item 21) start now [I].
