# memory-dungeon/t-040 — full note history archive

This file is the archaeology index for memory-dungeon/t-040 ("Memory Dungeon: deliver painted 6×6 House dungeon floorplans, not just the 8×8 overworld maps"). Its `note:` field in `roadmap.yaml` grew past `check_roadmap_note_size.py`'s 50,000-byte single-note threshold through ordinary recurring-cycle accumulation. The complete verbatim history through the archival point is preserved below; `roadmap.yaml` keeps only a short current-status pointer going forward. Do not restore this text into the live roadmap — read it here when you need to know what a specific past cycle found or did.

Archived under the AGENTS.md archival carve-out (byte-for-byte verified round-trip, pointer left behind, no history lost).

<!-- note:begin t-040 -->
2026-11-11 PT remaining: Gameplay geometry is not painted art; require delivered 6×6 floorplan images and visual acceptance. Evidence: RESET-TASK-EVIDENCE-AUDIT-2026-11-10.md (t-040 row).
FROM GITHUB ISSUE silasfelinus/kind_robots#4380 (https://github.com/silasfelinus/kind_robots/issues/4380), opened by @silasfelinus on 2026-10-28. Imported by scripts/sync_github_issues.py. Reference the issue in the implementing PR (`Closes silasfelinus/kind_robots#4380`) so it closes on merge; the bridge closes it otherwise once this task is done.

### Gap confirmed October 27, 2026 PT
The **original Briar / Dark Briar 8×8 overworld** already has rendered, delivered map assets (ArtJobs 46117 and 45570). PR #4379 fixes UI hardcoding that kept showing `briar-camp.svg`.

The **House That Remembers and Unremembered House 6×6 dungeon maps** remain interactive colored number grids, not painted floorplans. The existing `house-interior.webp` render is a room backdrop, not a coherent 36-room overhead atlas. No verified dedicated House atlas ArtJob was found in the Memory Dungeon art ledgers. Do not mark this House-map requirement complete on the strength of the 752/752 *other* delivered requests.

### Acceptance
1. Author **two original 6×6 top-down painterly maps**, one House and one mirrored House, each matching the existing immutable HD-01–HD-36 layout and paths/door orientations. Coordinate guide against `utils/memoryDungeon/house.ts` and `darkHouse.ts`. Render through normal durable Krea2 ArtJobs, record IDs, prompt, engine, image destination.
2. Deliver to predictable runtime media paths and verify actual image URLs via unauthenticated HEAD plus appropriate status, not just the request or `DONE`.
3. Integrate into `components/memory-dungeon/house-stage.vue` and `dark-house-stage.vue` beneath still-legible 6×6 clickable overlays; retain room orientation, disabled-state boundaries, reactivated 3D markers, keyboard focus, and SVG/design fallback on failed media.
4. Validate 390/768/1440-width one-screen layout, painted-map/room coordinate alignment, map visibility on first paint, save/resume compatibility and reduced-motion preference. No public-release human gate until art and adversarial QA complete.

