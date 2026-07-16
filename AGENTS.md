# AI_Networker — Agent Operating Manual

Standing instruction set for the coordinator. **Read it in full at the start of every
session before doing anything else.** Read by both the OpenAI Worker and the Claude
Reviewer, for every project.

## What this repo is

A service-agnostic spot where AI agents coordinate work on projects collaboratively, with
or without a human in the loop. The Worker (OpenAI) proposes work, implements scoped
changes, resolves merge friction, and may merge safe PRs. The Reviewer (Claude) reviews,
critiques, merges when appropriate, and escalates. The human (Silas) steers via each project's
`roadmap.yaml` and stays out of routine cycles.

Agents are not silent partners. Each role actively vets the other's output and methods —
not just once per PR but as a running practice. Critiques accumulate in TALKBACK files
and feed back into how both agents improve. When agents genuinely disagree, they escalate
rather than override each other.

Each project lives in `projects/<name>/` with its own `roadmap.yaml`.

## Project kinds — this changes what "done" means

Every roadmap declares a `kind`. It tells agents how to handle finished work:

- **software** — code work. Output is a PR. Reversible, scoped, low-stakes PRs may be
  merged by the Worker or Reviewer after verification. Outward-facing/irreversible work
  escalates to `needs-human`.
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
4. Apply normal project-kind rules: if the todo implies code work, open a PR and merge it
   when it is safe; if it implies a draft/content, write the file; if it's a pitch, write
   to `pitches/`.
5. When the work is done (PR merged/opened, file written, etc.), run:
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
   If none anywhere, stop — do not invent work. (Exceptions: a proposal-kind project may
   have a standing instruction to generate N pitches per cycle — follow its roadmap; and
   `autonomous: true` projects follow the "Autonomous projects — never idle" rule below.)
6. **Claim it before doing real work**: run
   `python scripts/claim_task.py <project> <task-id> --owner <worker|reviewer> --session <id>`.
   This checks the task's live state on `origin/main` (not your local checkout, which
   may be stale) and, if claimable, pushes a small `status: claimed` commit straight to
   `origin/main` before you write any implementation. If it exits non-zero
   (`ALREADY_CLAIMED`), someone else is already on that project/task — do not implement
   it; go back to step 5 and pick the next `ready` task instead. See "Rotation
   collisions" below for why this step exists.

### Rotation collisions

Picking a task from `priority.yaml`/`next_ready_task.py` only reads roadmap state — it
does not reserve anything. Two sessions triggered close together (e.g. concurrent
hourly burst-mode runs) can both read the same stale `ready` state, both fully
implement the same project/task, and only discover the collision when one of them
pushes. This happened for real on 2026-07-14 (`animation-manager/t-008` built twice —
see `TALKBACK.md` and `conductor/t-040`). Step 6 above (`claim_task.py`) exists
specifically to close this gap: it re-checks `origin/main` immediately before writing
the claim and retries under a push race, so a losing session fails fast into
`ALREADY_CLAIMED` instead of duplicating work. If a claiming session crashes before
finishing, the claim self-expires after `CLAIM_TTL_MINUTES` (90 minutes, see
`scripts/roadmap_claims.py`) so the task doesn't stay locked forever — `next_ready_task.py`
surfaces a stale-claimed task as pickable again automatically.

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

### Hard vs soft needs-human

`needs-human` has two flavors — agents must distinguish them:

**Hard** (Silas must act before anything proceeds):
- `gate_human: true` on the task
- `stakes: outward-facing` or `stakes: irreversible`
- Content or proposal kind reaching publication/delivery
- Security flags requiring acknowledgement

**Soft** (agent got stuck, no workaround found — but other work can continue):
- Connector/tooling failure mid-task where content is complete
- Unclear architectural direction without a blocking dependency
- Access limitation that prevents verification but doesn't invalidate the work

