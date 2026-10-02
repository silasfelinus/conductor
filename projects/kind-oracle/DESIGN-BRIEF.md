# Kind Oracle — Design Brief

date: 2026-10-02
status: approved by Silas 2026-10-02, widened to a full 78-card tarot deck; detailed spec is the first task
author: claude

## What it is

A full 78-card Kind Robots tarot deck (22 major arcana plus 56 minor arcana in four suits), each card a full piece of art with an upright and a reversed meaning, where you draw a one, three or five card spread and read a pre-written reading assembled from hand-authored card, pair and position texts. Every combination is written ahead of time, so it feels personal and costs nothing to run. The 22 major arcana ship first as a complete, playable oracle; the minor arcana follow in suit-sized slices.

Origin: the 2026-10-02 daily pitch docket (`pitches/daily/2026-10-02.yaml`), approved and widened by Silas.

## Why it exists

Much of Kind Robots is locked behind LLM API access. This is **free to play**: no LLM at runtime, no account required. Authoring tokens and image generation are plentiful, so everything that needs words or art is made ahead of time by sessions and shipped as static content.

## Effort and first slice

Effort: medium. First slice: Write the 22 major arcana meanings and the 3-card position grammar, then a draw page with flip animation.

## Art plan

78 card faces (22 majors first, then the minor suits) plus a back through ArtJobs under one style bible; spread layouts composed in code.

## Shape

- Home is kind_robots at `/play/oracle`, with a Pinia store that owns all state; components never call APIs.
- Rules and content logic are pure code in `utils/` with DB-free tsx tests and a contract-tests step.
- Static content and art live under `public/` with manifests carrying prompt and model metadata.
- Browser storage is per-viewer convenience only: wrap every access in try/catch and render correctly without it.
- Responsive at 375, 768 and 1280, reduced-motion safe, keyboard operable.

## Out of scope / guardrails

- No LLM or generation call in the player path; no accounts; no payments; no publishing or deploy steps.
- Art follows the Krea 2 prompt contract in ART-PROMPTS.md (concrete nouns first, no negations); keep prompt and model metadata.
- All-ages content; additive migrations only, and none are expected.

## Open questions (none block development)

Resolved by the first task's spec; Silas can redirect any agent pick with a one-line edit.
