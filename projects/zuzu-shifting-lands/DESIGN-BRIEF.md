# Zuzu: Shifting Lands | Experience & Gameplay Design Brief

> **Current creative decision, 2026-10-09 (supersedes the procedural encounter composition described later in this historical brief):** Shifting Lands now selects **complete pre-authored illustrated encounter cards**, with fixed species/occupation/cast and bespoke art, from multiple possibilities per location. Species is conveyed by illustration rather than the title. Every encounter has readable flavor text, at least two concrete choices, and dice-based success/failure consequences. The game uses dedicated Zuzu card backs and a legible persistent face-up flip. See [authored encounter implementation](encounters/IMPLEMENTATION-ORDER.md) and [the first 12](encounters/HOMESTEAD-12.json). Independent Facet taxonomies remain valid in the global resource catalog, but are **not** combined randomly in this game's encounter draw. The older sections below are retained only as background and must not override this decision.

**Owner:** Conductor project `zuzu-shifting-lands`; Kind Robots development preview `/admin/zuzu-shifting-lands`, linked from the Admin channel; future public release `/play/zuzu-shifting-lands` is a separate milestone. **Status:** authorized project, design phase; no playable production deployment asserted. **World authority:** [Zuzu world registry](../../worlds/zuzu/README.md), [setting guide](../../worlds/zuzu/WORLD-GUIDE.md), Book One, locked cast, and video guardrails. This game's generated outcomes are **alternate-play continuity**, never an automatic Book One retcon.

## Promise

An illustrated, replayable, solo narrative board-game RPG: **Armello's tactile sense of a living game board, cards and consequential quests, joined with the gamebook's branching stakes and Storybook's open-ended fiction**. Zuzu begins as an Edo-era samurai and outsider in a strange anthropomorphic weird-west wasteland. A user sets out across *five lands*, each with **three meaningful encounters in distinct locations**, then faces a major trial/boss, with companion recruitment, enemies, skill rolls, supplies, wounds, and persistent choices. Lands, settlements, inhabitants and alliances can shift across runs and **sometimes within a run for a causally supported reason**. Players see a growing card-grid travel map, encounter artwork, and a readable record of what occurred.

We borrow genre-level mood and tabletop tactility, **not** another game's characters, rule names, unique board assets, art, copied wording, exact card templates, or combat formula.

## Core dramatic rule: species is not destiny

A non-player participant is composed from independent, typed layers:

```text
SPECIES (appearance, movement, natural affordances)
  × OCCUPATION/ROLE (what the creature does)
  × FACTION (whose resources it serves)
  × DISPOSITION (how it treats Zuzu; may evolve)
  × MOTIVE/SECRET (what it actually seeks, usually hidden)
  × CONDITION (injury, enchantment, curse, hunger, blessing)
  × INDIVIDUAL IDENTITY (optional named Character + continuity history)
  × LOCATION + CURRENT WORLD STATE
    -> compatible encounter / art references / choices / consequences
```

`species:rabbit + occupation:homesteader + disposition:helpful` and `species:otter + occupation:homesteader + disposition:predatory` may share an encounter template. Conversely a rabbit may be a saloon host, soldier, healer, outlaw, occult predator, parent or wandering companion. **No hardwired rabbit=gentle / gorilla=evil / crow=witch**. Some established characters are explicitly witches or dangerous, but randomized unnamed members of their species need not be.

**Existing Kind Robots taxonomy supports this now.** `FacetProfile.taxonomy` includes `SPECIES`, `OCCUPATION`, `ARCHETYPE`, `ROLE`, `ALIGNMENT`, `SETTING`, `PERSONALITY`, `BACKSTORY` and `QUIRK`. Reuse `Facet` + `FacetProfile`; do **not** invent a replacement FacetType enum or insert new schema columns before auditing existing APIs. A `Character` is an individual with memory, appearance and relationships. A `Facet(SPECIES)` is a potentially randomizable archetype; do **not** clone 50 Rabbit Character records.

Metadata must give each facet `worlds:["zuzu"]`, rarity, compatible biomes, encounter tier and exclusion rules; `isRandomizable` and `randomWeight` already exist. A separate world membership join to `Project.conductorSlug=zuzu-shifting-lands` and established Pack, CharacterFacet / ScenarioFacet / RewardFacet / ProjectFacet relations may be used after a schema/access audit. **Do not pretend that all live legacy Resources are already tagged**. Import and retrofit is its own verifiable task.

