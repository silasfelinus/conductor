# Slime City: 300-card individual evolution ledger

**Goal:** every existing collectible has a unique, tested L1 → L2 → L3 mechanical journey, with a payoff worth playing toward. No extra card IDs or generic stat-only final forms. Status is **implementation evidence**, not artwork completion or playtest approval.

**Inventory verified against seven Kind Robots catalog source files:** six factions × 40 + 60 independent mercenary cards = **300 unique IDs**.

**Checkpoint (2026-11-08 PT):** All 300 existing IDs now have playable three-stage evolutions on Kind Robots `main`: 70 first-wave handcrafted twists (#4895, #4901, #4904, #4905), plus 230 authored data-driven arcs (#4906, #4907). All 230 are registered and smoke-tested at every stage; this does **not** yet certify each payoff's tactical value, unique play pattern, CPU selection, or matchup balance. The 230 new arcs are marked `LIVE_QA` until the adversarial, card-specific review is complete (Kind Robots #4908). Artwork is a separate generation and curation track.

**Checkpoint (2026-11-19 PT): agent QA complete for all 300; the 230 `LIVE_QA` rows are now `QA_PASSED`.** The four things the rows were waiting on, with the evidence on Kind Robots `main`:

- **Adversarial matchups:** `verifySlimeCityEvolutionMatchups` plays 1,080 seeded matches with all 300 cards fielded, and `verifySlimeCityClashConstructed` plays 3,120 bouts across 30 legal decks plus a held-out seed family (0 dead cards on either).
- **Distinct journeys:** 0 duplicate journey groups and 0 identical L2/L3 ability profiles among the 230, plus an individual editorial review of every crew's 40 cards and the 60 mercenaries (`docs/agents/slime-city-*-evolution-review.md`).
- **CPU reach:** every one of the 300 cards is played by the CPU in seeded QA: 294 in the matchup suite and the other six in the constructed suite. Both suites share one list (`utils/scripts/lib/slimeCityCpuReach.ts`) and fail if any card loses that evidence. The last two cards with none, Reveal the Ledger and Secondhand Halo, each gained a level-one payoff (kind_robots#5379).
- **Fixtures:** `verifySlimeCityEvolutions` runs all 230 crafted journeys through the real engine at every level.

All 300 cards also have curated level-two and level-three paintings.

What this does **not** claim:

- **Level three in CPU play:** the CPU plays 237 of the 300 cards at level three across the two suites. For the other 63, level three is exercised by the engine fixtures only; a card has to be played twice in a match first.
- **Low CPU pick rate:** six two-slot cards are chosen in under 3% of the bouts they sit in: `juggernaut` (Maw-9000), `chimera` (Madame Chimera), `s3-catgirls-spare-lives`, `merc-grease-oracle`, `s3-exchange-acquisition-clause` (Mark of the Procession) and `s2-exchange-compound-interest-notice` (Breeding Hunger). Each is played. Whether each is worth a whole turn is a playtest question, carried in `PLAYTEST-HANDOFF-2026-11-19.md`.
- **Fun:** human design acceptance is t-009 and t-014.

**Source cross-check:** `prototypes.ts` 60 founders; `reserveCards.ts` 12; `gutterCrownWaveTwo.ts` 36; `gutterCrownWaveThree.ts` 36; `gutterCrownFinaleA.ts` 48; `gutterCrownFinaleB.ts` 48; `mercenaryCards.ts` 60. All paths are under Kind Robots `utils/slimeCity/`. IDs were deduplicated across the seven sources, not counted from generated card faces or art jobs.

**Latest interaction contract (Silas, 2026-11-09 PT):**
[PLAYABLE-EVOLUTION-CONTRACT.md](PLAYABLE-EVOLUTION-CONTRACT.md) is the
design/QA acceptance bar for every row, including the original 70 and the 230
`LIVE_QA` evolutions. Default: a **useful, answerable L1** with one recognizable
job, a **synergistic L2**, and a **named, compounding L3**. Track a real
faction-relevant combo, early vulnerability, actual Solo/Alliance reachability,
CPU play rationale, and opponent counterplay. The presence of three coded
stages is not acceptance. Do not promote `LIVE_QA` to `MERGED` on the
basis of code-generation or automatic stat growth alone.

**Definition of done for each row:** three authored rules texts; three matching mechanics with a genuine L3 inflection; identity/archetype synergies and counterplay; deterministic seeded command replay; target/occupancy/copy-safe rules; battle fixture showing the payoff, not just strings. Review CPU strategic use and how often L3 is reachable. No faction-hate rules.

Legend: `MERGED` original 70 hand-built arcs with focused fixtures and merged CI · `QA_PASSED` authored journeys that passed the matchup, distinct-journey, CPU-reach and fixture checks in the 2026-11-19 PT checkpoint above; human fun acceptance still open · `LIVE_QA` authored and playable on main, but awaiting those checks (no rows currently). `DESIGNED` and `TODO` remain available for future work; no rows currently use them.

## Gene Riot Catgirls (40)

| Card ID | Card name | Type | Evolution status |
|---|---|---|---|
| `lynx` | Neon Lynx | creature | MERGED |
| `mau` | Mau-77 | creature | MERGED |
| `calico` | Clinic Calico | creature | MERGED |
| `chimera` | Madame Chimera | creature | MERGED |
| `pounce` | Catnip Overdrive | spell | MERGED |
| `scentmine` | Scent Mine | trap | MERGED |
| `reknit` | Reknit Serum | spell | MERGED |
| `shredders` | Patent Shredders | equipment | MERGED |
| `ninthlife` | Ninth Life Collar | equipment | MERGED |
| `laser` | Laser Pointer | spell | MERGED |
| `splice-runner` | Splice Runner | creature | QA_PASSED |
| `mutual-aid` | Mutual Aid Serum | spell | QA_PASSED |
| `s1-roof-phantom` | Rooftop Phantom | creature | QA_PASSED |
| `s1-alley-vet` | Alley Veterinarian | creature | QA_PASSED |
| `s1-clone-salvage` | Secondhand Life | spell | QA_PASSED |
| `s1-nine-lives` | Nine Lives, No Refunds | spell | QA_PASSED |
| `s1-catnip-tripwire` | Catnip Tripwire | trap | QA_PASSED |
| `s1-surgical-piercers` | Surgical Piercers | equipment | QA_PASSED |
| `s2-catgirls-backstreet-organ-donor` | Backstreet Organ Donor | creature | QA_PASSED |
| `s2-catgirls-parapet-ghost-kitten` | Parapet Ghost-Kitten | creature | QA_PASSED |
| `s2-catgirls-emergency-molt` | Emergency Molt | spell | QA_PASSED |
| `s2-catgirls-needle-thread-ambush` | Needle-Thread Ambush | spell | QA_PASSED |
| `s2-catgirls-sterile-alley-wire` | Sterile Alley Wire | trap | QA_PASSED |
| `s2-catgirls-lab-escape-atlas` | Lab Escape Atlas | equipment | QA_PASSED |
| `s3-catgirls-glasswalker` | Gutterglass Scout | creature | QA_PASSED |
| `s3-catgirls-patent-saboteur` | Patent Saboteur | creature | QA_PASSED |
| `s3-catgirls-alley-vet` | Noodle Cart Veterinarian | creature | QA_PASSED |
| `s3-catgirls-scalpel-captain` | Velvet Scalpel Captain | creature | QA_PASSED |
| `s3-catgirls-bicycle-clinic` | Sutures on Wheels | creature | QA_PASSED |
| `s3-catgirls-escaped-tiger` | Gene-Spliced Tiger | creature | QA_PASSED |
| `s3-catgirls-sidewalk-stitches` | Sidewalk Stitches | spell | QA_PASSED |
| `s3-catgirls-stolen-saw` | Stolen Bone Saw | spell | QA_PASSED |
| `s3-catgirls-fire-escape` | Climb the Fire Escape | spell | QA_PASSED |
| `s3-catgirls-counterfeit-heart` | Counterfeit Heart | spell | QA_PASSED |
| `s3-catgirls-spare-lives` | Spare Nine Lives | spell | QA_PASSED |
| `s3-catgirls-suture-line` | Suture Line | trap | QA_PASSED |
| `s3-catgirls-garrote` | Catwalk Garrote | trap | QA_PASSED |
| `s3-catgirls-false-clinic` | False Clinic Sign | trap | QA_PASSED |
| `s3-catgirls-hollow-scalpel` | Hollow Scalpel | equipment | QA_PASSED |
| `s3-catgirls-pounce-rig` | Second Pounce Rig | equipment | QA_PASSED |

## Punk Bloodfairies (40)

| Card ID | Card name | Type | Evolution status |
|---|---|---|---|
| `sprite` | Bloodsprite | creature | MERGED |
| `pogo` | Pogo Brat | creature | MERGED |
| `razor` | Razorwing | creature | MERGED |
| `queen` | Queen Safety Pin | creature | MERGED |
| `mosh` | Moshpit Massacre | spell | MERGED |
| `bloodwire` | Bloodwire | trap | MERGED |
| `spurs` | Razor Spurs | equipment | MERGED |
| `pinprick` | Safety-Pin Stab | spell | MERGED |
| `choker` | Spiked Choker | equipment | MERGED |
| `feedback` | Amp-Stack Feedback | spell | MERGED |
| `pogo-punk` | Pogo Punk | creature | QA_PASSED |
| `amp-tripwire` | Amp Tripwire | trap | QA_PASSED |
| `s1-riot-choir` | Glitter Riot Choir | creature | QA_PASSED |
| `s1-pocket-punk` | Pocket-Sized Problem | creature | QA_PASSED |
| `s1-confetti-cannon` | Confetti Shrapnel Cannon | spell | QA_PASSED |
| `s1-stage-dive` | Unlicensed Stage Dive | spell | QA_PASSED |
| `s1-feedback-wire` | Feedback Wire | trap | QA_PASSED |
| `s1-blood-mic` | Blood Karaoke Microphone | equipment | QA_PASSED |
| `s2-bloodfairies-mosquito-disc-jockey` | Mosquito Disc Jockey | creature | QA_PASSED |
| `s2-bloodfairies-bassquake-colossus` | Bassquake Colossus | creature | QA_PASSED |
| `s2-bloodfairies-glitterglass-flood` | Glitterglass Flood | spell | QA_PASSED |
| `s2-bloodfairies-afterparty-first-aid` | Afterparty First Aid | spell | QA_PASSED |
| `s2-bloodfairies-earworm-feedback` | Earworm Feedback | trap | QA_PASSED |
| `s2-bloodfairies-roadie-megaphone` | Roadie Megaphone | equipment | QA_PASSED |
| `s3-bloodfairies-mosh-firefly` | Moshpit Firefly | creature | QA_PASSED |
| `s3-bloodfairies-pollen-queen` | Punk Pollen Queen | creature | QA_PASSED |
| `s3-bloodfairies-backstage-vamp` | Backstage Vamp | creature | QA_PASSED |
| `s3-bloodfairies-karaoke-oracle` | Riot Karaoke Oracle | creature | QA_PASSED |
| `s3-bloodfairies-tour-bus` | Tour Bus Swarm | creature | QA_PASSED |
| `s3-bloodfairies-headliner` | Blood Moon Headliner | creature | QA_PASSED |
| `s3-bloodfairies-feedback-burst` | Feedback Burst | spell | QA_PASSED |
| `s3-bloodfairies-encore` | Encore or Die | spell | QA_PASSED |
| `s3-bloodfairies-rafter-dive` | Dive from the Rafters | spell | QA_PASSED |
| `s3-bloodfairies-festival-triage` | Festival Triage | spell | QA_PASSED |
| `s3-bloodfairies-cathedral-noise` | Cathedral of Noise | spell | QA_PASSED |
| `s3-bloodfairies-tripcord` | Moshpit Tripcord | trap | QA_PASSED |
| `s3-bloodfairies-amp-socket` | Broken Amp Socket | trap | QA_PASSED |
| `s3-bloodfairies-banana-bouncer` | Bouncer Banana Peel | trap | QA_PASSED |
| `s3-bloodfairies-van-radio` | Tour Van Radio | equipment | QA_PASSED |
| `s3-bloodfairies-encore-boots` | Last Encore Boots | equipment | QA_PASSED |

## Ironjaw Chrome Ogres (40)

| Card ID | Card name | Type | Evolution status |
|---|---|---|---|
| `scrapper` | Chrome Scrapper | creature | MERGED |
| `welder` | Spark Welder | creature | MERGED |
| `bulldozer` | Bulld-Ogre | creature | MERGED |
| `juggernaut` | Maw-9000 | creature | MERGED |
| `overclock` | Overclock Core | spell | MERGED |
| `shocktrap` | Shock Plate | trap | MERGED |
| `plating` | Foundry Plating | equipment | MERGED |
| `wreckingfist` | Wrecking Fist | equipment | MERGED |
| `ducttape` | Duct-Tape Weld | spell | MERGED |
| `slap` | Hydraulic Slap | spell | MERGED |
| `union-millwright` | Union Millwright | creature | QA_PASSED |
| `spare-pistons` | Spare Pistons | equipment | QA_PASSED |
| `s1-walking-foundry` | Walking Foundry | creature | QA_PASSED |
| `s1-scrap-welder` | Scrap Welder | creature | QA_PASSED |
| `s1-hydraulic-shift` | Emergency Overtime | spell | QA_PASSED |
| `s1-forge-spark` | Forge Lightning | spell | QA_PASSED |
| `s1-bolt-clamp` | Union Bolt Clamp | trap | QA_PASSED |
| `s1-union-plate` | Collective Bargaining Plate | equipment | QA_PASSED |
| `s2-ironjaw-union-bridgebearer` | Union Bridgebearer | creature | QA_PASSED |
| `s2-ironjaw-foundry-lion` | Foundry Lion | creature | QA_PASSED |
| `s2-ironjaw-shift-change-shove` | Shift-Change Shove | spell | QA_PASSED |
| `s2-ironjaw-spare-rivet-shower` | Spare Rivet Shower | spell | QA_PASSED |
| `s2-ironjaw-hydraulic-lockjaw` | Hydraulic Lockjaw | trap | QA_PASSED |
| `s2-ironjaw-overtime-pistons` | Overtime Pistons | equipment | QA_PASSED |
| `s3-ironjaw-night-welder` | Night Shift Welder | creature | QA_PASSED |
| `s3-ironjaw-dreadnought` | Scrapyard Dreadnought | creature | QA_PASSED |
| `s3-ironjaw-union-cook` | Union Lunch Lady | creature | QA_PASSED |
| `s3-ironjaw-bridgebreaker` | Bridgebreaker Ogre | creature | QA_PASSED |
| `s3-ironjaw-coal-racer` | Coal Cart Racer | creature | QA_PASSED |
| `s3-ironjaw-matriarch` | Iron Matriarch | creature | QA_PASSED |
| `s3-ironjaw-bonus-plate` | Shift Bonus Plates | spell | QA_PASSED |
| `s3-ironjaw-reallocation` | Union Reallocation | spell | QA_PASSED |
| `s3-ironjaw-hammer-register` | Sledgehammer Inventory | spell | QA_PASSED |
| `s3-ironjaw-weld-patch` | Cold-Weld Patch | spell | QA_PASSED |
| `s3-ironjaw-furnace-overdrive` | Furnace Overdrive | spell | QA_PASSED |
| `s3-ironjaw-forklift-chock` | Forklift Chock | trap | QA_PASSED |
| `s3-ironjaw-slag-spill` | Slag Spill | trap | QA_PASSED |
| `s3-ironjaw-overtime-toll` | Overtime Paywall | trap | QA_PASSED |
| `s3-ironjaw-toe-pistons` | Steel-Toed Pistons | equipment | QA_PASSED |
| `s3-ironjaw-foreman-crowbar` | Foreman Crowbar | equipment | QA_PASSED |

## Riot Saints (40)

| Card ID | Card name | Type | Evolution status |
|---|---|---|---|
| `rat` | Riot Rat | creature | MERGED |
| `firebrand` | Firebrand | creature | MERGED |
| `kaboom` | Sister Kaboom | creature | MERGED |
| `bomber` | Grand Detonator | creature | MERGED |
| `firestorm` | Accidental Firestorm | spell | MERGED |
| `badluck` | Whoops Grenade | trap | MERGED |
| `fuse` | Illegal Booster | equipment | MERGED |
| `confetti` | Confetti Cannon | spell | MERGED |
| `fusevest` | Lit-Fuse Vest | equipment | MERGED |
| `drink` | Hold My Drink | spell | MERGED |
| `spark-diver` | Spark Diver | creature | QA_PASSED |
| `firebreak-parade` | Firebreak Parade | spell | QA_PASSED |
| `s1-mime-fuse` | Matchstick Mime | creature | QA_PASSED |
| `s1-blast-radius` | Doctor Blast Radius | creature | QA_PASSED |
| `s1-no-witnesses` | No Witnesses, Especially Us | spell | QA_PASSED |
| `s1-chaos-firecracker` | Mystery-Flavor Firecracker | spell | QA_PASSED |
| `s1-fuse-alley` | Bottled Thunder | trap | QA_PASSED |
| `s1-volunteer-vest` | Volunteer Safety Vest | equipment | QA_PASSED |
| `s2-riot-fuse-lit-bicycle-courier` | Fuse-Lit Bicycle Courier | creature | QA_PASSED |
| `s2-riot-radioactive-parade-float` | Radioactive Parade Float | creature | QA_PASSED |
| `s2-riot-friendly-fire-rehearsal` | Friendly-Fire Rehearsal | spell | QA_PASSED |
| `s2-riot-homemade-bottle-rocket` | Homemade Bottle Rocket | spell | QA_PASSED |
| `s2-riot-fusebox-fireworks` | Fusebox Fireworks | trap | QA_PASSED |
| `s2-riot-last-stand-matchbook` | Last-Stand Matchbook | equipment | QA_PASSED |
| `s3-riot-bottle-rocket` | Bottle-Rocket Nun | creature | QA_PASSED |
| `s3-riot-detonation-deacon` | Detonation Deacon | creature | QA_PASSED |
| `s3-riot-alley-prophet` | Alley Prophet of Sparks | creature | QA_PASSED |
| `s3-riot-firework-bishop` | Firework Bishop | creature | QA_PASSED |
| `s3-riot-riot-bike-messenger` | Riot Bike Messenger | creature | QA_PASSED |
| `s3-riot-thermite-archangel` | Thermite Archangel | creature | QA_PASSED |
| `s3-riot-low-budget-grenade` | Low-Budget Grenade | spell | QA_PASSED |
| `s3-riot-wrong-side-of-blast` | Wrong Side of the Blast | spell | QA_PASSED |
| `s3-riot-horrible-idea` | This Is a Horrible Idea | spell | QA_PASSED |
| `s3-riot-stolen-detonator` | Stolen Detonator | spell | QA_PASSED |
| `s3-riot-final-benediction` | Final Benediction of Fire | spell | QA_PASSED |
| `s3-riot-fusewire` | Fusewire Rosary | trap | QA_PASSED |
| `s3-riot-night-market-rocket` | Night Market Rocket | trap | QA_PASSED |
| `s3-riot-confession-booth` | Booby-Trapped Confessional | trap | QA_PASSED |
| `s3-riot-charred-sneakers` | Charred Sneakers | equipment | QA_PASSED |
| `s3-riot-posthumous-saint` | Posthumous Saint Medal | equipment | QA_PASSED |

## Undertow Intelligence (40)

| Card ID | Card name | Type | Evolution status |
|---|---|---|---|
| `watcher` | Sewer Watcher | creature | MERGED |
| `frogtrooper` | Frog Trooper | creature | MERGED |
| `eel` | Eel Courier | creature | MERGED |
| `oracle` | Drowned Oracle | creature | MERGED |
| `blackout` | Signal Blackout | spell | MERGED |
| `tripwire` | Tripwire | trap | MERGED |
| `visor` | Spyglass Visor | equipment | MERGED |
| `grate` | Leech Grate | trap | MERGED |
| `sonar` | Drain Sonar | spell | MERGED |
| `drysuit` | Rubber Drysuit | equipment | MERGED |
| `pipe-seer` | Pipe Seer | creature | QA_PASSED |
| `snitch-grate` | Snitch Grate | trap | QA_PASSED |
| `s1-basement-ghost` | Basement Ghost | creature | QA_PASSED |
| `s1-static-listener` | Static Listener | creature | QA_PASSED |
| `s1-floodlight-sweep` | Floodlight Sweep | spell | QA_PASSED |
| `s1-wiretap-order` | Wiretap Restraining Order | spell | QA_PASSED |
| `s1-blue-ink-deadfall` | Blue-Ink Deadfall | trap | QA_PASSED |
| `s1-needle-wire` | Needle-Wire Antenna | equipment | QA_PASSED |
| `s2-undertow-drainpipe-interrogator` | Drainpipe Interrogator | creature | QA_PASSED |
| `s2-undertow-subsurface-warden` | Subsurface Warden | creature | QA_PASSED |
| `s2-undertow-floodlight-leak` | Floodlight Leak | spell | QA_PASSED |
| `s2-undertow-backwater-iou` | Backwater IOU | spell | QA_PASSED |
| `s2-undertow-culvert-tollwire` | Culvert Tollwire | trap | QA_PASSED |
| `s2-undertow-wiretap-spikes` | Wiretap Spikes | equipment | QA_PASSED |
| `s3-undertow-drain-sniper` | Drainpipe Sniper | creature | QA_PASSED |
| `s3-undertow-interrogation-eel` | Interrogation Eel | creature | QA_PASSED |
| `s3-undertow-quiet-listener` | Quiet Room Listener | creature | QA_PASSED |
| `s3-undertow-needle-rain-agent` | Needle Rain Agent | creature | QA_PASSED |
| `s3-undertow-basement-watchdog` | Basement Watchdog | creature | QA_PASSED |
| `s3-undertow-sewer-leviathan` | Sewer Leviathan | creature | QA_PASSED |
| `s3-undertow-weep-holes` | Weep Holes in the Wall | spell | QA_PASSED |
| `s3-undertow-long-drain-sting` | Long Drain Sting | spell | QA_PASSED |
| `s3-undertow-reveal-the-ledger` | Reveal the Ledger | spell | QA_PASSED |
| `s3-undertow-quiet-interdiction` | Quiet Interdiction | spell | QA_PASSED |
| `s3-undertow-citywide-blackmail` | Citywide Blackmail | spell | QA_PASSED |
| `s3-undertow-red-tape-sensor` | Red-Tape Sensor | trap | QA_PASSED |
| `s3-undertow-floodgate-clamp` | Floodgate Clamp | trap | QA_PASSED |
| `s3-undertow-anonymous-invoice` | Anonymous Invoice | trap | QA_PASSED |
| `s3-undertow-periscope-lens` | Periscope Lens | equipment | QA_PASSED |
| `s3-undertow-tunnel-harpoon` | Tunnel Harpoon | equipment | QA_PASSED |

## Meat Exchange (40)

| Card ID | Card name | Type | Evolution status |
|---|---|---|---|
| `repo` | Repo Goblin | creature | MERGED |
| `collector` | Debt Collector | creature | MERGED |
| `broker` | Flesh Broker | creature | MERGED |
| `mogul` | The Meat Mogul | creature | MERGED |
| `collection` | Hostile Collection | spell | MERGED |
| `debttrap` | Hidden Fees | trap | MERGED |
| `contract` | Iron Contract | equipment | MERGED |
| `foreclosure` | Foreclosure | spell | MERGED |
| `handshake` | Golden Handshake | equipment | MERGED |
| `hushmoney` | Hush Money | spell | MERGED |
| `audit-fiend` | Audit Fiend | creature | QA_PASSED |
| `debt-holiday` | Debt Holiday | spell | QA_PASSED |
| `s1-executive-repo` | Executive Repossessor | creature | QA_PASSED |
| `s1-guild-clerk` | Guild Clerk (Temporary) | creature | QA_PASSED |
| `s1-margin-call` | Emergency Margin Call | spell | QA_PASSED |
| `s1-buy-silence` | Buy Their Silence | spell | QA_PASSED |
| `s1-debt-garnish` | Garnishment Floor Tile | trap | QA_PASSED |
| `s1-golden-handshake` | Golden Handshake, Iron Grip | equipment | QA_PASSED |
| `s2-exchange-bargain-rate-collector` | Bargain-Rate Collector | creature | QA_PASSED |
| `s2-exchange-golden-bailiff` | Golden Bailiff | creature | QA_PASSED |
| `s2-exchange-compound-interest-notice` | Compound Interest Notice | spell | QA_PASSED |
| `s2-exchange-contract-amendment` | Contract Amendment | spell | QA_PASSED |
| `s2-exchange-invisible-lien` | Invisible Lien | trap | QA_PASSED |
| `s2-exchange-executive-health-coverage` | Executive Health Coverage | equipment | QA_PASSED |
| `s3-exchange-wage-garnisher` | Wage Garnisher | creature | QA_PASSED |
| `s3-exchange-mortgage-minotaur` | Mortgage Minotaur | creature | QA_PASSED |
| `s3-exchange-retainer-clerk` | Retainer Clerk | creature | QA_PASSED |
| `s3-exchange-seizure-executive` | Seizure Executive | creature | QA_PASSED |
| `s3-exchange-hostile-takeover-goon` | Hostile Takeover Goon | creature | QA_PASSED |
| `s3-exchange-golden-foreclosure` | Golden Foreclosure Engine | creature | QA_PASSED |
| `s3-exchange-payment-reminder` | Payment Reminder | spell | QA_PASSED |
| `s3-exchange-compound-notice` | Compound Notice | spell | QA_PASSED |
| `s3-exchange-executive-incentive` | Executive Incentive | spell | QA_PASSED |
| `s3-exchange-golden-parachute` | Golden Parachute | spell | QA_PASSED |
| `s3-exchange-acquisition-clause` | Acquisition Clause | spell | QA_PASSED |
| `s3-exchange-late-fee-sticker` | Late-Fee Sticker | trap | QA_PASSED |
| `s3-exchange-escrow-snare` | Escrow Snare | trap | QA_PASSED |
| `s3-exchange-repossession-notice` | Repossession Notice | trap | QA_PASSED |
| `s3-exchange-ledger-greaves` | Ledger Greaves | equipment | QA_PASSED |
| `s3-exchange-collection-badge` | Collection Badge | equipment | QA_PASSED |

## Mercenary Underground (60)

| Card ID | Card name | Type | Evolution status |
|---|---|---|---|
| `merc-bus-driver` | Gutterbus Driver | creature | MERGED |
| `merc-bribe-rat` | Bribe-Licked Rat | creature | MERGED |
| `merc-roof-dentist` | Rooftop Dentist | creature | MERGED |
| `merc-debt-slug` | Debt-Eating Slug | creature | MERGED |
| `merc-clock-grandma` | Clockwork Grandmother | creature | MERGED |
| `merc-smog-moth` | Smog Moth Courier | creature | MERGED |
| `merc-grease-oracle` | Grease Oracle | creature | MERGED |
| `merc-fungal-bouncer` | Fungal Bouncer | creature | MERGED |
| `merc-discount-angel` | Discount Archangel | creature | MERGED |
| `merc-union-owl` | Owl of All Trades | creature | MERGED |
| `merc-sewer-sommelier` | Sewer Sommelier | creature | QA_PASSED |
| `merc-skate-taxidermist` | Skating Taxidermist | creature | QA_PASSED |
| `merc-auction-golem` | Auction Golem | creature | QA_PASSED |
| `merc-spark-midwife` | Midwife of Sparks | creature | QA_PASSED |
| `merc-traffic-witch` | Traffic Witch | creature | QA_PASSED |
| `merc-picket-troll` | Picket Line Troll | creature | QA_PASSED |
| `merc-escape-crab` | Escape Artist Crab | creature | QA_PASSED |
| `merc-living-scaffold` | Living Scaffolding | creature | QA_PASSED |
| `merc-invisible-mime` | Invisible Mime | creature | QA_PASSED |
| `merc-midnight-janitor` | Midnight Janitor | creature | QA_PASSED |
| `merc-misaddressed-parcel` | Misaddressed Parcel | spell | QA_PASSED |
| `merc-crowd-lightning` | Crowd-Sourced Lightning | spell | QA_PASSED |
| `merc-unofficial-detour` | Unofficial Detour | spell | QA_PASSED |
| `merc-reputation-laundry` | Reputation Laundering | spell | QA_PASSED |
| `merc-flashmob-diversion` | Flashmob Diversion | spell | QA_PASSED |
| `merc-jury-rigged-radar` | Jury-Rigged Radar | spell | QA_PASSED |
| `merc-allergy-season` | Allergy Season | spell | QA_PASSED |
| `merc-supervised-demo` | Supervised Demolition | spell | QA_PASSED |
| `merc-unsupervised-demo` | Unsupervised Demolition | spell | QA_PASSED |
| `merc-mortgage-holiday` | Mortgage Holiday | spell | QA_PASSED |
| `merc-secondhand-halo` | Secondhand Halo | spell | QA_PASSED |
| `merc-take-stairs` | Take the Stairs | spell | QA_PASSED |
| `merc-streetlight-confession` | Streetlight Confession | spell | QA_PASSED |
| `merc-homebrew-antidote` | Homebrew Antidote | spell | QA_PASSED |
| `merc-whisper-network` | Whisper Network | spell | QA_PASSED |
| `merc-mothball-storm` | Mothball Storm | spell | QA_PASSED |
| `merc-festival-no-refunds` | Festival of No Refunds | spell | QA_PASSED |
| `merc-union-solidarity` | Union Solidarity | spell | QA_PASSED |
| `merc-glass-echo` | Glass Echo Plate | trap | QA_PASSED |
| `merc-tourist-trapdoor` | Tourist Trapdoor | trap | QA_PASSED |
| `merc-concealed-tollbooth` | Concealed Tollbooth | trap | QA_PASSED |
| `merc-boomerang-buffet` | Boomerang Buffet | trap | QA_PASSED |
| `merc-invisible-bump` | Invisible Speed Bump | trap | QA_PASSED |
| `merc-market-tripwire` | Night Market Tripwire | trap | QA_PASSED |
| `merc-flooded-fusebox` | Flooded Fusebox | trap | QA_PASSED |
| `merc-parking-meter` | Hostile Parking Meter | trap | QA_PASSED |
| `merc-dog-eared-mine` | Dog-Eared Mine | trap | QA_PASSED |
| `merc-cursed-sign` | Cursed Detour Sign | trap | QA_PASSED |
| `merc-ghoul-et-lot` | Ghoul-Et-Lot | trap | QA_PASSED |
| `merc-angry-bees` | Bag of Very Angry Bees | trap | QA_PASSED |
| `merc-borrowed-kneepads` | Borrowed Kneepads | equipment | QA_PASSED |
| `merc-squeaky-wheel` | Squeaky Wheel | equipment | QA_PASSED |
| `merc-edible-kevlar` | Edible Kevlar | equipment | QA_PASSED |
| `merc-emergency-wings` | Emergency Wings | equipment | QA_PASSED |
| `merc-red-tape-scissors` | Red Tape Scissors | equipment | QA_PASSED |
| `merc-theftproof-toolkit` | Theftproof Toolkit | equipment | QA_PASSED |
| `merc-counterfeit-license` | Counterfeit License | equipment | QA_PASSED |
| `merc-rooftop-map` | Rooftop Map | equipment | QA_PASSED |
| `merc-broken-halo` | Broken Halo | equipment | QA_PASSED |
| `merc-union-suit` | Union Suit | equipment | QA_PASSED |

## Keeping this ledger honest

**All 300 IDs now have playable evolution code**; this sheet is not a claim that every arc is balanced, narratively memorable, or visually complete. The 230 rows that waited on adversarial matchups, distinct-mechanical-journey inspection, L3 reachability and example fixtures were promoted to `QA_PASSED` on 2026-11-19 PT; the checkpoint at the top records the evidence and what it leaves open. Updating a card must reuse its existing ID. The original design brief is `CLASH-EVOLUTION-DESIGN.md`; QA method and results live in `CLASH-EVOLUTION-QA-2026-11-08.md`.
