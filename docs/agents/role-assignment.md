# Role assignment, the never-idle ladder and role playbooks

> Moved verbatim from `AGENTS.md` on 2026-11-01 PT (token-essentialization pass 2). `AGENTS.md`
> keeps the condensed rule and links here; this file holds the full detail and the incident
> history behind it. If the two ever disagree, the rule in `AGENTS.md` wins — fix this file.
> Read when `select_role.py` returns a role you have not run before, or `idle`.

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
   - **`role: roadmap-intent-auditor`** — the portfolio semantic review is
     within a day of its three-day deadline, or overdue. The six-hour
     Conductor Oversight GitHub workflow flags this early without a personal
     ChatGPT routine; `select_role.py` independently checks the report date
     and assigns this role before ordinary backlog work. Read
     `projects/conductor/OVERSIGHT-AGENT.md` and produce a genuine evidence-
     backed review, not a new date with no judgment. Do not email Silas for
     calendar staleness alone.
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
   may now recommend `workflow-medic`, `pr-medic`, `art-medic`, `branch-medic`, `roadmap-intent-auditor`, `site-auditor`,
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
| `role: roadmap-intent-auditor` | [`projects/conductor/OVERSIGHT-AGENT.md`](projects/conductor/OVERSIGHT-AGENT.md) |
| `role: site-auditor` | [`docs/agents/roles/site-auditor.md`](docs/agents/roles/site-auditor.md) |
| `idle` | "Never idle: the fallback ladder" above (no separate file) |
