# Chessweeper: human playtest checklist

For Silas, at [`/play/chessweeper`](https://kindrobots.org/play/chessweeper) once the
next scheduled deploy has picked up kind_robots #5587 (audio lifecycle) and #5597
(endings, scrapbook, achievements, QA fixes). This is a handoff sheet, not a gate.
It lists what to look at and what each thing should feel like, so a verdict can be
specific. Allow 20 minutes on a phone and 15 on a desktop. Use a **fresh browser
profile** (or a private window) for part 1, because progress lives on the device.

## 1. First five minutes (phone, fresh profile)

- [ ] The page opens inside the Kind Robots shell with the **?** help in the bar.
      The three world cards (Sugarbomb, Ashen, Jackpot) show their painted art.
- [ ] Tap **Sugarbomb Kingdom**. The board, the hearts row (`♥ ×6` once you have
      more than four), the chapter card *The First Sprinkle* and its two risk
      contracts are all readable on the pink theme.
- [ ] Below the chapter card the **operations console** is visible: MOVE, PROBE,
      FLAG, DASH SHIELD and NEW BATTLE. (This was hidden on phones before #5597.)
- [ ] Pick a contract, move a pawn, then PROBE a covered square. A clue number
      appears, the blades step, and Black answers.
- [ ] Long-press a square to flag it. *Question: does mixing chess moves and probes
      feel like one game, or like two games taking turns?*

## 2. Endings (any device)

Each world has four endings: **checkmate**, **clear the minefield**, **let the
arena destroy the enemy king**, and **lose (or draw)**.

- [ ] Lose a battle on purpose (probe a few mines). After the short "SUGAR CRASH"
      flash, an **ending scene** opens with a painted plate, two paragraphs of prose,
      a **Your run** box (your contract, turns, points) and *Try again / Scrapbook /
      View the board*.
- [ ] Win one by clearing every safe square. The scene says *Minefield ending ·
      2 of 4* and the prose fits the world.
- [ ] Finish chapter 4 in any world. The "Your run" box opens with **CAMPAIGN
      COMPLETE** and a world-specific epilogue.
- [ ] Ending plates: twelve paintings were queued in conductor #7848. Until a
      plate renders, the scene shows the world's painting instead. *Question: once
      they land, do they read as twelve different endings?*

## 3. The three worlds feel different

- [ ] **Sugarbomb:** charge Sugar Rush with clues and captures. A painted
      *Sugar Rush!* plate flashes and the wheels freeze for two beats.
- [ ] **Ashen:** two hearts each, more blades. Lose your last heart once: **Last
      Stand** plays its painted plate and gives you one armoured move.
- [ ] **Jackpot:** capture to build the multiplier, then **Double or Nothing**. The
      plate flashes and a payout follows if you survive.
- [ ] Each world plays its own music loop, and chapter 4 switches to its finale.
      Settings has music and effects sliders, and muting music stops it at once.
- [ ] *Question (balance):* in Ashen and Jackpot, does the enemy king still die to
      the blades too easily? #5597 taught the AI to read the blade forecast; before
      that it died by turn 18–28 every game.

## 4. Scrapbook, achievements and saves

- [ ] **Scrapbook**: it shows 12 ending pages (locked ones are blurred with a
      non-spoiler hint), each world's action plate and piece atlas, chapter
      milestones with ★ for mastery trials, and your last 12 battles. Tap an
      unlocked ending to replay its scene.
- [ ] **Achievements**: 24 in total. Locked ones say what to do.
- [ ] Mid-battle, reload the page. **↩ Continue saved run** restores the same battle.
- [ ] **Settings → Create transfer code**. Paste it into a second browser and choose
      **Merge pasted code**. Endings, achievements and campaign chapters appear
      there, and nothing that was already there is lost.
- [ ] Settings says plainly that progress is stored on this device for guests and
      signed-in players alike. *Decision for later:* should progress sync to the
      Kind Robots account? That needs a server model, so it is not in this build.

## 5. Accessibility and controls

- [ ] Desktop keyboard: **M / P / F / D / N** switch modes, dash, and start a new
      battle. **Esc** closes dialogs.
- [ ] Settings → turn off *Animated sawblades and transitions*. Ending scenes then
      open straight away, with no flashes.
- [ ] Settings → *High contrast* and *Show predicted blade paths* both take effect.

## What was verified by agents (not a substitute for the above)

`utils/scripts/verifyChessweeperPlaythrough.browser.test.mjs` (real Chromium) plays
all three four-chapter campaigns through visible clicks and reaches **12/12 endings
by play**. It also checks scrapbook replay, save/resume, transfer merges and
rejection of bad codes, settings persistence, keyboard, touch, reduced motion, that
no audio starts before a gesture, and 390/768/1440 layouts. See
[qa/2026-11-22-playthrough.md](qa/2026-11-22-playthrough.md).

Publishing, sharing the promo image and wider promotion each remain separate
decisions. This handoff does not authorize them.
