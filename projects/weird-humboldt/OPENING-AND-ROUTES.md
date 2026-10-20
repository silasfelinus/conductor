# Ecotone: the event opening, the two routes and the endings (2026-10-20 PT)

**Authoritative.** This doc supersedes the prelude and companion-introduction sections of
[PRELUDE-STATE-CONTRACT.md](PRELUDE-STATE-CONTRACT.md) and
[JOURNEY-LOOP-CONTRACT.md](JOURNEY-LOOP-CONTRACT.md). It drops two older rules:

- the opening lens no longer maps straight to a first companion;
- the run is no longer one unnamed festival weekend.

The crossroads, stay-or-follow, seeded cards and visible 2d6 rules stand. Built in kind_robots #3872 (t-032). The Playbook Manager (t-033) is the admin view and editor for all of it.

## Silas's direction, 2026-10-20 PT

- Every initial story draw is at least a binary choice: "white rabbits" to chase. An Alice riff with a Humboldt twist is welcome.
- The first choice is which event to attend:
  - **Fictional cannabis festival:** marijuana and psychedelics, the forest nymph (Juniper) and Kit.
  - **The Kinetic Sculpture Race:** the real race with a fictional afterparty. It leads to Cedar, alcohol, party drugs and the tattoo artist (Mara).
- Order inside an event: choose the area first (who you'll meet), then the offer by "some encounter", then interact with the companion and choose them **or not**. The loner path is real and has its own endings.
- The Kinetic route must reach a resolution where the protagonist is **conscripted to fill in for a last-minute racer injury**, races with the companion, then has a series of days of adventures. Longer than a weekend is fine.
- A psychedelic opening stays psychedelic all story.
- The through line:
  1. meet a companion;
  2. explore together, with weird experiences and skill checks;
  3. the event, companion and lens choices show **the Humboldt of your future**, which succeeds or fails on end-of-journey stats.
- Companions weave in and out and can be re-met on later days in other capacities.

## As built

**The opening.** A white rabbit in a racing helmet hops past two flyers on the Arcata Plaza ("Late, late, the fog won't wait"). You pick an event:

| Event | Area → companion | Offer (lenses) | Days |
| --- | --- | --- | --- |
| **The Green Ribbon Fair** (invented cannabis harvest fair at the forest edge) | Partner acro on the lawn → **Kit**; drum circle in the woods → **Juniper** | Sober, Stoned, Tripping | Fri–Sun |
| **The Kinetic Grand Championship** (real race; invented afterparty, teams and anomalies) | Pit row → **Cedar**; the tattoo table → **Mara** | Sober, Tipsy; The Fast Track and Everybody Loves Everybody shown locked "Being written" | Sat–Wed |

Each event has three beats: area (`prospect`), then offer (`lens`, with its check), then "Someone Worth Following". In the last one you travel together, or "go it alone" (Nerve +1). The texts vary by prospect.

**Green Ribbon route:**
1. **Day 1:** GR-1, GR-2, GR-3, then the Friday-night fork (Arcata cards).
2. **Day 2:** GR-4 *The Path Behind the Stage*, a looping forest trail with a banana slug in a racing helmet. Then the Saturday-coast fork, then the crossroads.
3. **Day 3:** the Sunday-in-Eureka fork, then GR-5 *The Closing Bonfire*: one petition to protect the forest, one to buy it.
4. Finale.

**Kinetic route:**
1. **Day 1:** KN-1 *Race Morning on the Plaza*, then KN-2 *The Afterparty* (the offer), then KN-3.
2. **Day 2:**
   - KN-4 *Conscripted*: Dot, pilot of the Banana Slug Express, sprained her ankle on the afterparty floor. You choose pilot, navigator, or talk the crew into taking Dot along.
   - KN-5 *The Bay Crossing*.
   - The Sunday-night Eureka fork.
3. **Day 3:** KN-6 *The Ferndale Finish*: the Eel River, Victorian Main Street, an invented dead dairyman on the cemetery hill, and helping the octopus team.
4. **Day 4:** the crossroads, then the Tuesday-coast fork.
5. **Day 5:** the back-in-Arcata fork.
6. Finale.

**Forks.**
- Each one deals up to three face-up encounter cards from its region pool, seeded and never one already played this run.
- It tops up from the rest of the county if a pool runs dry, so every fork offers at least two.
- A fork is the "where to" at the start of a day.

**The crossroads.** A seeded newcomer from the companions not yet met: stay with your guide, keep going alone, or follow. The prospect you declined counts as met. Kit can turn up on the race route as a fellow racer, the "different capacity".

**The lens.** `openingState` is immutable and sets each card's lens line. `clarity` stays at the offer's level all run.

**Endings: the Humboldt of your future.**
- An ending ID is `<lead|alone>.<opening lens>.<hope|dark>`: 5 × 7 × 2 = **70 slots**.
- The fate is hopeful when goodwill + evidence + a nerve modifier (+1 at nerve ≥5, −1 at ≤1) reaches the route's bar: **5** for the fair, **7** for the race.
- A 4,000-run random-play simulation landed near 50/50 overall (about 58% hopeful on the fair, 44% on the race).
- The end screen shows the math.
- The finales are first drafts:
  - one core epilogue per lead and fate;
  - a signature title and line per lead × open lens × fate (companion titles from ECOTONE-32-ENDINGS.md, plus 8 new Alone titles);
  - a lens coda.
- Earned endings unlock in the gallery. The full 1/10/30-year epilogues are still to write.
- Cedar's parents stay together in both his futures.

## Still open

- The party lenses (cocaine, MDMA, meth) need their offers, outcomes and lens lines before they unlock.
- Art for the new beats (GR-2..5, KN-2..6, the forks and the endings) waits on the checkpoint bake-off picks (art/CHECKPOINT-BAKEOFF.yaml).
- Longer epilogues, more cards per region, and history threads (t-030; Tuluwat material still needs Wiyot consultation and Silas's approval before it ships).
