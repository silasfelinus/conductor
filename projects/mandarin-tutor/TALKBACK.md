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

## 2026-08-28 — submitting the corpus, and why it could never have been submitted

Silas asked for the art to be submitted, for a consistent style that avoids AI-sameness,
and for a better-looking page with a colorful thematic banner. The submission part turned
out to be blocked twice over, neither blocker being the Alexandria container update this
project had been waiting on since 2026-08-25 (production has served the v2 manifest since
before this session).

**All 577 enqueues returned HTTP 422.** `artPromptContract` rejects conditional
instructions, and the v2 recipe hedged the way a person writes: "ground it in Chinese
detail *only when* it naturally belongs to the concept". Krea 2 cannot evaluate a
condition. The corpus was unsubmittable from the day the recipe was written, and nobody
had found out because nothing had ever tried to submit it at scale. The recipe and the
gate that guards the enqueue boundary were each tested, but never against each other —
`verifyMandarinArtRecipe.test.ts` now closes that, card by card and per category.

Two more of the same family were in there under the 422's threshold and worth fixing while
the recipe was open: "flashcard illustration" (the contract's format rule was learned from
"treasure card illustration", which rendered literal trading cards with rules boxes), and
fourteen ways of saying "no text" plus "lens flare, bokeh, neon glow" — all landing in
*positive* conditioning at cfg 1, where the ComfyUI negative prompt is inert.

**The tutor's probe reported every unrendered card as ready.** `probeCanonicalIllustration`
trusted `response.ok`, but a missing `/images/...` path is not a 404: Nuxt falls through to
the catch-all page and answers 200 `text/html`. So every card flipped to V2 READY, painted
a broken `<img>` over the Hanzi fallback, and hid the "Request illustration" button that
would have fixed it. That also fed a third-order bug: the broken images reported themselves
to `/api/conductor/art-request`, which cheerfully wrote generic prompts aimed at canonical
v2 card paths — one of them asking for readable 谢谢 and "digital painting blending
illustration and realism". Rendering that would have satisfied the canonical path with the
wrong picture, permanently. The endpoint now refuses that media root.

**On AI-sameness specifically.** The recipe was the cause, not the model. Every card got
the same style sentences, so any two prompts were ~82% identical and 38 pairs were
byte-identical. Fixed by keeping the house style fixed and drawing framing, light, palette,
paint handling, and ground per card from its stable token — 3600 combinations, 537 distinct
draws across 577 cards, all 577 prompts now unique. Deterministic, so a retry reproduces
what was submitted rather than silently restyling the card.

**Reviewer note for whoever picks this up next.** The pattern across all four bugs is the
same: something reported success it had not earned. A 200 that was an HTML error page. A
manifest that was correct but unsubmittable. A closed task whose "coverage" was never
measured. Before calling this project's art done, check media exists with an `image/*`
content type — `curl -I` and read the type, not the status.

**Not done, and not ours.** Alexandria's ComfyUI has lost sight of its model directory and
has rendered nothing since 2026-08-27T09:04Z; the 577 jobs are draining into that failure.
Filed as t-019. It is not Mandarin-specific — it burns every job the box is handed.