On a **soft** `needs-human`: set the task status, add `soft_gate: true`, document the reason clearly in the task
`note:`, then **immediately re-run task selection** and pick the next available `ready` task.
Do not end the cycle — there is almost always other work. Only stop if every ready task is
also blocked. `soft_gate: true` is metadata for auditors and coordinators; it never satisfies a dependency
or grants permission for outward-facing work.

On a **hard** `needs-human`: stop. Do not pick another task. Flag clearly for Silas.

**Scope gates on NEW projects are soft** (Silas, 2026-07-04): when a fresh project or
pitched idea lands, do not park it behind scope approval. Build the design brief and
start working immediately; raise the scope-confirmation task as a soft needs-human that
runs in parallel with development. Course correction after Silas responds is cheap and
expected — the bias is toward making things happen. (Outward-facing/irreversible steps
remain hard gates as always.)

**Autonomous projects — never idle** (Silas, 2026-07-10): a roadmap may declare
`autonomous: true` (first test run: ai-art-academy). These projects must keep moving
without Silas's input:
- Escalate only ACTUAL human gates — spend, publishing, outward-facing/irreversible
  steps, licensing doubts, backend schema needs. Everything else: decide, record the
  decision in the task note or docs, and keep building. Scope confirmations are soft
  gates that run in parallel; course-correct when Silas replies.
- When an autonomous project has no `ready` task, the Worker does NOT stop or invent
  arbitrary work — it may create and immediately claim exactly ONE improvement task
  from the standing menu: (a) a style/polish pass on the project's front end, (b) a
  roadmap upgrade (refine tasks, detail the next milestone, prune stale notes), (c)
  generate more art inspirations or content assets, (d) expand the project's
  docs/curriculum/content. `stakes: reversible`, normal PR flow, one per cycle.
  Prefer a recurring roadmap task that encodes this menu (e.g. ai-art-academy/t-010)
  over ad-hoc task creation when one exists.
- All other safety rules still apply unchanged — autonomy widens WHAT gets worked on,
  never WHO can approve gates.

**Generated art is pre-approved** (Silas, 2026-07-06): internal auto-generated project art
is not a human gate. Agents may request, create, commit, and promote generated images for
project icons/cards/heroes, inspirations, ArtCollections, Dream images, Bot avatars, and Bot
emotion/action portraits when the action is task-scoped, traceable, and reversible. Keep the
prompt/model/source metadata needed to recreate or delete the image. This does not authorize
publishing, external posting, paid tool spend, production deploys, billing, secrets, or DNS.

### Writing needs-human task notes for Silas (not for agents)

When a task ends at `needs-human`, rewrite the `note:` field so Silas can act on it
without reading the surrounding code or roadmap. Use this structure:

```
FOR SILAS: What was produced and where to find it (file path, one sentence).
What it contains (2-3 specific things, not agent jargon).
TO APPROVE: What Silas needs to read, decide, or change — and the exact edit
to make (set approved_by_human: true and status: done, or add a note with X).
What unblocks when he does (next task id + what it will do).
```

Do NOT write the note for the next agent to read. The agent reads the roadmap;
Silas reads the note. Agent-facing context belongs in the PR description.

## Security model — who can do what

Every agent operates within a strict permission boundary. Acting outside it is a safety
violation regardless of whether the action seems helpful.

### Worker (OpenAI) — CAN
- Push to `worker/*` branches
- Make exactly ONE atomic claim commit to `main` per task claimed (message: `claim: <project>/<task-id>`)
- Open PRs from `worker/*` into `main`
- Merge its own reversible, scoped, verified PRs when they are not human-gated, outward-facing, irreversible, or otherwise unsafe
- Smartly fix merge conflicts before merging; preserve independent valid changes and never delete conflicting work just to make Git happy
- Set `status: claimed`, `status: review`, `status: needs-human`, `status: ready` (on retry), and `status: done` after a successful safe merge
- Append entries to `TALKBACK.md` (global) or `projects/<name>/TALKBACK.md` — never overwrite
- Append outcome records to `LEARNING.yaml` when closing a task (append-only, like TALKBACK)
- Set `status: challenged` on a task where it disagrees with the Reviewer's rejection
- Run `scripts/fetch_todos.py`, `complete_todo.py`, `resolve_deps.py`
- Create new `ready` tasks in roadmap.yaml for out-of-scope issues discovered during work

