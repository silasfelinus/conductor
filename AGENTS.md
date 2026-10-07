# AI_Networker — Agent Operating Manual

Standing instruction set for the coordinator. **Read it in full at the start of every
session before doing anything else.** Read by both the OpenAI Worker and the Claude
Reviewer, for every project.

## What this repo is

A service-agnostic spot where AI agents coordinate work on projects collaboratively, with
or without a human in the loop. The Worker (OpenAI) proposes work, implements scoped
changes, resolves merge friction, and merges safe PRs. The Reviewer (Claude) reviews,
critiques, merges when appropriate, and escalates. Both aim to end every run with a clean
`main` — safe work merged, no branch left behind (see "Finish on clean main"). The human
(Silas) steers via each project's `roadmap.yaml` and stays out of routine cycles.

Agents are not silent partners. Each role actively vets the other's output and methods —
not just once per PR but as a running practice. Critiques accumulate in TALKBACK files
and feed back into how both agents improve. When agents genuinely disagree, they escalate
rather than override each other.

Each project lives in `projects/<name>/` with its own `roadmap.yaml`.

## Token discipline — context is the budget

Every hourly Routine run and every subagent pays for what it loads. Default to the smallest read
that answers the question (2026-09-30 token-essentialization pass):

- **Load the core, not the library.** Read this file in full; read a role playbook
  (`docs/agents/roles/`) only for the role `select_role.py` names in `playbook`; read
  `docs/sweep-checks.md`, `docs/agents/frontend-verification.md` or
  `docs/agents/git-troubleshooting.md` only when that situation comes up.
- **One sweep call.** `python scripts/session_sweep.py` runs every startup check and prints one
  line each plus the tail of anything flagged. Don't run the checks one by one, and don't re-run
  what the SessionStart hook already printed (git state, open PRs, ready/claimed tasks).
- **Never read a big file whole.** `TALKBACK.md` (>1MB), `projects/*/HISTORY.md`, run logs, and the
  large roadmaps (conductor ~240KB, interface-vision/kind-robots/storybook ~170KB each):
  - one task → `python scripts/show_task.py <project>/<task-id>` (`--no-note` / `--note-tail N`);
  - a project's task list → `python scripts/show_task.py <project> --list --status ready`;
  - TALKBACK → `tail -n 80 TALKBACK.md`, or `grep -n` for a task id then `sed -n 'A,Bp'`;
  - anything else → `grep -n` first, then read only the matching line range.
- **Trim tool output at the source.** `pytest -q` (add `-x`/a path while iterating), `git log --oneline`,
  `| tail -n 40` on long builds; GitHub MCP with `minimal_output`/small `perPage`, and `get_job_logs`
  with `failed_only` + `tail_lines`. Don't re-read a file you just edited to verify it.
- **Subagents get a brief, not a transcript.** Give a subagent file paths and the exact question — not
  pasted file contents, and not "read AGENTS.md first" unless it will make rule-bound changes (then point
  it at the specific section). Use `Explore` for read-only searches, and pass `model: "haiku"` or
  `"sonnet"` for mechanical lookups/greps; keep the session's own model for judgment calls. Ask for a
  short conclusion back, not file dumps. Git-mutating subagents still need `isolation: 'worktree'`
  (hard safety rule 11).
- **Recurring no-op cycles rest; gated ones don't re-arm.** Re-arm a cycle that found nothing to do
  with `close_task.py ... ready --noop` (2h→48h backoff every picker honors); send a cycle whose next
  step is Silas's call to `needs-human`. Details: `docs/agents/roles/worker.md` "No-op re-arms rest".
- **Don't narrate history into new text.** Put incident history in the task note / HISTORY.md / TALKBACK,
  and keep instructions in this file and CLAUDE.md to the rule plus a one-line why — both files are
  loaded by every session, so every sentence added there is paid for on every run.

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

## GitHub issues become roadmap tasks

Silas also files work as GitHub issues. The hourly `issue-bridge.yml` workflow
(`scripts/sync_github_issues.py`) mirrors each open collaborator-authored issue in a
repos.yaml repo into its owning project's roadmap as an ordinary `ready` task carrying
`source_issue: <owner/repo>#<n>`, so issues are picked up through the normal roadmap
queue rather than a separate inbox. Before it existed nothing read issues at all, and
kind_robots #2663–#2668 sat open for three weeks (2026-10-01).

- Work a mirrored task like any other. Its note opens with the issue URL; the issue
  thread is the spec, so read its comments too.
- Put `Closes <owner/repo>#<n>` in the implementing PR so the issue closes on merge.
  The bridge also closes an issue once its task is `done`, so a missed keyword is
  backstopped, not lost.
- Never hand-edit or remove `source_issue`: it is the idempotency key, and without it
  the next run imports the issue again.
- Routing: a `project:<slug>` label beats the default (the first repos.yaml entry for
  the repo); `conductor:skip` keeps an issue out. Issues from non-collaborators and
  issues whose project is paused/retired/finished are reported by the sweep
  (`issue_bridge`), never auto-imported.

## Picking what to work on
1. **Check Todos first** — run `scripts/fetch_todos.py` and handle the top OPEN todo
   before continuing to roadmap tasks (see "Todos" section above).
2. **Read `CONTROL.md` first** — its global overview, then the block for the project you'll
   work on. CONTROL.md holds Silas's current intent and OVERRIDES anything in a roadmap it
   conflicts with. Then read this file, `projects/priority.yaml`, and the relevant
   `projects/*/roadmap.yaml` (skip `_template`).
3. **Check `project-overrides.yaml`** — lifecycle is authoritative. Work finite
   `status: active` projects first. Only when no active project has claimable ready work may
   `status: continuous` projects run, in priority order. Paused, retired, and finished projects
   are off-limits. Continuous is intentionally a fallback tier, not an equal-priority synonym
   for active.
4. Honor CONTROL.md's direction and notes, then each project's `notes_from_silas`, over
   default ordering. (STATUS.md is auto-generated and read-only — never edit it.)