### Encounter composition

For a specific encounter, draw the **location first** (local geography, time and prevailing state), then an encounter template (Scene/Scenario), then a *compatible* role, then a species drawn from that land's ecological pool, then faction/agenda/disposition, then an optional named Character, a possible skill check and Reward. Independent layers do not mean unrestricted arbitrary pairing. Restrict by habitat, special anatomy, social plausibility, rarity, continuity, cast-specific identity locks and content rating. Never swap an already-revealed character species or redraw their motive mid-conversation.

Example: **The First Homestead**, with a crooked garden fence and one lantern. The inhabitants may be rabbit or otter settlers. Their *role* might be farmer or caretakers of a roadside sanctuary. The sanctuary's true relation to travelers is separately rolled and may later be exposed through observation, dialogue, or evidence. Friendly and dangerous outcomes each need earned, legible consequences, not random punishments.

Never reveal the `hiddenTruth` field until the player earns a reveal. A creature's card front may display species and profession; motive and danger level are discovered through gameplay, not spoiled by colors or icons.

**Lost-world canon:** anthropomorphic animals now occupy a world where humans previously existed; *something went wrong*, but the actual event and its relation to the cosmic horror have not yet been decided. Record the mystery openly in design docs without presenting an unapproved explanation as fact.

## Five-land expedition, with meaningful evolution

A run consists of 5 lands × 3 location encounters = **15 main encounters** plus a **major challenge at the end of every land**, travel stops, optional detours and epilogues. Each land has its own deck, ecology, assets, pressure meter, named anchors and at least three alternate layouts. These are **starting designs, not newly declared permanent geography**:

| Land | Starting identity | Potential locations | Typical danger and change |
| --- | --- | --- | --- |
| 1 | **The Homestead** (wasteland outskirts) | outlying farm; roadside chapel/mission; communal well | first mercy/intuition tests, unreliable hospitality, hidden local power, a sanctuary/convent confrontation as the climax |
| 2 | **Dustwater Crossing** (provisional) | trading post; river landing; toll gate | alliances, water rights, raiders and competing settlers; routes change after a drought or deal |
| 3 | **The Broken Tablelands** (provisional) | canyon camp; quarry; derelict waystation | hostile weather, shifting passes, dangerous bargains and higher-tier raiders |
| 4 | **Storm-Crow Depths** (provisional) | cavern mouth; witch's threshold; underground crossroads | magical cave-dwelling storm-crow witches, costly aid and unreliable geography; some encounters are benign or ambiguous |
| 5 | **The Black Verge** (provisional) | obsidian road; fortified dark encampment; threshold | high-tier gorilla figures, potential occult conditions and powerful antagonists; campaign-scale resolution |

A **land** is a chapter container, not just a scenery texture. Encounter results may add/remove/reorder accessible *unvisited* tiles, reveal a short route, put a destroyed settlement in the history log, or change the next land's entry conditions. Previously traveled locations remain pinned in the journey log; **history never silently rewrites itself**. On revisit, show the reason a location changed. A major confrontation can be resolved by combat, bargaining, stealth, rescue, escape or another earned route if an appropriate check/reward is present.

### World-one antagonist

Land 1 has a **convent/Abbess-centered major confrontation**. The Abbess has long orchestrated disappearances and dark sacrificial rites involving children; she aims to nourish a cosmic horror and ultimately bring it into the world. She can welcome Zuzu with food and lodging before evidence of her real purpose surfaces. This is canonical background, openly documented on GitHub. Players should encounter and interpret clues before the reveal, but developers and agents do not need to pretend the secret is unknown.

The Abbess's appearance, abilities, and narrative consequences must match existing locked Character references and case-sensitive source guardrails. Child-harm themes should be treated as disturbing narrative stakes **without sensationalized depictions of harm to children**.

## Art-first board and tactile deck system (MVP)

