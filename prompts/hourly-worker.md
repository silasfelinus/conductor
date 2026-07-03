# Hourly maintenance runbook

Use this runbook to keep scheduled conductor maintenance cycles productive without weakening project gates.

## Goals

- Finish one narrow, reversible unit of work per cycle whenever safe.
- Avoid spending a whole cycle on missing optional credentials, unavailable local runtimes, stale generated files, or other soft blockers.
- Preserve every human gate for content, proposal, outward-facing, irreversible, security-sensitive, production-data, deployment, secrets, billing, DNS, or publish/send work.
- Leave clear notes so the next cycle or Silas knows exactly what happened.

## Startup checklist

Read these files before selecting work:

1. `AGENTS.md`
2. `CONTROL.md`
3. `project-overrides.yaml`
4. `projects/priority.yaml`
5. The selected project's `roadmap.yaml`
6. The selected project's `TALKBACK.md`, if present

`CONTROL.md` overrides roadmap direction. `project-overrides.yaml` decides whether a project is active.

## Productive cycle behavior

1. Check todos with `python scripts/fetch_todos.py`.
   - Handle the highest-priority OPEN todo first when the script and token are available.
   - If the token or service is unavailable, record the limitation and continue to roadmap work.

2. Resolve dependencies with `python scripts/resolve_deps.py`.
   - If local execution is unavailable, inspect dependencies directly from roadmap files.
   - Never claim `waiting` tasks.

3. Select the highest-priority safe `ready` task from active projects.
   - Hard human gates stop unsafe work.
   - Soft blockers should be documented, then task selection should continue if other safe work exists.

4. Keep the implementation small.
   - Change only the files required by the task.
   - Prefer complete, reversible increments over broad partial rewrites.
   - Turn unrelated findings into a future task or kaizen note instead of expanding the diff.

5. Verify with the tools that exist.
   - Run tests or scripts when possible.
   - When local execution is unavailable, verify by reading the changed files and comparing the branch diff.
   - State verification limits plainly.

6. Handle generated-file noise pragmatically.
   - `STATUS.md` and `workspace.html` are generated outputs.
   - Do not hand-edit them for content.
   - If they create merge noise, accept the newest generated/main copy and keep moving.

7. Write useful handoff notes.
   - Name the task or todo.
   - List changed files.
   - Say what was verified.
   - Explain any human action needed with exact file/task edits.

## Soft blocker examples

Continue to another safe task after documenting:

- Missing optional API token.
- Local runtime unavailable, but the work can be statically checked.
- Branch deletion unavailable through the connector.
- A task is unclear but does not block unrelated ready work.

## Hard stop examples

Stop and ask for Silas action when work would require:

- Setting `approved_by_human: true`.
- Publishing, sending, deploying, or changing DNS/billing/secrets.
- Touching production data.
- Destructive database operations.
- Skipping a `gate_human: true` dependency.

## Final report template

- Task handled:
- Result:
- Files changed:
- Verification:
- Blockers or follow-up:
