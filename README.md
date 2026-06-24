# AI_Networker

A service-agnostic integration spot for AI agents to coordinate projects
collaboratively, with or without human intervention.

## How it works
- **Worker** (OpenAI, hourly): runs scripts/resolve_deps.py, then reads AGENTS.md +
  roadmaps, claims the top `ready` task, does it on a `worker/*` branch, opens a PR.
- **Reviewer** (Claude Code Routine, on `worker/*` PR opened): merges reversible software
  PRs; escalates content/proposal/gated/outward-facing work to `needs-human`.
- **Digest** (daily): emails Silas progress %, what merged, what needs attention, and
  pitches awaiting his vote.

## Project kinds
- **software** — output is a merged PR
- **content** — drafts/deliverables, never auto-published (always needs-human)
- **proposal** — the work is a pitch to `pitches/` for Silas to vet

## Pipelines & human gates
Tasks can declare `depends_on` and stay `status: waiting` until upstreams are done.
A task with `gate_human: true` blocks its dependents until Silas sets
`approved_by_human: true`. The Worker runs `resolve_deps.py` each cycle to auto-unblock
satisfied tasks. This is how staged flows work: research → (Silas picks) → create →
market → advertise, each stage gated.

## Layout
```
AGENTS.md                       # operating manual (CLAUDE.md points here)
projects/<name>/roadmap.yaml    # one queue per project; Silas steers here
projects/<name>/product-types.yaml   # (storefront) Silas-owned vocabulary
projects/priority.yaml          # which project leads
pitches/                        # proposal agents drop ideas for vetting
scripts/build_digest.py         # progress + pitches + summary
scripts/resolve_deps.py         # unblocks pipeline tasks
.github/workflows/daily-digest.yml
docs/SETUP.md
```

## Projects
- **humboldt-scoop** — existing site (add codebase under /site). software.
- **humboldt-poop-scoop-cms** — new customer-management software. software.
- **digital-storefront** — research→create→market→advertise pipeline. content. Builds
  only within product-types.yaml (Silas owns that list); nothing publishes/spends unattended.
- **approval-portal** — the console Silas lives in: pick pitches, validate upgrades,
  confirm updates, roll back. A face over the repo (git = source of truth). software.
- **kind-robots** — app(s) owning their logic, consuming the shared KR backend (read-only).
  Full roadmap TBD; see BOUNDARY note. software.

## Steering (Silas)
Edit `notes_from_silas` and tasks in any roadmap; set pitch `status:` to approved/rejected;
approve a gated task with `approved_by_human: true` + `status: done` to unblock its
pipeline. Everything routes through PRs; rollback = git revert.
