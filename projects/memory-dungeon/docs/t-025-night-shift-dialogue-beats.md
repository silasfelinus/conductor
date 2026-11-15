# Night Shift: playable dialogue and consequence beats (e03/e04)

Companion to `t-025-night-shift-encounters.md`. **Authored script, not integrated gameplay.** The scene IDs and choice IDs below are binding; do not invent substitute IDs when implementing. These four scenes must occupy four separate, reachable cells only after map occupancy is checked. They are optional, never required to leave e03 or e04.

## Presentation contract

Each scene has a compact setup (maximum two dialogue cards), three choice cards with an accessible self-contained label, one immediate response, and a one-sentence delayed callback. A locked choice stays visible with its reason. The narrator calls the protagonist **you**; NPCs recognize Morrow's face without asserting that the protagonist shares Morrow's identity. Every outcome commits once per expedition and is restored from the witnessed scene event, not a free-floating inventory flag.

### NS-01 · The Locked Laundromat · e03

**Art subject:** fluorescent laundromat at 2 a.m.; a tiny school uniform hangs in a circle of oversized adult coats. A name is stitched inside the sleeve. Do not show a recognizable child.

**Attendant:** “We close in six minutes. You used to arrive with three minutes left and fold everything before the dryer cooled.”

**You:** “I don't remember that.”

**Attendant:** “I can see. That's the part I'm worried about.”

- **`ns01-return` · “Take the uniform to the named lobby. Lose time, not the garment.”** The attendant points to an apartment entry visible from the street. **Immediate:** “The lobby's night light is still on. You hang the uniform where its owner can find it. Nobody comes to the door.” Commit `uniform-name` evidence and one time/pressure cost if that resource already exists; otherwise defer the next encounter. **Callback:** At a later family-facing site, “Someone found the uniform. They ask why you didn't knock.”
- **`ns01-ask` · “Ask what Morrow was like here. The family may hear about it.”** **Immediate:** “The attendant counts three winters of late pickups, then reaches for the phone. ‘Someone should know you're asking.’” Commit `attendant-account` and `family-suspicion` once. **Callback:** “The family has heard you asked about yourself in the third person.” If suspicion already existed, use “The attendant says the family has already called” with no second penalty.
- **`ns01-leave` · “Leave the uniform safely at the counter. Learn nothing tonight.”** **Immediate:** “The attendant writes a claim ticket and pins it to the sleeve. ‘I won't throw it away.’” No evidence or penalty. **Callback:** “The attendant kept the uniform, but no longer assumes you will collect it.”

### NS-02 · The Hospital Vending Machine · e03

**Art subject:** a tired nurse kneeling beside a jammed vending machine; coins visible behind glass, empty waiting-room chairs beyond. No implied medical emergency or child in danger.

**Nurse:** “It kept my coin. You used to know how to persuade it.”

**You:** “I don't think I know anything about machines.”

**Nurse:** “You knew when to sit with someone. That counted.”

- **`ns02-help` · “Help the nurse get a drink. Spend a supply or take extra time.”** **Immediate:** “You find a way to free the cup. The nurse writes visiting hours on a receipt instead of thanking you.” Commit `visiting-hours`; consume only an existing noncombat resource, or apply a time cost when no consumable exists. **Callback:** “The nurse remembers the drink, not the face you wore while helping.”
- **`ns02-listen` · “Hear the nurse's account. No item reward.”** **Immediate:** “‘Morrow was frightened, and still came back,’ the nurse says. ‘I don't know what that proves.’” Commit `nurse-account`. **Callback:** “You can quote the nurse, but she never claimed to know the whole story.”
- **`ns02-deflect` · “Decline the conversation. Leave the nurse available later.”** **Immediate:** “‘All right,’ she says, and returns to the broken machine.” No evidence or penalty. **Callback:** “The nurse still recognizes you, but lets you pass without a question.”

### NS-03 · The Wrong Emergency Contact · e04

**Art subject:** disconnected switchboard in a deserted, warped waiting room; one phone glows amber, its cord runs beneath a locked door. No depiction of an endangered child.

**Caller:** “This is the number on the card. Someone said you could help.”

