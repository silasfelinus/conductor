# Memory Dungeon: Twelve realities, four character acts, four crossover finales

**Authority: Silas's 2026-10-30 PT revision.** This document supersedes the **sixteen playable overworlds** scope in the former Reimaginer/Eight-Paired-Worlds and Sixteen-Realm production bibles, while preserving the first eight worlds' substantive choices, hard-won history and serialized identifiers. This file describes intended authoring and state contracts, not shipped end-to-end gameplay.

## One continuous campaign, twelve overworlds

The first **eight maps** are four original→twisted pairs:

| Maps | Geographic identity | Focal character | Dramatic hinge |
|---|---|---|---|
| 01 / 02 | Briar / Briar Understory | Human protagonist in Morrow's borrowed fey body; Pip introduces the party | Trust the witnesses or prioritize a sealed village; Vesper's betrayal emerges without being forgiven by fiat |
| 03 / 04 | Morrow's ordinary Earth / enchanted Earth | Morrow, struggling with ordinary human life | World Four tide-gate rescue: Scylla can witness Char die; or Char survives while people remain stranded or a district is sacrificed |
| 05 / 06 | Scylla's younger mermaid kingdom / warped second timeline | Scylla back in the days before she and Char ran away to human land | Repeat their escape, stay, or tell younger Char about the future and let her choose; then public vs private testimony |
| 07 / 08 | Vesper's childhood Hoshimori / uncanny yōkai Hoshimori | Vesper is the emotional focus, e07 existing protagonist game lens, e08 Scylla lens preserved | Protect refugees without making their routes an exploiters' atlas; forced perfect traceability corrupts the village |

The final **four maps** are a *connected continuous catastrophe*, not two new mirrored pairs and not eight more unrelated worlds. They each revisit a geography the player already knows, changed through collision with all the others:

| Map | Returned geography | Controlled viewpoint | Concrete crossover and fragment work |
|---|---|---|---|
| 09 | Briar | Human protagonist | A Briar wolf patrol traverses an office turnstile; the House's roots meet an underwater palace stair. Recover a displaced office key and a tide-root map |
| 10 | Morrow's Earth | Morrow | A yōkai house spirit claims an office break room; forest seasons rewrite commuter schedules. Recover the lantern refuge charter and a living-hours ledger |
| 11 | Mermaid kingdom | **Char** for the first time | Vesper's paper refuge atlas reaches the coral palace; an Earth station announcement names two versions of Char. Recover the underwater road and sister's witness bell |
| 12 | Hoshimori | **Vesper** | Briar wolves with office badges police the cedar bridge; the Red Oven's chimney reaches a sea gate. Recover the wolf-door and tidal hearth seal and resolve the Last Door |

**Four protagonists / one reunited party.** The final rotation is human protagonist, Morrow, Char (rather than Scylla in the returning sea episode), Vesper. Scylla still matters critically as someone who experienced the return to her childhood, witnessed (or narrowly avoided) Char's death, and may have disclosed the future. Pip remains a distinct companion with Red Oven debt and accountability. Oren's logistics must solve physical crossings rather than being erased by magic.

**Char causality:** On the tragic World Four branch Char died *in the present*, witnessed by Scylla. Scylla's real time displacement took her to the younger Char before their original escape. The post-change Char in World Eleven must have a clearly earned causal identity: the younger Char who made decisions in the altered timeline, or an explained echo that acknowledges original loss and cannot overwrite people who paid the price. On survival branches Char has a continuous personal history and remembers the Earth-side gate. Crucially **Char has agency**, is controlled by the player and can disagree with Scylla's attempted rescue. Do not force her to be alive in the original World Four branch or imply a free resurrection.

## The crossing problem is playable, not a cosmetic crossover

