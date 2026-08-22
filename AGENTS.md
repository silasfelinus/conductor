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

**Same-session post-compaction collisions** are the identical failure mode with a
different trigger: a session's context gets compacted mid-run and loses memory of
work it already completed earlier in the same scheduled window. Resuming from stale
in-memory state, it can find its own now-outdated `status: claimed` snapshot,
correctly avoid re-implementing (an open-PR check usually catches that part), but
then still draft an inaccurate wrap-up commit (roadmap/TALKBACK note) describing a
"nothing to do" or "releasing the claim" outcome that a real merge has since made
false. Hit twice the same day (2026-07-22): model-builder/t-029 and
storymaker/t-010, both in root/project `TALKBACK.md`. The fix is the same as the
concurrent-session case, just applied to the wrap-up step too, not only the
implementation step: **before writing any wrap-up commit for a claim this session
doesn't fully remember taking, `git fetch origin main` and diff the task's current
state** — a newer merge under the same or a related session id is the signal that
the "resume" is actually stale, and the wrap-up should defer to `origin/main`'s
version (via rebase, keeping the newer content) rather than push over it.

**Concurrent PR-conflict-resolution races** are a third variant: two independent
sessions both notice the *same* open PR has gone stale against `main` (e.g. because a
third PR just merged and moved the base) and both fix it themselves, unaware of each
other. Observed 2026-07-27: PR #1195 (ai-art-academy/t-010) and PR #1197
(music-mentor/t-007 close-out) both touched `music-mentor/roadmap.yaml` and
`LEARNING.yaml`. A Reviewer session merged #1197 first, then found #1195 conflicted
and fixed it by hand (dropping #1195's now-redundant duplicate music-mentor bundle,
keeping only its actual ai-art-academy scope) — but a *second*, independent session
had, in the meantime, pushed its own conflict-resolution commit to the same PR #1195
branch that took the opposite, wrong approach: it re-merged `main` but kept #1195's
stale, less-complete version of the music-mentor content instead of deferring to
what #1197 had already landed, which would have silently downgraded/reverted the
already-merged canonical entry had it been pushed on its own. The Reviewer session's
own second push caught this the normal way — `git push` (no force) failed with a
plain non-fast-forward rejection because the remote branch had moved — which is
exactly the safety net this depends on: **never force-push to resolve a PR conflict.**
The correct recovery is the same shape as the two collisions above: `git fetch` the
branch's actual current remote tip, `git merge` it in (not overwrite it), re-resolve
favoring whichever side matches `origin/main`'s already-merged canonical content for
any file both sides touched, verify the resulting diff against `origin/main` is
exactly the intended scope (`git diff origin/main --stat` should show only files the
PR is actually supposed to touch), and push normally. If a plain push is rejected,
that rejection is doing its job — fetch-merge-reresolve, don't force past it.

### Review-claim markers — avoiding duplicate review work

`claim_task.py` prevents two sessions from both *implementing* the same roadmap
task, but there was no equivalent for *reviewing* — nothing stopped several
concurrent sessions from all picking up the same open, green PR and racing to
review/merge/close it out. This happened for real (conductor/t-092, 2026-07-28
"four-way rotation collision" — see root `TALKBACK.md` that date): this session
and at least three others independently found the same two open kind_robots PRs
and the same recurring-task close-outs within about a minute of each other,
producing three redundant conductor PRs that had to be manually triaged after
the fact. No data was lost — git's non-fast-forward rejection is still the real
backstop, same as every other rotation-collision case above — but the duplicate
work itself is worth avoiding when practical.

Before starting a review pass on an open PR (this repo or kind_robots):
1. Fetch the PR's issue/PR comments using whatever GitHub access this session
   already has (GitHub MCP tools, `gh pr view --comments`, or a direct API call
   — read-only, so any working transport is fine even in a sandbox where direct
   `api.github.com` calls 403, as `select_role.py`'s docstring documents for at
   least one sandbox shape).
