# Pitch: Per-cycle cost + run-budget guard for AI_Networker
date: 2026-06-24
project-target: ai-networker-itself
status: passed

## The idea
A small check the Worker runs each cycle that tracks how many agent runs/PRs happened
today and pauses new work (writing a notice to STATUS.md) if a daily budget is hit —
protecting against the Pro-tier 5-routine/day limit and runaway API spend.

## Why it's worth doing
Right now nothing stops the loop from burning the daily Claude routine budget or stacking
PRs faster than Silas can review. A cheap guard makes unattended running genuinely safe.

## Rough effort
small

## Suggested first task
Add scripts/budget_guard.py + a budget setting in CONTROL.md; Worker calls it before claiming.
