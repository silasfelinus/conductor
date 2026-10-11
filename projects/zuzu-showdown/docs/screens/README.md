# Screen tour (t-019, t-008)

Taken 2026-10-10 PT with Playwright on Chromium against a local `nuxt dev` of kind_robots with the portrait
branch (kind_robots#3485), at three widths: 390 (phone), 768 (tablet) and 1366 (desktop).

- `<width>-1-title` … `<width>-5-fight`: the real page from title through character select (P1 picked, the
  opponent's cursor live), the VS slam, and the first seconds of the fight. At 390 and 768 the run picked a
  mirror match, so P2's portrait shows its hue-shifted colours.
- `1366-4-vs-zuzu-vs-coyote`: a non-mirror VS screen with both portraits and the Coyote's intro line.
- `harness-*`: the win screen (victory portrait, the loser's beaten portrait in the corner, the winner's
  quote). Drawn by the same `drawWinScreen` in Chromium through a small bundle, because headless software
  rendering runs the game far below real time and a full match did not finish in the run.
