# Nightmare on Crystal Street: design brief

Working title (Silas, 2026-10-24 PT). A full single-screen, console-style 80s horror-comedy
card adventure. One week on an idyllic suburban cul-de-sac beset by one of twenty-two nightmares (many flipped or bent classic villains);
days for investigation and friendship, nights for survival. Creepy but fun, camp as a weapon,
queer theatre and LGBT+ joy at its heart.

- **Runtime:** kind_robots `/admin/crystal-street` (admin-only development preview, per the
  admin route contract). Moves to `/play/crystal-street` only when Silas releases it.
- **Content:** kind_robots `utils/crystalStreet/` (JSON validated by `validate.ts`). Rules and
  rosters: [WRITING-GUIDE.md](WRITING-GUIDE.md). Complexity benchmarks: Emperor of Dust (days,
  followers, ledgers), Ecotone (companions, many endings), Shifting Desks (dealt encounter cards,
  no clean wins) and Shifting Lands (illustrated decks pulled by tag).

## Silas's brief (2026-10-24 PT, condensed)

Nightmare on Elm Street remix in an idyllic suburb; creepy, 80s-fun exploration of horror,
camp, slasher genres, queer theatre and LGBT+ positive themes. One week on Crystal Street (name
open), a malevolent entity, **20+ villains**. Each round is Day or Night. Days: library, gym,
traveling pawnshop, school and more, gaining information, solving daylight adventure beats,
developing skills. Nights: encounters unique to the entity, or randomized pulls from decks
matching its tags (a paranormal entity pulls from the paranormal deck, e.g. teleported to the
Junkyard's maze of endless cars, which pulls another encounter). Inventory. **20+ companions,
10 active max**, each with a range of emotions in illustrated and poster formats. Multiple
endings depending on whether the villain's central issue was explored and enough interesting
encounters were rolled successfully; **one Best ending per antagonist**; every run recorded in
a **scrapbook**. Memorable scenes, captivating backstories, and many choices with 2+ options
whose positive and negative outcomes all get art.

## The re-cast: flipped and bent classics (Silas, 2026-10-24 PT)

The nightmares start as gender-flipped or gender-bent takes on classic movie villains,
not all of them. The aim is to name the stereotype each original leaned on (the queer-coded
seducer vampire, the man in makeup as predator, sex as a death sentence, the killer-in-a-dress
reveal, the purity rule) and find what the story gains from a queerer, different angle, without
ever making gender variance or transness the scare. The roster is now 22: Counselor Chad
became Counselor Jess (Jason flipped), Screwhead became Magda Szabo (Pinhead flipped), and two
were added: The Shape in the Cardigan (Michael Myers flipped) and The Final Cut (the killer-reveal
trope itself as the villain). Each villain carries an `inspiration` block (original, film,
year, flip/bend/remix, old script, new lens), shown on the arrival splash and the case board.
Full table: [WRITING-GUIDE.md](WRITING-GUIDE.md#the-re-cast-classic-villains-flipped-and-bent-silas-2026-10-24-pt).

**Cover art (Silas, 2026-10-24 PT):** the approved gender-swapped Jason from the Hollywood
Monsters Recast coloring book ("Masking Up", `projects/coloring-book/sets/monster-recast/approved/masking-up-color.webp`).
It is the title-screen hero, the project icon/card/hero, and Counselor Jess's poster.

## Core loop

1. **New week.** Name, pronouns (free text), one of six 80s archetypes (Jock, Brain, Theatre
   Kid, Burnout, Prep, Weirdo; nine skill points each). Nightmare: "Surprise me" or any
   nightmare already met (to chase its Best ending).
2. **Day (3 actions).** Pick a pin on the Glimmer Falls map. Each location offers: a
   **daylight beat** (4 authored adventures per location, villain-agnostic), **follow a lead**
   (the nightmare's clue at that place, once revealed), **meet a companion** (an authored
   first-meeting scene; success recruits), **ask a friend back**, **train** the location's
   skill (once a day, to 4), **rest** at home (+2 nerve), or **shop** at Oddment and Daughters,
   the traveling pawnshop (five random items daily, parked somewhere new).
3. **Night.** Dread rises by one. Night 1 reveals the nightmare (poster, epithet, taunt).
   Nights 2, 4 and 6 deal its **signature scenes** in order; the rest are pulls from the
   **tag decks** it shares (paranormal, slasher, creature, cosmic, tech, camp, cult, dream).
   Outcomes can **teleport** you into another deck's card the same night (once per night).
4. **Halloween (night 7).** The finale offers **fight** (usually brawn 11), **trick** (usually
   9) and **heart** (requires all 3 leads; resolves the central issue).
5. **Ending and scrapbook.** Every week is pasted into the scrapbook with its ending, crew,
   leads, wins and highlight moments.

## Rolls and resources

- Every choice rolls **2d6 + skill + crew (+1 when any active friend has that skill) + best
  item (+1) + choice bonus (a named friend, item or earned flag) + ward (+2 when you carry the
  item or friend that wards the card's tag) − night** (at night: −1, and −1 more per 4 dread)
  against **7, 9 or 11**. Twelve always succeeds, two always fails. Odds are shown on every
  choice.
- **Nerve** 0-10 (start 7) is health: zero means you are Taken. **Dread** 0-10.
  **Quarters** buy gear. **Night wins** count successful rolls after dark (finale included).
- Failed night rolls can leave a friend **shaken** until dawn (no bonus).
- **Perks:** dawn nerve (+1 total however many friends have it), dawn quarters, one reroll and
  one shield (cancels a failed night roll's nerve loss) per phase across the whole crew, clue
  sense, tag wards. Perks do not stack, so a full crew is broad rather than invincible.

## Endings (4 per nightmare, 80 total, 20 Best)

| Tier | Condition |
| --- | --- |
| Best | Heart succeeds and the week had at least 10 night wins |
| Good | Fight or trick succeeds, or heart succeeds with fewer than 10 night wins |
| Bittersweet | Finale fails with nerve above 3 |
| Taken (bad) | Nerve reaches zero at any point, or finale fails with nerve 3 or less |

The scrapbook tracks all four per nightmare and shows **Best endings X/20**.

Balance (contract test, 400 seeded autoplayed weeks with a near-optimal policy, 2026-10-24):
Best 49%, Good 17%, Bittersweet 28%, Taken 6%; every nightmare's Best ending is reached.
Human play should land lower; roadmap t-006 tunes from real play.

## Companions

22 friends (crew limit 10), each with bio, pronouns, age, role, 1-2 skills, a perk, a palette,
a full-body **poster** prompt and six **emotion** portraits (neutral, happy, scared, angry, sad,
determined). The game picks the displayed emotion from play: happy after a daylight win,
determined after a night win and during the finale, scared after a night loss or while shaken,
angry after a daylight loss, sad or happy at the end. The crew panel lets you browse every mood
and flip between portrait and poster formats.

## Art

Every encounter carries a scene prompt, every choice outcome a success and a failure prompt,
every ending, location, item, villain (poster and portrait) and companion (poster plus six moods)
its own prompt. Until rendered art exists, the game draws code-built SVG scenes (seeded skyline,
moon, Heartstone, villain silhouette and palette) and keeps an image-sized slot that swaps to
the painted file at `/crystal-street/<kind>/<id>.webp` once delivered. Round 1 queues key art,
villain posters, companion posters and mood portraits, and locations
([art/ROUND-1.yaml](art/ROUND-1.yaml)); encounter and outcome plates follow in later rounds.

## Guardrails

- Queer-positive rules in the writing guide are non-negotiable: queerness is never the monster.
- PG-13 horror; bad endings mean Taken, not killed. No slurs. Parody names for real brands.
- Parody villains (Frieda Krueger, Screwhead) are original characters, not licensed ones.
- Admin-only until Silas accepts the visual state and approves a public release.

## Title alternatives

Silas asked for other names worth considering. "Crystal Street" keeps the Elm Street rhythm and
nods to Crystal Lake; alternatives:

- **Nightmare on Lavender Lane** (lavender as queer history, a sweeter suburban sound)
- **Seven Nights on Crystal Street** (says the structure out loud)
- **Slumber Party on Sapphire Court**
- **Glimmer Falls After Dark** (the town, not the street)
- **Halloween Week on Heartstone Drive** (names the geode at the street's center)
