# Ecotone: the seeded journey loop and companion crossroads

> **Superseded in part, 2026-10-20 PT:** the opening (event choice, then area, offer and companion or nobody), the two routes and the 70 endings are now in [OPENING-AND-ROUTES.md](OPENING-AND-ROUTES.md). Where this doc maps an opening lens straight to a first companion, that doc wins.

**Updated seven-lens user-directed structure, 2026-10-19 PT. Design only; no art, Play implementation or publication authorized.** This replaces any suggestion that the player selects an arbitrary companion as soon as the prelude ends. The *first companion is introduced by the freely chosen opening state and its scripted scene*, then later changes happen through authored crossroads. The original four opening-to-guide mappings are retained; the three added openings need their own written first-guide meetings. Later companion changes happen only during **authored encounters** with the other companions.

## One adventure, two layers

**Fixed dramatic spine:** Prelude → randomized side stories → meaningful encounter with another main character → **stay or follow** → more randomized stories → further companion meeting / stay-or-follow decisions → companion-deepening beats → county-fate finale and 1/10/30-year epilogue.

**Variable adventure body:** Most between-crossroads encounters are drawn from the **120 individually written canonical card records** and conditional pools. The set, order, dice results and choices permanently change stats, evidence, relationships, resources, reputations and chances of a hopeful or dark future. *Major crossroad meetings are guaranteed authored anchor scenes*, never rare random draws. The player can be surprised and even fail, but isn't robbed of the story by an unlucky deck.

### Prelude: sobriety chooses first companion

| Voluntary opening choice | First companion met |
| --- | --- |
| Sober | Mara (working name) |
| Tipsy | Kit |
| Stoned | Juniper |
| Tripping Balls | Cedar (working name) |
| Cocaine | One established companion, introduced through a newly authored scene (TBD) |
| Meth | One established companion, introduced through a newly authored scene (TBD) |
| MDMA | One established companion, introduced through a newly authored scene (TBD) |

These are **initial meetings, not permanent lead assignments**. The protagonist chooses whether to accompany this character as the initial guide; declining must still launch a playable solo/catch-up track and produce opportunities to join companions later. `opening_state` stays fixed as the story lens and collectible-ending dimension. `current_state` and `clarity` can evolve naturally; the user does not have to remain intoxicated, and all essential facts, hopeful trajectories and potential followers are reachable when the player is sober.

### Suggested six-chapter pacing, subject to authoring review

| Stage | Guaranteed dramatic anchor | Randomized side adventures | Player's choice |
| --- | --- | --- | --- |
| Prelude | Initial companion introduction keyed to opening state | One scene demonstrating story tone/skills | Accept guide or travel independently |
| Chapter 1 | Local mystery and companion-specific initial motivation | ~2–4 regional encounter cards | Shape skills, alliances and early evidence |
| Chapter 2 | **Crossroads 1:** meet a second member of the four-person main cast | ~2–4 cards before/after | Stay with current companion or follow newcomer |
| Chapter 3 | **Crossroads 2:** meet a different as-yet-unmet main companion | ~2–4 cards | Stay/follow, with prior choice remembered |
| Chapter 4 | **Crossroads 3:** meet the fourth main companion | ~2–4 cards | Stay/follow; establishes late-route stakes |
| Chapter 5 | Deepening and payoff of the **currently active companion's** personal arc (with route-history callbacks), county coalitions converge | ~2–4 cards + deterministic recovery anchor | Honour, complicate or betray accumulated commitments |
| Chapter 6 | County-fate convergence and character resolution | Curated/conditional surprises and finale checks | Consequences resolve, earned hope/dark finale |

This schedule ensures **every main character is encountered in every run**, though the order of second/third/fourth meetings is a **seeded permutation** of the other three, weighted by location/plot compatibility. Optional revisits allow a previously left-behind companion to reappear, but are not required for the 16 cross-combinations to be reachable. For a switch at Crossroads 3 to have a fully developed personal route, Chapter 5 must provide **authored catch-up/deepening beats** as well as earlier evidence/flags from side cards; never require completing an impossible number of earlier active-companion-only scenes. A late switch changes the *cost* and texture of the arc, not the availability of all hopeful outcomes.

**After a swap:** the former companion **stays in the world**, pursues personal work and may react later; they don't vanish from the map, die or join a permanent four-member procession. One **active lead** travels with you at a time. Other main characters are encountered, have their own ambitions and might be followed, declined or re-met. Leaving a companion may alter trust and knowledge without implying moral failure.

## A consequence engine, not a roulette wheel

