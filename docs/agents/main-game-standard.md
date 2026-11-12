# Main-game quality standard

Silas, 2026-11-11 PT, in session:

> Our games should all have a base standard of quality: a settings menu, save/load,
> achievements, some sort of scrapbook, multiple endings, in most cases, customizable
> characters (with exception for early zuzu gamebooks), and multiple hooks to get the user
> to keep replaying: unlockables, persistent save states, branching pathways, etc.
> Three achievements was the standard for arcade games, those are smaller scale. We want our
> main games to have 12 plus achievements. There's no reasonable limit, some games may have
> them tied to each ending, but let's not go overboard.

This is the floor every **main game** must reach before it can be called finished or put in
front of Silas for a final verdict. It doesn't replace each game's own design. It's the shared
baseline underneath.

## Which games

**Main games** are the full-length, story or campaign games:

- Slime City
- Ecotone: Weird Humboldt
- Zuzu Gamebook
- Zuzu: Shifting Lands
- Emperor of Dust
- Rainbow Bullet Hell Space Princess
- Save the Plumber
- Shifting Desks
- Memory Dungeon
- Terrors on Crystal Street
- The Ruler Is Hooked
- Cthulhuquarium
- Prom of Doom (`comet-city-academy`)
- Space Couch (`game-of-captains`)
- Every Villain Tactics
- MONSTRIQUE (`monstress-convention`)

A new full-length game joins this list when it's created. Paused or finished main games
(Zuzu's Lair, Zuzu Showdown) meet the standard if they're reopened.

**Arcade cabinets** (`kr-arcade`) and small toys keep the smaller arcade standard: three
achievements, plus settings and save where the game has progress worth keeping.

## The standard

1. **Title screen.** It offers New Game, Continue, Settings, Scrapbook and Achievements. The
   MONSTRIQUE console (kind_robots#4848) is the reference.
2. **Settings menu.** Reachable from the title screen and during play. At minimum:
   - music and sound volume
   - text size and reading speed
   - reduced motion and high contrast
   - reset progress, with a confirmation step

   Settings persist between visits.
3. **Save and load.**
   - Progress autosaves, and Continue picks up exactly where the player left off.
   - A page reload never loses progress.
   - Run-based games keep their unlocks permanently, separate from any single run.
   - Signed-in players get an account-backed save where the game has one, with local
     storage as the fallback.
   - Saves are versioned, so updates never wipe them.
4. **Achievements: 12 or more.**
   - Each is a live Achievement record created through the site's achievements API, with a
     unique `triggerCode` prefixed by the game slug.
   - Each is awarded in game and shown with `components/achievements/game-achievement-strip.vue`.
   - Mix story, skill, discovery and completion achievements. Tying some to endings is fine,
     but don't overboard: usually 12–30.
   - The pull request verifies one award live after deploy.
5. **Scrapbook.** A persistent collection of what the player has found:
   - endings earned
   - characters met
   - art unlocked
   - a page for each finished run (choices, losses, outcome)

   Unfound entries show as locked silhouettes with an "X of N found" count. It survives new
   runs, rewinds and reloads.
6. **Multiple endings.** Several earned endings, each with its own text and **its own painted
   plate** queued through a conductor art ledger. One generic "THE END" doesn't count.
7. **Customizable characters**, in most cases. Choose or design the player character (name,
   look or portrait, and stats where the genre has them), and the story adapts to who the
   player is.
8. **Replay hooks: at least three.** Pick from:
   - unlockables that carry into the next run
   - persistent saves or new game plus
   - branching paths
   - seeded or randomized content
   - difficulty modes
   - collectibles
   - alternate starting characters

## Character exceptions and decisions (Silas, 2026-11-11 PT)

- **Zuzu Gamebook keeps its fixed protagonist, Zuzu.** No character customization. Every other
  item in the standard still applies.
- **Zuzu: Shifting Lands gets a character creator with adjustable stats.** This is what sets it
  apart from the gamebook.
  - Playable characters include **Zuzu** and **Jeffery Mittens** (the young raccoon looter
    from Book One).
  - Encounters adapt to who is playing. For example, a player can't play a fennec sibling and
    then meet the siblings as strangers.

Any other exception to item 7 is Silas's call. Record it here when he makes one.

## How agents apply it

Each main game has a roadmap task titled "Main-game standard: …", plus an achievements task
unless one already exists. The standard task starts with an **audit**: a table, one row per
item above, marking each Met, Partial or Missing with evidence (file, route, live record). The
audit goes in the task note and the first PR. Close the gaps in small CI-tested PRs.

Art needed for endings, scrapbook entries or character portraits goes into a conductor art
ledger, auto_submit, so it renders without waiting for anyone.
