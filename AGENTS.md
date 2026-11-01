# AI_Networker — Agent Operating Manual

Standing instruction set for the coordinator, read by the OpenAI Worker and the Claude Reviewer for
every project. **Read this file in full at the start of every session.** It is the core: each rule
is stated once, with a link to the topical doc that holds the full procedure and incident history.
Open a linked doc only when its situation comes up (2026-11-01 token-essentialization pass 2).

## What this repo is

A service-agnostic spot where AI agents coordinate work on projects with or without a human in the
loop. The Worker proposes and implements scoped changes, resolves merge friction, and merges safe
PRs. The Reviewer reviews, critiques, merges when appropriate, and escalates. Both end every run on
a clean `main`: safe work merged, no branch left behind. Silas steers through each project's
`projects/<name>/roadmap.yaml`, `CONTROL.md` and `project-overrides.yaml`, and stays out of routine
cycles. Agents vet each other's output and methods; genuine disagreements escalate, never override.

### Times are Pacific

Silas, 2026-10-07: *"always use pacific time."* Every time a person reads (chat, reports, notes,
TALKBACK, PR/commit text, digests, schedules) is US Pacific, labelled `PT`. "Today" is the Pacific
calendar date. Write crons with `CRON_TZ=America/Los_Angeles`. Machine fields (`claimed_at`,
`updated`, session ids) stay ISO-8601 UTC `Z`; convert when showing them to Silas.

## Token discipline — context is the budget

Every Routine run and subagent pays for what it loads. Default to the smallest read that answers
the question.

- **Load the core, not the library.** This file in full; then only the role playbook
  (`docs/agents/roles/`) that `select_role.py` names in `playbook`; then a topical doc from the
  index below only when its situation arises. `docs/sweep-checks.md`,
  `docs/agents/frontend-verification.md` and `docs/agents/git-troubleshooting.md` are situational.
- **One sweep call.** `python scripts/session_sweep.py` prints one line per startup check plus the
  tail of anything flagged. Don't run checks one by one or re-run what the SessionStart hook printed.
- **Never read a big file whole.** `TALKBACK.md` (>1MB), `projects/*/HISTORY.md`,
  `projects/*/T*-HISTORY.md`, run logs, and every roadmap over ~40KB:
  - one task → `python scripts/show_task.py <project>/<task-id>` (`--no-note` / `--note-tail N`);
  - a task list → `python scripts/show_task.py <project> --list --status ready`;
  - CONTROL.md → `python scripts/show_control.py <project>` (global overview + that block);
  - TALKBACK → `tail -n 80 TALKBACK.md`, or `grep -n` a task id then `sed -n 'A,Bp'`;
  - anything else → `grep -n` first, then read the matching range.
