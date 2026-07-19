# Manager and Assistant bot parity spec

Every active project should be able to point at one primary companion bot using the **existing** Kind Robots Bot/narrator framework — no new models, no second menu system. This document is the concrete contract for that wiring: which `BotType` to pick, what the avatar and twenty-portrait image set must contain, how narrator topics/threads become the project's navigation menu, and how a project links to its bot. It replaces guesswork with field-level detail so `t-006` can turn gaps into small, correctly-scoped implementation tasks routed to the owning project.

This spec documents an existing framework; it does not create one. All fields below are real `kind_robots` Prisma fields as of this writing — verify against the live schema before implementing, since projects evolve (see `CONTROL.md` "Briefs are direction, not contracts").

## 1. botType selection

`Bot.BotType` is a free string by convention, not a DB enum. Use exactly one of these canonical values per bot:

| BotType | When to use | Owning link |
| --- | --- | --- |
| `MANAGER` | The bot's job is coordinating a **Project**: status, queues, approvals, task surfaces, "what's next." | `Project.managerBotId` → `Bot.id` |
| `NARRATOR` | The bot's job is voicing a **Dream** (a place, character, story beat) rather than managing project state. | `Dream.DreamNarrator` relation |
| `ASSISTANT` / `PROMPTBOT` | Standalone helper not tied to steering one specific project (e.g. a general creative assistant). | none required |

Decision rule for ecosystem-map's purpose: **every active, non-retired conductor project gets exactly one `MANAGER` bot**, linked through the real `kind_robots` `Project` row via `Project.managerBotId`, not through a Dream. There is no `DreamType: PROJECT` in the schema — "Project" is its own top-level model, joined to the conductor roadmap by `Project.conductorSlug`. Do not invent a Dream-based project link; it would duplicate the slug-parity join that `CONTROL.md` already establishes as canonical.

A project whose `kind` is `content` or `proposal` (roadmap.yaml) may skip a Manager bot if the project produces no ongoing user-facing surface — record that decision in the project's ecosystem-map row rather than silently omitting the bot.

## 2. Avatar image prompt rules

One avatar image per bot, stored via `Bot.avatarImage` (and optionally mirrored through `Bot.artImageId` → `ArtImage` when generated through the approval-gated pipeline). Prompt requirements:

- Square, app-icon-safe composition — the avatar doubles as the bot's chat/thread identity image at small sizes.
- Depict the bot as a character, not the project's product (the project already has its own icon/card/hero per `ASSET-COVERAGE-MATRIX.md` — the avatar is *who*, not *what*).
- Personality-forward: a Manager bot's design should read as organized/attentive (clipboard, tools, calm posture); tone should still match the project's own visual vocabulary established in its inspiration images.
- No readable text, logos, or watermarks — same quality bar as `DESIGN-BRIEF.md`'s image approval gate.
- Generated avatars are candidates until approved; do not wire a generated `artImageId` into `Bot.avatarImage`/canonical display until Silas approves it, per the existing image approval gate.

## 3. Twenty thin portrait emotion/action image slots

Portraits are **not** stored on `Bot` directly — they are rows in the `ExpressionMedia` model, unique per `[botId, expressionKey]`. A `MANAGER` or `NARRATOR` bot should have the full twenty-slot set; `PROMPTBOT`/`ASSISTANT` bots only need the avatar and may skip expressions.

The 20 slots come from the `Expression` enum, ten `EMOTION` kind + ten `ACTION` kind (`ExpressionMedia.kind`):

- **Emotions (10):** `NEUTRAL, JOYFUL, SORROWFUL, AFRAID, DISGUSTED, ENRAGED, SURPRISED, ANXIOUS, PROUD, LOVING`
- **Actions (10):** `LAUGHING, CRYING, SLEEPING, THINKING, SHRUGGING, WINKING, FACEPALMING, CHEERING, WHISPERING, SHOUTING`
- `CUSTOM` exists as a freeform escape hatch for a project-specific expression beyond the 20 — use sparingly, and only when none of the 20 fit a genuinely needed UI moment (e.g. a project-specific celebration beat).

Per-slot fields to populate: `expressionKey` (lowercase, matches the enum name or custom slug — this is also the filename stem), `imagePath` (`public/images/bots/expressions/{botSlug}/{expressionKey}_01.webp`), `artPrompt` (kept so the image can be regenerated/audited), `label`/`emoticon` (short UI-facing tag), and optionally `message`/`additionalPhrases` (a line the bot can say when that expression triggers) and `videoPath` (rare, for an animated variant). `ExpressionTransition` (`fromKey`→`toKey`) is optional polish for animated crossfades — not required for parity, sequence after the 20 static portraits exist.

