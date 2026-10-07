# Zuzu Showdown — Design Brief

date: 2026-10-06
status: v1.2 — building; scope confirmed by Silas (2026-10-06/07, see "Decisions")
author: Claude (from Silas's request, 2026-10-06)
title: **Zuzu Showdown** (confirmed by Silas, 2026-10-07)

## Silas's ask (verbatim)

> new arcade game project, this will be another distinct project, possibly our largest yet: I want a 2d
> fighting game styled like street fighter/skullgirls/marvel v capcom, in the world of Zuzu Koala
> Assassin. Characters should include Zuzu, Coyote Vagrant, The Abbess, the Siblings, Storm Crow, the
> River Croc, and a couple others. We'll need special moves per character, styled like street fighter or
> mortal kombat, a combo system, and some sort of paper rock scissors level of strategy. moving
> background animations, pixelly art graphics, punch, kick, dodge, flying kick, flying punch animations,
> plus special moves, victory and death poses, taunt screens before and after, customized lines per each
> matchup (aim for 8 starting fighters), life bars, special meter, unique super attacks.

## What it is

A one-on-one 2D fighting game, free in the browser on Kind Robots. It has the systems of Street Fighter
II (motion-input specials, footsies, rounds), the chain combos and launchers of Marvel vs. Capcom, and the
style and anti-infinite rules of Skullgirls. It all happens in the weird-west wasteland of *Zuzu: Koala
Assassin*. Eight fighters, each with special moves, a Level 1 super and a Level 3 Showdown super. A
strike/grab/guard triangle is the rock-paper-scissors core. The art is chunky pixel art and the stages
move. Matchup-specific lines play before and after every fight.

It is its **own project**, not an arcade cabinet. Its scope (eight fighters, sprite sets, a combat
engine, CPU AI and a content library) dwarfs any cabinet. It still borrows the arcade's leaderboard,
sound kit, pixel font, touch-play lock and cabinet chrome, and it gets a tile in the Arcade hall that
links to it, the same as `zuzu-lair`.

## Who it serves

Anyone on Kind Robots, free, with no account needed. That includes Silas's kids (11 and 14) and the
fighting-game crowd. It plays on desktop (keyboard or two gamepads for local versus), tablet and phone
(touch stick and buttons, plus the one-button Easy Specials scheme). No LLM runs at play time. Every
line, sprite and stage is pre-made.

## Canon and tone

The comic folder `projects/comic-creator/issues/zuzu-koala-assassin-01/` is the canon. CAST-PICKS.md
holds the locked designs, VIDEO-GUARDRAILS.md the rules, and BOOK-ONE.md the story of record. Like
`zuzu-lair`, this is an **original side story, not Book One**. A versus game lets anyone fight anyone, so
nothing here is canon about who beats whom.

- **Zuzu:** short and stocky, koala-sized (the Danny DeVito build), with a subtle beer belly. Rust-brown
  poncho with orange zigzag trim, conical straw kasa shading his eyes, dark tunic, orange sash, dark
  brown cloth trousers. The katana is strapped diagonally across his back, hilt over the RIGHT shoulder.
  Always serious, with Eastwood stillness.
- **Scale is part of the look.** Zuzu is the shortest adult on the roster. The sister is taller than he
  is. The croc and the komodo dwarf everyone. Skullgirls-style size variety is a feature here.
- **Tone: lighter than the comic.** Silas, 2026-10-07: *"this is a lighter game than the mature comic. More
  street fighter than mortal kombat."* The designs keep the comic's grit (rags, dust, the dusty palette),
  but the violence is Street Fighter level: impact sparks and dust, never blood or gore, no fatalities,
  and every KO is a fighter knocked out, dazed or sent flying, never killed.
- **bannedTerms apply everywhere:** every art prompt, line, stage name and ending. Never `human`,
  `humans`, `humanity`, `mankind`, `people`, `pharmacy`, `great wall`, `skyscraper`, `highway`,
  `billboard`, `road sign` or `english lettering`. Say "townsfolk" or name the species. The buried twist
  stays buried.
- **Words the image models draw literally** (VIDEO-GUARDRAILS.md): "duster" (use "long riding coat"),
  "mother" (use "abbess"), "muzzle", "squat" (use "chubby, standing upright"), "ribs showing" and "sea
  otter" (negate water and feral otters).
- **The comic's no-dialogue rule does not bind the game.** Silas asked for matchup lines, so the game
  has them. They are game UI text in the pixel font, never captions in the comic. They stay true to each
  voice. Zuzu barely speaks, and his lines are mostly silence or two or three words. The croc only hisses.
- **The children rule is absolute** (VIDEO-GUARDRAILS.md). The Siblings fighter is designed around it.
  See "The Siblings" below.

## The roster (8 fighters + 1 boss)

The full data (stats, normals, specials with inputs, supers, intro, taunt, victory and KO poses) is in
**`fighters.yaml`**, and the engine's frame data is ported from it. Summary:

| # | Fighter | Archetype | Home stage | Showdown super (Lv3) |
|---|---|---|---|---|
| 1 | **Zuzu**, koala ronin | all-rounder; quick-draw iai and a parry stance | Hollow Bell | *Hat to the Dead*: one cut, then he sheathes and doffs the kasa |
| 2 | **Coyote Vagrant**, one-eyed, destitute | scrappy trickster; unreliable left-hand gun, knife lashed to his stump, steals meter | The Watering Hole | *Six Bad Shots*: five misses, one ricochet that doesn't |
| 3 | **The Abbess**, sea-otter head nun | zoner and summoner; thrown daggers, tentacles from the thin places, teleport | The Mission | *Open the Door*: the Thing behind the portal, never fully seen |
| 4 | **The Siblings**, fennec sister and toddler | small, fast rushdown plus a "puppet" toddler who throws apples | The Lone Apple Tree | *Lone Survivor*: the shaky dagger, then the SF3 frame |
| 5 | **Storm Crow**, raider captain | air rushdown with a flight mode; talon dives, hooked blade, lightning | Storm Canyon | *The Murder*: the whole flock sweeps the screen under lightning |
| 6 | **River Croc**, giant crocodile | giant grappler; command grabs, submerge and erupt | The Watering Hole | *Death Roll*: the stage floods and the croc erupts and rolls |
| 7 | **The Hyena Matriarch** *(new)*, slaver chief | mid-range chain-and-hook footsies; her cackles build meter | The Bone Yard | *Last Laugh*: the whole pack cackles in and the chains close |
| 8 | **Old Komodo** *(new to the game)*, ancient desert lizard | slow armored tank; venom bite damages over time | The Dunes | *Feeding Time*: erupts from the sand, gulps, chews, and spits the victim out |
| boss | **The Thing Behind the Door** | unplayable arcade final boss; tentacles and an eye through a portal | The Thin Place | — |

### Choosing "a couple others"

Silas named six and asked for "a couple others" to reach eight. Both picks come from his own canon:
- **The Hyena Matriarch** leads the hyena tribe of slavers, one of the three factions in
  BRAINSTORM-ROUND-3.md (with the Storm Crows and the otter house). She is the only faction without a
  fighter yet.
- **Old Komodo** is Silas's own character. He is "a shock appearance who turns out not to be a villain,
  but that doesn't mean he won't try to eat the siblings", erupts from the sand, and was held out of
  Book One for a later book. Pixel art may finally draw him well; the image models drew "a giant enraged
  koala".
- **The boss** is the tentacled horror from the convent: "dark and cosmic, half through a portal, never
  fully seen". A portal boss is a natural fit.

Alternates if Silas wants to swap: the **Great Monitor** (the lizard whose youngling the kids later
ride), an **Otter Nun** (a lighter, faster convent fighter), or the Thing as a playable oddball.

### The Siblings: playable under the children rule

- **Only the sister is ever hit.** The toddler is not a hurtbox. He rides on her back, or toddles a
  step behind her and ducks behind her legs when she is hit.
- **No death pose.** On a KO the sister scoops up her brother and runs off screen, alive. Opponents'
  victory poses and lines against the Siblings never gloat over hurting children: Zuzu leaves food and
  walks away (Book One chapter 3), and the Abbess's sinister win is framed as a threat, never shown as
  harm.
- **Supers soften against them.** Any super that bites, stabs, swallows or rolls its victim (the Croc's
  Death Roll, Komodo's Feeding Time, the Abbess's altar grab) plays a **fling variant** against the
  Siblings: the sister is thrown clear and tumbles, with the same damage and a gentler animation.
- **They fight like the comic.** She is gaunt, scared and ferocious. She bares her teeth, shields her
  brother, and in her Showdown super lifts the dagger with shaking hands, the convent's save. The toddler
  throws apples from the lone tree.
- The art pipeline's own content rules sit on top: she is never sexualised or undressed, and her
  clothes are claw-torn rags.

## How it plays

### Controls

Six inputs: the stick plus **Punch (light)**, **Punch (heavy)**, **Kick (light)**, **Kick (heavy)** and
**Dodge**. Armed fighters' punch buttons use the weapon (Zuzu's sheathed or drawn katana, the Coyote's
knife-stump, the Abbess's dagger).

- **Flying punch and flying kick** are the jumping normals. Every fighter has jump LP, HP, LK and HK, and
  most have a diving or downward special attack.
- **Dodge** is a short evasive move: forward = roll through, back = sidestep, in the air = air dash for
  some fighters. See the triangle.
- **Keyboard:** P1 uses WASD with U I / J K and Space to dodge. P2 uses the arrows with numpad 4 5 / 1 2
  and 0 to dodge. Everything is remappable.
- **Gamepad:** standard mapping. Face buttons are the four attacks, a bumper is Dodge, Start pauses.
- **Touch:** a floating stick and four buttons plus Dodge, sized for thumbs. The arcade's touch-play lock
  pins the canvas and swallows scroll gestures (silasfelinus/kind_robots#3276).
- **Easy Specials** (on by default for touch, a toggle anywhere): a Special button plus a direction
  fires a special, and Special plus Heavy fires the super, like Street Fighter 6's Modern controls.
  Specials done this way do 20% less damage, so classic inputs stay worth learning. Kids can play on day
  one.

### Motion inputs

Street Fighter notation, with a lenient 10-frame buffer and shortcuts (a DP accepts down, down-forward):
QCF ↓↘→, QCB ↓↙←, DP →↓↘, HCB →↘↓↙←, 360, charge ←(45f)→ and ↓(45f)↑, and double-tap ↓↓. Every
fighter gets at least one fireball-motion move and one DP-motion move, so muscle memory carries across
the roster.

### The Showdown triangle (rock, paper, scissors)

The core read at every close exchange is **Strike, Grab or Guard**:

| Choice | Beats | Loses to | Why |
|---|---|---|---|
| **Strike** (any attack) | **Grab** | Guard | A strike starts faster than a grab, so it stuffs the grab. |
| **Grab** (throw, command grab) | **Guard** | Strike | A grab ignores blocking and catches a dodge's recovery. |
| **Guard** (block, Dodge, parry) | **Strike** | Grab | A blocked strike is punishable. A dodged strike opens a free counter window. |

- **READ!** When an exchange resolves along the triangle (a strike stuffs a grab, a grab catches a
  guard, a dodge or parry beats a strike), a small fist, hand or shield icon flashes and **READ!**
  appears. The winner gains a quarter bar of meter. The triangle is visible and teachable.
- **Dodge** has invulnerable frames against strikes and projectiles, but its last frames are grabbable.
  Spam it and you get thrown.
- **Parry specials** (Zuzu's Poncho Veil and similar) are the high-risk guard: they catch a strike and
  counter it, and they lose to a grab.
- **Throw tech:** pressing grab in the first 7 frames of a throw breaks it. Grab against grab cancels out.
- **High, low and overhead** sit on top of this: crouch-block lows, stand-block overheads, standard fare.

### Combos

- **Chains (MvC / Skullgirls):** light into heavy, punch into kick: LP → LK → HP → HK. Each fighter
  lists its legal chains in `fighters.yaml`.
- **Cancels:** a normal cancels into a special, and a special cancels into a super.
- **Launcher and air combo:** crouching HK (or down+HP for some fighters) launches. Jump-cancel it into
  an air chain of flying punches and kicks, then an air finisher that knocks the opponent down.
- **Damage scaling:** each hit after the second does 10% less damage, with a floor of 30%. Supers
  ignore half the scaling.
- **Infinite protection (Skullgirls-style, simplified):** a combo ends if the same move hits twice in it
  (except designated rapid-fire moves) or if hitstun has decayed past its limit. The victim gets a
  **Breakout** flash and recovers. No infinites, ever.
- **Combo Breaker:** two bars of meter while being comboed knocks the attacker back. It is the comeback
  tool, and it can't be used during a super.
- **Callouts:** hit counter, **FIRST ATTACK**, **COUNTER**, **REVERSAL**, **READ!** and **BREAKOUT**,
  all in the pixel font.

### Meter, life and rounds

- **Life bars:** 1000 health by default, from Siblings 900 to Old Komodo 1150. They have a Skullgirls/MvC
  **red recoverable** portion: blocked chip and some combo damage turns red and slowly regenerates while
  you aren't being hit.
- **Special meter:** three bars. It fills from landing hits, getting hit (less), blocking (a little),
  READ! wins and taunts (only the Hyena's build much).
- **Supers:** every fighter has a **Level 1** super (1 bar) and a **Level 3 Showdown** super (3 bars).
  A Showdown super cuts to a full-width **eye strip**, the comic's signature frame SF1, before it lands.
- **Rounds:** best of three, a 99-second timer, chip KOs on, and a double KO counts as a draw round.

## Presentation

### Taunt screens, before and after

- **Pre-fight VS screen:** both portraits slam in over the stage name. The matchup-specific exchange plays
  as a line from one fighter and the reply from the other, in pixel-font bands. Then ROUND 1, FIGHT.
- **Intro animation:** each fighter has a stage entrance. Zuzu steps out of heat shimmer with his thumb
  on the scabbard mouth. The croc surfaces with only its eyes showing.
- **In-match taunt:** a button combination (Dodge + Heavy Kick, or a Start tap on touch), a short animation
  that leaves you open.
- **KO:** a slow-motion final hit, a white flash (capped at 3 Hz and disabled under reduced motion), then
  the loser's **KO pose** and the winner's **victory pose**. Each fighter has two victory poses and one
  special one for a Perfect.
- **Post-fight win screen:** the winner's victory portrait, the loser's beaten portrait, and the winner's
  matchup-specific quote to the loser.

Every fighter's victory pose and KO pose is in `fighters.yaml`. The matchup lines live in `matchups.yaml`
(t-018): an intro exchange for every pairing (28 pairs plus 8 mirrors), a win quote for every ordered
pairing (64), and boss lines.

### Stages with moving backgrounds

Each stage has 3 to 5 parallax layers that scroll as the fighters move. Each also has animated elements
(sprite loops and palette cycling), and one stage event that reacts to the fight.

| Stage | Owner | Moving parts | Stage event |
|---|---|---|---|
| **Hollow Bell** | Zuzu | drifting smoke, the bell tower's bell swaying, tumbleweeds, a torn banner in the wind | the bell rings once by itself at round start and once at the KO (canon) |
| **The Watering Hole** | Coyote, River Croc | heat shimmer, a single dead tree, the water's glints, circling vultures | a pair of croc eyes surfaces in the water during fights the croc isn't in |
| **The Mission** | The Abbess | candle flicker, nuns swaying in the cloister arches, a rusted merry-go-round turning by itself | between rounds a portal flickers in the bell arch |
| **The Lone Apple Tree** | The Siblings | wasteland heat shimmer, leaves rustling, dust devils | apples drop; the toddler grabs them when the Siblings are fighting |
| **Storm Canyon** | Storm Crow | rain sheets, wheeling crows, cloud scroll | lightning flashes light the whole stage in silhouette |
| **The Bone Yard** | Hyena Matriarch | a bonfire, drums, cackling hyena silhouettes on the giant ribcage of something ancient | the pack howls on a Showdown super |
| **The Dunes** | Old Komodo | sand blowing off the crests, heat shimmer, a long sun | the dune behind the fighters slumps and a vast shape moves under it |
| **The Thin Place** | boss | a cosmic sky tearing at the seams, floating debris | the door widens between phases |

There are no lettered signs except the diegetic Hollow Bell arch and other signs the canon allows.
Everything else (titles, names, callouts, lines) is drawn by the game in the pixel font.

### Pixel art

- **Canvas:** 480×270 logical, integer-scaled to 1080p (×4) or 1440p, letterboxed elsewhere, with nearest
  neighbor sampling, the arcade's optional CRT scanline overlay, and a 16:9 frame.
- **Fighter height:** Zuzu about 72 px, Coyote about 104 px, the sister about 84 px, the croc and the
  komodo 140 px or more (they go off-screen when they rear up).
- **Palettes:** each fighter has an indexed palette of about 24 colors with **alternate colors**
  (P2 always gets a different palette, in the Street Fighter tradition). Stages use their own palettes,
  dusty ochre, rust and bone by day and moon-blue at night.
- **Animation list per fighter** (about 30 animations, 3 to 10 frames each): idle, walk forward and back,
  crouch, jump up/forward/back, the four standing, four crouching and four jumping (flying) normals,
  dodge forward and back, block high and low, hit high, low and air, knockdown, wake-up, throw and being
  thrown, each special, both supers, intro, taunt, two victory poses, the Perfect pose and the KO pose.

### The art pipeline (the big unknown; t-007 settles it)

Hand-pixeling around 1,000 frames is not realistic. Generated art is pre-approved (AGENTS.md, Silas
2026-07-06), so the plan is generated art plus programmatic cleanup, picked by a bake-off on Zuzu's idle,
walk and punch:

- **A. Pose-locked generation:** a pose skeleton for every frame, drawn as data so the poses stay
  consistent, rendered through ComfyUI with the house lane and the character LoRAs (comic-creator t-016)
  plus a pose ControlNet, then background removal, downscaling to the target height and quantizing to
  the fighter's indexed palette.
- **B. Cutout rig:** one generated, pixelized sprite per body part, rigged and animated in code. Fewer
  renders and perfect consistency, but it can look like a paper doll.
- **C. Hand-authored indexed pixel maps** (palette-indexed grids as data). A good look, slow to make. It
  suits effects, projectiles, sparks and small props whichever way the fighters go.

The default recommendation is **A for fighters, C for effects**, with B as the fallback if pose
consistency fails. Until then the engine runs on **placeholder fighters**: flat-colored silhouettes with
correct hitboxes, so the game is playable before any art lands.

Portraits (character select, VS screen, win screen) and stage layers are single images: house-lane
renders, pixelized and quantized. There is no lettering in any generated art.

### Sound

WebAudio chiptune through the arcade sound kit: one loop per stage, hit, block, whiff and parry sounds,
the KO sting, a super-flash stinger, and the bell. There is no voice acting, and the announcer callouts
are on-screen text. Sound is muted until the first interaction and the mute setting is remembered.

## Modes

- **Arcade:** pick a fighter and fight seven CPU opponents on a rising difficulty ladder. The last is your
  fighter's **rival** (Zuzu–Coyote, Croc–Coyote, Abbess–Siblings, Crow–Hyena, Komodo–Croc and so on), then
  **The Thing Behind the Door**. Each fighter has a short ending of two or three pixel-art stills and a
  line or two. The score (time, combos, Perfects, READ!s) goes to the shared `ArcadeScore` leaderboard as
  `zuzu-showdown` with three-initial entry.
- **Versus:** local two players on one keyboard, two gamepads, or a gamepad and a keyboard, or one player
  against the CPU at a chosen level.
- **Training:** a dummy (stand, crouch, jump, block all, block after first hit, random), a hitbox and
  hurtbox overlay, frame-advantage readout, input display, infinite meter and a position reset.
- **Options:** difficulty (Kid, Normal, Hard, Showdown), Easy Specials, button mapping, CRT filter, sound
  and reduced motion.

### CPU opponents

A state-machine AI that reads the same frame data as players, with a difficulty ladder. On higher levels
it **plays the triangle**: it tracks how often you strike, grab or guard at close range and leans toward
the counter, so your habits get read. Kid difficulty blocks rarely and never uses Showdown supers.

## Engine architecture (kind_robots)

- `utils/zuzuShowdown/` is a **pure, deterministic simulation** with no DOM: fixed 60 Hz, integer and
  fixed-point math, state in plain serializable objects, input frames in and state out. Determinism keeps
  online rollback netplay possible later without a rewrite.
- **Data-driven fighters:** each fighter is a TypeScript module of animations, per-frame hitboxes,
  hurtboxes and pushboxes, cancel windows, specials (motion plus button), supers and stats, ported from
  `fighters.yaml`.
- **Contract tests** run in `contract-tests.yml` the way `verifyArcadeEngine.test.ts` does: the motion
  parser, the triangle outcomes, chain and cancel rules, damage scaling, infinite protection, round and
  KO flow, and a determinism replay that runs the same input log twice and compares state hashes.
- **Renderer:** a canvas component draws the sim state with sprite atlases, parallax and HUD. It reuses
  `utils/arcade/font.ts`, `sound.ts` and `leaderboard.ts`, and extends `input.ts` for two players and six
  buttons.
- **Page:** `/play/zuzu-showdown` on the Projects tab (`content/channels/projects/zuzu-showdown.md` plus
  `utils/projectPlacements.ts`), with an Arcade hall tile that links to it. The page stays **unlisted**
  (reachable by URL, not in the hall or the Projects list) until Silas's verdict (t-025).
- **Assets:** sprite atlases and stage layers live under `public/images/zuzu-showdown/` as WebP or PNG
  sheets with JSON frame maps. Keep the prompt, model, seed and source metadata for every generated
  image (AGENTS.md).

## MVP and phases

1. **Engine slice:** two placeholder fighters fight a complete best-of-three on a placeholder stage, with
   life bars, meter, triangle, chains and supers, on keyboard, gamepad and touch.
2. **Art slice:** the pipeline bake-off, then Zuzu and the Coyote with full sprite sets on Hollow Bell and
   the Watering Hole, a VS screen and lines for their matchup. This is the first build Silas plays.
3. **The full eight:** the remaining six fighters in pairs, all eight stages, matchup lines, CPU AI,
   Arcade with the boss, Training, sound and the leaderboard.
4. **Polish and verdict:** a balance and feel pass, phone, tablet and desktop checks, then Silas's
   verdict, and the hall tile goes live.

**Later (not MVP):** online rollback netplay, a story mode, alternate stages, more fighters (the Great
Monitor, an Otter Nun, the Storm Crow faction's grunts), and tag or assist mechanics in the MvC style.

## Out of scope / guardrails

- Riff on the *genre* only: no Street Fighter, Skullgirls, MvC or Mortal Kombat names, sprites, sounds,
  move names or characters.
- No fatality-style finishing moves, no blood and no gore. KO poses are Street Fighter-style knockouts
  (dazed, slumped, sent flying), and the Siblings always flee.
- No money, no ads and no paywall. Renders run on our own Comfy backend.
- No LLM at runtime.
- Every bannedTerm applies to every prompt and every line.
- Making the game publicly listed waits for Silas's verdict (t-025). The art itself is pre-approved.

## Decisions (Silas, 2026-10-06, answering t-002)

> Love the two additions, tentacle monster is the perfect boss. Sibling rules are great.

1. **The roster is locked at eight:** the six he named plus the Hyena Matriarch and Old Komodo.
2. **The boss is The Thing Behind the Door**, the convent's tentacled horror.
3. **The Siblings rules stand:** the toddler is never hit, they flee on a KO instead of dying, and the
   grabs that bite, stab or roll play a fling variant against them.

### Second round (Silas, 2026-10-07)

> He should be without his hand. Yes on knockout tone, this is a lighter game than the mature comic. More
> street fighter than mortal kombat. Zuzu Showdown works for me. Sounds good on defraying online for later

4. **The Coyote fights without his right hand:** the knife lashed to the stump and left-handed shooting.
5. **The tone is lighter than the comic:** Street Fighter, not Mortal Kombat. No blood, no gore, no
   fatalities; KOs are knockouts.
6. **The name is Zuzu Showdown.**
7. **Online play is a later phase.** The engine stays deterministic so rollback netplay can be added.

Every scope question is answered; t-002 is done.
