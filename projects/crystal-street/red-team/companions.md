# companions.json red-team

Validated: `checkCrystalStreetFile.ts companions` -> 22 companions OK (before and after edits).

## Fixes (in redteam/companions.json), 0 blocking / 7 polish
- POLISH, contradiction: Joey's bio said "He built Sunny Castellanos's racing chair", but Sunny's bio says she "built her racing chair with Joey Benally's help". Joey's bio now reads "He helped Sunny Castellanos build her racing chair out of bicycle parts and stubbornness." That keeps Sunny as the one who built it (disability agency) and drops a second "and spite" that echoed Dani's bio.
- POLISH, brand: Barnaby's sandwich failure had "vanishes under a Cadillac" (text) and "a rusty Cadillac" (art), a real trademark. Both now say "a rusted / rusty tail-finned sedan".
- POLISH, grammar: Pearl's bio had Pearl alone "became one of the first Black families". It now says "in 1959 the two of them became one of the first Black families".
- POLISH, clarity: in Priya's roll-a-character success, "Priya fights it and fails and laughs" was ambiguous (fights the cube?). It now says "Priya tries to keep a straight face, fails, and laughs so hard she snorts."
- POLISH, broken line: Joey's ask-about-the-maze success said "\"Not if it moves,\" you say. \"Which way.\"". It now says "\"Not whether it moves,\" you say. \"Which way it moves.\"".
- POLISH, art/text mismatch: in Joey's jump-the-truck success, the text says Joey slaps the hood but the art said "slapping the dashboard". The art now says "leaning out of the driver's seat to slap the hood".
- POLISH, anachronism: in Wade's push-start success, "Get in, loser" is a 2004 movie catchphrase. Changed to "Get in, slowpoke."

## Checked, no change
- Cast table: all 22 ids, names, pronouns, ages, skills, locations and sketches match. Chip is "Charles 'Chip' Merriweather III" in his bio, which fits the table. Raven's "no pronoun needed" line is the table's wording.
- Dates hold: Delphine is 18 in 1966 and 38 now. Glory was 19 in 1961 and is 44 now. Frankie left Fresno at 19 and is 24 five years later. Pearl was in the WAC in 1944 and is 71 now. Zelda's career ran 1951-59 and she is 63 now.
- House numbers match the decks and villains: 7 is the Brightwaters, 9 is Haddad, 13 is the model home.
- Every meet has at least one recruit success. Every failure says "come back tomorrow". No meet choice is gated. Effects follow the scale. No real song lyrics appear ("Moon Over Crystal Springs" is invented). No slurs. The player is never given a gender, race or orientation.
- The weapons are held by adults and never pointed at a person: Pearl's rock-salt shotgun, Tammy Jo's bat. Wade (18) holds his tire iron up "like a sword", not aimed at anyone. The squirt guns are toys.
- Moose's "Hey Grandma" taunt is confronted in the same scene (the stand-up-for-him choice). Queer characters (Dani, Delphine, Glory, Frankie, Moose, Raven, Zelda and Ruth, Chip) get joy, competence and the last word.

## Silas calls (not changed)
- Known flag: Chip's bio outs him ("has known since junior high that he likes boys"). The meet handles it well: the player never outs him, and the cover-for-him choice protects him. Recommendation: keep the bio as author-facing context, but if the bio is shown to players before recruitment, move that sentence to a post-recruit reveal.
- Raven's say-it-right success has the player say "How are they doing today?" to Raven's face. It may be meant as pronoun practice, but addressing someone in the third person reads oddly, and Raven's own sad line is "Nobody asks how I'm doing." Recommendation: "How are you doing today, Raven?"
- Kev's meet mentions "Mr. Pruitt's dog" on Crystal Street, which shares a surname with Coach Tammy Jo Pruitt. Recommendation: rename the neighbor, or confirm he is her husband.
- Three companions (Delphine, Bea, Raven) share the clue-sense perk, and four (Frankie, Moose, Tammy Jo, Amir) share shield. This is a design choice, not a content fault.
- Cross-file, not in my scope: items.json names holy-water "Blessed Super Soaker" (a real trademark, and anachronistic in 1986) and first-aid "Bandages and Bactine" (also a real brand). The companions file's Iggy text calls them squirt guns, which is fine.
