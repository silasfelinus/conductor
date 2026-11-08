# Slime City: 300-card individual evolution ledger

**Goal:** every existing collectible has a unique, tested L1 → L2 → L3 mechanical journey, with a payoff worth playing toward. No extra card IDs or generic stat-only final forms. Status is **implementation evidence**, not artwork completion or playtest approval.

**Inventory verified against seven Kind Robots catalog source files:** six factions × 40 + 60 independent mercenary cards = **300 unique IDs**.

**Checkpoint (2026-11-07 PT):** 39 mechanically implemented and merged in PRs #4895/#4901; 20 authored and implemented in the current wave-3 branch but awaiting checks; 11 concepts from the original 70 remain unimplemented; 230 other existing cards still require original, individual ability design. This ledger does not count a generic level/stat upgrade as crafted.

**Source cross-check:** `prototypes.ts` 60 founders; `reserveCards.ts` 12; `gutterCrownWaveTwo.ts` 36; `gutterCrownWaveThree.ts` 36; `gutterCrownFinaleA.ts` 48; `gutterCrownFinaleB.ts` 48; `mercenaryCards.ts` 60. All paths are under Kind Robots `utils/slimeCity/`. IDs were deduplicated across the seven sources, not counted from generated card faces or art jobs.

**Definition of done for each row:** three authored rules texts; three matching mechanics with a genuine L3 inflection; identity/archetype synergies and counterplay; deterministic seeded command replay; target/occupancy/copy-safe rules; battle fixture showing the payoff, not just strings. Review CPU strategic use and how often L3 is reachable. No faction-hate rules.

Legend: `MERGED` tested + on main · `WAVE-3` new code, CI pending · `DESIGNED` one of original 70 concepts still needing implementation · `TODO` no authored arc yet. Later update these rows as cards ship.

## Gene Riot Catgirls (40)

| Card ID | Card name | Type | Evolution status |
|---|---|---|---|
| `lynx` | Neon Lynx | creature | MERGED |
| `mau` | Mau-77 | creature | WAVE-3 |
| `calico` | Clinic Calico | creature | MERGED |
| `chimera` | Madame Chimera | creature | MERGED |
| `pounce` | Catnip Overdrive | spell | MERGED |
| `scentmine` | Scent Mine | trap | WAVE-3 |
| `reknit` | Reknit Serum | spell | MERGED |
| `shredders` | Patent Shredders | equipment | DESIGNED |
| `ninthlife` | Ninth Life Collar | equipment | WAVE-3 |
| `laser` | Laser Pointer | spell | MERGED |
| `splice-runner` | Splice Runner | creature | TODO |
| `mutual-aid` | Mutual Aid Serum | spell | TODO |
| `s1-roof-phantom` | Rooftop Phantom | creature | TODO |
| `s1-alley-vet` | Alley Veterinarian | creature | TODO |
| `s1-clone-salvage` | Secondhand Life | spell | TODO |
| `s1-nine-lives` | Nine Lives, No Refunds | spell | TODO |
| `s1-catnip-tripwire` | Catnip Tripwire | trap | TODO |
| `s1-surgical-piercers` | Surgical Piercers | equipment | TODO |
| `s2-catgirls-backstreet-organ-donor` | Backstreet Organ Donor | creature | TODO |
| `s2-catgirls-parapet-ghost-kitten` | Parapet Ghost-Kitten | creature | TODO |
| `s2-catgirls-emergency-molt` | Emergency Molt | spell | TODO |
| `s2-catgirls-needle-thread-ambush` | Needle-Thread Ambush | spell | TODO |
| `s2-catgirls-sterile-alley-wire` | Sterile Alley Wire | trap | TODO |
| `s2-catgirls-lab-escape-atlas` | Lab Escape Atlas | equipment | TODO |
| `s3-catgirls-glasswalker` | Gutterglass Scout | creature | TODO |
| `s3-catgirls-patent-saboteur` | Patent Saboteur | creature | TODO |
| `s3-catgirls-alley-vet` | Noodle Cart Veterinarian | creature | TODO |
| `s3-catgirls-scalpel-captain` | Velvet Scalpel Captain | creature | TODO |
| `s3-catgirls-bicycle-clinic` | Sutures on Wheels | creature | TODO |
| `s3-catgirls-escaped-tiger` | Gene-Spliced Tiger | creature | TODO |
| `s3-catgirls-sidewalk-stitches` | Sidewalk Stitches | spell | TODO |
| `s3-catgirls-stolen-saw` | Stolen Bone Saw | spell | TODO |
| `s3-catgirls-fire-escape` | Climb the Fire Escape | spell | TODO |
| `s3-catgirls-counterfeit-heart` | Counterfeit Heart | spell | TODO |
| `s3-catgirls-spare-lives` | Spare Nine Lives | spell | TODO |
| `s3-catgirls-suture-line` | Suture Line | trap | TODO |
| `s3-catgirls-garrote` | Catwalk Garrote | trap | TODO |
| `s3-catgirls-false-clinic` | False Clinic Sign | trap | TODO |
| `s3-catgirls-hollow-scalpel` | Hollow Scalpel | equipment | TODO |
| `s3-catgirls-pounce-rig` | Second Pounce Rig | equipment | TODO |

