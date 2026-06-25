# Conductor

Conductor is a service-agnostic autonomous multi-agent project coordination system built by Silas Felinus.

## What it does

Conductor tracks a portfolio of projects in a structured Git repo. AI agents (a Worker and a Reviewer) coordinate work autonomously across those projects, cycling through tasks, opening PRs, reviewing them, and escalating when human judgment is needed — without requiring Silas to babysit individual cycles.

## How it works

- **Projects** live in `projects/<name>/` each with a `roadmap.yaml` (milestones + tasks) and `CHANGELOG.md`.
- **Agents** read `AGENTS.md` (the operating manual) and `CONTROL.md` (Silas's current steering instructions) before every session.
- **The Worker** (OpenAI, hourly) claims tasks, does the work, opens PRs.
- **The Reviewer** (Claude, event-triggered) reviews PRs, merges safe ones, escalates the rest.
- **Pitches** land in `pitches/` awaiting Silas's vote before any work proceeds on proposal-kind projects.
- **Status** is rendered into `STATUS.md` (auto-generated, read-only) and `workspace.html` (visual dashboard).

## Project kinds

| Kind | What "done" means |
|---|---|
| `software` | A merged PR |
| `content` | A draft file, human-approved before publish |
| `proposal` | A pitch file in `pitches/`, awaiting Silas |

## Repos tracked

See `repos.yaml` for the full list of external repos Conductor coordinates.

## Key files

| File | Purpose |
|---|---|
| `AGENTS.md` | Full agent operating manual — read first |
| `CONTROL.md` | Silas's live steering sheet — read before roadmaps |
| `STATUS.md` | Auto-generated project status snapshot (read-only) |
| `repos.yaml` | External repos mapped to project slugs |
| `workspace.html` | Visual dashboard (auto-generated) |
