# Dream Cycle — Design Brief

date: 2026-07-10 (revised same day: generalized from dreams-only to typed creations)
author: Reviewer (Claude), from Silas's session direction
status: awaiting soft scope confirmation (t-002) — development proceeds in parallel

## What this is

A new **idle fallback for conductor sweeps**: when no higher-priority project has a
ready task, the agent doesn't stop — it makes something for the site, **one creation
at a time**, roughly one per day, art included. The project keeps the name
"dream-cycle" (it dreams things up nightly), but a creation is not always a Dream:

## Creation types

Each backlog outline declares a `type`. Each type has a **playbook** in `specs/`
defining its build stages, verification, and ship checklist. The recurring build
task only picks outlines whose type has a playbook — new types come online by
writing one.

### `type: dream` (playbook: specs/dream.md, from t-004)

A complete, self-consistent slice of kind_robots content:

- a **location** (a LOCATION Dream) with a **vibe** (a GENRE Dream, new or existing),
  joined by DreamRelation edges
- **characters** who inhabit it, **rewards** it can grant, **scenarios** that play
  out there
- optionally a **bot narrator** who hosts it — with an expression set, topics, threads

Everything already exists in the kind_robots schema (Dream, DreamRelation,
Character, Reward, Scenario, Bot, ExpressionMedia, ExpressionTransition,
NarratorTopic, NarratorThread). No new models. Stages:

1. **Flesh out** — promote the outline into a full spec in its backlog file.
2. **Dreams** — LOCATION + vibe GENRE Dream (reuse existing GENRE when it fits) + relations.
3. **Characters** — 2–4, with backstory, drive, quirks, stats, art prompts.
4. **Rewards** — 3–6 with a rarity spread.
5. **Scenarios** — 1–2 wiring location, vibe, and cast together.
6. **Narrator** (if the outline calls for one) — Bot + NarratorThreads to fitting
   NarratorTopics (new topics only when none fit) + ExpressionMedia set
   (NEUTRAL + ≥5 emotions + ≥2 actions).
7. **Art** — everything via the pre-approved pipeline, prompt/model/seed metadata kept.
8. **Ship** — verify checklist, mark `built`, ledger entry, replenish backlog.

### `type: coloring-book` (playbook: specs/coloring-book.md, from t-009)

"Spend today drafting and making a coloring book." A creation day produces or
advances one book set following the coloring-book project's production sequence
(design → concept art → selection → Character creation → coloring conversion →
book assembly → PAUSE before publishing/POD, which stay hard-gated).

**Coordination rule — no second source of truth:** book sets live in
`projects/coloring-book/sets/<slug>/` and follow that project's specs and
originality guardrails. The dream-cycle backlog entry is the *scheduler card and
steering surface*: it names the set, tracks which production stage is next, and
carries Silas's notes; the set's actual content files belong to coloring-book.
For a brand-new book idea, stage 1 (design: cast bible + page plan, modeled on
`sets/monster-recast/`) happens as the creation's first day-stages, creating the
set folder in coloring-book; from then on it's the same delegation.

First coloring-book creation: **Monster Recast** (backlog/monster-recast.md) —
already design-ready in `projects/coloring-book/sets/monster-recast/`, so the
idler's job is driving its concept-art → selection → conversion → assembly
stages when idle capacity allows.

### Future types

Anything day-sized and reversible can become a type: an art-collection drop, a
curriculum unit for ai-art-academy, a scenario pack for an existing dream, a
davinci ending batch. Rule: write the playbook first (a `specs/<type>.md` PR),
then outlines of that type become buildable. Types whose output belongs to a home
project always delegate like coloring-book does.

## The backlog — accessible files Silas can steer

`projects/dream-cycle/backlog/` holds one markdown file per creation idea. These
files are the product surface between Silas and the agents:

- Frontmatter: `type`, and `status` (`outline | approved | building | built |
  parked | vetoed`) plus `priority` (`low | normal | high`) that Silas can flip
  directly.
- Every file has a **`## Notes from Silas`** section. Agents MUST read and fold in
  any notes there before starting or continuing that creation's build, and must
  never edit or delete Silas's notes (append-only for agents, Silas-owned).
- Every file has a **`## Build log`** section agents append to as stages complete,
  so Silas can see progress at a glance without reading PRs.
- Templates: `backlog/_template.md` (dream), `backlog/_template-coloring-book.md`.
  `backlog/README.md` documents the format.
- Shipped creations are recorded in `SHIPPED.md` (ledger: slug, type, date, PRs,
  what was created where).

Replenishment is part of the loop: when fewer than 5 buildable outlines
(`outline`/`approved` with a playbook-backed type) remain, the build task's final
stage generates new ones — a standing runway of future developments.

## The build loop — one creation, one day

The Worker runs hourly; a creation takes ~6–8 idle cycles ≈ one day. Each cycle
advances the **single active creation** (only one may be `building` at a time —
"one task at a time" applies at the creation level too) by exactly one stage of
its type's playbook. Queue order: `approved` before `outline`, then `priority`,
then oldest `created` — regardless of type.

Content-writing stages create **content rows or set files, not backend code** —
via the kind_robots REST API with KR_API_TOKEN where endpoints exist (t-003
audit), or as seed-data/set-file PRs where they don't. Rows are created with
`designer`/source metadata so a whole creation is traceable and removable — this
is what keeps the loop reversible.

## What this is NOT

- Not a scheduler change: "nothing better to do" is enforced by placement —
  dream-cycle sits last in `projects/priority.yaml`, so its always-ready
  recurring task is only picked when no other active project has ready work.
  (Corollary: when coloring-book itself has ready tasks, the Worker gets to them
  through normal priority long before the idler — a coloring-book *idler day*
  just means that pipeline also absorbs leftover capacity.)
- Not a backend project: kind_robots backend code stays read-only/external.
  Missing endpoints become kind_robots roadmap tasks or pitches, never direct edits.
- Not autonomous publishing: creations land as site content or set inventory
  under existing flags; anything outward-facing (publishing, POD accounts,
  store listings, spend, deploys) stays hard-gated as always.

## Autonomy contract

`autonomous: true` under the never-idle rule (AGENTS.md, 2026-07-10).
Pre-approved: art generation for all creation entities (generated-art rule,
2026-07-06); content-row creation via existing API endpoints once t-003/t-004
verify the path. Hard gates unchanged: spend, publishing, schema changes,
secrets, deploys. Silas steers through backlog file notes, frontmatter flips,
and CONTROL.md — course correction is expected and cheap.
