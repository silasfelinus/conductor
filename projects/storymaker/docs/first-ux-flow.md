# Storymaker First UX Flow

## Purpose

This document sketches the first implementation-ready Storymaker user experience: starting a collaborative story session, choosing a narrator, selecting story ingredients, taking turns through branch options or custom actions, and reviewing artifacts collected during play.

This is a UX and product-flow plan only. It does not add backend schema, API routes, live data writes, deploy hooks, or publishing behavior.

## UX goals

Storymaker should feel like a lightweight game table inside Kind Robots, not a form wizard. The first flow should let a user start quickly, understand whose turn it is, make a choice without reading a manual, and leave with visible story loot: characters, items, locations, rewards, or memories that can later become reusable profile artifacts.

The MVP supports two play modes:

- Guided Adventure: a narrator Bot drives a vivid second-person story, presents branch options, accepts custom player input, and advances state.
- Limited-visibility collaboration: players contribute in sequence with bounded prior context, preserving surprise while keeping the session coherent.

## Entry points

### Project workspace card

A Storymaker card can appear in the project workspace or a future games/story area with project title, hero image, mode chips, status, and a primary Start Story or Resume Story action.

### Dream or Scenario detail

A Scenario, Character, Location Dream, or Genre Dream can offer a secondary action to start a Storymaker session from that object. This should seed the session with the selected artifact but still let the user choose narrator and mode.

### Chat surface

A Serendipity or Storymaker Bot conversation can offer a guided handoff into a session. The chat should pass the seed prompt into the session-start flow rather than inventing a separate story state.

## Session start flow

### Step 1: choose mode

The first screen asks what kind of story the user wants to make.

Guided Adventure is best for solo or small-group play. The narrator offers choices and reacts to custom actions.

Limited-visibility collaboration is best for async group play. Each player sees limited prior context and the whole story is revealed as the session unfolds.

The selected mode determines the later turn UI, but the rest of setup should stay shared.

### Step 2: choose narrator

The narrator picker shows Bot cards with avatar, name, narrative voice, tone chips, and a sample intro line.

Default narrator profiles:

- Kind narrator: warm, vivid, encouraging.
- Mischief narrator: playful and surreal while staying safe.
- Mystery narrator: atmospheric and puzzle-forward.

The MVP can use existing Bot records or a hard-coded narrator catalog until app-owned Storymaker settings exist. The UI should make it clear that the narrator is the voice of the session, not necessarily a player.

### Step 3: choose story seed

The seed screen lets the user compose a starting prompt from existing Kind Robots concepts:

- Scenario
- Character
- Location Dream
- Genre Dream
- vibe or flavor tags
- optional freeform premise

The MVP should provide three seed styles:

1. Pick from library: choose Scenario, Location, and Genre cards.
2. Surprise me: roll from available Dreams and a narrator suggestion.
3. Custom spark: user enters one sentence; optional library picks enrich it.

The future implementation should turn this into a story seed object containing mode, narrator bot slug, optional scenario/location/genre slugs, character slugs, vibe tags, and premise.

### Step 4: confirm table

Before starting, show a compact confirmation panel with mode, narrator, seed summary, players, visibility rules, and safety rules.

Primary action: Begin Story.

Secondary action: Save Draft.

## Guided Adventure turn flow

### Layout

A Guided Adventure session screen should use a three-zone layout:

1. Story panel: current narrative beat, streamed or rendered as prose.
2. Choice panel: branch options and custom action input.
3. State panel: inventory, companions, location, active goals, collected artifacts.

On mobile, the state panel should collapse below the story and choices.

### Turn sequence

1. Narrator renders the current scene.
2. System shows 2-4 branch options.
3. User picks an option or writes a custom action.
4. Optional spend or reward prompt appears when relevant.
5. User confirms.
6. State preview shows what may change.
7. Narrator advances to the next scene.
8. New artifacts are added to the session collection.

### Branch option card

Each branch option should include a short title, one-sentence consequence hint, risk or tone badge, and optional stat or reward cost.

