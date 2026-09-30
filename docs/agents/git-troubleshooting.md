# Git push troubleshooting and background-agent safety

<!-- Moved verbatim out of CLAUDE.md on 2026-09-30 (token essentialization): CLAUDE.md is
auto-loaded into every session, so rationale and incident history live here and are read
only when a check fires or the situation comes up. Same authority as if still inline. -->

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