# Chessweeper: Three Dangerous Worlds

**Project slug:** `chessweeper`  
**Frontend:** `/play/chessweeper`  
**Master issue:** [Kind Robots #5304](https://github.com/silasfelinus/kind_robots/issues/5304)

## Shared stage

An 8×8 chessboard contains a 4-rank hidden minefield and ricocheting disc hazards. Player commands move, probe, flag and dash. White plays against a legal-move computer Black. A chess move or probe advances discs; flags do not. Win by checkmate or revealing every safe square; lose by losing the king or exhausting its protection. Chess special moves and promotions work, while hazards deliberately alter orthodox chess.

## Sugarbomb Kingdom

Lisa Frank-inspired neon-kawaii bubblegum joy, but wholly original characters/art. Candy pieces, sparkle particles, glitter wheels and lollipop traps. Safely reveal clues and capture enemy pieces to build Sugar Rush; a full meter freezes blades temporarily and pays a combo bonus. Lower pressure and sweeter forgiveness than Ashen.

## Ashen Checkmate

Soulslike grimdark stone-cathedral battlefield, oppressive ash and iron. Curse mines, heavier disc pressure, low armor. A once-per-run Last Stand gives the player a final recovery chance after taking fatal arena damage, while correctly read hazards preserve scarce defenses.

## Jackpot Apocalypse

Chrome-neon casino/pinball game show with lethal pinballs. Captures build the scoring multiplier; optional Double-or-Nothing wagers spend score, increase hazard speed/multiball pressure and magnify the payoff. Broken streaks lose the multiplier. High score is the lure; self-inflicted chaos is the punchline.

## UX and requirements

Single screen with stage dominant, compact controls, tutorial in the Kind Robots help sidebar, keyboard/mouse/touch, visible mode changes that reset the run. Register a Play channel tab and link from project metadata. Use durable ArtJobs and delivered image URLs, no borrowed franchise assets. Test 390/768/1440 widths and entire runs for every mode. Keep published release gated even if the code is mergeable.
