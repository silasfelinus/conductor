# CLAUDE.md

The operating manual for this repo is **[AGENTS.md](./AGENTS.md)** — read it in full at the start of every session. It applies to all agents (Worker and Reviewer) across all projects.

## Session startup

At the start of every session, before responding to any task, run a conductor sweep and report it to Silas:

1. Read `AGENTS.md` in full
2. Run `git status` and `git log --oneline -5`
3. Check for open PRs (use GitHub MCP tools if available)
4. Scan all `projects/*/roadmap.yaml` for tasks with `status: ready`, `status: needs-human`, or `status: claimed` —
   **first check `project-overrides.yaml` and skip any project whose `status` there is not `active`** (`paused`,
   `retired`, `finished`). Several projects (career-transition, pinball-hero, recipe-box, mermaids-of-venice,
   others) are deliberately tabled/closed there; a scan that reads `roadmap.yaml` directly without cross-checking
   this file resurfaces their stale tasks every session regardless (2026-07-25 — this exact bug surfaced
   career-transition/t-003 and pinball-hero/t-002 as live "needs-human" items after both had been `retired` for
   over a week). Before proposing a new project-status value to fix a "closed project keeps coming up" complaint,
   confirm the project isn't already correctly marked in `project-overrides.yaml` and simply not being checked.
5. Read `docs/state-reconciliation.md`, then run:
   - `python scripts/check_pr_merged_drift.py`
   - `python scripts/audit_human_gates.py`
   Treat exit 1 from either command as a reconciliation prompt, not permission to bypass a genuine gate. Both
   commands intentionally exclude paused, retired, and finished projects unless `--include-inactive` is supplied.
6. Check `TALKBACK.md` tail for any unresolved escalations or security flags
7. Run `python scripts/build_dream_proposal.py --check --fetch`. **This is now a
   backstop, not the primary path.** `daily-digest.yml` authors the day's proposal
   automatically in the step after the email goes out
   (`scripts/author_dream_proposal.py`), so on a normal day `--check` passes and
   there is nothing to do (Silas, 2026-08-09: *"I'm not sure why the next dreams
   aren't written the turn the digest is sent, or a step later if there isn't
   enough process. As progress goes, that's very high on automated tasks."*).

   If a proposal IS missing — the digest run failed, the model hiccuped, or it is
   a date the cron never covered — author it yourself, exactly as before: run
   `--brief` for the deterministic seed plan, then create exactly one dream vibe,
   one dream location, one Character, one ITEM Reward, one SKILL Reward, and one
   Scenario, with no narrator. Preserve the brief's `seed_facets` unchanged; the
   vibe is the umbrella, every dependent asset must follow its assigned Facets,
   and the Scenario is authored last and explicitly names the vibe, location, and
   Character. Write it with `--from-json` and commit it with the session's log
   commits. A missing proposal two days running means the automated step is
   broken — check the `daily-digest` run's "Author tomorrow's daily dream" step
   rather than just papering over it by hand each session.

Then report:
- **Branch** and whether the working tree is clean
- **Open PRs** (if any Worker PRs are waiting for review)
- **Ready tasks** (what the Worker should pick up next, in priority order)
- **Needs-human gates** from active projects only (what only Silas can unblock, grouped by project)
- **State reconciliation** findings (merged-PR drift, stale-gate signals, or milestone/task mismatches)
- **Any unresolved escalations** from TALKBACK
- **Creation fallback**: any delegated non-dream scheduler card currently
  `building`, its authoritative home-project stage, and any new Notes from Silas
- **Daily dream**: whether today's dated proposal exists; its steering/build/retry,
  Facet, art, and digest state; legacy Dream outlines are idea inventory rather
  than queued object builds (warn when useful idea inventory falls below five)

After the report, ask Silas what he wants to work on — or proceed directly if his first message is already a clear task.

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

### First push of a session fails with HTTP 413

If `git push -u origin <your-branch>` fails with an HTTP 413 from the git-smart-HTTP
proxy on the *first* push of a session, and the branch has never had a PR opened from
it, the branch likely doesn't exist on the actual GitHub remote yet — even if your local
checkout's remote-tracking ref shows a SHA for it (that's stale/local-only knowledge).
`GIT_TRACE_CURL` will show the proxy attempting to send a full-history pack (matching
the whole `.git` size) instead of a small delta, apparently because a brand-new ref
needs a full pack rather than one computed relative to objects already reachable via
other refs (e.g. `main`).

