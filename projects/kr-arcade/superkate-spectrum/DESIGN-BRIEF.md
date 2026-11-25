# Superkate's Spectrum: The Color Rebellion

**Project:** kr-arcade | **Cabinet:** `superkate-spectrum` | **Priority:** HIGH | **Style:** 16-bit premium western-animation | **Riff:** arcade hex-grid bubble shooters (mechanics only)

## Status (2026-11-25 PT): ready for human playtests

Agent-verified on every cabinet PR (kind_robots#5816). The full 30-stage campaign and all six bosses
are beaten by real shots on three choice routes, reaching all three endings. A careless-play soak
finds no hang or lost progress. The Co-op Relay (own orbs, gifted Prisms, duet boss, saved records)
and all 12 Atelier puzzles are proven solvable. Rendered cabinet QA covers 390/768 touch and 1440
keyboard/gamepad, covering the hub, settings (separate music and effects levels), the in-game save
state, and two-device account sync (kind_robots#5823). Every build task is done. What is left needs
people: visual acceptance and shelf placement (t-184). Superkate's six district illustrations are now the
Scrapbook memories, approved by Silas (t-189, kind_robots#5836).
See [PLAYTEST-CHECKLIST.md](PLAYTEST-CHECKLIST.md).

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


## Permanent career: the player never loses their history (Silas, 2026-11-22 PT)

The game is a long-term color adventure, not a one-off high-score arcade loop.
Its **career profile** is separate from any single run. A failed board never
takes away previously unlocked levels, best star ratings, earned rank or
cosmetic bubble styles. The first implementation is a versioned Arcade save
on the current browser/device, including backwards compatibility with the
previous version-1 checkpoint. **Cloud/account sync is a separate remaining
task and is not yet delivered**; guest saves need a safe account-claim migration.

- Story's 30 chapters/boards remain unlocked permanently once completed. The
  level selector can replay any unlocked stage and keeps the best of 1–3 stars
  earned on that level. Stars are awarded based on shots used, with reruns
  allowing improved medals. Later, the scrolling map should show all 30
  locations, best star ratings and milestones, not just a numeric selector.
- All popped and dropped bubbles grant Color XP. Clearing a stage grants
  additional XP and stars. A permanent **Color Rank** rises on a gradually
  growing XP curve, and unlocks cosmetic bubble looks: glass (1), candy (4),
  starlight (9), and prismatic (15). Cosmetic unlocks do not change the
  underlying collision mechanics or force spending.
- A durable profile records career XP, highest unlocked story stage, 30 best
  star ratings, lifetime bubble rescues, best Classic score and Classic runs.
  It survives game-over and voluntary exits. A board itself is recreated from
  the stage upon resume; mid-shot state is not yet saved.
- **Classic Mode:** select an infinite bubble-shooter run with pressure rising
  after shots, original matching, no special power bubbles, separate local
  personal best and runs played. A Classic loss never rewinds Story. Per-mode
  online leaderboard partitioning is still required before ranked competition.
- **Special orbs:** earn a Prism that mimics a helpful adjacent hue, a Burst
  that clears local neighbors, and a Ribbon that clears a row. Unlocked by
  Color Rank and earned through clearing bubbles, not purchasable. Classic
  mode disables them. These effects are drawn with distinct pulsing rings
  and sparkle fragments; bigger authored animations, sound and effects
  remain on the finite art/audio roadmap.
- **Never add Candy Crush-style predatory energy, timed heart refills or
  currency purchase gates.** The good part to borrow is visible lasting
  progress, better mastery, replayable levels and surprise rewards, not
  dark-pattern spending loops.

**Save invariant:** after game-over, `save` must still return the career
snapshot (not `null`), because the Arcade store interprets null as erasure.
A saved v1 checkpoint must migrate to v2 without losing its unlocked stage.
Validate and bound every untrusted save field; old saves and failed shots
must not erase more recent star/rank progress.

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

### Audio delivery status: original adaptive music, not final mastered tracks

The Kind Robots game PR now contains six original synthesized neighborhood
themes, six faster chapter-showdown arrangements (stage 5/10/15/20/25/30),
a dedicated Classic loop and a calmer title/menu loop, plus responsive shoot,
bubble-pop, row-blast, stage-clear and lost-life sound effects. The native
Settings screen can independently toggle music, effects, animation and
contrast, while its master volume and mute drive the *same* Arcade audio
mixer used by the surrounding cabinet. The settings live in the versioned
Spectrum career save; the Arcade-wide volume remains the shared source.

Important remaining deliverables: authored, approved and delivered mastered
music stems for each chapter, real audio balance tests on mobile and desktop,
mute/unmute transitions, chapter-boss reveal sequences and final QA. Synth
fallbacks are playable original music, not proof that the recorded soundtrack
was produced. Task t-182 remains partial until these checks are green.

## Retro-modern presentation contract (Silas, 2026-11-22 PT)

**The game is the interface.** The player enters Superkate's Spectrum through
the existing Arcade console cabinet, not through a stack of independent admin
pages. The cabinet silhouette, original chiptunes, score displays and joyful
precision of the classic puzzle-shooter era remain the DNA, while the actual
interaction behaves like a current polished game: tactile high-resolution
bubbles, bold animated feedback, modern accessible controls and a visually
legible, responsive one-screen stage.

The game home is a single connected place for:

- **Play:** Story map and the separate pressure-driven Classic mode.
- **Scrapbook:** saved progress for all 30 stage stars, citizen and character
  memories, six neighborhoods, three ending illustrations, collectible
  orb styles and gameplay discoveries. Locked entries tease the next reward.
- **Achievements:** three global Arcade awards and meaningful chapter
  milestones. Trophies earned in-game display in the user's scrapbook and
  global achievement shelf; locked trophies expose helpful hints.
- **Settings:** volume, music/effects mixing, CRT/pixel/HD preferences,
  reduced animation, high contrast, glyphs, aim-guide assistance and input
  help. Share ownership with existing Arcade settings, do not duplicate the
  actual audio source of truth.
- **Account:** explicit device versus account-save state, signed-in cloud
  backup and guest progression adoption without silently losing either
  version. Revision conflicts merge monotonically and retry safely.

Controller/keyboard and large touch targets must reach these screens from
within the cabinet. Keep gameplay and hub visually coherent and one screen,
including mobile portrait 390px. UI chrome should use polished glass, enamel
and candy color, not tiny pixel-font walls of instructions. The *playfield* can
remain retro-inspired without making the interface feel like a museum exhibit.

**Production distinction:** The initial PR implements an in-canvas hub,
private account-save model/endpoints, original 6-region oscillator themes,
Classic track and three global achievement definitions. Authenticated
cross-device workflow requires final CI, schema deployment, direct sign-in
and account-switch tests before it can be called verified. Premium album
portraits, published recordings, mobile touch polish and final menu
presentation remain incomplete. No image-queue request constitutes delivery.

## Game modes and replay

Story (30 authored puzzle boards), Arcade Endless (rising ceiling pressure and seeded weekly palettes), Puzzle Atelier (handcrafted challenge layouts with medal par), two-person Color Relay (alternate shots, joint combo meter), and accessible Practice (no ceiling pressure). Scoreboards separate modes and difficulties; never mix accessibility settings with ranked score submission.

## Controls, accessibility, QA

Keyboard/gamepad and thumb-friendly touch aim/fire/swap. Preview aim line with wall bounce. Adjustable aim speed, motion reduction, reduced flashes, high-contrast mode and glyphs on all colors. Pause and save on phone backgrounding. Test at 390, 768 and 1440 px, landscape and portrait; test 30-stage completion, losses, retry, save/resume, colorblind symbols, disconnected clusters, aim collision and score bounds. Test all six chapter bosses and endings. No LLM at runtime.

## Art direction and production priority

**HIGH priority, art-first.** Premium 2D western-animation splash, vivid purple/teal/coral/gold, strong readable silhouettes, neon glass bubbles and tactile enamel cabinet framing. Hero art: Superkate at her color-cannon salon station, distinct rainbow pixie-bob and angular iridescent glasses; behind her, a city turning from monochrome into self-chosen colors. Do not include text in image prompts. 2:3 portrait title card, 16:9 chapter splash, 1:1 cabinet icon, six chapter backdrops, six boss portraits, three ending illustrations, dialogue busts and UI orbs. Art queue must include durable image paths and job provenance. **Queued is not generated; generated is not delivered.**

### First slice and acceptance

Implemented in Kind Robots PR: a real 2D cabinet, hex collision, matching and cascade, swap, pressure, score, 30-stage progression, chapter labels, local save and regression tests. The premium portrait art, authored stages, special bubbles, bosses, endings, full audio, touch aim and adversarial playtests remain outstanding. Keep the game on the growing shelf and the roadmap open until the full campaign is verified.