**Binding implementation spec:** [BOARD-CARD-ARCHITECTURE.md](BOARD-CARD-ARCHITECTURE.md). Silas confirms that card fronts/backs, stacked draw decks, dealing, flipping and transitions must draw from **existing Kind Robots components**, not a parallel visual engine. Full persistent deck/hand/discard state is owned by Shifting Lands' tested journey reducer because the available KR card-visual components are not themselves a generic deck-state service. An illustrated game board with real interactions is a launch requirement, not a stretch goal.

## A 3 × 5 illustrated map that remembers

### Main UX composition

- **Art-dominant grid:** a central illustrated travel board with five land panels and a **three-card encounter strip for the active land**. Cards retain their illustration and completed-state stamp; completed lands can be browsed as travel history. Each card has image, evocative title, travel path, risk/terrain cue, fog-of-war visibility and its source ArtImage (or a deliberate image-shaped pending state).
- **Zuzu panel:** portrait and gear, health/wounds, six original skills (e.g. Steel, Awareness, Wits, Bearing, Resolve, Insight), condition cards and supplies. The **Edo-era code** creates dialogue/behavior options and evolving personal beliefs, not just +2 to swords.
- **Encounter focus:** large artwork, concise evocative prose, 2–4 action cards (an obvious safe option plus higher-risk or unlocked options), tactile dice/skill check and result animation. No overwhelming top-level tab stack.
- **Companion rail:** character cards with relationship, condition, personal motive and unique contributions; trust changes over time and can close/open routes.
- **Journal:** chronological facts, discovered identities, role history, map mutation reasons, promises and resolved branches. Optional lore inspector links to Zuzu World Studio.
- **Touch:** drag/swipe scroll the journey; readable one-card focus; keyboard and screen reader navigation; reduced motion alternative; no hover-only actions. Phone/tablet/desktop verification required.

A player's route is **spatial** rather than merely a sequence of text screens. The next card highlights reachable locations, including sealed alternatives and optional detours. A boss gate unlocks on the prescribed conditions (three encounters completed, or a designed alternate route), not on a hidden random roll.

### Rules and resource economy (prototype defaults for playtest)

- Zuzu begins each run with **8 HP**, one katana, travel kasa, 2 provisions and six stats on a scale of 0–4. The exact initial distribution is a proposal to balance, not existing canonical fact.
- Skill check: **roll 2d6 + stat + temporary help** versus difficulty 7 (routine), 9 (challenging), 11 (dire), each +/- difficulty modified for preparation or injury. Roll and modifiers visibly persist in the encounter history; success and failure both advance narrative with proportionate consequence. Do not re-roll for free by refreshing.
- A poor outcome may cost HP, provisions, trust, reputation, route access or an opportunity; failure must almost never equal “nothing happened”. Named companions may intercept damage, reveal clues or open noncombat paths.
- Reward deck: **Items**, **Techniques/skills**, **Allies**, **Knowledge**, **Conditions**. `Reward` owns reusable skills/items; narrative fact flags and temporary statuses stay inside run state, not cloned global Rewards.
- Combat shares stateless dice/results utilities with the gamebook where helpful, but has its **own state owner** and pacing; do not mount the gamebook page or conflate world-branch continuity. Transparent danger, escape cost and alternative solutions prevent five bosses becoming mandatory combat grinds.
- Victory when a land challenge is resolved and Zuzu survives; defeat yields a distinct ending/journal entry and re-seed affordance. Saves must be robust, versioned and resumable.

## Endless fiction without incoherent fiction

**Two-layer narrative:**
1. **Deterministic rules/state** decides what is possible, participants, species/roles, checks, inventory, casualties, permanent flags and a reversible run replay seed. The generation system can never invent a missing inventory object, move Zuzu to an unreachable tile, rewrite completed history or declare Book One canon.
2. **Narrative renderer** writes rich dialogue, choices and aftermath from a validated *fact packet*, with preference for curated Scenario template prose and controlled Storybook text generation when enabled. Allow a complete **pre-authored offline path** with no paid inference or API keys. Lore can be documented in the repository; prompts still follow actual provider privacy, consent and cost settings.

Character identities and hidden agendas are seeded once and persisted; so are the underlying land layout, encounter templates, and proposed location changes. AI proposes scene dialogue/content only and undergoes safety/continuity validation. Pin model version + content provenance + run seed; cache accepted text for replay/resume. Rejected model results fall back to authored text. Quota/cost/access gates follow existing Kind Robots mana rules; no unattended spend.

