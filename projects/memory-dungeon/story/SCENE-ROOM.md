# Quest Writer's Scene Room

[Writer's Room](../WRITERS-ROOM.md) · [Act pitches](ACT-PITCHES.md) · [Map plans](MAP-PLANS.md) · [Ending design](ENDING-MATRIX.md)

**Purpose:** turn a world pitch into *one* durable, playable location. This is a brief and writing checklist, not live runtime data. Current application locations, artwork and save reducers must be inspected before changing ID/flag names.

## The scene packet, in the order you need it

1. **Premise (1–2 sentences):** whose memory this is, what the location was in an earlier act, and what incompatible second-world rule now appears.
2. **Encounter (1 short paragraph):** character with goals, concrete physical problem, and why matching, conversation or traversal is appropriate. Not every site requires combat.
3. **Two or three consequential choices:** every option has a *fairly visible cost*, a distinct narrated outcome and a durable fact, resource, route, alliance or witness effect.
4. **Failure continuation:** a missed puzzle, wounded ally or refused bargain does not create an unrecoverable mandatory fragment.
5. **Callback (one later use):** a later world, reunion or one of the 32 ending families must reference an actual saved decision. Do not assert a witness who was never met.
6. **Art/QA:** original setting and crossover source visually legible, separate scene/choice art targets, actual ArtJob receipt versus undelivered prompt, a deterministic save/replay test.

### Writer-ready e11 Char quests (still not playable)

[The Sea Sister Bell and Unwritten Map packets](SEA-COLLISION-CHAR-QUESTS.json) contain two fully voiced encounters, six distinct decisions and nine e04 tide-gate × e05 departure history introductions. The contract explicitly requires earned e06 Char continuity before the playable e11 viewpoint can open; it does **not** resurrect the original Char, invent a prior decision, award a fragment for visiting a tile, or count proposed art as delivered. The companion `tests/test_memory_dungeon_char_sea_collision.py` simulates all 81 two-quest decision routes and rejects forged histories, repeated awards and rewritten choices. This is a **writer packet and state-contract test**, not runtime integration: e06 continuity, e11 scenes, durable ArtJobs, final media, device QA and playable callbacks still require implementation.

### Eight first-pass finale quest pitches (not yet playable)

| World / fragment | Opening beat | Two choices and costs | Later payoff |
|---|---|---|---|
| e09 `briar-office-key` | **Playable Pip** encounters a Briar wolf patrol blocking an accounting office while a night-shift guard insists on showing a valid badge. | **Translate** the guard's shift into an oath and owe the wolf a favor; **break** the clock and evacuate everyone but lose evidence of who worked there. | Morrow's office recognizes a real worker, or the timeline lacks reliable employment evidence |
| e09 `briar-tide-roots` | The House's roots follow Scylla's seawater currents into a shelter no official map should identify. | **Use** the tidal chart to guide a private escort, risking rising water; **dam** the route and find a slower public crossing, leaving families waiting. | Char can name the House/sea overlap, with or without displaced witnesses |
| e10 `city-lantern-charter` | An overnight yōkai caretaker locks the elevator to protect overworked employees. | **Negotiate** voluntary rest and delay evacuation; **remove** the ward so transit reopens while workers lose magical protection. | Hoshimori survivors lend aid or demand renewed safety terms |
| e10 `city-forest-hours` | Briar vines rewrite the train clock into seasons. Morrow must rescue a commuter who cannot remember which season they entered. | **Reconcile** the timetable and let a dangerous branch of forest remain; **cut** the canopy and lose an old witness route. | Vesper finds either a navigable green shortcut or a devastated but open platform |
| e11 `sea-unwritten-map` | A refuge atlas from Vesper's youth floats through the palace; Char discovers a person's real name erased from it. | **Return** the atlas to its owners, losing the most direct escape; **redact** a safe public passage under consent, risking a copied route. | Vesper's final map choice inherits a living promise, not a free pass |
| e11 `sea-sister-bell` | A train voice announces *two Chars* while Scylla recognizes the bell from the crossing where Char may have died. | **Listen** to both versions and accept a disputed record; **choose** Char's present testimony and leave a historical question unanswered. | Finale dialogue distinguishes remembered Char from played Char; no resurrection retcon |
| e12 `village-wolf-door` | A wolf with a corporate badge guards Hoshimori's childhood footbridge, demanding registered home addresses. | **Broker** an anonymous exit under witness oversight, weakening patrol control; **divert** the patrol with Vesper's old map and risk another copied route. | The final crossing admits privacy or keeps a dangerous unverified detour |
| e12 `village-tidal-oven` | The Red Oven opens into the royal tide gate. Hungry refugees are asked to feed it private childhood memories. | **Ration** ordinary meals and permit a slow crossing; **rebuild** the Oven's consent pact and accept reduced capacity. | Consent-based repair or separation of worlds can both still be reached |

**Fairness:** The fragments are earned through meaningful actions, not automatic tile visit. Every world has two, and no writer may require a dead character or a prior optional success as the *only* way to pass. A lost fragment can be recovered through an authored alternative, never fabricated by the finale reducer.

## Branch-aware dialogue checklist

- **Char:** `open-the-tide-gate` means Scylla witnessed death in the present; `seal-the-tide-gate` means stranded commuters; `divert-the-current` means a ruined district. e05 `run-again / stay / tell-char` is a second, separate decision. e11 must explain which Char the player controls under every legal history, with no imposed identity.
- **Vesper:** Read Briar/Dark Briar `3,2` before claiming a betrayal was confessed. In e07 `1,1`, `4,4`, `3,8`, `8,8` shape personal accountability, map custody and the final route.
- **Pip:** His Hoshimori `2,2` ledger choice and Red Oven witnesses are his; do not turn him into a subordinate mouthpiece for Vesper's apology.
- **Morrow:** Protect the existence and dignity of the Earth life he has built. The opening should not give away the children before earned Chronicle discoveries.
- **Oren:** Competent hooded logistics professional and royal headsman. He should solve impossible supply problems without a tired hidden-face reveal.

## Writer's handoff form

Write an issue or standalone brief with these fields:

```yaml
world: e10
site: proposed-coordinate-until-atlas-locked
focus: Morrow
original_landmark: "Office elevator"
collision_rule: "Hoshimori household guardian enforces rest"
dramatic_question: "Who may decide what is safe for exhausted workers?"
prerequisites: ["earned route history if available; fallback if not"]
choices:
  - id: "negotiate-rest"
    visible_cost: "The commute is delayed"
    saved_effect: "voluntary-protection-charter"
  - id: "open-elevator"
    visible_cost: "Caretaker ward ends"
    saved_effect: "evacuation-without-ward"
required_fragment: city-lantern-charter
failed_path: "Alternative fire stair and witness consent"
later_callback: "e12 shelter terms and finale"
art: "Original physical scene plus choice outcomes, no artist imitation"
tests: "Two choice saves, forged choice rejected, interrupted replay, 390px layout"
implementation_status: "PITCH ONLY"
```

Before submitting art: an art **idea** is not an ArtJob, an ArtJob **DONE** is not a delivered media file, and an existing unrelated painting is not proof of this character/world scene. Match assets to scene IDs and verify final paths.

## Deep references

- [Briar geography and House](../BRIAR-MARCHES-FIRST-WORLD.md)
- [Vesper's Hoshimori childhood and first 16 dark scenes](../VESPER-HOSHIMORI-CHILDHOOD-AND-HORROR.md)
- [Hoshimori warm source](https://github.com/silasfelinus/kind_robots/blob/main/utils/memoryDungeon/hoshimoriWarm.ts)
- [Cross-realm choices in game code](https://github.com/silasfelinus/kind_robots/blob/main/utils/memoryDungeon/firstTwoConsequences.ts)
- [Archived task provenance and actual earlier PR references](../archive/roadmap-2026-10-30-pre-12-world-slim.yaml)
