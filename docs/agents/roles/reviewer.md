# Playbook: reviewer

<!-- Moved verbatim out of AGENTS.md on 2026-09-30 (token essentialization) so sessions
only load it when their role or task needs it. AGENTS.md links here; rules in this file
carry the same authority as if they were still inline. -->

Read AGENTS.md (core) first; this playbook adds only what this role needs.

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


### Review-claim markers (moved from AGENTS.md "Picking what to work on") — avoiding duplicate review work

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
