# Site Audit Agent — Spec

Generated: 2026-06-30
Task: global-ui/t-009

---

## Purpose

A recurring agent that periodically compares the active conductor roadmap vocabulary against the actual Kind Robots frontend/backend, identifies gaps, and proposes small reversible follow-up tasks. Runs weekly. Does NOT rewrite roadmaps or make broad automatic changes.

---

## Schedule

**Interval:** Weekly (every Monday at 09:00 UTC).
**Trigger:** Claude Code Remote cron trigger → fires into the conductor session.

Cron expression: `0 9 * * 1`

---

## Agent Prompt (fires into conductor session)

```
SITE AUDIT — weekly check

You are running the weekly Kind Robots site audit. Read and follow:

1. Read /home/user/conductor/projects/*/roadmap.yaml for all active projects.
2. For each active project, check whether the key surfaces mentioned in the roadmap
   (API routes, Vue components, Pinia stores, schema models) actually exist in
   /home/user/kind_robots/. Use Glob and Grep — do NOT call the live site.
3. For each gap (roadmap mentions X but it doesn't exist in the codebase), write
   a one-line finding: [project] surface "X" — mentioned in roadmap, not found in code.
4. For each orphan (exists in code but no corresponding roadmap task), note it briefly.
5. Propose UP TO 3 small reversible follow-up tasks (one sentence each) based on the
   most impactful gaps. Write them as new `ready` tasks in the relevant roadmap.yaml
   files (stakes: reversible, owner: null).
6. Write a brief audit report to projects/global-ui/AUDIT-REPORT-<YYYY-MM-DD>.md.
7. Do NOT call live URLs, deploy anything, post externally, or modify tasks marked
   gate_human: true without human review.

This is a read-and-report run. Changes to roadmaps are the ONLY writes permitted.
```

---

## Scope of Reads

- `/home/user/conductor/projects/*/roadmap.yaml` — authoritative task list
- `/home/user/kind_robots/server/api/**/*.ts` — API routes
- `/home/user/kind_robots/stores/**/*.ts` — Pinia stores
- `/home/user/kind_robots/components/**/*.vue` — Vue components
- `/home/user/kind_robots/prisma/schema.prisma` — DB schema
- `/home/user/kind_robots/pages/**/*.vue` — page routes

---

## Output

- **Audit report:** `projects/global-ui/AUDIT-REPORT-<YYYY-MM-DD>.md`
- **New tasks:** up to 3 added to relevant `roadmap.yaml` files as `status: ready`
- **PR:** one PR per run, title `audit(site): weekly gap report YYYY-MM-DD`

---

## Boundaries (hard)

- No live HTTP requests to kind-robots.vercel.app
- No changes to `main` branch directly
- No writing to roadmaps marked `gate_human: true` without approval
- No deleting existing tasks or roadmap entries
- No running npm/pnpm builds
- No pushing directly — open a PR like any other worker task

---

## Setup Instructions (for Silas to activate)

1. Create a Claude Code Remote cron trigger with:
   - `cron_expression: "0 9 * * 1"` (Mondays 09:00 UTC)
   - `prompt:` the agent prompt above
   - `create_new_session_on_fire: true`
   - `notifications: { push: true }`
2. The trigger fires into a fresh session each Monday.
3. Review the generated PR and audit report before merging.

This trigger is defined here as a spec. Silas approves activation.
