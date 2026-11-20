# Slime City: ready for human testing, 2026-11-19 PT

**Playable route:** https://kindrobots.org/play/slime-city. Sign in first; an account is free. A friend duel starts from VS → VS PLAYERS, or from a shared `/play/slime-city-pvp?duel=<id>` link.

**Lifecycle:** `playtest` / `normal` priority (Silas, 2026-11-19 PT: *"You're responsible for getting slime city ready for human playtesting ... the kind robots project should be normal priority and set for 'playtest'."*). The finite build roadmap is complete. What's left is Silas's own calls (below) plus whatever playtesting turns up. New fixes go in as `playtest_iteration: true` tasks. This handoff is **not** publication, promotion or creative sign-off.

**Deploy status:** production is on build `db5d615` (deployed 2026-11-19 PT, about 6:30 PM). It contains every fix named here: kind_robots#5372, #5376, #5379 and #5380. The layout and input audits below were re-run against that build after it went live.

## What testers get

- **Five tabs:** HOME, VS, JOURNEY, TOWER, COLLECTION. Every fight is CLASH: five alleys, a 20-card deck, five cards a turn, two plays, then every fighter strikes across its alley. Bosses start at 40 life.
- **Six crews:** Gene Riot Catgirls, Queen Pin & the Bloodfairies, Ironjaw Chrome Lizards, Anarkiss, Undertow Intelligence, Meat Exchange. Each has a crew power, once per match.
- **300 cards:** 240 crew cards and 60 mercenaries (114 fighters, 92 spells, 51 traps, 43 gear). Every card levels up when played, to level three, with its own painting at each level.
- **JOURNEY:** a five-chapter story for each crew (15 scenes, 30 decisions and a crew meter that changes the fights), plus the seven-district city. The gallery holds 90 endings, 15 per crew. A finished run adds a scrapbook page and unlocks that crew's card back and title.
- **TOWER:** a twelve-floor climb with a two-crew Alliance deck.
- **VS:** the CPU with a Solo or Alliance deck, or another player by friend challenge, invite link or open duel, with hidden hands, reconnect, forfeit and rematch.
- **COLLECTION:** a named deck library. Everyone starts with the six crew starter decks and a set of mercenaries, and earns the rest in play.
- **Main-game standard:** title screen with Continue, 19 achievements, endings gallery and scrapbook, and settings for sound, motion, Clash speed, large text, high contrast and journey reset.
- **Input:** mouse, touch, keyboard (Tab and Enter) and gamepad.

**Who sees what.** An admin account banks Meat, XP and packs, and saves the journey to the account. Every other signed-in account sees LOCAL PLAY: the whole game is playable, the journey saves on that device, and Meat is shown but not banked. That is deliberate until launch (t-015). When account saves open for a player, the title screen offers to bring the device journey in.

## Verification on record