2. Call `scripts/review_claim.py`'s `find_active_claim(comments)` (or reimplement
   the same check inline: look for a comment matching `REVIEWING: <session> at
   <ISO8601>` posted within the last `REVIEW_CLAIM_TTL_MINUTES` — 20 minutes by
   default). If it returns a claim from a *different* session, skip this PR —
   someone else is already reviewing it — and move on to the next reviewable item.
3. Otherwise, post a marker comment (`scripts/review_claim.py format <session-id>`
   prints the exact text to post) *before* starting the substantive review.
4. This is advisory/best-effort, not a hard lock: a missed check is wasted
   duplicate work, not a safety violation. Never skip the normal git-conflict
   safety net described above on the assumption a marker makes it unnecessary.

The module is intentionally transport-agnostic — it defines the marker format,
the freshness rule, and the pure decision logic, but never calls the GitHub API
itself, since the right transport differs per session/platform. See
`tests/test_review_claim.py` for the full behavioral contract.

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

Several scripts here (`fetch_todos.py`, admin-gated kind_robots API calls, etc.) need
`KR_API_TOKEN` in the environment. To check whether it's set **without ever printing the
value itself**, run `scripts/kr_token_set.sh` (or `source` it) rather than hand-typing a
probe: `${VAR:-no}` looks like a safe fallback but actually substitutes the live value
once the variable is set, so a hand-rolled check can leak the token straight into a
session's own tool-output transcript (root `TALKBACK.md`, 2026-08-12 and 2026-08-13, two
independent sessions hit exactly this — conductor/t-116).

**Visually verifying a front-end change: kind_robots production is self-hosted at
`kindrobots.org`, not Vercel.** As of 2026-08-12 kind_robots migrated off Vercel
entirely — Vercel Git deployments are disabled repo-wide (there is no `vercel.json` in
the repo anymore) and production is served from a self-hosted container on Unraid at
`https://kindrobots.org` (kind-robots/t-064, closed 2026-08-12; see the
`kindrobots-unraid` project). **A `*.vercel.app` URL returning `402 Payment Required` /
`DEPLOYMENT_PAUSED` / `DEPLOYMENT_DISABLED`, or `mcp__Vercel__get_project` showing
`live: false`, is the expected state of retired infrastructure — it is NOT a production
incident and does not need a new gate or notification.** (Re-confirmed 2026-08-15: every
`*.vercel.app` URL for the project 402s/503s while `kindrobots.org` itself serves fine —
200, real SSR markup, real image assets.)

This changes what verification is actually possible and when:

- **No PR preview exists anymore.** Vercel previews are gone for every branch prefix,
  not just the `agent/*`/`worker/*`/`conductor/*` ones that were already disabled for
  cost before the migration. A session cannot visually verify an *unmerged* branch's UI
  — verification pre-merge is limited to `vue-tsc`/`eslint`/unit tests/
  `test:layout-contract`.
- **No auto-deploy-on-merge either.** The Unraid container only picks up a merged commit
  when Silas runs a manual "Force Update" in the Unraid UI (see the `kindrobots-unraid`
  roadmap and `docs/runbooks/migration-credential-boundary.md`). A merged, CI-green PR
  can sit un-deployed for a while — check `https://kindrobots.org/api/health/database`,
  and whether the specific code path you changed actually answers as expected, before
  concluding a change "isn't showing up" means it's wrong (davinci/t-018 hit exactly
  this deploy-timing gap on 2026-08-08: a new endpoint returned the SPA shell, not JSON,
  until the next Force Update).
- **Post-deploy, direct HTTPS is the verification path.** Plain `curl` or `WebFetch`
  against `https://kindrobots.org/<route>` (or an asset path such as
  `/images/dashboard-tabs/art/<slug>.webp`) works directly in this sandbox — no MCP
  connector is required for this host, egress to it is unrestricted like any ordinary
  HTTPS host. This returns real SSR markup with the same caveats as before: it proves a
  route loads, isn't a 500, and contains the markup you expect from SSR; it does NOT
  prove anything that only appears after hydration, nor layout, spacing, or anything
  pixel-level. Say which of those you actually checked.