## Punk Bloodfairies (40)

| Card ID | Card name | Type | Evolution status |
|---|---|---|---|
| `sprite` | Bloodsprite | creature | MERGED |
| `pogo` | Pogo Brat | creature | MERGED |
| `razor` | Razorwing | creature | MERGED |
| `queen` | Queen Safety Pin | creature | MERGED |
| `mosh` | Moshpit Massacre | spell | MERGED |
| `bloodwire` | Bloodwire | trap | WAVE-3 |
| `spurs` | Razor Spurs | equipment | DESIGNED |
| `pinprick` | Safety-Pin Stab | spell | WAVE-3 |
| `choker` | Spiked Choker | equipment | DESIGNED |
| `feedback` | Amp-Stack Feedback | spell | WAVE-3 |
| `pogo-punk` | Pogo Punk | creature | TODO |
| `amp-tripwire` | Amp Tripwire | trap | TODO |
| `s1-riot-choir` | Glitter Riot Choir | creature | TODO |
| `s1-pocket-punk` | Pocket-Sized Problem | creature | TODO |
| `s1-confetti-cannon` | Confetti Shrapnel Cannon | spell | TODO |
| `s1-stage-dive` | Unlicensed Stage Dive | spell | TODO |
| `s1-feedback-wire` | Feedback Wire | trap | TODO |
| `s1-blood-mic` | Blood Karaoke Microphone | equipment | TODO |
| `s2-bloodfairies-mosquito-disc-jockey` | Mosquito Disc Jockey | creature | TODO |
| `s2-bloodfairies-bassquake-colossus` | Bassquake Colossus | creature | TODO |
| `s2-bloodfairies-glitterglass-flood` | Glitterglass Flood | spell | TODO |
| `s2-bloodfairies-afterparty-first-aid` | Afterparty First Aid | spell | TODO |
| `s2-bloodfairies-earworm-feedback` | Earworm Feedback | trap | TODO |
| `s2-bloodfairies-roadie-megaphone` | Roadie Megaphone | equipment | TODO |
| `s3-bloodfairies-mosh-firefly` | Moshpit Firefly | creature | TODO |
| `s3-bloodfairies-pollen-queen` | Punk Pollen Queen | creature | TODO |
| `s3-bloodfairies-backstage-vamp` | Backstage Vamp | creature | TODO |
| `s3-bloodfairies-karaoke-oracle` | Riot Karaoke Oracle | creature | TODO |
| `s3-bloodfairies-tour-bus` | Tour Bus Swarm | creature | TODO |
| `s3-bloodfairies-headliner` | Blood Moon Headliner | creature | TODO |
| `s3-bloodfairies-feedback-burst` | Feedback Burst | spell | TODO |
| `s3-bloodfairies-encore` | Encore or Die | spell | TODO |
| `s3-bloodfairies-rafter-dive` | Dive from the Rafters | spell | TODO |
| `s3-bloodfairies-festival-triage` | Festival Triage | spell | TODO |
| `s3-bloodfairies-cathedral-noise` | Cathedral of Noise | spell | TODO |
| `s3-bloodfairies-tripcord` | Moshpit Tripcord | trap | TODO |
| `s3-bloodfairies-amp-socket` | Broken Amp Socket | trap | TODO |
| `s3-bloodfairies-banana-bouncer` | Bouncer Banana Peel | trap | TODO |
| `s3-bloodfairies-van-radio` | Tour Van Radio | equipment | TODO |
| `s3-bloodfairies-encore-boots` | Last Encore Boots | equipment | TODO |

