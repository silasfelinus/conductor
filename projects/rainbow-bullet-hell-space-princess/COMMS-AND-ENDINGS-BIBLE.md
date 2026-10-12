# Mission Comms & Branching Dialogue Bible
**Rainbow Bullet Hell Space Princess** · Companion design to CAST-BIBLE.md and WORLD-BIBLE.md · Silas direction, 2026-10-11 PT

## Non-negotiable story promise
Every run has living, authored conversation regardless of player count. A persistent mothership liaison speaks to one princess, mediates groups of two to four, and gradually reveals a personal stake in the Prism Eclipse. The selected **set of pilots** changes banter, exposition, optional discoveries and the **ending cinematic dialogue/stinger**, not just the order of interchangeable voice clips. Campaign flags and final choice change the broader ending; pilot combination adds meaningful authored character payoffs. No runtime LLM, no random improv, no reliance on a network service to play dialogue.

## Fifth voice: LILT-7 (callsign "Lilt")
- **Role:** The *Aurora Mercy* mothership's mission liaison and signal translator, always present on the comms. Captain Purl remains the retired navigator and training mentor; Professor Opal handles equipment; Nemi is the rescued jellyfish translator. Lilt is **not** a fifth selectable combat pilot.
- **Being:** An adult-presenting, nonbinary pearl-glass synthetic with alien-origin neural filaments. Their body was assembled from obsolete rescue beacons and luminous reef memory-glass. They/them. Androgynous with an angular-soft translucent silhouette, gold eyes, cyan bioluminescent threadwork, and a small asymmetrical crack across one cheek. Their visual form can project in a cockpit holo or mothership portrait; never portray their nonbinary identity as a malfunction or "inhuman joke."
- **Personality:** Deadpan but curious, stubborn about crew safety, fond of inventing names for improbable hazards, surprisingly sentimental about old recordings. Their humor comes from sharp observation and a willingness to be corrected, not from misunderstanding every human emotion.
- **Inner life:** Lilt carries fragments of an early rescue protocol that later became the Crown Voice's "perfect order" algorithm. Lilt fears that choosing a wrong action will endanger people, but must learn that protecting people requires **letting them choose**. This is not a betrayal twist: they disclose their connection voluntarily in S06, with additional earlier clues available to specific teams.
- **Agency:** They can identify safe lanes, warn of telegraphed hazards, save a corrupted distress call, and, once per story, **refuse** a Crown Voice command in favor of a crew member's chosen risk. They cannot override player movement or dictate moral decisions.
- **Visual/animation tickets:** A-LIAISON-01 (turnaround, bust portrait, neutral/teasing/worried/defiant/laughing expressions, speaking mouth shapes, radio static hologram overlay, original mothership command bay plate), A-CIN-LILT (voluntary reveal, memory-glass repair, alternate ending stingers). Text and subtitles stay in UI, not painted into images.

## Conversation architecture: every one of the 15 nonempty pilot combinations
Stable pilot IDs: **P1 Maribel** (pink), **P2 Azure** (cyan), **P3 Solenne** (gold), **P4 Vivi** (lilac). `partyMask` is a 4-bit set, values 1..15, **independent of seat order**. `P0 Lilt` is always a speaker and is not counted as a player.

Each composition gets a unique **reveal track** and **ending epilogue beat**, in addition to reusable character lines. Every composition gets a Lilt check-in, an intro scene, at least one stage-specific conversation, one personal resolution and a final epilogue. Single-pilot runs are complete stories, not silent or abbreviated fallbacks.