5. Within the selected lifecycle tier/project, take the highest-priority task with
   `status: ready`. If a finite active project's list reaches zero open tasks, do NOT infer
   completion from N/N. Reconcile its `goal` against the actual product and add missing work
   or explicitly finish/pause it. A user-facing software project is not `finished` until its
   live/preview front end has been checked at phone/tablet/desktop widths and Silas has either
   accepted the visual state or explicitly waived that check in the current session. Proposal
   projects may keep their documented pitch cadence. Never-idle work belongs to the continuous
   lifecycle described below, not to an exhausted finite active roadmap.
6. **Claim it before doing real work**: run
   `python scripts/claim_task.py <project> <task-id> --owner <worker|reviewer> --session <id>`.
   This checks the task's live state on `origin/main` (not your local checkout, which
   may be stale) and, if claimable, pushes a small `status: claimed` commit straight to
   `origin/main` before you write any implementation. If it exits non-zero
   (`ALREADY_CLAIMED`), someone else is already on that project/task — do not implement
   it; go back to step 5 and pick the next `ready` task instead. See "Rotation
   collisions" below for why this step exists.
   Pick a collision-resistant `--session <id>`: a full ISO timestamp with seconds
   plus a short task-specific suffix (or a random token), not a coarse hour/rotation
   label — `claim_task.py` keys on project/task rather than session id, so a reused
   label never causes a false claim conflict, but it does leave the `claimed_by`/
   TALKBACK trail looking like one continuous session did unrelated work when two
   concurrent burst-mode sessions happen to reuse the same label within the same
   hour (coat-dance/t-001, 2026-07-21 — see root `TALKBACK.md` same date).
   **Connector-only Workers** (connected GitHub tools but no local shell/Python)
   claim, review, and close out through session-aware `task-events` instead:
   a `claim` event now **requires** a non-empty, collision-resistant `session`,
   the processor writes `claimed_by`/`claimed_at` and preserves the same atomic
   `ALREADY_CLAIMED` invariant as `claim_task.py` (a rival session's claim is
   consumed as a collision with no roadmap mutation, not collapsed into an
   owner-level no-op), and `review`/`done` events may carry a matching `session`
   so a session that lost the claim cannot later close the winner's task. See
   `docs/github-connector-worker.md` for the full connector runbook.
