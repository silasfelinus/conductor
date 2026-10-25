# the-shape.json red-team findings

Validator: `checkCrystalStreetFile.ts villains` passes on the edited copy.

## Fixes made
1. **Blocking** - `the-shape-the-laugh` / `laugh-louder` success: "She cannot pick one loud girl out of a building full of them" gave the player a gender. Changed to "one loud laugh".
2. **Polish** - Woolco is a real trademark used as an in-world place (3 times: the `the-shape-stay-with-your-group` place, its text, and `flip-the-breakers`). Renamed it to the parody "Thriftco". Jaycees is a real civic group, not a product, so it stays.
3. **Polish** - finale `trick`: the decoy "slumps on the couch", then the Shape is suddenly "inside the hall closet", and the art put the dummy "on the floor". That contradicts itself and skips a step. The decoy now slumps just inside the hall closet, she steps in after it, and the door slams. I matched both art prompts to that.
4. **Polish** - `the-shape-every-sitter` / `walkie-check-in`: a toddler named "Joey" collided with the companion Joey Benally (17). Renamed the toddler Jamie.
5. **Polish** - `walkie-check-in` failure: fixed the comma splice "The sitter is fine, she dropped her walkie..." with a parenthetical.

## Checked and left as is
- Clue trio (Party Line tape = who lied, date book = what really happened, Harvest Hop negative = the love) explains the central issue and sets up the heart path. Every investigation success grants its clue, and the three locations are all different and not the pawnshop.
- Timeline holds: 1971 to 1986 is fifteen years, Teddy is 16, and Coach Pruitt was in her first year in 1971. Carol Lund is Carol Pickett.
- No lyrics quoted. "Crazy for you" in June's note is a common phrase, not a quote. "Bee Gees" names a band only.
- "Polaroid" (label of `snap-a-polaroid`, plus failure text) is a real trademark, but the reference file frieda-krueger.json uses it too, so I treated it as house convention. If it should change, change it repo-wide (the item is "Instant Camera").
- Tina's "I'll be right back" encounter has the same title as counselor-jess-right-back. That is fine within each file. Just noting the cross-file duplicate.

## For Silas (not changed)
- **Known flag: Mickey vanished on Halloween 1972** (backstory). She is a queer girl who is dead or gone, which is a bury-your-gays risk. Related point I found: the Best ending has her walk toward the Heartstone, toward "a porch light left on for a girl in a matching cardigan". That reads as June being dead or waiting in an afterlife too, so both girls are gone. Recommendation: make June Albright alive in 1986 (31, still in the valley, maybe at the KGLM broadcast or on the lawn), and have the Best ending reunite them in the living world rather than the light. That turns the ending into the Spring Queen's "last dance" pattern instead of a double loss.
- Finale `trick` is hustle 11 (the guide says a trick is usually 9). This is a balance call.
- The finale `trick` and Pearl in the pledge meeting show companions as if they are present whether or not they were recruited. Frieda's reference file does the same thing, so I left it.
