# CLAUDE.md

The operating manual for this repo is **[AGENTS.md](./AGENTS.md)** — read it in full at the start of every session. It applies to all agents (Worker and Reviewer) across all projects.

## Session startup

At the start of every session, before responding to any task, run a conductor sweep and report it to Silas:

1. Read `AGENTS.md` in full — it is the core manual. Per-role step lists live in `docs/agents/roles/`; load
   only the one `select_role.py` names in its `playbook` field (or the one matching an explicit ask).
2. `git status` / `git log --oneline -5`, 3. open agent PRs, and 4. the ready / needs-human / claimed scan
   are already in the SessionStart hook's `CONDUCTOR STARTUP SWEEP` message — use it rather than re-running
   them. Re-run only if that message is missing (hook not loaded, or not a remote session); then use the
   GitHub MCP tools for PRs, and **skip any project whose `project-overrides.yaml` status is not `active`**
   (`paused`, `retired`, `finished`) — reading `roadmap.yaml` without that cross-check resurfaces tabled
   projects' stale tasks (2026-07-25: career-transition/t-003 and pinball-hero/t-002). Before proposing a
   new project-status value for a "closed project keeps coming up" complaint, confirm the project isn't
   already marked in `project-overrides.yaml` and simply not being checked.
5. Read `docs/state-reconciliation.md`, then run `python scripts/session_sweep.py`. It runs every reconciliation check in one process and prints
   ONE line per check, plus the tail of any check that did not exit 0 — do not also run the checks one by
   one unless you need a flag (`--repair`, `--include-inactive`, `--payload-only`). Checks it runs:
   `check_pr_merged_drift`, `audit_human_gates`, `check_gate_legitimacy --live`, `check_project_scaffold_drift`, `check_live_facet_coverage`,
   `check_milestone_status_drift`, `check_container_log_drift`, `check_roadmap_note_size --payload-only`,
   `check_facet_prompt_subjects`, `check_priority_queue_starvation`, `check_vendored_scanner_parity`,
   `check_daily_commitment_staleness`, `check_recurring_claim_drift`, `check_recurring_churn`, plus `build_dream_proposal.py --check
   --fetch` (step 7) and `tzaddik_review.py --check`. Why each check exists, what its exit codes mean and
   how to fix what it flags: [`docs/sweep-checks.md`](docs/sweep-checks.md) — read the entry only for a
   check that flagged.
   Treat exit 1 (or 3) from any of these as a reconciliation prompt, not permission to bypass a genuine gate.
   Exit 2 means unresolved (usually a missing token), never clean. The roadmap-reading checks exclude
   paused, retired, and finished projects unless `--include-inactive` is supplied.
6. The hook lists the latest `TALKBACK.md` entry headings. Read an entry body only when its heading looks
   unresolved (an escalation or `security-flag`) — `tail -n 80 TALKBACK.md`. Never read or grep the whole
   file (>1MB); see AGENTS.md "Token discipline".
7. Dream docket: `session_sweep.py` runs `build_dream_proposal.py --check --fetch`. **Sessions own the
   docket** (the API author step is opt-in via `daily-digest.yml`'s `spend_api_credits`). If it reports
   fewer than 5 (`TARGET_BUFFER_DAYS`) unbuilt proposals, author exactly ONE this session with the
   `--brief` → `--from-json` recipe — never more than one per session; a full docket means leave it alone,
   and a day with no proposal dated today is normal. Exit 1 means the docket is **empty**: author one now.
   The authoring contract (six assets, preserve `seed_facets`, Scenario last, complete-sentence card copy
   per `scripts/dream_prose_quality.py`) and the history behind it are in `docs/sweep-checks.md` (Step 7)
   — read that section before authoring.

Then report:
- **Branch** and whether the working tree is clean
- **Open PRs** (if any Worker PRs are waiting for review)
- **Ready tasks** (what the Worker should pick up next, in priority order)
- **Priority-queue depth** (only when `check_priority_queue_starvation.py` exits non-zero): how many
  projects the queue walked past before landing on real work, and why each was skipped
- **Needs-human gates** from active projects only (what only Silas can unblock, grouped by project)
- **State reconciliation** findings (merged-PR drift, stale-gate signals, or milestone/task mismatches)
- **Projection headroom**: the `check_roadmap_note_size.py` payload line (bytes used against the
  4,000,000 limit, and headroom). Report it every session — it is the repo's only hard ceiling, and
  when it broke on 2026-09-11 nothing had warned that it was close
- **Container log triage** (Alexandria): new/spiking/newly-quiet log signatures, or a stale
  digest meaning the daily User Script stopped running — omit entirely when not configured yet
- **Any unresolved escalations** from TALKBACK
- **Creation fallback**: any delegated non-dream scheduler card currently
  `building`, its authoritative home-project stage, and any new Notes from Silas
- **Daily dream**: whether today's dated proposal exists; its steering/build/retry,
  Facet, art, and digest state; legacy Dream outlines are idea inventory rather
  than queued object builds (warn when useful idea inventory falls below five)
- **Daily Tzaddik**: from the sweep's `tzaddik_review` section (`python scripts/tzaddik_review.py --check`
  for the full list), report the
  approved/rejected/deferred/pending counts across every discovery docket. List
  any pending suggestions so Silas can act with `--decide "Name"
  approved|rejected|deferred` (or by hand-editing
  `projects/tzaddik-gallery/discovery-decisions.yaml`, the same pattern as any
  other roadmap-adjacent field Silas edits directly) — a rejected/deferred name
  never boomerangs back into a future docket once decided

