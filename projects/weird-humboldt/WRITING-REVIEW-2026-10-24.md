# Writing review: t-003 deck, anchors, endings, archetypes (2026-10-24 PT)

Mechanical pass over 121 cards, 6 anchors, 12 endings and 8 archetypes (agent review, not a substitute for the t-004 human creative review).

## Findings
- **Structure**: all 121 cards have exactly 3 options; `validate_weird_humboldt_cards.py` passes (121 cards, 7 with four-state lenses).
- **Variety**: lead tones are eerie 20, whimsical 9, funny 9, dry 8, warm 7, absurd 7, satirical 4. Skills: rizz 89, wits 86, psyche 28, local_lore 23, burly 19, plus 118 no-roll options. Psyche/lore/burly are the thin lanes; favour them in future checks.
- **Repetition**: no 6-word phrase is shared by more than two scenes; scene openers are almost all unique ("A hollow redwood", "On a porch", "A kinetic sculpture" appear twice each). Locations are spread (max 6 cards per place).
- **Exclusion scan**: no Tuluwat, Indian Island or massacre terms anywhere. Anchors, endings and archetypes carry only exclusion-comment mentions of Wiyot; the archetype "Tribal Community Organizer" names no tribe.

## Flag for Silas (owner decision needed)
**WH-121 "The Latitude Argument"** (`cards/ch2.yaml`) is the 1849 Mad River card. `EXCLUDED-CONTENT-2026-10-22.md` lists "the held 1849/Mad River/Wiyot expedition roleplay WH-121" as dropped. The authored card is a rewrite: a single-source Gregg-party anecdote with fog and sextant jokes. But its provenance and canon still name the Wiyot language (Baduwa't) and say it is "not a Wiyot-reviewed account", and the scene sign repeats the Baduwa't name. Decide: keep the rewrite as-is, strip the Wiyot naming, or remove the card. Removing it changes the validator and test count from 121 to 120. No change was made here.

## Follow-up (2026-10-24 PT)
WH-121 no longer names the Wiyot language or Baduwa't anywhere (provenance, canon, scene sign); it stays a fictionalized single-source surveyor anecdote, consistent with the owner's no-Wiyot-content direction. Validator passes at 121 cards. Removing the card entirely remains Silas's call.
