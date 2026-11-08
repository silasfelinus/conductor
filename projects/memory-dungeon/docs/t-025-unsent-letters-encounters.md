# Memory Dungeon e03/e04: The Unsent Letters
<!-- t-025; authored encounter packet, not a claim of runtime integration -->

## Contract

This packet adds four **optional** linked encounters to the existing Earth pair. It does not add map coordinates or replace the existing 64 authored sites. Bind each encounter to an existing compatible e03/e04 site only after verifying its current coordinate, choice IDs and saved-state schema. Rowan is the name used on Earth for Morrow. The player must never learn the contents of an unread letter simply by selecting an option.

The scenes share one small consequence ledger. Their stakes are trust, consent and the difference between protecting someone and editing their life. Each encounter has a short entry, three choices, one consequence line and no follow-up confirmation screen. The e04 horror versions remember e03 actions, but **never require** a particular e03 choice to remain completable.

### Ledger and validation

```ts
type LetterFlags = {
  e03Letter: 'unseen' | 'delivered' | 'shelved' | 'copied'
  e03Witness: 'none' | 'asked' | 'refused' | 'protected'
  e04Archive: 'unseen' | 'released' | 'sealed' | 'annotated'
  e04Return: 'unseen' | 'offered' | 'declined' | 'witnessed'
}
```

Initial state: all four flags `unseen` except `e03Witness: 'none'`. Each choice changes **only its own flag**; `e03Witness` is independent of the letter decision. Choices are single-use and their outcome is persisted atomically with the visited site. The e04 scene reads earlier flags but cannot rewrite them. A second invocation returns the recorded outcome with no extra reward. Invalid values, unknown choice IDs, a resolved scene with a conflicting new choice, or an e04 outcome claiming an unvisited e04 site are rejected during restore. Importing a legacy save with no ledger initializes defaults without changing existing story, resource, map, deck or photograph fields.

**Reachability cases:** e03 delivered/shelved/copied × e03 witness asked/refused/protected/none × e04 released/sealed/annotated × e04 return offered/declined/witnessed = 108 combinations. Every combination has an ending route; none consumes a mandatory key or photograph. This is a combinatorial specification, **not** a claim that 108 executable tests have run.

## e03 scene A: The Envelope With No Address

**Entry:** At the laundromat, the dryer coughs up an envelope with Rowan's handwriting. The name on the front has been rubbed away by a thumb. The machine is unplugged. Nobody else seems surprised.

**Delivery,** `earth-letter-deliver`: “It's addressed to someone,” you tell the attendant. “That doesn't make it mine.” She offers the lost-property drawer, then pauses. “Would you like me to leave the drawer unlocked?” You ask her to keep it shut. **Outcome:** The letter enters ordinary lost property. `e03Letter=delivered`. Consequence text: “You have given a stranger a chance to decide.”

**Shelve,** `earth-letter-shelve`: “Could you hold it until somebody asks?” The attendant writes today's date, not the name, on a paper sleeve. “Three days,” she says. “Then we decide again.” **Outcome:** The letter remains unopened in temporary custody. `e03Letter=shelved`. Consequence: “A delay is not an answer, but it can be a kindness.”

**Copy,** `earth-letter-copy`: You photograph the sealed envelope, including its damaged front, without opening it. “In case it vanishes,” you say. The attendant looks at your phone. “And if it doesn't?” **Outcome:** You keep evidence of the envelope's existence, not its contents. `e03Letter=copied`. Consequence: “Proof can protect someone. It can also follow them.”

## e03 scene B: The Research Assistant's Question

**Entry:** A student recognizes Rowan outside the library. “I used to work for them. Do you know why they stopped answering?” They hold out a lab keycard with the corner snapped off.

**Ask,** `earth-witness-ask`: “What did you need them to answer?” The student says, “Whether I could put my name on the work.” You do not promise a verdict. **Outcome:** `e03Witness=asked`. Consequence: “A grievance becomes a question someone might answer.”

