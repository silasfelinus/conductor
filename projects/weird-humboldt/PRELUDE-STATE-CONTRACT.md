# Weird Humboldt: Festival Prelude and Four Perception Lenses

**Date:** 2026-10-19 PT. **Stage:** Text-only creative design. **No art, live code or publishing.** This document captures Silas's latest direction and provisional implementation recommendations.

## Experience, not an event calendar

An unnamed, entirely **fictional composite** Humboldt festival opens the game with music, horticulture, jugglers, physical theatre, costumes, handmade kinetic sculptures and a trail leading into the trees. The protagonist does not initially hear announcements like "Cannifest," "Kinetic Grand Championship," "Reggae on the River," "Humboldt Juggling Festival" or "Dell'Arte." The **source ledger** can name actual inspirations, while the story reveals only what the protagonist experiences and learns. Events may be disconnected in real time; the game's fiction bends chronology.

A young adult woman smoking cannabis with a green ribbon in her hair may eventually be revealed as a **forest nymph**. Name chosen by Silas: **Juniper**. She has independent motives, can refuse requests and may become a recurring guide **in every branch**, including sober. Her supernatural origin is original fantasy, not a depiction of local Indigenous beliefs. No sexual content.

## Voluntary four-way festival choice

The protagonist is an **adult** and chooses what to consume, or nothing. A fictional enchanted brownie is clearly identified as such, never a surprise spiking. No real quantities, dosage instructions, drug preparation or impaired-driving gameplay. PG-13 references to substances are permitted. The choices alter narration, available solutions, NPC reactions and certain conditional checks, not whether the supernatural world is real.

| State | Explicit player choice | Distinct narrative opportunity | Real story tradeoff |
| --- | --- | --- | --- |
| **Sober** (`sober`) | Water/food, remain clearheaded | Observe contradictions, preserve witness statements, ask precise questions | Harder to win instant intimacy with a wary stranger, but no excluded mystery or ending |
| **Tipsy** (`tipsy`) | Voluntary social drink | Rizz-driven introductions, improvised dance and conversational leads | Impulsiveness can lose a detail; careful alternative routes available |
| **Stoned** (`stoned`) | Adult voluntarily chooses cannabis | Sensory analogies, philosophical comedy, optional Psyche interpretations | Confusing impressions need corroboration; timed tasks offer slower solutions |
| **Tripping Balls** (`tripping_balls`) | Deliberately try a clearly magical **fictional** brownie | Surreal spatial scenes, dream-logic pathways, novel Psyche interpretations | False leads and symbolic misreadings; grounding and factual evidence available |

**None is a power-up tier.** The protagonist may be mistaken in any state. Even a lucid sober witness may miss evidence; an altered-state character may have an accurate insight but must verify it. Do not end with "it was just a psychedelic trip": the anomalies are real, and every necessary clue and ending is accessible sober.

## Character sheet

Permanent skills, proposed 0–3 with six starting points: **Rizz** (charm, connection, improv), **Burly** (stamina, rowing, physical resolve), **Wits** (reason, investigation, mechanics), **Local Lore** (history, geography, community), **Psyche** (uncanny perception and psychic affinity). These replace the draft Grit/Read the Room/Know-How/Odd Sense names. No identity, heritage or body type implies a bonus, psychic talent or penalty.

**Sobriety is a changing state, not a permanent character stat or moral judgment.** Persist `opening_state` (initial choice/callback flag), `current_state` (may fade or change with the story) and provisional `clarity` (0–3, temporary recall/attention; recoverable in authored quiet/rest scenes). The baseline values 3/2/2/1 for sober/tipsy/stoned/tripping are **playtest hypotheses**, not medical facts or guaranteed final balance. Clarity can change through fatigue or weirdness, too. Never offer real-world advice that water/food/rest reverses intoxication.

Check remains visible **2d6 + chosen skill + context modifier vs 7/9/11**, with target/risk disclosed before commitment. A state might offer a different choice or situational modifier, not blanket bonuses. Save seed, exact authored card revision, choice, roll, observable result, relationship flags, current state and Clarity.

## One canonical reality, four authored lenses