Related: [Memory Dungeon master roadmap #4136](https://github.com/silasfelinus/kind_robots/issues/4136), [UI repair PR #4379](https://github.com/silasfelinus/kind_robots/pull/4379), [direct-media audit](https://github.com/silasfelinus/conductor/actions/runs/40429786760).

Scoped House atlas increment in review: immutable 6x6 row-major overlay and two Krea2 production requests. Do not close issue #4380 until both ArtJob IDs, delivered media, painted topology and rendered device acceptance are verified.

Partial t-040 increment merged: kind_robots#4384 and conductor#6766. Original/mirrored House atlas layers, stable HD-01..HD-36 overlays, two Krea2 request entries, orphan-job reconciliation and strict receipt audit are committed. Both requests remain pending without verified ArtJob IDs or delivered media. Next worker: verify the Auto Art Generate handoff, actual positive job IDs and media HEAD, then inspect painted 6x6 geometry and rendered 390/768/1440 gameplay. Issue kind_robots#4380 remains open; no human gate.

Focused House atlas ArtJob pipeline fix prepared: correct doubled shell line-continuation escapes in Auto Art Generate and add a parsed-workflow command regression test. Await exact-head CI and PR merge. Two ArtJob receipts and painted-media acceptance remain unverified; task and issue must stay active.

2026-10-28 PT partial House atlas production unblock: merged conductor PR #6767 (a809c8b4ee950022388668e1a2132039f975b6de) repairing doubled Bash line continuations in Auto Art Generate, with workflow-token regression test. Exact-head Worker PR CI #40675772650 passed 3110 tests (53 skipped), Security Audit #40675772595 and final handoff #40675834313 passed. Auto Art Generate #40676293032 passed House atlas submission/checkpoint and two-ID receipt audit. Original 6x6 House Krea2 ArtJob #50365 and mirrored House Krea2 ArtJob #50366 are durably recorded in HOUSE-ATLAS-REQUESTS.yaml. Both remain pending, with rendered media HEAD, 36-room topology and 390/768/1440 device acceptance unverified. Keep issue kind_robots#4380 open, project active, no human gate.

Focused House atlas delivery-evidence audit is ready for CI: reuse ArtJob identity and strict image HEAD proof, publish two-row status in Auto Art Generate, and keep issue #4380 open pending actual painted art and device QA.

2026-10-28 PT partial House atlas evidence increment merged: conductor PR #6768 (bc21797d8f7a619d92cdb755ab6a5453efb8e121). A read-only live two-job audit now verifies ArtJob identity, ArtImage and fresh image HEAD, checkpoints HOUSE-ATLAS-STATUS.json before long render work, and provides strict --require-delivered gating. Exact-head Worker PR CI #40682908879 passed 3114 tests (53 skipped), Security Audit #40682908838 and handoff #40682908849 passed. Existing Krea2 ArtJobs #50365 and #50366 remain unverified for delivery until live Auto Art Generate #40683403903 reports. Next: inspect live status and delivered images for 6x6 topology, then 390/768/1440 rendered, keyboard, reduced-motion and save/resume acceptance. Keep issue #4380 open, project active, no deployment or human gate.

Partial House atlas acceptance: corrected original and mirrored map overlay geometry (zero grid gap and padding, square hitboxes) and reduced visited/available tint opacity so eventual painted 6x6 images remain visible. Added source contract assertions. ArtJobs 50365 and 50366 still have no verified delivered ArtImages; keep issue #4380 open.

Partial House atlas alignment increment merged as kind_robots PR #4423, squash f10f47dec14383c0564f0532bae3f6d51f5b1c6e. Removed grid padding/gaps, squared the 36 clickable hitboxes, lowered painted-map obscuration and kept outer-edge keyboard focus outlines inside both original and mirrored maps. New contract assertions; all 14 exact-head Actions workflows passed on fe7ca13be02052687576653140aa674dbd15fcff (Contract Tests #40814820167, TypeScript #40814820204, Layout #40814820212, Formatting #40814820236). No new ArtJobs. Existing Krea2 atlas ArtJobs #50365 and #50366 remain PENDING with 0/2 delivered and null ArtImage IDs in latest committed HOUSE-ATLAS-STATUS.json; fresh media HEAD could not run in this sandbox (DNS resolution failure). Remaining: verify delivered image URLs, painted six-by-six room topology, rendered 390/768/1440 layout, keyboard, reduced-motion and save/resume. Issue kind_robots#4380 stays open; project ACTIVE, no deployment or human gate.

Partial House atlas delivery increment: implemented a deterministic illustrated SVG architectural fallback beneath both pending Krea2 atlases, with six-by-six row-major registration, genuine adjacent doors only, and regression checks for geometry and source wiring. Existing ArtJobs 50365 and 50366 remain pending (0/2 delivered at Auto Art Generate #40823293659); painted topology and rendered device acceptance remain open. Focused Kind Robots PR and exact-head CI follow; do not close issue #4380 or mark human gate.

2026-11-04 PT cleanup pass: stale review with an expired claim; the recorded slice
landed (or was superseded) and the note itself lists remaining scope, so back to ready
for the next slice rather than done.

Added six regression checks for committed House atlas delivery receipts, image IDs, destinations and aggregate counts. Both Krea2 jobs 50365/50366 now have delivered checkpoint entries with ArtImages 257966/257967. Live independent HEAD and rendered six-by-six topology/device QA remain outstanding; do not close issue #4380.
<!-- note:end t-040 -->
