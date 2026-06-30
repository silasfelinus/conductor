# AI_Networker — Agent Operating Manual

Standing instruction set for the coordinator. **Read it in full at the start of every
session before doing anything else.** Read by both the OpenAI Worker and the Claude
Reviewer, for every project.

## What this repo is

A service-agnostic spot where AI agents coordinate work on projects collaboratively, with
or without a human in the loop. The Worker (OpenAI) proposes work; the Reviewer (Claude)
reviews, critiques, and merges or escalates. The human (Silas) steers via each project's
`roadmap.yaml` and stays out of routine cycles.

Agents are not silent partners. Each role actively vets the other's output and methods —
not just once per PR but as a running practice. Critiques accumulate in TALKBACK files
and feed back into how both agents improve. When agents genuinely disagree, they escalate
rather than override each other.

Each project lives in `projects/<name>/` with its own `roadmap.yaml`.

## Project kinds — this changes what "done" means

Every roadmap declares a `kind`. It tells the Reviewer how to handle finished work:

- **software** — code work. Output is a PR. Reviewer merges reversible low-stakes PRs,
  bounces back the rest, escalates outward-facing/irreversible to `needs-human`.
- **content** — deliverables, not code (marketing plans, copy, content-pipeline output).
  Output is a file in the project folder. The Reviewer does NOT auto-publish anything;
  finished drafts go to `needs-human` for Silas to approve before anything goes live.
- **proposal** — the work IS a pitch for Silas to vet, not something to execute. Every
  task resolves by writing a pitch file to `pitches/` and setting `needs-human`. The
  Worker never implements a proposal-kind task beyond writing the pitch.

When unsure which bucket applies, treat it as the more cautious one (proposal > content >
software) and escalate.

## Todos — Silas's priority overrides

Silas creates Todos in the kind_robots workspace as lightweight, one-off tasks for agents
to handle. They are not tied to a project roadmap and archive themselves when done. Todos
take priority over roadmap tasks — if any are OPEN, handle the top one first.

**At the start of every Worker cycle:**
1. Run `python scripts/fetch_todos.py` (requires `KR_API_TOKEN` env var).
2. If it outputs any OPEN todos, handle **the first one** (sorted HIGH→NORMAL→LOW,
   newest first within the same priority) before touching any roadmap.
3. Treat the todo's `title` as the task description. The `description` field may name
   a specific project or provide context — follow it.
4. Apply normal project-kind rules: if the todo implies code work, open a PR;
   if it implies a draft/content, write the file; if it's a pitch, write to `pitches/`.
5. When the work is done (PR opened, file written, etc.), run:
   `python scripts/complete_todo.py <todo_id>`
   to mark it DONE in kind_robots. Silas will archive it when he's satisfied.
6. If `KR_API_TOKEN` is missing, log the warning and proceed to roadmap tasks normally.

**Todos are one-offs:** do not create follow-on roadmap tasks from a todo unless the
todo explicitly asks for it. Scope is exactly what the title/description says.

## Picking what to work on
1. **Check Todos first** — run `scripts/fetch_todos.py` and handle the top OPEN todo
   before continuing to roadmap tasks (see "Todos" section above).
2. **Read `CONTROL.md` first** — its global overview, then the block for the project you'll
   work on. CONTROL.md holds Silas's current intent and OVERRIDES anything in a roadmap it
   conflicts with. Then read this file, `projects/priority.yaml`, and the relevant
   `projects/*/roadmap.yaml` (skip `_template`).
3. **Check `project-overrides.yaml`** — skip any project where `status != active`. Paused,
   retired, and finished projects are off-limits; do not claim tasks for them.
4. Honor CONTROL.md's direction and notes, then each project's `notes_from_silas`, over
   default ordering. (STATUS.md is auto-generated and read-only — never edit it.)
5. Within the chosen project, take the highest-priority task with `status: ready`.
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

## Security model — who can do what

Every agent operates within a strict permission boundary. Acting outside it is a safety
violation regardless of whether the action seems helpful.

### Worker (OpenAI) — CAN
- Push to `worker/*` branches
- Make exactly ONE atomic claim commit to `main` per task cycle (message: `claim: <project>/<task-id>`)
- Open PRs from `worker/*` into `main`
- Set `status: claimed`, `status: review`, `status: needs-human`, `status: ready` (on retry)
- Append entries to `TALKBACK.md` (global) or `projects/<name>/TALKBACK.md` — never overwrite
- Set `status: challenged` on a task where it disagrees with the Reviewer's rejection
- Run `scripts/fetch_todos.py`, `complete_todo.py`, `resolve_deps.py`
- Create new `ready` tasks in roadmap.yaml for out-of-scope issues discovered during work

### Worker (OpenAI) — CANNOT
- Merge any PR, including its own
- Push to `main` beyond the single claim commit
- Push to branches named anything other than `worker/*`
- Set `approved_by_human: true` (Silas only)
- Set `status: done` directly (Reviewer does this on merge)
- Edit or delete another agent's TALKBACK entries
- Close, reopen, or force-push PRs