1. Saved seed chooses **one** complete encounter and its consistent facts.
2. State selects optional authored `narration_by_state`, `choices_by_state`, `check_modifiers_by_state`, with a shared fallback; no live LLM or random actor/cast mixing.
3. The player chooses among two or more meaningful options, rolls if needed, and persists the state and journal; those actions may actually change outcomes.
4. A statement the *player thinks they saw* is separate from a corroborated clue. A drug-related impression is neither automatic evidence nor proof a paranormal sighting was fake.
5. Every required mystery fact and ending stays reachable from sober; allow gradual changing or recovery of current state without erasing opening choice.

**120 authored canonical cards remain 120**, even if pivotal cards have four substantially different narrated/choice variants. Do not call that 480 complete encounters.

### Same encounter: Bigfoot's family picnic at Moonstone Beach

**Canon:** A Sasquatch relative is missing, a fourth person appears in a photo of three, and the tide moves backward.

- **Sober:** Wits can prove a timestamp anomaly and document the fourth figure.
- **Tipsy:** Rizz may negotiate a family reconciliation and accidentally become part of the photo.
- **Stoned:** A surf rhythm recalls an impossible festival song; Psyche supplies a lead that can be corroborated.
- **Tripping balls:** The picnic blanket resembles a moving county map; Psyche discovers a route or a funny false lead. The original camera photo remains obtainable.

A sober protagonist may still meet the nymph, Bigfoot and aliens and solve the frequency mystery. The state changes **how the journey unfolds**, not who exists.

## Authoring quality and safety tests

For each pivotal encounter verify: four interesting perspectives where warranted, two viable choices per state, no forced consumption, no secretly medicated food, no sexual content, no literal festival allegations, compatible PG-13 humor, no irreversible sober dead ends, no drug path that dominates every check. Balance smoke-test across all playable archetypes and changing clarity; save/reload preserves facts and rolls. Provide text-only design review **before any ArtJobs**.

**Real-world source reminders:** Cannifest's official 2026 dates were Sept. 12–13 at Arcata Ballpark (https://www.cannifest.com/). Reporting described **no on-site consumption zones** in 2026 (https://lostcoastoutpost.com/2026/feb/10/dellarte-was-excited-bring-cannifest-blue-lake-the/). The fictional festival is not an assertion that Cannifest distributes intoxicants. Juggling festival: https://humboldtjugglingsociety.org/Schedule.htm ; Dell'Arte event history: https://dellarte.com/past-events .

Other **inspirations, not IP to reuse**: *Fear and Loathing in Las Vegas*, Church of the SubGenius, *Illuminatus!* (also conspiracy-card-game absurdity), Burning Man, and a more mature *Gravity Falls*. Preserve the warmth, strangeness, satire and unexpected consequences, but write an original Humboldt story.

**Still exploratory:** Whether the mysterious frequency comes from layered realities, whether Wren is trying to fix or exploit it, which four-lens scenes deserve bespoke variations, the exact Clarity and skill balance, and final art. The user has not approved generation or publication.

## Companion character follow-up (2026-10-19 PT)

Four distinct recurring introductions are now preferred: **Sober → Mara** (Indigenous tattoo artist raised on a Humboldt reservation; casino-revenue grant helped start her studio; declines cannabis for precision), **Tipsy → Kit** (Chinese American kinetic performer whose fictional ancestors were expelled from Eureka in 1885; she later returned as an HSU student), **Stoned → Juniper** (forest nymph), **Tripping Balls → Cedar (working name)** (younger country Humboldt local from both timber-working and cannabis-growing families, with mechanical skill and funny CB conspiracies; Cedar himself need not consume anything). Juniper and Kit are selected concepts; Mara and Cedar are working names. The studio grant is **character fiction**, not proof of a named tribal casino grant program. For narratives and archetype-specific checks see [COMPANIONS-AND-PROLOGUE.md](COMPANIONS-AND-PROLOGUE.md). Festival choice never blocks any companion from later contact, and cannot establish a character's actual skills or culture. No image requests or publication yet.

