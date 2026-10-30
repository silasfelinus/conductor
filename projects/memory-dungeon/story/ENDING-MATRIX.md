# Ending Room · 32 distinct core outcomes, many lived histories

[Writer's Room](../WRITERS-ROOM.md) · [Act pitches](ACT-PITCHES.md) · [Map plans](MAP-PLANS.md) · [Scene handoff](SCENE-ROOM.md)

**Status:** detailed writer-facing **ending pitch matrix**, not 32 finished, delivered cinematics. Final count requested by Silas: “32 or so endings,” based on pivotal world-pair choices plus a final choice. The data-driven resolver and actual authored playable endings must be tested separately.

## Distinguish five pillars from the rest of the save

The player gets a high-stakes decision after each of the first four original→twisted pairs, followed by an ultimate choice at the end of the four-map convergence. Each adds **one bit** to select a core family, yielding `2^5 = 32`. The choices are not purely good/bad labels.

| Bit | Where | Core ending question | 0 | 1 |
|---|---|---|---|---|
| 0 | e02, Briar | Whose testimony counts? | Protect/seal village | Open to witnesses |
| 1 | e04, Earth | Who paid for the tide gate? | Char survives (with costs) | Char dies saving commuters |
| 2 | e06, Sea | Who controls the twins' account? | Protect private memory | Publish their testimony |
| 3 | e08, Hoshimori | Is shelter a right to leave? | Revocable refuge charter | Open every exit |
| 4 | e12, Last Door | What happens to the worlds? | Separate with safe passages | Negotiate shared crossings |

**Important math:** e04 has *three* actual options: gate open (fatal Char), sealed (commuters trapped), diverted (district destroyed). The two survival histories share the same **core bit** but **different rescue obligations, Char dialogue, scene art and epilogues**. Scylla's separate three-way choice (`run-again/stay/tell-char`), Vesper's earned restitution, Morrow's life, remaining e10/e12 choices, companions, delivered fragments and optional rescues shape the personal ending **without multiplying the 32 headline families**.

The first Briar ending choice is already part of a playable story engine. Do not invent an e02 `pairDecisions` entry for a player who never explicitly made that choice; the adapter must derive or migrate it from earned Briar/Dark Briar decision state. No default should masquerade as a choice. The final resolver should validate all required events before treating a family as earned.

## The 32 core story pitches

The table is a **story-writer assignment board**, not a completed ending string generator. Each row requires a distinct culminating action and a picture-worthy emotional scene written with character knowledge and branch-correct consequences. Combination labels are deliberately explicit so nobody accidentally writes two identical endings.

| Family | Saved moral history (5 pillars) | Distinct dramatic direction |
|---|---|---|
| 00 | Briar closes its gates; Char survived the tide gate; twins' memories private; Hoshimori refuge charter; separate but protected worlds | The worlds pull apart; gated villagers keep a right to send help while the stranded workers remains part of the account. |
| 01 | Briar welcomes witnesses; Char survived the tide gate; twins' memories private; Hoshimori refuge charter; separate but protected worlds | The worlds pull apart; forest witnesses keep a right to send help while the stranded workers remains part of the account. |
| 02 | Briar closes its gates; Char lost at the tide gate; twins' memories private; Hoshimori refuge charter; separate but protected worlds | The worlds pull apart; gated villagers keep a right to send help while Char's death remains part of the account. |
| 03 | Briar welcomes witnesses; Char lost at the tide gate; twins' memories private; Hoshimori refuge charter; separate but protected worlds | The worlds pull apart; forest witnesses keep a right to send help while Char's death remains part of the account. |
| 04 | Briar closes its gates; Char survived the tide gate; twins' account public; Hoshimori refuge charter; separate but protected worlds | The worlds pull apart; gated villagers keep a right to send help while the stranded workers remains part of the account. |
| 05 | Briar welcomes witnesses; Char survived the tide gate; twins' account public; Hoshimori refuge charter; separate but protected worlds | The worlds pull apart; forest witnesses keep a right to send help while the stranded workers remains part of the account. |
| 06 | Briar closes its gates; Char lost at the tide gate; twins' account public; Hoshimori refuge charter; separate but protected worlds | The worlds pull apart; gated villagers keep a right to send help while Char's death remains part of the account. |
| 07 | Briar welcomes witnesses; Char lost at the tide gate; twins' account public; Hoshimori refuge charter; separate but protected worlds | The worlds pull apart; forest witnesses keep a right to send help while Char's death remains part of the account. |
| 08 | Briar closes its gates; Char survived the tide gate; twins' memories private; Hoshimori roads opened; separate but protected worlds | The worlds pull apart; gated villagers keep a right to send help while the stranded workers remains part of the account. |
| 09 | Briar welcomes witnesses; Char survived the tide gate; twins' memories private; Hoshimori roads opened; separate but protected worlds | The worlds pull apart; forest witnesses keep a right to send help while the stranded workers remains part of the account. |
| 10 | Briar closes its gates; Char lost at the tide gate; twins' memories private; Hoshimori roads opened; separate but protected worlds | The worlds pull apart; gated villagers keep a right to send help while Char's death remains part of the account. |
| 11 | Briar welcomes witnesses; Char lost at the tide gate; twins' memories private; Hoshimori roads opened; separate but protected worlds | The worlds pull apart; forest witnesses keep a right to send help while Char's death remains part of the account. |
| 12 | Briar closes its gates; Char survived the tide gate; twins' account public; Hoshimori roads opened; separate but protected worlds | The worlds pull apart; gated villagers keep a right to send help while the stranded workers remains part of the account. |
| 13 | Briar welcomes witnesses; Char survived the tide gate; twins' account public; Hoshimori roads opened; separate but protected worlds | The worlds pull apart; forest witnesses keep a right to send help while the stranded workers remains part of the account. |
| 14 | Briar closes its gates; Char lost at the tide gate; twins' account public; Hoshimori roads opened; separate but protected worlds | The worlds pull apart; gated villagers keep a right to send help while Char's death remains part of the account. |
| 15 | Briar welcomes witnesses; Char lost at the tide gate; twins' account public; Hoshimori roads opened; separate but protected worlds | The worlds pull apart; forest witnesses keep a right to send help while Char's death remains part of the account. |
| 16 | Briar closes its gates; Char survived the tide gate; twins' memories private; Hoshimori refuge charter; negotiated crossings | A protected refuge links the surviving worlds under protected private memory; the cost of the survived crossing cannot be erased. |
| 17 | Briar welcomes witnesses; Char survived the tide gate; twins' memories private; Hoshimori refuge charter; negotiated crossings | A protected refuge links the surviving worlds under protected private memory; the cost of the survived crossing cannot be erased. |
| 18 | Briar closes its gates; Char lost at the tide gate; twins' memories private; Hoshimori refuge charter; negotiated crossings | A protected refuge links the surviving worlds under protected private memory; the cost of the fatal crossing cannot be erased. |
| 19 | Briar welcomes witnesses; Char lost at the tide gate; twins' memories private; Hoshimori refuge charter; negotiated crossings | A protected refuge links the surviving worlds under protected private memory; the cost of the fatal crossing cannot be erased. |
| 20 | Briar closes its gates; Char survived the tide gate; twins' account public; Hoshimori refuge charter; negotiated crossings | A protected refuge links the surviving worlds under open witness law; the cost of the survived crossing cannot be erased. |
| 21 | Briar welcomes witnesses; Char survived the tide gate; twins' account public; Hoshimori refuge charter; negotiated crossings | A protected refuge links the surviving worlds under open witness law; the cost of the survived crossing cannot be erased. |
| 22 | Briar closes its gates; Char lost at the tide gate; twins' account public; Hoshimori refuge charter; negotiated crossings | A protected refuge links the surviving worlds under open witness law; the cost of the fatal crossing cannot be erased. |
| 23 | Briar welcomes witnesses; Char lost at the tide gate; twins' account public; Hoshimori refuge charter; negotiated crossings | A protected refuge links the surviving worlds under open witness law; the cost of the fatal crossing cannot be erased. |
| 24 | Briar closes its gates; Char survived the tide gate; twins' memories private; Hoshimori roads opened; negotiated crossings | A freely chosen road links the surviving worlds under protected private memory; the cost of the survived crossing cannot be erased. |
| 25 | Briar welcomes witnesses; Char survived the tide gate; twins' memories private; Hoshimori roads opened; negotiated crossings | A freely chosen road links the surviving worlds under protected private memory; the cost of the survived crossing cannot be erased. |
| 26 | Briar closes its gates; Char lost at the tide gate; twins' memories private; Hoshimori roads opened; negotiated crossings | A freely chosen road links the surviving worlds under protected private memory; the cost of the fatal crossing cannot be erased. |
| 27 | Briar welcomes witnesses; Char lost at the tide gate; twins' memories private; Hoshimori roads opened; negotiated crossings | A freely chosen road links the surviving worlds under protected private memory; the cost of the fatal crossing cannot be erased. |
| 28 | Briar closes its gates; Char survived the tide gate; twins' account public; Hoshimori roads opened; negotiated crossings | A freely chosen road links the surviving worlds under open witness law; the cost of the survived crossing cannot be erased. |
| 29 | Briar welcomes witnesses; Char survived the tide gate; twins' account public; Hoshimori roads opened; negotiated crossings | A freely chosen road links the surviving worlds under open witness law; the cost of the survived crossing cannot be erased. |
| 30 | Briar closes its gates; Char lost at the tide gate; twins' account public; Hoshimori roads opened; negotiated crossings | A freely chosen road links the surviving worlds under open witness law; the cost of the fatal crossing cannot be erased. |
| 31 | Briar welcomes witnesses; Char lost at the tide gate; twins' account public; Hoshimori roads opened; negotiated crossings | A freely chosen road links the surviving worlds under open witness law; the cost of the fatal crossing cannot be erased. |

## What every ending must deliver

- **A different final action or answer,** not just a different adjective in a generic “the world was saved” epilogue. The forest witnesses, harmed citizens, twins and protected Hoshimori households must all have a plausible voice.
- **Char continuity:** On fatal e04 histories, the player witnessed Char's death. The Char controlled in e11 must have an explicit time/history identity. “Char lived” without that explanation is an invalid ending. On surviving histories, use the specific cost: stranded commuters or the devastated district.
- **Morrow and the original researcher:** Neither has a free claim to the other's body, and Morrow's Earth family cannot be treated as collateral with no say.
- **Vesper:** The rescue and betrayal both remain true; the final atlas or charter cannot undo people harmed by the duplicate map. Pip has his own ledger and Oven outcomes.
- **Eight displaced map fragments** must be earned or repaired by fair alternate quests before e12 is resolved; no menu bypass should select a finished ending.
- **32 unique core illustrations / finale beats** are a production target, not a delivered-art claim; extra conditional portraits, reactions and epilogue cards may be needed.
- **Tests:** verify 32 unique core keys, all three e04 choices, all three Scylla choices, lost/surviving Char without contradiction, save migration, no forged fragments, and two final choices. Player-facing UI must not show a numerical catalogue of endings ahead of discovery.

## Editorial assignment strategy

Author four initial exemplar endings first: (1) witnessed Char death + shared crossings, (2) witnessed death + separated worlds, (3) Char survival with stranded evacuees + shared crossings, (4) Char survival with district damage + separated worlds. Once those are genuinely different in location, voices and consequences, write the remaining 28 according to the five-axis matrix. The production count advances only for authored, QA-accepted sequences with clear saved-state predicates and real art receipt status.

[Archive of prior, now-superseded sixteen-world finale assumptions](../archive/roadmap-2026-10-30-pre-12-world-slim.yaml)
