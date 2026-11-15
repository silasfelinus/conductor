# Memory Dungeon: Earth-pair non-stat unlock economy (e03/e04)

Status: authored implementation contract, **not yet wired into the game**. Scope is the Morrow Earth original/twisted pair only. This packet contributes to t-029; it does not claim the full economy, art, or playtest acceptance.

## Economy invariants

1. Rewards are earned from witnessed outcomes, never merely from visiting a coordinate or possessing an unverified saved flag. Every reward has a stable ID and an independently verifiable source event.
2. A reward is granted at most once per Chronicle, including after save restoration, replay, returning through the mirrored world, or repeating a dialogue.
3. Permanent unlocks alter available **choices, information, or encounter composition**, not starting health, damage, currency, card-match odds, or extra turns. No purchase, grind, or hidden stat inflation.
4. The original and twisted versions of a source event share one reward identity when they represent the same moral decision. Mutually exclusive outcomes never yield both rewards in one run.
5. Unlock descriptions must be self-contained at every tier. Their UI must explain the changed decision before the player commits.
6. Every unlock can be declined or disabled at expedition setup without losing Chronicle discovery; an unlock may never trap a player or bypass an earned exit.

## Six paired unlock decisions

| ID | Earned source (must be witnessed) | Permanent unlock | Cost or counterweight | Rejection / forged-state rule |
| --- | --- | --- | --- | --- |
| `earth-second-platform` | Return the last-train passenger's ticket without taking their name | **Second Platform:** once per Earth expedition, reveal which of two station doors returns to the known map | The revealed door does not disclose its encounter contents | An unvisited station or restored ticket-only inventory grants nothing |
| `earth-unclaimed-letter` | Deliver the letter while preserving the absent recipient's right not to answer | **Unclaimed Letter:** optional third response on one courier scene: leave a message without demanding repayment | Forgoes the immediate courier trinket | A letter merely carried, discarded, or forged as delivered grants nothing |
| `earth-honest-inventory` | Record an actual missing object instead of replacing it with a comforting false count | **Honest Inventory:** preview one *category* of the next treasure pile (tool, charm, key), not its exact contents | Preview consumes the expedition's single inventory consultation | Repeated dialogue or altered save flags cannot duplicate the consultation |
| `earth-last-light` | Leave a functioning lamp for the person arriving after the protagonist | **Last Light:** open a noncombat detour in one dark corridor | Detour costs an exploration action and may contain no treasure | Simply lighting the lamp for oneself is not sufficient |
| `earth-borrowed-name` | Refuse to use a borrowed identity to cross a guarded threshold | **Borrowed Name:** request a nonviolent identity challenge at one checkpoint | Challenge can fail and returns to the normal route, never an automatic bypass | Both identity theft and refusal cannot be earned from the same decision ledger |
| `earth-two-witnesses` | Reconcile original and twisted accounts with two independently met witnesses | **Two Witnesses:** compare two contradictory quest clues side by side in the Chronicle | Comparison reveals disagreement, not which account is true | Visiting only one reality or injecting the other witness ID cannot unlock it |

## Deterministic acceptance matrix

For each of the six IDs, test all of the following in both e03 and e04 entry order: (1) genuine witnessed success, (2) alternate choice, (3) direct source flag forgery, (4) inventory-only forgery, (5) save/reload before resolution, (6) save/reload after resolution, (7) dialogue repeated three times, (8) reverse reality traversal, (9) two independent expeditions sharing a Chronicle, (10) a fresh Chronicle with an identical expedition seed. This is **120 scenario classes**, before seed expansion.

Assert: no more than one Chronicle award per ID; no reward on any forged or alternate path; stable restoration of a spent per-expedition consultation; no change to HP, damage, match odds, or base currency; no inaccessible mandatory route; every newly exposed option has a complete accessible label and art-shaped fallback. For a deterministic seed suite, use at least 32 seeds per entry order and include a saved mid-encounter checkpoint.

## Implementation handoff

Bind these IDs to the existing witnessed-consequence reducer, not a second independent inventory boolean. Add explicit `earned` predicates that verify source choice, encounter completion, and visited reality together; derive Chronicle unlocks from those predicates. Keep the six expedition-use counters in versioned current-save state. Wire descriptions through the existing choice-hand component and test actual button reachability at 390, 768 and 1440px. Production art should be queued only after choice IDs and visual subjects are accepted, with durable ArtJob receipts and verified delivered URLs.

**Remaining:** none of these six entries is claimed implemented, tested, integrated, or art-complete by this document. The 12-world economy, enemies, items, achievements, unlock catalogs, and end-to-end balance remain open.
