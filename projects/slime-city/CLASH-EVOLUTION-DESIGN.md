# Slime City CLASH: Evolution with actual plot twists

**Design pass:** 2026-11-07 PT. **Scope:** existing 300 distinct cards, no new IDs, no faction-hate cards; Clash-only, all Legacy cards/behaviors retained. **Status:** proposals for 70 named cards. A listed proposal is not playable until its matching engine/test path is merged.

## Research anchors

- Stoneblade official [SolForge Fusion rules](https://stoneblade.com/pages/solforge-fusion-rules): a played card creates its higher-level copy, and players trade immediate tempo for future card quality. SolForge designer Justin Gary stresses that level-one power and level-three power must be co-balanced.
- Mark Rosewater, [Lenticular Design](https://magic.wizards.com/en/news/making-magic/lenticular-design-2014-03-31): a card should be understandable to a new player and offer deeper combinatorial skill to veterans.
- Gameplay compass: one clean sentence explaining **what this version does now**; surprise comes from combinatorial outcomes, never from hidden rules text. A seeded random event shows its odds, source and result. Every L3 has visible counterplay and a matched playable test.

## Core requirements

1. No card IDs added. The 240 faction cards + 60 mercs retain their names, art and collection ownership. Faction identities remain independent of color.
2. Evolution triggers on playing/replaying a named card (L1→L2→L3); death-triggered bonuses are separate event-driven progression and must be recorded in the deterministic state. Do not accidentally accelerate an upgrade merely because a card died.
3. **Creatureless attacks** (0 base attack) are valid for support units. An attack that has no damage must be visibly skipped. Nonattackers can still block and activate passive support abilities.
4. Multi-lane summons must only spawn into vacant friendly slots and follow deterministic neighbor order. No hidden overflow or hand/card creation; any token is battlefield-only and expires when destroyed.
5. Sacrifice means an explicit voluntary cost, with clear target/benefit and a visible death. Enemy faction names, species and characters never appear in faction-specific bonus predicates. Bonuses may reference friendly tags, card effects, equipment, adjacency, casualties, or occupancy.
6. 40-life bosses, five static alleys, Clash turns/hand rules, existing reset/replay/CPU flow and legacy modes remain intact. Test early draw reachability, late-level impact, first seat and stall/timeout rates.

## 70 upgrade concepts by existing card ID

These are **redesigns**, not additions. L1 is useful; L2 invites a new sequencing choice; L3 should reward a plan, while still being beatable.

### Gene Riot Catgirls

| Existing card ID | L1 foundation | L2 twist | L3 payoff |
|---|---|---|---|
| `lynx` | Ambush scout | Repositions to any empty alley when replayed | Leaps into a neighboring empty alley with a decoy on arrival |
| `mau` | Single-target pouncer | Gains power when a rival was damaged this round | Lands a second strike against wounded defenders |
| `calico` | Low-power clinic defender | Heals wounded neighboring allies at round end | Nonattacking field surgeon; heals three allies and revives one defeated ally as a weak recruit |
| `chimera` | Fragile experiment worth nurturing | Survives one lethal hit by shedding a life | Apex chimera gains enormous stats and leaves a fresh clone when defeated |
| `pounce` | Refresh one ambush | Refresh ambush and grant extra power | Refresh and empower two adjacent pouncers |
| `scentmine` | One-alley stun trap | Also snares a neighbor | Spreads to two empty neighboring alleys after springing |
| `reknit` | Heal a fighter | Heal plus permanent +life | Heal, then rebuild a fallen ally in an empty alley |
| `shredders` | Sharpen a fighter | Give its attack armor piercing | Piercing striker splashes a fraction of damage into a neighboring alley |
| `ninthlife` | Regeneration equipment | Wearer survives its first lethal blow at 1 life | A survived fatal hit creates a second empowered life |
| `laser` | Stun one enemy | Also expose an adjacent threat | Stun up to three connected lanes so an ambush can cut through |

### Punk Bloodfairies

| Existing card ID | L1 foundation | L2 twist | L3 payoff |
|---|---|---|---|
| `sprite` | Fragile fast fighter | Deploys one tiny ally to an empty neighboring alley | Fills up to two empty neighbors with weak backup dancers |
| `pogo` | Swarm attacker | Flip a seeded coin: mighty strike or whiff | Coin toss becomes double strike when surrounded by friends |
| `razor` | Leech duelist | Leeches for wounded neighbors too | A blood chorus heals the entire adjacent choir on contact |
| `queen` | Leech + swarm leader | Gives nearby fairies +1 power | At level 3, a full five-ally stage grants the entire crew a huge one-round chorus |
| `mosh` | Local splash spell | Extends damage two alleys | At L3, a whole-row mosh blasts everyone, including badly placed allies |
| `bloodwire` | One-alley tripline | Spreads on triggering | At L3, three tripwires form a visible trap trio |
| `spurs` | Improve one fighter | Buffs an adjacent ally | An entire mosh cluster gets a small permanent boost |
| `pinprick` | Reliable chip damage | Critical on seeded 50/50 | A successful critical copies damage to neighboring enemies |
| `choker` | Grant swarm to one | Neighbors inherit swarm | Every fairy on the field gains a concert anthem while wearer survives |
| `feedback` | Aimed sonic blast | Grows with friendly adjacency | At L3 a five-member chorus echoes across all enemy alleys |

### Ironjaw Chrome Ogres

| Existing card ID | L1 foundation | L2 twist | L3 payoff |
|---|---|---|---|
| `scrapper` | Hardly attacks: blocks the lane | Provides +armor to adjacent workers | Turns into a stationary foundry that generates protective scrap for every ally |
| `welder` | Moderate attacker | Repairs a neighbor between rounds | Repairs two neighbors and saves one from its first fatal blow |
| `bulldozer` | Overkill spills through to boss | Pulls an adjacent enemy into its lane before striking | Shoves through a blocked alley and hits the boss behind it |
| `juggernaut` | Rusty inert chassis with huge life | Powerful engine starts up | Full-scale siege machine; adjacent allies gain armor as it batters blockers |
| `overclock` | Temporary boost | Sacrifice 2 fighter health for stronger power | Risk a life-burning overdrive to hit multiple alleys |
| `shocktrap` | Single-electric snare | Arcs to one neighboring intruder | At L3 triggers a chain discharge along up to three enemy slots |
| `plating` | Upgrade one ally's armor | Also upgrades neighbors | Full scrap wall grants every friendly occupied alley armor |
| `wreckingfist` | Permanent punch boost | Grants bulldoze | A crushing hit overflows into both an opposing fighter and the rival boss |
| `ducttape` | Repair one creature | Repair plus restore armor | Refit a fallen worker, replacing a friendly scrap unit if needed |
| `slap` | Knock one rival around | Stuns after heavy damage | A level-three industrial wave hits three adjacent enemies |

### Riot Saints

| Existing card ID | L1 foundation | L2 twist | L3 payoff |
|---|---|---|---|
| `rat` | Weak explosive vermin | After death its next incarnation gets bigger | Repeated destruction teaches it to detonate across adjacent alleys |
| `firebrand` | Unstable attacker | Seeded 25% chance to fizzle, otherwise double power | The fizzle becomes a harmless spark; a hit detonates the neighbor |
| `kaboom` | Piercing striker | Gains +1 on volatile allied death | At L3 converts accumulated casualties into a decisive boom |
| `bomber` | Weak ticking bomb | Death explosion doubles | The Grand Detonator's demise sets off a cross-alley chain reaction |
| `firestorm` | Random damage 1–N | Reroll the low result once | At L3 choose between safe blast or reckless all-lane fireworks |
| `badluck` | Trap that might misfire | High roll branches to the next lane | At L3 every revealed trap may chain unpredictably but visibly |
| `fuse` | Boost with a downside | Empowered attacker takes recoil | At L3 recoil can be channeled into a deliberately sacrificed ally |
| `confetti` | Area damage with friendly fire | Bigger neighboring damage | At L3 massive fireworks across the board: opponent and allies are fair game |
| `fusevest` | Grant volatile | Volatile affects adjacent lanes | When sacrificed, the vest blows up the entire enemy front |
| `drink` | Temporary risky boost | Seeded 50% underperform or overperform | At L3 pick a steady boost or roll for a ludicrous attack and backlash |

### Undertow Intelligence

| Existing card ID | L1 foundation | L2 twist | L3 payoff |
|---|---|---|---|
| `watcher` | Low-attack lookout | Reveals trapped alleys | Nonattacking wiretap node at L3: nearby rival attacks are weakened |
| `frogtrooper` | Tongue snare fighter | Snared target suffers reduced retaliation | At L3 a strike stuns adjacent defenders too |
| `eel` | Fast armor-piercer | Electrocutes a neighbor if defending a trap | At L3 shocks all opponents touching a trapped lane |
| `oracle` | Slow forecaster | Prevents first rival strike in its alley | At L3 blocks the strongest of three connected strikes |
| `blackout` | Stun single fighter | Stun plus small damage to neighboring fighter | At L3 enemy backline briefly cannot counterattack |
| `tripwire` | Hidden one-lane trap | Tripwire can arm another empty lane | At L3 becomes a visible three-lane wired network |
| `visor` | Grant piercing | Reveal an adjacent trap and boost ally | At L3 its wearer shares pierce with neighboring allies |
| `grate` | Powerful hidden damage | Victim also misses next strike | At L3 a triggered grate drags a second rival into the trap zone |
| `sonar` | Disarm in one lane | Draw extra card and disarm adjacent lane | At L3 sweep every lane for traps, drawing when disarmed |
| `drysuit` | Armor gear | Immune to next snare | At L3 ward the two neighboring allies from status effects |

### Meat Exchange

| Existing card ID | L1 foundation | L2 twist | L3 payoff |
|---|---|---|---|
| `repo` | Petty thief | Takes +1 power whenever a friendly ally falls | At L3 transforms fallen allies into permanent attack bonuses |
| `collector` | Scaling kill collector | Grows from enemy casualties anywhere | At L3 a fulfilled collection summons a debtor assistant next door |
| `broker` | Solid broker | Sacrifice a friendly creature for a permanent upgrade | At L3 the sacrifice funds an enormous replacement body |
| `mogul` | Weak bureaucrat in a luxury suit | Buys protection through allies | At L3 owns the block: nearby friendly fighters receive dividends on kills |
| `collection` | Direct collection strike | Successful strike heals your boss | At L3 damaged enemies pay tribute to all nearby allied collectors |
| `debttrap` | Single narrow snare | Snare and seize opponent tempo | At L3 spreads two small liens into adjacent empty lanes |
| `contract` | Defensive one-unit contract | Contract pays out on owner surviving a round | At L3 adjacent allies collect a share of the defense |
| `foreclosure` | Damage and stun rival | On knockout, steal 1 health for your boss | At L3 a knockout converts a rival slot into your new debtor recruit |
| `handshake` | Grant collect | Allied neighbor receives collect | At L3 the entire row shares bounty when any friendly collector downs a foe |
| `hushmoney` | Heal one asset | Heal your boss a little too | At L3 bail out a lethal-threatened allied fighter and refund part of the investment |

### Mercenary underground

| Existing card ID | L1 foundation | L2 twist | L3 payoff |
|---|---|---|---|
| `merc-bus-driver` | Plain reliable bus driver | Carries one ally to a vacant adjacent lane | L3 shifts two allied fighters into fresh unoccupied lanes |
| `merc-bribe-rat` | Cheap ambush rat | Seeded chance of bribing a blocker into no retaliation | At L3 the bribe can convert an opposing weak fighter |
| `merc-roof-dentist` | Regenerating medic | Stops attacking to heal adjacent allies | At L3 field surgery rescues two neighbors from lethal damage |
| `merc-debt-slug` | Slow draining slug | Grows when allied units die | At L3 grows after every fallen fighter on either side |
| `merc-clock-grandma` | Defensive old machine | Adjacent allies gain temporary protection | At L3 reverses a fatal hit once per game |
| `merc-smog-moth` | Tiny swarming courier | Deploys a weak ally into an empty lane | At L3 two couriers fan out into neighboring alleys |
| `merc-grease-oracle` | Faint fortune-teller | Predicts next random combat outcome | At L3 its owner may choose the safer of two seeded outcomes |
| `merc-fungal-bouncer` | Loyal wall | Absorbs one hit intended for adjacent ally | At L3 guards both neighbors once per round |
| `merc-discount-angel` | Unimpressive angel | Heals an ally when one dies | At L3 resurrects a friendly fighter as a cheap copy in an empty alley |
| `merc-union-owl` | Quiet organizer | Adjacent friendly units get +1 power | At L3 all friendly fighters get +1 and one resilient life |

## Implementation slices and fun acceptance

**First working slice:** build the shared Clash-exclusive primitives for death memory, evolving passive supports, seeded uncertainty, adjacency, multi-lane tokens, sacrifice-based buffs and a capstone. Wire them to named founders and mercenaries first; avoid promising the full 70 as playable until tested. All 70 named designs remain an inspectable backlog for further conversion to exact runtime text.

**Follow-on:** cover the remaining named effects with fixtures per level, assert 300 unchanged IDs/rarities, replay equality for every seeded outcome, and adversarial CPU-versus-CPU suites over six crews/seat orders. Cross-faction synergy should be possible through mercs; no team-hate predicates. Monitor L3 reachability so the exotic finishes actually appear during normal matches. See the core [faction archetypes](FACTION-DECK-ARCHETYPES.md).

**Counterplay:** telegraph big L3 setup before it resolves, give sacrifice a real board cost, cap repeated death buffs, prevent infinite respawns, never generate a token into an occupied slot, prevent hidden RNG changing replay, and keep nonattackers useful without creating permanent stalls.

**No release gate cleared:** testing fun requires Silas's subjective human review, but safe internal mechanics can merge normally.
