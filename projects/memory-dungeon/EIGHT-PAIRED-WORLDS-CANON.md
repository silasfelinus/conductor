# Memory Dungeon: Eight Overworlds, Eight Distortions

**Authority:** Silas's 2026-10-30 PT correction to the playable sequence. This supersedes the earlier optional middle-pair interpretation in the Reimaginer brief and the older sixteen-independent-realm list. **Internal story and production bible; includes major spoilers. Do not render this document in game.**

## Structural contract

There are **eight geographical overworlds, sixteen experienced incarnations**. The original incarnation is immediately followed by a **twisted version of the SAME overworld**. The second experience must retain recognizable geography, then transform the moral meaning, dangers, traversals, witnesses and visual treatment. The pairing is sequential and earned, not a chooser with e07/e09/e11 open simultaneously. No public level-count, spoiler-filled map picker or list of unseen realities.

| Pair | Original overworld | Twisted follow-up | Story focus and player knowledge |
|---|---|---|---|
| e01/e02 | Briar Marches | Briar Understory | Pip trapped in a twisted fairy tale; protagonist meets the general party and learns the rules. The second world recasts protectors as threats and vice versa |
| e03/e04 | Morrow's ordinary Earth | The Unbelieving City | Morrow attempts to survive actual mundane life: transit, employment, scholarship, relationships, ordinary human institutions. Revisit the same Earth sites in a dangerous magical distortion, not a different realm |
| e05/e06 | Scylla's remembered mermaid-princess home | Undertide Crown, a rewritten sea timeline | Scylla relives childhood, the twins' court, and their plan to escape for land. The second sea-world is an actively twisted version of the same memories and route. Scylla carries knowledge that changes her responses; the player does not immediately learn her full reason |
| e07/e08 | Hoshimori: Lantern Village | Hoshimori: Procession of Shut Doors | A light, gracious, original Japanese-folklore village partly connected to Pip's childhood. Immediately followed by demonic yōkai horror in the **same eight-by-eight geography**, with the Red Oven transformed from hospitality into coercive protection |
| e09/e10 | Carnival of Debts | Tomorrow Market | The same routes turn from human bargains to a predictive market of lives |
| e11/e12 | Between Sea | The Transfer Network | The same crossings become a cold apparatus of consent and identity transfer |
| e13/e14 | Index of What Happened | Index of What Could Be | Archive of competing testimony becomes the record of futures that can be imposed |
| e15/e16 | Forge of Consequences | Unwritten Country | The final geography is rewritten into a dangerous synthesis; cannot resolve history by deleting other people |

Pairs five through eight retain the current project ideas as provisional content briefs, not eight already-built overworlds. Production still requires individual 64-site maps, 36-room nested dungeons, an original-versus-twisted art identity, 30+2 collectible faces per reality and tested story choices. The `e01`–`e16` and concept identifiers, four early Briar photo sites, Hoshimori photo sites, saved machine IDs and existing art receipts remain stable.

## Spoiler vault: Char and the attempt to go ashore

**Canon fixed by Silas, 2026-10-30:** Charybdis (Char) **died as a consequence of the twins' decision/attempt to leave their mermaid home for land**. It is not an undetermined possibility, a merely predicted future, or a tragedy that can be retroactively prevented by choosing a different dialogue option. This is an **ultimate revelation for the player**, not e05's opening narration or an overworld-menu tooltip.

**Knowledge separation:** Scylla can know the loss and carry grief while the player still sees the voyage from the twins' earlier, hopeful point of view. e05 depicts the past truthfully as it was experienced before the departure, with clues and character choices but no retrospective spoiler caption. e06 twists the shared sea geography and those choices into an alternate account, testing what Scylla can bear to face. She may react with disproportionate urgency, avoidance, rage or tenderness, but neither a narrator nor a UI label calls Char's fate a reversible "possible future". A complete account emerges through earned late Archive testimony in e13–e16; the detailed staged reveal (evidence, confirmation, emotional response and reconciliation) must be authored and tested, not improvised by a menu or assumed from a single card.

**Continuity guard:** Char's earlier cast scenes, any apparently living Char in later realities, and Scylla's apparent "save her" decisions require **timeline/echo/remembered-self explanations**, not a contradiction or an automatic resurrection. A story can present a Char who does not know she is remembered. Such a scene must have its own understandable stakes and agency. Oren remains hooded, practical and capable; do not invent an unmasking secret to explain the tragedy. The protagonist and Morrow body exchange, Earth-photograph chronology, and the later ethical question of Morrow's family remain in force.

**Implementation compatibility:** Keep the existing serialized anchor ID `char-possible-future` so existing saves can be restored, but **deprecate its old writer-facing interpretation**. It now means Scylla has encountered testimony about the consequential departure, not that Char's death is optional. Do not expose the deprecated identifier to players. Add exact-order, no-skip, save migration and spoiler-safety tests.

## What is authored versus what is playable

As of this direction, the application holds a sixteen-experience **campaign metadata contract**, not sixteen completed maps. Briar and Dark Briar have map/dungeon gameplay; e07 Hoshimori has a 64-site authored village and nine Red Oven rooms but is gated behind unimplemented e03–e06. The Scylla and Morrow pair entries are currently planned story/route contracts, **not finished, reachable 64-site maps**. e08 has only a design brief, no full implemented demonic yōkai world or verified ArtJobs. Do not claim eight playable overworlds.

## Next implementation priority

1. Make the campaign's **eight contiguous original→twisted pairs** explicit and preserve historical machine IDs; adapt old branch-save snapshots by replaying legal earned scenes in canonical order.
2. Write the real e03/e04 Morrow Earth original-and-distortion scenes and nested dungeons next: these currently block ordinary access to e05–e08. Keep Earth geography recognizable.
3. Build e05/e06 Scylla scenes with a spoiler map separating her knowledge from the player's; place the ultimate Char death reveal later through earned evidence and consequences.
4. Continue e07's remaining Red Oven rooms and the e08 first sixteen horror sites in parallel where not blocked by content access, then art production and device acceptance.
5. Test every transition: original→twisted without jumping pairs, three-dimensional reimagining, two Earth photographs per reality where authored, save replays, pre-reveal privacy, playable noncombat outcomes, and Classic Mode untouched.

**Human gate:** public release and final subjective judgment only. These internal narrative and engineering corrections are reversible development work, not authority for a public deployment.