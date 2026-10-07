# Kind Robots Arcade — Design Brief

date: 2026-10-06
status: approved direction (Silas, in session, 2026-10-06)
author: Claude session (from Silas's brief)

## What it is

A free, in-browser arcade on its own **Arcade** tab in the Projects channel. You walk up to a row of
classic upright cabinets, pick one, watch its attract mode, press start, and play an original Kind Robots
game that riffs on a golden-age classic. Every game has an intro splash, rising difficulty, and a
three-initial high-score table. No LLM at runtime, no account required to play, all art pre-generated.

Silas, 2026-10-06, verbatim: *"users can play kind robots themed arcade games reminiscent of old games.
favorites personally were: joust, guantlet 2, mario bros, pinball. robotron, the logging game, that bubble
in the sink game, pacman. I want achievable games, with leaderboards, incremental challenge, intro splash,
classic retro looking style, stylish arcade cabinet frames, and playable in browser, for free."*

## Who it serves

Anyone who visits kindrobots.org, including kids (Silas's are 11 and 14) and the retro-arcade crowd. It
works on a phone in portrait with touch controls, on a tablet, and on a desktop with keyboard or gamepad.

## The two phases

1. **Launch (finite, `active`):** the Arcade tab, the cabinet front end, the shared engine kit, the
   leaderboard, and **two** launch games. This is milestone m2.
2. **Game factory (`continuous`):** once launch ships, the project flips to `continuous`. Building the next
   cabinet becomes standing fallback work, the same way animation-manager ships screensavers: an agent
   with no other task picks the next game from `games.yaml` and ships it (milestone m3, recurring task).
   Daily pitches can add new arcade games to that queue (see "Daily pitches" below).

## Look and feel — the cabinet

- **Classic upright cabinets** in the golden-age silhouette: a backlit marquee, a CRT screen behind a
  painted bezel, a control panel with a ball-top joystick and two or three buttons, coin door, and side art.
- **Kind Robots logo style** on top of that silhouette. Use the logo's palette of teal, pink, purple and
  gold, with candy-bright 80s Saturday-morning cartoon cel art. The two androids from the logo (the teal
  cat-eared android and the pink-haired android girl) are the arcade's hosts. Add a rainbow and a cosmic
  candy city in the side art and the hall backdrop.
- **The hall:** a neon arcade room at night with carpet, glowing cabinets in a row, and a rainbow neon
  sign shape with no lettering.
- **Retro screen treatment:** integer-scaled pixel art, an optional CRT scanline/curvature overlay (off
  under `prefers-reduced-motion`), and a bitmap pixel font for score, credits and initials.
- **Free play:** the coin slot reads FREE PLAY and there is never a paywall. PRESS START is the coin.
- **Generated art must contain no lettering.** All titles, scores and labels are rendered by the page in
  the pixel font over the art, so image models never have to spell anything.

## Every game ships with

1. **Intro splash / title card**: per-game art plus the game title in the pixel font.
2. **Attract mode** loop: title, a short scripted demo, how-to-play card, high scores, back to title.
3. **Incremental challenge**: waves or levels that ramp speed, enemy count and enemy types on a curve
   declared in the game module, plus a bonus round or intermission every few levels where it fits.
4. **Global leaderboard** (Silas, 2026-10-06: "global leaderboard is a high priority for all games"):
   top-10 all-time and today, worldwide, with three-initial entry on game over. Scores go through the
   arcade store (`submitScore`), never a board of the game's own, so they land in the shared
   `ArcadeScore` table and the hall of fame picks the cabinet up automatically from `ARCADE_GAMES`.
   Signed-in players are linked automatically.
5. **Controls** for keyboard, gamepad (Gamepad API) and touch (on-screen stick and buttons sized for
   thumbs). Pause on blur.
6. **Sound**: WebAudio chiptune bleeps and a jingle, muted by default until the first interaction, with a
   mute toggle that persists.
7. **Cabinet frame**: the shared marquee, bezel and control-panel chrome around the game canvas.

## Engine kit contract (kind_robots `utils/arcade/`)

Built once in t-004 so each later game is one module plus one registry row:

- fixed-timestep loop (60 Hz update, render on rAF), integer canvas scaling, and pause/resume;
- input map that unifies keyboard, gamepad and touch into abstract `up/down/left/right/a/b/start`;
- state machine `BOOT → TITLE → ATTRACT → PLAYING → GAME_OVER → INITIALS → SCORES`;
- HUD helpers (score, hi-score, lives, level), a pixel font renderer, and sprite-sheet helpers;
- a difficulty curve helper (`level → params`) so the ramp is data, not scattered constants;
- the game registry `utils/arcade/games.ts`: slug, title, riff, controls, `maxPlausibleScore`, art paths.

## Leaderboard (t-005)

- Additive Prisma model `ArcadeScore`: id, gameSlug, initials (3), score, level, optional userId,
  createdAt, and an index on (gameSlug, score desc). The migration is additive only, so it can merge
  after a line-by-line audit per AGENTS.md.
- `GET /api/arcade/scores/:game?range=all|today` returns the top 10. `POST /api/arcade/scores` validates
  initials (`A–Z 0–9`, small blocklist), the game slug against the registry, and the score against
  `maxPlausibleScore`, with a per-IP rate limit.
- It is a hobby leaderboard: the checks are plausibility checks, not anti-cheat. If the API is down, the
  board falls back to the browser's own local scores.
- **Global by default (t-011, kind_robots#3277):** `GET /api/arcade/leaderboard` is the hall of fame for
  every registered cabinet in one call (top 3, today's best, scores on the board), shown in the hall. A
  score that cannot reach the server waits in a per-browser pending queue and uploads on the next visit,
  on reconnect, or after the next successful submit; scores the server rejects are never retried.

## Game catalog

The queue lives in `games.yaml`, which agents edit. Names and art are original Kind Robots creations; the
riffs borrow *mechanics* from the classics, never names, sprites, sounds or level layouts.

| # | Game | Riffs on | Effort | Phase |
|---|------|----------|--------|-------|
| 0 | Butterfly Blaster | Asteroids (Silas's addition, 2026-10-06: rainbow butterflies vs mosquitoes, AMI tie-in) | small | launch |
| 1 | Battery Maze | Pac-Man | medium | launch |
| 2 | Rescue Rally | Robotron: 2084 | medium | launch |
| 3 | Sink Suds | Bubbles (Williams, 1982) | small | factory |
| 4 | Pipe Pals | Mario Bros. (1983) | medium | factory |
| 5 | Timber Bot | Timber (Bally Midway, 1984) — "the logging game" | small | factory |
| 6 | Butterfly Joust | Joust | medium | factory |
| 7 | Kind Pinball | pinball | large (sliced) | factory |
| 8 | Kindness Gauntlet | Gauntlet II | large (sliced) | factory |
| 9 | Gloom Invaders | Space Invaders | small | factory |
| 10 | Hedgehog Crossing | Frogger | small | factory |
| 11 | Ribbon Riders | Tron light cycles | small | factory |
| 12 | Burrow Buddy | Dig Dug | medium | factory |
| 13 | Repair Rampage | Rampage | medium | factory |
| 14 | Prize Show Panic | Smash TV | medium | factory |
| 15 | Zuzu: Ghost Trail (was Bolt Knight) | Ghosts 'n Goblins | large (sliced) | factory |
| 16 | Station Sweep | Xenophobe | large (sliced) | factory |

Rows 9-16 are Silas's second batch (2026-10-06). The table numbers them in the order he asked; the
build order is `games.yaml`, where the quick builds (Gloom Invaders, Hedgehog Crossing, Ribbon Riders,
Burrow Buddy, Repair Rampage) queue ahead of Kindness Gauntlet, and Prize Show Panic follows it because
it reuses Gauntlet's twin-stick input. Dragon's Lair is its own project (`zuzu-lair`), not a cabinet.

**Zuzu: Ghost Trail** (Silas, 2026-10-06: *"our ghosts and goblin game should also be zuzu themed"*) is the
one cabinet that leaves the Kind Robots logo style. It stars Zuzu in his comic canon look and tone, on a haunted
weird-west trail. The fighting game is `zuzu-showdown`, a separate project.

The launch games are the most achievable of the set (Butterfly Blaster, Silas's own addition, builds first): both use a fixed screen, simple collision and
well-understood enemy AI. Together they prove the engine kit for both maze/tile games and free-movement
arena games. Pinball and Gauntlet are deliberately last and get built in slices across several factory
cycles.

## Daily pitches

The daily pitch docket (`scripts/daily_pitches.py`, five pitches a day) may include Kind Robots arcade
games. A pitch with `target: kr-arcade` is a cabinet for this arcade, not a new project. When Silas
approves one, the next session appends it to `games.yaml` (`source: pitches/<stem>.md`), ahead of the
remaining catalog games. It does not scaffold a project with `intake.py`.

## Out of scope / guardrails

- No paid features, ads, coins-for-money, or LLM calls at runtime.
- No trademarked names, characters, sprites, music or level layouts from the original games. The games
  should be reminiscent of the originals, never copies of them.
- No violence beyond cartoon "bonk" and "reboot". Enemies are glitched or grumpy bots that get fixed,
  freed or sent home, which keeps it Kind.
- Leaderboard initials are filtered, and no free-text names are shown.

## Open questions (soft; defaults already chosen)

- The arcade tab's route defaults to `/play/arcade` in the `projects` channel.
- The default for two-player games (Pipe Pals, Kindness Gauntlet) is same-device co-op only, with no
  online multiplayer.
