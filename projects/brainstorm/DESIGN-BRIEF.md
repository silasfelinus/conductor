# Brainstorm — Design Brief

date: 2026-08-10
status: active
author: OpenAI Worker (Silas-directed session)

## What it is

Brainstorm is Kind Robots' creative divergence engine: give it a premise, constraint,
object, problem, joke setup, art target, or half-formed thought and ask for a deliberate
number of distinct ideas. The user can keep the promising responses, edit them, throw
away the weak ones, ask for replacements, and eventually save the survivors as reusable
creative material or hand them to another Kind Robots workflow.

This is a revival, not a greenfield invention. Brainstorm was one of the earliest working
LLM services on the site and has substantial repository history. The product should recover
its original interaction contract before expanding it.

The emotional center is playful human ideation, not project-management automation. A
request can be practical ("give me 20 art prompts for this Character") or gloriously
ridiculous ("ten terrible ice-cream flavors", fictional biographical facts, riddles,
character details, improbable products, dark-comedy improv). The system should reward
specificity, surprise, variety, and editability rather than produce ten paraphrases wearing
different hats.

## Why this project exists now

The current Kind Robots surface no longer represents the Brainstorm product:

- `content/brainstorm.md` renders `:dream-manager`, which makes the page a Dream gallery.
- `dashboardConfigs.brainstorm.tabs[0]` is titled `Dream Brainstorm` and routes to `/dreams`.
- the repository still contains a long Brainstorm development history from 2023-2024,
  including `components/content/prompts/brainstorm-view.vue`,
  `brainstorm-selector.vue`, `brainstorm-image.vue`, Pitch/PitchType work, and repeated
  revisions to the Brainstorm API.
- the 2024 `brainstorm-view.vue` composed a Brainstorm image, a selector, `add-pitch`, and
  a grid of newly generated Pitch cards. That is direct evidence of the original
  pitch -> generate -> curate/save interaction family.

Conductor also already has a `brainstorm` project, but it drifted into a proposal-kind
recurring task that generates internal pitches for Silas. That capability may remain useful,
but it is not the product definition. This roadmap repairs the existing project rather than
creating a duplicate slug.

## Product promise

A user should be able to arrive with one sentence and leave with a small, chosen set of
ideas they actually want to use.

The core loop is:

1. **Pitch** — enter what to brainstorm and optional constraints.
2. **Generate** — choose a response count and ask the active Kind Robots text server for
   genuinely varied candidates.
3. **Curate** — keep, reject, edit, reorder, or regenerate individual candidates without
   destroying the rest of the session.
4. **Refine** — ask for more like a selected idea, stranger versions, safer versions,
   shorter versions, different genres, another angle, or a fresh batch.
5. **Save / hand off** — persist selected ideas and, where appropriate, send them to a
   compatible Kind Robots object/workflow.

A single generation should never force an all-or-nothing decision.

## Personality and creative range

Brainstorm should have room for absurdity. It is not a corporate naming worksheet unless
the user asks for one.

Useful modes include:

- freeform idea lists;
- absurd/dark-comedy improv and fictional facts;
- riddles, jokes, prompts, names, titles, scenarios, rewards, character traits, settings;
- constrained variation ("20 ideas, each under 12 words, no repeats");
- expansion of one selected candidate;
- opposites / inversions / genre shifts;
- practical ideation and problem-solving;
- database-object-aware variations, especially art prompts for Characters, Dreams,
  Scenarios, Rewards, Bots, Projects, and other supported Kind Robots entities.

The output contract should explicitly push semantic diversity. Ten candidates that differ
only cosmetically count as a failed batch.

## Restoration target

Do not blindly resurrect old Vue code. Use historical Brainstorm code as behavioral evidence
and selectively port the useful interaction into current Nuxt 4 / Vue 3 / Pinia conventions.

Historical anchors to inspect before implementation:

- commit `19b37e0` (2023-09-25), `brainstorming page`;
- the 2024-08-31 remodel sequence (`0041e10`, `7ba1a20`, `d8cc25b`);
- the 2024-09-10/11 SPA and Pitch-store sequence (`21af63c`, `ac57ba0`, `06251f6`,
  `a37569d`, `6633ff5`, `d50f86b`, `694d127`, `3e54006`);
- the 2024-11-11 through 2024-11-13 Brainstorm endpoint/view/selector/image revisions,
  including `4434253`, `ef0779c`, `e6f39ed`, `4318321`, `508ed6c`.

The first implementation task should identify the last coherent old product snapshot and
write a short recovery map: historical files, current equivalents, reusable pieces, dead
assumptions, and the commit where the public surface was replaced or redirected.

## V1: text first

V1 is intentionally text-only at the center. It must be useful before image generation is
added.

### Input

- freeform pitch / request;
- desired number of results, with sensible bounds;
- optional constraints / examples;
- optional creative control such as novelty, tone, format, or "more like this";
- optional Kind Robots source object context.

Avoid a cockpit of model knobs. Advanced prompting can exist behind a disclosure or later
iteration; the default experience should take seconds to understand.

### Candidate cards

Every generated candidate should have its own identity and state so users can:

- keep / unkeep;
- edit inline;
- delete/reject;
- regenerate only that slot;
- duplicate or branch from it;
- request "more like this";
- eventually request art for it;
- save it independently.

Generation history should be recoverable within the session. Replacing one card must not
silently erase the previous text.

### Persistence

Model the durable data around sessions and candidates rather than treating one API response
as the product. Before adding schema, audit the current `Pitch`, Prompt, Project, Dream and
related models/stores and reuse an existing model where its semantics truly fit.

Do not overload Conductor `pitches/*.md` with user Brainstorm output. Conductor pitches are
coordination proposals; Brainstorm candidates are application/user data.