Same approval gate as avatars: all twenty are generation candidates until approved; do not flip `ExpressionMedia.isActive` to true or point production UI at them before that.

## 4. Narrator topic/thread wiring — the project navigation menu contract

This is the mechanism that satisfies `DESIGN-BRIEF.md`'s "project-specific navigation without inventing a second menu system" requirement. Two models, both already shared/reusable:

- **`NarratorTopic`** — a subject, shared across bots (`slug`, `title`, `icon`, `prompt`, `sampleUserPrompt`, `sortOrder`). Create one topic per distinct menu concern a project's bot should surface (e.g. "project status," "how to use this tool," "what's new"). Reuse an existing topic slug across projects wherever the concern is generic — do not fork a near-duplicate topic per project.
- **`NarratorThread`** — one bot's specific take on one topic, unique per `[botId, topicId]`. This is where the actual menu content lives: `openingText` (the bot's in-voice opener for that topic), `guidance` (topic-specific LLM steering layered on the bot's `botIntro`), and — the important part — **`starterPrompts`**, a JSON array of `{label, prompt, action, path?, flavor?, key?, screen?}` objects. Each entry is a literal clickable menu item; `path`/`screen` let a starter prompt double as an in-app navigation action (e.g. jump to `/superkate/stylist`), not just a chat suggestion.

Read path: `GET /api/narrators/{type}/{slug}` returns the Bot plus `NarratorThreads` (ordered by `sortOrder`, including `Topic`) plus active `ExpressionMedia` in one call — this is the query shape any project-manager page or panel should consume. `stores/seeds/narrators.ts` has ~36 full `NARRATOR` bot examples to copy the field-fill convention from; there is no `MANAGER` bot example in seed data yet, so the first one implemented under this spec becomes the reference pattern for the rest.

**Project navigation menu contract:** a project's Manager bot's navigation menu = the ordered `starterPrompts` across its `NarratorThreads` (by thread `sortOrder`, then within-array order). A project should not build a bespoke menu table or hardcoded tab list for bot-driven navigation — if a menu item needs to exist, it is a `starterPrompt` entry on a thread, full stop. Non-bot-driven navigation (the actual page's tabs/routes) remains governed by `TAB-INTEGRATION.md` and is a separate concern from the bot's conversational menu.

## 5. Project ↔ bot linkage — implementation shape

```
Project (kind_robots)
  conductorSlug   -- unique join key back to conductor projects/<slug>/
  managerBotId  →  Bot.id   (BotType: 'MANAGER')

Bot
  ManagedProjects  ←  reverse relation (Project[])
  ExpressionMedia[]  -- 20 portrait rows, botId FK
  NarratorThreads[]  -- menu content, botId FK
    → NarratorTopic   -- shared subject, topicId FK
```

Minimum viable parity for one project, in order:

1. Confirm/create the `kind_robots` `Project` row with `conductorSlug` matching the conductor directory name (per `CONTROL.md`'s slug-parity rule — do not create a new join field).
2. Create the `Bot` row with `BotType: 'MANAGER'`, avatar prompt per §2, personality/`botIntro`/`prompt` fields filled per the project's actual tone.
3. Set `Project.managerBotId` to the new bot's id.
4. Queue the 20 `ExpressionMedia` prompts per §3 (generation + approval, not committed at spec time).
5. Attach or create the `NarratorTopic`s the project needs (reuse existing slugs first), then write one `NarratorThread` per topic with real `starterPrompts` — this is the actual navigation menu and should not ship as a stub with zero entries.
6. Record the finished linkage (Project id, Bot id, topic/thread slugs) in the project's own roadmap or an ecosystem-map tracking note so `t-006` can verify parity without re-deriving it.

## Non-goals

- Do not add a `dreamType: PROJECT` — it doesn't exist; `Project` is its own model.
- Do not store portraits as a JSON blob on `Bot` — use `ExpressionMedia` rows.
- Do not build a per-project menu table — use `NarratorThread.starterPrompts`.
- Do not auto-promote generated avatar/portrait candidates before Silas approves them.
- Do not implement bot creation for any specific project from this task — this spec only defines the contract; `t-006` routes the actual per-project implementation tasks to their owning roadmaps.