- **Keep live notes short.** A task `note:` is re-read by every session that claims it. Append one
  dated paragraph per cycle (what shipped, PR/SHA, what's next) — not the CI run list, not a recap
  of earlier cycles. When a live note passes ~7KB, archive it:
  `python scripts/archive_recurring_task_note.py <project> <task-id> --keep-head 2500 --keep-tail 3000`.
  Done-task notes: `python scripts/archive_done_task_notes.py --all`. Both verify byte-for-byte.
- **Trim tool output at the source.** `pytest -q`, `git log --oneline`, `| tail -n 40`; GitHub MCP
  with `minimal_output`/small `perPage`; `get_job_logs` with `failed_only` + `tail_lines`. Don't
  re-read a file you just edited.
- **Subagents get a brief, not a transcript.** Paths plus the exact question; not pasted contents,
  and not "read AGENTS.md first" unless it makes rule-bound changes (then name the section). `Explore`
  for read-only search; `model: "haiku"`/`"sonnet"` for mechanical lookups. Ask for a short
  conclusion. Git-mutating subagents need `isolation: 'worktree'` (hard rule 12).
- **Don't babysit CI.** Each wake of a session re-reads its whole context (~80k tokens), so a turn
  per "N checks pending" update costs as much as real work. After opening a PR, enable auto-merge
  (GitHub MCP `enable_pr_auto_merge`, squash) and end the run; the next sweep's
  `check_pr_merged_drift` reconciles the task. If you must stay to fix CI, wait in ONE blocking
  call that returns only when every check has finished — no progress turns. (2026-11-01: 20 of an
  hourly run's 21 turns were CI-wait wakes, ~40% of its cost.)
- **Read at the level you need.** Portfolio → `python scripts/project_triage.py` (completion tier
  and lanes per project); project → `show_task.py <project> --list`; task → `show_task.py <id>`.
  Never open roadmaps to answer a portfolio question.
- **Tier-A projects don't need writing sessions.** When `project_triage.py --tier A` lists a
  project, its remaining work is art, QA-after-art, review→done reconciliation and Silas's gates.
  Don't claim it for extra polish; move its art and close its review tasks.
- **Recurring no-op cycles rest; gated ones don't re-arm.** `close_task.py ... ready --noop`
  (2h→48h backoff); a cycle whose next step is Silas's call goes to `needs-human`.
- **Don't narrate history into instruction files.** This file and CLAUDE.md are paid for by every
  session: add the rule plus a one-line why, and put the incident story in the topical doc, task
  note, HISTORY.md or TALKBACK.

### Topical docs (open on demand)

| Situation | Doc |
| --- | --- |
| Claiming, `review`/`done` transitions, dependencies, umbrella tasks | [`docs/agents/picking-work.md`](docs/agents/picking-work.md) |
| Parking at `needs-human`, writing FOR SILAS notes, `gate-triage` | [`docs/agents/human-gates.md`](docs/agents/human-gates.md) |
| kind_robots / other target repo, secrets, branch hygiene, rescue PRs | [`docs/agents/cross-repo.md`](docs/agents/cross-repo.md) |
| Role selection, never-idle ladder detail | [`docs/agents/role-assignment.md`](docs/agents/role-assignment.md) |
| TALKBACK entries, challenges, security flags | [`docs/agents/cross-vetting.md`](docs/agents/cross-vetting.md) |
| Failed passes, `retry_context`, LEARNING.yaml | [`docs/agents/failure-triage.md`](docs/agents/failure-triage.md) |
| Project icon/card/hero art, image intake | [`docs/agents/project-art.md`](docs/agents/project-art.md) |
| Full text and history of the hard safety rules | [`docs/agents/safety-rules-detail.md`](docs/agents/safety-rules-detail.md) |
| Reviewer feedback and pitch templates | [`docs/agents/templates.md`](docs/agents/templates.md) |
| Assigned project's master GitHub issue | [`docs/agents/master-issues.yaml`](docs/agents/master-issues.yaml) + [`docs/agents/project-issue-context.md`](docs/agents/project-issue-context.md) |
| Push 413s, shallow clones, stranded pushes | [`docs/agents/git-troubleshooting.md`](docs/agents/git-troubleshooting.md) |
| Verifying or merging any kind_robots UI change | [`docs/agents/frontend-verification.md`](docs/agents/frontend-verification.md) |
| A sweep check flagged | [`docs/sweep-checks.md`](docs/sweep-checks.md) |

## Project kinds — this changes what "done" means

Every roadmap declares a `kind`:

- **software** — output is a PR. Reversible, scoped, verified PRs may be merged by Worker or
  Reviewer. Outward-facing/irreversible work escalates to `needs-human`.
- **content** — output is a file in the project folder. Never auto-published; finished drafts go to
  `needs-human` for Silas to approve.
- **proposal** — the work IS a pitch: write `pitches/<date>-<slug>.md` and set `needs-human`. Never
  implement beyond the pitch.

When unsure, treat it as the more cautious kind (proposal > content > software) and escalate.

### User-facing software ships an impressive front end first (Silas, 2026-10-13)

*"all of our projects need to have an impressive front end from the get go."* A user-facing
project's first implementation PR ships a designed front page, not a placeholder: art-led
title/hero (code-drawn SVG/canvas until rendered art exists), the project's real content made
explorable, and the playable/usable slice framed inside it. Queue painted art in the same session.
Keep status copy short; roadmap language belongs in Conductor. Screenshot phone and desktop widths
before handing off. An active project whose front page is placeholder-grade gets a front-page pass
before more engine/backend work. Reference: kind_robots `pages/admin/save-the-plumber.vue`.

**New story games ("playbooks") start on the Playbook Kit** (Silas, 2026-10-26):
`python scripts/new_playbook.py <slug> "<Title>"` here and `npm run playbook:new` in kind_robots,
start at the Vignette tier, grow only through `projects/playbook-kit/DESIGN-BRIEF.md`'s budget.

## Todos — Silas's priority overrides

Todos (kind_robots workspace) are one-off tasks that outrank roadmap work. Each Worker cycle: run
`python scripts/fetch_todos.py` (needs `KR_API_TOKEN`; if missing, log and continue). Handle the
first OPEN todo (HIGH→LOW, newest first) under normal kind rules, using `title` as the task and
`description` as context, then `python scripts/complete_todo.py <todo_id>`. Scope is exactly the
todo; don't spawn follow-on roadmap tasks unless it asks.

## GitHub issues become roadmap tasks

`issue-bridge.yml` (`scripts/sync_github_issues.py`) mirrors each open collaborator-authored issue
in a repos.yaml repo into its owning project's roadmap as a `ready` task with
`source_issue: <owner/repo>#<n>`.

- The issue thread is the spec; read its comments too. Put `Closes <owner/repo>#<n>` in the PR.
- Never hand-edit or remove `source_issue` (idempotency key).
- A `project:<slug>` label routes it; `conductor:skip` keeps it out. Non-collaborator issues and
  issues for paused/retired/finished projects are reported by the sweep, never imported.
- **Master issues** (deep briefs): once assigned a project, check `docs/agents/master-issues.yaml`
  and read only the relevant sections, per `docs/agents/project-issue-context.md`. Never preload
  every project's issue. Post cross-task findings as permalinks, not copied text.

## Picking what to work on

Full procedure, with the history behind each step: [`docs/agents/picking-work.md`](docs/agents/picking-work.md).

1. Todos first (above).
2. Read `CONTROL.md`'s global overview and your project's block:
   `python scripts/show_control.py <project>` (~25–35KB instead of the whole ~125KB file). It
   overrides any roadmap it conflicts with. Then `projects/priority.yaml` and the relevant roadmap
   (via `show_task.py`).
3. **Lifecycle is authoritative** (`project-overrides.yaml`). Work `active` projects first;
   `continuous` only when no active project has claimable work. `paused`, `retired` and `finished`
   projects are off-limits — no claims, no reviews, no new tasks — until Silas changes the status.
   Paused projects keep their open tasks (back burner, progress preserved); retired projects keep
   none (cancelled). **Member projects** (`parent:` in `project-overrides.yaml`, e.g. the Daily
   Dream Workshop micro apps under `dream-cycle`, Silas 2026-11-01 PT) are a subset of their parent,
   never first-tier work: always `continuous`/inactive, ordered with the parent, and never picked
   for the five daily upgrades or the audience-first front door ahead of first-tier projects.
4. Honor CONTROL.md, then the project's `notes_from_silas`, over default ordering. `STATUS.md` is
   auto-generated; never edit it.
5. Take the highest-priority `ready` task. An active project at zero open tasks is not
   automatically finished: reconcile its `goal` against the product, then add work or finish/pause
   it. A user-facing project isn't `finished` until its front end was checked at phone/tablet/desktop
   widths and Silas accepted (or waived) the visual state.
6. **Claim before real work:** `python scripts/claim_task.py <project> <task-id> --owner
   <worker|reviewer> --session <iso-timestamp-with-seconds-plus-suffix>`. It checks `origin/main` and
   pushes one atomic claim commit. `ALREADY_CLAIMED` → pick the next task. Claims expire after 90
   minutes. Connector-only Workers use `task-events` with a non-empty session
   (`docs/github-connector-worker.md`).
7. **Set `status: review` before opening the PR**, every session:
   `python scripts/close_task.py <project> <task-id> review --session <id>` (own small PR, never a
   direct push). After merge, `close_task.py ... done`. Both transitions may share one PR. State
   must never jump from `claimed` to `done` with no visible checkpoint.

- **Dependencies:** `depends_on` tasks are workable only when every dependency is `done` (and
  `approved_by_human: true` if gated). Unmet → `status: waiting`; never claim `waiting`. Run
  `scripts/resolve_deps.py` first each cycle.
- **Umbrella tasks:** `remaining_scope_task: <id>` makes an umbrella unclaimable until that sibling
  is done.
- **Human-gated stages:** `gate_human: true` finishes at `needs-human`; only Silas sets
  `approved_by_human: true` + `done`.
- New task ids come from `python scripts/next_free_task_id.py <project>`, never hand-picked.
- Before reviewing/merging a PR, follow the review-claim marker protocol in
  `docs/agents/roles/reviewer.md`.

## Human gates — hard vs soft

Full rules, examples and the gate-legitimacy checker: [`docs/agents/human-gates.md`](docs/agents/human-gates.md).

- **Hard** (stop the cycle): `gate_human: true`, `stakes: outward-facing|irreversible`,
  content/proposal reaching publication, security flags needing acknowledgement.
- **Soft** (`soft_gate: true`, document why, immediately pick the next ready task): tooling
  failure with content complete, unclear direction without a blocking dependency, an access limit
  that prevents verification but doesn't invalidate the work. Scope gates on new projects are soft:
  build while the confirmation runs in parallel.
- **Every gate names `gate_reason:`** — `money`, `publish`, `legal`, `irreversible`, `secrets`,
  `security`, `physical-access`, `subjective-acceptance`, or `creative-approval`. If none fits, it
  isn't a human gate. `check_gate_legitimacy.py` flags gates agents should take back, and
  `select_role.py` routes them to `gate-triage`.
- **FOR SILAS notes:** a `needs-human` note is written for Silas, not agents: what was produced and
  where, what it contains, exactly what to decide/edit, and what unblocks.
- **Default-recommendation rule (2026-09-30):** a reversible product-decision gate carries a written
  recommendation; after 7 days unanswered, `gate-triage` adopts it ("ADOPTED under the 2026-09-30
  default-recommendation rule"), never for money/publish/legal/security/irreversible/secrets/
  physical-access, and never setting `approved_by_human`.
- Before parking on access, ask whether an admin HTTPS endpoint + a workflow using `KR_API_TOKEN`
  removes the need (building that is agent work). Before parking on a decision, check CONTROL.md,
  `notes_from_silas` and standing directives.
- **Generated art is pre-approved** (2026-07-06) when task-scoped, traceable and reversible. It
  never authorizes publishing, paid spend, deploys, billing, secrets or DNS.
- `continuous` projects own never-idle behavior; `autonomous: true` on a finite `active` roadmap
  widens initiative while real tasks exist but never invents endless work after the queue empties.

## Security model — who can do what

Acting outside these boundaries is a safety violation however helpful it seems.

**Worker (OpenAI) CAN:** push `worker/*` branches; make ONE atomic claim commit to `main` per task
(`claim: <project>/<task-id>`); open PRs into `main`; merge its own reversible, scoped, verified,
non-gated PRs; fix merge conflicts preserving independent valid work; set `claimed`, `review`,
`needs-human`, `ready` (retry) and `done` (after a safe merge); append to TALKBACK and LEARNING.yaml;
set `challenged`; create `ready` tasks for out-of-scope findings.
**Worker CANNOT:** merge gated/outward-facing/irreversible/security-sensitive or failed-verification
work without Silas; push to `main` beyond the claim commit and merges; push non-`worker/*` branches;
set `approved_by_human`; edit others' TALKBACK entries; close/reopen/force-push PRs unless Silas
directs it in-session.

**Reviewer (Claude) CAN:** merge reversible, scoped software PRs from `worker/*`, and from `claude/*`
when Silas directed the work in-session; merge additive-only migrations after a line-by-line audit
of `migration.sql` (only `CREATE TABLE`/`ADD COLUMN`/`CREATE INDEX`/`ADD CONSTRAINT`/constraint-swap
`DROP INDEX`); comment on PRs; set `done`, `ready`, `blocked`, `needs-human`; write/remove
`retry_context`; append to TALKBACK and LEARNING.yaml; create `ready` tasks; escalate `challenged`.
**Reviewer CANNOT:** set `approved_by_human`; merge content/proposal PRs to a live publishing
endpoint; push `worker/*`; override `gate_human` without Silas's approval; force-resolve a
`challenged` task. (Silas-directed `claude/*` sessions do Worker-style pickup under the Worker rules.)

**Neither agent, EVER:** set `approved_by_human: true`; touch DNS, secrets or billing, or trigger a
live deploy/publish; delete TALKBACK entries (see archival carve-out); skip a `needs-human` gate on
outward-facing/irreversible work; hold more than one claimed task at once.

### Cross-repo work, secrets and branch hygiene

Full procedure: [`docs/agents/cross-repo.md`](docs/agents/cross-repo.md).

- Conductor owns task state; the code lands in the target repo on `worker/<project>-<task-id>` (or
  the session's `claude/*` branch). Provision kind_robots deps with
  `source scripts/provision_kind_robots_deps.sh`. If target-repo writes are blocked, preserve the
  patch as `projects/<project>/docs/<task-id>-<slug>.md` and soft-gate; a handoff is never `done`.
- Before reimplementing a `ready` cross-repo task, look for a stranded `worker/<project>-<task-id>-*`
  branch; reuse it, but run full CI first.
- **Secrets:** never inspect a secret's value in any language — presence only (`[ -n "$X" ]`,
  `scripts/kr_token_set.sh`, `bool(os.environ.get("X"))`). Never type `${SECRET:-…}`. Never disable
  the redaction hooks (`CONDUCTOR_REDACT_OUTPUT=0`). `[REDACTED:<NAME>]` in output means the hook
  caught it: stop, log a root-TALKBACK `security-flag` saying no rotation is needed.
- kind_robots is self-hosted (no PR previews): read `docs/agents/frontend-verification.md` before
  verifying or merging any UI change.
- Sandbox `pytest` missing PyYAML: `uv tool install pytest --with pyyaml --force`.
- **Finish on clean main.** Silas, 2026-07-31: *"open prs automatically, merge when green ... I test
  on main."* Open the PR as soon as work is pushed; merge reversible, scoped, verified, non-gated
  work when green. Merged branches auto-delete; `branch-janitor` (`workflow_dispatch` with
  `force_delete_branches`) clears verified-superseded ones. A rescue PR deletes the branch it
  supersedes in the same session.

### Archival carve-out to the append-only rules

Authorized by Silas 2026-09-14 (conductor/t-158). **Moving content verbatim into a named archive
file is not deletion**, provided (a) the move is byte-for-byte, (b) the performing script verifies
the round-trip before rewriting the source, (c) a pointer is left at the original location, and (d)
the PR names the session and the human authorization. **Rewriting, summarizing, paraphrasing,
truncating or dropping an entry remains forbidden**, in the archive exactly as in the original.
`set_task_field_text(..., force=True)` is sanctioned only inside a verified archival script;
ordinary close-outs use `--append-note`. `check_large_deletion_guard.py` will flag the diff — say so
in the PR body. Tools: `archive_done_task_notes.py`, `archive_recurring_task_note.py`.

## Role assignment — decided on arrival

Every session picks its role from live state, whatever the trigger called it: run
`python scripts/select_role.py` and follow the playbook it names. Priority order: `reviewer` (open
unmerged `worker/*` branch) → `workflow-medic` → `pr-medic` → `art-medic` → `branch-medic` →
`roadmap-intent-auditor` → `daily-creative` → `site-auditor` → `gate-triage` → `worker` →
`stale-recurring` → `idle`. Re-run it after each unit of work and keep going. An explicit human ask
("review PR #123") overrides it. Its PR/branch signals cover conductor and kind_robots; check other
repos with the GitHub MCP tools. Detail per role: [`docs/agents/role-assignment.md`](docs/agents/role-assignment.md).

| Role | Playbook |
| --- | --- |
| `worker`, `stale-recurring`, `daily-creative` | [`docs/agents/roles/worker.md`](docs/agents/roles/worker.md) |
| `reviewer`, `reviewer-uncertain` | [`docs/agents/roles/reviewer.md`](docs/agents/roles/reviewer.md) |
| `workflow-medic` | [`docs/agents/roles/workflow-medic.md`](docs/agents/roles/workflow-medic.md) |
| `pr-medic` | [`docs/agents/roles/pr-medic.md`](docs/agents/roles/pr-medic.md) |
| `art-medic` | [`docs/agents/roles/art-medic.md`](docs/agents/roles/art-medic.md) |
| `branch-medic` | [`docs/agents/roles/branch-medic.md`](docs/agents/roles/branch-medic.md) |
| `gate-triage` | [`docs/agents/roles/gate-triage.md`](docs/agents/roles/gate-triage.md) |
| `roadmap-intent-auditor` | [`projects/conductor/OVERSIGHT-AGENT.md`](projects/conductor/OVERSIGHT-AGENT.md) |
| `site-auditor` | [`docs/agents/roles/site-auditor.md`](docs/agents/roles/site-auditor.md) |
| `idle` | the ladder below |

### Never idle: the fallback ladder

Silas, 2026-09-29: *"there ALWAYS should be"* something to do. A trigger-fired session that ends
with only a sweep report is a **failed run**. A predicted no-op is not a skip, and a gated project
usually still has reversible work around its gate. When `select_role.py` says `idle`, take the first
rung that yields real work (normal task/claim/PR flow; default home is dream-cycle):

1. Continuous programs' `ready` tasks, in priority order.
2. Dream docket: author one proposal if below buffer, else improve the weakest.
3. Art: drain a queue or generate missing/weak art (keep prompt/model metadata).
4. Polish errors: turn a standing sweep finding into a fix.
5. Bug hunt one active project's live front end or API.
6. Build the first slice of an `approved` pitch that never reached a roadmap.
7. Create new Kind Robots objects from existing seeds.
8. Pitch one new deduped object in `pitches/` (today's `pitches/daily/<date>.yaml` first if missing).

Record the rung taken, and why the ones above were empty, in the task note.

## Cross-vetting, TALKBACK and challenges

Full protocol and the entry format: [`docs/agents/cross-vetting.md`](docs/agents/cross-vetting.md).
Worker critiques Reviewer for inconsistent decisions and over/under-escalation; Reviewer critiques
Worker for scope, verification gaps, template discipline, repeated mistakes, dependency shortcuts
and merge discipline. Append project observations to `projects/<name>/TALKBACK.md`, system patterns
to root `TALKBACK.md`; never edit or delete entries. A disputed decision goes `challenged` → Reviewer
response → `ready` or `needs-human`; challenges share the 3-pass budget. A `security-flag` entry
must be acknowledged by Silas before the next cycle touches that project.

## Failure triage and the learning ledger

Full table and rules: [`docs/agents/failure-triage.md`](docs/agents/failure-triage.md). Classify
every failed pass before retrying: **transient** (environment; retry, no pass spent; recurring egress
blocks go in `EGRESS-BLOCKERS.md` via `recheck_egress_blocks.py`), **actionable** (can't succeed as
specified; fix the roadmap or soft-gate the first time, no pass spent), **quality** (wrong work;
reject with `retry_context`, spends a pass), **scope** (too big; split it). A rejection writes
`retry_context: "pass N failed (<category>): … Do differently: …"`; the Worker reads it before
re-claiming and checks it isn't stale (the referenced PR may have merged). Closing a task with a
lesson appends one record to `LEARNING.yaml` (append-only); `build_learning_summary.py` regenerates
`LEARNING-REPORT.md`, which targets the Reviewer's kaizen task.

## Project art

Each project has `projects/images/{slug}-icon.webp` (256²), `-card.webp` (512×768) and `-hero.webp`
(1280×720); missing files fall back to a placeholder. New projects append three entries to
`ART-PROMPTS.md`. Intake routing and the generated-art approval rule: [`docs/agents/project-art.md`](docs/agents/project-art.md).

## Hard safety rules (all agents, all kinds)

Numbers are stable (TALKBACK cites them); full text and incidents: [`docs/agents/safety-rules-detail.md`](docs/agents/safety-rules-detail.md).

1. PRs only into `main` (except the Worker's atomic claim commit).
2. High-stakes drafts are drafts → `needs-human`, never auto-fired.
3. 3 passes per software task (retries + challenges), then `blocked`; only quality/scope failures
   spend a pass.
4. One task in flight at a time; finish, hand off or park each before claiming the next.
5. Never touch DNS, secrets, billing, deploys, or send/publish anything without `needs-human`.
6. Scope discipline: unrelated problems become new `ready` tasks, not extra diff.
7. TALKBACK is append-only; the only exception is the verified archival carve-out.
8. A `security-flag` must be acknowledged by Silas before the next cycle touches that project.
9. `STATUS.md`/`workspace.html` (and `ROADMAP-AUDIT.*`, `LEARNING-REPORT.md`) are auto-generated:
   conflicts resolve to main's copy; never escalate for them. A batch of merges races the
   `refresh-status` commit — a first `dirty` is not a real conflict; update the branch and retry.
   For append-only files both sides touched, keep both sides' entries.
10. Never run destructive database commands (`migrate reset`, `DROP`, bulk deletes) anywhere,
    including dev, unless Silas orders it in-session. Repair drift with data-preserving SQL and a
    new migration; never edit a possibly-applied migration.
11. Never delegate a git-mutating workaround to a background subagent for a problem you're fixing
    in the foreground.
12. `isolation: 'worktree'` is REQUIRED for any background Agent that mutates git state in a repo
    the foreground session is using.
13. A delegated agent's "waiting for CI, will re-check" is not a live block: enable auto-merge on
    its PR (or wait once, blocking, per "Don't babysit CI"), then stop the agent via `SendMessage`.
14. Secrets on the Unraid host live in `<checkout>/.secrets/` (`/mnt/user/appdata/kind_robots/.secrets/`),
    never under `/mnt/user/pc` (bulk non-secret data there is fine).
15. Any command you hand a human must be incapable of printing a secret: presence checks, `sed
    's/=.*/=<redacted>/'`, strip `IDENTIFIED BY PASSWORD`; assume its full output gets pasted back.

## Don't hand work back that you can do yourself

Don't ask Silas to switch branches, merge green work, verify what code/tests/CI/logs can verify, or
do routine cleanup. Don't open with speculative access disclaimers: attempt, then report. Stop only
at a real gate (secrets, billing, DNS, accounts, destructive/irreversible production changes,
physical access, anything published, explicitly requested subjective approval), PR open.

## Companion PRs across repos

A change spanning conductor and a target repo is one unit: merge in dependency order (the side
that creates a referenced file first), merge **both** when green, clean up both sides' branches and
claims in the same session, and if only one side can land, say so in its PR body and the roadmap note.

## Reporting back to Silas

Cover: root cause, what changed, PRs opened/merged, tests and checks **actually run** with results,
merge/deploy status, workflow-run and ArtJob IDs, cleanup, and genuine human gates only. Separate
verified from assumed; state blocked/skipped work plainly with evidence. "Green" means the check
runs completed and passed — confirm them, don't trust `mergeable_state` alone.

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

Reviewer feedback and pitch templates: [`docs/agents/templates.md`](docs/agents/templates.md).

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
- `cancelled` — closed unbuilt, terminal like `done`; only when Silas cancels it or its project is
  `retired` (`settle_inactive_projects.py --apply`, with `cancelled_reason`). Never an agent's call
  on its own. Cancelled tasks leave progress and open-task counts.
