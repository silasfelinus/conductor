# Pitch: Worker Cycle-Time Dashboard in PR-TRIAGE.md

date: 2026-06-30
project-target: conductor
status: awaiting-silas

## The idea

Extend `scripts/build_pr_triage.py` to compute and display how long each active task has been in its current status. A fourth table in PR-TRIAGE.md shows: task id, project, time-in-status (days), and a "slow lane" flag if a task has been in `claimed` or `review` for more than 5 days without a PR. This gives Silas a quick read on where the loop is stalling — over-scoped tasks, orphaned claims, or tasks where Worker ran out of context and quietly stopped.

## Why it's worth doing

Right now PR-TRIAGE.md shows a snapshot but not velocity. Adding time-in-status turns the triage board into a true health dashboard: one glance tells you if a task is flowing, stalled, or forgotten. The data is already in the roadmap YAML (`updated:` timestamps); it just needs to be surfaced. No new infrastructure needed.

## Rough effort

small

## Suggested first task

Add a `slow_tasks()` function to `build_pr_triage.py` that computes `days_since_update` for each in-flight task, appends a "Slow Lane" table to PR-TRIAGE.md for any task > 5 days without movement, and includes a configurable threshold flag.
