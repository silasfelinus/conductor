# Zuzu's Lair — Design Brief

date: 2026-10-06
status: draft v1 (agents build from this; Silas confirms or redirects at t-002)
author: Claude (from Silas's request, 2026-10-06)

## Silas's ask (verbatim)

> And finally this one will need its own independent project: dragons lair. This will use a quick time
> system, with our animation creator making multiple paths depending on buttons pressed in time or not.
> This can use our character zuzu as we already have some work done with the characters, create first
> and last animations that then branch into success and death animations. Will need sound, optional on
> screen button and flash assist, etc.

## What it is

A quick-time animated adventure in the spirit of the 1983 laserdisc classic: the player watches Zuzu
move through a short, gorgeous, hand-animated-looking chapter, and at each danger has a fraction of a
second to press the right direction or the sword button. Press in time and the next animation picks up
where the last left off. Miss, or press the wrong thing, and a short death animation plays, a life is
lost, and the moment replays. Clear every moment and the closing animation plays.

It riffs on the *format* only (branching full-motion animation plus timed inputs), never on the original's
characters, scenes, name or music. It is its own project, not an arcade cabinet, because its content
pipeline (keyframes, clips, score) is the comic-film pipeline, not the code-drawn arcade engine. It can
still borrow the arcade's input, sound, leaderboard and mobile play lock.

## Who it serves

Anyone on Kind Robots, free in the browser, on phone, tablet or desktop. It is also a showcase for the
animation creator: a story told only through generated animation, where the viewer's timing chooses the
path.

## The character

**Zuzu**, the koala ronin from the comic `zuzu-koala-assassin-01`. The comic folder is the canon and
the guardrails (VIDEO-GUARDRAILS.md, CAST-PICKS.md) apply to every keyframe and clip:

- **Build:** short and stocky, koala-sized, Danny DeVito proportions, a slight paunch.
- **Kit:** rust-brown poncho with orange zigzag trim, a conical straw kasa shading the eyes, dark tunic, orange sash, dark brown cloth trousers.
- **Sword:** a katana strapped across his back, hilt above the right shoulder.
- **Manner:** always serious, Eastwood stillness.
- **References:** the locked 8-angle set (front 242395, 3/4 front left 242397, profile left 242193, 3/4 back left 242113, back 242117, 3/4 back right 242120, 3/4 front right 242399).
- **Render path:** keyframes use the comic house lane (`il-arthemy`) and its prefix, suffix and negatives, not Krea.
- **No words on screen:** no dialogue and no narration; the only words are diegetic signs and the title card.
- **bannedTerms:** copy the comic's list into every clip spec. In prompts, name the species, never "people".
- **Literal-word traps:** "duster", "muzzle", "squat" (use "chubby, standing upright") and "mother".

This is an original side adventure, not Book One. It must not reveal or depend on the buried twist.

## How it plays

1. **Opening animation** (the "first animation"): Zuzu walks into the danger. There is no input yet.
2. **A chain of moments.** Each moment is one clip that runs up to the danger and opens an *input window*
   (for example 0.8 s on Classic, 1.6 s on Assist) asking for one of UP, DOWN, LEFT, RIGHT or SWORD (A).
   - **Right press in the window:** the moment's *success clip* plays, then the next moment.
   - **Wrong press, or the window closes:** the moment's *death clip* plays, a life is lost, and the
     moment restarts from its own clip. Out of lives means a game over, with an option to continue from the
     last moment at a score penalty.
3. **Closing animation** (the "last animation"): Zuzu walks out of the danger. Then the score and time,
   and initials for the leaderboard.

Scoring rewards fast, clean play: points per moment scale with how early in the window you pressed, plus a
no-death bonus and a time bonus. Scores reuse the arcade's `ArcadeScore` board under the slug
`zuzu-lair`.

### Assists and options (all player-toggleable, remembered per browser)

- **Flash assist:** during the window the needed direction glows on screen, the way the arcade original's
  lit-up hints did. It is on by default on Assist difficulty and off on Classic. With
  `prefers-reduced-motion` the hint glows steadily instead of flashing, and it never strobes faster than 3 Hz.
- **On-screen buttons:** a touch d-pad and SWORD button. They are on by default for coarse pointers and
  can be toggled anywhere. Keyboard (arrows/WASD plus Space) and gamepads always work.
- **Difficulty:** Assist (wide windows, flash on, unlimited continues) or Classic (tight windows, flash
  off, 3 lives).
- **Sound:** clip audio, a weird-west score, and short stingers for success and death. Sound on/off.
- **Subtitles:** none are needed (there is no dialogue). The input prompt is an icon, not text.

### Mobile

It reuses the arcade's touch-play lock (silasfelinus/kind_robots#3276): while playing, the player pins
to the viewport, scrolling locks and gestures are swallowed. The video stays one size the whole time.

## Content pipeline

Each chapter is one `SCENES.yaml` graph (see `chapters/01-dry-gulch/SCENES.yaml`). It lists every
clip with:
- a keyframe prompt (house-lane tags, built on the canonical Zuzu string);
- a motion prompt (prose: one camera move plus one action);
- for moments, the input window and the expected button.

The clips are produced by the comic-film / music-video pipeline:
- a kind_robots spec (`utils/musicVideoSpecs.ts` style, `kind: film`);
- keyframes in the house lane;
- LTX image-to-video clips (`ltx-12gb-balanced`, about 4 s at 1280×720).

Death and success clips start from the moment's last frame, using music-video t-026's last-frame
pinning, so the branch cuts are seamless.

**Budget:** chapter 1 is about a dozen clips, roughly one overnight render on the single 12 GB card.
Until the clips land, the player runs on placeholder stills with Ken Burns motion, so the whole
loop is buildable and testable on day one.

Renders are private ArtImages. Making them playable publicly is the `publish` gate (t-011).

## MVP scope (chapter 1, "The Dry Gulch")

- An opening animation, four moments (each with a success and a death clip) and a closing animation:
  about 10 to 12 clips.
- A player page on the Kind Robots Projects tab, with keyboard, gamepad and touch input, flash assist,
  on-screen buttons, difficulty, sound, lives, score and leaderboard.
- A pure, contract-tested QTE engine: the scene graph, input windows and branch resolution.

## Out of scope / guardrails

- Never the original's name, characters, art, music or scene designs; the riff is the format only.
- No dialogue or narration, per the comic's rules.
- Nothing from the Book One twist; bannedTerms on every clip.
- **Deaths are quick, stylized and cut away**, in the spirit of the format's slapstick deaths but in
  Zuzu's grittier tone. Examples: the kasa spinning down into the gorge, dust settling over a still
  poncho, a cut to black on the strike. Never gore; injuries stay implied.
- No money. Renders run on our own Comfy backend.
- Publishing the clips publicly is a human gate.

## Open questions for Silas (t-002, soft; nothing waits on these)

1. **Chapter story.** The draft is "The Dry Gulch": rope bridge, scorpion, rockslide, gila-monster
   bandit. Keep it, or tie it to a Book One location?
2. **Tone of the death animations.** The draft is quick and stylized, cut away before anything
   graphic. Do you want more slapstick or more grit?
3. **Home.** Its own tab under Projects (the draft), or also a cabinet tile in the Arcade hall that
   links to it?
4. **Length.** Grow it chapter by chapter as a recurring task, the way the arcade factory does, or
   finish after chapter 1?
