# counselor-jess.json red-team findings

Validator: `checkCrystalStreetFile.ts villains` passes on the edited copy.

## Fixes made
1. **Blocking (art)** - `poster` showed "teens skinny-dipping" with "scattered clothes on the grass", and `endingPhoto` showed "skinny-dipping teens". These prompts would ask for nude minors. Changed to "teens swimming"/"scattered towels" and "teens in swimsuits". The skinny-dipping in the card text stays, because it is PG-13 (shoulders above water) and central to the remix.
2. **Blocking** - `endings.bad`: "The lake drains away at dawn and takes you with it", with the player seen under the water every year, reads as the player drowning. The guide says bad endings are Taken, not killed. Added "not drowned but Taken, down into a night swim that never ends."
3. **Polish (contradiction)** - The whistle signals disagreed with each other. The finale `trick` makes three short blasts "everybody out" and one long blast "everybody under". But `take-the-chair` used one long blast for "everybody out", `cover-the-pool` failure used one long blast for "get out", and `edge-1` used one blast for "swim's over". Changed those three to three short or soft blasts. The one long blast stays as Jess's menace signal everywhere else.
4. **Polish** - `endingPhoto` called the mask a "lake-rescue mask". It is a hockey mask everywhere else, so I changed it to "hockey-style mask".
5. **Polish** - `tear-it-down`: "You climb the folded bleachers" while the school is sitting in them. Changed to "the end of the bleachers" in the text and the art.
6. **Polish** - `counselor-jess-lights-out` text: "torn navy dress clinging" changed to "dripping". Jess is canonically twelve, so I removed the body-cling wording (see the Silas item below).

## Checked and left as is
- The cast table matches: a drowned girl, Camp Crystal Pines, August 1957, the lake drained two years later (the 1959 suburb). The "twenty-nine years" count is right, and Judy was 16 then and is 45 now.
- Clue trio (swim card plus Pratt's memos, Judy's side, the mother's headstone and the parish register) covers neglect, blaming the girl, and nobody having time. It points squarely at the heart path (say her name, get in the water). Every success grants its clue, at three different locations.
- No player gender, no slurs, no lyrics. "Bananarama" names a band only, and the camp song is invented.
- Kev Park (12) and the Delgados show up as NPCs. That is consistent with the cast table.

## For Silas (not changed)
- **Jess's grown-in-death costume.** She is a 12-year-old's ghost, yet `backstory`, `poster`, `portrait`, `endingPhoto` and several scene prompts dress her in a "torn sleeveless ... lace-up dress cinched with a leather belt" with "scars along her arms and thigh". Next to skinny-dipping teens, that pin-up look sits badly with PG-13 and the guide's line that a villain is never "scary because she's a woman". Recommendation: keep her towering and muscular, but make the outfit a too-small, rain-soaked navy camp counselor's dress or jumper with a whistle lanyard. Drop "laced up the front", "sleeveless" and "thigh". This touches about 6 art prompts plus the backstory, so it is your call.
- `swim-for-petey` success gives +2 nerve and +1 brawn. That is generous against the effects scale. It is a balance call.