- **Real cross-width geometry**: `responsive-layout-audit.yml`'s `audit` check now runs
  on a schedule and via manual `workflow_dispatch` against production
  (`https://kindrobots.org` by default, overridable via its `base_url` input) — Vercel
  preview support was removed from the workflow along with the rest of the Vercel infra,
  so it no longer fires per-PR against a branch preview. It measures rendered geometry at
  phone/tablet/desktop widths, fails on elements that spill past the viewport or get
  crushed to a sliver, and uploads screenshots as artifacts every run. Trigger it
  manually after a merge + confirmed Force Update if you need fresh geometry/screenshots
  for a specific change; it will not run automatically per-PR the way the retired
  Vercel-preview flow did.
- **Chromium-through-the-sandbox-proxy still fails on every HTTPS host, not just
  Vercel's** (interface-vision/t-091, measured 2026-08-04): a headless-Chromium fallback
  in this sandbox gets `net::ERR_CONNECTION_RESET`/`ERR_TUNNEL_CONNECTION_FAILED`
  regardless of target host (confirmed byte-identical against `example.com`),
  independent of proxy flags (`proxy:`, `--proxy-server`, `--disable-http2`,
  `--disable-quic`, `--ignore-certificate-errors`, `ignoreHTTPSErrors` all changed
  nothing). This is a Chromium-through-the-proxy limitation, not anything about the
  target being Vercel or kindrobots.org — don't reach for a local headless-browser
  fallback in a non-interactive session; use `curl`/`WebFetch` for markup and let CI's
  `audit` check carry real pixels.

