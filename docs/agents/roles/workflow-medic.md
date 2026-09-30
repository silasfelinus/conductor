# Playbook: workflow-medic

<!-- Moved verbatim out of AGENTS.md on 2026-09-30 (token essentialization) so sessions
only load it when their role or task needs it. AGENTS.md links here; rules in this file
carry the same authority as if they were still inline. -->

Read AGENTS.md (core) first; this playbook adds only what this role needs.

### If you're fixing a failing scheduled workflow

`select_role.py` recommended `workflow-medic`: a watched scheduled workflow
(default `process-task-events.yml`) has failed `--workflow-fail-threshold` (default
3) or more completed runs in a row, with nothing else having noticed.

- Read the most recent failing run's job logs directly (`get_job_logs` with
  `failed_only`, generous `tail_lines` — the default truncates before the real
  error on some jobs, a documented recurring gap). Diagnose the actual cause, not
  just "it's red": a malformed `task-events/*.yaml` entry, a real code regression in
  the workflow's own script, transient infra, or a downstream dependency (API rate
  limit, a repo it reads from being unreachable).
- **Fixable now:** push the fix (a corrected/quarantined malformed input, a script
  bug fix, a workflow-file correction) and re-run the workflow (`actions_run_trigger`
  if it supports `workflow_dispatch`, or wait for its next scheduled tick) to confirm
  it actually goes green — don't close this out on a plausible-looking diff alone,
  same discipline as every other fix-then-verify role here.
- **Malformed input from elsewhere** (e.g. a `task-events/*.yaml` entry another
  session queued incorrectly): fix or quarantine the bad entry rather than patching
  around it in the processor, unless the processor's own validation gap is the real
  root cause (in which case fix both — tighten validation so the next bad entry fails
  at PR time via `validate_task_events.py`, per conductor/t-103's precedent).
- **Not fixable from this session** (needs credentials/access this sandbox lacks, or
  a decision only Silas can make): leave a clear note on the affected roadmap task
  (or open one if none exists yet) at `status: needs-human` with `soft_gate: true` if
  other work can still proceed in parallel, and move on to the next role/task rather
  than stalling the whole session on it.
- This check only watches conductor-repo scheduled workflows by default (see the
  scope note above) — it does not replace reading `TALKBACK.md`/`RENDER-BACKLOG.md`
  for kind_robots-side incidents surfaced other ways.