Workaround: call the GitHub MCP `create_branch` tool (`owner`/`repo`/`branch`/
`from_branch: main`) first — this creates the ref instantly via the API with zero data
transfer, since it just points at a commit the remote already has. Then the normal
`git push` of your session's actual commits goes through as a small, fast delta.

### Later push in the same session also fails with HTTP 413 (after a rebase)

The same 413 can recur *after* the branch's first push already succeeded and its PR
merged, if you `git rebase origin/main` (or otherwise rewrite history) and then try a
force-push of new work on the same branch name (Silas, 2026-07-16, conductor/t-010
Bauhaus cycle: PR #592 merged cleanly, then a follow-up TALKBACK-only commit hit 413
on every retry — including a plain `git push`, a retry, and a `502` on one attempt —
even though the branch clearly still existed on the remote). Root cause suspected to
be the same "proxy wants a full pack, not a delta" behavior as the brand-new-ref case,
just triggered by a rewritten/diverged local history instead of a genuinely new ref.

Workaround: skip `git push` for that one commit and use the GitHub MCP `push_files`
tool instead, targeting the branch's *current remote tip* (do not rebase locally
first) — it commits via the REST API with zero pack-transfer, so the 413 doesn't
apply. Do not force-push to "fix" this. A PR opened from the resulting branch may
show a larger diff than expected if `main` already has equivalent content under a
different commit SHA (e.g. from an earlier squash merge) — GitHub's merge-base
detection may or may not collapse this back to the true incremental diff, so check
`additions`/`changed_files` on the created PR before assuming it duplicated
already-merged work; if it looks right (matches only your new commit's actual
diff), it's safe to merge as normal.

### Don't delegate an in-flight git workaround to a background subagent

If you dispatch a background subagent to run the `push_files` (or any other
git-state-mutating) workaround above, and then — before it returns — resolve the
same push in the foreground by a different route (e.g. `create_branch` + rebase +
`git push`), the background subagent has no way to learn its task was superseded.
It will still finish, using the file content it was handed at dispatch time, and
push that stale snapshot on top of whatever the foreground already landed —
silently reverting any commits the foreground made after dispatching it. This is a
real write race, not just wasted work: it can clobber later commits even within a
single session with no other human or agent involved (observed 2026-07-18,
conductor/t-066: a foreground `status: review → done` flip plus a completion note
were dropped this way; caught via the task-completion notification and reapplied,
so no permanent loss, but it cost an extra round-trip and could easily go
unnoticed for a subagent whose output isn't re-read afterward).

Rule: never delegate a git-state-mutating workaround (`push_files`, `create_branch`,
force-push, etc.) to a background subagent for a problem you are actively fixing
inline. Background delegation is for genuinely independent work — if you're already
solving it in the foreground, either wait for the subagent's result before doing
anything else to that branch, or cancel/ignore its eventual output once your
foreground fix lands. If delegation is truly unavoidable, have the subagent re-fetch
and diff against the *current* remote tip immediately before it pushes (not just use
the content it was handed at dispatch time), so a stale call fails loudly on an
unexpected base instead of silently overwriting newer commits.

**This generalizes beyond the workaround case above.** Two independent incidents within
24 hours (TALKBACK.md 2026-08-13 and 2026-08-14) showed the same root cause reaching
further than "in-flight workaround" scenarios: a non-isolated background Agent (no
`isolation: 'worktree'`) doing ANY git-mutating work (`claim_task.py`,
`set_task_field.py`, `close_task.py`, plain `git commit`/`push`) in the same working
directory as an active foreground session can silently discard that session's state.
2026-08-13 lost an uncommitted file edit; 2026-08-14 deleted the foreground session's
own designated git branch outright (recovered via `mcp__github__create_branch`, but a
session with unpushed local commits on that branch at dispatch time would have lost
them for real). See AGENTS.md hard safety rule 11 for the standing rule this promotes
to: `isolation: 'worktree'` is REQUIRED, not optional, for any background Agent that
will run git-mutating commands in a repo a foreground session is still actively (even
passively, mid-edit) using — not only for the narrower in-flight-workaround case above.