7. **Set `status: review` before opening the PR — every session, not just hourly
   `worker/*` runs.** This applies equally to Silas-directed `claude/*` sessions and
   burst-mode cycles doing Worker-style roadmap pickup, not only the OpenAI hourly
   Worker. Once implementation is done and you're about to `gh pr create` (or the
   GitHub MCP equivalent), run
   `python scripts/close_task.py <project> <task-id> review --session <id>` (own
   branch + its own small PR into `main` — **never** `set_task_field.py` followed by
   a direct commit/push, and never a direct push to `main` the way `claim_task.py`'s
   single atomic claim commit is sanctioned to do). `close_task.py` is not just for
   `done`: its `status` argument is generic (its own docstring's usage examples cover
   `done`, `needs-human`, and this `review` case identically), so the same
   collision-resistant, fetch-checked-against-`origin/main` git plumbing that avoids
   a stale-branch merge conflict on `done`/`needs-human` also covers `review` — no
   new script needed. (Resolved conductor/t-119, 2026-08-20: AGENTS.md previously left
   this transition's landing mechanism ambiguous — `claim_task.py` has an explicit,
   documented direct-to-`main` exception to hard rule 1 for its one atomic claim
   commit, `close_task.py`'s own docstring is explicit that hard rule 1 does **not**
   carve out a second exception for close-out-shaped bookkeeping, but nothing said
   which side of that line the `review` transition falls on. Prior git history
   (`4dac352`, `ec5086a`) was genuinely ambiguous either way. model-builder/t-029
   cycle 21 (2026-08-20) treated it as needing its own branch+PR per a strict reading
   of hard rule 1 and hit a real STATUS.md-refresh merge conflict doing so by hand
   with `set_task_field.py` + a manually-managed branch — but that conflict was a
   symptom of not using `close_task.py`'s fetch-fresh plumbing for the transition,
   not of branch+PR being the wrong shape. `close_task.py`'s own git plumbing commits
   directly against whatever `origin/main`/`origin/<branch>` looks like *at push
   time*, the same way `claim_task.py`'s does — so routing `review` through it avoids
   that conflict class without needing a new direct-to-`main` exception.) Confirm
   `claimed_by`/`owner` still identify your session and its actual branch name — it
   does not need to start with `worker/` — so a later Reviewer sweep can find the
   in-progress work by reading roadmap state, instead of having to hand-check the
   open-PR list on GitHub. Skipping this step is exactly what caused
   `superkate-hairstyle-ai/t-017` to sit at `status: claimed` after PR #317 had
   already merged (twice — see `TALKBACK.md` 2026-07-10 and 2026-07-16, and
   `superkate-hairstyle-ai/t-020`); a task left at `status: claimed` past a session's
   lifetime looks abandoned rather than in-review, and its claim can silently expire
   under `CLAIM_TTL_MINUTES` while the PR is still open. If your session merges its
   own PR in the same run (see "Reviewer (Claude) — CAN merge ... from `claude/*`
   branches" below), it's fine for `status: review` to be short-lived — set it before
   `gh pr create` and flip to `status: done` right after the merge via another
   `scripts/close_task.py` call (own branch + its own small PR, never a direct push
   to `main` — see the "software" close-out step below; several close-outs from the
   same PR/session can share one `close_task.py` branch, so the `review` and `done`
   transitions for the same task may land as one PR when both happen in the same
   run) — the point is that roadmap state never silently jumps from `claimed` to
   `done` with no externally-visible checkpoint in between.

### Rotation collisions

Picking a task does not reserve it — always claim with `claim_task.py` (step 6), which fails
fast into `ALREADY_CLAIMED` on a race; claims self-expire after 90 minutes. Full history and the
same-session post-compaction variant: `docs/agents/roles/worker.md`.

### Review-claim markers — avoiding duplicate review work

Before reviewing/merging a PR, follow the review-claim marker protocol in `docs/agents/roles/reviewer.md`.

### Task dependencies (pipelines)
A task may declare `depends_on: <task-id>` (or a list). A task is only workable when every
dependency is `status: done` AND, if the dependency is human-gated, `approved_by_human: true`.
Tasks waiting on an unmet dependency carry `status: waiting` — never claim a `waiting` task.
When Silas approves an upstream task, the next Worker run calls `scripts/resolve_deps.py`,
which flips any now-satisfied `waiting` tasks to `ready`. So the Worker's FIRST action each
cycle is to run the resolver, THEN pick a ready task.

### Umbrella sweep tasks — `remaining_scope_task`

A recurring umbrella task (e.g. a layout-contract sweep tracking several buckets toward
zero) can reach a state where every bucket is at zero except one already owned by a
dedicated follow-on task. At that point the umbrella has no independent slice left, and
claiming it directly only duplicates or collides with the follow-on. Set
`remaining_scope_task: <task-id>` on the umbrella pointing at that sibling task (same
roadmap): `run_worker.py`'s `find_ready_task`, `next_ready_task.py`'s `first_ready_task`,
and `claim_task.py` all treat the umbrella as not-yet-claimable for as long as the
referenced task exists and hasn't reached `status: done`. No field set — current behavior,
unaffected. (Filed from conductor issue #1627, interface-vision/t-017 vs. t-058.)

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

**Lifecycle clarification (Silas, 2026-08-07):** `continuous` now owns never-idle
behavior. The historical autonomous rules below apply only when the project's override
status is `continuous`. `autonomous: true` on a finite `active` roadmap may grant broad
initiative while real ready tasks exist, but it may not invent endless polish/content work
after the finite queue empties. AI Art Academy's test-run never-idle loop is explicitly
ended; Animation Manager and Dream Cycle are the initial continuous programs.

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

### A gate must say why it needs a human, or agents take it back

Silas, 2026-09-30: *"can we get some sort of oversight so that we aren't allowing things to hang
when its not really a human gate issue?"* The triage that prompted this found 15 of 51 open gates
were agent work. Examples: a dependency wait filed as a gate. A decision already answered by one of
Silas's standing directives. A "needs a Force Update" block on a fix that had been live for nine
days. A "needs DATABASE_URL" block that an admin endpoint plus a workflow would have removed.

- **`gate_reason:`** names why a human is needed. It is one of `money`, `publish`, `legal`,
  `irreversible`, `secrets`, `security`, `physical-access`, `subjective-acceptance`, or
  `creative-approval`. Set it whenever you park a task at `needs-human`. If none fits, it is
  probably not a human gate.
- **`python scripts/check_gate_legitimacy.py [--live]`** flags gates agents should take back:
  - NO_GATE_BASIS: a hard gate with no hard-gate marker.
  - APPROVED_PARKED: an approved decision nobody executed.
  - SHOULD_BE_WAITING: an unmet `depends_on`. Use `status: waiting` instead.
  - DEPLOY_PREREQ_MET: waiting on a deploy that has already shipped.
  - UNREVIEWED: not re-triaged in 7 days (soft), 14 days (hard), or 30 days (with a human-only
    `gate_reason`).
- **`select_role.py` returns `gate-triage`** while any finding exists. It ranks above `worker`.
  Clear each finding in one of three ways: execute it, reclassify it (`ready`/`waiting`, or a
  new ready task for the engineering it hides), or re-check it for real and stamp
  `gate_rechecked: YYYY-MM-DD` with a one-line reason in the note. A stamp without a real
  re-check is the failure this exists to stop.
- Before parking on access ("needs DB/shell/Alexandria"), ask whether an admin HTTPS endpoint
  plus a conductor workflow using `KR_API_TOKEN` would remove the need. That is how
  art-archive/t-040 turned a shell-only import into a button. Building that path is agent work.
- Before parking on a decision, check CONTROL.md, `notes_from_silas`, and standing directives.
  If Silas has already answered, apply the answer.
- **Default-recommendation rule (Silas, 2026-09-30, standing).** A reversible product decision
  gate can be parked only with a written recommendation. If Silas has not answered within 7 days,
  the next `gate-triage` session adopts the recommendation. It records "ADOPTED under the
  2026-09-30 default-recommendation rule" in the note, sets the task back to `ready`, and builds
  it. Silas can still reverse the decision later. This never applies to a gate whose
  `gate_reason` is money, publish, legal, security, irreversible, secrets, or physical-access.
  Leave `approved_by_human` unset when adopting. Only Silas's own answer sets it.

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
  — get the id from `python scripts/next_free_task_id.py <project>` (checks `origin/main`
  fresh) rather than hand-picking one, to avoid colliding with an id another session just
  assigned (see "Rotation collisions")

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

To verify kind_robots changes locally (vue-tsc / eslint) in an ephemeral sandbox, run
`source scripts/provision_kind_robots_deps.sh` — it installs node_modules + the Prisma
client with the two required workarounds (CYPRESS_INSTALL_BINARY=0 and a dummy
DATABASE_URL) baked in, instead of every session re-deriving them (conductor/t-046).

**Check for a stranded implementation branch before reimplementing a `ready` task.** A
`create_pull_request` connector failure can leave a target-repo branch fully implemented
and pushed with no PR ever opened, while the conductor task sits at `status: ready`
describing the blocker in its own `note:` (kind-robots/t-120's kaizen id-collision rescue
and t-122 both hit this within two days, 2026-09-24/26). Before claiming and reimplementing
such a task, check the task's `note:` for a referenced branch/commit, or list the target
repo's branches for a `worker/<project>-<task-id>-*` match. If one exists and its diff looks
complete against the task description, open the PR from it as-is rather than reimplementing
— but do not treat the stranded branch's own prior local verification as sufficient to merge.
Run full CI on it first: t-122's branch passed its author's one purpose-built verifier
locally, but a full CI run caught a real regression in a *different* file that pinned the
same string the change had renamed, which the original author's narrower local check never
touched. A stranded branch is safe to reuse; skipping CI on it is not.

Several scripts here (`fetch_todos.py`, admin-gated kind_robots API calls, etc.) need
`KR_API_TOKEN` in the environment. To check whether it's set **without ever printing the
value itself**, run `scripts/kr_token_set.sh` (or `source` it) rather than hand-typing a
probe: `${VAR:-no}` looks like a safe fallback but actually substitutes the live value
once the variable is set, so a hand-rolled check can leak the token straight into a
session's own tool-output transcript (root `TALKBACK.md`, 2026-08-12 and 2026-08-13, two
independent sessions hit exactly this — conductor/t-116; a **third** independent
recurrence, 2026-08-24, is logged in root `TALKBACK.md` and conductor/t-128 — that session
had just finished reading this exact warning and reproduced it anyway seconds later in an
unrelated ad hoc diagnostic one-liner, so treat "I already know the rule" as insufficient:
literally never type `${SOME_SECRET_VAR:-...}` by hand for any secret-shaped variable, not
just `KR_API_TOKEN`, not even in a quick debugging aside — always route through `-n`/`-z`
or a script like this one). Relatedly: in this sandbox, shell environment variables do
**not** persist between separate Bash tool invocations (each call starts a fresh shell
from profile) — `source scripts/kr_token_set.sh` in one call has no effect on a later
call's environment, so check presence in the *same* invocation that uses the token, not a
prior one.

**Secrets are guarded by hooks now, because remembering the rule has failed five times.**
(2026-09-27, after a Python `print(getattr(module, "KR_API_TOKEN", "NOATTR"))` diagnostic
printed the live token — a shape no shell rule could cover. Silas: *"The risks of training
data leaking my personal hobby project's admin key is not worth excessive hassle."*) Two
PreToolUse hooks in `.claude/settings.json`, mirrored to `~/.claude/` by
`scripts/install_secret_hooks.py` so sessions rooted outside this repo get them too:
- `.claude/hooks/block_secret_dump.py` refuses the command shapes that have leaked before,
  and Read/Grep of a live `.env`.
- `.claude/hooks/redact_bash_output.py` wraps every Bash command so its stdout and stderr
  pass through a filter that replaces the literal value of every secret-shaped env var
  (and every secret-shaped line in the project's dotenv files) with `[REDACTED:NAME]`.
  This is the layer that does not depend on anyone predicting the next shape.

What that means for you:
- **Never inspect a secret's value, in any language, for any reason** — not to print it,
  not a prefix, not its length next to its value, not a hash, not "just to confirm it
  resolved". Presence only: shell `[ -n "$X" ]` or `scripts/kr_token_set.sh`; Python
  `bool(os.environ.get("X"))` or `hasattr(module, "X")`. To learn whether a token *works*,
  make the authenticated call and report only the HTTP status.
- **Never set `CONDUCTOR_REDACT_OUTPUT=0`** or otherwise route around either hook. The kill
  switch exists for Silas debugging the hook itself, not for agents.
- **If `[REDACTED:<NAME>]` shows up in your output, the redactor caught a leak.** Stop that
  line of investigation and do not try to reveal what was masked. Log a root-TALKBACK
  `security-flag` entry naming the command shape and stating that the value did **not**
  reach the transcript — so **no rotation is needed**. Say that explicitly; an entry that
  leaves it ambiguous costs Silas a rotation for nothing.
- **If a value genuinely reached the transcript anyway** (the hooks weren't loaded, or a
  non-Bash tool printed it), append to the ONE open `FOR SILAS: rotate KR_API_TOKEN`
  conductor task instead of filing another, link kind_robots
  `docs/runbooks/admin-token-rotation.md`, and fix the hook so that shape is masked next
  time — that fix is the deliverable, a TALKBACK apology is not.

**Visually verifying a front-end change** (kind_robots is self-hosted at `kindrobots.org`, not
Vercel; no PR previews, no auto-deploy-on-merge; a UI change does not merge on structural CI
alone): read [`docs/agents/frontend-verification.md`](docs/agents/frontend-verification.md)
before verifying or merging any kind_robots UI change.

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

### Sandbox `pytest` is missing PyYAML

The session sandbox's isolated `pytest` tool (installed via `uv tool install pytest`) does
not carry PyYAML, so plain `pytest` fails to even *collect* any test that imports `yaml` —
`ModuleNotFoundError: No module named 'yaml'` — even though the system `python3` interpreter
the repo's own scripts (`consume_animation_pitches.py`, `check_animation_novelty.py`,
`claim_task.py`, etc.) run under has PyYAML installed fine. This is distinct from `python3 -m
pytest` failing with "no module named pytest" (a different, unrelated absence). If you hit
`ModuleNotFoundError: yaml` under a bare `pytest` invocation, don't re-derive the cause —
reinstall the tool with the extra baked in:

```
uv tool install pytest --with pyyaml --force
```

### Finish on clean main — no leftover branches

**Silas, 2026-07-31 (standing):** *"You should open prs automatically, merge when green, we
prefer a tight ship with a single main branch once work is done, and I test on main."* Open the
PR as soon as the work is pushed — never end a session having only pushed a branch, and never
pause to ask permission to open one. If your harness carries a default "do not open a PR unless
asked," this line is the ask, standing for every session. The real gates are unchanged: human-gated,
outward-facing, irreversible, and security-sensitive work still ends at `needs-human` with its PR
open but unmerged.

The goal of every run is an updated `main` with the run's safe work merged and **no branch
left behind**. This is not conditional on a human saying "merge" — for reversible, scoped,
verified, non-human-gated work, merging is the default terminal state (see the Worker/Reviewer
steps and the CAN/CANNOT lists above; the real gates — human-gated, outward-facing,
irreversible, security-sensitive — are unchanged and still stop at `needs-human`).

Branch hygiene:
- A merged PR's branch is deleted automatically (the repo's "delete head branch on merge"
  setting). Never open a fresh PR from, or re-push, a branch whose work already merged.
- Branches with no open PR are cleaned by the `branch-janitor` workflow
  (`.github/workflows/branch-janitor.yml` → `scripts/branch_janitor.py`): it deletes any
  `claude/*`/`worker/*` branch fully merged into `main`, and *reports* (never auto-deletes)
  unmerged stale branches so a session can rescue-or-delete them with judgment. To clear a
  branch you have verified is superseded, run that workflow via `workflow_dispatch` with
  `force_delete_branches` — session credentials 403 on ref deletion, so the workflow (with its
  Actions token) is the path, not `git push --delete`.

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
  — get the id from `python scripts/next_free_task_id.py <project>` (checks `origin/main`
  fresh) rather than hand-picking one, to avoid colliding with an id another session just
  assigned (see "Rotation collisions")
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
- Delete TALKBACK entries (the log is append-only) — see the archival carve-out below
- Skip a `needs-human` gate on an `outward-facing` or `irreversible` task
- Hold more than one claimed task at once (claims are sequential — finish, hand off, or cleanly park one before claiming the next)

### Archival carve-out to the append-only rules

Authorized by Silas on 2026-09-14, in session, for conductor/t-158.

The append-only rules above and hard safety rule 7 exist to stop **history loss**. Moving a record
to a named archive file, unchanged, does not lose it. So:

> **Moving content verbatim into a named archive file is not deletion**, provided (a) the move is
> byte-for-byte — the archived text is recoverable *identical* to the original, (b) the script
> performing it verifies that round-trip before it rewrites the source, (c) a pointer is left at the
> original location, and (d) the PR names the session and the human authorization for the sweep.

**Rewriting, summarizing, paraphrasing, truncating, or dropping an entry remains forbidden**, in an
archive file exactly as in the original. "I condensed it into the archive" is the prohibited thing,
not a lighter version of it. If you cannot verify the round-trip, you may not do the move.

This is what separates a deliberate archival pass from the incidents these rules were written for:
conductor/t-129 (a `--set note=` close-out silently dropped 199 lines of diagnostic history across
cthulhuquarium/t-033 and t-034, repaired in #2816) and the 11,014-line `art-prompts.yaml` deletion
that `check_large_deletion_guard.py` was written after. Both destroyed content. An archival pass
relocates it and proves it did.

Practical notes: `scripts/set_task_field.py`'s `set_task_field_text(..., force=True)` bypasses the
t-129 destructive-replace guard and is the sanctioned path **only inside a verified archival
script** — never for an ordinary close-out, which uses `--append-note`.
`check_large_deletion_guard.py` will flag the resulting diff; that is the guard working as designed
(its own docstring blesses "a deliberate large prune"), and the PR body should say so rather than
work around it.

## Role assignment — decided on arrival, not by which trigger fired

Historically "Worker" and "Reviewer" were treated as properties of *which platform
trigger* fired a session (an hourly Worker trigger, a separately-scheduled Reviewer
trigger). That caused a real, repeatedly-observed bug (conductor/t-026, 48+
recurrences): the Reviewer trigger fired far more often than Worker PR volume
justified, so sessions kept arriving with nothing to review and no fallback other
than a no-op report. The platform-level trigger *schedule* is still outside this
repo's control — but the SESSION's behavior no longer has to depend on it.

**Every session, regardless of what a trigger happened to name it, decides its own
role from live state on arrival:**

1. Run `python scripts/select_role.py` (composes seven existing, no-model-call state
   checks into one recommendation, in priority order). It returns one of:
   - **`role: reviewer`** — at least one `worker/*` branch is open and not yet merged
     into `main`. Reviewing an existing PR is higher-leverage than starting new work,
     so this wins even if anything else below also applies.
   - **`role: workflow-medic`** — no branch to review, but a watched scheduled
     workflow (default: `process-task-events.yml`, the task-events cron processor) has
     `--workflow-fail-threshold` (default 3) or more consecutive completed runs that
     didn't succeed. A scheduled workflow's failure otherwise only shows up in the
     Actions tab — nothing else pings a session (conductor/t-102: the 2026-08-05
     ai-art-academy/t-010 stuck-`rearm` incident sat failing on every run for hours
     before a manual sweep noticed). See `docs/agents/roles/workflow-medic.md`.
   - **`role: pr-medic`** — no branch to review, but an open PR (`run_reviewer.py`'s
     scope) has red CI that's gone stale (no push in `--pr-stale-hours`, default 3h)
     — a real error nobody is actively iterating on, not a PR mid-fix. See `docs/agents/roles/pr-medic.md`.
   - **`role: art-medic`** — `ops/art-queue-health.yaml` (written by every Auto Art
     Generate run) lists art queue failures an agent can fix: prompt-contract
     rejections, adoptions that 404, FAILED Kind Robots ArtJobs with no known repair,
     or a timeout/error persisting 2+ days. That workflow is green even when nothing
     renders (2026-10-07: 0/28 behind a green check), so this file is the signal.
     Fix the rows and the producer that wrote them. See `docs/agents/roles/art-medic.md`.
   - **`role: branch-medic`** — nothing to review or fix, but `branch_janitor.py`'s
     STRANDED tier is non-empty: a `claude/*`/`worker/*` branch with unique unmerged
     commits, old enough (`--branch-stale-hours`, default 12h) that nobody's actively
     pushing to it. `branch_janitor.py` itself deliberately never auto-acts on this
     tier — see `docs/agents/roles/branch-medic.md`.
   - **`role: daily-creative`** — a ready recurring task explicitly marked
     `daily_commitment: true` has not yet been checked on today's Pacific calendar date.
     This lane exists for human-designated daily creative output, initially
     `animation-manager/t-007`. It outranks weekly audit and ordinary ready-task pickup so a
     busy finite backlog cannot starve the daily creation goal, but reviewer, workflow-medic,
     pr-medic, and branch-medic still come first. Claim the specific task named in
     `due_daily_commitments`, follow normal Worker/PR rules, and re-arm it when finished.
   - **`role: site-auditor`** — nothing to review/fix/triage, but the weekly site
     audit (`projects/global-ui/SITE-AUDIT-AGENT.md`) is overdue: no
     `AUDIT-REPORT-<date>.md` exists yet, or the newest one is `--audit-stale-days`
     (default 7) old or older. This is time-boxed rather than purely reactive — it
     outranks fresh `worker` pickup once overdue, so it actually happens close to
     weekly instead of "whenever the queue happens to run dry." See `docs/agents/roles/site-auditor.md`.
   - **`role: gate-triage`** — `check_gate_legitimacy.py` found `needs-human` gates that are
     really agent work (see "A gate must say why it needs a human"). Clear every finding, then
     re-run. Outranks `worker` because each finding either releases work or takes an item off
     Silas's list. Playbook: `docs/agents/roles/gate-triage.md`.
   - **`role: worker`** — none of the above, but a `ready` task exists.
   - **`role: stale-recurring`** — no ordinary `ready` task and no due daily
     commitment won the cycle, but a `recurring: true` task (most often a
     `continuous`-lifecycle project's, e.g. animation-manager/t-006) has gone
     `--recurring-stale-days` (default 3) or more
     with no `RAN <date>`/`NO-OP <date>` note marker or `updated:` bump — the exact
     "sat `status: ready` unrun for two weeks with nothing flagging it" gap
     conductor/t-118 documents. Lowest-priority soft signal: it never preempts a
     genuine `worker` pickup, only fires when nothing else claims the cycle. Treat it
     as an ordinary `ready` task once you land on it (claim it, do the recurring
     work, re-arm per that task's own convention). `stale_recurring_tasks` is also
     reported in the JSON output even when a different role wins, so don't wait for
     this role to actually surface a staleness signal you notice while reading the
     output for another role.
   - **`role: idle`** — none of the above. **Idle is never a stopping point.** Walk
     "Never idle: the fallback ladder" below (also emitted as `idle_ladder` in the
     JSON) and ship at least one unit of work before the session ends.
2. Follow the matching playbook (table below). A session isn't locked to one role for its
   whole run: if you finish reviewing everything open, re-run `select_role.py` — it
   may now recommend `workflow-medic`, `pr-medic`, `art-medic`, `branch-medic`, `site-auditor`,
   `worker`, or `stale-recurring` — and keep going in the same session rather than
   stopping. This is what "agents disperse and work as needed" means in practice: the
   role is a live recommendation you re-check, not a label stamped on you before you
   started.
3. If a human explicitly asked for one role in this session (e.g. "review PR #123"),
   honor that directly — `select_role.py` is for the *unprompted, trigger-fired* case,
   not a override of an explicit instruction.
4. **Scope note:** `select_role.py`'s `pr-medic`/`branch-medic` signals cover BOTH
   `silasfelinus/conductor` and `silasfelinus/kind_robots` by default (`--repos` to
   change) — "a conductor agent does this" doesn't mean it only watches its own
   repo. Conductor's own checks use fast local git (via `branch_janitor.py`, no API
   calls); kind_robots has no guaranteed local checkout in every session/job that
   runs this script, so it's checked via the GitHub API instead (same information,
   different transport — see the script's own docstring). `workflow-medic`'s check
   is conductor-only (`--watched-workflows`, comma-separated filenames) since the
   scheduled workflows it currently watches are conductor-repo concepts (roadmap/
   task-events processing) — extend `--watched-workflows` if a kind_robots cron job
   ever needs the same coverage. If a session has access to still other repos beyond
   these two, check those via the session's own GitHub MCP tools (`list_pull_requests`
   + `pull_request_read`'s `get_check_runs`/`get_status` method; `list_branches`;
   `actions_list`'s `list_workflow_runs` method) before concluding there's nothing to
   fix/triage — `select_role.py`'s default scope isn't the ceiling, just the floor.

This doesn't require the platform to merge its Worker/Reviewer triggers into one —
it just means a session mislabeled by a stale trigger schedule self-corrects instead
of silently no-op'ing. Consolidating the trigger schedule itself is a platform
setting change outside this repo (see conductor/t-026's roadmap history) if Silas
wants to pursue it further; this section is the repo-side half of the fix and does
not depend on that happening.

### Never idle: the fallback ladder

Silas, 2026-09-29, verbatim: *"this sounds like there is nothing to do, and there ALWAYS
should be. ... we need a fallback idle. If there truly are no open tasks on roadmaps, no
dream digests to create, no art to generate, no work to be done polishing errors, merging
prs, creating new pitches for concepts, bug checking, then we should be creating new
objects, running with old pitches and making new material, we can create new object
pitches."*

A trigger-fired session that ends with only a sweep report and no shipped work is a
**failed run**, not a quiet one. The 2026-09-29 run that prompted this reported "nothing to
do" while a green PR sat unreviewed, animation-manager's daily commitment was due,
tzaddik-gallery/t-016 was ready, and two interface-vision recurring tasks were 8 days
stale. So:

- **Run `select_role.py` and act on it** — the startup sweep is the preamble, not the job.
  Re-run it after each unit of work and keep going while the session has budget.
- **A predicted no-op is not a skip.** If the top pickup looks like it would close as a
  no-op (e.g. a recurring polish task whose last cycle was a verified no-op), move to the
  next ready task or the next rung below; never end the session on that judgment alone.
- **Gated projects are not empty projects.** A project whose top tasks sit at
  `needs-human` usually still has reversible work around the gate — prep, tests, docs, art,
  a draft the gate will need. Look before walking past it.

When `select_role.py` returns `idle` (or every recommendation above is exhausted), walk this
ladder top-down and take the **first rung that yields a real unit of work**. Every rung uses
normal flow: create (or reuse) a roadmap task in the owning project, claim it, PR, merge when
green. Default home for work with no natural project is dream-cycle (`autonomous: true`,
`status: continuous`). Human gates are unchanged: publishing, spend, deploys, outreach, and
irreversible actions still stop at `needs-human`.

1. **Continuous programs** — any `ready` task in a `status: continuous` project
   (animation-manager, dream-cycle, interface-vision, …) in priority order, recurring ones
   included.
2. **Dream docket** — author one proposal if `build_dream_proposal.py --check` is below the
   buffer; if it is full, improve the weakest queued proposal instead.
3. **Art** — drain an art/media queue, or generate missing/weak art for existing records
   (generated art is pre-approved; keep prompt/model metadata).
4. **Polish errors** — turn a standing sweep finding into a fix: a noisy container-log
   signature, CARD COPY Facet prompts from `check_facet_prompt_subjects.py`, a check that
   keeps timing out (`check_live_facet_coverage.py`), a flaky test.
5. **Bug hunt** — audit one active project's live front end or API for real bugs and
   phone/tablet/desktop breakage; file and fix what you find.
6. **Run with old pitches** — take an `approved` pitch in `pitches/` (or a
   `projects/*/pitches/` entry, or a `projects/dream-cycle/backlog/` outline) whose work never
   reached a roadmap, and build its first real slice.
7. **Create new objects** — make new Kind Robots material from existing seeds: characters,
   rewards, scenarios, bots, art collections, coloring pages, screensavers.
8. **Pitch new objects** — write one new concept/object pitch in `pitches/` using the pitch
   template, after deduping against every existing pitch, project, and shipped feature.
   If today's `pitches/daily/<date>.yaml` docket is missing, author that first (five pitches; see
   `scripts/daily_pitches.py --brief`): it feeds the digest every day (dream-cycle/t-035 is the daily
   commitment). Sessions author pitches; Silas decides them from the digest email.

Rung 8 always has work, so a session that reaches the bottom of the ladder still ships.
Record which rung you took (and why the rungs above it were empty) in the task note so the
next session and the digest can see the ladder working.

### Role playbooks — read only the one you were assigned

The per-role step lists live in `docs/agents/roles/` so a session loads only its own.
`select_role.py` names the file in its `playbook` field. Re-read the new playbook whenever
you re-run `select_role.py` and the role changes.

| Role | Playbook |
| --- | --- |
| Worker (`role: worker`, `stale-recurring`, `daily-creative`) | [`docs/agents/roles/worker.md`](docs/agents/roles/worker.md) |
| Reviewer (`role: reviewer`, `reviewer-uncertain`) | [`docs/agents/roles/reviewer.md`](docs/agents/roles/reviewer.md) |
| `role: workflow-medic` | [`docs/agents/roles/workflow-medic.md`](docs/agents/roles/workflow-medic.md) |
| `role: pr-medic` | [`docs/agents/roles/pr-medic.md`](docs/agents/roles/pr-medic.md) |
| `role: art-medic` | [`docs/agents/roles/art-medic.md`](docs/agents/roles/art-medic.md) |
| `role: branch-medic` | [`docs/agents/roles/branch-medic.md`](docs/agents/roles/branch-medic.md) |
| `role: site-auditor` | [`docs/agents/roles/site-auditor.md`](docs/agents/roles/site-auditor.md) |
| `idle` | "Never idle: the fallback ladder" above (no separate file) |

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
- `retry_context` can go stale when a human merges the referenced PR directly,
  bypassing the reject-retry loop (Silas can and does override a Reviewer rejection).
  Before acting on a `retry_context` for a cross-repo task, check whether the PR it
  references already merged — or whether the task's `passes`/`status` otherwise looks
  inconsistent with an open PR — and re-verify against current target-repo `main`
  first, rather than assuming the recorded rejection still holds. See
  ruler-hooked/t-012 (conductor/t-074) for the case that prompted this: a
  `retry_context` sat stale for 5 days describing a rejection Silas had already
  overridden by merging directly.

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
7. TALKBACK files are append-only: never edit or delete a prior entry from either agent. The one
   exception is the archival carve-out under "Neither agent — EVER": a verified byte-for-byte move
   into a named archive file, leaving a pointer behind. Summarizing or trimming is still forbidden.
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
11. Never delegate a git-state-mutating workaround (`push_files`, `create_branch`,
    force-push, etc.) to a background subagent for a problem you are actively fixing
    inline in the foreground — its eventual push can silently overwrite commits you make
    after dispatching it, since it only knows the file content it was handed at dispatch
    time. See CLAUDE.md's "Don't delegate an in-flight git workaround to a background
    subagent" (conductor/t-066).
12. `isolation: 'worktree'` is REQUIRED, not optional, for any background Agent that will
    run git-mutating commands (`claim_task.py`, `set_task_field.py`, `close_task.py`, plain
    `git commit`/`push`, `push_files`, `create_branch`, force-push, etc.) in a repo a
    foreground session is still actively — even passively, mid-edit — using. This
    generalizes rule 11 beyond the narrower in-flight-workaround case: a non-isolated
    background Agent's git operations in a shared working directory can silently discard
    the foreground session's uncommitted edits (TALKBACK.md 2026-08-13) or delete its
    designated git branch outright, including any unpushed commits on it (TALKBACK.md
    2026-08-14, conductor/t-117). If the background task doesn't need to mutate git state
    in this repo, `isolation: 'worktree'` is unnecessary — the rule applies specifically
    when it does.
13. A delegated background agent's "waiting for CI, I'll re-check when my timer fires"
    self-report is not a live block — confirmed at least four independent times
    (`projects/model-builder/TALKBACK.md` 2026-08-21 cycle 30, 2026-08-22 cycle 41, and
    2026-08-22 cycle 42; root `TALKBACK.md` 2026-08-22 ai-art-academy/t-076) across
    different projects and sessions, including once with an explicit "poll directly,
    don't sleep-then-stop" instruction in the dispatch prompt. The agent still ends its
    turn and produces a `task-notification` instead of actually blocking until CI
    resolves. Never treat that self-report as equivalent to "still running and will
    merge on its own" — the delegating/coordinating session must poll the PR's CI status
    itself (`pull_request_read` with `get_check_runs`/`get_status`, or the GitHub MCP
    equivalent) and merge when green, then explicitly tell the sub-agent to stop (via
    `SendMessage` to the same agent, never a fresh `Agent` call — see rule 11's sibling
    guidance) to avoid both sides racing to merge or re-push the same PR.

14. SECRETS AND CREDENTIALS ON THE UNRAID HOST LIVE IN `<checkout>/.secrets/` — in
    practice `/mnt/user/appdata/kind_robots/.secrets/` — and **never** on
    `/mnt/user/pc`. Silas, 2026-08-25: *"We should only be using that directory, and
    never ever using pc as a root unless very explicitly told otherwise (but likely
    never)."* `/mnt/user/pc` is a general-access share and a primary thoroughfare for
    ordinary folders, which makes it exactly the wrong home for a mode-600 file. Do not
    write there, read credentials from there, or point `SECRETS_DIR` at a path under it,
    and do not treat it as a root for config or application state.
    This is not hypothetical bookkeeping. The agent DB lane was moved off
    `/mnt/user/pc/kindrobots-db-agent/` on 2026-08-21 for exactly this reason; the
    migrate lane's handoff file was supposed to move with it and did not survive, and its
    absence broke a production migration on 2026-08-25 — **silently**, because
    `. ./.secrets/<file>` prints one line and carries on when the file is missing, so the
    credential fell through from `.env` with its quotes attached and failed four steps
    later as what looked like a TLS error.
    NOT A BAN ON THE SHARE ITSELF: `/mnt/user/pc` remains the correct, established home
    for bulk non-secret data — `kindrobots/images`, `kindrobots/animate`, and the model
    store at `ai/models`. The rule is about credentials and config roots, not storage.
    Enforced by `utils/scripts/verifyMigrationCredentialBoundary.mjs` in kind_robots,
    which fails if either provisioner stops defaulting to `<repo>/.secrets` or names a
    `/mnt/user/pc` path outside a comment. Numbered 14 rather than inserted mid-list on
    purpose — a dozen TALKBACK entries reference "hard rule 12" meaning worktree
    isolation, and renumbering would silently invalidate all of them.

15. ANY COMMAND YOU HAND A HUMAN TO RUN MUST BE INCAPABLE OF PRINTING A SECRET.
    The existing `KR_API_TOKEN` guidance above covers probes an agent runs in its own
    shell. It does not cover the far easier mistake: writing a command for the operator,
    who runs it and pastes the output back into the transcript. Their paste is not the
    leak — **your command is**. Silas, 2026-08-25: *"If I copied my password, that's on
    me. If you ask me to send you back a response and the password is included but could
    have been obfuscated, that's on you."*
    This happened twice in one session, both times from commands an agent wrote:
    `grep -n '^MIGRATION_DATABASE_URL=' .env` printed a live production password in
    plaintext, and `SHOW GRANTS FOR 'kindrobot'@'%'` printed the account's
    `IDENTIFIED BY PASSWORD '<hash>'`. The same session had already written the redacted
    form of the first command one message later, and had cited conductor/t-116 and t-128
    — the three prior secret-in-transcript incidents — in its own commit messages while
    authoring the unredacted one. Knowing the rule is demonstrably not enough; the
    command has to be built so the mistake is impossible.
    WRITE IT REDACTED THE FIRST TIME, not the second:
    - Presence, not value: `grep -c '^KEY=' file`, `[ -n "$VAR" ]`, or a `case` that
      matches a prefix and echoes only OK/STOP. Never `echo "$VAR"`, never a bare `grep`
      of a line that has a credential on it.
    - Reading a config line: append `| sed 's/=.*/=<redacted>/'`.
    - `SHOW GRANTS`: append `| sed "s/ IDENTIFIED BY PASSWORD '[^']*'//"` — the grant
      shape is the answer; the hash is not, and for `mysql_native_password` the hash is
      itself sufficient to authenticate.
    - Anything writing a secret to a file the operator may later paste (backups,
      snapshots, `.env.bak`): say so at the time, and say when to shred it.
    If a value genuinely must be inspected, tell them to look at it themselves and
    explicitly tell them NOT to paste it back. Assume every command you write will have
    its full output pasted into the transcript, because that is the normal and helpful
    thing for someone to do.

**Reviewer batch-merge note (companion to rule 9):** `refresh-status.yml` lands a
`chore: refresh STATUS.md and workspace.html` commit on `main` within seconds of every
merge. When clearing several backlogged PRs in one sweep, expect each merge after the
first to race that auto-commit: a PR that was clean moments ago flips to
`mergeable_state: dirty` through no fault of the Worker (the staleness comes from the
Reviewer's own previous merge — Worker-side rebase-before-PR cannot prevent it). Do not
treat the first `dirty` as a real conflict: re-fetch `main` (update the PR branch) and
retry. If a genuine conflict remains, resolve it like any auto-gen conflict — take
main's copy of `STATUS.md` / `workspace.html` / `ROADMAP-AUDIT.*` / `LEARNING-REPORT.md`
and regenerate; for append-only files both sides touched (`TALKBACK.md`, `LEARNING.yaml`),
keep both sides' entries rather than picking one. (Kaizen from the 2026-07-16 8-PR
Reviewer sweep, conductor/t-056.)

## Don't hand work back that you can do yourself

Migrated from Silas's per-origin prompts (2026-07-31) so every agent gets it, not just the
one whose prompt happened to carry it.

Do not ask Silas to switch branches, merge work that is already green, or verify something
that code, tests, CI, logs, or a Vercel preview can verify. Do not assign routine cleanup
back to him. Do not open with speculative access disclaimers ("I may not be able to reach
X") — attempt the thing, then report what actually happened. Claim a tooling limitation only
after a specific operation has failed and you have tried the alternatives.

Stop only at a real human gate: secrets, billing, DNS, account creation, destructive or
irreversible production changes, physical access, anything outward-facing or published, and
explicitly requested subjective approval. Those still end at `needs-human` with the PR open.

Everything short of that is yours to finish.

## Companion PRs across repos

When a change spans `conductor` and a target repo (usually `kind_robots`), the two PRs are
one unit of work:

- Work out the dependency direction first, and merge in that order — if the conductor doc
  references a file the kind_robots PR creates, kind_robots merges first.
- Merge **both** when green. Half-landed companion work is worse than neither half: it
  leaves a reference pointing at something that does not exist yet.
- Clean up both sides — stale branches, claims, and superseded PRs — in the same session.
- If only one side can land (the other is gated or blocked), say so explicitly in the merged
  side's PR body and in the roadmap note, so the dangling reference is discoverable rather
  than silent.

## Reporting back to Silas

Migrated from Silas's per-origin prompts (2026-07-31). Every agent report should cover:

- root cause (not just the symptom you fixed)
- what changed
- PRs opened and merged
- the tests and checks you **actually ran**, and their results
- merge and deploy status
- relevant workflow-run and ArtJob IDs
- cleanup done
- genuine human gates only — nothing speculative

Say what you verified and what you assumed; never blur the two. If something was blocked or
skipped, say so plainly with the evidence. State finished work plainly, without hedging.

"Green" means the checks completed and passed — not that a PR exists. Confirm the check runs
themselves rather than trusting a `mergeable_state` that can read `clean` while checks are
still queued. (2026-07-31: a PR was merged 65 seconds after opening with 23 checks still
running. They passed, but that was luck, not verification.)

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
