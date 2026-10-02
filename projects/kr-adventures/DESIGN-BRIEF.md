# Kind Robots Adventures — Design Brief

date: 2026-10-02
status: draft (Silas-directed pitch; scope confirmation t-002 is a soft checkpoint and blocks nothing)
author: claude

## What it is

Gamebooks. Each adventure starts from an existing Kind Robots **Scenario**, gives you a preset hero,
and walks you through a fully pre-written branching story: every page, every choice, every ending
and every illustration is authored ahead of time and shipped as static content. Reading costs nothing
and needs no LLM.

Silas's pitch, 2026-10-02, verbatim: *"pre-written choose your own adventure stories that start from
our scenarios, with a preset main character, but have fully complete pre-written branching
storylines and art."*

## How it differs from Storymaker

Storymaker (approved pitch) is a live, LLM-narrated engine: open-ended and costly. Adventures is its
free sibling: closed, authored and illustrated, so quality is reviewed before anyone reads it. A
finished Adventure can later feed Storymaker as a known-good starting point; nothing here depends on it.

## Shape of a book

- **Opening.** Pulled from the Scenario's own premise, so the book is recognisably the scenario.
- **Hero.** One preset Character per book (name, look, a short voice note) shown on a cover card.
- **Graph.** 40 to 60 nodes, 2 or 3 choices per branching node, genuine divergence (not a bottleneck
  that rejoins in one page), 4 to 6 endings from triumphant to bittersweet to funny. No dead ends
  except marked endings; no unreachable nodes; loops are allowed only where authored.
- **Art.** One illustration per node (roughly 50 per book) plus a cover and per-ending plate,
  pre-generated through the ArtJob queue with a per-book style bible and the hero as a visual anchor.
- **Light state.** Optional flags and a small inventory (a key, an ally) gate some choices, so
  replay differs; kept deliberately simple so the validator can prove reachability.
- **Reader features.** Bookmark and resume (localStorage), a "path map" showing visited and unseen
  endings, back one page, restart, and an endings checklist as the replay hook.

## Who it serves

Everyone, with no signup: an easy first thing to do on the site. Kids can read it alone; the tone is
warm, a little silly, and kind. It is also a Daily Dream consumer: strong scenarios graduate into books.

## Data contract (static JSON bundle per book)

```ts
type Adventure = {
  version: 1
  slug: string; title: string; scenarioSlug: string
  hero: { characterSlug: string; name: string; blurb: string }
  styleBible: string
  start: string
  nodes: Record<string, {
    id: string; text: string            // 60-180 words
    art: { file: string; alt: string; prompt: string; model?: string }
    choices?: { label: string; to: string; requires?: string[]; sets?: string[] }[]
    ending?: { kind: 'triumph'|'bittersweet'|'funny'|'tragic'|'secret'; title: string }
  }>
}
```

A DB-free validator checks: every `to` exists, start reaches every node, every non-ending node has
at least one choice that is always available, every ending is reachable, no flag is required that is
never set, every node has art and alt text, reading level sanity (word counts).

## Architecture

- Home is kind_robots: `/play/adventures` (library) and `/play/adventures/[slug]` (reader), Pinia
  `adventureStore`, content under `content/` or `public/data/adventures/` per t-001's recommendation.
- No API and no migration for the reader; the bundle is fetched as a static file.
- Authoring is done by sessions: outline, then node text, then art prompts, then validate, then
  art, then review. A `scripts/author_adventure.*` helper keeps the pipeline repeatable.

## MVP scope

Schema, validator and reader with one short fixture book; then book 1 fully written and illustrated
as the quality bar; then books 2 and 3; then library, path map and polish. Scale to ~10 books only
after Silas accepts the first three.

## Out of scope / guardrails

- No LLM in the reader. No user-written branches in v1 (that is Storymaker).
- No publishing, payments, or deploy steps.
- Art is pre-generated with metadata; no scraped art.
- Mature themes stay out; keep it all-ages.
- Authoring is long-form writing: the author must read each branch through, not just validate the graph.

## Open questions (none block development)

1. Which three scenarios and heroes go first? (t-002 proposes candidates from the live scenario list.)
2. Content location (`content/` vs `public/data/`) is decided by the survey task.
3. Do endings grant Rewards or Characters on the user's profile when signed in? Not in v1.
