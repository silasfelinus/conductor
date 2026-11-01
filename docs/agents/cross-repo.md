# Cross-repo work, secrets handling and branch hygiene

> Moved verbatim from `AGENTS.md` on 2026-11-01 PT (token-essentialization pass 2). `AGENTS.md`
> keeps the condensed rule and links here; this file holds the full detail and the incident
> history behind it. If the two ever disagree, the rule in `AGENTS.md` wins — fix this file.
> Read before any kind_robots (or other target-repo) task, any secret-shaped probe, or a rescue PR.

### Cross-repo tasks

Some roadmap tasks describe changes in another Silas-owned repository, such as `kind_robots`,
`serendipity-voice`, or `portos`. The conductor roadmap still owns the task state, but the
code patch belongs in the target repository.

To verify kind_robots changes locally (vue-tsc / eslint) in an ephemeral sandbox, run
`source scripts/provision_kind_robots_deps.sh` — it installs node_modules + the Prisma
client with the two required workarounds (CYPRESS_INSTALL_BINARY=0 and a dummy
DATABASE_URL) baked in, instead of every session re-deriving them (conductor/t-046).

**Check for a stranded implementation branch before reimplementing a `ready` task.** A
`create_pull_request` connector failure can leave a target-repo branch fully implemented
and pushed with no PR ever opened, while the conductor task sits at `status: ready`
describing the blocker in its own `note:` (kind-robots/t-120's kaizen id-collision rescue
and t-122 both hit this within two days, 2026-09-24/26). Before claiming and reimplementing
such a task, check the task's `note:` for a referenced branch/commit, or list the target
repo's branches for a `worker/<project>-<task-id>-*` match. If one exists and its diff looks
complete against the task description, open the PR from it as-is rather than reimplementing
— but do not treat the stranded branch's own prior local verification as sufficient to merge.
Run full CI on it first: t-122's branch passed its author's one purpose-built verifier
locally, but a full CI run caught a real regression in a *different* file that pinned the
same string the change had renamed, which the original author's narrower local check never
touched. A stranded branch is safe to reuse; skipping CI on it is not.

Several scripts here (`fetch_todos.py`, admin-gated kind_robots API calls, etc.) need
`KR_API_TOKEN` in the environment. To check whether it's set **without ever printing the
value itself**, run `scripts/kr_token_set.sh` (or `source` it) rather than hand-typing a
probe: `${VAR:-no}` looks like a safe fallback but actually substitutes the live value
once the variable is set, so a hand-rolled check can leak the token straight into a
session's own tool-output transcript (root `TALKBACK.md`, 2026-08-12 and 2026-08-13, two
independent sessions hit exactly this — conductor/t-116; a **third** independent
recurrence, 2026-08-24, is logged in root `TALKBACK.md` and conductor/t-128 — that session
had just finished reading this exact warning and reproduced it anyway seconds later in an
unrelated ad hoc diagnostic one-liner, so treat "I already know the rule" as insufficient:
literally never type `${SOME_SECRET_VAR:-...}` by hand for any secret-shaped variable, not
just `KR_API_TOKEN`, not even in a quick debugging aside — always route through `-n`/`-z`
or a script like this one). Relatedly: in this sandbox, shell environment variables do
**not** persist between separate Bash tool invocations (each call starts a fresh shell
from profile) — `source scripts/kr_token_set.sh` in one call has no effect on a later
call's environment, so check presence in the *same* invocation that uses the token, not a
prior one.

**Secrets are guarded by hooks now, because remembering the rule has failed five times.**
(2026-09-27, after a Python `print(getattr(module, "KR_API_TOKEN", "NOATTR"))` diagnostic
printed the live token — a shape no shell rule could cover. Silas: *"The risks of training
data leaking my personal hobby project's admin key is not worth excessive hassle."*) Two
PreToolUse hooks in `.claude/settings.json`, mirrored to `~/.claude/` by
`scripts/install_secret_hooks.py` so sessions rooted outside this repo get them too:
- `.claude/hooks/block_secret_dump.py` refuses the command shapes that have leaked before,
  and Read/Grep of a live `.env`.
- `.claude/hooks/redact_bash_output.py` wraps every Bash command so its stdout and stderr
  pass through a filter that replaces the literal value of every secret-shaped env var
  (and every secret-shaped line in the project's dotenv files) with `[REDACTED:NAME]`.
  This is the layer that does not depend on anyone predicting the next shape.

What that means for you:
- **Never inspect a secret's value, in any language, for any reason** — not to print it,
  not a prefix, not its length next to its value, not a hash, not "just to confirm it
  resolved". Presence only: shell `[ -n "$X" ]` or `scripts/kr_token_set.sh`; Python
  `bool(os.environ.get("X"))` or `hasattr(module, "X")`. To learn whether a token *works*,
  make the authenticated call and report only the HTTP status.
- **Never set `CONDUCTOR_REDACT_OUTPUT=0`** or otherwise route around either hook. The kill
  switch exists for Silas debugging the hook itself, not for agents.
- **If `[REDACTED:<NAME>]` shows up in your output, the redactor caught a leak.** Stop that
  line of investigation and do not try to reveal what was masked. Log a root-TALKBACK
  `security-flag` entry naming the command shape and stating that the value did **not**
  reach the transcript — so **no rotation is needed**. Say that explicitly; an entry that
  leaves it ambiguous costs Silas a rotation for nothing.
- **If a value genuinely reached the transcript anyway** (the hooks weren't loaded, or a
  non-Bash tool printed it), append to the ONE open `FOR SILAS: rotate KR_API_TOKEN`
  conductor task instead of filing another, link kind_robots
  `docs/runbooks/admin-token-rotation.md`, and fix the hook so that shape is masked next
  time — that fix is the deliverable, a TALKBACK apology is not.

**Visually verifying a front-end change** (kind_robots is self-hosted at `kindrobots.org`, not
Vercel; no PR previews, no auto-deploy-on-merge; a UI change does not merge on structural CI
alone): read [`docs/agents/frontend-verification.md`](docs/agents/frontend-verification.md)
before verifying or merging any kind_robots UI change.

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
