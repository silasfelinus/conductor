# Chessweeper playthrough QA, 2026-11-22 PT (chessweeper/t-004)

Harness: kind_robots `utils/scripts/verifyChessweeperPlaythrough.browser.test.mjs`
with `chessweeperPlaythroughHarness.mjs`, run in real Chromium. It serves
`public/` statically and proxies the live painted art from kindrobots.org.
Timers run on Playwright's clock. Every action is a visible click or tap on the mode
buttons and board squares. The scripted player reads engine state only to choose a
move. Games are seeded (`?seed=N`), so a run is reproducible. CI runs it in the
`Chessweeper playthrough` workflow on every PR that touches the game.

Result: **pass in 226 s**, with zero page errors.

## Coverage

| Area | Checked |
| --- | --- |
| Layout 390 / 768 / 1440 × 3 worlds | no horizontal scroll, board fits and is ≥300 px, 64 squares, scrapbook / achievements / settings dialogs fit |
| Touch (390, 768) | tap a pawn, tap its destination, a move is played |
| Campaigns | all three four-chapter campaigns completed, `campaign-*` achievements awarded |
| Endings | **12/12 reached by play**; each scene shows prose ≥2 paragraphs and a "Your run" box, and *Next battle* starts a fresh battle |
| Scrapbook | one replayable page per discovered ending; replay opens the scene |
| Save/resume | reload mid-battle, *Continue saved run* restores the same turn count |
| Transfer codes | export, merge into a second device (all endings arrive), and a bad code is rejected without data loss |
| Settings | the motion toggle persists across reload |
| Keyboard | P / M switch modes |
| Reduced motion | the ending opens immediately, with no cinematic or plate overlay |
| Audio gesture policy | 0 AudioContexts before the first gesture, ≥1 after |

## Battle log (final run)

| World | Chapter | Strategy #seed | Ending | Turns | Score |
| --- | --- | --- | --- | --- | --- |
| sugar | 1 | fallen #1 | fallen | 14 | 60 |
| sugar | 1 | arena #1 | fallen | 249 | 526 |
| sugar | 1 | arena #2 | fallen | 162 | 427 |
| sugar | 1 | arena #3 | arena | 45 | 441 |
| sugar | 2 | sweep #1 | sweep | 35 | 1436 |
| sugar | 3 | sweep #20 | sweep | 31 | 1559 |
| sugar | 4 | sweep #21 | sweep | 33 | 1256 |
| ashen | 1 | fallen #1 | fallen | 10 | 0 |
| ashen | 1 | arena #1 | arena | 31 | 85 |
| ashen | 2 | sweep #1 | sweep | 37 | 828 |
| ashen | 3 | sweep #20 | sweep | 41 | 871 |
| ashen | 4 | sweep #21 | sweep | 41 | 811 |
| jackpot | 1 | fallen #1 | fallen | 8 | 0 |
| jackpot | 1 | arena #1 | fallen | 62 | 297 |
| jackpot | 1 | arena #2 | arena | 41 | 368 |
| jackpot | 2 | sweep #1 | sweep | 35 | 1277 |
| jackpot | 3 | sweep #20 | sweep | 39 | 1239 |
| jackpot | 4 | sweep #21 | sweep | 31 | 1180 |
| sugar | 1 | mate #1 | mate | 53 | 940 |
| ashen | 1 | mate #2 | mate | 17 | 85 |
| jackpot | 1 | mate #1 | mate | 29 | 648 |

The minefield strategy knows where the mines are, so it proves the sweep ending is
reachable; it does not measure how hard deduction is. Checkmate was hunted from fresh
chapter-1 profiles (late chapters wake all four blades) and merged into the main
profile through the in-game transfer-code UI.

## Defects found and fixed in kind_robots #5597

1. **The profile layer never loaded.** `progression.js` called the page-private
   `$('meta-close')` and threw on load. This had been on main since #5530. On the
   live site, achievements, ending records, checkpoints and settings were dead.
2. **The phone operations console was hidden.** At ≤700 px,
   `.panel .box:not(:first-child)` hid PROBE, FLAG, DASH, wager and New battle once
   campaign.js prepended its chapter card.
3. **Balance: passive arena wins.** The black AI ignored the blade forecast, so in
   Ashen and Jackpot the enemy king died to blades at turn 18–28 on every seed, and
   checkmate and minefield wins were effectively unreachable. Measured over 3 seeds
   × 4 strategies per world, before and after the fix:
   - Before: Ashen produced 9/9 arena wins, all at turn 17–20.
   - After: Ashen produced sweep 3/3, mate 4/16 in a 16-seed hunt, and arena wins at
     turn 19–73.
   - After: Jackpot produced sweep 3/3, mate 6/16, and varied arena wins.
4. **Sugarbomb contrast.** The campaign card and the Scrapbook / Achievements /
   Settings buttons had dark ink on dark panels.
5. **Hearts overflow.** Six hearts clipped on phones; the counter now reads `♥ ×6`.
6. **Ending scene on phones.** Focusing the dialog scrolled the plate out of view; it
   now opens at the top.

## Audio (t-008)

All six loops are live at `kindrobots.org/chessweeper/music/*.wav` (HTTP 200,
`audio/wav`, byte sizes match the repo), and each has a distinct hash. Offline
analysis results:

- format: 22.05 kHz mono
- peak: −2.8 dBFS on every track
- RMS: −10.5 to −13.7 dBFS
- clipped samples: 0
- loop seam jump: 0.0000

The browser run confirms no AudioContext before a gesture and one after, and the
soundscape contract covers mute/unmute retirement and disposal. A human ear on a
phone speaker is still worth a listen in part 3 of the checklist.

## Not covered by agents

- Subjective fun, difficulty feel and art taste. These belong to the human
  playtest; see [PLAYTEST-CHECKLIST.md](../PLAYTEST-CHECKLIST.md).
- Account-synced saves. Progress is explicitly device-local, with transfer codes.
- Gamepad input. The game has no gamepad bindings, so this was not tested.
