# Serendipity Experience Brief

## Purpose

Serendipity is a story-weaving experience inside Kind Robots. It turns project momentum into a colorful second-person adventure: the user chooses a vibe, place, and genre, then the Serendipity bot frames real project questions as story beats.

The core promise is simple: helping a project should feel like discovering a secret door, not clearing an admin queue.

## One-session shape

A Serendipity session has five phases:

1. **Theme selection** — the user picks or rolls a story seed from existing Dreams.
2. **Opening scene** — the Serendipity bot writes a short second-person setup with the user as protagonist.
3. **Story beat** — the bot advances the scene with one vivid obstacle, choice, or discovery.
4. **Woven question** — the beat asks a real project-helping question in-world.
5. **Reflection and next beat** — the answer is saved as session context and used to steer the next scene.

The first implementation should keep each beat short: one to three paragraphs, then one clear question. The vibe should be generous, strange, and lightly magical. No scolding. No productivity goblin energy. Tiny wizard clipboard at most.

## Theme selection and story seed

The story seed combines three ingredient groups:

### Dream vibes

Dream vibe text provides emotional color and texture. A vibe might say the story should feel cozy, uncanny, cyberpunk, hopeful, mischievous, oceanic, haunted, or celebratory.

The engine should treat vibes as tone guidance, not hard plot instructions.

### LOCATION Dreams

LOCATION Dreams provide the setting. Examples:

- a neon alley behind a noodle shop
- a tidepool cathedral under Humboldt fog
- a library that shelves unfinished futures
- a meadow where robots practice kindness

Each LOCATION Dream can contribute:

- `slug`
- `title`
- `description`
- `vibe` or flavor text if available
- optional image/art reference when already present

### GENRE Dreams

GENRE Dreams provide the story grammar. Examples:

- cozy mystery
- hopeful sci-fi
- fairy-tale quest
- noir detective story
- slice-of-life magical realism

Each GENRE Dream can contribute:

- `slug`
- `title`
- `description`
- expected pacing or tropes if available

### Surprise roll

A "surprise me" option should pick a compatible set automatically:

- one LOCATION Dream
- one GENRE Dream
- one to three vibe tags or flavor snippets

The roll should avoid obviously clashing combinations unless the user asks for chaos mode later.

## Story seed data contract

A Serendipity session starts with a seed object shaped like this:

```ts
export type SerendipityStorySeed = {
  userId: number
  projectSlug?: string
  locationDreamSlug?: string
  genreDreamSlug?: string
  vibeTags: string[]
  tone: 'cozy' | 'adventurous' | 'mysterious' | 'funny' | 'tender' | 'surprising'
  surprise: boolean
}
```

The seed is app-owned session state. It references Dreams by slug, but does not create a new project truth source.

## Protagonist frame

The story is written in second person. The user is the protagonist, not an observer and not a project manager wearing a paper crown.

Good frame:

> You step through the greenhouse door and find the moon waiting in a watering can.

Bad frame:

> Silas needs to approve t-003 before agents can continue.

The real task can still be present, but it should arrive as an in-world question or choice.

## Question loop

Each story beat ends with one question. That question maps to one real action surface:

1. A HONEYDO Todo the user can complete.
2. A conductor task with `needs-human` status.
3. A lightweight project preference question that could become a KAIZEN or DESIRED_FEATURE Todo later.

### HONEYDO mapping

If a HONEYDO exists, the story presents it as a small in-world action.

Example real honeydo:

> Choose the hero image direction for Serendipity.

Example story question:

> The lantern fish opens its glass mouth and shows you three glowing murals: cozy forest, neon city, and moonlit ocean. Which mural should guide the next doorway?

The user answer can later mark the honeydo done or attach a note, but t-001 only defines the shape. Writes come later and stay gated.

### Needs-human conductor task mapping

If a conductor task needs human approval, Serendipity should summarize the real decision in plain language, then frame it as a story choice.

