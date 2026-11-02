# Slime City: the 40-card-per-faction core and 50-card stretch

**Silas, November 1, 2026 PT (latest direction):** Aim for a base roster of about 200 cards, but, more importantly, give each of the six factions **40–50 distinct cards to choose from for its ten-card deck**. Since six × 40 = 240, the binding minimum is **240 total playable cards**, with **300 total** as the 50-per-faction stretch. This **supersedes** the older plan for 50 *additional* cards per faction plus the 60 founders (360 total). Card count is a means, not the design objective: make factions theatrical, mechanically distinct and actually fun.

## Counted milestones, including the always-free founders

| Stage | Per faction | Total playable cards | New beyond first 60 | Rare-or-better | Other | Three-card packs at 1 rare + 2 other |
| --- | ---: | ---: | ---: | ---: | ---: | ---: |
| Founders (S0) | 10 | 60 | 0 | 20 | 40 | 20 |
| Gutter Crown waves 1 + 2 | 18 | 108 | 48 | 36 | 72 | 36 |
| **Core complete** | **40** | **240** | **180** | **80** | **160** | **80** |
| Full stretch | 50 | 300 | 240 | 100 | 200 | 100 |

The 108-card stage includes Kind Robots #4620, which must be **merged with latest-head green checks** before counting as live source; Round 4 art in Conductor #6936 is authored, **not verified ArtJob acceptance or delivered media**. Do not count art as a software dependency.

**Next 132 playable cards to core:** 22 per faction. Each crew adds **eight creatures, seven spells, four traps and three equipment**. That creates a 40-card faction pool of roughly 15 creatures and 25 specials; legal decks still have exactly **four creatures and six specials**, require at least one spell, trap and equipment, retain the original signature, and do not duplicate cards. All starters are playable without purchases; all additional options are account-owned collections, never browser-local balances.

**Per-crew rare quotas at the 240-card core:** Catgirls 14, Bloodfairies 13, Ironjaw 13, Riot Saints 13, Undertow 14, Meat Exchange 13. The existing 108-card pool has 7, 6, 6, 5, 7 and 5 rares respectively, so the 22 new cards per faction must include **7, 7, 7, 8, 7 and 8 rares**, with the remainder commons/uncommons. Sum: **44 rares + 88 normal cards**, maintaining 1:2 even for the final pack. Never mark an expansion rare just for power; rare is frequency, not superiority. Legendary rarity is a future label only after adapting the account and pack contract without changing the guarantee.

**50-card stretch:** add ten optional distinct cards per crew once the 40-card pool proves fun and balanced. Add exactly 20 rare-or-better and 40 normals overall, producing 100 rare-guaranteed packs total. Revisit specialties, do not merely scale stats.

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
5. Test 80 rare-guaranteed, three-card packs to exhaustion at core size, with zero duplicates, no stranded cards and no purchase when either tier is exhausted. Check account ownership and concurrency, not just a local function.
6. Render using image-shaped placeholders until the art processor reports accepted ArtJob IDs and individually verified delivered ArtImages. The visual finish stays on the independent art task, not a blocker for gameplay.

**Implementation ordering:** merge/check #4620 (36 new cards, BULLDOZE), then deliver the next **22 cards per faction** in coherent, tested sub-archetype waves, checking pack ratios after each wave. The human game-fun and public-release gates remain separate and explicit.
