# Slime City: 300-card individual evolution ledger

**Goal:** every existing collectible has a unique, tested L1 → L2 → L3 mechanical journey, with a payoff worth playing toward. No extra card IDs or generic stat-only final forms. Status is **implementation evidence**, not artwork completion or playtest approval.

**Inventory verified against seven Kind Robots catalog source files:** six factions × 40 + 60 independent mercenary cards = **300 unique IDs**.

**Checkpoint (2026-11-08 PT):** All 300 existing IDs now have playable three-stage evolutions on Kind Robots `main`: 70 first-wave handcrafted twists (#4895, #4901, #4904, #4905), plus 230 authored data-driven arcs (#4906, #4907). All 230 are registered and smoke-tested at every stage; this does **not** yet certify each payoff's tactical value, unique play pattern, CPU selection, or matchup balance. The 230 new arcs are marked `LIVE_QA` until the adversarial, card-specific review is complete (Kind Robots #4908). Artwork is a separate generation and curation track.

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

Legend: `MERGED` original 70 hand-built arcs with focused fixtures and merged CI · `LIVE_QA` authored and playable on main, but awaiting full matchup/CPU-reachability and individual-payoff acceptance. `DESIGNED` and `TODO` remain available for future work; no rows currently use them.

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
| `splice-runner` | Splice Runner | creature | LIVE_QA |
| `mutual-aid` | Mutual Aid Serum | spell | LIVE_QA |
| `s1-roof-phantom` | Rooftop Phantom | creature | LIVE_QA |
| `s1-alley-vet` | Alley Veterinarian | creature | LIVE_QA |
| `s1-clone-salvage` | Secondhand Life | spell | LIVE_QA |
| `s1-nine-lives` | Nine Lives, No Refunds | spell | LIVE_QA |
| `s1-catnip-tripwire` | Catnip Tripwire | trap | LIVE_QA |
| `s1-surgical-piercers` | Surgical Piercers | equipment | LIVE_QA |
| `s2-catgirls-backstreet-organ-donor` | Backstreet Organ Donor | creature | LIVE_QA |
| `s2-catgirls-parapet-ghost-kitten` | Parapet Ghost-Kitten | creature | LIVE_QA |
| `s2-catgirls-emergency-molt` | Emergency Molt | spell | LIVE_QA |
| `s2-catgirls-needle-thread-ambush` | Needle-Thread Ambush | spell | LIVE_QA |
| `s2-catgirls-sterile-alley-wire` | Sterile Alley Wire | trap | LIVE_QA |
| `s2-catgirls-lab-escape-atlas` | Lab Escape Atlas | equipment | LIVE_QA |
| `s3-catgirls-glasswalker` | Gutterglass Scout | creature | LIVE_QA |
| `s3-catgirls-patent-saboteur` | Patent Saboteur | creature | LIVE_QA |
| `s3-catgirls-alley-vet` | Noodle Cart Veterinarian | creature | LIVE_QA |
| `s3-catgirls-scalpel-captain` | Velvet Scalpel Captain | creature | LIVE_QA |
| `s3-catgirls-bicycle-clinic` | Sutures on Wheels | creature | LIVE_QA |
| `s3-catgirls-escaped-tiger` | Gene-Spliced Tiger | creature | LIVE_QA |
| `s3-catgirls-sidewalk-stitches` | Sidewalk Stitches | spell | LIVE_QA |
| `s3-catgirls-stolen-saw` | Stolen Bone Saw | spell | LIVE_QA |
| `s3-catgirls-fire-escape` | Climb the Fire Escape | spell | LIVE_QA |
| `s3-catgirls-counterfeit-heart` | Counterfeit Heart | spell | LIVE_QA |
| `s3-catgirls-spare-lives` | Spare Nine Lives | spell | LIVE_QA |
| `s3-catgirls-suture-line` | Suture Line | trap | LIVE_QA |
| `s3-catgirls-garrote` | Catwalk Garrote | trap | LIVE_QA |
| `s3-catgirls-false-clinic` | False Clinic Sign | trap | LIVE_QA |
| `s3-catgirls-hollow-scalpel` | Hollow Scalpel | equipment | LIVE_QA |
| `s3-catgirls-pounce-rig` | Second Pounce Rig | equipment | LIVE_QA |

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
| `pogo-punk` | Pogo Punk | creature | LIVE_QA |
| `amp-tripwire` | Amp Tripwire | trap | LIVE_QA |
| `s1-riot-choir` | Glitter Riot Choir | creature | LIVE_QA |
| `s1-pocket-punk` | Pocket-Sized Problem | creature | LIVE_QA |
| `s1-confetti-cannon` | Confetti Shrapnel Cannon | spell | LIVE_QA |
| `s1-stage-dive` | Unlicensed Stage Dive | spell | LIVE_QA |
| `s1-feedback-wire` | Feedback Wire | trap | LIVE_QA |
| `s1-blood-mic` | Blood Karaoke Microphone | equipment | LIVE_QA |
| `s2-bloodfairies-mosquito-disc-jockey` | Mosquito Disc Jockey | creature | LIVE_QA |
| `s2-bloodfairies-bassquake-colossus` | Bassquake Colossus | creature | LIVE_QA |
| `s2-bloodfairies-glitterglass-flood` | Glitterglass Flood | spell | LIVE_QA |
| `s2-bloodfairies-afterparty-first-aid` | Afterparty First Aid | spell | LIVE_QA |
| `s2-bloodfairies-earworm-feedback` | Earworm Feedback | trap | LIVE_QA |
| `s2-bloodfairies-roadie-megaphone` | Roadie Megaphone | equipment | LIVE_QA |
| `s3-bloodfairies-mosh-firefly` | Moshpit Firefly | creature | LIVE_QA |
| `s3-bloodfairies-pollen-queen` | Punk Pollen Queen | creature | LIVE_QA |
| `s3-bloodfairies-backstage-vamp` | Backstage Vamp | creature | LIVE_QA |
| `s3-bloodfairies-karaoke-oracle` | Riot Karaoke Oracle | creature | LIVE_QA |
| `s3-bloodfairies-tour-bus` | Tour Bus Swarm | creature | LIVE_QA |
| `s3-bloodfairies-headliner` | Blood Moon Headliner | creature | LIVE_QA |
| `s3-bloodfairies-feedback-burst` | Feedback Burst | spell | LIVE_QA |
| `s3-bloodfairies-encore` | Encore or Die | spell | LIVE_QA |
| `s3-bloodfairies-rafter-dive` | Dive from the Rafters | spell | LIVE_QA |
| `s3-bloodfairies-festival-triage` | Festival Triage | spell | LIVE_QA |
| `s3-bloodfairies-cathedral-noise` | Cathedral of Noise | spell | LIVE_QA |
| `s3-bloodfairies-tripcord` | Moshpit Tripcord | trap | LIVE_QA |
| `s3-bloodfairies-amp-socket` | Broken Amp Socket | trap | LIVE_QA |
| `s3-bloodfairies-banana-bouncer` | Bouncer Banana Peel | trap | LIVE_QA |
| `s3-bloodfairies-van-radio` | Tour Van Radio | equipment | LIVE_QA |
| `s3-bloodfairies-encore-boots` | Last Encore Boots | equipment | LIVE_QA |

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
| `union-millwright` | Union Millwright | creature | LIVE_QA |
| `spare-pistons` | Spare Pistons | equipment | LIVE_QA |
| `s1-walking-foundry` | Walking Foundry | creature | LIVE_QA |
| `s1-scrap-welder` | Scrap Welder | creature | LIVE_QA |
| `s1-hydraulic-shift` | Emergency Overtime | spell | LIVE_QA |
| `s1-forge-spark` | Forge Lightning | spell | LIVE_QA |
| `s1-bolt-clamp` | Union Bolt Clamp | trap | LIVE_QA |
| `s1-union-plate` | Collective Bargaining Plate | equipment | LIVE_QA |
| `s2-ironjaw-union-bridgebearer` | Union Bridgebearer | creature | LIVE_QA |
| `s2-ironjaw-foundry-lion` | Foundry Lion | creature | LIVE_QA |
| `s2-ironjaw-shift-change-shove` | Shift-Change Shove | spell | LIVE_QA |
| `s2-ironjaw-spare-rivet-shower` | Spare Rivet Shower | spell | LIVE_QA |
| `s2-ironjaw-hydraulic-lockjaw` | Hydraulic Lockjaw | trap | LIVE_QA |
| `s2-ironjaw-overtime-pistons` | Overtime Pistons | equipment | LIVE_QA |
| `s3-ironjaw-night-welder` | Night Shift Welder | creature | LIVE_QA |
| `s3-ironjaw-dreadnought` | Scrapyard Dreadnought | creature | LIVE_QA |
| `s3-ironjaw-union-cook` | Union Lunch Lady | creature | LIVE_QA |
| `s3-ironjaw-bridgebreaker` | Bridgebreaker Ogre | creature | LIVE_QA |
| `s3-ironjaw-coal-racer` | Coal Cart Racer | creature | LIVE_QA |
| `s3-ironjaw-matriarch` | Iron Matriarch | creature | LIVE_QA |
| `s3-ironjaw-bonus-plate` | Shift Bonus Plates | spell | LIVE_QA |
| `s3-ironjaw-reallocation` | Union Reallocation | spell | LIVE_QA |
| `s3-ironjaw-hammer-register` | Sledgehammer Inventory | spell | LIVE_QA |
| `s3-ironjaw-weld-patch` | Cold-Weld Patch | spell | LIVE_QA |
| `s3-ironjaw-furnace-overdrive` | Furnace Overdrive | spell | LIVE_QA |
| `s3-ironjaw-forklift-chock` | Forklift Chock | trap | LIVE_QA |
| `s3-ironjaw-slag-spill` | Slag Spill | trap | LIVE_QA |
| `s3-ironjaw-overtime-toll` | Overtime Paywall | trap | LIVE_QA |
| `s3-ironjaw-toe-pistons` | Steel-Toed Pistons | equipment | LIVE_QA |
| `s3-ironjaw-foreman-crowbar` | Foreman Crowbar | equipment | LIVE_QA |

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
| `spark-diver` | Spark Diver | creature | LIVE_QA |
| `firebreak-parade` | Firebreak Parade | spell | LIVE_QA |
| `s1-mime-fuse` | Matchstick Mime | creature | LIVE_QA |
| `s1-blast-radius` | Doctor Blast Radius | creature | LIVE_QA |
| `s1-no-witnesses` | No Witnesses, Especially Us | spell | LIVE_QA |
| `s1-chaos-firecracker` | Mystery-Flavor Firecracker | spell | LIVE_QA |
| `s1-fuse-alley` | Bottled Thunder | trap | LIVE_QA |
| `s1-volunteer-vest` | Volunteer Safety Vest | equipment | LIVE_QA |
| `s2-riot-fuse-lit-bicycle-courier` | Fuse-Lit Bicycle Courier | creature | LIVE_QA |
| `s2-riot-radioactive-parade-float` | Radioactive Parade Float | creature | LIVE_QA |
| `s2-riot-friendly-fire-rehearsal` | Friendly-Fire Rehearsal | spell | LIVE_QA |
| `s2-riot-homemade-bottle-rocket` | Homemade Bottle Rocket | spell | LIVE_QA |
| `s2-riot-fusebox-fireworks` | Fusebox Fireworks | trap | LIVE_QA |
| `s2-riot-last-stand-matchbook` | Last-Stand Matchbook | equipment | LIVE_QA |
| `s3-riot-bottle-rocket` | Bottle-Rocket Nun | creature | LIVE_QA |
| `s3-riot-detonation-deacon` | Detonation Deacon | creature | LIVE_QA |
| `s3-riot-alley-prophet` | Alley Prophet of Sparks | creature | LIVE_QA |
| `s3-riot-firework-bishop` | Firework Bishop | creature | LIVE_QA |
| `s3-riot-riot-bike-messenger` | Riot Bike Messenger | creature | LIVE_QA |
| `s3-riot-thermite-archangel` | Thermite Archangel | creature | LIVE_QA |
| `s3-riot-low-budget-grenade` | Low-Budget Grenade | spell | LIVE_QA |
| `s3-riot-wrong-side-of-blast` | Wrong Side of the Blast | spell | LIVE_QA |
| `s3-riot-horrible-idea` | This Is a Horrible Idea | spell | LIVE_QA |
| `s3-riot-stolen-detonator` | Stolen Detonator | spell | LIVE_QA |
| `s3-riot-final-benediction` | Final Benediction of Fire | spell | LIVE_QA |
| `s3-riot-fusewire` | Fusewire Rosary | trap | LIVE_QA |
| `s3-riot-night-market-rocket` | Night Market Rocket | trap | LIVE_QA |
| `s3-riot-confession-booth` | Booby-Trapped Confessional | trap | LIVE_QA |
| `s3-riot-charred-sneakers` | Charred Sneakers | equipment | LIVE_QA |
| `s3-riot-posthumous-saint` | Posthumous Saint Medal | equipment | LIVE_QA |

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
| `pipe-seer` | Pipe Seer | creature | LIVE_QA |
| `snitch-grate` | Snitch Grate | trap | LIVE_QA |
| `s1-basement-ghost` | Basement Ghost | creature | LIVE_QA |
| `s1-static-listener` | Static Listener | creature | LIVE_QA |
| `s1-floodlight-sweep` | Floodlight Sweep | spell | LIVE_QA |
| `s1-wiretap-order` | Wiretap Restraining Order | spell | LIVE_QA |
| `s1-blue-ink-deadfall` | Blue-Ink Deadfall | trap | LIVE_QA |
| `s1-needle-wire` | Needle-Wire Antenna | equipment | LIVE_QA |
| `s2-undertow-drainpipe-interrogator` | Drainpipe Interrogator | creature | LIVE_QA |
| `s2-undertow-subsurface-warden` | Subsurface Warden | creature | LIVE_QA |
| `s2-undertow-floodlight-leak` | Floodlight Leak | spell | LIVE_QA |
| `s2-undertow-backwater-iou` | Backwater IOU | spell | LIVE_QA |
| `s2-undertow-culvert-tollwire` | Culvert Tollwire | trap | LIVE_QA |
| `s2-undertow-wiretap-spikes` | Wiretap Spikes | equipment | LIVE_QA |
| `s3-undertow-drain-sniper` | Drainpipe Sniper | creature | LIVE_QA |
| `s3-undertow-interrogation-eel` | Interrogation Eel | creature | LIVE_QA |
| `s3-undertow-quiet-listener` | Quiet Room Listener | creature | LIVE_QA |
| `s3-undertow-needle-rain-agent` | Needle Rain Agent | creature | LIVE_QA |
| `s3-undertow-basement-watchdog` | Basement Watchdog | creature | LIVE_QA |
| `s3-undertow-sewer-leviathan` | Sewer Leviathan | creature | LIVE_QA |
| `s3-undertow-weep-holes` | Weep Holes in the Wall | spell | LIVE_QA |
| `s3-undertow-long-drain-sting` | Long Drain Sting | spell | LIVE_QA |
| `s3-undertow-reveal-the-ledger` | Reveal the Ledger | spell | LIVE_QA |
| `s3-undertow-quiet-interdiction` | Quiet Interdiction | spell | LIVE_QA |
| `s3-undertow-citywide-blackmail` | Citywide Blackmail | spell | LIVE_QA |
| `s3-undertow-red-tape-sensor` | Red-Tape Sensor | trap | LIVE_QA |
| `s3-undertow-floodgate-clamp` | Floodgate Clamp | trap | LIVE_QA |
| `s3-undertow-anonymous-invoice` | Anonymous Invoice | trap | LIVE_QA |
| `s3-undertow-periscope-lens` | Periscope Lens | equipment | LIVE_QA |
| `s3-undertow-tunnel-harpoon` | Tunnel Harpoon | equipment | LIVE_QA |

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
| `audit-fiend` | Audit Fiend | creature | LIVE_QA |
| `debt-holiday` | Debt Holiday | spell | LIVE_QA |
| `s1-executive-repo` | Executive Repossessor | creature | LIVE_QA |
| `s1-guild-clerk` | Guild Clerk (Temporary) | creature | LIVE_QA |
| `s1-margin-call` | Emergency Margin Call | spell | LIVE_QA |
| `s1-buy-silence` | Buy Their Silence | spell | LIVE_QA |
| `s1-debt-garnish` | Garnishment Floor Tile | trap | LIVE_QA |
| `s1-golden-handshake` | Golden Handshake, Iron Grip | equipment | LIVE_QA |
| `s2-exchange-bargain-rate-collector` | Bargain-Rate Collector | creature | LIVE_QA |
| `s2-exchange-golden-bailiff` | Golden Bailiff | creature | LIVE_QA |
| `s2-exchange-compound-interest-notice` | Compound Interest Notice | spell | LIVE_QA |
| `s2-exchange-contract-amendment` | Contract Amendment | spell | LIVE_QA |
| `s2-exchange-invisible-lien` | Invisible Lien | trap | LIVE_QA |
| `s2-exchange-executive-health-coverage` | Executive Health Coverage | equipment | LIVE_QA |
| `s3-exchange-wage-garnisher` | Wage Garnisher | creature | LIVE_QA |
| `s3-exchange-mortgage-minotaur` | Mortgage Minotaur | creature | LIVE_QA |
| `s3-exchange-retainer-clerk` | Retainer Clerk | creature | LIVE_QA |
| `s3-exchange-seizure-executive` | Seizure Executive | creature | LIVE_QA |
| `s3-exchange-hostile-takeover-goon` | Hostile Takeover Goon | creature | LIVE_QA |
| `s3-exchange-golden-foreclosure` | Golden Foreclosure Engine | creature | LIVE_QA |
| `s3-exchange-payment-reminder` | Payment Reminder | spell | LIVE_QA |
| `s3-exchange-compound-notice` | Compound Notice | spell | LIVE_QA |
| `s3-exchange-executive-incentive` | Executive Incentive | spell | LIVE_QA |
| `s3-exchange-golden-parachute` | Golden Parachute | spell | LIVE_QA |
| `s3-exchange-acquisition-clause` | Acquisition Clause | spell | LIVE_QA |
| `s3-exchange-late-fee-sticker` | Late-Fee Sticker | trap | LIVE_QA |
| `s3-exchange-escrow-snare` | Escrow Snare | trap | LIVE_QA |
| `s3-exchange-repossession-notice` | Repossession Notice | trap | LIVE_QA |
| `s3-exchange-ledger-greaves` | Ledger Greaves | equipment | LIVE_QA |
| `s3-exchange-collection-badge` | Collection Badge | equipment | LIVE_QA |

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
| `merc-sewer-sommelier` | Sewer Sommelier | creature | LIVE_QA |
| `merc-skate-taxidermist` | Skating Taxidermist | creature | LIVE_QA |
| `merc-auction-golem` | Auction Golem | creature | LIVE_QA |
| `merc-spark-midwife` | Midwife of Sparks | creature | LIVE_QA |
| `merc-traffic-witch` | Traffic Witch | creature | LIVE_QA |
| `merc-picket-troll` | Picket Line Troll | creature | LIVE_QA |
| `merc-escape-crab` | Escape Artist Crab | creature | LIVE_QA |
| `merc-living-scaffold` | Living Scaffolding | creature | LIVE_QA |
| `merc-invisible-mime` | Invisible Mime | creature | LIVE_QA |
| `merc-midnight-janitor` | Midnight Janitor | creature | LIVE_QA |
| `merc-misaddressed-parcel` | Misaddressed Parcel | spell | LIVE_QA |
| `merc-crowd-lightning` | Crowd-Sourced Lightning | spell | LIVE_QA |
| `merc-unofficial-detour` | Unofficial Detour | spell | LIVE_QA |
| `merc-reputation-laundry` | Reputation Laundering | spell | LIVE_QA |
| `merc-flashmob-diversion` | Flashmob Diversion | spell | LIVE_QA |
| `merc-jury-rigged-radar` | Jury-Rigged Radar | spell | LIVE_QA |
| `merc-allergy-season` | Allergy Season | spell | LIVE_QA |
| `merc-supervised-demo` | Supervised Demolition | spell | LIVE_QA |
| `merc-unsupervised-demo` | Unsupervised Demolition | spell | LIVE_QA |
| `merc-mortgage-holiday` | Mortgage Holiday | spell | LIVE_QA |
| `merc-secondhand-halo` | Secondhand Halo | spell | LIVE_QA |
| `merc-take-stairs` | Take the Stairs | spell | LIVE_QA |
| `merc-streetlight-confession` | Streetlight Confession | spell | LIVE_QA |
| `merc-homebrew-antidote` | Homebrew Antidote | spell | LIVE_QA |
| `merc-whisper-network` | Whisper Network | spell | LIVE_QA |
| `merc-mothball-storm` | Mothball Storm | spell | LIVE_QA |
| `merc-festival-no-refunds` | Festival of No Refunds | spell | LIVE_QA |
| `merc-union-solidarity` | Union Solidarity | spell | LIVE_QA |
| `merc-glass-echo` | Glass Echo Plate | trap | LIVE_QA |
| `merc-tourist-trapdoor` | Tourist Trapdoor | trap | LIVE_QA |
| `merc-concealed-tollbooth` | Concealed Tollbooth | trap | LIVE_QA |
| `merc-boomerang-buffet` | Boomerang Buffet | trap | LIVE_QA |
| `merc-invisible-bump` | Invisible Speed Bump | trap | LIVE_QA |
| `merc-market-tripwire` | Night Market Tripwire | trap | LIVE_QA |
| `merc-flooded-fusebox` | Flooded Fusebox | trap | LIVE_QA |
| `merc-parking-meter` | Hostile Parking Meter | trap | LIVE_QA |
| `merc-dog-eared-mine` | Dog-Eared Mine | trap | LIVE_QA |
| `merc-cursed-sign` | Cursed Detour Sign | trap | LIVE_QA |
| `merc-ghoul-et-lot` | Ghoul-Et-Lot | trap | LIVE_QA |
| `merc-angry-bees` | Bag of Very Angry Bees | trap | LIVE_QA |
| `merc-borrowed-kneepads` | Borrowed Kneepads | equipment | LIVE_QA |
| `merc-squeaky-wheel` | Squeaky Wheel | equipment | LIVE_QA |
| `merc-edible-kevlar` | Edible Kevlar | equipment | LIVE_QA |
| `merc-emergency-wings` | Emergency Wings | equipment | LIVE_QA |
| `merc-red-tape-scissors` | Red Tape Scissors | equipment | LIVE_QA |
| `merc-theftproof-toolkit` | Theftproof Toolkit | equipment | LIVE_QA |
| `merc-counterfeit-license` | Counterfeit License | equipment | LIVE_QA |
| `merc-rooftop-map` | Rooftop Map | equipment | LIVE_QA |
| `merc-broken-halo` | Broken Halo | equipment | LIVE_QA |
| `merc-union-suit` | Union Suit | equipment | LIVE_QA |

## Keeping this ledger honest

**All 300 IDs now have playable evolution code**; this sheet is not a claim that every arc is balanced, narratively memorable, or visually complete. The 230 `LIVE_QA` rows require follow-up adversarial matchups, distinct-mechanical-journey inspection, real L3 reachability, and independent example fixtures before promotion to `MERGED`. Updating a card must reuse its existing ID. The original design brief is `CLASH-EVOLUTION-DESIGN.md`; QA method and results live in `CLASH-EVOLUTION-QA-2026-11-08.md`.
