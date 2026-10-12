# Rainbow Bullet Hell Space Princess: World & Production Bible
Status: **proposed authored canon (design only)**. Owner: rainbow-bullet-hell-space-princess. 2026-10-11 PT. This document is a production specification, not a claim of finished levels, generated art, implemented weapons, or multiplayer netcode.

## One-sentence world rule
The Luminous Ocean is a navigable star sea where living beings and machine-reef ships coexist. The **Prism Eclipse** turns wildlife-shaped rescue fleets into aggressive instrument-ships. The princess pilots must disrupt its control signal while preserving the infected creatures inside the hulls: defeat hostile hardware, save the life within. Never render boss death as animal cruelty.

## Four pilots: narrative and exact gameplay roles
All four are original, explicitly competent pilots, selected independently by each of up to four simultaneous players. Characters are authored, never randomized at runtime, and support skippable subtitles in group scenes.

**Casting and character-design authority:** [CAST-BIBLE.md](CAST-BIBLE.md). On 2026-10-11 PT Silas specified a diverse four-pilot ensemble encompassing a short-haired tomboy, a muscular princess, a tall trans-coded princess, and a curvy queer punk princess, with distinct cultural heritages, genders, personalities and body types. Preserve the established ship color/weapons, but merge stronger existing visual design elements where compatible. Never reduce a person to a demographic checklist. This row table summarizes mechanics; CAST-BIBLE contains the canonical appearance, identity, personal arc, relationships and prompts.

| ID | Pilot, ship, silhouette | Primary / focused fire | Super (earned charges, not spammable) | Story conflict |
| --- | --- | --- | --- | --- |
| P1 | **Princess Maribel Rowan** (short-haired tomboy, she/they, Irish-Norwegian family influences), *Petal Wing*: four swept swallowtail blades, rose-pink | wide Petal Spray / tight Rose Needle | **Bloom Nova**: cancels nearby projectiles and breaks light armor | Tries to rescue everyone even when it slows the fleet |
| P2 | **Princess Azure Lin** (tall Vietnamese-heritage trans woman, she/her), *Prism Lance*: pointed long single fin, powder cyan | piercing Prism Thread / charged Narrow Beam | **Tidal Prism**: sustained forward beam and guard wedge | Values a direct attack, must learn patience |
| P3 | **Princess Solenne Adisa** (muscular Black Nigerian-heritage pilot, she/her), *Halo Fin*: broad round disc and twin ringlets, butter yellow | two orbit drones / concentrated linked shots | **Halo Harbor**: shared brief shield + limited team revive | Responsible for surviving cadets |
| P4 | **Princess Vivi Reyes** (curvy queer Mexican-heritage punk, they/she), *Comet Crown*: three-point lilac arrowhead | rapid Spark Lances / delayed ricochet arc | **Comet Parade**: target-locked rainbow fleet of temporary drones | Wants glory and discovers quiet sacrifice |

**Comms continuity:** [COMMS-AND-ENDINGS-BIBLE.md](COMMS-AND-ENDINGS-BIBLE.md) defines **Lilt-7**, the always-present synthetic/alien mothership liaison, the authored 15-party-mask banter/reveal tracks, and composited ending cinematics. Lilt remains distinct from the existing Captain Purl tutorial mentor, Professor Opal engineer, and Nemi translator. Every solo playthrough must have meaningful banter and a complete Lilt arc. The Lilt reveal in S06 is mandatory but never blocks a clear.

Supporting cast: **Lilt-7** (Aurora Mercy mothership liaison; universal comms, own agency and story arc), **Captain Purl** (retired sea-mine navigator; tutorials/comms), **Professor Opal** (engineer and powerup host), **Nemi** (rescued jellyfish pilot and translator), **The Coral Choir** (survivor collective providing route intelligence), **The Crown Voice** (machine intelligence that mistakes perfect order for kindness), **The Lost Navigator** (rescued optional character who unlocks alternate finale route). Each gets one intro portrait, expression atlas, communication silhouette and credited voice-subtitle cue. No character portrait copied from existing franchises.

Ship geometry requirements: all four hulls use the same fair **central collision core** in normal mode, only clearly cosmetic silhouette differences; focus speed 55% of base, invulnerability signal after taking damage, selectable same power budget. Unique shots change playstyle, not the ability to survive a mandatory phase.

