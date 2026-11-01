# game-of-captains/t-008 — full note history archive

This file is the archaeology index for game-of-captains/t-008 ("Deliver Space Couch painted red-sofa ship, pocket-room, shield, crew and world art"). Its `note:` field in `roadmap.yaml` grew past `check_roadmap_note_size.py`'s 50,000-byte single-note threshold through ordinary recurring-cycle accumulation. The complete verbatim history through the archival point is preserved below; `roadmap.yaml` keeps only a short current-status pointer going forward. Do not restore this text into the live roadmap — read it here when you need to know what a specific past cycle found or did.

Archived under the AGENTS.md archival carve-out (byte-for-byte verified round-trip, pointer left behind, no history lost).

<!-- note:begin t-008 -->
Deliver branded Space Couch project icon/card/hero, detailed red couch/force bubble/pocket room/starmap, original personnel and emotional portraits, Vox/Serendipity/Fluke continuity plates, twelve worlds and eight antagonist identities; verify final URLs, ArtJobs and render provenance rather than SVG/placeholders.

Canonical cast portrait redesign round submitted for code/art review. 66 new Krea2 requests in CAST-REDESIGN-ROUND-2.yaml, with a Kind Robots v2 art-slot preference and legacy fallback. This is only the first art tranche: rendered delivery, runtime exports, ship/world/outcome coverage and visual review remain open.

2026-10-27 PT cast redesign tranche merged: Conductor PR #6759 (9f39f1e849164660dedc42108cc277f029755fb8), app PR #4353 (d1ed41f468944a765edb58022f048ea14b6bdaff). All 4 Conductor and 17 Kind Robots current-head workflow groups passed. The 66 Krea2 canonical portraits (6 captains, 12 playable plus 4 future crew, three expressions each) are authored at CAST-REDESIGN-ROUND-2.yaml with auto_submit, versioned portraits/v2 keys and legacy fallback. Post-merge audit found 0/66 ArtJob IDs, 0/66 DONE and 0 exported v2 assets at that time. Continue via automatic art sweep, reconcile actual ArtJob IDs, inspect render quality, export .webp and update app generated art manifest, validate crops at phone/tablet/desktop, then finish remaining title/icon, couch room, 12 worlds, antagonists and story consequence art. No art-complete or human design gate.

Triage 2026-10-30: cheapest visible win is export, not generation. CAST-REDESIGN-ROUND-2 has 66/66 DONE v2 captain/crew portraits (ArtImage 257797+), but none are under kind_robots public/game-of-captains (only 21 legacy renders). Run scripts/export_round_art.py with --max-edge, rebuild utils/gameOfCaptains/artManifest.ts, then render the 12 worlds, 8 antagonists, couch, pocket room, starmap and 20 casino venues (t-027 handoff).

2026-10-30 PT art export (no new generation): kind_robots PR #4483 merged at
fd9bd2396382fbe159d6fb1ecd0d44d4afe27e06, all 21 checks green. Shipped 18 CAST-REDESIGN-
ROUND-2 v2 portraits (6 captains + 12 playable crew, 640px) that portraitArt() prefers
over legacy faces, plus 10 RUNTIME-BEATS-ROUND-1 scenes (missions refugees/archive/bar,
antagonists auditor/moth/curdle, 4 base endings, 960px); WARP_ART 21 -> 49. Trio
interlude now reads faces via portraitArt so it shows v2 too; verifyGameOfCaptains
asserts every captain/crew face resolves to its v2 URL and every exported beat key
resolves. Contact sheet reviewed. Not exported because no runtime lookup exists yet: 48
defiant/vulnerable expression variants, 12 future-crew (nyra/gleam/harrow/edda)
portraits, 18 OPENING-TITLES, 21 CONSEQUENCES, 8 legacy pair portraits; REDSHIRTS-200
and SERENDIPITY-CASINOS-20 have 0 DONE rows. Remaining for this task: wiring expression
variants (e.g. injury/defeat states), ship/pocket-room/starmap/world art, the other 5
antagonists and 27 missions/12 earned endings, which still have no renders.