## Shared Kind Robots world-resource access contract

Resources should be **tagged Zuzu** so the game, Gamebook, Lair, cartoons, trailer and future productions can reuse the same identity and art, not copied textual approximations.

- **Facet**: use the existing `FacetProfile.taxonomy` for SPECIES, OCCUPATION, ROLE, ARCHETYPE, SETTING, etc.; `metadata.worlds=["zuzu"]` and `metadata.landIds`/tier/weight identify the randomizer pool. A world's `world` tag means *available to this universe*, not *canonical story fact*.
- **Character**: named individuals (Zuzu, Coyote Vagrant, fennec siblings, storm-crow character, the Abbess, etc.) with source provenance and relation(s) to approved species/role Facets; public guest enemies use generated participant snapshots, not hundreds of fake Character rows.
- **Scenario**: typed encounter templates with location constraints, open options, skill gates, outcomes and hiddenTruth stored separately when sensitive. `ScenarioFacet` links provide coarse discovery; prompt schema needs a precise versioned scenario payload owned by this game.
- **Reward**: named techniques, weapons, items and narrative tokens link to the world marker Facet/`Pack`; use `RewardFacet` where possible. Keep canonical appearance distinct from random mechanically spawned variants.
- **ArtImage / Resource / LoRA**: use the existing Zuzu World Studio's project-art links, cast picks and provenances; dynamically resolve signed media, maturity/privacy, shot aspect and approved version. Don't copy image bytes.
- **Project**: `conductorSlug: zuzu-shifting-lands` is the project join. A `ProjectFacet` relation can serve as a filter/selection for the new game, but does NOT automatically apply to all Zuzu-world consumers. For all-resource discovery, prefer an audited, server-side world-membership resolver.
- **Dramatic disclosure/authorization:** full boss lore can live in this repository and source manifests. The **player UI** reveals mysteries when earned, not through an early tooltip or card front. Mature/private settings of actual user-owned resources still govern access.

Seed a **world-marker** Facet on live DB after an identity/duplicate audit; do not guess its record ID or assume someone already imported the original resource-submission payload. Migrate old LLM-generated filler carefully under Silas's replacement authorization (preserve IDs and art history), only after comparing to locked story and design. World Studio needs UI to tag existing records and inspect Species/Role cards separately.

### Example procedural combination

```json
{
  "seed": "zuzu-journey-026",
  "land": "homestead",
  "locationTemplate": "roadside-farm",
  "encounterTemplate": "a-visitor-needs-shelter",
  "speciesFacet": "rabbit",
  "occupationFacet": "homesteader",
  "disposition": "wary",
  "privateMotiveRef": null,
  "choiceIds": ["accept-hospitality", "offer-work", "watch-at-distance"],
  "skillCheck": { "stat": "insight", "difficulty": 9 },
  "result": { "flag": "farmstead-trust", "value": 1 }
}
```

That is a **design illustration**, not a preexisting live Scenario. Replace hand-authored slugs with verified entity IDs only when the resolver proves they exist and are authorized.

## Scope and gates

**Milestone 1:** repo project + taxonomy/encounter manifests + engine contracts + composition test matrix + proof-of-concept art board with correct in-game mystery pacing.

**Milestone 2:** robust seeded 5-land game loop, 15+ encounters, 5 authored challenges, persistent state, deterministic choices/rolls, map mutation and encounter history; data adapters for Facets, Characters, Scenarios and Rewards with strict world isolation.

**Milestone 3:** imagery from existing cast and production ArtImages + deliberate variant ArtJobs, Storybook-adjacent text generator with authorial validators, companion dialogue and new encounter decks.

**Milestone 4:** admin curation controls, clue-based in-game narrative reveal, full playtesting, balancing, accessibility, responsive image-first visual acceptance, eventual publication **only when Silas explicitly approves**.

This is a **new project** with its own roadmap and app page; it must *not* replace or hijack `zuzu-gamebook` / `zuzu-lair`. Agents may autonomously implement reversible code/content drafts and internally queue scoped ArtJobs. Do not claim live row creation, paid generation, publishing or deploy without verification/authorization.
