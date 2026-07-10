# Dream Cycle — Design Brief

date: 2026-07-10
author: Reviewer (Claude), from Silas's session direction
status: awaiting soft scope confirmation (t-002) — development proceeds in parallel

## What this is

A new **idle fallback for conductor sweeps**: when no higher-priority project has a
ready task, the agent doesn't stop — it develops the site itself, **one dream at a
time**. Each cycle of idle capacity advances a single dream build until it ships,
roughly one complete dream per day, art included.

A **dream** here is a complete, self-consistent slice of kind_robots content:

- a **location** (a LOCATION Dream) with a **vibe** (a GENRE Dream, new or existing),
  joined by DreamRelation edges
- **characters** who inhabit it
- **rewards** it can grant
- **scenarios** that play out there
- optionally a **bot narrator** who hosts it — with an expression set, topics, and threads

Everything above already exists in the kind_robots schema (Dream, DreamRelation,
Character, Reward, Scenario, Bot, ExpressionMedia, ExpressionTransition,
NarratorTopic, NarratorThread). **No new models are needed.** What's needed is the
infrastructure tightening around the pipeline: a spec for "complete," a verified
build path, and a human-legible backlog.

## The backlog — accessible files Silas can steer

`projects/dream-cycle/backlog/` holds one markdown file per dream idea. These files
are the product surface between Silas and the agents:

- Every file has YAML frontmatter with `status` (`outline | approved | building |
  built | parked | vetoed`) and `priority` (`low | normal | high`) that Silas can
  flip directly.
- Every file has a **`## Notes from Silas`** section. Agents MUST read and fold in
  any notes there before starting or continuing that dream's build, and must never
  edit or delete Silas's notes (treat like TALKBACK — append-only for agents,
  Silas-owned).
- Every file has a **`## Build log`** section agents append to as stages complete,
  so Silas can see progress at a glance without reading PRs.
- `backlog/_template.md` defines the format; `backlog/README.md` documents it.
- Shipped dreams are recorded in `SHIPPED.md` (ledger: slug, date, PRs, what was
  created where).

Backlog replenishment is part of the loop: when fewer than 5 buildable outlines
(`outline`/`approved`) remain, the build task's final stage generates new ones —
so there is always a runway of future developments waiting.

## The build loop — one dream, one day

The Worker runs hourly; a dream takes ~6–8 idle cycles ≈ one day. Each cycle
advances the **single active dream** (only one may be `building` at a time —
"one task at a time" applies at the dream level too) by exactly one stage:

1. **Flesh out** — promote the chosen outline (`outline`/`approved`, highest
   priority first, honoring Silas notes) into a full spec inside its backlog file;
   set `status: building`.
2. **Dreams** — create the LOCATION Dream + vibe GENRE Dream (reuse an existing
   GENRE when it fits) + DreamRelation edges.
3. **Characters** — 2–4 Characters linked to the dream, with backstory, drive,
   quirks, stats, art prompts.
4. **Rewards** — 3–6 Rewards with a rarity spread, linked to the dream.
5. **Scenarios** — 1–2 Scenarios wiring the location, vibe, and cast together.
6. **Narrator** (if the outline calls for one) — a narrator Bot with
   NarratorThreads joining it to fitting NarratorTopics (create topics only when
   no existing one fits), plus an ExpressionMedia set: NEUTRAL + at least 5
   emotions + 2 actions.
7. **Art** — generate remaining art via the pre-approved pipeline (dream
   image/card/hero, character portraits, reward icons, scenario image, narrator
   avatar + expression portraits), preserving prompt/model/seed metadata.
8. **Ship** — verify against DREAM-SPEC.md's checklist, set `status: built`,
   append the SHIPPED.md ledger entry, replenish the backlog if below threshold.

Stages 2–6 write **content rows, not code** — via the kind_robots REST API with
KR_API_TOKEN where endpoints exist, or as seed-data PRs to kind_robots where they
don't. Which path applies per model is exactly what the m2 infrastructure tasks
pin down before the first build starts. Rows are created `isActive: true,
isPublic` per outline, are individually deletable, and carry `designer`/source
metadata so a whole dream can be traced and removed — this is what keeps the
loop reversible.

## What this is NOT

- Not a scheduler change: "nothing better to do" is enforced by placement —
  dream-cycle sits last in `projects/priority.yaml`, so its always-ready
  recurring task is only picked when no other active project has ready work.
- Not a backend project: kind_robots backend code stays read-only/external.
  Missing endpoints become kind_robots roadmap tasks or pitches, never direct edits.
- Not autonomous publishing: dreams land as site content under Silas's existing
  content flags; anything outward-facing (marketing, store listings, deploys)
  stays hard-gated as always.

## Autonomy contract

`autonomous: true` under the never-idle rule (AGENTS.md, 2026-07-10).
Pre-approved: art generation for all dream entities (generated-art rule,
2026-07-06); content-row creation via existing API endpoints once t-003/t-004
verify the path. Hard gates unchanged: spend, publishing, schema changes,
secrets, deploys. Silas steers through backlog file notes, frontmatter flips,
and CONTROL.md — course correction is expected and cheap.
