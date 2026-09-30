# Playbook: site-auditor

<!-- Moved verbatim out of AGENTS.md on 2026-09-30 (token essentialization) so sessions
only load it when their role or task needs it. AGENTS.md links here; rules in this file
carry the same authority as if they were still inline. -->

Read AGENTS.md (core) first; this playbook adds only what this role needs.

### If you're doing the weekly site audit

`select_role.py` recommended `site-auditor`: the weekly gap-audit is overdue (never
run, or `--audit-stale-days` old or older). This role folds
`projects/global-ui/SITE-AUDIT-AGENT.md`'s originally-planned dedicated Claude Code
Remote Trigger into the same self-assigning system every other role uses (Silas,
2026-07-26: "we have a weekly review job, can we add that as a role as well?") — it
no longer needs its own separately-approved platform trigger; it rides whichever
trigger fires next, as long as `select_role.py` runs first and nothing higher-priority
is pending.

- Read `projects/global-ui/SITE-AUDIT-AGENT.md` in full and follow its **Agent
  Prompt** section verbatim — that spec is authoritative for scope/boundaries, not a
  paraphrase here. In short: cross-reference every active project's roadmap
  vocabulary (API routes, Vue components, Pinia stores, schema models it mentions)
  against what actually exists in `/home/user/kind_robots/`, using Glob/Grep — never
  call the live site.
- Write findings as a report to `projects/global-ui/AUDIT-REPORT-<YYYY-MM-DD>.md`
  (today's date, matching `select_role.py`'s `AUDIT_REPORT_RE` filename contract
  exactly — a differently-named file won't be recognized as satisfying this week's
  audit, and the role will keep recommending itself next time).
- Propose **up to 3** small, reversible follow-up tasks from the most impactful
  gaps found — new `ready` tasks in the relevant `roadmap.yaml` files, `stakes:
  reversible`, `owner: null`. This is a read-and-report run: roadmap task additions
  are the only writes permitted besides the report itself and opening the PR.
- Never modify a task marked `gate_human: true` without human review, never run
  npm/pnpm builds, never push directly to `main` — one PR per run, same as any other
  software-kind task, title `audit(site): weekly gap report YYYY-MM-DD`.
- If `select_role.py` reports `site_audit_overdue` but you can't complete a full
  audit this cycle (e.g. genuinely out of session budget), it's fine to leave it for
  the next session that self-assigns this role — don't write a partial or empty
  report just to stop the recommendation from firing; an honest "still overdue" is
  better than a hollow report that silently lowers the bar for what counts as done.