User requested continued Space Couch build on October 31 PT. Taking next unclaimed art-delivery slice: wire completed painted assets into live game presentation, with tests and truthful delivery accounting.

Continued t-008 painted-art delivery slice: 106 DONE ArtImage IDs from three existing Conductor rounds now have access-filtered runtime URLs in Kind Robots, powering voyage main stage, Serendipity venues, and painted title art. Older conventional-bridge static art is intentionally excluded. This is a scoped delivery increment, not completion of all ship/world/portrait art. Full t-008 visual acceptance and other painted inventory remain open.

October 31 PT scoped painted-art runtime slice merged in Kind Robots PR #4564, commit 10b04371783a2de6ac83569f8fc0028dc9c1f6a0. All 20 exact-head checks passed. Connected 106 DONE ArtImages (27 missions, 5 antagonists, 36 endings, 20 Serendipity venues, 18 opening scenes) to title, stage and casino screens via access-filtered art lookup. Existing 22 onboarding illustrations remain registered. Main verified clean; branch deleted. This task is NOT complete: artwork accessibility in authenticated self-hosted production, large image visual QA, full couch and pocket-room continuity, character expression variants, unfinished maps and remaining scenes still need delivery. No publishing or deployment has been authorized.

Continue user-requested Space Couch art delivery by connecting completed cast expression renders and illustrated pocket-room shipboard scenes to active play states. Preserve image access controls and existing saves.

Scoped Space Couch art delivery: 44 DONE expression portraits are now served through the existing access-filtered ArtImage endpoint. Captain and crew dossiers expose three portraits, the away team shows defiant or vulnerable images based on assignment and injury, and briefing choices display the completed Holodeck, War Room and Infirmary artwork. Static contract tests include all unique keys. PR and CI pending. Do not mark the broader t-008 art campaign complete.

October 31 PT continuation merged Space Couch PR #4572 at fbd7f753a729e3c08da64147c7c084c540040eec with 20/20 exact-head workflow groups green. Delivered authenticated lookup for 44 completed Krea2 defiant/vulnerable portrait plates (CAST-REDESIGN-ROUND-2, ArtImage IDs 257798-257862, corresponding selected ArtJobs 50300-50364). Players can preview three expressions for each captain and crew member; away-team cards use defiant expressions, injured officers show vulnerable expressions. Pocket-room options display completed 09-holodeck, 10-war-room and 11-infirmary art; the selected room updates the briefing-stage painting. Main verified, branch deleted. Do not close t-008: final authenticated image reachability, responsive screenshots, couch/force-bubble/world art continuity and remaining illustrated consequences still need independent acceptance. No production deploy.

User requested continued Space Couch development. Connect the remaining 18 completed opening-title paintings to a full-screen player-stepped illustrated opening reel with original lines, accessible navigation, art fallbacks and contract tests; keep deployment and remaining t-008 art work separate.

Scoped delivery of 18 completed Space Couch OPENING-TITLES-ROUND-1 paintings: built accessible full-screen, player-stepped opening sequence inside existing main menu. Every frame has authored original dialogue, recorded art key and meaningful alt text; keyboard controls, reduced motion and image-failure fallback are covered by new static contracts. Game saves and private image access are unchanged. Opening PR/CI is in progress; larger t-008 art inventory remains unfinished.

Merged Kind Robots PR #4576 at c3b5d541401f76f81c4d27b67f72577e111da2e1 after all 17 exact-head GitHub workflow groups completed SUCCESS.  Added a playable 18-frame illustrated opening reel using the previously DONE OPENING-TITLES-ROUND-1 ArtImages 255479-255496 and original script; responsive full-screen presentation, player navigation, keyboard arrow/Escape support, reduced-motion handling, safe missing/private image fallback and clear exit/captain creation. No new ArtJobs, database changes or permission changes. Verified main commit and auto-deleted PR branch. Continue t-008 for ship/force-bubble art, authenticated image delivery and real 390/768/1440 visual checks; no self-hosted deployment or public release was authorized.
<!-- note:end t-008 -->