## Ironjaw Chrome Ogres (40)

| Card ID | Card name | Type | Evolution status |
|---|---|---|---|
| `scrapper` | Chrome Scrapper | creature | MERGED |
| `welder` | Spark Welder | creature | MERGED |
| `bulldozer` | Bulld-Ogre | creature | MERGED |
| `juggernaut` | Maw-9000 | creature | MERGED |
| `overclock` | Overclock Core | spell | WAVE-3 |
| `shocktrap` | Shock Plate | trap | WAVE-3 |
| `plating` | Foundry Plating | equipment | MERGED |
| `wreckingfist` | Wrecking Fist | equipment | DESIGNED |
| `ducttape` | Duct-Tape Weld | spell | WAVE-3 |
| `slap` | Hydraulic Slap | spell | DESIGNED |
| `union-millwright` | Union Millwright | creature | TODO |
| `spare-pistons` | Spare Pistons | equipment | TODO |
| `s1-walking-foundry` | Walking Foundry | creature | TODO |
| `s1-scrap-welder` | Scrap Welder | creature | TODO |
| `s1-hydraulic-shift` | Emergency Overtime | spell | TODO |
| `s1-forge-spark` | Forge Lightning | spell | TODO |
| `s1-bolt-clamp` | Union Bolt Clamp | trap | TODO |
| `s1-union-plate` | Collective Bargaining Plate | equipment | TODO |
| `s2-ironjaw-union-bridgebearer` | Union Bridgebearer | creature | TODO |
| `s2-ironjaw-foundry-lion` | Foundry Lion | creature | TODO |
| `s2-ironjaw-shift-change-shove` | Shift-Change Shove | spell | TODO |
| `s2-ironjaw-spare-rivet-shower` | Spare Rivet Shower | spell | TODO |
| `s2-ironjaw-hydraulic-lockjaw` | Hydraulic Lockjaw | trap | TODO |
| `s2-ironjaw-overtime-pistons` | Overtime Pistons | equipment | TODO |
| `s3-ironjaw-night-welder` | Night Shift Welder | creature | TODO |
| `s3-ironjaw-dreadnought` | Scrapyard Dreadnought | creature | TODO |
| `s3-ironjaw-union-cook` | Union Lunch Lady | creature | TODO |
| `s3-ironjaw-bridgebreaker` | Bridgebreaker Ogre | creature | TODO |
| `s3-ironjaw-coal-racer` | Coal Cart Racer | creature | TODO |
| `s3-ironjaw-matriarch` | Iron Matriarch | creature | TODO |
| `s3-ironjaw-bonus-plate` | Shift Bonus Plates | spell | TODO |
| `s3-ironjaw-reallocation` | Union Reallocation | spell | TODO |
| `s3-ironjaw-hammer-register` | Sledgehammer Inventory | spell | TODO |
| `s3-ironjaw-weld-patch` | Cold-Weld Patch | spell | TODO |
| `s3-ironjaw-furnace-overdrive` | Furnace Overdrive | spell | TODO |
| `s3-ironjaw-forklift-chock` | Forklift Chock | trap | TODO |
| `s3-ironjaw-slag-spill` | Slag Spill | trap | TODO |
| `s3-ironjaw-overtime-toll` | Overtime Paywall | trap | TODO |
| `s3-ironjaw-toe-pistons` | Steel-Toed Pistons | equipment | TODO |
| `s3-ironjaw-foreman-crowbar` | Foreman Crowbar | equipment | TODO |