Example option: Follow the glowing fox. You leave the market path and trust a creature that clearly knows more than it admits. Badge: Wonder / Unknown.

### Custom action input

The custom input should invite play without breaking the game.

Placeholder: Try something clever, kind, bold, or beautifully strange.

The confirmation step should normalize custom input into a bounded turn request: declared action, scene id, inventory, safety boundaries, and max mutation scope for this turn.

## Limited-visibility collaboration turn flow

### Layout

This mode should focus on turn ownership and mystery:

1. Prompt shard: what this player is allowed to see.
2. Contribution box: the player's text, choice, or artifact addition.
3. Constraint chips: tone, length, hidden reveals, required motif.
4. Reveal timeline: locked or partial previous segments.

### Turn sequence

1. System determines next contributor.
2. Player receives only the visible shard.
3. Player writes a contribution or chooses from optional prompts.
4. System validates length and safety limits.
5. Contribution is locked.
6. Turn passes to next player.
7. Reveal rules decide what everyone can see.

### Visibility states

- Hidden: not visible until reveal.
- Shard: short excerpt or last line only.
- Summary: narrator-safe summary of prior events.
- Full reveal: visible after the round or story completes.

The MVP can implement these as display rules before building deeper permission logic.

## Artifact review flow

At any point after the first few turns, the user should be able to open Collected Artifacts.

Artifact categories:

- Characters met
- Items found
- Locations discovered
- Rewards earned
- Story memories
- Branches not taken

Each artifact card should show name, type, rarity or importance, source turn, short description, and future-use status: Session Only, Save Candidate, or Saved to Profile.

For MVP planning, artifacts remain session-scoped until a later persistence task explicitly saves them to profile models.

## Session resume flow

Resume should answer three questions immediately:

1. Where was I?
2. Whose turn is it?
3. What can I do now?

Resume card fields: session title, mode, narrator, last updated, current location or scene, waiting player, and collected artifact count.

Primary action is Continue if it is the user's turn, or Watch/Review if waiting on someone else.

## Empty, loading, and blocked states

No narrator available: show a friendly empty state and fallback to a default local narrator profile.

No library seeds available: offer Custom Spark and Surprise Me from built-in prompt fragments.

Waiting on another player: show the last visible story state, the expected next player, and any open artifacts. Do not expose hidden content.

Session needs human approval: for any future flow that touches real task queues, publishing, profile persistence, or irreversible writes, show a needs-human banner and disable the action until approved. This UX plan itself does not implement those writes.

## Minimal component map

A future implementation can start with these app-owned components:

- StorymakerStartPanel.vue
- StorymakerModePicker.vue
- StorymakerNarratorPicker.vue
- StorymakerSeedPicker.vue
- StorymakerSessionShell.vue
- StorymakerStoryPanel.vue
- StorymakerChoicePanel.vue
- StorymakerArtifactTray.vue
- StorymakerResumeCard.vue

Suggested store responsibilities:

- hold session setup draft state
- hold current session state
- provide narrator, seed, turn, artifact, and resume helpers
- own all future API calls so components do not call API routes directly
- support local mock fixtures before schema or API work exists

## MVP cut line

Include in first prototype:

- mode picker
- narrator picker
- seed picker
- session shell
- Guided Adventure choice panel
- limited-visibility contribution box
- artifact tray with session-scoped mock artifacts
- resume card

Defer:

- real profile persistence
- real invitation system
- real task or honeydo write-back
- publishing or sharing
- database migrations
- paid or external integrations

## Verification checklist for implementation

A future implementation PR should demonstrate:

- starting a Guided Adventure draft from a seed
- choosing a narrator
- showing a scene with choices and custom input
- adding a mock artifact to the tray
- resuming an in-progress session
- starting a limited-visibility collaboration draft with bounded visibility copy
- no direct component API calls; state flows through a store
- no live endpoint, schema, secret, deployment, or production data changes

## Follow-up candidates

- Build the first StorymakerStartPanel.vue prototype with local mock data.
- Draft the Storymaker Pinia store contract and mock session fixture.
- Convert the artifact tray into a reusable profile-save review surface.
