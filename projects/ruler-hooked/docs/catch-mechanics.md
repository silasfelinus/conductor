# The Ruler Is Hooked — catch mechanics contract

Date: 2026-08-26
Source: Silas-directed vertical-slice implementation follow-up

## Goal

Turn the authored fish behaviors into **distinct playable catches** without building fifteen
unrelated minigames.

The fishing interaction should still feel like The Ruler Is Hooked: image-forward,
readable, funny, deterministic, mobile-friendly, and easy to port to a future offline
packaged build. The player should learn what a fish is doing from its visual cue and make
small meaningful responses rather than perform a generic progress-bar grind.

## Core decision: beat-based fishing, not twitch fishing

A catch resolves over a short sequence of **fishing beats**. A beat is a deterministic
micro-turn inside one cast, not a real-world timer gate.

Typical actions are:

- `REEL` — gain line progress but increase tension;
- `SLACK` — reduce tension and surrender a little progress;
- `WAIT` — hold position and observe the fish;
- a fish-specific contextual action when the encounter calls for one, such as
  `STRIKE`, `FOLLOW_LEFT`, `FOLLOW_RIGHT`, or a legendary encounter choice.

The fish presents a readable cue before the player acts. The engine then advances one
beat using the fish profile, current fight state, player action, and seeded RNG.

This has several advantages:

1. It keeps outcomes reproducible from the same run seed and sequence of player actions.
2. It works equally well with mouse, touch, keyboard, and controller.
3. It avoids turning an otherwise contemplative slideshow game into a reflex test.
4. It makes unusual fish mechanics legible rather than hiding them inside milliseconds of
   animation timing.
5. Animations can still make each beat lively without animation timing becoming the source
   of truth for game outcome.

Real-time visual flourish is welcome. **Real-time elapsed milliseconds must not determine
species availability or canonical catch outcome.**

## Shared fight state machine

Every cast uses the same high-level state machine:

```text
CAST
  -> APPROACH
  -> HOOK_WINDOW
  -> FIGHT (1..N beats)
  -> LANDED | ESCAPED
  -> RECORD
  -> KINGDOM_INTERRUPT
```

A fish may collapse or extend stages, but it should not invent a parallel lifecycle.

### `CAST`

The engine has already selected an available species from kingdom ecology, habitat, gear,
and seeded rarity weighting. The player does not know the result yet unless the species
reveals itself early.

### `APPROACH`

Optional pre-hook behavior. Examples: Sunspoke Koi circles until the player waits;
Lamplight Angler presents a false lure; The Pleasant Island initially reads as scenery.

### `HOOK_WINDOW`

The player commits to the hook. Some species hook immediately; others require a cue or
short pattern.

### `FIGHT`

A compact series of beats. The common state includes:

- `progress` — 0..100 toward landing the catch;
- `tension` — 0..100 line strain;
- `beat` — deterministic micro-turn count;
- `phase` — authored phase key for multi-stage species;
- `fishEnergy` — optional 0..100 resistance budget;
- `modifiers` — temporary profile-specific state;
- `history` — player actions and revealed cues needed for deterministic replay/debugging.

### `LANDED`

Generate/finalize specimen properties, update catch count and personal bests, and reveal
Fishopedia consequence text when appropriate.

### `ESCAPED`

The cast still consumes the kingdom turn unless a later design explicitly creates a
non-turn practice mode. An escaped known or visibly identified fish may support the
Fishopedia's future **discovered but not caught** state.

### `RECORD`

Persist fight result and enough history to reproduce/debug it. Do not store wall-clock
fight duration as game logic.

### `KINGDOM_INTERRUPT`

The existing card/arc loop continues after the fishing beat. Fishing remains the action
that advances the reign; governance keeps interrupting the ruler's preferred hobby.

## Composable behavior vocabulary

Fish are built from a small set of reusable behavior primitives. A species can combine
several primitives and tune parameters without requiring new engine code.

### Approach / hook primitives