## Riot Saints (40)

| Card ID | Card name | Type | Evolution status |
|---|---|---|---|
| `rat` | Riot Rat | creature | MERGED |
| `firebrand` | Firebrand | creature | MERGED |
| `kaboom` | Sister Kaboom | creature | MERGED |
| `bomber` | Grand Detonator | creature | MERGED |
| `firestorm` | Accidental Firestorm | spell | WAVE-3 |
| `badluck` | Whoops Grenade | trap | DESIGNED |
| `fuse` | Illegal Booster | equipment | DESIGNED |
| `confetti` | Confetti Cannon | spell | MERGED |
| `fusevest` | Lit-Fuse Vest | equipment | WAVE-3 |
| `drink` | Hold My Drink | spell | WAVE-3 |
| `spark-diver` | Spark Diver | creature | TODO |
| `firebreak-parade` | Firebreak Parade | spell | TODO |
| `s1-mime-fuse` | Matchstick Mime | creature | TODO |
| `s1-blast-radius` | Doctor Blast Radius | creature | TODO |
| `s1-no-witnesses` | No Witnesses, Especially Us | spell | TODO |
| `s1-chaos-firecracker` | Mystery-Flavor Firecracker | spell | TODO |
| `s1-fuse-alley` | Bottled Thunder | trap | TODO |
| `s1-volunteer-vest` | Volunteer Safety Vest | equipment | TODO |
| `s2-riot-fuse-lit-bicycle-courier` | Fuse-Lit Bicycle Courier | creature | TODO |
| `s2-riot-radioactive-parade-float` | Radioactive Parade Float | creature | TODO |
| `s2-riot-friendly-fire-rehearsal` | Friendly-Fire Rehearsal | spell | TODO |
| `s2-riot-homemade-bottle-rocket` | Homemade Bottle Rocket | spell | TODO |
| `s2-riot-fusebox-fireworks` | Fusebox Fireworks | trap | TODO |
| `s2-riot-last-stand-matchbook` | Last-Stand Matchbook | equipment | TODO |
| `s3-riot-bottle-rocket` | Bottle-Rocket Nun | creature | TODO |
| `s3-riot-detonation-deacon` | Detonation Deacon | creature | TODO |
| `s3-riot-alley-prophet` | Alley Prophet of Sparks | creature | TODO |
| `s3-riot-firework-bishop` | Firework Bishop | creature | TODO |
| `s3-riot-riot-bike-messenger` | Riot Bike Messenger | creature | TODO |
| `s3-riot-thermite-archangel` | Thermite Archangel | creature | TODO |
| `s3-riot-low-budget-grenade` | Low-Budget Grenade | spell | TODO |
| `s3-riot-wrong-side-of-blast` | Wrong Side of the Blast | spell | TODO |
| `s3-riot-horrible-idea` | This Is a Horrible Idea | spell | TODO |
| `s3-riot-stolen-detonator` | Stolen Detonator | spell | TODO |
| `s3-riot-final-benediction` | Final Benediction of Fire | spell | TODO |
| `s3-riot-fusewire` | Fusewire Rosary | trap | TODO |
| `s3-riot-night-market-rocket` | Night Market Rocket | trap | TODO |
| `s3-riot-confession-booth` | Booby-Trapped Confessional | trap | TODO |
| `s3-riot-charred-sneakers` | Charred Sneakers | equipment | TODO |
| `s3-riot-posthumous-saint` | Posthumous Saint Medal | equipment | TODO |

## Undertow Intelligence (40)

