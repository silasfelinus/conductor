# Kind Word Puzzles — Design Brief

date: 2026-10-02
status: approved (Silas, 2026-10-02: "I like all proposals"); detailed spec is the first task
author: claude

## What it is

A year of pre-authored word searches and mini crosswords built from the Kind Robots lexicon of characters, rewards, places and scenarios, one per day with the date picking the puzzle. Sessions write and validate every grid ahead of time, so the daily puzzle is free for everyone.

Origin: the 2026-10-02 daily pitch docket (`pitches/daily/2026-10-02.yaml`), approved by Silas.

## Why it exists

Much of Kind Robots is locked behind LLM API access. This is **free to play**: no LLM at runtime, no account required. Authoring tokens and image generation are plentiful, so everything that needs words or art is made ahead of time by sessions and shipped as static content.

## Effort and first slice

Effort: small. First slice: A grid generator with a solvability validator, 14 puzzles, and a daily puzzle page.

## Art plan

A small header illustration per puzzle theme, about 30 in total, reusing existing gallery art where it fits.

## Shape

- Home is kind_robots at `/play/word-puzzles`, with a Pinia store that owns all state; components never call APIs.
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
