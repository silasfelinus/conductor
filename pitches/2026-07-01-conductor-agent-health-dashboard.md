# Pitch: Conductor Agent Health Dashboard
date: 2026-07-01
project-target: ai-networker-itself
status: awaiting-silas

## The idea
A lightweight, local-first web dashboard (single HTML file or minimal Node server) that reads the conductor's existing roadmap YAML files, git log, and PR status to display a live view of: which tasks are in-flight, which agents are blocked, cumulative token/cost spend per project (pulling from any logged cost data), and a timeline of recent PR merges. No new backend — it reads the filesystem and calls the GitHub API directly from the browser using a personal access token stored in localStorage.

## Why it's worth doing
Right now, knowing what the conductor system is doing requires Silas to manually grep roadmap files and check GitHub. A dashboard removes that friction and makes the multi-agent system feel like a real product rather than a collection of YAML files. It also surfaces cost anomalies early, complementing the existing networker-cost-guard pitch (which was already approved). This can be built purely in the conductor repo and deployed as a GitHub Pages artifact with no ongoing hosting cost.

## Rough effort
medium

## Suggested first task
Scaffold a single `dashboard/index.html` that reads all `projects/*/roadmap.yaml` files via a local file-server (or fetches them from the GitHub raw API) and renders a task status board — columns: ready, claimed, review, needs-human, done — using vanilla JS and minimal CSS.
