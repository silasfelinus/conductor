# Slime City: the non-art finish line

**Human direction, November 1, 2026 PT:** Keep writing, gameplay, backend, testing, and UI development moving **regardless of the art queue**. Stop treating queued illustrations as blocking software. The only permitted art-only remaining work at the non-art handoff is rendering and placing illustrations that have already been **durably submitted** to the queue. Draft prompts and a ledger with `auto_submit: true` do **not** count as submitted until ArtJob IDs are recorded. Delivered art must still be verified independently.

The Slime City design is BLACKOUT-first: visible monsters on a 10×6 grid with orthogonal movement, fair four-card hands, explicit attack and summon delay. BLOODRUSH remains a secondary play mode with intelligible deaths; MEATBALL remains an internal experiment. Do not re-open format indecision as a coding blocker. Keep public Play publication and optional creative acceptance separate human gates.

## Completion tracks

### Non-art: developer-owned, must be complete

- **Story:** All six crew campaigns have five unique rival conflicts each, authored choices with different tactical setups, distinct success/failure consequences, coherent short prologues, earned epilogues, repeatable battles, and actual result-to-story transitions. Include district street decisions, championship aftermaths, civic crises, and Grand Pit resolutions. Ensure all chapters and endings are reachable and work from saved state. No generic filler for a unique outcome.
- **Cards:** All 60 starter cards are fully implemented and inspected in the UI; all proposed 50 additional cards per crew (300 Gutter Crown cards) must receive actual unique names, costs, stats/effects, ability text, rarity, playable legality and faction counterplay, not merely a numerical allocation or undeployed art prompt. The starter and expansion pools must not violate guaranteed rare/owned-only pack constraints. All named attack types must be actionable even with temporary artwork.
- **Game systems:** CPU tactics, seeded replays, manual attack feedback, frame-by-frame Bloodrush cause-of-death explanations, meaningful encounter and district routing, a finished deck builder, and nonduplicating collectible pack economy. Do not substitute design prose for a usable control.
- **Account ownership:** Wallet, XP, cards, claims, saved campaign/city progression and match receipts are account-backed, never browser-local authoritative balances. Validate payloads, double settlements, cross-tab concurrency, claims, timezone resets, and stale/forged results. Server-authoritative multiplayer/friend challenges must preserve private information, legal turns, and reconnects without exposing public matchmaking.
- **Experience and accessibility:** Full-screen console layout with keyboard, touch, reduced-motion and accessible combat log; first-run explanation of BLACKOUT and every unique mechanic; no dead buttons, user-visible error/retry affordances, responsive 390/768/1440/XL checks and real browser-play interaction after deployment.
- **Quality evidence:** Complete seeded adversarial suite for each crew and encounter family, both campaign endings, every mission, saving/restoring progress, wallet and pack race conditions, all battle variants and accessibility. Keep release acceptance strictly separate from internal testing. Merge clean source PRs only once latest-head checks pass.

### Art: independently queued/rendered/placed

- Maintain a stable manifest mapping each required image slot to a unique job/asset/path. Pending artwork always occupies an image-shaped slot. The story and mechanics remain fully playable using fallbacks.
- Round 1 currently reports 52 DONE ArtImage IDs. Round 2 contains 168 additional **authored** requests (24 starter cards, 6 prologues, 30 chapter openings, 60 unique choice-result scenes, 30 defeat scenes, 12 endings and 6 attack icons). Neither ledger inclusion nor a successful GitHub CI run establishes ArtJob acceptance or delivered media.
- On the art track, reconcile/reuse existing ArtJob IDs first, then confirm real queue receipts. Later attach completed ArtImages and verify actual bytes/URLs. The generator backlog must not gate any of the non-art items above.

## Honest status at this directive

- Implemented before this directive: six starter decks (60 cards), six five-chapter campaigns with 120 authored choice-specific victory/loss paragraphs, city street/gate/aftermath/crisis/finale systems, starter CPU, and database-backed XP/Meat/rare-guaranteed packs and daily/weekly claims. The Gutter Crown 300-card set is **a proposal**, not an implemented card set.
- Current session adds account story saving in kind_robots PR #4596; passing CI and merge are prerequisites to calling that implementation complete.
- T-004's lingering `review` state and waiting dependencies t-005/t-006/t-008/t-009/t-010/t-011/t-012 need active resolution, not passive stalling on t-017 art. T-013 is optional creative input and not a release prerequisite; t-014 subjective acceptance and t-015 public launch authorization remain real human gates.

**Release-candidate rule:** A non-art candidate is not ready merely because prompts are queued. It is ready when the above authored/mechanical/testing work is finished and every needed art slot has a submitted receipt. Generated art may still be rendering in parallel, and its eventual placement should not reopen unrelated engineering scope.
