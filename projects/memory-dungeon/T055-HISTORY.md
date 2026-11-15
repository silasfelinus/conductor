# memory-dungeon/t-055 — full note history archive

This file is the archaeology index for memory-dungeon/t-055 ("e08 Hearth of Perfect Safety: rewrite the 16 night sites to Vesper's POV and finish the map"). Its `note:` field in `roadmap.yaml` grew past `check_roadmap_note_size.py`'s 50,000-byte single-note threshold through ordinary recurring-cycle accumulation. The complete verbatim history through the archival point is preserved below; `roadmap.yaml` keeps only a short current-status pointer going forward. Do not restore this text into the live roadmap — read it here when you need to know what a specific past cycle found or did.

Archived under the AGENTS.md archival carve-out (byte-for-byte verified round-trip, pointer left behind, no history lost).

<!-- note:begin t-055 -->
2026-11-11 PT remaining: Audit every authored night site for Vesper's POV, original horror and earned consequences. Evidence: RESET-TASK-EVIDENCE-AUDIT-2026-11-10.md (t-055 row).
Silas 2026-11-05 PT: the first eight overworlds keep one protagonist per pair, so e08 is Vesper's, not Scylla's (kind_robots#4778 already moved the viewpoint contract). hoshimoriNight.ts's 16 playable sites and store still describe "a separate Scylla-viewpoint expedition". Rewrite them from Vesper's POV without changing coordinates or choice ids, keep the Junji-Ito-tonal psychological/architectural horror register, then continue toward 64 sites and the dark Oven per t-044. Char's fate branches still apply through campaign flags, not through POV.

Reframed all 48 currently authored e08 Hoshimori night sites from incorrect Scylla protagonist to Vesper, preserving stable choice IDs and Char agency. Remaining: expand to 64, validate runtime and browser, polish Vesper-specific outcomes; PR pending CI.

PR silasfelinus/kind_robots#4981 merged as b11622472e84b427b28b1a9bf282da85179fd523 after eight exact-head workflows passed. Reframed 48 existing e08 sites for Vesper without changing choices or Char agency. Remaining 16 sites and playable traversal/art verification are unfinished; return task to ready, not done.

Added 16 authored e08 southern Hoshimori sites, bringing the map to 64, with two consequential Vesper-led choices per site, updated reachability validator and seeded replay/forgery tests. Focused Kind Robots PR pending CI; art and rendered device QA remain.

PR kind_robots#4989 merged as bccbdf70c6c6ab3c38a33e9871c5c1bbf40b7fd0 after all eight exact-head workflows passed on f637057309700c1a7cd57b022bc78f4871099790. e08 now has 64 authored sites. Remaining: earned-exit end-to-end, integrated production art and rendered device QA. Keep active, not human-gated.

Added 16-seed full 64-site e08 traversal and restoration coverage, including Last Train platform forged-verdict rejection. Kind Robots commit ef3451f; PR and CI pending. Earned exit, dungeon, art and rendered UI remain open.

2026-11-11 PT: PR kind_robots#5019 merged (9de1c65) after six successful exact-head workflows. All 64 e08 sites now covered in seeded expedition regression with save/forgery assertions. Remaining earned-exit/dungeon integration, art verification and rendered QA; keep task active.

Scoped e08 save-restoration hardening rejects injected top-level fields and malformed saves, with regression assertions. Kind Robots worker PR pending CI; earned-exit/dungeon, art and rendered UI remain open.

2026-11-11 PT: Strict e08 Chronicle save-field validation and adversarial regressions merged as kind_robots PR #5062, squash 7bbd10a4. All eight exact-head Actions workflows passed on 3de3c16e, including TypeScript, Contract Tests and Memory Dungeon browser interruption. Partial t-055: earned-exit and dungeon end-to-end seeded integration, rendered-device acceptance and art remain open. Return to ready for remaining scope.

Added e08 64-site completed-route adversarial tests for truncated event histories and appended duplicate Last Train verdicts. Kind Robots PR pending exact-head CI. Earned exit, dungeon integration, production art and viewport QA remain.

PR silasfelinus/kind_robots#5096 merged as 11fff7fd after six successful exact-head GitHub Actions workflows on e565547. Added adversarial e08 64-site completed-route save-replay regressions for missing final event and duplicate Last Train verdict. Return ready: earned-exit/dungeon end-to-end, production art delivery and responsive UI verification remain.

Added 64-site e08 adversarial choice-fork replay: each alternative is executable, preserves previous decisions, rejects overwriting and restores exactly. Kind Robots PR pending CI. Earned exit/dungeon integration, production art and UI QA remain.

Merged kind_robots PR #5100 at 1605a6ac5d6101fe361e3e7fa2bd6ea2c001b2ce. All six GitHub Actions workflows passed on exact head cac85fbb83da99c66aa654290029f485847d64b4. The 64-site e08 alternative-branch replay and restoration regression is integrated. Remaining: earned-exit and dungeon integration, delivered production art, and rendered UI QA.

Added four tamper-resistance assertions to each of sixteen complete e08 64-site seeded expeditions: forged flags, missing visited site, forged position, and forged door-open state must be rejected on restore. Kind Robots PR pending CI; earned-exit, art, and rendered QA remain.

PR kind_robots#5105 merged as d7a24de after all six exact-head GitHub Actions passed on 5e26b1a. Added 16-seed adversarial e08 restoration assertions for forged consequence flags, visited locations, position and gate state. Remaining: earned exit/dungeon integration, delivered production art and device QA. Return ready; not human-gated.

Integrated e08 night overworld's 4,3 Furnace choice with the 36-room dungeon test, both entry states, three earned endings and save restoration. CI pending. Rendered UI, production art and full campaign exit integration remain.

PR silasfelinus/kind_robots#5110 merged as 107ea3037aa918330686866c5e5ade89540c3df4 after all six exact-head workflows passed on b790a13e438c444e18006893d58d50ae144cd8f1. Both e08 Furnace entry choices now run integrated 36-room earned-exit and save-restore tests. Remaining actual rendered button/reload, full campaign ending propagation, production art and responsive QA.

e08 night console now correctly credits Vesper and shows the actual 64-site authored count with the Furnace entry at 4,3. Added source-contract regression assertions for POV, site count and earned entrance. CI pending; real rendered UI, mid-dungeon reload, campaign ending propagation and production art remain.

PR kind_robots#5112 merged as 26bfb792 after all six exact-head checks passed on 2b5ca3a. The e08 night console now shows Vesper, 64 authored sites and the earned Furnace entry. Remaining rendered browser entry/reload, ending propagation, art and device acceptance. Keep active and ready.

Added adversarial Furnace tests for all three Kogane guardian resolutions, both entrance histories, all three endings, and restored-save replay. CI and actual rendered browser verification remain outstanding.

2026-11-13 04:52 PT: PR silasfelinus/kind_robots#5114 merged as 68b524acb73bdbb470549a8b3bd20e732e1211cc after all six exact-head GitHub Actions checks passed on fa098c5611c9e1d65c19de7c12b9312aa74e78fb. Added 18 guardian-entry-ending adversarial paths and replay/save integrity. Task remains ready: rendered e08 Furnace entry, mid-dungeon reload, campaign-ending propagation, production art and viewport QA remain unfinished.

Added interruption/save-restore assertions at FN-12, FN-24, FN-31, guardian and climax for both e08 Furnace entries; climax selection alone must not count as an earned exit. Implementation PR and exact-head CI pending. Real browser reload, art delivery and campaign propagation remain.
<!-- note:end t-055 -->
