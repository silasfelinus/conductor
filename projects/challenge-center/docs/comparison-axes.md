# Challenge Center — The Five Comparison Axes

Canonical reference for the M5 comparison-matrix design. Future task notes and
PR reviews should check against **this** doc instead of re-deriving the design
from scattered task notes. The axis list and Contender-design paragraphs below
are pulled verbatim from `notes_from_silas` in
`projects/challenge-center/roadmap.yaml` (Silas, 2026-07-05).

## What the arena actually compares

> this is NOT primarily a sibling-competition tool. The original inspiration —
> Silas's conductor (Claude agents) vs his brother's port0s stack — remains a
> flagship matchup, but it is one instance of the general mechanic. A contender
> is ANY distinct way of producing an artifact, and the framework must support
> comparing along every axis:
>
>   - **Provider vs provider:** the same prompt to OpenAI vs Claude.
>   - **Model vs model within a provider:** Fable vs Opus.
>   - **Generator vs generator for art:** the same prompt to SD, ComfyUI
>     (flux/sdxl/kontext/ltx), and OpenAI image generation — all already live in
>     kind_robots (server/api/art/sd, server/api/comfy/*, server/api/art/generate).
>   - **Prompt vs prompt on the same generator:** terse vs detailed phrasing, or
>     randomized variables via the kind_robots random-list feature (randomStore's
>     keyed pools — adjective/animal/genre/species/etc from stores/helpers/
>     randomHelper.ts — plus user-created RANDOMLIST dreams).
>   - **Settings vs settings:** same model + prompt, different temperature/sampler/
>     steps/cfg.

## Contender vs ChallengeSubmission — the "who" and the "how"

> Contender design (Silas, 2026-07-05 — supersedes the original Bot plan): do NOT
> use the Bot model. Bots are character-driven narrators and specialized GPTs; the
> arena compares configurations, so contenders get their own small first-class
> model. Reactions already attach to ChallengeSubmission directly, so no Bot
> infrastructure is actually needed for voting or scoring.
>
>   Contender = the leaderboard identity (the "who"): slug, name, kind
>   (AGENT_STACK | LLM_MODEL | ART_GENERATOR), provider/model/generator fields,
>   default settings, avatar art, description. Examples: conductor-claude,
>   portos-agent, claude-fable, claude-opus, openai-gpt, art-sd, art-comfy-flux.
>
>   ChallengeSubmission = the "how" of each individual entry: exact prompt used,
>   settings, random substitutions, variantKey. Uniqueness is
>   (challengeId, contenderId, variantKey) so one contender can enter multiple
>   prompt/settings variants in the same challenge.

**In short:** the `Contender` is the stable leaderboard identity; each
`ChallengeSubmission` is one concrete entry whose `variantKey`, `promptUsed`,
`settings`, and `randomSelections` capture exactly how that entry was produced.
Every comparison axis below is expressed as *which of those fields differ*
between the submissions being compared.

## Axis → field → implementing task

| # | Axis | What differs between submissions | Distinguished by | Implemented / carried by |
|---|------|----------------------------------|------------------|--------------------------|
| 1 | Provider vs provider | The backend provider (Anthropic vs OpenAI) | `Contender.provider` | t-002 (schema), t-012 (roster), t-013 (runner), t-015 (facet) |
| 2 | Model vs model | The specific model within a provider (Fable vs Opus) | `Contender.model` | t-002 (schema), t-012 (roster), t-013 (runner), t-015 (facet) |
| 3 | Generator vs generator | The art backend (SD vs Comfy-flux/sdxl vs OpenAI images) | `Contender.generator` | t-002 (schema), t-012 (roster), t-013 (runner), t-015 (facet) |
| 4 | Prompt vs prompt | The exact prompt / randomized variables on one generator | `ChallengeSubmission.variantKey` + `promptUsed` + `randomSelections` | t-002 (schema fields), t-014 (variant generator), t-013 (runner) |
| 5 | Settings vs settings | Same model + prompt, different temperature/sampler/steps/cfg | `ChallengeSubmission.settings` (overriding `Contender.defaultSettings`) | t-002 (schema fields), t-013 (runner) |

Notes on the mapping:

- **t-002** (`Schema: add Contender model and submission variant fields`) is the
  foundation for all five axes: it adds the `Contender` identity fields
  (`kind`/`provider`/`model`/`generator`/`defaultSettings`) that carry axes 1–3
  and the `ChallengeSubmission` variant fields (`variantKey`, `promptUsed`,
  `settings`, `randomSelections`) that carry axes 4–5, with uniqueness
  `(challengeId, contenderId, variantKey)`.
- **t-012** (`Seed contender roster`) creates the concrete fighter cards that
  make axes 1–3 real: agent stacks, LLM models, and art generators.
- **t-013** (`Matchup runner`) is where a single challenge is dispatched across a
  contender matrix, resolving backend/model/settings from the `Contender` record
  and applying per-entry overrides — the runtime that exercises all five axes.
- **t-014** (`Prompt-variant generator`) powers axis 4 specifically: it turns a
  base prompt with placeholder keys into N reproducible prompts using the
  kind_robots random pools, returning the key→value map stored as
  `randomSelections` so variants are auditable, not mystery rolls.
- **t-015** (`Faceted leaderboards`) is the read side: it groups results by
  `Contender.generator` / `Contender.model` / `Contender.kind` and by per-variant
  `variantKey` so each axis becomes its own "weight class" in the standings.

## Design guardrails carried across the axes

- **Contender is the leaderboard identity; ChallengeSubmission is the entry.**
  Aggregate scores group by `contenderId`, never by raw submission row, so a
  contender entering multiple variants still ranks as one identity with a
  per-variant breakdown.
- **Variants must be reproducible.** Any randomized prompt records its
  `randomSelections` key→value map so the comparison teaches something instead of
  being an unrepeatable roll.
- **The Bot model is not used** for contenders (superseded 2026-07-05). Reactions
  attach to `ChallengeSubmission` directly; scoring runs
  Reaction → ChallengeSubmission → Contender.
- **Matchups are N-way, not just 2-way.** A duel renders as the classic VS split;
  3+ renders as a select-screen grid. The same pages and runner handle both.