Each final map has an 8×8 *authored interactive geography* preserving its original landmarks but introducing new rules from other locations. The plot: the Reimaginer has splintered unfinished decisions across multiple histories; doors, people and ecological rules are bleeding together. You cannot repair a place until you recover two meaningful fragments displaced from another reality. One must be a hard cross-rules encounter (for example a Briar wolf refusing to release a subway platform). Another should have a noncombat solution through testimony, memory or consent. Ending a map requires both fragments, its authored local crisis and a lasting decision when prescribed; a fragment ID is not proof the art, level or interaction exists yet.

Physical causes and stakes: a sea creature in a research office is not just an illustration; it floods the equipment, alters routes and creates a rescue problem. A yōkai who mistakes security badge access for household consent does not become a generic monster. Vesper's map can help people escape the flooded palace but may disclose where refugees are hiding. Earlier companion decisions and the World Four death/survival branch alter NPC behavior and viable solutions. The final e09–e12 maps are not unlocked until e01–e08's earned gates are met.

## Thirty-two authored core endings, many more lived histories

The number of reachable **core ending identities** is **2^5 = 32**, from:
- The Briar trust/witness axis, concluded after e02
- The World Four catastrophic crossing axis, **Char lost vs Char survived**; its two distinct survival subbranches still have unique consequences
- The sea-court public/private testimony axis, concluded after e06
- The Hoshimori freedom/refuge-charter axis, concluded after e08
- The final shared repair vs negotiated separation decision after e12

World Ten and World Twelve's other major decisions, plus Scylla's three-way second-chance choice, do **not** balloon this into 128 or 192 static endings. They produce meaningful changes to assistance, missing people, physical routes, relationships, ending epilogues and art variants. Four paired acts, two meaningful crossover crossroads and a final choice make seven consequential game decisions while keeping **32 core endings**. A dramatic finale must report *what changed* for Morrow's human relationships, for displaced Briar families, for Vesper's betrayal, for Char and Scylla, and for Pip's protected memories. Never give a perfect outcome at the cost of previous choices.

Thirty-two title/closing-text **authoring records** live in the application campaign reducer; complete cinematic scenes, route scripting, graphics, achievements, balanced 64-square maps and 36-room dungeons are not thereby delivered.

## Persistence, maps and production cost

- Keep `e01–e08` as authored original/twisted pairs and preserve their saves, art assets and Earth photos, especially Hoshimori e07 `2,3` / `7,5` and e08 `1,4` / `6,7`.
- Use `e09–e12` for **the four new crossover maps**, replacing their previous **unbuilt** market/crossing prototypes in the campaign registry. The previous `e13–e16` are **retired from campaign routing**.
- Legacy saves that claim former e09–e16 completion are **archived, not discarded or blindly applied to the new finale**. Preserve historical IDs separately, migrate only earned old e01–e08 choices, and require eight real crossover fragments before the new last choice/ending can be earned. Do not forge Char's fate for a legacy save with no World Four decision.
- The Earth Chronicle remains a 32-photo story, not proof of sixteen live realms. Already-reserved later photo positions must be consciously rehomed as the four final maps get real coordinates; do not delete or claim the old e13–e16 photographs are collectible without a tested migration.
- Reuse existing character portraits/cross-world locations where geometrically and narratively valid; new environmental panoramas must depict the rule collisions, not introduce four unrelated biomes. Target 30+2 collectible illustrations per live experience only, or **384 planned** instead of 512, with tracked actual ArtJobs before calling art complete.
- Next game slices: e03/e04 Earth and Scylla's e05/e06 causal choices; e07's final Red Oven rooms; e08 first sixteen actual dark-mirror scenes; then e09/e10 collision proof with physical memory mechanics; e11 player-controlled Char; e12 Vesper and the 32 endings; adversarial saves and art/rendering/device tests.
- Public launch and subjective finale approval remain human gates. Internal reversible authoring and PR merge with green CI are authorized.

**The target is a smaller game with more interactions between finished worlds. Do not count planned crossovers, generated briefs or potential ending IDs as playable completion.**
