# Pocket Pet Robot — Design Brief

date: 2026-10-02
status: approved (Silas, 2026-10-02: "I like all proposals"); detailed spec is the first task
author: claude

## What it is

A tiny virtual pet you adopt, name, feed, play with and put to bed, whose mood sprites and room scenes are all pre-generated and whose state lives in your own browser. It grows through three forms over a couple of weeks of casual visits and never needs a server or a token.

Origin: the 2026-10-02 daily pitch docket (`pitches/daily/2026-10-02.yaml`), approved by Silas.

## Why it exists

Much of Kind Robots is locked behind LLM API access. This is **free to play**: no LLM at runtime, no account required. Authoring tokens and image generation are plentiful, so everything that needs words or art is made ahead of time by sessions and shipped as static content.

## Effort and first slice

Effort: medium. First slice: The needs and decay model as a pure tested engine, then a one-room page with placeholder sprites.

## Art plan

3 forms x 8 mood sprites and 6 room backdrops, generated for sprite-sheet consistency.

## Shape

- Home is kind_robots at `/play/pocket-pet`, with a Pinia store that owns all state; components never call APIs.
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
