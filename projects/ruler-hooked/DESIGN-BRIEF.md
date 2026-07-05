# The Ruler is Hooked — Design Brief

date: 2026-07-05
source: Silas, in session (verbatim pitch preserved below in spirit; this brief structures it)
kind: software
slug: ruler-hooked

## The one-liner

A fishing/kingdom-management simulator told in slideshow format. You are the
King (or Queen, or other) of a country — and you don't want to rule. You want
to fish all day. So you perch at the edge of a beautiful lake behind your
castle and start fishing, while the kingdom keeps interrupting.

## The core loop

1. **You fish.** The play screen is a composited landscape: roughly half
   nature view, built from several specific, changeable areas (sky, treeline,
   far shore, village edge, castle grounds — exact regions TBD in the
   compositing spec).
2. **The kingdom interrupts.** Occasionally a kingdom task is handed to you as
   a card/slide: a choice with real consequences. Example from the pitch: a
   warlock land developer wants in — or you release the area to Druid
   preservationists.
3. **Choices reshape the world.** Each choice moves one or more kingdom-health
   sliders, and slider states swap the artwork of specific landscape regions.
   Different runs produce visibly different worlds. The play screen is one
   image merged from the current state of every region's layer.
4. **Repeat.** Fish, get interrupted, choose, watch the world drift toward
   what you've made of it.

## Format and stack

- **Slideshow / card / image-focused web app first.** JavaScript front end
  with a backend — this is the proof of concept and a major milestone in
  itself. App-store packaging can follow the web version.
- **Future goal:** full Steam game; migration target is Unreal. Nothing in the
  PoC should be architected in a way that makes the content (decks, regions,
  character data, save format) unusable in that migration — keep game content
  as data, not code.
- **Offline-playable final game.** AI is used for asset generation and
  inspiration during development, but there are NO live LLM interactions at
  runtime. This is intentionally different from the usual kind_robots
  projects: the shipped game runs without an internet connection.
- **Save system from the start:** multiple named saves per player.

## Time (Silas, 2026-07-05 — design pillar)

**Zero time-locked activities. Play at your own pace — iterative play.**

- There is **no clock**. Not a hidden one either. Actions may advance a
  presented "day" for flavor if we ever want one, but nothing in the game is
  ever locked out of experience because time progressed. No missable
  content, no expiring choices, no "you slept through it." The player can
  put the game down mid-decision and pick it up next month unchanged.
- **Day/night is a visual cycle, not a timer.** Plan for a day/night cycle
  driven by play (turns/actions), and expect to generate **multiple
  time-of-day variants of every kingdom landscape piece** — each region's
  states multiply across times of day.
- **Transient beauty states are the surprise-and-delight layer:** morning
  dew and golden hour appear only briefly before transitioning into daytime
  or nighttime. They are short-lived *visuals* — a treat you happen to catch,
  never a window that gates content. If something special happens at golden
  hour, it must also be reachable outside it.

## Art direction

Cartoony and goofy. Exaggerated stereotypes of good and evil — but always
with wry twists, and characters that are nuanced underneath the archetype.
Reference points from Silas: Monkey Island, Bakshi, Treasure Planet, Steven
Universe, She-Ra: Princess of Power, and Prime Monster (see below).

## Primary UI/structure reference: Prime Monster

Prime Monster (Steam: https://store.steampowered.com/app/3214480/Prime_Monster/)
is the closest existing model for how this game should *work*, per Silas
(2026-07-05, in session — he's played it and found it charming):

- **Card-based selections** with a playful interface.
- **Delightful moral decisions from the perspective of honestly evil
  characters** — its hunting-versus-farming debate is whether humans should
  be hunted as food or farmed as a sustainable crop. That register (comically
  frank villainy with real decision weight) is the tone target for our
  warlock/druid-style choices.
- **Vibrantly alive without a controllable character animation:** everything
  is pre-baked, presented as navigable screens. No avatar to steer — the
  world feels alive through the screens themselves.
- "It works and it was fun" — treat it as proof that the slideshow/card/
  composited-image format carries a full game, not just a prototype.

Agents implementing the play loop should study its store page/screenshots for
the goal-type UI feel; the PoC's bar is that same navigable-screens
liveliness.

## Characters and narrative decks

- Game characters get entries in the kind_robots **Character** model — or
  reuse pre-existing Characters where they fit.
- Different characters and events appear on different run-throughs: narrative
  decks keyed to characters (e.g., the ruler's child wants to elope) so
  replays surface different arcs. The deck format should make adding an arc a
  content task, not a code task.

## What "proof of concept" means (m2 exit criteria)

- A playable web session: fish, receive event cards, make choices.
- At least two landscape regions with at least two visual states each,
  composited live into one play screen that visibly responds to choices.
- One complete narrative arc with a character (plus the warlock/druid choice
  from the pitch).
- Save/load with multiple save slots.

## Boundaries

- No app-store submission, no Steam page, no payments, no deploys without
  explicit approval from Silas — standard hard gates apply.
- Asset generation goes through the normal conductor art pipeline
  (art-prompts.yaml / ART-PROMPTS.md), not committed agent-generated binaries.

## Status

This is a bucket-list project of Silas's, pitched directly in session
2026-07-05. Per the 2026-07-04 soft-scope rule, work starts immediately;
scope confirmation (t-002) runs in parallel as a soft needs-human.