So a UI change on a `claude/*` branch is NOT merging on structural CI alone. The honest
summary of what a non-interactive session can claim: SSR markup via `curl`/`WebFetch`
against `kindrobots.org` post-deploy (itself), real cross-width geometry plus
screenshots via the `audit` check (CI, scheduled/manual against production), structural
invariants via the layout contract (CI), and nothing about aesthetics pre-deploy or
pre-Force-Update. The old Vercel MCP connector flow
(`list_teams`/`list_projects`/`list_deployments`/`web_fetch_vercel_url` against the
kind-robots Vercel project) is retired for kind_robots verification purposes — its data
now describes decommissioned infrastructure, not anything a merge or preview affects.

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
- Delete TALKBACK entries (the log is append-only)
- Skip a `needs-human` gate on an `outward-facing` or `irreversible` task
- Hold more than one claimed task at once (claims are sequential — finish, hand off, or cleanly park one before claiming the next)

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
     before a manual sweep noticed). See "If you're fixing a failing scheduled
     workflow" below.
   - **`role: pr-medic`** — no branch to review, but an open PR (`run_reviewer.py`'s
     scope) has red CI that's gone stale (no push in `--pr-stale-hours`, default 3h)
     — a real error nobody is actively iterating on, not a PR mid-fix. See "If you're
     fixing PR errors" below.
   - **`role: branch-medic`** — nothing to review or fix, but `branch_janitor.py`'s
     STRANDED tier is non-empty: a `claude/*`/`worker/*` branch with unique unmerged
     commits, old enough (`--branch-stale-hours`, default 12h) that nobody's actively
     pushing to it. `branch_janitor.py` itself deliberately never auto-acts on this
     tier — see "If you're triaging stale branches" below.
   - **`role: site-auditor`** — nothing to review/fix/triage, but the weekly site
     audit (`projects/global-ui/SITE-AUDIT-AGENT.md`) is overdue: no
     `AUDIT-REPORT-<date>.md` exists yet, or the newest one is `--audit-stale-days`
     (default 7) old or older. This is time-boxed rather than purely reactive — it
     outranks fresh `worker` pickup once overdue, so it actually happens close to
     weekly instead of "whenever the queue happens to run dry." See "If you're doing
     the weekly site audit" below.
   - **`role: worker`** — none of the above, but a `ready` task exists.
   - **`role: stale-recurring`** — no `ready` task from an active project, but a
     `recurring: true` task (most often a `continuous`-lifecycle project's, e.g.
     animation-manager/t-006) has gone `--recurring-stale-days` (default 3) or more
     with no `RAN <date>`/`NO-OP <date>` note marker or `updated:` bump — the exact
     "sat `status: ready` unrun for two weeks with nothing flagging it" gap
     conductor/t-118 documents. Lowest-priority soft signal: it never preempts a
     genuine `worker` pickup, only fires when nothing else claims the cycle. Treat it
     as an ordinary `ready` task once you land on it (claim it, do the recurring
     work, re-arm per that task's own convention). `stale_recurring_tasks` is also
     reported in the JSON output even when a different role wins, so don't wait for
     this role to actually surface a staleness signal you notice while reading the
     output for another role.
   - **`role: idle`** — none of the above. Fall through to the idle-fallback rule
     (dream-cycle's "nothing better to do" contract, or `autonomous: true` projects'
     own rule).
2. Follow the matching section below. A session isn't locked to one role for its
   whole run: if you finish reviewing everything open, re-run `select_role.py` — it
   may now recommend `workflow-medic`, `pr-medic`, `branch-medic`, `site-auditor`,
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

### If you're working
- **Step 0 — Todos**: run `python scripts/fetch_todos.py`. Handle the top OPEN todo if
  any exist (see "Todos" section). Call `complete_todo.py <id>` when done.
- **Step 1 — Resolve deps**: run `python scripts/resolve_deps.py`.
- **Step 2 — Claim**: run `python scripts/claim_task.py <project> <task-id> --owner worker
  --session <id>` (see "Rotation collisions" above). It checks `origin/main` fresh,
  refuses if another session already claimed the task, and otherwise pushes the
  `status: claimed`/`owner: worker`/`updated` commit straight to `main` for you. On
  `ALREADY_CLAIMED`, do not implement this task — pick the next `ready` task instead.
- Branch `worker/<project>-<task-id>`. Do ONLY that task.
- **Rebase onto `origin/main` immediately before opening the PR** (all kinds): run
  `git fetch origin main && git rebase origin/main` (or merge) right before `gh pr
  create`, so the PR opens conflict-free against the current tip instead of drifting
  stale while it waits for review. `STATUS.md` / `workspace.html` / `ROADMAP-AUDIT.*`
  are regenerated on every push to `main`, so a branch whose merge-base is even one
  `chore: refresh STATUS.md …` auto-commit behind will conflict on these files 100%
  of the time — resolve any such conflict by taking main's copy per hard rule 9
  (they're auto-generated). This keeps trivial auto-gen conflicts off the Reviewer's
  plate (kaizen from PR #550, conductor/t-045).
- **software:** open a PR into `main`, fill the handoff template (including "Flags for
  Reviewer"), set task `status: review`, verify it, resolve conflicts if present, and **merge
  it** — reversible/scoped/verified software work is merged, not parked at an open PR. After a
  successful safe merge, **before hand-writing `status: done`**, check `task-events/` for an
  already-queued event naming this same project/task (a "PR merged" auto-queue mechanism can
  race a manual close-out — both derive staleness from the same monotonically increasing
  `updated` timestamp, and whichever writes last makes the other look stale, silently
  discarding its `learning`/`note` payload with no trace; see conductor/t-085, TALKBACK.md
  2026-07-26). If a matching event exists, either let it apply on its own next processor run
  (don't also hand-write the transition) or explicitly consume it first — apply its
  `learning`/`note` payload, then delete the file — rather than racing it blind. Only once
  that's clear, close the task out with `python scripts/close_task.py <project> <task-id>
  done --session <id>` (the branch is auto-removed on merge) — **never** a plain
  `set_task_field.py` edit followed by a direct `git commit && git push` to `main`.
  `close_task.py` pushes the `status: done` edit to its own small branch (checked fresh
  against `origin/main`, same collision-resistant git plumbing as `claim_task.py`); open a
  tiny PR from that branch into `main` and merge it, exactly like any other software
  change. Hard safety rule 1 ("PRs only into `main`, except the Worker's atomic claim
  commit") does not carve out a second exception for close-out bookkeeping — a direct push
  here is exactly the gap conductor/t-091 self-flagged from the coloring-book/t-036
  close-out (2026-07-28): every prior close-out commit in this repo's history carries a
  `(#PR)` suffix, meaning a small follow-up PR was always the actual convention, just not
  the tooling default. Several close-outs from the same PR/session can share one
  `close_task.py` branch (call it once per task with the same `--branch`) so one PR closes
  a whole batch.
- **content:** write the draft file, open a PR, set `status: needs-human`.
- **proposal:** write `pitches/<date>-<slug>.md` using the pitch template, open a PR, set
  `status: needs-human`.
- **Every run ends with a clean `main` and no leftover branch.** The required terminal state
  for reversible, scoped, verified, non-gated work is **merged into `main`** — not an open PR
  left for a human to merge. Do not "park" safe work at an open PR because no one told you to
  merge: merging safe work is the default, not a request. Only work that is genuinely unsafe,
  human-gated, outward-facing, irreversible, or blocked ends unmerged — and it ends at
  `status: needs-human` with its PR open (so it isn't lost), never as a silent stranded branch.
  Merged branches are removed automatically (the repo's delete-on-merge setting + the
  `branch-janitor` workflow); never leave a no-PR branch behind. Work one task in flight at a
  time — you may complete several tasks in a single run, but finish each (merged, or parked at
  `needs-human` with a PR) before claiming the next. Never hold two active claims at once.
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

### If you're reviewing
- Read the project's `kind` first.
- **Before reviewing:** check the project's `TALKBACK.md` for any prior critique context
  on this task or recurring Worker patterns. Use it to calibrate your review.
- **software, reversible, does the task, scoped:** approve and merge if the Worker has not
  already merged it — do not leave a safe PR open for Silas; merging safe work is the
  Reviewer's job too. Otherwise audit the result and append TALKBACK if useful. Either way the
  run ends with the work on `main` and no branch left behind.
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
  theirs is weak). One sentence title, `stakes: reversible`. Get the id from
  `python scripts/next_free_task_id.py <project>` (checks `origin/main` fresh) rather than
  hand-picking one — this is the fix for the id-collision class that produced
  interface-vision/t-065 (`t-061`/`t-062` each hand-assigned twice in one day). This
  compounds improvement across cycles automatically. Check `LEARNING-REPORT.md` first
  — target a systematic
  weakness over a generic improvement when one applies (see "Learning ledger").
- **On a `challenged` task:** read the Worker's TALKBACK entry carefully. If the Worker's
  case has merit, adjust your decision and append a response. If not, escalate to
  `needs-human` for Silas to arbitrate — never re-reject a challenge silently.

### If you're fixing a failing scheduled workflow

`select_role.py` recommended `workflow-medic`: a watched scheduled workflow
(default `process-task-events.yml`) has failed `--workflow-fail-threshold` (default
3) or more completed runs in a row, with nothing else having noticed.

- Read the most recent failing run's job logs directly (`get_job_logs` with
  `failed_only`, generous `tail_lines` — the default truncates before the real
  error on some jobs, a documented recurring gap). Diagnose the actual cause, not
  just "it's red": a malformed `task-events/*.yaml` entry, a real code regression in
  the workflow's own script, transient infra, or a downstream dependency (API rate
  limit, a repo it reads from being unreachable).
- **Fixable now:** push the fix (a corrected/quarantined malformed input, a script
  bug fix, a workflow-file correction) and re-run the workflow (`actions_run_trigger`
  if it supports `workflow_dispatch`, or wait for its next scheduled tick) to confirm
  it actually goes green — don't close this out on a plausible-looking diff alone,
  same discipline as every other fix-then-verify role here.
- **Malformed input from elsewhere** (e.g. a `task-events/*.yaml` entry another
  session queued incorrectly): fix or quarantine the bad entry rather than patching
  around it in the processor, unless the processor's own validation gap is the real
  root cause (in which case fix both — tighten validation so the next bad entry fails
  at PR time via `validate_task_events.py`, per conductor/t-103's precedent).
- **Not fixable from this session** (needs credentials/access this sandbox lacks, or
  a decision only Silas can make): leave a clear note on the affected roadmap task
  (or open one if none exists yet) at `status: needs-human` with `soft_gate: true` if
  other work can still proceed in parallel, and move on to the next role/task rather
  than stalling the whole session on it.
- This check only watches conductor-repo scheduled workflows by default (see the
  scope note above) — it does not replace reading `TALKBACK.md`/`RENDER-BACKLOG.md`
  for kind_robots-side incidents surfaced other ways.

### If you're fixing PR errors

`select_role.py` recommended `pr-medic`: an open PR has CI that's both **red** and
**stale** (no push in the configured window despite failing) — a genuine orphaned
error, distinct from a PR mid-iteration whose latest push just hasn't gone green yet.

- For each PR in `red_stale_prs`: open it, read the actual failing check's logs (not
  just the red status), and diagnose the real cause — flaky/transient infra vs. a
  real regression vs. a pre-existing failure on the base branch the PR's diff didn't
  cause (check whether the base branch itself is also red before blaming the PR).
- **Fixable now:** push a commit that fixes it. Re-run/verify the check goes green.
  This follows the same "drive to green" discipline as the PR-activity CI-failure
  handling elsewhere in this manual — diagnose and push a fix, or reply explaining
  why not; never leave a red check silently unaddressed.
- **Base branch itself is broken** (the PR's own diff isn't the cause): say so once on
  the PR (which check, confirmed also red on base) rather than repeatedly re-diagnosing
  the same non-issue, and don't merge base into the PR until the base recovers.
- **Not actually fixable / needs a human call** (e.g. the fix requires a decision only
  Silas can make, or touches something outward-facing/irreversible): comment explaining
  the real blocker and leave the task at `status: needs-human` — do not force a merge
  past a red required check, and do not silently close the PR.
- **The PR is simply abandoned** (author/owner unclear, work superseded elsewhere,
  genuinely dead): don't unilaterally close someone else's PR — flag it in the
  project's `TALKBACK.md` with your read and, if the underlying task's roadmap status
  doesn't already reflect this, correct it (matching the same "roadmap state must
  reflect live reality" principle as `check_pr_merged_drift.py`).
- Cross-repo: `select_role.py` checks both conductor's and kind_robots' open PRs by
  default. If you have access to still other repos, check those too via GitHub MCP
  tools before concluding there's nothing to fix.

### If you're triaging stale branches

`select_role.py` recommended `branch-medic`: `branch_janitor.py`'s STRANDED tier has
entries — branches with unique unmerged commits, old enough that nobody's actively
pushing to them. This is deliberately the ONE tier `branch_janitor.py` itself never
acts on (it only auto-deletes MERGED/FORCE-named branches and *reports* STRANDED ones)
— judgment is required, and that's this role's job:

- For each stranded branch: read its actual diff against `main`, not just the commit
  messages — is this real, reviewable, not-yet-landed work, or leftover scratch state
  from an abandoned/superseded session?
- **Real, reviewable work:** open a PR from it (or, if you're confident it's safe,
  reversible, and scoped, finish and merge it directly per the normal Worker/Reviewer
  merge rules) rather than leaving it to rot further. If it's stale enough that it
  conflicts with current `main` in ways that need real judgment to resolve (not a
  mechanical STATUS.md/ROADMAP-AUDIT.* auto-gen conflict), rebase and resolve properly
  before opening the PR — do not force-push over unrelated newer history.
  Reuse the git-race guardrail already in this manual (see "Don't delegate an in-flight
  git workaround to a background subagent" pattern in `CLAUDE.md`-style operating
  notes) — verify the branch's current remote tip immediately before touching it, since
  time may have passed since `select_role.py` last checked.
- **Confirmed superseded/scratch, safe to discard:** delete it yourself if your
  session's credentials allow (`git push origin --delete <branch>`); if they 403 (the
  documented sandbox limitation — session credentials can't delete refs, only the
  `branch-janitor` workflow's `GITHUB_TOKEN` can), don't leave it hanging — trigger
  `branch-janitor.yml` via `workflow_dispatch` with `force_delete_branches` set to the
  branch name(s) you've verified, rather than reporting it and stopping.
- **Genuinely ambiguous** (can't tell if it's real unfinished work without more context
  than you have, e.g. a Silas-authored branch with unclear intent): do not guess either
  way — leave it reported (this is exactly the case STRANDED exists to surface to a
  human/session with more context) and note it in the project's `TALKBACK.md` or the
  root one if it's not project-scoped.
- Never touch `main` itself, and never delete a branch that still has an open PR
  against it (that's the reviewer role's territory, not this one's).
- Cross-repo: `select_role.py`'s STRANDED check covers both conductor (via
  `branch_janitor.py`'s local git) and kind_robots (via the GitHub API — the same
  classification, `list_branches`/compare/commit-date, just without needing a local
  checkout) by default. kind_robots branches accumulate the same way conductor's do
  (see conductor/t-078 for a real example this exact gap once produced) and now get
  the same STRANDED scrutiny. If you have access to still other repos beyond these
  two, check them via GitHub MCP `list_branches` using the same judgment above — there's
  no scripted classification for them yet, so read each candidate branch's actual
  state (merged? open PR? how old? real diff or empty?) directly.

### If you're doing the weekly site audit

`select_role.py` recommended `site-auditor`: the weekly gap-audit is overdue (never
run, or `--audit-stale-days` old or older). This role folds
`projects/global-ui/SITE-AUDIT-AGENT.md`'s originally-planned dedicated Claude Code
Remote Trigger into the same self-assigning system every other role uses (Silas,
2026-07-26: "we have a weekly review job, can we add that as a role as well?") — it
no longer needs its own separately-approved platform trigger; it rides whichever
trigger fires next, as long as `select_role.py` runs first and nothing higher-priority
is pending.

- Read `projects/global-ui/SITE-AUDIT-AGENT.md` in full and follow its **Agent
  Prompt** section verbatim — that spec is authoritative for scope/boundaries, not a
  paraphrase here. In short: cross-reference every active project's roadmap
  vocabulary (API routes, Vue components, Pinia stores, schema models it mentions)
  against what actually exists in `/home/user/kind_robots/`, using Glob/Grep — never
  call the live site.
- Write findings as a report to `projects/global-ui/AUDIT-REPORT-<YYYY-MM-DD>.md`
  (today's date, matching `select_role.py`'s `AUDIT_REPORT_RE` filename contract
  exactly — a differently-named file won't be recognized as satisfying this week's
  audit, and the role will keep recommending itself next time).
- Propose **up to 3** small, reversible follow-up tasks from the most impactful
  gaps found — new `ready` tasks in the relevant `roadmap.yaml` files, `stakes:
  reversible`, `owner: null`. This is a read-and-report run: roadmap task additions
  are the only writes permitted besides the report itself and opening the PR.
- Never modify a task marked `gate_human: true` without human review, never run
  npm/pnpm builds, never push directly to `main` — one PR per run, same as any other
  software-kind task, title `audit(site): weekly gap report YYYY-MM-DD`.
- If `select_role.py` reports `site_audit_overdue` but you can't complete a full
  audit this cycle (e.g. genuinely out of session budget), it's fine to leave it for
  the next session that self-assigns this role — don't write a partial or empty
  report just to stop the recommendation from firing; an honest "still overdue" is
  better than a hollow report that silently lowers the bar for what counts as done.

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