A seeded random generator chooses eligible authored side cards through weighted pools keyed by **region/chapter, already seen IDs, encounter flags, active companion, stats and local conditions**. Card selection can surprise players, but never invent facts or deadlock mandatory scenes. A card's conditional narration and choices may refer to companions' earlier meetings and the journey's actual timeline.

**Each side card must have:**
- Its own unique canonical ID, location and 2–4 actual choices with authored consequence text, not generative filler.
- At least one consequential resource, **five-skill** (`Rizz/Burly/Wits/Local Lore/Psyche`) or relationship/evidence/faction/land-use effect. Dice checks use the existing clearly shown **2d6 + skill + context modifier** contract; failures have authored consequences and occasional recovery opportunities.
- At least one callback key that later crossroad/finale scenes could reference. Not *every* card needs to feed the grand mystery, but each should matter locally, mechanically or emotionally.
- Optional **current-state** flavor/check adjustments and **opening-history** callbacks when appropriate. The past state colors how the relationship began; present Clarity or condition affects the current interaction. Sobriety does not predetermine character morality or outcome.
- A validity/consistency guard: no visit to an NPC not yet met as if already a friend, no resurrection of a collapsed site, no repetition after unique rewards, no conflicting location/date facts. Seed/save/reload reproduces the same eligible draws and roll results.

**RNG tuning proposal:** ~2–4 randomized encounters per interlude, with roughly 10–18 random side-card encounters across one weekend. Retain the ≥120 distinct written pool target for cross-run variety, six-region structure and a plausible 45–75-minute individual journey. The **32 ending stories are additional authored epilogues, not part of the 120 random encounter cards**. These counts are authoring targets to test, not completed content.

## The choice to stay or follow should matter

At each guaranteed meeting, write a real event involving **both** the current lead and the newcomer, followed by an explicit choice: **Stay with [current]** / **Follow [newcomer]** (plus a contextual solo/defer alternative only where story-appropriate). Neither option is a mere character avatar swap.

- **Stay:** deepen current companion's motivation and trust; newcomer remains available for later interactions or unresolved promises. Earn a special stay callback; do not immediately replay the same "meet" scene.
- **Follow:** leave current companion behind to pursue their own path; switch the active companion; pick up a different set of plot lenses, obligations, clues and encounters. Preserve earlier trust, betrayals and evidence.
- **Meeting order matters:** `meeting_order` logs the original four-person sequence; `follow_history` logs each active-companion transition with chapter, location and reason; `current_lead` holds one person or none. The later scene pulls from history without generating bogus claims that the player had met someone earlier.
- **Relationship depth:** each main companion should have at least one scene about a real internal contradiction, one costly commitment and one earned payoff. Content scales by whether the companion was first encountered, newly followed or left and re-met, without locking a late follower out of meaningful hope.

## Example: identical final companion, different roads

Both players **finish with Cedar** and both eventually achieve a locally accountable **technoutopia**:

1. **Tripping → Cedar from the beginning:** An impossible CB signal inspires the first lead. Random forest-safety and equipment cards determine whether Cedar responsibly verifies it before advocating a transparent computing/broadband cooperative.
2. **Sober → Mara → Kit → Cedar:** First the protagonist helps document a shop lease and a fair paid arts workshop, then follows a practical technician. Cedar's broadband co-op includes affordable studio connectivity and transparent contracts because of the earlier choices.
3. **Stoned → Juniper → Cedar:** Habitat commitments and ordinary birdlife are established first. Cedar's network may fund legitimate watershed sensors and protect wildlife corridors, or threaten them if the player ignores evidence.
4. **Tipsy → Kit → Juniper → Cedar:** Social allies and an ecological warning meet at the last crossroads. Cedar can bring artists, workers and ecological monitors together, but social trust lost in previous cards can damage the coalition.

Those four paths have **four different collectible Cedar hopeful ending IDs** because their `opening_state` differs, but should also vary internally based on **meeting order and side-card flags**. Two runs with the **same** opening and final lead still get recognizable different callback paragraphs, people and civic details based on their encounter order; such variation is not a 33rd collectible ending.

## How 56 journey signatures resolve

`ending_id = final_lead + "." + opening_lens + "." + outcome`, with 4 active final leads × 4 opening lenses × earned hope/dark = **32 stable collectible outcomes (16 of each)**. `final_lead` means the **last actively followed companion**, not the companion initially introduced. A solo path must get an authored, explicit rejoin/commit choice before the finale, or define a deterministic compatible fallback without inventing a new 33rd ending; do not silently assign an unseen lead. The screenplay must make the commitment legible.

