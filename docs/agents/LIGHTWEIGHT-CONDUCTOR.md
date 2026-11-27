# Lightweight Conductor infrastructure

Owner direction (2026-11-26 PT): private single-user Git-native manager, no new API/service. Optimize coordination infrastructure before individual roadmaps. Preserve Git as authority, existing task events, CI, human gates and existing Kind Robots projection.

## Operating model

Machines detect, order and reconcile. Agents use one common contract and one role instruction per session, then retrieve just the selected project and task. Human direction lives in current project briefs; historical decisions are references, not startup reading.

Six assignment types: developer (build/fix PRs), reviewer (review/merge/close), content (authored material), art (submit/curate/attach), QA (tests and rendered assessment), daily creative (Dream/Dead Air/other scheduled creative outputs). Existing medic roles are exception routes, not additional mandatory reading. Keep existing role selector until a compatible dispatch layer is tested.

## Finite infrastructure rollout

1. Common contract: consolidate AGENTS/CLAUDE startup, preserve prior detailed manuals verbatim as optional references, stop automatic one-new-task-per-merge. Keep every safety rule and required PR heading. No project roadmap or lifecycle edit.
2. Current direction: separate current global and per-project directives from superseded history. Preserve old text byte-for-byte; verify effective current direction and all consumer scripts/tests before changing CONTROL format. No individual roadmap redesign here.
3. Git-native compact dispatch: extend existing STATUS pickup hints and selector, do not create a second scheduler. Generate bounded project/role/task candidates and per-task packets (source SHA, status, dependencies, gates, acceptance, relevant references, latest implementation receipts) from canonical YAML; never treat derived output as a claim. Use connector-readable committed views and local CLI equivalents. Verify source/ownership at mutation time. Do not add an API.
4. Maintenance separation: group deterministic sweeps by owner/cadence and surface exceptions only. Reconcile stale claims/dependencies with existing serialized writer; do not infer done from a merged partial PR. Keep verified receipts and retry safely. Avoid competing main writers and duplicate checks.
5. Pilot on four game finishers: record startup size/calls, time to first useful action, scoped PRs/merges/closures, failure rate and claim collisions. Target routine prep under 2k tokens, one role load/session, no unrelated roadmaps, no weakened gates. Measure rather than assume improvement.
6. Retire superseded instructions and scripts only after equivalent coverage is verified. Then separately redesign project roadmaps into compact outline, task specifications and history. No endless infrastructure expansion.

## Acceptance

Canonical state remains Git, generated output is read-only/advisory, task ownership remains atomic/session-aware, all relevant current-head CI must pass before merge, and human gates remain unchanged. A failed/stale projection cannot authorize mutation. Full prior instructions remain available; current contract and current user direction override superseded procedures. Keep implementation changes small, tested and independently mergeable. Do not create extra finite roadmap tasks merely to document these phases.

## Architecture at a glance (2026-11-26 PT)

This is a review map, not a new agent startup requirement. Review the actual implementation and distinguish merged behavior from open PRs. The private repo is the only project-management authority.

| Layer | Canonical or derived | Implementation |
| --- | --- | --- |
| Direction | canonical | CONTROL.md, project-overrides.yaml, projects/priority.yaml |
| Tasks | canonical | projects/<slug>/roadmap.yaml |
| Ownership and transitions | canonical | task-events/, scripts/claim_task.py, scripts/close_task.py, serialized Process task events |
| Dispatch | live/advisory | scripts/select_role.py, scripts/run_worker.py, STATUS.md |
| Scoped retrieval | derived | scripts/build_agent_context.py, ops/agent-context/<slug>.json, scripts/show_task.py, scripts/show_control.py |
| Instructions | canonical | AGENTS.md once, one relevant docs/agents/roles/ card; optional procedures on demand |
| Implementation and evidence | canonical in owning repo | worker branches, PRs, current-head CI, verified merge SHA |
| Presentation | derived coordination, separate runtime authority | existing Kind Robots projection (SOURCE_OF_TRUTH.md) |

Flow: owner direction + roadmap -> deterministic selection -> live claim -> scoped agent work -> review + CI -> merge -> task event -> reconciled main -> refreshed advisory views. Neither a locator nor a PR is a claim or proof of completion.

### Rollout evidence

- #8075 merged: shared contract and compact pickup hints; original instruction blobs archived, finite-scope review policy.
- #8077 merged: scope global/project direction and daily creative; preserve original CONTROL and runbook.
- #8078 merged (fa563ca): specialist cards and Git-native task locators. Real-repository CI generated 39 locators and found zero structural roadmap errors. The Deep Heart locator was subsequently retrieved from main.
- #8079 merged (40e148f): smaller SessionStart hook, single parsed queue snapshot and architecture review entrypoint. The owner merged while the full Worker PR CI was still running; check its final result before claiming green.
- This closeout increment aligns live selection with locator role/dependency rules and documents the [roadmap polishing procedure](../../projects/README.md). See PR/CI for verification.
- Remaining follow-up: independent architecture review, production throughput measurement, and evidence-based maintenance consolidation. These do not prevent starting individual roadmap polishing once the shared changes pass CI. No new scheduler or speculative rewrite.

### Questions for independent reviewers

Review from the perspective of a low-token personal project manager, not a multi-tenant platform. Prefer deleting/reusing over adding.

1. Which inputs must actually be read before the first useful action? Identify duplicated or irrelevant context, including scripts/hooks and injected prompts.
2. Are there competing authorities or writers, stale views, unsafe claim/merge races, or completion loopholes? Suggest the smallest repair preserving the current safeguards.
3. Which deterministic checks duplicate existing workflows? Which must remain live, and what triggers/cadence are needed for the rest?
4. Are six assignment types sufficient? Can specialist selection reuse the existing selector rather than creating a second dispatcher?
5. What would you remove, simplify, or test next? Rank concrete recommendations by token/latency impact, reliability, complexity and migration risk; cite exact paths or code. Distinguish observed defects from hypotheses.
6. Are acceptance metrics measurable from real sessions rather than inferred from file length? Propose a minimal benchmark and stop condition.

Do not propose additional services, public publication, project roadmap rewrites or new tasks by default. Read-only critique first; return concise findings with evidence, tradeoffs and a bounded change proposal.

## Maintenance ownership and next-stage boundary

| Responsibility | Existing owner | Agent involvement |
| --- | --- | --- |
| Claims, expiration, dependencies | serialized Process task events; live claim helper | verify own task and repair genuine failures |
| PRs, CI and branch state | GitHub checks, selector, branch janitor | inspect latest head; repair or review actionable exceptions |
| Structural roadmap audit | Roadmap Audit workflow | fix reported defects, don't repeat portfolio-wide audit for directed work |
| Art queue, receipts and recovery | existing art workflows and ops reports | evaluate actual media, resolve exceptions |
| Project/task snapshots | Refresh Status | read only; check live source before writes |
| Daily creative/digest | existing daily workflows and explicit creative assignments | author/evaluate/deliver, don't duplicate writers |
| Full diagnostic sweep | scripts/session_sweep.py | on demand; do not require all 26 checks per session |

Keep the existing diagnostic scripts until coverage and real run results justify deletion. A directed finisher starts with its own task, not a full portfolio audit. Independent critiques should be evaluated as finite follow-up proposals rather than blocking all roadmap work.