| Card ID | Card name | Type | Evolution status |
|---|---|---|---|
| `watcher` | Sewer Watcher | creature | MERGED |
| `frogtrooper` | Frog Trooper | creature | MERGED |
| `eel` | Eel Courier | creature | MERGED |
| `oracle` | Drowned Oracle | creature | MERGED |
| `blackout` | Signal Blackout | spell | WAVE-3 |
| `tripwire` | Tripwire | trap | MERGED |
| `visor` | Spyglass Visor | equipment | DESIGNED |
| `grate` | Leech Grate | trap | WAVE-3 |
| `sonar` | Drain Sonar | spell | MERGED |
| `drysuit` | Rubber Drysuit | equipment | WAVE-3 |
| `pipe-seer` | Pipe Seer | creature | TODO |
| `snitch-grate` | Snitch Grate | trap | TODO |
| `s1-basement-ghost` | Basement Ghost | creature | TODO |
| `s1-static-listener` | Static Listener | creature | TODO |
| `s1-floodlight-sweep` | Floodlight Sweep | spell | TODO |
| `s1-wiretap-order` | Wiretap Restraining Order | spell | TODO |
| `s1-blue-ink-deadfall` | Blue-Ink Deadfall | trap | TODO |
| `s1-needle-wire` | Needle-Wire Antenna | equipment | TODO |
| `s2-undertow-drainpipe-interrogator` | Drainpipe Interrogator | creature | TODO |
| `s2-undertow-subsurface-warden` | Subsurface Warden | creature | TODO |
| `s2-undertow-floodlight-leak` | Floodlight Leak | spell | TODO |
| `s2-undertow-backwater-iou` | Backwater IOU | spell | TODO |
| `s2-undertow-culvert-tollwire` | Culvert Tollwire | trap | TODO |
| `s2-undertow-wiretap-spikes` | Wiretap Spikes | equipment | TODO |
| `s3-undertow-drain-sniper` | Drainpipe Sniper | creature | TODO |
| `s3-undertow-interrogation-eel` | Interrogation Eel | creature | TODO |
| `s3-undertow-quiet-listener` | Quiet Room Listener | creature | TODO |
| `s3-undertow-needle-rain-agent` | Needle Rain Agent | creature | TODO |
| `s3-undertow-basement-watchdog` | Basement Watchdog | creature | TODO |
| `s3-undertow-sewer-leviathan` | Sewer Leviathan | creature | TODO |
| `s3-undertow-weep-holes` | Weep Holes in the Wall | spell | TODO |
| `s3-undertow-long-drain-sting` | Long Drain Sting | spell | TODO |
| `s3-undertow-reveal-the-ledger` | Reveal the Ledger | spell | TODO |
| `s3-undertow-quiet-interdiction` | Quiet Interdiction | spell | TODO |
| `s3-undertow-citywide-blackmail` | Citywide Blackmail | spell | TODO |
| `s3-undertow-red-tape-sensor` | Red-Tape Sensor | trap | TODO |
| `s3-undertow-floodgate-clamp` | Floodgate Clamp | trap | TODO |
| `s3-undertow-anonymous-invoice` | Anonymous Invoice | trap | TODO |
| `s3-undertow-periscope-lens` | Periscope Lens | equipment | TODO |
| `s3-undertow-tunnel-harpoon` | Tunnel Harpoon | equipment | TODO |

## Meat Exchange (40)

