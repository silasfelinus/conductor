# Hard safety rules — full text with incident history

> Moved verbatim from `AGENTS.md` on 2026-11-01 PT (token-essentialization pass 2). `AGENTS.md`
> keeps the condensed rule and links here; this file holds the full detail and the incident
> history behind it. If the two ever disagree, the rule in `AGENTS.md` wins — fix this file.
> Rule numbers are stable and referenced from TALKBACK; never renumber.

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