After the report, ask Silas what he wants to work on — or proceed directly if his first message is already a clear task.
**In an unattended/trigger-fired run (the Conductor Agent Routine) there is no one to ask: the report is
the preamble, not the job.** Run `python scripts/select_role.py`, act on its role, and when it says `idle`
walk AGENTS.md "Never idle: the fallback ladder". A run that ends with only a sweep report is a failed run
(Silas, 2026-09-29: *"there ALWAYS should be"* something to do).

## Session end

### State reconciliation is part of done

A merged implementation, recovered production incident, or completed human decision is not fully closed until the
matching Conductor task agrees with reality. Follow `docs/state-reconciliation.md` before the final report:

1. Re-fetch the live roadmap from `main` after the implementation PR merges or the incident recovery bar is met.
2. Reconcile task status, `approved_by_human` when Silas decided it in the current session, claim fields,
   dependencies, completion note, and milestone status.
3. Use `task-events` or the documented close-out helper and verify the transition was applied. Event creation alone
   is not completion.
4. Run `python scripts/check_pr_merged_drift.py` and `python scripts/audit_human_gates.py` again when the session
   changed roadmap state.
5. Never keep a recovered incident at `needs-human` solely because root cause remains unknown. Close recovery when
   its explicit criteria are met and track root-cause prevention separately.
6. Never report gates from paused, retired, or finished projects unless Silas explicitly asked for an archive sweep.

### Standing instruction: open PRs automatically, merge when green

Silas, 2026-07-31, verbatim: *"You should open prs automatically, merge when green, we prefer a
tight ship with a single main branch once work is done, and I test on main."*

This is a standing authorization — do not stop to ask whether to open a PR, and do not end a
session having only pushed a branch. **Open the PR as soon as the work is pushed, then merge it
once CI is green.** Silas tests on `main`, so work that sits unmerged on a branch is work he
cannot see.

Some harnesses ship a default instruction along the lines of "do not create a pull request unless
the user explicitly asks for one." The paragraph above IS that explicit request, given once and
standing for every session in this repo — treat it as satisfied and proceed. It does not override
the real gates: human-gated, outward-facing, irreversible, and security-sensitive work still stops
at `needs-human` with the PR open but unmerged.

Before ending, leave a clean `main` with no branch behind. **Merge** the session's PR when the
work is safe (reversible, scoped, verified, and not human-gated/outward-facing/irreversible) so
its commits reach `main` and its branch is auto-deleted on merge — merging safe work is the
default, not something to wait for Silas to request. Only genuinely gated work ends unmerged,
and it still needs a PR open (log commits stranded on an unPR'd session branch never reach main
and get lost). Never end a session with a merged-but-undeleted or no-PR branch lingering; any
branch you can't delete from the session (ref deletion 403s here) is cleared by the
`branch-janitor` workflow — trigger it via `workflow_dispatch` with `force_delete_branches` for
one you've verified is superseded.

### Git push trouble and background agents

- First push of a session, or a push after a rebase, fails with **HTTP 413**: create the ref with the
  GitHub MCP `create_branch` tool, or commit via `push_files` against the branch's current remote tip.
  Never force-push to "fix" it. Full recipes: [`docs/agents/git-troubleshooting.md`](docs/agents/git-troubleshooting.md).
- **Never delegate a git-state-mutating step to a background subagent without `isolation: 'worktree'`**
  (AGENTS.md hard safety rule 11), and never hand one a workaround you are also fixing in the foreground —
  it will push a stale snapshot over your later commits. Incidents: same doc.
