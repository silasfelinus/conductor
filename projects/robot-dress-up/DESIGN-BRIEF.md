# Robot Dress-Up Workshop — Design Brief

date: 2026-10-02
status: approved (Silas, 2026-10-02: "I like all proposals"); detailed spec is the first task
author: claude

## What it is

A paper-doll workshop where you pick a robot body and layer on pre-generated hats, arms, antennae, paint jobs and accessories, save the result to your device and download it as a sticker. Pure client-side layering, with parts that snap to anchor points so nothing needs generation.

Origin: the 2026-10-02 daily pitch docket (`pitches/daily/2026-10-02.yaml`), approved by Silas.

## Why it exists

Much of Kind Robots is locked behind LLM API access. This is **free to play**: no LLM at runtime, no account required. Authoring tokens and image generation are plentiful, so everything that needs words or art is made ahead of time by sessions and shipped as static content.

## Effort and first slice

Effort: medium. First slice: Anchor-grid spec, 1 body with 10 parts, and the layering canvas with PNG export.

## Art plan

6 bodies and about 80 transparent parts on matching anchor grids, generated and cleaned in batches.

## Shape

- Home is kind_robots at `/play/dress-up`, with a Pinia store that owns all state; components never call APIs.
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
