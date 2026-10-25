# mister-fuzzbutton.json red-team

Validated: `checkCrystalStreetFile.ts villains` -> 1 villains OK.

## Fixes (in redteam/mister-fuzzbutton.json)
- BLOCKING - Real trademark: choice label "Snap a Polaroid every time you look away". Changed to "an instant photo".
- BLOCKING - Real trademark: "A clattering wall of Huffys". Changed to "BMX bikes".
- POLISH - Contradiction: the backstory has Ollie alone "until eleven at night", but Kev says "His dad works till midnight." Changed Kev's line to "works till eleven".

## Checked, no change
- Ages and dates hold: 8th birthday January 1985, 9th birthday party January 18, 1986, banner "still up after nine months", third grade.
- Clue trio (Ollie's tape and Gary, the kid in the window, 22 unmailed invitations) explains "left alone with a toy" and leads straight to the heart choice.
- Bowie, Cyndi and The Cure are named only, with no lyrics. "Duncan Heinz" and "Wondertoy" are parodies. All edge failures are -2.

## Silas calls (not changed)
- KNOWN FLAG, "Secrets on the Request Line" (Act II): a bear threatens to air "a secret about Chip Merriweather ... in his own voice". Read with Chip's closeted arc, this is a threatened on-air outing. Mitigations already in the card: the kind choice says "it isn't the bear's to tell", the failure sends out only dead air, and no secret is ever stated. Remaining risk: on failure, Chip goes silent ("it rings and rings"), so his pain is used as the stakes. Recommendation: (a) switch the target to a non-orientation secret, or a different character, or (b) keep Chip but have the failure end with Chip calling back angry at the bear, not wounded by an outing, and let his coming out happen only on his own terms in his companion arc.
- Corpus note: Walkman and Polaroid also show up in other villain files (prudence-thorn, countess-lacroix, queen-neferet, screwhead, the-shape, varsity-beast) and in decks.json and items.json. I suggest a corpus-wide sweep.
