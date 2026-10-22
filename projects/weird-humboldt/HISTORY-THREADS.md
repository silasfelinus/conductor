# Ecotone: Humboldt history, warts and all

> **ARCHIVED · SUPERSEDED October 22, 2026 PT.** This file documents an earlier Ecotone proposal, **not current instructions or planned development**. The owner withdrew the entire Wiyot/Tuluwat story, review and consultation workstream. No drafting, game use, art generation, outreach, release or queued follow-up is authorized by this archived document. Do not treat the earlier conditional approval below as active. See [the binding content-exclusion decision](EXCLUDED-CONTENT-2026-10-22.md). The original text remains below for internal provenance only.

**Silas, 2026-10-19 PT, verbatim:** *"I really want the history of Humboldt, warts and all to be a part of the experience. This game is partly a love letter to my home community, and I want people who explore it to get a better sense of our history. There's the Indian island massacre. I remember learning about one white man who made a large point of coming home for the evening and very expressively hanging his hat by the door to communicate that he wasn't involved (though theoretically he knew it would happen, one could be asked whether he was guilty, or could have done anything to affect it). There's the story about the explorers arguing as they crossed the river that became named after it: The Mad River."*

This is a design proposal for review. It turns those notes into plot material without breaking the rules already in ECOTONE-CORE.md and FACT-CHECK.md:
- Real history is fixed.
- No real atrocity is ever the cause of the game's weirdness.
- Living Indigenous nations are present-day communities, not a past era.

## How history enters the game

- **A love letter tells the truth.** The county's history is not set dressing. Players should leave knowing more about where Humboldt came from: what was beautiful, what was done, and who is still here.
- **The register changes when the history is grave.** Ecotone is comedy-horror, but its jokes, dice and supernatural machinery stop for atrocity. There is no roll, no clue and no collectible at a massacre site, and no ghost of a victim. Nothing in the game can undo or "fix" the past.
- **The present is part of the history.** Every grave historical thread ends in the living present: what the community did next, who carried on, what was returned or repaired, and what is still unresolved.
- **Provenance is visible.** Every history card shows its tier in the journal: documented, single-source account, or local telling. A memory like Silas's hat story is labelled as a local telling until it is sourced.
- **Comedy belongs to history too.** Some of Humboldt's real past is absurd, the Mad River's naming among it. Those threads can be as funny as the rest of the game, still sourced.

## Thread 1: Tuluwat, February 1860 (Chapter 3, Eureka and the Bay)

### What is documented

