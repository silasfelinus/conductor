# Game of Captains
**Status:** new, active, high-priority original science-fiction comedy playbook.
**Title:** provisional but takes Silas's last line as its starting point.
**Requested:** 2026-10-25 PT. **Master scope:** https://github.com/silasfelinus/kind_robots/issues/4182

## The playable promise
Choose a **captain** and core crew, lead a gloriously unreliable starship through space and **away-team missions**, and live with the moral responsibilities of an advanced civilization trying to stay impartial amid other civilizations' poor decisions. A comedy with genuine consequences: brisk absurd situations and arguments between old friends can coexist with difficult diplomacy and grief. A command is only successful if someone survives the cost.

Inspirations in tonal DNA: Space Quest, Red Dwarf, Hitchhiker's Guide, Star Wars, Star Trek, Lower Decks, Barbarella, The Orville. Write original characters, places, dialogue, visual designs and narrative arcs, never fan-fiction with renamed nouns.

### Existing Kind Robots continuity, VERIFIED
`kind_robots/stores/seeds/narrators.ts` and `utils/sceneChoices.ts` establish:
- **Barkeep Vox**: warm, dry humanoid-tardigrade storyteller at a neutral space bar. A recurring mission source, witness or friend.
- **Serendipity Space Bar** (Dream #44): a *sentient building*, its lights and gravity part of its personality. Vox and Serendipity are distinct entities. The house rule: "No vaporizing paying guests."
- **Captain Fluke** (Dream #49): narrator of the **Improbability Starcruiser**, charmingly confident in a ship whose computer quietly corrects the captain's log. Use as recurring guest/counterpoint or narrator; *do not silently overwrite the existing NARRATOR seed* to make Fluke a playable captain. If player-control mode is added for Fluke, reconcile the identity contract deliberately.
These are genuine legacy story assets, not the entire new crew roster. The existing `/serendipity` route is a voice-product route, not this game's path.

### Captain's chapter loop
1. **Captain creation/selection:** at least six authored leadership temperaments/backgrounds with genuine strengths, vulnerabilities, resources, obligations and rival reputations. Choose initial senior crew among at least sixteen recruitable NPCs. Every lineup is viable, not equally easy.
2. **Bridge briefing:** route options on a meaningful star chart, ship condition, crew objections, factions, deadlines and distress calls. Player chooses mission, ship assignments and command protocol.
3. **Away mission:** assign **0–3 available specialists** where sensible; experts leaving the ship cause an opportunity cost. Diplomacy, rescue, scientific crisis, exploration, engineering, contact, trade, medical ethics and absurd bureaucratic disasters all need distinct mechanisms. Multiple approaches and authored great/success/mixed/failure/refusal outcomes.
4. **Intervention debate:** the captain navigates consent and sovereignty, imminent harm, treaty compliance, truth versus secrecy, technological power asymmetry, humanitarian obligation and unintended harm. **Inaction is a consequential choice**, not a magic "ethical" option. Other cultures are complex, not classified on a linear better/worse scale.
5. **Debrief:** crew trust, hull/fuel/repair, resource cost, wounds, diplomatic position, factions, cultural consequences, promises, antagonist clues/pressure and navigable destinations update. Captain's log and save.

**Three acts** with interconnected planetary and shipboard arcs. Periodic comic chaos needs human stakes and logical callbacks; avoid an endless generic mission queue.

### The antagonist as a run-specific trouble engine
One of **eight original principal alien antagonists** selected by seed at run start. Each has a coherent agenda, signature ability, tagged complications, personal ties and a unique escalation pattern. Interfere in ordinary missions at multiple points (sabotage, diplomacy, false signals, crew recruitment, rumors, blackmail, treaty provocation), not simply a final boss reskin. Show enough evidence that the captain may uncover a motive, bargain, defeat, reconcile, or accidentally become complicit. Some antagonists are partially justified.

### Example consequential scenes
**The Library Planet's Due Date:** its self-aware archive's contract forbids evacuation before a stellar flare. Negotiation, force and data theft each save different things and upset different lives.
**The Serendipity Tab:** Vox will not disclose who paid a refugee's debt; Serendipity has physically concealed the missing patron through a gravity trick. A clue about the antagonist is available, but only after risking hospitality and trust.
**The Imperfect Rescue:** the ship can tow only one colony vessel. The away team may risk itself rescuing a second. A clear case where non-interference, bold intervention and secret aid have lasting consequences.
**The Last Log:** destination and finale change with crew confidence, societies affected, old vows, antagonist relationships and decisions made dozens of scenes earlier.

### Content, system and visual targets
Initial production floor: **6 captains, 16 crew, 12 distinct systems/ports, 40 meaningful encounter cards, 30 missions, 8 antagonists and 16 distinct earned endings**. Fully authored voices, moral tensions and real alternatives; varying result tiers and story callbacks, not an ending paragraph with different flags. Maintain one from-start seeded trace for every reachable ending and a machine-readable choice graph.

Seeded offline-at-playtime engine: captain doctrine, player/crew relationships and skills, equipment, ship resources, location access and systems, treaties, promises, faction trust, intervention ledger, antagonist state, crew absence/injury/departure, chapter time, ending flags, versioned save/load and ending/captain's-log archive. The ship vs away staffing split must change options. Save migration and resuming mid-mission cannot duplicate awards or undo casualties.

**Full-screen game, never a standard web app:** designed title/captain selection, bridge and starmap, assignment/away views, cinematic illustrated dilemmas, shipboard NPC conversations, crew dossiers and multiple destination-specific epilogues. Touch, keyboard, gamepad, accessible settings, phone/tablet/desktop. First implementation must be an *art-led playable end-to-end mini-voyage* with antagonist interference, not an empty UI.

Art: original bright lived-in retrofuture sci-fi, absurd technology rendered with coherent material design and distinct species/cultures as individuals, not trope monoliths. Reuse verified existing assets when appropriate; create unique ship/crew/planet/alien antagonist illustration, mood portraits, scene and result tiers and every ending. Maintain ArtJob/seed/model/source/prompt/scene metadata and **verify delivered URLs**; prompts/placeholder SVGs alone are not completion.

### Adversarial completion
Every antagonist across captain/crew combinations, legalist/non-interventionist/exploiter/rescuer/rogue strategies, neglected missions, low supplies, ship/away absence, injured/departed crew, no clue, hostile faction, betrayal and all endings. Analyze from-start seeded action logs for reachability, reasonable odds, narrative originality, ethical nuance and fun on failure. Independently read whole story transcripts and inspect rendered art on small and large devices. Fix all agent-owned writing, gameplay, art and UX weaknesses before final design review by Silas. Public publication is independently gated.

## Coordination
Conductor: `projects/game-of-captains/roadmap.yaml`. Build initial private Kind Robots Admin preview using the existing playbook framework where prudent, without changing Vox/Serendipity/Fluke canon. Master issue is a shared-context ledger with permalinks to relevant discoveries and PRs.
