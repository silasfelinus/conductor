# Slime City: six faction arsenals and the mercenary underground

**Latest direction, 2026-11-01 PT:** Exactly **40 distinct playable cards per faction** across six factions, plus **60 independent neutral mercenaries** legal in any crew. This is **300 distinct cards total**. The 60 permanently free starter/founder cards are INCLUDED in the 240 faction cards. The previous 40–50-per-faction stretch is historical and superseded. Each faction still supports at least three mechanically different ten-card archetypes with genuine payoff, readable weakness and counterplay.

## Milestones and fair packs

| Stage | Faction cards | Neutral mercenaries | Total | Rare | Other | 1 rare + 2 other packs |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Founders (S0) | 60 | 0 | 60 | 20 | 40 | 20 |
| Gutter Crown wave 2 (PR #4620, only once merged) | 108 | 0 | 108 | 36 | 72 | 36 |
| Six faction cores complete | 240 | 0 | 240 | 80 | 160 | 80 |
| **Target complete** | **240** | **60** | **300** | **100** | **200** | **100** |

The faction expansion after PR #4620 requires **22 new cards per faction**, 132 total: eight creatures, seven spells, four traps and three equipment each. Preserve the existing 44 rares + 88 other quota for these 132 cards, yielding 80 faction rares. The 60 mercenaries have 20 rares + 40 others; suggested functional mix: 20 creatures, 18 spells, 12 traps and 10 equipment. No scarcity-as-power premium. No filler cards. Every card must work in the actual engine and have a concrete tactical job, a counter, a unique written identity and an art provenance slot.

**Mercenary legality:** Ten distinct cards, four creatures, six specials, at least one spell/trap/equipment, and exactly the required faction signature. At most three neutrals (at least seven faction cards) to protect the crew's identity. Founder cards remain free; neutral unlocks require the same account-owned collection checks as reserves. Shared neutral abilities may diversify a faction but must not replace its defining tricks. Mercenary cards receive their own inspected collection section and can be used in any compatible slot, with legal-deck and seeded replay coverage. The initial three-neutral ceiling is reversible after balance testing.

**BLACKOUT resource/hand contract:** Start on three mana; add at most three new mana at the start of every later round; bank unused mana up to a provisional ten; debt reduces the incoming grant only. Start with five from the ten-card deck, keep every unplayed card unless explicitly marked for end-round discard, then draw back up to five. Played cards cannot return on the immediately next round, even if the draw pile reshuffles. Give human and CPU identical legal cycling, deterministic selection and public-readable explanations.

**Art delivery is separate from gameplay delivery.** Pending ArtJobs and visual placeholders never count as finished art, but they also never postpone card implementation or adversarial testing.

## A faction should feel different even if the art fails to load

Every faction needs **at least three supported and independently viable ten-card archetypes**, with a dramatic thing to do, a setup cost, visible payoff, and a counter. Those variants should change card *selection and sequencing*, not just color or incidental attack values.

| Crew | Deck variant A | Variant B | Variant C | Signature moment | Honest counter |
| --- | --- | --- | --- | --- | --- |
| **Gene Riot Catgirls** | **Rooftop Prowlers:** AP and one-time AMBUSH raids | **Unlicensed Clinic:** REGEN and tactical rescue | **Patent Pirates:** anti-armor PIERCE plus disabling decoys | A stitched-up fighter suddenly gets a second pounce; healing has real windows to punish | Anti-heal or pierce pressure, traps under predictable rush lanes, forced displacement |
| **Punk Bloodfairies** | **The Mosh:** adjacent SWARM clusters and crowd pushes | **Blood Karaoke:** LEECH sustain and fast duels | **Noise Complaints:** risky amplifier hazards and momentum | A fragile constellation of fairies turns into a dangerous chorus when properly placed | Area blasts and armored chokepoints; breaking one adjacency weakens the whole dance |
| **Ironjaw Chrome Ogres** | **Union Wall:** armored protectors and board anchors | **Wrecking Shift:** BULLDOZE lane displacement and flag engineering | **Scrapyard Specialists:** gear choices and deliberate breakpoints | An ogre shoves the blocker into a trap or clears a flag corridor, but never through a wall | PIERCE, ROOT, wide flanks, and pressure before expensive machines deploy |
| **Riot Saints** | **Fuse Choir:** VOLATILE chain-reaction sacrifices | **Safe-ish Pyro:** targeted enemy-only area bombs | **Lucky Catastrophe:** seeded random burst damage and reversal plays | A completely visible blast pattern lets you gamble on a huge comeback at real friendly-fire risk | Spread out, bait a fuse near its friends, deny predictable blast clusters |
| **Undertow Intelligence** | **Sewer Snipers:** ranged PIERCE and roots | **Counterintelligence:** scans, decoys and disarming | **The Deadfall:** layered concealed traps and choke routes | A trap and a long-range shot combine into a clever capture without free hidden deployment | Early aggression, scans and trap clearance, wide flanks before the network is established |
| **Meat Exchange** | **Collection Bureau:** COLLECT and bounded mana debt | **Hostile Takeover:** slow armored finishers and control | **Fine Print:** roots, debt traps, and careful comeback timing | A collector lands the hit that postpones the opponent's biggest play, without denying every turn | Cheap fast threats, mana-cap telegraphs, diversified low-cost plays and piercing damage |

### Mechanics worth their implementation cost

- **Ironjaw BULLDOZE is a player-visible, explicit Blackout move**: one AP, pushes one adjacent enemy into an empty square behind it, activates traps, cannot pass walls/monsters/occupied tiles or move a rooted ogre. Enemy CPU must only reason from visible facts. This is in #4620.
- **Blue-style stealth belongs to specific Undertow cards only**, never a universal hidden army. Each hidden behavior must have observable reveals and counterplay, including scanning and intentionally reading the board.
- **Riot explosions must telegraph adjacency and friendly fire**. Seeded random choices have bounded numerical outcomes and deterministic replays; do not hide arbitrary cause-of-death math.
- **Meat Exchange debt caps at the existing engine maximum**. Its payoff is delayed tempo, not a lock that denies playable turns. Never turn collectible rarity into an inherent combat-stat increase.
- A card's text must **describe the actual code path**: healing only if hurt, scan only within its radius, equipment permanently buffs as specified, and a printed two-armor grant must actually grant two (or instead print one). Don't introduce imaginary effect names with text-only functionality.
- Add truly new tactics only when tested end-to-end: card targeting, CPU decision, player button, replay command, battle log, deck legality, accessibility, and at least one concrete counter-scenario. A bespoke effect that never gets played is not finished.
- Make the **faction choice and archetype differences visible in the armory**. Provide three tested sample loadouts per crew drawn from cards actually available; preview missing collection cards without gifting ownership. Keep permanent founder loaner decks independently playable.

## No-card-padding acceptance test

For every new card record: unique readable name, memorable faction-specific flavor, kind, cost, stats/keywords/effects that genuinely run, rarity, short rules text, art slot, counterplay, and a specific deck role. Before accepting each wave:

1. Inspect all new cards in the armory and prove they can replace a legal same-kind non-signature slot. Owned-only deck saves and server-issued battle receipts must stay enforced.
2. Execute actual successful battle commands for every creature, spell, trap and equipment; check cards with special preconditions separately. Verify replay is deterministic and enemies cannot see hidden information.
3. Run adversarial seeded matchup matrices using **constructed decks**, including both seating orders and free founder decks. Track flag captures, knockouts, game duration, stalls, 0-HP traps, debt locks, CPU invalid actions and first meaningful choice. An archetype that cannot win without lucky draws needs repair, not cosmetic praise.
4. Replay one exciting *and* one disastrous sequence from every faction. Inspect whether the player could predict results from the UI and whether the funny failures were legible.
5. Test 100 rare-guaranteed, three-card packs to exhaustion at core size, with zero duplicates, no stranded cards and no purchase when either tier is exhausted. Check account ownership and concurrency, not just a local function.
6. Render using image-shaped placeholders until the art processor reports accepted ArtJob IDs and individually verified delivered ArtImages. The visual finish stays on the independent art task, not a blocker for gameplay.

**Implementation ordering:** merge/check #4620 (36 new cards, BULLDOZE), then deliver the next **22 faction cards per crew** and **60 shared mercenary cards** in coherent tested waves, checking pack ratios and all six faction deck mixes after each wave. The human game-fun and public-release gates remain separate and explicit.