### Worker (OpenAI) — CANNOT
- Merge work that is human-gated, outward-facing, irreversible, security-sensitive, or blocked by failed verification unless Silas explicitly approves it
- Push to `main` beyond the single claim commit and normal PR merges
- Push to branches named anything other than `worker/*`
- Set `approved_by_human: true` (Silas only)
- Edit or delete another agent's TALKBACK entries
- Close, reopen, or force-push PRs unless Silas explicitly directs it in the current session

### Cross-repo tasks

Some roadmap tasks describe changes in another Silas-owned repository, such as `kind_robots`,
`serendipity-voice`, or `portos`. The conductor roadmap still owns the task state, but the
code patch belongs in the target repository.

When a cross-repo task is selected:
1. Claim the conductor roadmap task exactly as usual on `main`.
2. Create the implementation branch in the target repository as `worker/<project>-<task-id>`
   when the connector/tooling allows it. Open the PR against that repository's `main` branch,
   then update the conductor roadmap task from the conductor repo branch.
3. If the connector blocks target-repo branch creation or writes, do not improvise a live
   workaround and do not switch to a non-`worker/*` branch. Preserve the intended patch as a
   conductor documentation handoff instead.
4. Use `projects/<project>/docs/<task-id>-<short-slug>.md` for the fallback handoff. Include:
   the target repository, intended branch name, files that would change, exact patch/code or
   implementation steps, verification that was possible, verification still needed, and any
   safety boundaries.
5. Open the conductor PR with the handoff document and set the roadmap task to soft
   `needs-human` unless the task output is fully complete in conductor. The note should tell
   Silas where the handoff lives, what it contains, what blocked the direct target-repo PR,
   and whether the next action is "apply this patch in the target repo" or "flip back to
   ready after access is fixed."
6. Never treat a preserved handoff as a live implementation. Do not mark target-repo code work
   `done` unless the actual target-repo change was merged or Silas explicitly marks it done.

This keeps blocked cross-repo work visible and reviewable without bypassing branch, repo,
secret, deploy, or human-gate boundaries.

### Rescue / salvage PRs — delete the superseded branch in the same session

