# Shifting Desks: Review Memory and Final Board Audit
*2026-10-21 PT · t-037 · narrative quality pass III*

## Found and corrected: review menus were already full

The existing Form 0 and Toy Division review screens each have seven authorized choices, which is also the upper bound asserted by `tests/test_shifting_desks_encounters.py`. Adding more choices would defeat the compact, one-screen decision interface and crowd out readable artwork. The initial proposal added four new review routes; CI caught the limit. Those routes were withdrawn in both canonical and runtime content. **No existing review choices, outcomes, authored art, or dice rules were removed.**

## What actually changed

The Kind Robots rules and desk now present a small, **personalized Case-file Exhibits** section above the existing choice list at relevant mandatory reviews, visible on mobile as well as desktop. The exhibits are deterministic, solely read the run's flags, and are capped at two at a time so the artwork and decision controls remain prominent.

**Records & Forms may remember:**
- Pip learning that no is a complete answer, rather than his personhood being filed as an unpaid extra
- The surface-tube parking stub marked WE READ, proof the Company's internal paperwork isn't the whole world
- The unauthorized group petition created by Kevin's get-well card
- Your original Buddy report that sent Pip to the Special Assignment Office

**Toy Division may remember:**
- A dented robot's minority objection to the ticking and the Company's eleven unanimous yes votes
- The parents who received a dated product-safety warning identifying next Thursday's incident
- The warning attached to the launch memo about the parking structure
- Whether the player's focus-group crayon drawing exposed the mechanism in the bear before the launch review

The current choices still let the player decide *how* to handle the review; the evidence tells the player **what the Company knows**. The Board need not reveal the scoring key to produce a recognizable record of decisions.

## Final Board endings

The existing ten ending families gained **18 new flag-keyed case-file paragraphs**, focused on obedience, complicity, safety warnings, the surface exit, minority dissent, Pip, Kevin, the Supervisor and consequences that cannot be erased with a stamp. Every flag now refers to an act the player can actually perform in a regular encounter or mandatory review. The Board's dialogue and final Sub-Level Zero encounter source were not edited to avoid overlap with t-034.

These are *conditional epilogue acknowledgements*, not new Board options and not guaranteed on every run. `endingLines` already displays all relevant earned passages and remains deterministic.

## Verification

- Retained the seven-choice limit, and added regression coverage for it.
- Added deterministic `reviewExhibits` tests: prior records produce the correct two-line maximum; irrelevant departments produce none.
- Confirmed a visible desk binding, without a second game state or API.
- Regenerated the canonical flag provenance from all five encounter packs, societies and endings: **514 granted flags; 244 without later readers**. The latter include intentional archival receipts, not 244 confirmed defects.
- Required merge gates: Conductor full Python suite/pack validator/security checks, Kind Robots Shifting Desks gameplay, TypeScript, Prettier and full contract CI. Code merge and Alexandria deployment are separate statuses.

## Remaining scope

The 120-card deck still warrants scene-by-scene editorial playtesting of compliant, opportunistic and compassionate runs, particularly at the Wellness/Board transition and the actual mobile viewport. Keep separate t-034 (Wellness/Sub-Level Zero tone text) and art t-032 claims intact. No art prompts were submitted in this pass.
