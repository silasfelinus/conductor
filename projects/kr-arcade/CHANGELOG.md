# kr-arcade CHANGELOG

## 2026-10-06
- Bolt Knight (the Ghosts 'n Goblins riff) re-themed as **Zuzu: Ghost Trail**, slug `zuzu-ghost-trail` (Silas:
  "our ghosts and goblin game should also be zuzu themed"): Zuzu in his comic canon on a haunted weird-west trail.
- Project scaffolded via intake.py
- Design brief, game catalog (games.yaml, 8 games from Silas's favourites) and roadmap written from
  Silas's in-session brief. Launch = Arcade tab + cabinet front end + leaderboard + Battery Maze and
  Rescue Rally; then the project goes continuous as a game factory.
- Queued 9 launch art requests (hall, cabinet, marquee, bezel, control panel, side art, intro splash,
  two game title pieces) for kind_robots public/images/arcade/, plus logo-style project icon/card/hero.
- Daily pitches can now target the arcade (`target: kr-arcade`).

## 2026-10-06 (later)
- Shipped through the factory: Sink Suds, Pipe Pals, Timber Bot, Butterfly Joust, Kind Pinball slices 1-2.
- Silas's second batch queued in games.yaml: Gloom Invaders (Space Invaders), Hedgehog Crossing
  (Frogger), Ribbon Riders (Tron), Burrow Buddy (Dig Dug), Repair Rampage (Rampage), Prize Show Panic
  (Smash TV), Bolt Knight (Ghosts 'n Goblins), Station Sweep (Xenophobe). Dragon's Lair became its own
  project, zuzu-lair.
- Touch play locks the cabinet to the viewport (silasfelinus/kind_robots#3276).
- Global leaderboard for every game (t-011, silasfelinus/kind_robots#3277): hall of fame API and hall
  section, pending-upload queue so no score stays stuck in one browser; per-game checklist updated.

## 2026-10-10
- **Timber Bot retired** (Silas: "the request timber falling game is questionable ethics, and I think we
  should kill it"). Removed from the arcade in silasfelinus/kind_robots#3438; games.yaml marks it
  `retired`, never to be rebuilt or re-pitched.
- **16-bit glow-up** (Silas: "Right now they all look like they could have come from an atari, and I want
  Super nes"). New milestone m6 and recurring task t-021: style upgrades come ahead of new games. The
  shared kit `utils/arcade/snes.ts` and the DESIGN-BRIEF "16-bit style bar" set the target. Sink Suds is
  the first cabinet upgraded (kind_robots#3438). games.yaml tracks `style: classic | snes` per cabinet.
- **16-bit glow-up complete** (Silas: "keep going, upgrade each until completed"). All 26 remaining
  2D cabinets were given the 16-bit render pass in five batches (silasfelinus/kind_robots#3451,
  #3453, #3454, #3455, #3456), render only, with tick-for-tick parity runs on eight of them. t-021
  done. Carry-outs: Ghost Trail's visual rebuild stays in m5 (t-013/t-014), and Kind Pinball's 2D
  no-WebGL fallback is follow-up t-022.
- **Ghost Trail becomes a real campaign** (Silas: "are we actually upgraded? at least an hour of content,
  multiple stages, boss fights, animations for all monsters" ... "keep working"). The four looping trails
  were replaced by six hand-built stages of 16 acts (19 relics), six headline bosses with telegraphed
  attacks (Grave Marshal, Bone Bull, Drowned Ferryman, Storm-Crow Matriarch, Bell Heretic, the two-phase
  Abbess) plus the Dust Devil mid-boss, 11 new painted foes, two new worlds (Storm Crow Pass, the Abbey),
  finite squads that stay down, save/resume per act, an ending and credits, a relic true ending and
  New Game+ (silasfelinus/kind_robots#3469, #3470, #3471, #3473, #3474, #3476, #3477, #3479).
  t-015..t-019 done; Zuzu's walk sped up at Silas's request ("zuzu play speed is a bit slow").
  The >=60-minute target is NOT verified: bot clear times are not human times, and the timed
  playtest stays open in t-020.

## 2026-10-11
- **Ghost Trail playtest notes** (Silas: "We should have checkpoints that don't send the player back to
  the beginning of the stage"; "The non-projectile sword is a bit lackluster"; "do we have a vertical
  level yet?"): close checkpoints, a boss-gate checkpoint and an in-game CONTINUE; saves resume at the
  checkpoint; the iai cut became a lunging crescent that cuts shots from the air; a vertical camera and
  THE BELL STAIR tower climb (silasfelinus/kind_robots#3488). Ghost Trail now has music -- a theme per
  world, boss and finale themes, an ending -- and its own sound effects (#3490).
- **Ghost Trail blueprint gaps closed**: River Croc ferries Zuzu across a flooded pool once the squad
  bothering him is down; the abbey's caged novice can be freed for an extra ending
  (silasfelinus/kind_robots#3496); Storm Crow Pass gets telegraphed lightning and a second vertical act,
  THE CLIFF ROAD (#3497). The campaign is now 18 acts and 21 relics.