| Card ID | Card name | Type | Evolution status |
|---|---|---|---|
| `repo` | Repo Goblin | creature | MERGED |
| `collector` | Debt Collector | creature | MERGED |
| `broker` | Flesh Broker | creature | MERGED |
| `mogul` | The Meat Mogul | creature | MERGED |
| `collection` | Hostile Collection | spell | WAVE-3 |
| `debttrap` | Hidden Fees | trap | WAVE-3 |
| `contract` | Iron Contract | equipment | DESIGNED |
| `foreclosure` | Foreclosure | spell | MERGED |
| `handshake` | Golden Handshake | equipment | MERGED |
| `hushmoney` | Hush Money | spell | WAVE-3 |
| `audit-fiend` | Audit Fiend | creature | TODO |
| `debt-holiday` | Debt Holiday | spell | TODO |
| `s1-executive-repo` | Executive Repossessor | creature | TODO |
| `s1-guild-clerk` | Guild Clerk (Temporary) | creature | TODO |
| `s1-margin-call` | Emergency Margin Call | spell | TODO |
| `s1-buy-silence` | Buy Their Silence | spell | TODO |
| `s1-debt-garnish` | Garnishment Floor Tile | trap | TODO |
| `s1-golden-handshake` | Golden Handshake, Iron Grip | equipment | TODO |
| `s2-exchange-bargain-rate-collector` | Bargain-Rate Collector | creature | TODO |
| `s2-exchange-golden-bailiff` | Golden Bailiff | creature | TODO |
| `s2-exchange-compound-interest-notice` | Compound Interest Notice | spell | TODO |
| `s2-exchange-contract-amendment` | Contract Amendment | spell | TODO |
| `s2-exchange-invisible-lien` | Invisible Lien | trap | TODO |
| `s2-exchange-executive-health-coverage` | Executive Health Coverage | equipment | TODO |
| `s3-exchange-wage-garnisher` | Wage Garnisher | creature | TODO |
| `s3-exchange-mortgage-minotaur` | Mortgage Minotaur | creature | TODO |
| `s3-exchange-retainer-clerk` | Retainer Clerk | creature | TODO |
| `s3-exchange-seizure-executive` | Seizure Executive | creature | TODO |
| `s3-exchange-hostile-takeover-goon` | Hostile Takeover Goon | creature | TODO |
| `s3-exchange-golden-foreclosure` | Golden Foreclosure Engine | creature | TODO |
| `s3-exchange-payment-reminder` | Payment Reminder | spell | TODO |
| `s3-exchange-compound-notice` | Compound Notice | spell | TODO |
| `s3-exchange-executive-incentive` | Executive Incentive | spell | TODO |
| `s3-exchange-golden-parachute` | Golden Parachute | spell | TODO |
| `s3-exchange-acquisition-clause` | Acquisition Clause | spell | TODO |
| `s3-exchange-late-fee-sticker` | Late-Fee Sticker | trap | TODO |
| `s3-exchange-escrow-snare` | Escrow Snare | trap | TODO |
| `s3-exchange-repossession-notice` | Repossession Notice | trap | TODO |
| `s3-exchange-ledger-greaves` | Ledger Greaves | equipment | TODO |
| `s3-exchange-collection-badge` | Collection Badge | equipment | TODO |

## Mercenary Underground (60)

