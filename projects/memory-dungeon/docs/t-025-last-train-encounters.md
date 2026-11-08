# Memory Dungeon e03/e04: The Last Train (optional encounter packet)

**Scope:** memory-dungeon/t-025, Morrow's ordinary Earth (e03) and its horror revisit (e04). Four authored scenes, twelve stable choice IDs, one persistent hinge with a later horror callback. **Not implemented in the game yet.** This packet adds no world coordinates, changes no existing map or save identifiers, and must be assigned only to currently unoccupied authored encounter slots after a collision audit. It is not a replacement for e04's existing tide-gate/Char decision.

## Premise and staging

The last commuter train is halted at a station whose announcement system has begun reading passengers' private apologies. On ordinary Earth the problem is human: a malfunctioning display, a frightened conductor, and an emergency exit that the railway insists must stay shut until a supervisor arrives. On the return visit, the same platform has lengthened beyond the tunnel, and the display reads the apologies *before anyone thinks them*. Morrow is the playable lead in both worlds. The train cannot strand the campaign: each scene offers a clear leave option and all outcomes lead back to exploration.

**Production art coverage required:** four unique 2:3 painted encounter illustrations, with distinct original/horror compositions rather than color-filtered duplicates. e03: conductor under amber platform lamps; passenger with a folded paper timetable. e04: impossible platform vanishing into a train window; carriage of empty coats facing a lit emergency door. No generated media or ArtJob IDs are claimed by this document.

## Scene 1, e03: The Door With a Red Handle

**Entry:** Morrow finds the conductor holding the emergency release. The display says DELAY: HUMAN ERROR. A teenager on the platform has a bleeding hand; their guardian is trapped on the other side of the locked doors.

**Conductor:** “If I open this without authorization, the system records me as the emergency.”  
**Morrow:** “It can record me too. It doesn't get to decide whether someone bleeds.”

- `md.train.e03.release`: Morrow helps the conductor pull the release, gets the teenager to their guardian, and agrees to give a truthful statement. Set `trainDoor=opened`, `trainWitness=public`. Consequence: the conductor may face discipline, but the injured passenger receives care now. **One-time reward:** a brass transit token, `trainToken=true`.
- `md.train.e03.wait`: Morrow improvises a pressure bandage and keeps the teenager talking while the conductor calls emergency services. Set `trainDoor=held`, `trainWitness=private`. Consequence: help arrives late but the conductor retains their job; the guardian remembers who stayed. **One-time reward:** the conductor's annotated route slip, `trainRouteSlip=true`.
- `md.train.e03.leave`: Morrow gives the conductor the station's emergency number, points out the medical kit, and leaves. Set `trainDoor=delegated`, `trainWitness=none`. Consequence: the conductor chooses independently; Morrow will not learn which decision they made. No item reward.

**Exit:** The loudspeaker says “SERVICE RESUMED” even though no train moves.

## Scene 2, e03: The Timetable That Wasn't Printed

**Entry:** A passenger offers Morrow a folded paper timetable. Its handwritten margins record which riders always wait for one another. The passenger asks whether the list should be shared with the conductor.

**Passenger:** “It's not a schedule. It's the reason some people make it home.”  
**Morrow:** “Then whoever reads it has to know the difference.”

- `md.train.e03.share`: Give a *copy* to the conductor with the passenger's permission. Set `trainLedger=shared`. The conductor arranges a reliable last-car check; public accountability improves, but the passengers' routines become easier to surveil.
- `md.train.e03.return`: Return the original and refuse to copy it. Set `trainLedger=returned`. The passenger keeps their trust network private; coordination remains fragile.
- `md.train.e03.redact`: With consent, remove names and preserve only meeting points. Set `trainLedger=redacted`. The conductor can improve service without tracking people individually, though the map is less precise.

**Callback:** If `trainDoor=opened`, the passenger recognizes Morrow from the emergency statement and asks whether the truth made anyone safer. If `held`, they offer thanks for staying. If `delegated`, they simply ask whether Morrow has ridden this line before. None of these lines changes the choice set.

## Scene 3, e04: Platform Zero

**Entry:** The horror counterpart of the platform has no tracks. Its red handle is mounted on the air, and each departing announcement speaks in the voice of someone Morrow once disappointed.

**Announcement:** “THE DELAY WAS YOURS. THE DELAY WAS ALWAYS YOURS.”  
**Morrow:** “You can have my words. You don't get their mouths.”

