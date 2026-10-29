# Prom of Doom: The Villain's 48 Signature Henchman Types

**Approved creative direction:** Silas, 2026-10-29 PT. The 48 permanent origin × affinity people stay the playable identities; these crews are supporting species assigned to **their villain mode**, not extra hero forms or 48 anonymous mercenary skins. Canonical machine-readable 48-entry authoring file: [Kind Robots villainHenchmen.json](https://github.com/silasfelinus/kind_robots/blob/main/utils/cometAcademy/villainHenchmen.json). Each entry records a named captain, a distinct silhouette, tactical move, readable counter and an ethical/story fault line tied to that villain.

## Combat grammar and narrative contract

- **One hit to route, disable or disarm** a standard troop, with an accessible nonlethal visual. One hit does **not** automatically mean on-screen death. Named bosses and two independently motivated primary accomplices per mastermind arc remain separate, persistent characters with negotiation/defection tracks.
- Each type has **one telegraphed trick**, giving the player a decision before it resolves. Counterplay must be previewable on the map, not a secret dice modifier. The counter should fit its character: return a stolen overdue book, disrupt a chorus or unfold an apology letter.
- Art must distinguish each species from any of the 48 human hero designs. Plan at minimum an identifiable pose/standee, one move telegraph, hit/disarm reaction, and one close-up captain portrait for story and Scrapbook. A JSON record is not rendered artwork or a spawned combat unit.
- Non-human breeds and sentient animated artifacts are candidates for Facet `SPECIES`. Their named representatives are **not** extra origin × affinity heroes. If a new breed's nature is reclassified during integration, respect the actual Facet schema, rather than inventing a DB enum.
- Default villain pairing means `henchmanForVillain(villainSignature)`, independent of who the protagonist is. A hand-authored foil path can make that henchman betray, protect or defect, but must not silently swap its canonical villain relationship.
- City Plaza one-shot **Picnic Panic** is the Warren Wreckers' featured first event: Foreman Thumpkin announces sidewalk tunnels, then bunny-men burrow around picnic tables. The encounter must be authored with civilian protection, clear dust-ring emergence telegraphs, and at least one negotiation over whose ground the plaza sits on.

## Complete one-to-one assignment ledger

| # | Villain's permanent codename | Signature crew | Named representative | Battlefield trick |
|---:|---|---|---|---|
| 1 | **Backdraft** | Claim Cinders | Ash Invoice | Stamp a glowing INSURED tile which ignites next turn |
| 2 | **Skyline** | Hushwings | Nell No-Air | Vacuum a telegraphed corridor to disrupt ranged attacks |
| 3 | **Cornerstone** | Warren Wreckers | Foreman Thumpkin | Burrow and surface from a visibly disturbed tile behind cover |
| 4 | **Tidewarden** | Drytap Octopi | Deputy Plink | Siphon a marked wet tile and leave slick ground |
| 5 | **The Second Hand** | Ninety-Seconders | Ticky Tuesday | Dash twice on the telegraphed countdown bell |
| 6 | **Eureka** | Mistake Makers | Dot Matrix | Mark a delayed error burst on an exact set of tiles |
| 7 | **Captain Valcourt** | Licensed Legends | Sir Cap-Permission | Stamp a trademark seal disabling one signature action for a turn |
| 8 | **Chorus** | Jinglejacks | Sponsor Moth | Link adjacent singers to extend a villain's range |
| 9 | **Ashborn** | Redaction Wraiths | Smudge | Lay down a drifting soot curtain that blocks sightlines |
| 10 | **Kestrel** | Confession Crows | Inspector Grackle | Steal an objective token and flee toward a marked perch |
| 11 | **Groundswell** | Tenant Bricks | Mortar Mabel | Punch marked cover into rubble |
| 12 | **Harbormaster** | Harbor Repossessors | Captain Clack | Throw a telegraphed anchor cable that roots a shore target |
| 13 | **Lotus Guard** | Fourfold Foils | Madame Practice | Spin four weapons to disarm a close hero for one action |
| 14 | **Contingency** | Domino Oracles | Seventh Pip | Topple in a telegraphed line to chain one-tile stuns |
| 15 | **The Guardian** | Charity Cherubs | Pennywing | Intercept one blow intended for a named boss or captive |
| 16 | **Common Ground** | Smile Deputies | Grinny | Flash forged friendly badges that swap target highlights for one action |
| 17 | **Torchlight** | Kiln Kittens | Sparkplug | Leave a glowing slag square that weakens adjacent cover |
| 18 | **Tailwind** | Air-Traffic Mayflies | Wingnut-9 | Draw a flashing no-fly lane, forcing airborne units to land |
| 19 | **Rebar** | Permit Crabs | Stampy | Raise a one-round barricade on a marked tile |
| 20 | **Lifeline** | Rescue Quackers | Buoy Wonder | Wrap a unit in opaque flotation bubbles to obscure shots |
| 21 | **Hurdler** | Parade Medals | Goldie Split | Relay an extra sprint through a visible ribbon chain |
| 22 | **Firewall** | Mabel's Biscuit Bots | Snickerdoodle-4 | Overclock a control panel and lock an adjacent door |
| 23 | **Sterling** | Warranty Wisps | Clause Nine | Wrap a villain ally in one-use cover at the cost of movement |
| 24 | **Witness** | Playback Puppets | Replay Ray | Conjure a false hero silhouette that attracts overwatch fire |
| 25 | **Lanternwitch** | Wicklings | Mother Ember | Carry delayed ignition along a visibly lit chain of candles |
| 26 | **The Weathervane** | Marginalia Nimbus | Dewey Storm | Rain ink on a marked area, obscuring line-of-sight labels |
| 27 | **Rootwarden** | Gnome Revolt | Sir Mulch | Send visible vines through paving seams to tether the next visitor |
| 28 | **Reflection** | Glass Doubles | Silver Sip | Place a watery duplicate where a hero last stood |
| 29 | **The Abbess** | Bellbound Novices | Sister Ding | Sound a timed chime that interrupts the queued ability in one square |
| 30 | **Theorem** | The Primelets | Eleven | Connect marked vertices into a zone-denying geometric proof |
| 31 | **The Hearthwitch** | Heirloom Hexes | Auntie Hem | Pin a house rule to one tile that punishes repeating an action |
| 32 | **Curtain Call** | Encore Hands | Velvet Glove | Double an adjacent ally's next movement through rhythmic applause |
| 33 | **Daystar** | Flare Skiffs | Little Sol | Sweep a light beam across a warned row then flee the edge |
| 34 | **The Envoy** | Cloud Clerks | Undersecretary Mist | Declare a marked square annexed, increasing entry cost |
| 35 | **Monolith** | Display Goblins | Curator Chip | Build a temporary glass case around an exposed target |
| 36 | **Lighthouse** | Pearl Choir | Alto Clam | Sing one target a tile closer to the watery edge |
| 37 | **The Deserter** | Honor Drones | Drillbit Seven | March in synchronized pairs to form one-unit shield walls |
| 38 | **Uplift** | Patent Pips | Provisional One | Confiscate the second use of a tagged gadget for one turn |
| 39 | **The Exile** | Mirror Pages | Squire Reverse | Hop between two marked mirrored tiles to flank a hero |
| 40 | **Assembly** | Welcome Mats | Hugbug Hob | Emotionally link two units so moving apart costs extra range |
| 41 | **Firekeeper** | Bedtime Matches | Tuck | Bring a nightmare-shaped burning tile beside a frightened hero |
| 42 | **Weightless** | Lift Bailiffs | Floaty Finch | Levitate a piece of cover away and expose a firing lane |
| 43 | **Groundtruth** | Confession Cobbles | Pebble Judge | Broadcast one buried secret, briefly disrupting the listener's focus |
| 44 | **Calm Waters** | Apology Boats | Captain Sorry | Flood a telegraphed square with grief and slow movement |
| 45 | **The Librarian** | Bookshades | Page Turn | Slip through one obstruction to tag a unit behind cover |
| 46 | **Mindsight** | Thoughtbubbles | Password Please | Predict and mark the destination of a planned move |
| 47 | **Second Sight** | Tomorrow Ravens | Miss Maybe | Mark a future strike tile then swoop precisely on schedule |
| 48 | **The Confidante** | Rumor Mites | Scoop Two | Post a false accusation that briefly diverts targeting to a decoy |

## Story and art hooks for the most surprising recruits

**Backdraft** uses the **Claim Cinders** to distribute fire insurance contracts. Ash Invoice is collecting proof that his villain is the arsonist behind the claims. The fight can turn into a whistleblower rescue if the player reads the receipts.

**Cornerstone** commands the **Warren Wreckers** who tunnel under the city; Foreman Thumpkin is a proper worksite foreman, with union bylaws and emergency exits. The same crew supports the picnic one-shot and any villain cameo built around property, tunnels and collapsed foundations.

**Firewall** has **Mabel's Biscuit Bots**, ridiculous cookie-tin security robots whose grandmotherly recipes outlast her AI's surveillance directives. An authentic family recipe is a better counter than raw damage.

**The Guardian** sends **Charity Cherubs** as shelter enforcers, but Pennywing knows whom her boss's charity is harming. Their defensive mechanic doubles as a defection trigger.

**Theorem** summons **Primelets**, living geometry that denies a polygon of battlefield space. One missing vertex breaks an entire mathematical proof, and Eleven is looking for a proof of mercy.

**Assembly** sends plush **Welcome Mats** that tangle lonely minds together. Hugbug Hob remembers what individual choice meant, and using a captive's name severs a link.

**Calm Waters** has **Apology Boats** folded from unsent letters. The boats can be routed through emotional closure rather than violence; Captain Sorry is carrying a letter the villain wrote.

**The Confidante** sends the **Rumor Mites** to forge accusations across Comet City. Scoop Two remembers and saves contradictory evidence; the counter to a false claim is an actual source.

## Provisional fan-favorite assignments pending t-021 reconciliation

The **current** Kind Robots 48-entry `identityArcs.json` does not yet list **Granny Mayhem** or **Dr. Frog** among its signature IDs; **Zuzu Koala Assassin** is an established dimensional guest, *outside* the 48 native origins. Task t-021/#4403 is the existing roster-and-visual reconciliation lane. **Do not silently overwrite an unrelated hero's ID or claim 51 of 48 playable slots.** The following three signature henchmen are ready for authors to use once their patron identity is confirmed:

- **Granny Mayhem → The Murder Doilies**, led by **Miss Hemstitch**. Hardened lace table mats with tiny brass-knuckle tassels slither beneath banquet tables, then cinch a lace circle around one hero's boots. The crochet pattern shows their next destination; pull the loose yarn to unravel the trap. Miss Hemstitch wants the villain to stop using the neighborhood mutual-aid sewing circle as a recruitment office. Comedy comes from formidable domestic equipment, **never** Granny's age.
- **Dr. Frog → The Prototype Puddles**, led by **Lab Assistant Blorp**. Walking leaked serum samples in mismatched spring-loaded exoskeletons ricochet between laboratory benches, coating one square with adhesive frog-spawn foam. The glowing pipette telegraphs the jump; activate the lab's rinse station to neutralize the goo. Blorp has learned that the formula changes bodies without asking and may help the protagonist expose the botched trials.
- **Zuzu Koala Assassin / possible Shogun Null → The Null-Ronin**, led by **Quiet Leaf**. Origami eucalyptus-mask sprites dart between two marked shadow squares, leaving a single silence zone rather than lethal harm. Illuminate the destination glyph to stop the jump. Quiet Leaf believes Zuzu's home-world oath outranks any mechanized villain persona and can refuse a dishonorable order.

These are **creative proposals**, not machine-linked rows, spawned enemies or art. Final bindings require the reconciled stable identities and consent to the established cross-game guest canon.

## Delivery and verification gates

1. The runtime catalogue must cover exactly the same **48 stable signatures** as `identityArcs.json`, with 48 unique names, named representatives, distinct tactics, counters, one-hit rule and story hooks. Automated test and Playbook Slices CI are required.
2. Prom of Doom: attach discoverable Yearbook/Playbook Forge species design cards and explicit enemy deployments to antagonist patrol missions, with meaningful dialogue/refusal/defection outcomes.
3. Every Villain Tactics: provide a reusable one-hit minion combat profile, telegraphed special movement/targeting, seeded tactical AI and map placement, with the special **burrow, summon, teleport and swarm** behaviors implemented as real mechanics. One-shot Picnic Panic uses actual burrowing units, not placeholder icons.
4. Assign durable art-generation requests and confirm ArtJob / ArtImage / URL provenance per type. Track proposed, queued, rendered and delivered as different states; no fake 48/48 art-complete counts.
5. Adversarial checks: all 48 assignments, no duplicates, one-hit semantics, previews equal resolved positions/odds, counters reachable, safe saved games and actual encounter variety across seeds. Production/public publishing remains separately gated.

**Current delivery:** authored and checkable catalog only. The 48 types are **not yet spawned, painted or integrated** into game encounters; the next gameplay and art tasks must earn those statuses.