Hope/dark is resolved by **accumulated decisions, evidence, friendship, repairs, compromises and visible dice outcomes**. A single last-minute dice failure alone must not undo the player's earned arc. There can be honest difficult endings and horror, yet the project's moral center is that outcomes are changeable. A dark ending may still preserve a person or an opening to repair; it does not necessarily mean a companion is evil.

The former **ten civic-future names** (Redwood Commons, Silicon Estuary, Global Terminal etc.) remain **scenario motifs and world-state descriptions** usable in multiple endings, not ten more collectibles. Cedar's hopeful path now specifically includes accountable broadband, distributed/reliable technology, skilled work, field monitoring, ecologically literate engineering and genuine local agency. In every possible future, **Cedar's parents remain a couple**.

## State contract and testable invariants

Suggested engine fields (adapt schema to existing reducer; not yet code):
```ts
type OpeningLens = 'sober' | 'tipsy' | 'stoned' | 'tripping_balls'
type CompanionId = 'mara' | 'kit' | 'juniper' | 'cedar'
type Fate = 'hope' | 'dark'
type JourneyState = {
  seed: string
  opening_state: OpeningLens           // immutable lens from prelude
  current_state: OpeningLens           // may change; not a moral score
  clarity: number
  intro_companion: CompanionId         // determined by opening_state
  active_lead: CompanionId | null      // changes only via authored stay/follow/rejoin
  meeting_order: CompanionId[]        // each of the 4 once on first meeting
  follow_history: Array<{ chapter: number; from: CompanionId | null; to: CompanionId | null; choice_id: string }>
  encounter_seen_ids: string[]
  companion_flags: Record<string, boolean | number>
  civic_flags: Record<string, boolean | number>
  skill_changes: Record<string, number> // validated against skill caps/contract
  outcome?: Fate
  ending_id?: string                   // only set by real finale
}
```

**Acceptance cases:**
1. All four first meetings are correct for the prelude; no separate initial companion picker. The next three first-time companion meetings form one consistent shuffled permutation of the *remaining three*, never a duplicate in the mandatory beats.
2. Stay, switch and leave-behind decisions persist and alter the next authored chapter and finale. Every `opening_state × final_lead` is naturally reachable via offered companion meetings, and both hope/dark are reachable through valid choices/rolls.
3. Two journeys with the same seed and choices produce the same encounter/meeting order/check outcomes after save/reload. Different seeds demonstrably produce varied side encounters and multiple companion permutations without deadlocked anchor beats.
4. All 56 ending IDs are naturally reachable (and 28/28 hopeful/dark), not injected into a fake save; every lens still has hopeful paths and no substance-specific universal penalty.
5. Stats and earned resources change through side cards and affect later rolls, reactions and outcome eligibility, while all reachable story content remains authored and no massive stat inflation bypasses decisions.
6. Nondefault companion order/relationships yield real different dialogue/callbacks at later fixed scenes and in 1/10/30-year epilogues, **without** multiplying the collectible ending count.
7. Each companion has a realistic full personal arc even when followed at the last guaranteed crossroad; if content needs extra deterministic anchor scenes, include them.
8. One-screen mobile/tablet/desktop game board survives all cards, crossroad decisions, dice UI, Companion/Journal/Endings tabs and the 56-slot gallery. Only internal bounded panes scroll.
9. The ten civic future motifs remain optional world-state settings. Real historical atrocities and Luna's record never change. Existing cultural boundaries remain.
10. Preserve user creative gates: text/design is allowed; **no art queue, unapproved gameplay deployment or publication**.

## Three additional full opening lenses and optional choice-driven short roads (2026-10-19)

**Supersedes the mandatory detour design.** Cocaine, meth and MDMA are now three **full valid opening lenses**, not three forced terminal side stories. Their first guide is revealed through an authored scene featuring one of the four companions; the remaining three companions still appear through seeded guaranteed Stay/Follow encounters. All three openings can lead to any final companion and either hope/dark fate. A voluntary **short road** may be taken from any opening when it is earned by decisions and clearly offered, but the opening drug never automatically ends the journey. The new total is **56** main collectible IDs (28 hopeful/dark), with **8 curated core finales + 56 distinct paragraph/image-prompt signatures + selected real-choice callbacks**. Do not require 56 full independent 1/10/30-year epilogue sequences. See [ECOTONE-ENDING-GRAMMAR.md](ECOTONE-ENDING-GRAMMAR.md) and revised [OPTIONAL-DETOURS.md](OPTIONAL-DETOURS.md). Single-screen, art and publication gates unchanged.
