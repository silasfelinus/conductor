# Slime City: player handoff checklist (t-012)

Started 2026-11-19 PT, closed 2026-11-19 PT. This is an agent-owned QA ledger. It is **not** a
playtest verdict (t-009, t-014) or publish authorization (t-015). A row is done only when its
evidence is merged on `kind_robots` main and was rechecked. The tester-facing handoff is
[PLAYTEST-HANDOFF-2026-11-19.md](PLAYTEST-HANDOFF-2026-11-19.md).

Legend: ✅ evidence on main or measured on production · 🧍 needs a person

## Story and campaign routes

| Check | State | Evidence |
| --- | --- | --- |
| Every crew × every one of the 32 choice paths finishes through the real engine, with multiple seeds and retry after loss | ✅ | `verifySlimeCityFullRoutes.test.ts`: 576 routes, 4,088 engine fights |
| Defeats and draws never advance the story or record decisions; stale, wrong-rival and post-finale results are ignored | ✅ | Same test |
| Both endings (triumph or compromise) are reachable for every crew | ✅ | Same test |
| Earned favour → story echo → crew legacy transitions | ✅ | Same test, plus `verifySlimeCityCampaignPlaytest.test.ts` |
| Per-crew journey scene branches (left/right) | ✅ | `verifySlimeCity*Journey.test.ts` (six crews and alliance) |
| Story save and restore, device and account | ✅ | `verifySlimeCityStorySave.test.ts`, `verifySlimeCityGuestStory.test.ts` |
| A device journey can move into a fresh account story, without the Tower legacy | ✅ | `verifySlimeCityGuestImport.test.ts` (kind_robots#5379), plus a real-browser run on a local build |
| A Journey chapter in a real browser on production: three decisions, approach, fight, defeat, TRY AGAIN | ✅ | 2026-11-19 PT, signed-in test user on production |

## Cards and balance

| Check | State | Evidence |
| --- | --- | --- |
| CLASH 300 L1/L2/L3 evolution coverage | ✅ | t-041 done. 230 crafted journeys through the engine at every level; 0 duplicate journeys; every one of the 300 cards played by the CPU in seeded QA (kind_robots#5379). `CARD-REDESIGN-300.md` records the evidence and what it leaves open |
| Constructed-deck balance across crews | ✅ | `verifySlimeCityClashConstructed.test.ts` on main `5b715a7`: 3,120 bouts over 30 legal decks, crews 43.4–55.1% (Riot lowest), first seat 52.4%, 0 dead cards on suite and held-out seeds. The worst crew pairing stays above the 30% target (asserted in `verifySlimeCityClash.test.ts`). The spell-heavy probe deck wins 26.7%, above its 25% ratchet floor |
| Resource exploits (double claims, pack duplication, wallet races) | ✅ | `verifySlimeCityStore.test.ts`, `verifySlimeCityAccountBoundary.test.ts`, `verifySlimeCityProgression.test.ts` |

Reported, not gated: the CPU picks six two-slot cards in under 3% of bouts, and plays 237 of the
300 cards at level three. Both are in the tester handoff.

## Multiplayer and accounts

| Check | State | Evidence |
| --- | --- | --- |
| Reconnect, stale tab, forfeit and expiry | ✅ | `verifySlimeCityPvp.test.ts`, `verifySlimeCityPvpReconnect.test.ts` (in-memory database), and on production 2026-11-19 PT: a real duel between two test accounts, 18 of 18 checks, including a refused stale move, reload onto the same board and idempotent forfeit. Idle expiry is covered by the unit test only |
| Account security and hidden-information redaction | ✅ | t-011 done; the production duel confirmed a signed-out visitor gets 401, a third account cannot join or read the board, a client-supplied seat is rejected, and each seat sees only a count of the rival's hand |

## Experience, art and layout

| Check | State | Evidence |
| --- | --- | --- |
| Keyboard and touch play a full match | ✅ | `npm run audit:slime-city-clash-input`, signed in on production: keyboard-only (Tab/Enter) and touch-only (Pixel 7) matches both finish, on builds `bf47039`, `16fd717`, `5b715a7` and `db5d615` |
| Gamepad | ✅ 🧍 | Bound in kind_robots#5336 and unit-tested (`verifySlimeCityClashGamepad.test.ts`). No physical controller has been tried |
| Clash layout in a real browser | ✅ | `npm run audit:slime-city-clash-layout`, signed in on production build `db5d615`: 21 of 21 cases. In-play controls at 390/768/1440 with and without TAP; a held card at each width; the rail at 1440×780, 1366×768 and 1280×720; result controls in both result states. Eight of these failed on `bf47039` and were fixed in kind_robots#5376. The UNDO label squeezed beside TAP was fixed in kind_robots#5380; the audit now fails any control narrower than its label, and passes on `db5d615` |
| Rendered 390 / 768 / 1440 / XL layouts | ✅ | Production build `16fd717`: title screen at 390/768/1440/2560 with the title inside its column (2560: 1286 of 1300px, the #5332 fix), no overflow or broken images. All five tabs at 390 and 1440: no console errors, broken images or page scroll |
| Real delivered ArtImages in every slot | ✅ | `npm run audit:slime-city-art-delivery` against production as a signed-in non-admin: 1,485 of 1,485 manifest slots return an image. `verifySlimeCityArtCoverage.test.ts`: 300/300 base cards, 300/300 with L2 and L3 paintings, every ArtImage id unique |
| Tutorial describes the game that ships | ✅ | kind_robots#5379: the Play tutorial no longer teaches BLACKOUT or offers MEATBALL |

## Human-owned, outside this checklist

- t-009 / t-014: subjective fun verdict and acceptance (Silas).
- t-015: public Play launch authorization (Silas).
- A physical gamepad.
- Optional: a non-admin audit account as the `KR_AUDIT_USERNAME` / `KR_AUDIT_PASSWORD` secrets, so the daily layout audit covers Slime City.