## Enemy behavior atlas
The following 24 variants are **mechanically** distinct; variants are authored presets, not recolors. Entries list readable tell, actual attack, player response and intended first stage.

| ID | Machine-life craft | Tell → behavior → counter | Debut |
| --- | --- | --- | --- |
| E01 | Seahorse Picket | glowing tail → sinusoidal single lane → pre-aim and sidestep | 1 |
| E02 | Seahorse Spiral Scout | curled fin → 3-point tightening spiral → escape opening at end | 1 |
| E03 | Seahorse Anchor | drops bead → stationary mine on a path → shoot anchor before crossing | 1 |
| E04 | Pearl Urchin | bristles fan → eight outward pellets with two gaps → use slow focus | 1 |
| E05 | Moonjelly Lantern | bell charges slowly → expanding pulsed ring → pass through large gap | 2 |
| E06 | Moonjelly Relay | paired tentacles light → one delayed lightning link → leave link corridor | 2 |
| E07 | Moonjelly Skimmer | folds bell → falling electric beads → move under spent column | 2 |
| E08 | Coral Drifter | coral chamber flashes → leaves breakable cover → choose safe opening | 2 |
| E09 | Clawstrike Shrimp | cannon retracts → straight kinetic bolt → leave targeting lane early | 3 |
| E10 | Pistol Shrimp Shuttle | bubble coils → timed concussive sphere → avoid its expanding edge | 3 |
| E11 | Angler Decoy | false pickup halo flickers → lures to trap → check cross-shaped warning | 3 |
| E12 | Glassfin Skate | mirrors tilt → reflected one-bounce pellet → read marked ricochet edge | 3 |
| E13 | Dolphin Pair | dual beacons pulse → crossed synchronized dives → exploit central stagger | 4 |
| E14 | Dolphin Courier | cargo light flickers → fast flyby / escort target → intercept without friendly fire | 4 |
| E15 | Electric Eel Threader | line segment lights → short lane barrier → travel around bright ends | 4 |
| E16 | Shark Cutter | jaws open twice → fast lateral charge → bait its single recovery lane | 5 |
| E17 | Shark Hammerhead | fin pods lock → opposing missiles → destroy one fin pod to make safe lane | 5 |
| E18 | Octopus Salvager | four arms point → grabs floating armor → shoot arms to disable grab | 5 |
| E19 | Manta Broodship | body wing shadows → deploys smaller interceptors → focus pod weak points | 6 |
| E20 | Reef Turret | flowers unfold → aimed petal barrage → strip stem or use terrain | 6 |
| E21 | Nautilus Bulwark | shell window opens → slow sweeping barrier → damage exposed spiral eye | 6 |
| E22 | Mirror Eel | blue afterimage → phased near-copy projectile → distinguish solid outlined pellet | 7 |
| E23 | Crystal Squid | lens glitters → splits one pellet into three after fixed delay → track split timer | 7 |
| E24 | Crown Harbinger | prismatic prism warms → remixes two earlier patterns → identify one at a time | 8 |

Tier design for production art: scout / veteran / guardian is 3 silhouette evolutions per **family** only when new mechanics justify an atlas. Enemy colors do not communicate threat alone: danger outline, pulse frequency and sound distinguish attacks. Never label E01–E24 implemented until a corresponding tested enemy state machine is merged.

## Stage score: eight authored chapters and finale
Every stage has four beats: reveal, learn, remix and boss approach. Target a measured **10–15 min first clear per chapter**, excluding retries; prototype timing is not evidence. Each includes optional loot pockets with accessible alternatives and actual checkpoints.