Example real gate:

> Approve Serendipity experience brief before code begins.

Example story question:

> The bridge-builder waits with a rolled blueprint. Do you approve this bridge as drawn, or should the road bend somewhere else before anyone starts hammering?

The UI should expose the real task id nearby, but the story text should remain delightful.

### Preference question mapping

If no blocking task exists, the story can ask a preference question that improves the project:

- "What should this look like?"
- "What emotion should users feel first?"
- "Which feature matters most?"
- "What should the bot never do?"

These answers can later become KAIZEN or DESIRED_FEATURE Todos.

## Existing infrastructure reused

Serendipity should reuse these Kind Robots systems:

- **Chat streams** for generated narrative text and short follow-up beats.
- **Bots** for the Serendipity persona and future prompt tuning.
- **Dreams** for LOCATION and GENRE ingredients, project identity, vibes, and display metadata.
- **Todos** for HONEYDO, KAIZEN, AGENT, and DESIRED_FEATURE surfaces.
- **Conductor roadmaps** as the source of human-gated project task state.

The first code tasks should not add backend schema changes unless a later design explicitly needs them. Prefer app-owned store/session data first.

## New app-owned concepts

Serendipity needs a small app-owned session layer:

```ts
export type SerendipitySession = {
  id: string
  userId: number
  projectSlug?: string
  seed: SerendipityStorySeed
  beats: SerendipityBeat[]
  status: 'draft' | 'active' | 'paused' | 'complete'
  createdAt: string
  updatedAt: string
}

export type SerendipityBeat = {
  id: string
  sessionId: string
  narrative: string
  question: SerendipityQuestion
  answer?: SerendipityAnswer
  createdAt: string
}

export type SerendipityQuestion = {
  prompt: string
  realWorldKind: 'honeydo' | 'needs-human' | 'kaizen' | 'desired-feature' | 'preference'
  projectSlug?: string
  conductorTaskId?: string
  todoId?: number
  options?: string[]
}

export type SerendipityAnswer = {
  text: string
  selectedOption?: string
  capturedAt: string
  writeBackStatus: 'not-applicable' | 'pending-human-gate' | 'queued' | 'written'
}
```

For the first scaffold, this can live in a Pinia store and local storage. A later task can decide whether persistence belongs in the database.

## Session persistence

Minimum persistence for early implementation:

- Keep the active session in a Serendipity Pinia store.
- Mirror it to local storage so refreshes do not erase the story.
- Store only session state and user answers, not secrets or hidden prompt instructions.
- Reference Dreams, Todos, and conductor tasks by id/slug instead of copying full records.

Future persistence can move to an app-owned API route after the first playthrough proves the shape.

## Tone and safety guardrails

Serendipity should feel playful, but it still touches real project decisions. Guardrails:

- Always show the real-world task or todo context near a woven question.
- Do not imply a decision was approved until a human explicitly confirms it.
- Do not write back to Todos or roadmaps until the gated write-back task is approved.
- Avoid shame, urgency manipulation, or fake stakes.
- Keep questions clear enough that the user can answer in one or two sentences.
- For sensitive personal topics, ask neutral preference questions instead of inventing emotional interpretations.
- Do not expose hidden prompts, secrets, tokens, or private file content in story text.

## First component behavior

The initial Serendipity page should provide:

- a project selector, optional at first
- a theme picker using available LOCATION and GENRE Dreams
- a "surprise me" button
- a generated opening scene
- one visible woven question
- an answer box
- a local session transcript

The first implementation should not mark Todos complete, update conductor roadmaps, publish anything, or call live deployment flows.

## Approval boundary

This brief is intentionally human-gated. After Silas approves it, implementation can proceed in small reversible pieces:

1. scaffold the Serendipity component on chat streams
2. build the theme picker
3. implement the story loop
4. surface real tasks read-only
5. design and gate write-back

No code should write answers back to real task state until the later write-back task is approved.