- `IMMEDIATE` — normal readable strike; baseline species.
- `PATIENCE` — aggressive input delays the bite; `WAIT` creates the hook window.
- `RHYTHM` — player follows a short authored/seeded sequence of cues.
- `DECOY` — an obvious false target appears before the real hook window.
- `SCENERY_REVEAL` — encounter begins as part of the environment, then changes scale/state.
- `ATTACHED` — the target arrives attached to or entangled with another catch.

### Fight primitives

- `STANDARD_TENSION` — reel to advance while keeping tension inside a safe band.
- `LOW_TENSION` — high tension strengthens the fish or stalls progress.
- `SLACK_WINDOW` — explicit cues require `SLACK` or `WAIT`; reeling is punished.
- `REVERSE_CONTROL` — a clear cue temporarily swaps the meaning/direction of an input.
- `LATERAL_BURST` — cue a left/right run and ask the player to follow it.
- `HEAT_PULSE` — tension becomes temporarily dangerous during visible heat phases.
- `DEAD_SLACK` — line abruptly appears dead; acting before a wake cue loses progress.
- `AUDIO_TELL` — sound cue forecasts the next movement; always pair with a visual cue for
  accessibility.
- `MULTI_BODY` — one Fishopedia species is represented by several coordinated bodies.
- `MULTI_PHASE` — authored phase transitions change rules during one encounter.

### Resolution primitives

- `SINGLE_SPECIMEN` — normal landed fish.
- `GROUP_SPECIMEN` — several bodies count as one species entry/specimen event.
- `RESCUE_OR_TAKE` — player chooses which of two entangled creatures/results to prioritize.
- `LEGENDARY_STAGE` — the encounter changes the lake presentation and resolves through
  several explicit phases rather than a normal fish lane.

## Vertical-slice behavior mapping

The first fifteen species should map onto the shared vocabulary as follows.

| Fish | Hook / approach | Fight | Resolution | Signature lesson |
| --- | --- | --- | --- | --- |
| Parlour Rustfish | `IMMEDIATE` | `STANDARD_TENSION` | `SINGLE_SPECIMEN` | Teaches the baseline rules. |
| Choirfish | `RHYTHM` | `MULTI_BODY` + `STANDARD_TENSION` | `GROUP_SPECIMEN` | Read three musical cues as one coordinated catch. |
| Sunspoke Koi | `PATIENCE` | `STANDARD_TENSION` | `SINGLE_SPECIMEN` | Stop pulling to create the opportunity. |
| Orchardjaw Perch | `IMMEDIATE` | `STANDARD_TENSION` | `SINGLE_SPECIMEN` | Easy catch with specimen variation as reward. |
| Bridgeback Sturgeon | `IMMEDIATE` | `LOW_TENSION` | `SINGLE_SPECIMEN` | Bigger does not mean pull harder. |
| Crown-of-Reeds Pike | `IMMEDIATE` | `MULTI_PHASE` + `SLACK_WINDOW` | `SINGLE_SPECIMEN` | Protect the living crown during still phases. |
| Errand Guppy | `IMMEDIATE` | `LATERAL_BURST` | `SINGLE_SPECIMEN` | Follow sharp movements; cargo adds collectible flavor. |
| Moebius Crab | `IMMEDIATE` | `REVERSE_CONTROL` | `SINGLE_SPECIMEN` | The rules visibly turn inside out for one phase. |
| Masquerade Ray | `PATIENCE` | `LATERAL_BURST` | `SINGLE_SPECIMEN` | Slow, theatrical directional reads. |
| Tollbell Sturgeon | `IMMEDIATE` | `AUDIO_TELL` + `LATERAL_BURST` | `SINGLE_SPECIMEN` | Bell/visual cue forecasts the run. |
| Drowned Carp | `IMMEDIATE` | `DEAD_SLACK` | `SINGLE_SPECIMEN` | Do nothing while the line is corpse-still. |
| Lamplight Angler | `DECOY` | `STANDARD_TENSION` | `SINGLE_SPECIMEN` | Do not strike the obvious light. |
| Ashbelly Gar | `IMMEDIATE` | `HEAT_PULSE` + `SLACK_WINDOW` | `SINGLE_SPECIMEN` | Give line during visible heat pulses. |
| Tithe Lamprey | `ATTACHED` | `STANDARD_TENSION` | `RESCUE_OR_TAKE` | Extraction becomes a literal player choice. |
| The Pleasant Island | `SCENERY_REVEAL` | `MULTI_PHASE` | `LEGENDARY_STAGE` | The entire lake becomes the encounter. |