Anonymous use may remain ephemeral if auth/persistence makes the first restoration pass too
large. Logged-in users should ultimately be able to reopen saved Brainstorms.

## Kind Robots infrastructure integration

Brainstorm should use the site's existing abstractions rather than invent its own AI stack:

- active/default text server and the current server/provider contract;
- centralized auth and mana/token gating where generation is billable;
- Pinia store owns API calls and browser persistence;
- Nitro routes return the standard `{ success, ... }` shape and use `errorHandler()`;
- existing object selectors and entity APIs for source-context brainstorming;
- existing project/channel/tutorial/navigation registration;
- current responsive design-system primitives and interface-vision rules.

The server prompt should request structured output, validate it, and be resilient to providers
returning wrappers or malformed items. Parsing should not depend on brittle prose splitting.

## Object-aware brainstorming

A high-value expansion is "brainstorm from this thing".

Examples:

- Character -> 20 portrait/action/art prompts that preserve canonical traits;
- Dream -> locations, encounters, titles, sensory details, threats, rewards;
- Scenario -> alternate choices, complications, endings;
- Reward -> names, powers, drawbacks, flavor text;
- Project -> feature ideas or visual concepts without creating Conductor tasks directly;
- existing prompt -> stylistic or structural variations.

Object context should be explicit and inspectable. The user should know what source object is
being used and be able to remove it.

Long-term, other Kind Robots surfaces should be able to deep-link into Brainstorm with a
source object and intent rather than each building a private mini-brainstorm endpoint.

## Art brainstorming and optional generation

Art is phase two, not a prerequisite for restoring the service.

Two separate capabilities matter:

1. **Brainstorm art prompts** — text-only generation of diverse image prompts. This should
   arrive early because it is cheap and immediately useful throughout Kind Robots.
2. **Generate art for a chosen candidate** — enqueue selected candidate(s) through the
   durable ArtJob pipeline.

When Brainstorm itself requests generated artwork, default to the site's current Krea2
baseline/settings unless the user deliberately chooses another supported build. Never create
a parallel browser-only image-generation path.

Art generation must preserve prompt, source object, candidate/session identity, model/build,
ArtJob id, and resulting ArtImage relationship so a user can tell which idea created which
image. Batch generation should be explicit to avoid turning "give me 20 ideas" into 20 costly
renders by accident.

## Brainstorm Bot

The original Brainstorm bot/history is part of the product's identity and should be audited,
not replaced with generic assistant copy. Determine what survives in seed data / production
Bot records and how it relates to the current narrator/chat architecture.

A revived Brainstorm persona may provide flavor and default system guidance, but the service
must not depend on one hard-coded provider or one bot record being present. The functional
contract is the brainstorm loop; the brain-in-a-jar host is the delightful layer on top.

## Relationship to Conductor's proposal generator

The current Conductor roadmap used `brainstorm` as an internal recurring proposal engine.
That behavior should not own the public project.

After the user-facing product is stable, the proposal workflow can become a **consumer** of
the Brainstorm engine: Conductor can request candidate project ideas under its dedup/policy
constraints and then promote only vetted candidates into canonical `pitches/*.md`.

That integration must preserve the source-of-truth boundary:

- Brainstorm generates candidate ideas in Kind Robots application state.
- Conductor decides whether something becomes a coordination pitch/task.
- No user brainstorm silently mutates a roadmap or project lifecycle.

## Routes and placement

Canonical public route: `/brainstorm`.

`/plan/brainstorm` should resolve to the same product (redirect or stitched workspace alias),
not a second implementation. The Brainstorm tab should stop routing to `/dreams`.

The current project presentation data already identifies Brainstorm as a Plan/Brainstorm
surface. Kind Robots remains authoritative for route/channel/tab presentation fields.

## UX direction

The page should feel like an idea workbench, not a gallery and not a chatbot transcript.

Recommended desktop structure:

- compact hero/persona strip;
- pitch composer and generation controls;
- responsive candidate-card workspace as the visual center;
- a small saved/history drawer or tab;
- source-object context chip/preview when present.

On mobile, generation controls collapse cleanly and candidate cards become a single-column
curation stream. Keep/edit/regenerate actions remain thumb-reachable.

The existing historical Brainstorm art/persona can inspire the visual identity, but the
restored interaction comes before decorative art work.

## Safety and content

Brainstorm is a general ideation tool, so normal Kind Robots maturity and safety boundaries
apply. Do not hard-code an artificially cheerful tone that ruins dark comedy, horror, satire,
or absurd improv that is otherwise allowed.

Generated candidates should remain user-controlled drafts. Saving or generating an idea does
not publish it externally.

## Definition of done

Brainstorm is not done when `/brainstorm` stops showing Dreams. It is done when all of these
are true:

- historical product behavior is documented and the accidental replacement point is known;
- `/brainstorm` and `/plan/brainstorm` land on one canonical Brainstorm experience;
- a user can submit a pitch, choose a result count, and receive validated diverse candidates;
- each candidate can be independently kept, edited, rejected, regenerated, and branched;
- selected candidates can be saved/reopened for logged-in users;
- object-aware brainstorming works for at least Character and Dream, with a reusable adapter
  pattern for additional entity types;
- art-prompt brainstorming works without rendering images;
- chosen candidates can optionally enqueue Krea2-default ArtJobs with traceable results;
- the Brainstorm persona/history is either restored or deliberately modernized from evidence;
- no duplicate Dream gallery, private AI stack, or second Conductor source of truth remains;
- direct load, refresh, empty/loading/error states, keyboard interaction, and auth transitions
  behave correctly;
- phone, tablet, and desktop layouts are visually verified on a PR preview;
- relevant typecheck/tests/CI pass and Silas has had a chance to play with the restored loop
  before the finite project is marked finished.