**Refuse,** `earth-witness-refuse`: “I can't speak for Rowan.” The student pockets the card. “Neither can Rowan, apparently.” **Outcome:** `e03Witness=refused`. Consequence: “You kept your boundary. They still have theirs to carry.”

**Protect,** `earth-witness-protect`: “Write down what you contributed, with dates. Keep a copy somewhere Rowan cannot edit.” The student nods, then asks if you will read it. “Only if you want me to.” **Outcome:** `e03Witness=protected`. Consequence: “You offered a method, not ownership of their story.”

## e04 scene C: The Filing Cabinet That Breathes

**Entry:** The same laundromat now has an archive cabinet where the dryer stood. Its drawers open on the inhale. A label reads: THINGS PEOPLE WOULD HAVE SAID IF YOU HAD LET THEM. The cabinet knows whether the envelope was delivered, shelved or photographed, but never quotes its contents.

**Release,** `earth-archive-release`: “Those aren't yours to keep.” You open the drawers toward the street. The pages lift like moths, each searching for its own reader. **Outcome:** `e04Archive=released`. Consequence: “You cannot choose where every page lands.”

**Seal,** `earth-archive-seal`: You close the cabinet with its own bent key. The breathing stops, but a thin whistle escapes from the lock. **Outcome:** `e04Archive=sealed`. Consequence: “Silence is not the same as safety.”

**Annotate,** `earth-archive-annotate`: On the outside, you write: THESE RECORDS MAY BE WRONG. The cabinet scratches out MAY, then slowly puts it back. **Outcome:** `e04Archive=annotated`. Consequence: “Doubt has become a door, not a verdict.”

**Conditional callback (one line only):** delivered → “A drawer opens for a person who might come back.” shelved → “A date stamped on paper repeats every three days.” copied → “Your phone shows an envelope you never opened.” unseen → “The cabinet offers no explanation of what you missed.”

## e04 scene D: The Door Marked RETURN TO SENDER

**Entry:** A door stands in the library corridor, its brass slot wide enough for a hand. Behind it, someone is rehearsing Rowan's voice. They keep getting the laugh wrong.

**Offer,** `earth-return-offer`: “You can use your own voice,” you tell the unseen speaker. The rehearsing stops. “What if nobody recognizes it?” “Then start with your name.” **Outcome:** `e04Return=offered`. Consequence: “You offered an exit without demanding a confession.”

**Decline,** `earth-return-decline`: You pass the door without turning the handle. A laugh follows you, imperfect and unmistakably alive. **Outcome:** `e04Return=declined`. Consequence: “Not every threshold belongs to you.”

**Witness,** `earth-return-witness`: “I can wait while you decide,” you say. A chair slides through the slot, one leg at a time. You sit. Nobody asks you to stay forever. **Outcome:** `e04Return=witnessed`. Consequence: “Witnessing is a promise with an end.”

## Acceptance before runtime integration

1. Validate each choice ID is unique across the existing Earth choice registry before adding it; do not replace or renumber existing IDs.
2. Test all twelve choices individually, each replayed twice; the second resolution must return the original record with zero additional effect.
3. Test the four e04 callbacks with delivered, shelved, copied and unseen e03 letter states; no branch reveals unread contents.
4. Test legacy save with no letter ledger, a forged e04 visit, an unknown choice ID and a conflicting second choice.
5. Verify no scene awards a mandatory key, photograph, deck unlock or combat resource, and all e03/e04 story exits remain reachable.
6. At 390/768/1440 widths, render one encounter with art-first choice cards, readable outcome text and no new page-level scrolling. Production art must be separately enqueued and delivery-verified; this packet supplies **zero ArtJob IDs**.

**Status:** Authored, with formal state/branch contract. Runtime binding, executable tests, illustration jobs and rendered QA remain outstanding. Do not mark t-025 done from this packet.
