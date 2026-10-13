# shifting-desks CHANGELOG

## 2026-10-12 PT
- Project scaffolded via intake.py (Silas-directed).
- DESIGN-BRIEF.md: best-of-both from Zuzu Shifting Lands + Zuzu Gamebook, the no-clean-wins rule, five meters, Rules v1, Successors, Society and Mutation cards, recommended world, art, tone and IP guardrails.
- PITCHES.md: seven directions (A-G), six expansions, a recommended synthesis and title options for Silas (soft gate t-002).
- encounters/: pack schema, validate_pack.py (CI via tests/test_shifting_desks_encounters.py), ORIENTATION-12.json (12 cards + the 90-Day Review boss).

## 2026-10-12 PT (later)
- Silas decided t-002: the synthesis fused with the vault test facility; lead flavors secret societies & traitors and paperwork & psych tests; party mode rejected; title left as working title.
- DESIGN-BRIEF "Decided world" (campus atop a sealed test vault, five levels down, hidden Test Results), PITCHES "Decision", CONTROL.md updated.
- Validator: `paperwork` tag and a lead-flavor quota (at least half of each pack). New task t-022 (hidden Test Results); t-021 now pitches only the afterlife expansion.

## 2026-10-13 PT
- t-010: encounters/RECORDS-12.json, Department 2 (Records & Forms): Pneumatic Tube Exchange, The Sub-Archive and Window 9, 4 cards each (4 good / 4 bad / 4 mixed, 11 of 12 lead-tagged), and the boss *The Form That Requires Itself* with five routes, five department outcomes and the `refiled` fallback. Nine choices pay off Orientation flags (forged-dale, halvorsen-envelope, stapler-front-contact, has-master-key, knows-the-ducts, roach-union-ally/member, pip-trusts-you, wearing-a-dead-mans-badge).
- validate_pack.py: a `requires.flag` may be granted by the same pack or any pack with a lower `department.order`.
- DECKS.json: every society has `records` objectives and betrayals keyed to flags RECORDS-12 grants. WORLD-BIBLE callback ledger updated with the Records callbacks.
