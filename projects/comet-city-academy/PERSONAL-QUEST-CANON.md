# Prom of Doom: 48 personal mysteries and identity consequences

This is **authoring canon and production scope**, not final 288-track completion. The additional case chain complements the existing `identitySerial.ts` chapters on days **4, 12, 21, and 27**, without replacing any of them. The playable first expansion is [Kind Robots `utils/cometAcademy/personalQuests.ts`](https://github.com/silasfelinus/kind_robots/blob/main/utils/cometAcademy/personalQuests.ts) paired with `personalQuests.json`. Branch source is subject to green PR merge.

## Drama model

Each original adult Comet City character owns a civilian past, a **student/sidekick**, a materially different **hero**, and a materially different **villain** future. New playable personal cases create four escalating decision scenes on days **6, 9, 19, 22**:

1. **Day 6 · Secret and witness:** reveal the physical evidence of the origin scandal. Protect the person at risk, confront the institution, or exploit the information.
2. **Day 9 · Intimacy and trust:** the identified adult witness/ally sets an original personal boundary. Invite an equal partnership, disclose the evidence and accept their decision, or break confidence. This creates **no automatic romance** and never lets a player force consent.
3. **Day 19 · Personal betrayal:** the distinct character-local betrayal surfaces, separately from the campaign's compulsory but independently foreshadowed NPC heel turn. The witness may be protected, the accused confronted, or the scandal weaponized.
4. **Day 22 · The identity reckoning:** student, hero, and villain have different canonical methods, and the last personal choice changes the story's graduating epilogue. This is separate from the previously earned day-16/day-23 hero/villain mantle checkpoints.

Choice history is validated and saved as `AcademyRun.personalHistory`. Older saved games without that property remain valid. Trust/betrayal modifies night-patrol effectiveness and prom-night support; personal relationships have negotiated boundaries and consequences, but the existing 6-student social engine is **not** silently expanded to 48 romance options. Four stages × three options × 48 identities = **576 new personal decision opportunities** added to the existing 576 choices across four identity-serial chapters, not 1,152 independent authored scripts. Each of the 48 cases has a unique location, named witness, evidence, betrayer and repair gesture.

## Individual cases and actor autonomy

| Civilian / identity | Personal landmark | Independent witness / ally | Core evidence and betrayal |
| --- | --- | --- | --- |
| **Dez Okafor** (Hotplate / Backdraft / Flashpoint) | Neon Row kitchen | Marta Bell, the food-cart union steward | The gas inspection ledger was signed after the explosion; his former manager sold the inspection stamps |
| **Pip Marchetti** (Windsock / Skyline / The Vacuum) | Comet Airfield hangar | Raul Chen, the runway marshal | The lightning rods were intentionally disconnected; the flight instructor kept the control-room key |
| **Tobias "Tug" Brannigan** (Pebble / Cornerstone / Sinkhole) | Old Quarry tunnel | Selma Pike, the rescue diver | A day-six stop-work order hides a private bank entrance; the rescue superintendent took a sealed envelope |
| **Marisol Reyes** (Splash / Tidewarden / Dry Season) | Comet Power spillway | Greta Solis, the family attorney | Cooling-pond discharge reports were altered; a company chemist sent the family a counterfeit sample |
| **Kenji Watanabe-Cole** (Bokken / The Second Hand / Metronome) | Narrows satellite observatory | Yuki Dela Cruz, the sparring partner | A defense contractor planted the orbital fragment; the dojo sponsor registered it as school property |
| **Ottoline "Otto" Fairweather** (Beaker / Eureka / Countess Calculus) | Morrow Pharmaceuticals cold room | Bea Ruiz, the lab custodian | The unlabeled beaker belonged to a discontinued memory trial; the professor shredded patients' consent forms |
| **Augustin "Gus" Valcourt-Hale** (Hand-Me-Down / Captain Valcourt / The Heirloom) | Valcourt family trophy room | Nico Vale, the estate archivist | A lightning rig was hidden behind grandfather's medals; an uncle rewrote the cape's inheritance trust |
| **Fen Halloran** (Busker / Chorus / The Headliner) | Old Market broadcast kiosk | Zadie Moon, the street percussionist | A signal booster altered every busker's voiceprint; the producer bought fake audition consent forms |
| **Ruby Szabo** (Tinder / Ashborn / Pyre) | Mutation Ministry archives | Darla Finch, the registry clerk | The copied memory is stored as an active government file; a school counselor handed the file to the registry |
| **Corvin Ashe** (Fledgling / Kestrel / The Rookery) | Garment District feather mill | Evelyn Moss, the union tailor | Designer capes contain feathers plucked from captive mutants; a fashion buyer tipped off the illegal trappers |
| **Hattie Nkemelu** (Tremor / Groundswell / Faultline) | Subway Seismic Institute | Dr. Leena Anwar, the field geologist | The childhood seismograms track Hattie's every step; a mentor sold the tracking data to developers |
| **Ilya Sorokin-Baptiste** (Guppy / Harbormaster / Black Tide) | East Harbor fish market | Papa Luc, the fishing co-op leader | Runoff from a luxury aquarium is killing nursery shoals; a harbor inspector buried the mortality numbers |
| **Asha Venkataraman** (Mudra / Lotus Guard / Quartermaster) | Venkataraman dance academy | Nirmala Rao, the senior choreographer | Recruiters catalogued dancers as combat assets; the talent scout photographed students without consent |
| **Theo Lindqvist** (Probability / Contingency / The Inevitable) | Saint Abel neurology ward | Dr. Ren Sato, the overnight neurologist | A researcher sells Theo's scans as tactical forecasts; a hospital administrator falsified the waiver |
| **Seraphine Delacroix-Moon** (Pinfeather / The Guardian / The Matriarch) | Delacroix Moon guardian crypt | Odette Vance, the skeptical cousin | A missing ancestor refused the guardian oath and survived; a family regent destroyed evidence of retirement |
| **Lucky Mbatha** (Charmer / Common Ground / The Patron) | East Station firehouse | Marsha Mbatha, the off-duty firefighter | Lucky's foundling note contains a compulsion charm pattern; a charity director exploited his charm to win donors |
| **Valentina "Vee" Castellanos** (Sparks / Torchlight / Foundry) | West End condemned apartments | Tomas Guerrero, the tenant organizer | An insurer paid contractors to bypass sprinklers; the landlord staged the inspection while residents slept |
| **Jun-ho Park** (Propwash / Tailwind / Air Traffic) | Skyloop prototype workshop | Dr. Min Park, the aerospace mentor | Jun-ho's wingsuit schematics were sold during the safety inquiry; the review witness worked for the buyer |
| **Delphine Okonkwo** (Hard Hat / Rebar / The Developer) | Comet Planning Hall | Etta Bell, the structural surveyor | The rebar certificate hides a politician's signature; a foreman accepted luxury repairs to stay silent |
| **Nalani Kahale** (Snorkel / Lifeline / The Trench) | Yacht Club rescue pier | Commander Reva Cruz, the retired lifeguard | Rescue boats were sold below scrap price; the coast-guard captain pocketed yacht-club money |
| **Marcus Fairbanks** (Stride / Hurdler / Drillmaster) | Civic Gymnastics Annex | Amir Price, the rehabilitation coach | The rewritten fall report conceals a faulty exoskeleton; the school's safety official changed the video timecode |
| **Priya Raman** (Ping / Firewall / Root Access) | Raman family repair shop | Mabel, the grandfather-voice home assistant | The audio company copied Mabel's training archive; a childhood friend accepted acquisition money |
| **Bartholomew "Bart" Sterling IV** (Prototype / Sterling / The Chairman) | Sterling Dynamics loading bay | Iona Clarke, the whistleblower engineer | A shipment ties Sterling rifles to gang violence; bart's cousin approved the side deal |
| **Dani Mercado** (Viral / Witness / The Algorithm) | Media District plaza | Suri Diaz, the activist photographer | The viral clip exposed protestors through metadata; an assistant sold the unblurred original |
| **Hollis Graymalkin** (Wick / Lanternwitch / Candlemass) | Old Lantern candlemaker's shop | Moss Holloway, the night candlemaker | The salamander's contract names an imprisoned ancestor; a curator buried the missing wax seals |
| **Ambrose Fairlie** (Whistle / The Weathervane / Thunderhead) | University rare-book vault | Merrin Shaw, the student librarian | The grimoire was written by a silenced stormcaller; a dean forged the overdue notice |
| **Willa Thornbury** (Seedling / Rootwarden / The Overgrowth) | Founders Circle parking structure | Evelyn Thorn, the urban gardener | A developer paved over a voluntary ancient nature pact; an elder druid sold the original map |
| **Caspian Lowe** (Puddle / Reflection / Augury) | Canal pawnbroker stall | Noor Shafik, the canal boatwright | The augury bowl contains the drowned owner's testimony; the pawnbroker forged a sale to bury the warning |
| **Adaeze "Ada" Ibekwe** (Novice / The Abbess / The Iron Hand) | Abbey refugee hospice | Sister Tamsin, the dissenting nun | The order rejected refugees after a secret donation; the treasurer sold the abbey gate keys |
| **Lucan Ferro** (Footnote / Theorem / The Grand Unifier) | Comet Mathematics Faculty | Professor Alba Senn, the former collaborator | Lucan's stolen proof could erase someone from a ledger; a rival stole the theorem's final page |
| **Isadora Blackwood** (Inkling / The Hearthwitch / The Coven Queen) | Blackwood manor kitchen | Aunt Nyx, the keeper of keys | A cookbook holds the final forbidden spell; an ancestor's portrait lied about isadora's mother |
| **Remy Lafleur** (Understudy / Curtain Call / Mister Midnight) | Civic Playhouse backstage | Talia Wynn, the stage manager | The crossroads spirit owns closing-night applause; a talent agent hid the old bargain's terms |
| **Ixi Solenne** (Sunspot / Daystar / Supernova) | Orbital refuge depot | Captain Sela Va, the escape-pod pilot | The authorities hid survivors of Ixi's colony; a customs officer falsified detention manifests |
| **Quillon Vey** (Fogbank / The Envoy / The Ambassador) | Western dimensional gate | Miren, the bilingual customs mediator | Reopening the rift would burn a residential district as fuel; a former envoy hid departure coordinates |
| **Kesh Tarrow** (Geode / Monolith / The Curator) | Civic Meteorite Museum | Archivist Ori, the mineral conservator | Collected stones contain living fragments of Kesh's people; a collector swapped the labels |
| **Thessaly Nauren** (Starfish / Lighthouse / The Siren) | East Quay whirlpool | Ari Sable, the deepwater navigator | The portal tide bears messages from Thessaly's ocean; a drilling firm suppressed the warnings |
| **Raxa Vel** (Recruit / The Deserter / Warlord Vel) | Gatewatch barracks | Mara Kes, Raxa's former squadmate | The commander's pursuit orders list civilian hostages; an old subordinate leaked raxa's location |
| **Oorin Faal** (Exchange Student / Uplift / The Exarch) | Interspecies research lab | Dr. Farah Bloom, the exchange scientist | Uplift trials made consent a biological reflex; a visiting observer sent results offworld |
| **Ysolde Quarren** (Pretender / The Exile / The Glass Empress) | Mirror Palace transit dock | Esmé Quarren, the foster mother's assistant | A mirror hid proof that exile was a rescue; a royal courier destroyed foster records |
| **Pellanor Six** (Solo / Assembly / Unanimous) | Crashsite Assembly Hall | Mika Six, an independent collective fragment | A salvaged receiver can reconnect the hive by force; a salvage dealer sold emergency frequencies |
| **Cassidy Molloy** (Fever / Firekeeper / Wildfire) | Saint Meridian pharmacy | Nadia Tran, the community pharmacist | Medicine suppresses empathy while amplifying anger; a clinic director enrolled cassidy without consent |
| **Avery Kwan** (Hover / Weightless / Freefall) | Kwan family attic | Grandmother Mei Kwan, the retired glider | A scrapbook proves three generations hid levitation; an uncle destroyed the sky-class letters |
| **Rafael "Rafa" Medeiros** (Touchstone / Groundtruth / The Foundation) | City Hall cornerstone vault | Detective Rosa Hale, the records examiner | The foundation contains a confession to a buried crime; a senior investigator sealed the archive |
| **Lior Ben-Ami** (Ripple / Calm Waters / Maelstrom) | Canal mental-health center | Elena Ben-Ami, Lior's mother | A board sells patients' sorrow to power tranquilizers; a clinician charged for treatment without consent |
| **Mei Lin Zhao** (Bookworm / The Librarian / The Stillness) | Shuttered Mind Library | Teacher Hana Li, the hiding librarian | A purge list names graduates of the secret school; a former student sold the safe-house map |
| **Ezra Calloway** (Cheat Sheet / Mindsight / Know-It-All) | Academy admissions office | Tutor Felix Ward, the exam proctor | The answer key came from a blackmail network; an honors student sold false confessions |
| **Celestine Arbogast** (Omen / Second Sight / Doomsayer) | Prom prophecy observatory | Yvette Marlow, the skeptical astronomer | The vision shows the precise chandelier failure; a prognosticator staged earlier false predictions |
| **Juniper Okeke** (Scoop / The Confidante / Hearsay) | Comet Tribune pressroom | Owen Bell, the union reporter | The leak was planted by a sponsor to silence a witness; the gossip editor paid someone to frame juniper |

## Illustration pipeline and status

The 144 requested outcome plates correspond to exactly:

```text
comet-city-academy/identities/<signature>/outcomes/student
comet-city-academy/identities/<signature>/outcomes/hero
comet-city-academy/identities/<signature>/outcomes/villain
```

These are **per-character consequence illustrations**, not aliases of character portraits. `projects/comet-city-academy/art/PERSONAL-CONSEQUENCES-ROUND-1.yaml` records each original scene's literal Krea2 prompt, asset key, seed and lane. The corresponding Play stage reads `personalOutcomeArtKey`, checks `promArt`'s exported/verified asset list and falls back to the preexisting scene if unavailable. Commission → ArtJob ID → render → approved final asset → export → validated public URL is the path to actual art delivery; no images are considered delivered by the presence of YAML alone. Do not populate imaginary ArtJob or ArtImage IDs.

**Remaining work:** full six-track protagonist/antagonist quest graphs per identity, 48 independent romance/recruitment systems with real agency (including consistent age and inter-character consent), more late-month personal events, nuanced betrayals and crew consequences, all ArtJob deliveries and device-width screenshots, comprehensive seeded adversarial *clean-start* trajectories, art continuity approval, and final subjective human review only after everything else is complete.
