# Superkate's Spectrum: human playtest checklist

**Prepared:** 2026-11-25 PT, after kind_robots#5816 and #5823. **Where:** Arcade, then the Superkate's Spectrum cabinet.
This is a handoff for people to play, not a gate the build roadmap waits on. Agents verified everything
in "Already machine-verified"; humans are asked only for what a machine cannot judge.

## Already machine-verified (on every cabinet PR)

- **Whole campaign beatable through real shots.** `verifySpectrumCampaign.test.ts` plays all 30
  Story boards and all 6 bosses on three choice routes, reaching all three endings (prism-partners,
  open-city, wild-colors), with every stage starred and all chapter trophies earned.
- **Careless play.** 12 visits and ~1,800 random shots found no hang, no relocked stage, no XP loss,
  and no erased save on game over. Each next visit opens on the furthest stage.
- **Co-op Relay.** Six boards plus the duet boss are solvable with each player's own orbs.
  **Atelier.** All 12 puzzles are solvable with their fixed orbs.
- **Real cabinet in Chromium.** `verifySuperkateSpectrumCabinet.browser.test.mjs` covers 390 and
  768 px by touch, and 1440 px by keyboard and gamepad: hub tabs, stage start, aim and fire, the
  power tip, all six bosses rendered, save → reopen, game over keeps progress, and relay turns.
  The touch controls never cover the board.
- **Hub.** `verifySuperkateSpectrumHub.browser.test.mjs` covers the Scrapbook (earned and locked
  memories), all trophy pages, every setting including the music and effects levels, the in-game save
  state, and site achievements awarded once.
- **Two devices, one account.** `verifySuperkateSpectrumAccounts.browser.test.mjs` covers guest
  adoption, a second device, a stale-device 409 merge, an account switch and an outage, all on the real
  sync code against a mock server.
- **Engine, save and audio suites.** Boards, bosses, cloud-save merges and races, 14 recorded music
  masters, and a music-versus-effects balance check.

## Please play and tell us

1. **First five minutes (phone, portrait).** Does tapping START, choosing stage 1, then dragging to
   aim and releasing to fire feel obvious without reading help? Is anything hard to read?
2. **Feel of aiming.** On phone, tablet and desktop, do bank shots go where the dotted guide says?
   Is keyboard aim speed comfortable? Try a real gamepad if you have one.
3. **Difficulty curve.** Play Rainbow Salon (stages 1–5) and its Greyscale Dryer boss. Too easy,
   right, or frustrating? Note the stage where you first lost a heart.
4. **Power orbs.** When the first Prism, Burst or Ribbon card appears, is it clear what to do?
5. **Story.** Do the choices after stages 5, 15 and 25 feel meaningful? Was the ending you reached
   satisfying? (Three exist.)
6. **Sound on a real device.** Phone speaker and headphones: are music and pops balanced? Try MUSIC LEVEL and EFFECTS LEVEL in
   Settings. The levels are balanced by measurement; only ears can judge the real speaker.
7. **Two devices, signed in.** Play a few stages on one device, sign in on a second device and
   confirm the stars and stage carried over, guest progress was adopted, and nothing went
   backwards. The hub's Settings page shows the save state. The sync logic is machine-verified against
   a mock server; this confirms the deployed server and database.
8. **Co-op Relay with two people on one device.** Classic card → LEFT or tap Relay. Is the turn
   passing clear? Is the gifted Prism noticeable?
9. **Look and feel.** Is the hub (Play, Scrapbook, Achievements, Settings) attractive enough for the
   showcase shelf? Anything that looks unfinished?
10. **Scrapbook memories.** Beat a district boss and open the Scrapbook. Do Superkate's district
    illustrations look right on the memory cards (Silas approved them in-game 2026-11-25, t-189)?

## Decisions only Silas or Kate can make

- **Visual acceptance (t-184)**, and moving the cabinet from the `growing` to the `showcase` shelf.
- **Any deploy or public promotion.**

Report findings as Conductor tasks with `playtest_iteration: true` under `kr-arcade`, or as comments
on kind_robots#4062.