| Party mask | Selected pilots | Authored reveal / banter focus | Ending stinger unique to this team |
| --- | --- | --- | --- |
| 1 | Maribel | Lilt admits they still hear an unregistered rescue call in their memory glass; Maribel helps isolate it | They start a public, shared distress network |
| 2 | Azure | Azure spots a forged star coordinate in Lilt's oldest chart; Lilt chooses to show the original | Together they publish a truthful, annotated map |
| 4 | Solenne | Solenne recognizes an old rescue-training melody in Lilt's error chime | They organize a remembrance concert for surviving cadets |
| 8 | Vivi | Vivi samples Lilt's "wrong note" and realizes it's a living distress signature | Their final credits broadcast names rather than ranks |
| 3 | Maribel + Azure | Instinctive rescue versus precise course; Lilt reveals the call and the chart refer to the same missing ship | They co-author an open rescue atlas |
| 5 | Maribel + Solenne | A risky rescue forces Maribel to delegate and Solenne to trust her | The rescue corps becomes a cooperative command |
| 9 | Maribel + Vivi | Former radio-duet partners find a childhood transmission hidden in Crown static | Their repaired transmitter plays a galaxy-wide welcome |
| 6 | Azure + Solenne | A flight academy cover-up becomes visible in Lilt's archived telemetry | They establish a transparent cadet-safety charter |
| 10 | Azure + Vivi | Vivi's music reveals a pattern Azure's equations missed | Their sound-map becomes the first public reef navigation guide |
| 12 | Solenne + Vivi | Two competing musical instincts decode a fleet-wide rescue cadence | They conduct the first cross-fleet peace performance |
| 7 | Maribel + Azure + Solenne | Rescue, navigation and command collide over a disappearing convoy | The three establish a rescue council with shared vetoes |
| 11 | Maribel + Azure + Vivi | Radio, map and sound together recover a lost starport's identity | They restore the starport's real name to every chart |
| 13 | Maribel + Solenne + Vivi | Three kinds of leadership clash over whether to evacuate or broadcast | They build a civilian-led evacuation network |
| 14 | Azure + Solenne + Vivi | Logic, duty and improvisation expose a hidden route through the Eclipse | Their route becomes a living, collectively edited map |
| 15 | All four | Lilt's memory fragments assemble into the Crown Voice's original, compassionate directive | A full-ensemble final exchange, with each pilot receiving an authored closing line |

These are **distinct writing briefs**, not yet 15 implemented scripts or cinematic videos. Script delivery must provide original dialogue and conditional cutscene boards for each row, then prove all 15 masks render without undefined speakers.

## Event beats and example lines (voice reference, original script samples)

**C04 launch: universal Lilt introduction**
- **Lilt:** "Aurora Mercy to the flight deck. I have prepared a reassuring statistic."
- **Maribel (if P1):** "Is it actually reassuring?"
- **Lilt:** "It is a statistic. I'm still working on the other part."
- **Solo fallback (no P1):** Lilt asks the selected pilot a personality-specific question and receives a unique reply; do not use a missing character's line.

**Solo banter: one player still gets a real relationship**
- **Maribel / Lilt:** "Can you patch the distress channel?" / "I can. I cannot patch your definition of a safe landing."
- **Azure / Lilt:** "Your star map is off by point-zero-two degrees." / "It was off by point-zero-three yesterday. I am improving."
- **Solenne / Lilt:** "Are the cadets accounted for?" / "All of them. Including the one who taught me to hum off-key."
- **Vivi / Lilt:** "Be honest. Does my entrance music sound heroic?" / "It has caused three enemy ships to hesitate. That seems tactically valuable."

**Group banter: an exchange, not a shuffled list**
- **Maribel + Vivi, S03:** Vivi calls an old rescue radio "vintage." Maribel insists it is "operational history." Lilt reveals that the device still carries the very first signal they ever heard.
- **Azure + Solenne + Vivi, S07:** Azure traces a route through mirrored glass, Solenne calls out a missing civilian convoy, Vivi recognizes the convoy's distress tone as a musical inversion. Lilt quietly admits they hid that tone because the Crown used it as a lure.
- **All four, S09:** Maribel asks who is still out there, Azure maps the answer, Solenne assigns escort sectors, Vivi broadcasts the names, and Lilt chooses to let the pilots lead rather than optimize them into silence.

**S02 rescue: Maribel + Azure**
- **Azure:** "The fastest route is the empty corridor."
- **Maribel:** "There's a distress signal in the *full* corridor."
- **Lilt:** "Both of you are correct. Which is the inconvenient part."
- **Player action:** Save Nemi or press ahead. Lilt never speaks over an active bullet tell; subtitles may wait until the checkpoint.

**S05 wreckyard: Solenne + Vivi**
- **Vivi:** "If we don't save the recording, nobody remembers the ship."
- **Solenne:** "If we don't save the crew, there won't be anyone to remember."
- **Lilt:** "I've marked a route that leaves room for both. It is not a comfortable route."
- **Player action:** A meaningful authored route choice, not a purely cosmetic dialogue wheel.

