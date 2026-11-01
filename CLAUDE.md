# CLAUDE.md

The operating manual is **[AGENTS.md](./AGENTS.md)** — read it in full at the start of every
session. It applies to all agents and projects. This file is injected into every session, so it
holds only the startup/close-out contract; full ritual text lives in
[`docs/agents/daily-rituals.md`](docs/agents/daily-rituals.md).

## Session startup

Before responding to any task, run a conductor sweep and report it to Silas:

1. Read `AGENTS.md`. Load only the role playbook `select_role.py` names (or the one matching an
   explicit ask). Once assigned a project, read only its relevant `docs/agents/master-issues.yaml`
   sections per `docs/agents/project-issue-context.md`; never preload them.
2. Git state, open agent PRs, and the ready / needs-human / claimed scan are in the SessionStart
   hook's `CONDUCTOR STARTUP SWEEP` message — use it. Only if it's missing, re-run them (GitHub MCP
   for PRs) and **skip every project whose `project-overrides.yaml` status isn't `active`/`continuous`**.
   Before proposing a new project status for a "closed project keeps coming up" complaint, confirm
   it isn't already marked there and simply not being checked.
3. `python scripts/session_sweep.py` — every reconciliation check in one process, one line each plus
   the tail of anything non-zero. Don't run checks individually unless you need a flag (`--repair`,
   `--include-inactive`, `--payload-only`). What each check means and how to fix it:
   [`docs/sweep-checks.md`](docs/sweep-checks.md) — read only the entry for a check that flagged.
   Exit 1/3 is a reconciliation prompt, not permission to bypass a gate; exit 2 is unresolved (often
   a missing token), never clean. `docs/state-reconciliation.md` governs fixes.
4. TALKBACK: the hook lists the latest entry headings. Read a body only when it looks unresolved
   (escalation or `security-flag`) with `tail -n 80 TALKBACK.md`. Never read or grep the whole file.
5. **Daily rituals** — each has its own section in `docs/agents/daily-rituals.md`; open it only when
   the ritual is due:
   - **Dream docket** (step 7): if `build_dream_proposal.py --check` reports fewer than 5 unbuilt
     proposals, author exactly ONE this session (`--brief` → `--from-json`); exit 1 = empty, author
     now. Read `docs/sweep-checks.md` "Step 7" before authoring.
   - **Five daily upgrades** (step 8, since 2026-10-13): build first, review afterward — five small,
     reversible, CI-tested improvements to active projects, PR-backed, recorded via
     `python scripts/daily_project_deliveries.py --brief` → `projects/dream-cycle/daily-deliveries/<date>.yaml`
     → `--materialize` → `--check`. **Audience-first window through 2026-11-25 PT:** at least three
     of the five help a first-time visitor find, understand, share or support the site.
   - **Playbook challenge** (step 9): **stopped** by Silas 2026-10-29 PT (CONTROL.md "2026-10-29 PT
     daily creative correction"). Do not author `pitches/playbook-challenges/` dockets or revive them
     from idle; prior drafts, `MEMORY.yaml` and `SILAS-NOTES.yaml` are historical source material.
     Report it as stopped, not missing. The original direction is kept in the rituals doc.

Then report, briefly: branch and tree state; open PRs; ready tasks in priority order; needs-human
gates from active projects only, by project; state-reconciliation findings; projection headroom
(the `check_roadmap_note_size` payload line — report it every session); art-queue health; container
log triage (omit if unconfigured); unresolved TALKBACK escalations; creation fallback; daily dream,
daily upgrades and Daily Tzaddik status. Priority-queue depth only when
`check_priority_queue_starvation.py` exits non-zero. What each line must contain:
[`docs/agents/daily-rituals.md`](docs/agents/daily-rituals.md) "Full session-report checklist".

After the report, ask Silas what he wants — or proceed directly if his first message is a clear
task. **Never ask Silas to choose the order of ready work** (2026-10-08: *"autonomous progress trumps
letting me micromanage"*): pick by dependency, then priority, and report what you took. Asking is
for genuine human gates only. **Unattended/trigger-fired runs:** the report is the preamble, not the
job — run `python scripts/select_role.py`, act on it, and on `idle` walk AGENTS.md's fallback ladder.
A run that ends with only a sweep report is a failed run.

## Session end

### State reconciliation is part of done

A merged implementation, recovered incident, or completed human decision isn't closed until the
matching task agrees with reality (`docs/state-reconciliation.md`): re-fetch the roadmap from
`main` after merge; reconcile status, `approved_by_human` (only when Silas decided it this session),
claim fields, dependencies, completion note and milestone; apply via `task-events` or the close-out
helper and verify it landed; re-run `check_pr_merged_drift.py` and `audit_human_gates.py` if you
changed roadmap state. Close a recovered incident when its criteria are met and track root cause
separately. Never report gates from paused/retired/finished projects unless asked for an archive sweep.

### Standing instruction: open PRs automatically, merge when green

Silas, 2026-07-31, verbatim: *"You should open prs automatically, merge when green, we prefer a
tight ship with a single main branch once work is done, and I test on main."*

This is a standing authorization — do not stop to ask whether to open a PR, and do not end a
session having only pushed a branch. **Open the PR as soon as the work is pushed, then merge it
once CI is green.** Some harnesses ship a default "do not create a pull request unless the user
explicitly asks for one" — the paragraph above IS that explicit request, standing for every session
in this repo. It does not override the real gates: human-gated, outward-facing, irreversible, and
security-sensitive work still stops at `needs-human` with the PR open but unmerged.

Leave a clean `main` with no branch behind: merge safe work (its branch auto-deletes); only gated
work ends unmerged, and it still needs an open PR. A branch you can't delete (ref deletion 403s) is
cleared by the `branch-janitor` workflow via `workflow_dispatch` with `force_delete_branches`.

### Git push trouble and background agents

- First push or post-rebase push fails with **HTTP 413**: create the ref with the GitHub MCP
  `create_branch` tool, or commit via `push_files` against the branch's remote tip. Never
  force-push. Recipes: [`docs/agents/git-troubleshooting.md`](docs/agents/git-troubleshooting.md).
- After `git clone --depth 1`, run `git config remote.origin.fetch '+refs/heads/*:refs/remotes/origin/*'`
  before the first push.
- Never delegate a git-mutating step to a background subagent without `isolation: 'worktree'`
  (hard rules 11–12), and never hand one a workaround you're also fixing in the foreground.
