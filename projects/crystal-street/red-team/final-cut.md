# final-cut.json red-team

Validator: `checkCrystalStreetFile.ts villains` passes on the edited copy.

## Fixes made
1. **Polish (contradiction)** - Finale text: "Celeste Navarro is standing exactly where she sat in 1980". In the backstory the 1980 premiere was at the Starlight Drive-In ("Celeste sat three cars away"), not in row F of the Glitter Box. Now "in the aisle by row F, Celeste Navarro has stayed for the midnight show after all", which also pays off the clue hint that she has stopped staying for midnight shows.
2. **Polish (contradiction)** - Call-sheet clue, ask-zelda success: "The movie on the tape has no Nurse Robin in it at all". The backstory and B.K.'s note ("Make the nurse the twist") say Robin is in the cut, as the fake killer reveal. Now "In the movie on the tape, Nurse Robin never leads anyone out of the woods."
3. **Polish (art)** - Finale fight failure art "A teenager rendered in flickering black-and-white film grain": "rendered" reads as a style word to the image model. Changed to "made of".

## Checked, no change needed
- The hard line holds: the "man in a dress" reveal is clearly the villain's lie (B.K.'s note is confronted by Len's "This is wrong and I know it"). "A dress is just a dress" is stated outright. Celeste (trans) and Len (closeted) are heroes. The kill-order targets (Ricky, Denise and Lorna, the Black friend in the script) all live and get joy beats. No slurs.
- **Known flag: Glory's "I Am What I Am"**: title only, no lyrics quoted. Compliant, so no change.
- Clue trio (call sheet billed as LEAD, draft three with Celeste's dawn line, trims reel) explains "the twist was a lie" and is exactly what the heart choice screens.
- PG-13: knives exist only as a box-cover shadow and a rubber prop on a rack, never in a teen's hand. Bad ending is Taken (trapped in reel two).
- Parody brands in use: Gas-N-Go, Bolt Cola, Choco-Nuggets.

## For Silas (not changed)
- **Camaro** (Lovers' Lane: card text, 4 outcome texts and most of its art, 13 uses in this file). It is a real trademark used as an in-world car. It is part of a codebase-wide pattern (varsity-beast, prudence-thorn, locations.json, and others). Recommendation: one decision and one sweep across the codebase (for example a parody "Comet SS" or a plain "cherry-red muscle car"), not a one-file fix.
- Cross-file: "old Mr. Abernathy from the hardware store" (Gas-N-Go card) clashes with screwhead.json, where the Abernathy-Coles are a Crystal Street couple and the hardware store (Szabo & Daughter) is closed. Recommend another surname or job, for example "from the bait shop".
- Minor: the three box-office clue paths put the same film can in three places (coat closet, behind the rewind bench, handed over at closing). Each path is separate, so this is harmless.
- The "Row F" encounter title has no payoff beyond the finale and the edge-1 line. Fine as flavor.
