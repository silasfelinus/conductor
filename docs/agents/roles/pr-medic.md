# Playbook: pr-medic

<!-- Moved verbatim out of AGENTS.md on 2026-09-30 (token essentialization) so sessions
only load it when their role or task needs it. AGENTS.md links here; rules in this file
carry the same authority as if they were still inline. -->

Read AGENTS.md (core) first; this playbook adds only what this role needs.

### If you're fixing PR errors

`select_role.py` recommended `pr-medic`: an open PR has CI that's both **red** and
**stale** (no push in the configured window despite failing) — a genuine orphaned
error, distinct from a PR mid-iteration whose latest push just hasn't gone green yet.

- For each PR in `red_stale_prs`: open it, read the actual failing check's logs (not
  just the red status), and diagnose the real cause — flaky/transient infra vs. a
  real regression vs. a pre-existing failure on the base branch the PR's diff didn't
  cause (check whether the base branch itself is also red before blaming the PR).
- **Fixable now:** push a commit that fixes it. Re-run/verify the check goes green.
  This follows the same "drive to green" discipline as the PR-activity CI-failure
  handling elsewhere in this manual — diagnose and push a fix, or reply explaining
  why not; never leave a red check silently unaddressed.
- **Base branch itself is broken** (the PR's own diff isn't the cause): say so once on
  the PR (which check, confirmed also red on base) rather than repeatedly re-diagnosing
  the same non-issue, and don't merge base into the PR until the base recovers.
- **Not actually fixable / needs a human call** (e.g. the fix requires a decision only
  Silas can make, or touches something outward-facing/irreversible): comment explaining
  the real blocker and leave the task at `status: needs-human` — do not force a merge
  past a red required check, and do not silently close the PR.
- **The PR is simply abandoned** (author/owner unclear, work superseded elsewhere,
  genuinely dead): don't unilaterally close someone else's PR — flag it in the
  project's `TALKBACK.md` with your read and, if the underlying task's roadmap status
  doesn't already reflect this, correct it (matching the same "roadmap state must
  reflect live reality" principle as `check_pr_merged_drift.py`).
- Cross-repo: `select_role.py` checks both conductor's and kind_robots' open PRs by
  default. If you have access to still other repos, check those too via GitHub MCP
  tools before concluding there's nothing to fix.
