# Auditor Duties

The Auditor is a studio duty that any connected LLM may perform. It is not a privileged model identity and does not replace Builders or Reviewers.

## Mission

Keep Conductor’s portfolio truthful, selectable, minimally gated, and resistant to repeated process mistakes.

The Auditor inspects; it does not casually rewrite product direction. Deterministic structural repairs may be proposed or applied through ordinary reversible PRs. Product decisions and hard-gate removals remain visible to Silas.

## Required inputs

Read in this order:

1. `CONTROL.md`
2. `AGENTS.md`
3. `STATUS.md`
4. `project-overrides.yaml`
5. `projects/priority.yaml`
6. every active `projects/<slug>/roadmap.yaml`
7. `LEARNING.yaml`, TALKBACK files, and relevant merged PR/code evidence when determining whether work is obsolete or complete

Run:

```bash
python scripts/resolve_deps.py --dry-run
python scripts/audit_roadmaps.py
```

## Audit categories

### Structural integrity

- YAML parses and expected top-level fields exist.
- Every active project appears exactly once in priority order.
- CONTROL’s current priority band matches `projects/priority.yaml`.
- `dream-cycle` remains last.
- Task IDs are unique and dependencies reference real IDs.
- Multi-dependency values use YAML lists, never comma-separated strings.
- Dependency graphs contain no cycles or self-dependencies.
- `ready` tasks have satisfied dependencies; `waiting` tasks do not remain waiting after dependencies are satisfied.

### State truth

- Claimed/review tasks have owner and timestamp.
- Stale in-progress work is reconciled with branches and PRs.
- Notes claiming “done,” “merged,” “superseded,” or “already exists” match task status.
- Shipped code, merged PRs, and roadmap state agree.
- Inactive projects with ready tasks are identified as harmless queue noise.
- Active projects with all work done are marked finished or given an explicit recurring maintenance task.

### Human gates

Classify every `needs-human` task as hard or soft.

Hard gates include concrete publishing, spend, billing, production deployment, DNS, secrets, destructive data changes, legal/licensing decisions, security acknowledgements, and irreversible outward actions.

Soft gates include uncertainty, missing verification, tool access, ordinary architecture ambiguity, reversible review, and scope confirmation on new projects. Intentional soft checkpoints use `soft_gate: true`; this records that the state is deliberate without pretending it is a hard approval boundary. Completed, approved historical gates are provenance and should not be flagged as current throughput problems.

The Auditor may recommend returning a soft-gated task to `ready`, splitting a hard outward action from reversible preparation, or improving the `FOR SILAS` note. It must not remove a genuine safety boundary merely to improve throughput.

### Scope and decomposition

- Identify tasks that combine architecture, implementation, deployment, publication, and verification.
- Split work so reversible preparation can proceed independently of hard-gated execution.
- Detect duplicate tasks and projects implementing the same source of truth.
- Mark superseded specification tasks as closed by implementation when executable reality is stronger evidence.
- Convert endless improvement milestones into explicit recurring tasks.

### Portfolio usefulness

- Check whether a project’s goal still matches CONTROL and current code reality.
- Identify nearly complete projects that need one integrated user test rather than more isolated features.
- Identify projects that need source material, pricing, product decisions, or other uniquely human input.
- Recommend pause/finish/merge decisions for low-value or redundant projects.

## Output

The Auditor produces:

- `ROADMAP-AUDIT.md` — readable portfolio report;
- `ROADMAP-AUDIT.json` — machine-readable findings with stable codes;
- a prioritized repair plan divided into:
  - deterministic framework repairs;
  - safe roadmap cleanup;
  - Silas decisions;
  - worker-ready execution;
- recurring-problem counts and recommended prevention mechanisms.

## Stable finding codes

Finding codes are a compatibility surface. Prefer adding a code over changing an existing code’s meaning.

Examples:

- `CONTROL_PRIORITY_DRIFT`
- `ACTIVE_MISSING_PRIORITY`
- `MALFORMED_DEPENDENCY_LIST`
- `MISSING_DEPENDENCY`
- `DEPENDENCY_CYCLE`
- `WAITING_WITH_SATISFIED_DEPS`
- `READY_WITH_UNMET_DEPS`
- `STALE_IN_PROGRESS`
- `SOFT_NEEDS_HUMAN`
- `POSSIBLY_UNNECESSARY_GATE`
- `ACTIVE_PROJECT_ALL_DONE`

Repeated codes should become schema validation, CI, helper scripts, or templates rather than recurring prose reminders.

## Repair authority

The Auditor may autonomously open reversible PRs that:

- normalize malformed metadata without changing intent;
- repair dependency syntax when the intended IDs are unambiguous;
- run the canonical resolver;
- align priority with explicit CONTROL direction;
- improve task notes and `FOR SILAS` actionability;
- add tests, schemas, lint rules, reports, and documentation;
- retire stale claims only after branch/PR evidence proves no live work will be lost.

The Auditor escalates rather than decides when the repair would:

- remove a hard gate;
- choose between product directions;
- publish, deploy, spend, send, delete, or expose data;
- retire a project whose value is unclear;
- reinterpret Silas’s creative intent.

## Cadence

- Structural audit on every roadmap-changing PR.
- Full portfolio report daily or after a major steering session.
- Focused audit after repeated selection failures, stale queues, or dependency anomalies.
- Monthly lifecycle review: finish, pause, merge, or explicitly renew active projects.

## Success metrics

- zero structural errors on main;
- no task waits after dependencies are satisfied;
- no ready task has unmet dependencies;
- stale claim count trends toward zero;
- hard/soft gate distinction is explicit and actionable;
- repeated finding codes decline after prevention is implemented;
- Silas spends focused time on decisions and integrated experience, not metadata repair.