The mapping is a starting contract, not a ban on tuning. New species should prefer
combinations of existing primitives before adding another engine concept.

## Difficulty and rarity are separate

Rarity controls **how unusual a species is to encounter**, after ecology and habitat have
made it eligible. Difficulty controls **how demanding its catch profile is**.

Do not assume COMMON means trivial or LEGENDARY means merely a larger health bar.
Legendary encounters should generally have stronger presentation, phase structure, or
world significance, while a strange COMMON fish can still have a memorable rule.

Suggested profile fields:

```ts
interface CatchProfile {
  approach: ApproachPrimitive[]
  fight: FightPrimitive[]
  resolution: ResolutionPrimitive
  beats: { min: number; max: number }
  safeTension?: { min: number; max: number }
  progressPerReel?: number
  slackRecovery?: number
  cueStrength?: number
  phases?: CatchPhase[]
}
```

The exact TypeScript shape may evolve. The important contract is composition rather than
fifteen hard-coded branches.

## Deterministic cue generation

For a given save state, selected fish, encounter seed, and action history:

- the cue sequence must be reproducible;
- any random left/right run must come from the encounter RNG;
- specimen size/quality should be finalized from deterministic values;
- replay/debug mode should be able to reconstruct the fight from seed + action history.

Animation frame rate, device speed, network state, and real-world clock must not alter the
canonical result.

## Fishopedia interaction

The Fishopedia should teach behavior gradually without becoming a wiki that solves every
fish before the player meets it.

Before catch:

- unknown species: silhouette or `?` only;
- lore-discovered species: vague habitat/behavior hint, no exact solution.

After first catch:

- reveal the field note and kingdom consequence;
- add a concise behavior observation such as “pulling hard makes it settle” or “the false
  lamp bites first”;
- keep exact numeric thresholds internal.

Repeated catches can support personal bests and later mastery badges without blocking
progression.

## Accessibility

Every mechanically relevant cue must have at least two channels when practical:

- color + shape/text/icon;
- sound + visible pulse/icon;
- movement + explicit state label.

Do not make hearing, fine pointer movement, rapid tapping, or color discrimination a
requirement for landing a species. Reduced-motion mode should preserve the same decisions
with quieter transitions, not replace catches with automatic success.

## Implementation sequence

1. Add a generic `FishingEncounter` state and reducer with `REEL`, `SLACK`, `WAIT`, and
   contextual actions.
2. Implement the baseline `STANDARD_TENSION` encounter using Parlour Rustfish.
3. Add behavior primitives one at a time, with deterministic reducer tests.
4. Map all fifteen vertical-slice species onto profiles.
5. Render a single reusable fishing panel whose cues/layout adapt to the profile.
6. Add discovered-but-not-caught Fishopedia state when an identified fish escapes.
7. Add visual/audio polish after the reducer behavior is proven.
8. Give The Pleasant Island a dedicated presentation layer while keeping it on the same
   encounter state machine.

## Slice acceptance

The interaction slice is complete when:

- a normal cast can land or lose a fish through player choices rather than automatic
  resolution;
- the same encounter seed + action sequence reproduces the same cues and result;
- all fifteen fish use data profiles composed from shared primitives;
- no species needs a one-off fork in the top-level turn loop;
- at least the baseline, patience, reverse-control, slack-window, decoy, and legendary
  families are visibly and mechanically distinct;
- touch, keyboard, reduced-motion, and non-audio play remain viable;
- kingdom interruptions still occur after the fishing attempt without bypassing the
  existing narrative loop.
