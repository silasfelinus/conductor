# varsity-beast.json red-team

Validated: `checkCrystalStreetFile.ts villains` -> 1 villains OK.

The "be a man" arc lands well. PG-13 holds: the Beast shoves, pins and chases but never bites, and the bad ending is Taken (Brick lost to the wolf, you stuck in "walk it off"). The queer-positive frame is good: Moose, Glory, Frankie, Chip and the Glitter Box all read as heroes. Homophobia appears only as Duke's, Hollings's and the boosters' failure, and the story confronts it. The clue trio (Brick's tap "playbook", Duke's yearbook quote "My father dances. I win.", Featherfoot's shoes and note) explains three generations of the wound, and the heart choice uses exactly those three objects. No slurs and no song lyrics. One +1 skill per encounter.

## Fixes (in redteam/varsity-beast.json)
- BLOCKING (real trademark used as an in-world product): "Camaro" appeared 5 times in the Surfin' Route 49 text. Changed it to "muscle car", which the art already said.
- BLOCKING (real trademark, same call as frieda-krueger): "snap a Polaroid" and "a fresh Polaroid developing" are now "instant photo". The item id `polaroid` in the bonus is unchanged.
- POLISH (contradiction): the logline said Brick "has three days to become a man", but the week is seven nights and the Monster Bowl is on Halloween. Changed it to "one week".
- POLISH (contradiction): the Wolfmania place was "the Friday-night autograph table", but that is an act 2 card and Friday night is the finale. Changed it to "late-night".
- POLISH (contradiction): the tap-shoes hint said the Glitter Box "was the Rialto before the war", but the lobby photo is dated 1946 and Duke left the shoes there in 1966. Changed it to "used to be the old Rialto".
- POLISH (clue/heart mismatch): the Ask Coach Pruitt success grants the yearbook clue but only shows a whiteboard, and the heart choice carries "Duke's yearbook". Added one sentence where Pruitt tucks the 1966 yearbook under your arm.
- POLISH (logic): the finale is in the fourth quarter, but the text said the crowd "thinks it's the halftime show". Changed it to "thinks it's part of the show".

## Checked, no change
- Cross-file: spring-queen called the 1966 yearbook "the Glimmer", while this file calls it "the Gold Nugget". I kept Gold Nugget here because it fits the Prospectors mascot and changed spring-queen to match. countess-lacroix now also uses this file's Rialto history for the Glitter Box building.
- Coach Hollings calls you "sweetheart" as an insult. It is a human failure, not an assignment of the player's gender. Kept.
- The finale trick and heart choices are both target 11, where the guide says trick is usually 9. Left as is, because targets are out of scope.

## Silas calls / systemic notes
- Several success texts assume a bonus companion is physically present even when they are not in the crew: Moose in the finale fight ("the way Moose taught you"), Hold the Line and New Tradition; Lou in Start a Rumor; Chip in Change the Chant. A companion bonus only adds to the roll. Recommendation: either gate companion-dependent prose on crew membership in the engine, or write companion cameos as conditional. This is a cross-file pattern, so I did not change it here.
- None of the known open flags appear in this file.
