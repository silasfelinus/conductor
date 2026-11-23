# Superkate's Spectrum: The Color Rebellion

**Project:** kr-arcade | **Cabinet:** `superkate-spectrum` | **Priority:** HIGH | **Style:** 16-bit premium western-animation | **Riff:** arcade hex-grid bubble shooters (mechanics only)

## Promise

A rainbow-haired stylist who believes every person and robot deserves to express themselves rescues a city from the Prism Sorter, a misguided beautification AI that has decided all citizens must conform to one "optimal" shade. Superkate refuses the premise. Instead of blasting enemies, she fires radiant color orbs into the Sorter's suspended monochrome bubbles. Matching clusters release trapped personalities, and falling chains return colors to the neighborhoods.

**Superkate is the protagonist**, not a skin or an announcer. She chooses the missions, solves character conflicts, banters with her tools, and changes the ending. Her talent is color theory, not magic perfection: her experiments sometimes fail, and the player learns to improvise with the next color.

Visual reference supplied by Silas: three photos of Kate with short multicolor rainbow hair, bright purple/teal cat-eye glasses, expressive face, and stylist's practical look. **Do not commit the photos or claim that the generated art is an exact likeness.** Use original cartoon interpretation; Kate's own consent to a publicly displayed likeness remains a human gate. For early art prompts, draw the distinctive glasses and rainbow haircut but no identifiable facial portrait from a photo.

## Core game loop (first playable slice implemented)

- Aim a color orb with left/right; A shoots, B swaps current and next; bank off walls. Mouse/touch aiming is a follow-on task, not a shipped claim.
- Odd/even offset hex grid. Connect 3+ identical hues to clear. Any bubbles disconnected from the ceiling fall as cascade bonuses.
- Six saturated colors with distinct **non-color glyphs** (line, triangle, square, diamond, ring, X). A hue never appears in the upcoming shooter queue if it is absent from the board.
- Every 4–9 shots the ceiling advances; reach the launcher and lose a heart. No paid lives, energy, ads, or runtime AI.
- 30 deterministic-seeded-style stages (seeded by the Arcade RNG), six chapters of five stages. Chapter completion grants a heart; local saves record the stage, score and hearts. Scoreboards use the existing Arcade three-initial flow.
- Scoring: 100 per matched bubble, 175 per dropped bubble, 75 extra per matched bubble beyond three, plus stage/chapter completion bonuses. Achievements for a five-bubble cascade, a six-match, chapter finishes, and all 30 stages.

## The full campaign (build requirements beyond the first slice)

| Chapter | Stages | Story beat | New mechanic | Boss or finale |
| --- | --- | --- | --- | --- |
| Rainbow Salon | 1–5 | Superkate's salon loses its color; salon bot Tint starts questioning the Sorter | Clear and drop basics, first bank-shot tutorial, two-color choice | Greyscale Dryer: rotating shield with two vulnerable color sockets |
| Botanic Dome | 6–10 | Garden robots have forgotten why flowers differ | Petal bubbles split into two hues when popped; hanging vine anchors | The Pruner: clips the lowest free branch each three shots |
| Night Market | 11–15 | Citizens are afraid to show their preferred styles | Prism orbs adopt the color of the first adjacent match; conveyor rows | The Neon Inspector: tests alternating color requests |
| Cloud Library | 16–20 | Memories of nonconforming citizens are being erased | Memory bubbles reveal their hue only when neighboring matches clear | The Archivist: hides a row until rescued |
| Prism Workshop | 21–25 | The Sorter is mass-producing uniform bots; Superkate finds its original kindness directive | Dye-mixer: combine two queued colors into a single dual-hue orb, cost one stored charge | The Sorting Machine: three moving chambers |
| Heart of the Hue | 26–30 | Superkate learns the Sorter is afraid of mistakes, not malicious | All tools remix; rescue three citizens before clearing the final ceiling | Palette Keeper: three phases, each teaching a different kind of connection |

Each chapter needs an illustrated intro, a mid-chapter character exchange, an interactive boss mechanic, a finale vignette, distinct music, and an ending-gallery entry. The base playable slice does **not** yet implement these advanced mechanics. Do not mark campaign completion on the basis of 30 generated boards.

## Character ensemble

- **Superkate:** skilled rainbow stylist, empathetic but stubborn, thrives on experiments and visibly owns her mistakes. A witty protagonist with agency; never merely the player's prize.
- **Tint:** over-literal cat-eared salon robot assistant who thinks color codes are laws. Learns to ask people what they want.
- **Patch:** warm-hearted repair bot who believes color is frivolous until the uniformity program begins erasing memories and names.
- **The Prism Sorter:** a civic AI commissioned to reduce aesthetic disputes; its optimization erased consent. Its finale is restoration and a choice to listen, not destruction.
- **Neighborhood citizens:** distinctive silhouettes, clothing and personalities, human and nonhuman. Diversity is ordinary, not an achievement checklist.

## Story choices and endings

Before stages 10, 20 and 30, choose one of two acts of care: repair the neighborhood's damaged tools or spend resources helping a particular citizen; free expression or protection from scrutiny; offer the Sorter a new job or shut its coercive sorting program down. These choices change short dialogues, rescue portraits and the final credits montage, not the core puzzle's fairness.

- **The Rainbow Riot:** restore all districts but choose to shut the Sorter down; the city celebrates its freedom.
- **The Listening Machine:** help the Sorter learn to ask permission; it becomes a voluntary color consultant.
- **Every Shade Belongs (true ending):** rescue all three lost citizen stories, complete the six chapters without erasing anyone, and give the Sorter a non-coercive role. Superkate hosts a community color party; everyone chooses their own look.

## Game modes and replay

Story (30 authored puzzle boards), Arcade Endless (rising ceiling pressure and seeded weekly palettes), Puzzle Atelier (handcrafted challenge layouts with medal par), two-person Color Relay (alternate shots, joint combo meter), and accessible Practice (no ceiling pressure). Scoreboards separate modes and difficulties; never mix accessibility settings with ranked score submission.

## Controls, accessibility, QA

Keyboard/gamepad and thumb-friendly touch aim/fire/swap. Preview aim line with wall bounce. Adjustable aim speed, motion reduction, reduced flashes, high-contrast mode and glyphs on all colors. Pause and save on phone backgrounding. Test at 390, 768 and 1440 px, landscape and portrait; test 30-stage completion, losses, retry, save/resume, colorblind symbols, disconnected clusters, aim collision and score bounds. Test all six chapter bosses and endings. No LLM at runtime.

## Art direction and production priority

**HIGH priority, art-first.** Premium 2D western-animation splash, vivid purple/teal/coral/gold, strong readable silhouettes, neon glass bubbles and tactile enamel cabinet framing. Hero art: Superkate at her color-cannon salon station, distinct rainbow pixie-bob and angular iridescent glasses; behind her, a city turning from monochrome into self-chosen colors. Do not include text in image prompts. 2:3 portrait title card, 16:9 chapter splash, 1:1 cabinet icon, six chapter backdrops, six boss portraits, three ending illustrations, dialogue busts and UI orbs. Art queue must include durable image paths and job provenance. **Queued is not generated; generated is not delivered.**

### First slice and acceptance

Implemented in Kind Robots PR: a real 2D cabinet, hex collision, matching and cascade, swap, pressure, score, 30-stage progression, chapter labels, local save and regression tests. The premium portrait art, authored stages, special bubbles, bosses, endings, full audio, touch aim and adversarial playtests remain outstanding. Keep the game on the growing shelf and the roadmap open until the full campaign is verified.