- **The massacre.** In the early hours of February 26, 1860, a small group of settlers crossed Humboldt Bay and attacked the Wiyot village of Tuluwat on what settlers called Indian Island. The Wiyot were gathered there for their annual World Renewal Ceremony, and many of the men had gone to the mainland for supplies. The dead were mostly women, children and elders.
- **Coordinated attacks.** The same night or within days, Wiyot people were killed at South Beach, on the South Fork of the Eel River and at Eagle Prairie.
- **Death-count attribution needs the Tribe's scope.** The Wiyot Tribe's [History](https://www.wiyot.us/148/Cultural) attributes estimates of **80–250** deaths to *that night's series of orchestrated massacres*, not to Tuluwat alone. Other accounts differ. Do not recast the Tribe's estimate as an island-specific death toll or imply one settled count.
- **No one was prosecuted.** Robert Gunther later recalled that the killers "were pointed out" in secret, and that "We soon found that we had better keep our mouths shut."
- **Bret Harte.** The assistant editor of Arcata's *Northern Californian* published an eyewitness account of the aftermath on February 29, 1860. He soon left the area after threats against his life. The *Humboldt Times* had run an editorial calling for Native people to be driven out of the county the day before the attack.
- **Robert Gunther.** He bought the island three days before the massacre. In his own later account he was asleep in Eureka that night, woke to what he thought were screams, and went back to sleep. A justice of the peace woke him the next morning, and they went to the island together. He later diked the marsh and ran a dairy there for decades.
- **The present.** The Wiyot Tribe began raising money to buy the land back in the late 1990s and bought its first parcel in 2000. The Tribe resumed the World Renewal Ceremony on Tuluwat in 2014. The City of Eureka voted in 2018 to return its island holdings and transferred them in 2019. Later shipyard use left contamination, which the Tribe has worked to remediate. Remains taken from graves were held in museum collections for generations; some have been returned.

### The hat by the door

**2026-10-21 decision:** The project owner approved the pre-consultation recommendation. This anecdote remains unverified and must NOT be presented as documented Tuluwat history, used to imply known advance knowledge, or used as the historical origin of a morality flag. The original brainstorm below is preserved as superseded development history, not approved playable copy. An independent, modern fictional bystander dilemma can be authored without tying itself to the massacre.

Silas's memory is of a settler who made a show of coming home that evening and hanging his hat by the door, so everyone would know he was not involved, though he likely knew what was coming. No source found so far records that detail. Robert Gunther's own documented account raises the same question in his own words: he heard screams across the bay and went back to sleep, and afterwards the town agreed to keep its mouth shut.

**Proposal:** make "the hat by the door" Ecotone's moral image for the **Agency ↔ Fate** axis (IDEOLOGICAL-ECOTONES.md). The image is someone who knows harm is coming and arranges to be seen not participating.
- Ground it in the documented account and cite Gunther's words.
- Present the hat itself as a local telling, marked in the journal as unverified, until a source turns up.
- Never invent a named perpetrator or witness, and never put words in a real person's mouth beyond what the record holds.

### Proposed anchor scene: "Across the Bay" (guaranteed, not a random draw)

At dusk the protagonist can see Tuluwat across the water from the Eureka waterfront. The comedy stops and the dice disappear; the CB, the festival PA and the companions go quiet. The scene shows the documented history and the present briefly. It offers three ways to spend the moment:
- **Read what happened**, then what came after: the purchase-back, the ceremony's return, the land transfer.
- **Listen** while the active companion responds in their own voice. Each companion's response must be authored and reviewed, never generic.
- **Keep walking.** The journal records the choice without judgment.

**Rules for this scene:**
- No violence is shown, the ceremony is not depicted, there is no sacred content, and no Wiyot character exists merely to explain the history.
- It never gives a stat, a clue toward the mystery or an achievement.
- The anomaly never touches this place, and the game should not imply a supernatural reason for that.

### How the hat echoes in the finale

**SUPERSEDED 2026-10-21:** Do not implement the proposed `hat_by_the_door` callback or invite the player to score or analogize conduct during the massacre. The following is an archived design thought only. A distinct present-day fictional dilemma may be written independently of the Tuluwat historical scene.

At the county-fate convergence the player meets a **present-day, fictional** moment where they know harm is coming to someone in the county. It could be a displacement vote, an unsafe worksite or a coalition about to abandon its most vulnerable members. They can act at a cost, or hang their hat by the door. The choice is labelled in plain words, recorded as a callback flag (`hat_by_the_door`) rather than a morality score, and can surface in the 1/10/30-year epilogue signatures.
- The parallel is about bystanders, not about equivalence. The writing must never suggest that a modern policy fight is comparable to a massacre.

### Before anything is published

**2026-10-21 owner authorization applies to internal drafting only.** Offer the Wiyot Tribe an opportunity to decline or review with compensation and agreed scope, through the Cultural Department's preferred process, *before* using tribe-specific game text, illustrations, audio or protected cultural material publicly. Prepare exact passage/art and source packet first. No outreach or tribal permission has yet occurred; no silence-as-consent and no approval by proxy.

- **Consult the Wiyot Tribe** (its cultural and historic-preservation office) before any player-facing Tuluwat text ships. Include the Tribe's own published history, and credit it.
- Use the Tribe's names and terms as the Tribe uses them: Tuluwat, Wiyot. Don't invent words in Soulatluk, the Wiyot language.
- Sources need checking against the Tribe's account and primary documents. Wikipedia and the North Coast Journal are starting points, not authorities.

## Thread 2: The Mad River, December 1849 (Chapter 2, Mad River / Hammond Trail)

### What is documented

The Josiah Gregg party, a starving overland expedition, reached the coast in December 1849.
- At the river mouth, Gregg insisted on fixing its latitude with his instruments, and the exhausted men refused to wait. They crossed without him, and he exploded at them from the far bank.
- By one account, some of them talked about throwing him and his instruments into the river. The river has been the Mad River since.
- **The only source** is L. K. Wood's memoir, and historians consider him not fully reliable, so the card is a single-source account.
- Gregg died in 1850 after a fall from his horse on the way back.
- The Wiyot Tribe publicly records **Baduwa't** as the Soulatluk name for what English-language maps call Mad River. That existing, living Indigenous identity predates the 1849 naming anecdote. Source: [Wiyot Tribe public place-name project](https://www.wiyot.us/450/A-Photographic-Exploration-of-Wigi). For any game use, seek language/cultural guidance; do not invent pronunciation or represent a tribal-only map.
- The Tribe's [newsletter about Ki-we-lat-tah](https://www.wiyot.us/Archive.aspx?ADID=122) describes Wiyot hospitality to the Gregg party at **Humboldt Bay**. Preserve the distinction between that documented meeting and the separate Mad River crossing; do not relocate named Wiyot people to an invented scene to supply a character or supernatural reward.

### Proposed card: WH-121 "The Latitude Argument"

**Current implementation warning (2026-10-21):** WH-121 exists in Kind Robots as a playable, explicitly fictionalized historical encounter, with art-job references, but it lacks the Wiyot homeland/welcome context. It is a development item for a bounded pre-consultation revision, **not** a Wiyot-reviewed or historically complete portrayal. The supernatural 1849 fog seam must not blur the line between a sourced settler anecdote and the Wiyot historical record.

A sixth seed for the Mad River / Hammond Trail pool. The joke works with history, not against it.

At the river mouth, a ragged party from 1849 is stuck in the fog, still arguing. One man is fussing with a sextant and swearing he will not cross until he has the latitude. The rest want to cross, eat and stop hearing about latitude. They ask the protagonist to settle it.

- **Help him take the reading** (Wits 9). Success: you record a precise latitude that is a little wrong for this Humboldt, and right for a different one (Evidence: a reading from another county). Failure: the fog takes the horizon and he blames you, at length.
- **Help the crew across** (Burly 7). Success: everyone is ashore and dry, and the shouting starts behind you on schedule (`mad_river_ferried`). Failure: you are as wet as they are and twice as cross.
- **Try to make peace** (Rizz 11). Success: thirty seconds of calm, then the argument resumes, because the river's name was never yours to change (`mad_river_peace`, Goodwill +1). Failure: you are now part of the argument.

- **Provenance on the card:** "Named in December 1849 after an argument recorded by L. K. Wood, the expedition's only chronicler. The river had other names first."
- **Characters:** Gregg's portrayal is clearly fictional. Mara's sober, evidence-first lens and Kit's absurdist timing both fit this card naturally.

## More threads to research (not yet claims)

Possible further threads. Each needs sourcing, and the community's own authorship where it is their history:
- The 1885 expulsion of Eureka's Chinese residents (already sourced in FACT-CHECK.md as its own thread).
- Hoopa, Yurok, Karuk and Tolowa histories, which are not interchangeable with the Wiyot.
- The timber economy and the Timber Wars (Luna, already sourced).
- The cannabis boom and bust.
- Major floods.
- The founding and renaming of the university.
- Labor history.

Each needs the same treatment as above: provenance, the living present, and no comedy over atrocity.

## Sources (starting points, to be checked against tribal and primary sources)

- 1860 Wiyot massacre: https://en.wikipedia.org/wiki/1860_Wiyot_massacre
- North Coast Journal, "The Tuluwat Island Massacre in Its Time" (Gunther's account quoted): https://northcoastjournal.com/life-outdoors/the-tuluwat-island-massacre-in-its-time-24834282
- HistoryNet on Bret Harte's reporting: https://historynet.com/bret-hartes-voice-for-the-wiyots/
- 2019 transfer ceremony: https://www.activenorcal.com/city-of-eureka-transfers-indian-island-back-to-wiyot-tribe-in-historic-ceremony/
- Return of remains (CBS SF): https://www.cbsnews.com/sanfrancisco/news/wiyot-tribe-massacre-uc-berkeley-hearst-museum-of-anthropology-returns-remains
- Mad River (California): https://en.wikipedia.org/wiki/Mad_River_(California)
- North Coast Journal, "Josiah Gregg in California": https://www.northcoastjournal.com/life-outdoors/josiah-gregg-in-california-23404660/
- Smithsonian, the Gregg expedition: https://www.smithsonianmag.com/science-nature/ill-fated-expedition-19th-century-scientist-explore-california-wilderness-180971048/
