# frieda-krueger.json red-team

Validated: `checkCrystalStreetFile.ts villains` -> 1 villains OK.

## Fixes (in redteam/frieda-krueger.json)
- BLOCKING - Cast/date contradiction: Glory (44 in 1986, born ~1942) says Frieda cut her hair "when I was nine" (1951, before the 1959 suburb and the 1961 salon). Changed to "when I was seventeen" (fits the 1959-61 salon, the cast note "first real haircut from Frieda", and the "kid in a tiara" snapshot).
- BLOCKING - Real trademark as in-world product: "Polaroids" (wig-room text, album snap success). Changed to "snapshots" / "instant photos" (item is named "Instant Camera").
- POLISH - The Gray Street failure: text said "your favorite jacket is gray" but the effect is `loseItems: ["leg-warmers"]`. Text now says your leg warmers have faded to dust; poster line kept.
- POLISH - "Grandma Pearl's porch light" could read as Pearl being the player's grandmother (implying the player's family/race). Changed to "Pearl Washington's porch light".
- POLISH - Art for "make her admit it" failure contained a comic-style direction ("a single scream line drawn in the air"). Removed that clause.

## Checked, no change
- Clue trio (eviction article, portfolio, Whitlock confession) explains the rumor and feeds the heart choice. Taken/PG-13 fine. One +1 skill per encounter. Edge failures all -2.
- "who kissed who" left as voice.

## Silas calls
- None specific to this file. Known open flags (Glory song, Chip, Shape, Goody Hale) do not appear here.
