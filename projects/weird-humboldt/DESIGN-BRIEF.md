# Weird Humboldt: design exploration (v0.1 + festival update)

> **2026-10-19 PT update supersedes the original draft stat names and opening assumption.** The protagonist starts at an **unnamed fictional composite festival**, voluntarily choosing sober/tipsy/stoned/tripping-balls perspectives. New stable stats: **Rizz, Burly, Wits, Local Lore, Psyche**. Sobriety/Clarity change over time; shared supernatural facts don't change by intoxication. Forest nymph guide possible in all routes; PG-13, no sexual content or forced dosing. `PRELUDE-STATE-CONTRACT.md` is the design authority for these changes. Real festival brands belong to source metadata, not initial player exposition. No artwork yet.


Date: 2026-10-19 PT · Status: **design-first / no art generation authorized in this phase**
Owner: Conductor `weird-humboldt` · Proposed eventual Kind Robots destination: Play, not Admin (not implemented or published).

## Promise and tone

A wacky comedy-horror, location-rooted, **single-player card adventure** through Humboldt County. Explore gorgeous, ordinary places; meet eccentric but recognizably human locals; make messy decisions; roll 2d6; discover that folklore, misunderstood science and actual supernatural anomalies are intersecting. Touchstones: the playfulness of the strangest *X-Files* episodes, *Twin Peaks*' affectionate unsettling small-town mystery, tabloid absurdism and Northern California backwoods counterculture. Original characters, words, twists and gameplay: references are tonal inspiration, not licensed adaptation.

**Reader voice:** second person ("You find..."), present tense, compact vivid prose, specific jokes with a setup and consequence. Comedy coexists with genuine mystery and occasional tenderness. At least one earned non-joke moment in each chapter. Avoid endless random whimsy that has no consequences.

## The design wager: a playable county, not a linear tour

Recommended **optional mystery / mandatory experience** hybrid. Each chapter begins in a recognizable region; choose two of four location/event pools, draw one of five **fully authored** eligible cards in each. An anchor scene may close the chapter. Recurring consequences surface again in later acts. Six chapters provide about 12 main random encounters plus anchors, varied reroutes, follow-ups and endings in an approximately 45–75 minute full run; a shorter three-chapter Tourist Cut can be prototyped. The full library must contain **at least 120 finished cards**, not just the 120 seeds in ENCOUNTER-SEEDS.md.

| Chapter | Region / mood | Four pools | Desired turn |
| --- | --- | --- | --- |
| 1 | Arcata After Hours · endear locals | Arcata Plaza, Minor Theatre, Redwood Park/Community Forest, Cal Poly Humboldt | The first unambiguous impossibility |
| 2 | Coast of Improbable Tides · wistful unease | Moonstone Beach, Trinidad, Luffenholtz, Mad River/Hammond Trail | Someone remembers an earlier version of you |
| 3 | Eureka and the Bay · civic absurdism | Old Town, F Street/Perilous Plunge, Humboldt Bay, Sequoia Park | Evidence of a coordinated cover-up |
| 4 | Backroads and Bad Reception · UFO/cryptid culture | Blue Lake, Kneeland, Willow Creek, Highway 299 | Meet a party whose motives aren't what they seem |
| 5 | Southern Humboldt and Older Roads · rural surrealism | Ferndale, Fortuna, Avenue of the Giants, Eel River valley | Decide whom to protect, not just what to learn |
| 6 | The Impossible Festival · converging timelines | Arcata Plaza race start, Manila dunes, bay water crossing, Ferndale finish | Player-authored, consequence-led finale |

**Calendar fiction:** Perilous Plunge (spring fundraiser), Kinetic Grand Championship (Memorial Day), and seasonal *Rocky Horror* screenings are distinct real-world occurrences. They overlap only because **the fictional weirdness has scrambled the calendar**. Do not present a single weekend of these events as local fact.

## Festival companions (2026-10-19 PT, updated cast)

Silas confirmed **Juniper** and **Kit**; replaced the previous sober dispatcher and psychedelic radio-hunter suggestions with a deeply rooted Indigenous Humboldt tattoo artist (working name **Mara**) and an older former cannabis grower / dispensary proprietor / licensed massage therapist with conspiratorial humor (working name **Cedar**). Each offers a first route (Sober/Mara, Tipsy/Kit, Stoned/Juniper, Tripping/Cedar) while remaining independently available in all runs. **Mara was raised on a local reservation and founded her studio with a small-business grant funded by tribal casino revenue; her tribal nation and specific grant program are not yet defined.** Her personal abstinence from cannabis is about linework, not moral superiority. Her heritage is not an occult shortcut or a skill modifier. See [COMPANIONS-AND-PROLOGUE.md](COMPANIONS-AND-PROLOGUE.md) for full bios and a test scene. The [PRELUDE-STATE-CONTRACT.md](PRELUDE-STATE-CONTRACT.md) is authoritative for skills, mutable `current_state`, and Clarity. No art yet.

## Player archetypes (fictional, contemporary, optional names)

Five **persistent** skills, each 0–3: **Rizz** (charm, connection, improvisation), **Burly** (physical resolve, rowing, stamina), **Wits** (reason, observation, machines), **Local Lore** (history, places and connections), **Psyche** (psychic affinity and uncanny patterns). All use the same six starting skill points with different distributions and one perk. **Sobriety is a temporary changing state and Clarity condition**, not a sixth permanent stat; see PRELUDE-STATE-CONTRACT.md. No ethnicity, origin, body type or disability carries a numeric penalty. Personality and affiliations matter through flags, dialogue and relationships.

