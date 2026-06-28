# Pitch: Add a CI build/lint gate for software projects
date: 2026-06-24
project-target: ai-networker-itself
status: approved

## The idea
Add a lightweight GitHub Actions CI check (lint + build) that runs on every worker/* PR,
so the Reviewer has a green-checks signal to merge against instead of judging by eye.

## Why it's worth doing
Gives the autonomous merge step an objective gate, cuts the chance of a broken merge,
and makes branch protection's "require status checks" actually meaningful.

## Rough effort
small

## Suggested first task
Add .github/workflows/ci.yml that installs deps and runs lint+build per project kind,
and update branch protection to require it.