**2026-10-19 Kit history update:** Kit has Chinese ancestry and a proposed fictional ancestor line affected by the **1885** expulsion from Eureka. Chinese American return to the county began in the **1950s**; Kit's much later return for Humboldt State-era schooling and Dell'Arte/Blue Lake theatre is her story, not a statement about actual historical descendants. Kit's skills remain learned, not ethnically assigned. See [COMPANIONS-AND-PROLOGUE.md](COMPANIONS-AND-PROLOGUE.md) and [FACT-CHECK.md](FACT-CHECK.md).


## Latest timber-family and Luna correction (2026-10-19)

The older ex-grower/hippie/dispensary/massage biography is retired. This companion is a younger rural Humboldt native whose logging-family and grower-family parents loved one another amid deeply divided local forest politics. Antenna ribbons (green in Silas's own childhood home, plus disputed yellow/green meanings across neighbors), the locally pejorative use of “Earth First!” and genuine safety fears about tree spiking are contested human history, not alignment markers. **Julia Butterfly Hill lived in Luna for 738 days in 1997–99**: her vigil and later conservation deal remain history, never a retconned fantasy. A fresh fictional CB signal starts the player's alternate-future mystery. See the updated character and provenance documents. No drugs necessary for the clue and no art authorized.


## Companion/opening/fate 32-ending update (2026-10-19)

The user now wants **32 collectible story epilogues (16 hopeful, 16 dark)** from 4 independently chosen lead companions × 4 initial voluntarily selected Sober/Tipsy/Stoned/Tripping story lenses × 2 earned consequences. The opening only favors a **first meeting**, not a permanent companion assignment. A guaranteed, independently chosen lead relationship gives every 4×4 pairing an authored path. `opening_state` persists as an ending-story dimension; `current_state` may change and cannot determine good/bad outcome. The finale reflects real choices, allies, verified evidence and 2d6 checks with repair. Sober-first players can help any lead achieve a happy future; collecting all lens-specific entries involves replaying four optional fictional starts, **never real-world substance consumption**. Details: [ECOTONE-32-ENDINGS.md](ECOTONE-32-ENDINGS.md). No art or publication.


## Newest prelude and story-interleaving rule (2026-10-19 PT)

The player **only chooses voluntary initial Sober, Tipsy, Stoned or Tripping Balls** at the festival; this choice deterministically maps to the **first companion encountered** (Mara, Kit, Juniper, Cedar respectively), with no additional first-lead selector. After introductory scenes, deal seeded **randomized authored card encounters** that alter stats, relationships, resources, clues and future consequences. A guaranteed later meeting with another main character presents **Stay with current / Follow newcomer**, and the old guide is left behind pursuing independent goals. Meet the rest of the cast at further guaranteed beats, in varying order; side encounters keep the runs distinct. Record the original `opening_state` for the 32-ending collection axis, changing `current_state` for subsequent dialogue/check flavor, and `meeting_order` / `follow_history` for ordered callback variants. End-frame companion is the person actually followed through the finale, with earned good/dark consequences from choices and dice; not automatically the first person met. Full scheme: [JOURNEY-LOOP-CONTRACT.md](JOURNEY-LOOP-CONTRACT.md) and [ECOTONE-32-ENDINGS.md](ECOTONE-32-ENDINGS.md). No art or public deployment.

## Four philosophical lenses, not chemical ideologies (2026-10-19)

[IDEOLOGICAL-ECOTONES.md](IDEOLOGICAL-ECOTONES.md) proposes four independent human/fictional axes: Autonomy–Solidarity, Continuity–Reinvention, Ecology–Engineering and Agency–Fate. To give each voluntary **opening** a distinct dramatic question, scene writers may foreground historical evidence (Sober), social obligations (Tipsy), living/technical interdependence (Stoned), or alternate-future causality (Tripping Balls). **These are original story-camera choices, not scientifically asserted drug effects, a hierarchy of intelligence, a moral alignment or a permanent ideology.** Every initial state can access every ideological argument, every lead companion, real/supernatural evidence and hopeful/dark choice consequences. No automatic axis points/stance upon opening. Ending registry remains 4 leads × 4 openings × hope/dark = 32.
