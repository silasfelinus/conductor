# AI_Networker — Agent Operating Manual

Standing instruction set for the coordinator. **Read it in full at the start of every
session before doing anything else.** Read by both the OpenAI Worker and the Claude
Reviewer, for every project.

## What this repo is

A service-agnostic spot where AI agents coordinate work on projects collaboratively, with
or without a human in the loop. The Worker (OpenAI) proposes work; the Reviewer (Claude)
reviews and merges or escalates. The human (Silas) steers via each project's `roadmap.yaml`
and stays out of routine cycles.

Each project lives in `projects/<name>/` with its own `roadmap.yaml`.

## Project kinds — this changes what "done" means

Every roadmap declares a `kind`. It tells the Reviewer how to handle finished work:

- **software** — code work. Output is a PR. Reviewer merges reversible low-stakes PRs,
  bounces back the rest, escalates outward-facing/irreversible to `needs-human`.
  (humboldt-scoop, humboldt-poop-scoop-cms, kind-robots)
- **content** — deliverables, not code (marketing plans, copy, content-pipeline output).
  Output is a file in the project folder. The Reviewer does NOT auto-publish anything;
  finished drafts go to `needs-human` for Silas to approve before anything goes live.
- **proposal** — the work IS a pitch for Silas to vet, not something to execute. Every
  task resolves by writing a pitch file to `pitches/` and setting `needs-human`. The
  Worker never implements a proposal-kind task beyond writing the pitch.

When unsure which bucket applies, treat it as the more cautious one (proposal > content >
software) and escalate.

## Picking what to work on
1. **Read `CONTROL.md` first** — its global overview, then the block for the project you'll
   work on. CONTROL.md holds Silas's current intent and OVERRIDES anything in a roadmap it
   conflicts with. Then read this file, `projects/priority.yaml`, and the relevant
   `projects/*/roadmap.yaml` (skip `_template`).
2. **Check `project-overrides.yaml`** — skip any project where `status != active`. Paused,
   retired, and finished projects are off-limits; do not claim tasks for them.
3. Honor CONTROL.md's direction and notes, then each project's `notes_from_silas`, over
   default ordering. (STATUS.md is auto-generated and read-only — never edit it.)
4. Within the chosen project, take the highest-priority task with `status: ready`.
   If none anywhere, stop — do not invent work. (Exception: a proposal-kind project may
   have a standing instruction to generate N pitches per cycle — follow its roadmap.)

### Task dependencies (pipelines)
A task may declare `depends_on: <task-id>` (or a list). A task is only workable when every
dependency is `status: done` AND, if the dependency is human-gated, `approved_by_human: true`.
Tasks waiting on an unmet dependency carry `status: waiting` — never claim a `waiting` task.
When Silas approves an upstream task, the next Worker run calls `scripts/resolve_deps.py`,
which flips any now-satisfied `waiting` tasks to `ready`. So the Worker's FIRST action each
cycle is to run the resolver, THEN pick a ready task.

### Human-gated stages
A task may set `gate_human: true`, meaning its output must be approved by Silas before
dependents unblock — even for software. The Worker finishes such tasks at `status: needs-human`.
Silas approves by setting `approved_by_human: true` and `status: done` in the roadmap. The
resolver treats a gated task as still blocking until `approved_by_human: true`.

## The two roles

### Worker (OpenAI, hourly)
- Atomically claim: set `status: claimed`, `owner: worker`, bump `updated`, commit that
  one change to `main` with message `claim: <project>/<task-id>`.
- Branch `worker/<project>-<task-id>`. Do ONLY that task.
- **software:** open a PR into `main`, fill the handoff template, set task `status: review`.
- **content:** write the draft file, open a PR, set `status: needs-human`.
- **proposal:** write `pitches/<date>-<slug>.md` using the pitch template, open a PR, set
  `status: needs-human`.
- Never merge your own PR. Never push to `main` except the claim commit. One task at a time.

**Recurring tasks** (`recurring: true`, e.g. brainstorm/t-001): these never reach `done`.
After doing the work and opening the PR, set the task's `status` back to `ready` (not
`review`/`needs-human`) so it re-arms for a future cycle. The pitches it produces are the
output that goes to Silas — the task itself just keeps cycling. A recurring task that
produced nothing this cycle (e.g. pitch queue full) still re-arms to `ready`; note "no-op"
in the PR. Recurring tasks don't count toward milestone progress.

### Reviewer (Claude, event-triggered on `worker/*` PR opened)
- Read the project's `kind` first.
- **software, reversible, does the task, scoped:** approve, merge, `status: done`, bump updated.
- **Needs changes:** comment specifically, set `status: ready`, increment `passes`.
  At `passes == 3`, set `status: blocked` instead. Do NOT re-implement.
- **content / proposal / outward-facing / irreversible:** do NOT merge to live. Confirm the
  draft or pitch is well-formed, then leave at `status: needs-human` for Silas. (You may
  merge the file into main so it's visible, but never trigger publish/deploy/send.)

## Project art

Every project has three visual assets displayed in the kind_robots Workspace panel:
- **icon** (256×256, 1:1) — used in the detail header
- **card** (512×768, 2:3) — shown on the project card
- **hero** (1280×720, 16:9) — shown as a banner when a project is selected

Files are stored as `projects/images/{slug}-{type}.webp`. The workspace derives image URLs
from the slug automatically; missing files degrade gracefully to a placeholder.

**When creating or merging a new project**, add an entry to `projects/art-prompts.yaml`
with all three image blocks set to `status: pending`. See `ART-PROMPTS.md` at the repo
root for the template and all existing prompts.

Do not commit generated image binaries from agent runs — images are generated manually by
Silas using the prompts in `ART-PROMPTS.md` and uploaded directly.

## Hard safety rules (all agents, all kinds)
1. PRs only into `main` (except the Worker's atomic claim commit).
2. Drafts not live actions when stakes are high → `needs-human`, never auto-fire.
3. Iteration budget: 3 passes per software task, then `blocked`.
4. One task at a time.
5. Never touch DNS, secrets, billing, deploys, or send/publish anything without `needs-human`.
6. Scope discipline: unrelated problems become new `ready` tasks, not extra diff.

## PR handoff template (Worker fills in)
```
### Task
<project>/<task-id>: <one line>  (kind: software|content|proposal)

### What changed / what I produced
- bullets

### How I verified
- what you ran / checked

### Stakes
reversible | outward-facing | irreversible

### Notes for reviewer
```

## Pitch template (proposal-kind tasks → pitches/<date>-<slug>.md)
```
# Pitch: <title>
date: <iso>
project-target: <existing project name, or "new", or "ai-networker-itself">
status: awaiting-silas        # awaiting-silas | approved | rejected

## The idea
2-4 sentences.

## Why it's worth doing
## Rough effort
small | medium | large
## Suggested first task
What the Worker would do first if you approve.
```

## Status lifecycle
`ready` → `claimed` → `review` → `done`
Side exits: `blocked` (budget exhausted), `needs-human` (content/proposal/outward-facing/irreversible)
