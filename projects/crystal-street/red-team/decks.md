# decks.json red-team

Validated: `checkCrystalStreetFile.ts decks` -> 8 decks OK (before and after edits).

## Fixes (in redteam/decks.json), 0 blocking / 10 polish (18 string edits)
- POLISH, cross-file contradiction: the babysitter card placed "The Delgado house, 9 Crystal Street", but companions.json puts Dr. Haddad's garage clinic at number 9. Changed to "The Delgado house on Crystal Street" (the-shape.json also uses the Delgado house with no number).
- POLISH, voice and player identity: the babysitter run-to-pearls success called Pearl "Grandma Pearl", which could read as the player's own grandmother and so imply the player's race and family. Changed to "Mrs. Washington", which matches companions.json.
- POLISH, contradiction: the watch meeting has "I nominate the president, for her service", but the HOA president is Chip's father, Mr. Merriweather (companions.json). Changed to "his service".
- POLISH, brands (real trademarks used as in-world products):
  - "Polaroid" in text and art, twice. Now "instant photo", matching items.json's "Instant Camera".
  - "Walkman", twice in the Side B card. Now "tape player".
  - "Frisbee(s)", in two text spots and one art spot. Now "flying disc(s)".
  - "the color of a Creamsicle". Now "the color of orange sherbet".
- POLISH, text/effect mismatch: the rink kill-the-music success said you "find three quarters" but the effect grants 1. Text and art now show one quarter.
- POLISH, text/effect mismatch: the garage-clinic tarp success said "three dollars in quarters" (12) but the effect grants 2. Now "two quarters".
- POLISH, factual: the porch-light success had a "1944 silver dollar", but no US silver dollars were minted from 1936 to 1970. Text and art now say "1944 silver half-dollar".

## Checked, no change
- Every named NPC fits the cast table and the companion file. Companion cameos (Pearl, Mix, Frankie, Glory, Amir "A.H.") are in character. Neighbor families are consistent: the Lindqvists are Bea's family, the Kowalskis are Moose's, plus the Fergusons, Delgados, Mrs. Feeney and Halvorsen's patch. Every bonus companion id is valid.
- No villain contradicts the cast or the world. The 1959 suburb, the quarry lake, the KGLM water tower, Channel 9 walkies and the 1979 softball cup are all consistent.
- No lyrics are quoted ("Moonlight on the Quarry" and the Moon Hop are invented). The parody brands are fine: Bolt Cola, Quik-Mart, Pet Paradise, Spirit-Talk, Seal-a-Fresh, Golden Tomorrow, Sugar Sergeant. The Jaycees are a civic group, not a product.
- PG-13 holds: the slashers are cartoon-scaled (canoe-paddle knife, crowbar skate key), with no gore and no deaths. Bad outcomes are lost time, teleports or being stuck. The bat and trophy are swung at masked monsters that turn out to be empty. The player is never given a gender, race or orientation. "The grown-ups from your own house" is good neutral phrasing.
- Every encounter has 2-3 ungated choices and no requires. Skill rewards are capped at one per encounter, and the effects follow the scale (worst is -2 nerve).
- The drag revue card ("The Show Must Go On") keeps Glory and Frankie as competent heroes. The creature's feather boa is slapstick, not queer-coded menace.

## Silas calls (not changed)
- Some successes are rich: Last Bus climb-aboard gives +1 nerve, -1 dread and +1 nerve skill at target 11, and several target-9 successes give both +1 nerve and -1 dread. This is within reason. Recommendation: leave it unless playtests show nerve inflation.
- Cross-file, not in my scope: hungry-house.json's bad ending Takes "the family from number 9", which is Dr. Haddad's house in companions.json. Recommendation: renumber that family, or make the line about Haddad on purpose.
- Cross-file: items.json has "Blessed Super Soaker" (a real trademark, and anachronistic in 1986) and "Bactine" (a real brand). Recommendation: "Blessed Squirt Gun" and "Bandages and Burn Spray".
- The "1959 prom" song here ("Moonlight on the Quarry") and Mix's 1966 prom song ("Moon Over Crystal Springs") are different invented songs with similar names. Recommendation: rename one, or make them the same song, if the overlap is unintended.
