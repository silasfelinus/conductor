# zuzu-lair — task history archive

Full `note:` prose for completed zuzu-lair tasks, moved out of `roadmap.yaml` so the
Kind Robots projection payload (`scripts/sync_kind_robots_projection.py`, hard limit
4,000,000 bytes) stays well clear of its ceiling. See conductor/t-158.

Each note below is the **verbatim** original — nothing is summarized or trimmed. The
`roadmap.yaml` task keeps its own first sentence plus a pointer here. The HTML comment
markers delimit each note exactly; `archive_done_task_notes.py --verify-only` re-extracts
every note and checks it byte-for-byte against what the roadmap recorded.

## t-002 — Confirm scope with Silas

<!-- note:begin t-002 -->
FOR SILAS: soft checkpoint, nothing is blocked on it. Read DESIGN-BRIEF.md "Open questions": the chapter 1 story (draft "The Dry Gulch": rope bridge, scorpion, rockslide, gila-monster bandit), the tone of the death animations (draft: quick, stylized cut-aways), where it lives (its own Projects tab, plus an Arcade hall tile?), and whether it grows chapter by chapter. Agents keep building meanwhile and fold any redirect into the roadmap.
DECIDED 2026-10-06 by Silas in session: keep The Dry Gulch; deaths cartoonishly violent at the original's level, each a 2-5 s clip; yes to an Arcade hall cabinet tile (t-009); grow chapter by chapter (t-013 recurring). Folded into DESIGN-BRIEF.md v2 and SCENES.yaml v2.
<!-- note:end t-002 -->

## t-003 — Chapter 1 scene graph (chapters/01-dry-gulch/SCENES.yaml)

<!-- note:begin t-003 -->
Draft v1, 2026-10-06: 14 nodes -- opening, four moments (bridge: up, scorpion: right, rockslide: left, bandit: sword), a success and a death clip for each, closing. Each node has a house-lane keyframe prompt ({ZUZU} = the canonical string), a prose motion prompt, clip length, and for moments the Classic input window. Success and death clips start from their moment's last frame. Silas confirmed the story (t-002, 2026-10-06); v2 rewrote the four deaths to his "cartoonishly violent" level and holds every clip to 2-5 s.
<!-- note:end t-003 -->

## t-004 — kind_robots: pure QTE engine + contract test (utils/zuzuLair/)

<!-- note:begin t-004 -->
Framework-free TypeScript, no DOM: scene-graph types mirroring SCENES.yaml (ported as a typed TS module), a pure reducer for the run (node, clip time, window open/closed, lives, score, deaths, continues), input judging (right button inside the window -> success; wrong button or timeout -> death; early presses before the window are ignored on Assist, count as wrong on Classic), scoring (earlier in the window = more points, no-death and time bonuses), and difficulty (Classic window vs Classic + assist_extra). Contract test under utils/scripts/ run by tsx in contract-tests.yml, like verifyArcadeEngine.test.ts: walks a full perfect run, a run with every death, timeout and wrong button, continue after game over, and validates the graph (every target id exists, no orphan nodes, windows inside clip length).
DONE 2026-10-11: engine + chapter1 graph + validator + contract test (npm run test:zuzu- lair, wired into contract-tests.yml) merged in kind_robots#3508. Unblocks t-005 (player page).
<!-- note:end t-004 -->

## t-005 — kind_robots: the player page (video branches, input, flash assist, on-screen buttons, sound)

<!-- note:begin t-005 -->
Page /play/zuzu-lair on the Projects tab (content/channels/projects/zuzu-lair.md + utils/projectPlacements.ts). Two stacked <video> elements: the current clip plays while the next possible branches preload, so success/death cuts are instant. Until real clips exist each node shows a placeholder still with Ken Burns motion, so the whole loop is playable on day one. - Input: utils/arcade/input.ts (keyboard, gamepad, touch). - Mobile: reuse the arcade's touch-play lock (silasfelinus/kind_robots#3276). - Flash assist: the needed direction glows during the window. It is steady under
  prefers-reduced-motion and never strobes faster than 3 Hz.
- Options: on-screen d-pad + SWORD toggle, Assist/Classic, sound on/off. Remembered via a Pinia
  store, never localStorage from the component.
- Sound: clip audio plus WebAudio stingers (utils/arcade/sound.ts presets). - Flow: title card, then the opening animation; at the end, score, initials and the leaderboard. Verify at phone, tablet and desktop with Playwright, and screenshot every state.
DONE 2026-10-11: player page /play/zuzu-lair merged in kind_robots#3521 (placeholder stills until t-006 clips, flash assist at 2 Hz, d-pad, Pinia options, leaderboard slug zuzu-lair). Verified at phone and desktop with Playwright.
<!-- note:end t-005 -->

## t-009 — Leaderboard and arcade hall tile

<!-- note:begin t-009 -->
Reuse the arcade ArcadeScore board under game slug zuzu-lair. Add it to the server plausibility check (a maxPlausibleScore entry the API reads) and keep the per-browser fallback board. Add a special cabinet tile in the Arcade hall linking to /play/zuzu-lair (Silas: "yes on arcade cabinet", t-002).
2026-10-12: kind_robots#3601 merged. zuzu-lair registered in LINKED_GAMES (hall tile -> /play/zuzu-lair, score API plausibility 100,000, hall of fame); contract test verifyZuzuLairArcade wired into test:zuzu-lair. Title art is a Showdown placeholder until Lair art exists.
<!-- note:end t-009 -->

## t-012 — Project art: confirm icon, card and hero landed

<!-- note:begin t-012 -->
intake.py queued the icon, card and hero in projects/art-prompts.yaml (prompts rewritten to the Krea rules: physical subject first, no negations). Confirm they landed on kindrobots.org and look right (Zuzu short and stocky in the kasa and poncho); re-stage any that miss.
Verified 2026-10-08: projects/images/zuzu-lair-{icon,card,hero}.webp are in the repo and show Zuzu short and stocky in kasa and poncho; no re-stage needed.
<!-- note:end t-012 -->

## t-015 — Move Zuzu's Lair tab into Admin and add a global Home icon

<!-- note:begin t-015 -->
Silas requested in session on 2026-10-20 PT: move the existing admin-only Zuzu's Lair game from Play navigation to Admin; keep /admin/zuzu-lair. Add a persistent leftmost home icon to the shared header that returns to /. Implementation belongs in kind_robots navigation, not Conductor presentation data.

Source patch prepared on kind_robots branch worker/zuzu-lair-t015-admin-home-20261020-c82a: moves the protected Zuzu's Lair tab to Admin, keeps its route, adds a persistent branded Home control, and updates affected navigation contracts.

Merged silasfelinus/kind_robots#3951 as a0f578211ca91a82c7921165f13f9f179a846ef1. All 21 PR check runs completed successfully on caf95e99b1c954a4582f3b5a9248c7386171a1f3, including navigation contracts, TypeScript, responsive tablet audit and changed-file Prettier. Zuzu's Lair has an ADMIN-only tab; global header Home icon links to /. This is source merged only; Alexandria deployment was not separately verified.
<!-- note:end t-015 -->
