# Conductor agent contract

Conductor is Silas's private project manager. Git is canonical; scripts and workflows coordinate; agents deliver work. Read this contract once per session, then load only the assigned role and task. Current user direction and CONTROL.md govern intent; never bypass safety.

## Pick work, not paperwork

- Honor a direct assignment. Otherwise use Todos first (`scripts/fetch_todos.py`; missing token: continue), then `scripts/select_role.py`. Connector-only: use open PRs and generated STATUS.md pickup hints, not a portfolio-wide roadmap scan.
- Read current global direction once and only the selected project's CONTROL block (`scripts/show_control.py`), lifecycle/priority and relevant live task (`scripts/show_task.py`). Connector agents use [task locators](docs/agents/agent-context.md) for exact source ranges. Never load unrelated roadmaps or full history. Snapshots are advisory.
- Work active projects first; playtest/continuous are fallback. Paused/retired/finished and member projects obey [lifecycle rules](docs/agents/picking-work.md).
- Choose an unblocked, non-resting ready task; respect dependencies, umbrella delegates and human approvals. Verify live ownership. One active claim per worker. Use collision-resistant sessions, `scripts/claim_task.py` or [connector task-events](docs/github-connector-worker.md). Expired claims are reconciled by the serialized workflow (90 minutes); diagnose failures instead of repeating the scan.
- Load one role playbook, relevant master-issue sections and target-repo instructions. Read additional references only when needed. If blocked, choose independent eligible work. Never end on inventory alone when work is available.

## Deliver and close

- Use worker/* branches, scoped changes and actual tests. Set and verify review before opening the implementation PR; use [handoff template](docs/agents/templates.md) and the CI-required headings below. Open PRs automatically; don't leave orphan branches.
- Reviewers check the [review claim](docs/agents/roles/reviewer.md) before acting. Fix red checks on the original branch; confirm every relevant latest-head check completed successfully. Merge reversible, scoped, ungated software using expected head SHA. Never force-push; preserve current main and independent work.
- While checks run, work on independent tasks; do not poll passively. After merge verify canonical transition (done only for full scope; ready for partial; rearm only for recurring), dependencies, projection and cleanup. Avoid duplicate events. Report actual evidence, pending work and genuine blockers.
- Keep task notes short, dated and linked; archive long notes verbatim with existing scripts. Append TALKBACK/LEARNING when required. Classify failures before spending retry passes (three quality/scope passes maximum); never silently override a challenge.
- Do not manufacture tasks after a merge. Add only a demonstrated defect, unmet original requirement or explicit user direction; optional ideas go to a nonblocking backlog. Finite games reach playtest/normal only when original build, art/text and QA are complete; flag and close their master issue then. Human playtesting and publication are separate.
- Software is PR-backed; content/proposal outputs are private drafts requiring approval before release. New user-facing software starts with an impressive designed front end, real content and queued original art. Use the Playbook Kit for new story games. Verify phone/tablet/desktop per current self-hosted procedure.

## Non-negotiable safeguards

1. PRs target main; only documented atomic claims and task-event writes are direct-to-main exceptions.
2. High-stakes drafts go to needs-human; never send/publish/deploy without explicit approval.
3. Only quality/scope failures consume passes; at three, block and record learning.
4. One active claim; verified review handoff permits independent work.
5. Never touch secrets, DNS, billing, accounts, irreversible actions or genuine human gates without authorization. Never infer human approval; record only explicit current-session approval through prescribed protocol.
6. Stay scoped; unrelated defects require separate work, not hidden diff expansion.
7. TALKBACK is append-only; only documented lossless archival is allowed.
8. Security flags require Silas's acknowledgement before further project work.
9. Generated STATUS/workspace/audit/learning reports resolve to main; preserve both sides of append-only logs. Never hand-edit generated views.
10. Never run destructive DB commands, including dev; preserve data and use authorized API writes.
11. No background git-mutating workaround for work being fixed in foreground.
12. Background agents mutating shared repos require isolated worktrees.
13. Pending delegated CI is a handoff, not a blocker; revisit completion and stop finished delegates.
14. Unraid secrets belong under the checkout's .secrets, never /mnt/user/pc.
15. Never inspect or print secret values, disable redaction or give commands that expose them; presence checks only.

Do not hand routine verification, merging or cleanup to Silas. Use Pacific time in human-facing reports, UTC ISO timestamps for machine state. Conductor owns coordination; Kind Robots owns runtime/presentation. No second authority.

## Load on demand

| Need | Reference |
| --- | --- |
| Task selection, lifecycle, claims | [Picking work](docs/agents/picking-work.md), [connector protocol](docs/github-connector-worker.md) |
| Roles and fallback | [Role assignment](docs/agents/role-assignment.md), [worker](docs/agents/roles/worker.md), [other role playbooks](docs/agents/roles/) |
| CI and parallel work | [Continuous production](docs/agents/continuous-production-pipeline.md), [Git troubleshooting](docs/agents/git-troubleshooting.md) |
| Gates and security | [Human gates](docs/agents/human-gates.md), [safety details](docs/agents/safety-rules-detail.md), [cross-repo](docs/agents/cross-repo.md) |
| Master issue and UI | [Issue index](docs/agents/master-issues.yaml), [issue context](docs/agents/project-issue-context.md), [frontend verification](docs/agents/frontend-verification.md) |
| Art and daily creative | [Project art](docs/agents/project-art.md), [daily rituals](docs/agents/daily-rituals.md) |
| Reconciliation and review | [State reconciliation](docs/state-reconciliation.md), [sweep checks](docs/sweep-checks.md), [cross-vetting](docs/agents/cross-vetting.md), [failure triage](docs/agents/failure-triage.md) |
| Full prior procedural detail | [Reference manual](docs/agents/reference-manual-2026-11-26.md) (not startup reading; current contract wins) |
| Source ownership | [SOURCE_OF_TRUTH.md](SOURCE_OF_TRUTH.md) |
| Infrastructure simplification | [Lightweight Conductor plan](docs/agents/LIGHTWEIGHT-CONDUCTOR.md) |

## Worker PR handoff

### Task
### What changed / what I produced
### How I verified
### Stakes
### Kaizen suggestion
Optional idea or "None"; not an instruction to create a task.
### Notes for reviewer

Use optional ### Flags for Reviewer for uncertainties. Report scope, tests actually run, PR/SHA, CI/merge/deploy state, task and ArtJob IDs as relevant. Keep historical detail in the relevant reference, not in this contract.
