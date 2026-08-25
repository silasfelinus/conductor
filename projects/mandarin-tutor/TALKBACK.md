# Mandarin Tutor — TALKBACK

## 2026-08-24 — project intake

Silas requested a visual Mandarin tutor built around the part he finds most useful in existing tools: seeing how characters are constructed and what those components contribute. The project also requires image-backed flashcards, requested-word creation, custom and curated study sets, 500+ initial cards, Krea 2 illustration requests, pronunciation guides and audio for every lexical card, broad beginner categories, a dedicated casino/gambling set, future official-test alignment, and eventual iOS/Android expansion.

Initial design decision: keep lexical facts, learner state, and generated media as separate layers. Character explanations explicitly distinguish semantic, phonetic, indexing/radical, and uncertain components so the tutor does not turn memorable folk etymology into asserted history.

## 2026-08-25 — Reviewer pass on t-001 (kind_robots PR #2083)

Worker's first pass at the MVP (route, catalog normalization, study sets, curated
sets, per-card art enqueue) is scoped well and the diff itself reads cleanly —
provenance metadata preserved, boundaries for t-003/t-004/t-005 called out
explicitly rather than silently expanded into. Not a design/scope rejection.

Two real, non-flaky CI failures held it back: `test:fetch-generic-pinning` caught
an unpinned `$fetch<SourceEntry[]>(...)` call in `server/utils/mandarinCatalog.ts`
(needs the second generic to pin the request type), and `vue-tsc` (`npm run test`)
exited 2 with diagnostics only in an uploaded artifact, not CI stdout. Left a
specific review comment with the exact fix and sent `t-001` back to `ready` with
`retry_context` (conductor PR #2827) rather than leaving the PR to rot or
re-implementing it myself.

Worker note for next pass: when a repo-specific lint contract like
fetch-generic-pinning exists, it's worth a self-check before opening the PR —
`grep -n '\$fetch<' <changed files>` for any call missing the second generic
would have caught this locally in seconds instead of costing a CI round-trip.
