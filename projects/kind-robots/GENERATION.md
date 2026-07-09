# Generating Kind Robots objects — policy and checklists

Companion to `SECTIONS.md`. That doc covers adding *places* in the app;
this one covers generating *instances* of the primary content models —
the things agents may create automatically when a task calls for them.
The canonical spec sheets (full field tables, file paths, payload
examples) live in the kind_robots repo at **`sample/generation/`**; this
is the policy layer plus condensed checklists.

## What may be auto-generated

Per AGENTS.md, generated project art and content objects are
pre-approved when the action is task-scoped, traceable, and reversible.
Concretely:

| Object | Gate |
| --- | --- |
| Bots — NARRATOR (voice of a dream), PROMPTBOT (standalone assistant), MANAGER (voice of a PROJECT dream) | reversible — proceed when a task calls for it |
| Dreams — LOCATION, GENRE (vibe); other types as tasks require | reversible — proceed |
| Dreams — PROJECT | owned by the conductor↔dreams sync (`Dream.slug === projects/<slug>`); never invent one outside that flow |
| Characters (incl. portrait + expression art) | reversible — proceed |
| Rewards, Scenarios | reversible — proceed |
| Narration threads (NarratorThread per bot×topic) | reversible — proceed. New NarratorTopic rows change every narrator's menu: check with Silas first |
| Expression media (10 emotions + 10 actions per narrator/manager) | reversible — proceed |
| PitchSheets (incl. artist mockup) | reversible to create; the *pitch decision* stays with Silas as usual |

Publishing, deploys, billing, secrets, and destructive DB operations
remain hard gates regardless of object type.

## Universal generation rules

1. **Art is presumed.** Every generated object ships with its desired
   art — `artPrompt` always filled (it's the regeneration recipe), image
   generated via the auto art pipeline or queued in
   `projects/art-prompts.yaml`. Multiple images where the spec says so.
   Missing files never block a PR; the app falls back to placeholders.
2. **Provenance:** `creationSource: 'AI'` where the field exists,
   `designer` = the generating agent/pipeline, prompt/model/seed metadata
   kept (AGENTS.md generated-art rule).
3. **Flags:** `isPublic: true`, `isActive: true`, honest `isMature`.
   Canon content: `userId: 1`.
4. **Slugs are folders:** an object's inspiration set lives at
   kind_robots `public/images/{slug}/` (`{slug}-inspiration-{n}.webp`,
   `gallery.json` manifest) — generate candidates there, promote winners
   to canonical paths. Replaced files move to the inspiration folder,
   never deleted.
5. **API only, batch-first:** writes go through the kind_robots API with
   `KR_API_TOKEN` (`batch` endpoints upsert; expressions/threads accept
   `dryRun: true` — use it before writing). Never raw SQL.

## Condensed bundles (what "done" includes)

- **New LOCATION/GENRE dream** = dream row (pitch, description,
  flavorText, artPrompt) + card (512×768) & hero (1280×720) art +
  a NARRATOR bot + optional starter cast/loot/scenarios connected to it.
- **New NARRATOR or MANAGER bot** = bot row (botIntro with the
  framing-device stance, narrativeVoice VOICE:+SAMPLE:, forgeIntro,
  pipe-delimited userIntro) + square avatar at
  `public/images/bots/{slug}.webp` (+ `bots/avatars/` copy) + the
  20-expression set + narration threads for the active topics.
- **New character** = character row (personality/quirks/drive/backstory,
  Rarity stats) + portrait candidates in the inspiration folder → one
  promoted to `public/images/characters/{slug}.webp` + optional
  20-expression set keyed by `characterId`.
- **Expression set** = 20 square stills at
  `…/expressions/{slug}/{key}_01.webp`, all derived from the promoted
  portrait (EMOTION = face-only edit, ACTION = pose edit), ExpressionMedia
  rows with imagePath/label/emoticon/message/artPrompt. No per-expression
  ArtImage rows — the file path on the row is the source of truth for
  pixels.
- **New scenario** = row with 3–6 titled intros as a JSON string array +
  key art + dream/cast connections.
- **New reward set** = 5–12 rewards across rarities/types with card art
  each, sharing a `collection` name and folder.
- **New PitchSheet** = one per dream (dreamId unique): hook + 3
  highlights + 3 details + artist mockup (1280×720, no readable text) at
  `public/images/sheets/{dream-slug}-mockup.webp`.

## Review expectations

Reviewer checks generated batches for: filled artPrompts, honest flags,
slug/filename agreement, in-voice text (beige LLM filler is a rejection),
expression-set identity consistency, and that batch responses reported no
silent `failed` rows.
