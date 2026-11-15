# e03/e04: The Night Shift (authored encounter packet)

Status: **authored, not implemented**. Scope: four optional, connected Earth-side encounters in Morrow's original/twisted pair. This is not a claim of 64-site completion, live state integration, production art, or device acceptance.

## Design contract

These encounters examine what it costs to keep another person's ordinary life running while a stranger occupies their body. No scene assumes that the player has forgiven Morrow, and none makes Morrow's children expendable. They share one local thread, `nightShift`, rather than creating four independent reward faucets.

Persistent keys (current-version saves only): `nightShift.witnessed` (set of scene IDs), `nightShift.decisions` (map of scene ID to choice ID), `nightShift.receipts` (set of reward IDs), `nightShift.evidence` (set of witnessed evidence IDs). These must be written atomically with the associated scene outcome, and restored only from the save's authenticated encounter ledger. An option may be displayed repeatedly, but its first committed decision is immutable for that run. Neither replaying a scene nor loading a save grants its reward twice. Unvisited scenes confer no evidence or Chronicle unlock.

The four encounters are optional authored landmarks to be assigned to **four distinct, connected e03/e04 cells** by the map implementer. Do not reuse photograph cells or override fixed geography. If no such cells remain, hold the packet rather than silently replacing an existing authored site.

## Scene NS-01: The Locked Laundromat (e03)

A laundromat is closing at 2 a.m. The attendant recognizes Morrow's face but not the way the protagonist folds a child's school uniform. A forgotten name is written on the inside of the sleeve. The attendant says: “You used to know whose it was without looking.”

- `ns01-return`: Return the uniform to the marked apartment lobby. Gain evidence `uniform-name`; lose one unit of the run's **existing** time/pressure resource, if supported. If not, represent the cost as a delayed next encounter, never invent a new currency.
- `ns01-ask`: Ask the attendant how Morrow used to behave. Gain evidence `attendant-account`, but the attendant alerts the family that something is wrong. Set `family-suspicion` consequence.
- `ns01-leave`: Leave the garment safely at the counter, with no evidence. Preserve a later opportunity to learn the name elsewhere.

The attendant never states that the protagonist is Morrow. If `family-suspicion` already exists, replace the alert with an acknowledgement, not a duplicate penalty.

## Scene NS-02: The Hospital Vending Machine (e03)

A night nurse is feeding a machine that has swallowed her last coin. She recognizes Morrow as the person who used to bring spare change for families waiting through the night. “You stopped coming. People noticed.”

- `ns02-help`: Spend an existing consumable or noncombat resource (only if available); the nurse shares `visiting-hours` evidence. If payment is unavailable, allow a non-resource alternative with an equivalent time cost.
- `ns02-listen`: Sit through the nurse's account of Morrow's difficult first months. Gain `nurse-account` evidence, with no item reward.
- `ns02-deflect`: Refuse the conversation. Gain no evidence; preserve the nurse as a future contact.

The nurse's account is incomplete and should not settle the identity dispute. The machine is never a loot chest.

## Scene NS-03: The Wrong Emergency Contact (e04)

An old phone rings in the twisted world's empty waiting room. The caller asks for Morrow, whose number remains listed as an emergency contact. The caller knows a child is waiting, but not which adult will answer.

- `ns03-answer`: Give practical directions without claiming to be the child's parent. Gain `contact-call` evidence and `promise-made` consequence.
- `ns03-transfer`: Route the call to a trusted contact established by witnessed prior dialogue. Gain `contact-transfer` evidence. **Gate:** this choice is unavailable without that witnessed contact; a forged save flag must not expose it.
- `ns03-silence`: Let the call end, then record the number for later. Gain `missed-call` evidence; no promise.

If `promise-made` exists, later dialogue must acknowledge whether it was kept. No branch asserts that the child was harmed solely because this optional scene was missed.

## Scene NS-04: The Ledger of Small Favors (e04)

A paper ledger contains mundane debts: bus fare, a borrowed coat, a repaired zipper, a birthday cake. The protagonist can recognize the handwriting, but not the memories. A margin note reads: “Not everything owed can be repaid by the same person.”

- `ns04-copy`: Copy the names without taking the original. Gain `favor-ledger` evidence; this may support a later Chronicle interpretation, not an instant stat boost.
- `ns04-return`: Deliver the ledger to the rightful keeper if that keeper has been witnessed in NS-01 or NS-02. Gain `ledger-returned` consequence; **gate:** require an actual witnessed keeper, not merely a choice string.
- `ns04-close`: Close the book and leave it intact. Gain `ledger-preserved` consequence without evidence.

If the player previously made `promise-made`, add one concise callback to the relevant ledger entry. Never require the player to complete NS-01 through NS-03 to finish e04.

## Branching and narrative acceptance

- All twelve choices have stable IDs and one mutually exclusive first outcome per scene. Every scene has a nonviolent path and a no-reward path.
- NS-03 transfer and NS-04 return are conditional; when gated, show a comprehensible disabled reason and preserve other choices.
- The player may visit these scenes in any order allowed by the map, including e04 before witnessing any e03 optional scene. No dead end or forced identity conclusion.
- At most one reward receipt per scene per run; evidence is knowledge, not a repeatable item or permanent combat modifier.
- A Chronicle interpretation may require **two independently witnessed** evidence IDs from distinct scenes. It cannot be earned by a restored, manually forged `evidence` set without corresponding encounter receipts.
- Dialogue is perspective-aware: the player is not casually called Morrow by the narrator; NPCs may mistake their face for Morrow's.
- Choices should have one short immediate response and one later callback, rather than verbose exposition or universal “good/bad” morality.

## Executable acceptance matrix for implementation

Use seeded route and save/restore tests, not only static text assertions:

| Case | Required result |
| --- | --- |
| 4 scenes × 3 choices | Exactly 12 stable outcomes, no undefined transition |
| 4 scenes × 3 replay attempts | First outcome remains committed; receipts and costs unchanged |
| 4 scenes × reload before/after choice | Same scene eligibility and exactly-once consequence |
| NS-03 forged contact flag | Transfer remains unavailable without witnessed contact |
| NS-04 forged keeper flag | Return remains unavailable without witnessed keeper |
| e04-first route | NS-03 and NS-04 remain playable without e03 evidence |
| family-suspicion preexisting | NS-01 does not double-apply suspicion |
| promise-made callback | Later ledger text changes without rewriting past choices |
| two same-scene evidence IDs | Does not satisfy distinct-scene Chronicle gate |
| unvisited evidence injection | Cannot grant Chronicle unlock |
| no available resource at NS-02 | Noncombat alternative remains accessible |
| world exit and return | No duplicate reward or re-opened irreversible decision |

**Implementation order:** bind four distinct map cells; implement the typed outcome ledger and dialogue callbacks; add seeded reducer/save tests; verify rendered single-screen mobile/tablet/desktop choices; queue four production scene illustrations and verify delivered media. Until those steps pass, leave t-025 active.
