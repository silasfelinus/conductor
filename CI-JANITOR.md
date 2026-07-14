# CI Janitor

CI Janitor is Conductor's incident-routing role for critical automated checks on repositories Silas owns.

## Operating contract

1. A scheduled workflow checks the latest completed run for each configured critical workflow.
2. A green, neutral, or skipped run produces no work.
3. A failed, timed-out, cancelled, stale, startup-failed, or action-required run creates one deduplicated HIGH-priority Kind Robots Todo.
4. Todos already outrank roadmap tasks in `AGENTS.md`, so the next Worker cycle handles the incident before ordinary project selection.
5. The Todo points to the exact source run and tells the Worker to inspect logs and artifacts, identify the shared root cause, repair the affected repository, and verify the relevant check.
6. The Worker must not delete, skip, weaken, or blanket-retry legitimate tests merely to manufacture a green badge.

## Scope

The initial monitored workflow is:

- `silasfelinus/kind_robots` → `.github/workflows/cypress.yml` on `main`

Additional workflows can be supplied through `CI_JANITOR_CHECKS_JSON` as an array of objects with `repository`, `workflow`, `branch`, and optional `label` fields.

## Deduplication

Every generated Todo includes a stable marker:

```text
ci-janitor:<owner/repository>:<workflow-file>:<workflow-run-id>
```

The watcher searches all existing Todos for that marker before creating work. A persistent red run therefore creates one incident, not an hourly flock of identical robot firefighters.

## Credentials and boundaries

- `GITHUB_TOKEN` reads public GitHub Actions metadata.
- `KR_API_TOKEN` creates the internal Todo through the existing Kind Robots API.
- The watcher cannot merge, deploy, modify secrets, alter branch protection, or change production data.
- Auth, secret rotation, billing, DNS, destructive data repair, and other hard gates remain human-controlled.
- If `KR_API_TOKEN` is missing or rejected, the workflow fails visibly instead of silently pretending incident routing succeeded.

## Source files

- `.github/workflows/ci-janitor.yml`
- `scripts/ci_janitor.py`
- `tests/test_ci_janitor.py`
