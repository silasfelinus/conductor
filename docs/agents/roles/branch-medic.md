# Playbook: branch-medic

<!-- Moved verbatim out of AGENTS.md on 2026-09-30 (token essentialization) so sessions
only load it when their role or task needs it. AGENTS.md links here; rules in this file
carry the same authority as if they were still inline. -->

Read AGENTS.md (core) first; this playbook adds only what this role needs.

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