When a rescue or salvage PR rebuilds stranded work from a stale `worker/*` or `claude/*`
branch onto current `main` and supersedes that branch, **delete the superseded branch in
the same session the rescue PR merges** — do not leave it for a later cycle to rediscover.
A stale branch that has diverged from the rescue merge can be reopened as its own PR and
reintroduce already-superseded or conflicting content. (It only merges as a harmless no-op
when its diff is byte-identical to what the rescue already landed — don't count on that.)
If the rescue PR's own body says a branch "can be deleted," treat that as the instruction to
delete it now, not an observation for later. (Kaizen from challenge-center/t-002 resolution,
2026-07-07: kind_robots PR #116 rescued t-002's work and said the old
`worker/challenge-center-t-002` branch could be deleted, but it was instead reopened as PR
#118 and merged separately ~10 minutes later.)

### Reviewer (Claude) — CAN
- Merge reversible, scoped, software PRs from `worker/*` branches
- Merge additive-only database migration PRs after auditing `migration.sql`
  line-by-line — every statement must be `CREATE TABLE` / `ADD COLUMN` /
  `CREATE INDEX` / `ADD CONSTRAINT` / `DROP INDEX` (constraint swaps only);
  no `DROP` of tables/columns/data, no data rewrites. This holds even though
  merge-to-main deploys the migration to prod (Silas, 2026-07-05 — resolves the
  gate_human ambiguity flagged in challenge-center t-001's TALKBACK). Destructive
  or ambiguous migrations remain hard `needs-human`.
- Merge reversible, scoped, software PRs from `claude/*` branches when the work was
  directed by Silas in the session (e.g. conductor tooling improvements, startup hooks,
  ops scripts). Treat these identically to Worker PRs for review purposes.
- Comment on PRs with specific, actionable feedback
- Set `status: done`, `status: ready`, `status: blocked`, `status: needs-human`
- Append entries to `TALKBACK.md` (global) or `projects/<name>/TALKBACK.md` — never overwrite
- Append outcome records to `LEARNING.yaml` when closing a task (append-only, like TALKBACK)
- Write, overwrite, or remove the `retry_context:` field on a task per the Failure triage rules
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
- Hold more than one claimed task at once (claims are sequential — finish, hand off, or cleanly park one before claiming the next)

## The two roles

### Worker (OpenAI, hourly)
- **Step 0 — Todos**: run `python scripts/fetch_todos.py`. Handle the top OPEN todo if
  any exist (see "Todos" section). Call `complete_todo.py <id>` when done.
- **Step 1 — Resolve deps**: run `python scripts/resolve_deps.py`.
- **Step 2 — Claim**: run `python scripts/claim_task.py <project> <task-id> --owner worker
  --session <id>` (see "Rotation collisions" above). It checks `origin/main` fresh,
  refuses if another session already claimed the task, and otherwise pushes the
  `status: claimed`/`owner: worker`/`updated` commit straight to `main` for you. On
  `ALREADY_CLAIMED`, do not implement this task — pick the next `ready` task instead.
- Branch `worker/<project>-<task-id>`. Do ONLY that task.
- **software:** open a PR into `main`, fill the handoff template (including "Flags for
  Reviewer"), set task `status: review`, verify it, resolve conflicts if present, and merge
  it when safe. After a successful safe merge, set task `status: done`.
- **content:** write the draft file, open a PR, set `status: needs-human`.
- **proposal:** write `pitches/<date>-<slug>.md` using the pitch template, open a PR, set
  `status: needs-human`.
- Keep the default outcome as an updated `main` branch unless the task is unsafe, human-gated,
  outward-facing, irreversible, or genuinely blocked. Work one task in flight at a
  time — you may complete several tasks in a single run, but finish (merge, hand off,
  or cleanly park) each before claiming the next. Never hold two active claims at once.
- **On closing a task at `done`** (e.g. after a safe self-merge): append the outcome record
  to `LEARNING.yaml`.
- **Merge conflicts:** resolve them intelligently. Keep both sides when they are independent,
  follow CONTROL.md and Silas notes when they conflict, and for `STATUS.md` / `workspace.html`
  accept the latest generated/main version. Re-check relevant verification after fixing conflicts.
- **After a Reviewer rejection:** read the Reviewer's feedback AND the task's
  `retry_context:` carefully before re-claiming — never retry blind. If you agree,
  fix and resubmit, saying in "Flags for Reviewer" how the retry addressed the
  retry_context. If you disagree, write your case to the project's `TALKBACK.md` and
  set `status: challenged` — do not silently retry a disputed decision.

**Recurring tasks** (`recurring: true`, e.g. brainstorm/t-001): these never reach `done`.
After doing the work and opening/merging the PR, set the task's `status` back to `ready`
(not `review`/`needs-human`) so it re-arms for a future cycle. The pitches it produces are the
output that goes to Silas — the task itself just keeps cycling. A recurring task that
produced nothing this cycle (e.g. pitch queue full) still re-arms to `ready`; note "no-op"
in the PR. Recurring tasks don't count toward milestone progress.

### Reviewer (Claude, event-triggered on `worker/*` PR opened)
- Read the project's `kind` first.
- **Before reviewing:** check the project's `TALKBACK.md` for any prior critique context
  on this task or recurring Worker patterns. Use it to calibrate your review.
- **software, reversible, does the task, scoped:** approve and merge if the Worker has not
  already merged it; otherwise audit the result and append TALKBACK if useful.
- **Needs changes:** triage the failure first (see "Failure triage" — only quality/scope
  consume a pass; transient/actionable failures route differently and never do). For a
  quality/scope rejection: comment specifically, write `retry_context:` on the task,
  set `status: ready`, increment `passes`. At `passes == 3`, set `status: blocked`
  instead and append the ledger record. Do NOT re-implement.
- **content / proposal / outward-facing / irreversible:** do NOT merge to live. Confirm the
  draft or pitch is well-formed, then leave at `status: needs-human` for Silas. (You may
  merge the file into main so it's visible, but never trigger publish/deploy/send.)
- **After every review decision** (merge, reject, audit, or escalate): append a brief entry to
  the project's `TALKBACK.md` noting your reasoning, any patterns you observed in the
  Worker's output, and any suggestions for how the Worker could improve. This is not
  optional — the critique log is how the system learns.
- **Log commits must reach main**: TALKBACK/roadmap commits made on a session branch are only
  preserved if that branch gets a PR — never end a session with log commits stranded on an
  unPR'd branch.
- **Ledger on close**: whenever your decision closes a task (`done` after merge, or
  `blocked` at passes == 3), append the outcome record to `LEARNING.yaml` — including
  the failure category and a one-line lesson.
- **Kaizen on merge**: after every successful merge, create exactly one new `ready` task
  in the project's roadmap from the Worker's kaizen suggestion (or substitute your own if
  theirs is weak). One sentence title, `stakes: reversible`. This compounds improvement
  across cycles automatically. Check `LEARNING-REPORT.md` first — target a systematic
  weakness over a generic improvement when one applies (see "Learning ledger").
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
- Merge discipline problems (dropping valid changes, skipping conflicts, or failing to re-check after conflict fixes)

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

## Failure triage — classify before you retry or escalate

(Adopted 2026-07-11 from the PortOS CoS error-triage design — see
`docs/2026-07-11-portos-cos-learnings.md`.) A failed pass is not one thing. Before
deciding what happens next, whoever observed the failure (Worker mid-task, or Reviewer
on rejection) assigns one of four categories. The category decides whether the pass
budget is spent and where the task goes:

| Category | What it looks like | Route | Consumes a pass? |
|---|---|---|---|
| **transient** | Environment hiccup unrelated to the work: connector/tooling failure, rate or session limits, CI flake, generated-file merge noise, network errors | Retry within the cycle if cheap; otherwise leave `ready` with a note and move to other work | No |
| **actionable** | The task cannot succeed as specified no matter how many retries: missing access/credentials for the core work, stale or wrong task spec, an undeclared dependency, verification permanently impossible | Do NOT retry. Fix the roadmap (add `depends_on`, create the prerequisite task) or go straight to soft `needs-human` with a FOR SILAS note | No — retrying is waste |
| **quality** | The work was attempted and is wrong: bugs, scope violations, verification gaps, doesn't do what the task says | Reviewer rejects with `retry_context` (below), task back to `ready`, Worker retries | Yes — this is what the budget is for |
| **scope** | The task is too big to land in one pass: oversized diff, half-finished work, "and also" sprawl | Split it: create smaller `ready` tasks covering the remainder; the original either shrinks to its landable core or goes `waiting` on the new parts | Yes (the failed attempt), but stop retrying the monolith |

Rules:
- Only **quality** and **scope** failures increment `passes`. A transient or actionable
  failure never burns the budget — the budget exists to bound *rework*, not to punish
  environment problems.
- **Sandbox egress blocks** (a `transient` network failure that recurs across sessions,
  e.g. a museum/CDN/API host the agent proxy's allowlist rejects) belong in the shared
  `EGRESS-BLOCKERS.md` ledger, not a new hand-written "RECHECKED &lt;date&gt;..." paragraph
  on the task. Run `python scripts/recheck_egress_blocks.py <host> --task <project>/<task-id>`
  to probe and stamp a dated entry; link the task note to the ledger instead of repeating
  the recheck prose each cycle (conductor/t-052).
- On **actionable**: escalate or fix the roadmap the FIRST time. Burning three passes on
  a task that can never succeed as specified is the failure mode this section exists to
  prevent.
- On **scope**: prefer decomposition over a third heroic attempt. Scope discipline
  (hard rule 6) already says unrelated problems become new tasks — this extends it to
  oversized related work.
- The Reviewer records the category as `**Failure category:**` in its rejection feedback
  and in the learning ledger (below). A Worker that self-triages mid-task records it in
  the task `note:`.
- When genuinely unsure between transient and quality, treat it as quality (spend the
  pass). When unsure between quality and actionable, spend one pass before escalating.

### Retry context — failed passes must teach the next one

When the Reviewer rejects a task (`status: ready`, `passes` incremented), it also writes
a `retry_context:` field on the task in `roadmap.yaml`:

```yaml
retry_context: >
  pass 1 failed (quality): <what specifically went wrong, with file/PR reference>.
  Do differently: <the concrete change of approach for the next attempt>.
```

- The Worker MUST read `retry_context` before re-claiming any task with `passes > 0`,
  and the retry PR's "Flags for Reviewer" section must say how the attempt addressed it.
- The Reviewer overwrites `retry_context` on each subsequent rejection (git history
  preserves priors) and removes the field when the task reaches `done`.
- A task at `passes > 0` with no `retry_context` is a template-discipline gap — the
  Worker should note it in TALKBACK and reconstruct the context from the PR comments
  before retrying blind.

## Learning ledger — outcomes feed back into behavior

Kaizen improves the system one suggestion per merge; the ledger makes *systematic*
weaknesses visible across tasks, projects, and cycles (adopted from the PortOS CoS
task-learning design). `LEARNING.yaml` at the repo root is an append-only ledger of
task outcomes.

**When a task closes** (`done`, `blocked`, or cancelled by Silas), the agent that closes
it appends one record:

```yaml
- date: YYYY-MM-DD
  project: <slug>
  task: <task-id>
  kind: software | content | proposal
  stakes: reversible | outward-facing | irreversible
  passes: <final pass count>
  outcome: done | blocked | cancelled
  failure_category: transient | actionable | quality | scope | null
  lesson: "one sentence — what the next similar task should know"
```

- Append-only, same rule as TALKBACK: never edit or delete a prior record.
- `failure_category` is `null` for clean first-pass successes; for anything that burned
  a pass or blocked, use the triage category of the *dominant* failure.
- Recurring tasks don't get a record per cycle — only if one cycle blocks or teaches
  something worth a `lesson`.
- `python scripts/build_learning_summary.py` regenerates `LEARNING-REPORT.md`
  (auto-generated, read-only — same rules as STATUS.md / KAIZEN.md).
- **Kaizen targeting:** before creating the kaizen task on a merge, the Reviewer checks
  `LEARNING-REPORT.md`. If a systematic weakness (success rate < 60% for a project or
  kind with 3+ records, or a failure category recurring 3+ times) applies to the project
  at hand, the kaizen task targets that weakness instead of a generic improvement.

## Project art

Every project has three visual assets displayed in the kind_robots Workspace panel:
- **icon** (`{slug}-icon.webp`, 256×256) — shown in the detail header
- **card** (`{slug}-card.webp`, 512×768) — shown on the project card
- **hero** (`{slug}-hero.webp`, 1280×720) — shown as a banner when a project is selected

Files live in `projects/images/`. The workspace derives URLs from the project slug; missing
files fall back to a placeholder automatically.

**Image intake pipeline** (`projects/process/` → `scripts/distribute_images.py`, run
automatically by the distribute-images workflow on pushes to main): each file routes by
art-generate.yaml / art-prompts.yaml entry, then filename convention. A file that matches a
known slug but has no specific resolution (e.g. `{slug}-inspiration.webp`, `{slug}-sketch.webp`)
becomes a new inspiration at kind_robots `public/images/{slug}/{slug}-inspiration-{n}.webp` —
a slug's folder there IS its art collection, tracked by a `gallery.json` manifest the script
maintains. If a distributed image would replace an existing file, the original is moved into
its slug's inspiration folder first and the new image takes its place. Files that match
nothing land in `projects/process/unmatched/` for Silas.

**Generated image approval rule:** Silas lifted the old approval block on 2026-07-06. Agents
may let the auto generator create images without asking first, and generated outputs may move
into canonical project images, ArtCollection inspirations, Dream images, Bot avatars, or Bot
emotion/action portraits when the task calls for it. This is intentionally low-stakes: generated
images are disposable and easy for Silas to delete, replace, or regenerate. Preserve prompt,
model, seed/source path, destination, and project slug metadata whenever practical so the image
can be traced or recreated. Do not use this rule to publish externally, spend money, modify
secrets/DNS/billing, or bypass any unrelated human gate.

**When creating or merging a new project**, append three image request entries to
`ART-PROMPTS.md` at the repo root using the template in that file. Remove each entry once
its image file is committed to `projects/images/`. Agents may also generate and commit those
assets directly through the auto art pipeline when a scoped task requests it; no separate
Silas approval is required for the image generation itself.

## Hard safety rules (all agents, all kinds)
1. PRs only into `main` (except the Worker's atomic claim commit).
2. Drafts not live actions when stakes are high → `needs-human`, never auto-fire.
3. Iteration budget: 3 passes per software task (retries + challenges share the counter), then `blocked`.
   Only quality/scope failures consume a pass — transient and actionable failures never do (see "Failure triage").
4. One task *in flight* at a time. A single run may complete several tasks sequentially —
   finish, hand off, or cleanly park each (its own atomic claim commit, its own scoped PR)
   before claiming the next. Never hold two active claims at once.
5. Never touch DNS, secrets, billing, deploys, or send/publish anything without `needs-human`.
6. Scope discipline: unrelated problems become new `ready` tasks, not extra diff.
7. TALKBACK files are append-only: never edit or delete a prior entry from either agent.
8. A `security-flag` entry in TALKBACK.md must be acknowledged by Silas before the next
   cycle touches that project. Include a note in the task if one exists.
9. `STATUS.md` and `workspace.html` are auto-generated. Merge conflicts in these files
   always resolve to the latest version (accept main's copy, or the most recent CI commit).
   Never stop the cycle or escalate to `needs-human` for an auto-gen conflict.
10. Never run destructive database commands — `prisma migrate reset`, `DROP DATABASE`,
    `DROP TABLE`, bulk deletes — against any environment, including dev. Databases hold
    real data; a reset happens only when Silas explicitly orders one in the current
    session. Repair migration drift with data-preserving steps (targeted SQL via
    `prisma db execute`, then `prisma migrate resolve --applied`), and never rename or
    edit a migration that may already be applied somewhere — ship a new migration instead.

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

**Decision:** merged | rejected (pass N) | escalated to needs-human | challenge resolved | audited already-merged work

**Failure category:** (rejections/blocks only) transient | actionable | quality | scope —
per the "Failure triage" section. Quality/scope: also write `retry_context:` on the task.

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
`ready` → `claimed` → (`review` optional) → `done`

Side exits:
- `blocked` — iteration budget exhausted (passes == 3, quality/scope failures only —
  see "Failure triage"). Closing agent appends a `LEARNING.yaml` record.
- `needs-human` — hard gate (gate_human/outward-facing/irreversible/content+proposal) OR soft
  escalation (stuck, connector failure, unclear path). Hard: stop cycle. Soft: continue to
  next ready task. Document which kind in the task `note:`.
- `challenged` — Worker disputes Reviewer decision; always resolves to `needs-human` or back to `ready`
- `waiting` — dependency not yet met