| ID | Background layers (far→near) | Four encounter beats | Choice / collectible | Boss |
| --- | --- | --- | --- | --- |
| S01 Pinkwake Estuary | pink cloud sea; glass buoys; pearly shoal; foreground coral | school of E01; E02 spiral; E03 mine corridors; E04 escort | rescue stranded station for shield cell | B01 Pearl Seahorse |
| S02 Moonjelly Fields | translucent nebula; floating bell towers; charged tendrils; passing glass fronds | E05 gap lesson; E06 relays; cross-linked relays; breakable E08 cover | Nemi rescued or left, influences S08 support | B02 Aurelia Array |
| S03 Chromatic Trench | indigo void; volcanic vents; abandoned vaults; near rock ribs | E09 snipers; E10 concussive pockets; E11 lure; E12 ricochets | salvage vault or safe passage | B03 Clawburst |
| S04 Rosefin Express | streaming aurora; transit rings; migrating trains; near light rails | acceleration intro; E13 pairs; E14 escort; E15 barrier remix | rescue courier, unlock optional escort beat | B04 Delphion |
| S05 Blossom Wreckyard | ship graveyard stars; petal wreck slabs; dock machinery; foreground broken hull | E16 charge lane; E17 side pods; E18 grab; moving scrap field | liberate survivor depot or raid armory | B05 Sawtooth Regent |
| S06 Crown Reef | gold nebula; coral megastructures; bioluminescent arches; branch tendrils | E19 brood; E20 destructible stems; E21 bulwark; timed reef gate | choose shield cache or damage relay route | B06 Lantern Ray |
| S07 Glass Current | mirrored star canyon; crystalline strata; fractured beams; front lens ribbons | E22 false copies; E23 delayed splits; old patterns refracted; break prism pylons | optional Lost Navigator rescue | B07 Glass Eel |
| S08 Eclipse Palace | eclipse corona; captive armada; heart spires; near pearl fractures | E24 warning; recognizable legacy motifs; convoy protection; climb to core | payoff for earlier rescue and route choices | B08 Prism Leviathan |
| S09 Finale | machine nerve halo; fractured stained glass; distant reunited fleet; foreground crown fragments | single dramatic boss, three distinct playable phases, moral choice then earned escape | restore/evacuate/sacrifice routes | B09 Eclipse Crown |

Progress flags (persistent, named): rescuedNemi, securedSalvage, rescuedCourier, freedDepot, stoppedRelay, rescuedNavigator. These alter dialogue, support pickups, ending art and optional difficulty goals but must not block the canonical clear. Branch exits reconnect; no undocumented divergent 8th-stage skip.

## Boss move sheets (mechanics, cues, breakable parts)
| ID | Silhouette and weak spot | Phase 1 -> phase 2 -> finish, with mandatory readable tell | Defeat/rescue image |
| --- | --- | --- | --- |
| B01 Pearl Seahorse | tall coil cruiser; glowing pearl throat | rolling 3-bullet pearls → rotating tail shield → exposed throat | pearl cracks and living pod escapes |
| B02 Aurelia Array | three translucent bells; central antenna | linked current lanes → timed bell contractions → sever relays | freed luminous jelly colony |
| B03 Clawburst | mantis-shrimp forward punch cannon; joint socket | single rail shot → alternating armor fists → charge-break window | shattered cannon, rescued pilot |
| B04 Delphion | two dolphin scimitar ships; rear coupling | synchronized crossing → leapfrog lane swap → link core exposed | fleet chooses free movement |
| B05 Sawtooth Regent | shark wedge cruiser; jaw hinge | charge jaw warning → missile hammerhead escort → fin-to-jaw vulnerability | broken teeth become coral rain |
| B06 Lantern Ray | immense manta carrier; underside beacons | broad shadow lanes → two removable drone nurseries → beacon exposed | juveniles drift away alive |
| B07 Glass Eel | silver threaded dreadnought; solid core in afterimages | fake ghost copy → delayed ricochet splits → true core remains outlined | mirrored shell fragments peel back |
| B08 Prism Leviathan | vast whale-shaped palace escort; forehead gem | tidal resonant wave → four removable spire locks → whale core stabilizes | captive whale fleet freed |
| B09 Eclipse Crown | circular crown-machine; heart node | 1) spoke hazard / generous gaps → 2) moving exposed heart → 3) team escape through shrinking prism corridors | full-screen liberation sequence, not an endless boss loop |

Every boss phase is a separate deterministic pattern fixture with **telegraph, active, recovery** frames defined by engineering and verified with worst-position replay. Damage feedback comes from breakable functional modules. Bosses have at least one visually dramatic but never collision-obscuring transition.