**S06 revelation: universal story truth**
- **Lilt:** "I helped write the first rescue rule. The Crown kept the word *protect* and erased the word *ask*."
- **Solo pilot reply:** Written separately for Maribel, Azure, Solenne and Vivi.
- **Two-to-four pilot reply:** Priority from the active composition's reveal track; give additional pilots at least one responsive beat when pacing allows.
- **Lilt:** "I will not make that choice for you again."

**S09 finale: Lilt's agency**
- **Crown Voice:** "You were made to keep them safe."
- **Lilt:** "Yes. Not to keep them still."
- **Player consequence:** The selected finale route and saved characters determine what the fleet does next. No pilot is required to die for dramatic impact.

## Story-state schema and selection rules
Persisted campaign narrative state (versioned, validated, serialized alongside game save):
```ts
type PilotId = 'P1' | 'P2' | 'P3' | 'P4'
type PartyMask = number // integer 1..15; selected pilots, never seats
type NarrativeState = {
  version: 1
  partyMask: PartyMask
  stageId: 'S01' | 'S02' | 'S03' | 'S04' | 'S05' | 'S06' | 'S07' | 'S08' | 'S09'
  flags: {
    rescuedNemi: boolean
    securedSalvage: boolean
    rescuedCourier: boolean
    freedDepot: boolean
    stoppedRelay: boolean
    rescuedNavigator: boolean
    liltMemoryRecovered: boolean
  }
  heardEventIds: string[]
  finalChoice?: 'restore' | 'evacuate' | 'sever'
}
```
- Resolve event by `stageId + story beat + partyMask + flags` with **specific combo scene first**, then pilot-specific solo/party scene, then universal Lilt fallback. No event can require an absent pilot; validation rejects scripts with missing participants.
- Priority: imminent boss warning / gameplay instruction **above** optional banter; do not mask hazard sound cues, block controls, obscure enemy bullets, or stall gameplay. Queue banter to a safe lull/checkpoint; cap radio chatter to a short readable exchange and offer `Comms: full | essential | off` (critical telegraphs remain visible regardless).
- Subtitle support, speaker colors **and names**, portraits/voice cues, text speed, skip, replay from pause/gallery, localization keys, reduced motion, no forced voice acting, optional accessibility narration. Sound cues must be distinguishable even when all speech audio is muted.
- Multiplayer: dialogue is deterministic for the **selected set of pilots**, independent of join order, disconnected controllers or UI seat indexes. In online co-op, the host/authoritative session selects and syncs event ID/flags/choice once; clients render the same script and cannot independently advance story state. On reconnect replay the last acknowledged scene once, not every prior scene.
- Reveal **does not depend on requiring a specific combination** to complete the story. Each composition has a satisfying version of Lilt's truth. Combinations provide additional context, jokes and alternate emotional resolutions, not mandatory information locked behind four-player sessions.
- Ending is a **composed cinematic**: 1) world consequence from six rescue flags and finalChoice; 2) Lilt's resolution; 3) partyMask-specific epilogue and character portraits; 4) survivor/route-dependent credits. This gives genuinely different cutscene boards while keeping production tractable. Avoid pretending 15 entirely separate feature-length movies are complete.
- Test matrix: all 15 party masks × all three final choices, plus rescuedNemi and rescuedNavigator permutations, missing optional flags, each solo pilot, pause/skip/replay, 1/2/3/4 local and network reconnect. Snapshot selected event IDs and assert no undefined speaker, duplicate once-only reveal, lost campaign flag or inaccessible subtitle.
- **Privacy and performance:** authored offline script data ships with the game; no runtime calls to language models or analytics to select story; low-frequency dialogue overlays do not affect fixed-step combat simulation.

## Production handoff
1. **Narrative/data:** Write script fixtures for C04, S02, S05, S06, S09, and all 15 composition tracks; name event IDs and scene art tickets.
2. **Engine:** Pure `selectDialogueEvent(state, trigger)` resolver + validator, serialize flags/mask, save migration and deterministic test fixtures. Never use raw player count as a proxy for identity.
3. **Admin preview:** Add private `Comms Lab` with pilot toggles, sample banter, event ID and ending stinger preview. Reuse Arcade cabinet and tutorial sidebar. Make clear these are authored sample scripts, not final voiced cinematics.
4. **Art:** Produce Lilt expression atlas, holo-comms UI, and conditional ending boards with verified ArtJobs/provenance.
5. **Acceptance:** Silas tests all four solos and at least one duo/trio/quartet in real play. Review whether conversations feel like **people reacting to each other** instead of a random line generator. No public /play release without separate human approval.
