# Pitch: kind_robots dashboard as the shared front-end for Conductor + PortOS CoS

date: 2026-07-19
project-target: ai-networker-itself
status: awaiting-silas

## The idea

kind_robots is already Conductor's web control plane: `server/api/conductor/*`
(projects, PRs, pitch votes, overrides, inbox, messages, art requests) reads and
writes this repo, `components/pages/conductor-manager.vue` renders the admin
dashboard, and `stores/helpers/conductorTabs.ts` already carries a `portos` tab
with a narrative describing "connect Portos without burying server state in
component goo" — currently just a server-address/pairing stub, not yet backed
by anything. Rather than building a second, separate dashboard if/when a
CoS-style runtime (worktree-parallel Workers, PM2 scheduler, learning-driven
model routing — see `docs/2026-07-11-portos-cos-learnings.md`) gets adopted
here, extend the existing `portos` tab into a real second execution-runtime
view fed by its own read API, so kind_robots stays the one place Silas looks
regardless of which backend is doing the work.

## Why it's worth doing

- **The seam already exists and is intentionally named for this.** The
  `portos` tab in `conductorTabs.ts` isn't a random stub — its own narrative
  ("Connect Portos... through the proper server-entry flow once that
  persistence contract is built") is written as a forward reference to exactly
  this convergence, just waiting on a runtime to exist behind it.
- **Avoids a second UI Silas has to context-switch into.** If
  `conductor/t-033` (worktree-parallel Workers pitch, currently `needs-human`)
  or any CoS-style runtime experiment ships, its natural operator surface
  (live task queue, active worktrees, model-routing stats) belongs next to the
  roadmap/pitch/PR views Silas already checks daily, not in a standalone tool.
- **Slug-parity and `server/api/conductor/*` are proven patterns to extend,
  not invent.** The existing endpoints already bridge Git+YAML state
  (roadmap.yaml, TALKBACK.md, pitches/) into REST reads the front end
  consumes; a CoS-style backend's task/queue/worker state is the same shape
  of problem (durable backend state → REST read → dashboard tab), so the
  integration is additive, not a rearchitecture.
- **Low commitment now.** This pitch asks for a design note, not a runtime.
  Nothing here presumes PortOS CoS (or any specific runtime) actually gets
  adopted — `conductor/t-033` is still `needs-human` and unapproved. The value
  of doing this now is cheap: it settles the *shape* of convergence before
  anyone has to decide whether to build it.

## Rough effort

small (for the suggested first task below) — a full second-runtime
integration would be medium-to-large and is explicitly out of scope until
`t-033` (or an equivalent runtime pitch) is approved.

## Suggested first task

Write a design note at `projects/conductor/docs/portos-dashboard-shape.md`,
no code:

1. **What the `portos` tab shows today vs. what it would need to show for a
   real second runtime** — task queue depth, active worktrees/agents, recent
   completions, model-routing/success-rate stats (the CoS `taskLearning`
   analog) — grounded against the tab's current narrative text so the
   upgrade path is additive to the existing copy, not a rewrite.
2. **One new read-only API shape** (e.g. `server/api/conductor/portos-status.get.ts`)
   that a runtime would populate, mirroring how `projects.get.ts` /
   `prs.get.ts` already expose Conductor's own state — so the pattern is
   proven twice, not once.
3. **Explicit non-goals**: this pitch does not authorize building or deploying
   any CoS-style runtime, does not touch the `portos` tab's existing
   server-address/pairing flow, and stays inert (no new nav, no live data)
   until a runtime pitch like `t-033` is separately approved.
4. **Dependency note**: flag this design note as informative context for
   whoever picks up `t-033`, not a blocker on it — the two can be approved
   independently or together.