## Upgrade and pickup catalog
| ID | Name | Rules, counters, visual pickup shape |
| --- | --- | --- |
| U01 | Rose Petal Matrix | spread 1/2/3 lanes, 35% less damage per lane at widest tier, pink fan diamond |
| U02 | Prism Needle | concentrated piercing beam; charge up to 0.8s; cyan thin diamond |
| U03 | Tide Tracker | limited homing buds, capped concurrent projectiles; teal arrow charm |
| U04 | Orbit Garden | 1–3 guard drones intercept one incoming pellet each on cooldown; lilac ring charm |
| U05 | Echo Charge | slow focused heavy projectile that breaches armor modules; gold crescent |
| U06 | Bubble Shield | +1 layer up to 3; never fully invulnerable; white hexagon |
| U07 | Repair Pearl | restores one life after enough collectible shards; pink heart with dark rim |
| U08 | Super Shard | fills limited special gauge; max 2 banked; prism star |
| U09 | Rescue Beacon | revives one downed co-op player at cost of shared token; green beacon |
| U10 | Mirror Lens | briefly highlights reflected shots and boss weak points; blue outlined eye |
| U11 | Score Coral | multiplier collectible, no combat stat; gold coral bud |
| U12 | Recovery Cache | drops partial previous loadout on lost life, accessible within 4s; white chevron |

Weapon levels and shield counts are data, validated as bounded scalars; all default loadouts must be able to clear every boss. Supers share a cooldown and cannot erase a boss without interacting with at least one authored phase. Bullet telegraphs distinguish dangerous from decorative particles in grayscale and reduced-motion mode.

## Cinematic storyboard / shot inventory
| Shot IDs | Narrative shot | Asset / implementation |
| --- | --- | --- |
| C01–C03 | calm Luminous Ocean palace; migrating fleet; alarm in mirror-glass | 3 panoramic intro plates, separate subtitle overlay |
| C04–C06 | four pilots power up in separate chambers; seamless launch choreography | 4 character portraits + 3 animation plates |
| C07–C09 | Eclipse machine captures wildlife; first pearl carrier revealed; player control handoff | 3 intro battle plates, skip-to-game supported |
| C10–C11 | Nemi signal decoded after S02; choices acknowledged | 2 midgame interlude plates |
| C12–C13 | Lost Navigator memory after S05/S07; reveal machine motivation | 2 late interlude plates |
| C14–C16 | route-conditioned liberation / evacuation / bittersweet finale | 3 ending families with 2–3 layered illustrations each |
| C17 | world restored and playable ship credits parade | original scrolling credits with pause/skip |

Render subtitles as actual text; any static image text is non-canonical. Cutscenes can be skipped and rewatched in an admin-only gallery without losing flags. Avoid spoilers in public preview; GitHub source docs can freely include them.

## Asset production tickets (queued design targets; nothing rendered or submitted here)
- A-PILOT-01..04: 4 pilot portrait rigs × neutral/confident/concerned; full ship profile + top view, 12 thrust/tilt frames per hull and deterministic collision core guide.
- A-ENEMY-01..24: 24 behavior silhouettes, idle/telegraph/fire/damage/destruction clips, hitbox overlays, texture atlases; optional veteran forms only when mechanically distinct.
- A-BOSS-01..09: layered hull plates, articulation/hit-zones, 3 phase palettes, telegraph atlas, rescue cut-in and destruction pass.
- A-STAGE-01..08: four independent parallax planes per stage, exposure/contrast variants and UI-safe margins; S09 has its own finale backdrop.
- A-HUD: 4 player markers, shield pips, supers, hit flashes, pickups and accessibility symbols, working at 375px.
- A-FX: friendly fire families vs lethal enemy bullet families, shields, explosion/super shader and reduced-motion replacements.
- A-CIN-01..17: narrative panels as listed; original music themes/voice-optional SFX and subtitles.
- Target visual capture: 375/768/1440 browser widths, a full 4-player boss phase at 60Hz, contrast/readability reference at dim brightness.

**ArtJob tracking rule:** for every actual internal queue submission add a manifest row with ticket, prompt revision, generator/server, seed, Job ID, status, approved asset URL, license/provenance, atlas mapping and CI/screenshot evidence. An art prompt alone is not an asset. No queue submission or paid compute is claimed by this file.

## Build order and handoff gates
1. Implement P1/P2 hull geometry and E01–E04 in the shared Arcade preview, record deterministic hitbox/weapon tests.
2. Prove S01 four beats + B01 phase fixture, checkpoint, pause/replay and first mobile visual audit.
3. Add P3/P4 and real four-seat collision soak, then rooms/netcode with rollback/reconnect.
4. Expand S02..S08 from this authored score, ship boss-by-boss, keep all progression flags serializable and route exits verifiable.
5. Produce mastered art/sound from tracked ArtJobs and perform whole-campaign first-clear and 1/2/3/4-player timings.
6. Final human verdict and **separate** public release approval. No public route/Arcade hall entries before the release gate.