**You:** “What kind of help?”

**Caller:** “Directions. A person to answer. Anything certain.”

- **`ns03-answer` · “Give directions without pretending to be the child's parent.”** **Immediate:** “You describe the lit entrance and repeat the address until the caller can say it back. ‘Will you still be there?’” Commit `contact-call` and `promise-made`. **Callback:** At NS-04, “One margin note has today's date: *Someone said they'd stay.*” A later resolution must distinguish kept from broken promise without implying offscreen harm.
- **`ns03-transfer` · “Transfer to a contact you actually met.”** **Gate:** a trusted contact must have a witnessed encounter event, not merely `trustedContact: true`. Locked text: “Meet and speak with a trusted contact first.” **Immediate:** “You repeat the contact's name; the switchboard clicks, and another human voice answers.” Commit `contact-transfer`. **Callback:** “The ledger records a call passed along, not a debt erased.”
- **`ns03-silence` · “Let the call end. Save the number for later.”** **Immediate:** “The ringing stops. You write down the number before the ink on the phone label fades.” Commit `missed-call`; no promise. **Callback:** “The number remains legible, though nobody has called it back.”

### NS-04 · The Ledger of Small Favors · e04

**Art subject:** open paper ledger on a table of keys and mended clothes; two columns of handwriting disagree about who owes whom. No legible invented family names in the image.

**You:** “These are debts?”

**A voice behind the wall:** “Some are. Some are things people did because they could.”

**You:** “And if the wrong person pays them?”

**Voice:** “Then it becomes another debt.”

- **`ns04-copy` · “Copy the names. Leave the original in place.”** **Immediate:** “The paper takes the pressure of your pen; the ledger keeps its history.” Commit `favor-ledger` evidence, no stat increase. **Callback:** “The Chronicle can compare these names with another witnessed account, but cannot declare which person is owed.”
- **`ns04-return` · “Return the ledger to a keeper you personally met.”** **Gate:** witnessed NS-01 attendant or NS-02 nurse encounter **and** a dialogue-established keeper relationship, not just a scene visit. Locked text: “You have not learned who keeps this ledger.” **Immediate:** “The keeper recognizes the binding before your face. ‘I thought it was gone.’” Commit `ledger-returned`. **Callback:** “The ledger's keeper can correct one account without proving the others false.”
- **`ns04-close` · “Close the book. Keep its contents private.”** **Immediate:** “The cover settles over the names. No one has asked you to decide for them.” Commit `ledger-preserved`, no evidence. **Callback:** “The book remains where you left it, and its names remain unclaimed.”

When `promise-made` is witnessed before NS-04, append to **any** NS-04 immediate response: “Beside the phone number, a fresh pencil mark reads: *Still waiting for an answer.*” When NS-04 precedes NS-03, never retroactively rewrite its saved dialogue; only future encounters acknowledge the call.

## State and adversarial acceptance

| Sequence | Expected outcome |
| --- | --- |
| NS-04 first, no e03 scenes | Copy and close available; return visibly locked; e04 route remains completable |
| NS-03 first, no witnessed contact | Answer and silence available; transfer visibly locked |
| Forged `trustedContact` or keeper flag | Locked choices stay locked; witnessed encounter provenance required |
| NS-01 ask twice, suspicion already set | Exactly one suspicion; later dialogue acknowledges existing state |
| NS-02 help with no consumables | Time-cost alternative available; no negative inventory |
| NS-03 answer then NS-04 | Promise callback appears once; no assertion of offscreen harm |
| NS-04 then NS-03 answer | Earlier saved dialogue unchanged; later callback may acknowledge promise |
| All 12 choices individually, save/reload, replay | One immutable choice and receipt per scene, no duplicate reward or cost |
| Two evidence IDs injected without source events | No Chronicle interpretation; distinct witnessed scenes required |
| Original/twisted crossing and return | Event identity persists; no scene may be farmed for repeated reward |

**Production status:** four scene art subjects are specified, but **zero new ArtJobs** are claimed by this packet. Runtime cell binding, reducer integration, executable tests, painted art delivery, and 390/768/1440px rendered acceptance remain open. Do not mark t-025 complete from this writing alone.
