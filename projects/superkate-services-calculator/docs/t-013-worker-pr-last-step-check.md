# Worker PR Last-Step Check

Date: 2026-07-06  
Task: `superkate-services-calculator/t-013`  
Status: process note for Worker flow

## Purpose

This note preserves the process improvement requested by the Superkate Services Calculator kaizen task: when a Worker pushes a task branch, it must open the corresponding pull request before ending the work cycle.

The task was created after prior Worker branches were left stranded after implementation. A pushed branch without a PR is invisible to the normal Reviewer flow and can make completed work look lost even when the branch contains valid changes.

## Last-step check

Before ending any software task cycle after pushing a `worker/*` branch, the Worker must verify all of the following:

1. A pull request exists from the task branch into `main`.
2. The PR body uses the handoff template from `AGENTS.md`.
3. The conductor roadmap status has been advanced appropriately on the task branch:
   - `review` for normal reversible software work.
   - `needs-human` for hard-gated, outward-facing, irreversible, content, proposal, or blocked fallback work.
4. If the PR cannot be opened, the Worker leaves a visible fallback artifact in conductor explaining exactly what was produced, what branch or target repo was blocked, and what Silas or the next Worker should do.

## Intended AGENTS.md insertion

The canonical Worker section in `AGENTS.md` should include this sentence after the branch instruction:

> Before ending any cycle that pushed a `worker/*` task branch, confirm that a PR from that branch into `main` exists, even when merging is deferred.

## Verification possible in this connector run

- Confirmed `AGENTS.md` already requires Worker task branches and PR handoffs.
- Confirmed the kaizen task is scoped to preventing stranded branches.
- Created this process note on the task branch so the rule is visible and reviewable.

## Verification still needed

A future full-repo edit should place the intended sentence directly in `AGENTS.md`. The GitHub connector can replace whole files, but this run could not safely apply a small patch to the middle of `AGENTS.md` without risking accidental overwrite of the full operating manual. Tiny goblin, very sharp teeth.
