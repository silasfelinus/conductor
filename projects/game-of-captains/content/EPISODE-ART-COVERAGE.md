# Space Couch episode art coverage contract

Updated 2026-11-01 PT. The playable route is `/play/game-of-captains`. All requested image generation is internal (`is_public: false`), not an external launch. **A request, ArtJob ID, DONE render and player-visible image are four different milestones.**

## Canonical stages

For every distinct episode card, the player needs:
1. A **reveal** plate showing the specific dilemma before choices, not merely the generic couch backdrop.
2. Three choice paths: `ask`, `document` and `override`.
3. **Two result illustrations per choice**, one for a success and one for a complication, with separate prompts reflecting *actual authored* prose. Failed options cannot reuse triumph art.
4. A valid access-filtered ArtImage URL to be wired by key when the renderer finishes, a working fallback while queued or blocked, and a mobile/desktop crop inspection.
5. The ending epilogue must use art for the *earned* ending, including refusal and bad outcomes, not a random generic happy ending.

Asset key contract for the planet tranche is `episode/<episodeCard.id>-reveal` and `episode/<episodeCard.id>-<ask|document|override>-<success|failure>`. These keys exactly match Kind Robots `episodeArtwork.ts` and `PLANET-CHOICE-OUTCOMES-ROUND-1.yaml`. It is an identity-preserving slot contract, not a claim that these URLs exist today.

## Inventory and submission order

| Episode family | Authored card/beat units | Expected image slots (7 per unit) | State |
| --- | ---: | ---: | --- |
| Planet civic dilemmas | 10 | 70 | **New internal Krea 2 requests in PLANET-CHOICE-OUTCOMES-ROUND-1**, auto-submit, no render proof yet |
| Occupied casino incident archetypes | 8 | 56 | Not submitted; use actual incident/outcome text, include giant's ownership and consent |
| Serendipity franchises | 20 × 3 authored venue beats | 420 | Not submitted for branches; 20 existing venue establishment plates are DONE and separate |
| Constellation quests | 12 signs × 3 quests | 252 | Not submitted; unique sign visuals with meaningful success/failure |
| Nemesis guest-star chapters | 8 antagonists × 4 even chapters | 224 | Not submitted; same enemy design, unique beat/choice outcome |
| **Total full episode decision target** | **146 units** | **1,022** | **70 newly queued, 952 still to author/queue** |

This inventory counts choice-driven *episode decks* only. It excludes expedition quest-card reveal/outcomes, the 220 trio adventures (1,100 separate plates), character portraits and expression plates, finale coda variants, onboarding tests and pocket rooms. Their totals must remain independently inspectable.

### Existing trio production, no duplicate requests

All 1,100 `PARTY-ADVENTURES-ROUND-1` step/ending slots have been assigned ArtJob IDs already. Previous reconciliation recorded 798 DONE across 161 combinations and 302 pending/running slots. `kind_robots` PR #4585 merged authorized lazy delivery for the completed set. The existing requests must continue draining; never submit the same `asset` twice to inflate progress.

## Remaining agent-owned art and acceptance checklist

- Reconcile actual job status for the new 70 slots after the auto-submit workflow; then attach the returned ArtImage IDs to the authorized Space Couch route. A new `auto_submit: true` YAML on main triggers the existing Auto Art Generate workflow, but does not itself prove the render box accepted a job.
- Author and queue the other 952 episode-deck slots using source-specific visual prompts. Break into smaller round ledgers, preserve stable keys, actual failures and the red couch/transparent protective bubble.
- Expand Act II and III expedition encounter pools so the same 17 galactic quest jokes no longer fill most late boards. **Do not change pinned seeded ending outcomes while reducing repetition**; test the existing ending and save suite.
- Run a final independent narrative, ethics, comic-pacing and balance review only after the new choices are playable and art is visually verified. Specifically audit crew agency, non-intervention consequences, casualty dignity, late-run trust inflation and whether different orders matter.
- Verify actual signed-in phone/tablet/desktop screenshots and paint continuity before offering Silas final subjective acceptance. Keep that separate from any public-release authorization.
