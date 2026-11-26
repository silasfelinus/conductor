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