- **Story:** 576 routes (6 crews × 32 choice paths × 3 seeds) through the real engine, 4,088 fights, both endings reached for every crew (`verifySlimeCityFullRoutes`).
- **Cards:** all 230 crafted journeys run through the engine at every level, with no duplicate journey. Every one of the 300 cards is played by the CPU in seeded QA: 294 in the 1,080-match suite and the other six in the 3,120-bout constructed suite, held by a shared guard (kind_robots#5379). Constructed crews win 43.4–55.1%; first seat 52.4%.
- **Art:** 1,485 of 1,485 manifest slots return an image from production to a signed-in player (`npm run audit:slime-city-art-delivery`). All 300 cards have level-two and level-three paintings.
- **Real browser, signed in on production:**
  - keyboard-only and touch-only full matches (re-run on `db5d615`)
  - the Clash layout audit, 21 of 21 cases on `db5d615`: controls at 390/768/1440 with and without TAP, a held card at each width, the rail at three laptop sizes, and the result controls
  - all five tabs at 390 and 1440 wide: no console errors, broken images or page scroll
  - a Journey chapter from the first decision through the fight, a defeat and TRY AGAIN
- **Multiplayer on production:** a real duel between two test accounts, 18 of 18 checks: access control, hidden hands, turn order, a refused move from a stale tab, reconnect onto the same board, and forfeit.
- **Seven Clash defects** found by that pass. Six were fixed in kind_robots#5376 and the last in #5380:
  - a held card covered the middle alley on laptop and desktop widths, so a click could not place a card there
  - crew power buttons slid under the control strip on laptop-height screens
  - the three result buttons ran off the screen on phones and clipped their labels on desktop
  - the banner read VICTORY! when the rival won
  - boss life could read below zero
  - a signed-in local-play account was told to sign in
  - with TAP in the control row on laptop and desktop widths, the UNDO label was cut off
- **A production build break** in another game's page stopped every deploy from about 3:15 PM to 4:45 PM PT. Fixed in kind_robots#5372, with a guard that compiles every Vue template in CI.

## Known limits

- **Six cards the CPU rarely plays** (under 3% of the bouts they sit in): Maw-9000, Madame Chimera, Spare Nine Lives, Grease Oracle, Mark of the Procession and Breeding Hunger. Each costs both of a turn's plays. They work and are played; whether they are worth a whole turn is a question for human play.
- **Gamepad** is bound and unit-tested, but nobody has held a physical controller.
- **An achievement earned mid-match** opens the site's achievement dialog over the fight until it is dismissed. That is site-wide behavior, not Slime City's.
- **The scheduled layout audit** skips its Slime City step until a non-admin audit account exists as the `KR_AUDIT_USERNAME` and `KR_AUDIT_PASSWORD` repository secrets. The audit can be run by hand any time with a signed-in browser state.

## Owner decisions

- **t-009 and t-014:** your fun verdict and acceptance of the finished game.
- **t-015:** public launch and promotion. Nothing here authorizes either.
- **Device-journey import (t-063):** built as the written recommendation (a): offered only into a fresh account story, never carrying Tower cinders or records. You had not picked between (a), (b) and (c); say so if you want one of the others.
- **Audit account (optional):** add the two secrets above if you want the daily audit to cover Slime City.

## Human playtest checklist

1. **First visit, on a phone.** Sign in, skip the welcome tour, pick a crew. Does HOME explain itself without help?
2. **VS → FIGHT CPU.** Play a whole match. Try each way to play a card: tap it then a glowing alley, and drag it. Use UNDO once and your crew power once.
3. **End of the match.** Read the banner and the rewards report, then SEE BOARD, REWARDS, REMATCH and BACK TO VS. On a phone, nothing should run off the screen.
4. **On a laptop, with the browser at its normal size** (not full screen): hold a card and place it in the middle alley. Check that both crew powers and FIGHT stay reachable.
5. **JOURNEY, chapter one.** Make the three decisions, pick an approach, fight. Lose once on purpose: TRY AGAIN should keep your decisions. Win, and choose one of the two cards.
6. **Finish one crew's five chapters.** Check the ending, the gallery, the scrapbook page and the new card back and title.
7. **TOWER.** Enter the pit and climb until you lose or reach floor twelve. Does each fork change the next fight?
8. **COLLECTION.** Copy a deck, rename it, change a few cards and play it in VS.
9. **A friend duel** with two accounts on two devices. Close one tab mid-match and reopen it.
10. **Settings.** Large text, high contrast, reduced motion and Clash speed.
11. **The six rarely-played cards.** Put two or three in a deck. Are they worth a whole turn?
12. **Tone.** Do the six crews read as six different crews? Is the meat economy funny or just odd?

When reporting, include the tab, crew, deck, device and window size, the round, the exact card, and a screenshot if you can.

**Master issue:** [Kind Robots #4535](https://github.com/silasfelinus/kind_robots/issues/4535). It is flagged ready for human testing and closed as completed because agent production is complete. That is not a claim that anyone has played or accepted it.
