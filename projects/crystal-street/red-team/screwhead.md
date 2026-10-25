# screwhead.json red-team

Validator: `checkCrystalStreetFile.ts villains` passes on the edited copy.

## Fixes made (exact-string, effects/ids untouched)

1. **Blocking** - Real trademark "7-Eleven" used as an in-world store 3x (Aisle Nine card text, sprint success, knock-the-paint success). Changed to the established parody "Quik-Stop" (already used in characters.json).
2. **Blocking** - Real song lyric quoted: "You put your left foot in" (The Hokey Pokey) in the Clockwise Forever hokey-pokey success and failure. Rewrote as dance calls ("Left foot in!") and "how the song ends" -> "how the dance ends". The title mention ("half Hokey Pokey") stays, which is fine.
3. **Polish** - Real trademark "Walkmans" in the Best ending repair list -> "tape players".
4. **Polish** - Finale edge-3 success copied the heart success almost word for word (sign/ledger/letter, "He forgave all of them", the promise/cage line, the aisle-to-aisle ending). Rewrote the second half so the edge path has its own beat: you loosen the first screw with her consent, she takes out the next one herself, and she waits for each neighbor's answer. The consent theme stays and the opening line still calls back to the night before.
5. **Polish** - Ledger clue: "crossed out every single debt in his own: FORGIVEN" -> "in his own hand".
6. **Polish** - Letter clue: "You read it, and you're sorry, Magda." spoke to Magda directly in the middle of a second-person card. Now "it feels like opening somebody else's mail."
7. **Polish** - The Leveling, loosen-the-chains success: broken construction "every neighbor who manages a yes, their chain goes slack" -> "for every neighbor who manages a yes, the chain goes slack".

## Checked, no change needed
- The cast table's Magda "Screwhead" Szabo flip is consistent. The timeline holds: arrived at age 6 in 1956, so 36 in 1986; first key cut in 1964; Laszlo died June 1985; box bought October 1985.
- Leather/kink handled well: the Velvet Hammers' own chains are respected ("Ours we picked") and the consent theme is consistent. No queer-coded menace. The Abernathy-Coles are a married gay couple shown with joy.
- PG-13 holds: bad outcomes are frozen, chained or Taken (the bad ending), with no gore. Every clue choice grants its clue, and the three clues (sign, ledger, letter) explain control-as-grief and are exactly what the heart choice uses.
- Effects: at most one skill per encounter. hold-it-shut failure gives dread +2, slightly above scale, but it is act 3, so I left it.

## For Silas (not changed)
- **Period product names as scenery**: "a crushed Pinto" (clue 1) and "Allen key" (Some Assembly Required). Across the content, Camaro (~48 uses), Walkman (~23) and Cadillac are used the same way. Recommendation: decide once, for the whole codebase, whether car models and genericized names are allowed as scenery. If not, run one sweep rather than fixing file by file.
- Bittersweet line "never laugh at the same jokes twice" reads oddly (it may mean they never laugh at all now). Optional rewording.
- Cross-file: final-cut.json has "old Mr. Abernathy from the hardware store", while here the Abernathy-Coles are a Crystal Street couple and the town's hardware store was Szabo & Daughter, now closed. Recommend renaming the final-cut character or his job.
