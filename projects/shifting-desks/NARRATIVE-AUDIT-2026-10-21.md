# Shifting Desks: Narrative Coherence Audit
*2026-10-21 PT · t-035 · first full-inventory assessment and scoped repair pass*

## What was actually inspected

The canonical, current five department packs comprise **120 encounter cards**, eight cards in each of three locations per department, plus five distinct boss reviews. Encounter choices total **412 before this pass**: Orientation 79, Records 96, Toy Division 78, Wellness 76, Sub-Level Zero 83. Four window shifts and ten ending families with authored flag-gated epilogue variants were also inventoried. The per-run design draws one of eight cards at each location, so an existing flag's callback can be correctly authored and still never appear during an individual run.

The initial FLAG-MAP contained **498 distinct flags**, **268 without an explicit later reader**. This is a *candidate list*, not 268 confirmed defects. Several flags are valid one-scene receipts or late-game outcomes. But a flag recorded for a major sacrifice, a recurring relationship, or an explicit future promise warrants a callback or a deliberate explanation of why it stays archival. An isolated modifier and a line saying the player was noticed are not automatically a meaningful narrative payoff.

This is an inventory-based editorial assessment, not a claim that every success/failure sentence across all 120 cards has now received an equally deep human playtest. The implementation below is one coherent slice of that larger standard.

## Findings by department

| Floor | Cards | Choices before | Concrete strength | Most useful follow-up |
| --- | ---: | ---: | --- | --- |
| Orientation | 24 | 79 | Gus, the duplicate guard, the inkblot and the office-supply test establish bureaucratic dread without explaining every mystery | Let early classification, Pip-as-inventory, PAL Buddy report and the safety-film conditioning recur as actual institutions rather than optional flavor |
| Records & Forms | 24 | 96 | Window 9, Beverly, Pemberton, future capsules and stamp quotas create dilemmas with recognizable victims | The up-tube, suggestion system and permanent-file decisions each create strong records but rarely get answered by later floors; follow their surviving flags into late encounters or ending variants |
| Toy Division | 24 | 78 | The nursery, union inspection, dissenting robot and launch review blend humor, collateral harm and living products | Fix prompts that omit an action's setup, then let apparently trivial earlier tests pay off in specific toys and later judgments |
| Wellness & Testing | 24 | 76 | Role-reversal exams, memory subtraction and the kindness of Halvorsen's silence make poor rolls interesting | PAL's monitoring, Pip's classification and several human relationships still have no direct reader. Coordinate with t-034's separate tone-ladder revision before editing these cards |
| Sub-Level Zero | 24 | 83 | The Founder, backup tapes, Successor room and Board expose who benefits from earlier choices | Four-card late-game choices like PAL's review and Item Four record vivid flags without a corresponding epilogue reader. Prioritize specific moral debts in ending callbacks |

## Reproducible narrative contract misses fixed in this slice

1. **Questionnaire for a Five-Year-Old**: The text previously numbered three questions; a third route depended on a *fourth* drawing box never disclosed. The setup now names the box, the availability of crayons and the promised consequence of writing someone's name. The seemingly kind answer of naming colleagues thus has an explicit human cost, not a surprise disconnected from the player's understanding.
2. **Rate Their Sincerity**: The test names a young subject `TYLER, 7`, then a later choice unexpectedly calls him `B`. The setup now exposes his Successor ID in the small print before the player judges his worth. The mystery remains who put him here and why PAL takes sincerity scores so seriously.
3. **Writing the Warning Label**: The earlier focus-group sketch, previously granted as `drew-the-warning` with no reader, unlocks an authored fourth action here. A successful attempt publicizes the actual dangerous mechanism; a failure turns the warning drawing into advertising. Both answers arise from the player's chosen attempt.
4. **Confidante Prototype**: An earlier Buddy wellbeing report about PAL, previously just a colorful flag, returns as a conditional dialogue with a memory-leaking doll. The positive result makes PAL register unsolicited kindness; the negative result has its privacy fail in a plausible way.
5. **Range Safety Quiz**: The safety-film jingle from Orientation, previously never read again, is now audible here. An employee conditioned by that film may intentionally sing a wrong note, causing a specific scripted disruption; a failed skill check reproduces the conditioning instead.

These five repaired scenes retain their original cards, locations and art prompts. Three new routes remain within the **2–4 choices per encounter** contract. No runtime LLM or unseeded narrative generation is introduced.

## Ending echo audit

Six new epilogue lines acknowledge distinct earlier acts: whether a warning reached parents, a safety jingle was broken, PAL received unrequested kindness, Pip was counted as inventory, Pip was reported to the Company by his Buddy, and Successor B was condemned by his own double. Each is a **variant**, not a guaranteed alternative ending; a player must reach the relevant ending with the matching flag. That is honest about the branching graph and keeps outcomes from becoming a combinatorial explosion.

## Remaining editorial queue, prioritized

**P1, next small pass:** The Records up-tube, future suggestion trail, and Pip's Window 10 review, with at least one read per consequential flag where the story explicitly promises a future meeting. Check reachable gated options and both roll outcomes. Preserve the three-stage floor pacing.

**P1, after t-034's tone pass:** Wellness Halvorsen outcomes and the final Board's treatment of PAL, where named relationship flags ought to affect the institution's final interpretation. Avoid parallel writes to the same Wellness and Sub-Level packs.

**P2:** Stronger ending coverage for the Toy Division's dissenting robots, real warning-label risks, Beverly's denied application, and Marguerite's smuggling promises, with moral rather than mechanical emphasis. Some scenes deliberately end in a sealed file; that is fine when the silence itself has meaning.

**P2, validation:** Seeded adversarial runs that choose very different grade profiles and test success/failure for each new route, a flag-reader audit that distinguishes deliberate one-scene receipts from broken foreshadowing, and viewport verification at 390/768/1440. Re-run the balance report when any probability/effect changes. Image prompts and delivered art stay unchanged for this pass.

## Acceptance and limitations

A card passes narrative review when its setup tells the player enough to understand its options, each result is causally tied to the attempted action, the failure is interesting rather than a dead end, and important promises recur or are intentionally unresolved. A hidden rule is permitted; a hidden omitted option is not.

The current t-035 implementation provides this inventory assessment, five concrete scene repairs, three earlier-choice callbacks and six more ending echoes, with canonical and Kind Robots tests. It **does not declare the entire deck finished**, claim live deployment, claim new render delivery, or replace Silas's creative verdict.