| Card ID | Card name | Type | Evolution status |
|---|---|---|---|
| `merc-bus-driver` | Gutterbus Driver | creature | WAVE-3 |
| `merc-bribe-rat` | Bribe-Licked Rat | creature | DESIGNED |
| `merc-roof-dentist` | Rooftop Dentist | creature | MERGED |
| `merc-debt-slug` | Debt-Eating Slug | creature | MERGED |
| `merc-clock-grandma` | Clockwork Grandmother | creature | WAVE-3 |
| `merc-smog-moth` | Smog Moth Courier | creature | MERGED |
| `merc-grease-oracle` | Grease Oracle | creature | DESIGNED |
| `merc-fungal-bouncer` | Fungal Bouncer | creature | MERGED |
| `merc-discount-angel` | Discount Archangel | creature | MERGED |
| `merc-union-owl` | Owl of All Trades | creature | MERGED |
| `merc-sewer-sommelier` | Sewer Sommelier | creature | TODO |
| `merc-skate-taxidermist` | Skating Taxidermist | creature | TODO |
| `merc-auction-golem` | Auction Golem | creature | TODO |
| `merc-spark-midwife` | Midwife of Sparks | creature | TODO |
| `merc-traffic-witch` | Traffic Witch | creature | TODO |
| `merc-picket-troll` | Picket Line Troll | creature | TODO |
| `merc-escape-crab` | Escape Artist Crab | creature | TODO |
| `merc-living-scaffold` | Living Scaffolding | creature | TODO |
| `merc-invisible-mime` | Invisible Mime | creature | TODO |
| `merc-midnight-janitor` | Midnight Janitor | creature | TODO |
| `merc-misaddressed-parcel` | Misaddressed Parcel | spell | TODO |
| `merc-crowd-lightning` | Crowd-Sourced Lightning | spell | TODO |
| `merc-unofficial-detour` | Unofficial Detour | spell | TODO |
| `merc-reputation-laundry` | Reputation Laundering | spell | TODO |
| `merc-flashmob-diversion` | Flashmob Diversion | spell | TODO |
| `merc-jury-rigged-radar` | Jury-Rigged Radar | spell | TODO |
| `merc-allergy-season` | Allergy Season | spell | TODO |
| `merc-supervised-demo` | Supervised Demolition | spell | TODO |
| `merc-unsupervised-demo` | Unsupervised Demolition | spell | TODO |
| `merc-mortgage-holiday` | Mortgage Holiday | spell | TODO |
| `merc-secondhand-halo` | Secondhand Halo | spell | TODO |
| `merc-take-stairs` | Take the Stairs | spell | TODO |
| `merc-streetlight-confession` | Streetlight Confession | spell | TODO |
| `merc-homebrew-antidote` | Homebrew Antidote | spell | TODO |
| `merc-whisper-network` | Whisper Network | spell | TODO |
| `merc-mothball-storm` | Mothball Storm | spell | TODO |
| `merc-festival-no-refunds` | Festival of No Refunds | spell | TODO |
| `merc-union-solidarity` | Union Solidarity | spell | TODO |
| `merc-glass-echo` | Glass Echo Plate | trap | TODO |
| `merc-tourist-trapdoor` | Tourist Trapdoor | trap | TODO |
| `merc-concealed-tollbooth` | Concealed Tollbooth | trap | TODO |
| `merc-boomerang-buffet` | Boomerang Buffet | trap | TODO |
| `merc-invisible-bump` | Invisible Speed Bump | trap | TODO |
| `merc-market-tripwire` | Night Market Tripwire | trap | TODO |
| `merc-flooded-fusebox` | Flooded Fusebox | trap | TODO |
| `merc-parking-meter` | Hostile Parking Meter | trap | TODO |
| `merc-dog-eared-mine` | Dog-Eared Mine | trap | TODO |
| `merc-cursed-sign` | Cursed Detour Sign | trap | TODO |
| `merc-ghoul-et-lot` | Ghoul-Et-Lot | trap | TODO |
| `merc-angry-bees` | Bag of Very Angry Bees | trap | TODO |
| `merc-borrowed-kneepads` | Borrowed Kneepads | equipment | TODO |
| `merc-squeaky-wheel` | Squeaky Wheel | equipment | TODO |
| `merc-edible-kevlar` | Edible Kevlar | equipment | TODO |
| `merc-emergency-wings` | Emergency Wings | equipment | TODO |
| `merc-red-tape-scissors` | Red Tape Scissors | equipment | TODO |
| `merc-theftproof-toolkit` | Theftproof Toolkit | equipment | TODO |
| `merc-counterfeit-license` | Counterfeit License | equipment | TODO |
| `merc-rooftop-map` | Rooftop Map | equipment | TODO |
| `merc-broken-halo` | Broken Halo | equipment | TODO |
| `merc-union-suit` | Union Suit | equipment | TODO |

## Keeping this ledger honest

This sheet is **not** an autogenerated claim that 300 cards already have custom mechanics. A card moves to `MERGED` only when its playable effect, text, replay tests and latest-head CI have landed on main. Whenever new work overlaps a previous card, update the row rather than adding a collectible duplicate. The original design brief remains `CLASH-EVOLUTION-DESIGN.md`; this document is the complete roster and its implementation debt.