- `md.train.e04.open`: Pull the handle and accept that a corridor may open onto witnesses rather than escape. Set `trainNightDoor=opened`. If `trainDoor=opened`, the conductor's earlier statement becomes an audible guide to the safe exit. Otherwise, Morrow follows the sound of a real train's brakes. Reward a one-time `trainEchoFragment` only if not previously collected.
- `md.train.e04.listen`: Refuse the false urgency; listen for a voice that breathes between announcements. Set `trainNightDoor=listened`. If `trainWitness=private`, the teenager's steady counting points toward the exit; otherwise, a living passenger's footsteps do. Reward a one-time `trainEchoFragment` only if not previously collected.
- `md.train.e04.retreat`: Step away from the handle and take the maintenance stairs. Set `trainNightDoor=retreated`. No fragment, no soft lock, no punishment for refusing the haunted mechanism.

**Exit:** The announcements continue after Morrow leaves, but now each voice sounds slightly less certain.

## Scene 4, e04: The Carriage of Empty Coats

**Entry:** Every coat in the empty carriage has a name pinned inside. A ticket inspector with no face asks Morrow to announce the names aloud so their owners can be “returned.”

**Inspector:** “A name is proof of a passenger.”  
**Morrow:** “A coat isn't proof of a person.”

- `md.train.e04.name`: Read only the names whose owners are present and explicitly consent. Set `trainNightLedger=consented`. If `trainLedger=shared`, the inspector offers a list of every rider; Morrow rejects the extra names. The coats belonging to present passengers fall still.
- `md.train.e04.map`: Describe the safe exits and meeting places, never the passengers. Set `trainNightLedger=routes`. If `trainLedger=redacted`, Morrow recognizes the shape of their earlier compromise and can guide the carriage out more quickly.
- `md.train.e04.silence`: Decline the inspector's demand and leave the carriage door propped open for anyone who chooses to walk out. Set `trainNightLedger=refused`. If `trainLedger=returned`, the passenger's folded timetable appears beneath the door, still unread.

**Exit:** The inspector stamps an empty ticket. The stamp reads NOT YOURS TO KEEP.

## Persistent state and validation

Namespace all new keys under a versioned Memory Dungeon expedition-story object, not Classic Match or card-gallery progress. Store only choice IDs and booleans/enums, not the prose itself. Never infer e04 completion from e03 outcomes, and never rewrite historical e13–e16 data. Preserve the existing e04 tide-gate/Char branch unchanged.

- `trainDoor` ∈ {opened, held, delegated}; `trainWitness` is derived exactly from it: opened→public, held→private, delegated→none.
- `trainLedger` ∈ {shared, returned, redacted}.
- `trainNightDoor` ∈ {opened, listened, retreated}.
- `trainNightLedger` ∈ {consented, routes, refused}.
- Scene completion keys are independent. Each scene can be skipped. A later scene with absent earlier state uses the unconditional fallback text, never fabricates a previous choice.
- A scene's first accepted choice is final for that save; re-entering shows its consequence and offers only Continue. No second reward or contradictory choice. Restoring a save mid-dialogue must not commit an outcome until the player confirms.
- The brass token, route slip and echo fragment are unique-per-save; a replay or duplicated action cannot increase inventory counts. Leaving or retreating does not remove existing rewards.
- No scene can grant a finale fragment, complete a dungeon, change Char's fate, unlock an overworld, or modify a 30+2 collectible deck.

## Acceptance matrix for implementation

1. All 3×3 e03 choice combinations can reach both e04 scenes; each scene also loads independently with missing e03 state.
2. All 3×3 e04 combinations exit to the existing map without a blocked route.
3. Every `trainDoor` value yields exactly its documented `trainWitness` value; malformed saved values fall back to no callback and do not create rewards.
4. Save and restore before confirmation leaves all four scene decisions unset; after confirmation, the exact choice persists.
5. Duplicate choice submissions and repeated scene visits cannot duplicate the token, route slip, or echo fragment.
6. No option changes the existing tide-gate, Char, world-completion, gallery, or Classic Match keys.
7. Render choice cards with art and readable text on a single screen at 390, 820 and 1440px; reduced-motion navigation retains clear focus and feedback.
8. The art pipeline records four durable ArtJob IDs and verifies four delivered, correctly bound images before the packet is called art-complete.

**Integration handoff:** Audit occupied e03/e04 map cells, select four available encounter slots without displacing authored content, bind these scene IDs into the existing encounter registry and Pinia persistence, implement the matrix as executable tests, submit actual art jobs, and run rendered browser checks. This writing packet is a partial task increment, not a completed world or human gate.