### Reviewer (Claude) — CAN
- Merge reversible, scoped, software PRs from `worker/*` branches
- Comment on PRs with specific, actionable feedback
- Set `status: done`, `status: ready`, `status: blocked`, `status: needs-human`
- Append entries to `TALKBACK.md` (global) or `projects/<name>/TALKBACK.md` — never overwrite
- Reference past TALKBACK entries when explaining a decision
- Create new `ready` tasks in roadmap.yaml for unrelated issues spotted during review
- Escalate a `challenged` task to `needs-human` for Silas to resolve

### Reviewer (Claude) — CANNOT
- Claim tasks, branch, or execute work (that is Worker's role exclusively)
- Set `approved_by_human: true` (Silas only)
- Merge content or proposal PRs to a live publishing endpoint
- Set `status: claimed` or push to `worker/*` branches
- Override a `gate_human: true` task without `approved_by_human: true` from Silas
- Force-resolve a `challenged` task unilaterally — escalate to Silas

### Neither agent — EVER
- Set `approved_by_human: true`
- Touch DNS, secrets, billing, or trigger a live deploy or publish
- Delete TALKBACK entries (the log is append-only)
- Skip a `needs-human` gate on an `outward-facing` or `irreversible` task
- Claim more than one task at a time

## The two roles

### Worker (OpenAI, hourly)
- **Step 0 — Todos**: run `python scripts/fetch_todos.py`. Handle the top OPEN todo if
  any exist (see "Todos" section). Call `complete_todo.py <id>` when done.
- **Step 1 — Resolve deps**: run `python scripts/resolve_deps.py`.
- **Step 2 — Claim**: atomically set `status: claimed`, `owner: worker`, bump `updated`,
  commit that one change to `main` with message `claim: <project>/<task-id>`.
- Branch `worker/<project>-<task-id>`. Do ONLY that task.
- **software:** open a PR into `main`, fill the handoff template (including "Flags for
  Reviewer"), set task `status: review`.
- **content:** write the draft file, open a PR, set `status: needs-human`.
- **proposal:** write `pitches/<date>-<slug>.md` using the pitch template, open a PR, set
  `status: needs-human`.
- Never merge your own PR. Never push to `main` except the claim commit. One task at a time.
- **After a Reviewer rejection:** read the Reviewer's feedback carefully. If you agree,
  fix and resubmit. If you disagree, write your case to the project's `TALKBACK.md` and
  set `status: challenged` — do not silently retry a disputed decision.

**Recurring tasks** (`recurring: true`, e.g. brainstorm/t-001): these never reach `done`.
After doing the work and opening the PR, set the task's `status` back to `ready` (not
`review`/`needs-human`) so it re-arms for a future cycle. The pitches it produces are the
output that goes to Silas — the task itself just keeps cycling. A recurring task that
produced nothing this cycle (e.g. pitch queue full) still re-arms to `ready`; note "no-op"
in the PR. Recurring tasks don't count toward milestone progress.

### Reviewer (Claude, event-triggered on `worker/*` PR opened)
- Read the project's `kind` first.
- **Before reviewing:** check the project's `TALKBACK.md` for any prior critique context
  on this task or recurring Worker patterns. Use it to calibrate your review.
- **software, reversible, does the task, scoped:** approve, merge, `status: done`, bump updated.
- **Needs changes:** comment specifically, set `status: ready`, increment `passes`.
  At `passes == 3`, set `status: blocked` instead. Do NOT re-implement.
- **content / proposal / outward-facing / irreversible:** do NOT merge to live. Confirm the
  draft or pitch is well-formed, then leave at `status: needs-human` for Silas. (You may
  merge the file into main so it's visible, but never trigger publish/deploy/send.)
- **After every review decision** (merge, reject, or escalate): append a brief entry to
  the project's `TALKBACK.md` noting your reasoning, any patterns you observed in the
  Worker's output, and any suggestions for how the Worker could improve. This is not
  optional — the critique log is how the system learns.
- **Kaizen on merge**: after every successful merge, create exactly one new `ready` task
  in the project's roadmap from the Worker's kaizen suggestion (or substitute your own if
  theirs is weak). One sentence title, `stakes: reversible`. This compounds improvement
  across cycles automatically.
- **On a `challenged` task:** read the Worker's TALKBACK entry carefully. If the Worker's
  case has merit, adjust your decision and append a response. If not, escalate to
  `needs-human` for Silas to arbitrate — never re-reject a challenge silently.

## Cross-vetting protocol

Agents are expected to critique each other's methods, not just the output of a single task.
This section defines how.

### What Worker critiques in Reviewer
- Decisions that seem inconsistent with AGENTS.md or CONTROL.md
- Rejections where the stated reason doesn't match the diff
- Patterns of over-escalation (sending reversible work to `needs-human` unnecessarily)
- Patterns of under-escalation (merging work that should have been gated)

### What Reviewer critiques in Worker
- Scope violations (doing more or less than the task specified)
- Verification gaps (claimed "verified" but didn't check the relevant thing)
- Template discipline (missing or thin sections in the handoff)
- Recurring mistakes across tasks (same error in multiple cycles)
- Dependency shortcuts (doing work before a gate is properly cleared)

### How to write a talkback entry

Both agents use this format. Append to `projects/<name>/TALKBACK.md` for project-specific
observations, or to the root `TALKBACK.md` for system-level patterns. Never edit or
delete existing entries.

```
## YYYY-MM-DD | <Worker|Reviewer> → <Reviewer|Worker> | <project>/<task-id> | <type>
type: critique | pattern | challenge | response | security-flag

**Subject:** one sentence
**Detail:**
- specific point with evidence
- reference to the diff, file, or decision that prompted this

**Suggested action:** what the other agent or Silas should do differently
```

### Challenge flow (Worker disputes a Reviewer decision)

1. Worker sets `status: challenged` on the task in `roadmap.yaml`.
2. Worker appends a `challenge` entry to the project's `TALKBACK.md` with its full case.
3. Reviewer reads the challenge entry and appends a `response` — either adjusting the
   decision (→ set `status: ready`, back to normal flow) or holding it (→ set
   `status: needs-human`, Silas arbitrates).
4. Silas resolves by editing the roadmap directly and leaving a note in the roadmap's
   task `note:` field. Challenged tasks never auto-resolve.
5. After resolution, both agents append a brief `response` entry noting what was learned.

A `challenged` task counts toward the iteration budget: if a task reaches `passes == 3`
via the normal retry loop, it goes to `blocked` as usual. Challenges and retries share the
same counter.

### Security flags

Either agent may append a `security-flag` entry to TALKBACK.md at any time. A security
flag is for observations about the system itself — scope creep, unexpected permissions,
suspicious patterns in PRs, or anything that makes the system less safe. Security flags
do NOT block the task cycle automatically, but they MUST be reviewed by Silas before
the next cycle that touches the flagged project. Include `security-flag: true` on the
relevant roadmap task if one exists.

## Project art

Every project has three visual assets displayed in the kind_robots Workspace panel:
- **icon** (`{slug}-icon.webp`, 256×256) — shown in the detail header
- **card** (`{slug}-card.webp`, 512×768) — shown on the project card
- **hero** (`{slug}-hero.webp`, 1280×720) — shown as a banner when a project is selected

Files live in `projects/images/`. The workspace derives URLs from the project slug; missing
files fall back to a placeholder automatically.

**When creating or merging a new project**, append three image request entries to
`ART-PROMPTS.md` at the repo root using the template in that file. Remove each entry once
its image file is committed to `projects/images/`. Do not commit generated image binaries
from agent runs — images are generated by Silas from the prompts and uploaded directly.

## Hard safety rules (all agents, all kinds)
1. PRs only into `main` (except the Worker's atomic claim commit).
2. Drafts not live actions when stakes are high → `needs-human`, never auto-fire.
3. Iteration budget: 3 passes per software task (retries + challenges share the counter), then `blocked`.
4. One task at a time.
5. Never touch DNS, secrets, billing, deploys, or send/publish anything without `needs-human`.
6. Scope discipline: unrelated problems become new `ready` tasks, not extra diff.
7. TALKBACK files are append-only: never edit or delete a prior entry from either agent.
8. A `security-flag` entry in TALKBACK.md must be acknowledged by Silas before the next
   cycle touches that project. Include a note in the task if one exists.
9. `STATUS.md` and `workspace.html` are auto-generated. Merge conflicts in these files
   always resolve to the latest version (accept main's copy, or the most recent CI commit).
   Never stop the cycle or escalate to `needs-human` for an auto-gen conflict.

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

### Flags for Reviewer
- anything I'm uncertain about
- past Reviewer decisions I'd like revisited on this task
- access or context limitations that affected the work
(omit section if nothing to flag)

### Kaizen suggestion
One specific, actionable improvement the next cycle could make (beyond this task's scope).
The Reviewer decides whether to create a task from it or defer.

### Notes for reviewer
```

## Reviewer feedback template (Reviewer appends to TALKBACK.md on every review)
```
## YYYY-MM-DD | Reviewer → Worker | <project>/<task-id> | <critique|pattern|response>

**Decision:** merged | rejected (pass N) | escalated to needs-human | challenge resolved

**What was good:**
- specific things the Worker did well

**What to improve:**
- specific, actionable critique with reference to the diff or output

**Kaizen task:** <task-id created> — <one sentence> (or "deferred — <reason>")
On every merge: create one new `ready` task in the project roadmap from the Worker's
kaizen suggestion (or your own if better). Mark it `stakes: reversible`. This is the
kaizen layer — targeted, compounding, one per merge. Deferred only if genuinely redundant.

**Pattern note:** (optional — only if this is a recurring issue across tasks)
- describe the pattern and link to prior instances in this file
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

Side exits:
- `blocked` — iteration budget exhausted (passes == 3)
- `needs-human` — content/proposal/outward-facing/irreversible, or challenge escalated
- `challenged` — Worker disputes Reviewer decision; always resolves to `needs-human` or back to `ready`
- `waiting` — dependency not yet met