| Archetype | Vantage / dramatic weakness | Distinct perk |
| --- | --- | --- |
| **North Coast Reporter** | Writes for an independent weekly; addicted to getting the quote, bad at accepting a no | Once per chapter, ask one extra sourcing question before a choice |
| **Cal Poly Student** | Smart, sleep-deprived, uncertain what to believe | Reframe one failure as a partial success via study notes |
| **Bay Rower** | Knows currents, crews and cold water; impulsively volunteers | Ignore one environmental travel penalty per chapter |
| **Lifelong Humboldt Local** | Has family/community connections and contradictory memories of town | Recognize a local connection on one eligible card per chapter |
| **Tribal Community Organizer** | A contemporary fictional Wiyot-community character with independent commitments, humor, boundaries and local relationships | Invoke community-network support with permission and reciprocity; **not** a mystical racial ability |
| **Kinetic Sculpture Mechanic** | Knows broken things and unreliable teams; never leaves a contraption behind | Improvise a mechanical workaround at a material cost |
| **Backwoods Gardener** | Knowledgeable about cultivation, land-use disputes and survival; wary of authorities | Identify environmental and practical risks, not plant-based magic |
| **Night-Shift Casino Dealer** | Reads tells effortlessly, chronically tired, accustomed to fantastic stories | Once per chapter, test whether an NPC is bluffing without revealing the truth |

The `Tribal Community Organizer` is a **candidate to be developed carefully, not a claim to represent a particular tribe**. Contemporary Native presence is ordinary and vital to the place. The narrative must not appropriate ceremonies, sacred sites, languages, or depict Indigenous identity as a mystic detector of monsters. Before publication, seek appropriate cultural review/tribal-authored sources for specific material. Fictional occult groups are explicitly unrelated to any Native tradition.

## Mechanics for a first paper prototype

- **Roll:** 2d6 + skill + situational modifier vs target 7, 9, or 11. Show skill, target, risk and approximate stakes *before choice*. A natural 2 or 12 unlocks an authored complication/bonus. No reroll by refreshing; persist seed, draw, check and result.
- **Resources:** Nerve (0–8, pressure), Time (chapter actions; no clock-based grinding), Goodwill (relationships, not a moral score), Evidence (facts vs hearsay ledger), and Weird Exposure (0–8, doors open at a personal cost). Player actions change people and spaces, not merely meters. Recoverable setbacks beat abrupt dead ends.
- **Outcomes:** 2–4 materially distinct actions per card; for rolled options, clear success, failure and sometimes mixed outcomes. Failing must *move the story*. At least one quiet observational or empathetic action per several cards; absurdity cannot require cruelty to proceed.
- **Causality:** named callbacks (e.g. `helped_sasquatch_family`, `minor_reel_seen`, `plunge_other_day`, `tribal_organizer_trust`) unlock follow-ups and endings. Encounters are authored as fixed compositions; never procedural mix-and-match of identity, job and scene at play time.
- **Pacing:** reveal animated card front that stays readable; persistent compact one-screen layout across phone/tablet/desktop with scroll confined to card/journal overlays. Map tracks only selected points; character sheet/journal accessible without leaving run. Reduced motion and keyboard/gamepad touch accessibility.
- **Production:** no LLM in live dice or canonical narrative resolver. Seeded deterministic content, versioned saves, explicit provenance. Reuse only stateless shared card UI from Shifting Lands/Desks; keep stores, decks and decisions isolated.

## Mystery: keep the answer optional until user review

See PITCHES.md. Recommended hybrid is **The County Has a Frequency**: brief recurring static on radios, festival PA systems, cinema speakers and the bay reveals that **several possible Humboldts overlap**. A daft regional agency tries to contain it with forms. Who is causing it remains deliberately undecided. You can complete a run with no interest in solving it; investigators find 3+ evidence categories and can attempt an additional revelation ending. The game's heart remains unexpected local encounters, not collecting mandatory MacGuffins.

## Quality and story constraints

- Writing quality first: distinct voices, local texture without turning real people into slurs or stock caricatures; joke density with quiet beats and surprises.
- Contemporary locals, transient students, Native people, queer community, coastal workers, farmers, service staff and tourists have lives beyond providing clues. Include solidarity and friction; avoid 'outsider saves Humboldt' framing.
- Fictional marijuana cultivation plots can be strange, tense, human and satirical, but never teach illegal evasion, insinuate actual farms/crimes at identifiable properties, or reduce Southern Humboldt to stoner jokes.
- **Fact/fiction provenance:** `verified_place`, `documented_event`, `unverified_local_lore`, `original_fiction`; cite trustworthy references, mark uncertainty in journal. Minor Theatre Houdini performance/trapdoor is **local testimony + disputed confirmation**, not verified magic history.
- Real businesses/venues named only for geographic grounding, not as villains or participants in invented wrongdoing. Historical figure portrayals clearly fictional; no deception about endorsements.
- Art is explicitly postponed. Text-only prototypes and composition briefs are fine; **do not create ArtJobs, ART-PROMPTS queue entries, icons/cards/heroes or published screenshots until Silas requests the art phase.**

## Design decision gate

Review PITCHES.md and three sample playable cards. The shape is a recommendation, **not a locked canon**. After discussion, decide (a) whether the mystery is wholly optional, (b) whether six-stage/45–75 minute play feels right, (c) how far toward PG-13 horror we lean, and (d) whether the tribal archetype needs outside editorial collaboration. These answers can change the authored-deck plan without wasting art.
