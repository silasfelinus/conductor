# Pitch: AI Session Credits Subscription
date: 2026-07-01
project-target: new
status: awaiting-silas

## The idea
A lightweight recurring subscription service (monthly tiers: Spark $9/mo, Builder $29/mo, Studio $79/mo) where subscribers purchase a monthly allotment of "AI session credits" — pre-paid blocks of time or task runs powered by the conductor/kind_robots infrastructure. Subscribers submit creative or coding tasks (story outlines, code scaffolds, character sheets, prompt-deck customizations) via a simple web form; a conductor Worker agent handles the task and delivers output by email or a private dashboard link. Positioning: "your personal AI collaborator, on retainer."

## Why it's worth doing
One-off digital product sales have high variance; a subscription creates predictable monthly recurring revenue that compounds. Silas already has the conductor agent infrastructure — this monetizes it directly rather than building new tooling. Starting with a small cohort (5-10 subscribers at Spark tier) validates demand with near-zero additional cost, and the Builder/Studio tiers create natural upsell paths. All publishing and subscriber communication is gated on Silas, so no autonomous outbound happens without approval.

## Rough effort
large

## Suggested first task
Write the service definition doc (tiers, credit amounts, what task types are in scope, SLA for turnaround) and design the intake form schema (task type, description, output format, subscriber tier) — no code yet. This doc becomes the source of truth for the landing page and conductor task routing rules.
